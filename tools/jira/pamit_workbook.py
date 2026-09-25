#!/usr/bin/env python3
"""One consolidated Excel workbook for the client-ticket analysis (`OBJ-029`).

    python tools\\jira\\pamit_workbook.py            # build from the newest capture
    python tools\\jira\\pamit_workbook.py --refetch  # re-query Jira first

⛔ ONE WORKBOOK, MANY WORKSHEETS — owner ruling `D44`. A new analysis area becomes
a new **worksheet in this file**, never a new `.xlsx`. `WORKBOOK` below is the one
output path, and `build()` is the ordered sheet list — adding an analysis means
adding a `sheet_*` builder there and a row to the manifest in `sheet_readme()`.
⚠️ Those two are hand-kept in step: if you add a builder, add its manifest row, or
the README will describe a workbook that is not the one on disk.

⛔ EVERY COUNT MUST BE TRACEABLE TO ITS TICKETS — owner ruling `D43`. No sheet may
report a bare total. The rule this module enforces:

  * `04 Ticket Details` carries one row per ticket in the union of every pool the
    report counts, with the pool-membership flags and the area flags as columns.
    Filtering that sheet reproduces any reported figure exactly.
  * `09 Count Reconciliation` restates every headline count **as a live
    COUNTIFS formula over `04 Ticket Details`**, beside the value the analysis
    computed. Excel recomputes it on open, so a mismatch is visible to the reader
    without trusting this script. That is the difference between claiming the
    totals reconcile and showing it.

⚠️ Two Excel limits that silently corrupt a sheet if ignored:

  * A cell holds at most 32,767 characters. A PAM ADF `description` can exceed
    that, so `_cell()` truncates and marks the truncation. Writing an over-length
    value raises no error in openpyxl but produces a file Excel repairs on open,
    discarding the sheet.
  * A value beginning `=` is written as a FORMULA by openpyxl, not as text, so a
    ticket summary starting `=` would become `#NAME?`. `_cell()` prefixes only
    that case. ⚠️ It deliberately does NOT escape `+`, `-` or `@`: those trigger
    formula parsing when a human *types* into Excel, but openpyxl writes them as
    string cells and Excel renders them verbatim. Escaping them put a visible
    apostrophe in front of every negative delta and every ticket title starting
    with a dash.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from openpyxl import Workbook                                        # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill              # noqa: E402
from openpyxl.utils import get_column_letter                          # noqa: E402
from openpyxl.worksheet.table import Table, TableStyleInfo            # noqa: E402

import pamit_analysis_rules as R                                      # noqa: E402
from pamit_fmt import pct                                             # noqa: E402

sys.path.insert(0, str(HERE.parent))
from paths import workspace_root                                      # noqa: E402

ROOT = workspace_root()
WORKBOOK = ROOT / "artifacts" / "workbooks" / "PAM-Client-Ticket-Analysis.xlsx"

MAX_CELL = 32_767
TRUNC_MARK = "  …[truncated]"

#: Owner-specified sentinel (`OBJ-029` #9). ⛔ Never a blank cell, a dash or a
#: derived guess — a blank cannot be told apart from "not applicable".
NA = R.NOT_IN_JIRA

#: Regression-shaped record keys that must show the sentinel when empty rather
#: than a blank. Anything not listed here keeps its natural blank.
REGRESSION_FALLBACK = {
    "prev_working_version", "func_working_prev", "reopen_from_customer",
    "rca", "rca_details", "fixed_date", "reopen_rca", "reopen_rca_details",
    "reopen_original_id", "reopen_date", "reopen_time_spent", "rca_reviewed",
    "rca_review_remarks", "affected_build",
}

HDR_FILL = PatternFill("solid", fgColor="1F3864")
HDR_FONT = Font(color="FFFFFF", bold=True, size=10)
TITLE_FONT = Font(bold=True, size=13, color="1F3864")
NOTE_FONT = Font(italic=True, size=9, color="595959")
WARN_FONT = Font(bold=True, size=10, color="9C0006")
MONO = Font(name="Consolas", size=9)


# --------------------------------------------------------------------- cell safety

def _cell(v):
    """One value, safe for Excel.

    ⛔ Do not simplify the truncation away: an over-length cell makes Excel
    declare the file corrupt and drop the whole sheet on open, with no error at
    write time.

    ⚠️ The formula guard covers `=` ONLY. openpyxl promotes a string starting
    `=` to a formula cell; `+`, `-` and `@` are written as strings and render
    verbatim, so escaping them only added a visible apostrophe to every negative
    delta and every title beginning with a dash.
    """
    if v is None:
        return ""
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, (list, tuple, set)):
        v = " | ".join(str(x) for x in v)
    s = str(v)
    if len(s) > MAX_CELL:
        s = s[:MAX_CELL - len(TRUNC_MARK)] + TRUNC_MARK
    if s[:1] == "=":
        s = "'" + s
    return s


def _sheet(wb: Workbook, name: str, title: str, notes: list[str]) -> tuple:
    """A sheet with a title block, returning (ws, first_data_row)."""
    ws = wb.create_sheet(name[:31])
    ws["A1"] = title
    ws["A1"].font = TITLE_FONT
    row = 2
    for n in notes:
        ws.cell(row=row, column=1, value=_cell(n)).font = (
            WARN_FONT if n.startswith(("⛔", "⚠")) else NOTE_FONT)
        row += 1
    return ws, row + 1


def _header(ws, row: int, cols: list[str]) -> None:
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.fill, cell.font = HDR_FILL, HDR_FONT
        cell.alignment = Alignment(vertical="top", wrap_text=True)


def _write(ws, hrow: int, cols: list[str], rows: list[list], widths=None,
           table_name: str | None = None, wrap_from: int = 0) -> None:
    """Header + rows + autofilter + widths + freeze, in the order Excel wants."""
    _header(ws, hrow, cols)
    for r, data in enumerate(rows, hrow + 1):
        for c, v in enumerate(data, 1):
            cell = ws.cell(row=r, column=c, value=_cell(v))
            if wrap_from and c >= wrap_from:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
            else:
                cell.alignment = Alignment(vertical="top")
    last = hrow + len(rows)
    ncol = len(cols)
    if table_name and rows:
        ref = f"A{hrow}:{get_column_letter(ncol)}{last}"
        t = Table(displayName=table_name, ref=ref)
        t.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
        ws.add_table(t)
    elif rows:
        ws.auto_filter.ref = f"A{hrow}:{get_column_letter(ncol)}{last}"
    for i in range(1, ncol + 1):
        ws.column_dimensions[get_column_letter(i)].width = (
            widths[i - 1] if widths and i - 1 < len(widths) else 18)
    ws.freeze_panes = ws.cell(row=hrow + 1, column=1)


# ------------------------------------------------------------------ ticket universe

#: Pools the report counts over. `04 Ticket Details` is their union, and each pool
#: becomes a Yes/No column so a filter reproduces that pool's denominator exactly.
POOLS = [
    ("build_line", "Build line (Affected Milestone)",
     "Client tickets whose `Affected Milestone` names a 35.8.29 version. "
     "THE build-wise population (`D42`)."),
    ("focus", "Focus builds",
     "Full records for the in-flight builds — carries links and description."),
    ("last30", "Last 30 days",
     "Client tickets created in the window, independent of any version."),
    ("query_c", "Query C (open, unversioned)",
     "Open client defects carrying no fix version."),
]


def ticket_universe(A: dict) -> dict[str, dict]:
    """Every ticket the report counts, keyed by issue key, with pool flags.

    ⚠️ Records for the same key can arrive from two pools with different depth:
    the build line is fetched with `LIGHT_FIELDS` (no description, no links) and
    the other three with the full field set. The richer record wins, or the
    workbook would show an empty description for a ticket whose description was
    fetched — indistinguishable from a ticket that has none.
    """
    uni: dict[str, dict] = {}
    sources = {
        "build_line": A.get("trend_records") or [],
        "focus": A["focus"]["client_records"],
        "last30": A["current"]["records"],
        "query_c": A["query_c"]["records"],
    }
    for pool, recs in sources.items():
        for r in recs:
            k = r["key"]
            cur = uni.get(k)
            if cur is None:
                cur = dict(r)
                cur["_pools"] = set()
                uni[k] = cur
            elif r.get("desc_len", 0) > cur.get("desc_len", 0):
                pools = cur["_pools"]
                cur = dict(r)
                cur["_pools"] = pools
                uni[k] = cur
            uni[k]["_pools"].add(pool)
    return uni


# ------------------------------------------------------------------------- builders

def sheet_readme(wb: Workbook, A: dict, uni: dict) -> None:
    ws = wb.create_sheet("00 README")
    ws["A1"] = "PAM client-ticket analysis — consolidated workbook"
    ws["A1"].font = Font(bold=True, size=16, color="1F3864")
    rows = [
        ("Generated", A["generated"]),
        ("Current build", A["current_build"]),
        ("Source", "Jira PAMIT, read-only (jira_query.ReadOnlyJira)"),
        ("Objective", "OBJ-029 (supersedes the OBJ-028 methodology)"),
        ("", ""),
        ("THE BUILD AXIS", "Affected Milestone — customfield_10092 — 97.3% populated"),
        ("NOT the build axis", "Fix versions (where the fix ships, not where it was found)"),
        ("No usable axis", "every Milestone-named field: 0–9% populated — see '10 Field Audit'"),
        ("", ""),
        ("Build-line tickets (Affected Milestone)", A["trend_total"]),
        ("Build-line tickets (old fixVersion basis)", 1384),
        ("Tickets in this workbook (union of all pools)", len(uni)),
        ("Escaped defects (found earlier than fixed)", A["escape_am_escaped"]),
        ("Tickets stating a regression signal", A["regression"]["stated"]),
    ]
    r = 3
    for k, v in rows:
        ws.cell(row=r, column=1, value=_cell(k)).font = Font(bold=bool(k))
        ws.cell(row=r, column=2, value=_cell(v))
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Worksheets").font = TITLE_FONT
    r += 1
    _header(ws, r, ["Sheet", "What it holds", "Traceability"])
    manifest = [
        ("00 README", "This page — methodology, totals, sheet manifest",
         "—"),
        ("01 Testing Weak Spots", "One row per ticket per testing weak spot, with the "
         "PAM-specific recommendation for that weak spot",
         "Filter by 'Testing Weak Spot' → the row count is the reported count"),
        ("02 Weak Spot Summary", "One row per testing area: counts, shape, priority, "
         "root cause, existing/missing coverage, PAM recommendation",
         "'Tickets' column reconciles against sheet 01 and sheet 09"),
        ("03 Test Scenario Gaps", "One row per identified scenario gap, with the "
         "derivation method and the source of identification",
         "'Related tickets' lists every backing key; 'Source of identification' "
         "names the derivation"),
        ("04 Ticket Details", "THE SOURCE DATA. One row per ticket in the union of "
         "every counted pool, with all analysis fields and all pool/area flags",
         "Every other sheet's count is a filter over this one"),
        ("05 Build-wise", "Per build: found-count (Affected Milestone) beside "
         "fixed-count (fixVersion), defects, regression signal",
         "'Found (AM)' reconciles via COUNTIF on sheet 04"),
        ("06 Escape Latency", "Every ticket where the affected build precedes the fix "
         "build — the escape census",
         "One row per ticket; 'Hotfixes late' is the measured gap"),
        ("07 Regression Signal", "The three client-facing regression fields per ticket, "
         "with the derived class",
         "One row per ticket that states any regression signal"),
        ("08 Module & Category", "Module-wise and category-wise counts",
         "Both reconcile via COUNTIF on sheet 04"),
        ("09 Count Reconciliation", "Every headline count, beside a live COUNTIFS over "
         "sheet 04 and a PASS/FAIL formula",
         "This sheet IS the validation — Excel recomputes it on open"),
        ("10 Field Audit", "Every milestone-shaped and regression-shaped field measured, "
         "with population and verdict",
         "Explains why cf 10092 is the axis and the others are not, and names "
         "every fact marked 'Info not available in JIRA'"),
        ("11 RCA Analysis", "Jira's own root-cause taxonomy (cf 10245, 80.7% "
         "populated): every value, every family, the defect/non-defect/"
         "testing-failure class, and why reopened fixes failed",
         "Counts reconcile against the RCA column on sheet 04"),
        ("12 Daily History", "One row per retained dated snapshot with day-over-day "
         "deltas, so change across daily refreshes is trackable",
         "Derived from artifacts/client-tickets/snapshots/, which are never "
         "deleted and are the history's source of truth"),
    ]
    r += 1
    for m in manifest:
        for c, v in enumerate(m, 1):
            cell = ws.cell(row=r, column=c, value=_cell(v))
            cell.alignment = Alignment(vertical="top", wrap_text=True)
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="⛔ Rules this workbook obeys").font = WARN_FONT
    r += 1
    for line in [
        "ONE workbook. A new analysis area is a new worksheet here, never a new "
        ".xlsx file (D44).",
        "NO bare counts. Every reported figure has its tickets in sheet 04 and a "
        "live reconciliation formula in sheet 09 (D43).",
        "Build-wise counts key on Affected Milestone, never on Fix versions (D42).",
        "The three regression fields sit at ~25% population, so every regression "
        "figure is quoted over the populated subset with that subset's size beside "
        "it. 'Unstated' is an unfilled field, NOT evidence of 'no regression'.",
        "Per-build counts sum above the ticket total: 55 tickets name two in-family "
        "builds. The de-duplicated total is the population.",
        "REFRESHED DAILY, IN PLACE. The 09:00 PAM-Client-Ticket-Analysis task "
        "rebuilds this same file after each analysis (D45). History is not lost: "
        "the dated snapshots under artifacts/client-tickets/snapshots/ are "
        "retained for ever and sheet 12 is a view over them.",
        "'" + R.NOT_IN_JIRA + "' means Jira genuinely does not hold the fact - "
        "either the field does not exist, or it exists and is never populated, or "
        "it is empty on that ticket. It is never a blank cell, a dash, or a "
        "derived guess. Sheet 10 names every such field.",
    ]:
        ws.cell(row=r, column=1, value=_cell(line)).font = NOTE_FONT
        ws.cell(row=r, column=1).alignment = Alignment(vertical="top", wrap_text=True)
        r += 1
    for col, w in zip("ABC", (46, 62, 62)):
        ws.column_dimensions[col].width = w


WEAK_COLS = [
    "Ticket Number", "Testing Weak Spot / Gap", "Description",
    "Related Module / Feature", "Build / Version (Affected Milestone)",
    "Fixed In (Fix Version)", "Severity", "Priority", "Impact / Risk",
    "Possible Root Cause", "Existing Coverage", "Missing Coverage",
    "Recommended Precaution / Preventive Action",
    "Recommended Solution / Improvement", "PAM-specific Recommendation",
    "Suggested Test Coverage", "Recommended Automation Coverage",
    "Source / Evidence", "JIRA Reference", "Status / Remarks",
]


def sheet_weak_spots(wb: Workbook, A: dict, uni: dict, base_url: str) -> int:
    """Ticket-level weak spots: one row per (ticket, weak spot) pair."""
    ws, hrow = _sheet(
        wb, "01 Testing Weak Spots", "Testing weak spots — ticket level",
        ["One row per ticket per testing weak spot. A ticket appears once for each "
         "area it maps to, because a defect that is both a boundary failure and a "
         "compatibility failure is a gap in both kinds of testing.",
         "⚠ Areas are multi-label, so the row count exceeds the distinct-ticket "
         "count. Filter by 'Testing Weak Spot' to reproduce a reported area count "
         "exactly; de-duplicate 'Ticket Number' for the distinct figure.",
         "Root cause, coverage, precaution and the PAM recommendation are "
         "properties of the WEAK SPOT and repeat down its rows — that is "
         "deliberate, so a single filtered view is self-contained."])
    area_rows = {a["area"]: a for a in A["areas"]}
    rows = []
    for area in sorted(area_rows, key=lambda a: -area_rows[a]["count"]):
        ar = area_rows[area]
        d = R.area_detail(area)
        _gap, scenario = R.AREA_GAP.get(area, ("—", "—"))
        for key in ar["members"]:
            r = uni.get(key)
            if r is None:
                continue
            rows.append([
                key, area, r["summary"],
                " | ".join(r["components"]) or "«none»",
                " | ".join(r.get("affected_milestone") or []) or "«not set»",
                " | ".join(r["fix_versions"]) or "«none»",
                r.get("severity") or "«not set»", r["priority"],
                f"{ar['shape']} / priority {ar['priority']} — area carries "
                f"{ar['count']} tickets ({ar['share_pct']}), "
                f"{ar['showstoppers']} ShowStopper, {ar['clients']} clients",
                d["root_cause"], d["existing_coverage"], d["missing_coverage"],
                d["precaution"], scenario, d["pam_recommendation"],
                d["suggested_coverage"], d["automation"],
                f"Jira field data + derived testing-area axis "
                f"(title+description match); category={r['category']} "
                f"(source: {r.get('category_source', '?')})",
                f"{base_url}/browse/{key}",
                f"{r['status']} — {r['issuetype']}; client {r['client']}; "
                f"created {r['created']}; regression: {r['regression_class']}",
            ])
    _write(ws, hrow, WEAK_COLS, rows,
           widths=[14, 26, 52, 20, 22, 18, 12, 12, 40, 46, 40, 40, 46, 46, 66,
                   40, 34, 40, 34, 42],
           table_name="TestingWeakSpots", wrap_from=3)
    return len(rows)


SUMMARY_COLS = [
    "Testing Weak Spot / Area", "Tickets", "Share of pool", "Shape", "Priority",
    "Confidence", "ShowStoppers", "Clients affected", "Modules affected",
    "Gap identified", "Possible Root Cause", "Existing Coverage",
    "Missing Coverage", "Recommended Precaution", "Recommended Solution",
    "PAM-specific Recommendation", "Suggested Test Coverage",
    "Recommended Automation Coverage", "Evidence tickets (first 6)",
    "All backing tickets",
]


def sheet_weak_summary(wb: Workbook, A: dict) -> None:
    ws, hrow = _sheet(
        wb, "02 Weak Spot Summary", "Testing weak spots — area summary",
        ["One row per testing area. 'Tickets' is the count reported in the "
         "analysis; 'All backing tickets' lists every key behind it.",
         "Share is of the distinct tickets across the three full-record pools "
         "(focus builds, last 30 days, Query C). Areas are multi-label, so shares "
         "sum past 100%.",
         "⚠ Priority is density-based, not volume-based: an area is High when its "
         "share is >=15% or it carries >=10 tickets with >=45% ShowStopper. "
         "ShowStopper is not rare in this data, so an absolute-count rule marked "
         "every area High."])
    rows = []
    for a in A["areas"]:
        d = R.area_detail(a["area"])
        gap, scenario = R.AREA_GAP.get(a["area"], ("—", "—"))
        rows.append([
            a["area"], a["count"], a["share_pct"], a["shape"], a["priority"],
            a["confidence"], f"{a['showstoppers']} ({a['ss_share_pct']})",
            a["clients"], len(a["modules"]), gap,
            d["root_cause"], d["existing_coverage"], d["missing_coverage"],
            d["precaution"], scenario, d["pam_recommendation"],
            d["suggested_coverage"], d["automation"],
            " ".join(a["evidence"]), " ".join(a["members"]),
        ])
    _write(ws, hrow, SUMMARY_COLS, rows,
           widths=[28, 9, 12, 10, 10, 14, 14, 10, 10, 44, 46, 40, 40, 46, 46,
                   70, 42, 36, 30, 60],
           table_name="WeakSpotSummary", wrap_from=10)


GAP_COLS = [
    "Test Scenario Name", "Test Scenario Gap", "Related Module / Feature",
    "Related Ticket Number(s)", "Ticket count", "Build / Version (Affected Milestone)",
    "Expected Behavior", "Existing Test Coverage", "Missing Coverage",
    "Risk / Impact", "Source of Identification", "Derivation method",
    "Recommended Test Scenario", "Recommended Automation Coverage", "Remarks",
]

#: How each scenario gap was arrived at. ⛔ The owner's requirement is that the
#: *provenance* of every gap is traceable, so this is a per-area statement of which
#: evidence produced it, not a generic label.
GAP_PROVENANCE = {
    "derivation": (
        "Derived, not authored. Three ordered steps, each mechanical: "
        "(1) every client ticket in the three full-record pools is matched against "
        "the testing-area axis in `pamit_analysis_rules.testing_areas()` — a "
        "word-boundary term match over title + first 1,500 chars of description, "
        "multi-label; (2) an area qualifies as a gap only at >=3 tickets from >=2 "
        "distinct clients (`confidence = measured`) — a single client's tickets are "
        "an incident, not a coverage gap; (3) the gap statement and recommended "
        "scenario come from `AREA_GAP`, and the PAM-specific detail from "
        "`AREA_DETAIL`, both keyed on the area."),
    "sources": {
        "primary": "Client-raised JIRA tickets (production/customer issues) — the "
                   "population, via Affected Milestone",
        "secondary": "Previous build/version behaviour — the three regression "
                     "fields, where populated",
        "tertiary": "Existing automation coverage — the bootstrap suite inventory "
                    "(what the framework can already do vs what it is run with)",
        "not_used": "Requirements, user stories and functional specifications were "
                    "NOT used: PAMIT holds no requirement links, and the product "
                    "documentation is confirmed not up to date. Any gap claiming a "
                    "requirement source would be unfounded.",
    },
}


def sheet_scenario_gaps(wb: Workbook, A: dict, uni: dict) -> None:
    P = GAP_PROVENANCE
    ws, hrow = _sheet(
        wb, "03 Test Scenario Gaps", "Test scenario gaps — with derivation",
        ["METHODOLOGY. " + P["derivation"],
         "SOURCE OF IDENTIFICATION — primary: " + P["sources"]["primary"],
         "  secondary: " + P["sources"]["secondary"],
         "  tertiary: " + P["sources"]["tertiary"],
         "⛔ NOT USED: " + P["sources"]["not_used"],
         "⚠ A gap below the >=3 tickets / >=2 clients threshold is excluded and "
         "listed at the bottom as 'insufficient evidence' rather than dropped "
         "silently — an excluded area is information."])
    rows, weak = [], []
    for a in A["areas"]:
        d = R.area_detail(a["area"])
        gap, scenario = R.AREA_GAP.get(a["area"], ("—", "—"))
        builds = collections.Counter()
        for k in a["members"]:
            for b in (uni.get(k, {}).get("affected_builds") or []):
                builds[b] += 1
        row = [
            f"{a['area']} — core journeys", gap,
            " | ".join(sorted(a["modules"])[:12]),
            " ".join(a["members"]), a["count"],
            " | ".join(f"{b} ({n})" for b, n in builds.most_common(8)) or "«not set»",
            d["existing_coverage"].split(".")[0] + "." if d["existing_coverage"]
            else "—",
            d["existing_coverage"], d["missing_coverage"],
            f"{a['shape']} / priority {a['priority']} — {a['count']} tickets "
            f"({a['share_pct']}) from {a['clients']} clients, "
            f"{a['showstoppers']} ShowStopper ({a['ss_share_pct']})",
            "Client-raised JIRA tickets (production/customer issues); "
            f"{a['count']} tickets from {a['clients']} distinct clients across "
            f"{len(a['modules'])} modules",
            "Testing-area term match over ticket title + description, "
            ">=3 tickets from >=2 clients required",
            scenario, d["automation"],
            d["pam_recommendation"],
        ]
        (rows if a["confidence"] == "measured" else weak).append(row)
    for w in weak:
        w[14] = "EXCLUDED — insufficient evidence (<3 tickets or <2 clients). " + w[14]
    _write(ws, hrow, GAP_COLS, rows + weak,
           widths=[34, 44, 26, 56, 11, 30, 40, 40, 40, 46, 46, 40, 50, 34, 70],
           table_name="TestScenarioGaps", wrap_from=2)


TICKET_COLS = [
    ("key", "Ticket Number"), ("summary", "Summary"),
    ("_desc", "Description"), ("issuetype", "Issue Type"),
    ("status", "Status"), ("status_category", "Status Category"),
    ("priority", "Priority"), ("_severity", "Severity"),
    ("_hosting", "Environment (Hosting Environment)"),
    ("_am", "Affected Milestone (ALL values)"),
    ("affected_build", "Affected Milestone — attributed build"),
    ("_am_other", "Affected Milestone — other build line"),
    ("_fixv", "Fixed Version(s)"), ("release", "Fix release (short)"),
    ("_milestone", "Milestone"),
    ("prev_working_version", "Previous Working Version"),
    ("func_working_prev", "Functionality Working in Previous Version"),
    ("reopen_from_customer", "Is Reopen from Customer"),
    ("regression_class", "Regression class (derived)"),
    # --- RCA: Jira's own root-cause taxonomy, 80.7% populated (`OBJ-029` #9)
    ("rca", "RCA"), ("rca_family", "RCA family"),
    ("rca_class", "RCA class (derived)"),
    ("rca_details", "RCA Details (Impact Analysis)"),
    ("fixed_date", "Fixed Date"),
    ("reopen_rca", "Reopen RCA"),
    ("reopen_rca_details", "Reopen RCA details"),
    ("reopen_original_id", "Reopen Original Ticket ID"),
    ("reopen_date", "ReOpen Date"),
    ("reopen_time_spent", "ReOpen Time Spent (hrs)"),
    ("rca_reviewed", "RCA Category / Description updated?"),
    ("rca_review_remarks", "RCA Review Remarks"),
    # --- fields that EXIST in the Jira schema but are never populated. Carried as
    # ⛔ explicit columns rather than omitted: a missing column reads as "not
    # analysed", while a column reading `Info not available in JIRA` all the way
    # down states the fact the owner asked to be stated.
    ("_phase", "Defect Injection Phase"),
    ("_reopen_count", "ReopenCount"),
    ("_components", "Module / Component"),
    ("client", "Primary Client (normalised)"),
    ("client_raw", "Primary Client (raw)"),
    ("_reporter", "Reporter"), ("_assignee", "Assignee"),
    ("created", "Created Date"), ("updated", "Updated Date"),
    ("_resolution", "Resolution"), ("category", "Issue Category (derived)"),
    ("category_source", "Category source"),
    ("_areas", "Testing areas (derived)"),
    ("_labels", "Labels"), ("parent", "Parent"),
    ("_links", "Linked tickets"), ("env_config", "Env/config-sensitive"),
    ("is_defect", "Counted as defect"), ("is_distinct", "Counted as distinct"),
    ("is_internal", "Internal (excluded from client counts)"),
]


def sheet_ticket_details(wb: Workbook, A: dict, uni: dict, base_url: str) -> int:
    """The source data. Every count in the report is a filter over this sheet."""
    areas_all = [a["area"] for a in A["areas"]]
    ws, hrow = _sheet(
        wb, "04 Ticket Details", "Ticket details — the source data",
        [f"{len(uni)} tickets: the union of every pool the analysis counts. "
         "Every reported figure is reproducible as a filter over this sheet, "
         "which is what makes the counts verifiable rather than asserted.",
         "Pool columns (Yes/No) give each population its own denominator. Area "
         "columns (Yes/No) give each testing weak spot its count.",
         "⚠ 'Milestone' is intentionally near-empty: PAMIT has no usable Milestone "
         "field. See sheet '10 Field Audit'. The build axis is Affected Milestone.",
         "⚠ Description is flattened from Atlassian Document Format and truncated "
         "at Excel's 32,767-character cell limit where necessary."])
    cols = ([h for _, h in TICKET_COLS]
            + [f"Pool: {lbl}" for _, lbl, _ in POOLS]
            + [f"Area: {a}" for a in areas_all]
            + ["JIRA Reference"])
    area_member = {a["area"]: set(a["members"]) for a in A["areas"]}
    rows = []
    for key in sorted(uni):
        r = uni[key]
        get = {
            "_desc": r.get("_description", ""),
            "_severity": r.get("severity") or NA,
            "_hosting": r.get("hosting_env") or NA,
            "_am": r.get("affected_milestone") or [],
            "_am_other": r.get("affected_other_line") or [],
            "_fixv": r.get("fix_versions") or [],
            "_milestone": NA,
            # ⛔ Whole-field unavailable in PAMIT — see `REGRESSION_AUDIT`.
            "_phase": NA,
            "_reopen_count": NA,
            "_components": r.get("components") or ["«none»"],
            "_reporter": r.get("reporter_name") or "",
            "_assignee": r.get("assignee_name") or "",
            "_resolution": r.get("resolution_name") or "«not set»",
            "_areas": r.get("areas") or [],
            "_labels": r.get("labels") or [],
            "_links": [f"{t}:{k}" for t, _, k in (r.get("links") or [])],
        }
        # ⛔ An empty regression cell is exactly the ambiguity the owner asked to
        # remove, so every regression-shaped field falls back to the sentinel
        # rather than to a blank. Non-regression fields keep their natural blank:
        # marking an empty `Labels` cell "Info not available in JIRA" would be
        # noise, not information.
        row = [get[f] if f in get
               else (r.get(f) if r.get(f) not in (None, "", [])
                     else (NA if f in REGRESSION_FALLBACK else r.get(f)))
               for f, _ in TICKET_COLS]
        row += ["Yes" if p in r["_pools"] else "No" for p, _, _ in POOLS]
        row += ["Yes" if key in area_member[a] else "No" for a in areas_all]
        row += [f"{base_url}/browse/{key}"]
        rows.append(row)
    base_w = [14, 60, 70, 14, 16, 14, 12, 12, 22, 26, 24, 22, 22, 12, 24, 22,
              26, 20, 22, 30, 18, 20, 46, 14, 22, 40, 24, 14, 16, 26, 40,
              26, 18, 22, 22, 22, 22, 20, 20, 12, 12, 14, 26, 14, 30, 20, 14,
              34, 14, 14, 14, 14]
    widths = ([base_w[i] if i < len(base_w) else 20 for i in range(len(TICKET_COLS))]
              + [14] * len(POOLS) + [12] * len(areas_all) + [40])
    _write(ws, hrow, cols, rows, widths=widths, table_name="TicketDetails")
    return hrow


BUILD_COLS = [
    "Build", "Short", "Jira release date", "Flagged released", "Is current",
    "In focus", "Found here (Affected Milestone)", "Fixed here (same population)",
    "Defects (distinct)", "ShowStoppers", "Distinct clients",
    "Regression stated", "Regression confirmed", "Reopen from customer = Yes",
    "First ticket", "Latest ticket", "Top module", "Top named category",
    "Uncategorised %",
]


def sheet_builds(wb: Workbook, A: dict) -> None:
    ws, hrow = _sheet(
        wb, "05 Build-wise", "Build-wise analysis — Affected Milestone basis",
        ["⛔ 'Found here' is the build-wise count: tickets whose Affected Milestone "
         "names this build — where the client FOUND the defect (D42).",
         "⚠ 'Fixed here' counts tickets WITHIN this same Affected-Milestone "
         "population whose fix version names this build — the same 2,010 tickets "
         "seen from both ends, so the found-vs-fixed divergence is visible per "
         "row. It is NOT the standalone 1,384-ticket fixVersion population the "
         "superseded methodology used; those figures are in the report's §0.1.",
         "⚠ Regression columns are over the ~25%-populated subset. 'Regression "
         "stated' is the denominator for 'Regression confirmed', never 'Found here'.",
         "⚠ Ordering is by build number. Jira releaseDate is a planned date and is "
         "non-monotonic here (HF13 2026-06-22 precedes HF12 2026-07-31), so it "
         "orders nothing."])
    rows = [[b["build"], b["short"], b["release_date"],
             "Yes" if b["released"] else "No",
             "Yes" if b["is_current"] else "No",
             "Yes" if b["in_focus"] else "No",
             b["client"], b["client_by_fixversion"], b["defects"],
             b["showstoppers"], b["clients"], b["reg_stated"],
             b["reg_confirmed"], b["reopen_yes"],
             b["first_ticket"], b["latest_ticket"], b["top_module"],
             b["top_category"], b["uncategorised_pct"]]
            for b in A["builds"]]
    tot: list = ["TOTAL (per-build sum)", "", "", "", "", ""]
    for i in range(6, 14):
        tot.append(sum(r[i] for r in rows if isinstance(r[i], int)))
    tot += ["", "", "", "", ""]
    rows.append(tot)
    rows.append([f"DISTINCT TICKETS = {A['trend_total']}", "", "", "", "", "",
                 A["trend_total"], "", "", "", "", "", "", "", "", "", "",
                 "55 tickets name two in-family builds, so the per-build sum "
                 "exceeds the distinct total", ""])
    _write(ws, hrow, BUILD_COLS, rows,
           widths=[20, 10, 16, 14, 11, 10, 24, 22, 17, 13, 14, 16, 18, 22, 13,
                   13, 20, 26, 15], wrap_from=17)


def sheet_escape(wb: Workbook, A: dict, base_url: str) -> None:
    ws, hrow = _sheet(
        wb, "06 Escape Latency", "Escape latency — found-on build vs fixed-in build",
        ["One row per ticket carrying an in-family Affected Milestone AND an "
         "in-family fix version. 'Hotfixes late' = fix build number minus affected "
         "build number.",
         "⛔ The previous methodology recovered the found-on build from build tokens "
         f"typed into ticket titles and reported 9 rows. This is a field-based "
         f"census: {A['escape_am_escaped']} escaped defects. Where both methods "
         "fire they agree.",
         "⚠ A negative 'Hotfixes late' is a data anomaly (fix version earlier than "
         "affected build), not an escape. Those rows are retained for correction."])
    rows = [[e["key"], e["client"], e["component"], e["category"], e["priority"],
             e["found_build"], e["fixed_build"], e["hotfixes_late"],
             "Yes" if e["escaped"] else "No", e["regression_class"],
             e["title"], f"{base_url}/browse/{e['key']}"]
            for e in A["escape_am"]]
    _write(ws, hrow,
           ["Ticket Number", "Primary Client", "Module", "Issue Category",
            "Priority", "Found on (Affected Milestone)", "Fixed in (Fix Version)",
            "Hotfixes late", "Escaped", "Regression class", "Title",
            "JIRA Reference"],
           rows, widths=[14, 26, 20, 28, 13, 26, 22, 13, 10, 22, 60, 40],
           table_name="EscapeLatency", wrap_from=11)


def sheet_regression(wb: Workbook, A: dict, base_url: str) -> None:
    RG = A["regression"]
    ws, hrow = _sheet(
        wb, "07 Regression Signal", "Regression signal — the three client-facing fields",
        [f"{RG['stated']} of {RG['population']} build-line tickets "
         f"({RG['stated_pct']}) state a regression signal. Only those are listed.",
         "⛔ " + RG["confidence"],
         "⚠ 'Previous Working Version' is a select field whose option list includes "
         "the literal string 'None'. That is not the same as an empty field: it "
         "means 'no previously working version'. 130 tickets carry it, and treating "
         "it as a version would corrupt every bisect range.",
         "Derived class: confirmed-regression = worked before AND the version is "
         "named; likely-regression = worked before, version not named; "
         "not-a-regression = did not work before; customer-reopen = reopened, "
         "regression status not stated."])
    rows = [[r["key"], r["issuetype"], r["status"], r["priority"], r["client"],
             " | ".join(r["components"]) or "«none»",
             r.get("affected_build") or "«not set»",
             " | ".join(r["fix_versions"]) or "«none»",
             r.get("func_working_prev") or "«not set»",
             r.get("prev_working_version") or "«not set»",
             r.get("reopen_from_customer") or "«not set»",
             r["regression_class"],
             R.REGRESSION_CLASSES.get(r["regression_class"], ""),
             (f"{r.get('prev_working_version')} → {r.get('affected_build')}"
              if r["regression_class"] == "confirmed-regression" else "—"),
             r["category"], r["summary"], f"{base_url}/browse/{r['key']}"]
            for r in sorted(RG["records"],
                            key=lambda x: (x["regression_class"], x["key"]))]
    _write(ws, hrow,
           ["Ticket Number", "Issue Type", "Status", "Priority", "Primary Client",
            "Module / Component", "Affected Milestone", "Fixed Version(s)",
            "Functionality Working in Previous Version", "Previous Working Version",
            "Is Reopen from Customer", "Regression class (derived)",
            "Class meaning", "Bisect range (prev working → affected)",
            "Issue Category", "Summary", "JIRA Reference"],
           rows, widths=[14, 14, 16, 12, 24, 24, 22, 22, 26, 24, 20, 22, 44, 34,
                         26, 60, 40], table_name="RegressionSignal", wrap_from=13)


def sheet_module_category(wb: Workbook, A: dict) -> None:
    ws, hrow = _sheet(
        wb, "08 Module & Category", "Module-wise and category-wise counts",
        ["Both axes over the focus-build client defects, the same population the "
         "report's §4 and §5 use.",
         "⚠ 'All Modules' is used as a component on a meaningful share of tickets. "
         "It is a non-answer for module attribution and those tickets cannot be "
         "assigned to a real module.",
         "⚠ 'Uncategorised' is a taxonomy-coverage figure, not a finding."])
    F = A["focus"]
    from pamit_fmt import tally
    mods = tally(F["defects"], lambda r: r["components"] or ["«none»"])
    cats = tally(F["defects"], lambda r: r["category"])
    base = len(F["defects"])
    rows = [["MODULE", m, n, f"{100 * n / base:.1f}%" if base else "—"]
            for m, n in mods.most_common()]
    rows += [["CATEGORY", c, n, f"{100 * n / base:.1f}%" if base else "—"]
             for c, n in cats.most_common()]
    _write(ws, hrow, ["Axis", "Value", "Defects", "Share of focus defects"],
           rows, widths=[12, 46, 12, 22], table_name="ModuleCategory")


def sheet_reconciliation(wb: Workbook, A: dict, uni: dict, td_hrow: int,
                         weak_rows: int) -> None:
    """Every headline count beside a live COUNTIFS over `04 Ticket Details`.

    ⛔ The formulas are the point. A number this script computes and also prints
    proves nothing — both come from the same code. A COUNTIFS Excel evaluates
    against the source sheet is an independent check the reader can see, and it
    keeps working if someone edits the data.
    """
    ws, hrow = _sheet(
        wb, "09 Count Reconciliation", "Count reconciliation — every total, verified",
        ["Column C is what the analysis computed. Column D is a live COUNTIFS over "
         "'04 Ticket Details' that Excel recomputes when the file opens. Column E "
         "compares them.",
         "⛔ This sheet is the validation the owner asked for: no reported count is "
         "left as an assertion. If any row reads FAIL, the analysis and the source "
         "data disagree and the analysis is wrong.",
         "⚠ Per-build counts are deliberately NOT summed to the population: 55 "
         "tickets name two in-family builds, so the sum exceeds the distinct total. "
         "The build rows below each reconcile individually."])
    n = len(uni)
    first, last = td_hrow + 1, td_hrow + n
    td = "'04 Ticket Details'"
    cols = {h: get_column_letter(i + 1)
            for i, (_, h) in enumerate(TICKET_COLS)}
    pcol = {p: get_column_letter(len(TICKET_COLS) + i + 1)
            for i, (p, _, _) in enumerate(POOLS)}
    acol = {a["area"]: get_column_letter(len(TICKET_COLS) + len(POOLS) + i + 1)
            for i, a in enumerate(A["areas"])}

    def cf(col: str, val: str) -> str:
        return f'=COUNTIFS({td}!{col}{first}:{col}{last},"{val}")'

    rows = []

    def add(section, label, value, formula, note):
        rows.append([section, label, value, formula, None, note])

    add("Population", "Tickets in this workbook (union of all pools)", n,
        f"=COUNTA({td}!A{first}:A{last})",
        "Every row of the source sheet. All other counts are filters over it.")
    for p, lbl, desc in POOLS:
        val = {"build_line": A["trend_total"],
               "focus": A["focus"]["counts"]["client"],
               "last30": A["current"]["counts"]["tickets"],
               "query_c": A["query_c"]["count"]}[p]
        add("Pool", lbl, val, cf(pcol[p], "Yes"), desc)
    add("Pool", "Build line — old fixVersion basis (for comparison only)", 1384,
        "", "⛔ NOT the methodology. Shown to make the +45% axis change visible.")

    add("Regression", "Tickets stating any regression signal",
        A["regression"]["stated"],
        f'=COUNTIFS({td}!{cols["Regression class (derived)"]}{first}:'
        f'{cols["Regression class (derived)"]}{last},"<>unstated",'
        f'{td}!{pcol["build_line"]}{first}:{pcol["build_line"]}{last},"Yes")',
        "Over the build line. ~25% population — the denominator for every "
        "regression share.")
    for k, v in A["regression"]["by_class"].most_common():
        add("Regression", f"Regression class = {k}", v,
            f'=COUNTIFS({td}!{cols["Regression class (derived)"]}{first}:'
            f'{cols["Regression class (derived)"]}{last},"{k}",'
            f'{td}!{pcol["build_line"]}{first}:{pcol["build_line"]}{last},"Yes")',
            R.REGRESSION_CLASSES.get(k, ""))

    for a in A["areas"]:
        add("Testing weak spot", a["area"], a["count"], cf(acol[a["area"]], "Yes"),
            f"{a['shape']} / {a['priority']} — {a['clients']} clients, "
            f"{a['showstoppers']} ShowStopper. Sheet 01 carries the ticket rows.")

    for b in A["builds"]:
        add("Build (Affected Milestone)", b["build"], b["client"],
            f'=COUNTIFS({td}!{cols["Affected Milestone (ALL values)"]}{first}:'
            f'{cols["Affected Milestone (ALL values)"]}{last},"*{b["build"]}*")',
            "Wildcard match: a multiselect cell can hold two builds, which is why "
            "the per-build sum exceeds the distinct total.")

    add("Escape latency", "Tickets with both an affected build and a fix build",
        len(A["escape_am"]), "", "Sheet 06 carries every row.")
    add("Escape latency", "Escaped (fixed later than found)",
        A["escape_am_escaped"], "",
        "⛔ Previous methodology reported 9, recovered from title text.")
    add("Weak spots", "Rows on sheet 01 (ticket x weak spot pairs)", weak_rows, "",
        "Exceeds the distinct-ticket count because areas are multi-label.")

    _header(ws, hrow, ["Section", "Reported figure", "Analysis value",
                       "Live COUNTIFS over sheet 04", "Match", "Note"])
    r = hrow + 1
    for section, label, value, formula, _m, note in rows:
        ws.cell(row=r, column=1, value=_cell(section))
        ws.cell(row=r, column=2, value=_cell(label))
        ws.cell(row=r, column=3, value=value)
        if formula:
            ws.cell(row=r, column=4, value=formula).font = MONO
            ws.cell(row=r, column=5,
                    value=f'=IF(C{r}=D{r},"PASS","FAIL — differs by "&(D{r}-C{r}))')
        else:
            ws.cell(row=r, column=4, value="—")
            ws.cell(row=r, column=5, value="not filter-reproducible")
        c6 = ws.cell(row=r, column=6, value=_cell(note))
        c6.alignment = Alignment(vertical="top", wrap_text=True)
        r += 1
    ws.auto_filter.ref = f"A{hrow}:F{r - 1}"
    for col, w in zip("ABCDEF", (24, 52, 15, 62, 30, 64)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = ws.cell(row=hrow + 1, column=1)



def sheet_rca(wb: Workbook, A: dict, base_url: str) -> None:
    """Jira's own root-cause taxonomy — the field the report had declared absent."""
    RC = A["rca"]
    ws, hrow = _sheet(
        wb, "11 RCA Analysis", "Root cause — Jira's own taxonomy (cf 10245)",
        [f"`RCA` is populated on {RC['stated']} of {RC['population']} build-line "
         f"tickets ({RC['stated_pct']}) with {len(RC['by_value'])} values in "
         f"{len(RC['by_family'])} families. It is the most populated analytical "
         "field in the project.",
         "⛔ The report previously stated Jira held no root-cause categorisation. "
         "That measured `cf 10113` (0.2%) and `cf 10199` (0.1%) — two decoy "
         "fields — and never `cf 10245`. Same error class as the "
         "`affectedVersion` miss behind D42.",
         "⛔ `non-defect` rows are tickets the PRODUCT TEAM classified as not a "
         "defect (enhancement, information request, working as expected, not a "
         "bug). A testing weak spot attributed to one of these is a FALSE "
         "FINDING. ⚠ Reported, not silently applied: the defect population stays "
         "keyed on issue type (D38), because re-cutting a denominator on a field "
         "that is 19% empty would be a worse error.",
         "✅ `testing-failure` rows name a testing or analysis failure as the "
         "root cause — the strongest evidence in the analysis for a testing gap, "
         "because it was recorded by the product team rather than inferred."])
    rows = []
    for v, n in RC["by_value"].most_common():
        rows.append(["VALUE", v, R.rca_family(v), R.rca_class(v), n,
                     pct(n, RC["stated"]), ""])
    for k, n in RC["by_family"].most_common():
        rows.append(["FAMILY", k, "", "", n, pct(n, RC["stated"]), ""])
    for k, n in RC["by_class"].most_common():
        rows.append(["CLASS", k, "", "", n, pct(n, RC["population"]),
                     "share is of the whole population, not of stated"])
    for k, n in RC["reopen_rca"].most_common():
        rows.append(["REOPEN RCA", k, "", "", n, "", "why a delivered fix failed"])
    _write(ws, hrow,
           ["Axis", "Value", "Family", "Class", "Tickets", "Share", "Note"],
           rows, widths=[14, 48, 22, 18, 11, 11, 52], table_name="RCAAnalysis",
           wrap_from=7)


def sheet_daily_history(wb: Workbook, snapshots: list[dict]) -> None:
    """Day-over-day history, so a daily refresh can be tracked rather than lost.

    ⛔ OWNER REQUIREMENT (`OBJ-029` #8): the master workbook is refreshed daily
    IN PLACE, and previous data is retained so change across days is trackable.
    The workbook itself is overwritten each day, so history cannot live in the
    other sheets — it is rebuilt here from the retained dated snapshots under
    `artifacts/client-tickets/snapshots/`, which are never deleted.

    ⚠️ That is why this sheet is derived rather than appended: an appended sheet
    would be lost the first time the workbook was rebuilt from scratch, and would
    silently disagree with the snapshots. The snapshots are the source of truth
    for history; this sheet is a view over them.
    """
    ws, hrow = _sheet(
        wb, "12 Daily History", "Daily history — tracked across refreshes",
        ["One row per dated snapshot under `artifacts/client-tickets/snapshots/`. "
         "Those files are retained and never deleted, so they are the history; "
         "this sheet is a view over them and is rebuilt on every refresh.",
         "⚠ A break in the date sequence means the daily job did not run that "
         "day — the gap is visible rather than smoothed over.",
         "⚠ Figures before the OBJ-029 methodology change are on the OLD "
         "`fixVersion` build-line basis and are NOT comparable with later rows. "
         "The 'Basis' column says which.",
         "⚠ 'Build line (per-build sum)' is the sum of the per-build counts a "
         "snapshot records, NOT the de-duplicated ticket total — a snapshot does "
         "not store the total. For 2026-08-31 the sum is 2,025 against a "
         "de-duplicated population of 2,010, the difference being tickets whose "
         "Affected Milestone names two in-family builds."])
    rows = []
    prev = None
    for snap in snapshots:
        bl = snap.get("build_line")
        basis = snap.get("basis") or ("Affected Milestone (D42)" if
                                      (bl or 0) > 1500 else "fixVersion (superseded)")
        row = [snap.get("date", "?"), snap.get("generated", ""), basis, bl,
               snap.get("focus_client"), snap.get("focus_defects"),
               snap.get("window_tickets"), snap.get("query_c")]
        for i, key in enumerate(("build_line", "focus_client", "focus_defects",
                                 "window_tickets", "query_c")):
            cur, was = snap.get(key), (prev or {}).get(key)
            row.append("—" if prev is None or cur is None or was is None
                       else ("0" if cur == was else f"{cur - was:+d}"))
        rows.append(row)
        prev = snap
    _write(ws, hrow,
           ["Date", "Generated", "Build-line basis", "Build line (per-build sum)",
            "Focus client",
            "Focus defects", "30-day window", "Query C",
            "Δ build line", "Δ focus client", "Δ focus defects",
            "Δ window", "Δ Query C"],
           rows, widths=[12, 18, 28, 12, 13, 14, 14, 11, 13, 15, 15, 12, 13],
           table_name="DailyHistory")


def sheet_field_audit(wb: Workbook) -> None:
    ws, hrow = _sheet(
        wb, "10 Field Audit", "Jira field audit — which field, and why",
        ["Every milestone-shaped and regression-shaped field in this Jira instance, "
         "measured against the PAMIT client population.",
         "⛔ Three fields are named 'Affected Milestone'-something and two are empty "
         "on PAMIT. Selecting one of those returns an empty build line, which reads "
         "as a clean result rather than a wrong query. That is why the whole set is "
         "recorded rather than only the chosen field."])
    rows = [
        ["customfield_10092", "Affected Milestone.", "array / multiselect",
         "1,346 / 1,384 = 97.3%", "✅ THE BUILD AXIS",
         "The build the client was running. Trailing period is part of the name.",
         "Every build-wise count keys on this (D42)."],
        ["fixVersions", "Fix versions", "array / native",
         "100% of the versioned slice", "✅ secondary axis only",
         "The release the fix ships in.",
         "Used only as the second axis of escape latency."],
        ["customfield_10214", "Affected Milestone", "array / multiselect",
         "0 / 1,384", "⛔ rejected", "Not on the PAMIT screen.",
         "Name collision with the real field. Do not select."],
        ["customfield_10219", "Affected Milestone", "array / multiselect",
         "0 / 1,384", "⛔ rejected", "Not on the PAMIT screen.",
         "Name collision with the real field. Do not select."],
        ["customfield_10143", "Custom Affected Milestone (**Only use if …)",
         "string / textarea", "0 / 1,384", "⛔ rejected",
         "Free-text escape hatch for a version missing from the list.", "Unused."],
        ["customfield_10174", "Custom Affected Milestone (**Only use if …)",
         "string / textarea", "0 / 1,384", "⛔ rejected",
         "Free-text escape hatch.", "Unused."],
        ["versions", "Affects versions", "array / native", "0 / 1,384",
         "⛔ rejected — and consequential",
         "Unused project-wide.",
         "⛔ THIS is the field the previous methodology checked. Finding it empty, "
         "it concluded no field records the build a client was on, and fell back to "
         "parsing build tokens out of ticket titles."],
        ["customfield_10100", "Release Milestone.", "array / multiselect", "9%",
         "⛔ rejected",
         "Legacy. Values are unrelated old lines (35.8.13 HF 7, "
         "4.8.5.0_U16SP2_B35.8.21), all singletons.",
         "No usable signal."],
        ["customfield_10238", "Forward Merge Milestone", "array / multiselect",
         "63% populated", "⛔ rejected",
         "344 of 388 values are the literal string 'None'.",
         "Population without information — the trap this audit exists to catch."],
        ["customfield_10131", "Release Milestone", "array / multiselect", "0%",
         "⛔ rejected", "Unused.", ""],
        ["customfield_10221", "PAM_Release Milestone", "option / radiobuttons",
         "0%", "⛔ rejected", "Unused.", ""],
        ["customfield_10223", "CI_Release_Milestone", "array / multiselect", "0%",
         "⛔ rejected", "Unused.", ""],
        ["customfield_10780", "Is reopen from customer", "option / select",
         "512 / 2,010 = 25.5% (47 = Yes)", "✅ in use",
         "The customer re-opened after a delivered fix — a failed fix, not a new "
         "defect.",
         "Was already captured before this revision but never used in a view. Now "
         "drives the regression classification and escalates the weak spot that "
         "produced it."],
        ["customfield_11253", "Functionality working in previous version",
         "option / select", "499 / 2,010 = 24.8% (275 Yes / 224 No)", "✅ NEW",
         "Yes = the feature worked before, so the defect is a regression.",
         "The regression gate. Yes promotes a ticket into the regression "
         "population."],
        ["customfield_11254", "Previous working version", "option / select",
         "491 / 2,010 = 24.4% (130 of them the literal 'None')", "✅ NEW",
         "The last build where it worked.",
         "Turns a regression into a bisect range: (previous working, affected "
         "milestone]. ⚠ 'None' is an option value, not an empty field."],
        ["customfield_10190", "Severity", "option / select", "~11%",
         "⚠ too sparse", "Impact severity.",
         "priority (100% populated) is used for impact instead."],
        ["customfield_11220", "Hosting Environment", "option / select", "~62%",
         "✅ in use", "Client deployment shape.",
         "Environment classification, alongside title text."],
        ["customfield_10112", "Primary Client", "option / select", "100%",
         "✅ in use", "The client who raised it.",
         "Defines the client population. Alias-merged: ICICI splits across two "
         "values unmerged."],
        ["customfield_10245", "RCA", "option / select",
         "1,622 / 2,010 = 80.7%", "✅ NEW — the root-cause axis",
         "The product team's own root-cause classification: 33 values in 15 "
         "families.",
         "⛔ THE FIELD THE REPORT DECLARED ABSENT. §13 said Jira held no "
         "categorisation to cross-check the derived taxonomy against, having "
         "measured cf 10113 (0.2%) and cf 10199 (0.1%). Same error class as the "
         "affectedVersion miss. Sheet 11 uses it."],
        ["customfield_10567", "RCA Details (Impact Analysis)", "string / textarea",
         "1,591 / 2,010 = 79.2%", "✅ NEW",
         "Free-text impact analysis behind the RCA value.",
         "Per-ticket evidence on sheet 04. Not aggregated — it is free text."],
        ["customfield_10249", "Fixed Date", "datetime", "1,026 / 2,010 = 51.0%",
         "✅ NEW", "When the fix was recorded.",
         "The second half of a fix-latency measure. On sheet 04."],
        ["customfield_10741", "Reopen RCA", "option / select",
         "147 / 2,010 = 7.3%", "✅ NEW", "Why a delivered fix failed.",
         "Code Fix (48), Dependency failure (29), Audit (23), Hosting Issue (22), "
         "Tester Understanding (17), Data Issue (8). Sheet 11."],
        ["customfield_10600 / 10781 / 10236 / 10235",
         "Reopen RCA details / Original Ticket ID / ReOpen Date / ReOpen Time Spent",
         "textarea / textfield / datetime / float",
         "7.6% / 7.1% / 4.1% / 3.6%", "✅ NEW",
         "The reopen trail: why, from where, when, and the rework cost.",
         "⚠ Reopen Original Ticket ID is free text and 64 of 142 values are junk "
         "('No', 'NONE', 'na'); FIELD_SENTINELS strips those so no link is "
         "invented."],
        ["customfield_11353 / 11355",
         "RCA Category / Description updated? · RCA Review Remarks",
         "select / textarea", "1.2% / 1.2%", "⚠ too sparse for a rate",
         "RCA review hygiene.", "Carried per ticket; no aggregate is quoted."],
        ["customfield_10113 / 10199", "Root Cause · Root cause",
         "string / textarea", "5 and 3 tickets — 0.2% / 0.1%",
         "⛔ decoys — do not use",
         "Two near-empty same-named fields.",
         "⛔ These are the fields whose emptiness was read as 'Jira holds no "
         "root-cause categorisation'. The live field is cf 10245."],
        ["customfield_10164", "Phase", "option / select", "0 / 2,010",
         "⛔ Info not available in JIRA",
         "Defect-injection phase (requirement / design / code / test).",
         "⛔ EXISTS BUT NEVER POPULATED, so injection phase is NOT ANSWERABLE. "
         "Deriving it from the RCA family would be inference presented as "
         "measurement: 'Code - *' says where the defect was found in code, not "
         "where it was introduced."],
        ["customfield_11018", "ReopenCount", "number / float", "0 / 2,010",
         "⛔ Info not available in JIRA", "How many times a ticket was reopened.",
         "⛔ EXISTS BUT NEVER POPULATED. A reopen is visible as a boolean, never "
         "as a count — 'reopened three times' is not answerable."],
        ["customfield_10065 / 10051", "Module / Category",
         "option / select", "0%", "⛔ Info not available in JIRA",
         "The product's own module and category fields.",
         "Unpopulated, so the module axis uses `components` and the category axis "
         "is derived from text. Kept in the field list to detect them filling."],
        ["customfield_10147 / 10136 / 10150",
         "Hotfix Release Date · Affected QA Build · QA Build/Drop",
         "date / select / select", "1 / 9 / 9 tickets",
         "⚠ near-empty", "QA build provenance.",
         "Too sparse to use. Affected QA Build reads 'Build 35.8.29' on all nine."],
        ["—", "Regression test executed / suite name", "—", "no such field",
         "⛔ Info not available in JIRA",
         "Which test should have caught this defect.",
         "No field exists, so 'was this covered?' is answered by the derived "
         "testing-area axis rather than by Jira."],
        ["—", "Requirement / user-story link", "—", "no populated field",
         "⛔ Info not available in JIRA", "The requirement a defect traces to.",
         "Why the scenario-gap provenance table marks requirements NOT USED."],
        ["—", "Detected-by / found-in-testing stage", "—", "no such field",
         "⛔ Info not available in JIRA", "Who found the defect.",
         "Every ticket here is client-raised by definition, so an "
         "internal-vs-external detection ratio is not measurable."],
    ]
    _write(ws, hrow,
           ["Field ID", "Name as shown in Jira", "Type",
            "Population on the PAMIT client set", "Verdict",
            "What it represents", "How it is used / why rejected"],
           rows, widths=[34, 40, 22, 38, 26, 50, 66], wrap_from=6)


# ------------------------------------------------------------------------ assembly

SNAPSHOT_DIR = ROOT / "artifacts" / "client-tickets" / "snapshots"


def load_snapshot_history() -> list[dict]:
    """Every retained dated snapshot, oldest first, reduced to its headline counts.

    ⚠️ Tolerant by design. These files span three capture formats and two
    build-line bases, and a snapshot that cannot be parsed must not stop the
    workbook from building — the history sheet is a convenience, the current
    analysis is the deliverable. An unreadable file is skipped and its date is
    still emitted so the gap is visible.
    """
    import json as _json
    out = []
    for f in sorted(SNAPSHOT_DIR.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].json")):
        rec = {"date": f.stem}
        try:
            d = _json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            rec["generated"] = "unreadable snapshot — skipped"
            out.append(rec)
            continue
        fc = d.get("focus_counts") or {}
        cc = d.get("current_counts") or {}
        builds = d.get("builds") or {}
        rec.update({
            "generated": d.get("generated", ""),
            # ⚠️ A snapshot records per-build counts, not the de-duplicated total,
            # so this sum is the per-build sum. Labelled as such on the sheet.
            "build_line": sum(builds.values()) if builds else None,
            "focus_client": fc.get("client"),
            "focus_defects": fc.get("defects"),
            "window_tickets": cc.get("tickets"),
            "query_c": d.get("query_c"),
        })
        out.append(rec)
    return out


def build(A: dict, base_url: str, out: Path = WORKBOOK) -> Path:
    uni = ticket_universe(A)
    wb = Workbook()
    if wb.active is not None:
        wb.remove(wb.active)
    sheet_readme(wb, A, uni)
    weak_rows = sheet_weak_spots(wb, A, uni, base_url)
    sheet_weak_summary(wb, A)
    sheet_scenario_gaps(wb, A, uni)
    td_hrow = sheet_ticket_details(wb, A, uni, base_url)
    sheet_builds(wb, A)
    sheet_escape(wb, A, base_url)
    sheet_regression(wb, A, base_url)
    sheet_module_category(wb, A)
    sheet_reconciliation(wb, A, uni, td_hrow, weak_rows)
    sheet_field_audit(wb)
    sheet_rca(wb, A, base_url)
    sheet_daily_history(wb, load_snapshot_history())
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


def verify(A: dict, uni: dict) -> list[str]:
    """Reconcile in Python too, so a mismatch fails the build rather than shipping.

    The workbook's COUNTIFS formulas are for the reader; this is for the run. A
    figure that cannot be reproduced from the ticket universe is a defect in the
    analysis, and shipping the workbook anyway would hide it.
    """
    bad = []
    pool_of = lambda p: sum(1 for r in uni.values() if p in r["_pools"])  # noqa: E731
    checks = [
        ("build line", A["trend_total"], pool_of("build_line")),
        ("focus client", A["focus"]["counts"]["client"], pool_of("focus")),
        ("last 30 days", A["current"]["counts"]["tickets"], pool_of("last30")),
        ("Query C", A["query_c"]["count"], pool_of("query_c")),
    ]
    for label, reported, measured in checks:
        if reported != measured:
            bad.append(f"{label}: report says {reported}, ticket universe holds "
                       f"{measured}")
    for a in A["areas"]:
        if a["count"] != len(a["members"]):
            bad.append(f"area {a['area']}: count {a['count']} vs "
                       f"{len(a['members'])} member keys")
        missing = [k for k in a["members"] if k not in uni]
        if missing:
            bad.append(f"area {a['area']}: {len(missing)} member keys absent from "
                       f"the ticket universe ({', '.join(missing[:4])})")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refetch", action="store_true",
                    help="re-query Jira instead of reusing the newest capture")
    ap.add_argument("--out", type=Path, default=WORKBOOK)
    a = ap.parse_args()

    import pamit_client_analysis as P
    if a.refetch:
        from jira_query import ReadOnlyJira
        j = ReadOnlyJira()
        print(f"connected as {j.whoami()} | project {j.project}", file=sys.stderr)
        bundle = P.capture(j, R.CURRENT_WINDOW_DAYS)
        base = j.base
    else:
        bundle = P.load_capture()
        base = "https://arcon-tech-solution.atlassian.net"
    A = P.run_analysis(bundle, dt.date.today())
    uni = ticket_universe(A)
    problems = verify(A, uni)
    out = build(A, base.rstrip("/"), a.out)
    print(f"workbook: {out}")
    print(f"  tickets {len(uni)} | build line {A['trend_total']} | "
          f"areas {len(A['areas'])} | escaped {A['escape_am_escaped']} | "
          f"regression stated {A['regression']['stated']}")
    if problems:
        print("\n⛔ RECONCILIATION FAILED:", file=sys.stderr)
        for p in problems:
            print(f"   {p}", file=sys.stderr)
        return 1
    print("  reconciliation: every pool and every area count matches its tickets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
