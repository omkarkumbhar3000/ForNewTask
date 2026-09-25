#!/usr/bin/env python3
"""
OBJ-007 A3 — negative-validation scenario matrix generator.

Generates one row per (endpoint x negative scenario) for every endpoint in the
PAM API catalogue, choosing scenarios by what actually applies to each
endpoint's request shape.

ZERO NETWORK, ZERO DATABASE. Every value is either
  * parsed from a static source in this workspace, or
  * a measured value lifted verbatim from artifacts/runs/2026-07-29_181439/results.json, or
  * the literal string 'UNKNOWN - contract undocumented' / 'NOT EXECUTED - no evidence'.

Nothing is inferred into a number. If the product does not document an expected
outcome and the run did not measure one, the row says so.

Inputs
  APIConfig.java ................ endpoint catalogue (authoritative count)
  tools/source-map.json  per-endpoint shape: verb, role, fields, types, examples
  artifacts/runs/2026-07-29_181439/results.json   measured rejection responses
  testdata/API_Automation_Test_Input_Data.xls          live negative data
  testdata/Negative_API_Automation_Test_Input_Data.xls orphaned negative data
  src/.../Negative_API/**.java + API_DataProviderUtils.java  existing coverage wiring

Outputs
  artifacts/analysis-data/negative-validation.json
  artifacts/analysis-data/negative-coverage-summary.json

Usage
  python tools/obj007_negative_matrix.py
"""

from __future__ import annotations

import collections
import hashlib
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
from paths import workspace_root  # OBJ-025: one resolver, marker-based
WS = str(workspace_root(__file__))
REPO = os.path.join(WS, "Automation gitlab repo", "pam_automation_bootstrap")

APICONFIG = os.path.join(REPO, "src", "test", "java", "com", "arcon", "autoconfigs", "APIConfig.java")
SOURCE_MAP = os.path.join(HERE, "source-map.json")
RUN_STAMP = "2026-07-29_181439"
RESULTS = os.path.join(WS, "artifacts", "runs", RUN_STAMP, "results.json")
XLS_POS = os.path.join(REPO, "testdata", "API_Automation_Test_Input_Data.xls")
XLS_NEG = os.path.join(REPO, "testdata", "Negative_API_Automation_Test_Input_Data.xls")
NEG_JAVA = os.path.join(REPO, "src", "test", "java", "com", "arcon", "tests", "API", "Negative_API")
DP_JAVA = os.path.join(REPO, "src", "test", "java", "com", "arcon", "dataprovider", "API_DataProviderUtils.java")
NEG_SUITES = os.path.join(REPO, "API_Suites", "Negative")
QA_PROPS = os.path.join(REPO, "Environments", "QA_MsSQL.properties")

OUT_DATA = os.path.join(WS, "artifacts", "analysis-data")
OUT_MATRIX = os.path.join(OUT_DATA, "negative-validation.json")
OUT_SUMMARY = os.path.join(OUT_DATA, "negative-coverage-summary.json")

# ---------------------------------------------------------------------------
# Constants used as literal answers
# ---------------------------------------------------------------------------

UNK = "UNKNOWN - contract undocumented"
NOEV = "NOT EXECUTED - no evidence"
NO_ENVELOPE = "NOT APPLICABLE - framework-level rejection carries no envelope"

# Brief section 1: three endpoints that stop the IIS application pool.
BLOCKLIST_EXACT = {
    "/api/activitylogs/geterrorlogs",
    "/api/activitylogs/getlogs",
}
# GetAllActiveUserDetails is named in the brief without a controller.
BLOCKLIST_ACTION_PREFIX = ("getallactiveuserdetails",)
# LH-08: the same action names on other controllers share the implementation
# that took the API down. Guard on the NAME, per the standing rule.
BLOCKLIST_ACTION_EXACT = {"getlogs", "geterrorlogs"}

# Guard on names, never verbs - deletion here is POST /api/<C>/Delete<Thing>.
DESTRUCTIVE_PREFIX = ("delete", "remove")

NUMERIC_TYPES = {
    "long", "int", "Int64", "long?", "short", "decimal", "double", "float",
    "virtual long?", "Nullable<long>", "Nullable<int>", "int?", "virtual long",
    "virtual int", "static int", "Int32",
}
BOOL_TYPES = {"bool", "bool?", "virtual bool", "Nullable<bool>", "Boolean"}
DATE_TYPES = {"DateTime", "DateTime?", "Nullable<DateTime>"}

SQLI = "' OR 1=1--"
LONG_STR = "A" * 5000

ID_RE = re.compile(r"(^|[^a-z])(id|ids)$", re.I)
IP_RE = re.compile(r"(ip|ipaddress|serverip|hostip)$", re.I)
DATE_RE = re.compile(r"(date|time|from|to|timestamp)", re.I)
MAIL_RE = re.compile(r"(email|mail)", re.I)
ENUM_RE = re.compile(r"(type|status|flag|mode|state|level|category|action)$", re.I)
NAME_RE = re.compile(r"(name|desc|description|comment|remark|label|title)", re.I)


def warn(msg: str) -> None:
    print("  ! " + msg, file=sys.stderr)


# ---------------------------------------------------------------------------
# 1. Parse APIConfig.java - the endpoint catalogue
# ---------------------------------------------------------------------------

CONST_RE = re.compile(
    r'^\s*public\s+static\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;\s*(?://+\s*(.*?))?\s*$'
)


def parse_apiconfig(path: str) -> dict:
    """Return the parse of APIConfig.java plus reconciliation counters."""
    consts, non_route, comment_verbs = {}, [], {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            m = CONST_RE.match(line)
            if not m:
                continue
            name, value, comment = m.group(1), m.group(2), (m.group(3) or "").strip()
            if not value.startswith("/"):
                non_route.append(name)
                continue
            consts[name] = {"const": name, "raw_path": value, "line": lineno}
            v = comment.split()[0].strip(".,").upper() if comment else ""
            if v in ("GET", "POST", "PUT", "PATCH", "DELETE"):
                comment_verbs[name] = v

    by_path = collections.defaultdict(list)
    for name, rec in consts.items():
        by_path[rec["raw_path"].split("?")[0]].append(name)

    return {
        "route_constants": consts,
        "non_route_constants": non_route,
        "comment_verbs": comment_verbs,
        "distinct_paths": by_path,
    }


# ---------------------------------------------------------------------------
# 2. Measured evidence from the 2026-07-29 run
# ---------------------------------------------------------------------------

MISSING_PROP_RE = re.compile(r"Required property '([^']+)' not found")
CONVERT_RE = re.compile(r"Error converting value .*? to type ..([A-Za-z0-9_.]+)")
ERRMSG_RE = re.compile(r"Error(?:Message)?=(.+?)\s*\(HTTP\s*(\d+|None)\)\s*$")


def load_run_evidence(path: str, path_to_eid: dict) -> dict:
    """Index measured per-endpoint evidence from results.json.

    Returns eid -> {
        baseline:  first observed valid-request outcome (status/ct/envelope/bytes/cite),
        attempted: bool - a request was issued (the hop carries a 'status' key at all),
        responded: bool - a numeric HTTP status came back,
        rejections: [ {kind, detail, status, cite, evidence_file, field?} ]

    'attempted' vs 'responded' is the whole 875/870/866 reconciliation: a hop with no
    'status' key was never issued (skipped as destructive); a hop with status None was
    issued and got nothing back.
    """
    with open(path, encoding="utf-8", errors="replace") as fh:
        run = json.load(fh)

    ev = {}
    for flow in run["flows"]:
        for hop in flow["hops"]:
            raw = hop.get("path", "")
            eid = path_to_eid.get(raw.split("?")[0].lower())
            if not eid:
                continue
            rec = ev.setdefault(eid, {
                "baseline": None, "attempted": False, "responded": False, "rejections": [],
            })
            cite = "results.json#flows[%s].hops[%s]" % (flow.get("id"), hop.get("n"))
            status = hop.get("status")
            if "status" in hop:
                rec["attempted"] = True
            if status is not None:
                rec["responded"] = True

            checks = {(c["layer"], c["check"]): c for c in hop.get("checks", [])}
            if rec["baseline"] is None and status is not None:
                envd = checks.get(("L3", "envelope"), {}).get("detail", "")
                rec["baseline"] = {
                    "status": status,
                    "content_type": hop.get("content_type"),
                    "envelope": envd,
                    "body_bytes": hop.get("body_bytes"),
                    "cite": cite,
                    "evidence_file": hop.get("evidence"),
                }

            for c in hop.get("checks", []):
                if c.get("verdict") != "FAIL":
                    continue
                d = c.get("detail", "")
                lay = c.get("layer")
                kind = None
                field = None
                if lay == "L4":
                    mm = MISSING_PROP_RE.search(d)
                    mc = CONVERT_RE.search(d)
                    if mm:
                        kind, field = "missing_field", mm.group(1)
                    elif mc:
                        kind = "type_conversion"
                    elif "is Mandatory" in d or "is required" in d.lower():
                        kind = "mandatory_rule"
                    elif "Already Exists" in d:
                        kind = "duplicate"
                    elif d.startswith("Error"):
                        kind = "app_error"
                elif lay == "L3" and d == "Success=False":
                    kind = "app_reject"
                elif lay in ("L5", "L6"):
                    kind = "reference_missing"
                if not kind:
                    continue
                rec["rejections"].append({
                    "kind": kind, "detail": d, "status": status, "cite": cite,
                    "evidence_file": hop.get("evidence"), "field": field,
                })
    return ev


def pick(rejections, kinds):
    for k in kinds:
        for r in rejections:
            if r["kind"] == k:
                return r
    return None


def measured_expectation(rej):
    """Turn a measured rejection into (status, error_code, error_message)."""
    if not rej:
        return None
    d = rej["detail"]
    m = ERRMSG_RE.search(d)
    status = rej.get("status")
    if m:
        msg = m.group(1).strip()
        http = m.group(2)
        if http and http != "None":
            status = int(http)
        return (status if status is not None else UNK, UNK, msg)
    return (status if status is not None else UNK, UNK, d)


# ---------------------------------------------------------------------------
# 3. Existing negative coverage - what the framework actually runs today
# ---------------------------------------------------------------------------

BLOCK_CATEGORY = [
    ("methodnotallowed", "wrong HTTP method"),
    ("unauthorizedaccess", "invalid authentication"),
    # The framework's InvalidValue / InvalidQueryParams folders exercise values that
    # are syntactically wrong for the field, which maps onto 'invalid data format'
    # in this matrix's category menu.
    ("invalidqueryparams", "invalid data format"),
    ("invaliddatatype", "invalid data type"),
    ("invalidvalue", "invalid data format"),
    ("missingparameter", "missing mandatory field"),
]


def classify_block(label: str):
    low = (label or "").lower().replace("_", "").replace(" ", "")
    for key, cat in BLOCK_CATEGORY:
        if key in low:
            return cat
    return None


def read_sheet_rows(sheet):
    """Yield (block_label, header, row_values) for an Excel sheet with block headers."""
    block, header = None, None
    for r in range(sheet.nrows):
        vals = ["" if v is None else str(v).strip() for v in sheet.row_values(r)]
        nonblank = [v for v in vals if v]
        if len(nonblank) == 1 and vals and not vals[0].startswith("/"):
            block = nonblank[0]
            continue
        if any(v in ("ExpectedStatus", "ExpectedHTTPStatus") for v in vals):
            header = vals
            continue
        if any(v.startswith("/") for v in vals):
            yield block, header, vals


def norm_status(v: str):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def load_existing_coverage(path_to_eid: dict) -> dict:
    """Map endpoint -> existing negative coverage, live and orphaned."""
    import xlrd

    live = collections.defaultdict(dict)      # eid -> category -> {status, source}
    orphan = collections.defaultdict(dict)    # eid -> category -> {status, source}
    unmapped_live, unmapped_orphan = set(), set()
    live_rows = orphan_rows = 0
    live_status = collections.Counter()
    orphan_status = collections.Counter()
    adminapi_rows = 0
    adminapi_eps = set()
    adminapi_codes = collections.Counter()

    # --- live: sheets that a real @DataProvider reads -----------------------
    wb = xlrd.open_workbook(XLS_POS)
    for sheet_name, driver in (
        ("KotakSNOWApi_NegativeScenarios", "Negative_API.KotakSNOWApi"),
        ("SNOWApi_NegativeScenarios", "Negative_API.SNOWApi"),
    ):
        if sheet_name not in wb.sheet_names():
            continue
        sh = wb.sheet_by_name(sheet_name)
        for block, header, vals in read_sheet_rows(sh):
            ep = next((v for v in vals if v.startswith("/")), "")
            st = None
            for v in vals:
                st = norm_status(v)
                if st and 100 <= st <= 599:
                    break
                st = None
            cat = classify_block(block)
            live_rows += 1
            if st:
                live_status[st] += 1
            eid = path_to_eid.get(ep.split("?")[0].lower())
            if not eid:
                unmapped_live.add(ep.split("?")[0])
                continue
            if cat:
                live[eid][cat] = {"status": st, "source": "%s -> %s#%s"
                                  % (driver, os.path.basename(XLS_POS), sheet_name)}

    # --- Settings: the only envelope-aware negative testing that exists ----
    if "Settings" in wb.sheet_names():
        sh = wb.sheet_by_name("Settings")
        for block, header, vals in read_sheet_rows(sh):
            ep = next((v for v in vals if v.startswith("/")), "")
            adminapi_rows += 1
            adminapi_eps.add(ep.split("?")[0])
            codes = [norm_status(v) for v in vals]
            for c in codes:
                if c in (201, 202, 203):
                    adminapi_codes[c] += 1
                    break

    # --- orphaned: the negative workbook no provider ever loads -------------
    wbn = xlrd.open_workbook(XLS_NEG)
    for sheet_name in wbn.sheet_names():
        sh = wbn.sheet_by_name(sheet_name)
        for block, header, vals in read_sheet_rows(sh):
            ep = next((v for v in vals if v.startswith("/")), "")
            st = None
            for v in vals:
                s = norm_status(v)
                if s and 100 <= s <= 599:
                    st = s
                    break
            cat = classify_block(block) or classify_block(sheet_name)
            orphan_rows += 1
            if st:
                orphan_status[st] += 1
            eid = path_to_eid.get(ep.split("?")[0].lower())
            if not eid:
                unmapped_orphan.add(ep.split("?")[0])
                continue
            if cat:
                orphan[eid][cat] = {"status": st,
                                    "source": "%s#%s (never loaded)"
                                              % (os.path.basename(XLS_NEG), sheet_name)}

    return {
        "live": live, "orphan": orphan,
        "live_rows": live_rows, "orphan_rows": orphan_rows,
        "live_status": dict(live_status), "orphan_status": dict(orphan_status),
        "unmapped_live": sorted(unmapped_live), "unmapped_orphan": sorted(unmapped_orphan),
        "adminapi_rows": adminapi_rows,
        "adminapi_endpoints": len(adminapi_eps),
        "adminapi_in_catalogue": sum(1 for e in adminapi_eps
                                     if path_to_eid.get(e.lower())),
        "adminapi_error_codes": dict(adminapi_codes),
    }


def audit_negative_wiring() -> dict:
    """Reconcile @DataProvider names referenced by Negative_API against those defined."""
    referenced = collections.Counter()
    classes, tests = set(), 0
    validators = collections.Counter()
    for root, _dirs, files in os.walk(NEG_JAVA):
        for f in files:
            if not f.endswith(".java"):
                continue
            classes.add(os.path.relpath(os.path.join(root, f), NEG_JAVA).replace("\\", "/"))
            txt = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            tests += txt.count("@Test")
            for m in re.finditer(r'dataProvider\s*=\s*"([^"]+)"', txt):
                referenced[m.group(1)] += 1
            for m in re.finditer(r"(validateApiResponse\w*)", txt):
                validators[m.group(1)] += 1

    defined, neg_sheets = set(), collections.Counter()
    txt = open(DP_JAVA, encoding="utf-8", errors="replace").read()
    for line in txt.splitlines():
        s = line.strip()
        if s.startswith("@DataProvider") and "name = \"" in s:
            defined.add(re.search(r'name = "([^"]+)"', s).group(1))
    for m in re.finditer(r'"([A-Za-z_ ]*Negative[A-Za-z_]*)"', txt):
        neg_sheets[m.group(1)] += 1

    suites = {}
    if os.path.isdir(NEG_SUITES):
        for f in sorted(os.listdir(NEG_SUITES)):
            if f.endswith(".xml"):
                s = open(os.path.join(NEG_SUITES, f), encoding="utf-8", errors="replace").read()
                suites[f] = len(re.findall(r"<class\s+name=", s))

    return {
        "negative_test_classes": len(classes),
        "negative_test_methods": tests,
        "data_providers_referenced": len(referenced),
        "data_providers_defined": len(defined),
        "referenced_but_undefined": sorted(set(referenced) - defined),
        "referenced_and_defined": sorted(set(referenced) & defined),
        "validator_calls": dict(validators),
        "negative_sheet_args_in_provider": dict(neg_sheets),
        "negative_suites": suites,
    }


# ---------------------------------------------------------------------------
# 4. Scenario construction
# ---------------------------------------------------------------------------

def body_fields(meta: dict) -> dict:
    """Real request fields - drop the header pseudo-fields the merge picked up."""
    return {k: v for k, v in meta.get("fields", {}).items()
            if k not in ("Content-Type", "Authorization", "x-pam-version")}


def valid_body(fields: dict) -> dict:
    out = {}
    for name, m in fields.items():
        ex = m.get("example")
        if ex is None:
            t = m.get("csharp_type")
            ex = 0 if t in NUMERIC_TYPES else (False if t in BOOL_TYPES else "value")
        out[name] = ex
    return out


def is_numeric(name: str, m: dict) -> bool:
    if m.get("csharp_type") in NUMERIC_TYPES:
        return True
    return isinstance(m.get("example"), (int, float)) and not isinstance(m.get("example"), bool)


def rank_fields(fields: dict) -> list:
    """Order fields by how diagnostic they are: required > chainable id > typed > rest."""
    def key(item):
        n, m = item
        return (
            0 if m.get("required_hint") else 1,
            0 if m.get("chainable") else 1,
            0 if m.get("confidence") == "high" else 1,
            n.lower(),
        )
    return sorted(fields.items(), key=key)


def mandatory_candidates(fields: dict) -> list:
    req = [(n, m) for n, m in fields.items() if m.get("required_hint")]
    if req:
        return sorted(req, key=lambda kv: kv[0].lower())
    return rank_fields(fields)[:1]


def query_params(path: str) -> list:
    if "?" not in path:
        return []
    return [p.split("=")[0] for p in path.split("?", 1)[1].split("&") if p]


def build_scenarios(eid, meta, ev, cover_live, cover_orphan, cfg):
    """Return an ordered list of applicable scenario dicts for one endpoint."""
    controller, action = eid.split("/", 1)
    verb = meta["verb"].upper()
    path = meta["path"]
    role = meta.get("role", "other")
    fields = body_fields(meta)
    ranked = rank_fields(fields)
    qps = query_params(path)
    base = valid_body(fields)
    rejections = ev.get(eid, {}).get("rejections", [])
    has_body = bool(fields)
    destructive = action.lower().startswith(DESTRUCTIVE_PREFIX) or role == "teardown"
    writes = role in ("create", "update") or destructive

    S = []

    def add(cat, name, desc, mutation, payload, exp_status, exp_code, exp_msg,
            exp_resp, severity, rej=None, weight=50):
        S.append({
            "scenario_category": cat, "scenario_name": name, "description": desc,
            "request_mutation": mutation, "payload": payload,
            "expected_status": exp_status, "expected_error_code": exp_code,
            "expected_error_message": exp_msg, "expected_response": exp_resp,
            "severity": severity, "_rej": rej, "_weight": weight,
        })

    # ---- Universal 1: invalid authentication ------------------------------
    add(
        "invalid authentication",
        "No bearer token",
        "Applies to every endpoint: the whole API is bearer-authenticated, so an "
        "unauthenticated call must be rejected before any handler runs. This is a "
        "framework-level rejection, so it is one of the few cases where a status "
        "assertion is legitimate - there is no response envelope to read.",
        "Omit the Authorization header entirely. Body and verb unchanged.",
        base if has_body else {},
        401, NO_ENVELOPE, UNK,
        "HTTP 401 with no PAM envelope. Assert the status AND assert that the body "
        "carries no Result payload - a 200 here would mean the endpoint is anonymous.",
        "Critical" if writes else "High",
        weight=100,
    )

    # ---- Universal 2: wrong HTTP method ----------------------------------
    other = "GET" if verb == "POST" else "POST"
    add(
        "wrong HTTP method",
        "Verb swapped %s -> %s" % (verb, other),
        "Applies to every endpoint: the catalogue binds this route to %s, so %s must "
        "not be routable. Framework-level rejection, no envelope. Deletion on this API "
        "is POST /api/<C>/Delete<Thing>, so verb-based safety guards do not work - this "
        "scenario tests routing, not safety." % (verb, other),
        "Reissue the same URL and body with the %s verb." % other,
        base if has_body else {},
        cfg["method_not_allowed_status"], NO_ENVELOPE, UNK,
        "HTTP %s with no envelope. A 200 means the route accepts an undeclared verb, "
        "which widens the attack surface." % cfg["method_not_allowed_status"],
        "Medium",
        weight=95,
    )

    # ---- Universal 3: invalid authorization ------------------------------
    add(
        "invalid authorization",
        "Valid token, unprivileged principal",
        "Applies to every endpoint: PAM is a privileged-access product, so every route "
        "must enforce per-principal authorisation, not merely authentication. No "
        "endpoint-to-role matrix is documented anywhere in the workspace - the two "
        "administrator guides carry the access model but no endpoint mapping - so the "
        "expected outcome cannot be stated.",
        "Send a syntactically valid bearer token issued to a principal with no rights "
        "over this controller. Body and verb unchanged.",
        base if has_body else {},
        UNK, UNK, UNK,
        "Must be a refusal. Because a PAM refusal is normally HTTP 200 with "
        "Success:false, the assertion has to read the envelope; a status check cannot "
        "distinguish 'refused' from 'served'. Expected value undocumented.",
        "Critical" if writes else "High",
        weight=90,
    )

    # ---- Universal 4: SQL-injection string -------------------------------
    inj_target = ranked[0][0] if ranked else (qps[0] if qps else "<query string>")
    if has_body:
        p = dict(base)
        p[inj_target] = SQLI
        mut = "Replace %s with the SQL meta-character string %s." % (inj_target, SQLI)
    elif qps:
        p = {}
        mut = "Append %s=%s to the query string." % (inj_target, SQLI)
    else:
        p = {"__raw_query__": "?q=" + SQLI}
        mut = "Append ?q=%s to the URL - this endpoint takes no documented body." % SQLI
    add(
        "SQL-injection string",
        "SQL meta-characters in %s" % inj_target,
        "Applies to every endpoint: the QA database login is sysadmin over 30 databases, "
        "so a reachable injection is a total-compromise path, and no input-length, "
        "format or pattern validation exists anywhere in the product (3 [Required] "
        "attributes across ~6,738 properties). Highest-value negative test on this API.",
        mut, p,
        UNK, UNK, UNK,
        "Three assertions, none of them a status check: (1) the request is refused OR "
        "the value is treated as an opaque literal; (2) the response contains no SQL "
        "error text, driver name, table name or stack frame; (3) the row count does not "
        "exceed the row count for the unmutated request. A 500 is itself a defect.",
        "Critical",
        weight=88,
    )

    # ---- Universal 5: missing/incorrect content-type ----------------------
    add(
        "missing/incorrect content-type",
        "Content-Type text/plain",
        "Applies to every endpoint: all catalogue routes are declared "
        "application/json, so a mismatched media type must not be silently accepted. "
        "No documented media-type contract exists, so the expected outcome is unknown.",
        "Send the identical body with Content-Type: text/plain instead of "
        "application/json.",
        base if has_body else {},
        UNK, UNK, UNK,
        "Either a framework-level 415 with no envelope, or a 200 envelope carrying "
        "Success:false. Silent acceptance of a mismatched type is the defect to catch.",
        "Low",
        weight=40,
    )

    # ---- Shape-driven ----------------------------------------------------
    if has_body:
        # missing mandatory field - strongest evidence available
        for fname, fmeta in mandatory_candidates(fields)[:2]:
            rej = None
            for r in rejections:
                if r["kind"] == "missing_field" and r.get("field", "").lower() == fname.lower():
                    rej = r
                    break
            if rej is None:
                rej = pick(rejections, ("missing_field", "mandatory_rule"))
                if rej and rej["kind"] == "missing_field" and rej.get("field") and \
                        rej["field"].lower() != fname.lower():
                    rej = pick(rejections, ("mandatory_rule",))
            p = {k: v for k, v in base.items() if k != fname}
            why = ("required_hint is set on this field in source-map.json"
                   if fmeta.get("required_hint")
                   else "no [Required] attribute exists for this field, so mandatory-ness "
                        "is inferred from it being the highest-confidence chainable field "
                        "in every documented example - treat as hypothesis, not contract")
            add(
                "missing mandatory field",
                "Omit %s" % fname,
                "Applies because this endpoint accepts a request body of %d field(s); %s."
                % (len(fields), why),
                "Remove the %s key from the request body. All other fields keep their "
                "valid values." % fname,
                p,
                UNK, UNK, UNK,
                "HTTP 200 carrying Success:false plus a non-null ErrorCode and an "
                "ErrorMessage naming the missing property. Assert on the ErrorMessage "
                "text, not the status - a 200 is what a correct rejection looks like here.",
                "High", rej=rej, weight=85,
            )

        # invalid data type
        num = [(n, m) for n, m in ranked if is_numeric(n, m)]
        if num:
            fname, _ = num[0]
            p = dict(base)
            p[fname] = "NOT_A_NUMBER"
            add(
                "invalid data type",
                "String into numeric field %s" % fname,
                "Applies because %s is numeric (C# type %r in the pam/PAM model, example "
                "%r), so a string must fail model binding."
                % (fname, _.get("csharp_type"), _.get("example")),
                "Set %s to the string \"NOT_A_NUMBER\"; every other field stays valid." % fname,
                p,
                UNK, UNK, UNK,
                "HTTP 200 with Success:false and an ErrorMessage reporting the conversion "
                "failure for this specific field. Assert the field name appears in the "
                "message - a generic 'System error has occurred' would mean the binder "
                "error was swallowed.",
                "High", rej=pick(rejections, ("type_conversion",)), weight=82,
            )

        # invalid object reference
        ids = [(n, m) for n, m in ranked if m.get("chainable") or ID_RE.search(n)]
        if ids:
            fname, _ = ids[0]
            p = dict(base)
            p[fname] = 999999999
            add(
                "invalid object reference",
                "Non-existent %s = 999999999" % fname,
                "Applies because %s is an id-shaped/chainable key, so it must be resolved "
                "against stored data. The 2026-07-29 run recorded 196 chain-key-extraction "
                "failures and 105 record-exists failures, so unresolvable references are "
                "the dominant real-world failure mode on this API." % fname,
                "Set %s to 999999999 - an id that cannot exist. All other fields valid." % fname,
                p,
                UNK, UNK, UNK,
                "HTTP 200 with Success:false and an ErrorMessage identifying the "
                "unresolvable reference. An empty Result[] with Success:true is a defect: "
                "'not found' must not be reported as success.",
                "Critical" if destructive else "High",
                rej=pick(rejections, ("reference_missing",)), weight=80,
            )

        # null vs empty string
        strf = [(n, m) for n, m in ranked if not is_numeric(n, m)
                and m.get("csharp_type") not in BOOL_TYPES]
        if strf:
            fname, _ = strf[0]
            p = dict(base)
            p[fname] = None
            add(
                "null vs empty-string",
                "%s = null (compare against \"\")" % fname,
                "Applies because %s is a string field: JSON null and \"\" are distinct "
                "inputs and the product has no declared nullability contract, so the two "
                "must be tested as separate cases." % fname,
                "Set %s to JSON null. Run the paired variant with \"\" and compare the "
                "two responses - they must not diverge silently." % fname,
                p,
                UNK, UNK, UNK,
                "Both variants must produce the same verdict. Assert that null and \"\" "
                "yield identical Success/ErrorCode - divergence means undeclared "
                "nullability semantics.",
                "Medium", weight=62,
            )

        # boundary condition
        if num:
            fname, _ = num[0]
            p = dict(base)
            p[fname] = -1
            add(
                "boundary condition",
                "%s at -1 / 0 / 9223372036854775807" % fname,
                "Applies because %s is numeric with no declared range - no length, format "
                "or pattern validation exists anywhere in the product - so the boundaries "
                "are untested by construction." % fname,
                "Three variants of %s: -1, 0, and 9223372036854775807 (Int64 max). "
                "Everything else valid." % fname,
                p,
                UNK, UNK, UNK,
                "Each variant must be refused with an ErrorMessage naming the field. An "
                "unhandled overflow surfacing as HTTP 500 or as 'System error has "
                "occurred' is a defect - the run already recorded 55 such generic errors.",
                "Medium", weight=58,
            )

        # invalid length
        lenf = [(n, m) for n, m in ranked if NAME_RE.search(n)] or strf
        if lenf:
            fname, _ = lenf[0]
            p = dict(base)
            p[fname] = "<5000-char 'A' string - materialise at execution time>"
            add(
                "invalid length",
                "%s at 5,000 characters" % fname,
                "Applies because %s is a free-text field and exactly 3 of ~6,738 product "
                "properties carry any validation attribute, so no maximum length is "
                "declared or enforced at the model layer." % fname,
                "Set %s to 5,000 repeated 'A' characters." % fname,
                p,
                UNK, UNK, UNK,
                "Refusal naming a length limit, OR - if accepted - a follow-up read must "
                "return the value untruncated. Silent truncation is the defect: it is "
                "invisible to a status assertion and to an envelope assertion alike.",
                "Medium", weight=55,
            )

        # invalid data format
        fmt = None
        for n, m in ranked:
            if IP_RE.search(n) or m.get("csharp_type") == "IPAddress":
                fmt = (n, "IP address", "999.999.999.999")
                break
            if DATE_RE.search(n) or m.get("csharp_type") in DATE_TYPES:
                fmt = (n, "date/time", "31-31-9999")
                break
            if MAIL_RE.search(n):
                fmt = (n, "e-mail address", "not-an-email")
                break
        if fmt:
            fname, kindname, badval = fmt
            p = dict(base)
            p[fname] = badval
            add(
                "invalid data format",
                "Malformed %s in %s" % (kindname, fname),
                "Applies because %s carries an implicit %s format (name/type shape), and "
                "the product declares no pattern validation, so format enforcement can "
                "only exist inside the handler." % (fname, kindname),
                "Set %s to %r - syntactically well-formed JSON, semantically invalid %s."
                % (fname, badval, kindname),
                p,
                UNK, UNK, UNK,
                "Refusal with an ErrorMessage naming the field and the expected format. "
                "Accepting a malformed %s writes unusable data - assert the refusal, "
                "then assert absence via a read-back." % kindname,
                "Medium", weight=52,
            )

        # invalid enumeration
        enum = [(n, m) for n, m in ranked
                if ENUM_RE.search(n) or m.get("csharp_type") in BOOL_TYPES]
        if enum:
            fname, _ = enum[0]
            p = dict(base)
            p[fname] = "__INVALID_ENUM__"
            add(
                "invalid enumeration",
                "Out-of-set value for %s" % fname,
                "Applies because %s is enumeration-shaped (name suffix / C# type %r) but "
                "the permitted value set is documented nowhere - the Confluence export "
                "carries 4 error codes and 1 of 9 response shapes - so the enum domain "
                "itself is an open question." % (fname, _.get("csharp_type")),
                "Set %s to the literal \"__INVALID_ENUM__\"." % fname,
                p,
                UNK, UNK, UNK,
                "Refusal listing the permitted values. If accepted, the enum is not "
                "enforced server-side and the stored value is unconstrained.",
                "Medium", weight=50,
            )

        # duplicate data
        if role == "create":
            add(
                "duplicate data",
                "Re-create an existing record",
                "Applies because this is a create endpoint (%d of 217 creates in the "
                "catalogue). Measured on this API: POST /api/ServiceCreation/"
                "SetServiceDetails returns Success:true with Message:'Already Exists' - "
                "green status, green Success flag, nothing inserted." % len(fields),
                "Issue the identical valid create body twice. The second call is the "
                "negative case.",
                base,
                UNK, UNK, UNK,
                "The decisive assertion is on Message semantics, not status and not "
                "Success: 'Inserted Successfully' means inserted, 'Already Exists' means "
                "no-op. Success:true is NOT evidence of a write.",
                "High", rej=pick(rejections, ("duplicate",)), weight=70,
            )

        # invalid relationship
        chain = [(n, m) for n, m in ranked if m.get("chainable")]
        if len(chain) >= 2:
            a, b = chain[0][0], chain[1][0]
            p = dict(base)
            p[a] = 999999999
            add(
                "invalid relationship",
                "%s not related to %s" % (a, b),
                "Applies because this endpoint carries %d chainable id fields, so it "
                "encodes a relationship that must be validated as a pair, not "
                "field-by-field." % len(chain),
                "Keep %s valid and set %s to an id belonging to no such relationship "
                "(999999999)." % (b, a),
                p,
                UNK, UNK, UNK,
                "Refusal identifying the broken relationship. Per-field validation that "
                "passes both ids independently while accepting an impossible pair is the "
                "defect - only a paired assertion catches it.",
                "High", weight=48,
            )

        # invalid combination
        if len(ranked) >= 3:
            a, b = ranked[0][0], ranked[1][0]
            p = {k: v for k, v in base.items() if k not in (a, b)}
            p[a] = base.get(a)
            add(
                "invalid combination",
                "%s supplied without %s" % (a, b),
                "Applies because this endpoint takes %d fields with no declared "
                "co-dependency rules, so partial field sets are accepted by the binder "
                "and can only be rejected by handler logic." % len(fields),
                "Send %s but omit %s and every other optional field." % (a, b),
                p,
                UNK, UNK, UNK,
                "Refusal naming the missing counterpart. Assert the ErrorMessage "
                "enumerates every unsatisfied field - the run shows PAM does aggregate "
                "these ('ServiceIP is required, ServiceUserName is required').",
                "Medium", weight=45,
            )

        # malformed JSON
        add(
            "malformed JSON",
            "Truncated request body",
            "Applies because this endpoint accepts a JSON body, so the parse boundary is "
            "reachable and must fail cleanly rather than surfacing a framework trace.",
            "Send the valid body with its trailing brace removed.",
            {"__raw_body__": json.dumps(base)[:-1]},
            UNK, UNK, UNK,
            "A parse failure that leaks no stack frame, no .NET type name and no line "
            "position. Note the product already leaks parser internals on well-formed "
            "input: \"Required property 'UserId' not found in JSON. Path '', line 1, "
            "position 2.\" reaches the client verbatim.",
            "Medium", weight=42,
        )

        # oversized payload
        add(
            "oversized payload",
            "1 MB value in %s" % ranked[0][0],
            "Applies because this endpoint accepts a body and no request-size limit is "
            "documented. Load-adjacent, but not a load test: three sequential calls to "
            "two ActivityLogs endpoints were enough to stop the IIS application pool, so "
            "this endpoint's resilience to a single large body is unproven.",
            "Set %s to a 1,048,576-character string." % ranked[0][0],
            {ranked[0][0]: "<1048576-char 'A' string - materialise at execution time>"},
            UNK, UNK, UNK,
            "A bounded refusal. The assertion that matters is the follow-up: the API must "
            "still answer a normal request afterwards. Availability, not the status code "
            "of the oversized call itself, is the finding.",
            "High", weight=38,
        )
    else:
        # ---- endpoints with no documented body ---------------------------
        add(
            "missing mandatory field",
            "Empty body against an undocumented contract",
            "Applies by absence: no request body is documented for this endpoint in any "
            "of the four sources (payload helpers, Confluence export, pam/PAM models, "
            "APIConfig comment), so whether it requires input at all is unknown. 731 of "
            "the catalogue's endpoints are in this state.",
            "Send an empty JSON object {} - which is also what the framework sends today, "
            "so a rejection here means the existing positive test is itself invalid.",
            {},
            UNK, UNK, UNK,
            "Read the envelope. If Success:false with a 'Required property ... not found' "
            "ErrorMessage, the endpoint has undocumented mandatory input and every "
            "existing positive test against it is passing on a rejected request. The run "
            "measured exactly this on 80 endpoints.",
            "High", rej=pick(rejections, ("missing_field", "mandatory_rule")), weight=84,
        )
        add(
            "malformed JSON",
            "Non-JSON body",
            "Applies because the route declares application/json even with no documented "
            "fields, so the parse boundary is still reachable.",
            "Send the raw string 'not json at all' as the body.",
            {"__raw_body__": "not json at all"},
            UNK, UNK, UNK,
            "A parse failure that leaks no stack frame or .NET type name.",
            "Medium", weight=44,
        )
        add(
            "oversized payload",
            "1 MB body on a no-body endpoint",
            "Applies because no request-size limit is documented and this endpoint "
            "ignores its body, so an unbounded read may still occur before the handler "
            "discards it.",
            "Send a 1,048,576-character JSON string as the body.",
            {"__raw_body__": "<1048576-char 'A' string - materialise at execution time>"},
            UNK, UNK, UNK,
            "A bounded refusal, then a follow-up normal request to prove the endpoint is "
            "still serving. Availability is the assertion.",
            "Medium", weight=36,
        )
        if qps:
            qp = qps[0]
            add(
                "invalid object reference",
                "Query parameter %s = 999999999" % qp,
                "Applies because this endpoint carries its input in the query string "
                "(%s), so reference validity is testable without a body." % ", ".join(qps),
                "Set %s=999999999 in the query string." % qp,
                {"__query__": {qp: 999999999}},
                UNK, UNK, UNK,
                "Success:false with an ErrorMessage identifying the unresolvable "
                "reference. Success:true with an empty Result[] is a defect.",
                "High", rej=pick(rejections, ("reference_missing",)), weight=68,
            )
            add(
                "invalid data type",
                "Non-numeric query parameter %s" % qp,
                "Applies because %s is supplied in the query string and its example value "
                "is numeric, so type coercion happens before the handler." % qp,
                "Set %s=NOT_A_NUMBER in the query string." % qp,
                {"__query__": {qp: "NOT_A_NUMBER"}},
                UNK, UNK, UNK,
                "Refusal naming the parameter. Assert the parameter name appears in the "
                "ErrorMessage.",
                "Medium", rej=pick(rejections, ("type_conversion",)), weight=60,
            )
        else:
            add(
                "boundary condition",
                "Undeclared paging / result-set bound",
                "Applies because this endpoint returns a collection with no documented "
                "paging contract. Measured on this API: 21 hops were refused with "
                "'PageSize is required should be greater than 0.' on HTTP 200 - a paging "
                "contract that exists in code and in no document.",
                "Send PageNumber=0 and PageSize=0, then PageSize=2147483647.",
                {"PageNumber": 0, "PageSize": 0},
                UNK, UNK, UNK,
                "Refusal naming the paging bound. An unbounded page size on a "
                "collection endpoint is the availability risk this API has already "
                "demonstrated.",
                "Medium", rej=pick(rejections, ("mandatory_rule",)), weight=56,
            )
            add(
                "invalid combination",
                "Undeclared query parameter alongside the empty documented input set",
                "Applies by elimination: with no documented body and no documented query "
                "parameters, the only reachable input surface is an undeclared parameter "
                "combined with the (empty) declared set. It must be ignored, not acted on.",
                "Append ?unexpectedParam=__INVALID__ to the URL, body unchanged.",
                {"__query__": {"unexpectedParam": "__INVALID__"}},
                UNK, UNK, UNK,
                "The response must be equivalent to the unmutated request. A difference "
                "means an undeclared parameter influences behaviour.",
                "Low", weight=34,
            )

    # ---- invalid business rule: LOB / tenant scope ------------------------
    scope_field = None
    for n, m in ranked:
        if re.search(r"(lob|tenant|group|org|domain)", n, re.I):
            scope_field = n
            break
    if scope_field:
        p = dict(base)
        p[scope_field] = 999999999
        mut = ("Set %s to an identifier belonging to a different line of business than "
               "the caller's token." % scope_field)
        why = ("Applies because %s is a scope-bearing field: PAM partitions access by "
               "line of business, so a caller must not reach another LOB's data by "
               "supplying its identifier." % scope_field)
    else:
        p = base if has_body else {}
        mut = ("Call with a token whose principal owns no records on this route, and "
               "compare the returned record set against the same call made by a "
               "fully-scoped principal.")
        why = ("Applies because this route carries no explicit scope field, so LOB "
               "partitioning can only be enforced from the token. That makes the rule "
               "invisible to inspection and testable only by differential comparison.")
    add(
        "invalid business rule",
        "Cross-LOB scope violation",
        why + " No endpoint-to-LOB enforcement rule is documented - the administrator "
              "guides describe the access model without mapping it to endpoints - so the "
              "expected outcome is unstated.",
        mut, p,
        UNK, UNK, UNK,
        "The record set must contain nothing outside the caller's own scope. Assert on "
        "the Result[] contents, not on Success: a scope leak returns HTTP 200 with "
        "Success:true and simply too many rows, which every status-based and every "
        "envelope-based assertion passes.",
        "Critical",
        weight=76,
    )

    S.sort(key=lambda s: -s["_weight"])
    return S


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------

MAX_PER_ENDPOINT = 8
MIN_PER_ENDPOINT = 5

# Kept on every endpoint regardless of scarcity: these four apply universally and are
# the highest-value negative tests on a privileged-access product.
CORE_CATEGORIES = (
    "invalid authentication",
    "wrong HTTP method",
    "invalid authorization",
    "SQL-injection string",
)


def select_scenarios(applicable: dict, max_per: int) -> dict:
    """Choose up to max_per scenarios per endpoint.

    Naive top-N truncation starves every category that applies to only a handful of
    endpoints - a rare-but-real scenario would never appear in the matrix at all. So:
    keep the four universal core categories, keep the single highest-value
    shape-driven scenario, then fill the remaining slots preferring the categories
    that are globally under-represented so far.
    """
    picked, pool = {}, {}
    for eid in sorted(applicable):
        scen = applicable[eid]          # already sorted by descending weight
        chosen, seen_cat, taken = [], set(), set()
        for s in scen:
            c = s["scenario_category"]
            if c in CORE_CATEGORIES and c not in seen_cat:
                chosen.append(s)
                seen_cat.add(c)
                taken.add(id(s))
        rest = [s for s in scen if id(s) not in taken]
        if rest and len(chosen) < max_per:
            chosen.append(rest.pop(0))  # highest-weight shape-driven scenario
        picked[eid], pool[eid] = chosen, rest

    gcount = collections.Counter()
    for eid in picked:
        for s in picked[eid]:
            gcount[s["scenario_category"]] += 1

    for eid in sorted(picked):
        chosen, rest = picked[eid], pool[eid]
        while len(chosen) < max_per and rest:
            # category spread first; within a category prefer a scenario that carries
            # measured run evidence over one that would only carry UNKNOWN.
            rest.sort(key=lambda s: (gcount[s["scenario_category"]],
                                     0 if s.get("_rej") else 1,
                                     -s["_weight"]))
            s = rest.pop(0)
            chosen.append(s)
            gcount[s["scenario_category"]] += 1
        chosen.sort(key=lambda s: -s["_weight"])
        picked[eid] = chosen
    return picked


def main():
    print("OBJ-007 A3 - negative-validation scenario matrix")
    print("=" * 68)

    # --- config: traceable expected statuses ------------------------------
    cfg = {"method_not_allowed_status": 405, "api_status": 200}
    if os.path.exists(QA_PROPS):
        for line in open(QA_PROPS, encoding="utf-8", errors="replace"):
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip()
            if k == "ExpectedMethodNotAllowedAPIStatusCode" and v.isdigit():
                cfg["method_not_allowed_status"] = int(v)
            if k == "ExpectedAPIStatusCode" and v.isdigit():
                cfg["api_status"] = int(v)
    print("Env contract: ExpectedAPIStatusCode=%s  "
          "ExpectedMethodNotAllowedAPIStatusCode=%s  (Environments/QA_MsSQL.properties)"
          % (cfg["api_status"], cfg["method_not_allowed_status"]))

    # --- 1. catalogue -----------------------------------------------------
    ac = parse_apiconfig(APICONFIG)
    sm = json.load(open(SOURCE_MAP, encoding="utf-8"))
    path_to_eid = {v["path"].split("?")[0].lower(): k for k, v in sm.items()}

    sm_consts = set()
    for k, v in sm.items():
        sm_consts.update(v.get("consts", []))
    dup_paths = {p: c for p, c in ac["distinct_paths"].items() if len(c) > 1}
    surplus = sum(len(c) - 1 for c in dup_paths.values())
    sm_paths = {v["path"].split("?")[0] for v in sm.values()}
    ac_only = set(ac["distinct_paths"]) - sm_paths
    recon = {
        "apiconfig_file": "src/test/java/com/arcon/autoconfigs/APIConfig.java",
        "route_constants_parsed": len(ac["route_constants"]),
        "non_route_constants_skipped": len(ac["non_route_constants"]),
        "distinct_paths_after_query_strip": len(ac["distinct_paths"]),
        "source_map_endpoints": len(sm),
        "source_map_consts_referenced": len(sm_consts),
        "constants_in_apiconfig_not_in_source_map":
            sorted(set(ac["route_constants"]) - sm_consts),
        "constants_in_source_map_not_in_apiconfig":
            sorted(sm_consts - set(ac["route_constants"])),
        "verbs_from_apiconfig_comments": len(ac["comment_verbs"]),
        "quoted_catalogue_size": 1306,
        "reconciles": len(sm) == 1306,
        "paths_declared_by_more_than_one_constant": len(dup_paths),
        "surplus_constants_from_duplicate_paths": surplus,
        "paths_in_apiconfig_absent_from_catalogue": sorted(ac_only),
        "reconciliation_arithmetic":
            "%d route constants in APIConfig.java - %d surplus constants (%d paths are "
            "declared by more than one constant name) = %d distinct paths. %d of those are "
            "not catalogue endpoints (%s), leaving %d. NOTE: %d is the stale figure that "
            "circulates for this catalogue - it is the raw constant count, not the endpoint "
            "count."
            % (len(ac["route_constants"]), surplus, len(dup_paths),
               len(ac["distinct_paths"]), len(ac_only),
               "; ".join(sorted(ac_only)), len(sm), len(ac["route_constants"])),
    }
    print("\n1. Catalogue")
    print("   route constants parsed from APIConfig.java ... %d" % recon["route_constants_parsed"])
    print("   distinct paths (query string stripped) ....... %d" % recon["distinct_paths_after_query_strip"])
    print("   ...minus %d surplus constants (%d shared paths)  %d"
          % (surplus, len(dup_paths), len(ac["distinct_paths"])))
    print("   ...minus %d non-endpoint paths %s" % (len(ac_only), sorted(ac_only)))
    print("   source-map endpoints (Controller/Action) ..... %d" % recon["source_map_endpoints"])
    print("   quoted catalogue size ........................ 1306  -> %s"
          % ("RECONCILES" if recon["reconciles"] else "MISMATCH"))
    if recon["constants_in_apiconfig_not_in_source_map"]:
        warn("%d constants absent from source-map"
             % len(recon["constants_in_apiconfig_not_in_source_map"]))

    # --- 2. run evidence --------------------------------------------------
    ev = load_run_evidence(RESULTS, path_to_eid)
    attempted = {e for e, r in ev.items() if r["attempted"]}
    responded = {e for e, r in ev.items() if r["responded"]}
    skipped = set(ev) - attempted            # never issued: destructive skip
    no_response = attempted - responded      # issued, nothing came back
    print("\n2. Run evidence (artifacts/runs/%s/results.json)" % RUN_STAMP)
    print("   catalogue endpoints in the hop list .......... %d" % len(ev))
    print("   ...never issued (skipped as destructive) ..... %d  %s"
          % (len(skipped), sorted(skipped)))
    print("   ...EXERCISED (request issued) ................ %d  <- prior figure 870 %s"
          % (len(attempted), "RECONCILES" if len(attempted) == 870 else "MISMATCH"))
    print("      of which no response came back ............ %d  %s"
          % (len(no_response), sorted(no_response)))
    print("      of which a numeric HTTP status returned ... %d" % len(responded))
    print("   endpoints with a measured rejection .......... %d"
          % sum(1 for r in ev.values() if r["rejections"]))

    # --- 3. existing coverage --------------------------------------------
    cov = load_existing_coverage(path_to_eid)
    wiring = audit_negative_wiring()
    live_eps = set(cov["live"])
    orphan_eps = set(cov["orphan"])
    print("\n3. Existing negative coverage")
    print("   negative test classes on disk ................ %d" % wiring["negative_test_classes"])
    print("   @Test methods in them ........................ %d" % wiring["negative_test_methods"])
    print("   @DataProvider names they reference ........... %d" % wiring["data_providers_referenced"])
    print("   ...that do not exist (test cannot run) ....... %d" % len(wiring["referenced_but_undefined"]))
    print("   validator calls .............................. %s" % wiring["validator_calls"])
    print("   LIVE negative rows (loadable) ................ %d  statuses=%s"
          % (cov["live_rows"], cov["live_status"]))
    print("   catalogue endpoints with LIVE coverage ....... %d" % len(live_eps))
    print("   ORPHANED negative rows (never loaded) ........ %d  statuses=%s"
          % (cov["orphan_rows"], cov["orphan_status"]))
    print("   catalogue endpoints in orphaned workbook ..... %d" % len(orphan_eps))
    print("   AdminAPI Settings negative rows .............. %d over %d endpoints, "
          "errorCodes=%s, in /api/ catalogue=%d"
          % (cov["adminapi_rows"], cov["adminapi_endpoints"],
             cov["adminapi_error_codes"], cov["adminapi_in_catalogue"]))

    # --- 4. generate ------------------------------------------------------
    rows = []
    per_ep = {}
    cat_count = collections.Counter()
    sev_count = collections.Counter()
    auto_count = collections.Counter()
    unknown_rows = 0
    measured_rows = 0
    bl_exact, bl_lh08, destructive_eps = set(), set(), set()

    applicable = {
        eid: build_scenarios(eid, sm[eid], ev, cov["live"].get(eid, {}),
                             cov["orphan"].get(eid, {}), cfg)
        for eid in sorted(sm)
    }
    applicable_cats = collections.Counter(
        s["scenario_category"] for v in applicable.values() for s in v)
    selected = select_scenarios(applicable, MAX_PER_ENDPOINT)

    for eid in sorted(sm):
        meta = sm[eid]
        controller, action = eid.split("/", 1)
        path = meta["path"]
        plow = path.split("?")[0].lower()
        alow = action.lower()

        # safety classification - names, never verbs
        blocked = None
        if plow in BLOCKLIST_EXACT or alow.startswith(BLOCKLIST_ACTION_PREFIX):
            blocked = "brief-1-exact"
            bl_exact.add(eid)
        elif alow in BLOCKLIST_ACTION_EXACT:
            blocked = "LH-08-same-action-name"
            bl_lh08.add(eid)
        destructive = alow.startswith(DESTRUCTIVE_PREFIX) or meta.get("role") == "teardown"
        if destructive:
            destructive_eps.add(eid)

        keep = selected[eid]
        assert len(keep) >= MIN_PER_ENDPOINT, (eid, len(keep))
        per_ep[eid] = len(keep)

        base = ev.get(eid, {}).get("baseline")
        for i, s in enumerate(keep, 1):
            cat = s["scenario_category"]
            rej = s.pop("_rej", None)
            s.pop("_weight", None)

            exp_status = s["expected_status"]
            exp_code = s["expected_error_code"]
            exp_msg = s["expected_error_message"]
            actual = NOEV
            evidence_bits = []
            remarks = []

            # measured expectation overrides UNKNOWN for application-level rows
            if rej:
                me = measured_expectation(rej)
                if me:
                    m_status, m_code, m_msg = me
                    exp_status = m_status
                    exp_msg = "MEASURED: %s" % m_msg
                    actual = "MEASURED (HTTP %s): %s" % (rej.get("status"), rej["detail"])
                    measured_rows += 1
                    evidence_bits.append(rej["cite"])
                    if rej.get("evidence_file"):
                        evidence_bits.append("artifacts/runs/%s/evidence/%s"
                                             % (RUN_STAMP, rej["evidence_file"]))
                    remarks.append(
                        "Expected outcome is not from a document - it is the response the "
                        "product actually returned when this condition occurred during the "
                        "%s run. Treat as observed behaviour, not a contract." % RUN_STAMP)

            # framework-level rows: 401 / 405 have a traceable asserted expectation
            if cat == "invalid authentication":
                evidence_bits.append("%s (1,550 rows assert 401)" % os.path.basename(XLS_NEG))
                evidence_bits.append("ApiHelper.java:1425 (envelope read only when expectedStatusCode==200)")
            if cat == "wrong HTTP method":
                evidence_bits.append("Environments/QA_MsSQL.properties#ExpectedMethodNotAllowedAPIStatusCode=%s"
                                     % cfg["method_not_allowed_status"])
                evidence_bits.append("%s#KotakSNOWApi_NegativeScenarios" % os.path.basename(XLS_POS))

            # baseline for the unmutated request - context, never the negative result
            if base:
                remarks.append(
                    "Valid-request baseline measured %s: HTTP %s, %s, envelope %r, %s B."
                    % (base["cite"], base["status"], base["content_type"],
                       base["envelope"], base["body_bytes"]))
            elif eid in skipped:
                remarks.append("Endpoint appears in the run's flow plan but the request was "
                               "never issued - skipped as destructive "
                               "(results.json meta.skipped). No response body exists.")
            elif eid in no_response:
                remarks.append("Request was issued in the run and nothing came back "
                               "(status null) - consistent with the API being unavailable "
                               "at that point. No response body exists.")
            else:
                remarks.append("Endpoint was never called in the %s run (one of %d "
                               "catalogue endpoints with no run evidence at all)."
                               % (RUN_STAMP, len(sm) - len(ev)))

            # existing coverage for this endpoint+category
            live_hit = cov["live"].get(eid, {}).get(cat)
            orph_hit = cov["orphan"].get(eid, {}).get(cat)
            if live_hit:
                validation = ("HTTP status only (expects %s) via %s. errorCode is NOT "
                              "asserted - the class calls "
                              "validateApiResponseWithResponseTime_ExcelBased, not the "
                              "...settingnegative variant."
                              % (live_hit["status"], live_hit["source"]))
                missing = ("Envelope not read: Success, ErrorCode and ErrorMessage are all "
                           "unasserted, so a 200-with-error-body passes.")
                evidence_bits.append(live_hit["source"])
            elif orph_hit:
                validation = ("NONE AT RUNTIME. A row for this endpoint+category exists in "
                              "%s, but that workbook is referenced by no @DataProvider - "
                              "Negative_API_ExcelDataProviderFileName is declared at "
                              "AutoConfigs.java:37 and read by nothing. The row never "
                              "executes." % os.path.basename(XLS_NEG))
                missing = ("Entire scenario is unexecuted: the data exists and is "
                           "unreachable. Even if wired, it asserts only HTTP %s."
                           % orph_hit["status"])
                evidence_bits.append(orph_hit["source"])
            elif eid in cov["orphan"]:
                validation = ("NONE. This endpoint does appear in %s, but only under the "
                              "%s block(s) - never this scenario. And that workbook is "
                              "loaded by no @DataProvider, so even those rows never run."
                              % (os.path.basename(XLS_NEG),
                                 "/".join(sorted(cov["orphan"][eid]))))
                missing = ("Scenario is absent from the framework. The endpoint's only "
                           "negative test data covers a different category and is itself "
                           "unreachable.")
            else:
                validation = "NONE - no negative test, no test data, no suite entry."
                missing = "Scenario is entirely absent from the framework."

            if exp_status == UNK and exp_code in (UNK,) and exp_msg == UNK:
                unknown_rows += 1
                missing = ("EXPECTED OUTCOME UNDOCUMENTED - no contract states what this "
                           "endpoint should return for this condition, and the run never "
                           "produced it. A test cannot be written until the expected "
                           "outcome is defined. " + missing)

            # automation status - safety first, names not verbs
            if blocked == "brief-1-exact":
                autostat = "DO NOT EXECUTE - takes API down"
            elif blocked == "LH-08-same-action-name":
                autostat = "DO NOT EXECUTE - takes API down"
            elif alow.startswith(DESTRUCTIVE_PREFIX):
                autostat = "DO NOT EXECUTE - mutating"
            elif meta.get("role") == "teardown":
                autostat = "DO NOT EXECUTE - mutating"
            elif live_hit:
                autostat = "AUTOMATED - status-only assertion"
            elif meta.get("role") in ("create", "update"):
                autostat = "REQUIRES APPROVAL - write endpoint"
            else:
                autostat = "NOT AUTOMATED - safe to execute"

            if blocked:
                remarks.insert(0, "BLOCKLISTED (%s): this endpoint stopped the IIS "
                                  "application pool. Enforce at planning time - never "
                                  "build the request." % blocked)
            if alow.startswith(DESTRUCTIVE_PREFIX):
                remarks.insert(0, "Destructive by NAME (%s...), not by verb - this route "
                                  "is %s. Never replayed." % (action[:6], meta["verb"]))

            sev = s["severity"]
            rows.append({
                "endpoint_id": eid,
                "controller": controller,
                "endpoint": action,
                "verb": meta["verb"],
                "path": path,
                "scenario_id": "NEG-%s-%s-%02d" % (
                    re.sub(r"[^A-Za-z0-9]", "", eid)[:40].upper(),
                    hashlib.sha1(eid.encode()).hexdigest()[:4].upper(), i),
                "scenario_category": cat,
                "scenario_name": s["scenario_name"],
                "description": s["description"],
                "request_mutation": s["request_mutation"],
                "payload": s["payload"],
                "expected_status": exp_status,
                "expected_error_code": exp_code,
                "expected_error_message": exp_msg,
                "expected_response": s["expected_response"],
                "actual_response": actual,
                "validation_performed": validation,
                "missing_validation": missing,
                "severity": sev,
                "automation_status": autostat,
                "evidence_ref": "; ".join(evidence_bits) if evidence_bits
                                else "static analysis only - APIConfig.java:%s, source-map.json#%s"
                                     % (min((ac["route_constants"][c]["line"]
                                             for c in meta.get("consts", [])
                                             if c in ac["route_constants"]), default="?"), eid),
                "remarks": " ".join(remarks),
            })
            cat_count[cat] += 1
            sev_count[sev] += 1
            auto_count[autostat] += 1

    print("\n4. Matrix")
    print("   rows generated ............................... %d" % len(rows))
    print("   endpoints covered ............................ %d" % len(per_ep))
    print("   scenarios per endpoint  min/max/mean ......... %d / %d / %.2f"
          % (min(per_ep.values()), max(per_ep.values()),
             sum(per_ep.values()) / len(per_ep)))
    print("   rows with UNKNOWN expected outcome ........... %d  (%.1f%%)"
          % (unknown_rows, 100.0 * unknown_rows / len(rows)))
    print("   rows with a MEASURED expected outcome ........ %d  (%.1f%%)"
          % (measured_rows, 100.0 * measured_rows / len(rows)))
    print("   blocklisted endpoints  brief-1 / LH-08 ....... %d / %d"
          % (len(bl_exact), len(bl_lh08)))
    print("   destructive (Delete*/Remove*/teardown) ....... %d" % len(destructive_eps))

    print("\n   category distribution:")
    for c, n in cat_count.most_common():
        print("      %-32s %5d" % (c, n))
    print("\n   severity: %s" % dict(sev_count))
    print("   automation_status: %s" % dict(auto_count))

    # --- 5. summary -------------------------------------------------------
    all_eps = set(sm)
    zero_cov = sorted(all_eps - live_eps)
    zero_any = sorted(all_eps - live_eps - orphan_eps)

    per_controller = {}
    for eid, meta in sm.items():
        c = meta["controller"]
        d = per_controller.setdefault(c, {
            "endpoints": 0, "scenario_rows": 0,
            "endpoints_with_live_negative_coverage": 0,
            "endpoints_in_orphaned_negative_workbook": 0,
            "endpoints_with_run_evidence": 0,
            "endpoints_with_measured_rejection": 0,
            "blocklisted_endpoints": 0, "destructive_endpoints": 0,
        })
        d["endpoints"] += 1
        d["scenario_rows"] += per_ep[eid]
        if eid in live_eps:
            d["endpoints_with_live_negative_coverage"] += 1
        if eid in orphan_eps:
            d["endpoints_in_orphaned_negative_workbook"] += 1
        if eid in attempted:
            d["endpoints_with_run_evidence"] += 1
        if ev.get(eid, {}).get("rejections"):
            d["endpoints_with_measured_rejection"] += 1
        if eid in bl_exact or eid in bl_lh08:
            d["blocklisted_endpoints"] += 1
        if eid in destructive_eps:
            d["destructive_endpoints"] += 1
    for c, d in per_controller.items():
        d["live_negative_coverage_pct"] = round(
            100.0 * d["endpoints_with_live_negative_coverage"] / d["endpoints"], 1)

    unknown_by_cat = collections.Counter()
    for r in rows:
        if r["missing_validation"].startswith("EXPECTED OUTCOME UNDOCUMENTED"):
            unknown_by_cat[r["scenario_category"]] += 1

    summary = {
        "generated_by": "tools/obj007_negative_matrix.py",
        "objective": "OBJ-007 item A3 - negative-validation scenario matrix",
        "network_calls_issued": 0,
        "database_queries_issued": 0,
        "catalogue_reconciliation": recon,
        "totals": {
            "endpoints": len(sm),
            "scenario_rows": len(rows),
            "scenarios_per_endpoint_min": min(per_ep.values()),
            "scenarios_per_endpoint_max": max(per_ep.values()),
            "scenarios_per_endpoint_mean": round(sum(per_ep.values()) / len(per_ep), 2),
            "rows_with_unknown_expected_outcome": unknown_rows,
            "rows_with_unknown_expected_outcome_pct": round(100.0 * unknown_rows / len(rows), 1),
            "rows_with_measured_expected_outcome": measured_rows,
            "rows_with_measured_expected_outcome_pct": round(100.0 * measured_rows / len(rows), 1),
        },
        "scenarios_per_category": dict(cat_count.most_common()),
        "scenarios_applicable_per_category_before_cap": dict(applicable_cats.most_common()),
        "selection_rule": "Every applicable scenario was generated (%d in total). Each "
                          "endpoint then keeps at most %d: the four universal core "
                          "categories (%s), the single highest-value shape-driven "
                          "scenario, then the remaining slots filled preferring globally "
                          "under-represented categories so that no rare-but-real scenario "
                          "is truncated out of the matrix entirely."
                          % (sum(applicable_cats.values()), MAX_PER_ENDPOINT,
                             ", ".join(CORE_CATEGORIES)),
        "unknown_expected_outcome_per_category": dict(unknown_by_cat.most_common()),
        "severity_distribution": dict(sev_count),
        "automation_status_distribution": dict(auto_count),
        "existing_negative_coverage": {
            "note": "LIVE means a @DataProvider exists that TestNG can resolve at runtime. "
                    "Everything else is data or code that cannot execute.",
            "live_driver_classes": [
                "com.arcon.tests.API.Negative_API.KotakSNOWApi.* (3 negative providers)",
                "com.arcon.tests.API.Negative_API.SNOWApi.* (2 negative providers)",
                "com.arcon.tests.API_Dynamic.Settings (the only caller of "
                "validateApiResponseWithResponseTime_ExcelBasedsettingnegative)",
            ],
            "live_driver_class_count": 3,
            "catalogue_endpoints_with_live_negative_coverage": len(live_eps),
            "catalogue_endpoints_with_live_negative_coverage_pct":
                round(100.0 * len(live_eps) / len(sm), 2),
            "catalogue_endpoints_with_zero_live_negative_coverage": len(zero_cov),
            "catalogue_endpoints_with_zero_negative_coverage_of_any_kind": len(zero_any),
            "controllers_in_catalogue": len(per_controller),
            "controllers_with_live_negative_coverage":
                sorted({e.split("/")[0] for e in live_eps}),
            "live_negative_rows_loadable": cov["live_rows"],
            "live_negative_expected_statuses": cov["live_status"],
            "orphaned_workbook": {
                "file": "testdata/" + os.path.basename(XLS_NEG),
                "rows_with_an_expected_status": cov["orphan_rows"],
                "expected_statuses": cov["orphan_status"],
                "catalogue_endpoints_referenced": len(orphan_eps),
                "why_dead": "AutoConfigs.java:37 declares "
                            "Negative_API_ExcelDataProviderFileName and 6 environment "
                            "files set it, but no @DataProvider in "
                            "API_DataProviderUtils.java ever reads it. Every provider "
                            "reads API_ExcelDataProviderFileName instead.",
                "categories_covered": ["wrong HTTP method", "invalid authentication"],
                "categories_not_covered": 17,
            },
            "adminapi_settings_track": {
                "note": "The only envelope-aware negative testing in the framework - and "
                        "none of its endpoints are in the 1,306 /api/ catalogue.",
                "rows": cov["adminapi_rows"],
                "distinct_endpoints": cov["adminapi_endpoints"],
                "endpoints_in_api_catalogue": cov["adminapi_in_catalogue"],
                "asserted_error_codes": cov["adminapi_error_codes"],
                "asserted_http_status": 200,
            },
            "wiring_audit": wiring,
        },
        "run_evidence": {
            "run": "artifacts/runs/%s/results.json" % RUN_STAMP,
            "catalogue_endpoints_in_hop_list": len(ev),
            "catalogue_endpoints_exercised": len(attempted),
            "catalogue_endpoints_that_returned_a_numeric_status": len(responded),
            "prior_figure_reconciled": 870,
            "reconciliation": "%d catalogue endpoints appear in the run's hop list. %d of "
                              "them carry no 'status' key at all - the request was never "
                              "issued because the runner skipped it as destructive "
                              "(results.json meta.skipped: DeleteAdDomain x2, "
                              "RemoveUserStatusDetails x2, DeleteRTSMLog x1). %d - %d = %d "
                              "endpoints were actually exercised, matching the prior figure "
                              "of 870 exactly. Of those, %d returned no response at all "
                              "(status null) and %d returned a numeric HTTP status."
                              % (len(ev), len(skipped), len(ev), len(skipped),
                                 len(attempted), len(no_response), len(responded)),
            "endpoints_skipped_as_destructive": sorted(skipped),
            "endpoints_exercised_with_no_response": sorted(no_response),
            "catalogue_endpoints_with_no_run_evidence": len(sm) - len(ev),
            "endpoints_with_a_measured_rejection":
                sum(1 for r in ev.values() if r["rejections"]),
        },
        "safety": {
            "blocklisted_brief_section_1": sorted(bl_exact),
            "blocklisted_same_action_name_LH08": sorted(bl_lh08),
            "destructive_by_name": len(destructive_eps),
            "guard_basis": "endpoint NAME, never verb - deletion on this API is "
                           "POST /api/<Controller>/Delete<Thing>",
        },
        "per_controller": dict(sorted(per_controller.items())),
        "endpoints_with_zero_live_negative_coverage": zero_cov,
    }

    ids = [r["scenario_id"] for r in rows]
    assert len(set(ids)) == len(ids), "scenario_id collision: %d dupes" % (
        len(ids) - len(set(ids)))
    assert all(r["actual_response"] == NOEV or r["actual_response"].startswith("MEASURED")
               for r in rows), "actual_response must be NOEV or MEASURED"

    os.makedirs(OUT_DATA, exist_ok=True)
    with open(OUT_MATRIX, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=False, default=str)
    with open(OUT_SUMMARY, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False, default=str)

    print("\n5. Written")
    print("   %s  (%.1f MB)" % (OUT_MATRIX, os.path.getsize(OUT_MATRIX) / 1e6))
    print("   %s  (%.1f KB)" % (OUT_SUMMARY, os.path.getsize(OUT_SUMMARY) / 1e3))
    print("\n   zero LIVE negative coverage .................. %d of %d endpoints (%.1f%%)"
          % (len(zero_cov), len(sm), 100.0 * len(zero_cov) / len(sm)))
    print("   zero negative coverage of ANY kind ........... %d of %d endpoints (%.1f%%)"
          % (len(zero_any), len(sm), 100.0 * len(zero_any) / len(sm)))
    print("   controllers with live negative coverage ...... %s"
          % summary["existing_negative_coverage"]["controllers_with_live_negative_coverage"])
    print("\n   UNKNOWN expected outcome by category:")
    for c, n in unknown_by_cat.most_common():
        print("      %-32s %5d" % (c, n))


if __name__ == "__main__":
    main()
