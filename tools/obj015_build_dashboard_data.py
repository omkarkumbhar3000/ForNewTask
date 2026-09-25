#!/usr/bin/env python3
"""
obj015_build_dashboard_data.py — build the management dashboard's data layer.

OBJ-015. Reads only measured / authored artifacts already in this workspace and emits JSON
into `tools/dashboard/src/data/`. Nothing is estimated, rounded up, or invented: where a
figure was never captured the dataset carries the string "N/A" and the reason lands in
`gaps.json`.

Read-only on the workspace. The ONLY directory written is tools/dashboard/src/data/.
Zero HTTP calls — no PAM endpoint is touched.

    python tools\\obj015_build_dashboard_data.py            # build + verify
    python tools\\obj015_build_dashboard_data.py --verify   # verify only, no write

Source of truth per dataset is recorded in manifest.json and printed by --verify.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl

from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
# OBJ-016: served as static files and fetched at runtime, NOT bundled into the JS. That is what
# lets the daily job refresh the figures without an `npm run build`. Keep exactly one copy —
# a leftover src/data/ would be a second, silently diverging source.
OUT = ROOT / "tools" / "dashboard" / "public" / "data"

# ⛔ N and N-1 are RESOLVED AT RUN TIME, never hardcoded (OBJ-017).
#
# They were hardcoded until the weekly execution schedule existed, and that would have made every
# weekly run invisible: the newest run would land in artifacts/runs/ and the dashboard would keep
# reporting August's as current. `resolve_runs()` picks the newest substantive run as N and the one
# before it as N-1.
#
# ⚠️ AUTHORED analysis is a different matter and is pinned. The benchmark narrative, the "overall
# trend" line and the three headline findings (1,022 false passes · 19 endpoints accepting an invalid
# token · 85 minutes of downtime) were WRITTEN ABOUT ONE RUN. They are not properties of whatever run
# is newest. When N moves to a run nobody has analysed, those fields are withheld and the UI says so
# — attaching last month's findings to this week's execution would be exactly the invented-number
# failure this whole data layer exists to prevent.
AUTHORED_ANALYSIS_RUN = "2026-08-05_114315"

# Findings are pinned to the run whose retained evidence proves them
# (.claude/rules/api-surface.md — LoopholeSpec.run_id). A new run inherits nothing.
FINDINGS_BY_RUN: dict[str, list[str]] = {
    "2026-08-05_114315": ["LH-13"],
    "2026-07-29_181439": [f"LH-{n:02d}" for n in range(1, 13)],   # LH-01 … LH-12
}

# A run must reach this many executed test cases to count as substantive — i.e. to be eligible as
# N or N-1. Below it, the run is a probe: real history, but not a benchmark baseline.
SUBSTANTIVE_MIN_EXECUTED = 100

BENCHMARK_MD = (ROOT / "docs" / "management" / "summary"
                / "OBJ-010-Execution-Benchmark.md")
FINDINGS_MD = ROOT / "docs" / "findings" / "FINDINGS-SUMMARY-AND-PRIORITY.md"
REPO_FINDINGS_CSV = ROOT / "docs" / "findings" / "repository" / "findings.csv"
MGMT_FINDINGS = ROOT / "data" / "analysis" / "management-findings.json"
OBSERVATIONS = ROOT / "data" / "analysis" / "observations.json"
SEGMENTS = ROOT / "state" / "obj010" / "segments.json"
BLOCKED_ROWS = ROOT / "tools" / ".obj010" / "blocked-rows.json"
PROFILE = ROOT / "data" / "profiles" / "pam.json"
RUNS_DIR = ROOT / "artifacts" / "runs"
APICONFIG = (ROOT / "Automation gitlab repo" / "pam_automation_bootstrap" / "src" / "test" / "java"
             / "com" / "arcon" / "autoconfigs" / "APIConfig.java")

# The canonical endpoint count. APIConfig.java yields five different totals depending on what
# is counted; 1,306 (distinct controller+action pairs) is the one the workspace quotes, and
# every coverage percentage in artifacts/runs/ is computed against it. Do not "correct" this to the
# 1,308 distinct path strings the path parser below returns — they answer different questions.
CATALOGUE_COUNT = 1306

NA = "N/A"
_sources: list[dict] = []
_gaps: list[dict] = []
_warnings: list[str] = []

# Assigned exactly once, by resolve_runs(), before anything reads them. Module globals rather
# than parameters threaded through twenty call sites: there is one current run per build, and
# making that implicit-but-single is clearer than passing it everywhere.
RUN_N: str = ""
RUN_N1: str = ""
WORKBOOK: Path = Path()
VALIDATION: Path = Path()

# results.json is up to 7 MB and is read by both the resolver and the run builder.
_results_cache: dict[str, dict] = {}


def src(path: Path, what: str) -> Path:
    """Record a source file in the provenance manifest. Idempotent — the workbook is opened
    twice (once to build, once to verify) and must appear once."""
    rel = path.relative_to(ROOT).as_posix()
    if any(s["path"] == rel for s in _sources):
        return path
    if path.exists():
        st = path.stat()
        _sources.append({"path": rel, "provides": what, "bytes": st.st_size, "exists": True})
    else:
        _sources.append({"path": rel, "provides": what, "bytes": 0, "exists": False})
        _warnings.append(f"source missing: {rel}")
    return path


def gap(item: str, why: str, would_close: str) -> None:
    _gaps.append({"item": item, "why": why, "wouldClose": would_close})


# ─────────────────────────────────────────────────────────────────────────────
# workbook
# ─────────────────────────────────────────────────────────────────────────────
def read_workbook() -> dict:
    """Every sheet as {name: {"subtitle": str, "rows": [dict]}}.

    Sheet layout written by obj010_build_workbook.py: row 1 title, row 2 subtitle,
    row 3 header, data from row 4.
    """
    wb = openpyxl.load_workbook(src(WORKBOOK, "run N results, benchmark, modules, performance"),
                                read_only=True, data_only=True)
    out = {}
    for name in wb.sheetnames:
        ws = wb[name]
        rows = list(ws.iter_rows(values_only=True))
        subtitle = str(rows[1][0]) if len(rows) > 1 and rows[1][0] else ""
        header = [str(c).strip() if c is not None else "" for c in rows[2]] if len(rows) > 2 else []
        data = []
        for r in rows[3:]:
            if all(c is None or str(c).strip() == "" for c in r):
                continue
            rec = {}
            for k, v in zip(header, r):
                if not k:
                    continue
                rec[k] = "" if v is None else (v if isinstance(v, (int, float)) else str(v).strip())
            data.append(rec)
        out[name] = {"subtitle": subtitle, "rows": data}
    wb.close()
    return out


def num(v, default=None):
    """Parse a workbook cell into int/float, or return default. '' and 'N/A' -> default."""
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip().replace(",", "").replace("%", "")
    if s in ("", NA, "n/a", "none", "None"):
        return default
    try:
        f = float(s)
        return int(f) if f.is_integer() else f
    except ValueError:
        return default


# ─────────────────────────────────────────────────────────────────────────────
# markdown table parsing
# ─────────────────────────────────────────────────────────────────────────────
def md_section(text: str, heading_re: str) -> str:
    """Return the body of the first '## ' section whose heading matches."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("#") and re.search(heading_re, ln):
            start = i + 1
            break
    if start is None:
        return ""
    body = []
    for ln in lines[start:]:
        if ln.startswith("## "):
            break
        body.append(ln)
    return "\n".join(body)


def md_table(body: str) -> list[list[str]]:
    """Rows of the first pipe table in `body`, header excluded, cells stripped of markup."""
    rows, in_table = [], False
    for ln in body.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            if in_table:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") and c for c in cells):
            in_table = True
            continue
        if in_table:
            rows.append([strip_md(c) for c in cells])
        # header row before the separator is skipped by the in_table flag
    return rows


def strip_md(s: str) -> str:
    """Plain text out of markdown.

    re.S matters: bold and code spans in the authored benchmark wrap across line breaks, and
    without DOTALL the non-greedy match fails and the literal ** markers reach the UI.
    """
    s = re.sub(r"\[(.+?)\]\([^)]*\)", r"\1", s, flags=re.S)
    s = re.sub(r"`(.+?)`", r"\1", s, flags=re.S)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s, flags=re.S)
    s = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", s, flags=re.S)
    s = re.sub(r"[ \t]*\n[ \t]*", " ", s)   # unwrap hard-wrapped prose into a paragraph
    return re.sub(r"\s{2,}", " ", s).strip()


SEV_ICON = re.compile(r"[🔴🟠🟡🟢⬜⚠️✅⛔🤝▲▼▬]")


def clean_sev(s: str) -> str:
    return SEV_ICON.sub("", s).strip()


# Severity buckets. The source documents use five distinct vocabularies; this is the only
# normalisation in this script and it is deliberately explicit so it can be audited.
SEV_MAP = {
    "critical": "Critical",
    "high": "High",
    "review": "Medium",     # LH-09's "Review" — orange tier in the source table
    "medium": "Medium",
    "low": "Low",
    "informational": "Informational",
    "info": "Informational",
}


def bucket(label: str) -> str:
    key = clean_sev(label).lower().split()[0] if clean_sev(label) else ""
    return SEV_MAP.get(key, "Informational")


# ─────────────────────────────────────────────────────────────────────────────
# findings
# ─────────────────────────────────────────────────────────────────────────────
def build_findings() -> dict:
    sets = []

    # 1 — the 13 API findings. CLAUDE.md names docs/briefs/developer-loopholes.md as the
    # source of truth for the list; this table is its prioritised presentation.
    _f = src(FINDINGS_MD, "13 API findings with severity, effort, priority, Jira")
    if not _f.exists():                      # OBJ-025: src() records the miss but still
        raise SystemExit(                    # returns the path, so read_text() crashed the
            f"required source missing: {_f}"  # whole daily job. Fail with the reason instead.
        )
    text = _f.read_text(encoding="utf-8")
    rows = md_table(md_section(text, r"Prioritised findings"))
    api_items = []
    for r in rows:
        if len(r) < 7:
            continue
        priority, fid, finding, sev, effort, scope, jira = r[:7]
        raised = "PAMIT-" in jira
        api_items.append({
            "id": fid,
            "title": finding,
            "priority": clean_sev(priority),
            "severityLabel": clean_sev(sev),
            "severity": bucket(sev),
            "effort": clean_sev(effort),
            "scope": scope,
            "jira": clean_sev(jira) if raised else None,
            "status": "Raised" if raised else "Not raised",
            "statusDetail": clean_sev(jira),
        })
    if len(api_items) != 13:
        _warnings.append(f"expected 13 API findings, parsed {len(api_items)}")
    sets.append({
        "id": "api",
        "name": "PAM API findings",
        "description": "Implementation findings from automated execution of the PAM API surface.",
        "source": FINDINGS_MD.relative_to(ROOT).as_posix() + " §3",
        "items": api_items,
    })

    # 2 — developer repository size findings (OBJ-014)
    if REPO_FINDINGS_CSV.exists():
        src(REPO_FINDINGS_CSV, "14 developer-repository size findings with severity")
        repo_items = []
        with REPO_FINDINGS_CSV.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                fid = (row.get("id") or "").strip()
                if not fid:
                    continue
                ticket = (row.get("ticket") or "").strip()
                raised = ticket.startswith("PAMIT-")
                mv, unit = (row.get("measured_value") or "").strip(), (row.get("unit") or "").strip()
                repo_items.append({
                    "id": fid,
                    "title": (row.get("finding") or "").strip(),
                    "priority": f"rank {row.get('rank')}",
                    "severityLabel": (row.get("severity") or "").strip().title(),
                    "severity": bucket(row.get("severity") or ""),
                    "effort": (row.get("remediation_risk") or "").strip() or NA,
                    "scope": f"{mv} {unit}".strip() or NA,
                    "jira": ticket if raised else None,
                    "status": "Raised" if raised else "Not raised",
                    "statusDetail": ticket or NA,
                    "layer": (row.get("layer") or "").strip(),
                    "remediation": (row.get("remediation") or "").strip(),
                    "evidence": (row.get("evidence_file") or "").strip(),
                })
        sets.append({
            "id": "repo",
            "name": "Developer repository size",
            "description": "Why the product repository is 35.57 GB. Recommendations only — nothing was remediated.",
            "source": REPO_FINDINGS_CSV.relative_to(ROOT).as_posix(),
            "items": repo_items,
        })
    else:
        gap("Developer repository findings", "findings.csv not present", "run the OBJ-014 regenerate scripts")

    # 3 — management findings
    if MGMT_FINDINGS.exists():
        data = json.loads(src(MGMT_FINDINGS, "16 management-level findings").read_text(encoding="utf-8"))
        items = []
        for f in data:
            pr = (f.get("priority") or "")
            sev = pr.split("-", 1)[1].strip() if "-" in pr else pr
            items.append({
                "id": f.get("finding_id"),
                "title": f.get("finding"),
                "priority": pr,
                "severityLabel": sev or NA,
                "severity": bucket(sev),
                "effort": NA,
                "scope": f.get("theme") or NA,
                "jira": None,
                "status": f.get("status") or NA,
                "statusDetail": f.get("owner_team") or NA,
                "impact": f.get("business_impact"),
                "remediation": f.get("recommendation"),
            })
        sets.append({
            "id": "management",
            "name": "Management findings",
            "description": "Business-impact framing of the same programme, one row per theme.",
            "source": MGMT_FINDINGS.relative_to(ROOT).as_posix(),
            "items": items,
        })

    # 4 — observations
    if OBSERVATIONS.exists():
        data = json.loads(src(OBSERVATIONS, "50 engineering observations").read_text(encoding="utf-8"))
        items = []
        for o in data:
            items.append({
                "id": o.get("observation_id"),
                "title": (o.get("observation") or "")[:220],
                "priority": o.get("category") or NA,
                "severityLabel": (o.get("severity") or "").title(),
                "severity": bucket(o.get("severity") or ""),
                "effort": NA,
                "scope": o.get("area") or NA,
                "jira": None,
                "status": o.get("status") or NA,
                "statusDetail": o.get("raised_by") or NA,
                "impact": o.get("impact"),
                "remediation": o.get("workaround"),
            })
        sets.append({
            "id": "observations",
            "name": "Engineering observations",
            "description": "Lower-severity observations captured during analysis.",
            "source": OBSERVATIONS.relative_to(ROOT).as_posix(),
            "items": items,
        })

    order = ["Critical", "High", "Medium", "Low", "Informational"]
    for s in sets:
        c = Counter(i["severity"] for i in s["items"])
        s["severityRollup"] = [{"severity": k, "count": c.get(k, 0)} for k in order]
        s["total"] = len(s["items"])
        s["raised"] = sum(1 for i in s["items"] if i["status"] == "Raised")

    return {
        "primarySetId": "api",
        "severityOrder": order,
        "severityMapping": {
            "note": "Source documents use five different severity vocabularies. severityLabel is the "
                    "original text; severity is the normalised bucket used for charts.",
            "map": SEV_MAP,
        },
        "sets": sets,
    }


# ─────────────────────────────────────────────────────────────────────────────
# runs / execution history
# ─────────────────────────────────────────────────────────────────────────────
def hop_verdict(hop: dict) -> str | None:
    """chain_runner does not persist a hop verdict; it is the AND of the check layers.

    Verified against the published OBJ-010 figures: this reproduces 3,459/1,957/14 for run N
    and 1,200/668/5 for run N-1 exactly.
    """
    checks = hop.get("checks") or []
    if not checks:
        return None  # withheld at call time — never counted as pass or fail
    return "FAIL" if any(c.get("verdict") == "FAIL" for c in checks) else "PASS"


def catalogue_paths() -> set[str]:
    """Every `/api/...` path declared in APIConfig.java, lowercased and query-stripped.

    Needed because "endpoints reached" and "endpoints declared" are DIFFERENT populations.
    The generated-data flows are built from the QA team's Excel corpus, which contains
    endpoints that APIConfig.java never declares — so dividing one by the other produces a
    coverage figure above 100%. Measured: run N reached 1,388 distinct endpoints, of which
    248 are absent from the catalogue.
    """
    if not APICONFIG.exists():
        _warnings.append("APIConfig.java not found — catalogue coverage will be reported as N/A")
        return set()
    text = src(APICONFIG, "declared endpoint catalogue, for true coverage").read_text(
        encoding="utf-8", errors="replace")
    out = set()
    for m in re.finditer(r'"(/?api/[^"]+)"', text, re.I):
        p = m.group(1)
        if not p.startswith("/"):
            p = "/" + p
        out.add(p.split("?")[0].rstrip("/").lower())
    return out


def load_results(run_id: str) -> dict | None:
    """Parsed results.json for a run, cached. None when the run never wrote one."""
    if run_id in _results_cache:
        return _results_cache[run_id]
    p = RUNS_DIR / run_id / "results.json"
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _warnings.append(f"unreadable results.json in {run_id}: {exc}")
        return None
    _results_cache[run_id] = data
    return data


def executed_count(data: dict) -> int:
    return sum(1 for f in data.get("flows", []) for h in f.get("hops", [])
               if hop_verdict(h) is not None)


def resolve_runs() -> None:
    """Pick N and N-1 from what is actually on disk, and set the module globals.

    Newest substantive run is N; the substantive run before it is N-1. This is what makes a
    weekly execution show up on its own: drop a new run folder in and it becomes current.

    Ordering is by folder stamp, which is `YYYY-MM-DD_HHMMSS` and therefore sorts
    lexicographically in time order — no date parsing needed.
    """
    global RUN_N, RUN_N1, WORKBOOK, VALIDATION

    substantive: list[str] = []
    for d in sorted((p for p in RUNS_DIR.iterdir() if p.is_dir()),
                    key=lambda p: p.name, reverse=True):
        data = load_results(d.name)
        if data and executed_count(data) >= SUBSTANTIVE_MIN_EXECUTED:
            substantive.append(d.name)

    if not substantive:
        raise SystemExit(
            f"No run under {RUNS_DIR.relative_to(ROOT)} has at least "
            f"{SUBSTANTIVE_MIN_EXECUTED} executed test cases. There is nothing to report on."
        )

    RUN_N = substantive[0]
    RUN_N1 = substantive[1] if len(substantive) > 1 else ""
    WORKBOOK = RUNS_DIR / RUN_N / "QA_MsSQL_API_Execution.xlsx"
    VALIDATION = RUNS_DIR / RUN_N / "validation.json"

    if not RUN_N1:
        gap("A previous-vs-current benchmark",
            "only one substantive execution exists, so there is nothing to compare against",
            "a second full execution")
    if RUN_N != AUTHORED_ANALYSIS_RUN:
        gap("Authored analysis for the current execution",
            f"the benchmark narrative, the overall-trend line and the three headline findings were "
            f"written about run {AUTHORED_ANALYSIS_RUN}, not {RUN_N}. They describe a different "
            f"execution and are withheld rather than reattached",
            f"an analysis of run {RUN_N} written into docs/management/summary/, then re-run this generator")


def classify_run(flows: list[dict], executed: int) -> str:
    """Executed volume first — several probe runs generate `data_*` flows but issue only a dozen calls."""
    if executed == 0:
        return "Started, no test case executed"
    if executed < 50:
        return "Feasibility / probe"
    if any(str(f.get("id", "")).startswith("data") for f in flows):
        return "Full suite — positive + negative"
    return "Generated positive chains"


def build_runs(segments: dict, findings_by_run: dict, catalogue: set[str]) -> list[dict]:
    runs = []
    for d in sorted(RUNS_DIR.iterdir()):
        if not d.is_dir():
            continue
        rid = d.name
        results = d / "results.json"
        report_md = d / "RUN_REPORT.md"
        evidence = d / "evidence"
        rec = {
            "id": rid,
            "date": rid.split("_")[0],
            "projectId": "PAM",
            "runFolder": (d.relative_to(ROOT)).as_posix(),
            "hasRunReport": report_md.exists(),
            "evidenceFiles": len(list(evidence.iterdir())) if evidence.is_dir() else 0,
            "findingIds": findings_by_run.get(rid, []),
            "findings": len(findings_by_run.get(rid, [])),
        }
        if not results.exists():
            rec.update({
                "type": "Aborted before any result was written",
                "status": "Aborted",
                "environment": NA, "flows": NA, "total": NA, "executed": NA,
                "passed": NA, "failed": NA, "blocked": NA, "successRate": NA,
                "durationMin": NA, "distinctEndpoints": NA, "latencyMedianMs": NA,
                "note": "No results.json — only a checkpoint exists." if (d / "checkpoint.json").exists()
                        else "No results.json and no checkpoint.",
                "endpointsInCatalogue": NA, "endpointsOutsideCatalogue": NA, "cataloguePct": NA,
                "isBaseline": False, "isCurrent": False, "substantive": False,
            })
            gap(f"Run {rid} metrics", "the run produced no results.json", "nothing — the run aborted; kept for completeness")
            runs.append(rec)
            continue

        data = load_results(rid)
        if data is None:
            j = rec  # unreadable results.json — treat as a run with no measurements
            j.update({
                "type": "results.json is present but unreadable", "status": "Unknown",
                "environment": NA, "flows": NA, "total": NA, "executed": NA,
                "passed": NA, "failed": NA, "blocked": NA, "successRate": NA,
                "durationMin": NA, "distinctEndpoints": NA, "latencyMedianMs": NA,
                "endpointsInCatalogue": NA, "endpointsOutsideCatalogue": NA, "cataloguePct": NA,
                "note": "The file could not be parsed; see the generator warnings.",
                "isBaseline": False, "isCurrent": False, "substantive": False,
            })
            runs.append(rec)
            continue
        meta, flows = data.get("meta", {}), data.get("flows", [])
        hops = [h for f in flows for h in f.get("hops", [])]
        verdicts = Counter(hop_verdict(h) for h in hops)
        passed, failed = verdicts.get("PASS", 0), verdicts.get("FAIL", 0)
        blocked = verdicts.get(None, 0)
        executed = passed + failed
        lat = sorted(int(x) for h in hops
                     if (x := str(h.get("latency_ms", "")).strip()).isdigit())

        reached = {str(h.get("path", "")).split("?")[0].rstrip("/").lower()
                   for h in hops if hop_verdict(h) is not None}
        reached.discard("")
        in_cat = reached & catalogue

        # Elapsed: a resumed run's meta.elapsed_s covers the LAST process only. segments.json
        # holds the recovered true total. Using meta here would understate run N by 234 min.
        if rid == segments.get("run") and segments.get("totals", {}).get("elapsed_min"):
            duration = segments["totals"]["elapsed_min"]
            duration_basis = "segments.json — total across all segments"
        elif meta.get("elapsed_s"):
            duration = round(meta["elapsed_s"] / 60, 1)
            duration_basis = "results.json meta.elapsed_s"
        else:
            duration = NA
            duration_basis = "not captured"

        rec.update({
            "type": classify_run(flows, executed),
            "status": "Complete" if executed else "No test case executed",
            "environment": meta.get("env", NA),
            "mode": meta.get("mode", NA),
            "flows": len(flows),
            "flowsPassed": sum(1 for f in flows if f.get("verdict") == "PASS"),
            "flowsFailed": sum(1 for f in flows if f.get("verdict") == "FAIL"),
            "total": len(hops),
            "executed": executed,
            "passed": passed,
            "failed": failed,
            "blocked": blocked,
            "successRate": round(100 * passed / executed, 1) if executed else NA,
            "durationMin": duration,
            "durationBasis": duration_basis,
            # Basis: distinct endpoint path with the query string stripped, over EXECUTED hops only.
            # Verified against the workbook — this is the definition behind its 1,388 and N-1's 870.
            # Counting (verb, path) instead yields 2,361, and counting unexecuted hops too yields 1,402.
            "distinctEndpoints": len(reached),
            # Of those, how many the catalogue actually declares. Run N reaches 248 endpoints
            # APIConfig.java does not declare (they come from the QA Excel corpus), so
            # reached/declared is NOT a coverage figure — it exceeds 100%.
            "endpointsInCatalogue": len(in_cat) if catalogue else NA,
            "endpointsOutsideCatalogue": len(reached - catalogue) if catalogue else NA,
            "cataloguePct": round(100 * len(in_cat) / CATALOGUE_COUNT, 1) if catalogue else NA,
            "latencyMeanMs": round(statistics.fmean(lat)) if lat else NA,
            "latencyMedianMs": int(statistics.median(lat)) if lat else NA,
            "latencyP95Ms": lat[int(len(lat) * 0.95)] if lat else NA,
            "downtimePauses": segments.get("totals", {}).get("downtime_pauses")
                              if rid == segments.get("run") else len(meta.get("downtime_events") or []),
            "note": "",
            "isBaseline": rid == RUN_N1,
            "isCurrent": rid == RUN_N,
            "substantive": executed >= SUBSTANTIVE_MIN_EXECUTED,
        })
        runs.append(rec)

    runs.sort(key=lambda r: r["id"], reverse=True)
    return runs



# -----------------------------------------------------------------------------
# execution reliability (OBJ-020)
#
# The owner's complaint that started this: the Sunday 2026-08-16 execution was terminated by a
# timeout and the dashboard showed nothing at all - it simply kept presenting the older run as
# "latest". Refusing to PROMOTE a partial run to N is correct; making it INVISIBLE is not. This
# dataset is the reliability record: what was scheduled, what finished, what was interrupted,
# what was resumed, and where each one actually stopped.
# -----------------------------------------------------------------------------
WEEKLY_DIR = ROOT / "state" / "weekly"
DAILY_DIR = ROOT / "state" / "daily"
FLOWS_DIR = ROOT / "tools" / "flows"


def _read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def planned_flow_count() -> int:
    """Flows in the current generated set. The basis is stated in the dataset - a run executed
    before the last regeneration was measured against a different set, so this is context."""
    n = 0
    for f in FLOWS_DIR.rglob("*.json"):
        d = _read_json(f)
        if isinstance(d, list):
            n += len(d)
        elif isinstance(d, dict):
            # A file may hold a LIST of flows, a wrapper with a flows/chains key, or - as the three
            # hand-written flows do - one bare flow object. Missing that last case undercounted the
            # corpus by 3 and made a complete run read as 100.4%.
            inner = d.get("flows") or d.get("chains")
            n += len(inner) if isinstance(inner, list) else (1 if d.get("id") else 0)
    return n


def weekly_job_history() -> list[dict]:
    """Parse the append-only weekly log into one record per EXECUTE invocation."""
    log = WEEKLY_DIR / "weekly.log"
    if not log.exists():
        return []
    out: list[dict] = []
    cur = None
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.rstrip()
        if line.startswith("===== ") and "(execute)" in line:
            cur = {"startedAt": line.split("=====")[1].strip().replace(" (execute)", ""),
                   "steps": [], "result": NA, "run": NA}
            out.append(cur)
        elif line.startswith("===== "):
            cur = None
        elif cur is not None:
            head = line[:9]
            if line.startswith(("[ FAIL ]", "[  OK  ]", "[ SKIP ]")):
                status = "failed" if "FAIL" in head else ("ok" if "OK" in head else "skipped")
                cur["steps"].append({"status": status, "text": line[9:].strip()[:240]})
            elif line.startswith("result:"):
                parts = line.split("run:")
                cur["result"] = parts[0].replace("result:", "").strip()
                cur["run"] = parts[1].strip() if len(parts) > 1 else NA
    return out


def run_reliability(rec: dict) -> dict:
    """Terminal state for one run folder, derived from what is on disk - never assumed."""
    d = RUNS_DIR / rec["id"]
    ck = _read_json(d / "checkpoint.json") or {}
    flows = ck.get("flows", []) if isinstance(ck, dict) else []
    verdicts: dict[str, int] = {}
    for f in flows:
        v = (f or {}).get("verdict") or "UNKNOWN"
        verdicts[v] = verdicts.get(v, 0) + 1

    has_results = (d / "results.json").exists()
    has_report = (d / "RUN_REPORT.md").exists()

    if has_results and has_report:
        state = "Completed"
        why = "results.json and RUN_REPORT.md were both written"
    elif flows and not has_results:
        state = "Incomplete - interrupted"
        why = ("the runner was terminated before it could write results.json; only its checkpoint "
               "survives, recording " + str(len(flows)) + " flows")
    elif has_results and not has_report:
        state = "Incomplete - no report"
        why = "results.json exists but no RUN_REPORT.md was written"
    else:
        state = "No result recorded"
        why = "neither a checkpoint nor results.json is present"

    return {
        "terminalState": state,
        "whyItStopped": why,
        "flowsRecorded": len(flows),
        "flowVerdicts": verdicts,
        "abortedFlows": verdicts.get("ABORTED", 0),
        "hasResults": has_results,
        "hasRunReport": has_report,
        "evidenceFiles": rec.get("evidenceFiles", 0),
        "promotedToCurrent": rec["id"] == RUN_N,
        "promotedNote": ("this run is N - the dashboard's headline figures come from it"
                         if rec["id"] == RUN_N else
                         "not promoted: a run without a workbook cannot become N, by design"),
    }


def build_reliability(runs: list[dict]) -> dict:
    planned = planned_flow_count()
    weekly = weekly_job_history()
    sup = _read_json(WEEKLY_DIR / "obj020-supervisor.json")
    daily = _read_json(DAILY_DIR / "last-run.json")
    last_weekly = _read_json(WEEKLY_DIR / "last-run.json")

    records = []
    for r in runs:
        rel = run_reliability(r)
        rel["plannedFlows"] = planned
        rel["completionPct"] = (round(100 * rel["flowsRecorded"] / planned, 1)
                                if planned and rel["flowsRecorded"] else NA)
        rel.update({"id": r["id"], "date": r["date"], "type": r.get("type", NA),
                    "executed": r.get("executed", NA),
                    "substantive": r.get("substantive", False)})
        rel["jobInvocations"] = [w for w in weekly if w.get("run") == r["id"]]
        records.append(rel)

    interrupted = [r for r in records if r["terminalState"].startswith("Incomplete")]
    completed = [r for r in records if r["terminalState"] == "Completed"]

    return {
        "generatedBy": "tools/obj015_build_dashboard_data.py (build_reliability)",
        "objective": "OBJ-020",
        "purpose": ("Every execution and what became of it. An interrupted run is shown here with "
                    "where it stopped - it is never dropped from the record."),
        "plannedFlows": planned,
        "plannedBasis": ("count of flows in tools/flows/ at build time. A run executed "
                         "before the last flow regeneration was measured against a different set, "
                         "so completion % for older runs is indicative, not exact."),
        "summary": {
            "totalRuns": len(records),
            "completed": len(completed),
            "interrupted": len(interrupted),
            "substantive": len([r for r in records if r["substantive"]]),
            "currentRun": RUN_N,
        },
        "retryPolicy": {
            "rule": ("A timeout or temporary backend interruption is not a permanent failure. Wait "
                     "30 minutes, resume, repeat; at least five intervals; stop only on success or "
                     "after 12 hours of continuous failure."),
            "implementedBy": "tools/obj020_execution_supervisor.py",
            "tokenSafety": ("The bearer token is resolved once and pinned into the environment, so "
                            "no retry ever calls /arcontoken. Retry-on-failure against that "
                            "endpoint is what locked a shared service account in July."),
        },
        "activeSupervisor": sup,
        "lastWeeklyJob": last_weekly,
        "lastDailyJob": daily,
        "weeklyJobHistory": weekly,
        "runs": records,
    }


# ─────────────────────────────────────────────────────────────────────────────
# benchmark
# ─────────────────────────────────────────────────────────────────────────────
BENCH_GROUPS = [
    ("Run context", ("Run folder", "Environment", "Mode", "Inter-call delay", "Verbs permitted")),
    ("Scale", ("Total flows", "Test cases planned", "Test cases reached", "Not reached", "Executed")),
    ("Outcome", ("Passed", "Failed", "Blocked", "of which, by guard", "Hop success rate",
                 "Flow success rate", "Flows passed", "Flows failed")),
    ("Coverage", ("Distinct endpoints reached", "Positive test cases executed",
                  "Negative test cases executed", "Negative pass rate", "scenario:")),
    ("Performance", ("Latency", "Elapsed", "of which spent waiting", "Downtime pauses",
                     "Calls to /arcontoken")),
    ("Regression", ("Comparable test cases", "Fixed failures", "New failures", "Newly added",
                    "retired since N-1", "re-scored")),
    ("Withheld", ("withheld:",)),
]


def group_of(metric: str) -> str:
    for name, keys in BENCH_GROUPS:
        if any(k.lower() in metric.lower() for k in keys):
            return name
    return "Other"


def build_benchmark(sheets: dict, bench_text: str) -> dict:
    rows = sheets["Execution Benchmark"]["rows"]
    metrics = []
    for r in rows:
        metric = str(r.get("Metric", "")).strip()
        if not metric:
            continue
        metrics.append({
            "metric": metric.replace("  of which", "of which").strip(),
            "indent": metric.startswith("  "),
            "previous": str(r.get("N Minus 1", "")).strip() or NA,
            "current": str(r.get("N Current", "")).strip() or NA,
            "delta": str(r.get("Delta", "")).strip() or "",
            "note": str(r.get("Note", "")).strip(),
            "group": group_of(metric),
            "previousNum": num(r.get("N Minus 1")),
            "currentNum": num(r.get("N Current")),
        })

    scen = [{
        "scenario": r["Scenario"],
        "executed": num(r["Executed"], 0),
        "passed": num(r["Passed"], 0),
        "failed": num(r["Failed"], 0),
        "blocked": num(r["Blocked"], 0),
        "successRate": num(r["Success Rate"], 0),
    } for r in sheets["Scenario Coverage"]["rows"]]

    # N-1 per-scenario comes from the benchmark sheet's "scenario:" rows, not re-derived.
    prev_scen = {m["metric"].replace("scenario:", "").strip(): m["previousNum"]
                 for m in metrics if m["metric"].startswith("scenario:")}
    for s in scen:
        s["previousExecuted"] = prev_scen.get(s["scenario"], 0)

    def find(pattern: str, field="currentNum"):
        for m in metrics:
            if re.search(pattern, m["metric"], re.I):
                return m[field]
        return None

    dimensions = {
        "note": "Only the Chain dimension existed in N-1, so it is the only apples-to-apples comparison.",
        "comparable": find(r"^Comparable test cases"),
        "fixed": find(r"^Fixed failures"),
        "regressed": find(r"^New failures"),
        "added": find(r"^Newly added"),
        "retired": find(r"retired since N-1"),
    }
    unchanged = None
    if dimensions["comparable"] and dimensions["fixed"] is not None and dimensions["regressed"] is not None:
        unchanged = dimensions["comparable"] - dimensions["fixed"] - dimensions["regressed"]
    dimensions["unchanged"] = unchanged

    # trend + narrative, authored in the benchmark document
    trend, trend_level = "", "neutral"
    m = re.search(r"\*\*Overall trend:\*\*\s*(.+)", bench_text)
    if m:
        raw = strip_md(m.group(1))
        trend_level = {"🟢": "good", "🟡": "caution", "🔴": "bad"}.get(raw[:1], "neutral")
        trend = clean_sev(raw)
    outcome = md_section(bench_text, r"Outcome in one paragraph").strip()
    outcome = "\n".join(ln for ln in outcome.splitlines() if ln.strip() and not ln.startswith("**Overall trend"))

    # ⛔ The narrative, the trend line and the outcome paragraph were authored about ONE run.
    # If N has moved on, the workbook's own N-1-vs-N metric table is still valid (the workbook is
    # rebuilt per run), but the prose is not — it is withheld rather than reattached.
    authored = RUN_N == AUTHORED_ANALYSIS_RUN

    return {
        "currentRunId": RUN_N,
        "previousRunId": RUN_N1 or None,
        "authoredNarrativeFor": AUTHORED_ANALYSIS_RUN,
        "authoredNarrativeApplies": authored,
        "trend": trend if authored else "",
        "trendLevel": trend_level if authored else "neutral",
        "outcome": strip_md(outcome) if authored else "",
        "metrics": metrics,
        "groups": [g for g, _ in BENCH_GROUPS] + ["Other"],
        "scenarios": scen,
        "regression": dimensions,
        "source": BENCHMARK_MD.relative_to(ROOT).as_posix() + " + workbook sheet 'Execution Benchmark'",
    }


# ─────────────────────────────────────────────────────────────────────────────
# improvements
# ─────────────────────────────────────────────────────────────────────────────
def build_improvements(bench_text: str, regression: dict) -> dict:
    fixed_defects = []
    for r in md_table(md_section(bench_text, r"Framework defects found and fixed")):
        if len(r) >= 3:
            fixed_defects.append({"n": r[0], "defect": r[1], "impact": r[2]})

    recs = []
    for r in md_table(md_section(bench_text, r"^#+ .*Recommendations")):
        if len(r) >= 2:
            pr = clean_sev(r[0])
            recs.append({"priority": pr, "action": r[1],
                         "tier": "High" if pr in ("1", "2") else "Medium" if pr in ("3", "4") else "Low"})

    return {
        "productMovement": {
            "note": regression.get("note"),
            "comparable": regression.get("comparable"),
            "unchanged": regression.get("unchanged"),
            "fixed": regression.get("fixed"),
            "regressed": regression.get("regressed"),
            "added": regression.get("added"),
            "retired": regression.get("retired"),
        },
        "frameworkDefectsFixed": fixed_defects,
        "recommendations": recs,
        "source": BENCHMARK_MD.relative_to(ROOT).as_posix() + " §6, §9, §11",
    }


def performance_trend(current: dict, previous: dict | None) -> str:
    """Describe the latency movement from the measurements, not from a remembered sentence."""
    if not previous:
        return "No baseline execution to compare against."
    parts = []
    for label, key in (("mean", "latencyMeanMs"), ("median", "latencyMedianMs"), ("p95", "latencyP95Ms")):
        a, b = current.get(key), previous.get(key)
        if isinstance(a, int) and isinstance(b, int) and b:
            parts.append(f"{label} {'up' if a > b else 'down' if a < b else 'flat'}")
    return ", ".join(parts) if parts else "Latency was not captured on both runs."


def duration_hint(current: dict, segments: dict) -> str:
    """Explain the duration figure using whatever this run actually recorded.

    The 85-minutes-lost figure belongs to the one resumed run that has a segments.json. Any
    other run gets its own downtime-pause count, or nothing at all — never the other run's number.
    """
    if current["id"] == segments.get("run"):
        waited = segments.get("totals", {}).get("downtime_minutes_waiting")
        if waited:
            return f"{waited} min of it was spent waiting for the environment."
    pauses = current.get("downtimePauses")
    if isinstance(pauses, int) and pauses > 0:
        return f"Includes {pauses} pause(s) waiting for the environment to recover."
    return "No environment downtime recorded during this run."


# ─────────────────────────────────────────────────────────────────────────────
# main build
# ─────────────────────────────────────────────────────────────────────────────
def build() -> dict:
    resolve_runs()          # must come first: everything below is scoped to the resolved N
    authored = RUN_N == AUTHORED_ANALYSIS_RUN

    if not WORKBOOK.exists():
        raise SystemExit(
            f"Run {RUN_N} has no workbook at {WORKBOOK.relative_to(ROOT).as_posix()}.\n"
            f"The workbook carries the scenario, module, performance and benchmark sheets, so the\n"
            f"dashboard cannot be built without it. Build it with:\n"
            f"  python tools\\obj010_build_workbook.py {RUN_N}"
            + (f" --baseline artifacts/runs/{RUN_N1}" if RUN_N1 else "")
        )

    sheets = read_workbook()
    validation = json.loads(src(VALIDATION, "10-gate validation checklist, failing-layer counts")
                            .read_text(encoding="utf-8")) if VALIDATION.exists() else {}
    if not VALIDATION.exists():
        gap("Run validation gates for the current execution",
            f"run {RUN_N} has no validation.json",
            f"python tools\\obj010_collect.py {RUN_N}")
    # Segments are per-run. A run resumed under the OBJ-020 retry policy executes in several
    # segments, and results.json meta records only the LAST one — 112.5 min for a run that really
    # spent 840.8 min executing. Prefer a per-run file; fall back to the shared one only when it
    # names this run, never unconditionally (that is how the 2026-08-05 total once landed on a
    # later run's workbook).
    per_run = SEGMENTS.parent / f"segments-{RUN_N}.json"
    segments = json.loads(src(per_run, f"measured segment totals for {RUN_N}").read_text(encoding="utf-8")) \
        if per_run.exists() else (
            json.loads(src(SEGMENTS, "true elapsed time for a resumed run").read_text(encoding="utf-8"))
            if SEGMENTS.exists() else {})
    bench_text = src(BENCHMARK_MD, "authored benchmark narrative, trend, recommendations").read_text(encoding="utf-8")
    profile = json.loads(src(PROFILE, "project identity and catalogue basis").read_text(encoding="utf-8"))

    findings = build_findings()

    runs = build_runs(segments, FINDINGS_BY_RUN, catalogue_paths())
    benchmark = build_benchmark(sheets, bench_text)
    improvements = build_improvements(bench_text, benchmark["regression"])

    current = next(r for r in runs if r["id"] == RUN_N)
    previous = next((r for r in runs if r["id"] == RUN_N1), None)
    api_set = next(s for s in findings["sets"] if s["id"] == "api")

    def prev(key: str):
        """A field of the baseline run, or N/A when there is no baseline yet."""
        return previous[key] if previous else NA

    substantive = [r for r in runs if r["substantive"]]
    kpis = {
        "currentRunId": RUN_N,
        "previousRunId": RUN_N1,
        "asOf": current["date"],
        "trend": benchmark["trend"],
        "tiles": [
            {"id": "executed", "label": "Test cases executed", "value": current["executed"],
             "previous": prev("executed"), "unit": "", "direction": "up-good",
             "hint": "Generated, executed and validated with no hand-written test code."},
            {"id": "passed", "label": "Passed", "value": current["passed"], "previous": prev("passed"),
             "unit": "", "direction": "up-good", "hint": "All validation layers passed."},
            {"id": "failed", "label": "Failed", "value": current["failed"], "previous": prev("failed"),
             "unit": "", "direction": "down-good", "hint": "At least one validation layer failed."},
            {"id": "successRate", "label": "Success rate", "value": current["successRate"],
             "previous": prev("successRate"), "unit": "%", "direction": "up-good",
             "hint": "Test-case level. Flow-level rate punishes long chains and understates reality."},
            {"id": "duration", "label": "Execution duration", "value": current["durationMin"],
             "previous": prev("durationMin"), "unit": "min", "direction": "neutral",
             "hint": duration_hint(current, segments)},
            {"id": "endpoints", "label": "Distinct endpoints reached", "value": current["distinctEndpoints"],
             "previous": prev("distinctEndpoints"), "unit": "", "direction": "up-good",
             "hint": f"Against a catalogue of {profile['catalogue']['expected_count']:,} declared endpoints."},
            {"id": "findings", "label": "Findings identified", "value": api_set["total"], "previous": NA,
             "unit": "", "direction": "down-good",
             "hint": f"{api_set['raised']} raised in Jira so far."},
            {"id": "projects", "label": "Projects", "value": 1, "previous": NA, "unit": "",
             "direction": "neutral", "hint": "PAM. The dashboard is built to take more."},
            {"id": "runs", "label": "Execution runs retained", "value": len(runs), "previous": NA,
             "unit": "", "direction": "neutral",
             "hint": f"{len(substantive)} substantive, {len(runs) - len(substantive)} probes or aborted. "
                     f"Runs are never deleted."},
        ],
        "severityRollup": api_set["severityRollup"],
        "statusSplit": [
            {"name": "Passed", "value": current["passed"]},
            {"name": "Failed", "value": current["failed"]},
            {"name": "Blocked", "value": current["blocked"]},
        ],
        # ⛔ Attached ONLY when the current run is the one these were measured in. They are
        # authored findings about a specific execution, not standing properties of the API.
        "headlinesFor": AUTHORED_ANALYSIS_RUN,
        "headlinesApply": authored,
        "headlines": [] if not authored else [
            {"label": "Green by status code, wrong in substance",
             "value": 1022, "unit": "test cases",
             "detail": "18.9% of everything executed returned HTTP 200 while failing validation. "
                       "A status-only assertion would have passed every one.",
             "source": "OBJ-010-Execution-Benchmark.md §4"},
            {"label": "Endpoints accepting an invalid auth token",
             "value": 19, "unit": "endpoints",
             "detail": "Of 57 that answered HTTP 200 to an invalid bearer, 19 require review — "
                       "several are writes, several disclose real data.",
             "source": "OBJ-010-Execution-Benchmark.md §5"},
            {"label": "Environment time lost",
             "value": segments.get("totals", {}).get("downtime_minutes_waiting", NA), "unit": "minutes",
             "detail": f"{segments.get('totals', {}).get('downtime_pauses', NA)} downtime pauses during the run — "
                       "the single largest cost in it.",
             "source": "OBJ-010-Execution-Benchmark.md §8"},
        ],
    }

    modules = [{
        "module": r["Module"], "hops": num(r["Hops"], 0), "executed": num(r["Executed"], 0),
        "passed": num(r["Passed"], 0), "failed": num(r["Failed"], 0), "blocked": num(r["Blocked"], 0),
        "negative": num(r["Negative Cases"], 0), "successRate": num(r["Success Rate"], 0),
    } for r in sheets["Module Results"]["rows"]]

    perf_rows = sheets["Performance"]["rows"]
    performance = {
        "overall": next(({"count": num(r["Count"], 0), "meanMs": num(r["Mean Ms"], 0),
                          "medianMs": num(r["Median Ms"], 0), "p95Ms": num(r["P95 Ms"], 0),
                          "maxMs": num(r["Max Ms"], 0)} for r in perf_rows if r["Scope"] == "ALL"), None),
        "byModule": [{"module": r["Scope"], "count": num(r["Count"], 0), "meanMs": num(r["Mean Ms"], 0),
                      "medianMs": num(r["Median Ms"], 0), "p95Ms": num(r["P95 Ms"], 0),
                      "maxMs": num(r["Max Ms"], 0)}
                     for r in perf_rows if r["Scope"] != "ALL"],
        # Derived from the baseline RUN, not hardcoded — otherwise a new N would be compared
        # against August's latency for ever.
        "previous": {
            "runId": RUN_N1 or None,
            "meanMs": prev("latencyMeanMs"),
            "medianMs": prev("latencyMedianMs"),
            "p95Ms": prev("latencyP95Ms"),
            "source": f"derived from {RUN_N1}/results.json" if RUN_N1 else "no baseline run exists",
        },
        "note": sheets["Performance"]["subtitle"],
    }

    failures = {
        "note": sheets["Failure Analysis"]["subtitle"],
        "layers": [{"layer": r["Failing Layer"], "hops": num(r["Hops"], 0),
                    "topEndpoints": [e.strip() for e in str(r["Top Endpoints"]).split(";") if e.strip()]}
                   for r in sheets["Failure Analysis"]["rows"]],
        "validationLayers": validation.get("failing_layers", {}),
    }

    excl_rows = sheets["Blocked and Exclusions"]["rows"]
    by_class: defaultdict[str, int] = defaultdict(int)
    for r in excl_rows:
        by_class[str(r["Item"])] += int(num(r["Count"], 0) or 0)
    exclusions = {
        "note": sheets["Blocked and Exclusions"]["subtitle"],
        "byClass": [{"item": k, "count": v} for k, v in sorted(by_class.items(), key=lambda kv: -kv[1])],
        "rows": [{"source": r["Source"], "item": r["Item"], "count": num(r["Count"], 0),
                  "reason": r["Reason"], "exampleEndpoint": r["Example Endpoint"]} for r in excl_rows],
        "withheldAtGenerationTime": validation.get("excel_rows_withheld_at_generation"),
        "withheldAtCallTime": validation.get("hops_withheld_at_call_time"),
    }

    gates = {
        "runId": validation.get("run"),
        "networkCallsIssued": validation.get("network_calls_issued"),
        "checklist": [{"item": c["item"], "verdict": c["verdict"], "detail": c.get("detail", "")}
                      for c in validation.get("checklist", [])],
        "passed": sum(1 for c in validation.get("checklist", []) if c["verdict"] in ("PASS", "✅", "OK")),
        "total": len(validation.get("checklist", [])),
        "source": VALIDATION.relative_to(ROOT).as_posix(),
    }

    projects = [{
        "id": profile["project"]["key"],
        "name": profile["project"]["name"],
        "tracker": profile["project"]["tracker"],
        "owner": profile["project"]["owner"],
        "notes": profile["project"]["notes"],
        "environment": profile["environment"].get("name") or current["environment"],
        "catalogueEndpoints": profile["catalogue"]["expected_count"],
        "catalogueBasis": profile["catalogue"]["count_basis"],
        "totalRuns": len(runs),
        "substantiveRuns": len(substantive),
        "latestRunId": RUN_N,
        "latestSuccessRate": current["successRate"],
        "totalTestCases": current["executed"],
        "endpointsReached": current["distinctEndpoints"],
        # ⚠ Coverage is measured against the CATALOGUE-DECLARED subset of what was reached,
        # not against everything reached. Run N exercised 248 endpoints APIConfig.java does not
        # declare, so reached/declared would read 106% and mean nothing.
        "endpointsInCatalogue": current["endpointsInCatalogue"],
        "endpointsOutsideCatalogue": current["endpointsOutsideCatalogue"],
        "coveragePct": current["cataloguePct"],
        "coverageBasis": (
            f"{current['endpointsInCatalogue']:,} of the {current['distinctEndpoints']:,} endpoints reached are "
            f"declared in APIConfig.java, against a catalogue of {CATALOGUE_COUNT:,}. The other "
            f"{current['endpointsOutsideCatalogue']:,} come from the QA team's Excel test corpus, which "
            f"contains endpoints the catalogue does not declare — so 'reached' and 'declared' are "
            f"different populations and their raw ratio is not a coverage figure."
        ),
        "findings": api_set["total"],
        "findingsRaised": api_set["raised"],
        "performanceTrend": performance_trend(current, previous),
        "profileSource": PROFILE.relative_to(ROOT).as_posix(),
        "onboardingKit": "tools/onboarding/",
    }]

    # per-execution management reports
    reports = {}
    for r in runs:
        is_current = r["id"] == RUN_N
        reports[r["id"]] = {
            "runId": r["id"],
            "date": r["date"],
            "projectId": r["projectId"],
            "projectName": projects[0]["name"],
            "scope": {
                "engine": "AI dynamic API framework (tools/) — generate_flows.py + "
                          "generate_data_flows.py → chain_runner.py",
                "bootstrapSuiteExecuted": False,
                "environment": r["environment"],
                "mode": r.get("mode", NA),
                "type": r["type"],
                "flows": r["flows"],
                "endpointsReached": r["distinctEndpoints"],
            },
            "summary": {k: r[k] for k in ("total", "executed", "passed", "failed", "blocked",
                                          "successRate", "durationMin", "durationBasis",
                                          "flowsPassed", "flowsFailed", "downtimePauses")
                        if k in r},
            "overallResult": r["status"],
            "hasBenchmark": is_current,
            "hasDetail": r["substantive"],
            "performance": {"meanMs": r.get("latencyMeanMs", NA), "medianMs": r.get("latencyMedianMs", NA),
                            "p95Ms": r.get("latencyP95Ms", NA)},
            "findingsCount": r["findings"],
            "findingIds": r["findingIds"],
            "evidenceFiles": r["evidenceFiles"],
            "runFolder": r["runFolder"],
            "note": r.get("note", ""),
        }
    # The authored narrative belongs to the run it was written about — which may no longer be N.
    reports[RUN_N].update({
        "gatesPassed": f"{gates['passed']} of {gates['total']}" if gates["total"] else NA,
    })
    if AUTHORED_ANALYSIS_RUN in reports:
        reports[AUTHORED_ANALYSIS_RUN].update({
            "trend": benchmark["trend"] if authored else "",
            "outcome": benchmark["outcome"] if authored else "",
            "observations": [h["detail"] for h in kpis["headlines"]],
            "conclusion": benchmark["trend"] if authored else "",
            "authoredNarrative": authored,
        })
    if not authored:
        reports[RUN_N].setdefault("authoredNarrative", False)

    gap("A single endpoint-coverage percentage",
        f"the {current['distinctEndpoints']:,} endpoints reached and the {CATALOGUE_COUNT:,} declared in "
        f"APIConfig.java are different populations — {current['endpointsOutsideCatalogue']:,} reached "
        f"endpoints are not declared anywhere in the catalogue, so their raw ratio reads over 100%",
        "a reconciled endpoint catalogue that includes the endpoints present only in the QA Excel corpus")
    gap("Per-run findings attribution beyond LH-01…13",
        "findings are pinned to a source run by LoopholeSpec.run_id, and only two runs are cited",
        "a finding→run index emitted by build_lh_pack.py")
    gap("Second project",
        "only data/profiles/pam.json exists — no other project has been onboarded or executed",
        "an onboarding profile plus at least one run for the new project")
    gap("N-1 negative dimension",
        "run N-1's generator emitted positive flows only, so its negative pass rate was never measured",
        "nothing — it is a genuine property of the baseline, shown as N/A")
    gap("Per-module figures for the baseline run",
        f"the module and performance breakdowns come from a run's own workbook, and only {RUN_N} has one",
        f"run obj010_build_workbook.py against the {RUN_N1 or 'baseline'} run folder")

    manifest = {
        "generator": "tools/obj015_build_dashboard_data.py",
        "objective": "OBJ-015 (run resolution and authored-analysis gating added under OBJ-017)",
        "currentRunId": RUN_N,
        "previousRunId": RUN_N1 or None,
        "runsResolved": "newest substantive run is N; the one before it is N-1. Never hardcoded.",
        "authoredAnalysisRun": AUTHORED_ANALYSIS_RUN,
        "authoredAnalysisApplies": authored,
        "httpCallsIssued": 0,
        "sources": _sources,
        "warnings": _warnings,
        "principle": "Every figure traces to a source file listed here. A figure that was never "
                     "measured is the string \"N/A\" and appears in gaps.json — it is never estimated.",
    }

    return {
        "manifest.json": manifest,
        "projects.json": projects,
        "runs.json": runs,
        "kpis.json": kpis,
        "benchmark.json": benchmark,
        "findings.json": findings,
        "modules.json": modules,
        "performance.json": performance,
        "failures.json": failures,
        "exclusions.json": exclusions,
        "gates.json": gates,
        "improvements.json": improvements,
        "reports.json": reports,
        "reliability.json": build_reliability(runs),
        "gaps.json": _gaps,
    }


# ─────────────────────────────────────────────────────────────────────────────
# verification
# ─────────────────────────────────────────────────────────────────────────────
def verify(datasets: dict) -> bool:
    """Cross-check derived figures against the workbook's own authored Summary sheet."""
    sheets = read_workbook()
    summary = {str(r["Item"]).strip(): str(r["Value"]).strip() for r in sheets["Summary"]["rows"]}
    current = next(r for r in datasets["runs.json"] if r["id"] == RUN_N)
    checks = [
        ("Flows", current["flows"], num(summary["Flows"])),
        ("Hops (test cases)", current["total"], num(summary["Hops (test cases)"])),
        ("Executed", current["executed"], num(summary["Executed"])),
        ("Passed", current["passed"], num(summary["Passed"])),
        ("Failed", current["failed"], num(summary["Failed"])),
        ("Blocked", current["blocked"], num(summary["Blocked"])),
        ("Hop success rate", current["successRate"], num(summary["Hop success rate"])),
        ("Distinct endpoints reached", current["distinctEndpoints"], num(summary["Distinct endpoints reached"])),
        ("Elapsed (min), all segments", current["durationMin"], num(summary["Elapsed (min), all segments"])),
    ]
    print("\n  Derived vs the workbook's authored Summary sheet")
    print(f"  {'metric':32} {'derived':>10} {'authored':>10}   result")
    ok = True
    for name, got, want in checks:
        good = got == want
        ok &= good
        print(f"  {name:32} {got!s:>10} {want!s:>10}   {'match' if good else 'MISMATCH'}")

    # scenario totals must reconcile to the executed count
    scen_total = sum(s["executed"] for s in datasets["benchmark.json"]["scenarios"])
    good = scen_total == current["executed"]
    ok &= good
    print(f"  {'scenario executed sums to':32} {scen_total!s:>10} {current['executed']!s:>10}   "
          f"{'match' if good else 'MISMATCH'}")
    return bool(ok)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true", help="verify only; write nothing")
    args = ap.parse_args()

    print("=" * 74)
    print("  OBJ-015 — dashboard data layer")
    print("=" * 74)
    datasets = build()
    ok = verify(datasets)

    if args.verify:
        print(f"\n  {'ALL CHECKS PASS' if ok else 'VERIFICATION FAILED'}")
        print("  --verify: nothing written.")
        return 0 if ok else 1

    # OBJ-025: create the LEAF only, never the whole chain. mkdir(parents=True)
    # meant that if OUT's parent moved, this rebuilt the old tree from nothing and
    # wrote 15 datasets into a directory the dashboard does not read - exit 0, a
    # success line, and a UI frozen at the moment of the move.
    if not OUT.parent.exists():
        raise SystemExit(
            f"dashboard app dir is missing: {OUT.parent} -- refusing to "
            f"create it. Fix the path in paths.py instead."
        )
    OUT.mkdir(exist_ok=True)
    print(f"\n  writing {len(datasets)} datasets -> {OUT.relative_to(ROOT).as_posix()}")
    for name, payload in datasets.items():
        p = OUT / name
        p.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    {name:22} {p.stat().st_size / 1024:8.1f} KB")

    if _warnings:
        print("\n  warnings:")
        for w in _warnings:
            print(f"    - {w}")
    print(f"\n  gaps recorded: {len(_gaps)} (see gaps.json — surfaced in the UI, not hidden)")
    print(f"  {'ALL CHECKS PASS' if ok else 'VERIFICATION FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
