#!/usr/bin/env python3
"""PAMIT ticket analysis — 01 Jan 2026 to present.

Fetches all PAMIT tickets created in the date range and produces a
comprehensive markdown report covering status, priority, type,
components, assignees, reporters, creation trends, and more.

    python tools\\jira\\jira_analysis_2026.py              # fetch, analyse, write report
    python tools\\jira\\jira_analysis_2026.py --offline    # reuse newest snapshot, zero HTTP
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
from jira_query import ReadOnlyJira, field_value
from pamit_fmt import pct, table, tally, snapshot_provenance
import analysis_classify as C

ROOT = workspace_root()
OUT_DIR = ROOT / "docs" / "analysis"
SNAP_DIR = ROOT / "artifacts" / "client-tickets" / "snapshots"

JIRA_BROWSE_BASE = "https://arcon-tech-solution.atlassian.net"

FIELDS = [
    "key", "summary", "issuetype", "status", "priority", "created", "updated",
    "components", "fixVersions", "labels", "reporter", "assignee", "resolution",
    "customfield_10092",   # Affected Milestone.
    "customfield_10112",   # Primary Client
    "customfield_10190",   # Severity
    "customfield_10245",   # RCA
    "customfield_10156",   # Database Type
    "customfield_11220",   # Hosting Environment
    "customfield_10065",   # Module
    "customfield_10051",   # Category
]

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



def fetch_tickets(j: ReadOnlyJira) -> list[dict]:
    jql = (f"project = {j.project} AND created >= '{DATE_FROM}' "
           f"AND created < '{DATE_TO_EXCLUSIVE}' ORDER BY created ASC, key ASC")
    print(f"  JQL: {jql}", file=sys.stderr)
    return j.search(jql, FIELDS, max_pages=200,
                    progress=lambda p, b, t: print(f"  page {p}: +{b} -> {t}", file=sys.stderr))


def normalise(issue: dict) -> dict:
    f = issue.get("fields", {})
    return {
        "key": issue.get("key", ""),
        "summary": f.get("summary", ""),
        "issuetype": field_value(f, "issuetype") or "Unknown",
        "status": field_value(f, "status") or "Unknown",
        "priority": field_value(f, "priority") or "Unknown",
        "resolution": field_value(f, "resolution") or "Unresolved",
        "created": (f.get("created") or "")[:10],
        "updated": (f.get("updated") or "")[:10],
        "components": field_value(f, "components") or [],
        "fixVersions": field_value(f, "fixVersions") or [],
        "labels": f.get("labels") or [],
        "reporter": field_value(f, "reporter") or "Unknown",
        "assignee": field_value(f, "assignee") or "Unassigned",
        # ⛔ `D42` build axis. Listed in FIELDS and read by §12 since the first
        # edition, but never emitted here — so §12 saw None for every ticket and
        # published 100% `Not set` across all 5,740. Multiselect: `field_value`
        # returns a list (or None), which §12 already loops over and counts as
        # milestone assignments. Emit the raw shape; §12 owns the "Not set" default.
        "affected_milestone": field_value(f, "customfield_10092"),
        "primary_client": field_value(f, "customfield_10112") or "Unknown",
        "severity": field_value(f, "customfield_10190") or "Not set",
        "rca": field_value(f, "customfield_10245") or "Not set",
        "hosting_env": field_value(f, "customfield_11220") or "Not set",
        "module": field_value(f, "customfield_10065") or "Not set",
        "category": field_value(f, "customfield_10051") or "Not set",
    }


def is_client_ticket(t: dict) -> bool:
    """Kept for callers outside this module; the rule lives in analysis_classify."""
    return C.is_client_ticket(t["primary_client"])


def monthly_key(date_str: str) -> str:
    return date_str[:7]  # YYYY-MM


def build_report(tickets: list[dict], snapshot: Path | None = None) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(tickets)

    # --- Classification ------------------------------------------------------
    # Open/Closed and Client/Internal both come from `analysis_classify`, which the
    # CI census imports too. Stamping each ticket once keeps every table below on
    # one definition — the previous build had a private `open_statuses` set holding
    # generic Jira defaults (`To Do`, `Done`, `Verified`) that do not occur in PAMIT,
    # which is why 23% of tickets used to land in "Other status".
    for t in tickets:
        t["_state"] = C.classify_status(t["status"])
        t["_bucket"] = C.client_bucket(t["primary_client"])

    client_tickets = [t for t in tickets if t["_bucket"] == C.CLIENT]
    internal_tickets = [t for t in tickets if t["_bucket"] == C.INTERNAL]
    client_count = len(client_tickets)
    internal_count = len(internal_tickets)

    open_count = sum(1 for t in tickets if t["_state"] == C.OPEN)
    closed_count = sum(1 for t in tickets if t["_state"] == C.CLOSED)
    unmapped_count = sum(1 for t in tickets if t["_state"] == C.UNMAPPED)
    duplicate_count = sum(1 for t in tickets if t["status"] == "Duplicate")

    def _status(t):
        return t["status"]

    def _client(t):
        return t["primary_client"]

    # --- Section numbering ---------------------------------------------------
    # Auto-numbered so deleting or inserting a section cannot leave a stale heading.
    # Removing the old "5. Resolution" is exactly the change that used to require
    # hand-editing eighteen f-strings.
    _sec = {"n": 0}

    def H(title: str) -> str:
        _sec["n"] += 1
        return f"## {_sec['n']}. {title}"

    def cur() -> int:
        """The number of the section currently being written — for 6A / 6B sub-headings."""
        return _sec["n"]

    # --- Table helpers -------------------------------------------------------
    def count_table(label, counter, *, limit=None, show_pct=True, denom=None,
                    unit="tickets"):
        """A `label | Count | % of Total` table that always ends in a Total row.

        When `limit` truncates the rows, the Total row says so and a line beneath
        states how much was left out — a capped table must never read as complete.
        """
        base = total if denom is None else denom
        items = counter.most_common(limit) if limit else counter.most_common()
        shown = sum(c for _, c in items)
        grand = sum(counter.values())
        truncated = len(items) < len(counter)

        headers = [label, "Count"] + (["% of Total"] if show_pct else [])
        align = ["---", "---:"] + (["---:"] if show_pct else [])
        rows = [[s, str(c)] + ([pct(c, base)] if show_pct else []) for s, c in items]
        tot = f"**Total (top {len(items)} shown)**" if truncated else "**Total**"
        rows.append([tot, f"**{shown}**"]
                    + ([f"**{pct(shown, base)}**"] if show_pct else []))
        out = table(headers, rows, align)
        if truncated:
            out += (f"\n\n_{len(counter) - len(items)} further values not shown, "
                    f"accounting for {grand - shown} of {grand} {unit}._")
        return out

    def bif(category_fn, *, multi=False):
        triples = C.prepare(tickets, _status, _client, category_fn)
        return C.bifurcate(triples, multi=multi)

    def listing_total(shown: int, available: int, noun: str) -> str:
        if shown < available:
            return (f"\n**Total listed:** {shown} of {available} {noun} "
                    f"({available - shown} not shown).")
        return f"\n**Total listed:** {shown} {noun}."

    def multi_counter(field: str) -> tuple[collections.Counter, int]:
        """Count *assignments* for a multi-value field, and how many tickets carry one.

        The unit is assignments, not tickets: a ticket carrying two milestones
        contributes two. ⛔ An unpopulated ticket contributes **nothing** — it is not an
        assignment. Folding one in as a `Not set` row is what made §12 publish
        "5,832 milestone assignments" when only 4,615 exist, and it put a `Not set` row
        at the top of a table whose every other row is a real build. Coverage is stated
        separately by `coverage_line` — `D46`: a figure over its populated subset, with
        the subset size beside it. Sharing one counter across components, fix versions
        and milestones is what stops the three drifting apart again.
        """
        counter: collections.Counter = collections.Counter()
        populated = 0
        for t in tickets:
            v = t.get(field)
            if not v:
                continue
            populated += 1
            for x in (v if isinstance(v, list) else [v]):
                counter[x] += 1
        return counter, populated

    def coverage_line(noun: str, populated: int, counter: collections.Counter) -> str:
        """The sentence that keeps an assignment count from reading as a ticket count.

        `noun` carries its own article — the two fields need different ones.
        """
        return (f"**Coverage:** {populated} of {total} tickets ({pct(populated, total)}) "
                f"carry {noun}; they account for {sum(counter.values())} assignments "
                f"across {len(counter)} distinct values. The table counts **assignments**, "
                f"so a ticket carrying more than one appears more than once, and the "
                f"{total - populated} tickets with none are not represented in it.")

    # --- Tallies -------------------------------------------------------------
    by_status = tally(tickets, lambda t: t["status"])
    by_type = tally(tickets, lambda t: t["issuetype"])
    by_reporter = tally(tickets, lambda t: t["reporter"])
    by_assignee = tally(tickets, lambda t: t["assignee"])
    by_rca = tally(tickets, lambda t: t["rca"])
    by_hosting = tally(tickets, lambda t: t["hosting_env"])
    by_module = tally(tickets, lambda t: t["module"])
    by_category = tally(tickets, lambda t: t["category"])

    # ⛔ No `comp_counter` here. A component tally was computed over every ticket and then
    # never read — §6 is built from `bif()` / `C.prepare`, not from a counter. Removed
    # 2026-09-22 after confirming, by AST, that the name was loaded nowhere.

    monthly: collections.Counter = collections.Counter()
    monthly_client: collections.Counter = collections.Counter()
    for t in tickets:
        mk = monthly_key(t["created"])
        monthly[mk] += 1
        if t["_bucket"] == C.CLIENT:
            monthly_client[mk] += 1

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

    fv_counter, fv_tickets = multi_counter("fixVersions")
    am_counter, am_tickets = multi_counter("affected_milestone")

    # --- Header --------------------------------------------------------------
    lines = []
    lines.append(f"# PAMIT Ticket Analysis — {DATE_FROM} to {DATE_TO}")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    if snapshot is not None:
        lines.append(snapshot_provenance(snapshot))
    lines.append(f"**Project:** PAMIT · **Date range:** {DATE_FROM} to {DATE_TO}")
    lines.append(f"**Total tickets:** {total} · **Client tickets:** {client_count} "
                 f"· **Internal:** {internal_count}")
    lines.append("")
    lines.append("> **Open / Closed classification.** Every status is mapped by the owner's "
                 "status lists, case-insensitively. A status in neither list is reported as "
                 "**Unmapped** and is never guessed into a bucket, so each bifurcated table "
                 f"carries its own Unmapped column and **Total Count = Open Total + Closed "
                 f"Total + Unmapped**. {unmapped_count} of {total} tickets "
                 f"({pct(unmapped_count, total)}) are unmapped — see the final section.")
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
         ["Open", f"{open_count} ({pct(open_count, total)})"],
         ["Closed", f"{closed_count} ({pct(closed_count, total)})"],
         ["Unmapped status", f"{unmapped_count} ({pct(unmapped_count, total)})"],
         ["Duplicates", f"{duplicate_count} ({pct(duplicate_count, total)})"]],
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
        lambda t: (t["components"] if isinstance(t["components"], list) and t["components"]
                   else ["(No component)"]),
        multi=True)
    assignments = sum(b.total for _, b in crows)
    multi_tickets = sum(1 for t in tickets
                        if isinstance(t["components"], list) and len(t["components"]) > 1)

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

    # --- Top reporters / assignees ------------------------------------------
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
    m_rows = [[m, str(monthly[m]), str(monthly_client.get(m, 0)),
               pct(monthly_client.get(m, 0), monthly[m])] for m in sorted(monthly)]
    m_tot = sum(monthly.values())
    m_cli = sum(monthly_client.values())
    m_rows.append(["**Total**", f"**{m_tot}**", f"**{m_cli}**", f"**{pct(m_cli, m_tot)}**"])
    lines.append(table(["Month", "Total", "Client", "% Client"], m_rows,
                       ["---", "---:", "---:", "---:"]))
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

    # --- Fix version / milestone --------------------------------------------
    lines.append(H("Fix Version Distribution"))
    lines.append("")
    lines.append(coverage_line("a fix version", fv_tickets, fv_counter))
    lines.append("")
    lines.append(count_table("Fix Version", fv_counter, limit=30, show_pct=False,
                             unit="fix-version assignments"))
    lines.append("")

    # ⛔ `D42`: this — where the client FOUND the defect — is the build axis, not
    # `Fix versions` above, which records where a fix SHIPS. Their coverage lines sit
    # side by side deliberately: the ruling rests on the gap between them.
    lines.append(H("Affected Milestone Distribution"))
    lines.append("")
    lines.append(coverage_line("an affected milestone", am_tickets, am_counter))
    lines.append("")
    lines.append(count_table("Affected Milestone", am_counter, limit=30, show_pct=False,
                             unit="milestone assignments"))
    lines.append("")

    # --- RCA / environment / module / category -------------------------------
    lines.append(H("Root Cause Analysis (RCA)"))
    lines.append("")
    lines.append(count_table("RCA", by_rca, limit=20))
    lines.append("")

    lines.append(H("Hosting Environment"))
    lines.append("")
    lines.append(count_table("Hosting Environment", by_hosting))
    lines.append("")

    lines.append(H("Module"))
    lines.append("")
    lines.append(count_table("Module", by_module, limit=20))
    lines.append("")

    lines.append(H("Category"))
    lines.append("")
    lines.append(count_table("Category", by_category, limit=20))
    lines.append("")

    # --- Client vs internal cross-tabs --------------------------------------
    lines.append(H("Client vs Internal by Issue Type"))
    lines.append("")
    cbt = tally(client_tickets, lambda t: t["issuetype"])
    ibt = tally(internal_tickets, lambda t: t["issuetype"])
    rows_ct = []
    for k in sorted(set(cbt) | set(ibt)):
        rows_ct.append([k, str(cbt.get(k, 0)), str(ibt.get(k, 0)),
                        str(cbt.get(k, 0) + ibt.get(k, 0))])
    rows_ct.append(["**Total**", f"**{client_count}**", f"**{internal_count}**",
                    f"**{total}**"])
    lines.append(table(["Issue Type", "Client", "Internal", "Total"], rows_ct,
                       ["---", "---:", "---:", "---:"]))
    lines.append("")

    lines.append(H("Client vs Internal by Status"))
    lines.append("")
    cbs = tally(client_tickets, lambda t: t["status"])
    ibs = tally(internal_tickets, lambda t: t["status"])
    rows_cs = []
    for k in sorted(set(cbs) | set(ibs)):
        rows_cs.append([k, str(cbs.get(k, 0)), str(ibs.get(k, 0)),
                        str(cbs.get(k, 0) + ibs.get(k, 0))])
    rows_cs.append(["**Total**", f"**{client_count}**", f"**{internal_count}**",
                    f"**{total}**"])
    lines.append(table(["Status", "Client", "Internal", "Total"], rows_cs,
                       ["---", "---:", "---:", "---:"]))
    lines.append("")

    # --- Open tickets by priority -------------------------------------------
    lines.append(H("Open Tickets by Priority"))
    lines.append("")
    open_tickets = [t for t in tickets if t["_state"] == C.OPEN]
    obp = tally(open_tickets, lambda t: t["priority"])
    rows_op = [[s, str(c)] for s, c in obp.most_common()]
    rows_op.append(["**Total**", f"**{len(open_tickets)}**"])
    lines.append(table(["Priority", "Open Count"], rows_op, ["---", "---:"]))
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
            ["Key", "Summary", "Type", "Priority", "Client"],
            [[f"[{t['key']}]({JIRA_BROWSE_BASE}/browse/{t['key']})",
              t["summary"][:80], t["issuetype"], t["priority"],
              t["primary_client"] if t["_bucket"] == C.CLIENT else "Internal"]
             for t in shown],
        ))
        lines.append(listing_total(len(shown), len(unassigned), "unassigned tickets"))
        lines.append("")

    # --- High-priority open --------------------------------------------------
    lines.append(H("High-Priority Open Tickets (High / ShowStopper)"))
    lines.append("")
    high_open = [t for t in open_tickets if t["priority"] in ("High", "ShowStopper")]
    if high_open:
        shown = high_open[:30]
        lines.append(table(
            ["Key", "Summary", "Status", "Priority", "Assignee"],
            [[f"[{t['key']}]({JIRA_BROWSE_BASE}/browse/{t['key']})",
              t["summary"][:80], t["status"], t["priority"], t["assignee"]]
             for t in shown],
        ))
        lines.append(listing_total(len(shown), len(high_open), "high-priority open tickets"))
    else:
        lines.append("_No high-priority open tickets._")
    lines.append("")

    # --- Labels --------------------------------------------------------------
    lines.append(H("Labels"))
    lines.append("")
    label_counter: collections.Counter = collections.Counter()
    for t in tickets:
        labels = t.get("labels") or []
        if isinstance(labels, list):
            for lb in labels:
                label_counter[lb] += 1
        elif labels:
            label_counter[str(labels)] += 1
    if label_counter:
        lines.append(count_table("Label", label_counter, limit=20, show_pct=False,
                                 unit="label assignments"))
    else:
        lines.append("_No labels found._")
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
    alias_rows = [[jira, owner] for jira, owner in sorted(C.STATUS_ALIASES.items())]
    lines.append(table(["Jira status (normalised)", "Owner list entry"], alias_rows))
    lines.append("")

    # --- Footer --------------------------------------------------------------
    lines.append("---")
    lines.append("")
    lines.append(f"*Report generated by `tools/jira/jira_analysis_2026.py` on {now}*")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="PAMIT ticket analysis 2026")
    parser.add_argument("--offline", action="store_true",
                        help="Reuse newest snapshot, zero HTTP")
    args = parser.parse_args()

    snap_dir = SNAP_DIR
    snap_dir.mkdir(parents=True, exist_ok=True)
    snap_file = snap_dir / f"jira-analysis-{DATE_FROM}-to-{DATE_TO}.json"

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
        print(f"Connected as: {j.whoami()} | Project: {j.project}", file=sys.stderr)
        print(f"Fetching tickets created {DATE_FROM} to {DATE_TO}...", file=sys.stderr)
        raw = fetch_tickets(j)
        print(f"Fetched {len(raw)} tickets total.", file=sys.stderr)
        # Save snapshot
        snap_file.write_text(json.dumps(raw, indent=2, ensure_ascii=False),
                             encoding="utf-8")
        print(f"Snapshot saved: {snap_file}", file=sys.stderr)

    # Normalise
    tickets = [normalise(issue) for issue in raw]
    print(f"Normalised {len(tickets)} tickets.", file=sys.stderr)

    # Build report
    report = build_report(tickets, snapshot=snap_file)

    # Write report
    out_file = OUT_DIR / f"Jira_Analysis_{RANGE_SLUG}.md"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file.write_text(report, encoding="utf-8")
    print(f"\nReport written: {out_file}", file=sys.stderr)
    print(f"Total tickets: {len(tickets)}", file=sys.stderr)


if __name__ == "__main__":
    # `main()` returns a non-zero code on refusal; a bare call would discard it
    # and report success to whatever ran this.
    sys.exit(main() or 0)
