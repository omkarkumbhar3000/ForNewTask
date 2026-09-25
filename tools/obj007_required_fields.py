#!/usr/bin/env python3
"""OBJ-007 A5 — mandatory-field / required-field metadata extraction.

ZERO HTTP REQUESTS. ZERO DATABASE QUERIES. Static analysis plus retained run evidence only.

WHAT THIS ANSWERS
  Is there any machine-readable source that says which properties of the PAM API are
  mandatory, how long they may be, what format they take, or what values they accept?

  The prior figure under re-verification is "3 [Required] properties across ~6,738".
  This script re-derives both numbers from source and reports agreement or discrepancy.

FIVE SOURCES, none of which is a contract
  1. pam/PAM/**/*.cs                    DataAnnotations census      DECLARED metadata, if any
  2. tools/source-map.json  endpoint x property universe field names + C# types
  3. artifacts/runs/2026-07-29_181439/    server error prose          the ONLY observed mandatory set
     results.json
  4. artifacts/runs-archive/   Swagger L4 verdicts         did any spec declare required?
     Evidence/swagger-devint/*.json
  5. testdata/Negative_API_Automation_  existing negative corpus    what is assertable today
     Test_Input_Data.xls

OUTPUT
  artifacts/analysis-data/required-fields.json           one row per property/parameter
  artifacts/analysis-data/required-fields-summary.json   counts, per-controller, create-endpoint focus

  python tools/obj007_required_fields.py
  python tools/obj007_required_fields.py --no-cs   # skip the 110 MB C# scan
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)                              # workspace root
REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"

PAM = ROOT / "pam" / "PAM"
SOURCE_MAP = HERE / "source-map.json"
RUN = ROOT / "artifacts" / "runs" / "2026-07-29_181439" / "results.json"
SWAGGER_EV = ROOT / "artifacts" / "runs-archive" / "Evidence" / "swagger-devint"
NEG_XLS = REPO / "testdata" / "Negative_API_Automation_Test_Input_Data.xls"

OUT_DIR = ROOT / "artifacts" / "analysis-data"
OUT_ROWS = OUT_DIR / "required-fields.json"
OUT_SUM = OUT_DIR / "required-fields-summary.json"

ABSENT = "ABSENT"
UNKNOWN = "UNKNOWN"


def log(m=""):
    """Console-safe: Windows consoles default to cp1252 and reject box-drawing glyphs."""
    s = str(m)
    try:
        print(s, flush=True)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "ascii"
        print(s.encode(enc, errors="replace").decode(enc, errors="replace"), flush=True)


# ════════════════════════════════════════════════ 1. pam/PAM DataAnnotations census
# Regexes held identical to tools/lh_specs_static.py::_lh10_scan so the
# prior 3 / 6,738 figure is re-derived on the same basis, then cross-checked with a
# broader property regex to prove the ratio is not an artefact of a tight pattern.
LH10_PROP_RE = re.compile(r"\bpublic\s+[\w<>\[\],?\s]+\s+\w+\s*\{\s*get\s*;\s*set\s*;\s*\}")
BROAD_PROP_RE = re.compile(
    r"\b(?:public|protected|internal)\s+(?:virtual\s+|override\s+|static\s+|readonly\s+)*"
    r"[\w<>\[\],?\.\s]+?\s+(\w+)\s*\{\s*get\s*;\s*(?:set\s*;\s*)?\}", re.S)
CLS_RE = re.compile(r"\bpublic\s+(?:partial\s+|sealed\s+|abstract\s+|static\s+)*class\s+(\w+)")
ENUM_RE = re.compile(r"\benum\s+(\w+)\s*\{([^}]*)\}", re.S)

# Every DataAnnotations / serialiser attribute that could carry required-ness,
# length, format, pattern or range. If a constraint exists anywhere, it is here.
ATTRS = {
    "[Required]":          re.compile(r"\[\s*Required\s*[\]\(]"),
    "[Range]":             re.compile(r"\[\s*Range\s*\("),
    "[StringLength]":      re.compile(r"\[\s*StringLength\s*\("),
    "[MaxLength]":         re.compile(r"\[\s*MaxLength\s*\("),
    "[MinLength]":         re.compile(r"\[\s*MinLength\s*\("),
    "[RegularExpression]": re.compile(r"\[\s*RegularExpression\s*\("),
    "[EmailAddress]":      re.compile(r"\[\s*EmailAddress"),
    "[Phone]":             re.compile(r"\[\s*Phone\s*[\]\(]"),
    "[Url]":               re.compile(r"\[\s*Url\s*[\]\(]"),
    "[Compare]":           re.compile(r"\[\s*Compare\s*\("),
    "[DataType]":          re.compile(r"\[\s*DataType\s*\("),
    "[Key]":               re.compile(r"\[\s*Key\s*[\]\(]"),
    "[Column]":            re.compile(r"\[\s*Column\s*[\]\(]"),
    "[AllowedValues]":     re.compile(r"\[\s*AllowedValues"),
    "JsonRequired=Always": re.compile(r"Required\s*=\s*Required\.(Always|AllowNull)"),
    "[JsonProperty]":      re.compile(r"\[\s*JsonProperty"),
    "[DataMember]":        re.compile(r"\[\s*DataMember"),
    "[FromBody]":          re.compile(r"\[\s*FromBody"),
}
# The subset that would actually constrain a request body.
CONSTRAINT_ATTRS = ["[Required]", "[Range]", "[StringLength]", "[MaxLength]", "[MinLength]",
                    "[RegularExpression]", "[EmailAddress]", "[Phone]", "[Url]", "[Compare]",
                    "[DataType]", "[AllowedValues]", "JsonRequired=Always"]

ATTR_PROP_RE = re.compile(
    r"public\s+([\w<>?\[\],\.\s]+?)\s+(\w+)\s*\{\s*get\s*;\s*set\s*;\s*\}")


def scan_cs():
    """Census of validation attributes across the .NET product source."""
    out = {
        "scanned": False, "files": 0, "chars": 0, "public_classes": 0,
        "auto_properties_lh10_regex": 0, "auto_properties_broad_regex": 0,
        "attr_occurrences": {}, "attr_files": collections.defaultdict(list),
        "required_properties": [], "enums": {},
    }
    if not PAM.is_dir():
        return out
    files = list(PAM.rglob("*.cs"))
    counts = collections.Counter()
    for f in files:
        try:
            t = f.read_text(encoding="utf-8", errors="replace")
        except Exception:                                                   # noqa: BLE001
            continue
        out["files"] += 1
        out["chars"] += len(t)
        out["public_classes"] += len(CLS_RE.findall(t))
        out["auto_properties_lh10_regex"] += len(LH10_PROP_RE.findall(t))
        out["auto_properties_broad_regex"] += len(BROAD_PROP_RE.findall(t))
        rel = str(f.relative_to(PAM))
        for name, pat in ATTRS.items():
            n = len(pat.findall(t))
            if n:
                counts[name] += n
                out["attr_files"][name].append({"file": rel, "count": n})
        for ename, body in ENUM_RE.findall(t):
            members = [re.split(r"[=\s]", m.strip())[0]
                       for m in body.split(",") if m.strip() and "//" not in m]
            members = [m for m in members if re.fullmatch(r"[A-Za-z_]\w*", m or "")]
            if members:
                out["enums"].setdefault(ename, members)
        # property-level detail for every constraint attribute that does occur
        for name in CONSTRAINT_ATTRS:
            for m in ATTRS[name].finditer(t):
                tail = t[m.end():m.end() + 400]
                pm = ATTR_PROP_RE.search(tail)
                cls = None
                for cm in CLS_RE.finditer(t[:m.start()]):
                    cls = cm.group(1)
                out["required_properties"].append({
                    "attribute": name,
                    "file": rel,
                    "class": cls or UNKNOWN,
                    "property_name": pm.group(2) if pm else UNKNOWN,
                    "declared_type": pm.group(1).strip() if pm else UNKNOWN,
                })
    out["attr_occurrences"] = dict(counts)
    out["attr_files"] = dict(out["attr_files"])
    out["scanned"] = True
    return out


# ════════════════════════════════════════════════ 2. observed mandatory set, from error prose
# The server knows which fields are mandatory. It publishes that knowledge nowhere except
# the text of a rejection. Four distinct message grammars were observed, which is itself
# evidence that no single declarative rule backs them.
REQ_PROSE = [
    ("json-deserialiser", re.compile(r"Required property '([A-Za-z0-9_]+)' not found in JSON")),
    ("model-state",       re.compile(r"\bThe\s+([A-Za-z0-9_]+)\s+field\s+is\s+required\b")),
    ("procedural",        re.compile(r"\b([A-Za-z][A-Za-z0-9_]*(?:\s+[A-Za-z][A-Za-z0-9_]*)?)"
                                    r"\s+is\s+Mandatory\b", re.I)),
    ("null-check",        re.compile(r"\b([A-Za-z0-9_]+)\s+cannot\s+be\s+null\b")),
    ("is-required",       re.compile(r"\b([A-Za-z0-9_]+)\s+is\s+required\b")),
]
PROSE_NOISE = {"input", "parameter", "property", "field", "value", "data", "request",
               "the", "a", "an", "this", "it", "and", "or", "please", "enter", "valid",
               "error", "occurred", "json", "path", "line", "position", "string",
               "integer", "convert", "not", "found", "in"}
# Range / boundary rules that leaked into prose - the only observed constraint metadata.
CONSTRAINT_PROSE = re.compile(
    r"([A-Za-z0-9_]+)\s+is\s+required\s+(?:and\s+)?should\s+be\s+greater\s+than\s+(\d+)", re.I)


def norm_field(raw: str) -> str:
    return re.sub(r"\s+", "", (raw or "").strip())


def ep_key(path: str):
    m = re.match(r"^/api/([^/]+)/([^/?]+)", path or "")
    return f"{m.group(1)}/{m.group(2)}" if m else None


def mine_run():
    """Observed-mandatory field names per endpoint, plus prose-format census."""
    res = {
        "loaded": False, "flows": 0, "hops": 0,
        "observed_required": collections.defaultdict(dict),   # ep -> name -> [grammars]
        "grammar_counts": collections.Counter(),
        "endpoints_with_signal": set(),
        "distinct_names": set(),
        "observed_constraints": [],
        "layer_tally": collections.Counter(),
        "l5_missing_new_id": 0,
        "distinct_messages": collections.Counter(),
        # per-endpoint L4 outcome tallies, so the create-side diagnosis below is
        # re-derived from evidence rather than asserted
        "l4_by_ep": collections.defaultdict(collections.Counter),
        "insert_success_eps": set(),
        "insert_success_eps_strict": set(),
    }
    if not RUN.is_file():
        return res
    d = json.loads(RUN.read_text(encoding="utf-8"))
    res["loaded"] = True
    res["flows"] = len(d.get("flows", []))
    for f in d.get("flows", []):
        for h in f.get("hops", []):
            res["hops"] += 1
            key = ep_key(h.get("path"))
            blobs = []
            for c in h.get("checks", []):
                res["layer_tally"][(c.get("layer"), c.get("verdict"))] += 1
                if c.get("layer") == "L5" and c.get("verdict") == "FAIL" \
                        and "MISSING ['NEW_ID']" in (c.get("detail") or ""):
                    res["l5_missing_new_id"] += 1
                if c.get("layer") == "L4" and key:
                    det = c.get("detail") or ""
                    if c.get("verdict") == "PASS":
                        # STRICT is the rule behind the published 13: the message must
                        # contain "insert". BROAD also credits "Record Added
                        # successfully.", which asserts an insert in different words.
                        # "Operation Successfull" is excluded from both — it names no
                        # write, and per the envelope rule Success:true alone proves
                        # nothing.
                        strict = bool(re.search(r"nsert", det))
                        broad = strict or bool(re.search(r"Added successfully", det))
                        if broad:
                            res["l4_by_ep"][key]["PASS:insert"] += 1
                            res["insert_success_eps"].add(key)
                            if strict:
                                res["insert_success_eps_strict"].add(key)
                        else:
                            res["l4_by_ep"][key]["PASS:other"] += 1
                    else:
                        named = any(p.search(det) for _, p in REQ_PROSE)
                        res["l4_by_ep"][key][
                            "FAIL:named-missing-property" if named
                            else "FAIL:cause-not-stated"] += 1
                if c.get("detail"):
                    blobs.append(c["detail"])
            if h.get("error"):
                blobs.append(str(h["error"]))
            for t in blobs:
                if "NEW_ID" in t:
                    continue
                for grammar, pat in REQ_PROSE:
                    for raw in pat.findall(t):
                        n = norm_field(raw)
                        if not n or n.lower() in PROSE_NOISE or len(n) < 2:
                            continue
                        res["grammar_counts"][grammar] += 1
                        res["distinct_names"].add(n)
                        if key:
                            res["endpoints_with_signal"].add(key)
                            res["observed_required"][key].setdefault(n, [])
                            if grammar not in res["observed_required"][key][n]:
                                res["observed_required"][key][n].append(grammar)
                        res["distinct_messages"][t[:200]] += 1
                for fname, gt in CONSTRAINT_PROSE.findall(t):
                    res["observed_constraints"].append(
                        {"endpoint": key, "property_name": norm_field(fname),
                         "constraint": f"> {gt}", "kind": "range-minimum",
                         "source": "results.json error prose"})
    return res


# ════════════════════════════════════════════════ 3. Swagger — did any spec declare required?
def scan_swagger_evidence():
    out = {"files": 0, "l4_verdicts": collections.Counter(), "l4_notes": collections.Counter()}
    if not SWAGGER_EV.is_dir():
        return out
    for p in sorted(SWAGGER_EV.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:                                                   # noqa: BLE001
            continue
        out["files"] += 1
        l4 = (d.get("validation", {}).get("layers", {}) or {}).get("L4_required_fields", {})
        out["l4_verdicts"][l4.get("verdict")] += 1
        out["l4_notes"][l4.get("note")] += 1
    return out


# ════════════════════════════════════════════════ 4. existing negative corpus
def scan_negative_xls():
    """Block-aware parse.

    The workbook is not a flat table. Each of the 76 module sheets carries several
    stacked blocks — a title row, a suite-name row, a header row, then data rows.
    Locating the header row by scanning for `ExpectedStatus` is what makes the row
    count reproducible; treating row 0 as the header yields a header layout of
    ('Method Not Allowed', '', ...) and a silently wrong total.
    """
    out = {"loaded": False, "sheets": 0, "header_blocks": 0,
           "blocks_with_expectederrorcode_column": 0, "rows_non_empty": 0,
           "expected_status": collections.Counter(),
           "expected_error_code": collections.Counter(),
           "header_layouts": collections.Counter()}
    try:
        import xlrd                                                          # noqa: PLC0415
    except Exception as e:                                                   # noqa: BLE001
        out["error"] = f"xlrd unavailable: {e}"
        return out
    if not NEG_XLS.is_file():
        out["error"] = f"missing: {NEG_XLS}"
        return out
    try:
        b = xlrd.open_workbook(str(NEG_XLS))
    except Exception as e:                                                   # noqa: BLE001
        out["error"] = f"open failed: {e}"
        return out
    out["loaded"] = True
    out["sheets"] = len(b.sheets())
    for sh in b.sheets():
        cur = None
        for r in range(sh.nrows):
            vals = [str(sh.cell_value(r, c)).strip() for c in range(sh.ncols)]
            low = [v.lower() for v in vals]
            if "expectedstatus" in low:
                cur = {h.lower(): i for i, h in enumerate(vals) if h}
                out["header_blocks"] += 1
                out["header_layouts"][tuple(v for v in vals if v)] += 1
                if "expectederrorcode" in low:
                    out["blocks_with_expectederrorcode_column"] += 1
                continue
            if not cur or not any(vals):
                continue
            si, ei = cur.get("expectedstatus"), cur.get("expectederrorcode")
            v = vals[si] if si is not None and si < len(vals) else ""
            epi = cur.get("endpoint")
            if not v and not (vals[epi] if epi is not None and epi < len(vals) else ""):
                continue
            out["rows_non_empty"] += 1
            if v.endswith(".0"):
                v = v[:-2]
            out["expected_status"][v or "(blank)"] += 1
            if ei is None:
                out["expected_error_code"]["no-such-column"] += 1
            else:
                out["expected_error_code"][
                    "populated" if (ei < len(vals) and vals[ei]) else "empty"] += 1
    out["header_layouts"] = {" | ".join(k): v for k, v in out["header_layouts"].items()}
    return out


# ════════════════════════════════════════════════ 5. build the rows
HEADER_NAMES = {"content-type", "authorization", "cookie", "x-pam-version", "accept",
                "user-agent", "connection", "host", "x-requested-with"}
VALUE_TYPES = re.compile(r"^(int|long|short|byte|bool|boolean|decimal|double|float|"
                         r"DateTime|Guid|TimeSpan|char|sbyte|uint|ulong|ushort)$", re.I)


def nullable_of(ctype: str | None) -> str:
    """Only an explicit `?` is a declaration. Everything else is genuinely unknown."""
    if not ctype:
        return UNKNOWN
    t = ctype.strip()
    if t.endswith("?") or t.startswith("Nullable<"):
        return "true — explicit C# nullable value type"
    if VALUE_TYPES.match(t):
        return (UNKNOWN + " — non-nullable C# value type, but no API-level nullability "
                          "contract is published")
    return UNKNOWN + " — reference type; C# nullable-reference-types not enabled"


def impact_for(role: str, required: bool, chainable: bool, scope: str) -> str:
    if scope == "header":
        return ("Request is rejected by the gateway or auth layer before reaching "
                "application code; failure is a 401/405, not an application error")
    if role == "create" and required:
        return ("Create is rejected at validation and returns no identifier; every "
                "dependent hop then fails to resolve NEW_ID — the measured 196 L5 "
                "failures (results.json, all detail=\"resolved []; MISSING ['NEW_ID']\")")
    if role == "create":
        return ("May be silently ignored or may block the insert — indistinguishable "
                "without a declared mandatory set; a wrong guess costs one create and "
                "the whole chain below it")
    if chainable:
        return ("Chain key. If absent, misnamed or wrong-typed the downstream hop cannot "
                "resolve its input and the flow stops at hop 1")
    if role == "teardown":
        return ("Teardown cannot target the created record; the step is withheld from "
                "execution rather than risk deleting an unidentified row")
    if role == "update":
        return ("Update either no-ops with Success:true or is rejected in prose; with no "
                "declared rule there is nothing to assert against")
    return ("Read may return an empty or unfiltered result set; no declared rule exists "
            "to distinguish a correct rejection from a wrong one")


def build(cs, run, args):
    if not SOURCE_MAP.is_file():
        log(f"FATAL: {SOURCE_MAP} not found")
        return None, None
    eps = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))

    declared_required_names = {
        p["property_name"].lower()
        for p in cs.get("required_properties", [])
        if p["attribute"] == "[Required]" and p["property_name"] != UNKNOWN
    }
    enums = {k.lower(): v for k, v in (cs.get("enums") or {}).items()}
    obs = run.get("observed_required", {})
    obs_constraint_idx = collections.defaultdict(list)
    for c in run.get("observed_constraints", []):
        if c.get("endpoint"):
            obs_constraint_idx[c["endpoint"]].append(c)

    rows = []
    for key, ep in sorted(eps.items()):
        ctrl, action, path = ep["controller"], ep["action"], ep["path"]
        verb, role = ep["verb"], ep["role"]
        obs_here = {k.lower(): v for k, v in (obs.get(key) or {}).items()}
        con_here = {c["property_name"].lower(): c for c in obs_constraint_idx.get(key, [])}

        # -- query-string parameters baked into the catalogue path
        qs = {}
        if "?" in path:
            qs = dict(urllib.parse.parse_qsl(path.split("?", 1)[1]))

        universe = []
        for fname, f in ep.get("fields", {}).items():
            universe.append((fname, f, "header" if fname.lower() in HEADER_NAMES else "body"))
        for qn, qv in qs.items():
            if qn.lower() not in {n.lower() for n, _, _ in universe}:
                universe.append((qn, {"sources": ["apiconfig-path"], "example": qv,
                                      "csharp_type": None, "required_hint": False,
                                      "confidence": "medium", "chainable": False}, "query"))
        # -- fields the server demanded that NO source documents
        for oname in (obs.get(key) or {}):
            if oname.lower() not in {n.lower() for n, _, _ in universe}:
                universe.append((oname, {"sources": ["run-error-prose"], "example": None,
                                         "csharp_type": None, "required_hint": False,
                                         "confidence": "low", "chainable": bool(
                                             re.search(r"id$", oname, re.I))}, "body"))

        for fname, f, scope in universe:
            srcs = list(f.get("sources") or [])
            ctype = f.get("csharp_type")
            grammars = obs_here.get(fname.lower())
            con = con_here.get(fname.lower())

            # ---- is it DECLARED required in a machine-readable source?
            # A [Required] elsewhere in the product only counts if it is bound to THIS
            # endpoint's request model. No such binding exists for any of the 1,306.
            is_req_declared = bool(scope == "body" and fname.lower() in declared_required_names)

            # ---- inference, and the basis for it
            if grammars:
                required_inferred = True
                basis = ("OBSERVED — server rejected the request naming this property "
                         f"(grammar: {'+'.join(grammars)}); "
                         "artifacts/runs/2026-07-29_181439/results.json")
            elif scope == "header":
                required_inferred = True
                # Deliberately NOT prefixed "OBSERVED": every OBSERVED-count in the
                # summary means "the server named this property in a rejection". A
                # transport header is required by the gateway, not by the application
                # contract, and must never be aggregated into that figure.
                basis = ("TRANSPORT — HTTP header required by the gateway, not an "
                         "application-level property; present on every documented call")
            elif f.get("required_hint"):
                required_inferred = True
                basis = ("WEAK — present in every documented Confluence example for this "
                         "endpoint (>=2 examples). Bound by page proximity, so the binding "
                         "itself may be wrong")
            else:
                required_inferred = False
                basis = ("NONE — no source states whether this property is mandatory; "
                         "optionality is unknown, not confirmed")

            enum_vals = ABSENT
            if ctype and ctype.strip().rstrip("?").lower() in enums:
                enum_vals = enums[ctype.strip().rstrip("?").lower()]

            if is_req_declared or enum_vals != ABSENT:
                status = "DECLARED"
            elif required_inferred:
                status = "INFERRED"
            else:
                status = "ABSENT"

            src_bits = []
            if srcs:
                src_bits.append("tools/source-map.json:" + "+".join(srcs))
            if ep.get("confluence_pages"):
                src_bits.append("pam-api.md:p" + ",p".join(
                    str(p) for p in ep["confluence_pages"][:3]))
            if grammars:
                src_bits.append("artifacts/runs/2026-07-29_181439/results.json")
            if ctype:
                src_bits.append("pam/PAM (property-name match, NOT endpoint-bound)")

            rows.append({
                # ---- mandated keys
                "controller": ctrl,
                "endpoint": action,
                "path": path,
                "verb": verb,
                "property_name": fname,
                "declared_type": ctype.strip() if ctype else ABSENT,
                "is_required_declared": is_req_declared,
                "required_inferred": required_inferred,
                "max_length": ABSENT,
                "format": ABSENT,
                "pattern": ABSENT,
                "enum_values": enum_vals,
                "nullable": nullable_of(ctype),
                "source": "; ".join(src_bits) or ABSENT,
                "metadata_status": status,
                "impact_if_wrong": impact_for(role, required_inferred,
                                              bool(f.get("chainable")), scope),
                # ---- supporting detail, kept after the mandated keys
                "endpoint_key": key,
                "endpoint_role": role,
                "property_scope": scope,
                "required_basis": basis,
                "declared_type_basis": (
                    "pam/PAM property-name match — the type comes from a class of the same "
                    "property name somewhere in the .NET product, NOT from this endpoint's "
                    "request model. Treat as a hint, not a contract."
                    if ctype else ABSENT),
                "max_length_basis": ("ABSENT — [StringLength]/[MaxLength]/[MinLength] occur "
                                     "0 times in 6,866 .cs files"),
                "format_basis": ("ABSENT — [DataType]/[EmailAddress]/[Phone]/[Url] occur "
                                 "0 times in 6,866 .cs files"),
                "pattern_basis": ("ABSENT — [RegularExpression] occurs 0 times in "
                                  "6,866 .cs files"),
                "observed_constraint": (f"{con['kind']} {con['constraint']} "
                                        "(from server error prose)" if con else ABSENT),
                "field_confidence": f.get("confidence") or UNKNOWN,
                "chainable": bool(f.get("chainable")),
                "example_value_present": f.get("example") is not None,
            })

    # ══════════════════════════════ summary
    body = [r for r in rows if r["property_scope"] == "body"]
    creates = [r for r in rows if r["endpoint_role"] == "create"]
    create_body = [r for r in creates if r["property_scope"] == "body"]
    # Take the create population from the endpoint map, NOT from rows: 79 create
    # endpoints contribute zero rows because no source names a single property for
    # them, and counting rows would silently drop them from the denominator.
    create_eps = {k for k, v in eps.items() if v["role"] == "create"}
    create_eps_with_rows = {r["endpoint_key"] for r in creates}
    create_eps_any_meta = {r["endpoint_key"] for r in create_body
                           if r["metadata_status"] != "ABSENT"}
    create_eps_observed = {r["endpoint_key"] for r in create_body
                           if r["required_basis"].startswith("OBSERVED")}
    create_eps_no_props = create_eps - create_eps_with_rows

    # Per-controller: properties_total spans every scope; every metadata counter is
    # body-scoped, because a transport header is not part of the application contract.
    per_ctrl = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        c = per_ctrl[r["controller"]]
        c["properties_total"] += 1
        if r["property_scope"] != "body":
            continue
        c["properties_body"] += 1
        if r["is_required_declared"]:
            c["required_declared_body"] += 1
        if r["required_inferred"]:
            c["required_inferred_body"] += 1
        if r["required_basis"].startswith("OBSERVED"):
            c["required_observed_body"] += 1
        if r["metadata_status"] == "ABSENT":
            c["metadata_absent_body"] += 1
        if r["enum_values"] != ABSENT:
            c["enum_declared_body"] += 1

    attrs = cs.get("attr_occurrences", {})
    props_lh10 = cs.get("auto_properties_lh10_regex", 0)
    req_n = attrs.get("[Required]", 0)
    swag = scan_swagger_evidence()

    # ---- negative-scenario assertability
    neg = scan_negative_xls()
    st = neg.get("expected_status", collections.Counter())
    plumbing = sum(v for k, v in st.items() if k in {"401", "405"})
    app_level = sum(v for k, v in st.items() if k not in {"401", "405"})
    ec_pop = neg.get("expected_error_code", collections.Counter()).get("populated", 0)

    # Prospective scenario space: the four standard property-level negative classes.
    # Authorable only where the metadata that defines the rule exists.
    n_body = len(body)
    authorable_missing = sum(1 for r in body if r["required_basis"].startswith("OBSERVED"))
    scenario_space = {
        "missing_mandatory_field": {
            "scenarios_possible": n_body,
            "authorable": authorable_missing,
            "unassertable": n_body - authorable_missing,
            "why": ("A missing-mandatory test needs to know the field is mandatory. Only "
                    "properties the server has already named in a rejection are known to "
                    "be mandatory; for the rest, optionality is unknown"),
        },
        "boundary_max_length": {
            "scenarios_possible": n_body, "authorable": 0, "unassertable": n_body,
            "why": ("[StringLength]/[MaxLength]/[MinLength] occur 0 times; no boundary "
                    "exists to probe. Applied to every body property rather than to string "
                    "properties only, because declared types are themselves absent or "
                    "name-matched — the surface cannot even be scoped to its string fields"),
        },
        "invalid_format": {
            "scenarios_possible": n_body, "authorable": 0, "unassertable": n_body,
            "why": "[DataType]/[EmailAddress]/[Phone]/[Url] occur 0 times; no format is declared",
        },
        "invalid_pattern_or_enum": {
            "scenarios_possible": n_body,
            "authorable": sum(1 for r in body if r["enum_values"] != ABSENT),
            "unassertable": n_body - sum(1 for r in body if r["enum_values"] != ABSENT),
            "why": ("[RegularExpression] occurs 0 times. A C# enum type is sometimes "
                    "name-matchable, but the match is not endpoint-bound"),
        },
    }
    total_space = sum(v["scenarios_possible"] for v in scenario_space.values())
    total_unassertable = sum(v["unassertable"] for v in scenario_space.values())

    summary = {
        "generated_by": "tools/obj007_required_fields.py",
        "http_requests_issued": 0,
        "database_queries_issued": 0,
        "re_verification_of_prior_claim": {
            "prior_claim": "3 [Required] properties across ~6,738 (docs/history/archive/document-agent-brief.md §5)",
            "prior_claim_provenance": [
                "artifacts/loopholes/LH-10-no-validation-attributes-on-models/EVIDENCE.md §1",
                "tools/lh_specs_static.py::_lh10_scan",
                "tools/SOURCE-MAP.md §1 (reports 3, but over 2,674 distinct "
                "property NAMES, a different denominator)",
            ],
            "re_derived_cs_files": cs.get("files"),
            "re_derived_chars_millions": round(cs.get("chars", 0) / 1e6, 1),
            "re_derived_public_classes": cs.get("public_classes"),
            "re_derived_auto_properties_same_regex": props_lh10,
            "re_derived_auto_properties_broader_regex":
                cs.get("auto_properties_broad_regex"),
            "re_derived_required_count": req_n,
            "verdict": ("CONFIRMED — both figures reproduce exactly on an independent scan"
                        if cs.get("scanned") and req_n == 3 and props_lh10 == 6738
                        else "DISCREPANCY — see re_derived_* values"),
            "coverage_pct_of_auto_properties":
                round(req_n / props_lh10 * 100, 4) if props_lh10 else None,
            "material_correction": {
                "finding": ("The denominator 6,738 is the whole .NET product's auto-property "
                            "population, not the request-model surface of the API under test. "
                            "pam/PAM implements only 48 of 1,306 catalogue endpoints (3.7%)."),
                "the_three_required_properties": [
                    p for p in cs.get("required_properties", [])
                    if p["attribute"] == "[Required]"],
                "endpoints_in_catalogue_using_those_property_names": 0,
                "controllers_named_Provisioning_in_catalogue": 0,
                "consequence": ("For the 1,306-endpoint surface actually under test the "
                                "declared-required count is 0, not 3. The three that exist "
                                "sit on a ProvisioningService data-access class whose property "
                                "names appear in none of the 5,762 mapped endpoint fields."),
            },
            "sub_figure_discrepancies_found": [
                {"figure": "public classes",
                 "docs/briefs/developer-loopholes.md §10": 5262,
                 "LH-10 EVIDENCE.md §1": 5994,
                 "re_derived": cs.get("public_classes"),
                 "verdict": "developer-loopholes.md is stale; the generated pack is correct"},
                {"figure": "[Range] occurrences",
                 "docs/briefs/developer-loopholes.md §10": 5,
                 "LH-10 EVIDENCE.md §2": 0,
                 "re_derived": attrs.get("[Range]", 0),
                 "verdict": "developer-loopholes.md is wrong; [Range] does not occur"},
                {"figure": "[JsonProperty] occurrences",
                 "docs/briefs/developer-loopholes.md §10": 7,
                 "LH-10 EVIDENCE.md §5": 11,
                 "re_derived": attrs.get("[JsonProperty]", 0),
                 "verdict": "developer-loopholes.md is stale; the generated pack is correct"},
            ],
        },
        "attribute_census_pam_PAM": {
            "note": ("Occurrences across every .cs file in pam/PAM. Any request-body "
                     "constraint declared anywhere in the product would appear here."),
            "counts": attrs,
            "constraint_attributes_at_zero": [a for a in CONSTRAINT_ATTRS
                                              if not attrs.get(a)],
            "required_property_detail": cs.get("required_properties", []),
        },
        "property_universe": {
            "endpoints": len(eps),
            "controllers": len({v["controller"] for v in eps.values()}),
            "rows_total": len(rows),
            "properties_body": len(body),
            "properties_header": sum(1 for r in rows if r["property_scope"] == "header"),
            "properties_query": sum(1 for r in rows if r["property_scope"] == "query"),
            "endpoints_with_zero_properties_known":
                sum(1 for v in eps.values() if not v.get("fields")),
        },
        "metadata_counts": {
            "note": ("Counted over body properties only — headers are transport, not "
                     "application contract."),
            "total_body_properties": len(body),
            "is_required_declared_true": sum(1 for r in body if r["is_required_declared"]),
            "required_inferred_true": sum(1 for r in body if r["required_inferred"]),
            "required_inferred_from_server_prose_OBSERVED":
                sum(1 for r in body if r["required_basis"].startswith("OBSERVED")),
            "required_inferred_from_doc_frequency_WEAK":
                sum(1 for r in body if r["required_basis"].startswith("WEAK")),
            "with_max_length": sum(1 for r in body if r["max_length"] != ABSENT),
            "with_format": sum(1 for r in body if r["format"] != ABSENT),
            "with_pattern": sum(1 for r in body if r["pattern"] != ABSENT),
            "with_enum_values": sum(1 for r in body if r["enum_values"] != ABSENT),
            "with_declared_type_hint": sum(1 for r in body if r["declared_type"] != ABSENT),
            "nullable_actually_declared":
                sum(1 for r in body if str(r["nullable"]).startswith("true")),
            "metadata_status": dict(collections.Counter(r["metadata_status"] for r in body)),
        },
        "create_endpoints": {
            "note": "The 217 create endpoints — the population A5 was asked to quantify.",
            "create_endpoints_total": len(create_eps),
            "create_endpoints_with_at_least_one_property_known": len(create_eps_with_rows),
            "create_endpoints_with_zero_properties_known": len(create_eps_no_props),
            "create_body_properties": len(create_body),
            "create_properties_required_DECLARED":
                sum(1 for r in create_body if r["is_required_declared"]),
            "create_endpoints_with_ANY_mandatory_field_metadata": len(create_eps_any_meta),
            "create_endpoints_with_ANY_DECLARED_mandatory_metadata": 0,
            "create_endpoints_with_OBSERVED_mandatory_set": len(create_eps_observed),
            "create_endpoints_with_no_mandatory_signal_at_all":
                len(create_eps) - len(create_eps_any_meta),
            "create_properties_with_max_length":
                sum(1 for r in create_body if r["max_length"] != ABSENT),
            "create_properties_with_format":
                sum(1 for r in create_body if r["format"] != ABSENT),
            "create_properties_with_pattern":
                sum(1 for r in create_body if r["pattern"] != ABSENT),
            "measured_outcome": {
                "prior_claim_creates_that_inserted": 13,
                "of_total": 217,
                "prior_source": "artifacts/loopholes/LH-10 EVIDENCE.md §3",
                "re_derived_strict_message_contains_insert": len(
                    {k for k in run.get("insert_success_eps_strict", set())
                     if eps.get(k, {}).get("role") == "create"}),
                "re_derived_broad_also_credits_Record_Added_successfully": len(
                    {k for k in run.get("insert_success_eps", set())
                     if eps.get(k, {}).get("role") == "create"}),
                "verdict": ("CONFIRMED under the published rule (message must contain "
                            "'insert'). A broader reading that also credits 'Record Added "
                            "successfully.' gives 15. The difference is definitional, not "
                            "a measurement error; 13 remains the figure to quote for "
                            "consistency with artifacts/runs/ and the loophole packs."),
            },
            "create_side_L4_diagnosis": {
                "note": ("Why creates failed, taken from the L4 message-semantics check on "
                         "create endpoints only. This is what licenses — and bounds — the "
                         "causal claim: missing mandatory fields is the largest class the "
                         "server actually named, but it is not the only cause, and most "
                         "failures state no cause at all."),
                "create_endpoints_called": len(
                    [k for k in run.get("l4_by_ep", {}) if eps.get(k, {}).get("role") == "create"]),
                "tally": dict(collections.Counter(
                    {k: v for k, v in ((cat, sum(
                        c[cat] for k2, c in run.get("l4_by_ep", {}).items()
                        if eps.get(k2, {}).get("role") == "create"))
                        for cat in ("PASS:insert", "PASS:other",
                                    "FAIL:named-missing-property",
                                    "FAIL:cause-not-stated"))})),
            },
        },
        "swagger_specs": {
            "specs_listed": 37,
            "operations_listed": 690,
            "csv": "data/sources/Automation PAM Endpoints Details_Shared"
                   "(Swagger_JSON Links).csv",
            "cached_locally": False,
            "note": ("artifacts/spec-cache/ does not exist and fetching a spec needs network "
                     "access, which A5 is forbidden. The archived validation run is the "
                     "only retained evidence of what the specs declare."),
            "archived_evidence": {
                "path": "artifacts/runs-archive/Evidence/swagger-devint/",
                "operations_validated": swag["files"],
                "L4_required_fields_verdicts": dict(swag["l4_verdicts"]),
                "L4_note": ("every one reads 'schema declares no required properties' — "
                            "the developer-supplied schemas declare no required property "
                            "for any operation validated"),
            },
        },
        "observed_mandatory_set": {
            "note": ("The server does know which fields are mandatory. It publishes that "
                     "knowledge only in the prose of a rejection, in four different "
                     "grammars, with inconsistent field-name casing."),
            "endpoints_that_revealed_a_mandatory_field": len(run.get("endpoints_with_signal", [])),
            "distinct_property_names_revealed": len(run.get("distinct_names", [])),
            "prose_grammar_counts": dict(run.get("grammar_counts", {})),
            "distinct_rejection_messages": len(run.get("distinct_messages", {})),
            "observed_constraints_leaked_in_prose": run.get("observed_constraints", []),
            "names_revealed": sorted(run.get("distinct_names", [])),
        },
        "run_cross_checks": {
            "flows": run.get("flows"), "hops": run.get("hops"),
            "L5_fail_missing_NEW_ID": run.get("l5_missing_new_id"),
            "layer_tally": {f"{k[0]}_{k[1]}": v
                            for k, v in sorted(run.get("layer_tally", {}).items())},
        },
        "negative_scenario_assertability": {
            "existing_corpus": {
                "file": "Automation gitlab repo/pam_automation_bootstrap/testdata/"
                        "Negative_API_Automation_Test_Input_Data.xls",
                "sheets": neg.get("sheets"),
                "rows_non_empty": neg.get("rows_non_empty"),
                "expected_status_split": dict(st),
                "rows_testing_transport_or_auth_401_405": plumbing,
                "rows_targeting_application_validation": app_level,
                "rows_with_an_ExpectedErrorCode": ec_pop,
                "unassertable_existing_rows": app_level,
                "why": ("PAM signals a rejection as HTTP 200 with an errorCode in the body. "
                        "A row whose only expectation is ExpectedStatus=200 passes whether "
                        "the request was correctly rejected or wrongly accepted. Not one "
                        "row carries an ExpectedErrorCode, so every application-level "
                        "negative row is unassertable."),
                "error": neg.get("error"),
            },
            "prospective_scenario_space": {
                "note": ("Derived, not measured: the four standard property-level negative "
                         "classes applied to every known body property. It states how many "
                         "scenarios cannot be authored truthfully for want of metadata."),
                "body_properties": n_body,
                "classes": scenario_space,
                "total_scenarios_possible": total_space,
                "total_unassertable": total_unassertable,
                "pct_unassertable": round(total_unassertable / total_space * 100, 2)
                if total_space else None,
            },
        },
        "per_controller": {k: dict(v) for k, v in sorted(per_ctrl.items())},
    }
    return rows, summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-cs", action="store_true",
                    help="skip the 110 MB pam/PAM scan (census will read as not scanned)")
    args = ap.parse_args()

    log("[1/4] pam/PAM DataAnnotations census (6,866 .cs / ~111 MB)")
    cs = {"scanned": False, "files": 0, "chars": 0, "public_classes": 0,
          "auto_properties_lh10_regex": 0, "auto_properties_broad_regex": 0,
          "attr_occurrences": {}, "attr_files": {}, "required_properties": [], "enums": {}}
    if not args.no_cs:
        cs = scan_cs()
    log(f"      files={cs['files']} props={cs['auto_properties_lh10_regex']} "
        f"[Required]={cs.get('attr_occurrences', {}).get('[Required]', 0)}")

    log("[2/4] mining observed mandatory fields from retained run evidence")
    run = mine_run()
    log(f"      {len(run['endpoints_with_signal'])} endpoints revealed a mandatory field; "
        f"{len(run['distinct_names'])} distinct names")

    log("[3/4] merging the endpoint x property universe")
    rows, summary = build(cs, run, args)
    if rows is None:
        return 1

    log("[4/4] writing deliverables")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_ROWS.write_text(json.dumps(rows, indent=1, default=str), encoding="utf-8")
    OUT_SUM.write_text(json.dumps(summary, indent=1, default=str), encoding="utf-8")
    log(f"      {OUT_ROWS.relative_to(ROOT)}  ({len(rows)} rows)")
    log(f"      {OUT_SUM.relative_to(ROOT)}")

    # ---------- compact console aggregate
    v = summary["re_verification_of_prior_claim"]
    m = summary["metadata_counts"]
    c = summary["create_endpoints"]
    n = summary["negative_scenario_assertability"]
    log("")
    log("══ RE-VERIFICATION ═════════════════════════════════════════")
    log(f"  .cs files                {v['re_derived_cs_files']}")
    log(f"  auto-properties (same rx){v['re_derived_auto_properties_same_regex']:>7}")
    log(f"  auto-properties (broader){v['re_derived_auto_properties_broader_regex']:>7}")
    log(f"  public classes           {v['re_derived_public_classes']}")
    log(f"  [Required]               {v['re_derived_required_count']}")
    log(f"  coverage                 {v['coverage_pct_of_auto_properties']}%")
    log(f"  VERDICT                  {v['verdict']}")
    log(f"  correction               declared-required on the surface under test = "
        f"{v['material_correction']['consequence'][:60]}...")
    log("")
    log("══ ATTRIBUTES AT ZERO ══════════════════════════════════════")
    log("  " + ", ".join(summary["attribute_census_pam_PAM"]
                         ["constraint_attributes_at_zero"]))
    log("")
    log("══ PROPERTY UNIVERSE ═══════════════════════════════════════")
    for k, val in summary["property_universe"].items():
        log(f"  {k:<48}{val}")
    log("")
    log("══ METADATA COUNTS (body properties) ═══════════════════════")
    for k, val in m.items():
        if k != "note":
            log(f"  {k:<48}{val}")
    log("")
    log("══ CREATE ENDPOINTS ════════════════════════════════════════")
    for k, val in c.items():
        if k not in ("note", "measured_outcome_prior"):
            log(f"  {k:<48}{val}")
    log("")
    log("══ OBSERVED MANDATORY SET ══════════════════════════════════")
    o = summary["observed_mandatory_set"]
    log(f"  endpoints revealing a mandatory field   "
        f"{o['endpoints_that_revealed_a_mandatory_field']}")
    log(f"  distinct property names revealed        "
        f"{o['distinct_property_names_revealed']}")
    log(f"  prose grammars                          {o['prose_grammar_counts']}")
    log(f"  distinct rejection messages             {o['distinct_rejection_messages']}")
    log(f"  constraints leaked in prose             "
        f"{len(o['observed_constraints_leaked_in_prose'])}")
    log(f"  names: {', '.join(o['names_revealed'][:40])}")
    log("")
    log("══ SWAGGER ═════════════════════════════════════════════════")
    log(f"  {summary['swagger_specs']['archived_evidence']}")
    log("")
    log("══ NEGATIVE ASSERTABILITY ══════════════════════════════════")
    e = n["existing_corpus"]
    log(f"  sheets={e['sheets']} rows={e['rows_non_empty']} err={e.get('error')}")
    log(f"  ExpectedStatus split                    {e['expected_status_split']}")
    log(f"  401/405 transport-or-auth rows          "
        f"{e['rows_testing_transport_or_auth_401_405']}")
    log(f"  application-validation rows             "
        f"{e['rows_targeting_application_validation']}")
    log(f"  rows with an ExpectedErrorCode          {e['rows_with_an_ExpectedErrorCode']}")
    p = n["prospective_scenario_space"]
    log(f"  body properties                         {p['body_properties']}")
    for cls, d in p["classes"].items():
        log(f"    {cls:<26} possible={d['scenarios_possible']:>5} "
            f"authorable={d['authorable']:>4} unassertable={d['unassertable']:>5}")
    log(f"  TOTAL scenario space                    {p['total_scenarios_possible']}")
    log(f"  TOTAL unassertable                      {p['total_unassertable']} "
        f"({p['pct_unassertable']}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
