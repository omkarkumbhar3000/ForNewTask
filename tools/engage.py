#!/usr/bin/env python3
"""
engage.py - one-word workspace readiness for DevProjects.

OBJ-026. Inspect -> Synchronize -> Analyze -> Validate -> Prepare -> Summarize. Brings the
workspace into a safe, synchronized, understood state and reports what changed, what needs
attention, and what to do next.

    python tools\\engage.py                # the full sequence
    python tools\\engage.py --dry-run      # decide everything, change nothing
    python tools\\engage.py --no-refresh   # skip the derived-data refresh
    python tools\\engage.py --offline      # no fetch; classify against local refs
    python tools\\engage.py --json         # machine-readable context on stdout

Safe by default, not deny by default
------------------------------------
Every other script in this directory requires `--execute`, because they run unattended and can
issue HTTP to a shared environment. `engage` is different and the difference is deliberate (D31):
it is invoked by a human, issues **zero** HTTP to the product, and its only state changes are
`git fetch` and a guarded `git pull --ff-only`. Neither can lose work - `--ff-only` cannot create
a merge commit and refuses outright on a dirty tree. Requiring a second flag would defeat the one
thing this is for.

What it will never do
---------------------
  · push, merge, rebase, reset, checkout, stash, clean, or resolve a conflict
  · pull a repository that is dirty, diverged, detached, or mid-operation
  · pull a repository the owner has not classified in engage_core.POLICIES
  · call /arcontoken, the PAM API, or any endpoint - it issues no product HTTP at all
  · run the API suite, the weekly execution, or apply drift auto-fixes
  · delete anything

Reuse
-----
The synchronize half of this already existed. `obj016_daily_refresh.py` supplies `Journal`,
`child_env()`, `make_output_safe()` and the FORBIDDEN list, and `engage` calls that script rather
than reimplementing the derived-data refresh. `engage_core` owns discovery and the decision table.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engage_core as core                                            # noqa: E402
from obj016_daily_refresh import Journal, child_env, make_output_safe, now  # noqa: E402

ROOT = core.ROOT
STATE_DIR = ROOT / "state" / "engage"
TOOLS_DIR = ROOT / "tools"      # where control_center.py lives
CONTEXT_FILE = STATE_DIR / "context.json"
BRIEFING_FILE = STATE_DIR / "briefing.md"
LOG_FILE = STATE_DIR / "engage.log"

# ── Every workspace path engage binds to, in one place ──────────────────────────────────────
# OBJ-025 will move some of these. Keeping them in one block means that restructure re-points
# engage with a single edit instead of a search across the file.
PATHS = {
    "objective":      ROOT / "BLAST" / "Objective.md",
    "register":       ROOT / "docs/history/README.md",
    "daily_state":    ROOT / "state" / "daily" / "last-run.json",
    "weekly_state":   ROOT / "state" / "weekly" / "last-run.json",
    "drift_report":   ROOT / "state" / "drift" / "drift-report.json",
    "runs":           ROOT / "artifacts" / "runs",
    "resume_points":  [ROOT / "state" / "weekly" / "OBJ-023-RESUME.md",
                       ROOT / "state" / "perf" / "OBJ-019-STATE.md"],
    "scripts":        ROOT / "tools",
}

# Files whose presence together identifies this workspace. `engage` refuses to act anywhere else.
WORKSPACE_MARKERS = ["CLAUDE.md", "BLAST/Objective.md", "tools/engage_core.py"]

REFRESH_STALE_HOURS = 24
SEVERITY_ORDER = {"critical": 0, "high": 1, "normal": 2, "low": 3, "info": 4}
SEVERITY_LABEL = {"critical": "CRITICAL", "high": "HIGH", "normal": "NORMAL",
                  "low": "LOW", "info": "INFO"}


# ═══════════════════════════════════════════════════════════════════════════════════════════
# helpers
# ═══════════════════════════════════════════════════════════════════════════════════════════
def is_workspace(root: Path) -> bool:
    return all((root / m).exists() for m in WORKSPACE_MARKERS)


def read_json(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def age_hours(ts: datetime | None) -> float | None:
    if ts is None:
        return None
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - ts).total_seconds() / 3600


def human_age(hours: float | None) -> str:
    if hours is None:
        return "never"
    if hours < 1:
        return f"{int(hours * 60)} min ago"
    if hours < 48:
        return f"{hours:.0f} h ago"
    return f"{hours / 24:.0f} days ago"


class Attention:
    """One thing that needs the owner, with an honest provenance label.

    `source` is not decoration. "engage measured this just now" and "a project file says this"
    fail in different ways, and a briefing that blurs them invites acting on a stale claim as if
    it were fresh. The third value, `needs-confirmation`, marks an item engage will not act on
    at all.
    """

    def __init__(self, priority: str, text: str, source: str, action: str | None = None):
        self.priority, self.text, self.source, self.action = priority, text, source, action

    def to_dict(self) -> dict:
        return {"priority": self.priority, "text": self.text,
                "source": self.source, "action": self.action}


# ═══════════════════════════════════════════════════════════════════════════════════════════
# phase 1-2 - inspect and synchronize
# ═══════════════════════════════════════════════════════════════════════════════════════════
def sync_repositories(j: Journal, dry_run: bool, offline: bool) -> list[dict]:
    """Discover, fetch, classify, and fast-forward what is safe to fast-forward."""
    results: list[dict] = []
    discovered = core.discover_repos(ROOT)
    j.say(f"  discovered {len(discovered)} repositories")

    for path, rel in discovered:
        pol, known = core.policy_for(rel)

        # Fetch first: ahead/behind are read from remote-tracking refs, which are only current
        # after a fetch. Classifying before fetching would report yesterday's position.
        fetched = False
        fetch_note = ""
        if not offline and not dry_run:
            probe = core.inspect_repo(path, rel)
            if probe.remotes:
                rc, out = core.run_git(path, "fetch", "--all", "--quiet", "--no-tags")
                fetched = rc == 0
                if not fetched:
                    fetch_note = out.strip().splitlines()[-1][:160] if out.strip() else "fetch failed"

        st = core.inspect_repo(path, rel)
        plan = core.classify(st, pol, known)

        rec: dict = {
            "rel": rel, "name": pol.name, "known": known, "policy": pol.pull,
            "state": st.to_dict(), "action": plan.action, "reason": plan.reason,
            "severity": plan.severity, "needs_confirmation": plan.needs_confirmation,
            "attention": plan.attention, "fetched": fetched, "fetch_error": fetch_note,
            "pulled": False, "commits": [], "files": {},
        }

        if plan.action == "pull" and not dry_run:
            before = st.head
            rc, out = core.run_git(path, "pull", "--ff-only", "--quiet")
            if rc == 0:
                after = core.inspect_repo(path, rel).head
                rec.update(pulled=True, before=before, after=after,
                           pulled_commits=st.behind)
                rec["commits"] = changed_commits(path, before, after)
                rec["files"] = changed_files(path, before, after)
                j.step(f"pull {rel}", "ok", f"fast-forwarded {before} -> {after} "
                                            f"({st.behind} commit(s))")
            else:
                # A refused fast-forward is information, not a failure to route around.
                rec.update(action="skip", severity="high",
                           reason=f"fast-forward refused: {out.strip()[:160]}",
                           attention=f"{rel}: fast-forward refused by git - {out.strip()[:160]}")
                j.step(f"pull {rel}", "failed", rec["reason"])
        elif plan.action == "pull" and dry_run:
            j.step(f"pull {rel}", "dry-run", f"would fast-forward {st.behind} commit(s)")
        else:
            status = "skipped" if plan.action == "skip" else "ok"
            j.step(rel, status, plan.reason)

        results.append(rec)
    return results


def changed_commits(repo: Path, before: str, after: str, limit: int = 8) -> list[dict]:
    rc, out = core.run_git(repo, "log", "--no-merges", f"--max-count={limit}",
                           "--pretty=format:%h\x1f%an\x1f%s", f"{before}..{after}")
    if rc != 0:
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split("\x1f")
        if len(parts) == 3:
            rows.append({"sha": parts[0], "author": parts[1], "subject": parts[2]})
    return rows


def changed_files(repo: Path, before: str, after: str) -> dict:
    rc, out = core.run_git(repo, "diff", "--name-status", f"{before}..{after}")
    if rc != 0:
        return {}
    added = modified = deleted = 0
    names: list[str] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        code = line[0]
        added += code == "A"
        modified += code == "M"
        deleted += code == "D"
        if len(names) < 12:
            names.append(line.split("\t", 1)[-1])
    return {"added": added, "modified": modified, "deleted": deleted,
            "total": added + modified + deleted, "sample": names}


# ═══════════════════════════════════════════════════════════════════════════════════════════
# phase 3 - analyze the workspace itself
# ═══════════════════════════════════════════════════════════════════════════════════════════
def refresh_derived(j: Journal, dry_run: bool, allowed: bool) -> dict:
    """Re-derive drift, the evidence index and the dashboard datasets when they are stale.

    Delegates to `obj016_daily_refresh.py --execute --skip-git`. `--skip-git` matters: engage has
    already synchronized the repositories under its own policy, and letting the daily job pull
    again would duplicate the work and report it twice.
    """
    state = read_json(PATHS["daily_state"]) or {}
    finished = parse_iso(state.get("finished"))
    hrs = age_hours(finished)
    out = {"last": state.get("finished"), "age_hours": hrs, "ran": False,
           "stale": hrs is None or hrs > REFRESH_STALE_HOURS}

    if not out["stale"]:
        j.step("derived data", "ok", f"current ({human_age(hrs)}); nothing to re-derive")
        return out
    if not allowed:
        j.step("derived data", "skipped", f"stale ({human_age(hrs)}) but --no-refresh was passed")
        return out
    if dry_run:
        j.step("derived data", "dry-run", f"stale ({human_age(hrs)}); would run "
                                          f"obj016_daily_refresh.py --execute --skip-git")
        return out

    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(PATHS["scripts"] / "obj016_daily_refresh.py"), "--execute", "--skip-git"],
        capture_output=True, text=True, cwd=str(ROOT), timeout=1800,
        encoding="utf-8", errors="replace", env=child_env(),
    )
    out["ran"] = True
    out["ok"] = proc.returncode == 0
    out["elapsed"] = round(time.time() - t0, 1)
    j.step("derived data", "ok" if out["ok"] else "failed",
           f"was {human_age(hrs)}; re-derived drift, evidence index and dashboards "
           f"in {out['elapsed']}s" if out["ok"] else
           f"refresh exited {proc.returncode}: {proc.stdout.strip()[-200:]}")
    return out


def read_drift() -> dict:
    d = read_json(PATHS["drift_report"]) or {}
    summary = d.get("summary", {})
    open_items = [f for f in d.get("findings", []) if f.get("status") not in ("ok", None)]
    return {"summary": summary, "open": [
        {"id": f.get("id"), "severity": f.get("severity"), "status": f.get("status"),
         "note": (f.get("note") or "")[:220]} for f in open_items]}


def read_scheduled_tasks() -> list[dict]:
    """Query the Windows scheduled tasks, including each one's trigger interval.

    The interval is fetched rather than inferred, and that is the whole point. The obvious
    heuristic - "compare the last run to the gap between last and next" - cannot detect a missed
    occurrence, because a skipped firing is exactly what stretches that gap. Measured here:
    PAM-Weekly-API-Execution last ran 2026-08-16 with next set to 2026-08-30, so the inferred
    period was 14 days and the missed Sunday looked perfectly on schedule. Reading DaysInterval /
    WeeksInterval off the trigger gives the real period, and the miss becomes obvious.
    """
    ps = (
        "$out = @(); "
        "foreach ($t in Get-ScheduledTask -TaskName 'PAM-*' -ErrorAction SilentlyContinue) { "
        "  $i = $t | Get-ScheduledTaskInfo; "
        "  $days = $null; "
        "  foreach ($g in $t.Triggers) { "
        "    if ($g.DaysInterval)  { $days = [double]$g.DaysInterval } "
        "    elseif ($g.WeeksInterval) { $days = 7.0 * [double]$g.WeeksInterval } } "
        "  $out += [pscustomobject]@{ TaskName=$t.TaskName; State=[string]$t.State; "
        "    LastRunTime=$i.LastRunTime; NextRunTime=$i.NextRunTime; "
        "    LastTaskResult=$i.LastTaskResult; PeriodDays=$days } }; "
        "$out | ConvertTo-Json -Compress -Depth 4"
    )
    try:
        proc = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps],
                              capture_output=True, text=True, timeout=90,
                              encoding="utf-8", errors="replace")
        data = json.loads(proc.stdout.strip() or "[]")
    except Exception:
        return []
    if isinstance(data, dict):
        data = [data]
    rows = []
    for t in data:
        rows.append({
            "name": t.get("TaskName"),
            "state": t.get("State"),
            "last": _ps_date(t.get("LastRunTime")),
            "next": _ps_date(t.get("NextRunTime")),
            "result": t.get("LastTaskResult"),
            "period_days": t.get("PeriodDays"),
        })
    return rows


def _ps_date(v) -> str | None:
    """PowerShell's ConvertTo-Json renders DateTime as /Date(ms)/ or an ISO string."""
    if not v:
        return None
    if isinstance(v, str):
        m = re.search(r"/Date\((\d+)", v)
        if m:
            return datetime.fromtimestamp(int(m.group(1)) / 1000).astimezone().isoformat(
                timespec="seconds")
        return v
    return str(v)


def read_token_state() -> dict:
    """`token_guard.py status` is documented as report-only: zero HTTP, no /arcontoken call."""
    try:
        proc = subprocess.run([sys.executable, str(PATHS["scripts"] / "token_guard.py"), "status"],
                              capture_output=True, text=True, cwd=str(ROOT), timeout=60,
                              encoding="utf-8", errors="replace", env=child_env())
        text = proc.stdout
    except Exception as exc:
        return {"error": str(exc)}
    return {
        "cache": _grab(text, r"^cache\s*:\s*(.+)$"),
        "latch": _grab(text, r"^latch\s*:\s*(.+)$"),
        "env_token": "not set" not in (_grab(text, r"PAM_API_TOKEN\s*:\s*(.+)$") or "not set"),
    }


def _grab(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else None


def read_active_objective() -> dict:
    """The current instruction, and any objective the register still calls In Progress."""
    out: dict = {"id": None, "title": None, "in_progress": []}
    try:
        text = PATHS["objective"].read_text(encoding="utf-8")
        m = re.search(r"\*\*`(OBJ-\d+)`\s*[-—]\s*(.+?)\*\*", text, re.DOTALL)
        if m:
            out["id"] = m.group(1)
            out["title"] = re.sub(r"\s+", " ", m.group(2)).strip().rstrip(".")
    except Exception:
        pass
    try:
        reg = PATHS["register"].read_text(encoding="utf-8")
        for line in reg.splitlines():
            if line.startswith("| OBJ-") and "In Progress" in line:
                cells = [c.strip() for c in line.split("|")]
                if len(cells) > 2:
                    out["in_progress"].append({"id": cells[1], "title": cells[2]})
    except Exception:
        pass
    return out


def read_latest_run() -> dict | None:
    d = PATHS["runs"]
    if not d.is_dir():
        return None
    runs = sorted([p for p in d.iterdir() if p.is_dir()], key=lambda p: p.name)
    if not runs:
        return None
    newest = runs[-1]
    info: dict = {"id": newest.name, "total_runs": len(runs)}
    cp = newest / "checkpoint.json"
    if cp.exists():
        data = read_json(cp) or {}
        flows = data.get("flows") or data.get("completed") or []
        info["checkpoint"] = True
        info["flows_done"] = len(flows) if isinstance(flows, list) else flows
    info["has_report"] = (newest / "RUN_REPORT.md").exists()
    return info


def read_resume_points() -> list[dict]:
    """Files whose entire purpose is to say 'unfinished work continues here'."""
    out = []
    for p in PATHS["resume_points"]:
        if not p.exists():
            continue
        first = ""
        try:
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.startswith("**Status:**") or line.startswith("**Purpose.**"):
                    first = re.sub(r"\*+", "", line).strip()[:200]
                    break
        except Exception:
            pass
        out.append({"file": p.relative_to(ROOT).as_posix(), "note": first})
    return out


def scan_todos(limit: int = 40) -> list[dict]:
    """TODO/FIXME markers in code this workspace actually owns.

    Bounded to `tools/` on purpose: the nested repos are read-only, and scanning
    them would return hundreds of other people's markers as though they were the owner's backlog.
    """
    hits: list[dict] = []
    pattern = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b[:\s-]*(.{0,110})")
    for f in sorted(PATHS["scripts"].glob("*.py")):
        try:
            for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                m = pattern.search(line)
                if m and not line.lstrip().startswith("#  ·"):
                    hits.append({"file": f.relative_to(ROOT).as_posix(), "line": n,
                                 "kind": m.group(1), "text": m.group(2).strip()})
                    if len(hits) >= limit:
                        return hits
        except Exception:
            continue
    return hits


# ═══════════════════════════════════════════════════════════════════════════════════════════
# phase 4 - validate: turn findings into a prioritized attention list
# ═══════════════════════════════════════════════════════════════════════════════════════════
def build_attention(repos: list[dict], drift: dict, tasks: list[dict], token: dict,
                    objective: dict, resumes: list[dict], refresh: dict) -> list[Attention]:
    items: list[Attention] = []

    for r in repos:
        if r.get("attention"):
            pri = {"critical": "critical", "high": "high"}.get(r["severity"], "normal")
            action = None
            if r["state"].get("diverged"):
                action = "Decide rebase or merge, then reconcile by hand."
            elif r["severity"] == "high" and r["state"].get("dirty"):
                action = f"Review or commit the changes in {r['rel']}, then re-run engage."
            elif r["state"].get("in_progress"):
                action = f"Finish or abort the {r['state']['in_progress']} in {r['rel']}."
            items.append(Attention(pri, r["attention"], "detected", action))

    for f in drift.get("open", []):
        sev = f.get("severity") or "normal"
        pri = "high" if sev == "critical" else ("normal" if sev == "high" else "low")
        items.append(Attention(pri, f"Drift: {f['id']} ({sev}) - {f['note']}", "project-data",
                               "python tools\\obj013_loop.py check"))

    for t in tasks:
        if t.get("result") not in (0, None):
            items.append(Attention("high",
                                   f"Scheduled task {t['name']} last exited {t['result']}.",
                                   "detected",
                                   f"Inspect its log before {t.get('next') or 'the next run'}."))
        # Missed occurrences, measured against the trigger's real period (see read_scheduled_tasks).
        gap = age_hours(parse_iso(t.get("last") or ""))
        period_h = (t.get("period_days") or 0) * 24
        if gap and period_h and gap > period_h * 1.1:
            missed = int(gap // period_h)
            items.append(Attention(
                "high" if missed > 1 else "normal",
                f"Scheduled task {t['name']} last ran {human_age(gap)} but fires every "
                f"{period_h / 24:g} day(s) — {missed} occurrence(s) did not run. "
                f"Next: {t.get('next')}.",
                "detected",
                f"Confirm the machine was on. Run it now if the gap matters: "
                f"Start-ScheduledTask -TaskName {t['name']}"))

    if token.get("latch") and "none" not in (token["latch"] or "").lower():
        items.append(Attention("critical",
                               f"Token attempt latch is set: {token['latch']}",
                               "project-data",
                               "Fix the cause, then: python tools\\token_guard.py clear-latch"))

    for r in resumes:
        items.append(Attention("normal", f"Unfinished work recorded in {r['file']}. {r['note']}",
                               "project-data", "Read the file before starting anything adjacent."))

    if refresh.get("stale") and not refresh.get("ran"):
        items.append(Attention("normal",
                               f"Derived data is stale ({human_age(refresh.get('age_hours'))}).",
                               "detected",
                               "python tools\\obj016_daily_refresh.py --execute"))

    items.sort(key=lambda a: SEVERITY_ORDER.get(a.priority, 5))
    return items


def recommend(repos: list[dict], attention: list[Attention], objective: dict) -> list[str]:
    """Next actions, drawn only from what was actually found. Never invented."""
    out: list[str] = []
    for a in attention:
        if a.priority in ("critical", "high") and a.action:
            out.append(a.action)
    for r in repos:
        if r["state"].get("ahead") and r["policy"] and r.get("known"):
            pol, _ = core.policy_for(r["rel"])
            if pol.push:
                how = "" if pol.push_auto else " (manual push, D47 - your explicit go-ahead)"
                out.append(f"Push {r['state']['ahead']} commit(s) from {r['rel']}.{how}")
    if objective.get("id"):
        out.append(f"Continue {objective['id']} - {(objective.get('title') or '')[:100]}")
    seen, unique = set(), []
    for o in out:
        if o not in seen:
            seen.add(o)
            unique.append(o)
    return unique[:6]


# ═══════════════════════════════════════════════════════════════════════════════════════════
# phase 5-6 - prepare and summarize
# ═══════════════════════════════════════════════════════════════════════════════════════════
BAR = "─" * 74


def render(ctx: dict) -> str:
    L: list[str] = []
    s = ctx["summary"]
    L.append("=" * 74)
    L.append(f"  ENGAGE · {ctx['workspace_name']}"
             f"{'  [DRY RUN - nothing was changed]' if ctx['dry_run'] else ''}")
    L.append(f"  {ctx['finished']}   elapsed {ctx['elapsed']}s")
    L.append("=" * 74)
    L.append("")
    L.append(f"  Repositories   {s['repos']} checked · {s['pulled']} updated · "
             f"{s['current']} already current · {s['attention_repos']} need attention")
    L.append(f"  Derived data   {s['derived']}")
    L.append(f"  Attention      {s['attention_total']} item(s) · "
             f"{s['critical']} critical · {s['high']} high")
    if ctx.get("open_objectives"):
        ids = ", ".join(o["id"] for o in ctx["open_objectives"])
        L.append(f"  Open work      {len(ctx['open_objectives'])} objective(s) in progress: {ids}")
    L.append("")

    L.append("REPOSITORIES")
    L.append(BAR)
    for r in ctx["repositories"]:
        st = r["state"]
        mark = "✓" if r["severity"] == "info" else "·"
        if r.get("pulled"):
            mark = "↓"
        if r["severity"] in ("critical", "high"):
            mark = "!"
        if r.get("pulled"):
            detail = (f"pulled {r.get('pulled_commits', 0)} commit(s) "
                      f"{r.get('before')} → {r.get('after')}")
        else:
            detail = r["reason"]
        L.append(f"  {mark} {r['name'][:38]:38s} {st.get('branch', '?')[:14]:14s} {detail}")
    L.append("")

    if ctx["changes"]["commits"] or ctx["changes"]["files"]:
        L.append("WHAT CHANGED")
        L.append(BAR)
        for r in ctx["repositories"]:
            if not r.get("pulled"):
                continue
            f = r.get("files") or {}
            L.append(f"  {r['rel']}  —  {f.get('total', 0)} file(s): "
                     f"{f.get('added', 0)} added, {f.get('modified', 0)} modified, "
                     f"{f.get('deleted', 0)} deleted")
            for c in r["commits"][:5]:
                L.append(f"      {c['sha']}  {c['subject'][:58]}")
        L.append("")

    if ctx["attention"]:
        L.append("NEEDS YOUR ATTENTION")
        L.append(BAR)
        for a in ctx["attention"]:
            tag = SEVERITY_LABEL.get(a["priority"], a["priority"].upper())
            L.append(f"  [{tag:8s}] {a['text']}")
            L.append(f"             ({a['source']})")
        L.append("")

    if ctx["recommended"]:
        L.append("RECOMMENDED NEXT")
        L.append(BAR)
        for i, rec in enumerate(ctx["recommended"], 1):
            L.append(f"  {i}. {rec}")
        L.append("")

    L.append(BAR)
    verdict = "DevProjects is engaged and ready." if s["critical"] == 0 else \
              "DevProjects is engaged — with blocking items above."
    L.append(f"  {verdict}")
    L.append(f"  context: {CONTEXT_FILE.relative_to(ROOT).as_posix()}")
    L.append("=" * 74)
    return "\n".join(L)


def write_briefing(ctx: dict) -> None:
    """A markdown briefing later turns can read instead of re-deriving all of this."""
    L = [f"# engage briefing — {ctx['finished']}", "",
         f"Generated by `tools/engage.py` in {ctx['elapsed']}s. "
         f"Machine-readable form: `state/engage/context.json`.", "",
         "## Repositories", "",
         "| Repository | Branch | State | Action |", "|---|---|---|---|"]
    for r in ctx["repositories"]:
        st = r["state"]
        L.append(f"| `{r['rel']}` | {st.get('branch')} | "
                 f"{st.get('ahead')} ahead / {st.get('behind')} behind, "
                 f"{st.get('dirty')} dirty | {r['action']} — {r['reason']} |")
    L += ["", "## Attention", ""]
    if ctx["attention"]:
        for a in ctx["attention"]:
            L.append(f"- **{a['priority'].upper()}** ({a['source']}) — {a['text']}"
                     + (f"  \n  *Action:* {a['action']}" if a["action"] else ""))
    else:
        L.append("Nothing outstanding.")
    L += ["", "## Recommended next", ""]
    L += [f"{i}. {r}" for i, r in enumerate(ctx["recommended"], 1)] or ["Nothing pending."]
    L += ["", "## Active objective", "",
          f"`{ctx['objective'].get('id')}` — {ctx['objective'].get('title')}", ""]
    BRIEFING_FILE.write_text("\n".join(L) + "\n", encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════════════════════════════
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="decide everything, change nothing: no fetch, no pull, no writes")
    ap.add_argument("--no-refresh", action="store_true",
                    help="do not re-derive drift/index/dashboards even if they are stale")
    ap.add_argument("--offline", action="store_true",
                    help="skip fetching; classify against local refs only")
    ap.add_argument("--json", action="store_true", help="print the context JSON to stdout")
    ap.add_argument("--quiet", action="store_true", help="suppress the per-step log")
    ap.add_argument("--ui", action="store_true",
                    help="after analysing, open the Control Center in the browser "
                         "(tools/control_center.py) so decisions can be made and "
                         "approved actions executed")
    args = ap.parse_args()

    make_output_safe()
    if not is_workspace(ROOT):
        print(f"engage: {ROOT} is not the DevProjects workspace "
              f"(expected {', '.join(WORKSPACE_MARKERS)}). Refusing to act.", file=sys.stderr)
        return 2

    t0 = time.time()
    j = Journal(dry_run=args.dry_run)
    if not args.quiet and not args.json:
        print("=" * 74)
        print(f"  engage — {'DRY RUN' if args.dry_run else 'inspecting and synchronizing'}")
        print("=" * 74)

    repos = sync_repositories(j, args.dry_run, args.offline)
    refresh = refresh_derived(j, args.dry_run, allowed=not args.no_refresh)

    drift = read_drift()
    tasks = read_scheduled_tasks()
    token = read_token_state()
    objective = read_active_objective()
    latest_run = read_latest_run()
    resumes = read_resume_points()
    todos = scan_todos()

    attention = build_attention(repos, drift, tasks, token, objective, resumes, refresh)
    recommended = recommend(repos, attention, objective)

    pulled = sum(1 for r in repos if r.get("pulled"))
    ctx = {
        "generated_by": "tools/engage.py (OBJ-026)",
        "workspace": str(ROOT),
        "workspace_name": "DevProjects",
        "started": j.started, "finished": now(), "elapsed": round(time.time() - t0, 1),
        "dry_run": args.dry_run, "offline": args.offline,
        "summary": {
            "repos": len(repos),
            "pulled": pulled,
            "current": sum(1 for r in repos if r["severity"] == "info"),
            "attention_repos": sum(1 for r in repos if r.get("attention")),
            "attention_total": len(attention),
            "critical": sum(1 for a in attention if a.priority == "critical"),
            "high": sum(1 for a in attention if a.priority == "high"),
            "derived": ("re-derived just now" if refresh.get("ran")
                        else f"current ({human_age(refresh.get('age_hours'))})"
                        if not refresh.get("stale")
                        else f"stale ({human_age(refresh.get('age_hours'))})"),
        },
        "repositories": repos,
        "changes": {
            "commits": sum(r.get("pulled_commits", 0) for r in repos),
            "files": sum((r.get("files") or {}).get("total", 0) for r in repos),
        },
        "attention": [a.to_dict() for a in attention],
        "open_objectives": objective.get("in_progress", []),
        "recommended": recommended,
        "drift": drift, "scheduled_tasks": tasks, "token": token,
        "objective": objective, "latest_run": latest_run,
        "resume_points": resumes, "todos": todos,
        "steps": j.steps,
    }

    if not args.dry_run:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        CONTEXT_FILE.write_text(json.dumps(ctx, indent=1, ensure_ascii=False), encoding="utf-8")
        write_briefing(ctx)
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(f"\n{'=' * 74}\n{ctx['finished']}  elapsed {ctx['elapsed']}s\n")
            for line in j.lines:
                fh.write(line + "\n")
            fh.write(f"result: {ctx['summary']['attention_total']} attention item(s), "
                     f"{ctx['summary']['critical']} critical\n")

    if args.json:
        print(json.dumps(ctx, indent=1, ensure_ascii=False))
    else:
        print()
        print(render(ctx))

    if args.ui:
        # Hand over to the Control Center. Deliberately AFTER the terminal report is
        # printed, so the CLI stays complete on its own and the UI is an addition
        # rather than a replacement - if the browser never opens, nothing is lost.
        #
        # This process is replaced rather than forked: the server runs in the
        # foreground so Ctrl+C stops it, and there is no orphaned listener left
        # behind if the terminal goes away.
        cc = TOOLS_DIR / "control_center.py"
        if not cc.is_file():
            print(f"\n  cannot open the Control Center - missing {cc}")
            return 0
        print("\n  opening the Control Center; Ctrl+C to stop the server")
        return subprocess.call([sys.executable, str(cc), "--open"], cwd=str(ROOT))

    return 0


if __name__ == "__main__":
    sys.exit(main())
