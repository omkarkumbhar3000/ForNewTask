#!/usr/bin/env python
"""OBJ-007 item A2 - document every API covered under positive testing.

ZERO HTTP requests. ZERO database queries. Pure static + evidence analysis.

Inputs (all read-only)
  tools/source-map.json                       canonical 1,306-endpoint catalogue
  .../src/test/java/com/arcon/autoconfigs/APIConfig.java  cross-check of the catalogue
  artifacts/runs/2026-07-29_181439/results.json             326 flows / 1,873 hops / L1-L7 verdicts
  artifacts/runs/2026-07-29_181439/evidence/*.json          1,868 per-call request+response captures
  .../API_Suites/Positive_All/*.xml                       71 framework positive suites
  .../src/test/java/com/arcon/tests/API/All_API_Positive/ 79 framework positive test classes
  .../src/test/java/com/arcon/dataprovider/API_DataProviderUtils.java
  .../testdata/API_Automation_Test_Input_Data.xls         framework positive test data

Outputs
  artifacts/analysis-data/positive-validation.json   one row per positive endpoint-invocation, all 1,306 covered
  artifacts/analysis-data/envelope-shapes.json       empirical response-shape census over all 1,868 calls
  stdout                                   the tallies quoted in docs/analysis/A2-positive-validation.md

Usage
  python tools\\obj007_positive_analysis.py
"""

from __future__ import annotations

import collections
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------

from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
RUN = ROOT / "artifacts" / "runs" / "2026-07-29_181439"
EVIDENCE = RUN / "evidence"
SRC = REPO / "src" / "test" / "java" / "com" / "arcon"

SOURCE_MAP = ROOT / "tools" / "source-map.json"
APICONFIG = SRC / "autoconfigs" / "APIConfig.java"
APIHELPER = SRC / "utils" / "ApiHelper.java"
DATAPROVIDER = SRC / "dataprovider" / "API_DataProviderUtils.java"
POSITIVE_CLASSES = SRC / "tests" / "API" / "All_API_Positive"
POSITIVE_SUITES = REPO / "API_Suites" / "Positive_All"
TESTDATA = REPO / "testdata" / "API_Automation_Test_Input_Data.xls"

OUT_DATA = ROOT / "artifacts" / "analysis-data"

NOT_EXEC = "NOT EXECUTED - no evidence"
UNKNOWN = "UNKNOWN"
BODY_TRUNC = 400

# Authoritative tallies from docs/history/archive/document-agent-brief.md. The script compares its own
# extraction against these and shouts on any disagreement rather than overwriting them.
BRIEF = {
    "endpoints": 1306,
    "flows": 326,
    "hops": 1873,
    "calls": 1868,
    "endpoints_exercised": 870,
    "checks": {
        "L1": (1688, 180),
        "L2": (1864, 4),
        "L3": (1278, 590),
        "L4": (1410, 458),
        "L5": (982, 196),
        "L6": (2, 105),
        "L7": (1855, 13),
    },
}

DISAGREEMENTS: list[str] = []


def check(label: str, measured, expected) -> None:
    if measured != expected:
        DISAGREEMENTS.append(f"{label}: measured {measured!r}, brief says {expected!r}")


# ---------------------------------------------------------------------------
# canonicalisation
# ---------------------------------------------------------------------------


def canon(path: str) -> str:
    """`/api/<Controller>/<Action>` -> `Controller/Action`. Matches source-map keys."""
    p = (path or "").split("?")[0]
    while "//" in p:
        p = p.replace("//", "/")
    segs = [s for s in p.split("/") if s]
    if segs and segs[0].lower() == "api":
        if len(segs) >= 3:
            return f"{segs[1]}/{segs[2]}"
        if len(segs) == 2:
            return f"{segs[1]}/"
    return "/".join(segs)


# ---------------------------------------------------------------------------
# 1. catalogue
# ---------------------------------------------------------------------------


def load_catalogue() -> dict:
    cat = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
    check("catalogue size (source-map.json keys)", len(cat), BRIEF["endpoints"])
    return cat


def parse_apiconfig() -> dict:
    """Independent parse of APIConfig.java, for cross-checking the catalogue."""
    pat = re.compile(
        r'^\s*public\s+static\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;\s*(?://\s*(.*))?$'
    )
    verbs = ("get", "post", "put", "patch", "delete")
    decls, by_ep = [], {}
    for lineno, line in enumerate(
        APICONFIG.read_text(encoding="utf-8", errors="replace").splitlines(), 1
    ):
        if line.strip().startswith("//"):
            continue
        m = pat.match(line)
        if not m:
            continue
        name, value, comment = m.group(1), m.group(2), (m.group(3) or "").strip()
        if not value.startswith("/"):
            continue
        verb = next(
            (v.upper() for v in verbs if re.search(rf"\b{v}\b", comment.lower())), None
        )
        ep = canon(value)
        decls.append({"line": lineno, "const": name, "path": value, "verb": verb})
        by_ep.setdefault(ep, []).append(lineno)
    return {"decls": decls, "by_endpoint": by_ep}


# ---------------------------------------------------------------------------
# 2. framework positive coverage: suite XML -> class -> dataProvider -> xls table
# ---------------------------------------------------------------------------


def load_framework() -> dict:
    # suite XMLs -> class simple names
    suite_files = sorted(POSITIVE_SUITES.glob("*.xml"))
    suite_of_class: dict[str, list[str]] = collections.defaultdict(list)
    for f in suite_files:
        txt = re.sub(r"<!--.*?-->", "", f.read_text(encoding="utf-8", errors="replace"), flags=re.S)
        for m in re.finditer(r'class\s+name\s*=\s*"([^"]+)"', txt):
            suite_of_class[m.group(1).rsplit(".", 1)[-1]].append(f.name)
    suite_classes = set(suite_of_class)

    # class -> active @Test dataProvider names (comment-stripped)
    disk_classes = sorted(p.stem for p in POSITIVE_CLASSES.glob("*.java"))
    providers_of_class: dict[str, list[str]] = {}
    for cls in disk_classes:
        raw = (POSITIVE_CLASSES / f"{cls}.java").read_text(encoding="utf-8", errors="replace")
        body = "\n".join(l for l in raw.splitlines() if not l.strip().startswith("//"))
        body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
        names = []
        for m in re.finditer(r"@Test\(([^)]*)\)", body, flags=re.S):
            args = m.group(1)
            if re.search(r"enabled\s*=\s*false", args):
                continue
            dp = re.search(r'dataProvider\s*=\s*"([^"]+)"', args)
            if dp:
                names.append(dp.group(1))
        providers_of_class[cls] = names

    # dataProvider name -> (sheet, table)
    dp_src = DATAPROVIDER.read_text(encoding="utf-8", errors="replace")
    dp_live = "\n".join(l for l in dp_src.splitlines() if not l.strip().startswith("//"))
    provider_target: dict[str, tuple[str, str]] = {}
    for name, block in re.findall(
        r'@DataProvider\(name\s*=\s*"([^"]+)"\)\s*public\s+static\s+Object\[\]\[\]\s+\w+\(\)\s*\{(.*?)\n\t\}',
        dp_live,
        flags=re.S,
    ):
        strs = [s for s in re.findall(r'"([^"]*)"', block) if s != "testdata"]
        if len(strs) >= 2:
            provider_target[name] = (strs[-2], strs[-1])

    # xls tables -> rows
    import xlrd  # noqa: PLC0415  (optional dep, only needed here)

    wb = xlrd.open_workbook(str(TESTDATA))
    tables: dict[tuple[str, str], list[dict]] = {}
    marker_cells: dict[tuple[str, str], tuple[int, int]] = {}
    for sheet_name in wb.sheet_names():
        sh = wb.sheet_by_name(sheet_name)
        # locate every table marker anywhere on the sheet (jxl findCell scans all cells)
        for r in range(sh.nrows):
            for c in range(sh.ncols):
                v = str(sh.cell_value(r, c)).strip()
                if v:
                    marker_cells.setdefault((sheet_name, v), (r, c))
        current = None
        for r in range(sh.nrows):
            c0 = str(sh.cell_value(r, 0)).strip()
            if c0:
                current = c0
                tables.setdefault((sheet_name, current), [])
                continue
            if current is None:
                continue
            c1 = str(sh.cell_value(r, 1)).strip()
            if not c1 or c1 == "InputType":
                continue
            cells = [str(sh.cell_value(r, c)).strip() for c in range(sh.ncols)]
            tables[(sheet_name, current)].append(
                {
                    "row": r + 1,
                    "input_type": cells[1],
                    "module": cells[2],
                    "verb": cells[3],
                    "endpoint": cells[4],
                    "payload": cells[5],
                    "expected_status": cells[6],
                }
            )

    # resolve: endpoint -> framework provenance
    fw: dict[str, list[dict]] = collections.defaultdict(list)
    broken_providers, wired = [], []
    for cls in disk_classes:
        in_suite = cls in suite_classes
        for prov in providers_of_class[cls]:
            target = provider_target.get(prov)
            if target is None:
                broken_providers.append((cls, prov, "no active @DataProvider of that name"))
                continue
            if target not in tables:
                broken_providers.append((cls, prov, f"table {target[1]!r} absent from sheet {target[0]!r}"))
                continue
            wired.append((cls, prov, target, in_suite, len(tables[target])))
            for row in tables[target]:
                if not row["endpoint"].startswith("/"):
                    continue
                fw[canon(row["endpoint"])].append(
                    {
                        "class": cls,
                        "provider": prov,
                        "sheet": target[0],
                        "table": target[1],
                        "xls_row": row["row"],
                        "verb": (row["verb"] or "").upper(),
                        "payload": row["payload"],
                        "expected_status": row["expected_status"],
                        "in_suite": in_suite,
                        "suites": suite_of_class.get(cls, []),
                    }
                )

    return {
        "suite_files": [f.name for f in suite_files],
        "suite_classes": sorted(suite_classes),
        "disk_classes": disk_classes,
        "classes_not_in_any_suite": sorted(set(disk_classes) - suite_classes),
        "provider_targets": provider_target,
        "broken_providers": broken_providers,
        "wired": wired,
        "endpoints": dict(fw),
        "table_row_counts": {f"{k[0]}::{k[1]}": len(v) for k, v in tables.items()},
    }


# ---------------------------------------------------------------------------
# 3. response-shape classification
# ---------------------------------------------------------------------------

ENVELOPE_MARKERS = ("Success", "success", "IsSuccess", "isSuccess",
                    "ErrorCode", "errorCode", "Result", "result", "Data", "data",
                    "Message", "message", "ErrorMessage", "errorMessage")


def _looks_like_envelope(node) -> bool:
    return isinstance(node, dict) and any(k in node for k in ENVELOPE_MARKERS)


def pam_envelope_shape(body):
    """Python mirror of com.arcon.utils.validation.PamEnvelope.Shape classification.

    Kept deliberately in lock-step with PamEnvelope.of(String) so the census
    measures exactly what the Java class will see at runtime.
    """
    if body is None:
        return "EMPTY", None
    if isinstance(body, str):
        if not body.strip():
            return "EMPTY", None
        return "NOT_JSON", None  # evidence stores the decoded body; a str here is a non-JSON body
    env = body
    if isinstance(body, list) and len(body) == 1 and _looks_like_envelope(body[0]):
        env = body[0]
    if isinstance(env, list):
        return "BARE_ARRAY", env
    if not _looks_like_envelope(env):
        return "BARE_OBJECT", env
    success = None
    for k in ("Success", "success", "IsSuccess", "isSuccess"):
        if k in env and isinstance(env[k], bool):
            success = env[k]
            break
    has_error_code = any(k in env for k in ("ErrorCode", "errorCode"))
    if success is False or has_error_code:
        return "ENVELOPE_ERROR", env
    result_key = next((k for k in ("Result", "result", "Data", "data") if k in env), None)
    if result_key is None:
        return "ENVELOPE_NO_RESULT", env
    return ("ENVELOPE_RESULT_ARRAY" if isinstance(env[result_key], list)
            else "ENVELOPE_RESULT_OBJECT"), env


def structural_signature(body) -> str:
    """Fine-grained signature: exact top-level structure. Two calls share a
    signature only if a single generic parser could treat them identically."""
    if body is None:
        return "null-body"
    if isinstance(body, bool):
        return "bare-boolean"
    if isinstance(body, str):
        return "empty-string" if not body.strip() else "bare-string(text/plain payload)"
    if isinstance(body, (int, float)):
        return "bare-number"
    if isinstance(body, list):
        if not body:
            return "bare-array(empty)"
        inner = body[0]
        if isinstance(inner, dict):
            return "bare-array(of objects)"
        return f"bare-array(of {type(inner).__name__})"
    if isinstance(body, dict):
        keys = ",".join(sorted(body.keys()))
        res = body.get("Result", body.get("result", "\0"))
        if res == "\0":
            rt = "no-Result"
        elif isinstance(res, list):
            rt = "Result:array"
        elif isinstance(res, dict):
            rt = "Result:object"
        elif res is None:
            rt = "Result:null"
        else:
            rt = f"Result:{type(res).__name__}"
        return f"object{{{keys}}} + {rt}"
    return f"other({type(body).__name__})"


DOCUMENTED_SHAPES = {
    # brief S2: the five shapes documented before this session
    "object{DateTime,Message,Program,Result,Success,Version} + Result:array":
        "S1 documented - {Program,Version,DateTime,Success,Message,Result[]}",
    "object{DateTime,Program,Result,Success,Version} + Result:array":
        "S2 documented - same, no Message",
    "object{DateTime,Program,Result,Success,Version} + Result:object":
        "S3 documented - same, Result is an object",
    "object{DateTime,Message,Program,Result,Success,Version} + Result:object":
        "S3 documented - same, Result is an object",
    "bare-array(of objects)":
        "S4 documented - bare array, no envelope",
    "object{DateTime,ErrorCode,ErrorMessage,Program,Success,Version} + no-Result":
        "S5 documented - Success:false + ErrorCode + ErrorMessage on HTTP 200",
}


# ---------------------------------------------------------------------------
# 4. envelope field reads
# ---------------------------------------------------------------------------


def read_envelope_fields(body):
    """Extract Success / Message / ErrorCode / ErrorMessage / Result stats, case-tolerant."""
    out = {
        "success": None, "message": None, "error_code": None,
        "error_message": None, "result_type": None, "result_count": None,
    }
    _, env = pam_envelope_shape(body)
    if isinstance(body, list) and env is body:
        out["result_type"] = "array(root)"
        out["result_count"] = len(body)
        return out
    if not isinstance(env, dict):
        return out
    def pick(*names):
        for n in names:
            if n in env and env[n] is not None:
                return env[n]
        return None
    s = pick("Success", "success", "IsSuccess", "isSuccess")
    out["success"] = s if isinstance(s, bool) else (None if s is None else str(s))
    for key, names in (
        ("message", ("Message", "message")),
        ("error_code", ("ErrorCode", "errorCode")),
        ("error_message", ("ErrorMessage", "errorMessage")),
    ):
        v = pick(*names)
        out[key] = None if v is None else str(v)
    rk = next((k for k in ("Result", "result", "Data", "data") if k in env), None)
    if rk is not None:
        r = env[rk]
        if isinstance(r, list):
            out["result_type"], out["result_count"] = "array", len(r)
        elif isinstance(r, dict):
            out["result_type"], out["result_count"] = "object", len(r)
        elif r is None:
            out["result_type"] = "null"
        else:
            out["result_type"] = type(r).__name__
    return out


# ---------------------------------------------------------------------------
# 5. false-success classification (the `Already Exists` class)
# ---------------------------------------------------------------------------

NOOP_MESSAGE = re.compile(
    r"already\s*exist|no\s*record\s*found|^0\s*-?\s*records?\s+found|not\s*found|"
    r"invalid|mandatory|is\s*required|error|fail|denied|unauthor",
    re.I,
)
INSERT_OK = re.compile(r"insert|updat|delet|save|success|creat|added", re.I)
WRITE_ROLES = {"create", "update", "teardown"}


def classify_false_success(role, status, fields, shape, body):
    """Return (category, explanation) when a green signal hides a non-write / non-result.

    A positive assertion built on `status == 200` (framework today) or on
    `status == 200 && Success == true` (the strongest thing the harness did at L3)
    would pass on every case returned here.
    """
    msg = (fields.get("message") or "").strip()
    succ = fields.get("success")

    if status == 200 and shape == "bare-boolean" and body is False:
        return ("D-bare-false", "HTTP 200 with a bare `false` body - the write failed and "
                                "there is no envelope, no Success flag and no message to read")

    if status != 200 or succ is not True:
        return (None, None)

    if re.search(r"already\s*exist", msg, re.I):
        return ("A-already-exists", f"Success:true with Message={msg!r} - the record was NOT written")

    if role in WRITE_ROLES and msg and not INSERT_OK.search(msg) and NOOP_MESSAGE.search(msg):
        return ("B-write-noop", f"write endpoint returned Success:true with Message={msg!r} - no write semantics")

    if re.search(r"invalid|mandatory|is\s*required|must\s*be", msg, re.I):
        return ("C-success-with-validation-error",
                f"Success:true while Message={msg!r} reports a rejected input")

    if re.search(r"no\s*record\s*found|^0\s*-?\s*records?\s+found", msg, re.I):
        return ("E-success-empty-result",
                f"Success:true with Message={msg!r} - the call returned no data")

    if role in WRITE_ROLES and not msg and fields.get("result_count") in (0, None):
        return ("F-write-silent",
                "write endpoint returned Success:true with no Message and no Result - "
                "nothing in the response evidences a write")

    return (None, None)


# ---------------------------------------------------------------------------
# 6. missing-validation model
# ---------------------------------------------------------------------------

MISSING_CATALOGUE = {
    "schema": "response JSON Schema / contract shape never asserted - no OpenAPI or Swagger covers this endpoint",
    "mandatory-fields": "no assertion that documented mandatory response fields are present and non-null",
    "field-types": "no assertion on field data types, formats, ranges or enumerations",
    "result-cardinality": "Result row count never reconciled against the Message record count or a known baseline",
    "business-rules": "no assertion on domain invariants (ownership, LOB scoping, state machine, referential integrity)",
    "persistence": "no database read-back - the write is never proven to have reached a table",
    "audit": "no assertion that the action produced an audit-log / activity-log entry",
    "idempotency": "endpoint never re-invoked to establish idempotent vs duplicate-creating behaviour",
    "authorization": "no assertion that the response respects the caller's role or LOB scope",
    "message-semantics": "response Message string never parsed for write-vs-no-op semantics",
    "envelope": "application-level Success / ErrorCode envelope never inspected - a rejected request passes",
    "error-code-domain": "ErrorCode values never validated against a complete known set (KNOWN_ERROR_CODES holds only 201/202/203)",
    "read-back": "created / updated record never re-read through the API to prove it exists",
    "latency": "no response-time budget asserted",
    "http-status": "HTTP status never asserted",
    "content-type": "Content-Type never asserted",
    "pagination": "list endpoint never exercised for paging, sorting or filtering correctness",
    "execution": "endpoint is never invoked by any positive test - nothing at all is validated",
}

LAYER_TO_MISSING = {
    "L1": "http-status",
    "L2": "content-type",
    "L3": "envelope",
    "L4": "message-semantics",
    "L6": "read-back",
    "L7": "latency",
}


def missing_for(role, verb, layers_run, executed, framework_only=False):
    """Everything an industry-standard positive assertion would check, minus what ran."""
    if not executed:
        return ["execution", "http-status", "content-type", "envelope", "message-semantics",
                "schema", "mandatory-fields", "field-types", "business-rules",
                "persistence", "audit", "authorization", "error-code-domain"] + \
               (["read-back", "idempotency"] if role in WRITE_ROLES else ["result-cardinality", "pagination"])

    want = ["http-status", "content-type", "envelope", "message-semantics",
            "schema", "mandatory-fields", "field-types", "business-rules",
            "authorization", "error-code-domain", "latency"]
    if role in WRITE_ROLES:
        want += ["persistence", "audit", "read-back", "idempotency"]
    else:
        want += ["result-cardinality", "pagination"]

    if framework_only:
        satisfied = {"http-status", "latency"}
    else:
        satisfied = {LAYER_TO_MISSING[l] for l in layers_run if l in LAYER_TO_MISSING}
    return [w for w in want if w not in satisfied]


def missing_str(codes):
    return "; ".join(f"{c}: {MISSING_CATALOGUE[c]}" for c in codes)


# ---------------------------------------------------------------------------
# 7. main
# ---------------------------------------------------------------------------


def truncate(obj, limit=BODY_TRUNC):
    if obj is None:
        return ""
    s = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s if len(s) <= limit else s[:limit] + f"...[+{len(s) - limit} chars]"


def main() -> int:
    print("=" * 78)
    print("OBJ-007 A2 - positive validation extraction (zero HTTP, zero DB)")
    print("=" * 78)

    cat = load_catalogue()
    apiconfig = parse_apiconfig()
    print(f"\n[catalogue] source-map.json endpoints          : {len(cat)}")
    print(f"[catalogue] APIConfig.java path declarations    : {len(apiconfig['decls'])}")
    print(f"[catalogue] APIConfig.java distinct Ctrl/Action : {len(apiconfig['by_endpoint'])}")
    only_cfg = sorted(set(apiconfig["by_endpoint"]) - set(cat))
    only_map = sorted(set(cat) - set(apiconfig["by_endpoint"]))
    print(f"[catalogue] in APIConfig only                   : {len(only_cfg)} {only_cfg[:5]}")
    print(f"[catalogue] in source-map only                  : {len(only_map)} {only_map[:5]}")

    fw = load_framework()
    print(f"\n[framework] positive suite XMLs                 : {len(fw['suite_files'])}")
    print(f"[framework] classes referenced by those suites  : {len(fw['suite_classes'])}")
    print(f"[framework] classes on disk in All_API_Positive : {len(fw['disk_classes'])}")
    print(f"[framework] classes in NO positive suite        : {len(fw['classes_not_in_any_suite'])} "
          f"{fw['classes_not_in_any_suite']}")
    print(f"[framework] data providers that cannot resolve  : {len(fw['broken_providers'])}")
    for cls, prov, why in fw["broken_providers"]:
        print(f"              - {cls}.{prov}: {why}")
    fw_eps = set(fw["endpoints"])
    fw_eps_in_cat = fw_eps & set(cat)
    fw_eps_suited = {e for e, rows in fw["endpoints"].items() if any(r["in_suite"] for r in rows)}
    print(f"[framework] distinct endpoints in positive xls  : {len(fw_eps)} "
          f"({len(fw_eps_in_cat)} of them in the 1,306 catalogue)")
    print(f"[framework] ... reachable from a positive suite : {len(fw_eps_suited & set(cat))}")

    # ---- run evidence -----------------------------------------------------
    run = json.loads((RUN / "results.json").read_text(encoding="utf-8"))
    flows = run["flows"]
    hops = [(f, h) for f in flows for h in f["hops"]]
    check("flow count", len(flows), BRIEF["flows"])
    check("hop count", len(hops), BRIEF["hops"])
    check("meta.calls", run["meta"]["calls"], BRIEF["calls"])

    ev_files = sorted(p.name for p in EVIDENCE.glob("*.json"))
    check("evidence file count", len(ev_files), BRIEF["calls"])

    ev_cache: dict[str, dict] = {}
    for name in ev_files:
        ev_cache[name] = json.loads((EVIDENCE / name).read_text(encoding="utf-8"))

    tallies = collections.defaultdict(lambda: collections.Counter())
    for _f, h in hops:
        for c in h.get("checks", []):
            tallies[c["layer"]][c["verdict"]] += 1
    for layer, (p, f_) in BRIEF["checks"].items():
        check(f"{layer} PASS", tallies[layer]["PASS"], p)
        check(f"{layer} FAIL", tallies[layer]["FAIL"], f_)

    executed_eps = {canon(h["path"]) for _f, h in hops if h.get("evidence")}
    named_eps = {canon(h["path"]) for _f, h in hops}
    check("endpoints exercised (hops with evidence)", len(executed_eps), BRIEF["endpoints_exercised"])
    print(f"\n[run] flows {len(flows)} - hops {len(hops)} - evidence files {len(ev_files)}")
    print(f"[run] endpoints named in flows      : {len(named_eps)}")
    print(f"[run] endpoints actually called     : {len(executed_eps)}  <- the 870 figure")
    print(f"[run] named but never called (skip) : {sorted(named_eps - executed_eps)}")
    print(f"[run] called endpoints not in the 1,306 catalogue: {len(executed_eps - set(cat))}")

    # ---- shape census over all 1,868 calls --------------------------------
    sig_counter = collections.Counter()
    sig_example: dict[str, dict] = {}
    enum_counter = collections.Counter()
    enum_by_sig = collections.defaultdict(collections.Counter)
    status_by_sig = collections.defaultdict(collections.Counter)
    for name, ev in ev_cache.items():
        body = ev.get("response")
        sig = structural_signature(body)
        shape, _ = pam_envelope_shape(body)
        sig_counter[sig] += 1
        enum_counter[shape] += 1
        enum_by_sig[sig][shape] += 1
        status_by_sig[sig][str(ev.get("status"))] += 1
        sig_example.setdefault(sig, {
            "evidence_file": name,
            "endpoint": canon((ev.get("url") or "").split("/api/", 1)[-1] and "/api/" + (ev.get("url") or "").split("/api/", 1)[-1]),
            "verb": ev.get("verb"),
            "http_status": ev.get("status"),
            "body_truncated": truncate(body, 300),
        })
    print(f"\n[shapes] distinct structural signatures across {len(ev_cache)} calls: {len(sig_counter)}")
    for sig, n in sig_counter.most_common():
        print(f"   {n:5d}  {sig}")
    print(f"[shapes] PamEnvelope.Shape classes actually seen: {len(enum_counter)} of 8")
    for s, n in enum_counter.most_common():
        print(f"   {n:5d}  {s}")
    documented = {s for s in sig_counter if s in DOCUMENTED_SHAPES}
    print(f"[shapes] signatures matching a previously documented shape: {len(documented)}")
    print(f"[shapes] signatures NOT previously documented              : {len(sig_counter) - len(documented)}")

    envelope_rows = []
    for sig, n in sig_counter.most_common():
        envelope_rows.append({
            "shape_signature": sig,
            "pam_envelope_shape": "; ".join(f"{k}={v}" for k, v in enum_by_sig[sig].most_common()),
            "calls": n,
            "pct_of_calls": round(100.0 * n / len(ev_cache), 2),
            "http_statuses": "; ".join(f"{k}={v}" for k, v in status_by_sig[sig].most_common()),
            "documented_before": DOCUMENTED_SHAPES.get(sig, "NOT DOCUMENTED"),
            "example_evidence_file": sig_example[sig]["evidence_file"],
            "example_verb": sig_example[sig]["verb"],
            "example_http_status": sig_example[sig]["http_status"],
            "example_body_truncated": sig_example[sig]["body_truncated"],
        })

    # ---- per-invocation rows ---------------------------------------------
    rows = []
    false_success = []
    fs_counter = collections.Counter()
    per_controller = collections.defaultdict(lambda: {"total": 0, "harness": set(), "framework": set()})

    for ep, meta in cat.items():
        per_controller[meta["controller"]]["total"] += 1
        if ep in executed_eps:
            per_controller[meta["controller"]]["harness"].add(ep)
        if ep in fw_eps:
            per_controller[meta["controller"]]["framework"].add(ep)

    for flow, hop in hops:
        ep = canon(hop["path"])
        meta = cat.get(ep, {})
        role = meta.get("role", UNKNOWN)
        ev_name = hop.get("evidence")
        ev = ev_cache.get(ev_name) if ev_name else None
        in_fw = ep in fw_eps
        source = ("both" if in_fw else "harness-run") if ev else ("framework-suite" if in_fw else "harness-run")

        checks = hop.get("checks", [])
        layers_run = [c["layer"] for c in checks]
        vp = "; ".join(f"{c['layer']} {c['check']}={c['verdict']} [{c.get('detail','')}]" for c in checks) \
            if checks else "NONE - hop was skipped before any HTTP call was issued (destructive-teardown guard)"

        body = ev.get("response") if ev else None
        fields = read_envelope_fields(body) if ev else {k: None for k in
                 ("success", "message", "error_code", "error_message", "result_type", "result_count")}
        sig = structural_signature(body) if ev else NOT_EXEC
        shape_enum, _ = pam_envelope_shape(body) if ev else (NOT_EXEC, None)

        if ev:
            actual = (f"shape={sig} | PamEnvelope.Shape={shape_enum} | Success={fields['success']} | "
                      f"Message={fields['message']!r} | ErrorCode={fields['error_code']} | "
                      f"ErrorMessage={fields['error_message']} | Result={fields['result_type']}"
                      f"({fields['result_count']}) | body={truncate(body)}")
            payload = ev.get("request_body")
            if (hop.get("verb") or "").upper() == "GET" and not payload:
                payload_s = "NONE (GET)"
            elif payload in (None, {}, ""):
                payload_s = "{} (empty body sent)"
            else:
                payload_s = truncate(payload, 600)
            status = ev.get("status") if ev.get("status") is not None else "NONE (transport error)"
            latency = ev.get("latency_ms")
            expected = ("HTTP 200; body contract: NOT DOCUMENTED - no OpenAPI/Swagger covers this "
                        f"endpoint (source-map sources={meta.get('sources') or 'none'})")
        else:
            actual = NOT_EXEC + " - hop skipped, no HTTP call issued"
            payload_s = NOT_EXEC
            status = NOT_EXEC
            latency = None
            expected = "not applicable - call deliberately skipped by the destructive-endpoint guard"

        verdicts = [c["verdict"] for c in checks]
        if not checks:
            vstatus = "SKIPPED - destructive teardown withheld"
        elif "FAIL" not in verdicts:
            vstatus = f"PASS - all {len(checks)} layers passed"
        else:
            vstatus = "FAIL - " + ",".join(sorted({c["layer"] for c in checks if c["verdict"] == "FAIL"}))

        miss = missing_for(role, hop.get("verb"), layers_run, executed=bool(ev))

        remarks = []
        if ev:
            cat_fs, why = classify_false_success(role, ev.get("status"), fields, sig, body)
            if cat_fs:
                fs_counter[cat_fs] += 1
                remarks.append(f"FALSE-SUCCESS[{cat_fs}] {why}")
                false_success.append({
                    "category": cat_fs, "endpoint_id": ep, "controller": meta.get("controller"),
                    "role": role, "flow_id": flow["id"], "hop_number": hop.get("n"),
                    "evidence_file": ev_name, "http_status": ev.get("status"),
                    "success": fields["success"], "message": fields["message"],
                    "shape_signature": sig, "explanation": why,
                })
            if ev.get("transport_error"):
                remarks.append(f"transport error: {ev['transport_error']}")
            if sig not in DOCUMENTED_SHAPES:
                remarks.append("response shape was NOT among the five previously documented shapes")
            if fields["error_code"] and str(fields["error_code"]) not in ("201", "202", "203"):
                remarks.append(f"ErrorCode {fields['error_code']!r} is outside ApiHelper.KNOWN_ERROR_CODES "
                               "{201,202,203} (ApiHelper.java:1423)")
        if in_fw:
            frow = fw["endpoints"][ep][0]
            remarks.append(f"framework positive test: {frow['class']}.java via provider {frow['provider']} "
                           f"-> {frow['sheet']}::{frow['table']} row {frow['xls_row']} "
                           f"(expected status {frow['expected_status']}), suite="
                           f"{','.join(frow['suites']) or 'NONE'}")
        else:
            remarks.append("no framework positive test covers this endpoint")

        rows.append({
            "endpoint_id": ep,
            "controller": meta.get("controller", UNKNOWN),
            "endpoint": meta.get("action", ep.split("/", 1)[-1]),
            "verb": (hop.get("verb") or meta.get("verb") or UNKNOWN).upper(),
            "path": meta.get("path", hop.get("path")),
            "role": role,
            "source": source,
            "flow_id": flow["id"],
            "hop_number": hop.get("n"),
            "evidence_file": ev_name or NOT_EXEC,
            "payload": payload_s,
            "expected_response": expected,
            "actual_response": actual,
            "envelope_shape": sig if ev else NOT_EXEC,
            "pam_envelope_shape": shape_enum,
            "success_flag": fields["success"],
            "message": fields["message"],
            "error_code": fields["error_code"],
            "result_type": fields["result_type"],
            "result_count": fields["result_count"],
            "http_status": status,
            "latency_ms": latency if latency is not None else NOT_EXEC,
            "validation_performed": vp,
            "layers_run": len(checks),
            "layers_passed": sum(1 for v in verdicts if v == "PASS"),
            "missing_validation": missing_str(miss),
            "missing_validation_count": len(miss),
            "validation_status": vstatus,
            "remarks": " | ".join(remarks),
        })

    # endpoints with no harness invocation at all
    for ep, meta in sorted(cat.items()):
        if ep in named_eps:
            continue
        in_fw = ep in fw_eps
        role = meta.get("role", UNKNOWN)
        miss = missing_for(role, meta.get("verb"), [], executed=False, framework_only=in_fw)
        if in_fw:
            frow = fw["endpoints"][ep][0]
            n_rows = len(fw["endpoints"][ep])
            source = "framework-suite"
            payload_s = ("NONE (GET)" if frow["verb"] == "GET" and not frow["payload"]
                         else (truncate(frow["payload"], 600) or "{} (empty body in Excel)"))
            expected = (f"HTTP {frow['expected_status'].split('.')[0]} from Excel column ExpectedStatus; "
                        "body contract: NOT DOCUMENTED")
            vp = ("framework only - ApiHelper.validateApiResponseWithResponseTime_ExcelBased asserts "
                  "HTTP status equality (ApiHelper.java:1273) and response time (ApiHelper.java:1276); "
                  "response-body validation is commented out (ApiHelper.java:1286-1293). "
                  "NOT EXECUTED in this evidence base - no measured verdict")
            vstatus = "NOT EXECUTED - framework test exists but was not run in this evidence base"
            remarks = (f"framework positive test: {frow['class']}.java via provider {frow['provider']} "
                       f"-> {frow['sheet']}::{frow['table']} row {frow['xls_row']} ({n_rows} Excel row(s)), "
                       f"suite={','.join(frow['suites']) or 'NONE - class is in no Positive_All suite'} | "
                       "never reached by the harness run, so no measured request/response exists")
            miss = missing_for(role, meta.get("verb"), [], executed=True, framework_only=True) + ["execution"]
            miss = list(dict.fromkeys(miss))
        else:
            source = "neither"
            payload_s = NOT_EXEC
            expected = NOT_EXEC
            vp = "NONE - no harness hop and no framework positive test targets this endpoint"
            vstatus = NOT_EXEC
            remarks = ("zero positive coverage: absent from the harness run and from every "
                       "All_API_Positive data table")
        rows.append({
            "endpoint_id": ep, "controller": meta["controller"], "endpoint": meta["action"],
            "verb": (meta.get("verb") or UNKNOWN).upper(), "path": meta["path"], "role": role,
            "source": source, "flow_id": NOT_EXEC, "hop_number": None,
            "evidence_file": NOT_EXEC, "payload": payload_s, "expected_response": expected,
            "actual_response": NOT_EXEC, "envelope_shape": NOT_EXEC,
            "pam_envelope_shape": NOT_EXEC, "success_flag": None, "message": None,
            "error_code": None, "result_type": None, "result_count": None,
            "http_status": NOT_EXEC, "latency_ms": NOT_EXEC,
            "validation_performed": vp, "layers_run": 0, "layers_passed": 0,
            "missing_validation": missing_str(miss), "missing_validation_count": len(miss),
            "validation_status": vstatus, "remarks": remarks,
        })

    # ---- coverage summary -------------------------------------------------
    covered_any = executed_eps | (fw_eps & set(cat))
    print(f"\n[coverage] catalogue                 : {len(cat)}")
    print(f"[coverage] harness-run endpoints     : {len(executed_eps)} "
          f"({100.0*len(executed_eps)/len(cat):.1f}%)")
    print(f"[coverage] framework-suite endpoints : {len(fw_eps & set(cat))} "
          f"({100.0*len(fw_eps & set(cat))/len(cat):.1f}%)")
    print(f"[coverage] both                      : {len(executed_eps & fw_eps)}")
    print(f"[coverage] either                    : {len(covered_any)} "
          f"({100.0*len(covered_any)/len(cat):.1f}%)")
    print(f"[coverage] neither (zero positive)   : {len(set(cat) - covered_any)}")
    print(f"[coverage] harness only              : {len(executed_eps - fw_eps)}")
    print(f"[coverage] framework only            : {len((fw_eps & set(cat)) - executed_eps)}")

    src_counter = collections.Counter(r["source"] for r in rows)
    print(f"\n[rows] total rows written            : {len(rows)}")
    print(f"[rows] by source                     : {dict(src_counter)}")
    print(f"[rows] distinct endpoint_id in rows  : {len({r['endpoint_id'] for r in rows})}")
    vs = collections.Counter(r["validation_status"].split(" - ")[0] for r in rows)
    print(f"[rows] by validation_status          : {dict(vs)}")

    print(f"\n[false-success] total flagged calls   : {sum(fs_counter.values())}")
    for k, v in fs_counter.most_common():
        print(f"   {v:5d}  {k}")

    # per-controller table for the report
    print("\n[per-controller] controller | catalogue | harness | framework | neither")
    ctrl_rows = []
    for c in sorted(per_controller):
        d = per_controller[c]
        neither = d["total"] - len(d["harness"] | d["framework"])
        ctrl_rows.append((c, d["total"], len(d["harness"]), len(d["framework"]), neither))
    for r in sorted(ctrl_rows, key=lambda x: -x[1]):
        print(f"   {r[0]:<34s} {r[1]:5d} {r[2]:5d} {r[3]:5d} {r[4]:5d}")

    # ---- write outputs ---------------------------------------------------
    OUT_DATA.mkdir(parents=True, exist_ok=True)
    (OUT_DATA / "positive-validation.json").write_text(
        json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT_DATA / "envelope-shapes.json").write_text(
        json.dumps({
            "meta": {
                "source": "artifacts/runs/2026-07-29_181439/evidence/ (1,868 per-call captures)",
                "calls_censused": len(ev_cache),
                "distinct_structural_signatures": len(sig_counter),
                "distinct_pam_envelope_shapes": len(enum_counter),
                "pam_envelope_shape_classes_defined": 8,
                "signatures_previously_documented": len(documented),
                "signatures_not_previously_documented": len(sig_counter) - len(documented),
                "classifier": "python mirror of com.arcon.utils.validation.PamEnvelope.of(String)",
            },
            "shapes": envelope_rows,
            "pam_envelope_shape_totals": [
                {"pam_envelope_shape": k, "calls": v,
                 "pct_of_calls": round(100.0 * v / len(ev_cache), 2)}
                for k, v in enum_counter.most_common()
            ],
        }, indent=1, ensure_ascii=False), encoding="utf-8")
    # Flat list of row objects, same convention as the two contracted files, so a
    # consolidating workbook build can ingest it without special-casing.
    (OUT_DATA / "_a2-false-success.json").write_text(
        json.dumps(false_success, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"\n[write] {OUT_DATA / 'positive-validation.json'} ({len(rows)} rows)")
    print(f"[write] {OUT_DATA / 'envelope-shapes.json'} ({len(envelope_rows)} shapes)")
    print(f"[write] {OUT_DATA / '_a2-false-success.json'} ({len(false_success)} instances)")

    print("\n" + "=" * 78)
    if DISAGREEMENTS:
        print("!! DISAGREEMENT WITH docs/history/archive/document-agent-brief.md - reported, not overwritten:")
        for d in DISAGREEMENTS:
            print("   !! " + d)
    else:
        print("OK every brief tally reproduced exactly (endpoints, flows, hops, calls, L1-L7).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
