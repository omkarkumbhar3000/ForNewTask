#!/usr/bin/env python3
"""
obj016_daily_refresh.py — the daily pull-and-refresh job.

OBJ-016. Pulls what can safely be pulled, then re-derives everything downstream that does
not require executing the API suite. Designed to be run unattended by Windows Task Scheduler.

    python tools\\obj016_daily_refresh.py              # DRY RUN — changes nothing
    python tools\\obj016_daily_refresh.py --execute     # do it
    python tools\\obj016_daily_refresh.py --execute --skip-git   # refresh only

Deny-by-default, matching every other harness script here: a bare run performs no fetch, no
pull and no write. `--execute` is required.

⛔ What this job will never do, by construction — see FORBIDDEN below:
  · push, merge, rebase, reset, checkout, stash, clean, gc, prune, or branch surgery
  · touch `AI`. That branch has NO upstream, so the automation repo is fetch-and-report only
  · call any PAM endpoint, or `/arcontoken`. It issues zero HTTP to the product
  · run the API suite. That decision was taken explicitly: fresh source changes no KPI, and a
    daily 5.5 h run against an environment that lost 85 of 329 minutes to app-pool downtime
    would produce a daily false alarm
  · apply drift auto-fixes. `obj013_fix.py` writes to CLAUDE.md, README.md and .claude/rules/*
    in folders with no git history. Drift is REPORTED daily and applied by a human

Exit codes: 0 all steps ok or safely skipped · 1 at least one step failed.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
STATE_DIR = ROOT / "state" / "daily"
STATE_FILE = STATE_DIR / "last-run.json"
LOG_FILE = STATE_DIR / "daily.log"

# The dashboard reads its datasets from here at runtime (OBJ-016), so the refresh stamp the
# UI shows must land in the same directory.
APP_DATA = ROOT / "tools" / "dashboard" / "public" / "data"

PAM = ROOT / "pam"
BOOTSTRAP = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"

# Any git subcommand not on this list is refused before it reaches a subprocess. This is a
# structural guard, not a reminder: an unattended job must not be one typo away from moving a
# branch the owner has not merged.
GIT_ALLOWED = {
    "status", "rev-parse", "rev-list", "log", "fetch", "pull",
    "stash",          # `stash list` only — read-only; enforced in run_git
    "config", "remote", "count-objects",
}
FORBIDDEN = {
    "push", "merge", "rebase", "reset", "checkout", "switch", "clean",
    "gc", "prune", "repack", "filter-repo", "branch", "tag", "cherry-pick", "commit", "am",
}


def make_output_safe() -> None:
    """This process prints ⛔ and em-dashes too, so give our own stdout the same treatment.

    `errors="replace"` rather than a hard failure: a job must never die because it could not
    render a character in its own progress message.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except (AttributeError, ValueError):
            pass


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


class Journal:
    """Per-step outcome, written to disk whatever happens."""

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self.started = now()
        self.steps: list[dict] = []
        self.lines: list[str] = []

    def say(self, msg: str) -> None:
        print(msg)
        self.lines.append(msg)

    def step(self, name: str, status: str, detail: str, **extra) -> dict:
        rec = {"step": name, "status": status, "detail": detail, **extra}
        self.steps.append(rec)
        icon = {"ok": "  OK  ", "skipped": " SKIP ", "failed": " FAIL ", "dry-run": " DRY  "}[status]
        self.say(f"[{icon}] {name}: {detail}")
        return rec

    @property
    def failed(self) -> bool:
        return any(s["status"] == "failed" for s in self.steps)


def run_git(repo: Path, *args: str, timeout: int = 600) -> tuple[int, str]:
    """Run one git command, refusing anything not explicitly allowed."""
    sub = args[0] if args else ""
    if sub in FORBIDDEN or sub not in GIT_ALLOWED:
        raise RuntimeError(f"refused git subcommand {sub!r} — not on the allow-list")
    if sub == "stash" and (len(args) < 2 or args[1] != "list"):
        raise RuntimeError("refused: only `git stash list` is permitted, never a stash mutation")
    if sub == "pull" and "--ff-only" not in args:
        raise RuntimeError("refused: `git pull` must be --ff-only so it can never create a merge commit")
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace",
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def child_env() -> dict[str, str]:
    """Force UTF-8 on every child script.

    ⛔ This is load-bearing, and it is why the first scheduled run failed. Under Task Scheduler
    there is no console, so a child Python picks cp1252 from the locale for its stdout. Several
    scripts here print ⛔ and em-dashes, so they die with
    `UnicodeEncodeError: 'charmap' codec can't encode character '\\u26d4'` — a failure that never
    reproduces from an interactive shell. Setting the encoding explicitly makes the job behave
    identically whether a human or the scheduler starts it.
    """
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_script(script: str, *args: str, timeout: int = 1800) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / script), *args],
        capture_output=True, text=True, cwd=str(ROOT), timeout=timeout,
        encoding="utf-8", errors="replace", env=child_env(),
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def head(repo: Path) -> str:
    rc, out = run_git(repo, "rev-parse", "--short", "HEAD")
    return out.strip() if rc == 0 else "unknown"


def dirty_count(repo: Path) -> int:
    rc, out = run_git(repo, "status", "--porcelain")
    if rc != 0:
        return -1
    return len([ln for ln in out.splitlines() if ln.strip()])


def pack_bytes(repo: Path) -> int:
    """Total size of .git/objects/pack. Cheap (~100 files) and it is where the bulk lives.

    Worth logging daily: OBJ-014 measured a routine 106-commit pull adding 1.1 GB to this
    repository because compressed archives are committed to it. Silent growth is how it got
    to 27.88 GB.
    """
    pack = repo / ".git" / "objects" / "pack"
    if not pack.is_dir():
        return 0
    return sum(f.stat().st_size for f in pack.iterdir() if f.is_file())


# ─────────────────────────────────────────────────────────────────────────────
# step 1 — the developer repository: fast-forward only
# ─────────────────────────────────────────────────────────────────────────────
def step_pull_pam(j: Journal, execute: bool) -> None:
    name = "pull pam/ (developer repo)"
    if not (PAM / ".git").is_dir():
        j.step(name, "skipped", "pam/ is not a git checkout here")
        return

    dirty = dirty_count(PAM)
    branch = run_git(PAM, "rev-parse", "--abbrev-ref", "HEAD")[1].strip()
    before = head(PAM)

    if dirty != 0:
        j.step(name, "skipped",
               f"working tree is not clean ({dirty} changed) — refusing to pull. "
               f"pam/ must be left clean; resolve by hand",
               branch=branch, head=before, dirty=dirty)
        return

    rc, out = run_git(PAM, "rev-parse", "--abbrev-ref", "@{upstream}")
    if rc != 0:
        j.step(name, "skipped", f"no upstream configured for {branch}", branch=branch, head=before)
        return
    upstream = out.strip()

    if not execute:
        j.step(name, "dry-run", f"would run: git pull --ff-only  ({branch} <- {upstream}, at {before}, tree clean)",
               branch=branch, head=before, upstream=upstream)
        return

    pack_before = pack_bytes(PAM)
    rc, out = run_git(PAM, "pull", "--ff-only", timeout=1800)
    after = head(PAM)
    pack_after = pack_bytes(PAM)
    grew_mb = round((pack_after - pack_before) / 1024 / 1024, 1)

    if rc != 0:
        j.step(name, "failed",
               f"git pull --ff-only failed — NOT forced. {out.strip().splitlines()[-1] if out.strip() else 'no output'}",
               branch=branch, head=before, upstream=upstream)
        return

    still_clean = dirty_count(PAM) == 0
    if before == after:
        j.step(name, "ok", f"already up to date at {after}; tree clean",
               branch=branch, head=after, changed=False, packDeltaMb=grew_mb)
    else:
        j.step(name, "ok",
               f"fast-forwarded {before} -> {after}; packfiles grew {grew_mb} MB; "
               f"tree {'clean' if still_clean else 'NOT CLEAN — investigate'}",
               branch=branch, head=after, changed=True, packDeltaMb=grew_mb, cleanAfter=still_clean)


# ─────────────────────────────────────────────────────────────────────────────
# step 2 — the automation repository: fetch and report, never move `AI`
# ─────────────────────────────────────────────────────────────────────────────
def step_fetch_bootstrap(j: Journal, execute: bool) -> None:
    name = "fetch automation repo (report only)"
    if not (BOOTSTRAP / ".git").is_dir():
        j.step(name, "skipped", "automation repo is not a git checkout here")
        return

    branch = run_git(BOOTSTRAP, "rev-parse", "--abbrev-ref", "HEAD")[1].strip()
    dirty = dirty_count(BOOTSTRAP)
    stashes = len([ln for ln in run_git(BOOTSTRAP, "stash", "list")[1].splitlines() if ln.strip()])

    if not execute:
        j.step(name, "dry-run",
               f"would run: git fetch origin --prune  (on {branch}, {dirty} uncommitted, {stashes} stash). "
               f"Never a pull or merge — {branch} has no upstream",
               branch=branch, dirty=dirty, stashes=stashes)
        return

    rc, out = run_git(BOOTSTRAP, "fetch", "origin", "--prune", timeout=900)
    if rc != 0:
        last = out.strip().splitlines()[-1] if out.strip() else "no output"
        j.step(name, "failed", f"git fetch failed: {last}", branch=branch, dirty=dirty)
        return

    behind = ahead = None
    rc2, out2 = run_git(BOOTSTRAP, "rev-list", "--left-right", "--count", f"{branch}...origin/Dev")
    if rc2 == 0 and out2.strip():
        parts = out2.split()
        if len(parts) == 2:
            ahead, behind = int(parts[0]), int(parts[1])

    detail = f"fetched origin. {branch} is {ahead} ahead / {behind} behind origin/Dev"
    if dirty:
        detail += f"; {dirty} uncommitted files and {stashes} stash left untouched"
    detail += ". ⛔ Not merged — that is the owner's decision"
    j.step(name, "ok", detail, branch=branch, ahead=ahead, behind=behind, dirty=dirty, stashes=stashes)


# ─────────────────────────────────────────────────────────────────────────────
# step 3 — drift check (read-only, offline)
# ─────────────────────────────────────────────────────────────────────────────
def step_drift(j: Journal, execute: bool) -> None:
    name = "drift check"
    if not (ROOT / "tools" / "obj013_loop.py").exists():
        j.step(name, "skipped", "obj013_loop.py not present")
        return
    if not execute:
        j.step(name, "dry-run", "would run: obj013_loop.py check --json (read-only, offline)")
        return

    rc, out = run_script("obj013_loop.py", "check", "--json", timeout=900)
    summary = None
    try:
        summary = json.loads(out).get("summary")
    except Exception:
        pass
    if summary:
        sev = summary.get("by_severity") or {}
        j.step(name, "ok",
               f"{summary.get('clean', '?')} clean · {summary.get('open', '?')} open "
               f"({sev.get('critical', 0)} critical, {sev.get('high', 0)} high). "
               f"Reported, not auto-fixed",
               summary=summary)
    else:
        # A non-zero exit from the drift check means drift was FOUND, which is information.
        # But output we cannot parse is a genuine failure of this step: the job did not learn
        # the drift state, and calling that "ok" would hide it.
        tail = [ln for ln in out.strip().splitlines() if ln.strip()]
        j.step(name, "failed",
               f"could not read the drift summary (exit {rc}): "
               f"{tail[-1].strip()[:180] if tail else 'no output at all'}")


# ─────────────────────────────────────────────────────────────────────────────
# step 4 — workspace evidence index
# ─────────────────────────────────────────────────────────────────────────────
def step_rag(j: Journal, execute: bool) -> None:
    name = "rag evidence index"
    script = ROOT / "tools" / "obj013_rag_ingest.py"
    if not script.exists():
        j.step(name, "skipped", "obj013_rag_ingest.py not present")
        return
    if not execute:
        j.step(name, "dry-run", "would run: obj013_rag_ingest.py --apply")
        return

    rc, out = run_script("obj013_rag_ingest.py", "--apply", timeout=1800)
    tail = [ln for ln in out.strip().splitlines() if ln.strip()]
    if rc == 0:
        j.step(name, "ok", tail[-1].strip() if tail else "rebuilt")
    else:
        j.step(name, "failed", f"exit {rc}: {tail[-1].strip() if tail else 'no output'}")


# ─────────────────────────────────────────────────────────────────────────────
# step 5 — dashboard data
# ─────────────────────────────────────────────────────────────────────────────
def step_dashboard(j: Journal, execute: bool) -> None:
    name = "dashboard datasets"
    script = ROOT / "tools" / "obj015_build_dashboard_data.py"
    if not script.exists():
        j.step(name, "skipped", "obj015_build_dashboard_data.py not present")
        return
    if not execute:
        # Judge on the exit code, not on a string in the output: --verify deliberately writes
        # nothing and prints no verdict banner, so grepping for one always reported a failure.
        rc, _ = run_script("obj015_build_dashboard_data.py", "--verify", timeout=900)
        j.step(name, "dry-run",
               f"would run the generator; its self-verification currently "
               f"{'passes' if rc == 0 else f'FAILS (exit {rc}) — fix before scheduling'}")
        return

    rc, out = run_script("obj015_build_dashboard_data.py", timeout=1800)
    if rc != 0:
        tail = [ln for ln in out.strip().splitlines() if ln.strip()]
        j.step(name, "failed",
               f"generator exited {rc} — its self-check against the run workbook did not pass. "
               f"{tail[-1].strip() if tail else ''}")
        return
    written = len([ln for ln in out.splitlines() if ".json" in ln and "KB" in ln])
    j.step(name, "ok", f"regenerated {written} datasets; all self-checks against the run workbook pass",
           datasets=written)


# ─────────────────────────────────────────────────────────────────────────────
# refresh stamp — what the dashboard shows
# ─────────────────────────────────────────────────────────────────────────────
def write_refresh_stamp(j: Journal, execute: bool) -> None:
    """A tiny file the UI reads so a stale or failed refresh is visible on screen.

    Without this a failed 02:00 job looks exactly like a successful one: the dashboard would
    keep showing yesterday's figures with no indication they are yesterday's.
    """
    if not execute:
        j.step("refresh stamp", "dry-run", f"would write {APP_DATA.name}/refresh.json for the UI")
        return
    if not APP_DATA.is_dir():
        j.step("refresh stamp", "skipped", f"{APP_DATA} does not exist — is the app data directory in place?")
        return

    stamp = {
        "lastAttempt": j.started,
        "lastAttemptFinished": now(),
        "ok": not j.failed,
        "steps": [{k: v for k, v in s.items() if k in ("step", "status", "detail")} for s in j.steps],
        "failedSteps": [s["step"] for s in j.steps if s["status"] == "failed"],
        "generator": "tools/obj016_daily_refresh.py",
        "note": "Written by the daily job. 'ok' false means the figures on screen may be stale — "
                "the step list says which part failed.",
    }
    (APP_DATA / "refresh.json").write_text(json.dumps(stamp, indent=1), encoding="utf-8")
    j.step("refresh stamp", "ok", f"wrote refresh.json (ok={not j.failed})")


def persist(j: Journal) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state = {
        "started": j.started,
        "finished": now(),
        "dryRun": j.dry_run,
        "ok": not j.failed,
        "steps": j.steps,
    }
    STATE_FILE.write_text(json.dumps(state, indent=1), encoding="utf-8")
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(f"\n===== {j.started} ({'dry run' if j.dry_run else 'execute'}) =====\n")
        fh.write("\n".join(j.lines) + "\n")
        fh.write(f"result: {'OK' if not j.failed else 'FAILED'}\n")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--execute", action="store_true",
                    help="actually pull, fetch and write. Without it, nothing changes.")
    ap.add_argument("--skip-git", action="store_true",
                    help="refresh derived artifacts only; no fetch and no pull")
    args = ap.parse_args()
    execute = args.execute

    make_output_safe()
    j = Journal(dry_run=not execute)
    t0 = time.time()
    j.say("=" * 74)
    j.say(f"  OBJ-016 daily refresh — {'EXECUTE' if execute else 'DRY RUN (nothing will change)'}")
    j.say(f"  {j.started}")
    j.say("=" * 74)

    steps = []
    if args.skip_git:
        j.step("git", "skipped", "--skip-git was passed")
    else:
        steps += [step_pull_pam, step_fetch_bootstrap]
    steps += [step_drift, step_rag, step_dashboard]

    for fn in steps:
        try:
            fn(j, execute)
        except subprocess.TimeoutExpired as exc:
            j.step(fn.__name__, "failed", f"timed out after {exc.timeout}s")
        except Exception as exc:  # a broken step must not abort the rest of the job
            j.step(fn.__name__, "failed", f"{type(exc).__name__}: {exc}")

    try:
        write_refresh_stamp(j, execute)
    except Exception as exc:
        j.step("refresh stamp", "failed", f"{type(exc).__name__}: {exc}")

    j.say("-" * 74)
    counts: dict[str, int] = {}
    for s in j.steps:
        counts[s["status"]] = counts.get(s["status"], 0) + 1
    j.say("  " + " · ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    j.say(f"  elapsed {time.time() - t0:.1f}s · {'FAILED' if j.failed else 'OK'}")
    if not execute:
        j.say("  Nothing was changed. Re-run with --execute.")
    j.say("=" * 74)

    persist(j)
    return 1 if j.failed else 0


if __name__ == "__main__":
    sys.exit(main())
