#!/usr/bin/env python3
"""Client-raised PAMIT ticket analysis — patterns, trends and testing gaps (`OBJ-028`).

Connects related tickets into patterns instead of listing them. Jira access is
read-only by construction: every request goes through `jira_query.ReadOnlyJira`,
which refuses any method or path that could change anything.

    python tools\\jira\\pamit_client_analysis.py              # fetch, analyse, write reports
    python tools\\jira\\pamit_client_analysis.py --no-write   # analyse, write nothing
    python tools\\jira\\pamit_client_analysis.py --offline    # reuse newest snapshot, zero HTTP
    python tools\\jira\\pamit_client_analysis.py --json       # machine-readable to stdout

Five views, each with its own denominator, never mixed:

    1. Build / release      every 35.8.29 version, with the Jira release date reported
                            beside it and build number — not date — doing the ordering
    2. Focus builds         HF12 / HF13 (current) / HF14 / HF15 + in-flight patches:
                            deep analysis with the clone-link graph
    3. Last 30 days         what clients are reporting *now*, at any fix version
    4. Query C              open client defects carrying **no** fix version — invisible
                            to any build-based query by construction
    5. Testing areas        15 areas answering "which kind of testing would have
                            caught this", independent of module

Outputs (`D40` — no new top-level folder):

    docs/analysis/summary/summary_<date>.md         dated daily summary, never overwritten
    docs/analysis/summary.md                        index of the dated summaries
    docs/analysis/D1-client-ticket-patterns.md      the full living analysis
    artifacts/client-tickets/snapshots/<date>.json  immutable daily snapshot
    artifacts/client-tickets/tickets.csv            one row per ticket, pool-tagged
    artifacts/client-tickets/testing-areas.csv      the weak-spot table as data
    artifacts/client-tickets/patterns.json          groups, themes, areas, escape latency
    state/client-analysis/last-run.json + analysis.log

⚠️ **Two counting rules that must not drift.** `D38`: defect percentages use the
Bug/Security Fix/Client-Support/Performance subset, and `Duplicate`-status
tickets are held out of that denominator (a duplicate is the same defect twice).
`D39`: linked and parent tickets outside the fix-version window are evidence
only — they never enter a denominator. Every table states its own basis.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))          # tools/ — for paths.py

from paths import workspace_root                                    # noqa: E402
from jira_query import ReadOnlyJira, adf_text, field_value, link_edges  # noqa: E402
import pamit_analysis_rules as R                                    # noqa: E402
from pamit_fmt import pct, tally                                    # noqa: E402

ROOT = workspace_root()
OUT_DOCS = ROOT / "docs" / "analysis"

#: Base for `browse/<KEY>` links in the workbook. Held as a constant because an
#: `--offline` run has no Jira handle to read `j.base` from, and a workbook whose
#: links only work on online days would be worse than one that never links.
JIRA_BROWSE_BASE = "https://arcon-tech-solution.atlassian.net"
OUT_ART = ROOT / "artifacts" / "client-tickets"
OUT_STATE = ROOT / "state" / "client-analysis"

#: Link types that mean "the same defect, tracked again". `Cloners` dominates
#: this project: the working practice is to clone a client ticket into each
#: hotfix, so a clone edge is the strongest recurrence signal available.
RECURRENCE_LINKS = {"Cloners", "Duplicate"}


# ------------------------------------------------------------------------ fetching

def fetch_population(j: ReadOnlyJira, versions: list[str]) -> list[dict]:
    vlist = ", ".join(f'"{v}"' for v in versions)
    jql = f"project = {j.project} AND fixVersion IN ({vlist}) ORDER BY created ASC"
    return j.search(jql, R.FIELDS,
                    progress=lambda p, b, t: print(f"  page {p}: +{b} -> {t}", file=sys.stderr))


def fetch_context(j: ReadOnlyJira, keys: set[str]) -> dict[str, dict]:
    """Read linked/parent tickets outside the window — evidence only (`D39`).

    Batched through `key IN (...)` rather than one GET per key: 61 context
    tickets is 1 request, not 61. Keys from other projects are included; a
    pattern that reaches into another project is exactly the kind of finding
    worth surfacing.
    """
    if not keys:
        return {}
    ctx: dict[str, dict] = {}
    keys_l = sorted(keys)
    for i in range(0, len(keys_l), 90):
        batch = keys_l[i:i + 90]
        jql = "key IN (" + ", ".join(batch) + ") ORDER BY created ASC"
        try:
            for iss in j.search(jql, ["key", "summary", "issuetype", "status",
                                      "created", "fixVersions", "components",
                                      "customfield_10112"]):
                ctx[iss["key"]] = iss
        except SystemExit as e:
            # A key can be unreadable (deleted, or a project we lack rights to).
            # That is a data limitation to report, not a reason to abort.
            print(f"  context batch {i//90 + 1} unreadable: {e}", file=sys.stderr)
    return ctx


# ---------------------------------------------------------------------- normalising

def build_record(iss: dict) -> dict:
    f = iss["fields"]
    summary = f.get("summary") or ""
    desc = adf_text(f.get("description"))
    comps = [c["name"] for c in f.get("components") or []]
    fixv = [v["name"] for v in f.get("fixVersions") or []]
    release = next((R.FIX_VERSIONS[v] for v in fixv if v in R.FIX_VERSIONS), "?")
    # ⛔ `D42` — the build axis. `affected_build` is where the client FOUND it and
    # is what every build-wise count keys on; `fix_versions` is where the fix
    # SHIPS and is kept only as the second axis of escape latency.
    am_raw = field_value(f, R.AFFECTED_MILESTONE)
    am_infam, am_other = R.milestone_builds(am_raw)
    affected_build = R.earliest_build(am_raw)
    raw_client = field_value(f, "customfield_10112")
    title = R.clean_title(summary)
    # ⚠️ Title first, description only as a fallback. Categorising on the two
    # combined was measured wrong: the description mentions neighbouring
    # subsystems in passing, so `PAMIT-41274` ("SSH MYSQL service not accessible
    # in MAC") was pulled into "Session Recording & Audit Evidence" because its
    # description happens to say "video". The title is the reporter's own summary
    # of the defect and is the only high-signal field; `category_source` records
    # which one was used so a description-derived label can be discounted.
    primary, tags = R.categorise(title)
    source = "title"
    if primary == "Uncategorised" and desc:
        primary, tags = R.categorise(desc[:1500])
        source = "description" if primary != "Uncategorised" else "none"
    links = link_edges(f)
    return {
        "key": iss["key"],
        "summary": summary,
        "title": title,
        "release": release,
        "fix_versions": fixv,
        "issuetype": (f.get("issuetype") or {}).get("name"),
        "status": (f.get("status") or {}).get("name"),
        "status_category": ((f.get("status") or {}).get("statusCategory") or {}).get("name"),
        "priority": (f.get("priority") or {}).get("name"),
        "created": (f.get("created") or "")[:10],
        "updated": (f.get("updated") or "")[:10],
        "components": comps,
        "component": comps[0] if comps else "«none»",
        "labels": f.get("labels") or [],
        # Carried for the workbook's per-ticket sheet. `desc_len` alone was enough
        # while the description was only ever measured; the owner now needs the
        # text itself, so it travels with the record.
        "_description": desc,
        "reporter_name": ((f.get("reporter") or {}).get("displayName") or ""),
        "assignee_name": ((f.get("assignee") or {}).get("displayName") or ""),
        "resolution_name": ((f.get("resolution") or {}).get("name") or ""),
        "client_raw": raw_client,
        "client": R.normalise_client(raw_client),
        "is_internal": raw_client in R.INTERNAL_CLIENTS,
        "is_defect": (f.get("issuetype") or {}).get("name") in R.DEFECT_TYPES,
        "is_distinct": (f.get("status") or {}).get("name") not in R.NON_DISTINCT_STATUSES,
        "severity": field_value(f, "customfield_10190"),
        # --- the build axis (`D42`)
        "affected_milestone": R.as_list(am_raw),
        "affected_builds": am_infam,
        "affected_other_line": am_other,
        "affected_build": affected_build,
        "affected_hf": R.hf_number(affected_build) if affected_build else None,
        # --- the three regression-signal fields the owner named
        "reopen_from_customer": R.clean_value(field_value(f, "customfield_10780")),
        "func_working_prev": R.clean_value(field_value(f, "customfield_11253")),
        "prev_working_version": R.clean_value(field_value(f, "customfield_11254")),
        "regression_class": R.regression_class(
            field_value(f, "customfield_11253"),
            field_value(f, "customfield_11254"),
            field_value(f, "customfield_10780")),
        "hosting_env": field_value(f, "customfield_11220"),
        # --- RCA: Jira's own root-cause taxonomy, 80.7% populated (`OBJ-029` #9)
        "rca": R.clean_field(f, "customfield_10245"),
        "rca_family": R.rca_family(R.clean_field(f, "customfield_10245")),
        "rca_class": R.rca_class(R.clean_field(f, "customfield_10245")),
        "rca_details": adf_text(f.get("customfield_10567")) or None,
        "fixed_date": (R.clean_field(f, "customfield_10249") or "")[:10] or None,
        "reopen_rca": R.clean_field(f, "customfield_10741"),
        "reopen_rca_details": adf_text(f.get("customfield_10600")) or None,
        "reopen_original_id": R.clean_field(f, "customfield_10781"),
        "reopen_date": (R.clean_field(f, "customfield_10236") or "")[:10] or None,
        "reopen_time_spent": R.clean_field(f, "customfield_10235"),
        "rca_reviewed": R.clean_field(f, "customfield_11353"),
        "rca_review_remarks": adf_text(f.get("customfield_11355")) or None,
        "category": primary,
        "category_tags": tags,
        "category_source": source,
        # Second, independent axis: which *kind of testing* would have caught it.
        # Matched on title + description because a testing area is often only
        # visible in the reproduction steps ("after Windows patching", "bulk of
        # 5000"), unlike the category, which the title states directly.
        "areas": R.testing_areas(f"{title} {desc[:1500]}"),
        "env_config": R.is_env_config(f"{title} {desc[:600]}"),
        "builds_in_title": R.extract_builds(summary),
        "parent": (f.get("parent") or {}).get("key"),
        "links": links,
        "recurrence_links": [k for t, _, k in links if t in RECURRENCE_LINKS],
        "signature": sorted(R.signature(title)),
        "desc_len": len(desc),
    }


# ------------------------------------------------------------------------ grouping

def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class Union:
    def __init__(self, keys):
        self.p = {k: k for k in keys}

    def find(self, k):
        while self.p[k] != k:
            self.p[k] = self.p[self.p[k]]
            k = self.p[k]
        return k

    def join(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def group_tickets(recs: list[dict], tight: float = 0.50,
                  assisted: float = 0.30) -> tuple[list[list[dict]], dict]:
    """Group tickets that are the *same* issue reported more than once.

    Three joining rules, recorded per group so a reader can see why tickets were
    merged:
      1. an explicit clone/duplicate link between two in-scope tickets;
      2. title-signature Jaccard >= `tight`;
      3. same category **and** same component **and** Jaccard >= `assisted` —
         a lower bar, but only when two independent axes already agree.

    Zero of the 82 client tickets share an exact summary, so exact matching finds
    nothing and similarity is the only route.
    """
    by_key = {r["key"]: r for r in recs}
    u = Union(by_key)
    why: dict[tuple[str, str], str] = {}

    for r in recs:
        for other in r["recurrence_links"]:
            if other in by_key:
                u.join(r["key"], other)
                why[tuple(sorted((r["key"], other)))] = "explicit clone/duplicate link"

    keys = list(by_key)
    for i, ka in enumerate(keys):
        ra = by_key[ka]
        sa = set(ra["signature"])
        for kb in keys[i + 1:]:
            rb = by_key[kb]
            sc = jaccard(sa, set(rb["signature"]))
            if sc >= tight:
                u.join(ka, kb)
                why.setdefault(tuple(sorted((ka, kb))), f"title similarity {sc:.2f}")
            elif (sc >= assisted and ra["category"] == rb["category"]
                  and ra["component"] == rb["component"] and ra["component"] != "«none»"):
                u.join(ka, kb)
                why.setdefault(tuple(sorted((ka, kb))),
                               f"same category+component, similarity {sc:.2f}")

    buckets: dict[str, list[dict]] = collections.defaultdict(list)
    for r in recs:
        buckets[u.find(r["key"])].append(r)
    groups = sorted(buckets.values(), key=lambda g: (-len(g), g[0]["key"]))
    return groups, why


def classify(members: list[dict], ctx_evidence: list[str]) -> list[str]:
    """Apply the owner's requested classification vocabulary to one cluster.

    ⚠️ **A clone edge is not by itself proof that a defect recurred.** The working
    practice in this project is to clone a client ticket into each hotfix that
    carries the fix, so most in-scope tickets have clone ancestry by construction
    — 43 of 55 defects do. Calling all of those "recurring" would be a
    fabrication. The vocabulary therefore separates three different things:

      * `repeated in scope`   — 2+ independent tickets inside the window. The
                                strongest claim, and the rarest.
      * `cross-release lineage` — the clone family carries fix versions from 2+
                                hotfixes, so the defect was in flight across
                                releases rather than fixed once.
      * `clone-tracked`       — ancestry exists but resolves to one release. This
                                is workflow, not evidence of recurrence.
    """
    n = len(members)
    clients = {m["client"] for m in members}
    comps = {c for m in members for c in (m["components"] or ["«none»"])}
    rels = {m["release"] for m in members}
    family = {v for m in members for v in m.get("family_hf", [])}
    tags = []

    if n >= 2:
        tags.append("repeated in scope")
    elif len(family) >= 2:
        tags.append("cross-release lineage")
    elif ctx_evidence:
        tags.append("clone-tracked")
    else:
        tags.append("one-time")

    if len(comps) >= 2:
        tags.append("cross-module")
    if len(clients) >= 2:
        tags.append("cross-client")
    tags.append("cross-release" if len(rels) >= 2 else f"release-specific ({next(iter(rels))})")
    if any(m["env_config"] for m in members):
        tags.append("config/environment-sensitive")
    if n >= 3 and len(clients) >= 3:
        tags.append("potentially systematic")
    if any(m["reopen_from_customer"] == "Yes" for m in members):
        tags.append("client-reopened")

    # "Insufficient evidence" means the *finding* cannot be supported, not that a
    # title was terse. Two independent tickets that agree are evidence even when
    # both titles are two words long — the DBeaver pair is exactly that case, and
    # an earlier version of this rule labelled the strongest finding in the set
    # "insufficient evidence" because its titles were short.
    thin = sum(1 for m in members if len(m["signature"]) < 3 or m["component"] == "«none»")
    if n == 1 and thin == n and not ctx_evidence and len(family) < 2:
        tags.append("insufficient evidence")
    return tags


def escape_analysis(recs: list[dict]) -> list[dict]:
    """Where a title records the build the client found the issue on, measure the gap."""
    out = []
    for r in recs:
        found = [b for b in r["builds_in_title"] if "HF" in b]
        if not found:
            continue
        target = r["release"]                      # HF12 / HF13
        tnum = int(target[2:]) if target.startswith("HF") else None
        best = None
        for b in found:
            m = re.match(r"(\d{2}\.\d{1,2}\.\d{1,2}) HF(\d{1,2})", b)
            if not m:
                continue
            base, hf = m.group(1), int(m.group(2))
            if base == "35.8.29" and tnum and hf < tnum:
                gap = tnum - hf
            elif base != "35.8.29":
                gap = None                          # different base line
            else:
                continue
            if best is None or (gap is not None and (best["gap"] is None or gap > best["gap"])):
                best = {"found_build": b, "gap": gap}
        if best:
            out.append({"key": r["key"], "client": r["client"], "component": r["component"],
                        "category": r["category"], "fix_release": target,
                        "found_build": best["found_build"], "hotfixes_late": best["gap"],
                        "title": r["title"][:80]})
    return sorted(out, key=lambda x: (x["hotfixes_late"] is None, -(x["hotfixes_late"] or 0)))


def escape_analysis_am(recs: list[dict]) -> list[dict]:
    """Escape latency from the **fields**, not from title text — `D42`.

    ⛔ This supersedes `escape_analysis()` as the reported census. That function
    recovers the found-on build from build tokens the reporter happened to type
    into the title, which fired on **9** tickets. `Affected Milestone` records the
    same fact as a structured field on 97% of the population.

    ⚠️ The escape figure moves with the denominator, so state which one:
      * all client tickets carrying both fields  — 580 tickets, **439 escaped**
      * distinct client *defects* only (`D38`)   — **what this function returns**
    This function takes the second, narrower basis: `Bug`/`Security Fix`/
    `Client-Support`/`Performance` with `Duplicate`/`Rejected` held out, matching
    every other defect figure in the report. Quoting 439 beside a defect-based
    percentage would mix the two denominators.

    The title-derived version is retained as an independent cross-check: where
    both fire they agree (`PAMIT-41274`, found HF1 / fixed HF12, +11 on both).
    """
    out = []
    for r in recs:
        found_hf = r.get("affected_hf")
        found = r.get("affected_build")
        if found_hf is None or not found:
            continue
        fixed = sorted(
            (n for v in r["fix_versions"] if v.startswith(R.BUILD_PREFIX)
             and (n := R.hf_number(v)) is not None))
        if not fixed:
            continue
        gap = fixed[0] - found_hf
        out.append({
            "key": r["key"], "client": r["client"], "component": r["component"],
            "category": r["category"], "priority": r["priority"],
            "found_build": found, "fixed_build": f"HF{fixed[0]}" if fixed[0] else "base",
            "hotfixes_late": gap,
            "escaped": gap > 0,
            "regression_class": r["regression_class"],
            "title": r["title"][:80],
        })
    return sorted(out, key=lambda x: -x["hotfixes_late"])


def analyse_rca(recs: list[dict]) -> dict:
    """Jira's own root-cause taxonomy as an analysis axis (`OBJ-029` #9).

    ⛔ This is the field the report previously declared absent. §13 said
    "`Root Cause` ... 0 / 376 ... Jira holds no categorisation to cross-check
    [the derived taxonomy] against", having measured `cf 10113` (0.2%) and
    `cf 10199` (0.1%) — never `cf 10245`, which is **80.7% populated** with 33
    values in 15 families.

    Two things it makes possible that were previously impossible:
      * **A cross-check on the derived category axis.** The report's own taxonomy
        is inferred from ticket text; this one is authored by the product team.
        Where they disagree, that is a finding about the derivation.
      * **Separating non-defects from defects on Jira's own say-so.** 315 tickets
        are classified Enhancement / Information Request / Working as expected /
        Not a bug. A testing weak spot attributed to those is a false finding.
        ⚠️ Reported, never silently applied — the defect population stays keyed
        on issue type (`D38`), because changing a denominator on a field that is
        19% empty would be a worse error than the one it fixes.
    """
    stated = [r for r in recs if r.get("rca")]
    return {
        "population": len(recs),
        "stated": len(stated),
        "stated_pct": pct(len(stated), len(recs)),
        "unstated": len(recs) - len(stated),
        "by_value": tally(stated, lambda r: r["rca"]),
        "by_family": tally(stated, lambda r: r["rca_family"]),
        "by_class": tally(recs, lambda r: r["rca_class"]),
        "non_defect": [r for r in stated if r["rca_class"] == "non-defect"],
        "testing_failure": [r for r in stated if r["rca_class"] == "testing-failure"],
        "by_module": tally(stated, lambda r: r["components"] or ["«none»"]),
        # The cross-check: derived category against authored RCA family.
        "derived_vs_rca": tally(
            [r for r in stated if r["category"] != "Uncategorised"],
            lambda r: f"{r['rca_family']} ← {r['category'][:34]}"),
        "uncat_but_rca": sum(1 for r in stated if r["category"] == "Uncategorised"),
        "reopen_rca": tally([r for r in recs if r.get("reopen_rca")],
                            lambda r: r["reopen_rca"]),
        "reopen_dated": sum(1 for r in recs if r.get("reopen_date")),
        "reopen_hours": sum(float(r["reopen_time_spent"]) for r in recs
                            if r.get("reopen_time_spent")),
        "fixed_dated": sum(1 for r in recs if r.get("fixed_date")),
        "records": stated,
    }


def analyse_regression(recs: list[dict]) -> dict:
    """The three owner-named fields as a regression view.

    ⛔ Quoted over the **populated subset**, never the whole population — the
    fields sit at ~25% coverage, so a rate over everything would read ~75%
    "not a regression" when the truth is "not recorded". `stated` is the
    denominator every percentage here uses, and it is always reported.
    """
    stated = [r for r in recs if r["regression_class"] != "unstated"]
    conf = [r for r in stated if r["regression_class"] == "confirmed-regression"]
    by_prev = tally(conf, lambda r: r["prev_working_version"] or "«unnamed»")
    return {
        "population": len(recs),
        "stated": len(stated),
        "stated_pct": pct(len(stated), len(recs)),
        "by_class": tally(recs, lambda r: r["regression_class"]),
        "confirmed": len(conf),
        "confirmed_pct_of_stated": pct(len(conf), len(stated)),
        "reopen_yes": sum(1 for r in recs if r["reopen_from_customer"] == "Yes"),
        "reopen_stated": sum(1 for r in recs if r["reopen_from_customer"] is not None),
        "func_prev_stated": sum(1 for r in recs if r["func_working_prev"] is not None),
        "prev_ver_stated": sum(1 for r in recs if r["prev_working_version"] is not None),
        "by_prev_working_version": by_prev,
        "by_module": tally(conf, lambda r: r["components"] or ["«none»"]),
        "by_category": tally(conf, lambda r: r["category"]),
        "by_area": tally(conf, lambda r: r["areas"] or ["«unmapped»"]),
        "records": stated,
        "confidence": R.REGRESSION_CONFIDENCE,
    }


# ----------------------------------------------------------------------- statistics
# `pct` and `tally` live in pamit_fmt so the report module can share them without
# importing this one (which imports the report module to write its outputs).


HF_RE = re.compile(r"35\.8\.29 HF(\d+)")


def family_versions(rec: dict, ctx: dict[str, dict]) -> list[str]:
    """Hotfix versions covered by a ticket's clone family, itself included.

    A family spanning 2+ hotfixes means the same defect was carried across
    releases — the distinction between real cross-release churn and the routine
    clone-per-hotfix workflow.
    """
    fam = set(rec["fix_versions"])
    for k in rec["recurrence_links"]:
        f = (ctx.get(k) or {}).get("fields", {})
        fam.update(v["name"] for v in f.get("fixVersions") or [])
    hits = {v: m for v in fam if (m := HF_RE.search(v))}
    return sorted(hits, key=lambda v: int(hits[v].group(1)))


def analyse(pop: list[dict], ctx: dict[str, dict], versions: list[str]) -> dict:
    recs = [build_record(i) for i in pop]
    for r in recs:
        r["family_hf"] = family_versions(r, ctx)
    client = [r for r in recs if not r["is_internal"]]
    internal = [r for r in recs if r["is_internal"]]
    defects = [r for r in client if r["is_defect"] and r["is_distinct"]]
    nondefect = [r for r in client if not r["is_defect"]]
    dupes = [r for r in client if r["is_defect"] and not r["is_distinct"]]

    groups, why = group_tickets(defects)
    inscope = {r["key"] for r in recs}

    enriched = []
    for g in groups:
        ext = sorted({k for m in g for k in (m["recurrence_links"] + ([m["parent"]] if m["parent"] else []))
                      if k not in inscope})
        cls = classify(g, ext)
        enriched.append({
            "members": [m["key"] for m in g],
            "size": len(g),
            "label": max(g, key=lambda m: len(m["title"]))["title"][:110],
            "category": collections.Counter(m["category"] for m in g).most_common(1)[0][0],
            "components": sorted({c for m in g for c in (m["components"] or ["«none»"])}),
            "clients": sorted({m["client"] for m in g}),
            "releases": sorted({m["release"] for m in g}),
            "priorities": sorted({m["priority"] for m in g}),
            "external_evidence": ext,
            "external_readable": [k for k in ext if k in ctx],
            "classification": cls,
        })

    themes = []
    for cat, members in sorted(
            {c: [d for d in defects if d["category"] == c] for c in {d["category"] for d in defects}}.items(),
            key=lambda kv: -len(kv[1])):
        ext = sorted({k for m in members for k in m["recurrence_links"] if k not in inscope})
        themes.append({
            "category": cat,
            "tickets": [m["key"] for m in members],
            "count": len(members),
            "pct_defects": pct(len(members), len(defects)),
            "clients": sorted({m["client"] for m in members}),
            "components": sorted({c for m in members for c in (m["components"] or ["«none»"])}),
            "releases": collections.Counter(m["release"] for m in members),
            "showstoppers": sum(1 for m in members if m["priority"] == "ShowStopper"),
            "external_evidence": len(ext),
            "classification": classify(members, ext),
        })

    return {
        "generated": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "scope_versions": versions,
        "counts": {
            "population": len(recs), "client": len(client), "internal": len(internal),
            "defects": len(defects), "non_defects": len(nondefect),
            "duplicates_held_out": len(dupes),
            "context_tickets_read": len(ctx),
        },
        "records": recs, "client_records": client, "defects": defects,
        "nondefect": nondefect, "duplicates": dupes,
        "groups": enriched, "themes": themes, "why": {f"{a}|{b}": v for (a, b), v in why.items()},
        "escape": escape_analysis(defects),
        "context": ctx,
    }



# ==================================================== build / release-date analysis

_BUILD_KEY = re.compile(r"HF\s*(\d+)(?:\s*(?:P|Patch)\s*(\d+))?", re.I)


def build_sort_key(name: str) -> tuple[int, int]:
    """Order builds by number, never by release date.

    ⛔ `releaseDate` must not order anything here. Measured: HF13 is 2026-06-22,
    HF14 2026-07-10, HF11 2026-07-15, HF12 2026-07-31 — sorting by date would
    interleave the build line and produce a nonsense trend. The base version
    (`35.8.29`, no HF token) sorts first.
    """
    m = _BUILD_KEY.search(name)
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2) or 0))


def fetch_build_versions(j: ReadOnlyJira) -> list[dict]:
    """Version metadata for the whole build line, ordered by build number."""
    vs = j.versions(R.BUILD_PREFIX)
    out = [{"name": v["name"], "release_date": v.get("releaseDate"),
            "released": bool(v.get("released")), "archived": bool(v.get("archived"))}
           for v in vs]
    return sorted(out, key=lambda v: build_sort_key(v["name"]))


def analyse_builds(trend: list[dict], versions: list[dict]) -> list[dict]:
    """Per-build client view, with the Jira release date reported alongside.

    `trend` records are light (no description/links), which is why this table
    reports counts, dates, modules and categories but not recurrence — recurrence
    needs the link graph and is computed on the focus builds only.
    """
    # ⛔ `D42` — group by Affected Milestone (where the client FOUND it), not by
    # fix version (where the fix SHIPS). Both are kept per row so the two views
    # can be compared rather than silently swapped.
    by_build: dict[str, list[dict]] = collections.defaultdict(list)
    by_fixver: dict[str, list[dict]] = collections.defaultdict(list)
    for r in trend:
        for v in r["affected_builds"]:
            by_build[v].append(r)
        for v in r["fix_versions"]:
            if v.startswith(R.BUILD_PREFIX):
                by_fixver[v].append(r)

    rows = []
    for v in versions:
        members = by_build.get(v["name"], [])
        fixmembers = by_fixver.get(v["name"], [])
        defects = [m for m in members if m["is_defect"] and m["is_distinct"]]
        dates = sorted(m["created"] for m in members if m["created"])
        mods = tally(defects, lambda r: r["components"] or ["«none»"])
        cats = tally(defects, lambda r: r["category"])
        # Report the top *named* category. "Uncategorised" as a headline is not a
        # finding, it is a coverage gap — so it gets its own column instead of
        # occupying the one that is supposed to say what broke.
        named = collections.Counter({k: v for k, v in cats.items()
                                     if k != "Uncategorised"})
        uncat = cats.get("Uncategorised", 0)
        rows.append({
            "build": v["name"],
            "short": v["name"].replace(R.BUILD_PREFIX, "").strip() or "base",
            "release_date": v["release_date"] or "—",
            "released": v["released"],
            "is_current": v["name"] == R.CURRENT_BUILD,
            "in_focus": v["name"] in R.FOCUS_BUILDS,
            "client": len(members),
            "client_by_fixversion": len(fixmembers),
            "defects": len(defects),
            # Regression signal, over the populated subset only (`REGRESSION_CONFIDENCE`)
            "reg_stated": sum(1 for m in members if m["regression_class"] != "unstated"),
            "reg_confirmed": sum(1 for m in members
                                 if m["regression_class"] == "confirmed-regression"),
            "reg_likely": sum(1 for m in members
                              if m["regression_class"] == "likely-regression"),
            "reopen_yes": sum(1 for m in members if m["reopen_from_customer"] == "Yes"),
            "showstoppers": sum(1 for m in defects if m["priority"] == "ShowStopper"),
            "clients": len({m["client"] for m in members}),
            "first_ticket": dates[0] if dates else "—",
            "latest_ticket": dates[-1] if dates else "—",
            "top_module": mods.most_common(1)[0][0] if mods else "—",
            "top_category": named.most_common(1)[0][0] if named else "—",
            "uncategorised": uncat,
            "uncategorised_pct": pct(uncat, len(defects)),
        })
    return rows


# ============================================ current window and open/unversioned

def analyse_current(recs: list[dict], days: int, today: dt.date) -> dict:
    """The last-`days` client picture, independent of any fix version.

    This is the question the build-based query cannot answer: what are clients
    reporting *now*. A ticket here may carry a fix version, may carry none, and
    may predate the current build entirely.
    """
    cutoff = (today - dt.timedelta(days=days)).isoformat()
    win = [r for r in recs if r["created"] >= cutoff]
    defects = [r for r in win if r["is_defect"] and r["is_distinct"]]
    unversioned = [r for r in win if not r["fix_versions"]]
    open_unver = [r for r in unversioned
                  if r["status"] not in ("Closed", "Rejected", "Duplicate", "RCA Rejection")]

    # Emerging: a category whose last 7 days already match or beat the prior 23.
    recent = (today - dt.timedelta(days=7)).isoformat()
    c7 = collections.Counter(r["category"] for r in defects if r["created"] >= recent)
    cprev = collections.Counter(r["category"] for r in defects if r["created"] < recent)
    emerging = sorted(
        ({"category": k, "last7": v, "prior": cprev.get(k, 0)}
         for k, v in c7.items() if v >= max(2, cprev.get(k, 0))),
        key=lambda x: -x["last7"])

    return {
        "days": days, "cutoff": cutoff,
        "records": win, "defects": defects,
        "unversioned": unversioned, "open_unversioned": open_unver,
        "counts": {
            "tickets": len(win), "defects": len(defects),
            "unversioned": len(unversioned), "open_unversioned": len(open_unver),
            "showstoppers": sum(1 for r in win if r["priority"] == "ShowStopper"),
            "clients": len({r["client"] for r in win}),
        },
        "by_category": tally(defects, lambda r: r["category"]),
        "by_module": tally(defects, lambda r: r["components"] or ["«none»"]),
        "by_client": tally(win, lambda r: r["client"]),
        "emerging": emerging,
    }


def analyse_query_c(cur: dict) -> dict:
    """Query C — open client defects carrying no fix version.

    These are invisible to any build-based query by definition: nothing has
    scheduled them into a release yet. Treated as its own population with its own
    denominator, never merged into the build figures.
    """
    qc = [r for r in cur["open_unversioned"] if r["is_defect"] and r["is_distinct"]]
    groups, why = group_tickets(qc)
    n = len(qc)
    return {
        "records": qc, "count": n,
        "by_module": tally(qc, lambda r: r["components"] or ["«none»"]),
        "by_category": tally(qc, lambda r: r["category"]),
        "by_client": tally(qc, lambda r: r["client"]),
        "by_priority": tally(qc, lambda r: r["priority"]),
        "by_status": tally(qc, lambda r: r["status"]),
        "groups": [g for g in
                   ([{"members": [m["key"] for m in g], "size": len(g),
                      "label": max(g, key=lambda m: len(m["title"]))["title"][:96],
                      "clients": sorted({m["client"] for m in g}),
                      "components": sorted({c for m in g
                                            for c in (m["components"] or ["«none»"])}),
                      "category": collections.Counter(
                          m["category"] for m in g).most_common(1)[0][0]}
                     for g in groups]) if g["size"] > 1],
        "why": {f"{a}|{b}": v for (a, b), v in why.items()},
        "oldest": min((r["created"] for r in qc), default="—"),
        "newest": max((r["created"] for r in qc), default="—"),
    }


# =============================================== testing weak-spot / blind-spot axis

def analyse_areas(pools: dict[str, list[dict]]) -> list[dict]:
    """Testing areas across every pool, so a weak spot is visible wherever it lives.

    `pools` maps a label ("focus builds", "last 30 days", "Query C") to its
    records. An area's evidence is the union; its per-pool counts are kept so a
    reader can see whether a gap is historical, current, or both.
    """
    all_recs = {r["key"]: (label, r)
                for label, recs in pools.items() for r in recs}
    base = len(all_recs) or 1
    rows = []
    for area, _ in R.TESTING_AREAS:
        hits = [(label, r) for label, r in all_recs.values() if area in r["areas"]]
        if not hits:
            continue
        recs = [r for _, r in hits]
        per_pool = collections.Counter(label for label, _ in hits)
        gap, scenario = R.AREA_GAP.get(area, ("—", "—"))
        ss = sum(1 for r in recs if r["priority"] == "ShowStopper")
        clients = {r["client"] for r in recs}
        share = len(recs) / base
        ss_share = ss / len(recs)
        # ⚠️ Priority is relative, twice over, and both calibrations were wrong
        # once. An absolute count threshold (>=8) marked every area High. Adding
        # an absolute ShowStopper threshold (>=8) did the same, because
        # ShowStopper is *not rare* here — one area carries 45. What separates a
        # broad area from an acute one is ShowStopper **density**: Performance is
        # only 22 tickets but 55% of them are ShowStopper, and that deserves
        # attention a raw count would bury.
        rows.append({
            "area": area, "count": len(recs), "base": base,
            "share": share, "share_pct": f"{100 * share:.1f}%",
            "ss_share_pct": f"{100 * ss_share:.0f}%",
            "per_pool": dict(per_pool),
            "clients": len(clients), "client_names": sorted(clients),
            "modules": sorted({c for r in recs for c in (r["components"] or ["«none»"])}),
            "showstoppers": ss,
            "evidence": [r["key"] for r in sorted(recs, key=lambda x: x["created"])][:6],
            # ⛔ EVERY member key, not a sample. The workbook must be able to list
            # all `count` tickets behind this row, or the count is unverifiable.
            "members": [r["key"] for r in sorted(recs, key=lambda x: x["created"])],
            "gap": gap, "scenario": scenario,
            "priority": ("High" if (share >= 0.15 or (len(recs) >= 10 and ss_share >= 0.45))
                         else "Medium" if share >= 0.07 else "Low"),
            "shape": ("broad" if share >= 0.15
                      else "acute" if ss_share >= 0.45 else "narrow"),
            "confidence": ("measured" if len(recs) >= 3 and len(clients) >= 2
                           else "insufficient evidence"),
        })
    return sorted(rows, key=lambda x: (-x["count"], x["area"]))


# =========================================================== fetching, all pools

CLIENT_EXCL = ('"primary client[dropdown]" NOT IN (Internal, "Internal (ARCON)", '
               '"Internal(ARCON)", "Internal (Bulwark)", "Wipro Internal")')

#: Enough to place a ticket on a build and describe it, without the ~19 KB of ADF
#: description each full record carries. Used for the whole-build-line trend,
#: where 1,394 full records would be wasteful and slow.
LIGHT_FIELDS = ["key", "summary", "issuetype", "status", "priority", "created",
                "updated", "components", "fixVersions", "labels",
                "customfield_10112", "customfield_10780",
                R.AFFECTED_MILESTONE,   # `D42` — without this the trend cannot
                "customfield_11253",    #        group by the build axis at all
                "customfield_11254",
                # `OBJ-029` #9 — RCA is 80.7% populated and is the most
                # analytically useful field in the project. ⚠️ `rca_details`
                # (79%) is deliberately NOT here: it is free text averaging
                # ~400 chars and would add ~800 KB to a 2,010-ticket fetch for
                # no aggregate value. The full-record pools carry it.
                "customfield_10245",
                "customfield_10741",
                "customfield_10236",
                "customfield_10249"]


def fetch_trend(j: ReadOnlyJira, versions: list[dict]) -> list[dict]:
    """Every client ticket **reported against** the build line — the trend backbone.

    ⛔ `D42` — keyed on `Affected Milestone` (`cf[10092]`), not `fixVersion`.
    Measured difference on the same 20 versions: 1,384 tickets by fixVersion vs
    **2,010** by Affected Milestone, with 1,369 carrying an Affected Milestone and
    *no fix version at all* — invisible to the old query. The JQL uses `cf[10092]`
    rather than the field name because the name carries a trailing period
    (`Affected Milestone.`) that JQL will not quote cleanly.
    """
    names = ", ".join(f'"{v["name"]}"' for v in versions)
    jql = (f"project = {j.project} AND {CLIENT_EXCL} AND cf[10092] IN ({names}) "
           f"ORDER BY created ASC")
    return j.search(jql, LIGHT_FIELDS, max_pages=40,
                    progress=lambda p, b, t: print(f"    trend page {p}: +{b} -> {t}",
                                                   file=sys.stderr))


def fetch_focus(j: ReadOnlyJira, versions: list[dict]) -> list[dict]:
    """Full records for the in-flight builds — needs links and description."""
    present = [v["name"] for v in versions if v["name"] in R.FOCUS_BUILDS]
    if not present:
        return []
    names = ", ".join(f'"{n}"' for n in present)
    jql = (f"project = {j.project} AND fixVersion IN ({names}) ORDER BY created ASC")
    return j.search(jql, R.FIELDS, max_pages=20,
                    progress=lambda p, b, t: print(f"    focus page {p}: +{b} -> {t}",
                                                   file=sys.stderr))


def fetch_current(j: ReadOnlyJira, days: int) -> list[dict]:
    """Client tickets created in the last `days`, whatever their fix version.

    Deliberately unfiltered on version and status: the whole point is to see what
    the build-based query cannot.
    """
    jql = (f"project = {j.project} AND {CLIENT_EXCL} AND created >= -{days}d "
           f"ORDER BY created ASC")
    return j.search(jql, R.FIELDS, max_pages=40,
                    progress=lambda p, b, t: print(f"    current page {p}: +{b} -> {t}",
                                                   file=sys.stderr))


def context_keys(pop: list[dict]) -> set[str]:
    inscope = {i["key"] for i in pop}
    want: set[str] = set()
    for i in pop:
        f = i["fields"]
        for t, _, k in link_edges(f):
            if t in RECURRENCE_LINKS and k not in inscope:
                want.add(k)
        par = (f.get("parent") or {}).get("key")
        if par and par not in inscope:
            want.add(par)
    return want


def run_analysis(bundle: dict, today: dt.date) -> dict:
    """Assemble every view from one captured bundle."""
    versions = bundle["versions"]
    ctx = bundle["context"]

    focus = analyse(bundle["focus"], ctx, [v["name"] for v in versions
                                           if v["name"] in R.FOCUS_BUILDS])
    trend = [build_record(i) for i in bundle["trend"]]
    for r in trend:
        r["family_hf"] = []
    current_recs = [build_record(i) for i in bundle["current"]]
    for r in current_recs:
        r["family_hf"] = family_versions(r, ctx)

    builds = analyse_builds(trend, versions)
    cur = analyse_current(current_recs, R.CURRENT_WINDOW_DAYS, today)
    qc = analyse_query_c(cur)
    # `D42` — escape latency and the regression view are computed over the WHOLE
    # build line, not the focus builds: both derive from fields present on 97% /
    # 25% of the 2,010-ticket population, and restricting them to the focus builds
    # would throw away the escapes the analysis exists to find (HF12/13/14 carry
    # 3/2/1 Affected-Milestone tickets between them).
    trend_defects = [r for r in trend if r["is_defect"] and r["is_distinct"]]
    escape_am = escape_analysis_am(trend_defects)
    regression = analyse_regression(trend)
    rca = analyse_rca(trend)
    areas = analyse_areas({
        "focus builds": focus["defects"],
        "last 30 days": cur["defects"],
        "Query C": qc["records"],
    })

    return {
        "generated": bundle.get("captured") or dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "date": today.isoformat(),
        "current_build": R.CURRENT_BUILD,
        "previous_build": R.PREVIOUS_BUILD,
        "versions": versions,
        "builds": builds,
        "focus": focus,
        "current": cur,
        "query_c": qc,
        "areas": areas,
        "trend_total": len(trend),
        "trend_records": trend,
        "trend_defects_total": len(trend_defects),
        "escape_am": escape_am,
        "escape_am_escaped": sum(1 for e in escape_am if e["escaped"]),
        "regression": regression,
        "rca": rca,
        # `OBJ-029` #10 — `generated` is when the DATA was captured; `updated` is
        # when this document was last written. They differ whenever a report is
        # re-rendered from a cached capture, which is exactly when a reader needs
        # to know that the figures are older than the file.
        "updated": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


# ================================================================ snapshot + diff

def snapshot_of(A: dict) -> dict:
    """The comparable shape — what a daily diff needs, and no more."""
    F = A["focus"]
    return {
        "date": A["date"], "generated": A["generated"],
        "current_build": A["current_build"],
        "focus_counts": F["counts"],
        "current_counts": A["current"]["counts"],
        "query_c": A["query_c"]["count"],
        "builds": {b["build"]: b["client"] for b in A["builds"]},
        "tickets": {r["key"]: {"status": r["status"], "priority": r["priority"],
                               "release": r["release"], "component": r["component"],
                               "category": r["category"], "client": r["client"]}
                    for r in F["client_records"]},
        "current_tickets": {r["key"]: r["status"] for r in A["current"]["records"]},
        "areas": {a["area"]: a["count"] for a in A["areas"]},
        "themes": {t["category"]: t["count"] for t in F["themes"]},
    }


def previous_snapshot(today: str) -> dict | None:
    d = OUT_ART / "snapshots"
    if not d.is_dir():
        return None
    prior = sorted(p for p in d.glob("2*.json") if p.stem < today)
    for p in reversed(prior):
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
    return None


def diff_snapshots(cur: dict, prev: dict | None) -> dict:
    if not prev:
        return {"baseline": True}
    ct, pt = cur["tickets"], prev.get("tickets", {})
    cc, pc = cur["current_tickets"], prev.get("current_tickets", {})
    return {
        "baseline": False,
        "since": prev.get("date", "?"),
        "new_focus": sorted(ct.keys() - pt.keys()),
        "gone_focus": sorted(pt.keys() - ct.keys()),
        "status_moved": {k: (pt[k]["status"], ct[k]["status"])
                         for k in ct.keys() & pt.keys()
                         if pt[k]["status"] != ct[k]["status"]},
        "new_current": sorted(cc.keys() - pc.keys()),
        "query_c_delta": cur["query_c"] - prev.get("query_c", 0),
        "build_delta": {k: cur["builds"].get(k, 0) - prev.get("builds", {}).get(k, 0)
                        for k in cur["builds"].keys() | prev.get("builds", {}).keys()
                        if cur["builds"].get(k, 0) != prev.get("builds", {}).get(k, 0)},
        "area_delta": {k: cur["areas"].get(k, 0) - prev.get("areas", {}).get(k, 0)
                       for k in cur["areas"].keys() | prev.get("areas", {}).keys()
                       if cur["areas"].get(k, 0) != prev.get("areas", {}).get(k, 0)},
    }


# ========================================================================= output

CSV_COLUMNS = ["key", "pool", "release", "fix_versions", "issuetype", "status",
               "status_category", "priority", "client", "client_raw", "component",
               "components", "category", "category_source", "category_tags",
               "testing_areas", "classification", "env_config",
               "reopen_from_customer", "hosting_env", "severity", "created",
               "updated", "builds_in_title", "family_hf", "parent",
               "recurrence_links", "group_id", "is_defect", "is_distinct",
               "labels", "title"]


def _csv_row(r: dict, pool: str, gid: str, cls: str) -> dict:
    row = dict(r)
    row["pool"] = pool
    row["group_id"] = gid
    row["classification"] = cls
    for k in ("components", "category_tags", "labels", "builds_in_title",
              "recurrence_links", "fix_versions", "family_hf", "areas"):
        if isinstance(row.get(k), list):
            row[k] = "|".join(str(x) for x in row[k])
    row["testing_areas"] = row.pop("areas", "")
    return row


def write_outputs(A: dict, snap: dict, d: dict) -> list[Path]:
    import pamit_report as REP
    for p in (OUT_DOCS / "summary", OUT_ART / "snapshots", OUT_STATE):
        p.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    # 1. dated daily summary — never overwritten across days
    daily = OUT_DOCS / "summary" / f"summary_{A['date']}.md"
    daily.write_text(REP.render_daily(A, d), encoding="utf-8")
    written.append(daily)

    # 2. stable entry point: an index, not a second copy of the content
    prior = sorted((OUT_DOCS / "summary").glob("summary_*.md"), reverse=True)
    idx = ["# PAMIT client ticket analysis — daily summaries", "",
           f"**Latest:** [`{daily.name}`](summary/{daily.name}) · generated {A['generated']}",
           "", f"Full living analysis: [`D1-client-ticket-patterns.md`]"
               f"(D1-client-ticket-patterns.md) · data: `artifacts/client-tickets/`", "",
           "| Date | File |", "| --- | --- |"]
    idx += [f"| {p.stem.replace('summary_', '')} | [`{p.name}`](summary/{p.name}) |"
            for p in prior[:30]]
    idx += ["", f"{len(prior)} daily summar{'y' if len(prior) == 1 else 'ies'} retained. "
                "Files are never overwritten across days; a same-day re-run replaces "
                "that day's file only."]
    p = OUT_DOCS / "summary.md"
    p.write_text("\n".join(idx) + "\n", encoding="utf-8")
    written.append(p)

    # 3. the full living report
    p = OUT_DOCS / "D1-client-ticket-patterns.md"
    p.write_text(REP.render_full(A, d), encoding="utf-8")
    written.append(p)

    # 4. snapshot for tomorrow's diff
    p = OUT_ART / "snapshots" / f"{A['date']}.json"
    p.write_text(json.dumps(snap, indent=1), encoding="utf-8")
    written.append(p)

    # 5. one row per ticket, every pool, with the derived columns
    F = A["focus"]
    gid = {k: str(i) for i, g in enumerate(F["groups"], 1) for k in g["members"]}
    cls = {m: "; ".join(g["classification"]) for g in F["groups"] for m in g["members"]}
    seen: set[str] = set()
    rows = []
    for pool, recs in (("focus-build", F["client_records"]),
                       ("last-30-days", A["current"]["records"]),
                       ("query-c", A["query_c"]["records"])):
        for r in recs:
            tag = pool if r["key"] not in seen else f"{pool}(dup)"
            if r["key"] in seen:
                continue
            seen.add(r["key"])
            rows.append(_csv_row(r, tag, gid.get(r["key"], ""), cls.get(r["key"], "")))
    p = OUT_ART / "tickets.csv"
    with p.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    written.append(p)

    # 6. the weak-spot table as data
    p = OUT_ART / "testing-areas.csv"
    with p.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["area", "tickets", "clients", "modules", "showstoppers",
                    "priority", "confidence", "focus_builds", "last_30_days",
                    "query_c", "gap", "recommended_scenario", "evidence"])
        for a in A["areas"]:
            w.writerow([a["area"], a["count"], a["clients"], len(a["modules"]),
                        a["showstoppers"], a["priority"], a["confidence"],
                        a["per_pool"].get("focus builds", 0),
                        a["per_pool"].get("last 30 days", 0),
                        a["per_pool"].get("Query C", 0),
                        a["gap"], a["scenario"], " ".join(a["evidence"])])
    written.append(p)

    # 7. patterns
    p = OUT_ART / "patterns.json"
    p.write_text(json.dumps({
        "generated": A["generated"], "date": A["date"],
        "current_build": A["current_build"],
        "builds": A["builds"],
        "focus_counts": F["counts"],
        "groups": F["groups"],
        "themes": [{**t, "releases": dict(t["releases"])} for t in F["themes"]],
        "merge_reasons": F["why"],
        "escape_latency": F["escape"],
        "current": {k: (dict(v) if isinstance(v, collections.Counter) else v)
                    for k, v in A["current"].items()
                    if k not in ("records", "defects", "unversioned", "open_unversioned")},
        "query_c": {k: (dict(v) if isinstance(v, collections.Counter) else v)
                    for k, v in A["query_c"].items() if k != "records"},
        "areas": A["areas"],
    }, indent=1, default=str), encoding="utf-8")
    written.append(p)

    # 8. job state
    p = OUT_STATE / "last-run.json"
    p.write_text(json.dumps({
        "date": A["date"], "generated": A["generated"],
        "current_build": A["current_build"],
        "focus": F["counts"], "current": A["current"]["counts"],
        "query_c": A["query_c"]["count"],
        "areas_flagged": [a["area"] for a in A["areas"] if a["priority"] == "High"],
        "diff": {k: v for k, v in d.items() if k != "status_moved"},
        "outputs": [str(x.relative_to(ROOT)) for x in written],
    }, indent=1), encoding="utf-8")
    written.append(p)

    with (OUT_STATE / "analysis.log").open("a", encoding="utf-8") as fh:
        fh.write(f"{A['generated']}  build={A['current_build']}  "
                 f"focus_client={F['counts']['client']} focus_defects={F['counts']['defects']}  "
                 f"cur30={A['current']['counts']['tickets']} "
                 f"queryC={A['query_c']['count']}  "
                 f"areas_high={sum(1 for a in A['areas'] if a['priority'] == 'High')}  "
                 f"new_focus={len(d.get('new_focus', []))} "
                 f"new_cur={len(d.get('new_current', []))}\n")
    return written


# =========================================================================== main

RAW_CACHE = "_raw-latest.json"

#: Bumped whenever the capture shape changes. `--offline` refuses an older cache
#: rather than failing deep inside the analysis with a KeyError, which is what a
#: v1 cache did when the four-pool capture replaced the single-population one.
CAPTURE_FORMAT = 4   # v4: `OBJ-029` #9 — RCA + every populated regression field


def load_capture(path: Path | None = None) -> dict:
    """The newest capture, with its format checked.

    ⛔ The format check is not optional. A stale cache does not fail loudly — it
    fails deep inside the analysis with a `KeyError` on a field the older capture
    never fetched, which reads as a code defect rather than a stale file. Shared
    with `pamit_workbook.py` so there is one check, not two that can disagree.
    """
    cache = path or (OUT_ART / "snapshots" / RAW_CACHE)
    if not cache.exists():
        raise FileNotFoundError(cache)
    bundle = json.loads(cache.read_text(encoding="utf-8"))
    if bundle.get("format") != CAPTURE_FORMAT:
        raise ValueError(
            f"capture at {cache} is format {bundle.get('format', 1)}, this build "
            f"needs {CAPTURE_FORMAT} — re-run the analysis online once to refresh it")
    return bundle


def capture(j: ReadOnlyJira, days: int) -> dict:
    versions = fetch_build_versions(j)
    print(f"  build line: {len(versions)} versions under {R.BUILD_PREFIX}", file=sys.stderr)
    trend = fetch_trend(j, versions)
    focus = fetch_focus(j, versions)
    current = fetch_current(j, days)
    ctx = fetch_context(j, context_keys(focus) | context_keys(current))
    print(f"  trend {len(trend)} | focus {len(focus)} | last-{days}d {len(current)} "
          f"| context {len(ctx)} | {j.calls} HTTP calls", file=sys.stderr)
    return {"format": CAPTURE_FORMAT,
            "captured": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "versions": versions, "trend": trend, "focus": focus,
            "current": current, "context": ctx}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Client-raised PAMIT ticket analysis: builds, current window, "
                    "open/unversioned defects and testing blind spots. Read-only.")
    ap.add_argument("--days", type=int, default=R.CURRENT_WINDOW_DAYS,
                    help=f"current-window size (default {R.CURRENT_WINDOW_DAYS})")
    ap.add_argument("--no-write", action="store_true", help="analyse and print only")
    ap.add_argument("--no-workbook", action="store_true",
                    help="skip the Excel refresh (the report is still written)")
    ap.add_argument("--offline", action="store_true",
                    help="reuse the last capture; issues zero HTTP")
    ap.add_argument("--json", action="store_true", help="machine-readable to stdout")
    args = ap.parse_args()

    cache = OUT_ART / "snapshots" / RAW_CACHE
    if args.offline:
        try:
            bundle = load_capture()
        except FileNotFoundError:
            print(f"no capture at {cache} — run online once first", file=sys.stderr)
            return 2
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 2
        print(f"offline: capture of {bundle['captured']}", file=sys.stderr)
    else:
        j = ReadOnlyJira()
        print(f"read-only Jira as {j.whoami()} | project {j.project}", file=sys.stderr)
        bundle = capture(j, args.days)
        if not args.no_write:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps(bundle), encoding="utf-8")

    A = run_analysis(bundle, dt.date.today())
    snap = snapshot_of(A)
    d = diff_snapshots(snap, previous_snapshot(A["date"]))

    if args.json:
        print(json.dumps({"date": A["date"], "current_build": A["current_build"],
                          "focus": A["focus"]["counts"],
                          "current": A["current"]["counts"],
                          "query_c": A["query_c"]["count"],
                          "builds": {b["short"]: b["client"] for b in A["builds"]},
                          "areas": {a["area"]: a["count"] for a in A["areas"]},
                          "diff": {k: v for k, v in d.items() if k != "status_moved"}},
                         indent=1))
    else:
        F, C = A["focus"], A["current"]
        print(f"\ncurrent build {A['current_build']}  |  build line {A['trend_total']} "
              f"client tickets across {len(A['builds'])} versions")
        print(f"focus builds : client {F['counts']['client']} | defects {F['counts']['defects']}")
        print(f"last {C['days']} days  : tickets {C['counts']['tickets']} | "
              f"defects {C['counts']['defects']} | unversioned {C['counts']['unversioned']} "
              f"| open unversioned {C['counts']['open_unversioned']}")
        print(f"Query C      : {A['query_c']['count']} open unversioned client defects")
        print("\ntesting areas (top 8):")
        for a in A["areas"][:8]:
            print(f"  {a['count']:>3}  {a['priority']:<7} {a['confidence']:<22} {a['area']}")

    if args.no_write:
        print("\n--no-write: nothing written", file=sys.stderr)
        return 0

    for p in write_outputs(A, snap, d):
        print(f"  wrote {p.relative_to(ROOT)}", file=sys.stderr)

    # ---------------------------------------------------------------- #8: workbook
    # ⛔ OWNER REQUIREMENT: the master workbook is refreshed as part of the DAILY
    # run, in place, and a new .xlsx is never created (`D44`, `D45`). Building it
    # here rather than as a second scheduled task means the two can never drift
    # apart — the workbook is always the workbook for the analysis just written.
    #
    # ⚠️ A workbook failure must NOT fail the analysis. The report, the snapshot
    # and the CSVs are already on disk and are the primary deliverable; the most
    # likely failure is the file being open in Excel, which is a desk-level
    # problem, not an analysis problem. Reported loudly, exit code unchanged.
    if not args.no_workbook:
        try:
            import pamit_workbook as WB
            uni = WB.ticket_universe(A)
            problems = WB.verify(A, uni)
            out = WB.build(A, JIRA_BROWSE_BASE, WB.WORKBOOK)
            print(f"  refreshed {out.relative_to(ROOT)} "
                  f"({len(uni)} tickets, in place)", file=sys.stderr)
            if problems:
                print("  \u26d4 WORKBOOK RECONCILIATION FAILED:", file=sys.stderr)
                for q in problems:
                    print(f"     {q}", file=sys.stderr)
        except PermissionError:
            print("  \u26d4 workbook NOT refreshed: the file is locked \u2014 close it "
                  "in Excel and re-run `python tools\\jira\\pamit_workbook.py`",
                  file=sys.stderr)
        except Exception as e:                       # noqa: BLE001
            print(f"  \u26d4 workbook NOT refreshed: {type(e).__name__}: {e}",
                  file=sys.stderr)
            print("     the analysis above is written and valid; rebuild with "
                  "`python tools\\jira\\pamit_workbook.py`", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
