#!/usr/bin/env python3
"""
obj017_weekly_execution.py — the weekly API execution.

OBJ-017. Runs the full dynamic-framework execution once a week, then folds its result into the
dashboard so the benchmark rolls forward on its own. Intended to be started by Windows Task
Scheduler every Sunday at 10:00.

    python tools\\obj017_weekly_execution.py               # DRY RUN, zero HTTP
    python tools\\obj017_weekly_execution.py --execute      # the real thing
    python tools\\obj017_weekly_execution.py --execute --resume-only  # finish a partial run

Deny-by-default, like every harness script here. A bare run issues **no HTTP at all** — not even
the health probe — and changes nothing.

⛔ THE THINGS THIS MUST NEVER DO
--------------------------------
· `--allow-teardown` / `--allow-preexisting-teardown` — would delete records
· `--include-unsafe` — re-enables GetLogs / GetErrorLogs / GetAllActiveUserDetails, which stop the
  IIS application pool and took the whole API to 503 in three requests (ISSUE-010)
· retry the token. ONE attempt, via token_guard, and only after the environment answers
· run Maven or a TestNG suite. "Execute" means the dynamic framework, per the standing rule
Those flags are asserted absent below, not merely omitted.

⚠️ WHY THERE IS A PRE-FLIGHT PROBE HERE RATHER THAN RELYING ON --wait-for-env
-----------------------------------------------------------------------------
`chain_runner` acquires the token at line ~993 and only *then* runs `--wait-for-env`, whose probe
needs that token. So its own wait cannot protect the credential. This job probes first, without any
credential, so a token is never spent against a host that cannot answer — which is the whole point
of the agreed token policy.

Exit codes: 0 complete · 1 a step failed · 2 aborted before execution (env down, or token latched).
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
SCRIPTS = ROOT / "tools"
RUNS_DIR = ROOT / "artifacts" / "runs"
STATE_DIR = ROOT / "state" / "weekly"
STATE_FILE = STATE_DIR / "last-run.json"
LOG_FILE = STATE_DIR / "weekly.log"
APP_DATA = ROOT / "tools" / "dashboard" / "public" / "data"

ENV_PROPS = (ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
             / "Environments" / "QA_MsSQL.properties")
TOKEN_LATCH = SCRIPTS / ".token_attempt_block.json"

# Agreed execution shape: the full suite inside a six-hour wall clock. --budget-seconds recomputes
# the inter-call delay each hop to land inside the window, with a 250 ms floor.
# OBJ-020: the Sunday 2026-08-16 run was killed by this ceiling (outer timeout fired at
# BUDGET_SECONDS + 1800 = 23400 s) with 431 of 744 flows still outstanding, so the owner raised the
# per-attempt budget for a resume. --budget-seconds overrides it; the scheduled Sunday job is
# unchanged and still runs at six hours.
BUDGET_SECONDS = 6 * 3600
DELAY_MS = 2000
ALLOW_VERBS = "GET,POST,PUT,PATCH"      # as run N did; PUT/PATCH exist for the QA team's rows
ENV_WAIT_MINUTES = 45                   # how long to wait for the host before giving up
SUBSTANTIVE_MIN_EXECUTED = 100

FORBIDDEN_FLAGS = ("--allow-teardown", "--allow-preexisting-teardown", "--include-unsafe")

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE     # the QA host serves a self-signed certificate

_lines: list[str] = []


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def rel(path: Path) -> str:
    """Workspace-relative path for display, falling back to absolute.

    `Path.relative_to` RAISES for anything outside the workspace, and this is used inside error
    reporting — the one place a second exception is least welcome.
    """
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def say(msg: str) -> None:
    print(msg)
    _lines.append(msg)


def make_output_safe() -> None:
    """Task Scheduler gives no console, so stdout defaults to the ANSI codepage and dies on ⛔."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except (AttributeError, ValueError):
            pass


def child_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


class Journal:
    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self.started = now()
        self.steps: list[dict] = []

    def step(self, name: str, status: str, detail: str, **extra) -> dict:
        rec = {"step": name, "status": status, "detail": detail, **extra}
        self.steps.append(rec)
        icon = {"ok": "  OK  ", "skipped": " SKIP ", "failed": " FAIL ",
                "dry-run": " DRY  ", "aborted": "ABORT "}[status]
        say(f"[{icon}] {name}: {detail}")
        return rec

    @property
    def failed(self) -> bool:
        return any(s["status"] in ("failed", "aborted") for s in self.steps)

    @property
    def aborted(self) -> bool:
        return any(s["status"] == "aborted" for s in self.steps)


def run_script(script: str, *args: str, timeout: int) -> tuple[int, str]:
    for bad in FORBIDDEN_FLAGS:
        if bad in args:
            raise RuntimeError(f"refused: {bad} must never be passed by an unattended run")
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True, cwd=str(ROOT), timeout=timeout,
        encoding="utf-8", errors="replace", env=child_env(),
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def api_base() -> str | None:
    if not ENV_PROPS.exists():
        return None
    for line in ENV_PROPS.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("pam_BaseAPIURL="):
            return line.split("=", 1)[1].strip().rstrip("/")
    return None


def host_answers(base: str, timeout: int = 20) -> tuple[bool, str]:
    """Unauthenticated liveness probe against the site root.

    Deliberately hits `/` and NOT an API action: it carries no credential, touches no endpoint on
    the safety blocklist, and still distinguishes the failure mode that matters. A dead IIS
    application pool answers 503 for the whole site, which is exactly the state that wrecked the
    last full run.

    Anything below 500 means the host is serving — 401/403/404 are all fine for a liveness check.
    """
    try:
        req = urllib.request.Request(base + "/", method="GET")
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as r:
            return (r.status < 500), f"HTTP {r.status}"
    except urllib.error.HTTPError as exc:
        return (exc.code < 500), f"HTTP {exc.code}"
    except Exception as exc:                                          # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def run_folders() -> set[str]:
    return {p.name for p in RUNS_DIR.iterdir() if p.is_dir()}


def executed_in(run_id: str) -> int:
    p = RUNS_DIR / run_id / "results.json"
    if not p.exists():
        return 0
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    n = 0
    for f in data.get("flows", []):
        for h in f.get("hops", []):
            if h.get("checks"):
                n += 1
    return n


def substantive_runs() -> list[str]:
    """Newest first. Same definition the dashboard generator uses."""
    out = []
    for p in sorted((d for d in RUNS_DIR.iterdir() if d.is_dir()),
                    key=lambda d: d.name, reverse=True):
        if executed_in(p.name) >= SUBSTANTIVE_MIN_EXECUTED:
            out.append(p.name)
    return out


def aborted_flows(run_id: str) -> list[str]:
    """Flows the runner marked ABORTED — they reached the checkpoint without executing."""
    for name in ("results.json", "checkpoint.json"):
        p = RUNS_DIR / run_id / name
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        flows = data.get("flows", data if isinstance(data, list) else [])
        ids = [f.get("id") for f in flows if isinstance(f, dict) and f.get("verdict") == "ABORTED"]
        if ids:
            return [i for i in ids if i]
    return []


# ─────────────────────────────────────────────────────────────────────────────
# steps
# ─────────────────────────────────────────────────────────────────────────────
def step_token_latch(j: Journal) -> bool:
    """Zero HTTP. If a previous token attempt failed, nothing may proceed until a human clears it."""
    name = "token latch check"
    if TOKEN_LATCH.exists():
        try:
            info = json.loads(TOKEN_LATCH.read_text(encoding="utf-8"))
        except Exception:                                             # noqa: BLE001
            info = {}
        j.step(name, "aborted",
               f"⛔ a previous token attempt FAILED and latched — no attempt will be made in this "
               f"run or any future one until a human clears it. "
               f"Reason on record: {info.get('reason', 'not recorded')}. "
               f"Clear with: python tools\\token_guard.py clear-latch",
               latchFile=rel(TOKEN_LATCH))
        return False
    j.step(name, "ok", "no latch — one token attempt is permitted this run")
    return True


def step_env_probe(j: Journal, execute: bool) -> bool:
    name = "environment pre-flight"
    base = api_base()
    if not base:
        j.step(name, "failed", f"could not read pam_BaseAPIURL from {ENV_PROPS.name}")
        return False

    if not execute:
        j.step(name, "dry-run",
               f"would probe {base}/ unauthenticated, waiting up to {ENV_WAIT_MINUTES} min. "
               f"No HTTP is issued in a dry run")
        return True

    deadline = time.time() + ENV_WAIT_MINUTES * 60
    attempt = 0
    while True:
        attempt += 1
        up, detail = host_answers(base)
        if up:
            j.step(name, "ok",
                   f"{base} answered {detail}"
                   + (f" after {attempt} probes" if attempt > 1 else "")
                   + ". Safe to spend a token",
                   base=base, probes=attempt)
            return True
        if time.time() >= deadline:
            j.step(name, "aborted",
                   f"⛔ {base} did not answer within {ENV_WAIT_MINUTES} min (last: {detail}). "
                   f"Nothing was executed and NO token was requested — the credential is intact. "
                   f"The next scheduled run will try again",
                   base=base, probes=attempt, lastError=detail)
            return False
        say(f"         host not answering ({detail}) — retrying in 60 s")
        time.sleep(60)


def step_generate(j: Journal, execute: bool) -> bool:
    name = "generate flows"
    if not execute:
        j.step(name, "dry-run", "would run generate_flows.py then generate_data_flows.py")
        return True
    for script in ("generate_flows.py", "generate_data_flows.py"):
        rc, out = run_script(script, timeout=1800)
        if rc != 0:
            tail = [ln for ln in out.strip().splitlines() if ln.strip()]
            j.step(name, "failed", f"{script} exited {rc}: {tail[-1][:180] if tail else 'no output'}")
            return False
    j.step(name, "ok", "positive and data-driven flows regenerated from the current corpus")
    return True


def step_execute(j: Journal, execute: bool) -> str | None:
    """Returns the new run's folder name, or None."""
    name = "execute suite"
    args = ["--execute",
            "--budget-seconds", str(BUDGET_SECONDS),
            "--delay-ms", str(DELAY_MS),
            "--allow-verbs", ALLOW_VERBS,
            "--wait-for-env", "15"]
    if not execute:
        j.step(name, "dry-run",
               f"would run: chain_runner.py {' '.join(args)}  "
               f"(no teardown, no unsafe endpoints)")
        return None

    before = run_folders()
    # +30 min of headroom over the budget so the runner finishes and writes its report itself.
    rc, out = run_script("chain_runner.py", *args, timeout=BUDGET_SECONDS + 1800)
    new = sorted(run_folders() - before)

    if not new:
        tail = [ln for ln in out.strip().splitlines() if ln.strip()]
        j.step(name, "failed",
               f"chain_runner exited {rc} and created no run folder: "
               f"{tail[-1][:200] if tail else 'no output'}")
        return None

    run_id = new[-1]
    n = executed_in(run_id)
    ab = aborted_flows(run_id)
    if rc != 0:
        j.step(name, "failed",
               f"chain_runner exited {rc} after {n} executed test cases in {run_id}"
               + (f"; {len(ab)} flow(s) ABORTED" if ab else ""),
               runId=run_id, executed=n, aborted=len(ab))
    else:
        j.step(name, "ok", f"{n} test cases executed into {run_id}"
                           + (f"; {len(ab)} flow(s) ABORTED" if ab else ""),
               runId=run_id, executed=n, aborted=len(ab))
    return run_id


def step_resume(j: Journal, run_id: str, execute: bool) -> None:
    """One resume, then stop. Agreed policy: a transient failure gets one retry, never a loop."""
    name = "resume once"
    if not execute:
        j.step(name, "dry-run",
               "would resume the run ONCE if any flow came back ABORTED, then stop either way")
        return
    ab = aborted_flows(run_id)
    if not ab:
        j.step(name, "skipped", "no ABORTED flow — nothing to resume")
        return

    say(f"         {len(ab)} ABORTED flow(s); resuming {run_id} once")
    # chain_runner resolves a relative --resume against artifacts/runs itself, so this must be the
    # BARE run id. Passing "artifacts/runs/<id>" made it search artifacts/runs/artifacts/runs/<id>
    # and exit 2 -- this resume path had never once succeeded (OBJ-020).
    rc, out = run_script("chain_runner.py", "--execute", "--resume", run_id,
                         "--budget-seconds", str(BUDGET_SECONDS),
                         "--delay-ms", str(DELAY_MS),
                         "--allow-verbs", ALLOW_VERBS,
                         timeout=BUDGET_SECONDS + 1800)
    still = aborted_flows(run_id)
    if rc == 0 and not still:
        j.step(name, "ok", f"resume completed; no flow left ABORTED ({executed_in(run_id)} executed)")
    else:
        j.step(name, "failed",
               f"resume exited {rc} and {len(still)} flow(s) are still ABORTED. "
               f"⛔ Not retrying again — the run is kept and flagged as incomplete",
               aborted=len(still))


def step_validate(j: Journal, run_id: str, execute: bool) -> None:
    name = "validation gate"
    if not execute:
        j.step(name, "dry-run", "would run obj010_collect.py <run>")
        return
    rc, out = run_script("obj010_collect.py", f"artifacts/runs/{run_id}", timeout=1800)
    # A non-zero exit means a gate failed, which is a finding about the run, not a broken step.
    vj = RUNS_DIR / run_id / "validation.json"
    if not vj.exists():
        j.step(name, "failed", f"obj010_collect.py exited {rc} and wrote no validation.json")
        return
    try:
        v = json.loads(vj.read_text(encoding="utf-8"))
        checks = v.get("checklist", [])
        passed = sum(1 for c in checks if str(c.get("verdict", "")).upper().startswith(("PASS", "✅")))
        j.step(name, "ok", f"{passed} of {len(checks)} gates passed", gatesPassed=passed,
               gatesTotal=len(checks))
    except Exception as exc:                                          # noqa: BLE001
        j.step(name, "failed", f"validation.json unreadable: {exc}")


def step_workbook(j: Journal, run_id: str, execute: bool) -> None:
    name = "run workbook"
    if not execute:
        j.step(name, "dry-run", "would run obj010_build_workbook.py <run> --baseline <previous>")
        return
    subs = [r for r in substantive_runs() if r != run_id]
    if not subs:
        j.step(name, "failed", "no previous substantive run to use as a baseline")
        return
    baseline = subs[0]
    rc, out = run_script("obj010_build_workbook.py", f"artifacts/runs/{run_id}",
                         "--baseline", f"artifacts/runs/{baseline}", timeout=1800)
    wb = RUNS_DIR / run_id / "QA_MsSQL_API_Execution.xlsx"
    if rc == 0 and wb.exists():
        j.step(name, "ok", f"built against baseline {baseline} ({wb.stat().st_size / 1024:.0f} KB)",
               baseline=baseline)
    else:
        tail = [ln for ln in out.strip().splitlines() if ln.strip()]
        j.step(name, "failed",
               f"exited {rc}; the dashboard cannot promote this run without its workbook. "
               f"{tail[-1][:180] if tail else ''}")


def step_dashboard(j: Journal, execute: bool) -> None:
    name = "dashboard datasets"
    if not execute:
        j.step(name, "dry-run", "would regenerate the dashboard datasets (resolves N automatically)")
        return
    rc, out = run_script("obj015_build_dashboard_data.py", timeout=1800)
    if rc != 0:
        tail = [ln for ln in out.strip().splitlines() if ln.strip()]
        j.step(name, "failed",
               f"generator exited {rc} — its self-check against the run workbook did not pass. "
               f"{tail[-1][:180] if tail else ''}")
        return
    cur = ""
    for ln in out.splitlines():
        if "resolved" in ln.lower() or "current run" in ln.lower():
            cur = ln.strip()
    j.step(name, "ok", f"regenerated; N is now the newest substantive run. {cur}".strip())


def write_execution_stamp(j: Journal, run_id: str | None, execute: bool) -> None:
    name = "execution stamp"
    if not execute:
        j.step(name, "dry-run", "would write data/execution.json for the dashboard")
        return
    if not APP_DATA.is_dir():
        j.step(name, "skipped", f"{APP_DATA} does not exist")
        return
    payload = {
        "lastAttempt": j.started,
        "lastAttemptFinished": now(),
        "ok": not j.failed,
        "aborted": j.aborted,
        "runId": run_id,
        "executed": executed_in(run_id) if run_id else None,
        "abortedFlows": len(aborted_flows(run_id)) if run_id else None,
        "steps": [{k: v for k, v in s.items() if k in ("step", "status", "detail")} for s in j.steps],
        "failedSteps": [s["step"] for s in j.steps if s["status"] in ("failed", "aborted")],
        "schedule": "Sundays 10:00, Windows task PAM-Weekly-API-Execution",
        "generator": "tools/obj017_weekly_execution.py",
        "note": "The weekly full execution. 'aborted' true means the run never started — most often "
                "the environment did not answer, in which case no token was spent.",
    }
    (APP_DATA / "execution.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")
    j.step(name, "ok", f"wrote execution.json (ok={not j.failed})")


def persist(j: Journal, run_id: str | None) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({
        "started": j.started, "finished": now(), "dryRun": j.dry_run,
        "ok": not j.failed, "aborted": j.aborted, "runId": run_id, "steps": j.steps,
    }, indent=1), encoding="utf-8")
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(f"\n===== {j.started} ({'dry run' if j.dry_run else 'execute'}) =====\n")
        fh.write("\n".join(_lines) + "\n")
        fh.write(f"result: {'OK' if not j.failed else 'FAILED'}  run: {run_id or 'none'}\n")


def main() -> int:
    global BUDGET_SECONDS
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--execute", action="store_true",
                    help="actually execute. Without it, nothing runs and no HTTP is issued.")
    ap.add_argument("--resume-only", metavar="RUN",
                    help="skip generation and execution; resume this run, then finish the chain")
    ap.add_argument("--no-generate", action="store_true",
                    help="skip flow regeneration and execute the flow set already on disk. Required "
                         "for a reproducibility re-run (OBJ-023): a regenerated corpus is not "
                         "comparable hop-for-hop against the run being reproduced.")
    ap.add_argument("--budget-seconds", type=int, default=BUDGET_SECONDS, metavar="S",
                    help=f"wall-clock budget handed to chain_runner (default {BUDGET_SECONDS}). "
                         "The outer subprocess timeout is this + 1800 s of headroom.")
    args = ap.parse_args()
    execute = args.execute

    if args.budget_seconds != BUDGET_SECONDS:
        say(f"  budget override: {BUDGET_SECONDS} s -> {args.budget_seconds} s "
            f"({args.budget_seconds / 3600:.1f} h per attempt)")
        BUDGET_SECONDS = args.budget_seconds

    make_output_safe()
    j = Journal(dry_run=not execute)
    t0 = time.time()
    say("=" * 74)
    say(f"  OBJ-017 weekly API execution — {'EXECUTE' if execute else 'DRY RUN (no HTTP at all)'}")
    say(f"  {j.started}")
    say("=" * 74)

    run_id: str | None = args.resume_only

    try:
        # 1 & 2 — never spend a credential against a host that cannot answer
        if not step_token_latch(j):
            persist(j, None)
            return 2
        if not step_env_probe(j, execute):
            persist(j, None)
            return 2

        if args.resume_only:
            j.step("generate flows", "skipped", "--resume-only")
            j.step("execute suite", "skipped", f"--resume-only: resuming {run_id}")
        elif args.no_generate:
            j.step("generate flows", "skipped",
                   "--no-generate: executing the flow set already on disk, unchanged, so the run "
                   "stays comparable hop-for-hop against the run being reproduced")
            run_id = step_execute(j, execute)
        else:
            if not step_generate(j, execute):
                persist(j, None)
                return 1
            run_id = step_execute(j, execute)

        # In a dry run there is no real run folder, but every downstream step must still report
        # what it *would* do — a dry run is how this job gets checked before a Sunday.
        if not execute and not run_id:
            run_id = "<the run this would create>"

        if execute and not run_id:
            say("-" * 74)
            say("  no run folder was produced — stopping before the reporting chain")
            persist(j, None)
            return 1

        if run_id:
            step_resume(j, run_id, execute)
            step_validate(j, run_id, execute)
            step_workbook(j, run_id, execute)
        step_dashboard(j, execute)
        write_execution_stamp(j, run_id, execute)

    except subprocess.TimeoutExpired as exc:
        j.step("weekly execution", "failed", f"timed out after {exc.timeout}s")
    except Exception as exc:                                          # noqa: BLE001
        j.step("weekly execution", "failed", f"{type(exc).__name__}: {exc}")

    say("-" * 74)
    counts: dict[str, int] = {}
    for s in j.steps:
        counts[s["status"]] = counts.get(s["status"], 0) + 1
    say("  " + " · ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    say(f"  elapsed {(time.time() - t0) / 60:.1f} min · run {run_id or 'none'} · "
        f"{'FAILED' if j.failed else 'OK'}")
    if not execute:
        say("  Nothing was changed and no HTTP was issued. Re-run with --execute.")
    say("=" * 74)

    persist(j, run_id)
    return 1 if j.failed else 0


if __name__ == "__main__":
    sys.exit(main())
