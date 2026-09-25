#!/usr/bin/env python3
"""OBJ-007 A1/A4 - chaining-validation and Level-6 read-back extraction.

Pure analysis over an existing run artifact. ZERO HTTP requests, ZERO database access.
Everything is derived from three read-only inputs:

  1. artifacts/runs/2026-07-29_181439/results.json    326 flows, 1,873 hops, all L1-L7 verdicts
  2. artifacts/runs/2026-07-29_181439/evidence/*.json 1,868 per-call request/response captures
  3. tools/flows/**/*.json              the flow definitions (planned hops,
                                                    placeholders, expectations)

Output (JSON only - the workbook is built centrally, this script never writes .xlsx):

  artifacts/analysis-data/chaining-validation.json   one row per executed hop      (1,873 rows)
  artifacts/analysis-data/l6-read-back.json          one row per L6 record-exists check (107 rows)

Every derived column - expected_result, failure_reason, required_fix,
additional_observations - comes from a rule table keyed on the check detail strings, so
the output is reproducible rather than editorial. No value is invented: where the evidence
cannot settle a question the cell says UNKNOWN and names what would settle it.

    python tools/obj007_chain_analysis.py            # write both files + stats
    python tools/obj007_chain_analysis.py --stats     # stats only, write nothing
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

HERE = Path(__file__).resolve().parent


def _workspace_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if True:  # OBJ-025: markers now via workspace_root
            return workspace_root(p)
    raise SystemExit(f"cannot locate the workspace root above {start}")


ROOT = _workspace_root(HERE)
RUN = ROOT / "artifacts" / "runs" / "2026-07-29_181439"
RESULTS = RUN / "results.json"
EVIDENCE = RUN / "evidence"
FLOW_DIR = HERE / "flows"
OUT_DIR = ROOT / "artifacts" / "analysis-data"

# Figures the shared agent brief declares authoritative. A mismatch is reported loudly.
BRIEF = {
    "hops": 1873, "calls": 1868, "flows": 326, "flow_pass": 30, "flow_fail": 296,
    "L1": (1688, 180), "L2": (1864, 4), "L3": (1278, 590), "L4": (1410, 458),
    "L5": (982, 196), "L6": (2, 105), "L7": (1855, 13),
}

PLACEHOLDER = re.compile(r"\$\{([A-Za-z0-9_.]+)\}")
KNOWN_ERROR_CODES = {"201", "202", "203"}          # ApiHelper's hardcoded set
CREATED_MESSAGES = ("inserted", "created", "added", "saved", "success")
NOOP_MESSAGES = ("already exists", "duplicate")
ERROR_TONE = re.compile(
    r"(error occurred|is mandatory|not found|invalid|cannot be null|does not exist|"
    r"already exists|no record|failed|exception)", re.I)
STACKTRACE = re.compile(r"(\.cs:line|\n\s+at\s|System\.[A-Za-z]+Exception)")
DESTRUCTIVE_TOKEN = re.compile(
    r"(delete|remove|drop|purge|revoke|disable|deactivate|unmap|offboard)", re.I)
DESTRUCTIVE_ANCHORED = re.compile(
    r"^(delete|remove|drop|purge|reset|revoke|disable|deactivate|terminate|kill|wipe)", re.I)
EMAILISH = re.compile(r"^[^@\s]+@[^@\s]+$")

LAYER_COLUMN = {
    "L1": "level_1_http_status",
    "L2": "level_2_content_type",
    "L3": "level_3_envelope",
    "L4": "level_4_message_semantics",
    "L5": "level_5_chain_key_extracted",
    "L6": "level_6_record_exists",
    "L7": "level_7_latency",
}

# What each layer proves when it passes - used to build expected_result.
LAYER_INTENT = {
    "L1": "HTTP status matches the expectation",
    "L2": "Content-Type is application/json",
    "L3": "the response carries the standard envelope with Success=true (or a known errorCode)",
    "L4": "the Message text asserts the outcome the hop expects",
    "L5": "every chain key this hop must publish resolves to a non-empty value",
    "L6": "the record this flow created is readable back through a list/read endpoint",
    "L7": "latency is inside the hop SLA",
}


# ----------------------------------------------------------------- loading
def load_flow_defs() -> dict[str, dict]:
    """flow id -> {planned hop count, per-hop definition}."""
    out: dict[str, dict] = {}
    for p in sorted(FLOW_DIR.rglob("*.json")):
        doc = json.loads(p.read_text(encoding="utf-8"))
        for fl in (doc if isinstance(doc, list) else [doc]):
            out[fl["id"]] = {
                "planned": len(fl["hops"]),
                "tier": fl.get("tier"),
                "generated": bool(fl.get("generated")),
                "controller": fl.get("controller") or "",
                "file": str(p.relative_to(FLOW_DIR)),
                "hops": fl["hops"],
            }
    return out


def placeholders_of(hopdef: dict) -> list[str]:
    """Every ${VAR} the hop definition references, in path, body and verify clauses."""
    if not hopdef:
        return []
    blob = json.dumps({k: v for k, v in hopdef.items() if k != "note"}, default=str)
    seen, out = set(), []
    for name in PLACEHOLDER.findall(blob):
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


def load_evidence(name: str) -> dict:
    p = EVIDENCE / (name or "")
    if not name or not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                                    # noqa: BLE001
        return {}


# ----------------------------------------------------------------- envelope reading
def env_read(resp) -> dict:
    """Normalised view of whatever shape the response came back in."""
    v = {"shape": "", "success": None, "error_code": "", "error_message": "",
         "message": "", "result_type": "ABSENT", "result_len": None, "keys": []}
    if resp is None:
        v["shape"] = "no-body"
        return v
    if isinstance(resp, str):
        v["shape"] = "empty-body" if resp == "" else "bare-string"
        v["message"] = resp[:300]
        return v
    if isinstance(resp, bool):
        v["shape"] = "bare-boolean"
        v["message"] = str(resp)
        return v
    if isinstance(resp, list):
        v["shape"] = "bare-array"
        v["result_len"] = len(resp)
        return v
    if not isinstance(resp, dict):
        v["shape"] = f"bare-{type(resp).__name__}"
        return v
    v["shape"] = "envelope" if "Success" in resp or "ErrorCode" in resp else "non-standard-object"
    v["keys"] = list(resp)[:12]
    v["success"] = resp.get("Success")
    v["error_code"] = str(resp.get("ErrorCode") or resp.get("errorCode") or "")
    v["error_message"] = str(resp.get("ErrorMessage") or "")
    v["message"] = str(resp.get("Message") or "")
    if "Result" in resp:
        r = resp["Result"]
        v["result_type"] = type(r).__name__
        if isinstance(r, (list, dict)):
            v["result_len"] = len(r)
    return v


def walk_dicts(node, depth=0):
    if depth > 12:
        return
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk_dicts(v, depth + 1)
    elif isinstance(node, list):
        for v in node:
            yield from walk_dicts(v, depth + 1)


ID_FIELD = re.compile(r"id$", re.I)
ID_ISH = re.compile(r"(id|code|key|guid|ref|no|num|seq|sr)", re.I)
ENVELOPE_KEYS = {"program", "version", "datetime", "success", "message",
                 "errorcode", "errormessage"}


def id_candidates(resp) -> dict:
    """Does an id-shaped value exist ANYWHERE in this response?

    This is what separates cause (c) - the extractor missed a field that was present -
    from cause (b) - no id was ever returned. Deliberately far broader than the runner's
    any_id(): every dict at any depth, and every id-ish key name, not only /id$/.
    """
    strict, loose = [], []
    for node in walk_dicts(resp):
        for k, val in node.items():
            if k.lower() in ENVELOPE_KEYS:
                continue
            if isinstance(val, bool) or not isinstance(val, (str, int, float)):
                continue
            if not str(val).strip():
                continue
            if ID_FIELD.search(k):
                strict.append((k, val))
            elif ID_ISH.search(k):
                loose.append((k, val))
    return {"strict": strict, "loose": loose}


# ----------------------------------------------------------------- L5 cause split
def l5_cause(hop: dict, resp) -> tuple[str, str]:
    """Classify one 'MISSING [NEW_ID]' hop into the a/b/c taxonomy.

    (a) the create genuinely failed - there was no id to extract
    (b) the create was acknowledged but the response carries no id field  -> API gap
    (c) an id WAS present and the extractor's key pattern missed it       -> harness bug
    (d) no id and no determinate outcome signal                           -> UNKNOWN
    """
    cand = id_candidates(resp)
    if cand["strict"] or cand["loose"]:
        return ("c", "an id-shaped field was present in the response but any_id() "
                     f"did not reach it: {cand['strict'][:3] or cand['loose'][:3]}")

    v = env_read(resp)
    st = hop.get("status")
    if st != 200:
        return ("a", f"HTTP {st} - the request never reached a successful create")
    if v["shape"] == "empty-body":
        return ("d", "HTTP 200 with a zero-byte body: no envelope, no id, and no "
                     "statement of whether the write happened")
    if v["shape"] in ("bare-string", "bare-boolean"):
        text = v["message"].strip().strip('"')
        if text.casefold() == "false":
            return ("a", "endpoint returned bare JSON false - read as 'not inserted'")
        if text.casefold() == "true":
            return ("b", "endpoint returned bare JSON true - the write is acknowledged "
                         "but the shape has no field an id could live in")
        return ("d", f"endpoint returned a bare string {text[:60]!r} - it carries no "
                     "success flag, no id and no insert statement")
    if v["success"] is False:
        return ("a", f"Success=false, ErrorCode={v['error_code'] or 'NONE'}, "
                     f"ErrorMessage={v['error_message'][:120]!r}")
    if v["success"] is True:
        low = (v["message"] or v["error_message"]).casefold()
        if any(n in low for n in NOOP_MESSAGES):
            return ("a", f"Success=true but Message={v['message']!r} - a no-op, "
                         "nothing was inserted")
        if any(c in low for c in CREATED_MESSAGES):
            return ("b", f"Success=true and Message/ErrorMessage="
                         f"{(v['message'] or v['error_message'])!r} - the insert is "
                         f"acknowledged, yet Result is {v['result_type']} and holds no id")
        return ("d", "Success=true with no Message at all - the response neither names "
                     "the created record nor confirms an insert")
    if v["error_code"] and v["error_code"] not in KNOWN_ERROR_CODES:
        return ("a", f"errorCode={v['error_code']!r} on HTTP 200")
    if ERROR_TONE.search(json.dumps(resp, default=str)[:2000]):
        return ("a", "non-standard payload carrying an error message "
                     f"({json.dumps(resp, default=str)[:120]})")
    return ("d", f"response shape {v['shape']} carries neither a success flag nor an id")


CAUSE_LABEL = {
    "a": "a - CREATE FAILED (no id existed to extract)",
    "b": "b - API CONTRACT GAP (create acknowledged, no id in the response)",
    "c": "c - HARNESS BUG (an id was present and the extractor missed it)",
    "d": "d - UNKNOWN (no id and no determinate create signal)",
    "": "",
}
CAUSE_FIX = {
    "a": "Fix the request first: publish the request contract for this endpoint so a "
         "valid body can be built. Until the create succeeds, chaining cannot start.",
    "b": "Product change: a create must return the primary key of the record it "
         "inserted, inside Result. Until then no downstream hop can be chained and no "
         "read-back can be verified.",
    "c": "Harness change: widen chain_runner.any_id() - it scans only the top-level keys "
         "of Result[0], Result and the root, and only /id$/.",
    "d": "Two changes, in this order: (1) product must state the outcome of a write in "
         "the envelope; (2) the generator must stop classifying this endpoint as a create "
         "(generate_flows.py:37 WRITE_NEW matches any name starting 'set').",
    "": "",
}


# ----------------------------------------------------------------- L6 cause split
def l6_cause(readback_resp, detail: str, searched: str) -> tuple[str, str, str]:
    """(root_cause, failure_reason, suggested_solution) for one record-exists check."""
    v = env_read(readback_resp)
    if "${" in searched:
        return ("UNRESOLVED PLACEHOLDER - the check could not pass by construction",
                f"The read-back searched for the literal string {searched!r}. The create "
                "hop published no id, so substitute() left the placeholder untouched "
                "(chain_runner.py:200) and value_anywhere() then hunted for the token "
                "itself (chain_runner.py:522). No response can ever contain it. This "
                "verdict says nothing about whether the record exists.",
                "Skip the read-back when its input variable is unresolved and record it "
                "as NOT VERIFIABLE, not FAIL. Then fix the upstream create so an id is "
                "published.")
    if v["success"] is False:
        return ("READ-BACK ENDPOINT REJECTED THE REQUEST - persistence was never queried",
                f"The read-back call itself failed: ErrorCode={v['error_code'] or 'NONE'}, "
                f"ErrorMessage={v['error_message'][:140]!r}. The store was never "
                "interrogated, so the FAIL is about the read endpoint, not the record.",
                "Give the read-back a valid request body (pick_readback() in "
                "generate_flows.py:187 selects on name only and supplies {} for POST "
                "reads), or choose a read endpoint that needs no body.")
    noop = any(n in (v["message"] or "").casefold() for n in NOOP_MESSAGES)
    if noop:
        return ("HARNESS FALSE NEGATIVE - existence confirmed in the Message, not in a "
                "payload the matcher can read",
                f"The read-back answered Success=true, Message={v['message']!r}. That is "
                "positive evidence the record is there, but the endpoint returns no "
                "record body, so value_anywhere() had nothing to match and the layer "
                "recorded NOT FOUND.",
                "Treat a Message-level existence confirmation as a PASS signal in "
                "assess(); the record-exists layer must not require a payload the "
                "endpoint never returns.")
    empty = (v["result_type"] in ("list", "NoneType") and (v["result_len"] or 0) == 0)
    if empty or "no record" in (v["message"] or "").casefold():
        return ("NOT VISIBLE THROUGH THIS ENDPOINT - zero records returned",
                f"The read-back succeeded (Success={v['success']}, "
                f"Message={v['message']!r}) and returned an empty Result, so the created "
                "object is not listed by this endpoint. Whether it was never written or "
                "is written somewhere this endpoint does not read is UNKNOWN from the "
                "API alone.",
                "Confirm with the API owner which read endpoint lists this entity. If it "
                "is the right one, raise a persistence defect; settle it with a "
                "read-only SELECT against ARCOSDB_U16SP2_WEBSM_QA.")
    return ("SEARCHED VALUE ABSENT FROM A POPULATED RESPONSE",
            f"The read-back returned data (Result={v['result_type']}, "
            f"len={v['result_len']}) but {searched} appears nowhere in it "
            f"(recorded detail: {detail!r}). Either the value taken from the create is "
            "not this entity's key, or the record is not in the returned set.",
            "Check what the create actually returned - if any_id() picked a non-key "
            "field, pin the key per endpoint instead of guessing at run time.")


# ----------------------------------------------------------------- per-layer rules
def layer_reason(layer: str, detail: str, hop: dict, _resp, ctx: dict) -> tuple[str, str]:
    """(failure_reason, required_fix) for one failing layer. Keyed on the detail string."""
    st = hop.get("status")
    v = ctx["env"]

    if layer == "L1":
        if hop.get("error"):
            return (f"No HTTP response - transport error: {hop['error']}",
                    "Investigate reachability/timeout for this endpoint; a 45 s timeout "
                    "with no answer is a product defect, not a test defect.")
        if st == 404:
            return ("HTTP 404 - the route is not served on this build.",
                    "Correct or remove the declaration in APIConfig.java, and confirm "
                    "with the API team which service version serves this path.")
        if st == 400:
            return (f"HTTP 400 - the request was rejected at the framework boundary "
                    f"before any business logic ran ({v['message'] or v['error_message'] or 'no detail'})."[:400],
                    "Publish the request contract for this endpoint. The payload literal "
                    "in utils/apiPayload does not bind to the current model.")
        if st in (401, 403):
            return (f"HTTP {st} - the bearer token was not accepted for this endpoint.",
                    "Confirm the service account's authorisation for this controller; "
                    "framework-level rejections carry no envelope to assert on.")
        if st == 405:
            return ("HTTP 405 - verb not allowed on this route.",
                    "Correct the verb comment in APIConfig.java.")
        if st is not None and st >= 500:
            return (f"HTTP {st} - unhandled server error.",
                    "Raise as a product defect: the endpoint must return a handled "
                    "application error, never a 5xx.")
        return (f"HTTP status check failed: {detail}.",
                "Reconcile the expected status for this hop with the endpoint's contract.")

    if layer == "L2":
        return (f"Content-Type was {detail!r}, not application/json.",
                "The endpoint must declare application/json; a non-JSON content type "
                "breaks every downstream assertion.")

    if layer == "L3":
        if detail.startswith("expected a JSON object"):
            return (f"No response envelope at all - {detail}. The documented "
                    "{Program,Version,DateTime,Success,Message,Result} shape is absent.",
                    "Return the standard envelope, or publish the bare shape as the "
                    "contract so assertions can be generated against it.")
        if detail.startswith("Success=False"):
            return (f"Application-level rejection delivered on HTTP {st}: Success=false, "
                    f"ErrorCode={v['error_code'] or 'NONE'}, "
                    f"ErrorMessage={v['error_message'][:160]!r}.",
                    "Two fixes: the request needs a valid contract, and a rejected "
                    "request should not be returned as HTTP 200 - a status-only "
                    "assertion passes against it.")
        if detail.startswith("errorCode="):
            return (f"Unrecognised application error code on HTTP {st}: {detail}.",
                    "Publish the error-code catalogue and extend "
                    "ApiHelper.KNOWN_ERROR_CODES beyond {201,202,203}.")
        if detail.startswith("neither Success nor errorCode"):
            return (f"The response object carries neither Success nor errorCode "
                    f"({detail}), so there is no machine-readable outcome to assert.",
                    "Add the standard envelope fields to this endpoint's response.")
        return (f"Envelope check failed: {detail}.", "Align the response with the "
                "documented envelope.")

    if layer == "L4":
        if "nothing was created" in detail:
            return (f"The endpoint reported a no-op: {detail}. Success was true and the "
                    "status was 200, but no record was inserted.",
                    "Assert on Message semantics, never on Success alone; and seed "
                    "unique per-run data so a create is not a duplicate.")
        if detail.startswith("ErrorMessage="):
            return (f"Error message present on HTTP {st}: {detail}.",
                    "Fix the request contract; and return a non-2xx status for an error, "
                    "so the transport layer agrees with the body.")
        if detail == "no envelope to read":
            return ("No envelope, so the outcome of the call cannot be read from the "
                    "response at all.",
                    "Return the standard envelope for this endpoint.")
        if detail == "Message=''":
            return ("The Message field is present but empty - there is no semantic "
                    "statement of the outcome.",
                    "Populate Message with the outcome ('Inserted Successfully', "
                    "'Already Exists', ...) - it is the only reliable create signal.")
        if hop.get("_expect_created"):
            return (f"A create was expected but the message does not assert one: {detail}.",
                    "Return an explicit insert confirmation; 'Success: true' alone is "
                    "not evidence of a write.")
        return (f"Message semantics failed: {detail}.",
                "State the outcome of the call in Message.")

    if layer == "L5":
        cause = ctx.get("l5_cause", "")
        why = ctx.get("l5_why", "")
        keys = re.search(r"MISSING (\[[^\]]*\])", detail)
        keyname = keys.group(1) if keys else "[?]"
        return (f"Chain key {keyname} did not resolve, so no downstream hop could use it. "
                f"Cause {CAUSE_LABEL.get(cause, cause)}: {why}",
                CAUSE_FIX.get(cause, ""))

    if layer == "L6":
        _rc, fr, sol = ctx.get("l6_triple", ("", f"record-exists failed: {detail}", ""))
        return (fr, sol)

    if layer == "L7":
        return (f"Latency SLA breached: {detail}.",
                "Profile the endpoint. A hop slower than its SLA breaks any chain that "
                "has to run inside a token's 24 h life.")

    return (f"{layer} failed: {detail}.", "")


# ----------------------------------------------------------------- observations
def observations(hop: dict, _hopdef: dict, resp, ctx: dict, flowctx: dict) -> list[str]:
    out = []
    v = ctx["env"]
    st = hop.get("status")
    blob = json.dumps(resp, default=str)[:8000] if resp is not None else ""

    if STACKTRACE.search(blob):
        out.append("Server stack trace and build paths disclosed in the error payload "
                   "(information disclosure).")
    if st == 200 and v["success"] is False:
        out.append("Rejection returned as HTTP 200 - a status-only assertion would pass "
                   "against a fully rejected request.")
    if st is not None and st != 200 and v["success"] is True:
        out.append(f"Contradictory envelope: HTTP {st} with Success=true.")
    if v["error_code"] and v["error_code"].split("-")[0].strip() not in KNOWN_ERROR_CODES:
        out.append(f"ErrorCode {v['error_code'][:40]!r} is outside "
                   "ApiHelper.KNOWN_ERROR_CODES {201,202,203}.")
    if v["shape"] == "bare-string" and "Setting up" in v["message"]:
        out.append("Endpoint returns a fixed banner string - it is a status probe, not a "
                   "create. generate_flows.py:37 (WRITE_NEW matches any name starting "
                   "'set') misclassified it as a create endpoint.")
    if v["shape"] == "empty-body":
        out.append("HTTP 200 with a zero-byte body and Content-Type: application/json.")
    if v["shape"] in ("bare-boolean",):
        out.append("Endpoint returns a bare JSON boolean with no envelope.")
    if v["result_type"] == "bool":
        out.append("Result is a boolean, not a record - nothing an id could be read from.")

    # id-quality observations on whatever this hop published
    req_body = ctx.get("request_body") or {}
    for name, val in (hop.get("extracted") or {}).items():
        if val in (None, "", []):
            continue
        field = hop.get("id_field_used")
        if isinstance(req_body, dict):
            echoed = [k for k, rv in req_body.items()
                      if not isinstance(rv, (dict, list)) and str(rv) == str(val)]
            if echoed:
                out.append(f"{name}={val!r} echoes the value submitted in request field "
                           f"{echoed[0]!r} - it is not a server-generated key.")
        if str(val) == "0":
            out.append(f"{name}=0 - the create acknowledged an insert but returned id 0.")
        if isinstance(val, str) and EMAILISH.match(val):
            out.append(f"any_id() matched field {field!r} and took an email address as "
                       "the record id (chain_runner.py:502 matches any key ending 'id', "
                       "so EmailID qualifies).")

    name = hop.get("name", "")
    if DESTRUCTIVE_TOKEN.search(name) and not DESTRUCTIVE_ANCHORED.match(name) \
            and not hop.get("skipped"):
        out.append(f"Endpoint name {name!r} contains a destructive token, but the guard "
                   "at chain_runner.py:84 is anchored with ^ - so this call was issued.")
    if hop.get("skipped"):
        out.append(f"Not executed: {hop['skipped']}")
    if flowctx.get("stopped_here"):
        out.append(f"The flow stopped after this hop; "
                   f"{flowctx['lost']} planned hop(s) never ran.")
    if ctx.get("consumed_unresolved"):
        out.append("This hop was sent with unresolved placeholder(s) "
                   + ", ".join("${%s}" % k for k in ctx["consumed_unresolved"])
                   + " - the literal token was transmitted, not a value.")
    return out


# ----------------------------------------------------------------- main extraction
def build_rows():
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    defs = load_flow_defs()
    rows, l6rows = [], []
    stats = {
        "tally": Counter(), "l5_cause": Counter(), "l5_by_controller": Counter(),
        "l5_by_endpoint": Counter(), "l5_cause_by_endpoint": defaultdict(Counter),
        "depth": Counter(), "reach": Counter(), "l6_rootcause": Counter(),
        "planned_lost": 0, "flows_truncated": 0, "starved_hops": 0,
        "starved_flows": 0, "placeholder_hops": 0, "cause_examples": defaultdict(list),
        "hops": 0, "skipped": 0, "flow_verdict": Counter(), "unresolved_hops": 0,
        "unresolved_by_var": Counter(), "l5_stop": Counter(), "l5_prefix": Counter(),
        "layer_fail_patterns": defaultdict(Counter), "l5_cause_ctrl": defaultdict(Counter),
    }

    for flow in data["flows"]:
        fid = flow["id"]
        fdef = defs.get(fid, {})
        hopdefs = fdef.get("hops", [])
        planned = fdef.get("planned", len(flow["hops"]))
        executed = flow["hops"]
        stats["flow_verdict"][flow.get("verdict", "")] += 1

        # producer map: variable -> (hop n, hop name) of the last hop that published it.
        # Pre-seeded with the run's per-run identity variables: run_flow() is handed the
        # seed dict (chain_runner.py:538 `vars = dict(vars)`), so those placeholders
        # resolve from hop 1 onward and are NOT starved dependencies.
        produced: dict[str, tuple[int, str]] = {
            k: (0, "run seed") for k in data.get("seed", {})}
        # which vars were available before each hop
        l5_fail_hop = None
        for idx, hop in enumerate(executed):
            n = hop.get("n", idx + 1)
            hopdef = hopdefs[n - 1] if n - 1 < len(hopdefs) else {}
            ev = load_evidence(hop.get("evidence", ""))
            resp = ev.get("response")
            env = env_read(resp)
            checks = {c["layer"]: c for c in hop.get("checks", [])}
            ctx = {"env": env, "request_body": ev.get("request_body")}
            hop["_expect_created"] = bool(hopdef.get("expect_created"))

            consumed = placeholders_of(hopdef)
            dep_parts, unresolved = [], []
            for var in consumed:
                if var in produced:
                    pn, pname = produced[var]
                    dep_parts.append(f"{var} <- hop {pn} {pname}")
                else:
                    unresolved.append(var)
                    dep_parts.append(f"{var} <- UNRESOLVED (never published upstream)")
            ctx["consumed_unresolved"] = unresolved
            if unresolved:
                stats["unresolved_hops"] += 1
                for var in unresolved:
                    stats["unresolved_by_var"][var] += 1

            # L5 cause, only meaningful on a failing chain-key check
            l5 = checks.get("L5")
            if l5 and l5["verdict"] == "FAIL":
                cause, why = l5_cause(hop, resp)
                ctx["l5_cause"], ctx["l5_why"] = cause, why
                stats["l5_cause"][cause] += 1
                ctrl = fdef.get("controller") or fid.split("__")[0]
                stats["l5_by_controller"][ctrl] += 1
                stats["l5_by_endpoint"][f"{hop['verb']} {hop['path']}"] += 1
                stats["l5_cause_by_endpoint"][cause][f"{hop['name']} ({ctrl})"] += 1
                stats["l5_cause_ctrl"][ctrl][cause] += 1
                pref = re.match(r"^(Set|Insert|Add|Save|Create)", hop["name"])
                stats["l5_prefix"][(pref.group(1) if pref else "other")] += 1
                stats["l5_stop"][
                    "flow stopped here - no later hop executed"
                    if idx == len(executed) - 1 else
                    "flow continued past this hop"] += 1
                stats["l5_stop"][f"  tier {fdef.get('tier')}"] += 1
                if len(stats["cause_examples"][cause]) < 6:
                    stats["cause_examples"][cause].append(
                        f"{fid} hop {n} {hop['name']} -> {why[:150]}")
                l5_fail_hop = n

            # L6
            l6 = checks.get("L6")
            l6_triple = None
            if l6:
                searched = ""
                m = re.search(r"created record id=(.*?) -> ", l6["detail"])
                if m:
                    searched = m.group(1)
                else:
                    m2 = re.search(r"for (\S+?=\S+?) -> ", l6["detail"])
                    searched = m2.group(1) if m2 else ""
                if l6["verdict"] == "PASS":
                    l6_triple = ("VERIFIED - the created record was found in the "
                                 "read-back",
                                 "None - the id published by the create was located in "
                                 "the read-back response.",
                                 "None required.")
                else:
                    l6_triple = l6_cause(resp, l6["detail"], searched)
                ctx["l6_triple"] = l6_triple
                if "${" in searched:
                    stats["placeholder_hops"] += 1
                stats["l6_rootcause"][l6_triple[0]] += 1

                # upstream create hop, for object_created
                up = next((h for h in executed if h.get("n") == n - 1), None)
                upev = load_evidence(up.get("evidence", "")) if up else {}
                upenv = env_read(upev.get("response"))
                created_desc = "UNKNOWN - no preceding hop recorded"
                if up:
                    got = up.get("extracted") or {}
                    created_desc = (
                        f"hop {up.get('n')} {up.get('name')} -> HTTP {up.get('status')}, "
                        f"Success={upenv['success']}, "
                        f"Message={(upenv['message'] or upenv['error_message'])[:80]!r}, "
                        f"extracted={got or 'NONE'}"
                        + (f" (id field used: {up.get('id_field_used')!r})"
                           if up.get("id_field_used") else ""))
                l6rows.append({
                    "api": hop["name"],
                    "flow_id": fid,
                    "hop_number": n,
                    "object_created": created_desc,
                    "expected_read": (
                        f"{hop['verb']} {hop['path']} returns a record in which "
                        f"{searched or 'the created id'} appears, proving the object "
                        "written by the preceding hop is readable back"),
                    "actual_read": (
                        f"HTTP {hop.get('status')}, shape={env['shape']}, "
                        f"Success={env['success']}, Message={env['message'][:80]!r}, "
                        f"ErrorCode={env['error_code'] or 'NONE'}, "
                        f"Result={env['result_type']}"
                        + (f"[{env['result_len']}]" if env["result_len"] is not None else "")
                        + f" -> {l6['detail']}"),
                    "failure_reason": l6_triple[1] if l6["verdict"] == "FAIL" else "None",
                    "root_cause": l6_triple[0],
                    "suggested_solution": l6_triple[2],
                    "verdict": l6["verdict"],
                })

            # ---- level columns
            levels = {}
            for layer, col in LAYER_COLUMN.items():
                c = checks.get(layer)
                if not c:
                    levels[col] = "NOT RUN — this hop declares no such expectation"
                else:
                    levels[col] = f"{c['verdict']} — {c['detail']}"

            # ---- expected / actual / reason / fix
            expected_bits = []
            for layer in ("L1", "L2", "L3", "L4", "L5", "L6", "L7"):
                if layer in checks:
                    expected_bits.append(f"{layer}: {LAYER_INTENT[layer]}")
            if hop.get("skipped"):
                expected = "Hop was planned but not executed."
            else:
                expected = "; ".join(expected_bits) or "No expectation declared."

            reasons, fixes = [], []
            for layer in ("L1", "L2", "L3", "L4", "L5", "L6", "L7"):
                c = checks.get(layer)
                if c and c["verdict"] == "FAIL":
                    r, fx = layer_reason(layer, c["detail"], hop, resp, ctx)
                    reasons.append(f"[{layer}] {r}")
                    if fx and fx not in fixes:
                        fixes.append(fx)

            if hop.get("skipped"):
                status_col = "SKIPPED"
            elif not checks:
                status_col = "NOT RUN"
            elif reasons:
                status_col = "FAIL"
            else:
                status_col = "PASS"

            actual = (f"HTTP {hop.get('status')}, {hop.get('latency_ms')} ms, "
                      f"{hop.get('body_bytes')} bytes, content_type="
                      f"{hop.get('content_type') or 'NONE'}, shape={env['shape']}, "
                      f"Success={env['success']}, "
                      f"Message={(env['message'] or env['error_message'])[:120]!r}, "
                      f"Result={env['result_type']}"
                      + (f"[{env['result_len']}]" if env["result_len"] is not None else "")
                      + f", extracted={hop.get('extracted') or {}}")
            if hop.get("skipped"):
                actual = f"NOT EXECUTED — {hop['skipped']}"

            # flow truncation bookkeeping
            stopped_here = (idx == len(executed) - 1 and len(executed) < planned)
            flowctx = {"stopped_here": stopped_here, "lost": planned - len(executed)}

            obs = observations(hop, hopdef, resp, ctx, flowctx)

            gen = hop.get("extracted") or {}
            gen_nonempty = {k: v for k, v in gen.items() if v not in (None, "", [])}
            if gen_nonempty:
                generated_id = ", ".join(
                    f"{k}={v!r}" for k, v in gen_nonempty.items())
                if hop.get("id_field_used"):
                    generated_id += f" (id field: {hop['id_field_used']})"
                for k in gen_nonempty:
                    produced[k] = (n, hop["name"])
            else:
                generated_id = "NONE"

            prev = executed[idx - 1] if idx > 0 else None
            nxt = executed[idx + 1] if idx + 1 < len(executed) else None

            rows.append({
                "flow_id": fid,
                "flow_title": flow.get("title", ""),
                "hop_number": n,
                "api_name": hop.get("name", ""),
                "verb": hop.get("verb", ""),
                "path": hop.get("path", ""),
                "parent_api": prev.get("name") if prev else None,
                "child_api": nxt.get("name") if nxt else None,
                "dependency": "; ".join(dep_parts) if dep_parts
                              else "NONE — this hop needs nothing from its parent",
                "input_data": json.dumps({
                    "resolved_path": hop.get("path"),
                    "request_body": ev.get("request_body"),
                    "vars_consumed": {var: (produced.get(var, ("?", "?"))[1]
                                            if var in produced else "UNRESOLVED")
                                      for var in consumed},
                }, default=str)[:3000],
                "generated_id": generated_id,
                **levels,
                "expected_result": expected,
                "actual_result": actual,
                "failure_reason": " | ".join(reasons) if reasons else "None",
                "required_fix": " | ".join(fixes) if fixes else "None",
                "validation_status": status_col,
                "additional_observations": " ".join(obs) if obs else "None",
                # traceability extras
                "controller": fdef.get("controller") or fid.split("__")[0],
                "flow_tier": fdef.get("tier"),
                "flow_verdict": flow.get("verdict", ""),
                "http_status": hop.get("status"),
                "latency_ms": hop.get("latency_ms"),
                "l5_cause_bucket": ctx.get("l5_cause", ""),
                "evidence_file": hop.get("evidence", ""),
            })
            stats["hops"] += 1
            if hop.get("skipped"):
                stats["skipped"] += 1
            for layer, c in checks.items():
                stats["tally"][(layer, c["verdict"])] += 1
                if c["verdict"] == "FAIL":
                    norm = re.sub(r"'[^']*'", "'…'", c["detail"])
                    norm = re.sub(r"\d+", "N", norm)[:80]
                    stats["layer_fail_patterns"][layer][norm] += 1

        # per-flow depth
        ran = [h for h in executed if not h.get("skipped")]
        stats["depth"][len(ran)] += 1
        for k in range(1, len(ran) + 1):
            stats["reach"][k] += 1
        if len(executed) < planned:
            stats["flows_truncated"] += 1
            stats["planned_lost"] += planned - len(executed)
            if l5_fail_hop is not None:
                stats["starved_flows"] += 1
                stats["starved_hops"] += planned - len(executed)

    return rows, l6rows, stats, data


# ----------------------------------------------------------------- reporting
def print_stats(rows, l6rows, stats, data):
    def head(t):
        print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)

    head("row counts")
    print(f"chaining-validation rows : {len(rows)}  (brief: {BRIEF['hops']} hops)")
    print(f"l6-read-back rows        : {len(l6rows)}  (brief: 107)")
    print(f"flows                    : {len(data['flows'])}  (brief: {BRIEF['flows']})")
    print(f"hops not executed (skipped): {stats['skipped']}")

    head("check tallies vs the brief")
    ok = True
    for layer in ("L1", "L2", "L3", "L4", "L5", "L6", "L7"):
        p = stats["tally"][(layer, "PASS")]
        f = stats["tally"][(layer, "FAIL")]
        bp, bf = BRIEF[layer]
        flag = "OK" if (p, f) == (bp, bf) else "*** MISMATCH ***"
        ok &= (p, f) == (bp, bf)
        print(f"  {layer}  PASS {p:>5} / FAIL {f:>5}   brief {bp:>5}/{bf:<5} {flag}")
    print(f"  flow verdicts: {dict(stats['flow_verdict'])}")
    print("  ALL FIGURES AGREE WITH THE BRIEF" if ok else
          "  *** DISCREPANCY - do not overwrite the brief silently ***")

    head("L5 'MISSING [NEW_ID]' cause split")
    tot = sum(stats["l5_cause"].values())
    for k in ("a", "b", "c", "d"):
        v = stats["l5_cause"].get(k, 0)
        print(f"  cause {CAUSE_LABEL[k]:<66} {v:>4}  "
              f"{(100.0 * v / tot if tot else 0):.1f}%")
    print(f"  total {tot}")
    for k in ("a", "b", "c", "d"):
        if stats["cause_examples"].get(k):
            print(f"\n  -- examples, cause {k}")
            for e in stats["cause_examples"][k]:
                print(f"     {e}")

    head("L5 failures by controller")
    for c, v in stats["l5_by_controller"].most_common():
        print(f"  {v:>4}  {c}")
    print(f"  controllers touched: {len(stats['l5_by_controller'])}")

    head("L5 failures by endpoint (top 25 of %d)" % len(stats["l5_by_endpoint"]))
    for c, v in stats["l5_by_endpoint"].most_common(25):
        print(f"  {v:>4}  {c}")

    head("chain depth achieved (hops actually executed per flow)")
    for k in sorted(stats["depth"]):
        print(f"  {k:>3} hops : {stats['depth'][k]:>4} flows")
    print("  cumulative reach:")
    for k in sorted(stats["reach"]):
        if k <= 8:
            print(f"    reached hop {k:>2} : {stats['reach'][k]:>4} flows")
    six_plus = sum(v for k, v in stats["depth"].items() if k >= 6)
    print(f"    reached hop 6 or deeper : {six_plus} flows")

    head("cascade")
    print(f"  flows truncated before their last planned hop : {stats['flows_truncated']}")
    print(f"  planned hops never executed                   : {stats['planned_lost']}")
    print(f"  of those, in flows whose create failed L5     : "
          f"{stats['starved_hops']} hops across {stats['starved_flows']} flows")
    print(f"  hops sent with an unresolved placeholder      : {stats['unresolved_hops']}")
    print(f"  L6 checks searching for the literal '${{NEW_ID}}' : "
          f"{stats['placeholder_hops']}")

    head("unresolved placeholders, by variable")
    for k, v in stats["unresolved_by_var"].most_common():
        print(f"  {v:>4}  ${{{k}}}")

    head("L5-failing create hops - endpoint name prefix and flow outcome")
    for k, v in stats["l5_prefix"].most_common():
        print(f"  {v:>4}  {k}*")
    for k, v in stats["l5_stop"].most_common():
        print(f"  {v:>4}  {k}")

    head("cause split by controller (controllers with 3+ L5 failures)")
    for ctrl, cc in sorted(stats["l5_cause_ctrl"].items(),
                           key=lambda t: -sum(t[1].values())):
        if sum(cc.values()) < 3:
            continue
        print(f"  {sum(cc.values()):>3}  {ctrl:<24} "
              + "  ".join(f"{k}={cc[k]}" for k in ("a", "b", "c", "d") if cc.get(k)))

    head("failure-detail patterns per layer (top 6 each)")
    for layer in ("L1", "L2", "L3", "L4", "L5", "L6", "L7"):
        pats = stats["layer_fail_patterns"][layer]
        if not pats:
            continue
        print(f"  {layer} ({sum(pats.values())} failures)")
        for k, v in pats.most_common(6):
            print(f"      {v:>4}  {k}")

    head("L6 root-cause split")
    for k, v in stats["l6_rootcause"].most_common():
        print(f"  {v:>4}  {k}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    if not RESULTS.exists():
        raise SystemExit(f"missing {RESULTS}")
    rows, l6rows, stats, data = build_rows()
    print_stats(rows, l6rows, stats, data)

    if args.stats:
        print("\n--stats: nothing written")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "chaining-validation.json").write_text(
        json.dumps(rows, indent=1, default=str), encoding="utf-8")
    (OUT_DIR / "l6-read-back.json").write_text(
        json.dumps(l6rows, indent=1, default=str), encoding="utf-8")
    print(f"\nwritten: {OUT_DIR / 'chaining-validation.json'} ({len(rows)} rows)")
    print(f"written: {OUT_DIR / 'l6-read-back.json'} ({len(l6rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
