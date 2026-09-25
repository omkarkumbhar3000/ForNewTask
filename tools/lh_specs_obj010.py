#!/usr/bin/env python3
"""Loophole specs derived from the OBJ-010 run: LH-13.

Separate module because these source a DIFFERENT run. LH-01…12 are pinned to
`2026-07-29_181439` so their published figures stay reproducible; LH-13 could only be
found in `2026-08-05_114315`, the first run in which the dynamic framework sent a
deliberately INVALID credential.

Why LH-13 did not exist before
------------------------------
The reference suite holds 1,153 `*_UnauthorizedAccess` test cases asserting HTTP 401. The
Excel rows carry no token column, and the reference class sends the SAME valid token as
every other test, so as authored those assertions can never exercise unauthorized access —
with a valid credential the endpoint answers 200 and the test simply fails. OBJ-010's
generator sets `hop.auth = "invalid"` for those rows, which turned 1,153 inert assertions
into real tests. 57 endpoints answered HTTP 200.

⛔ Replay is FORBIDDEN for the write endpoints in this set and the pack does not replay at
all. Several of the affected endpoints mutate (`UpdateMobileOTPRegistrationDetails`,
`InsertFileServerConfiguration`, `UpdateDatabaseAfterDeletionOfFilesOnFileServer`), and
re-issuing them unauthenticated to prove a point would be writing to QA with no credential.
The captured evidence is decisive on its own.
"""
from __future__ import annotations

import json
import re
from collections import Counter

from pathlib import Path

from lh_common import (                                                  # noqa: F401
    ENVIRONMENT, MD, LoopholeSpec, RunData, Xlsx, base_row, header_block,
    reproduce_footer, revalidation_section,
)

FLOW_DIR = Path(__file__).resolve().parent / "flows"

OBJ010_RUN = "2026-08-05_114315"

# The probe credential the framework sent. Not a real token; recorded so a reader can see
# exactly what was presented.
PROBE_TOKEN = "Bearer invalid.token.obj010-unauthorized-probe"

# Health probes: an unauthenticated 200 here is plausibly intentional, so they are
# classified out of the finding rather than counted in it.
HEALTH = re.compile(r"^(GetStatus|GetDatabaseStatus)$", re.I)
# Client bootstrap/registration endpoints - also plausibly unauthenticated by design.
BOOTSTRAP = re.compile(r"^(ClientAuth|RegisterClient)$", re.I)
WRITE_INTENT = re.compile(r"^(set|insert|add|create|update|save|edit|modify|delete)", re.I)


def _invalid_auth_keys() -> set[tuple[str, int, str]]:
    """(flow id, hop index, hop name) for every hop the generator marked auth=invalid.

    `run_flow` does not copy a hop's spec fields into the result record, so the auth mode
    cannot be read back from results.json. The flow definitions on disk are the authority,
    and they are deterministic — OBJ-010 proved the generators reproduce byte-identically
    (1,868/1,868 hops re-matched a week later). Keying on the triple, not on the path,
    matters: the same endpoint is also exercised with a VALID token by the positive and
    chain dimensions, and those hops must not be pulled into this finding.
    """
    keys: set[tuple[str, int, str]] = set()
    for f in sorted(FLOW_DIR.rglob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        for d in (doc if isinstance(doc, list) else [doc]):
            for i, h in enumerate(d.get("hops", []), 1):
                if h.get("auth") == "invalid":
                    keys.add((str(d.get("id")), i, str(h.get("name"))))
    return keys


def _lh13_rows() -> list[dict]:
    """Hops that presented an INVALID credential and still answered HTTP 200."""
    keys = _invalid_auth_keys()
    run = RunData.get(OBJ010_RUN)
    rows = []
    for flow, hop in run.hops:
        if hop.get("status") != 200:
            continue
        if (str(flow.get("id")), hop.get("n"), str(hop.get("name"))) not in keys:
            continue
        ev = run.evidence(hop)
        r = base_row(flow, hop, ev)
        r["response"] = ev.get("response")
        rows.append(r)
    # One row per endpoint - the same endpoint can appear in several negative batches.
    seen, unique = set(), []
    for r in sorted(rows, key=lambda x: x["path"]):
        k = (r["controller"], r["action"], r["verb"])
        if k in seen:
            continue
        seen.add(k)
        unique.append(r)
    return unique


def _lh13_classify(row) -> str:
    action = row.get("action") or ""
    if HEALTH.match(action):
        return "health probe - unauthenticated 200 plausibly by design"
    if BOOTSTRAP.match(action):
        return "client bootstrap - unauthenticated 200 plausibly by design"
    if WRITE_INTENT.match(action):
        return "WRITE reachable without authentication"
    body = json.dumps(row.get("response")) if row.get("response") is not None else ""
    if len(body) > 120:
        return "data disclosed without authentication"
    return "responds without authentication, payload trivial"


def _in_scope(rows):
    """The finding proper: everything that is not a health probe or client bootstrap."""
    return [r for r in rows if "by design" not in r["klass"]]


def _body_len(r) -> int:
    return len(json.dumps(r.get("response"))) if r.get("response") is not None else 0


def _lh13_narrative(payload, md):
    spec = LH13
    rows = payload["rows"]
    scope = _in_scope(rows)
    writes = [r for r in scope if r["klass"].startswith("WRITE")]
    disclose = [r for r in scope if r["klass"].startswith("data disclosed")]
    header_block(md, payload, spec)

    md.h(2, "1. What was measured")
    md.p(f"Every request in this pack carried `{PROBE_TOKEN}` as its `Authorization` "
         "header — a syntactically shaped but meaningless bearer token. No real "
         "credential was used and `/arcontoken` was never called. Each of these "
         f"**{len(rows)}** endpoints answered **HTTP 200**.")
    md.table(["Class", "Endpoints"],
             [[k, v] for k, v in Counter(r["klass"] for r in rows).most_common()])
    md.p(f"**{len(rows) - len(scope)}** are health probes or client-bootstrap endpoints, "
         "where an unauthenticated 200 is plausibly intentional; they are listed for "
         f"completeness and excluded from the finding. The finding is the remaining "
         f"**{len(scope)}**, of which **{len(writes)}** are writes and **{len(disclose)}** "
         "returned business data.")

    md.h(2, "2. Why this was invisible until now")
    md.p("The reference suite contains **1,153** `*_UnauthorizedAccess` test cases that "
         "assert HTTP 401. Those Excel rows carry no token column, and the reference test "
         "class sends **the same valid token as every other test** — so as authored the "
         "assertion cannot exercise unauthorized access at all. With a valid credential "
         "the endpoint answers 200 and the test fails; it could only ever 'pass' if the "
         "shared `ApiToken` happened to be expired, which is passing for the wrong "
         "reason.")
    md.p("The dynamic framework supplies an invalid credential for exactly these rows "
         "(`hop.auth = \"invalid\"` in `generate_data_flows.py`, honoured by "
         "`chain_runner.Runner.call`). That single change converted 1,153 inert "
         "assertions into real tests and produced this finding.")

    if disclose:
        md.h(2, "3. Business data returned to an unauthenticated caller")
        md.table(["#", "Endpoint", "Verb", "Body bytes", "Evidence"],
                 [[i, f"`{r['path']}`", r["verb"], _body_len(r), f"`{r['evidence_file']}`"]
                  for i, r in enumerate(sorted(disclose, key=_body_len, reverse=True), 1)])

    if writes:
        md.h(2, "4. Write endpoints reachable without authentication")
        md.p("⛔ These are the most serious entries: a caller with no valid credential "
             "reaches a state-changing operation.")
        md.table(["#", "Endpoint", "Verb", "Evidence"],
                 [[i, f"`{r['path']}`", r["verb"], f"`{r['evidence_file']}`"]
                  for i, r in enumerate(sorted(writes, key=lambda x: x["path"]), 1)])

    md.h(2, "5. Full register")
    md.table(["#", "Controller", "Action", "Verb", "HTTP", "Class", "Body bytes",
              "Evidence"],
             [[i, f"`{r['controller']}`", f"`{r['action']}`", r["verb"], r["http_status"],
               r["klass"], _body_len(r), f"`{r['evidence_file']}`"]
              for i, r in enumerate(sorted(rows, key=lambda x: (x["klass"], x["path"])), 1)])

    revalidation_section(md, payload, spec, 6)

    md.h(2, "7. Proposed fix")
    md.table(["#", "Action", "Effort", "Effect"], [
        ["1", "Apply the authorization filter globally and make it opt-out, so a "
              "controller cannot be unauthenticated by omission", "Medium",
         "Closes the whole class, not just these endpoints"],
        ["2", "Explicitly allow-list the endpoints that are intended to be anonymous "
              "(health probes, client bootstrap) and document why", "Low",
         "Makes the intended exceptions auditable"],
        ["3", "Reject a malformed or unverifiable bearer token with 401 before any "
              "handler runs", "Low", "Removes the ambiguity that hid this"],
        ["4", "Add a credential column to the 1,153 `*_UnauthorizedAccess` source rows "
              "so the reference suite can exercise this itself", "Low",
         "Stops the tests being inert"],
    ])
    reproduce_footer(md, spec, 8)


def _lh13_sheets(payload, xl: Xlsx):
    rows = payload["rows"]
    scope = _in_scope(rows)
    writes = [r for r in scope if r["klass"].startswith("WRITE")]
    disclose = [r for r in scope if r["klass"].startswith("data disclosed")]
    xl.summary("LH-13 — Endpoints accept an invalid authentication token", [
        ("Severity", "Critical"), ("Environment", ENVIRONMENT),
        ("Source run", payload["source_run"]), ("", ""),
        ("Endpoints answering HTTP 200 to an invalid token", len(rows)),
        ("…excluded as plausibly-by-design (health / bootstrap)", len(rows) - len(scope)),
        ("…IN SCOPE for this finding", len(scope)),
        ("……of which are writes", len(writes)),
        ("……of which returned business data", len(disclose)),
        ("", ""),
        ("Credential presented", PROBE_TOKEN),
        ("Real credential used", "No"),
        ("Calls to /arcontoken", 0),
        ("", ""),
        ("Why not found before",
         "The 1,153 *_UnauthorizedAccess reference cases assert 401 but send a VALID "
         "token, so they could never exercise unauthorized access."),
        ("Replay", "Not replayed. Several affected endpoints mutate; re-issuing them "
                   "unauthenticated to prove the point would write to QA with no "
                   "credential."),
    ])
    xl.sheet("In Scope",
             ["#", "Controller", "Action", "Verb", "Path", "HTTP", "Class", "Body bytes",
              "Evidence file"],
             [[i, r["controller"], r["action"], r["verb"], r["path"], r["http_status"],
               r["klass"], _body_len(r), r["evidence_file"]]
              for i, r in enumerate(sorted(scope, key=lambda x: -_body_len(x)), 1)],
             [5, 22, 40, 6, 62, 7, 44, 12, 52])
    xl.sheet("Excluded By Design",
             ["#", "Controller", "Action", "Verb", "Path", "Class", "Evidence file"],
             [[i, r["controller"], r["action"], r["verb"], r["path"], r["klass"],
               r["evidence_file"]]
              for i, r in enumerate([r for r in rows if r not in scope], 1)],
             [5, 22, 40, 6, 62, 46, 52])
    xl.sheet("Classes", ["Class", "Endpoints"],
             [[k, v] for k, v in Counter(r["klass"] for r in rows).most_common()],
             [50, 12])


LH13 = LoopholeSpec(
    num="13", slug="endpoints-accept-invalid-auth-token",
    title="Endpoints accept an invalid authentication token and return HTTP 200",
    severity="🔴 Critical", priority="Highest", effort="Medium",
    jira_summary=("API returns HTTP 200 with business data and reaches write operations "
                  "when presented an invalid bearer token"),
    one_liner=("An invalid bearer token is accepted: endpoints return real data and "
               "state-changing operations are reachable without authentication."),
    source="run", run_id=OBJ010_RUN,
    revalidate="forbidden",
    revalidate_note=("Not replayed. Several affected endpoints are writes "
                     "(UpdateMobileOTPRegistrationDetails, InsertFileServerConfiguration, "
                     "UpdateDatabaseAfterDeletionOfFilesOnFileServer). Re-issuing them "
                     "with no valid credential in order to prove the finding would itself "
                     "write to QA unauthenticated. The captured evidence is decisive."),
    cross_refs=[
        "LH-01 (delivered at HTTP 200, so invisible to status-code monitoring)",
        "LH-09 (credentials returned in responses - the same trust-boundary theme)",
        "LH-10 (no validation attributes: authorization is likewise not declared)",
    ],
    rows_static=_lh13_rows, classify=_lh13_classify,
    narrative=_lh13_narrative, sheets=_lh13_sheets,
    TICKET={
        "labels": ["security", "authentication", "authorization",
                   "information-disclosure"],
        "what": ("Requests carrying a deliberately invalid bearer token "
                 f"(`{PROBE_TOKEN}`) were answered with HTTP 200 by 57 endpoints. "
                 "Excluding 34 health probes and 4 client-bootstrap endpoints where an "
                 "anonymous 200 is plausibly intentional, 19 endpoints remain: several "
                 "returned real business data, and several are write operations."),
        "scope_rows": [
            ("Endpoints answering HTTP 200 to an invalid token", "57"),
            ("Excluded as plausibly by design (health / bootstrap)", "38"),
            ("**In scope**", "**19**"),
            ("…returning business data", "see EVIDENCE.md §3"),
            ("…write operations", "see EVIDENCE.md §4"),
        ],
        "example": ("GET /api/FileDetails/GetFileSharedData\n"
                    "Authorization: Bearer invalid.token.obj010-unauthorized-probe\n\n"
                    "HTTP 200\n"
                    "[{\"OwnerUser\":\"RUSHI\",\"SharedFileId\":\"35\","
                    "\"SharedFileName\":\"User.txt\",\"SharedWith\":\"RUSHIKESH\","
                    "\"SharedWithUserId\":\"49\",\"SharedWithUserDomain\":\"ARCOSAUTH\"}]"),
        "sections": [
            ("Why the existing test suite never caught this",
             "The suite contains *1,153* `*_UnauthorizedAccess` cases asserting HTTP 401. "
             "The rows carry no token column and the test class sends the SAME VALID "
             "token as every other test, so the assertion cannot exercise unauthorized "
             "access. With a valid credential the endpoint answers 200 and the test "
             "fails; it could only pass if the shared token happened to be expired - "
             "passing for the wrong reason."),
            ("What was actually returned",
             "|| Endpoint || Disclosed ||\n"
             "| /api/Lob/Get | 6,856 bytes of LOB configuration |\n"
             "| /api/FileDetails/GetDetailsOfFilesOnFileServer | file name, size, "
             "content, creator |\n"
             "| /api/FileDetails/GetFileSharedData | real usernames, domain ARCOSAUTH |\n"
             "| /api/Encryption/GetAESEncryptedText | a working encryption oracle |"),
            ("Write operations reachable unauthenticated",
             "* /api/DualFactor/UpdateMobileOTPRegistrationDetails\n"
             "* /api/FileServerDetail/InsertFileServerConfiguration\n"
             "* /api/FileServerDetail/UpdateFileUploadConfiguration\n"
             "* /api/FileDetails/UpdateDatabaseAfterDeletionOfFilesOnFileServer\n"
             "* /api/FileDetails/UpdateDatabaseAfterDeletionOfFilesOnFileServerByUser"),
        ],
        "repro": """Preconditions:
  - Environment: QA_MsSQL, https://u16hf.arconnet.com:6302
  - NO valid token is required - that is the point of the test.

1. GET /api/FileDetails/GetFileSharedData
   Header: Authorization: Bearer invalid.token.obj010-unauthorized-probe
   Header: Content-Type: application/json

2. Read the status and the body.
   EXPECTED: HTTP 401, no body
   ACTUAL:   HTTP 200 with real shared-file records including usernames
             and the ARCOSAUTH domain

3. Repeat for the endpoints in the attached EVIDENCE.xlsx, sheet "In Scope".

4. Do NOT replay the write endpoints listed in sheet "In Scope" with
   class "WRITE reachable without authentication" - issuing them
   unauthenticated would mutate QA data.""",
        "expected": ("HTTP 401 with no body when the bearer token is absent, malformed or "
                     "unverifiable."),
        "actual": ("HTTP 200 with business data, and write operations reachable, when the "
                   "bearer token is invalid."),
        "severity_rows": [
            ["**Authentication bypass**", "An invalid credential is accepted"],
            ["**Data disclosure**", "Usernames, domains, file names and file content "
                                    "returned to an unauthenticated caller"],
            ["**Integrity**", "Write operations reachable with no valid credential"],
            ["**Reachability**", "Any network caller; no credential needed at all"],
            ["**Detectability**", "None - delivered at HTTP 200 (see LH-01)"],
            ["**Existing test coverage**", "1,153 cases nominally cover this and are all "
                                           "inert"],
        ],
        "severity_argument": ("Rated Critical. This is the only finding in the set where "
                             "an unauthenticated caller both reads business data and "
                             "reaches state-changing operations. It also invalidates the "
                             "assurance the 1,153 existing UnauthorizedAccess cases were "
                             "believed to provide."),
        "fix_rows": [
            ["1", "Make the authorization filter global and opt-out, so a controller "
                  "cannot be anonymous by omission", "Medium",
             "Closes the class, not the instances"],
            ["2", "Allow-list the intentionally anonymous endpoints and document why",
             "Low", "Makes the exceptions auditable"],
            ["3", "Reject a malformed or unverifiable bearer with 401 before any handler "
                  "runs", "Low", "Removes the ambiguity"],
            ["4", "Add a credential column to the 1,153 UnauthorizedAccess source rows",
             "Low", "Stops the reference tests being inert"],
        ],
        "fix_note": ("Item 3 is the immediate containment; item 1 is the durable fix. "
                     "Item 4 belongs to QA and is what stops this regressing unnoticed."),
        "acceptance": """1. Every endpoint not on the documented anonymous allow-list
   returns HTTP 401 for an absent, malformed or unverifiable bearer token.
2. The anonymous allow-list exists, is reviewed, and contains no endpoint
   that reads business data or writes.
3. Re-running the dynamic harness reports 0 in-scope endpoints answering
   HTTP 200 to an invalid credential.
4. The 1,153 *_UnauthorizedAccess rows carry a credential column and fail
   if the behaviour regresses.""",
        "target": "0 in-scope endpoints accepting an invalid token",
    },
)

OBJ010_SPECS = [LH13]
