#!/usr/bin/env python3
"""Independent validation of the 2026 census reports against their own source data.

    python tools\\jira\\validate_analysis.py                 # both projects
    python tools\\jira\\validate_analysis.py --project CI    # one of PAMIT | CI
    python tools\\jira\\validate_analysis.py --json          # machine-readable

Exit code: 0 = every check passed, 1 = at least one FAIL, 2 = could not run.

Why this exists
---------------
`OBJ-030` shipped eleven gates per project and both live defects passed all of them,
because those gates test **reproducibility against the generator's own rule** — re-running
the generator reproduces the report, so a rule that is correctly implemented and wrongly
named reconciles perfectly. Reconciliation is not validation.

So this script deliberately does **not** call the generators. It re-derives every headline
figure straight from the raw snapshot, reads the published markdown as text, and compares
the two. A figure only passes when the report and the source agree, which is the one thing
the generator cannot assert about itself.

It is offline by construction: it reads snapshots and files on disk and issues no HTTP.

Its own wording is ASCII; the report text it quotes back (section headings carry em dashes)
is not, so `main()` reconfigures the streams with `errors="replace"`. Verified to run clean
under `PYTHONIOENCODING=cp1252` — the console-less-child failure mode the other scripts in
this folder carry a warning about cannot kill this one mid-report.

Check families
--------------
    A  snapshot integrity        the source data is well formed
    B  published vs recount      every headline figure re-derived from the snapshot
    C  markdown self-consistency totals sum, percentages divide, footnotes reconcile
    D  artifact provenance       .docx/.xlsx and the delivery pack derive from the .md
    E  cross-report agreement    both reports describe the same window
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from paths import workspace_root                                        # noqa: E402
import analysis_classify as C                                           # noqa: E402

ROOT = workspace_root()
ANALYSIS = ROOT / "docs" / "analysis"

#: Everything that differs between the two census lines, in one place. Adding a third
#: project is a row here, not a branch inside the checks.
PROJECTS = {
    "PAMIT": {
        "prefix": "PAMIT",
        "report": ANALYSIS / "Jira_Analysis_01Jan26-21Sep26.md",
        "snapshot": (ROOT / "artifacts" / "client-tickets" / "snapshots"
                     / "jira-analysis-2026-01-01-to-2026-09-21.json"),
        "pack": ROOT / "21-09-2026" / "PAM" / "PAM_Analysis.md",
        "generator": "jira_analysis_2026.py",
    },
    "CI": {
        "prefix": "CI",
        "report": ANALYSIS / "CI_Jira_Analysis_01Jan26-21Sep26.md",
        "snapshot": (ROOT / "artifacts" / "snapshots"
                     / "ci-analysis-2026-01-01-to-2026-09-21.json"),
        "pack": ROOT / "21-09-2026" / "CI" / "CI_Analysis.md",
        "generator": "ci_analysis_2026.py",
    },
}

DATE_FROM = "2026-01-01"
DATE_TO = "2026-09-21"

_INT_CELL = re.compile(r"^-?[\d,]+$")
_N_PCT = re.compile(r"^([\d,]+)\s*\(([\d.]+)%\)$")


# ---------------------------------------------------------------- result plumbing

class Results:
    """Ordered PASS/FAIL/WARN/INFO ledger. Only FAIL moves the exit code.

    INFO exists so a fact that cannot be proven offline — an empty calendar day might
    be a genuine zero or a fetch gap — is reported rather than silently dropped or
    turned into a failure the operator learns to ignore.
    """

    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add(self, scope: str, check: str, ok, detail: str) -> None:
        state = "INFO" if ok is None else ("PASS" if ok else "FAIL")
        self.rows.append({"scope": scope, "check": check, "state": state,
                          "detail": detail})

    @property
    def failed(self) -> int:
        return sum(1 for r in self.rows if r["state"] == "FAIL")

    def counts(self) -> dict:
        c = collections.Counter(r["state"] for r in self.rows)
        return {k: c.get(k, 0) for k in ("PASS", "FAIL", "WARN", "INFO")}


def eq(res: Results, scope: str, check: str, published, recount, unit: str = "") -> None:
    """The workhorse: assert a published figure equals an independently derived one."""
    ok = published == recount
    u = " " + unit if unit else ""
    if ok:
        detail = "report {}{} == source {}{}".format(published, u, recount, u)
    elif isinstance(published, int) and isinstance(recount, int):
        detail = "report says {}{}, source says {}{} (difference {:+d})".format(
            published, u, recount, u, published - recount)
    else:
        detail = "report says {!r}, source says {!r}".format(published, recount)
    res.add(scope, check, ok, detail)


# ---------------------------------------------------------------- markdown parsing

def parse_tables(md: str) -> list:
    """Every markdown table in the document, with the section heading above it.

    A deliberately small, self-contained parser. Reusing `analysis_render.parse_md`
    would make the validator inherit any bug in the renderer it is meant to check.
    """
    tables = []
    section = "(preamble)"
    #: Prose seen since the previous table. A note explaining a table often sits under
    #: the PARENT heading ("## 6. Components") while the table sits under a child
    #: ("### 6A. ..."), so the buffer deliberately spans headings rather than resetting
    #: on each one - otherwise the explanation a check needs is invisible to it.
    prose: list = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            section = line.lstrip("#").strip()
            prose.append(line)
            i += 1
            continue
        is_sep = (i + 1 < len(lines)
                  and lines[i + 1].startswith("|")
                  and set(lines[i + 1].replace("|", "").replace(" ", "")) <= set("-:")
                  and lines[i + 1].strip() != "")
        if line.startswith("|") and is_sep:
            header = _cells(line)
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(_cells(lines[j]))
                j += 1
            # Text immediately BELOW the table. A note qualifying a table - the
            # truncation footnote, or a statement of what the table had to leave out -
            # is written underneath it, so a check that only looked at `prose` (which is
            # what precedes) would never see it.
            after, footnote = [], ""
            for k in range(j, min(j + 4, len(lines))):
                s = lines[k].strip()
                if not s:
                    continue
                if s.startswith(("|", "#")):
                    break
                after.append(s)
                if s.startswith("_") and s.endswith("_") and not footnote:
                    footnote = s
            tables.append({"section": section, "header": header, "rows": rows,
                           "footnote": footnote, "line": i + 1,
                           "prose": "\n".join(prose), "after": "\n".join(after)})
            prose = []
            i = j
            continue
        if line.strip():
            prose.append(line)
        i += 1
    return tables


def _cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _int(cell: str):
    """The integer in a cell, through bold markers and thousands separators."""
    c = cell.replace("**", "").strip()
    if _INT_CELL.match(c):
        return int(c.replace(",", ""))
    return None


def summary_metrics(tables: list) -> dict:
    """The section 1 Summary rows as {metric: (count, percentage or None)}."""
    for t in tables:
        if t["section"].lower().endswith("summary"):
            out = {}
            for r in t["rows"]:
                if len(r) < 2:
                    continue
                m = _N_PCT.match(r[1])
                if m:
                    out[r[0]] = (int(m.group(1).replace(",", "")), float(m.group(2)))
                else:
                    v = _int(r[1])
                    if v is not None:
                        out[r[0]] = (v, None)
            return out
    return {}


def _header_total(md: str) -> int:
    m = re.search(r"\*\*Total tickets:\*\*\s*([\d,]+)", md)
    return int(m.group(1).replace(",", "")) if m else -1


# ---------------------------------------------------------------- A: snapshot

def check_snapshot(res: Results, name: str, cfg: dict, raw: list) -> None:
    scope = name + "/A snapshot"
    res.add(scope, "A1-loaded", bool(raw),
            "{} issues in {}".format(len(raw), cfg["snapshot"].name))

    keys = [i.get("key", "") for i in raw]
    dupes = [k for k, n in collections.Counter(keys).items() if n > 1]
    res.add(scope, "A2-unique-keys", not dupes,
            "no duplicate issue keys" if not dupes
            else "duplicates: {}".format(dupes[:5]))

    wrong = sorted({k.split("-")[0] for k in keys if k} - {cfg["prefix"]})
    res.add(scope, "A3-project-prefix", not wrong,
            "every key is {}-*".format(cfg["prefix"]) if not wrong
            else "foreign prefixes present: {}".format(wrong))

    created = [(i.get("fields", {}).get("created") or "")[:10] for i in raw]
    out_of_range = [d for d in created if d and not (DATE_FROM <= d <= DATE_TO)]
    res.add(scope, "A4-window", not out_of_range,
            "every created date within {}..{}".format(DATE_FROM, DATE_TO)
            if not out_of_range
            else "{} outside the window, e.g. {}".format(
                len(out_of_range), out_of_range[:3]))

    missing = sum(1 for i in raw
                  if not i.get("key")
                  or not (i.get("fields") or {}).get("created")
                  or not (i.get("fields") or {}).get("status"))
    res.add(scope, "A5-required-fields", missing == 0,
            "key, created and status present on every issue" if not missing
            else "{} issues missing a required field".format(missing))

    # A calendar gap cannot be proven genuine offline, so it is reported, never failed.
    have = set(created)
    lo, hi = dt.date.fromisoformat(DATE_FROM), dt.date.fromisoformat(DATE_TO)
    span = [(lo + dt.timedelta(days=n)).isoformat() for n in range((hi - lo).days + 1)]
    gaps = [d for d in span if d not in have]
    res.add(scope, "A6-calendar-gaps", None,
            "no empty days in the window" if not gaps
            else "{} days with zero tickets ({}{}) - confirm each is a genuine zero "
                 "at source".format(len(gaps), ", ".join(gaps[:6]),
                                    " ..." if len(gaps) > 6 else ""))


# ---------------------------------------------------------------- B: recount

def check_recount(res: Results, name: str, cfg: dict, raw: list,
                  md: str, tables: list) -> None:
    scope = name + "/B recount"
    total = len(raw)
    summary = summary_metrics(tables)

    # B0 first: if the report was not built from this snapshot, every comparison below
    # is measuring two unrelated things and its PASSes would mean nothing.
    claimed = re.search(r"\*\*Source snapshot:\*\*\s*`([^`]+)`.*?sha256\s*`([0-9a-f]+)`",
                        md)
    if claimed is None:
        res.add(scope, "B0-provenance", False,
                "report names no source snapshot - it cannot be traced to the data it "
                "was built from; re-run the generator")
    else:
        actual_name = cfg["snapshot"].name
        actual_sha = _sha256_prefix(cfg["snapshot"], len(claimed.group(2)))
        ok = claimed.group(1) == actual_name and claimed.group(2) == actual_sha
        res.add(scope, "B0-provenance", ok,
                "built from {} (sha256 {})".format(actual_name, actual_sha) if ok
                else "report claims {} sha256 {}, on disk {} hashes to {} - the report "
                     "does not describe this snapshot".format(
                         claimed.group(1), claimed.group(2), actual_name, actual_sha))

    eq(res, scope, "B1-header-total", _header_total(md), total, "tickets")
    if "Total tickets" in summary:
        eq(res, scope, "B2-summary-total", summary["Total tickets"][0], total, "tickets")

    # Client / internal, re-derived through the shared rule. The rule IS the definition,
    # so re-implementing it here would only test a transcription; what is worth checking
    # is that the published figure is the one the rule actually produces over this data.
    buckets = collections.Counter(C.client_bucket(_primary_client(i)) for i in raw)
    if "Client tickets" in summary:
        eq(res, scope, "B3-client", summary["Client tickets"][0],
           buckets[C.CLIENT], "tickets")
    if "Internal tickets" in summary:
        eq(res, scope, "B4-internal", summary["Internal tickets"][0],
           buckets[C.INTERNAL], "tickets")

    states = collections.Counter(
        C.classify_status(((i.get("fields") or {}).get("status") or {}).get("name"))
        for i in raw)
    for label, key, cid in (("Open", C.OPEN, "B5-open"),
                            ("Closed", C.CLOSED, "B6-closed"),
                            ("Unmapped status", C.UNMAPPED, "B7-unmapped")):
        if label in summary:
            eq(res, scope, cid, summary[label][0], states[key], "tickets")

    # The two identities the report's own preamble promises the reader.
    o, c, u = states[C.OPEN], states[C.CLOSED], states[C.UNMAPPED]
    res.add(scope, "B8-identity-status", o + c + u == total,
            "Open {} + Closed {} + Unmapped {} = {} vs total {}".format(
                o, c, u, o + c + u, total))
    cl, it = buckets[C.CLIENT], buckets[C.INTERNAL]
    res.add(scope, "B9-identity-client", cl + it == total,
            "Client {} + Internal {} = {} vs total {}".format(cl, it, cl + it, total))

    if name == "CI":
        subs = sum(1 for i in raw
                   if ((i.get("fields") or {}).get("issuetype") or {}).get("subtask"))
        by_name = sum(1 for i in raw
                      if (((i.get("fields") or {}).get("issuetype") or {})
                          .get("name")) == "Sub-task")
        res.add(scope, "B10-subtask-agreement", subs == by_name,
                "issuetype.subtask ({}) agrees with issuetype.name ({})".format(
                    subs, by_name))
        if "Sub-tasks" in summary:
            eq(res, scope, "B11-subtasks", summary["Sub-tasks"][0], subs, "sub-tasks")
        if "Standalone (non-sub-task)" in summary:
            eq(res, scope, "B12-standalone", summary["Standalone (non-sub-task)"][0],
               total - subs, "tickets")
        # The defect this file was written too late to prevent: `parent` spans the whole
        # hierarchy, so parent-presence is not a sub-task test. Keep measuring the gap.
        by_parent = sum(1 for i in raw if (i.get("fields") or {}).get("parent"))
        res.add(scope, "B13-parent-not-subtask", None,
                "{} issues carry a parent but only {} are sub-tasks - the other {} are "
                "Epic children; never count parent-presence".format(
                    by_parent, subs, by_parent - subs))

    if name == "PAMIT":
        for cid, field, jira_field, noun in (
                ("B10-milestone", "customfield_10092", "Affected Milestone",
                 "an affected milestone"),
                ("B11-fixversion", "fixVersions", "Fix Version", "a fix version")):
            stats = _multi_stats(raw, field)
            claim = _coverage_claim(md, noun)
            if claim is None:
                res.add(scope, cid, False,
                        "no coverage line found for {} - the section must state its "
                        "populated subset (D46)".format(jira_field))
                continue
            res.add(scope, cid, claim == stats,
                    "{}: report (tickets, assignments, values)={} == source {}".format(
                        jira_field, claim, stats) if claim == stats
                    else "{}: report says (tickets, assignments, values)={}, source "
                         "says {}".format(jira_field, claim, stats))



def _sha256_prefix(path: Path, length: int) -> str:
    """The digest a report's provenance line should carry, recomputed from the file."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:length]


def _primary_client(issue: dict):
    v = (issue.get("fields") or {}).get("customfield_10112")
    if isinstance(v, dict):
        return v.get("value") or v.get("name")
    if isinstance(v, list):
        return v[0].get("value") if v and isinstance(v[0], dict) else None
    return v


def _multi_stats(raw: list, field: str) -> tuple:
    """(tickets carrying the field, assignments, distinct values) - assignments only.

    An unpopulated ticket contributes nothing. That is the whole point: counting it as
    a `Not set` assignment is what published 5,832 milestone assignments where 4,615
    exist.
    """
    populated, assigns = 0, 0
    values = set()
    for i in raw:
        v = (i.get("fields") or {}).get(field)
        if not v:
            continue
        populated += 1
        for x in (v if isinstance(v, list) else [v]):
            label = (x.get("value") or x.get("name")) if isinstance(x, dict) else x
            if label:
                assigns += 1
                values.add(label)
    return populated, assigns, len(values)


def _coverage_claim(md: str, noun: str):
    m = re.search(
        r"\*\*Coverage:\*\*\s*([\d,]+) of [\d,]+ tickets \([\d.]+%\) carry "
        + re.escape(noun)
        + r"; they account for ([\d,]+) assignments across ([\d,]+) distinct values",
        md)
    if not m:
        return None
    return tuple(int(g.replace(",", "")) for g in m.groups())


# ---------------------------------------------------------------- C: self-consistency

#: A unit that names an assignment, not a ticket. A table counting these must not carry
#: a row for the tickets that have none - that is the section 12 defect, as a reusable
#: lint so the whole class cannot come back in another section.
_ASSIGNMENT_UNITS = ("assignments",)
_EMPTY_LABELS = {"not set", "none", "unknown", "unassigned", "n/a", "-"}

#: The sentence a section uses to declare that its rows deliberately out-sum its Total.
_DECLARED_SUM = re.compile(r"rows sum to ([\d,]+)")


def _declared_row_sum(prose: str):
    """The row sum a section claims for itself, if it claims one."""
    m = _DECLARED_SUM.search(prose or "")
    return int(m.group(1).replace(",", "")) if m else None


def check_markdown(res: Results, name: str, md: str, tables: list) -> None:
    scope = name + "/C markdown"
    total = _header_total(md)

    bad_totals, checked_totals, explained = [], 0, 0
    for t in tables:
        if not t["rows"]:
            continue
        last = t["rows"][-1]
        if "total" not in last[0].lower() or "**" not in last[0]:
            continue
        # A multi-value axis (components, labels) legitimately has rows that sum past
        # the ticket total, because one ticket lands in several rows. That is only
        # acceptable when the report SAYS so and states the figure - so the check does
        # not wave it through, it verifies the stated number against the real row sum.
        declared = _declared_row_sum(t["prose"])
        body = t["rows"][:-1]
        first_numeric = True
        for col in range(1, len(last)):
            head = t["header"][col] if col < len(t["header"]) else ""
            if "%" in head:
                continue
            claimed = _int(last[col])
            if claimed is None:
                continue
            parts = [_int(r[col]) for r in body if col < len(r)]
            if not parts or any(p is None for p in parts):
                continue
            actual = sum(p for p in parts if p is not None)
            checked_totals += 1
            is_first, first_numeric = first_numeric, False
            if actual == claimed:
                continue
            if declared is None:
                bad_totals.append(
                    "{!r} col {!r}: rows sum to {}, Total says {}, and nothing in the "
                    "section explains the gap".format(
                        t["section"], head, actual, claimed))
            elif is_first and actual != declared:
                # The declared figure names the leading count column - the one the
                # prose calls "assignments". If that number is wrong the explanation is
                # worse than none, so it is checked rather than taken on trust.
                bad_totals.append(
                    "{!r} col {!r}: prose says the rows sum to {}, they actually sum "
                    "to {}".format(t["section"], head, declared, actual))
            else:
                # Same multi-value cause, stated once for the table; the remaining
                # columns inherit it and carry no separate figure to verify.
                explained += 1
    res.add(scope, "C1-totals-sum", not bad_totals,
            "{} Total cells checked; {} equal their column sum, {} differ for a reason "
            "the report states and this check verified".format(
                checked_totals, checked_totals - explained, explained)
            if not bad_totals else "; ".join(bad_totals[:4]))

    bad_pct = []
    for t in tables:
        for col, h in enumerate(t["header"]):
            if h.strip().lower() != "% of total" or col == 0:
                continue
            for r in t["rows"]:
                if col >= len(r):
                    continue
                n = _int(r[col - 1])
                p = r[col].replace("**", "").rstrip("%")
                if n is None or not re.match(r"^-?[\d.]+$", p):
                    continue
                if total > 0 and abs(float(p) - (100.0 * n / total)) > 0.1:
                    bad_pct.append("{!r} {!r}: says {}%, {}/{} is {:.1f}%".format(
                        t["section"], r[0], p, n, total, 100.0 * n / total))
    res.add(scope, "C2-percentages", not bad_pct,
            "every '% of Total' cell equals its count over the ticket total"
            if not bad_pct else "; ".join(bad_pct[:4]))

    bad_foot = []
    for t in tables:
        m = re.match(r"_(\d+) further values not shown, accounting for "
                     r"([\d,]+) of ([\d,]+) (.+?)\._$", t["footnote"])
        if not m:
            continue
        hidden = int(m.group(2).replace(",", ""))
        grand = int(m.group(3).replace(",", ""))
        shown = _int(t["rows"][-1][1]) if t["rows"] else None
        if shown is not None and shown + hidden != grand:
            bad_foot.append("{!r}: shown {} + hidden {} = {}, footnote grand total "
                            "says {}".format(t["section"], shown, hidden,
                                             shown + hidden, grand))
    res.add(scope, "C3-footnotes", not bad_foot,
            "every truncation footnote reconciles with its Total row"
            if not bad_foot else "; ".join(bad_foot[:4]))

    # C5: the trend tables partition the population by date, so their Totals must equal
    # the ticket total - unless the report states how many tickets it had to leave out.
    # Without this, a dropped date leaves a Total that is quietly low and still exactly
    # equals the sum of its own rows, which is invisible to C1 and to any reconciliation.
    bad_trend = []
    for t in tables:
        if "creation trend" not in t["section"].lower() or not t["rows"]:
            continue
        claimed = _int(t["rows"][-1][1])
        if claimed is None or claimed == total:
            continue
        m = re.search(r"\*\*(\d+) of [\d,]+ tickets carry no parsable", t["after"])
        stated = int(m.group(1)) if m else None
        if stated is None:
            bad_trend.append("{!r}: Total {} against a population of {}, with nothing "
                             "accounting for the {} missing".format(
                                 t["section"], claimed, total, total - claimed))
        elif claimed + stated != total:
            bad_trend.append("{!r}: Total {} + {} stated as undated = {}, not the "
                             "population of {}".format(t["section"], claimed, stated,
                                                       claimed + stated, total))
    res.add(scope, "C5-trend-partition", not bad_trend,
            "every creation-trend Total accounts for the whole population"
            if not bad_trend else "; ".join(bad_trend[:4]))

    bad_unit = []
    for t in tables:
        # A table declares "assignments" in two places: the truncation footnote, and the
        # coverage line above it. Keying on both matters - the original section 12 had
        # no footnote at all (it was short enough not to truncate), so a footnote-only
        # lint would have let the very defect it exists for straight through.
        declares_assignments = (
            any(u in t["footnote"] for u in _ASSIGNMENT_UNITS)
            or "The table counts **assignments**" in t["prose"])
        if not declares_assignments:
            continue
        for r in t["rows"]:
            if r[0].replace("**", "").strip().lower() in _EMPTY_LABELS:
                bad_unit.append("{!r} carries a {!r} row in a table whose unit is "
                                "assignments - unpopulated tickets are not assignments; "
                                "state coverage instead (D46)".format(t["section"], r[0]))
    res.add(scope, "C4-assignment-unit", not bad_unit,
            "no assignment table counts unpopulated tickets as assignments"
            if not bad_unit else "; ".join(bad_unit[:4]))


# ---------------------------------------------------------------- D: provenance

def check_provenance(res: Results, name: str, cfg: dict) -> None:
    scope = name + "/D provenance"
    md = cfg["report"]
    for ext in (".docx", ".xlsx"):
        sib = md.with_suffix(ext)
        if not sib.exists():
            res.add(scope, "D1-" + ext.lstrip(".") + "-exists", False,
                    "missing render: {}".format(sib.name))
            continue
        fresh = sib.stat().st_mtime >= md.stat().st_mtime
        res.add(scope, "D1-" + ext.lstrip(".") + "-fresh", fresh,
                "{} rendered after the markdown".format(sib.name) if fresh
                else "{} is OLDER than {} - it does not describe the current report; "
                     "re-render it".format(sib.name, md.name))

    pack = cfg["pack"]
    if not pack.exists():
        res.add(scope, "D2-pack-present", False,
                "delivery pack missing: {}".format(pack))
        return
    same = pack.read_bytes() == md.read_bytes()
    res.add(scope, "D2-pack-identical", same,
            "{}/{} is byte-identical to the canonical report".format(
                pack.parent.name, pack.name) if same
            else "{}/{} DIFFERS from {} - the pack ships a different analysis; re-run "
                 "build_delivery_pack.py".format(pack.parent.name, pack.name, md.name))
    for ext in (".docx", ".xlsx"):
        sib = pack.with_suffix(ext)
        if not sib.exists():
            res.add(scope, "D3-" + ext.lstrip(".") + "-exists", False,
                    "missing pack render: {}".format(sib.name))
        else:
            fresh = sib.stat().st_mtime >= pack.stat().st_mtime
            res.add(scope, "D3-" + ext.lstrip(".") + "-fresh", fresh,
                    "pack {} rendered after its markdown".format(sib.name) if fresh
                    else "pack {} is OLDER than {}".format(sib.name, pack.name))


# ---------------------------------------------------------------- E: cross-report

def check_cross(res: Results, loaded: dict) -> None:
    scope = "cross/E agreement"
    pairs = {}
    for n, d in loaded.items():
        m = re.search(r"\*\*Date range:\*\*\s*(\S+) to (\S+)", d["md"])
        if m:
            pairs[n] = (m.group(1), m.group(2))
    if len(pairs) < 2:
        res.add(scope, "E1-same-window", None,
                "only one project loaded; nothing to compare")
        return
    same = len(set(pairs.values())) == 1
    res.add(scope, "E1-same-window", same,
            "both reports cover {}".format(sorted(set(pairs.values()))[0]) if same
            else "reports cover DIFFERENT windows: {}".format(pairs))
    declared = (DATE_FROM, DATE_TO)
    matches = [n for n, v in pairs.items() if v == declared]
    res.add(scope, "E2-matches-validator", len(matches) == len(pairs),
            "both reports cover the window this validator checks {}".format(declared)
            if len(matches) == len(pairs)
            else "validator is pinned to {} but reports cover {} - update DATE_FROM/"
                 "DATE_TO here when the census window moves".format(declared, pairs))


# ---------------------------------------------------------------- self-test

#: (label, markdown, the check that must FAIL on it — or None if it must come out clean).
#: A check that has only ever been seen to pass is indistinguishable from one that cannot
#: fail, so each markdown check is paired here with the smallest input that separates the
#: two, and with the corrected version of the same input. There is no test framework in
#: this workspace, so this rides along in the file it tests rather than importing one.
SELF_TEST_CASES = [
    ("undated tickets dropped from a trend table, silently",
     """# T

**Total tickets:** 100

## 9. Weekly Creation Trend

| Week | Count |
| --- | ---: |
| 2026-W01 | 97 |
| **Total** | **97** |
""", "C5-trend-partition"),

    ("...the same drop, stated under the table",
     """# T

**Total tickets:** 100

## 9. Weekly Creation Trend

| Week | Count |
| --- | ---: |
| 2026-W01 | 97 |
| **Total** | **97** |

**3 of 100 tickets carry no parsable `created` date** and are therefore absent.
""", None),

    ("a 'Not set' row inside a table counting assignments",
     """# T

**Total tickets:** 100

## 12. Affected Milestone

**Coverage:** 60 of 100 tickets (60.0%) carry an affected milestone; they account for 70 assignments across 5 distinct values. The table counts **assignments**, so a ticket carrying more than one appears more than once.

| Affected Milestone | Count |
| --- | ---: |
| Not set | 40 |
| HF6 | 70 |
| **Total** | **110** |
""", "C4-assignment-unit"),

    ("a Total that is not its column sum, with no explanation",
     """# T

**Total tickets:** 100

## 6. Components

| Component | Count |
| --- | ---: |
| A | 60 |
| B | 50 |
| **Total** | **100** |
""", "C1-totals-sum"),

    ("...the same table, with the row sum declared and correct",
     """# T

**Total tickets:** 100

## 6. Components

Components are multi-valued, so the rows sum to 110 component assignments across 100 distinct tickets. The **Total** row states distinct tickets.

| Component | Count |
| --- | ---: |
| A | 60 |
| B | 50 |
| **Total** | **100** |
""", None),

    ("a percentage that does not equal its own count over the total",
     """# T

**Total tickets:** 100

## 2. Status

| Status | Count | % of Total |
| --- | ---: | ---: |
| Open | 25 | 80.0% |
| Closed | 75 | 75.0% |
| **Total** | **100** | **100.0%** |
""", "C2-percentages"),
]


def self_test() -> int:
    """Run every markdown check against the defect it exists for. 0 = all behaved."""
    print("Self-test: each check against the defect it exists for")
    print("=" * 72)
    bad = 0
    for label, md, expected in SELF_TEST_CASES:
        res = Results()
        check_markdown(res, "self-test", md, parse_tables(md))
        fired = sorted(r["check"] for r in res.rows if r["state"] == "FAIL")
        if expected is None:
            ok = not fired
            got = "clean" if ok else "unexpectedly failed " + ", ".join(fired)
        else:
            ok = fired == [expected]
            got = ("caught by " + expected) if ok else (
                "expected " + expected + ", got " + (", ".join(fired) or "nothing"))
        bad += 0 if ok else 1
        print("  [{}] {:<58} {}".format("PASS" if ok else "FAIL", label, got))
    print("\n" + "=" * 72)
    if bad:
        print("SELF-TEST FAILED - {} case(s) did not behave as specified. The checks "
              "cannot be trusted until this is green.".format(bad))
        return 1
    print("SELF-TEST PASSED - every check fires on its defect and stays quiet without it.")
    return 0


# ---------------------------------------------------------------- driver

def run(selected: list) -> Results:
    res = Results()
    loaded = {}
    for name in selected:
        cfg = PROJECTS[name]
        if not cfg["snapshot"].exists():
            res.add(name + "/A snapshot", "A1-loaded", False,
                    "snapshot not found: {}".format(cfg["snapshot"]))
            continue
        if not cfg["report"].exists():
            res.add(name + "/B recount", "B0-report", False,
                    "report not found: {}".format(cfg["report"]))
            continue
        raw = json.loads(cfg["snapshot"].read_text(encoding="utf-8"))
        md = cfg["report"].read_text(encoding="utf-8")
        tables = parse_tables(md)
        loaded[name] = {"raw": raw, "md": md, "tables": tables}

        check_snapshot(res, name, cfg, raw)
        check_recount(res, name, cfg, raw, md, tables)
        check_markdown(res, name, md, tables)
        check_provenance(res, name, cfg)
    check_cross(res, loaded)
    return res


def report(res: Results, as_json: bool) -> int:
    if as_json:
        print(json.dumps({"counts": res.counts(), "checks": res.rows}, indent=2))
        return 1 if res.failed else 0

    width = max([len(r["check"]) for r in res.rows] + [10])
    scope = None
    for r in res.rows:
        if r["scope"] != scope:
            scope = r["scope"]
            print("\n" + scope)
            print("-" * len(scope))
        print("  [{:<4}] {:<{}}  {}".format(r["state"], r["check"], width, r["detail"]))

    c = res.counts()
    print("\n" + "=" * 72)
    print("PASS {}   FAIL {}   WARN {}   INFO {}".format(
        c["PASS"], c["FAIL"], c["WARN"], c["INFO"]))
    if res.failed:
        print("\nRESULT: FAIL - fix the generator and re-run it. Never hand-edit the "
              "markdown to make a check pass.")
        return 1
    print("\nRESULT: PASS - every published figure matches the source data.")
    return 0


def main() -> int:
    # The report text quoted in details is not ASCII (em dashes in headings) and a
    # Windows ANSI console would otherwise kill the process mid-report.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(
        description="Validate the census reports against their snapshots.")
    ap.add_argument("--project", choices=sorted(PROJECTS) + ["all"], default="all",
                    help="limit the run to one project (default: all)")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable output for CI or a scheduled check")
    ap.add_argument("--self-test", action="store_true",
                    help="run each markdown check against the defect it exists for, "
                         "and against the corrected version; touches no project data")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    selected = sorted(PROJECTS) if a.project == "all" else [a.project]
    try:
        res = run(selected)
    except Exception as exc:                                            # noqa: BLE001
        print("validator could not run: {}: {}".format(type(exc).__name__, exc),
              file=sys.stderr)
        return 2
    return report(res, a.json)


if __name__ == "__main__":
    sys.exit(main())
