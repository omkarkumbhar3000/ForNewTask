#!/usr/bin/env python3
"""CI (Converged Identity) project analysis — 01 Jan 2026 to present.

Fetches all CI tickets created in the date range and produces a
comprehensive markdown report.

    python tools\\jira\\ci_analysis_2026.py
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from paths import workspace_root
from jira_query import ReadOnlyJira
from pamit_fmt import pct, table, tally, snapshot_provenance
import analysis_classify as C

ROOT = workspace_root()
OUT_DIR = ROOT / "docs" / "analysis"
SNAP_DIR = ROOT / "artifacts" / "snapshots"

JIRA_BROWSE_BASE = "https://arcon-tech-solution.atlassian.net"

PROJECT_KEY = "CI"
DATE_FROM = "2026-01-01"
DATE_TO = "2026-09-21"

#: Filename slug derived from the date constants — `01Jan26-21Sep26`.
#: ⛔ Never hardcode this. The 03 Sep report was renamed by hand after generation, so the
#: script's computed name and the file on disk disagreed: re-running wrote a NEW file and
#: left the intended deliverable stale. Deriving it means the name can never drift again.
RANGE_SLUG = (dt.datetime.strptime(DATE_FROM, "%Y-%m-%d").strftime("%d%b%y") + "-"
              + dt.datetime.strptime(DATE_TO, "%Y-%m-%d").strftime("%d%b%y"))

#: ⛔ JQL `created <= 'YYYY-MM-DD'` means `<= YYYY-MM-DD 00:00` — it EXCLUDES the end
#: date entirely. Measured: `created <= '2026-09-21'` returned 0 tickets for 21 Sep while
#: `>= '2026-09-21' AND < '2026-09-22'` returned 44 (PAMIT) / 38 (CI). The 03 Sep edition
#: of this report carried the same off-by-one and silently omitted its own final day
#: (24 PAMIT / 31 CI tickets). Query the half-open interval instead.
DATE_TO_EXCLUSIVE = (dt.datetime.strptime(DATE_TO, "%Y-%m-%d")
                     + dt.timedelta(days=1)).strftime("%Y-%m-%d")


FIELDS = [
    "key", "summary", "issuetype", "status", "priority", "created", "updated",
    "components", "fixVersions", "labels", "reporter", "assignee", "resolution",
    "description", "parent", "issuelinks",
    "customfield_10112",   # Primary Client (may not exist in CI)
    "customfield_10190",   # Severity (may not exist in CI)
    "customfield_10245",   # RCA (may not exist in CI)
    "customfield_11220",   # Hosting Environment (may not exist in CI)
]


def fetch_tickets(j: ReadOnlyJira) -> list[dict]:
    jql = (f"project = {PROJECT_KEY} AND created >= '{DATE_FROM}' "
           f"AND created < '{DATE_TO_EXCLUSIVE}' ORDER BY created ASC, key ASC")
    print(f"  JQL: {jql}", file=sys.stderr)
    return j.search(jql, FIELDS, max_pages=200,
                    progress=lambda p, b, t: print(f"  page {p}: +{b} -> {t}", file=sys.stderr))


def normalise(issue: dict) -> dict:
    f = issue.get("fields", {})
    # Safely extract nested objects
    issuetype = f.get("issuetype")
    # ⛔ Capture the authoritative sub-task flag BEFORE `issuetype` collapses to its name.
    # `parent` spans the WHOLE hierarchy in modern Jira — Epic children (Bug, Story, Task)
    # carry it too — so counting parent-presence published 4,241 sub-tasks where only
    # 1,443 exist, contradicting this report's own §3 by 2,798. `issuetype.subtask` is the
    # flag Jira sets itself; it agrees exactly with `issuetype.name == "Sub-task"` here.
    is_subtask = bool(issuetype.get("subtask")) if isinstance(issuetype, dict) else False
    if isinstance(issuetype, dict):
        issuetype = issuetype.get("name", "Unknown")
    else:
        issuetype = str(issuetype) if issuetype else "Unknown"

    status = f.get("status")
    if isinstance(status, dict):
        status = status.get("name", "Unknown")
    else:
        status = str(status) if status else "Unknown"

    priority = f.get("priority")
    if isinstance(priority, dict):
        priority = priority.get("name", "Unknown")
    else:
        priority = str(priority) if priority else "Unknown"

    resolution = f.get("resolution")
    if isinstance(resolution, dict):
        resolution = resolution.get("name", "Unresolved")
    else:
        resolution = str(resolution) if resolution else "Unresolved"

    reporter = f.get("reporter")
    if isinstance(reporter, dict):
        reporter = reporter.get("displayName") or reporter.get("name") or "Unknown"
    else:
        reporter = str(reporter) if reporter else "Unknown"

    assignee = f.get("assignee")
    if isinstance(assignee, dict):
        assignee = assignee.get("displayName") or assignee.get("name") or "Unassigned"
    else:
        assignee = str(assignee) if assignee else "Unassigned"

    components = []
    raw_comps = f.get("components") or []
    if isinstance(raw_comps, list):
        for c in raw_comps:
            if isinstance(c, dict):
                components.append(c.get("name", ""))
            else:
                components.append(str(c))

    fix_versions = []
    raw_fv = f.get("fixVersions") or []
    if isinstance(raw_fv, list):
        for fv in raw_fv:
            if isinstance(fv, dict):
                fix_versions.append(fv.get("name", ""))
            else:
                fix_versions.append(str(fv))

    labels = f.get("labels") or []

    parent = f.get("parent")
    parent_key = ""
    if isinstance(parent, dict):
        parent_key = parent.get("key", "")

    # Custom fields - safe extraction
    def safe_custom(field_id):
        v = f.get(field_id)
        if v is None:
            return "Not set"
        if isinstance(v, dict):
            return v.get("value") or v.get("name") or v.get("displayName") or "Not set"
        if isinstance(v, list):
            vals = []
            for x in v:
                if isinstance(x, dict):
                    vals.append(x.get("value") or x.get("name") or "")
                else:
                    vals.append(str(x))
            return ", ".join(vals) if vals else "Not set"
        return str(v)

    return {
        "key": issue.get("key", ""),
        "summary": f.get("summary", ""),
        "issuetype": issuetype,
        "status": status,
        "priority": priority,
        "resolution": resolution,
        "created": (f.get("created") or "")[:10],
        "updated": (f.get("updated") or "")[:10],
        "components": components,
        "fixVersions": fix_versions,
        "labels": labels,
        "reporter": reporter,
        "assignee": assignee,
        "parent_key": parent_key,
        "is_subtask": is_subtask,
        "primary_client": safe_custom("customfield_10112"),
        "severity": safe_custom("customfield_10190"),
        "rca": safe_custom("customfield_10245"),
        "hosting_env": safe_custom("customfield_11220"),
    }


def monthly_key(date_str: str) -> str:
    return date_str[:7]


def build_report(tickets: list[dict], snapshot: Path | None = None) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(tickets)

    # --- Classification ------------------------------------------------------
    # Shared with the PAMIT census through `analysis_classify`. CI had no
    # Client/Internal split before this edition: its internal marker is
    # `Internal Arcon`, which matches none of PAMIT's variants, so reusing PAMIT's
    # set here would have called 3,713 internal tickets "Client". The 825 tickets
    # with no Primary Client at all fall to Internal under PAMIT's long-standing
    # rule for an unset field, and are listed in their own section.
    for t in tickets:
        t["_state"] = C.classify_status(t["status"])
        t["_bucket"] = C.client_bucket(t["primary_client"])
        t["_unspec"] = C.unspecified_client(t["primary_client"])

    client_tickets = [t for t in tickets if t["_bucket"] == C.CLIENT]
    internal_tickets = [t for t in tickets if t["_bucket"] == C.INTERNAL]
    client_count = len(client_tickets)
    internal_count = len(internal_tickets)
    unspecified = [t for t in tickets if t["_unspec"]]

    open_count = sum(1 for t in tickets if t["_state"] == C.OPEN)
    closed_count = sum(1 for t in tickets if t["_state"] == C.CLOSED)
    unmapped_count = sum(1 for t in tickets if t["_state"] == C.UNMAPPED)

    def _status(t):
        return t["status"]

    def _client(t):
        return t["primary_client"]

    # --- Section numbering ---------------------------------------------------
    _sec = {"n": 0}

    def H(title: str) -> str:
        _sec["n"] += 1
        return f"## {_sec['n']}. {title}"

    def cur() -> int:
        return _sec["n"]

    # --- Table helpers -------------------------------------------------------
    def count_table(label, counter, *, limit=None, show_pct=True, unit="tickets"):
        items = counter.most_common(limit) if limit else counter.most_common()
        shown = sum(c for _, c in items)
        grand = sum(counter.values())
        truncated = len(items) < len(counter)
        headers = [label, "Count"] + (["% of Total"] if show_pct else [])
        align = ["---", "---:"] + (["---:"] if show_pct else [])
        rows = [[s, str(c)] + ([pct(c, total)] if show_pct else []) for s, c in items]
        tot = f"**Total (top {len(items)} shown)**" if truncated else "**Total**"
        rows.append([tot, f"**{shown}**"]
                    + ([f"**{pct(shown, total)}**"] if show_pct else []))
        out = table(headers, rows, align)
        if truncated:
            out += (f"\n\n_{len(counter) - len(items)} further values not shown, "
                    f"accounting for {grand - shown} of {grand} {unit}._")
        return out

    def bif(category_fn, *, multi=False):
        return C.bifurcate(C.prepare(tickets, _status, _client, category_fn), multi=multi)

    def listing_total(shown: int, available: int, noun: str) -> str:
        if shown < available:
            return (f"\n**Total listed:** {shown} of {available} {noun} "
                    f"({available - shown} not shown).")
        return f"\n**Total listed:** {shown} {noun}."

    # --- Tallies -------------------------------------------------------------
    by_status = tally(tickets, lambda t: t["status"])
    by_type = tally(tickets, lambda t: t["issuetype"])
    by_reporter = tally(tickets, lambda t: t["reporter"])
    by_assignee = tally(tickets, lambda t: t["assignee"])
    by_rca = tally(tickets, lambda t: t["rca"])
    by_hosting = tally(tickets, lambda t: t["hosting_env"])

    comp_counter: collections.Counter = collections.Counter()
    for t in tickets:
        for c in t["components"]:
            if c:
                comp_counter[c] += 1

    label_counter: collections.Counter = collections.Counter()
    for t in tickets:
        for lb in t["labels"]:
            if lb:
                label_counter[lb] += 1

    monthly: collections.Counter = collections.Counter()
    for t in tickets:
        monthly[monthly_key(t["created"])] += 1

    # ⚠️ A ticket with an absent or unparsable `created` date used to vanish from the
    # weekly table without trace, leaving its Total quietly below the population while
    # still equalling the sum of its own rows — so nothing, here or in a reconciliation
    # check, could see it. Count the drops instead and state them under the table.
    weekly: collections.Counter = collections.Counter()
    undated = 0
    for t in tickets:
        try:
            weekly["{}-W{:02d}".format(
                *dt.date.fromisoformat(t["created"]).isocalendar()[:2])] += 1
        except (ValueError, TypeError):
            undated += 1

    fv_counter: collections.Counter = collections.Counter()
    for t in tickets:
        for fv in t["fixVersions"]:
            if fv:
                fv_counter[fv] += 1

    subtask_count = sum(1 for t in tickets if t["is_subtask"])
    parent_keys = set(t["parent_key"] for t in tickets
                      if t["is_subtask"] and t["parent_key"])

    # --- Header --------------------------------------------------------------
    lines = []
    lines.append(f"# CI (Converged Identity) Ticket Analysis — {DATE_FROM} to {DATE_TO}")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    if snapshot is not None:
        lines.append(snapshot_provenance(snapshot))
    lines.append(f"**Project:** CI ({PROJECT_KEY}) · **Date range:** {DATE_FROM} to {DATE_TO}")
    lines.append(f"**Total tickets:** {total} · **Client tickets:** {client_count} "
                 f"· **Internal:** {internal_count}")
    lines.append("")
    lines.append("> **Open / Closed classification.** Every status is mapped by the owner's "
                 "status lists, case-insensitively. A status in neither list is reported as "
                 "**Unmapped** and is never guessed into a bucket, so each bifurcated table "
                 "carries its own Unmapped column and **Total Count = Open Total + Closed "
                 f"Total + Unmapped**. {unmapped_count} of {total} tickets "
                 f"({pct(unmapped_count, total)}) are unmapped.")
    lines.append("")
    lines.append(f"> **Client / Internal.** CI's internal marker is `Internal Arcon`. "
                 f"{len(unspecified)} tickets ({pct(len(unspecified), total)}) carry no "
                 f"Primary Client and are counted as **Internal**, per the owner's decision; "
                 f"they are listed in their own section so the fallback is never silent.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- Summary -------------------------------------------------------------
    lines.append(H("Summary"))
    lines.append("")
    lines.append(table(
        ["Metric", "Count"],
        [["Total tickets", str(total)],
         ["Client tickets", f"{client_count} ({pct(client_count, total)})"],
         ["Internal tickets", f"{internal_count} ({pct(internal_count, total)})"],
         ["— of which no Primary Client", f"{len(unspecified)} ({pct(len(unspecified), total)})"],
         ["Sub-tasks", f"{subtask_count} ({pct(subtask_count, total)})"],
         ["Standalone (non-sub-task)",
          f"{total - subtask_count} ({pct(total - subtask_count, total)})"],
         ["Open", f"{open_count} ({pct(open_count, total)})"],
         ["Closed", f"{closed_count} ({pct(closed_count, total)})"],
         ["Unmapped status", f"{unmapped_count} ({pct(unmapped_count, total)})"]],
        ["---", "---:"],
    ))
    lines.append("")
    lines.append("_No Total row: these rows count overlapping populations of the same "
                 "ticket set, so summing them would double-count._")
    lines.append("")

    # --- Status distribution -------------------------------------------------
    lines.append(H("Status Distribution"))
    lines.append("")
    status_rows = [[s, C.classify_status(s), str(c), pct(c, total)]
                   for s, c in by_status.most_common()]
    status_rows.append(["**Total**", "", f"**{total}**", f"**{pct(total, total)}**"])
    lines.append(table(["Status", "Class", "Count", "% of Total"], status_rows,
                       ["---", "---", "---:", "---:"]))
    lines.append("")

    # --- Issue type ----------------------------------------------------------
    lines.append(H("Issue Type Distribution"))
    lines.append("")
    lines.append(count_table("Issue Type", by_type))
    lines.append("")

    # --- Priority (bifurcated) ----------------------------------------------
    lines.append(H("Priority Distribution"))
    lines.append("")
    rows, grand, _ = bif(lambda t: t["priority"])
    lines.append(C.grouped_table("Priority", rows, grand))
    lines.append("")

    # --- Severity (bifurcated) ----------------------------------------------
    lines.append(H("Severity Distribution"))
    lines.append("")
    rows, grand, _ = bif(lambda t: t["severity"])
    lines.append(C.grouped_table("Severity", rows, grand))
    lines.append("")
    sev_set = sum(1 for t in tickets if t["severity"] not in ("Not set", "", None))
    lines.append(f"⚠️ **Severity is populated on {sev_set} of {total} tickets "
                 f"({pct(sev_set, total)}).** Every figure above other than the `Not set` "
                 f"row is quoted over that subset; an unfilled Severity is not evidence of "
                 f"low severity.")
    lines.append("")

    # --- Components (two analyses) ------------------------------------------
    lines.append(H("Components"))
    lines.append("")
    crows, cgrand, cdistinct = bif(
        lambda t: ([c for c in t["components"] if c] or ["(No component)"]), multi=True)
    assignments = sum(b.total for _, b in crows)
    multi_tickets = sum(1 for t in tickets if len([c for c in t["components"] if c]) > 1)

    lines.append(f"⚠️ **Components are multi-valued.** {multi_tickets} tickets carry two or "
                 f"more components and are counted once per component, so the rows sum to "
                 f"{assignments} component assignments across {cdistinct} distinct tickets. "
                 f"The **Total** row states distinct tickets, which reconciles to the "
                 f"project count; it is deliberately not the column sum.")
    lines.append("")
    lines.append(f"### {cur()}A. Component — Total, Open and Closed")
    lines.append("")
    lines.append(C.simple_open_closed_table(
        "Component", crows, cgrand, total_label="**Total (distinct tickets)**"))
    lines.append("")
    lines.append(f"### {cur()}B. Component — Client and Internal split")
    lines.append("")
    lines.append(C.grouped_table("Component", crows, cgrand,
                                 total_label="**Total (distinct tickets)**"))
    lines.append("")

    # --- Reporters / assignees ----------------------------------------------
    lines.append(H("Top Reporters (Top 20)"))
    lines.append("")
    lines.append(count_table("Reporter", by_reporter, limit=20))
    lines.append("")

    lines.append(H("Top Assignees (Top 20)"))
    lines.append("")
    lines.append(count_table("Assignee", by_assignee, limit=20))
    lines.append("")

    # --- Trends --------------------------------------------------------------
    lines.append(H("Monthly Creation Trend"))
    lines.append("")
    m_rows = [[m, str(monthly[m])] for m in sorted(monthly)]
    m_rows.append(["**Total**", f"**{sum(monthly.values())}**"])
    lines.append(table(["Month", "Count"], m_rows, ["---", "---:"]))
    lines.append("")

    lines.append(H("Weekly Creation Trend"))
    lines.append("")
    w_rows = [[w, str(weekly[w])] for w in sorted(weekly)]
    w_rows.append(["**Total**", f"**{sum(weekly.values())}**"])
    lines.append(table(["Week", "Count"], w_rows, ["---", "---:"]))
    if undated:
        lines.append("")
        lines.append(f"⚠️ **{undated} of {total} tickets carry no parsable `created` "
                     f"date** and are therefore absent from this table, whose Total is "
                     f"{sum(weekly.values())} rather than {total}. They are not lost "
                     f"from any other section — every other count keys on the ticket, "
                     f"not on its date.")
    lines.append("")

    # --- Fix version ---------------------------------------------------------
    lines.append(H("Fix Version Distribution"))
    lines.append("")
    if fv_counter:
        lines.append(count_table("Fix Version", fv_counter, limit=30, show_pct=False,
                                 unit="fix-version assignments"))
    else:
        lines.append("_No fix versions set._")
    lines.append("")

    # --- RCA -----------------------------------------------------------------
    lines.append(H("Root Cause Analysis (RCA)"))
    lines.append("")
    if len(by_rca) <= 1 and "Not set" in by_rca:
        lines.append("_RCA field not populated in this project._")
    else:
        lines.append(count_table("RCA", by_rca))
    lines.append("")

    # --- Hosting -------------------------------------------------------------
    lines.append(H("Hosting Environment"))
    lines.append("")
    if len(by_hosting) <= 1 and "Not set" in by_hosting:
        lines.append("_Hosting Environment field not populated in this project._")
    else:
        lines.append(count_table("Hosting Environment", by_hosting))
    lines.append("")

    # --- Labels --------------------------------------------------------------
    lines.append(H("Labels"))
    lines.append("")
    if label_counter:
        lines.append(count_table("Label", label_counter, limit=20, show_pct=False,
                                 unit="label assignments"))
    else:
        lines.append("_No labels found._")
    lines.append("")

    # --- Sub-task analysis ---------------------------------------------------
    lines.append(H("Sub-task Analysis"))
    lines.append("")
    # A partition, so the Total row is a real sum. `Unique parent tickets` counts
    # PARENTS, not tickets in this window — inside this column it would push the rows
    # past the report total, so it is stated beneath instead.
    lines.append(table(
        ["Ticket Kind", "Count"],
        [["Sub-tasks", str(subtask_count)],
         ["Standalone (non-sub-task)", str(total - subtask_count)],
         ["**Total**", f"**{total}**"]],
        ["---", "---:"],
    ))
    lines.append("")
    lines.append(f"The {subtask_count} sub-tasks hang off **{len(parent_keys)} unique "
                 f"parent tickets**. That is a count of parents, not of tickets in this "
                 f"window, so it is kept out of the table above rather than added into a "
                 f"column it does not belong to.")
    lines.append("")
    if parent_keys:
        parent_counts = collections.Counter(
            t["parent_key"] for t in tickets if t["is_subtask"] and t["parent_key"])
        lines.append(f"### {cur()}A. Top parent tickets by sub-task count")
        lines.append("")
        shown = parent_counts.most_common(15)
        p_rows = [[k, str(c)] for k, c in shown]
        p_rows.append([f"**Total (top {len(shown)} shown)**",
                       f"**{sum(c for _, c in shown)}**"])
        lines.append(table(["Parent Key", "Sub-tasks"], p_rows, ["---", "---:"]))
        if len(parent_counts) > len(shown):
            lines.append("")
            lines.append(f"_{len(parent_counts) - len(shown)} further parent tickets not "
                         f"shown, accounting for "
                         f"{subtask_count - sum(c for _, c in shown)} sub-tasks._")
        lines.append("")

    # --- Unassigned ----------------------------------------------------------
    lines.append(H("Unassigned Tickets"))
    lines.append("")
    unassigned = [t for t in tickets if t["assignee"] == "Unassigned"]
    unassigned_client = [t for t in unassigned if t["_bucket"] == C.CLIENT]
    lines.append(table(
        ["Metric", "Count"],
        [["Total unassigned", str(len(unassigned))],
         ["Client unassigned", str(len(unassigned_client))],
         ["Internal unassigned", str(len(unassigned) - len(unassigned_client))]],
        ["---", "---:"],
    ))
    lines.append("")
    if unassigned:
        lines.append("### Unassigned ticket details")
        lines.append("")
        shown = unassigned[:30]
        lines.append(table(
            ["Key", "Summary", "Type", "Priority", "Status"],
            [[f"[{t['key']}]({JIRA_BROWSE_BASE}/browse/{t['key']})",
              t["summary"][:80], t["issuetype"], t["priority"], t["status"]]
             for t in shown],
        ))
        lines.append(listing_total(len(shown), len(unassigned), "unassigned tickets"))
        lines.append("")

    # --- Open high-priority --------------------------------------------------
    lines.append(H("Open High-Priority Tickets (High / ShowStopper / Critical)"))
    lines.append("")
    high_open = [t for t in tickets
                 if t["_state"] == C.OPEN
                 and t["priority"] in ("High", "ShowStopper", "Critical")]
    if high_open:
        shown = high_open[:30]
        lines.append(table(
            ["Key", "Summary", "Status", "Priority", "Assignee"],
            [[f"[{t['key']}]({JIRA_BROWSE_BASE}/browse/{t['key']})",
              t["summary"][:80], t["status"], t["priority"], t["assignee"]]
             for t in shown],
        ))
        lines.append(listing_total(len(shown), len(high_open),
                                   "open high-priority tickets"))
    else:
        lines.append("_No open high-priority tickets._")
    lines.append("")

    # --- Unmapped status review ---------------------------------------------
    lines.append(H("Unmapped Status Review"))
    lines.append("")
    breakdown = C.unmapped_breakdown(tickets, _status, _client)
    if breakdown:
        lines.append(f"These {unmapped_count} tickets ({pct(unmapped_count, total)}) carry a "
                     f"status present in neither the Open nor the Closed list. They are "
                     f"counted in every **Total Count** and in the **Unmapped** column, and "
                     f"in neither Open nor Closed. Listed here for a mapping decision.")
        lines.append("")
        lines.append(C.unmapped_table(breakdown))
    else:
        lines.append("_Every status mapped to Open or Closed._")
    lines.append("")
    lines.append("**Mapping applied** — case-insensitive, with these wording aliases:")
    lines.append("")
    lines.append(table(["Jira status (normalised)", "Owner list entry"],
                       [[j, o] for j, o in sorted(C.STATUS_ALIASES.items())]))
    lines.append("")

    # --- Unspecified primary client -----------------------------------------
    lines.append(H("Unspecified Primary Client"))
    lines.append("")
    if unspecified:
        u_open = sum(1 for t in unspecified if t["_state"] == C.OPEN)
        u_closed = sum(1 for t in unspecified if t["_state"] == C.CLOSED)
        u_unmapped = sum(1 for t in unspecified if t["_state"] == C.UNMAPPED)
        lines.append(f"{len(unspecified)} tickets ({pct(len(unspecified), total)}) carry no "
                     f"Primary Client. They are counted as **Internal** throughout this "
                     f"report, which is the owner's decision and matches PAMIT's rule for an "
                     f"unset field — it is a fallback, not a measurement. Without it they "
                     f"would be unattributable and the Client + Internal identity would fail.")
        lines.append("")
        lines.append(table(
            ["Metric", "Count"],
            [["Open", str(u_open)],
             ["Closed", str(u_closed)],
             ["Unmapped status", str(u_unmapped)],
             ["**Total**", f"**{len(unspecified)}**"]],
            ["---", "---:"],
        ))
        lines.append("")
        u_types = collections.Counter(t["issuetype"] for t in unspecified)
        u_rows = [[k, str(v)] for k, v in u_types.most_common()]
        u_rows.append(["**Total**", f"**{len(unspecified)}**"])
        lines.append(table(["Issue Type", "Count"], u_rows, ["---", "---:"]))
    else:
        lines.append("_Every ticket carries a Primary Client._")
    lines.append("")

    # --- Footer --------------------------------------------------------------
    lines.append("---")
    lines.append("")
    lines.append(f"*Report generated by `tools/jira/ci_analysis_2026.py` on {now}*")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=f"CI project analysis {DATE_FROM} to {DATE_TO}")
    parser.add_argument("--offline", action="store_true",
                        help="Reuse newest snapshot, zero HTTP")
    args = parser.parse_args()

    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    snap_file = SNAP_DIR / f"ci-analysis-{DATE_FROM}-to-{DATE_TO}.json"

    if args.offline and not snap_file.exists():
        # ⛔ Never fall through to a live fetch here. `--offline` is a promise of zero
        # HTTP, and the operator is told to prefer it; silently honouring the opposite
        # would hit production Jira and overwrite the snapshot the run meant to reuse.
        # `pamit_client_analysis.py` already refuses this way — match it.
        print("--offline requested, but there is no snapshot at:", file=sys.stderr)
        print(f"  {snap_file}", file=sys.stderr)
        print("Run once without --offline to capture it.", file=sys.stderr)
        return 2

    if args.offline:
        print(f"Loading snapshot: {snap_file}", file=sys.stderr)
        raw = json.loads(snap_file.read_text(encoding="utf-8"))
    else:
        j = ReadOnlyJira()
        print(f"Connected as: {j.whoami()} | Project: {PROJECT_KEY}", file=sys.stderr)
        print(f"Fetching tickets created {DATE_FROM} to {DATE_TO}...", file=sys.stderr)
        raw = fetch_tickets(j)
        print(f"Fetched {len(raw)} tickets total.", file=sys.stderr)
        snap_file.parent.mkdir(parents=True, exist_ok=True)
        snap_file.write_text(json.dumps(raw, indent=2, ensure_ascii=False),
                             encoding="utf-8")
        print(f"Snapshot saved: {snap_file}", file=sys.stderr)

    tickets = [normalise(issue) for issue in raw]
    print(f"Normalised {len(tickets)} tickets.", file=sys.stderr)

    report = build_report(tickets, snapshot=snap_file)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_DIR / f"CI_Jira_Analysis_{RANGE_SLUG}.md"
    out_file.write_text(report, encoding="utf-8")
    print(f"\nReport written: {out_file}", file=sys.stderr)


if __name__ == "__main__":
    # `main()` returns a non-zero code on refusal; a bare call would discard it
    # and report success to whatever ran this.
    sys.exit(main() or 0)
