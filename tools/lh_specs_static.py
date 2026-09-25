#!/usr/bin/env python3
"""Catalogue, static-analysis and incident loophole specs: LH-06, 07, 08, 10.

These are not selected from run responses. LH-06 and LH-07 come from the endpoint
catalogue and the payload helpers; LH-10 from the .NET product source; LH-08 from a
recorded incident that must never be reproduced.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from lh_common import (                                                  # noqa: F401
    API_BASE, ENVIRONMENT, HERE, MD, REPO, ROOT, LoopholeSpec, Xlsx,
    esc, header_block, reproduce_footer, revalidation_section,
)

SOURCE_MAP = HERE / "source-map.json"
_sm_cache = None


def source_map() -> dict:
    global _sm_cache
    if _sm_cache is None:
        _sm_cache = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
    return _sm_cache


def _row(controller, action, verb, path, **kw):
    """Static findings still need the shape base_row() would have produced."""
    base = {"flow": "", "flow_title": "", "hop": None, "controller": controller,
            "action": action, "verb": verb, "path": path, "url": API_BASE + path,
            "http_status": None, "latency_ms": None, "body_bytes": None,
            "content_type": None, "request_body": None, "l1": None, "l3": None,
            "l4": None, "evidence_file": None, "response": None}
    base.update(kw)
    return base


# ═══════════════════════════════════════════════════════════ LH-06
MUTATING_PREFIX = re.compile(
    r"^(set|insert|add|create|update|save|edit|modify|assign|import|upload|generate|"
    r"approve|reject|map|unmap)", re.I)
DESTRUCTIVE_PREFIX = re.compile(r"^(delete|remove|drop|purge|revoke|disable)", re.I)


def _lh06_rows():
    rows = []
    for key, e in source_map().items():
        if e.get("verb") != "GET":
            continue
        if not MUTATING_PREFIX.match(e["action"]):
            continue
        rows.append(_row(e["controller"], e["action"], "GET", e["path"],
                         role=e.get("role")))
    return rows


def _lh06_classify(r):
    return f"{r['action']} over GET"


def _lh06_verbstats():
    sm = source_map()
    verbs = Counter(e.get("verb") for e in sm.values())
    delete_named = [e for e in sm.values() if DESTRUCTIVE_PREFIX.match(e["action"])]
    return verbs, delete_named


def _lh06_narrative(payload, md):
    rows = payload["rows"]
    spec = LH06
    verbs, delete_named = _lh06_verbstats()
    total = sum(verbs.values())
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p("Actions that change server state are declared over **HTTP GET**. GET is defined "
         "as safe and idempotent; anything in the path between client and server is "
         "entitled to treat it that way.")
    md.table(["Measure", "Value"], [
        ["Endpoints in the catalogue", f"{total:,}"],
        ["Declared GET", f"{verbs.get('GET', 0)}"],
        ["…with a state-changing action name", f"**{len(rows)}**"],
        ["Distinct such actions", len({r["action"] for r in rows})],
        ["Controllers exposing them", payload["distinct_controllers"]],
    ])
    md.p(f"All {len(rows)} are the same action — **`SetStatus`** — declared as GET on "
         f"{payload['distinct_controllers']} separate controllers. A name beginning `Set` "
         "served over a safe verb is a state change hiding behind a read.")

    md.h(2, "2. Why a safe verb matters")
    md.table(["Actor", "Behaviour it is entitled to"], [
        ["Browsers and proxies", "Prefetch, cache and re-issue GETs freely"],
        ["Load balancers / CDNs", "Cache GET responses; may serve or replay them"],
        ["Crawlers and link-checkers", "Follow any GET URL they discover"],
        ["Retry logic", "Automatically retries a failed GET — safe by definition"],
        ["Browser history / back button", "Re-issues the GET"],
        ["Security scanners", "Treat GET as non-destructive and will call it"],
    ])
    md.p("Any of these can invoke `SetStatus` without user intent.")

    md.h(2, "3. The related half — deletion is not DELETE")
    md.p("The reverse problem exists too. Across the whole catalogue:")
    md.table(["Verb", "Endpoints", "Share"],
             [[f"`{v}`", n, f"{n / total * 100:.1f}%"]
              for v, n in sorted(verbs.items(), key=lambda kv: -kv[1])])
    md.p(f"**{len(delete_named)} endpoints have a destructive action name** "
         "(`Delete…`, `Remove…`, `Revoke…`, `Disable…`) yet the catalogue declares only "
         f"**{verbs.get('DELETE', 0)} DELETE** endpoints. Deletion is expressed as "
         "`POST /api/<Controller>/Delete<Thing>`.")
    md.table(["Consequence", "Detail"], [
        ["Verb-based safety guards do not work",
         "A destructive call is indistinguishable from an ordinary POST by verb alone"],
        ["Our harness guards on **action names** instead",
         "`DESTRUCTIVE` regex in `chain_runner.py` — a workaround for a contract problem"],
        ["Firewall / gateway policy cannot express intent",
         "\"Block DELETE for this role\" protects 2 endpoints out of "
         f"{len(delete_named)} destructive ones"],
    ])

    md.h(2, "4. Full register of state changes over GET")
    md.table(["#", "Controller", "Action", "Verb", "Path"],
             [[i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"], f"`{r['path']}`"]
              for i, r in enumerate(rows, 1)])

    md.h(2, "5. ⛔ Why this pack contains no live execution evidence")
    md.p("`SetStatus` **changes state**. Calling it to demonstrate that calling it changes "
         "state would be both circular and irresponsible on a shared environment. This "
         "finding is proven from the endpoint catalogue — `APIConfig.java` declares the "
         "verb, and that declaration is the defect.")
    md("> The harness withholds every action matching the mutating-name pattern from "
       "replay for this pack. That guard is enforced in code, not by convention.")
    md("")

    revalidation_section(md, payload, spec, 6)

    md.h(2, "7. Proposed fix")
    md.table(["#", "Action", "Effort"], [
        ["1", "Move `SetStatus` to POST on all "
              f"{payload['distinct_controllers']} controllers", "Medium — 49 declarations "
              "plus every caller"],
        ["2", "Audit the remaining GET surface for other state changes", "Low"],
        ["3", "Express deletion as HTTP DELETE, or accept POST and document it "
              "explicitly so gateway policy can be written", "Medium"],
        ["4", "Add a build-time check rejecting a `Set*`/`Insert*`/`Delete*` action "
              "declared as GET", "Low — prevents recurrence"],
    ])
    md.p("Item 4 is the one that stops this returning. Items 1 and 3 are the backlog it "
         "leaves behind.")
    reproduce_footer(md, spec, 8)


def _lh06_sheets(payload, xl):
    rows = payload["rows"]
    verbs, delete_named = _lh06_verbstats()
    xl.summary("LH-06 — Mutation exposed over HTTP GET", [
        ("Severity", "Medium"), ("Environment", ENVIRONMENT),
        ("Source", "APIConfig.java catalogue (1,306 endpoints)"), ("", ""),
        ("State-changing actions declared GET", len(rows)),
        ("Distinct actions", len({r["action"] for r in rows})),
        ("Controllers affected", payload["distinct_controllers"]),
        ("", ""),
        ("Catalogue GET", verbs.get("GET", 0)),
        ("Catalogue POST", verbs.get("POST", 0)),
        ("Catalogue DELETE", verbs.get("DELETE", 0)),
        ("Catalogue PUT", verbs.get("PUT", 0)),
        ("Endpoints with a destructive action name", len(delete_named)),
        ("", ""),
        ("⛔ Live execution", "Deliberately none. Calling SetStatus mutates state; the "
                             "catalogue declaration is the evidence."),
    ])
    xl.sheet("State Change Over GET",
             ["#", "Controller", "Action", "Declared verb", "Path", "Role"],
             [[i, r["controller"], r["action"], r["verb"], r["path"], r.get("role")]
              for i, r in enumerate(rows, 1)],
             [5, 30, 20, 14, 52, 12],
             note="Every catalogue endpoint whose action name denotes a state change but "
                  "is declared over GET.")
    xl.sheet("Verb Distribution", ["Verb", "Endpoints", "Share"],
             [[v, n, f"{n / sum(verbs.values()) * 100:.1f}%"]
              for v, n in sorted(verbs.items(), key=lambda kv: -kv[1])],
             [10, 12, 10])
    xl.sheet("Destructive by Name",
             ["#", "Controller", "Action", "Declared verb", "Path"],
             [[i, e["controller"], e["action"], e.get("verb"), e["path"]]
              for i, e in enumerate(sorted(delete_named,
                                           key=lambda x: (x["controller"], x["action"])), 1)],
             [5, 30, 40, 14, 56],
             note="Actions whose name is destructive. Only 2 endpoints in the entire "
                  "catalogue use the DELETE verb, so verb-based guards cannot protect "
                  "these.")


LH06 = LoopholeSpec(
    num="06", slug="mutation-over-http-get",
    title="Mutation exposed over HTTP GET",
    severity="🟠 Medium", priority="Medium", effort="Medium",
    jira_summary=("SetStatus is declared as HTTP GET on 49 controllers - state change "
                  "over a safe, cacheable, retryable verb"),
    one_liner="49 controllers expose SetStatus over GET; deletion is POST, not DELETE.",
    revalidate="partial", replay_excludes_mutating=True,
    revalidate_note="SetStatus mutates state and is never called by this harness",
    source="catalogue",
    cross_refs=["LH-08 (the same 49-controller diagnostic scaffold)"],
    rows_static=_lh06_rows, classify=_lh06_classify,
    narrative=_lh06_narrative, sheets=_lh06_sheets,
    reproduces=lambda row, res: False,
    replay_summary=lambda res: "n/a",
    TICKET={
        "labels": ["api-design", "http-semantics"],
        "what": ("SetStatus is declared as HTTP GET on 49 controllers. GET is defined "
                 "as safe and idempotent; everything between client and server is "
                 "entitled to treat it that way - browsers prefetch it, proxies and "
                 "CDNs cache it, crawlers follow it, retry logic re-issues it "
                 "automatically, and the back button replays it.\n\n"
                 "A name beginning Set served over GET is a state change hiding behind "
                 "a read."),
        "scope_rows": [("Endpoints in the catalogue", "1,306"),
                       ("Declared GET", "321"),
                       ("*…with a state-changing action name*", "*49*"),
                       ("Distinct such actions", "1 (SetStatus)"),
                       ("Controllers exposing it", "*49*"),
                       ("Catalogue DELETE endpoints", "*2*"),
                       ("Endpoints with a destructive action name", "see EVIDENCE.md §3")],
        "sections": [
            ("Actors entitled to call a GET without user intent",
             "* Browsers and proxies - prefetch, cache and re-issue freely\n"
             "* Load balancers and CDNs - cache GET responses, may serve or replay them\n"
             "* Crawlers and link-checkers - follow any GET URL they discover\n"
             "* Retry logic - automatically retries a failed GET, safe by definition\n"
             "* Browser history and the back button - re-issue the GET\n"
             "* Security scanners - treat GET as non-destructive and will call it"),
            ("The related half - deletion is not DELETE",
             "The catalogue declares only 2 DELETE endpoints against 982 POST. "
             "Deletion is expressed as POST /api/<Controller>/Delete<Thing>.\n\n"
             "Consequence: verb-based safety guards do not work on this API. A "
             "destructive call is indistinguishable from an ordinary POST by verb "
             "alone, and a gateway policy of \"block DELETE for this role\" protects "
             "almost nothing. Our own harness has to guard on action NAMES instead - a "
             "workaround for a contract problem."),
            ("Why there is no execution evidence in this ticket",
             "SetStatus changes state. Calling it to demonstrate that calling it "
             "changes state would be both circular and irresponsible on a shared "
             "environment. The finding is proven from the endpoint catalogue: "
             "APIConfig.java declares the verb, and that declaration IS the defect.\n\n"
             "The harness withholds every mutating-named action from replay for this "
             "finding; the guard is enforced in code."),
        ],
        "repro": """No live execution is required, and none should be performed - calling
SetStatus changes state.

1. Open
   Automation gitlab repo/pam_automation_bootstrap/src/test/java/
     com/arcon/autoconfigs/APIConfig.java

2. Search for SetStatus.
   Observe 49 declarations, one per controller, each with the GET verb.

3. Confirm the same in the deployed route table (a route dump would settle
   this definitively - see LH-05).

4. For the deletion half: search the same file for Delete and Remove action
   names and compare against the DELETE verb count. Destructive actions are
   declared over POST; only 2 endpoints in the whole catalogue use DELETE.

5. The full register of all 49, and of every destructively-named action, is
   in the attached EVIDENCE.xlsx.""",
        "expected": ("GET is safe and idempotent. State changes are POST (or PUT/PATCH); "
                     "deletion is DELETE, or is documented so gateway policy can be "
                     "written."),
        "actual": ("SetStatus is GET on 49 controllers, and deletion is POST throughout - "
                   "so HTTP verbs carry no reliable safety information on this API."),
        "severity_rows": [
            ["**Correctness**", "An intermediary can trigger a state change with no user "
                                "intent"],
            ["**Blast radius**", "49 controllers for SetStatus; the whole destructive "
                                 "surface for the DELETE half"],
            ["**Security tooling**", "Verb-based gateway and firewall policy cannot "
                                     "express intent on this API"],
            ["**Test safety**", "Our harness must maintain a name-based destructive-action "
                                "regex as compensation"],
            ["**Cost to fix**", "Medium - 49 declarations plus every caller; Low to add "
                                "the build-time check that prevents recurrence"],
        ],
        "severity_argument": ("Rated Medium: no confirmed incident, but it removes the "
                              "single strongest safety signal in HTTP and forces every "
                              "consumer and every safety tool to compensate."),
        "fix_rows": [
            ["1", "Move `SetStatus` to POST on all 49 controllers", "Medium",
             "Removes the primary case"],
            ["2", "Audit the remaining GET surface for other state changes", "Low",
             "Confirms nothing else is hiding"],
            ["3", "Express deletion as HTTP DELETE, or document the POST convention "
                  "explicitly so gateway policy can be written", "Medium",
             "Restores verb-based safety"],
            ["4", "Add a build-time check rejecting a `Set*`/`Insert*`/`Delete*` action "
                  "declared as GET", "Low", "Prevents recurrence - the durable fix"],
        ],
        "fix_note": ("Item 4 is what stops this returning. Items 1 and 3 are the backlog "
                     "it leaves behind and can be scheduled incrementally."),
        "acceptance": """1. No action whose name denotes a state change is declared over GET.
2. A build-time check rejects such a declaration.
3. Deletion is either expressed as HTTP DELETE or the POST convention is
   documented for gateway policy authors.""",
        "target": "0 mutating actions over GET",
    },
)


# ═══════════════════════════════════════════════════════════ LH-07
def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _lh07_groups():
    fields = defaultdict(set)          # normalised -> {spellings}
    where = defaultdict(set)           # spelling -> {endpoints}
    for key, e in source_map().items():
        for fn in (e.get("fields") or {}):
            fields[_norm(fn)].add(fn)
            where[fn].add(f"{e['controller']}/{e['action']}")
    return ({k: v for k, v in fields.items() if len(v) > 1}, where, fields)


def _lh07_rows():
    var, where, _ = _lh07_groups()
    rows = []
    for norm, spellings in sorted(var.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        for sp in sorted(spellings):
            rows.append(_row("", sp, "", "", concept=norm,
                             spellings=len(spellings),
                             variants=", ".join(sorted(spellings)),
                             endpoints=len(where[sp])))
    return rows


def _lh07_classify(r):
    n = r.get("spellings", 1)
    return f"{n} spellings"


def _lh07_narrative(payload, md):
    rows = payload["rows"]
    spec = LH07
    var, where, allfields = _lh07_groups()
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p("The same logical field is spelled differently across controllers. A client "
         "cannot bind one model to the API; it must handle every spelling, or match "
         "case-insensitively and hope.")
    md.table(["Measure", "Value"], [
        ["Distinct field names in the catalogue", f"{len(allfields):,} normalised concepts"],
        ["Total distinct spellings", sum(len(v) for v in allfields.values())],
        ["**Concepts with more than one spelling**", f"**{len(var)}**"],
        ["Worst case", f"**{max(len(v) for v in var.values())} spellings of one concept**"],
    ])

    md.h(2, "2. The worst offenders")
    md.table(["Concept", "Spellings", "Variants observed"],
             [[f"`{norm}`", len(sp), " · ".join(f"`{s}`" for s in sorted(sp))]
              for norm, sp in sorted(var.items(),
                                     key=lambda kv: (-len(kv[1]), kv[0]))[:20]])
    md.p("`serviceid` in **seven** spellings — `ServiceID`, `ServiceId`, `Service_Id`, "
         "`Serviceid`, `serviceId`, `service_id`, `serviceid` — is the clearest case. "
         "Four distinct conventions (PascalCase, camelCase, snake_case and "
         "SCREAMING fragments) coexist for one identifier.")

    md.h(2, "3. Type instability on top of naming")
    md.p("Naming is only half of it. The same field also changes **type** between "
         "operations:")
    md.table(["Field", "Observed behaviour", "Consequence"], [
        ["`ServiceId`", "string on create, integer on read",
         "A round-trip needs an explicit cast; a strongly-typed client fails"],
        ["`UserName` / `UserDisplayName`", "silently **upper-cased** on write "
                                           "(`DemoUser` → `DEMOUSER`)",
         "A client that reads back what it wrote sees different data"],
        ["`LobId`", "integer in the envelope, string in some payload helpers",
         "Chain values must be normalised before reuse"],
    ])
    md.p("The upper-casing is the most surprising: it is a **silent server-side mutation "
         "of submitted data** with nothing in the contract announcing it.")

    md.h(2, "4. What our tooling had to do about it")
    md.table(["Workaround", "Where"], [
        ["Case-insensitive field matching when extracting chain values",
         "`chain_runner.py` value extraction"],
        ["Explicit casts when carrying an id between hops",
         "`chain_runner.py` substitution"],
        ["Normalised-key grouping when building the field map",
         "`build_source_map.py`"],
    ])
    md.p("Every one of these is a workaround for a contract problem, and each one is a "
         "place a real client would have to reimplement the same compensation.")

    md.h(2, "5. Full variance register")
    md.table(["#", "Concept", "Spellings", "Variants"],
             [[i, f"`{norm}`", len(sp), " · ".join(f"`{s}`" for s in sorted(sp))]
              for i, (norm, sp) in enumerate(
                  sorted(var.items(), key=lambda kv: (-len(kv[1]), kv[0])), 1)])

    revalidation_section(md, payload, spec, 6)

    md.h(2, "7. Proposed fix")
    md.table(["#", "Action", "Effort"], [
        ["1", "Publish a canonical field-name and type register", "Low"],
        ["2", "Apply it to **new** endpoints as a build-time check — stop the divergence "
              "growing", "Low"],
        ["3", "Keep an identifier's type stable across create, read and update",
         "Medium"],
        ["4", "Document or remove the silent upper-casing of `UserName`", "Low"],
        ["5", "Converge existing spellings behind a serialiser alias so old names keep "
              "working", "High — but can be incremental"],
    ])
    md.p("Items 1 and 2 are the whole value here. Item 5 is a long tail that does not "
         "need to block them.")
    reproduce_footer(md, spec, 8)


def _lh07_sheets(payload, xl):
    var, where, allfields = _lh07_groups()
    xl.summary("LH-07 — Field naming and types inconsistent across controllers", [
        ("Severity", "Medium"), ("Environment", ENVIRONMENT),
        ("Source", "APIConfig.java + payload helpers + observed responses"), ("", ""),
        ("Normalised concepts", len(allfields)),
        ("Total distinct spellings", sum(len(v) for v in allfields.values())),
        ("Concepts with >1 spelling", len(var)),
        ("Worst case", f"{max(len(v) for v in var.values())} spellings of one concept"),
        ("", ""),
        ("Also observed", "ServiceId is a string on create and an integer on read; "
                          "UserName is silently upper-cased on write."),
    ])
    xl.sheet("Variant Groups",
             ["#", "Concept (normalised)", "Spellings", "Variants observed"],
             [[i, norm, len(sp), ", ".join(sorted(sp))]
              for i, (norm, sp) in enumerate(
                  sorted(var.items(), key=lambda kv: (-len(kv[1]), kv[0])), 1)],
             [5, 30, 11, 96])
    rows = []
    for norm, sp in sorted(var.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        for s in sorted(sp):
            rows.append([norm, s, len(where[s]),
                         ", ".join(sorted(where[s])[:8])])
    xl.sheet("Spelling Usage",
             ["Concept", "Spelling", "Endpoints using it", "Endpoints (first 8)"],
             rows, [26, 26, 16, 90],
             note="Which endpoints use which spelling. A client integrating across two "
                  "of these must handle both.")
    xl.sheet("Type Instability", ["Field", "Behaviour", "Consequence"],
             [["ServiceId", "string on create, integer on read",
               "Round-trip requires an explicit cast"],
              ["UserName / UserDisplayName", "silently upper-cased on write",
               "Read-back does not match what was written"],
              ["LobId", "integer in envelope, string in some payload helpers",
               "Chain values need normalising"]],
             [26, 46, 56])


LH07 = LoopholeSpec(
    num="07", slug="inconsistent-field-naming-and-types",
    title="Field naming and types inconsistent across controllers",
    severity="🟠 Medium", priority="Medium", effort="High",
    jira_summary=("61 field concepts have multiple spellings across the API - ServiceId "
                  "appears in 7 forms, and types change between operations"),
    one_liner="One concept, up to seven spellings; ids change type between operations.",
    revalidate="static",
    revalidate_note="derived from the catalogue and payload helpers",
    source="catalogue",
    cross_refs=["LH-03 (response shape variance)"],
    rows_static=_lh07_rows, classify=_lh07_classify,
    narrative=_lh07_narrative, sheets=_lh07_sheets,
    reproduces=lambda row, res: False, replay_summary=lambda res: "n/a",
    TICKET={
        "labels": ["api-consistency", "contract"],
        "what": ("The same logical field is spelled differently across controllers, and "
                 "the same identifier changes type between operations. A client cannot "
                 "bind one model to the API; it must handle every spelling, or match "
                 "case-insensitively and hope."),
        "occurrence_label": "Concepts with more than one spelling",
        "occurrence_value": 61,
        "hide_endpoint_counts": True,
        "scope_rows": [("Total spellings across those concepts", "147"),
                       ("Worst case", "*7 spellings of one concept*"),
                       ("Distinct field names catalogued", "951")],
        "sections": [
            ("The worst offenders",
             "|| Concept || Spellings observed ||\n"
             "| service id | ServiceID, ServiceId, Service_Id, Serviceid, serviceId, "
             "service_id, serviceid |\n"
             "| LOB id | LOBID, LOBId, LOBid, LobID, LobId |\n"
             "| server IP | ServerIP, ServerIp, serverIP, serverIp, server_ip |\n"
             "| user id | UserID, UserId, Userid, userid |\n"
             "| user name | UserName, Username, userName, username |\n"
             "| service type id | ServiceTypeID, ServiceTypeId, serviceTypeId, "
             "service_type_id |\n\n"
             "Four distinct conventions - PascalCase, camelCase, snake_case and "
             "SCREAMING fragments - coexist for a single identifier."),
            ("Type instability on top of naming",
             "|| Field || Behaviour || Consequence ||\n"
             "| ServiceId | string on create, integer on read | A round-trip needs an "
             "explicit cast; a strongly-typed client fails |\n"
             "| UserName / UserDisplayName | silently UPPER-CASED on write "
             "(DemoUser -> DEMOUSER) | A client that reads back what it wrote sees "
             "different data |\n"
             "| LobId | integer in the envelope, string in some payload helpers | Chain "
             "values must be normalised before reuse |\n\n"
             "The upper-casing is the most surprising: a silent server-side mutation of "
             "submitted data, with nothing in the contract announcing it."),
            ("What our tooling had to do about it",
             "* case-insensitive field matching when extracting chain values\n"
             "* explicit casts when carrying an id between hops\n"
             "* normalised-key grouping when building the field map\n\n"
             "Each is a workaround for a contract problem, and each is a place a real "
             "client would have to reimplement the same compensation."),
        ],
        "repro": """No live execution is required - this is established by inspection.

1. Open the payload helpers under
   Automation gitlab repo/pam_automation_bootstrap/src/test/java/
     com/arcon/utils/apiPayload/

2. Search for ServiceId, ServiceID, Service_Id and serviceId.
   All four appear, in payloads sent to different controllers.

3. For the type instability:
   a. POST /api/ServiceCreation/SetServiceDetails - ServiceId is returned as a
      STRING in the Result.
   b. POST /api/ServiceDetails/GetServiceDetails - ServiceId is returned as an
      INTEGER.

4. For the upper-casing:
   a. Create a user with UserName "DemoUser".
   b. Read the user back.
   c. Observe UserName is returned as "DEMOUSER".

5. The full variance register - all 61 concepts with every spelling and the
   endpoints using each - is in the attached EVIDENCE.xlsx.""",
        "expected": ("One canonical spelling and one stable type per concept, applied "
                     "consistently across controllers."),
        "actual": ("61 concepts have multiple spellings, up to 7 for one identifier; "
                   "ids change type between create and read; UserName is silently "
                   "upper-cased on write."),
        "severity_rows": [
            ["**Correctness**", "A strongly-typed client fails on the type change; a "
                                "read-back does not match what was written"],
            ["**Integration cost**", "Every consumer reimplements case-insensitive "
                                     "matching and explicit casts"],
            ["**Blast radius**", "61 concepts across the catalogue"],
            ["**Silent data mutation**", "Upper-casing on write is undocumented and "
                                         "unannounced"],
            ["**Cost to fix**", "High to converge fully; Low to publish a register and "
                                "stop the divergence growing"],
        ],
        "severity_argument": ("Rated Medium: individually survivable, collectively a "
                              "sustained tax on every consumer. The register and the "
                              "build-time check are cheap and stop it worsening."),
        "fix_rows": [
            ["1", "Publish a canonical field-name and type register", "Low",
             "The reference everything else depends on"],
            ["2", "Apply it to **new** endpoints as a build-time check", "Low",
             "Stops the divergence growing - highest value per unit effort"],
            ["3", "Keep an identifier's type stable across create, read and update",
             "Medium", "Removes the cast requirement"],
            ["4", "Document or remove the silent upper-casing of `UserName`", "Low",
             "Removes a surprising data mutation"],
            ["5", "Converge existing spellings behind serialiser aliases so old names "
                  "keep working", "High", "The long tail; can be incremental"],
        ],
        "fix_note": ("Items 1 and 2 carry nearly all the value. Item 5 is a long tail "
                     "that should not block them."),
        "acceptance": """1. A canonical field-name and type register is published.
2. New endpoints are checked against it at build time.
3. No identifier changes type between create, read and update.
4. Any server-side normalisation of submitted values (such as upper-casing)
   is documented in the contract.""",
        "target": "0 new variant spellings",
    },
)


# ═══════════════════════════════════════════════════════════ LH-08
CRASH_ACTIONS = ("GetLogs", "GetErrorLogs")


def _lh08_rows():
    rows = []
    for key, e in source_map().items():
        if e["action"] in CRASH_ACTIONS:
            rows.append(_row(e["controller"], e["action"], e.get("verb", "GET"),
                             e["path"], blocklisted=True))
    return rows


def _lh08_classify(r):
    return r["action"]


def _lh08_narrative(payload, md):
    rows = payload["rows"]
    spec = LH08
    byact = Counter(r["action"] for r in rows)
    header_block(md, payload, spec)

    md("> ⛔ **This finding is documentary. It is not re-validated, and must not be.** "
       "Reproducing it stops the IIS application pool and takes the environment down. "
       "The harness blocklists these endpoints permanently.")
    md("")

    md.h(2, "1. The defect")
    md.p("Two read-only GET endpoints hang for 30 seconds and **stop the IIS application "
         "pool** serving the PAM API. After that the entire API returns `503 Service "
         "Unavailable` and does not recover without intervention.")
    md.p("**Three sequential requests were enough to take down the whole API.** This was "
         "not a load test — no concurrency, one request at a time.")

    md.h(2, "2. The exact sequence, from ISSUE-010")
    md.table(["#", "Request", "HTTP", "Latency", "Outcome"], [
        ["1", "`GET /api/ActivityLogs/GetDatabaseStatus`", "200", "614 ms",
         "✅ Healthy — `Database Connected, ARCOSDB : True`"],
        ["2", "`GET /api/ActivityLogs/GetErrorLogs`", "—", "**30,020 ms**",
         "⛔ Hung, no response"],
        ["3", "`GET /api/ActivityLogs/GetLogs`", "—", "**30,170 ms**",
         "⛔ Hung, no response"],
        ["4", "`GET /api/ActivityLogs/GetSsmVideoPath`", "**503**", "82 ms",
         "⛔ Pool stopped"],
        ["5–325", "*everything else*", "**503**", "17–82 ms", "⛔ Pool stopped"],
    ])
    md.p("Request 1 proves the API and its database connection were healthy immediately "
         "before the failure. From request 4 onward the API was gone.")

    md.h(2, "3. Why this is a pool stop, not overload")
    md.table(["Observation", "What it rules out"], [
        ["503s returned in 17–82 ms",
         "Not saturation — a loaded server responds slowly, it does not refuse instantly"],
        ["503 body is an **IIS HTML page**, not an application response",
         "The request never reached application code"],
        ["Requests were strictly sequential", "Not thread- or connection-pool exhaustion"],
        ["Only 3 requests preceded the failure", "Not cumulative load"],
        ["Still 503 long after the run ended", "Not transient; no auto-recovery"],
    ])
    md.p("This is the signature of IIS **rapid-fail protection**: the worker crashed "
         "repeatedly inside the failure interval, so IIS stopped the pool.")

    md.h(2, "4. It then degraded further")
    md.table(["Time", "`:6302` (API)", "`:1302` (application + Swagger)"], [
        ["Before the run", "✅ HTTP 200", "✅ HTTP 200, Swagger served"],
        ["Calls #2–#3", "⛔ hung, 30 s each", "not probed"],
        ["Calls #4–#325", "⛔ HTTP 503 (IIS HTML)", "not probed"],
        ["Later probe", "⛔ **TCP connection refused**", "⛔ **TCP connection refused**"],
    ])
    md.p("The progression **503 → connection refused** matters: at 503 IIS was still "
         "listening; afterwards nothing was listening on either port. The impact extended "
         "beyond the API application pool to the host's web services, and past the "
         "endpoints that were actually called.")

    md.h(2, "5. Probable cause, and its limits")
    md.p("`GetLogs` and `GetErrorLogs` accept **no parameters at all** — no page, no page "
         "size, no date range, no row limit. An unparameterised log-retrieval endpoint can "
         "only mean *return everything*. Against a log table on a long-lived environment "
         "that is an unbounded query and an unbounded serialisation, which exhausts the "
         "worker.")
    md("> **What cannot be confirmed from the client side:** the implementing source is "
       "not in the developer snapshot — the `ActivityLogs` controller in `pam/PAM` "
       "implements only `InsertSSMLogs`. The developer must confirm root cause from the "
       "IIS/application event log and the worker crash dump.")
    md("")

    md.h(2, "6. ⚠️ Blast radius — this is not two endpoints")
    md.p("`GetLogs` and `GetErrorLogs` are part of a five-action diagnostic scaffold "
         "repeated across the controller set:")
    md.table(["Action", "Controllers exposing it", "Measured here"],
             [[f"`{a}`", byact.get(a, 0), f"{byact.get(a, 0)} endpoints in the catalogue"]
              for a in CRASH_ACTIONS])
    md.p(f"**{len(rows)} endpoints carry the same unbounded-query risk.** Two of them are "
         "confirmed to hang. The related actions `GetDatabaseStatus`, `GetStatus` and "
         "`SetStatus` complete the scaffold across the same ~49 controllers — see LH-06 "
         "for the `SetStatus` half.")
    md.p("If the cause is in a shared base controller, **one fix addresses all "
         f"{len(rows)}**. If each is separately implemented, {len(rows)} need fixing. "
         "That question should be answered first because it changes the plan.")

    md.h(2, "7. Full register of blocklisted endpoints")
    md.table(["#", "Controller", "Action", "Verb", "Path"],
             [[i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"], f"`{r['path']}`"]
              for i, r in enumerate(sorted(rows, key=lambda x: (x["controller"],
                                                                x["action"])), 1)])

    md.h(2, "8. Harness controls in force")
    md.table(["Control", "Detail"], [
        ["Blocklist", "`GetLogs`, `GetErrorLogs`, `GetAllActiveUserDetails` are refused "
                      "at planning time in `chain_runner.py`, `run_chains.py`, "
                      "`run_qa_mssql.py` and `lh_common.py`"],
        ["Reporting", "Reported as `EXCLUDED — blocked`, never silently skipped"],
        ["Consequence", f"These {len(rows)} endpoints are also permanently **untested**"],
        ["Removal", "Once paging is added the block comes off and they re-enter coverage "
                    "automatically"],
    ])

    revalidation_section(md, payload, spec, 9)

    md.h(2, "10. Required action")
    md.table(["#", "Action", "Owner", "Priority"], [
        ["1", "Retrieve the IIS application event log and worker crash dump for the "
              "failure window — this gives the actual exception", "Development",
         "🔴 High"],
        ["2", "Capture the SQL executed by `GetLogs`/`GetErrorLogs` and check for a "
              "missing `TOP` / `OFFSET FETCH`", "Development", "🔴 High"],
        ["3", "Add mandatory paging parameters with a server-side maximum, across all "
              f"{len(rows)} endpoints", "Development", "🔴 High"],
        ["4", "Add a server-side query timeout and row cap so no single request can "
              "exhaust a worker", "Development", "🟠 Medium"],
        ["5", "Confirm whether the diagnostic actions come from a shared base controller "
              "— determines a 1-line fix versus 98", "Development",
         "🟠 Medium — answer first"],
        ["6", "Enable IIS pool auto-recovery so a crash does not leave the API dead "
              "indefinitely", "Infrastructure", "🟠 Medium"],
    ])
    md.p("An unauthenticated-reachable endpoint that halts the application pool is a "
         "denial-of-service vector, not merely a testing obstacle. That is the reason "
         "for the Critical rating.")
    reproduce_footer(md, spec, 11)


def _lh08_sheets(payload, xl):
    rows = payload["rows"]
    byact = Counter(r["action"] for r in rows)
    xl.summary("LH-08 — Two endpoints stop the IIS application pool", [
        ("Severity", "Critical"), ("Environment", ENVIRONMENT),
        ("Source", "Incident record — docs/findings/issues/ISSUE-010"), ("", ""),
        ("Actions confirmed to hang", 2),
        ("Endpoints carrying the same risk", len(rows)),
        ("Requests needed to stop the pool", 3),
        ("Environment downtime", "Approximately one working day"),
        ("Degradation observed", "HTTP 503 -> TCP connection refused on both :6302 and :1302"),
        ("", ""),
        ("⛔ Re-validation", "FORBIDDEN. Reproducing this takes the environment down. "
                            "Endpoints are permanently blocklisted in the harness."),
        ("Consequence", f"These {len(rows)} endpoints are also permanently untested."),
    ])
    xl.sheet("Blocklisted Endpoints",
             ["#", "Controller", "Action", "Declared verb", "Path", "Status"],
             [[i, r["controller"], r["action"], r["verb"], r["path"],
               "BLOCKLISTED - never called"]
              for i, r in enumerate(sorted(rows, key=lambda x: (x["controller"],
                                                                x["action"])), 1)],
             [5, 30, 16, 14, 52, 26],
             note="Every catalogue endpoint exposing GetLogs or GetErrorLogs. Two are "
                  "confirmed to hang; all carry the same unbounded-query risk.")
    xl.sheet("Incident Timeline",
             ["#", "Request", "HTTP", "Latency", "Outcome"],
             [[1, "GET /api/ActivityLogs/GetDatabaseStatus", "200", "614 ms",
               "Healthy - Database Connected"],
              [2, "GET /api/ActivityLogs/GetErrorLogs", "none", "30,020 ms",
               "HUNG - no response"],
              [3, "GET /api/ActivityLogs/GetLogs", "none", "30,170 ms",
               "HUNG - no response"],
              [4, "GET /api/ActivityLogs/GetSsmVideoPath", "503", "82 ms",
               "Application pool stopped"],
              ["5-325", "everything else", "503", "17-82 ms",
               "Application pool stopped"],
              ["later", "TCP probe :6302 and :1302", "none", "-",
               "Connection refused - nothing listening"]],
             [8, 46, 8, 12, 40])
    xl.sheet("By Action", ["Action", "Endpoints", "Confirmed to hang"],
             [[a, byact.get(a, 0), "YES"] for a in CRASH_ACTIONS], [18, 12, 18])


LH08 = LoopholeSpec(
    num="08", slug="endpoints-stop-iis-app-pool",
    title="Two endpoints hang and stop the IIS application pool",
    severity="🔴 Critical", priority="ShowStopper", effort="Medium",
    jira_summary=("GetLogs and GetErrorLogs hang 30s and stop the IIS application pool - "
                  "3 sequential requests took QA down for a day"),
    one_liner="Three read requests stopped the API host. 98 endpoints carry the same risk.",
    revalidate="forbidden",
    revalidate_note=("reproducing it stops the IIS application pool and takes the "
                     "environment down; three requests previously caused a full day of "
                     "downtime (ISSUE-010)"),
    source="incident",
    cross_refs=["ISSUE-010 (the incident record)",
                "LH-12 (the non-fatal cases of the same unbounded-query pattern)",
                "LH-06 (the SetStatus half of the same 49-controller scaffold)"],
    rows_static=_lh08_rows, classify=_lh08_classify,
    narrative=_lh08_narrative, sheets=_lh08_sheets,
    reproduces=lambda row, res: False, replay_summary=lambda res: "n/a",
    TICKET={
        "labels": ["availability", "denial-of-service", "performance"],
        "what": ("Two read-only GET endpoints hang for 30 seconds and stop the IIS "
                 "application pool serving the PAM API. After that the entire API "
                 "returns 503 Service Unavailable and does not recover without "
                 "intervention.\n\n"
                 "*Three sequential requests were enough to take down the whole API.* "
                 "This was not a load test - no concurrency, one request at a time. "
                 "The environment was unusable for a working day."),
        "scope_rows": [("Actions confirmed to hang", "*2* (GetLogs, GetErrorLogs)"),
                       ("Endpoints carrying the same risk", "*98*"),
                       ("Requests needed to stop the pool", "*3*"),
                       ("Environment downtime", "approximately one working day"),
                       ("Degradation observed", "HTTP 503 -> TCP connection refused on "
                                                "both :6302 and :1302")],
        "sections": [
            ("The exact sequence",
             "|| # || Request || HTTP || Latency || Outcome ||\n"
             "| 1 | GET /api/ActivityLogs/GetDatabaseStatus | 200 | 614 ms | Healthy - "
             "Database Connected |\n"
             "| 2 | GET /api/ActivityLogs/GetErrorLogs | none | *30,020 ms* | HUNG |\n"
             "| 3 | GET /api/ActivityLogs/GetLogs | none | *30,170 ms* | HUNG |\n"
             "| 4 | GET /api/ActivityLogs/GetSsmVideoPath | *503* | 82 ms | Pool stopped |\n"
             "| 5-325 | everything else | *503* | 17-82 ms | Pool stopped |\n\n"
             "Request 1 proves the API and its database connection were healthy "
             "immediately before the failure. From request 4 onward the API was gone."),
            ("Why this is a pool stop, not overload",
             "|| Observation || What it rules out ||\n"
             "| 503s returned in 17-82 ms | Not saturation - a loaded server responds "
             "slowly, it does not refuse instantly |\n"
             "| 503 body is an IIS HTML page, not an application response | The request "
             "never reached application code |\n"
             "| Requests were strictly sequential | Not thread- or connection-pool "
             "exhaustion |\n"
             "| Only 3 requests preceded the failure | Not cumulative load |\n"
             "| Still 503 long after the run ended | Not transient; no auto-recovery |\n\n"
             "This is the signature of IIS rapid-fail protection: the worker crashed "
             "repeatedly inside the failure interval, so IIS stopped the pool."),
            ("It then degraded further",
             "The environment did not stay at 503. A later probe found *TCP connection "
             "refused* on both :6302 and :1302 - nothing listening on either port. "
             ":1302 was serving the application URL and the Swagger specs before the "
             "run.\n\n"
             "The progression 503 -> connection refused raises this from \"one pool "
             "needs restarting\" to \"the host's web services need investigation\"."),
            ("Probable cause, and its limits",
             "GetLogs and GetErrorLogs accept NO parameters at all - no page, no page "
             "size, no date range, no row limit. An unparameterised log-retrieval "
             "endpoint can only mean return everything. Against a log table on a "
             "long-lived environment that is an unbounded query and an unbounded "
             "serialisation, which exhausts the worker.\n\n"
             "What cannot be confirmed from the client side: the implementing source is "
             "not in the developer snapshot. The developer must confirm root cause from "
             "the IIS application event log and the worker crash dump."),
            ("Blast radius - this is not two endpoints",
             "GetLogs and GetErrorLogs are part of a five-action diagnostic scaffold "
             "repeated across ~49 controllers (GetDatabaseStatus, GetErrorLogs, "
             "GetLogs, GetStatus, SetStatus). *98 endpoints carry the same "
             "unbounded-query risk.* Two are confirmed to hang.\n\n"
             "If the cause is in a shared base controller, one fix addresses all 98. If "
             "each is separately implemented, 98 need fixing. That question should be "
             "answered first, because it changes the plan."),
        ],
        "repro": """⛔ DO NOT REPRODUCE CASUALLY. One request is expected to hang a worker.
   Two stopped the application pool and took QA_MsSQL down for a working day.
   Do not run this against any shared or production environment.

To reproduce SAFELY, on an isolated instance you are prepared to restart:

1. Isolate a single instance. Attach a profiler, or enable SQL Profiler /
   Extended Events to capture the query.

2. GET /api/ActivityLogs/GetErrorLogs
   Header: Authorization: Bearer <token>

   EXPECTED: a bounded, paged response
   ACTUAL:   no response; the request consumes the full client timeout (30 s)
             and the worker process does not recover

3. Capture the SQL that was executed and check for a missing TOP /
   OFFSET FETCH clause.

4. Retrieve the IIS application event log and the worker-process crash dump
   for the window around the failure. This gives the actual exception and is
   the only way to settle root cause.

The QA harness permanently blocklists these endpoints in chain_runner.py,
run_chains.py, run_qa_mssql.py and lh_common.py, so no future automated run
can take the environment down again. They are reported as
"EXCLUDED - blocked", never silently skipped - which also means these 98
endpoints are permanently UNTESTED.""",
        "expected": ("A log-retrieval endpoint accepts mandatory paging parameters and "
                     "cannot return an unbounded result set. No single request can "
                     "exhaust a worker process."),
        "actual": ("Two unparameterised GET endpoints hang for 30 s each; three "
                   "sequential requests stopped the IIS application pool and the host's "
                   "web services, requiring manual intervention."),
        "severity_rows": [
            ["**Availability**", "Three requests took the entire API down for a working "
                                 "day"],
            ["**Reachability**", "Ordinary GET endpoints, reachable by any authenticated "
                                 "caller"],
            ["**Attack surface**", "An endpoint that halts the application pool is a "
                                   "denial-of-service vector, not merely a test obstacle"],
            ["**Blast radius**", "98 endpoints carry the same unbounded-query risk"],
            ["**Recovery**", "No auto-recovery observed; the pool stayed stopped and then "
                             "degraded to connection-refused"],
            ["**Test coverage cost**", "These 98 endpoints are permanently blocklisted "
                                       "and therefore untested"],
            ["**Cost to fix**", "Medium - possibly one shared base controller"],
        ],
        "severity_argument": ("Rated Critical / ShowStopper: this is an availability "
                              "defect with a confirmed production-severity signature, "
                              "reachable by an ordinary authenticated caller."),
        "fix_rows": [
            ["1", "Retrieve the IIS application event log and worker crash dump for the "
                  "failure window", "Low", "Gives the actual exception; settles root cause"],
            ["2", "Capture the SQL executed and check for a missing `TOP` / "
                  "`OFFSET FETCH`", "Low", "Confirms the unbounded-query hypothesis"],
            ["3", "Add mandatory paging parameters with a server-side maximum across all "
                  "98 endpoints", "Medium", "The durable fix"],
            ["4", "Add a server-side query timeout and row cap", "Low",
             "Bounds every endpoint in this class - shared with LH-12"],
            ["5", "Confirm whether the diagnostic actions come from a shared base "
                  "controller", "Low", "Determines a 1-line fix versus 98 - answer first"],
            ["6", "Enable IIS pool auto-recovery and health monitoring", "Low",
             "A crash should not leave the API dead indefinitely"],
        ],
        "fix_note": ("Item 5 should be answered before anything is scheduled — it "
                     "determines whether item 3 is a single edit or ninety-eight."),
        "acceptance": """1. GetLogs and GetErrorLogs accept mandatory paging parameters with
   a server-side maximum, on all 98 endpoints.
2. A server-side query timeout and row cap prevent any single request from
   exhausting a worker process.
3. IIS pool auto-recovery is enabled.
4. The QA harness blocklist is removed and all 98 endpoints re-enter coverage
   without incident.""",
        "target": "blocklist removed, 98 endpoints back in coverage",
    },
)


# ═══════════════════════════════════════════════════════════ LH-10
ATTRS = {
    "[Required]": re.compile(r"\[\s*Required\s*[\]\(]"),
    "[Range]": re.compile(r"\[\s*Range\s*\("),
    "[StringLength]": re.compile(r"\[\s*StringLength\s*\("),
    "[MaxLength]": re.compile(r"\[\s*MaxLength\s*\("),
    "[MinLength]": re.compile(r"\[\s*MinLength\s*\("),
    "[RegularExpression]": re.compile(r"\[\s*RegularExpression\s*\("),
    "[EmailAddress]": re.compile(r"\[\s*EmailAddress"),
    "[Compare]": re.compile(r"\[\s*Compare\s*\("),
    "[JsonProperty]": re.compile(r"\[\s*JsonProperty"),
    "[DataMember]": re.compile(r"\[\s*DataMember"),
}
CLS_RE = re.compile(r"\bpublic\s+(?:partial\s+|sealed\s+|abstract\s+|static\s+)*class\s+\w+")
PROP_RE = re.compile(r"\bpublic\s+[\w<>\[\],?\s]+\s+\w+\s*\{\s*get\s*;\s*set\s*;\s*\}")
_scan_cache = None


def _lh10_scan():
    global _scan_cache
    if _scan_cache is not None:
        return _scan_cache
    root = ROOT / "pam" / "PAM"
    files = list(root.rglob("*.cs"))
    counts = Counter()
    hits = defaultdict(list)
    classes = props = 0
    for f in files:
        try:
            t = f.read_text(encoding="utf-8", errors="replace")
        except Exception:                                                # noqa: BLE001
            continue
        classes += len(CLS_RE.findall(t))
        props += len(PROP_RE.findall(t))
        for name, pat in ATTRS.items():
            n = len(pat.findall(t))
            if n:
                counts[name] += n
                hits[name].append((str(f.relative_to(root)), n))
    _scan_cache = {"files": len(files), "classes": classes, "props": props,
                   "counts": counts, "hits": hits}
    return _scan_cache


def _lh10_rows():
    s = _lh10_scan()
    rows = []
    for name in ATTRS:
        n = s["counts"].get(name, 0)
        rows.append(_row("", name, "", "", attribute=name, occurrences=n,
                         files=", ".join(f"{p} ({c})" for p, c in s["hits"].get(name, []))))
    return rows


def _lh10_classify(r):
    return "present" if r.get("occurrences") else "absent entirely"


def _lh10_narrative(payload, md):
    spec = LH10
    s = _lh10_scan()
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p("Request models in the product source carry almost no validation metadata. "
         "Nothing — not a client, not a code generator, not a new developer — can "
         "determine which fields are mandatory without calling the endpoint and reading "
         "the error.")
    md.table(["Measure", "Value"], [
        ["`.cs` files scanned", f"{s['files']:,}"],
        ["Public classes", f"{s['classes']:,}"],
        ["Public auto-properties", f"{s['props']:,}"],
        ["**Properties carrying `[Required]`**", f"**{s['counts'].get('[Required]', 0)}**"],
        ["Coverage",
         f"{s['counts'].get('[Required]', 0) / s['props'] * 100:.4f}% of auto-properties"],
    ])

    md.h(2, "2. Attribute census")
    md.table(["Validation attribute", "Occurrences", "Status"],
             [[f"`{name}`", s["counts"].get(name, 0),
               "present" if s["counts"].get(name) else "⛔ **absent entirely**"]
              for name in ATTRS])
    md.p("Four of the standard `System.ComponentModel.DataAnnotations` constraints — "
         "`[StringLength]`, `[MaxLength]`, `[MinLength]`, `[RegularExpression]` — do not "
         "appear **once** in 6,866 source files. There is no declared length or format "
         "constraint anywhere in the product's request models.")

    md.h(2, "3. What this costs, measured")
    md.p("This is not a theoretical concern. It is the direct cause of the single worst "
         "number in the whole API automation programme:")
    md.table(["Measure", "Value"], [
        ["Create endpoints in the catalogue", "217"],
        ["…with a request body defined anywhere in the framework", "111 (51%)"],
        ["…**that successfully insert a record**", "**13 of 217 (6%)**"],
        ["…with no request body derivable from any source", "101"],
    ])
    md.p("The failures are overwhelmingly *missing mandatory field* and *wrong type* — "
         "`Validation error occurred - Port is Mandatory`, `Could not convert string to "
         "integer`. Those requirements exist only in server-side procedural code, so the "
         "only way to discover them is to call the endpoint and parse the error prose.")
    md("> When two payloads were corrected **by hand** after reading the error messages, "
       "both created records successfully on the same environment the same day. This is "
       "a **metadata problem, not a tooling problem**.")
    md("")

    md.h(2, "4. Consequence")
    md.table(["Area", "Impact"], [
        ["Test generation", "Cannot construct a valid request without trial and error, "
                            "capping generated write coverage at 6%"],
        ["Client integration", "Every consumer rediscovers the same mandatory fields "
                               "empirically"],
        ["Server-side safety", "No model-level validation runs, so checks are hand-written "
                               "per action and can be forgotten"],
        ["Documentation", "Nothing can be generated — there is no metadata to render"],
        ["Error quality", "Validation failures surface as prose (LH-04), because there is "
                          "no declarative rule to reference"],
    ])

    md.h(2, "5. Where the few that exist live")
    for name in ("[Required]", "[JsonProperty]", "[DataMember]", "[Range]"):
        h = s["hits"].get(name, [])
        if h:
            md.p(f"`{name}` — {s['counts'].get(name)} occurrence(s):")
            md.table(["File", "Count"], [[f"`{p}`", c] for p, c in h])

    revalidation_section(md, payload, spec, 6)

    md.h(2, "7. Proposed fix")
    md.table(["#", "Action", "Effort", "Effect"], [
        ["1", "Annotate request models for the **most-used create endpoints** with "
              "`[Required]` and length/range constraints", "Medium, incremental",
         "Directly lifts generated write coverage from 13/217"],
        ["2", "Enable model-state validation in the pipeline so annotations are enforced "
              "server-side", "Low", "Turns metadata into behaviour"],
        ["3", "Return a structured field-level error listing which fields failed and why",
         "Medium", "Removes the need to parse prose"],
        ["4", "Add the annotations to the definition of done for new endpoints", "Low",
         "Stops the gap growing"],
    ])
    md.p("This is rated the **highest-leverage single change** available on the API. It "
         "unblocks automated write coverage, improves error quality, and enables "
         "generated documentation — from one class of edit.")
    reproduce_footer(md, spec, 8)


def _lh10_sheets(payload, xl):
    s = _lh10_scan()
    xl.summary("LH-10 — Request models carry almost no validation metadata", [
        ("Severity", "Medium"), ("Source", "Static analysis of pam/PAM"), ("", ""),
        (".cs files scanned", s["files"]),
        ("Public classes", s["classes"]),
        ("Public auto-properties", s["props"]),
        ("[Required] occurrences", s["counts"].get("[Required]", 0)),
        ("Coverage",
         f"{s['counts'].get('[Required]', 0) / s['props'] * 100:.4f}% of auto-properties"),
        ("", ""),
        ("Create endpoints", 217),
        ("…that successfully insert", "13 (6%)"),
        ("", ""),
        ("Headline", "Mandatory-ness exists only in procedural code, so it can only be "
                     "discovered by calling the endpoint and reading the error."),
    ])
    xl.sheet("Attribute Census", ["Validation attribute", "Occurrences", "Status"],
             [[name, s["counts"].get(name, 0),
               "present" if s["counts"].get(name) else "ABSENT ENTIRELY"]
              for name in ATTRS], [26, 14, 20],
             note="Standard System.ComponentModel.DataAnnotations constraints across all "
                  f"{s['files']} .cs files in the product snapshot.")
    occ = []
    for name, h in s["hits"].items():
        for p, c in h:
            occ.append([name, p, c])
    xl.sheet("Occurrences", ["Attribute", "File", "Count"], occ, [24, 100, 8],
             note="Every file containing any validation or serialisation attribute.")


LH10 = LoopholeSpec(
    num="10", slug="no-validation-attributes-on-models",
    title="Request models carry almost no validation metadata",
    severity="🟠 Medium", priority="High", effort="High",
    jira_summary=("Request models declare 3 [Required] attributes across 6,738 "
                  "properties - mandatory fields are undiscoverable without calling the API"),
    one_liner="3 [Required] in 6,738 properties; zero length or format constraints.",
    revalidate="static",
    revalidate_note="derived from static analysis of the product source",
    source="static",
    cross_refs=["LH-04 (validation failures surface as prose because no rule exists)",
                "LH-02 (create outcomes are equally undiscoverable)"],
    rows_static=_lh10_rows, classify=_lh10_classify,
    narrative=_lh10_narrative, sheets=_lh10_sheets,
    reproduces=lambda row, res: False, replay_summary=lambda res: "n/a",
    TICKET={
        "labels": ["api-design", "validation", "test-enablement"],
        "what": ("Request models in the product source carry almost no validation "
                 "metadata. Nothing - not a client, not a code generator, not a new "
                 "developer - can determine which fields are mandatory without calling "
                 "the endpoint and reading the error prose."),
        "occurrence_label": "[Required] attributes in the whole product",
        "occurrence_value": 3,
        "hide_endpoint_counts": True,
        "scope_rows": [(".cs files scanned", "6,866"),
                       ("Public auto-properties", "6,738"),
                       ("*Properties carrying [Required]*", "*3*"),
                       ("[StringLength] / [MaxLength] / [MinLength] / "
                        "[RegularExpression]", "*0 - absent entirely*")],
        "sections": [
            ("Attribute census across the whole product snapshot",
             "|| Attribute || Occurrences ||\n"
             "| [Required] | *3* |\n"
             "| [Range] | 0 |\n"
             "| [StringLength] | 0 |\n"
             "| [MaxLength] | 0 |\n"
             "| [MinLength] | 0 |\n"
             "| [RegularExpression] | 0 |\n"
             "| [EmailAddress] | 0 |\n\n"
             "Four of the standard System.ComponentModel.DataAnnotations constraints do "
             "not appear once in 6,866 source files. There is no declared length or "
             "format constraint anywhere in the product's request models."),
            ("What this costs, measured",
             "This is not theoretical. It is the direct cause of the worst number in "
             "the API automation programme:\n\n"
             "|| Measure || Value ||\n"
             "| Create endpoints in the catalogue | 217 |\n"
             "| …with a request body defined anywhere in the framework | 111 (51%) |\n"
             "| …*that successfully insert a record* | *13 of 217 (6%)* |\n"
             "| …with no request body derivable from any source | 101 |\n\n"
             "The failures are overwhelmingly missing-mandatory-field and wrong-type: "
             "\"Validation error occurred - Port is Mandatory\", \"Could not convert "
             "string to integer\". Those requirements exist only in server-side "
             "procedural code, so the only way to discover them is to call the endpoint "
             "and parse the error.\n\n"
             "When two payloads were corrected BY HAND after reading the error "
             "messages, both created records successfully on the same environment the "
             "same day. This is a metadata problem, not a tooling problem."),
            ("Knock-on effects",
             "* Test generation cannot construct a valid request without trial and "
             "error, capping generated write coverage at 6%\n"
             "* Every consumer rediscovers the same mandatory fields empirically\n"
             "* No model-level validation runs server-side, so checks are hand-written "
             "per action and can be forgotten\n"
             "* No documentation can be generated - there is no metadata to render\n"
             "* Validation failures surface as prose (LH-04) because there is no "
             "declarative rule to reference"),
        ],
        "repro": """No live execution is required - this is established by static analysis
of the product source.

1. From the product repository root (pam/PAM):

   grep -rn "\\[Required\\]" --include=*.cs . | wc -l      ->  3
   grep -rn "\\[StringLength(" --include=*.cs . | wc -l    ->  0
   grep -rn "\\[MaxLength(" --include=*.cs . | wc -l       ->  0
   grep -rn "\\[RegularExpression(" --include=*.cs . | wc -l -> 0

2. Count auto-properties for comparison:
   6,738 public { get; set; } properties across 6,866 .cs files.

3. To see the consequence, pick any create endpoint and send a plausible
   payload:

   POST /api/ServiceCreation/SetServiceDetails
   Body: { "LOBID": 108, "ServerGroupId": 282, "Hostname": "10.11.0.48",
           "IPAddress": "10.11.0.48", "Domain": 2, "ServiceTypeId": 1,
           "ServiceUserName": "SVC001" }

   ACTUAL: 200 OK with
   { "Success": false, "ErrorCode": "201-SCC-SSDN",
     "ErrorMessage": "Validation error occurred - Port is Mandatory" }

   Port is mandatory. Nothing in the model says so. The only way to learn it
   was to call the endpoint and read the prose.

4. The full attribute census and every file containing any validation
   attribute are in the attached EVIDENCE.xlsx.""",
        "expected": ("Request models declare their mandatory fields, types and "
                     "constraints, so a client or generator can construct a valid "
                     "request without calling the endpoint."),
        "actual": ("3 [Required] attributes across 6,738 properties and zero length or "
                   "format constraints. Mandatory-ness exists only in procedural code "
                   "and is discoverable only by trial and error."),
        "severity_rows": [
            ["**Test enablement**", "Caps generated write coverage at 13 of 217 create "
                                    "endpoints (6%) - the single worst measured number "
                                    "in the programme"],
            ["**Integration cost**", "Every consumer rediscovers the same mandatory "
                                     "fields empirically"],
            ["**Server-side safety**", "No model-level validation runs; checks are "
                                       "hand-written per action and can be omitted"],
            ["**Documentation**", "Nothing can be generated - there is no metadata"],
            ["**Error quality**", "Drives the prose-only validation errors in LH-04"],
            ["**Cost to fix**", "High in total, but fully incremental - the most-used "
                                "create endpoints first"],
        ],
        "severity_argument": ("This is rated the highest-leverage single change "
                              "available on the API. One class of edit unblocks "
                              "automated write coverage, improves error quality and "
                              "enables generated documentation."),
        "fix_rows": [
            ["1", "Annotate request models for the most-used create endpoints with "
                  "`[Required]` and length/range constraints", "Medium, incremental",
             "Directly lifts generated write coverage from 13/217"],
            ["2", "Enable model-state validation in the pipeline so annotations are "
                  "enforced server-side", "Low", "Turns metadata into behaviour"],
            ["3", "Return a structured field-level error listing which fields failed and "
                  "why", "Medium", "Removes the need to parse prose"],
            ["4", "Add the annotations to the definition of done for new endpoints",
             "Low", "Stops the gap growing"],
        ],
        "fix_note": ("Item 1 does not need to be done all at once. Annotating the twenty "
                     "most-used create endpoints would be measurable immediately in the "
                     "next QA run."),
        "acceptance": """1. Request models for the agreed priority endpoints declare
   [Required] and appropriate length/range constraints.
2. Model-state validation is enforced in the pipeline.
3. Validation failures return a structured field-level error, not prose.
4. Re-running the QA harness shows generated create coverage above the agreed
   target (currently 13 of 217).""",
        "target": "an agreed create-coverage target",
    },
)


STATIC_SPECS = [LH06, LH07, LH08, LH10]
