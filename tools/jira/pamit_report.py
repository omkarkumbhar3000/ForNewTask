#!/usr/bin/env python3
"""Report rendering for the client-raised PAMIT ticket analysis (`OBJ-028`).

Two documents from one analysis:

  * `render_daily`  — the dated daily summary. Change-first, management-facing,
                      every section capped so it stays consumable.
  * `render_full`   — the living deep report: every row, methodology, and the
                      measured data-quality limits that bound the claims.

⛔ **Denominators are never mixed.** Four populations appear here — the build
line, the focus builds, the last-30-day window and Query C — and each table
states which one it is counting. A percentage without its base is a defect in
this report, not a formatting preference.

⛔ **Detected is never presented as recommended.** Ticket counts, module splits
and clone lineage are measured. Testing gaps and scenarios are inference, and
every one carries a `confidence` of `measured` or `insufficient evidence`.
"""
from __future__ import annotations

import collections

import pamit_analysis_rules as R
from pamit_fmt import delta, pct, table, tally


# --------------------------------------------------------------------- fragments

def _release_context(A: dict) -> str:
    cur = next((b for b in A["builds"] if b["is_current"]), None)
    prev = next((b for b in A["builds"] if b["build"] == A["previous_build"]), None)
    L = [f"**Current build:** `{A['current_build']}` — owner-stated. "
         f"**Previous:** `{A['previous_build']}`.", ""]
    L.append("> ⚠️ " + R.RELEASE_DATE_CAVEAT)
    L.append("")
    rows = []
    for b in (prev, cur):
        if b:
            rows.append([f"`{b['build']}`" + (" ← current" if b["is_current"] else ""),
                         b["release_date"], "yes" if b["released"] else "**no**",
                         b["client"], b["defects"], b["first_ticket"], b["latest_ticket"]])
    L.append(table(["Build", "Jira release date", "Flagged released", "Client tickets",
                    "Defects", "First client ticket", "Latest client ticket"], rows,
                   ["---", "---", "---", "---:", "---:", "---", "---"]))
    if cur and prev:
        L.append("")
        L.append(f"The `releaseDate` values are **not** in build order "
                 f"(`{prev['build'].split()[-1]}` {prev['release_date']} vs "
                 f"`{cur['build'].split()[-1]}` {cur['release_date']}), which is why every "
                 f"table below is ordered by build number and the date is reported as "
                 f"context only.")
    return "\n".join(L)


def _build_table(A: dict, focus_only: bool = False) -> str:
    rows = []
    for b in A["builds"]:
        if focus_only and not b["in_focus"]:
            continue
        name = f"`{b['short']}`"
        if b["is_current"]:
            name += " **← current**"
        rows.append([name, b["release_date"], "✅" if b["released"] else "🟡",
                     b["client"], b["client_by_fixversion"],
                     b["defects"], b["showstoppers"], b["clients"],
                     b["reg_stated"], b["reg_confirmed"], b["reopen_yes"],
                     b["first_ticket"], b["latest_ticket"],
                     b["top_module"], b["top_category"][:28],
                     b["uncategorised_pct"]])
    out = table(["Build", "Jira release date", "Rel.", "Found (AM)", "Fixed here (same pop.)",
                 "Defects", "SS", "Clients", "Reg. stated", "Reg. confirmed",
                 "Reopen=Yes", "First ticket", "Latest ticket", "Top module",
                 "Top named category", "Uncat."], rows,
                ["---", "---", ":-:", "---:", "---:", "---:", "---:", "---:",
                 "---:", "---:", "---:", "---", "---", "---", "---", "---:"])
    note = (
        "*⛔ **`Found (AM)` is the build-wise count** — tickets whose `Affected "
        "Milestone` names this build, i.e. where the client **found** the defect "
        "(`D42`).*\n\n"
        "*⚠ **`Fixed here (same pop.)` is not the old build line.** It counts "
        "tickets **within this same Affected-Milestone population** whose fix "
        "version names this build — so the two columns describe the same 2,010 "
        "tickets from both ends, which is what makes the found-vs-fixed divergence "
        "visible per row. It is **not** the standalone `fixVersion` population the "
        "superseded methodology used: that was a different 1,384-ticket set, and "
        "its figures are in §0.1, not in this column.*\n\n"
        "*`Reg. stated` / `Reg. confirmed` / `Reopen=Yes` come from the three "
        "regression fields, which sit at ~25% population. `Reg. stated` **is** the "
        "denominator for `Reg. confirmed` — never the `Found (AM)` count.*\n\n"
        "*`Uncat.` is the share of that build's defects the derived taxonomy could "
        "not name. It is a **coverage figure, not a finding**. It runs higher on the "
        "released builds for two measured reasons: the trend query fetches light "
        "records without the description fallback, and the taxonomy was derived from "
        "current-build tickets, so older vocabulary is under-covered.*")
    return f"{out}\n\n{note}"


def _area_table(A: dict, limit: int | None = None) -> str:
    rows = []
    for a in A["areas"][:limit]:
        rows.append([a["area"], a["count"], a["share_pct"],
                     f"{a['per_pool'].get('focus builds', 0)}/"
                     f"{a['per_pool'].get('last 30 days', 0)}/"
                     f"{a['per_pool'].get('Query C', 0)}",
                     a["clients"], len(a["modules"]),
                     f"{a['showstoppers']} ({a['ss_share_pct']})", a["shape"],
                     a["gap"], f"**{a['priority']}**" if a["priority"] == "High"
                     else a["priority"],
                     "measured" if a["confidence"] == "measured"
                     else "**insufficient evidence**"])
    out = table(["Testing area", "Tickets", "Share", "Focus/30d/QC", "Clients",
                 "Modules", "ShowStopper", "Shape", "Gap identified", "Priority",
                 "Confidence"], rows,
                ["---", "---:", "---:", ":-:", "---:", "---:", "---:", ":-:", "---",
                 ":-:", "---"])
    if A["areas"]:
        out += (f"\n\n*Share is of the {A['areas'][0]['base']} distinct tickets across all "
                f"three pools. Areas are multi-label, so shares sum past 100% — a ticket "
                f"that is both a boundary and a compatibility failure is counted in both, "
                f"because both kinds of testing would have had to catch it.*")
    return out


def _module_table(recs: list[dict], base: int, groups=None, limit=None) -> str:
    t = tally(recs, lambda r: r["components"] or ["«none»"])
    rows = []
    for name, n in t.most_common(limit):
        members = [r for r in recs if name in (r["components"] or ["«none»"])]
        cats = collections.Counter(r["category"] for r in members)
        rep = len([g for g in (groups or []) if name in g["components"] and g["size"] > 1])
        rows.append([f"`{name}`", n, pct(n, base), cats.most_common(1)[0][0][:34],
                     f"{rep} group(s)" if rep else "—",
                     len({r["client"] for r in members}),
                     sum(1 for r in members if r["priority"] == "ShowStopper")])
    return table(["Module", "Tickets", "Percentage", "Major pattern",
                  "Repeat frequency", "Clients", "SS"], rows,
                 ["---", "---:", "---:", "---", "---", "---:", "---:"])


def _category_table(counter: collections.Counter, base: int, recs: list[dict],
                    limit=None) -> str:
    rows = []
    for cat, n in counter.most_common(limit):
        members = [r for r in recs if r["category"] == cat]
        rows.append([cat, n, pct(n, base),
                     len({r["client"] for r in members}),
                     len({c for r in members for c in (r["components"] or ["«none»"])}),
                     sum(1 for r in members if r["priority"] == "ShowStopper"),
                     " ".join(f"`{r['key']}`" for r in members[:3])])
    return table(["Issue category", "Count", "Percentage", "Clients", "Modules", "SS",
                  "Sample tickets"], rows,
                 ["---", "---:", "---:", "---:", "---:", "---:", "---"])


def _recurring_table(F: dict, limit=None) -> str:
    rows = []
    for g in sorted(F["groups"], key=lambda x: (-x["size"], -len(x["external_evidence"]))):
        if g["size"] < 2 and "cross-release lineage" not in g["classification"]:
            continue
        rows.append([g["label"][:58],
                     " ".join(f"`{k}`" for k in g["members"]), g["size"],
                     ", ".join(f"`{c}`" for c in g["components"][:2]),
                     ", ".join(g["clients"][:3]) + ("…" if len(g["clients"]) > 3 else ""),
                     "/".join(g["releases"]), len(g["external_evidence"]),
                     "; ".join(g["classification"])])
        if limit and len(rows) >= limit:
            break
    return table(["Pattern", "Tickets", "n", "Modules", "Clients", "Release",
                  "Older linked", "Classification"], rows,
                 ["---", "---", "---:", "---", "---", "---", "---:", "---"])


def _current_table(cur: dict, limit: int | None = 8) -> str:
    """Last-30-day view keyed by pattern, as the owner's template asks."""
    rows = []
    for cat, n in cur["by_category"].most_common(limit):
        members = [r for r in cur["defects"] if r["category"] == cat]
        dates = sorted(r["created"] for r in members)
        statuses = collections.Counter(r["status"] for r in members)
        openn = sum(1 for r in members
                    if r["status"] not in ("Closed", "Rejected", "Duplicate",
                                           "RCA Rejection"))
        unver = sum(1 for r in members if not r["fix_versions"])
        rows.append([cat, n,
                     ", ".join(sorted({c for r in members
                                       for c in (r["components"] or ["«none»"])})[:3]),
                     dates[0], dates[-1],
                     f"{openn} open / {len(members)}",
                     f"{unver} unversioned",
                     statuses.most_common(1)[0][0][:18]])
    return table(["Issue / pattern", "Count", "Modules", "First reported",
                  "Latest reported", "Current status", "Version state",
                  "Commonest state"], rows,
                 ["---", "---:", "---", "---", "---", "---", "---", "---"])


def _scenario_table(A: dict, limit=None) -> str:
    rows = []
    for a in A["areas"][:limit]:
        if a["confidence"] != "measured":
            continue
        rows.append([a["gap"][:52], a["area"],
                     " ".join(f"`{k}`" for k in a["evidence"][:3]),
                     a["scenario"],
                     f"**{a['priority']}**" if a["priority"] == "High" else a["priority"]])
    return table(["Observed client issue", "Testing area", "Evidence",
                  "Recommended scenario", "Priority"], rows,
                 ["---", "---", "---", "---", ":-:"])


def _what_changed(A: dict, d: dict) -> str:
    if d.get("baseline"):
        return ("**First run — baseline.** Every subsequent day reports movement "
                "against the previous snapshot.")
    bits = []
    if d.get("new_focus"):
        bits.append(f"**{len(d['new_focus'])} new** on the focus builds: "
                    + ", ".join(f"`{k}`" for k in d["new_focus"][:6])
                    + ("…" if len(d["new_focus"]) > 6 else ""))
    if d.get("new_current"):
        bits.append(f"**{len(d['new_current'])} new** client ticket(s) in the "
                    f"{A['current']['days']}-day window")
    if d.get("status_moved"):
        bits.append(f"**{len(d['status_moved'])} status change(s)**: " + ", ".join(
            f"`{k}` {a} → {b}" for k, (a, b) in list(d["status_moved"].items())[:5]))
    if d.get("query_c_delta"):
        bits.append(f"**Query C {d['query_c_delta']:+d}** "
                    f"(now {A['query_c']['count']} open unversioned defects)")
    if d.get("build_delta"):
        bits.append("**Build movement**: " + ", ".join(
            f"{k.replace(R.BUILD_PREFIX, '').strip() or 'base'} {v:+d}"
            for k, v in sorted(d["build_delta"].items(),
                               key=lambda kv: -abs(kv[1]))[:5]))
    if d.get("area_delta"):
        bits.append("**Testing-area movement**: " + ", ".join(
            f"{k} {v:+d}" for k, v in sorted(d["area_delta"].items(),
                                             key=lambda kv: -abs(kv[1]))[:4]))
    if not bits:
        return f"No change since {d['since']} — same populations, same statuses, same areas."
    return "\n".join(f"- {b}" for b in bits)


def _emerging(A: dict) -> str:
    em = A["current"]["emerging"]
    if not em:
        return ("No category reached the emerging threshold (2+ defects in the last 7 "
                "days, at or above the prior 23). Recorded as no signal, not as no risk.")
    rows = [[e["category"], e["last7"], e["prior"],
             "rising" if e["last7"] > e["prior"] else "sustained"] for e in em]
    return table(["Category", "Last 7 days", "Prior 23 days", "Shape"], rows,
                 ["---", "---:", "---:", "---"])


# ------------------------------------------------------------------- daily report

def render_daily(A: dict, d: dict) -> str:
    F, C, Q = A["focus"], A["current"], A["query_c"]
    fc, cc = F["counts"], C["counts"]
    L: list[str] = []
    add = L.append

    add("# PAMIT Client Ticket Analysis")
    add("")
    add("## Analysis Date")
    add("")
    add(f"**{A['date']}** · generated {A['generated']} · source Jira `PAMIT`, "
        f"**read-only** · objective `{R.OBJECTIVE}`")
    add("")
    add("## What changed since the last run")
    add("")
    add(_what_changed(A, d))
    add("")
    add("## Current Build / Release Context")
    add("")
    add(_release_context(A))
    add("")
    add("## Release-Date & Build-wise Analysis")
    add("")
    add(f"*Basis: **{A['trend_total']}** client-raised tickets across "
        f"**{len(A['builds'])}** `{R.BUILD_PREFIX}` versions. Ordered by build number.*")
    add("")
    add(_build_table(A))
    add("")
    add("## Current Client Issues — Last 30 Days")
    add("")
    add(f"*Basis: **{cc['tickets']}** client tickets created since {C['cutoff']}, "
        f"**any** fix version — this is the view the build-based query cannot give. "
        f"{cc['defects']} defects · {cc['clients']} clients · {cc['showstoppers']} "
        f"ShowStopper · **{cc['unversioned']} carry no fix version** "
        f"({cc['open_unversioned']} of those still open).*")
    add("")
    add(_current_table(C))
    add("")
    add("## Blind-Spot Analysis")
    add("")
    add(f"The build-based query sees **{fc['client']}** tickets. The 30-day window sees "
        f"**{cc['tickets']}**, of which **{cc['unversioned']}** ({pct(cc['unversioned'], cc['tickets'])}) "
        f"carry no fix version and are therefore invisible to any release-scoped query. "
        f"That gap — not the build tables — is where current client pain is least visible.")
    add("")
    add("## Open & Unversioned Client Defects")
    add("")
    add(f"### Query C — {Q['count']} open client defects with no fix version")
    add("")
    add(f"*Own denominator: **{Q['count']}**. Created {Q['oldest']} → {Q['newest']}. "
        f"Never merged into the build figures.*")
    add("")
    rows = [[f"`{m}`", n, pct(n, Q["count"]),
             Q["by_category"].most_common(1)[0][0][:30] if Q["by_category"] else "—"]
            for m, n in Q["by_module"].most_common(8)]
    add(table(["Module", "Defects", "% of Query C", "Top category overall"], rows,
              ["---", "---:", "---:", "---"]))
    add("")
    add("**By category** — " + " · ".join(
        f"{k} {v} ({pct(v, Q['count'])})" for k, v in Q["by_category"].most_common(6)))
    add("")
    add("**By priority** — " + " · ".join(
        f"{k} {v}" for k, v in Q["by_priority"].most_common()))
    add("")
    if Q["groups"]:
        add(f"**Repeat groups inside Query C ({len(Q['groups'])}):**")
        add("")
        add(table(["Pattern", "Tickets", "Clients", "Modules", "Category"],
                  [[g["label"][:54], " ".join(f"`{k}`" for k in g["members"]),
                    ", ".join(g["clients"][:3]),
                    ", ".join(f"`{c}`" for c in g["components"][:2]), g["category"]]
                   for g in sorted(Q["groups"], key=lambda x: -x["size"])[:6]],
                  ["---", "---", "---", "---", "---"]))
    else:
        add("**No multi-ticket repeat group inside Query C** — these are currently "
            "distinct reports, not one issue raised repeatedly. *Insufficient evidence* "
            "for a Query-C-specific recurring pattern.")
    add("")
    add("## Module-wise Analysis")
    add("")
    add(f"*Basis: {fc['defects']} focus-build defects. `components` is the module axis; "
        f"Jira's `Module` field is 0% populated.*")
    add("")
    add(_module_table(F["defects"], fc["defects"], F["groups"], limit=8))
    add("")
    add("## Issue Category Analysis")
    add("")
    add(_category_table(tally(F["defects"], lambda r: r["category"]),
                        fc["defects"], F["defects"], limit=8))
    add("")
    add("## Recurring Patterns")
    add("")
    add("*A clone edge alone is **not** recurrence — cloning is how a fix is carried "
        "into a hotfix here. Only 2+ in-scope tickets, or a clone family spanning 2+ "
        "hotfixes, qualifies.*")
    add("")
    add(_recurring_table(F, limit=10))
    add("")
    add("## Testing Weak Spots / Blind Spots")
    add("")
    add("*Independent of module: which **kind of testing** would have caught each "
        "ticket. Multi-label — one ticket can implicate several areas. "
        "`Focus/30d/QC` shows which population supplied the evidence.*")
    add("")
    add(_area_table(A))
    add("")
    tp = next((a for a in A["areas"] if a["area"] == "Third-Party Compatibility"), None)
    add("## Third-Party Compatibility")
    add("")
    if tp:
        add(f"**{tp['count']} tickets · {tp['clients']} clients · "
            f"{len(tp['modules'])} modules · {tp['showstoppers']} ShowStopper.** "
            f"Evidence: {' '.join(f'`{k}`' for k in tp['evidence'])}")
        add("")
        add(f"Gap: {tp['gap']}.  \nScenario: {tp['scenario']}.")
    else:
        add("No third-party-compatibility evidence in the current populations.")
    add("")
    add("## Session Recording / Logging / Integration Analysis")
    add("")
    rows = []
    for name in ("Session Recording", "Logging / Monitoring", "API / Integration",
                 "Data Integrity / Consistency"):
        a = next((x for x in A["areas"] if x["area"] == name), None)
        rows.append([name, a["count"] if a else 0, a["clients"] if a else 0,
                     a["showstoppers"] if a else 0,
                     " ".join(f"`{k}`" for k in (a["evidence"][:3] if a else [])),
                     (a["gap"] if a else "no evidence in scope")])
    add(table(["Area", "Tickets", "Clients", "SS", "Evidence", "Gap"], rows,
              ["---", "---:", "---:", "---:", "---", "---"]))
    add("")
    add("## Build / Release Trend Comparison")
    add("")
    add(_build_table(A, focus_only=True))
    add("")
    h12 = [r for r in F["defects"] if r["release"] == "HF12"]
    h13 = [r for r in F["defects"] if r["release"] == "HF13"]
    add(f"⚠️ **HF13 is the current build and still in flight.** Its lower counts "
        f"({len(h13)} defects vs HF12's {len(h12)}) are **not** a quality improvement — "
        f"tickets accumulate against a build over its life. The comparable signals are "
        f"the severity mix and which modules appear, not the volume.")
    add("")
    add("## Potential Test Case / Test Scenario Gaps")
    add("")
    add(_scenario_table(A))
    add("")
    add("## Recommended QA Actions")
    add("")
    high = [a for a in A["areas"] if a["priority"] == "High" and a["confidence"] == "measured"]
    for i, a in enumerate(high[:6], 1):
        add(f"{i}. **{a['area']}** ({a['count']} tickets, {a['clients']} clients) — "
            f"{a['scenario']}.")
    if not high:
        add("No area met the High threshold with measured confidence this run.")
    add("")
    add("## Management Summary")
    add("")
    top3 = A["areas"][:3]
    add(f"- **Current build `{A['current_build']}`** carries {len(h13)} client defects "
        f"so far; `{A['previous_build']}` carries {len(h12)}. Build number, not release "
        f"date, orders these — the dates are non-monotonic.")
    add(f"- **What clients are reporting now:** {cc['tickets']} tickets in "
        f"{C['days']} days across {cc['clients']} clients, "
        f"{cc['showstoppers']} ShowStopper.")
    add(f"- **The biggest visibility gap:** {Q['count']} open client defects have no fix "
        f"version and appear in no release report.")
    if top3:
        add("- **Where testing is weakest:** "
            + "; ".join(f"{a['area']} ({a['count']})" for a in top3) + ".")
    add(f"- **Repeating:** {sum(1 for g in F['groups'] if g['size'] > 1)} in-scope repeat "
        f"group(s); {sum(1 for g in F['groups'] if 'cross-release lineage' in g['classification'])} "
        f"defects have a clone family spanning 2+ hotfixes.")
    add("")
    add("## Newly Identified Risks / Emerging Patterns")
    add("")
    add(_emerging(A))
    add("")
    add("---")
    add("")
    add(f"Full analysis: [`../D1-client-ticket-patterns.md`](../D1-client-ticket-patterns.md) "
        f"· data: `artifacts/client-tickets/` · re-run: "
        f"`python tools\\jira\\pamit_client_analysis.py`")
    add("")
    return "\n".join(L)


# -------------------------------------------------------------------- full report

def render_full(A: dict, d: dict) -> str:
    F, C, Q = A["focus"], A["current"], A["query_c"]
    fc, cc = F["counts"], C["counts"]
    CL = F["client_records"]
    L: list[str] = []
    add = L.append

    add("# Client-raised PAMIT ticket analysis — the full picture")
    add("")
    add(f"**Generated:** {A['generated']}")
    add(f"**Updated:** {A.get('updated', A['generated'])}")
    add("")
    add(f"**Current build:** `{A['current_build']}` · **Source:** Jira `PAMIT`, "
        f"read-only · **Objective:** `{R.OBJECTIVE}` *({R.OBJECTIVE_LINEAGE})*")
    add("")
    add("> **`Generated`** is when the Jira data behind these figures was "
        "captured. **`Updated`** is when this file was last written. They differ "
        "whenever the report is re-rendered from a cached capture (`--offline`) "
        "— which is precisely when a reader needs to know that the figures are "
        "older than the file they are reading.")
    add("")
    add("> Four populations, four denominators, never mixed: the **build line** "
        f"({A['trend_total']} client tickets across {len(A['builds'])} versions), the "
        f"**focus builds** ({fc['client']} client / {fc['defects']} defects), the "
        f"**last {C['days']} days** ({cc['tickets']}), and **Query C** ({Q['count']}). "
        "Linked tickets outside a window are evidence only, never population (`D39`).")
    add("")

    add("## 0. Build-wise methodology — which Jira field, and why")
    add("")
    add("**The build axis is `Affected Milestone` (`customfield_10092`). Not "
        "`Fix versions`. Not `Milestone`.** Owner ruling `D42`.")
    add("")
    add(table(["Question", "Field", "Populated", "What it actually means"],
              [["**Where was the defect found?** ← the build-wise axis",
                "`Affected Milestone` (`cf[10092]`)", "**97.3%** (1,346/1,384)",
                "The build the **client was running** when they hit it. A build's "
                "count is therefore *the defects that escaped into it*"],
               ["Where was the fix shipped?",
                "`Fix versions` (native)", "100% of the versioned slice",
                "The release the fix **lands in**. A hotfix accumulates fixes for "
                "defects found on earlier builds, so this counts release content, "
                "not build quality"],
               ["*(no usable field)*", "the `Milestone`-named fields", "0–9%",
                "Every milestone-shaped field in this instance was measured and "
                "rejected — §0.2 has the table"]],
              ["---", "---", "---:", "---"]))
    add("")
    add("### 0.1 Why the previous methodology was wrong")
    add("")
    add("Until this revision every build-wise count keyed on `fixVersion`. That "
        "was **incorrect**, and the error changes conclusions rather than "
        "decimal places:")
    add("")
    add(table(["Measured on the same 20 versions", "By `fixVersion`",
               "By `Affected Milestone`"],
              [["Client tickets placed on the build line", "1,384", "**2,010** (+45%)"],
               ["Tickets the other field cannot see",
                "38 carry a fix version and no Affected Milestone",
                "**1,369** carry an Affected Milestone and *no fix version at "
                "all* — structurally invisible to the old query"],
               ["Heaviest build", "`base` (262)",
                "`HF6` (399) and `HF1` (388) — `base` is only 69"],
               ["The two newest released-line builds HF12 / HF13",
                "55 / 27", "**3 / 2** — almost nothing has been *reported "
                "against* them yet"]],
              ["---", "---:", "---"]))
    add("")
    add("The last row is the one that matters operationally. Under the old "
        "methodology the current build `HF13` appeared to carry **27 client "
        "tickets**; that figure was *27 fixes scheduled into HF13*, and it was "
        "being read as *27 client problems found in HF13*. The Affected-"
        "Milestone count for HF13 is **2**.")
    add("")
    add("*The `fixVersion` figures in the table above are quoted from the "
        "superseded revision of this report, which enumerated that basis "
        "directly. They are **not** the `Fixed here (same pop.)` column in §2 — "
        "that column re-counts the Affected-Milestone population by fix version "
        "and is a different, smaller set by construction.*")
    add("")
    add("The root cause is recorded so it cannot be repeated. The previous "
        "revision checked the **native** `affectedVersion` field, measured it at "
        "0% project-wide, and concluded that no field records the build a client "
        "was on — then recovered the fact from build tokens clients had typed "
        "into ticket titles. PAMIT does record it, in a custom field, on 97% of "
        "the population. §7 is the cost of that miss: **9** escaped defects "
        "found by the title heuristic against **" + str(A["escape_am_escaped"]) +
        "** measured from the field.")
    add("")
    add("### 0.2 The `Milestone` fields — all of them, measured")
    add("")
    add("⚠ **Three fields in this Jira instance are named `Affected "
        "Milestone`-something and two of them are empty on PAMIT.** Selecting one "
        "of those returns an empty build line, which reads as a clean result "
        "rather than as a wrong query — so the whole set is recorded here.")
    add("")
    add(table(["Field", "Name as shown in Jira", "On the PAMIT client population",
               "Verdict"],
              [["`customfield_10092`", "`Affected Milestone.` *(trailing period)*",
                "**1,346 / 1,384 — 97.3%**", "✅ **the axis**"],
               ["`customfield_10214`", "`Affected Milestone`", "0 / 1,384",
                "⛔ not on the PAMIT screen"],
               ["`customfield_10219`", "`Affected Milestone`", "0 / 1,384",
                "⛔ not on the PAMIT screen"],
               ["`customfield_10143` · `customfield_10174`",
                "`Custom Affected Milestone (**Only use if …)`", "0 / 1,384",
                "⛔ free-text escape hatch, unused"],
               ["`versions`", "`Affects versions` *(native)*", "0 / 1,384",
                "⛔ unused project-wide — **this is the field the old analysis "
                "checked**"],
               ["`customfield_10100`", "`Release Milestone.`", "9%",
                "⛔ legacy — values are unrelated old lines (`35.8.13 HF 7`, "
                "`4.8.5.0_U16SP2_B35.8.21`), all singletons"],
               ["`customfield_10238`", "`Forward Merge Milestone`", "63%",
                "⛔ **344 of 388 values are the literal string `None`** — no signal"],
               ["`customfield_10131` · `10221` · `10223`",
                "`Release Milestone` · `PAM_Release Milestone` · "
                "`CI_Release_Milestone`", "0%", "⛔ unused"]],
              ["---", "---", "---:", "---"]))
    add("")
    add("**Conclusion on `Milestone`: PAMIT has no usable `Milestone` axis.** The "
        "only two build fields carrying data are `Affected Milestone` (found) and "
        "`Fix versions` (fixed). Every build-wise count in this report keys on "
        "the first; the second appears only as the second axis of escape latency.")
    add("")
    add("### 0.3 Multi-value and out-of-family handling")
    add("")
    add("`Affected Milestone` is a multiselect. Measured on the 2,010-ticket "
        "population: **1,955** tickets carry one value, **49** carry two, **6** "
        "carry three or more, and **41** carry a value from a different build "
        "line alongside an in-family one. Three rules, applied consistently:")
    add("")
    add("- **A ticket is attributed to the *earliest* in-family build it names.** "
        "A defect reported against both HF5 and HF9 escaped from HF5. Crediting "
        "HF9 would blame the later build for an inherited defect and understate "
        "the escape gap.")
    add("- **Out-of-family values are reported, never silently dropped.** A "
        "ticket affecting `35.8.28` and `35.8.29 HF6` sits on the HF6 row, and "
        "its other value travels with it into the workbook.")
    add("- **Per-build counts sum above the ticket total** where one ticket names "
        "two in-family builds. The de-duplicated ticket total is the population "
        "figure, and it is the one quoted as the denominator.")
    add("")

    add("## 1. Release-date context")
    add("")
    add(_release_context(A))
    add("")

    add("## 2. The whole build line")
    add("")
    add(_build_table(A))
    add("")
    empty = [b for b in A["builds"] if b["in_focus"] and b["client"] == 0]
    if empty:
        add("**Reported deliberately:** "
            + ", ".join(f"`{b['short']}`" for b in empty)
            + " currently carries **zero** client tickets. An empty release is "
              "information; omitting the row would hide it.")
        add("")

    add("## 3. Focus builds — overall summary")
    add("")
    add(table(["Metric", "Count", "Percentage", "Observation"],
              [["Tickets on focus builds, all clients", fc["population"], "—", ""],
               ["**Client-raised**", f"**{fc['client']}**", "100% (base)",
                "`Primary Client` is 100% populated; no ticket is lost to an empty field"],
               ["Internal", fc["internal"], pct(fc["internal"], fc["population"]), "Excluded"],
               ["**Client-raised defects**", f"**{fc['defects']}**",
                pct(fc["defects"], fc["client"]), "The defect denominator (`D38`)"],
               ["Non-defects", fc["non_defects"], pct(fc["non_defects"], fc["client"]),
                "Story / Task / Sub-task"],
               ["`Duplicate`, held out", fc["duplicates_held_out"],
                pct(fc["duplicates_held_out"], fc["client"]), "Same defect counted twice"],
               ["In a multi-ticket repeat group",
                sum(g["size"] for g in F["groups"] if g["size"] > 1),
                pct(sum(g["size"] for g in F["groups"] if g["size"] > 1), fc["defects"]),
                f"{sum(1 for g in F['groups'] if g['size'] > 1)} group(s)"],
               ["Cross-release lineage",
                sum(1 for g in F["groups"] if "cross-release lineage" in g["classification"]),
                pct(sum(1 for g in F["groups"] if "cross-release lineage" in g["classification"]),
                    fc["defects"]), "Clone family spans 2+ hotfixes"],
               ["Clone-tracked only",
                sum(1 for g in F["groups"] if "clone-tracked" in g["classification"]),
                pct(sum(1 for g in F["groups"] if "clone-tracked" in g["classification"]),
                    fc["defects"]), "Workflow, **not** recurrence"],
               ["One-time", sum(1 for g in F["groups"] if "one-time" in g["classification"]),
                pct(sum(1 for g in F["groups"] if "one-time" in g["classification"]),
                    fc["defects"]), "No lineage, single report"],
               ["Context tickets read outside the windows", fc["context_tickets_read"],
                "—", "Evidence only"]],
              ["---", "---:", "---:", "---"]))
    add("")

    add("## 4. Module-wise — every module")
    add("")
    add(_module_table(F["defects"], fc["defects"], F["groups"]))
    add("")

    add("## 5. Issue category — every category")
    add("")
    add(_category_table(tally(F["defects"], lambda r: r["category"]),
                        fc["defects"], F["defects"]))
    add("")

    add("## 6. Recurring patterns — every qualifying group")
    add("")
    add(_recurring_table(F))
    add("")

    EA = A["escape_am"]
    if EA:
        esc = [e for e in EA if e["escaped"]]
        same = [e for e in EA if e["hotfixes_late"] == 0]
        neg = [e for e in EA if e["hotfixes_late"] < 0]
        add("## 7. Escape latency — found-on build vs fixed-in build")
        add("")
        add("### 7.1 The census")
        add("")
        add("*`Affected Milestone` says which build the client was running; "
            "`fixVersion` says which build the fix shipped in. The gap is how many "
            "hotfixes the defect survived undetected. Both are fields, so this is a "
            "**census over the tickets carrying both**, not a sample.*")
        add("")
        add(table(["Measure", "Tickets", "Note"],
                  [["Carry an in-family `Affected Milestone` **and** an in-family "
                    "`fixVersion`", f"**{len(EA)}**",
                    "the population this section can measure"],
                   ["**Escaped** — fixed in a *later* hotfix than reported against",
                    f"**{len(esc)}**", "the finding"],
                   ["Reported and fixed in the same hotfix", f"{len(same)}",
                    "caught within the release — no escape"],
                   ["Fix version *earlier* than the affected build", f"{len(neg)}",
                    "data anomaly, not an escape — listed in the workbook for "
                    "correction"]],
                  ["---", "---:", "---"]))
        add("")
        add("⛔ **The previous revision reported 9 rows here.** It recovered the "
            "found-on build from build tokens clients had typed into ticket titles, "
            "which fired on 9 tickets and was labelled *\"a floor, not a census\"*. "
            "The field gives " + str(len(esc)) + " — " +
            (f"{len(esc) / 9:.0f}x" if len(esc) else "0x") + " the sample. Where "
            "both methods fire they agree (`PAMIT-41274`: found HF1, fixed HF12, "
            "+11 on each), so the heuristic was accurate and simply blind.")
        add("")
        gap = collections.Counter(e["hotfixes_late"] for e in EA if e["hotfixes_late"] >= 0)
        add("**Hotfix-gap distribution** — how many releases each defect survived:")
        add("")
        add(table(["Hotfixes late", "Defects", "Reading"],
                  [[("**0** (same release)" if g == 0 else f"**+{g}**"), n,
                    ("caught before shipping onward" if g == 0
                     else "one release missed" if g == 1
                     else f"survived {g} releases undetected")]
                   for g, n in sorted(gap.items())],
                  ["---:", "---:", "---"]))
        add("")
        add("**Worst escapes** — every row is traceable in the workbook "
            "`Escape Latency` sheet:")
        add("")
        add(table(["Ticket", "Client", "Module", "Category", "Priority",
                   "Found on", "Fixed in", "Late", "Regression signal", "Title"],
                  [[f"`{e['key']}`", e["client"], f"`{e['component']}`",
                    e["category"][:24], e["priority"], e["found_build"],
                    e["fixed_build"], f"+{e['hotfixes_late']}",
                    e["regression_class"], e["title"][:48]]
                   for e in esc[:25]],
                  ["---", "---", "---", "---", "---", "---", "---", "---:",
                   "---", "---"]))
        add("")
        if len(esc) > 25:
            add(f"*25 of {len(esc)} shown. All {len(esc)} are in the workbook — "
                "§15 states the traceability rule.*")
            add("")

    RG = A["regression"]
    add("### 7.2 Regression signal — the three client-facing fields")
    add("")
    add("*The owner asked for `Is reopen from customer`, `Functionality working in "
        "previous version` and `Previous working version` to be brought into the "
        "analysis. All three exist; all three are select fields. The first was "
        "already captured but never used in a view, the other two are new here.*")
    add("")
    add(table(["Field", "ID", "Populated on the build line", "What it means",
               "How it is used"],
              [["`Is reopen from customer`", "`customfield_10780`",
                f"{RG['reopen_stated']} / {RG['population']}",
                "The customer re-opened the ticket after a delivered fix. A `Yes` "
                "is a **failed fix**, not a new defect",
                "Escalates the weak spot that produced it; already used as a "
                "`client-reopened` tag on recurring groups"],
               ["`Functionality working in previous version`", "`customfield_11253`",
                f"{RG['func_prev_stated']} / {RG['population']}",
                "`Yes` = the feature worked before, so the defect is a "
                "**regression**. `No` = pre-existing or never worked",
                "The regression gate. `Yes` promotes a ticket into the "
                "regression population"],
               ["`Previous working version`", "`customfield_11254`",
                f"{RG['prev_ver_stated']} / {RG['population']} *(naming a real "
                f"version)*",
                "The last build where it worked. Bounds the breakage to the "
                "interval `(previous working, affected milestone]`",
                "Turns a regression into a **bisect range** — the actionable "
                "form for a developer"]],
              ["---", "---", "---:", "---", "---"]))
    add("")
    add("⛔ **" + RG["confidence"] + "**")
    add("")
    add("⚠ **`Previous working version` is a select field whose option list "
        "includes the literal string `None`.** That is a real value meaning *there "
        "is no previously working version* — not an empty field. 491 tickets "
        "carry something, of which **130 carry `None`**, so the figure above "
        "counts the 361 that name an actual version. Counting `None` as populated "
        "overstates coverage; treating it as a version corrupts every bisect "
        "range, because `None` has no position in the build order.")
    add("")
    add(table(["Regression class", "Tickets", "Share of *stated*", "Meaning"],
              [[f"`{k}`", n, pct(n, RG["stated"]) if k != "unstated" else "—",
                R.REGRESSION_CLASSES.get(k, "")]
               for k, n in RG["by_class"].most_common()],
              ["---", "---:", "---:", "---"]))
    add("")
    add(f"**{RG['stated']} of {RG['population']} tickets ({RG['stated_pct']}) state "
        f"a regression signal at all**, and of those "
        f"**{RG['confirmed']} ({RG['confirmed_pct_of_stated']} of stated)** are "
        "confirmed regressions with a named previous working version. "
        f"**{RG['reopen_yes']}** tickets are customer re-opens.")
    add("")
    if RG["by_prev_working_version"]:
        add("**Where confirmed regressions were last working** — the build that "
            "broke is the one *after* this:")
        add("")
        add(table(["Previous working version", "Confirmed regressions"],
                  [[f"`{k}`", n] for k, n
                   in RG["by_prev_working_version"].most_common(12)],
                  ["---", "---:"]))
        add("")
    if RG["by_area"]:
        add("**Confirmed regressions by testing area** — a regression is a "
            "*coverage* failure by definition: the feature worked, so a test that "
            "existed and ran would have caught it.")
        add("")
        add("⚠ **`«unmapped»` is the largest row and that is a "
            "measurement limit, not a finding.** The build line is fetched with "
            "light records to keep 2,010 tickets affordable, so it carries no "
            "`description` — and the testing-area axis matches on title **plus** "
            "description. On the build line it therefore runs on the title alone "
            "and maps fewer tickets. The area figures to quote are the ones in "
            "§11, which are computed over the three full-record pools. Read this "
            "table as *the relative shape of confirmed regressions*, not as area "
            "counts comparable with §11.")
        add("")
        add(table(["Testing area", "Confirmed regressions"],
                  [[k, n] for k, n in RG["by_area"].most_common(12)],
                  ["---", "---:"]))
        add("")
    RC = A["rca"]
    add("### 7.3 Root cause — Jira's own taxonomy, 81% populated")
    add("")
    add("⛔ **This report previously stated that Jira held no root-cause "
        "categorisation. That was wrong, and wrong in the same way §0.1 was.** "
        "§13 read *\"`Root Cause` … 0 / 376 … Jira holds no categorisation to "
        "cross-check it against\"* — having measured `customfield_10113` "
        "(*Root Cause*, 0.2%) and `customfield_10199` (*Root cause*, 0.1%). "
        "Neither is the live field. **`customfield_10245` (*RCA*) is "
        f"{RC['stated_pct']} populated** — {RC['stated']} of {RC['population']} "
        f"tickets — with a structured taxonomy of {len(RC['by_value'])} values in "
        f"{len(RC['by_family'])} families. It is the most populated analytical "
        "field in the project and it had never been used.")
    add("")
    add("**By family:**")
    add("")
    add(table(["RCA family", "Tickets", "Share of stated", "Reading"],
              [[k, n, pct(n, RC["stated"]),
                ("product code" if k == "Code"
                 else "environment / deployment, not the product binary"
                 if k.startswith("Environment")
                 else "**not a defect** — enhancement or information request"
                 if k == "Requests"
                 else "**analysis / design / coverage failure**" if k == "Analysis"
                 else "closed without a product change" if k == "Others"
                 else "documentation, not code" if k == "Documentation" else "")]
               for k, n in RC["by_family"].most_common()],
              ["---", "---:", "---:", "---"]))
    add("")
    add("**Every RCA value:**")
    add("")
    add(table(["RCA", "Tickets", "Class"],
              [[k, n, R.rca_class(k)] for k, n in RC["by_value"].most_common()],
              ["---", "---:", ":-:"]))
    add("")
    add("Two consequences worth acting on:")
    add("")
    add(f"- ⛔ **{len(RC['non_defect'])} tickets are classified by the product team "
        "as *not a product defect*** — `Requests - Enhancement`, `Requests - "
        "Information Request`, `Requests - APEM Tool`, `Requests - Script "
        "Request`, `Others - Working as expected`, `Not a bug`, "
        "`Miscommunication`. A testing weak spot attributed to one of those is a "
        "**false finding**. ⚠ This is **reported, not silently applied**: the "
        "defect population stays keyed on issue type (`D38`), because re-cutting "
        "a denominator on a field that is 19% empty would be a worse error than "
        "the one it corrects. The workbook flags every such ticket so a reader "
        "can exclude them deliberately.")
    add(f"- ✅ **{len(RC['testing_failure'])} tickets name a testing or analysis "
        "failure as the root cause** — `Analysis - Inadequate Test Coverage`, "
        "`Insufficient Unit Test case`, `Analysis - Incomplete Requirement`, "
        "`Analysis - Inadequate Technical Design`, `Environment - Non "
        "replicated`. **This is the strongest evidence in the analysis for a "
        "testing gap**, because the product team recorded the cause — this "
        "report did not infer it.")
    add("")
    if RC["reopen_rca"]:
        add("**Why fixes failed** — `Reopen RCA`, populated on "
            f"{sum(RC['reopen_rca'].values())} tickets:")
        add("")
        add(table(["Reopen RCA", "Tickets", "Reading"],
                  [[k, n, ("the fix itself was wrong" if k == "Code Fix"
                           else "an upstream component broke it"
                           if k == "Dependency failure"
                           else "environment, not the fix" if k == "Hosting Issue"
                           else "**a QA misunderstanding, not a product failure**"
                           if k == "Tester Understanding" else "")]
                   for k, n in RC["reopen_rca"].most_common()],
                  ["---", "---:", "---"]))
        add("")
        add(f"`ReOpen Date` is set on **{RC['reopen_dated']}** tickets, and "
            f"`ReOpen Time Spent` totals **{RC['reopen_hours']:.0f} hours** of "
            "recorded rework across this population.")
        add("")
    add(f"⚠ **{RC['uncat_but_rca']} tickets carry an RCA while the derived "
        "category axis could not name them.** Those are the clearest targets for "
        "improving the derived taxonomy, because an authored answer already "
        "exists to check against.")
    add("")

    add("### 7.4 Regression facts Jira cannot supply")
    add("")
    add("⛔ **Owner requirement: where a regression field or fact is not available "
        "in Jira, say so explicitly rather than leaving it ambiguous or inferring "
        f"it.** The sentinel used throughout this report and the workbook is "
        f"**`{R.NOT_IN_JIRA}`**. It is never replaced by a blank cell, a dash, or "
        "a derived guess.")
    add("")
    add(table(["Question", "Why it cannot be answered", "Consequence"],
              [[q, w, c] for q, w, c in R.REGRESSION_NOT_AVAILABLE],
              ["---", "---", "---"]))
    add("")
    add("Fields that **exist in the Jira schema but are never populated**, so any "
        "value derived from them would be invented:")
    add("")
    add(table(["Field", "ID", "Populated", "Verdict"],
              [[nm, f"`{fid}`", f"{n} ({pc}%)", role]
               for fid, nm, n, pc, avail, role in R.REGRESSION_AUDIT if not avail],
              ["---", "---", "---:", "---"]))
    add("")
    add("**Every regression-shaped field measured, in population order:**")
    add("")
    add(table(["Field", "ID", "Populated", "Available", "Role"],
              [[nm, f"`{fid}`", f"{n} ({pc}%)", "✅" if avail else "⛔", role]
               for fid, nm, n, pc, avail, role in R.REGRESSION_AUDIT],
              ["---", "---", "---:", ":-:", "---"]))
    add("")

    add("⚠ **These fields do not change any count in §§2–12.** They "
        "classify tickets already in the population; they never add or remove "
        "one. Nothing in the build-wise, module, category or weak-spot analysis "
        "needed restating because of them — the restatement in this revision "
        "comes entirely from the `fixVersion` → `Affected Milestone` axis change "
        "(§0.1).")
    add("")

    add("## 8. Client concentration")
    add("")
    rows = []
    for name, n in tally(CL, lambda r: r["client"]).most_common(15):
        mem = [r for r in CL if r["client"] == name]
        rows.append([name, n, pct(n, len(CL)), sum(1 for r in mem if r["is_defect"]),
                     len({c for r in mem for c in (r["components"] or ["«none»"])}),
                     collections.Counter(r["category"] for r in mem).most_common(1)[0][0][:30]])
    add(table(["Client", "Tickets", "% of client base", "of which defects",
               "Modules touched", "Dominant category"], rows,
              ["---", "---:", "---:", "---:", "---:", "---"]))
    add("")

    add(f"## 9. Last {C['days']} days — the current client picture")
    add("")
    add(f"*Basis: {cc['tickets']} client tickets created since {C['cutoff']}, any fix "
        f"version, any status.*")
    add("")
    add(_current_table(C, limit=None))
    add("")
    add("**Module split (30-day defects):**")
    add("")
    add(_module_table(C["defects"], cc["defects"], limit=10))
    add("")

    add(f"## 10. Query C — {Q['count']} open client defects with no fix version")
    add("")
    add("*These are structurally invisible to any release-scoped query: nothing has "
        "scheduled them into a build. Own denominator throughout.*")
    add("")
    add(table(["Cut", "Breakdown"],
              [["By module", " · ".join(f"`{k}` {v}" for k, v in Q["by_module"].most_common(10))],
               ["By category", " · ".join(f"{k} {v}" for k, v in Q["by_category"].most_common(8))],
               ["By priority", " · ".join(f"{k} {v}" for k, v in Q["by_priority"].most_common())],
               ["By status", " · ".join(f"{k} {v}" for k, v in Q["by_status"].most_common(8))],
               ["By client", " · ".join(f"{k} {v}" for k, v in Q["by_client"].most_common(8))],
               ["Created span", f"{Q['oldest']} → {Q['newest']}"]],
              ["---", "---"]))
    add("")

    add("## 11. Testing weak spots — every area")
    add("")
    add(_area_table(A))
    add("")

    add("## 12. Test scenario gaps")
    add("")
    add(_scenario_table(A))
    add("")

    add("## 13. Data-quality limitations")
    add("")
    add("*Each measured, not assumed. These bound what the analysis can claim.*")
    add("")
    recs = F["records"]
    pop = len(recs) or 1
    add(table(["Limitation", "Measured", "Consequence"],
              [               ["⛔ **`Root Cause` — THIS ROW WAS WRONG.** `Module`, `Category`, "
                "`Sub-Category` and `Product/Operational categorization` are "
                "genuinely unpopulated, but **`RCA` (`cf 10245`) is 80.7% "
                "populated** with a 33-value taxonomy",
                "0 for `cf 10113`/`10199` · **1,622 for `cf 10245`**",
                "The previous wording — *\"the whole taxonomy is derived from "
                "ticket text; Jira holds no categorisation to cross-check it "
                "against\"* — measured two decoy fields and missed the live one. "
                "Jira **does** hold an authored root-cause classification, and "
                "§7.3 now uses it. The derived text taxonomy remains, with a "
                "cross-check it never had"],
               ["**`affectedVersion` (native) unused — but `Affected Milestone` "
                "(`cf[10092]`) is not**", "0 native / **97.3%** custom",
                "⛔ **This row previously read \"no field records the build a "
                "client was on\" and was wrong.** The native field is empty; the "
                "custom field carries the fact on 97.3% of the population and is "
                "now the build axis (`D42`, §0)"],
               ["`Severity` sparsely populated",
                f"{sum(1 for r in recs if r['severity'])} / {pop}",
                "`priority` (100%) is used for impact; severity-based views unavailable"],
               ["`environment` and `resolution` never set", f"0 / {pop}",
                "Environment classification leans on `Hosting Environment` "
                f"({sum(1 for r in recs if r['hosting_env'])}/{pop}) and title text"],
               ["`Primary Client` holds alias duplicates", "—",
                "ICICI splits across two values (21 + 4); TCL Global and ITD-MC likewise. "
                "Merged by rule — unmerged, 'most affected client' is wrong"],
               ["Clone-driven workflow displaces dates", "—",
                "Most focus-build summaries begin with `CLONE`, so `created` is when the "
                "clone was cut for the hotfix, not when the client reported. This is why "
                "the 30-day view exists as a separate population"],
               ["Jira `releaseDate` is planned, and non-monotonic", "—",
                "HF13 2026-06-22 < HF14 2026-07-10 < HF11 2026-07-15 < HF12 2026-07-31, "
                "and no in-flight build is flagged released. Ordering uses build number"],
               ["`/search/approximate-count` is inaccurate", "190 vs 201",
                "A 5.5% undercount on this population. Every figure here comes from full "
                "enumeration"],
               ["`All Modules` used as a component",
                f"{sum(1 for r in recs if 'All Modules' in (r['components'] or []))} / {pop}",
                "A non-answer for module attribution; those tickets cannot be assigned"],
               ["Fix-version scope is a small slice of client reporting", "19,296 unversioned",
                "Client tickets with no fix version, all time. Build-based analysis covers "
                "**fix-scheduled** defects, not everything clients report"]],
              ["---", "---:", "---"]))
    add("")

    add("## 14. How this was produced")
    add("")
    add("Read-only Jira enumeration through `tools/jira/jira_query.ReadOnlyJira`, which "
        "permits GET on a fixed path list plus POST to the two search endpoints and "
        "refuses everything else — 16 guard assertions cover it, including `GET "
        "/transitions`. Classification rules, client aliases and the testing-area axis "
        "are in `tools/jira/pamit_analysis_rules.py`; grouping is union-find over "
        "explicit clone links plus word-boundary title-signature similarity. Rendering "
        "is `tools/jira/pamit_report.py`.")
    add("")
    add("```powershell")
    add("python tools\\jira\\pamit_client_analysis.py            # fetch, analyse, write")
    add("python tools\\jira\\pamit_client_analysis.py --no-write # analyse only")
    add("python tools\\jira\\pamit_client_analysis.py --offline  # zero HTTP, last capture")
    add("python tools\\jira\\pamit_workbook.py                   # build the workbook")
    add("python tools\\jira\\pamit_workbook.py --refetch         # re-query Jira first")
    add("```")
    add("")

    add("## 15. Ticket-level traceability \u2014 no count without its tickets")
    add("")
    add("**Owner ruling `D43`: every reported count must be traceable to the "
        "individual tickets behind it.** A total, a percentage and a summary are "
        "not an answer on their own \u2014 if the analysis says *Environment "
        "Compatibility: " + str(next((a["count"] for a in A["areas"]
                                      if a["area"] == "Environment Compatibility"),
                                     0)) +
        " tickets*, all " + str(next((a["count"] for a in A["areas"]
                                      if a["area"] == "Environment Compatibility"),
                                     0)) + " keys must be listed.")
    add("")
    add("How that is enforced rather than promised:")
    add("")
    add(table(["Mechanism", "Where", "What it guarantees"],
              [["**Sheet `04 Ticket Details`**", "the workbook",
                "One row per ticket in the union of every counted pool, with each "
                "pool and each testing area as a Yes/No column. **Filtering that "
                "sheet reproduces any reported figure exactly** \u2014 the count is a "
                "view over the data, not a separate assertion"],
               ["**Sheet `09 Count Reconciliation`**", "the workbook",
                "Every headline count restated as a live `COUNTIFS` over sheet 04, "
                "beside the value this analysis computed, beside a `PASS`/`FAIL` "
                "comparison. **Excel recomputes it on open**, so the reader "
                "verifies the totals without trusting the generator"],
               ["**`verify()` gate**", "`tools/jira/pamit_workbook.py`",
                "Reconciles every pool count and every area count against the "
                "ticket universe *before* the workbook is declared good, and exits "
                "non-zero on any mismatch. A figure that cannot be reproduced from "
                "its tickets fails the build instead of shipping"],
               ["**`members` on every area row**", "`pamit_client_analysis.py`",
                "Each testing area carries **every** backing key, not a sample of "
                "six. The sample is still shown in \u00a712 for readability; the full "
                "list is in the workbook"]],
              ["---", "---", "---"]))
    add("")
    add("\u26a0 **Two places where counts legitimately do not add up, and why.** "
        "Both are stated wherever the figure appears:")
    add("")
    add("- **Per-build counts sum above the ticket total.** `Affected Milestone` is "
        "a multiselect and 55 tickets name two in-family builds. The "
        "de-duplicated ticket total is the population; the per-build sum is not.")
    add("- **Testing-area counts sum past 100%.** The area axis is multi-label \u2014 "
        "a defect that is both a boundary failure and a compatibility failure is a "
        "gap in both kinds of testing, so it is counted in both. Sheet 01 "
        "therefore has more rows than distinct tickets, and both figures are "
        "reported.")
    add("")

    add("## 16. The consolidated workbook")
    add("")
    add("**Owner ruling `D44`: one workbook, many worksheets.** All ticket-level "
        "detail lands in a single file and a new analysis area becomes a **new "
        "worksheet in it**, never a new `.xlsx`.")
    add("")
    add("`artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx`")
    add("")
    add(table(["Sheet", "Holds", "How its counts are verified"],
              [["`00 README`", "Methodology, headline totals, sheet manifest, the "
                "rules the workbook obeys", "\u2014"],
               ["`01 Testing Weak Spots`", "**One row per ticket per weak spot** "
                "with the full 20-column JIRA-oriented structure: ticket, gap, "
                "description, module, build, severity, priority, impact, root "
                "cause, existing and missing coverage, precaution, solution, "
                "PAM-specific recommendation, suggested coverage, automation, "
                "evidence, JIRA link, status",
                "Filter by *Testing Weak Spot* \u2192 row count equals the reported "
                "area count"],
               ["`02 Weak Spot Summary`", "One row per testing area with the same "
                "recommendation columns aggregated",
                "*Tickets* column reconciles against sheet 01 and sheet 09"],
               ["`03 Test Scenario Gaps`", "One row per gap with expected "
                "behaviour, existing and missing coverage, risk, **source of "
                "identification** and **derivation method**",
                "*Related Ticket Number(s)* lists every backing key"],
               ["`04 Ticket Details`", "**The source data** \u2014 every ticket, every "
                "analysis field, every pool and area flag",
                "Every other sheet's count is a filter over this one"],
               ["`05 Build-wise`", "Per build: found-count beside fixed-count, "
                "defects, ShowStoppers, regression signal",
                "*Found here* reconciles via `COUNTIF` on sheet 04"],
               ["`06 Escape Latency`", "Every ticket whose affected build precedes "
                "its fix build", "One row per ticket; the gap is measured, not "
                "estimated"],
               ["`07 Regression Signal`", "The three client-facing fields per "
                "ticket, the derived class, and the bisect range",
                "One row per ticket stating any signal"],
               ["`08 Module & Category`", "Module-wise and category-wise counts",
                "Both reconcile via `COUNTIF` on sheet 04"],
               ["`09 Count Reconciliation`", "**Every headline count beside a live "
                "`COUNTIFS` and a `PASS`/`FAIL`**", "This sheet *is* the validation"],
               ["`10 Field Audit`", "Every milestone-shaped and regression-shaped "
                "field measured, with population and verdict",
                "Explains why `cf[10092]` is the axis and the rest are not"]],
              ["---", "---", "---"]))
    add("")
    add("\u26d4 **Do not create a second file for a new analysis.** Add a "
        "`sheet_*` builder to `build()` in `tools/jira/pamit_workbook.py` and a "
        "matching row to the manifest in `sheet_readme()`, and the analysis "
        "becomes a worksheet here. \u26a0 Those two are hand-kept in step \u2014 add the "
        "builder and forget the manifest row and sheet `00 README` will describe "
        "a workbook that is not the one on disk.")
    add("")

    add("## 17. Methodology for the two derived axes")
    add("")
    add("### 17.1 Testing weak spots")
    add("")
    add("A weak spot is **derived, not authored**. Four ordered steps:")
    add("")
    add("1. Every client ticket in the three full-record pools is matched against "
        "the testing-area axis in `pamit_analysis_rules.testing_areas()` \u2014 a "
        "**word-boundary** term match over title plus the first 1,500 characters "
        "of description, multi-label.")
    add("2. An area qualifies at **\u22653 tickets from \u22652 distinct clients** "
        "(`confidence = measured`). One client's tickets are an incident, not a "
        "coverage gap. Areas below the threshold are reported as *insufficient "
        "evidence* rather than dropped.")
    add("3. Priority is **density-based, not volume-based**: High at \u226515% share, "
        "or \u226510 tickets with \u226545% ShowStopper. An absolute-count rule marked "
        "every area High, because ShowStopper is not rare in this data.")
    add("4. The gap statement and recommended scenario come from `AREA_GAP`; the "
        "root cause, existing and missing coverage, precaution, PAM-specific "
        "recommendation, suggested coverage and automation advice come from "
        "`AREA_DETAIL`. Both are keyed on the area, so a filtered view of sheet 01 "
        "is self-contained.")
    add("")
    add("\u26d4 **Word boundaries are load-bearing.** Substring matching tagged "
        "*\"Login with SAML\"* as a **Logging** issue (`log` \u2282 `login`); the "
        "word-boundary fix then silently dropped plurals (`cipher` misses "
        "*ciphers*). Both are fixed and both are the kind of defect that produces "
        "a confident wrong answer.")
    add("")
    add("### 17.2 Test scenario gaps \u2014 and where each one came from")
    add("")
    add("Every gap names its **source of identification**, because a gap whose "
        "provenance cannot be traced is an opinion:")
    add("")
    add(table(["Source of identification", "Used?", "Detail"],
              [["**Client-raised JIRA tickets** (production / customer issues)",
                "\u2705 **primary**",
                "The population itself, placed on builds by `Affected Milestone`. "
                "Every gap row carries its backing keys and the client count"],
               ["**Previous build/version behaviour**", "\u2705 secondary",
                "The three regression fields, where populated. A confirmed "
                "regression is the strongest possible evidence of a coverage gap: "
                "the feature demonstrably worked before"],
               ["**Existing automation coverage**", "\u2705 tertiary",
                "The bootstrap suite inventory \u2014 specifically the gap between what "
                "the framework *can* do (20 environment files, five browser "
                "targets, a k6 harness) and what it is actually *run* with"],
               ["**Defect recurrence**", "\u2705 supporting",
                "Union-find grouping over clone links plus title-signature "
                "similarity. \u26d4 A clone edge alone is **not** recurrence here: "
                "cloning is how a fix is carried into a hotfix, so only families "
                "spanning 2+ hotfixes count"],
               ["Requirements · user stories · functional specifications",
                "\u26d4 **not used**",
                "PAMIT holds no requirement links, and the product documentation is "
                "confirmed not up to date (70% of endpoints undocumented). A gap "
                "claiming a requirements source would be unfounded, so none does"],
               ["Existing manual test cases", "\u26d4 not used as a denominator",
                "The available manual corpus is 63 cases covering Login and "
                "Dashboard only. Absence there proves nothing about coverage, so it "
                "is not treated as evidence either way"]],
              ["---", ":-:", "---"]))
    add("")

    add("## 18. The daily process")
    add("")
    add("**Owner ruling `D45`: the master workbook is refreshed as part of the "
        "daily run, in place. A second `.xlsx` is never created.**")
    add("")
    add("The scheduled task **`PAM-Client-Ticket-Analysis`** runs at **09:00 "
        "daily** and now performs all four steps in one process:")
    add("")
    add(table(["Step", "What happens", "Output"],
              [["1", "Read-only Jira enumeration of all four populations",
                "`artifacts/client-tickets/snapshots/_raw-latest.json`"],
               ["2", "Analyse — build line on `Affected Milestone`, escape "
                "latency, regression signal, RCA, testing areas",
                "in memory"],
               ["3", "Write the report and the dated summary",
                "**this file** (`Updated` timestamp moves) · "
                "`summary/summary_<date>.md` · `<date>.json` · the CSVs"],
               ["4", "**Refresh the master workbook in place**",
                "`artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx`"]],
              [":-:", "---", "---"]))
    add("")
    add("⚠️ **Step 4 lives inside the analysis script, not in a second scheduled "
        "task.** That is deliberate: two tasks could run at different times and "
        "leave the workbook describing yesterday's analysis while the report "
        "described today's. One process cannot drift from itself.")
    add("")
    add("⚠️ **A workbook failure never fails the analysis.** The report, the "
        "snapshot and the CSVs are written first and are the primary "
        "deliverable. The likeliest failure is the file being open in Excel — a "
        "desk-level problem, not an analysis problem — so it is reported loudly "
        "and the exit code is unchanged. Rebuild with "
        "`python tools\\jira\\pamit_workbook.py`.")
    add("")
    add("### 18.1 History across daily refreshes")
    add("")
    add("The workbook is **overwritten** each day, so history cannot live in its "
        "sheets. It lives where it cannot be lost:")
    add("")
    add(table(["What", "Where", "Retention"],
              [["Per-day headline counts and full ticket state",
                "`artifacts/client-tickets/snapshots/<date>.json`",
                "**Never deleted.** The history's source of truth"],
               ["Per-day narrative summary",
                "`docs/analysis/summary/summary_<date>.md`",
                "Never overwritten across days; a same-day re-run replaces only "
                "that day's file"],
               ["Day-over-day deltas, read at a glance",
                "workbook sheet `12 Daily History`",
                "**Derived** from the snapshots on every refresh"],
               ["What changed since the last run",
                "§*What changed* in the dated summary",
                "Computed against the previous snapshot"]],
              ["---", "---", "---"]))
    add("")
    add("⛔ **Sheet 12 is derived, not appended.** An appended sheet would be "
        "lost the first time the workbook was rebuilt from scratch, and could "
        "silently disagree with the snapshots. A break in its date sequence "
        "means the job did not run that day — the gap is shown rather than "
        "smoothed over.")
    add("")
    add("### 18.2 `" + R.NOT_IN_JIRA + "`")
    add("")
    add("**Owner ruling: never leave an unavailable fact ambiguous, and never "
        "infer one without labelling it.** The sentinel is used in three "
        "distinct situations, all of which a blank cell would have flattened "
        "into one:")
    add("")
    add(table(["Situation", "Example", "Where it shows"],
              [["The field does not exist in PAMIT",
                "regression-test-executed, requirement link, detected-by",
                "§7.4 and workbook sheet `10 Field Audit`"],
               ["The field exists but is **never** populated",
                "`Phase` (`cf 10164`) · `ReopenCount` (`cf 11018`) · `Module` · "
                "`Category`",
                "an explicit workbook column reading the sentinel all the way "
                "down — a *missing* column would read as 'not analysed'"],
               ["The field is populated in general but empty on **this ticket**",
                "`RCA` on 486 of 2,169 · `Previous working version` on 1,744",
                "that ticket's cell on sheet `04 Ticket Details`"]],
              ["---", "---", "---"]))
    add("")
    add("⛔ **Nothing in this report infers a value for an unavailable field.** "
        "The clearest case is defect-injection phase: the RCA family looks like "
        "an answer (`Code - *`, `Analysis - *`, `Environment - *`) and is not "
        "one — `Code - Logic Issue` records where the defect was **found in "
        "code**, not the phase in which it was **introduced**. Mapping one to "
        "the other would produce a phase-containment metric that reads as "
        "measured and would drive real test-strategy decisions. `Phase` is 0% "
        "populated, so the honest answer is the sentinel.")
    add("")
    return "\n".join(L)
