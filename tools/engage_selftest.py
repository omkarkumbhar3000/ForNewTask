#!/usr/bin/env python3
"""
engage_selftest.py - scenario tests for the `engage` decision table.

OBJ-026. Run it directly; it needs no network, no PAM environment and no dependency beyond git
and the standard library:

    python tools\\engage_selftest.py           # run every scenario
    python tools\\engage_selftest.py --keep     # leave the fixtures on disk to inspect

Two layers, deliberately
------------------------
**Fixtures** build real git repositories in a temp directory and drive them into each state, then
assert what `engage` decides. This is what proves `parse_status()` against porcelain output that
git actually emits, rather than output someone believed it emits.

**Table** feeds hand-built `RepoState` objects straight into `classify()`. Some rows cannot be
produced in isolation by real git - an unmerged path essentially always arrives with MERGE_HEAD
alongside it - so the fixture layer would only ever reach them through the earlier row. Testing
the table directly is the only way to prove the rows underneath are reachable and correct.

This module never touches the real workspace. Every repository it creates lives under a temp
directory it made itself, and the only git commands run against the real tree are the read-only
ones inside `engage_core`.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import workspace_root  # OBJ-025: one resolver, marker-based
import engage_core as core  # noqa: E402

# Fixture setup uses raw git on purpose. `engage_core.run_git` refuses commit/push/merge/checkout
# by design, and that guard is exactly what we do NOT want to weaken to build a test repo.
GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "engage selftest", "GIT_AUTHOR_EMAIL": "selftest@localhost",
    "GIT_COMMITTER_NAME": "engage selftest", "GIT_COMMITTER_EMAIL": "selftest@localhost",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
}

PASS, FAIL = [], []


def git(repo: Path, *args: str, check: bool = True) -> str:
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=GIT_ENV)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {repo}:\n{p.stdout}{p.stderr}")
    return p.stdout


def check(name: str, got, want, extra: str = "") -> None:
    if got == want:
        PASS.append(name)
        print(f"  [ PASS ] {name}")
    else:
        FAIL.append(f"{name}: expected {want!r}, got {got!r} {extra}")
        print(f"  [ FAIL ] {name}: expected {want!r}, got {got!r} {extra}")


def write(p: Path, text: str) -> None:
    p.write_text(text, encoding="utf-8")


def rmtree(p: Path) -> None:
    """Delete a git tree on Windows.

    git marks objects under .git/objects read-only, and Windows refuses to unlink a read-only
    file - so a plain rmtree leaves the directory behind and the next clone into that path fails
    with 'already exists and is not an empty directory'. Clear the bit and retry.
    """
    def force(func, path, _exc):
        os.chmod(path, 0o700)
        func(path)

    shutil.rmtree(p, onexc=force)


# ---------------------------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------------------------
def make_origin(base: Path) -> Path:
    """A bare 'remote' plus one seed commit, so clones have something to track."""
    origin = base / "origin.git"
    git(base, "init", "--bare", "-b", "main", str(origin))
    seed = base / "_seed"
    git(base, "clone", str(origin), str(seed))
    write(seed / "file.txt", "line 1\n")
    git(seed, "add", "-A")
    git(seed, "commit", "-m", "seed")
    git(seed, "push", "-u", "origin", "main")
    rmtree(seed)
    return origin


def clone(base: Path, origin: Path, name: str) -> Path:
    d = base / name
    git(base, "clone", str(origin), str(d))
    return d


def advance_origin(base: Path, origin: Path, n: int = 1, text: str = "remote") -> None:
    """Push `n` new commits to the bare remote via a throwaway clone."""
    tmp = base / "_pusher"
    git(base, "clone", str(origin), str(tmp))
    for i in range(n):
        write(tmp / "file.txt", f"line 1\n{text} {i}\n")
        git(tmp, "add", "-A")
        git(tmp, "commit", "-m", f"{text} {i}")
    git(tmp, "push", "origin", "main")
    rmtree(tmp)


# Fixtures stand in for a *classified* repository unless a test says otherwise. Passing an
# unclassified path here would send every fixture down the fetch-only default and quietly assert
# nothing - the harness must ask about the policy it means to test.
FIXTURE_POLICY = core.POLICIES["."]


def state_of(repo: Path, pol: core.Policy = FIXTURE_POLICY,
             known: bool = True) -> tuple[core.RepoState, core.Plan]:
    """Fetch (as engage does) then inspect and classify."""
    core.run_git(repo, "fetch", "--all", "--quiet")
    st = core.inspect_repo(repo, "fixture")
    return st, core.classify(st, pol, known)


def run_fixtures(base: Path) -> None:
    print("\nFixtures - real git repositories")
    print("-" * 74)
    origin = make_origin(base)

    # 1 - clean and level with the remote
    r = clone(base, origin, "clean")
    st, plan = state_of(r)
    check("clean repo -> no action", (plan.action, plan.severity), ("skip", "info"))
    check("clean repo -> tree reported clean", st.clean, True)

    # 2 - already up to date (same shape, asserted separately because it is the common case)
    st, plan = state_of(r)
    check("already up to date -> still no action", plan.action, "skip")
    check("already up to date -> zero behind", (st.ahead, st.behind), (0, 0))

    # 3 - remote has moved, tree clean  ->  the one case that may pull
    r = clone(base, origin, "behind")
    advance_origin(base, origin, 2)
    st, plan = state_of(r)
    check("behind + clean -> pull", plan.action, "pull")
    check("behind + clean -> counted 2 behind", st.behind, 2)

    # 4 - remote has moved AND there is uncommitted work  ->  protect the work
    r = clone(base, origin, "behind_dirty")
    advance_origin(base, origin, 1, "more")
    write(r / "file.txt", "local edit not committed\n")
    st, plan = state_of(r)
    check("behind + dirty -> skip", plan.action, "skip")
    check("behind + dirty -> high severity", plan.severity, "high")
    check("behind + dirty -> needs confirmation", plan.needs_confirmation, True)
    check("behind + dirty -> says work is protected",
          "protect" in (plan.attention or ""), True, f"({plan.attention})")

    # 5 - ahead of the remote
    r = clone(base, origin, "ahead")
    write(r / "local.txt", "local\n")
    git(r, "add", "-A")
    git(r, "commit", "-m", "local only")
    st, plan = state_of(r)
    check("ahead -> skip", plan.action, "skip")
    check("ahead -> counted 1 ahead", st.ahead, 1)

    # 6 - diverged: local commits AND remote commits
    r = clone(base, origin, "diverged")
    write(r / "mine.txt", "mine\n")
    git(r, "add", "-A")
    git(r, "commit", "-m", "mine")
    advance_origin(base, origin, 1, "theirs")
    st, plan = state_of(r)
    check("diverged -> skip", plan.action, "skip")
    check("diverged -> high severity", plan.severity, "high")
    check("diverged -> detected as diverged", st.diverged, True)
    check("diverged -> needs confirmation", plan.needs_confirmation, True)

    # 7 - merge conflict, left mid-merge (how a conflict actually presents)
    r = clone(base, origin, "conflict")
    write(r / "file.txt", "my version\n")
    git(r, "add", "-A")
    git(r, "commit", "-m", "my version")
    advance_origin(base, origin, 1, "their version")
    git(r, "fetch", "origin")
    git(r, "merge", "origin/main", check=False)          # expected to conflict
    st, plan = state_of(r)
    check("merge conflict -> skip", plan.action, "skip")
    check("merge conflict -> critical", plan.severity, "critical")
    check("merge conflict -> merge detected in progress", st.in_progress, "merge")

    # 8 - rebase in progress
    r = clone(base, origin, "rebase")
    write(r / "file.txt", "rebase side\n")
    git(r, "add", "-A")
    git(r, "commit", "-m", "rebase side")
    advance_origin(base, origin, 1, "upstream moves")
    git(r, "fetch", "origin")
    git(r, "rebase", "origin/main", check=False)         # expected to stop on conflict
    st, plan = state_of(r)
    check("rebase in progress -> skip", plan.action, "skip")
    check("rebase in progress -> critical", plan.severity, "critical")
    check("rebase in progress -> rebase detected", st.in_progress, "rebase")

    # 9 - no remote at all
    r = base / "no_remote"
    r.mkdir()
    git(r, "init", "-b", "main")
    write(r / "a.txt", "a\n")
    git(r, "add", "-A")
    git(r, "commit", "-m", "only commit")
    st = core.inspect_repo(r, "fixture")
    plan = core.classify(st, FIXTURE_POLICY)
    check("no remote -> skip", plan.action, "skip")
    check("no remote -> no remotes recorded", st.remotes, {})

    # 10 - a branch with no upstream
    r = clone(base, origin, "no_upstream")
    git(r, "checkout", "-b", "feature")
    st = core.inspect_repo(r, "fixture")
    plan = core.classify(st, FIXTURE_POLICY)
    check("no upstream -> fetch-only", plan.action, "fetch-only")
    check("no upstream -> upstream is None", st.upstream, None)

    # 11 - detached HEAD
    r = clone(base, origin, "detached")
    sha = git(r, "rev-parse", "HEAD").strip()
    git(r, "checkout", "--detach", sha)
    st = core.inspect_repo(r, "fixture")
    plan = core.classify(st, FIXTURE_POLICY)
    check("detached HEAD -> skip", plan.action, "skip")
    check("detached HEAD -> detected", st.detached, True)

    # 12 - a newly discovered repository nobody has classified, sitting behind its remote
    r = clone(base, origin, "unclassified")
    advance_origin(base, origin, 1, "unseen")
    core.run_git(r, "fetch", "--all", "--quiet")
    st = core.inspect_repo(r, "definitely/not/in/the/policy/table")
    pol, known = core.policy_for("definitely/not/in/the/policy/table")
    plan = core.classify(st, pol, known)
    check("unclassified repo -> known=False", known, False)
    check("unclassified repo -> never pulled", plan.action, "fetch-only")
    check("unclassified repo -> flagged for classification",
          "Unclassified" in (plan.attention or ""), True, f"({plan.attention})")

    # 13 - discovery across several repositories, ignoring vendored trees
    ws = base / "workspace"
    (ws / "node_modules" / "pkg").mkdir(parents=True)
    git(ws, "init", "-b", "main")
    git(ws / "node_modules" / "pkg", "init", "-b", "main")
    clone(ws, origin, "nested_a")
    (ws / "group").mkdir()
    clone(ws / "group", origin, "nested_b")
    found = {rel for _p, rel in core.discover_repos(ws)}
    check("discovery -> finds root, depth-1 and depth-2 repos",
          found, {".", "nested_a", "group/nested_b"})
    check("discovery -> ignores node_modules", any("node_modules" in f for f in found), False)


# ---------------------------------------------------------------------------------------------
# the decision table, exercised directly
# ---------------------------------------------------------------------------------------------
def run_table() -> None:
    print("\nDecision table - synthetic states")
    print("-" * 74)
    pol = core.POLICIES["."]

    def s(**kw) -> core.RepoState:
        st = core.RepoState(rel="t", path="t", is_repo=True, head="abc1234", branch="main",
                            upstream="origin/main",
                            remotes={"origin": "https://example/x.git"})
        for k, v in kw.items():
            if not hasattr(st, k):
                raise AttributeError(f"RepoState has no field {k!r}")
            setattr(st, k, v)
        return st

    # An unmerged path with no in-progress marker: unreachable via real git, but it is the row
    # directly under the in-progress row, so it must be proven reachable on its own.
    plan = core.classify(s(conflicts=2, conflict_files=["a.txt", "b.txt"]), pol)
    check("table: conflicts without a marker -> critical",
          (plan.action, plan.severity), ("skip", "critical"))

    plan = core.classify(s(in_progress="cherry-pick"), pol)
    check("table: cherry-pick in progress -> critical",
          (plan.action, plan.severity), ("skip", "critical"))

    plan = core.classify(s(is_repo=False, error="not a git work tree"), pol)
    check("table: not a repository -> skip", plan.action, "skip")

    plan = core.classify(s(behind=3, untracked=1), pol)
    check("table: behind + untracked file only -> still protected", plan.action, "skip")

    plan = core.classify(s(behind=3, staged=1), pol)
    check("table: behind + staged change -> protected", plan.action, "skip")

    plan = core.classify(s(behind=3), pol)
    check("table: behind + clean -> pull", plan.action, "pull")

    plan = core.classify(s(behind=3), core.UNKNOWN_POLICY, known=False)
    check("table: behind + clean + no policy -> fetch-only", plan.action, "fetch-only")

    plan = core.classify(s(behind=3), core.POLICIES["pam"])
    check("table: behind + clean + pam policy -> pull (D30)", plan.action, "pull")

    plan = core.classify(s(ahead=2), core.POLICIES["pam"])
    check("table: ahead in a pull-only repo -> says the owner pushes",
          "owner pushes" in (plan.attention or ""), True, f"({plan.attention})")

    plan = core.classify(s(ahead=2), pol)
    check("table: ahead in the workspace repo -> says ready to push",
          "ready to push" in (plan.attention or ""), True, f"({plan.attention})")

    plan = core.classify(s(unstaged=4), pol)
    check("table: dirty and level -> reported, not acted on",
          (plan.action, plan.severity), ("skip", "normal"))

    plan = core.classify(s(), pol)
    check("table: clean and level -> informational", plan.severity, "info")

    # No path through the table may return an action that is not one of these three.
    actions = set()
    for kw in (dict(), dict(behind=1), dict(ahead=1), dict(behind=1, ahead=1), dict(unstaged=1),
               dict(behind=1, unstaged=1), dict(conflicts=1), dict(in_progress="merge"),
               dict(detached=True), dict(remotes={}), dict(upstream=None), dict(is_repo=False)):
        actions.add(core.classify(s(**kw), pol).action)
    check("table: only safe actions are reachable", actions <= {"pull", "fetch-only", "skip"}, True,
          f"(reachable: {sorted(actions)})")


# ---------------------------------------------------------------------------------------------
def run_guards() -> None:
    """The allow-list is a safety control, so it gets tested like one."""
    print("\nSafety guards")
    print("-" * 74)
    here = workspace_root(__file__)

    for verb in ("push", "reset", "clean", "merge", "rebase", "checkout", "commit", "gc"):
        try:
            core.run_git(here, verb, "--help")
            check(f"guard: `git {verb}` refused", False, True)
        except RuntimeError:
            check(f"guard: `git {verb}` refused", True, True)

    try:
        core.run_git(here, "pull")
        check("guard: bare `git pull` refused (must be --ff-only)", False, True)
    except RuntimeError:
        check("guard: bare `git pull` refused (must be --ff-only)", True, True)

    try:
        core.run_git(here, "stash", "push")
        check("guard: `git stash push` refused", False, True)
    except RuntimeError:
        check("guard: `git stash push` refused", True, True)

    check("guard: allow-list and ban-list do not overlap",
          bool(core.ALLOWED & core.FORBIDDEN), False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", action="store_true", help="leave the fixture repositories on disk")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    base = Path(tempfile.mkdtemp(prefix="engage-selftest-"))
    print("=" * 74)
    print("  engage self-test")
    print(f"  fixtures: {base}")
    print("=" * 74)
    try:
        run_fixtures(base)
        run_table()
        run_guards()
    finally:
        if args.keep:
            print(f"\nfixtures kept at {base}")
        else:
            shutil.rmtree(base, ignore_errors=True)

    print("-" * 74)
    print(f"  {len(PASS)} passed, {len(FAIL)} failed")
    for f in FAIL:
        print(f"    FAIL {f}")
    print("=" * 74)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
