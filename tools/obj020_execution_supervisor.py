#!/usr/bin/env python3
"""
OBJ-020 - unattended execution supervisor.

Owns the owner's retry policy for a long API execution so that completion does NOT depend on any
interactive session staying alive. Launched detached; it writes its state to disk and keeps going
through anything that happens to the terminal that started it.

    python obj020_execution_supervisor.py                      # DRY RUN - prints the plan, no HTTP
    python obj020_execution_supervisor.py --execute            # resume the pinned run for real

Retry policy (owner instruction, 2026-08-18):
  * A timeout / temporary deployment / backend interruption is NOT a permanent failure.
  * Wait 30 minutes, then retry. Repeat.
  * At least FIVE retry intervals before the window is allowed to close.
  * Stop only when the execution completes, or when failures have run continuously past 12 hours.
  * Do not report every transient failure - report at the end.

Token safety (this is the part that must never be "improved" into a loop):
  The bearer token is resolved ONCE by the launcher and pinned into this process's environment as
  $PAM_API_TOKEN. token_guard.py resolves $PAM_API_TOKEN before anything else, so every retry below
  reuses that one token and NO retry ever reaches /arcontoken. Retry-on-failure against that
  endpoint is what locked the shared GenericScheduler account in July; the pin is what makes an
  unattended retry loop safe here.
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

SCRIPTS = Path(__file__).resolve().parent
from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
STATE_DIR = ROOT / "state" / "weekly"
STATE = STATE_DIR / "obj020-supervisor.json"
LOG = STATE_DIR / "obj020-supervisor.log"
RUNS = ROOT / "artifacts" / "runs"

RESUME_RUN = "2026-08-16_100005"
BUDGET_SECONDS = 12 * 3600          # owner decision: 12 h per attempt
RETRY_WAIT_S = 30 * 60              # owner decision: 30 minutes between attempts
MIN_RETRIES = 5                     # owner decision: at least five intervals
MAX_FAILURE_WINDOW_S = 12 * 3600    # owner decision: give up after 12 h of continuous failure

FORBIDDEN = ("--allow-teardown", "--allow-preexisting-teardown", "--include-unsafe")


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def say(msg: str) -> None:
    line = f"[{now()}] {msg}"
    print(line, flush=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def child_env() -> dict[str, str]:
    """A child Python launched detached has no console and picks the ANSI codepage; forcing UTF-8
    is what stops it dying while printing a non-ASCII status character."""
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def flow_state(run_id: str) -> dict:
    """How far the run actually got, straight from its checkpoint."""
    ck = RUNS / run_id / "checkpoint.json"
    if not ck.exists():
        return {"checkpoint": False}
    try:
        flows = json.loads(ck.read_text(encoding="utf-8")).get("flows", [])
    except (OSError, json.JSONDecodeError):
        return {"checkpoint": False}
    verdicts: dict[str, int] = {}
    for f in flows:
        v = f.get("verdict") or "UNKNOWN"
        verdicts[v] = verdicts.get(v, 0) + 1
    return {
        "checkpoint": True,
        "flowsRecorded": len(flows),
        "verdicts": verdicts,
        "aborted": verdicts.get("ABORTED", 0),
        "reportWritten": (RUNS / run_id / "RUN_REPORT.md").exists(),
    }


def newest_run() -> str | None:
    """Newest run folder on disk. Used to discover the folder a fresh execution just minted."""
    if not RUNS.is_dir():
        return None
    names = sorted(d.name for d in RUNS.iterdir() if d.is_dir())
    return names[-1] if names else None


def persist(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")


def attempt(n: int, execute: bool, run_id: str | None) -> tuple[bool, str, str]:
    """One attempt. With run_id, resumes it; without, starts a fresh run (OBJ-023).

    A fresh run never regenerates flows: a reproducibility re-run is only comparable against the
    run it reproduces if the flow set is byte-identical.
    """
    args = [sys.executable, str(SCRIPTS / "obj017_weekly_execution.py"), "--execute"]
    if run_id:
        args += ["--resume-only", run_id]
    else:
        args += ["--no-generate"]
    args += ["--budget-seconds", str(BUDGET_SECONDS)]
    assert not any(f in args for f in FORBIDDEN), "forbidden execution flag"

    if not execute:
        return True, f"DRY RUN - would run: {' '.join(args[1:])}", (run_id or "<fresh run>")

    say(f"attempt {n}: starting (budget {BUDGET_SECONDS / 3600:.0f} h)")
    t0 = time.time()
    try:
        proc = subprocess.run(args, cwd=str(ROOT), env=child_env(),
                              capture_output=True, text=True,
                              timeout=BUDGET_SECONDS + 3600)
        rc = proc.returncode
        tail = [ln for ln in (proc.stdout or "").strip().splitlines() if ln.strip()]
        detail = tail[-1][:300] if tail else f"exit {rc}, no output"
    except subprocess.TimeoutExpired:
        rc, detail = -1, f"outer timeout after {BUDGET_SECONDS + 3600}s"
    mins = (time.time() - t0) / 60

    # A fresh run mints its own folder; find the newest one this attempt produced.
    if not run_id:
        run_id = newest_run() or RESUME_RUN
        say(f"attempt {n}: fresh run folder is {run_id}")
    fs = flow_state(run_id)
    # ⛔ Judge the RUN, not obj017's exit code. obj017 exits non-zero when any step failed, and a
    # downstream reporting step can fail for reasons that have nothing to do with the execution —
    # a dashboard self-check, for instance. Gating on rc made this supervisor re-run an execution
    # that had completed at 07:23 five more times before a human noticed. The run is done when its
    # own artefacts say so: no aborted flow, a report, and results.json on disk.
    ok = bool(fs.get("aborted", 1) == 0
              and fs.get("reportWritten")
              and (RUNS / run_id / "results.json").exists())
    if ok and rc != 0:
        say(f"attempt {n}: obj017 exited {rc}, but the run itself is complete "
            f"(no aborted flow, report and results.json present). Treating as done; "
            f"the non-zero exit belongs to a downstream reporting step, not the execution.")
    say(f"attempt {n}: {'OK' if ok else 'FAILED'} after {mins:.1f} min - {detail}")
    say(f"attempt {n}: checkpoint now {fs.get('flowsRecorded', 0)} flows, "
        f"{fs.get('aborted', 0)} aborted, report={fs.get('reportWritten')}")
    return ok, detail, run_id


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--execute", action="store_true",
                    help="actually run. Without it nothing is executed and no HTTP is issued.")
    ap.add_argument("--fresh", action="store_true",
                    help="start a NEW full execution against the flow set already on disk "
                         "(OBJ-023 reproducibility re-run) instead of resuming an existing run. "
                         "Retries after the first attempt resume the run it created.")
    ap.add_argument("--resume", metavar="RUN", default=RESUME_RUN,
                    help=f"run folder to resume (default {RESUME_RUN}). Ignored with --fresh.")
    ap.add_argument("--label", default="API execution resume",
                    help="what this supervision is for, recorded in the state file.")
    args = ap.parse_args()

    run_id: str | None = None if args.fresh else args.resume

    state = {
        "objective": "OBJ-023" if args.fresh else "OBJ-020",
        "activity": args.label,
        "mode": "fresh full execution (no flow regeneration)" if args.fresh else "resume",
        "run": run_id or "(a fresh run folder will be minted)",
        "comparisonBaseline": RESUME_RUN if args.fresh else None,
        "startedAt": now(),
        "policy": {
            "budgetSecondsPerAttempt": BUDGET_SECONDS,
            "retryWaitSeconds": RETRY_WAIT_S,
            "minRetries": MIN_RETRIES,
            "maxContinuousFailureSeconds": MAX_FAILURE_WINDOW_S,
        },
        "tokenPinned": bool(os.environ.get("PAM_API_TOKEN")),
        "status": "running",
        "attempts": [],
        "flowStateAtStart": flow_state(run_id) if run_id else {"checkpoint": False},
    }
    persist(state)

    say("=" * 70)
    say(f"supervisor - {args.label} - {'EXECUTE' if args.execute else 'DRY RUN'}")
    say(f"mode: {state['mode']}  target: {state['run']}")
    say(f"token pinned in env: {state['tokenPinned']}")
    say(f"at start: {state['flowStateAtStart']}")
    say("=" * 70)

    if not state["tokenPinned"] and args.execute:
        say("STOP: $PAM_API_TOKEN is not set. Refusing to run - a retry loop without a pinned "
            "token would attempt /arcontoken on every cycle.")
        state["status"] = "refused"
        state["reason"] = "PAM_API_TOKEN not pinned"
        persist(state)
        return 2

    first_failure: float | None = None
    n = 0
    while True:
        n += 1
        ok, detail, run_id = attempt(n, args.execute, run_id)
        state["run"] = run_id
        state["attempts"].append({
            "n": n, "at": now(), "ok": ok, "detail": detail, "run": run_id,
            "flowState": flow_state(run_id),
        })
        persist(state)

        if ok:
            state["status"] = "completed"
            state["finishedAt"] = now()
            persist(state)
            say(f"COMPLETED after {n} attempt(s)")
            return 0

        if not args.execute:
            state["status"] = "dry-run"
            persist(state)
            return 0

        if first_failure is None:
            first_failure = time.time()
        failing_for = time.time() - first_failure
        retries_done = n - 1

        # Owner policy: honour at least five intervals even if the 12 h window has passed, and
        # keep going until the window closes.
        if retries_done >= MIN_RETRIES and failing_for >= MAX_FAILURE_WINDOW_S:
            state["status"] = "abandoned"
            state["finishedAt"] = now()
            state["reason"] = (f"failed continuously for {failing_for / 3600:.1f} h across "
                               f"{n} attempts - past the 12 h ceiling")
            persist(state)
            say(f"STOPPING: {state['reason']}")
            return 1

        say(f"attempt {n} failed; failing for {failing_for / 3600:.1f} h; "
            f"waiting {RETRY_WAIT_S // 60} min before attempt {n + 1}")
        state["status"] = f"waiting (attempt {n + 1} at +{RETRY_WAIT_S // 60}min)"
        persist(state)
        time.sleep(RETRY_WAIT_S)


if __name__ == "__main__":
    sys.exit(main())
