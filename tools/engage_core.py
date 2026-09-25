#!/usr/bin/env python3
"""
engage_core.py - repository discovery, policy and state classification for `engage`.

OBJ-026. This module is deliberately **pure**: it reads git state and decides what *would* be
safe to do. It never pulls, never writes a file, and never prints. `engage.py` owns every side
effect and all rendering. The split exists so the decision table below can be exercised against
fabricated repositories without a network, a schedule, or a real workspace.

Why a decision table at all
---------------------------
"Pull if behind" is wrong in six different ways: behind *and* dirty, behind *and* ahead,
mid-rebase, detached, no upstream, no remote. Each needs a different answer, and one of them
(diverged) must never be answered by a machine. Writing them as an ordered table rather than as
nested ifs is what makes them reviewable and testable.

Safety
------
`FORBIDDEN` is imported from `obj016_daily_refresh` rather than restated, so this workspace has
exactly one list of banned git subcommands. This module adds read-only verbs to the allowed set
and asserts at import time that it has not accidentally re-permitted a banned one.
"""
from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from obj016_daily_refresh import FORBIDDEN  # noqa: E402  the single source of truth for bans

from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)

# Read-only verbs, plus the two state-changing ones `engage` is permitted: `fetch` (touches only
# remote-tracking refs) and `pull --ff-only` (enforced in run_git; refuses on a dirty tree and
# cannot create a merge commit).
ALLOWED = {
    "status", "rev-parse", "rev-list", "log", "diff", "show", "fetch", "pull",
    "stash", "config", "remote", "for-each-ref", "ls-files", "symbolic-ref", "count-objects",
}
assert not (ALLOWED & FORBIDDEN), f"engage re-permitted a banned subcommand: {ALLOWED & FORBIDDEN}"

# Directories never worth descending into when hunting for repositories. `node_modules` alone is
# 105 MB of two byte-identical trees here, and vendored packages carry their own .git.
SKIP_DIRS = {
    "node_modules", "target", "dist", "build", "__pycache__", ".venv", "venv",
    ".vite", ".pytest_cache", ".idea", ".vs", "coverage", ".gradle", "bin", "obj",
}
MAX_DEPTH = 3


# ---------------------------------------------------------------------------------------------
# policy - who may be pulled, who may be pushed, and what happens to a repo nobody classified
# ---------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Policy:
    name: str
    pull: str          # "ff-only" | "none"
    push: bool         # may this repo be pushed at all?
    note: str
    push_auto: bool = False   # may a push happen WITHOUT an explicit per-push instruction?


# Keyed by path relative to the workspace root; "." is the workspace repository itself.
# The rights differ per repository - owner decisions D28 (push), D30 (pull), D47 (manual push).
# Three-valued since D47, and the two push fields must NOT be flattened back into one:
#   push=True, push_auto=True   -> may be pushed, including without being asked each time
#   push=True, push_auto=False  -> may be pushed ONLY on an explicit per-push instruction
#   push=False                  -> never pushed, and a pushurl block enforces it
# `engage` itself pushes nothing in any case: "push" is absent from ALLOWED and present in
# FORBIDDEN, so these fields drive reporting and recommendation only.
POLICIES: dict[str, Policy] = {
    ".": Policy(
        name="dynamic-api-validator (workspace)",
        pull="ff-only", push=True, push_auto=True,
        note="The owner's own repository. Pull and push both permitted (D28).",
    ),
    "pam": Policy(
        name="PAM product (developer repo)",
        pull="ff-only", push=False,
        note="Reference only. Fast-forward pull permitted (D28/D30); push blocked by pushurl.",
    ),
    "Automation gitlab repo/pam_automation_bootstrap": Policy(
        name="PAM Bootstrap Automation",
        pull="ff-only", push=True, push_auto=False,
        note="Develop on Dev. Fast-forward pull permitted (D30). Manual push permitted (D47) - "
             "an explicit per-push instruction only, never automatic, never as part of "
             "finishing a task. The owner still bumps the pam submodule gitlink.",
    ),
}

# push_auto without push would be a right nobody granted. Asserted rather than assumed, because
# the two fields are edited by hand and a mismatch would read as deliberate.
assert not [k for k, v in POLICIES.items() if v.push_auto and not v.push],     "a policy grants automatic push without granting push"

# The safe default for anything not in the table above. A repository nobody has classified is
# fetched and reported, never pulled - `engage` must not invent policy for a repo the owner has
# not seen. This is what makes leaving discovery switched on safe.
UNKNOWN_POLICY = Policy(
    name="unclassified", pull="none", push=False,
    note="Newly discovered and not in the policy table. Fetched and reported only, never pulled, "
         "until the owner classifies it in engage_core.POLICIES.",
)


def policy_for(rel: str) -> tuple[Policy, bool]:
    """Return (policy, is_known). `rel` is a POSIX-style path relative to ROOT, or '.'."""
    pol = POLICIES.get(rel)
    return (pol, True) if pol else (UNKNOWN_POLICY, False)


# ---------------------------------------------------------------------------------------------
# git plumbing
# ---------------------------------------------------------------------------------------------
def run_git(repo: Path, *args: str, timeout: int = 300) -> tuple[int, str]:
    """Run one git command, refusing anything not explicitly allowed.

    Mirrors `obj016_daily_refresh.run_git` and shares its FORBIDDEN set. Two extra guards matter
    here: `pull` must carry --ff-only so it can never create a merge commit, and `stash` is
    read-only - `stash list` and nothing else.
    """
    sub = args[0] if args else ""
    if sub in FORBIDDEN or sub not in ALLOWED:
        raise RuntimeError(f"refused git subcommand {sub!r} - not on the allow-list")
    if sub == "pull" and "--ff-only" not in args:
        raise RuntimeError("refused: `git pull` must be --ff-only")
    if sub == "stash" and (len(args) < 2 or args[1] != "list"):
        raise RuntimeError("refused: only `git stash list` is permitted, never a stash mutation")
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace",
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


CONFLICT_PAIRS = {"DD", "AA"}


@dataclass
class RepoState:
    """Everything `engage` knows about one repository, before deciding anything."""
    rel: str
    path: str
    name: str = ""
    is_repo: bool = True
    head: str = ""
    branch: str = ""
    detached: bool = False
    upstream: str | None = None
    ahead: int = 0
    behind: int = 0
    staged: int = 0
    unstaged: int = 0
    untracked: int = 0
    conflicts: int = 0
    conflict_files: list[str] = field(default_factory=list)
    stashes: int = 0
    remotes: dict[str, str] = field(default_factory=dict)
    push_blocked: bool = False
    in_progress: str | None = None      # merge | rebase | cherry-pick | bisect | revert
    error: str | None = None

    @property
    def dirty(self) -> int:
        return self.staged + self.unstaged + self.untracked + self.conflicts

    @property
    def clean(self) -> bool:
        return self.dirty == 0

    @property
    def diverged(self) -> bool:
        return self.ahead > 0 and self.behind > 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d.update(dirty=self.dirty, clean=self.clean, diverged=self.diverged)
        return d


_BRANCH_RE = re.compile(
    r"^## (?P<branch>\S+?)"
    r"(?:\.\.\.(?P<upstream>\S+))?"
    r"(?: \[(?P<track>[^\]]+)\])?$"
)


def parse_status(porcelain: str) -> dict:
    """Parse `git status --porcelain=v1 -b` into counts.

    One command yields branch, upstream, ahead/behind, staged, unstaged, untracked and conflicts.
    Fewer round-trips than asking six times and, more importantly, one consistent snapshot rather
    than six that can disagree if something changes underneath.

    Note: ahead/behind here are measured against the *remote-tracking ref*, which is only current
    after a fetch. `engage` always fetches before reading this, for exactly that reason.
    """
    out: dict = {"branch": "", "upstream": None, "ahead": 0, "behind": 0, "detached": False,
                 "staged": 0, "unstaged": 0, "untracked": 0, "conflicts": 0, "conflict_files": []}
    for line in porcelain.splitlines():
        if line.startswith("## "):
            if line.startswith("## HEAD (no branch)"):
                out["detached"] = True
                out["branch"] = "HEAD (detached)"
                continue
            if "No commits yet on " in line:
                out["branch"] = line.split("No commits yet on ", 1)[1].strip()
                continue
            m = _BRANCH_RE.match(line.rstrip())
            if not m:
                out["branch"] = line[3:].strip()
                continue
            out["branch"] = m.group("branch")
            out["upstream"] = m.group("upstream")
            track = m.group("track") or ""
            a = re.search(r"ahead (\d+)", track)
            b = re.search(r"behind (\d+)", track)
            if a:
                out["ahead"] = int(a.group(1))
            if b:
                out["behind"] = int(b.group(1))
            continue
        if not line.strip():
            continue
        xy, name = line[:2], line[3:]
        if xy == "??":
            out["untracked"] += 1
        elif "U" in xy or xy in CONFLICT_PAIRS:
            out["conflicts"] += 1
            if len(out["conflict_files"]) < 10:
                out["conflict_files"].append(name)
        else:
            if xy[0] not in " ?":
                out["staged"] += 1
            if xy[1] not in " ?":
                out["unstaged"] += 1
    return out


def detect_in_progress(repo: Path) -> str | None:
    """Detect a half-finished git operation.

    This is the single most important thing to check before touching a repository. A tree
    mid-rebase looks merely 'dirty' to a naive check, and an automated recovery attempt on it can
    destroy work that exists nowhere else.
    """
    rc, out = run_git(repo, "rev-parse", "--absolute-git-dir")
    if rc != 0:
        return None
    g = Path(out.strip())
    for marker, label in (
        ("rebase-merge", "rebase"), ("rebase-apply", "rebase"),
        ("MERGE_HEAD", "merge"), ("CHERRY_PICK_HEAD", "cherry-pick"),
        ("REVERT_HEAD", "revert"), ("BISECT_LOG", "bisect"),
    ):
        if (g / marker).exists():
            return label
    return None


def inspect_repo(path: Path, rel: str) -> RepoState:
    """Read one repository's complete state. Read-only - issues no fetch and no pull."""
    pol, _known = policy_for(rel)
    st = RepoState(rel=rel, path=str(path), name=pol.name)
    try:
        rc, out = run_git(path, "rev-parse", "--is-inside-work-tree")
        if rc != 0 or out.strip() != "true":
            st.is_repo, st.error = False, "not a git work tree"
            return st

        rc, out = run_git(path, "status", "--porcelain=v1", "-b")
        if rc != 0:
            st.error = f"git status failed: {out.strip()[:200]}"
            return st
        for k, v in parse_status(out).items():
            setattr(st, k, v)

        rc, out = run_git(path, "rev-parse", "--short", "HEAD")
        st.head = out.strip() if rc == 0 else "(no commits)"

        rc, out = run_git(path, "remote", "-v")
        if rc == 0:
            for line in out.splitlines():
                parts = line.split()
                if len(parts) >= 2 and parts[-1] == "(fetch)":
                    st.remotes[parts[0]] = parts[1]

        rc, out = run_git(path, "config", "--get", "remote.origin.pushurl")
        st.push_blocked = rc == 0 and "DISABLED" in out.upper()

        rc, out = run_git(path, "stash", "list")
        st.stashes = len([ln for ln in out.splitlines() if ln.strip()]) if rc == 0 else 0

        st.in_progress = detect_in_progress(path)
    except Exception as exc:                      # a broken repo must not stop the sweep
        st.error = f"{type(exc).__name__}: {exc}"
    return st


# ---------------------------------------------------------------------------------------------
# discovery
# ---------------------------------------------------------------------------------------------
def discover_repos(root: Path, max_depth: int = MAX_DEPTH) -> list[tuple[Path, str]]:
    """Find every git repository at or under `root`, without hard-coding names.

    Rule: descend from the workspace root, and when a directory turns out to be a repository,
    record it and stop descending into it. That finds the nested checkouts (one and two levels
    down) while never walking into a repository's own contents - which is what keeps a vendored
    dependency's .git, and the uninitialised `pam/Automation/` submodule, out of the results.
    """
    found: list[tuple[Path, str]] = []

    def rel_of(p: Path) -> str:
        r = p.relative_to(root).as_posix()
        return r or "."

    if (root / ".git").exists():
        found.append((root, "."))

    def walk(d: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(e for e in d.iterdir() if e.is_dir())
        except (PermissionError, OSError):
            return
        for e in entries:
            if e.name in SKIP_DIRS or e.name == ".git":
                continue
            if (e / ".git").exists():
                found.append((e, rel_of(e)))
                continue                      # never descend into a repository
            walk(e, depth + 1)

    walk(root, 1)
    return found


# ---------------------------------------------------------------------------------------------
# the decision table
# ---------------------------------------------------------------------------------------------
@dataclass
class Plan:
    action: str                 # "pull" | "fetch-only" | "skip"
    reason: str
    severity: str               # "critical" | "high" | "normal" | "low" | "info"
    needs_confirmation: bool = False
    attention: str | None = None


def classify(st: RepoState, pol: Policy, known: bool = True) -> Plan:
    """Decide what is safe to do with one repository. First match wins; the order *is* the policy.

    Nothing here can return an action that loses work. The only mutating action it can return is
    "pull", and it returns that only for a clean tree strictly behind its upstream.
    """
    if not st.is_repo or st.error:
        return Plan("skip", st.error or "not a git repository", "high",
                    attention=f"{st.rel}: {st.error or 'not a git repository'}")

    if st.in_progress:
        return Plan("skip", f"a {st.in_progress} is in progress - finish or abort it first",
                    "critical", True,
                    f"{st.rel}: {st.in_progress} in progress. Manual action required; engage will "
                    f"not touch a half-finished operation.")

    if st.conflicts:
        shown = ", ".join(st.conflict_files[:3])
        return Plan("skip", f"{st.conflicts} unmerged path(s)", "critical", True,
                    f"{st.rel}: {st.conflicts} merge conflict(s) need manual resolution ({shown}).")

    if st.detached:
        return Plan("skip", f"detached HEAD at {st.head}", "high", True,
                    f"{st.rel}: detached HEAD at {st.head} - commits here are on no branch.")

    if not st.remotes:
        return Plan("skip", "no remote configured", "normal",
                    attention=f"{st.rel}: no remote configured, so nothing can be synchronized.")

    if not st.upstream:
        return Plan("fetch-only", f"branch {st.branch} has no upstream", "normal",
                    attention=f"{st.rel}: branch '{st.branch}' tracks nothing; fetched, not compared.")

    if st.diverged:
        return Plan("skip", f"diverged - {st.ahead} ahead, {st.behind} behind", "high", True,
                    f"{st.rel}: diverged from {st.upstream} ({st.ahead} ahead, {st.behind} behind). "
                    f"Reconciling needs a rebase or a merge - your call, not engage's.")

    if st.behind and not st.clean:
        return Plan("skip", f"{st.behind} behind, but {st.dirty} uncommitted change(s)", "high", True,
                    f"{st.rel}: {st.behind} commit(s) behind {st.upstream}, pull skipped to protect "
                    f"{st.dirty} uncommitted change(s).")

    if st.behind:
        if pol.pull == "ff-only":
            return Plan("pull", f"{st.behind} behind, tree clean - fast-forward is safe", "normal")
        return Plan("fetch-only", f"{st.behind} behind; policy is report-only", "normal",
                    attention=f"{st.rel}: {st.behind} behind {st.upstream}. "
                              f"{'Unclassified repository - ' if not known else ''}not pulled.")

    if st.ahead:
        if pol.push and pol.push_auto:
            where = "ready to push"
        elif pol.push:
            where = "ready to push - manual push only, on an explicit instruction (D47)"
        else:
            where = "the owner pushes this repo"
        return Plan("skip", f"{st.ahead} unpushed commit(s)", "normal",
                    attention=f"{st.rel}: {st.ahead} commit(s) ahead of {st.upstream} - {where}.")

    if not st.clean:
        return Plan("skip", f"{st.dirty} uncommitted change(s)", "normal",
                    attention=f"{st.rel}: {st.dirty} uncommitted change(s) in the working tree.")

    return Plan("skip", "up to date and clean", "info")
