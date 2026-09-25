#!/usr/bin/env python3
"""Run-derived loophole specs: LH-02, 03, 04, 05, 09, 11, 12.

Each is selected from the same 1,873 hops of artifacts/runs/2026-07-29_181439/. The shared
engine is lh_common; only the selector, the classification and the prose live here.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict

from lh_common import (                                                  # noqa: F401
    API_BASE, ENVIRONMENT, LEAK, MD, RUN_ID, SECRET_KEY, LoopholeSpec, Xlsx,
    default_replay_summary, esc, header_block, reproduce_footer, revalidation_section,
)

WRITE_INTENT = re.compile(
    r"^(set|insert|add|create|update|save|edit|modify|assign|map|unmap)", re.I)
NOOP_MSG = re.compile(r"already exist|no record|not found|no records|no change", re.I)


def _by(rows, key):
    return Counter(r[key] for r in rows)


def _endpoint_table(md, rows, limit=None, extra=None, extra_hdr=None):
    hdr = ["#", "Controller", "Action", "Verb", "HTTP"] + ([extra_hdr] if extra_hdr else [])
    body = []
    for i, r in enumerate(rows if limit is None else rows[:limit], 1):
        line = [i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"], r["http_status"]]
        if extra:
            line.append(esc(extra(r))[:160])
        body.append(line)
    md.table(hdr, body)


# ═══════════════════════════════════════════════════════════ LH-02
def _lh02_select(hop, resp):
    if hop.get("status") != 200 or not isinstance(resp, dict):
        return False
    if resp.get("Success") is not True:
        return False
    return bool(str(resp.get("Message") or "").strip())


def _lh02_classify(r):
    msg = str((r.get("response") or {}).get("Message") or "")
    write = bool(WRITE_INTENT.match(r["action"]))
    if write and NOOP_MSG.search(msg):
        return "write-noop"          # the headline defect
    if write:
        return "write-success"       # succeeded, but with unstandardised wording
    if NOOP_MSG.search(msg):
        return "read-empty"          # arguably correct, but indistinguishable
    return "read-success"


def _lh02_msg(r):
    return (r.get("response") or {}).get("Message")


def _lh02_narrative(payload, md):
    rows = payload["rows"]
    spec = LH02
    noop = [r for r in rows if r["klass"] == "write-noop"]
    wsucc = [r for r in rows if r["klass"] == "write-success"]
    rempty = [r for r in rows if r["klass"] == "read-empty"]
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p("A write endpoint returns `Success: true` at HTTP 200 when **nothing was "
         "written**. The only thing distinguishing a real insert from a silent no-op is "
         "the English prose in the `Message` field.")
    md.code('POST /api/UserDetails/SetUserDetails\n\n'
            'HTTP/1.1 200 OK\n'
            '{ "Success": true,\n'
            '  "Message": "Already Exists" }', "http")
    md.p("Status code: green. `Success` flag: green. Records created: **zero**.")
    md.table(["Measure", "Value"], [
        ["`Success: true` responses carrying a Message", len(rows)],
        ["…on a **write-intent** action reporting a no-op", f"**{len(noop)}**"],
        ["…on a write-intent action reporting success", len(wsucc)],
        ["…on a read reporting no records", len(rempty)],
        ["Distinct Message strings across all of them",
         len({str(_lh02_msg(r)) for r in rows})],
    ])

    md.h(2, "2. Confirmed create no-ops")
    md.p("Write-intent actions that returned `Success: true` while reporting that nothing "
         "happened:")
    _endpoint_table(md, noop, extra=_lh02_msg, extra_hdr="Message")
    md.p("⚠️ `POST /api/ServiceCreation/SetServiceDetails` is the case originally recorded "
         "in the developer brief, returning `Success: true` with `Message: \"Already "
         "Exists\"` and a populated `Result` carrying the *pre-existing* `ServiceId`. In "
         "this particular run that endpoint failed earlier on validation "
         "(`201-SCC-SSDN — Port is Mandatory`, see LH-01), so it appears in LH-01's set "
         "rather than here. The behaviour is documented and reproducible when the payload "
         "is valid and the record already exists.")

    md.h(2, "3. The deeper problem — success has no stable vocabulary")
    md.p("Because the outcome is only expressed in prose, a client must string-match. "
         "That is already impossible: write-intent actions in this single run reported "
         "success in **" + str(len({str(_lh02_msg(r)) for r in wsucc})) +
         " different ways**.")
    md.table(["Message returned on a successful write", "Calls"],
             [[f"`{esc(k)}`", v]
              for k, v in Counter(str(_lh02_msg(r)) for r in wsucc).most_common()])
    md.p("Note `Operation Successfull` — a **spelling error in the product's own success "
         "string**. Any client matching `\"Successful\"` fails on it. This is exactly why "
         "correctness must not depend on message text.")

    md.h(2, "4. Reads are indistinguishable from writes")
    md.p(f"A further {len(rempty)} responses return `Success: true` with a no-op message "
         "on **read** actions — 'No Record Found', 'Record Already Exists.'. Those are "
         "arguably correct behaviour for a query, and that is the problem: the envelope "
         "gives a client no way to tell 'your write was ignored' from 'your query matched "
         "nothing'. Both are `Success: true` plus prose.")
    md.table(["Message", "Read calls"],
             [[f"`{esc(k)}`", v]
              for k, v in Counter(str(_lh02_msg(r)) for r in rempty).most_common(8)])

    md.h(2, "5. Consequence")
    md.table(["Area", "Impact"], [
        ["Automated tests", "A create assertion that checks `Success == true` passes "
                            "against a record that was never created"],
        ["Idempotency", "A retry cannot tell whether the first attempt landed"],
        ["Data integrity", "A migration or bulk load reports 100% success while silently "
                           "skipping every duplicate"],
        ["Our harness", "Create assertions must parse `Message` semantics — the direct "
                        "cause of the L4 `message-semantics` layer existing at all"],
    ])

    revalidation_section(md, payload, spec, 6)

    md.h(2, "7. Proposed fix")
    md.table(["#", "Action", "Effort"], [
        ["1", "Return a machine-readable outcome — `\"created\": true|false`, or an "
              "`Outcome` enum (`Inserted` / `AlreadyExists` / `Updated` / `NoChange`)",
         "Low"],
        ["2", "Or use status codes semantically: `201 Created` on insert, `200 OK` on "
              "update, `409 Conflict` on duplicate", "Medium"],
        ["3", "Standardise the success vocabulary and fix `Operation Successfull`", "Low"],
        ["4", "Never require a client to string-match prose to determine an outcome",
         "—"],
    ])
    md.p("Item 1 is the smallest change that fixes correctness and stays backward "
         "compatible: existing clients keep reading `Success` and `Message`, new clients "
         "read the flag.")

    md.h(2, "8. Full register")
    md.p("Every `Success: true` response carrying a Message, grouped by class.")
    for k in ("write-noop", "write-success", "read-empty", "read-success"):
        sub = [r for r in rows if r["klass"] == k]
        if not sub:
            continue
        md.h(3, f"`{k}` — {len(sub)} call{'s' if len(sub) != 1 else ''}")
        md.table(["#", "Controller", "Action", "Verb", "Message", "Evidence"],
                 [[i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"],
                   esc(_lh02_msg(r))[:80], f"`{esc(r['evidence_file'])}`"]
                  for i, r in enumerate(sub, 1)])
    reproduce_footer(md, spec, 9)


def _lh02_sheets(payload, xl):
    rows = payload["rows"]
    noop = [r for r in rows if r["klass"] == "write-noop"]
    xl.summary("LH-02 — Success: true returned when nothing was created", [
        ("Severity", "Critical"), ("Environment", ENVIRONMENT),
        ("Source run", RUN_ID), ("", ""),
        ("Success:true responses with a Message", len(rows)),
        ("…confirmed write no-ops", len(noop)),
        ("…write successes (unstandardised wording)",
         sum(1 for r in rows if r["klass"] == "write-success")),
        ("…reads reporting no records",
         sum(1 for r in rows if r["klass"] == "read-empty")),
        ("Distinct Message strings", len({str(_lh02_msg(r)) for r in rows})),
        ("", ""),
        ("Headline", "A write returns Success:true having written nothing; only English "
                     "prose distinguishes the two"),
    ])
    xl.sheet("Write No-Ops",
             ["Controller", "Action", "Verb", "Path", "Message", "Request body",
              "Evidence file"],
             [[r["controller"], r["action"], r["verb"], r["path"], _lh02_msg(r),
               json.dumps(r["request_body"])[:900] if r["request_body"] else "",
               r["evidence_file"]] for r in noop],
             [20, 30, 6, 46, 26, 80, 46],
             note="Write-intent actions that returned Success:true while reporting that "
                  "nothing was written. This is the defect.")
    xl.sheet("Message Vocabulary",
             ["Message", "Class", "Calls", "Distinct endpoints"],
             [[m, k, n, len({(r["controller"], r["action"]) for r in rows
                             if str(_lh02_msg(r)) == m and r["klass"] == k})]
              for (m, k), n in Counter((str(_lh02_msg(r)), r["klass"])
                                       for r in rows).most_common()],
             [56, 16, 8, 18],
             note="Every distinct Message string. A client forced to string-match must "
                  "handle all of these — including the misspelled 'Operation Successfull'.")
    xl.sheet("All Success-True Responses",
             ["#", "Class", "Controller", "Action", "Verb", "Path", "Message",
              "Latency ms", "Evidence file"],
             [[i, r["klass"], r["controller"], r["action"], r["verb"], r["path"],
               _lh02_msg(r), r["latency_ms"], r["evidence_file"]]
              for i, r in enumerate(rows, 1)],
             [5, 15, 20, 32, 6, 46, 40, 11, 46])


LH02 = LoopholeSpec(
    num="02", slug="success-true-nothing-created",
    title="Success: true returned when nothing was created",
    severity="🔴 Critical", priority="High", effort="Low",
    jira_summary=("API returns Success:true at HTTP 200 for writes that created nothing - "
                  "outcome is only distinguishable by parsing English prose"),
    one_liner="A write returns Success:true having written nothing.",
    revalidate="safe", replay_limit=60,
    # ⛔ 28 of these rows are successful INSERTs. Replaying them would create fresh
    # records on every re-validation. Only the no-ops and the reads are replayed - the
    # no-ops are the finding, and they insert nothing by definition.
    replay_filter=lambda r: r["klass"] in ("write-noop", "read-empty"),
    cross_refs=["LH-01 (the `Success:false` half of the same envelope problem)",
                "LH-03 (response shapes)"],
    select=_lh02_select, classify=_lh02_classify,
    narrative=_lh02_narrative, sheets=_lh02_sheets,
    reproduces=lambda row, res: (
        res.get("status") == 200 and isinstance(res.get("response"), dict)
        and res["response"].get("Success") is True),
    replay_summary=default_replay_summary,
    TICKET={
        "labels": ["error-handling", "response-envelope"],
        "what": ("A write endpoint returns Success:true at HTTP 200 when nothing was "
                 "written. The only thing distinguishing a real insert from a silent "
                 "no-op is the English prose in the Message field.\n\n"
                 "Status code: green. Success flag: green. Records created: zero."),
        "occurrence_label": "Confirmed write no-ops",
        "occurrence_value": 2,
        "scope_rows": [("Success:true responses examined", "552"),
                       ("Write successes with unstandardised wording", "28"),
                       ("Reads reporting no records the same way", "47"),
                       ("Distinct Message strings in one run", "*70*")],
        "example": ('POST /api/UserDetails/SetUserDetails\n\n'
                    'HTTP/1.1 200 OK\n'
                    '{ "Success": true,\n'
                    '  "Message": "Already Exists" }'),
        "sections": [
            ("Success has no stable vocabulary",
             "Because the outcome is only expressed in prose, a client must "
             "string-match. That is already impossible - write actions in a single run "
             "reported success in 8 different ways:\n\n"
             "|| Message || Calls ||\n"
             "| Record Inserted successfully. | 10 |\n"
             "| Operation Successfull | 9 |\n"
             "| Inserted Successfully | 3 |\n"
             "| Record Added successfully. | 2 |\n"
             "| Modified Successfully | 2 |\n"
             "| Already Exists | 2 |\n"
             "| Disabled Successfully | 1 |\n"
             "| SSH Linux vault saved successfully. | 1 |\n\n"
             "Note *Operation Successfull* - a spelling error in the product's own "
             "success string. A client matching \"Successful\" fails on it."),
            ("Reads are indistinguishable from writes",
             "47 further responses return Success:true with a no-op message on read "
             "actions. Those are arguably correct for a query - and that is the "
             "problem. The envelope gives a client no way to tell \"your write was "
             "ignored\" from \"your query matched nothing\"."),
        ],
        "repro": """Preconditions:
  - Environment: QA_MsSQL, https://u16hf.arconnet.com:6302
  - A valid bearer token. Generate ONE and reuse it - repeated /arcontoken
    requests lock the GenericScheduler account (PAMIT ISSUE-009).
  - A user record that already exists.

1. POST /api/UserDetails/SetUserDetails
   Header: Authorization: Bearer <token>
   Header: Content-Type: application/json
   Body:   a valid user payload whose UserName ALREADY EXISTS

2. Observe the HTTP status line and the Success flag.
   EXPECTED: 409 Conflict, or 200 with a machine-readable "created": false
   ACTUAL:   200 OK with { "Success": true, "Message": "Already Exists" }

3. Query the user list and confirm no new record was created.
   The call reported success. Nothing was written.

4. Repeat against /api/UserDetailsV3/SetUserDetails - same behaviour.

5. For the success-vocabulary half: call any two different Insert* endpoints
   that succeed, and compare the Message strings. They will not match.""",
        "expected": ("A write that changes nothing is distinguishable from a write that "
                     "inserted, without parsing prose."),
        "actual": ("Both return HTTP 200 with Success:true. Only the English text of "
                   "Message differs, and that text is itself unstandardised across 8 "
                   "variants including a misspelling."),
        "severity_rows": [
            ["**Correctness**", "A create assertion checking `Success == true` passes "
                                "against a record that was never created"],
            ["**Idempotency**", "A retry cannot determine whether the first attempt "
                                "landed"],
            ["**Data integrity**", "A bulk load or migration reports 100% success while "
                                   "silently skipping every duplicate"],
            ["**Detectability**", "Invisible to any monitor - status and flag are both "
                                  "green"],
            ["**Workaround**", "String-match English prose, across 8 known variants"],
            ["**Cost to fix**", "Low - one additional field in the envelope"],
        ],
        "severity_argument": ("The defect is not that a duplicate is rejected — that is "
                              "correct. It is that the rejection is reported as success, "
                              "so no automated consumer can detect it."),
        "fix_rows": [
            ["1", "Return a machine-readable outcome: `\"created\": true|false`, or an "
                  "`Outcome` enum (`Inserted`/`AlreadyExists`/`Updated`/`NoChange`)",
             "Low", "Fixes correctness, fully backward compatible"],
            ["2", "Or use status codes semantically: `201 Created`, `200 OK`, "
                  "`409 Conflict`", "Medium", "Cleaner, but changes existing behaviour"],
            ["3", "Standardise the success vocabulary and fix `Operation Successfull`",
             "Low", "Removes the misspelling trap"],
            ["4", "Never require a client to string-match prose for an outcome", "—",
             "Policy"],
        ],
        "fix_note": ("Item 1 is the smallest change that fixes correctness while staying "
                     "backward compatible: existing clients keep reading `Success` and "
                     "`Message`; new clients read the flag."),
        "acceptance": """1. A write that creates nothing is distinguishable from one that
   creates a record, using a machine-readable field only - no prose parsing.
2. The success-message vocabulary is documented and consistent; the
   "Operation Successfull" misspelling is corrected.
3. Re-running the QA harness reports 0 write-intent calls returning
   Success:true with a no-op Message.""",
        "target": "0 write-noop occurrences",
    },
)


# ═══════════════════════════════════════════════════════════ LH-03
def shape_of(r):
    """Coarse family (matches the developer brief's 8) plus a finer variant."""
    if r is None:
        return "8. absent / null body", "null"
    if isinstance(r, bool):
        return "8. bare scalar, no envelope", "bare boolean"
    if isinstance(r, str):
        return ("8. bare scalar, no envelope",
                "empty string" if not r.strip() else "bare string")
    if isinstance(r, list):
        return "4. bare array, no envelope", f"bare array[{len(r)}]"
    if isinstance(r, dict):
        k = set(r)
        if "aaData" in k:
            return "6. DataTables grid format", "{aaData, aaData1, aaData11}"
        if "Output" in k and len(k) <= 2:
            return "7. delimited string inside a field", '{"Output": "1|..."}'
        if "Success" in k:
            if r.get("Success") is False:
                return ("5. error envelope at HTTP 200",
                        "{Success:false, ErrorCode, ErrorMessage}")
            res, msg = r.get("Result"), "Message" in k
            if isinstance(res, list):
                return (("1. standard envelope, Result[]" if msg
                         else "2. standard envelope, Result[], no Message"),
                        f"Result[] {'(+Message)' if msg else '(no Message)'}")
            if isinstance(res, dict):
                return ("3. envelope, Result is an object",
                        f"Result{{}} {'(+Message)' if msg else '(no Message)'}")
            if "Result" not in k:
                return ("2. standard envelope, Result[], no Message",
                        "envelope, no Result field")
            return "3. envelope, Result is an object", f"Result={type(res).__name__}"
        return "9. plain object, no envelope", "plain object"
    return "8. bare scalar, no envelope", type(r).__name__


def _lh03_select(hop, resp):
    return hop.get("evidence") is not None


def _lh03_classify(r):
    fam, _ = shape_of(r.get("response"))
    return fam


def _lh03_narrative(payload, md):
    rows = payload["rows"]
    spec = LH03
    fams = Counter(r["klass"] for r in rows)
    variants = Counter(shape_of(r.get("response"))[1] for r in rows)
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p(f"One API answers in **{len(fams)} structurally different response families** "
         f"({len(variants)} distinct variants once optional fields are counted). A client "
         "cannot write one deserialiser; it must branch per endpoint, discovered "
         "empirically.")
    md.table(["#", "Response family", "Calls", "Distinct endpoints"],
             [[i, f"**{k.split('. ', 1)[1]}**", v,
               len({(r["controller"], r["action"]) for r in rows if r["klass"] == k})]
              for i, (k, v) in enumerate(sorted(fams.items()), 1)])

    md.h(2, "2. The same data, two different shapes")
    md.p("`GetLOBList` is served by several controllers. Some wrap it in the standard "
         "envelope; at least one returns a bare array. Same logical payload, "
         "incompatible parsing:")
    md.code('# GET /api/DeviceOnboarding/GetLOBList  -> bare array\n'
            '[ { "LobId": 108, "LobName": "AUTOMATION_TEST_LOB" }, ... ]\n\n'
            '# POST /api/ADbridging/GetLOBList       -> standard envelope\n'
            '{ "Program": "ARCON PAM API", "Version": "1.0", "Success": true,\n'
            '  "Result": [ { "LobId": 108, "LobName": "AUTOMATION_TEST_LOB" } ] }', "json")

    md.h(2, "3. The worst shapes")
    md.table(["Shape", "Why it is a problem"], [
        ["`{\"Output\": \"1\\|Parameter error occurred - ...\"}`",
         "The error is a **pipe-delimited string inside a JSON field**. A client must "
         "split a string to discover the call failed"],
        ["`{aaData, aaData1, aaData11}`",
         "A **jQuery DataTables grid format** leaking into an API contract. It binds the "
         "API to one UI widget"],
        ["Bare `false` / bare `\"\"`",
         "The entire body is a scalar. No status, no message, no diagnostics"],
        ["Bare array",
         "No envelope at all, so no `Success` flag — the client cannot distinguish "
         "'empty result' from 'failed'"],
    ])

    md.h(2, "4. Variant detail")
    md.p("Within the families, these are the distinct structural variants observed:")
    md.table(["Variant", "Calls"],
             [[f"`{esc(k)}`", v] for k, v in variants.most_common()])
    md.p("Families 1 and 2 differ only by the presence of `Message`; family 3 differs by "
         "`Result` being an object rather than an array. Those three are the same "
         "envelope with optional parts, which a tolerant client can absorb — but only if "
         "it is told they are optional. Nothing documents that.")

    md.h(2, "5. Blast radius by controller")
    ctrl = defaultdict(set)
    for r in rows:
        ctrl[r["controller"]].add(r["klass"])
    multi = sorted(((c, s) for c, s in ctrl.items() if len(s) > 2),
                   key=lambda x: -len(x[1]))
    md.p(f"**{len(multi)} controllers return three or more different shapes** from their "
         "own endpoints, so a per-controller client is not sufficient either:")
    md.table(["Controller", "Distinct shapes", "Families"],
             [[f"`{c}`", len(s), ", ".join(sorted(x.split('.')[0] for x in s))]
              for c, s in multi[:20]])

    revalidation_section(md, payload, spec, 6)

    md.h(2, "7. Proposed fix")
    md.table(["#", "Action", "Effort"], [
        ["1", "Converge on the standard envelope for every endpoint; make `Message` and "
              "`Result` always present, `Result` always an array", "Medium"],
        ["2", "If (1) is too large, **publish which endpoints use which shape** and stop "
              "adding new ones", "Low"],
        ["3", "Retire the DataTables shape from the API — build the grid payload in the "
              "UI layer", "Medium"],
        ["4", "Retire `{\"Output\": \"1|...\"}`; never encode errors in delimited strings",
         "Low"],
    ])
    reproduce_footer(md, spec, 8)


def _lh03_sheets(payload, xl):
    rows = payload["rows"]
    fams = Counter(r["klass"] for r in rows)
    shapes_per_ctrl = {c: len({r["klass"] for r in rows if r["controller"] == c})
                       for c in {r["controller"] for r in rows}}
    xl.summary("LH-03 — Multiple response shapes on one API", [
        ("Severity", "High"), ("Environment", ENVIRONMENT), ("Source run", RUN_ID),
        ("", ""),
        ("Responses classified", len(rows)),
        ("Distinct response families", len(fams)),
        ("Distinct structural variants",
         len({shape_of(r.get("response"))[1] for r in rows})),
        ("Controllers returning 3+ shapes",
         sum(1 for n in shapes_per_ctrl.values() if n > 2)),
        ("", ""),
        ("Headline", "One API, many response contracts. A client cannot write a single "
                     "deserialiser."),
    ])
    xl.sheet("Shape Families", ["Family", "Calls", "Distinct endpoints", "Example endpoint"],
             [[k, v, len({(r["controller"], r["action"]) for r in rows
                          if r["klass"] == k}),
               next(f"{r['controller']}/{r['action']}" for r in rows if r["klass"] == k)]
              for k, v in sorted(fams.items())],
             [44, 8, 18, 44])
    xl.sheet("Variants", ["Variant", "Family", "Calls"],
             [[v, next(r["klass"] for r in rows
                       if shape_of(r.get("response"))[1] == v), n]
              for v, n in Counter(shape_of(r.get("response"))[1]
                                  for r in rows).most_common()],
             [40, 44, 8])
    xl.sheet("All Responses",
             ["#", "Family", "Variant", "Controller", "Action", "Verb", "HTTP",
              "Bytes", "Content-Type", "Evidence file"],
             [[i, r["klass"], shape_of(r.get("response"))[1], r["controller"],
               r["action"], r["verb"], r["http_status"], r["body_bytes"],
               r["content_type"], r["evidence_file"]]
              for i, r in enumerate(rows, 1)],
             [5, 42, 30, 20, 32, 6, 7, 10, 20, 46])


LH03 = LoopholeSpec(
    num="03", slug="multiple-response-shapes",
    title="Multiple incompatible response shapes on one API",
    severity="🔴 High", priority="High", effort="Medium",
    jira_summary=("One API returns 9 structurally different response shapes - no single "
                  "client deserialiser is possible"),
    one_liner="Nine response families on one API; two endpoints return the same data "
              "with and without an envelope.",
    revalidate="safe", replay_limit=40,
    cross_refs=["LH-01 (shape 5 is the error envelope at HTTP 200)",
                "LH-04 (error-code register)"],
    select=_lh03_select, classify=_lh03_classify,
    narrative=_lh03_narrative, sheets=_lh03_sheets,
    reproduces=lambda row, res: (shape_of(res.get("response"))[0] == row["klass"]),
    replay_summary=lambda res: shape_of(res.get("response"))[1],
    TICKET={
        "labels": ["response-envelope", "api-consistency"],
        "what": ("One API answers in 9 structurally different response families. A "
                 "client cannot write a single deserialiser; it must branch per "
                 "endpoint, and the correct branch is discoverable only by calling "
                 "the endpoint and inspecting what comes back."),
        "occurrence_label": "Distinct response families",
        "occurrence_value": 9,
        "scope_rows": [("Responses classified", "1,868"),
                       ("Distinct structural variants", "16"),
                       ("Controllers returning 3+ different shapes", "see EVIDENCE.md §5")],
        "example": ('# GET /api/DeviceOnboarding/GetLOBList  -> bare array\n'
                    '[ { "LobId": 108, "LobName": "AUTOMATION_TEST_LOB" } ]\n\n'
                    '# POST /api/ADbridging/GetLOBList       -> standard envelope\n'
                    '{ "Program": "ARCON PAM API", "Version": "1.0", "Success": true,\n'
                    '  "Result": [ { "LobId": 108, "LobName": "AUTOMATION_TEST_LOB" } ] }'),
        "sections": [
            ("The worst shapes",
             '|| Shape || Why it is a problem ||\n'
             '| {"Output": "1\\|Parameter error occurred - ..."} | The error is a '
             'pipe-delimited string inside a JSON field. A client must split a string '
             'to discover the call failed |\n'
             '| {aaData, aaData1, aaData11} | A jQuery DataTables grid format leaking '
             'into an API contract, binding the API to one UI widget |\n'
             '| bare false, or bare "" | The entire body is a scalar - no status, no '
             'message, no diagnostics |\n'
             '| bare array | No envelope, so no Success flag - "empty result" and '
             '"failed" are indistinguishable |'),
            ("Same data, two contracts",
             "GetLOBList is served by several controllers. Some wrap it in the standard "
             "envelope; DeviceOnboarding returns a bare array. Same logical payload, "
             "incompatible parsing, no documentation of which is which."),
        ],
        "repro": """Preconditions:
  - Environment: QA_MsSQL, https://u16hf.arconnet.com:6302
  - A valid bearer token (generate ONE - see PAMIT ISSUE-009).

1. GET /api/DeviceOnboarding/GetLOBList
   Observe: the body is a BARE JSON ARRAY, with no envelope and no Success flag.

2. POST /api/ADbridging/GetLOBList
   Observe: the body is the standard envelope
            { Program, Version, DateTime, Success, Result[] }

   Two endpoints, the same logical data, two incompatible contracts.

3. POST /api/ServiceDetails/GetServiceDetails
   Observe: Result is an OBJECT, not an array.

4. GET /api/AccessControl/GetAccessControlLogs
   Observe: { aaData, aaData1, aaData11 } - a DataTables grid shape.

5. POST /api/UserDetails/SetPAMUserDetails  (with an invalid payload)
   Observe: { "Output": "1|Parameter error occurred - ..." } - the error is a
            pipe-delimited string inside a JSON field.

6. The full classification of all 1,868 responses is in the attached
   EVIDENCE.xlsx, sheet "All Responses".""",
        "expected": ("Every endpoint returns the same envelope, so one deserialiser "
                     "handles the whole API."),
        "actual": ("Nine structurally different families are in use, including a bare "
                   "array, a bare scalar, a UI grid format and an error encoded as a "
                   "delimited string."),
        "severity_rows": [
            ["**Correctness**", "A client that assumes the envelope crashes or silently "
                                "mis-parses on 4 of the 9 families"],
            ["**Blast radius**", "872 distinct endpoints classified; the variance spans "
                                 "most controllers"],
            ["**Integration cost**", "Every consumer reimplements the same per-endpoint "
                                     "branching"],
            ["**Discoverability**", "Nothing documents which endpoint uses which shape - "
                                    "it is found by calling"],
            ["**Cost to fix**", "Medium to converge; Low to publish the mapping"],
        ],
        "severity_argument": ("Rated High rather than Critical because each shape is "
                              "individually parseable — the cost is borne by every "
                              "consumer, repeatedly, rather than producing a wrong answer."),
        "fix_rows": [
            ["1", "Converge on the standard envelope; make `Message` and `Result` always "
                  "present and `Result` always an array", "Medium", "Removes the problem"],
            ["2", "If (1) is too large, publish which endpoints use which shape and stop "
                  "adding new ones", "Low", "Makes it survivable"],
            ["3", "Retire the DataTables shape from the API; build grid payloads in the "
                  "UI layer", "Medium", "Removes a UI dependency from the contract"],
            ["4", "Retire `{\"Output\": \"1|...\"}`; never encode errors in delimited "
                  "strings", "Low", "Removes the worst shape"],
        ],
        "acceptance": """1. Every endpoint returns one documented envelope shape, or the
   shape-per-endpoint mapping is published and complete.
2. No endpoint returns a bare scalar or a delimited error string.
3. Re-running the QA harness classifies every response into a documented shape.""",
        "target": "1 documented shape family",
    },
)


# ═══════════════════════════════════════════════════════════ LH-04
def _code_of(resp):
    if not isinstance(resp, dict):
        return None
    c = resp.get("ErrorCode", resp.get("errorCode"))
    return None if c in (None, "") else str(c)


def _lh04_select(hop, resp):
    return _code_of(resp) is not None


def _lh04_classify(r):
    c = _code_of(r.get("response")) or ""
    m = re.match(r"\s*(\d{3})", c)
    return m.group(1) if m else "non-numeric"


KNOWN_TO_FRAMEWORK = {"201", "202", "203"}


def _lh04_narrative(payload, md):
    rows = payload["rows"]
    spec = LH04
    codes = Counter(_code_of(r.get("response")).splitlines()[0][:60] for r in rows)
    pfx = Counter(r["klass"] for r in rows)
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p("The API signals failure through an `ErrorCode` in the response body. There is "
         "no published register of those codes, and the set in use is far larger than "
         "anything documented.")
    md.table(["Measure", "Value"], [
        ["Responses carrying an `ErrorCode`", len(rows)],
        ["**Distinct `ErrorCode` values observed**", f"**{len(codes)}**"],
        ["Codes recognised by the QA framework", "3 — `201`, `202`, `203`"],
        ["Codes documented in the 2,470-page Confluence reference", "**4**"],
        ["Distinct numeric prefixes in use", len(pfx)],
    ])
    md.p(f"So the product emits **{len(codes)} codes** against a documented register of "
         "**4**. A client cannot determine which codes are retryable, which are "
         "permanent, or which indicate a server fault.")

    md.h(2, "2. The prefix taxonomy the product already uses")
    md.p("The codes are not arbitrary — the three-digit prefix consistently encodes a "
         "failure class. This is the register that exists implicitly and has never been "
         "written down:")
    md.table(["Prefix", "Meaning (inferred from every message carrying it)",
              "Distinct codes", "Calls", "Known to the framework?"],
             [[f"`{p}`",
               spec.TAXONOMY.get(p, ("unclassified", ""))[0],
               len({_code_of(r.get("response")).splitlines()[0][:60] for r in rows
                    if r["klass"] == p}),
               n,
               "✅ yes" if p in KNOWN_TO_FRAMEWORK else "⛔ **no**"]
              for p, n in sorted(pfx.items(), key=lambda kv: (-kv[1], kv[0]))])
    unknown = sum(v for k, v in pfx.items() if k not in KNOWN_TO_FRAMEWORK)
    md.p(f"**{unknown} of {len(rows)} responses carry a code the framework does not "
         "recognise.** Its `KNOWN_ERROR_CODES` set is a hardcoded three-element literal.")

    md.h(2, "3. The codes are not machine-readable")
    md.p("Beyond the missing register, the field itself is not consistently formed:")
    defects = []
    for c in codes:
        f = []
        if c != c.strip():
            f.append("whitespace")
        if re.match(r"^\s*\d{3}[A-Za-z]", c):
            f.append("no separator after prefix")
        if re.match(r"^\s*\d{3}\s+-", c) or re.match(r"^\s*\d{3}\s[^-]", c):
            f.append("space in separator")
        if c.rstrip().endswith("-"):
            f.append("trailing separator")
        if not re.match(r"^\s*\d{3}", c):
            f.append("no numeric prefix")
        if len(c) > 40:
            f.append("stack trace concatenated into the code")
        if f:
            defects.append((c, "; ".join(f)))
    md.table(["Malformed code", "Defect"],
             [[f"`{esc(c)}`", d] for c, d in sorted(defects)[:24]])
    md.p(f"**{len(defects)} of {len(codes)} distinct codes are malformed.** Variants "
         "observed for what is evidently the same family: `201-UDC-…`, `201SDC-GSDBI`, "
         "`203 -ULC-GUL`, `203-ACC-GAC-`, `GSAPLR`. One regex cannot parse these.")

    md.h(2, "4. Full observed register")
    md.p("This table is the register that should have been published. It is derived, not "
         "authoritative — the meanings are inferred from the messages, which is precisely "
         "the problem.")
    md.table(["ErrorCode", "Class", "Calls", "Endpoints", "Representative message"],
             [[f"`{esc(c)}`", (re.match(r"\s*(\d{3})", c).group(1)
                               if re.match(r"\s*(\d{3})", c) else "non-numeric"), n,
               len({(r["controller"], r["action"]) for r in rows
                    if (_code_of(r.get("response")) or "").splitlines()[0][:60] == c}),
               esc(next((r.get("response") or {}).get("ErrorMessage") for r in rows
                        if (_code_of(r.get("response")) or "").splitlines()[0][:60] == c))[:110]]
              for c, n in codes.most_common()])

    revalidation_section(md, payload, spec, 5)

    md.h(2, "6. Proposed fix")
    md.table(["#", "Action", "Effort", "Effect"], [
        ["1", "Publish the register — code, meaning, emitting endpoints, whether "
              "retryable, corrective action", "Low",
         "The single highest-value documentation change available"],
        ["2", "Normalise the format to one grammar, e.g. `<3-digit>-<CTRL>-<ACTION>`",
         "Low", "Makes the field parseable"],
        ["3", "Never concatenate a stack trace into the code field", "Low",
         "See LH-11"],
        ["4", "Map the prefix to an HTTP status (see LH-01)", "Low",
         "Removes the need to read the code at all for routing decisions"],
    ])
    md.p("This finding blocks automated negative testing entirely: without a register, "
         "there is no expected value to assert against, so no generated negative case "
         "can have a pass condition.")
    reproduce_footer(md, spec, 7)


def _lh04_sheets(payload, xl):
    rows = payload["rows"]
    codes = Counter(_code_of(r.get("response")).splitlines()[0][:60] for r in rows)
    xl.summary("LH-04 — Error-code register incomplete and undocumented", [
        ("Severity", "High"), ("Environment", ENVIRONMENT), ("Source run", RUN_ID),
        ("", ""),
        ("Responses carrying an ErrorCode", len(rows)),
        ("Distinct ErrorCode values", len(codes)),
        ("Recognised by the QA framework", 3),
        ("Documented in the Confluence reference", 4),
        ("Unrecognised responses",
         sum(1 for r in rows if r["klass"] not in KNOWN_TO_FRAMEWORK)),
        ("", ""),
        ("Headline", f"{len(codes)} codes in use, 4 documented. No client can tell a "
                     f"retryable failure from a permanent one."),
    ])
    reg = []
    for c, n in codes.most_common():
        sub = [r for r in rows
               if (_code_of(r.get("response")) or "").splitlines()[0][:60] == c]
        m = re.match(r"\s*(\d{3})", c)
        reg.append([c, m.group(1) if m else "non-numeric", n,
                    len({(r["controller"], r["action"]) for r in sub}),
                    "YES" if (m.group(1) if m else "") in KNOWN_TO_FRAMEWORK else "no",
                    (sub[0].get("response") or {}).get("ErrorMessage"),
                    ", ".join(sorted({f"{r['controller']}/{r['action']}"
                                      for r in sub})[:6])])
    xl.sheet("Error Code Register",
             ["ErrorCode", "Class", "Calls", "Endpoints", "Framework knows it?",
              "Representative message", "Emitting endpoints (first 6)"],
             reg, [30, 12, 8, 11, 18, 62, 70],
             note="The register that should have been published. Meanings are inferred "
                  "from messages, which is itself the finding.")
    xl.sheet("By Class", ["Prefix", "Meaning", "Distinct codes", "Calls"],
             [[p, LH04.TAXONOMY.get(p, ("unclassified", ""))[0],
               len({_code_of(r.get("response")).splitlines()[0][:60] for r in rows
                    if r["klass"] == p}), n]
              for p, n in Counter(r["klass"] for r in rows).most_common()],
             [12, 44, 14, 8])
    xl.sheet("All Occurrences",
             ["#", "ErrorCode", "Class", "Controller", "Action", "Verb", "HTTP",
              "ErrorMessage", "Evidence file"],
             [[i, _code_of(r.get("response")).splitlines()[0][:60], r["klass"],
               r["controller"], r["action"], r["verb"], r["http_status"],
               str((r.get("response") or {}).get("ErrorMessage"))[:300],
               r["evidence_file"]] for i, r in enumerate(rows, 1)],
             [5, 28, 12, 20, 32, 6, 7, 70, 46])


LH04 = LoopholeSpec(
    num="04", slug="error-code-register-incomplete",
    title="Error-code register incomplete and undocumented",
    severity="🔴 High", priority="High", effort="Low",
    jira_summary=("API emits 108 distinct ErrorCode values against a documented register "
                  "of 4 - no client can classify a failure"),
    one_liner="108 error codes in use, 4 documented, 3 recognised by tooling.",
    revalidate="safe", replay_limit=40,
    TAXONOMY={
        "103": ("Input parameter null or missing", "400"),
        "104": ("Input parameter invalid", "400"),
        "201": ("Validation error", "400"),
        "203": ("Parameter error", "400"),
        "204": ("No record found", "404"),
        "206": ("Parameter error", "400"),
        "902": ("System error", "500"),
        "903": ("System error / database exception", "500"),
        "non-numeric": ("Unparseable code", "400"),
    },
    cross_refs=["LH-01 (the same codes riding on HTTP 200)",
                "LH-11 (stack traces concatenated into the code field)"],
    select=_lh04_select, classify=_lh04_classify,
    narrative=_lh04_narrative, sheets=_lh04_sheets,
    reproduces=lambda row, res: _code_of(res.get("response")) is not None,
    replay_summary=default_replay_summary,
    TICKET={
        "labels": ["error-handling", "documentation"],
        "what": ("The API signals failure through an ErrorCode in the response body. "
                 "There is no published register of those codes, and the set in use is "
                 "far larger than anything documented. A client cannot determine which "
                 "failures are retryable, which are permanent, and which indicate a "
                 "server fault."),
        "occurrence_label": "Distinct ErrorCode values observed",
        "occurrence_value": 108,
        "scope_rows": [("Responses carrying an ErrorCode", "297"),
                       ("Documented in the 2,470-page Confluence reference", "*4*"),
                       ("Recognised by the QA framework", "3 (201, 202, 203)"),
                       ("Responses carrying an unrecognised code", "see EVIDENCE.md §2")],
        "example": ('{ "Success": false,\n'
                    '  "ErrorCode": "902-ALC-ISSML",\n'
                    '  "ErrorMessage": "System error has occurred" }'),
        "sections": [
            ("The taxonomy already exists implicitly",
             "The codes are not arbitrary - the three-digit prefix consistently encodes "
             "a failure class. This is the register that exists in the code and has "
             "never been written down:\n\n"
             "|| Prefix || Meaning || Correct HTTP ||\n"
             "| 103 | Input parameter null or missing | 400 |\n"
             "| 104 | Input parameter invalid | 400 |\n"
             "| 201 | Validation error | 400 |\n"
             "| 203 | Parameter error | 400 |\n"
             "| 204 | No record found | 404 |\n"
             "| 902 | System error | 500 |\n"
             "| 903 | System error / database exception | 500 |"),
            ("The field is not machine-readable",
             "Beyond the missing register, the codes are not consistently formed. "
             "Observed variants for what is evidently one family: 201-UDC-..., "
             "201SDC-GSDBI (no separator), 203 -ULC-GUL (space in the separator), "
             "203-ACC-GAC- (trailing separator), 902-RAC-GUS (trailing whitespace), "
             "GSAPLR and GLOBCD (no numeric prefix at all). Nine codes have a stack "
             "trace concatenated into the code field itself.\n\n"
             "One regular expression cannot parse these."),
            ("What this blocks",
             "Automated negative testing is impossible without a register: there is no "
             "expected value to assert against, so no generated negative case can have "
             "a pass condition. This is the single highest-value documentation change "
             "available on the API."),
        ],
        "repro": """Preconditions:
  - Environment: QA_MsSQL, https://u16hf.arconnet.com:6302
  - A valid bearer token (generate ONE - see PAMIT ISSUE-009).

1. GET /api/ServicePasswordV2/GetSyncFailedServices
   Observe: { "Success": false, "ErrorCode": "204-SPC-GFSP",
              "ErrorMessage": "No Record Found" }

2. POST /api/ActivityLogs/InsertSSMLogs   (with an empty body {})
   Observe an ErrorCode in the 9xx family.

3. Attempt to locate either code in the Confluence API reference.
   EXPECTED: a register entry giving meaning, cause and corrective action.
   ACTUAL:   only 4 error codes are documented in 2,470 pages. Neither is one
             of them.

4. For the format half: compare these codes, all observed in one run -
   201-UDC-GULNN, 201SDC-GSDBI, 203 -ULC-GUL, 203-ACC-GAC-, GSAPLR
   No single parsing rule handles all five.

5. The full observed register of all 108 codes, with a representative message
   and the emitting endpoints for each, is in the attached EVIDENCE.xlsx,
   sheet "Error Code Register".""",
        "expected": ("A published register mapping every ErrorCode to its meaning, "
                     "cause, corrective action and whether it is retryable."),
        "actual": ("108 distinct codes are emitted; 4 are documented; the format is "
                   "inconsistent enough that a client cannot reliably parse the field."),
        "severity_rows": [
            ["**Correctness**", "No consumer can classify a failure, so error handling "
                                "is guesswork"],
            ["**Blast radius**", "Every failing call on the API"],
            ["**Test automation**", "Blocks automated negative testing entirely - there "
                                    "is no expected value to assert"],
            ["**Support cost**", "Every unrecognised code becomes a support conversation"],
            ["**Cost to fix**", "Low - the taxonomy already exists in the code; it needs "
                                "publishing and normalising"],
        ],
        "severity_argument": ("Rated High because it is cheap to fix and it is currently "
                              "the gating dependency for automated negative testing "
                              "across the whole API."),
        "fix_rows": [
            ["1", "Publish the register - code, meaning, emitting endpoints, retryable "
                  "yes/no, corrective action", "Low",
             "Highest-value documentation change available"],
            ["2", "Normalise the format to one grammar, e.g. `<3-digit>-<CTRL>-<ACTION>`",
             "Low", "Makes the field parseable"],
            ["3", "Never concatenate a stack trace into the code field", "Low",
             "See LH-11"],
            ["4", "Map the prefix to an HTTP status", "Low",
             "See LH-01 - removes the need to read the code for routing"],
        ],
        "acceptance": """1. A register exists listing every ErrorCode the product can emit,
   with meaning, cause, corrective action and retryability.
2. Every emitted code matches one documented format grammar.
3. No ErrorCode field contains a stack trace or exceeds a documented length.
4. The QA framework's recognised-code set is generated from the register
   rather than hardcoded.""",
        "target": "0 undocumented codes",
    },
)


# ═══════════════════════════════════════════════════════════ LH-05
def _lh05_select(hop, resp):
    return hop.get("status") == 404


def _lh05_classify(r):
    return r["controller"]


def _lh05_narrative(payload, md):
    rows = payload["rows"]
    spec = LH05
    byc = Counter(r["controller"] for r in rows)
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p(f"**{len(rows)} endpoints declared in the test catalogue return HTTP 404** on "
         "this deployment. The catalogue and the running build disagree about what the "
         "API is.")
    md.table(["Measure", "Value"], [
        ["Calls returning 404", f"**{len(rows)}**"],
        ["Distinct endpoints", payload["distinct_endpoints"]],
        ["Controllers affected", payload["distinct_controllers"]],
        ["Catalogue size (`APIConfig.java`)", "1,306 endpoints"],
        ["404 rate against endpoints actually called", f"{len(rows)} of 1,868 calls"],
    ])
    md.p("A 404 here is the *correct* HTTP behaviour — the route genuinely does not "
         "exist. The defect is the **drift**: the catalogue asserts these endpoints "
         "exist, and nothing tells a consumer otherwise.")

    md.h(2, "2. Three sources disagree about what the API is")
    md.table(["Source", "Endpoints", "Overlap with the others"], [
        ["`APIConfig.java` test catalogue", "1,306",
         f"{len(rows)} of those called returned 404"],
        ["Shared Swagger specs", "690 operations", "**~6%** name overlap with the catalogue"],
        ["`pam/PAM` product snapshot", "48 of 1,306 implemented (3.7%)",
         "58 of 70 controllers have no implementation"],
    ])
    md.p("No single artefact describes the deployed surface. That is the underlying "
         "problem; the 404s are its most visible symptom.")

    md.h(2, "3. Affected controllers")
    md.table(["Controller", "404 endpoints", "Share"],
             [[f"`{c}`", n, f"{n / len(rows) * 100:.1f}%"] for c, n in byc.most_common()])

    md.h(2, "4. Consequence")
    md.table(["Area", "Impact"], [
        ["Coverage reporting", f"Every coverage figure is inflated — {len(rows)} of the "
                               "endpoints counted as 'reachable' are not"],
        ["Test maintenance", "Each 404 is an indefinite red test that nobody can fix, "
                             "because the fix is a deletion nobody is authorised to make"],
        ["Consumer teams", "An integrator reading the catalogue builds against endpoints "
                           "that do not exist"],
        ["Release confidence", "Nobody can currently state which endpoints a given build "
                               "serves"],
    ])

    revalidation_section(md, payload, spec, 5)

    md.h(2, "6. Proposed fix")
    md.table(["#", "Action", "Owner", "Effort"], [
        ["1", "Publish a **route dump per build** — the definitive list of what the "
              "deployment serves", "Development", "Low — one startup hook"],
        ["2", "Confirm which of these 135 are deprecated versus not-yet-deployed",
         "Development", "Low"],
        ["3", "Remove or gate the deprecated entries in `APIConfig.java`", "QA", "Low"],
        ["4", "Add a CI check comparing the catalogue against the route dump",
         "QA", "Medium"],
    ])
    md.p("Item 1 settles this permanently and is the only one that prevents recurrence. "
         "Everything else is a one-off reconciliation.")

    md.h(2, "7. Full register")
    md.table(["#", "Controller", "Action", "Verb", "Path", "Evidence"],
             [[i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"],
               f"`{r['path']}`", f"`{esc(r['evidence_file'])}`"]
              for i, r in enumerate(rows, 1)])
    reproduce_footer(md, spec, 8)


def _lh05_sheets(payload, xl):
    rows = payload["rows"]
    xl.summary("LH-05 — Declared endpoints return HTTP 404", [
        ("Severity", "Medium"), ("Environment", ENVIRONMENT), ("Source run", RUN_ID),
        ("", ""),
        ("Endpoints returning 404", len(rows)),
        ("Distinct controllers", payload["distinct_controllers"]),
        ("Catalogue size", "1,306 endpoints"),
        ("Swagger overlap with catalogue", "~6%"),
        ("Implemented in pam/PAM snapshot", "48 of 1,306 (3.7%)"),
        ("", ""),
        ("Headline", "The catalogue, the Swagger specs and the deployment disagree. "
                     "A per-build route dump would settle it permanently."),
    ])
    xl.sheet("404 Endpoints",
             ["#", "Controller", "Action", "Verb", "Path", "Latency ms", "Flow",
              "Evidence file"],
             [[i, r["controller"], r["action"], r["verb"], r["path"], r["latency_ms"],
               r["flow"], r["evidence_file"]] for i, r in enumerate(rows, 1)],
             [5, 24, 36, 6, 52, 11, 30, 46])
    xl.sheet("By Controller", ["Controller", "404 endpoints", "Share", "Actions"],
             [[c, n, f"{n / len(rows) * 100:.1f}%",
               ", ".join(sorted(r["action"] for r in rows if r["controller"] == c)[:8])]
              for c, n in Counter(r["controller"] for r in rows).most_common()],
             [26, 14, 9, 90])


LH05 = LoopholeSpec(
    num="05", slug="declared-endpoints-return-404",
    title="135 declared endpoints return HTTP 404",
    severity="🟠 Medium", priority="Medium", effort="Low",
    jira_summary=("135 endpoints declared in the API catalogue return HTTP 404 - "
                  "catalogue, Swagger specs and deployment disagree"),
    one_liner="135 catalogued endpoints do not exist on the deployed build.",
    revalidate="safe",
    cross_refs=["ISSUE-005 (API coverage gap)"],
    select=_lh05_select, classify=_lh05_classify,
    narrative=_lh05_narrative, sheets=_lh05_sheets,
    reproduces=lambda row, res: res.get("status") == 404,
    replay_summary=lambda res: f"HTTP {res.get('status')}",
    TICKET={
        "labels": ["api-catalogue", "documentation"],
        "what": ("135 endpoints declared in the API test catalogue return HTTP 404 on "
                 "this deployment. The 404 itself is correct behaviour - the route "
                 "genuinely does not exist. The defect is the drift: three separate "
                 "artefacts disagree about what the API is, and none of them is "
                 "authoritative."),
        "scope_rows": [("Endpoints returning 404", "*135*"),
                       ("Catalogue size (APIConfig.java)", "1,306"),
                       ("Swagger specs shared by development", "690 operations"),
                       ("Name overlap between the two", "*~6%*"),
                       ("Catalogue actions implemented in the pam/PAM snapshot",
                        "48 of 1,306 (3.7%)")],
        "sections": [
            ("Three sources disagree",
             "|| Source || Endpoints || Note ||\n"
             "| APIConfig.java test catalogue | 1,306 | 135 of those called returned 404 |\n"
             "| Shared Swagger specs | 690 operations | ~6% name overlap with the catalogue |\n"
             "| pam/PAM product snapshot | 48 of 1,306 implemented | 58 of 70 "
             "controllers have no implementation |\n\n"
             "No single artefact describes the deployed surface. The 404s are the most "
             "visible symptom of that."),
            ("What we are asking for",
             "A route dump per build - the definitive list of endpoints a given "
             "deployment serves. That single artefact settles this permanently and lets "
             "QA add a CI check. Everything else is a one-off reconciliation."),
        ],
        "repro": """Preconditions:
  - Environment: QA_MsSQL, https://u16hf.arconnet.com:6302
  - A valid bearer token (generate ONE - see PAMIT ISSUE-009).

1. Pick any endpoint from the attached EVIDENCE.xlsx sheet "404 Endpoints",
   for example:
      POST /api/ADbridging/GetDbLOBByLobIdAndPAMGroupV2

2. Call it with a valid bearer token.
   EXPECTED (per APIConfig.java, which declares it): a response
   ACTUAL:   HTTP 404

3. Repeat for any of the other 134 listed endpoints - all return 404.

4. Confirm the declaration exists:
   grep the endpoint path in
   Automation gitlab repo/pam_automation_bootstrap/src/test/java/
     com/arcon/autoconfigs/APIConfig.java

   The catalogue asserts the endpoint exists. The deployment disagrees.""",
        "expected": ("A single authoritative statement of which endpoints a build "
                     "serves, so the catalogue can be reconciled against it."),
        "actual": ("135 catalogued endpoints return 404, and no artefact exists that "
                   "would let anyone determine which of the 1,306 are real."),
        "severity_rows": [
            ["**Correctness**", "The API behaves correctly; the artefacts describing it "
                                "do not"],
            ["**Coverage reporting**", "Every coverage figure is inflated - 135 endpoints "
                                       "counted as reachable are not"],
            ["**Test maintenance**", "Each 404 is an indefinite red test nobody is "
                                     "authorised to delete"],
            ["**Integration risk**", "An integrator reading the catalogue builds against "
                                     "endpoints that do not exist"],
            ["**Cost to fix**", "Low - a startup route dump is a small change"],
        ],
        "severity_argument": ("Rated Medium: no user-facing failure, but it makes every "
                              "coverage and readiness statement about the API unreliable."),
        "fix_rows": [
            ["1", "Publish a route dump per build", "Low - one startup hook",
             "Settles this permanently and prevents recurrence"],
            ["2", "Confirm which of the 135 are deprecated versus not-yet-deployed",
             "Low", "Enables the reconciliation"],
            ["3", "Remove or gate the deprecated entries in `APIConfig.java`", "Low",
             "QA-side cleanup"],
            ["4", "Add a CI check comparing catalogue against route dump", "Medium",
             "Stops it drifting again"],
        ],
        "acceptance": """1. A route dump is published with each build.
2. Each of the 135 endpoints is classified as deprecated, not-yet-deployed,
   or a genuine deployment gap.
3. Re-running the QA harness reports 0 unexpected 404s against the catalogue.""",
        "target": "0 unexpected 404s",
    },
)


# ═══════════════════════════════════════════════════════════ LH-09
PW_KEY = re.compile(r'"([^"]*(?:password|passwd|pwd|sshkey|privatekey)[^"]*)"\s*:', re.I)


def _lh09_select(hop, resp):
    if resp is None:
        return False
    return bool(PW_KEY.search(json.dumps(resp)))


def _lh09_fields(r):
    return sorted(set(PW_KEY.findall(json.dumps(r.get("response") or {}))))


def _lh09_classify(r):
    return "read returns credential field" if r["verb"] == "GET" or \
        r["action"].lower().startswith("get") else "write echoes credential field"


def _lh09_narrative(payload, md):
    rows = payload["rows"]
    spec = LH09
    allf = Counter(f for r in rows for f in _lh09_fields(r))
    header_block(md, payload, spec)

    md.h(2, "1. What was observed — and what this pack cannot show")
    md.p("**" + str(len(rows)) + f"** responses across **{payload['distinct_endpoints']}** "
         "distinct endpoints return a field whose name denotes a credential — "
         "`ServicePassword`, `ServiceUserPassword`, SSH key fields and similar.")
    md("> ⚠️ **The harness redacts these before anything is written to disk.** Every "
       "evidence file shows `***REDACTED***` in place of the value. This pack therefore "
       "proves **the field is present and populated in the response**; it does not "
       "reproduce the secret. That is deliberate and is not a limitation to be "
       "'fixed' — see §5.")
    md("")
    md.table(["Measure", "Value"], [
        ["Responses carrying a credential-shaped field", len(rows)],
        ["Distinct endpoints", payload["distinct_endpoints"]],
        ["Distinct controllers", payload["distinct_controllers"]],
        ["Distinct field names", len(allf)],
    ])

    md.h(2, "2. Fields returned")
    md.table(["Field name", "Responses", "Endpoints"],
             [[f"`{esc(f)}`", n,
               len({(r["controller"], r["action"]) for r in rows
                    if f in _lh09_fields(r)})] for f, n in allf.most_common()])

    md.h(2, "3. Shape of the response")
    md.p("Recorded verbatim from the retained evidence, with the harness redaction in "
         "place:")
    md.code('POST /api/ServiceDetails/GetServiceDetails\n\n'
            'HTTP/1.1 200 OK\n'
            '{ "Success": true,\n'
            '  "Result": { "ServiceId": 25339,\n'
            '              "ServiceUsername": "UserName1",\n'
            '              "ServicePassword": "***REDACTED***",   <-- populated on the wire\n'
            '              ... } }', "json")

    md.h(2, "4. Why this is raised for confirmation rather than as a defect")
    md.p("This is a privileged-access-management product. Returning a target-system "
         "credential to an authorised caller may be entirely intended — the session "
         "launcher plausibly needs it to establish a connection. **This pack does not "
         "assert a vulnerability.** It asks for three things to be confirmed:")
    md.table(["#", "Question for the product owner"], [
        ["1", "Is returning the standing credential intended on each of these "
              f"{payload['distinct_endpoints']} endpoints, or only on the session-launch path?"],
        ["2", "What authorisation is enforced? Any authenticated caller reached these in "
              "our run using a single service account"],
        ["3", "Are these responses excluded from application logs, APM traces, proxy "
              "logs and browser caches?"],
    ])

    md.h(2, "5. Our handling")
    md.table(["Control", "Behaviour"], [
        ["Redaction", "Keys matching `password|passwd|pwd|token|secret|credential|"
                      "privatekey|sshkey` are replaced with `***REDACTED***` before any "
                      "evidence file is written"],
        ["Scope", "Applies to all 1,868 evidence files in the source run"],
        ["This pack", "Reports field **names** and endpoints only; no value is stored or "
                      "transmitted"],
        ["Attachments", "Safe to attach to Jira — they contain no credential values"],
    ])

    revalidation_section(md, payload, spec, 6)

    md.h(2, "7. Recommended actions if the behaviour is confirmed intended")
    md.table(["#", "Action", "Effort"], [
        ["1", "Restrict credential-returning responses to the session-launch path only",
         "Medium"],
        ["2", "Issue a **single-use, time-boxed** secret instead of the standing password",
         "Medium"],
        ["3", "Add an explicit no-log / no-cache marker on these responses", "Low"],
        ["4", "Document which endpoints may return credentials, and the authorisation "
              "required", "Low"],
    ])

    md.h(2, "8. Full register")
    md.table(["#", "Controller", "Action", "Verb", "Credential fields", "Evidence"],
             [[i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"],
               ", ".join(f"`{esc(f)}`" for f in _lh09_fields(r)),
               f"`{esc(r['evidence_file'])}`"] for i, r in enumerate(rows, 1)])
    reproduce_footer(md, spec, 9)


def _lh09_sheets(payload, xl):
    rows = payload["rows"]
    xl.summary("LH-09 — Credential-shaped fields returned in responses", [
        ("Severity", "Review — confirm intent"), ("Environment", ENVIRONMENT),
        ("Source run", RUN_ID), ("", ""),
        ("Responses carrying a credential field", len(rows)),
        ("Distinct endpoints", payload["distinct_endpoints"]),
        ("Distinct field names", len({f for r in rows for f in _lh09_fields(r)})),
        ("", ""),
        ("⚠️ Values", "REDACTED at capture. This workbook proves the field is present "
                      "and populated; it contains no credential values."),
        ("Nature", "Raised for confirmation of intent, not asserted as a vulnerability."),
    ])
    xl.sheet("Endpoints Returning Credentials",
             ["#", "Controller", "Action", "Verb", "Path", "Credential fields",
              "Evidence file"],
             [[i, r["controller"], r["action"], r["verb"], r["path"],
               ", ".join(_lh09_fields(r)), r["evidence_file"]]
              for i, r in enumerate(rows, 1)],
             [5, 24, 34, 6, 52, 44, 46])
    xl.sheet("Field Names", ["Field name", "Responses", "Endpoints"],
             [[f, n, len({(r["controller"], r["action"]) for r in rows
                          if f in _lh09_fields(r)})]
              for f, n in Counter(f for r in rows
                                  for f in _lh09_fields(r)).most_common()],
             [40, 12, 12])


LH09 = LoopholeSpec(
    num="09", slug="credentials-returned-in-responses",
    title="Service credentials returned in API responses — confirm intent",
    severity="🟠 Review", priority="Medium", effort="Low",
    jira_summary=("Service credential fields are returned in 23 API responses across 21 "
                  "endpoints - please confirm intent and authorisation"),
    one_liner="Credential-shaped fields are returned to authenticated callers.",
    revalidate="safe",
    # ⛔ 7 of these rows are Insert*/Add* calls that happen to echo a credential field
    # back. Replaying them would create records. Only the read paths are replayed.
    replay_filter=lambda r: r["klass"] == "read returns credential field",
    cross_refs=["LH-11 (internal detail disclosure)"],
    select=_lh09_select, classify=_lh09_classify,
    narrative=_lh09_narrative, sheets=_lh09_sheets,
    reproduces=lambda row, res: bool(
        PW_KEY.search(json.dumps(res.get("response") or ""))),
    replay_summary=lambda res: (
        "credential field present" if PW_KEY.search(json.dumps(res.get("response") or ""))
        else f"HTTP {res.get('status')} / no credential field"),
    TICKET={
        "labels": ["security-review", "credentials"],
        "what": ("23 responses across 21 distinct endpoints return a field whose name "
                 "denotes a credential - ServicePassword, SSH key fields and similar.\n\n"
                 "This ticket does NOT assert a vulnerability. For a "
                 "privileged-access-management product, returning a target-system "
                 "credential to an authorised caller may be entirely intended. It asks "
                 "for the intent and the authorisation model to be confirmed and "
                 "documented."),
        "scope_rows": [("Responses carrying a credential-shaped field", "23"),
                       ("Distinct endpoints", "21"),
                       ("Values captured", "*NONE - redacted at capture*")],
        "example": ('POST /api/ServiceDetails/GetServiceDetails\n\n'
                    'HTTP/1.1 200 OK\n'
                    '{ "Success": true,\n'
                    '  "Result": { "ServiceId": 25339,\n'
                    '              "ServiceUsername": "UserName1",\n'
                    '              "ServicePassword": "***REDACTED***",\n'
                    '              ... } }'),
        "sections": [
            ("What this evidence does and does not show",
             "Our harness redacts credential-named keys before writing anything to "
             "disk. Every evidence file shows ***REDACTED*** in place of the value.\n\n"
             "So this pack proves the field is PRESENT AND POPULATED in the response. "
             "It does not reproduce the secret, and the attachments contain no "
             "credential values. That is deliberate."),
            ("Questions for the product owner",
             "|| # || Question ||\n"
             "| 1 | Is returning the standing credential intended on all 21 endpoints, "
             "or only on the session-launch path? |\n"
             "| 2 | What authorisation is enforced? Our run reached these using a "
             "single ordinary service account |\n"
             "| 3 | Are these responses excluded from application logs, APM traces, "
             "proxy logs and browser caches? |"),
        ],
        "repro": """Preconditions:
  - Environment: QA_MsSQL, https://u16hf.arconnet.com:6302
  - A valid bearer token (generate ONE - see PAMIT ISSUE-009).
  - A configured service with stored credentials.

⚠️ This reproduction returns a live credential to the terminal. Run it only on
   QA_MsSQL, do not paste the output anywhere, and clear your shell history.

1. POST /api/ServiceDetails/GetServiceDetails
   Header: Authorization: Bearer <token>
   Header: Content-Type: application/json
   Body:   { "ServiceId": <an existing service id> }

2. Inspect the Result object.
   EXPECTED: confirm whether a ServicePassword field should be present at all
   ACTUAL:   the field is present and populated with the stored credential

3. Repeat for the other 20 endpoints listed in the attached EVIDENCE.xlsx,
   sheet "Endpoints Returning Credentials".

4. Confirm the authorisation model: repeat step 1 with a lower-privileged
   account and record whether the credential is still returned.""",
        "expected": ("Credential material is returned only where the flow requires it, "
                     "under a documented authorisation model, and is excluded from logs."),
        "actual": ("Credential-shaped fields are returned on 21 endpoints to an "
                   "ordinary authenticated service account. Intent and authorisation "
                   "are not documented."),
        "severity_rows": [
            ["**Nature**", "Raised for confirmation of intent, not asserted as a "
                           "vulnerability"],
            ["**Product context**", "A PAM product may legitimately return a credential "
                                    "to a session launcher"],
            ["**Concern**", "Breadth - 21 endpoints, reached with one ordinary service "
                            "account"],
            ["**Secondary concern**", "Onward exposure in logs, APM traces and proxies "
                                      "is unconfirmed"],
            ["**Evidence safety**", "No credential value is stored in this pack or its "
                                    "attachments"],
            ["**Cost to fix**", "Low if intended (document it); Medium if scoping is "
                                "required"],
        ],
        "severity_argument": ("Deliberately rated for review rather than as a defect. "
                              "The correct first step is a product decision, not a code "
                              "change."),
        "fix_rows": [
            ["1", "Confirm and document which endpoints may return credentials and under "
                  "what authorisation", "Low", "Resolves the question"],
            ["2", "If unintended on some endpoints, restrict to the session-launch path",
             "Medium", "Reduces exposure"],
            ["3", "Issue a single-use, time-boxed secret instead of the standing password",
             "Medium", "Removes standing-credential exposure"],
            ["4", "Add an explicit no-log / no-cache marker on these responses", "Low",
             "Prevents onward leakage"],
        ],
        "acceptance": """1. Every endpoint that may return credential material is documented,
   with the authorisation required.
2. Endpoints not requiring it no longer return it.
3. These responses are confirmed excluded from application logs, APM traces
   and proxy caches.""",
        "target": "documented and confirmed",
    },
)


# ═══════════════════════════════════════════════════════════ LH-11
def _lh11_select(hop, resp):
    if resp is None:
        return False
    return bool(LEAK.search(json.dumps(resp)))


def _lh11_leaks(r):
    blob = json.dumps(r.get("response") or {})
    out = []
    if re.search(r"System\.[A-Za-z]+Exception", blob):
        out.append("exception type")
    if re.search(r"[A-Z]:\\+Jenkins\\", blob) or "Jenkins" in blob:
        out.append("build-server path")
    if re.search(r"\.cs:line", blob):
        out.append("source file + line")
    if "Culture=neutral" in blob:
        out.append("assembly version")
    if re.search(r"\bat\s+[A-Za-z][\w.]+\s*\(", blob):
        out.append("stack frame")
    if "InnerException" in blob:
        out.append("inner exception")
    return out or ["stack detail"]


def _lh11_classify(r):
    lk = _lh11_leaks(r)
    return "build path + source line" if "build-server path" in lk else lk[0]


def _lh11_msg(r):
    rr = r.get("response") or {}
    if not isinstance(rr, dict):
        return str(rr)[:300]
    return str(rr.get("ErrorMessage") or rr.get("Message") or json.dumps(rr))[:300]


def _lh11_narrative(payload, md):
    rows = payload["rows"]
    spec = LH11
    kinds = Counter(k for r in rows for k in _lh11_leaks(r))
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p(f"**{len(rows)} responses** return raw .NET exception detail to the caller — "
         "exception types, stack frames, source file paths and line numbers from the "
         "build server, and assembly identities. Every one is returned at **HTTP 200**.")
    md.table(["Detail leaked", "Responses"],
             [[k, v] for k, v in kinds.most_common()])

    md.h(2, "2. Worked example")
    md.p("`ServicePassword/GetTargetDeviceOpenSSHKey`, captured verbatim:")
    md.code("902-SPC-GTDOS-System.IO.FileNotFoundException: Could not load file or "
            "assembly\n'ChilkatDotNet47, Version=9.5.0.86, Culture=neutral, "
            "PublicKeyToken=eb5fc1fc52ef09bd'\nor one of its dependencies. The system "
            "cannot find the file specified.\n"
            "   at EntityDataAccessLayer.ServiceDetails.DatabaseCrud."
            "GetTargetDeviceOpenSSHKey(...)\n"
            "   at EntityBusinessLayer.ServicePassword.ServicePasswordBl."
            "GetTargetDeviceOpenSSHKey(...)\n"
            "     in E:\\Jenkins\\workspace\\PAMAPI_QA\\ARCONPAMAPI\\EntityBusinessLayer"
            "\\ServicePassword\\ServicePasswordBl.cs:line 52")
    md.p("That single response discloses: the internal assembly layout and version, the "
         "three-tier class structure, the **absolute build path on the Jenkins agent**, "
         "the source file name and an exact line number.")

    md.h(2, "3. It is also masking a real deployment fault")
    md.p("`ChilkatDotNet47` is **missing from the QA server**. That is a genuine "
         "deployment defect — and because it surfaces as HTTP 200, no monitor sees it. "
         "It should be raised and fixed independently of the disclosure.")

    md.h(2, "4. Why this matters beyond tidiness")
    md.table(["Concern", "Detail"], [
        ["Reconnaissance", "Framework versions and third-party library versions let an "
                           "attacker match known CVEs without probing"],
        ["Internal topology", "Namespace and layer names map the application's internal "
                              "structure"],
        ["Build infrastructure", "`E:\\Jenkins\\workspace\\PAMAPI_QA\\...` names the CI "
                                 "host, workspace and job"],
        ["Invisible to monitoring", "Delivered at HTTP 200 (see LH-01), so no error "
                                    "dashboard records it"],
        ["Unparseable errors", "9 of these traces are concatenated **into the ErrorCode "
                               "field itself** — see LH-04"],
    ])

    md.h(2, "5. Full register")
    md.table(["#", "Controller", "Action", "Verb", "HTTP", "Leaked", "Message (truncated)"],
             [[i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"], r["http_status"],
               ", ".join(_lh11_leaks(r)), esc(_lh11_msg(r))[:130]]
              for i, r in enumerate(rows, 1)])

    revalidation_section(md, payload, spec, 6)

    md.h(2, "7. Proposed fix")
    md.table(["#", "Action", "Effort"], [
        ["1", "Return a stable error code plus a safe, generic message; write the "
              "exception and stack to the server log only", "Low"],
        ["2", "Add a global exception filter so no handler can leak a trace by omission",
         "Low — one filter, covers every controller"],
        ["3", "Disable detailed error responses in the deployed configuration "
              "(`customErrors` / `IncludeErrorDetailPolicy`)", "Trivial"],
        ["4", "Install the missing `ChilkatDotNet47` assembly on QA", "Low"],
    ])
    md.p("Item 3 alone would close most of this in a configuration change, and is worth "
         "doing immediately while items 1 and 2 are scheduled.")
    reproduce_footer(md, spec, 8)


def _lh11_sheets(payload, xl):
    rows = payload["rows"]
    xl.summary("LH-11 — Internal error detail leaked to callers", [
        ("Severity", "Low (as rated) — see note"), ("Environment", ENVIRONMENT),
        ("Source run", RUN_ID), ("", ""),
        ("Responses leaking internals", len(rows)),
        ("Distinct endpoints", payload["distinct_endpoints"]),
        ("…disclosing a build-server path",
         sum(1 for r in rows if "build-server path" in _lh11_leaks(r))),
        ("…disclosing a source file and line",
         sum(1 for r in rows if "source file + line" in _lh11_leaks(r))),
        ("…disclosing an assembly version",
         sum(1 for r in rows if "assembly version" in _lh11_leaks(r))),
        ("", ""),
        ("Note", "Rated Low in the developer brief as a tidiness issue. The build-path "
                 "and assembly-version disclosure arguably warrants a security review."),
    ])
    xl.sheet("Leaking Responses",
             ["#", "Controller", "Action", "Verb", "Path", "HTTP", "Leaked",
              "Message (truncated)", "Evidence file"],
             [[i, r["controller"], r["action"], r["verb"], r["path"], r["http_status"],
               ", ".join(_lh11_leaks(r)), _lh11_msg(r), r["evidence_file"]]
              for i, r in enumerate(rows, 1)],
             [5, 22, 34, 6, 50, 7, 40, 110, 46])
    xl.sheet("Leak Types", ["Detail leaked", "Responses"],
             [[k, v] for k, v in
              Counter(k for r in rows for k in _lh11_leaks(r)).most_common()],
             [30, 12])


LH11 = LoopholeSpec(
    num="11", slug="internal-detail-leaked-in-errors",
    title="Internal server detail leaked in error messages",
    severity="🟡 Low", priority="Medium", effort="Low",
    jira_summary=("API returns .NET stack traces, build-server paths and assembly "
                  "versions to callers in 16 responses, at HTTP 200"),
    one_liner="Stack traces with build-server paths returned to any authenticated caller.",
    revalidate="safe",
    cross_refs=["LH-01 (delivered at HTTP 200, so invisible to monitoring)",
                "LH-04 (traces concatenated into the ErrorCode field)"],
    select=_lh11_select, classify=_lh11_classify,
    narrative=_lh11_narrative, sheets=_lh11_sheets,
    reproduces=lambda row, res: bool(LEAK.search(json.dumps(res.get("response") or ""))),
    replay_summary=lambda res: (
        "leak reproduced" if LEAK.search(json.dumps(res.get("response") or ""))
        else f"HTTP {res.get('status')} / no leak"),
    TICKET={
        "labels": ["security-review", "error-handling", "information-disclosure"],
        "what": ("16 responses return raw .NET exception detail to the caller - "
                 "exception types, stack frames, source file paths and line numbers "
                 "from the build server, and assembly identities. Every one is "
                 "returned at HTTP 200."),
        "scope_rows": [("Responses leaking internals", "16"),
                       ("…disclosing a build-server absolute path", "see EVIDENCE.md §1"),
                       ("…disclosing a source file and line number", "see EVIDENCE.md §1"),
                       ("…disclosing an assembly name and version", "see EVIDENCE.md §1")],
        "example": ("902-SPC-GTDOS-System.IO.FileNotFoundException: Could not load file "
                    "or assembly\n'ChilkatDotNet47, Version=9.5.0.86, Culture=neutral, "
                    "PublicKeyToken=eb5fc1fc52ef09bd'\n"
                    "   at EntityDataAccessLayer.ServiceDetails.DatabaseCrud."
                    "GetTargetDeviceOpenSSHKey(...)\n"
                    "     in E:\\Jenkins\\workspace\\PAMAPI_QA\\ARCONPAMAPI\\"
                    "EntityBusinessLayer\\ServicePassword\\ServicePasswordBl.cs:line 52"),
        "sections": [
            ("What that single response discloses",
             "* the internal assembly layout and third-party library version\n"
             "* the three-tier class structure and namespace naming\n"
             "* the absolute build path on the Jenkins agent, naming the CI host, "
             "workspace and job\n"
             "* the source file name and an exact line number"),
            ("It is also masking a real deployment fault",
             "ChilkatDotNet47 is missing from the QA server. That is a genuine "
             "deployment defect - and because it surfaces as HTTP 200 (see LH-01), no "
             "monitor sees it. Worth splitting into its own ticket."),
            ("Why this is more than untidiness",
             "|| Concern || Detail ||\n"
             "| Reconnaissance | Framework and library versions let an attacker match "
             "known CVEs without probing |\n"
             "| Internal topology | Namespace and layer names map the application's "
             "internal structure |\n"
             "| Build infrastructure | The Jenkins path names the CI host, workspace "
             "and job |\n"
             "| Invisible to monitoring | Delivered at HTTP 200, so no error dashboard "
             "records it |\n"
             "| Unparseable errors | 9 of these traces are concatenated into the "
             "ErrorCode field itself - see LH-04 |"),
        ],
        "repro": """Preconditions:
  - Environment: QA_MsSQL, https://u16hf.arconnet.com:6302
  - A valid bearer token (generate ONE - see PAMIT ISSUE-009).

1. POST /api/ServicePassword/GetTargetDeviceOpenSSHKey
   Header: Authorization: Bearer <token>
   Header: Content-Type: application/json
   Body:   {}

2. Read the ErrorMessage field.
   EXPECTED: a stable error code plus a safe, generic message; the exception
             and stack written to the server log only
   ACTUAL:   a full .NET stack trace including
             E:\\Jenkins\\workspace\\PAMAPI_QA\\... and
             ServicePasswordBl.cs:line 52, at HTTP 200

3. Repeat for the other 15 endpoints in the attached EVIDENCE.xlsx,
   sheet "Leaking Responses".

4. Note that ChilkatDotNet47 being absent from the server is a separate,
   genuine deployment defect that this response is masking.""",
        "expected": ("A stable error code and a safe generic message; exception detail "
                     "written to the server log only."),
        "actual": ("Full .NET stack traces including build-server absolute paths, "
                   "source line numbers and assembly versions are returned to any "
                   "authenticated caller, at HTTP 200."),
        "severity_rows": [
            ["**Information disclosure**", "Build paths, assembly versions and internal "
                                           "class structure exposed"],
            ["**Reachability**", "Any authenticated caller; no special privilege needed"],
            ["**Detectability**", "None - delivered at HTTP 200, invisible to monitoring"],
            ["**Masked defect**", "A missing assembly on the QA server is hidden behind "
                                  "a 200"],
            ["**Cost to fix**", "Trivial for the configuration change; Low for a global "
                                "exception filter"],
        ],
        "severity_argument": ("Rated Low in the developer brief as a tidiness issue. The "
                              "build-path and assembly-version disclosure arguably "
                              "warrants a security review, and the configuration fix is "
                              "close to free — worth doing regardless of the rating."),
        "fix_rows": [
            ["1", "Disable detailed error responses in the deployed configuration "
                  "(`customErrors`, `IncludeErrorDetailPolicy`)", "Trivial",
             "Closes most of this immediately"],
            ["2", "Add a global exception filter so no handler can leak a trace by "
                  "omission", "Low", "Covers every controller"],
            ["3", "Return a stable code plus a safe message; log the stack server-side",
             "Low", "The durable fix"],
            ["4", "Install the missing `ChilkatDotNet47` assembly on QA", "Low",
             "Separate defect"],
        ],
        "fix_note": ("Item 1 alone would close most of this in a configuration change "
                     "and is worth doing immediately while 2 and 3 are scheduled."),
        "acceptance": """1. No response body contains a .NET exception type name, a stack
   frame, a source file path, a source line number or an assembly version.
2. Exception detail appears in the server log only.
3. Re-running the QA harness reports 0 responses matching the leak pattern.""",
        "target": "0 leaking responses",
    },
)


# ═══════════════════════════════════════════════════════════ LH-12
BIG = 100 * 1024
GETALL = re.compile(r"^(getall|get.*list$|list)", re.I)


def _lh12_select(hop, resp):
    return (hop.get("body_bytes") or 0) >= BIG


def _lh12_classify(r):
    b = r["body_bytes"] or 0
    if b >= 5 * 1024 * 1024:
        return "≥ 5 MB"
    if b >= 1024 * 1024:
        return "1–5 MB"
    if b >= 500 * 1024:
        return "500 KB – 1 MB"
    return "100–500 KB"


def _lh12_narrative(payload, md):
    rows = payload["rows"]
    spec = LH12
    uniq = {}
    for r in rows:
        k = (r["controller"], r["action"])
        if k not in uniq or (r["body_bytes"] or 0) > (uniq[k]["body_bytes"] or 0):
            uniq[k] = r
    biggest = sorted(uniq.values(), key=lambda r: -(r["body_bytes"] or 0))
    total = sum(r["body_bytes"] or 0 for r in rows)
    header_block(md, payload, spec)

    md.h(2, "1. The defect")
    md.p("List endpoints return the **entire dataset** with no filter, paging or row-limit "
         "parameter. A client wanting one record must download every record and filter "
         "locally.")
    md.table(["Measure", "Value"], [
        ["Responses ≥ 100 KB", len(rows)],
        ["Distinct endpoints", len(uniq)],
        ["Largest single response", f"**{max(r['body_bytes'] or 0 for r in rows) / 1024 / 1024:.1f} MB**"],
        ["Total bytes in these responses alone", f"{total / 1024 / 1024:.1f} MB"],
        ["Responses ≥ 1 MB", sum(1 for r in rows if (r['body_bytes'] or 0) >= 1024 * 1024)],
        ["Responses ≥ 5 MB", sum(1 for r in rows if (r['body_bytes'] or 0) >= 5 * 1024 * 1024)],
    ])

    md.h(2, "2. The largest offenders")
    md.table(["Endpoint", "Verb", "Size", "Latency", "Paging parameter?"],
             [[f"`{r['controller']}/{r['action']}`", r["verb"],
               f"**{(r['body_bytes'] or 0) / 1024 / 1024:.2f} MB**",
               f"{r['latency_ms']} ms", "⛔ none"] for r in biggest[:15]])
    md.p("None of these accepts a `page`, `pageSize`, `top`, `skip`, `filter` or date-range "
         "parameter. The response size is a function of the dataset, so it grows without "
         "bound as the estate grows.")

    md.h(2, "3. This is the same defect that took the environment down")
    md.p("`GetLogs` and `GetErrorLogs` are the fatal case of exactly this pattern — "
         "unparameterised retrieval over a log table. Two calls stopped the IIS "
         "application pool and took `QA_MsSQL` down for a day (**LH-08**, ISSUE-010). "
         "They are permanently blocklisted and therefore absent from the table above.")
    md("> The endpoints listed here are the *survivors* of the same design. "
       "`LobandService/GetDomainServices` returning 8 MB is on the same trajectory.")
    md("")

    md.h(2, "4. Consequence")
    md.table(["Area", "Impact"], [
        ["Worker exhaustion", "An unbounded query plus unbounded serialisation is what "
                              "stopped the app pool in ISSUE-010"],
        ["Client memory", "A UI or integration must hold the whole set in memory to find "
                          "one row"],
        ["Network and latency", f"{total / 1024 / 1024:.0f} MB transferred across "
                                f"{len(rows)} calls in one run"],
        ["Scales with the estate", "Response size tracks user and service counts, so this "
                                   "worsens on exactly the largest customers"],
        ["Our harness", "Body reads are capped at 2 MB during replay so a single response "
                        "cannot exhaust the runner"],
    ])

    revalidation_section(md, payload, spec, 5)

    md.h(2, "6. Proposed fix")
    md.table(["#", "Action", "Effort"], [
        ["1", "Add `pageNumber` / `pageSize` to the `GetAll*` and `*List` families, with "
              "a **server-side maximum**", "Medium"],
        ["2", "Add a server-side row cap and query timeout so no single request can "
              "exhaust a worker", "Low"],
        ["3", "Add filter parameters for the common lookups (by LOB, by name, by id)",
         "Medium"],
        ["4", "Return `Content-Length` and a total-count field so a client can plan",
         "Low"],
    ])
    md.p("Item 2 is the safety net and should land first — it bounds the blast radius of "
         "every endpoint in this class, including ones not yet identified.")

    md.h(2, "7. Full register")
    md.table(["#", "Controller", "Action", "Verb", "Size", "Latency ms", "Evidence"],
             [[i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"],
               f"{(r['body_bytes'] or 0) / 1024:.0f} KB", r["latency_ms"],
               f"`{esc(r['evidence_file'])}`"]
              for i, r in enumerate(sorted(rows, key=lambda x: -(x['body_bytes'] or 0)), 1)])
    reproduce_footer(md, spec, 8)


def _lh12_sheets(payload, xl):
    rows = payload["rows"]
    uniq = {(r["controller"], r["action"]) for r in rows}
    xl.summary("LH-12 — Endpoints return unfiltered full datasets", [
        ("Severity", "Low"), ("Environment", ENVIRONMENT), ("Source run", RUN_ID),
        ("", ""),
        ("Responses >= 100 KB", len(rows)),
        ("Distinct endpoints", len(uniq)),
        ("Largest response",
         f"{max(r['body_bytes'] or 0 for r in rows) / 1024 / 1024:.2f} MB"),
        ("Total bytes across these responses",
         f"{sum(r['body_bytes'] or 0 for r in rows) / 1024 / 1024:.1f} MB"),
        ("", ""),
        ("Related", "LH-08 / ISSUE-010 — the fatal case of this same pattern; two "
                    "unparameterised log reads stopped the IIS application pool."),
    ])
    xl.sheet("Large Responses",
             ["#", "Size KB", "Band", "Controller", "Action", "Verb", "Path",
              "Latency ms", "Evidence file"],
             [[i, round((r["body_bytes"] or 0) / 1024, 1), r["klass"], r["controller"],
               r["action"], r["verb"], r["path"], r["latency_ms"], r["evidence_file"]]
              for i, r in enumerate(
                  sorted(rows, key=lambda x: -(x["body_bytes"] or 0)), 1)],
             [5, 10, 16, 22, 40, 6, 52, 11, 46])
    xl.sheet("By Band", ["Band", "Responses", "Distinct endpoints"],
             [[k, v, len({(r["controller"], r["action"]) for r in rows
                          if r["klass"] == k})]
              for k, v in Counter(r["klass"] for r in rows).most_common()],
             [18, 12, 18])


LH12 = LoopholeSpec(
    num="12", slug="unfiltered-full-datasets",
    title="Endpoints return unfiltered full datasets",
    severity="🟡 Low", priority="Medium", effort="Medium",
    jira_summary=("List endpoints return entire datasets with no paging or filter - "
                  "largest observed response is 8 MB"),
    one_liner="No paging anywhere; the largest response is 8 MB and grows with the estate.",
    revalidate="safe", replay_limit=25,
    cross_refs=["LH-08 / ISSUE-010 (the fatal case of the same pattern)"],
    select=_lh12_select, classify=_lh12_classify,
    narrative=_lh12_narrative, sheets=_lh12_sheets,
    reproduces=lambda row, res: (res.get("body_bytes") or 0) >= BIG or res.get("truncated"),
    replay_summary=lambda res: (
        f"HTTP {res.get('status')} / {(res.get('body_bytes') or 0) / 1024:.0f} KB"
        + (" (capped)" if res.get("truncated") else "")),
    TICKET={
        "labels": ["performance", "api-design"],
        "what": ("List endpoints return the entire dataset with no filter, paging or "
                 "row-limit parameter. A client wanting one record must download every "
                 "record and filter locally. Response size is a function of the estate, "
                 "so this worsens on exactly the largest customers."),
        "scope_rows": [("Responses >= 100 KB", "25"),
                       ("Distinct endpoints", "13"),
                       ("*Largest single response*", "*8.0 MB*"),
                       ("Responses >= 1 MB", "19")],
        "sections": [
            ("The largest offenders",
             "|| Endpoint || Size ||\n"
             "| POST /api/LobandService/GetDomainServices | *8.00 MB* |\n"
             "| POST /api/LobandService/GetDomainServicesBytype | 5.84 MB |\n"
             "| GET /api/ServicePasswordDependancy/"
             "GetActiveServiceListWithoutMandateValue | 3.05 MB |\n"
             "| GET /api/UserDetails/GetAllActiveUserList | 1.13 MB |\n\n"
             "None accepts a page, pageSize, top, skip, filter or date-range parameter."),
            ("This is the same defect that took the environment down",
             "GetLogs and GetErrorLogs are the fatal case of exactly this pattern - "
             "unparameterised retrieval over a log table. Two calls stopped the IIS "
             "application pool and took QA_MsSQL down for a working day (LH-08 / "
             "ISSUE-010). They are permanently blocklisted and therefore absent from "
             "the figures above.\n\n"
             "The endpoints listed here are the survivors of the same design. "
             "GetDomainServices returning 8 MB is on the same trajectory."),
        ],
        "repro": """Preconditions:
  - Environment: QA_MsSQL, https://u16hf.arconnet.com:6302
  - A valid bearer token (generate ONE - see PAMIT ISSUE-009).

⚠️ These responses are large. Cap your client's read buffer - one is 8 MB.

1. POST /api/LobandService/GetDomainServices
   Header: Authorization: Bearer <token>
   Header: Content-Type: application/json

2. Measure the response size.
   EXPECTED: a bounded page, with a paging parameter available
   ACTUAL:   ~8.0 MB, the entire dataset, with no way to request less

3. Inspect the endpoint's declaration for any page / pageSize / top / skip /
   filter parameter. There is none.

4. GET /api/UserDetails/GetAllActiveUserList
   Observe ~1.13 MB returned to fetch what is usually a single user.

5. The full list of 13 endpoints and 25 measured responses is in the attached
   EVIDENCE.xlsx, sheet "Large Responses".""",
        "expected": ("List endpoints accept paging and filter parameters and enforce a "
                     "server-side maximum page size."),
        "actual": ("The full dataset is returned unconditionally; the largest observed "
                   "response is 8.0 MB and grows with the estate."),
        "severity_rows": [
            ["**Worker exhaustion**", "An unbounded query plus unbounded serialisation "
                                      "is what stopped the app pool in ISSUE-010"],
            ["**Client cost**", "A consumer must hold the whole set in memory to find "
                                "one row"],
            ["**Scales badly**", "Response size tracks user and service counts, so this "
                                 "is worst on the largest customers"],
            ["**Detectability**", "Visible as latency, but not attributed to a design "
                                  "cause"],
            ["**Cost to fix**", "Low for the safety cap; Medium for full paging"],
        ],
        "severity_argument": ("Rated Low individually, but it shares a root cause with "
                              "LH-08, which is Critical. The server-side row cap should "
                              "be treated as the shared mitigation for both."),
        "fix_rows": [
            ["1", "Add a server-side row cap and query timeout so no single request can "
                  "exhaust a worker", "Low",
             "The safety net - bounds every endpoint in this class, including ones not "
             "yet identified"],
            ["2", "Add `pageNumber` / `pageSize` to the `GetAll*` and `*List` families, "
                  "with a server-side maximum", "Medium", "The durable fix"],
            ["3", "Add filter parameters for the common lookups (by LOB, by name, by id)",
             "Medium", "Removes most of the need to page at all"],
            ["4", "Return a total-count field so a client can plan", "Low", "Usability"],
        ],
        "fix_note": ("Item 1 should land first — it bounds the blast radius of every "
                     "endpoint in this class and is the same mitigation LH-08 needs."),
        "acceptance": """1. No endpoint can return an unbounded result set; a server-side
   row cap is enforced.
2. The GetAll* and *List families accept paging parameters with a documented
   server-side maximum.
3. Re-running the QA harness reports 0 responses above the agreed size
   threshold.""",
        "target": "0 unbounded responses",
    },
)


RUN_SPECS = [LH02, LH03, LH04, LH05, LH09, LH11, LH12]
