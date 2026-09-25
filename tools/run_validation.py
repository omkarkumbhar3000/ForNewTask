#!/usr/bin/env python3
"""
PAM API Dynamic Validation Harness  -  Phase 1: GET request type, end to end.

WHAT THIS DOES, in one command:
  1. DISCOVER   parse the developer-shared Swagger link sheet, fetch every reachable
                swagger.json, and enumerate every operation. No hand-written endpoint list.
  2. GENERATE   select the Phase-1 slice (GET, zero required parameters) and build one
                validation case per operation from the spec alone. No per-endpoint code.
  3. EXECUTE    call each endpoint and capture status, latency, content-type and body.
  4. VALIDATE   seven layers, not just the status code (see LAYERS below).
  5. REPORT     Excel workbook + coverage metrics + JSON evidence + executive summary.

RETAINED BY DESIGN: every run writes into its own dated folder under artifacts/runs/, and
nothing is ever deleted or overwritten. Runs can therefore be compared against each other.

USAGE
  python tools/run_validation.py                    # full run
  python tools/run_validation.py --dry-run          # plan only, no HTTP calls
  python tools/run_validation.py --verb GET --limit 25
  python tools/run_validation.py --promote-baseline # accept this run as known-good

VALIDATION LAYERS
  L1 http-status        actual status vs the codes the spec declares
  L2 envelope           body StatusCode / Message consistency with the HTTP status
  L3 schema             JSON Schema conformance against the spec's response schema
  L4 required-fields    every schema-required property present and non-null
  L5 types              each present property matches its declared type
  L6 content-type       JSON declared => JSON returned (catches HTML/plaintext errors)
  L7 latency           within the configured SLA budget
  DIFF differential     compared against the approved baseline, when one exists

Exit code 0 always; verdicts live in the report. Never fails a pipeline by accident.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import ssl
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

# ---------------------------------------------------------------- configuration
HERE = Path(__file__).resolve().parent


def _workspace_root(start: Path) -> Path:
    """Find the folder holding both Reports/ and the automation repo.

    Resolved by search rather than a fixed number of parent hops, so these scripts keep
    working from wherever they are stored. They live in tools/ now.
    """
    for p in [start, *start.parents]:
        if (p / "CLAUDE.md").is_file() and (p / ".claude").is_dir():
            return p
    raise SystemExit(f"cannot locate the workspace root above {start}")


ROOT = _workspace_root(HERE)
REPORTS = ROOT / "artifacts"   # OBJ-025: runs live at artifacts/runs

LINK_SHEET = (ROOT / "data" / "sources"
              / "Automation PAM Endpoints Details_Shared(Swagger_JSON Links).csv")

# Every run gets its own dated folder. Nothing is ever overwritten or deleted.
RUN_STAMP = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d_%H%M%S")
RUN_DIR = REPORTS / "Runs" / f"{RUN_STAMP}_swagger"
RUN_REL = f"artifacts/runs/{RUN_STAMP}_swagger"

SPEC_CACHE = REPORTS / "SpecCache"         # shared cache, not per-run output
EVIDENCE = RUN_DIR / "evidence"
BASELINE = HERE / "baseline.json"          # kept beside the script, never under output

LATENCY_SLA_MS = 2000
HTTP_TIMEOUT = 20

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE        # internal hosts use self-signed certs

VERBS = {"get", "post", "put", "patch", "delete", "head", "options"}


def log(msg: str = "") -> None:
    print(msg, flush=True)


# ------------------------------------------------------------------ 0. cleaning
def regenerate_dirs() -> None:
    """Ensure this run's output folders exist.

    Prior report data is RETAINED. Each run writes into its own dated folder under
    artifacts/runs/, so nothing needs deleting and no earlier run can be overwritten.
    """
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    SPEC_CACHE.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------- 1. discovery
def read_link_sheet() -> list[dict]:
    rows = []
    with LINK_SHEET.open(encoding="utf-8-sig", errors="replace", newline="") as fh:
        for r in csv.reader(fh):
            if len(r) < 6 or not r[0].strip().isdigit():
                continue
            rows.append({
                "sr": r[0].strip(), "module": r[1].strip(), "swagger": r[2].strip(),
                "json": r[3].strip(), "status": r[4].strip(), "comment": r[5].strip(),
            })
    return rows


def normalise(url: str) -> str:
    url = url.strip()
    if url and not url.startswith("http"):
        url = "https://" + url          # several sheet rows omit the scheme
    return url


def fetch_specs(rows: list[dict], offline: bool = False) -> tuple[dict, dict, dict]:
    """Return (specs, failures, sheet_quality).

    ⛔ SAFETY (OBJ-013): `offline=True` guarantees ZERO network calls — specs are
    read from SPEC_CACHE only. This is what makes `--dry-run` honest. Previously
    this function was called unconditionally, BEFORE the dry-run branch, so
    `--dry-run` still opened sockets to every distinct spec URL across four live
    hosts, contradicting the deny-by-default invariant that root CLAUDE.md and
    .claude/rules/api-surface.md both assert for every harness script.
    """
    seen: dict[str, list[dict]] = {}
    malformed = []
    for r in rows:
        raw = r["json"]
        u = normalise(raw)
        if not u.endswith(".json"):
            continue
        if raw and not raw.startswith("http"):
            malformed.append(raw)
        seen.setdefault(u, []).append(r)

    specs, failures = {}, {}
    for u in sorted(seen):
        name = re.sub(r"[^A-Za-z0-9]+", "_", u)[-90:]
        cached = SPEC_CACHE / f"{name}.json"
        if offline:
            if cached.exists():
                try:
                    specs[u] = json.loads(cached.read_bytes().decode("utf-8", "replace"))
                except Exception as exc:                             # noqa: BLE001
                    failures[u] = f"cache unreadable: {type(exc).__name__}: {exc}"
            else:
                failures[u] = "not cached (offline: no request made)"
            continue
        try:
            with urllib.request.urlopen(u, timeout=HTTP_TIMEOUT, context=SSL_CTX) as resp:
                raw = resp.read()
            specs[u] = json.loads(raw.decode("utf-8", "replace"))
            cached.write_bytes(raw)
        except Exception as exc:                                     # noqa: BLE001
            failures[u] = f"{type(exc).__name__}: {exc}"

    quality = {
        "sheet_rows": len(rows),
        "extraction_status": dict(Counter(r["status"] or "(blank)" for r in rows)),
        "distinct_json_urls": len(seen),
        "rows_missing_scheme": len(malformed),
        "rows_marked_duplicate": sum(1 for r in rows if r["status"].lower() == "duplicate"),
        "rows_marked_unavailable": sum(1 for r in rows if r["status"].lower() == "unavailable"),
        "specs_fetched": len(specs),
        "specs_failed": failures,
    }
    return specs, failures, quality


def base_url_of(spec_url: str) -> str | None:
    m = re.match(r"(https?://[^/]+(?:/[^/]+)*?)/swagger/", spec_url)
    return m.group(1) if m else None


def enumerate_operations(specs: dict) -> list[dict]:
    ops = []
    for spec_url, spec in specs.items():
        info = spec.get("info") or {}
        base = base_url_of(spec_url)
        for path, item in (spec.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            shared = item.get("parameters") or []
            for verb, op in item.items():
                if verb.lower() not in VERBS or not isinstance(op, dict):
                    continue
                params = (op.get("parameters") or []) + shared
                required_params = [p for p in params
                                   if isinstance(p, dict) and p.get("required")]
                ops.append({
                    "spec_url": spec_url,
                    "spec_title": info.get("title", "?"),
                    "spec_version": info.get("version", "?"),
                    "base_url": base,
                    "path": path,
                    "verb": verb.upper(),
                    "declared_codes": sorted((op.get("responses") or {}).keys()),
                    "n_params": len(params),
                    "n_required_params": len(required_params),
                    "has_request_body": bool(op.get("requestBody")),
                    "operation_id": op.get("operationId") or "",
                    "tags": op.get("tags") or [],
                    "summary": op.get("summary") or "",
                    "_spec": spec,
                    "_op": op,
                })
    return ops


# ---------------------------------------------------------------- 2. generation
def select_slice(ops: list[dict], verb: str, limit: int | None,
                 tier: str = "strict") -> list[dict]:
    """Phase 1 slice.

    tier="strict"   zero parameters of any kind - the approved Phase 1 scope.
    tier="extended" also allows operations whose parameters are all optional.
                    These need no seed data either, so they are the natural next tier.
    """
    def eligible(o):
        if o["verb"] != verb.upper() or o["has_request_body"] or not o["base_url"]:
            return False
        return o["n_params"] == 0 if tier == "strict" else o["n_required_params"] == 0

    sel = [o for o in ops if eligible(o)]
    sel.sort(key=lambda o: (o["spec_title"], o["path"]))
    return sel[:limit] if limit else sel


def response_schema_for(op: dict) -> dict | None:
    for code in ("200", "201", "2XX", "default"):
        r = (op.get("responses") or {}).get(code)
        if not isinstance(r, dict):
            continue
        content = r.get("content") or {}
        for ctype, media in content.items():
            if "json" in ctype and isinstance(media, dict) and media.get("schema"):
                return media["schema"]
        if r.get("schema"):
            return r["schema"]
    return None


# ----------------------------------------------------------------- 3. execution
def execute(case: dict) -> dict:
    url = case["base_url"].rstrip("/") + case["path"]
    started = time.time()
    out = {"url": url, "error": None}
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "PAM-Validation-Harness/1.0",
        }, method=case["verb"])
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT, context=SSL_CTX) as resp:
            body = resp.read()
            out.update(status=resp.status,
                       content_type=(resp.headers.get("Content-Type") or "").split(";")[0].strip(),
                       body=body[:200_000])
    except urllib.error.HTTPError as exc:
        body = b""
        try:
            body = exc.read()
        except Exception:                                            # noqa: BLE001
            pass
        ctype = ""
        if exc.headers is not None:
            ctype = exc.headers.get("Content-Type") or ""
        out.update(status=exc.code,
                   content_type=ctype.split(";")[0].strip(),
                   body=body[:200_000])
    except Exception as exc:                                         # noqa: BLE001
        out.update(status=None, content_type="", body=b"", error=f"{type(exc).__name__}: {exc}")
    out["latency_ms"] = int((time.time() - started) * 1000)
    return out


# ---------------------------------------------------------------- 4. validation
def validate(case: dict, res: dict) -> dict:
    """Run the seven layers. Each returns PASS / FAIL / NA plus a note."""
    layers: dict[str, dict] = {}
    body_raw = res.get("body") or b""
    parsed, parse_err = None, None
    if body_raw:
        try:
            parsed = json.loads(body_raw.decode("utf-8", "replace"))
        except Exception as exc:                                     # noqa: BLE001
            parse_err = str(exc)[:120]

    def put(name, verdict, note=""):
        layers[name] = {"verdict": verdict, "note": note}

    # -- L1 http status vs declared -----------------------------------------
    declared = [c for c in case["declared_codes"] if c.isdigit()]
    actual = res.get("status")
    if res.get("error"):
        put("L1_http_status", "FAIL", f"transport error: {res['error'][:80]}")
    elif not declared:
        put("L1_http_status", "NA", "spec declares no numeric status code")
    elif actual is not None and str(actual) in declared:
        put("L1_http_status", "PASS", f"{actual} is declared")
    else:
        put("L1_http_status", "FAIL",
            f"got {actual}; spec declares only {','.join(declared)}")

    # -- L2 envelope consistency -------------------------------------------
    if isinstance(parsed, dict):
        env_code = parsed.get("StatusCode", parsed.get("statusCode"))
        env_msg = parsed.get("Message", parsed.get("message"))
        err_code = parsed.get("errorCode", parsed.get("ErrorCode"))
        notes = []
        bad = False
        if env_code is not None and actual is not None and str(env_code) != str(actual):
            notes.append(f"body StatusCode={env_code} != HTTP {actual}")
            bad = True
        if (env_code is not None and str(env_code) not in ("200", "201", "202", "204")
                and isinstance(env_msg, str) and env_msg.strip().lower() == "success"):
            notes.append(f'StatusCode={env_code} but Message="{env_msg}"')
            bad = True
        if err_code not in (None, "", "null"):
            notes.append(f"errorCode={err_code}")
            bad = True
        if not notes:
            notes.append("envelope consistent" if env_code is not None else "no envelope fields")
        put("L2_envelope", "FAIL" if bad else "PASS", "; ".join(notes))
    elif parse_err:
        put("L2_envelope", "FAIL", f"body is not JSON: {parse_err}")
    else:
        put("L2_envelope", "NA", "no body")

    # -- L3 schema conformance ---------------------------------------------
    schema = case.get("response_schema")
    if schema is None:
        put("L3_schema", "NA", "spec declares no response schema")
    elif parsed is None:
        put("L3_schema", "FAIL", "no parseable JSON body to validate")
    else:
        try:
            from jsonschema import Draft7Validator
            doc = dict(schema)
            comps = (case["_spec"].get("components") or {})
            if comps:
                doc["components"] = comps
            if case["_spec"].get("definitions"):
                doc["definitions"] = case["_spec"]["definitions"]
            errs = sorted(Draft7Validator(doc).iter_errors(parsed),
                          key=lambda e: list(e.path))
            if errs:
                first = errs[0]
                loc = "/".join(str(p) for p in first.path) or "(root)"
                put("L3_schema", "FAIL",
                    f"{len(errs)} violation(s); first at {loc}: {first.message[:90]}")
            else:
                put("L3_schema", "PASS", "conforms")
        except Exception as exc:                                     # noqa: BLE001
            put("L3_schema", "NA", f"validator unavailable: {type(exc).__name__}")

    # -- L4 required fields -------------------------------------------------
    req = (schema or {}).get("required") if isinstance(schema, dict) else None
    if not req:
        put("L4_required_fields", "NA", "schema declares no required properties")
    elif not isinstance(parsed, dict):
        put("L4_required_fields", "FAIL", "body is not a JSON object")
    else:
        missing = [k for k in req if k not in parsed]
        nulls = [k for k in req if k in parsed and parsed[k] is None]
        if missing or nulls:
            put("L4_required_fields", "FAIL",
                f"missing={missing or '-'} null={nulls or '-'}")
        else:
            put("L4_required_fields", "PASS", f"all {len(req)} present")

    # -- L5 declared types --------------------------------------------------
    props = (schema or {}).get("properties") if isinstance(schema, dict) else None
    if not props or not isinstance(parsed, dict):
        put("L5_types", "NA", "no typed properties to check")
    else:
        jsmap = {"string": str, "integer": int, "number": (int, float),
                 "boolean": bool, "array": list, "object": dict}
        bad = []
        for key, spec_prop in props.items():
            if key not in parsed or parsed[key] is None:
                continue
            want = spec_prop.get("type") if isinstance(spec_prop, dict) else None
            py = jsmap.get(want) if isinstance(want, str) else None
            if py and not isinstance(parsed[key], py):
                bad.append(f"{key}: want {want}, got {type(parsed[key]).__name__}")
        put("L5_types", "FAIL" if bad else "PASS",
            "; ".join(bad[:3]) if bad else f"{len(props)} propert(y/ies) checked")

    # -- L6 content type ----------------------------------------------------
    ct = (res.get("content_type") or "").lower()
    if not ct:
        put("L6_content_type", "FAIL" if body_raw else "NA", "no Content-Type header")
    elif "json" in ct:
        put("L6_content_type", "PASS", ct)
    else:
        put("L6_content_type", "FAIL", f"expected JSON, got {ct}")

    # -- L7 latency ---------------------------------------------------------
    ms = res.get("latency_ms", 0)
    put("L7_latency", "PASS" if ms <= LATENCY_SLA_MS else "FAIL",
        f"{ms} ms (SLA {LATENCY_SLA_MS} ms)")

    fails = [k for k, v in layers.items() if v["verdict"] == "FAIL"]
    passes = [k for k, v in layers.items() if v["verdict"] == "PASS"]
    verdict = "PASS" if not fails else ("FAIL" if len(fails) > 1 or "L1_http_status" in fails
                                        else "WARN")
    return {"layers": layers, "fail_layers": fails,
            "n_pass": len(passes), "n_fail": len(fails), "verdict": verdict}


def shape_of(parsed, prefix="") -> list[str]:
    """Structural fingerprint - key paths and types, values discarded."""
    out = []
    if isinstance(parsed, dict):
        for k in sorted(parsed):
            out += shape_of(parsed[k], f"{prefix}.{k}" if prefix else k)
    elif isinstance(parsed, list):
        out += shape_of(parsed[0], f"{prefix}[]") if parsed else [f"{prefix}[]:empty"]
    else:
        out.append(f"{prefix}:{type(parsed).__name__}")
    return out


# -------------------------------------------------------------------- 5. report
def write_excel(rows: list[dict], coverage: dict, quality: dict, meta: dict) -> Path:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    HEAD = PatternFill("solid", fgColor="1F3864")
    HEADF = Font(bold=True, color="FFFFFF", size=10)
    GOOD = PatternFill("solid", fgColor="C6EFCE")
    BAD = PatternFill("solid", fgColor="FFC7CE")
    WARN = PatternFill("solid", fgColor="FFEB9C")
    NA = PatternFill("solid", fgColor="EDEDED")

    def style_header(ws, ncols):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=1, column=c)
            cell.fill, cell.font = HEAD, HEADF
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        ws.freeze_panes = "A2"

    def autosize(ws, maxw=52):
        for col in ws.columns:
            letter = get_column_letter(col[0].column)
            width = max((len(str(c.value)) for c in col if c.value is not None), default=8)
            ws.column_dimensions[letter].width = min(max(width + 2, 9), maxw)

    wb = Workbook()

    # ---- Summary ----------------------------------------------------------
    ws = wb.active
    assert ws is not None, "a new Workbook always has an active sheet"
    ws.title = "Summary"
    ws.append(["PAM API Dynamic Validation - Executive Summary"])
    ws["A1"].font = Font(bold=True, size=14)
    ws.append([])
    for k, v in meta.items():
        ws.append([k, v])
    ws.append([])
    ws.append(["RESULT COUNTS"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    vd = Counter(r["verdict"] for r in rows)
    for k in ("PASS", "WARN", "FAIL"):
        ws.append([k, vd.get(k, 0), f"{vd.get(k,0)/max(len(rows),1)*100:.1f}%"])
    ws.append([])
    ws.append(["PER-LAYER FAILURES", "count", "% of executed"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    lf = Counter()
    for r in rows:
        for L in r["fail_layers"]:
            lf[L] += 1
    for L in sorted(set(k for r in rows for k in r["layers"])):
        ws.append([L, lf.get(L, 0), f"{lf.get(L,0)/max(len(rows),1)*100:.1f}%"])
    autosize(ws)

    # ---- Results ----------------------------------------------------------
    ws = wb.create_sheet("Results")
    layer_names = sorted({k for r in rows for k in r["layers"]})
    cols = (["#", "Spec", "Module/Tag", "Verb", "Path", "HTTP", "Declared", "Latency ms",
             "Content-Type", "Verdict"] + layer_names + ["Fail detail", "Shape hash"])
    ws.append(cols)
    for i, r in enumerate(rows, 1):
        detail = " | ".join(f"{L}: {r['layers'][L]['note']}" for L in r["fail_layers"])
        ws.append([i, r["spec_title"][:38], ",".join(r["tags"])[:28], r["verb"], r["path"],
                   r["status"], ",".join(r["declared_codes"]), r["latency_ms"],
                   r["content_type"], r["verdict"]]
                  + [r["layers"].get(L, {}).get("verdict", "") for L in layer_names]
                  + [detail[:300], r["shape_hash"]])
        row = ws.max_row
        vcell = ws.cell(row=row, column=10)
        vcell.fill = {"PASS": GOOD, "WARN": WARN, "FAIL": BAD}.get(r["verdict"], NA)
        vcell.font = Font(bold=True)
        for j, L in enumerate(layer_names):
            c = ws.cell(row=row, column=11 + j)
            c.fill = {"PASS": GOOD, "FAIL": BAD, "NA": NA}.get(c.value, NA)
    style_header(ws, len(cols))
    autosize(ws)

    # ---- Coverage ---------------------------------------------------------
    ws = wb.create_sheet("Coverage")
    ws.append(["API COVERAGE BY REQUEST TYPE"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Surface", "Verb", "Documented", "Executed this run", "Coverage %"])
    style_header(ws, 5)
    for surface, per_verb in coverage["by_surface_verb"].items():
        for verb, d in sorted(per_verb.items()):
            ws.append([surface, verb, d["documented"], d["executed"],
                       f"{d['executed']/d['documented']*100:.1f}%" if d["documented"] else "-"])
    ws.append([])
    ws.append(["SURFACE TOTALS"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    ws.append(["Surface", "Endpoints", "Note"])
    for s, d in coverage["surfaces"].items():
        ws.append([s, d["count"], d["note"]])
    autosize(ws)

    # ---- Spec quality -----------------------------------------------------
    ws = wb.create_sheet("Spec Quality")
    ws.append(["DEVELOPER-SUPPLIED SPEC QUALITY"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Metric", "Value"])
    style_header(ws, 2)
    for k, v in quality.items():
        if k == "specs_failed":
            ws.append(["specs_failed", len(v)])
            for u, e in v.items():
                ws.append(["  " + u[:70], e[:70]])
        else:
            ws.append([k, json.dumps(v) if isinstance(v, (dict, list)) else v])
    autosize(ws)

    # ---- Excluded ---------------------------------------------------------
    ws = wb.create_sheet("Excluded")
    ws.append(["Endpoints NOT executed this run, with reason"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Verb", "Path", "Spec", "Reason"])
    style_header(ws, 4)
    for e in coverage["excluded"]:
        ws.append([e["verb"], e["path"], e["spec_title"][:38], e["reason"]])
    autosize(ws)

    out = RUN_DIR / "PAM_API_Validation_Results.xlsx"
    wb.save(out)
    return out


# ----------------------------------------------------------------------- driver
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verb", default="GET")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--tier", choices=["strict", "extended"], default="strict",
                    help="strict = zero parameters (approved Phase 1 scope); "
                         "extended = also operations whose parameters are all optional")
    # OBJ-013: deny-by-default. `--dry-run` alone was opt-out, and worse, it did not
    # even suppress network access — fetch_specs() ran before the dry-run branch and
    # opened sockets to every distinct spec URL across four live hosts. Both halves
    # are fixed: fetch_specs takes offline=, and HTTP now requires --execute.
    ap.add_argument("--execute", action="store_true",
                    help="REQUIRED to issue any HTTP request (spec fetch or validation "
                         "call). Without it the run plans from cached specs only and "
                         "contacts nothing.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Explicit plan-only. Now the default; retained for "
                         "compatibility with existing invocations and docs.")
    ap.add_argument("--promote-baseline", action="store_true")
    args = ap.parse_args()

    # OBJ-013 deny-by-default gate. Collapsing --execute into the existing dry-run
    # flag makes every downstream branch honour it without touching any of them,
    # which keeps the change small and auditable.
    if not args.execute:
        args.dry_run = True

    started = datetime.now(timezone.utc)
    log("=" * 78)
    log("PAM API DYNAMIC VALIDATION HARNESS   Phase 1 - request type: " + args.verb)
    log("=" * 78)
    if not args.execute:
        log("PLAN ONLY - zero HTTP requests will be issued. Pass --execute to run live.")

    if not args.dry_run:
        log("\n[0/5] Preparing this run's output folder (prior runs retained)")
        regenerate_dirs()
        log(f"      created  {RUN_REL}/  + evidence/")
    else:
        SPEC_CACHE.mkdir(parents=True, exist_ok=True)

    log("\n[1/5] DISCOVER - parsing developer link sheet and fetching specs"
        + ("  (OFFLINE: cache only, zero HTTP)" if args.dry_run else ""))
    rows = read_link_sheet()
    specs, failures, quality = fetch_specs(rows, offline=args.dry_run)
    log(f"      sheet rows {quality['sheet_rows']}  distinct spec URLs {quality['distinct_json_urls']}"
        f"  fetched {len(specs)}  failed {len(failures)}")
    ops = enumerate_operations(specs)
    log(f"      operations discovered: {len(ops)} across {len(specs)} specs")
    vd = Counter(o["verb"] for o in ops)
    log(f"      verb mix: " + "  ".join(f"{k}={v}" for k, v in vd.most_common()))

    log(f"\n[2/5] GENERATE - selecting the {args.verb} slice, tier={args.tier}")
    cases = select_slice(ops, args.verb, args.limit, args.tier)
    for c in cases:
        c["response_schema"] = response_schema_for(c["_op"])
    with_schema = sum(1 for c in cases if c["response_schema"])
    log(f"      cases generated: {len(cases)}   ({with_schema} carry a response schema)")
    if args.tier == "strict":
        nxt = len(select_slice(ops, args.verb, None, "extended")) - len(cases)
        log(f"      next tier available without seed data: +{nxt} "
            f"{args.verb} operations with optional-only parameters (--tier extended)")

    selected = {id(c) for c in cases}
    excluded = []
    for o in ops:
        if id(o) in selected:
            continue
        if o["verb"] != args.verb.upper():
            reason = f"verb {o['verb']} - out of Phase 1 scope"
        elif o["has_request_body"]:
            reason = "requires a request body"
        elif not o["base_url"]:
            reason = "base URL not derivable from spec URL"
        elif o["n_required_params"]:
            reason = f"{o['n_required_params']} required parameter(s) - needs seed data"
        elif o["n_params"]:
            reason = (f"{o['n_params']} optional parameter(s) - available now via "
                      f"--tier extended")
        else:
            reason = "not selected"
        excluded.append({"verb": o["verb"], "path": o["path"],
                         "spec_title": o["spec_title"], "reason": reason})

    if args.dry_run:
        log("\n[DRY RUN] plan only - no HTTP calls will be made\n")
        for c in cases[:40]:
            log(f"      {c['verb']:<5} {c['path'][:66]:<66} schema={'Y' if c['response_schema'] else 'N'}")
        if len(cases) > 40:
            log(f"      ... and {len(cases)-40} more")
        log(f"\n      would execute {len(cases)}; would exclude {len(excluded)}")
        log("      exclusion reasons: "
            + json.dumps(dict(Counter(e['reason'] for e in excluded)), indent=8))
        return 0

    log(f"\n[3/5] EXECUTE + [4/5] VALIDATE - {len(cases)} calls, 7 layers each")
    baseline = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    results, new_baseline = [], {}
    for i, c in enumerate(cases, 1):
        res = execute(c)
        val = validate(c, res)
        parsed = None
        try:
            parsed = json.loads((res.get("body") or b"").decode("utf-8", "replace"))
        except Exception:                                            # noqa: BLE001
            pass
        shape = shape_of(parsed) if parsed is not None else []
        import hashlib
        shash = hashlib.sha256("|".join(shape).encode()).hexdigest()[:12] if shape else ""
        key = f"{c['verb']} {c['base_url']}{c['path']}"
        drift = "NO BASELINE"
        if key in baseline:
            b = baseline[key]
            if b.get("shape_hash") != shash:
                drift = "CHANGED"
            elif str(b.get("status")) != str(res.get("status")):
                drift = "STATUS CHANGED"
            else:
                drift = "STABLE"
        new_baseline[key] = {"status": res.get("status"), "shape_hash": shash,
                             "latency_ms": res.get("latency_ms")}

        row = {**{k: v for k, v in c.items() if not k.startswith("_")},
               "status": res.get("status"), "latency_ms": res.get("latency_ms"),
               "content_type": res.get("content_type"), "error": res.get("error"),
               "shape_hash": shash, "drift": drift, **val}
        results.append(row)

        ev = {"request": {"verb": c["verb"], "url": res["url"]},
              "response": {"status": res.get("status"),
                           "content_type": res.get("content_type"),
                           "latency_ms": res.get("latency_ms"),
                           "body_preview": (res.get("body") or b"")[:1500].decode("utf-8", "replace")},
              "declared_codes": c["declared_codes"],
              "validation": val, "drift": drift}
        safe = re.sub(r"[^A-Za-z0-9]+", "_", f"{c['verb']}_{c['path']}").strip("_")[:110]
        (EVIDENCE / f"{i:03d}_{safe}.json").write_text(
            json.dumps(ev, indent=2), encoding="utf-8")

        if i % 10 == 0 or i == len(cases):
            log(f"      {i:>3}/{len(cases)}  last: {row['verdict']:<5} {c['path'][:52]}")

    if args.promote_baseline or not BASELINE.exists():
        BASELINE.write_text(json.dumps(new_baseline, indent=1), encoding="utf-8")
        log(f"      baseline {'promoted' if args.promote_baseline else 'initialised'}"
            f" ({len(new_baseline)} endpoints) -> {BASELINE.name}")

    log("\n[5/5] REPORT")
    lat = [r["latency_ms"] for r in results if r["latency_ms"]]
    meta = {
        "Generated (UTC)": started.strftime("%Y-%m-%d %H:%M:%S"),
        "Harness": "tools/run_validation.py",
        "Phase": f"1 - request type {args.verb}, zero required inputs",
        "Specs fetched": len(specs),
        "Operations discovered": len(ops),
        "Cases generated": len(cases),
        "Cases executed": len(results),
        "Endpoints excluded": len(excluded),
        "Median latency ms": int(statistics.median(lat)) if lat else 0,
        "Max latency ms": max(lat) if lat else 0,
        "Validation layers": 7,
    }

    by_sv: dict[str, dict] = defaultdict(dict)
    doc_by_verb = Counter(o["verb"] for o in ops)
    exec_by_verb = Counter(r["verb"] for r in results)
    for v, n in doc_by_verb.items():
        by_sv["Swagger microservices (live)"][v] = {
            "documented": n, "executed": exec_by_verb.get(v, 0)}
    coverage = {
        "by_surface_verb": dict(by_sv),
        "surfaces": {
            "Swagger microservices (live, documented)": {
                "count": len(ops),
                "note": f"{len(specs)} specs fetched from the developer-shared sheet"},
            "Legacy /api/<Controller>/<Action> (APIConfig.java)": {
                "count": 1322,
                "note": "No Swagger. Declared in the automation repo; ~6% name overlap with the above"},
        },
        "excluded": excluded,
    }

    xlsx = write_excel(results, coverage, quality, meta)
    log(f"      Excel     -> {xlsx.relative_to(ROOT)}")

    slim = [{k: v for k, v in r.items() if k not in ("_spec", "_op", "response_schema")}
            for r in results]
    (RUN_DIR / "results.json").write_text(
        json.dumps({"meta": meta, "results": slim}, indent=1, default=str), encoding="utf-8")
    (RUN_DIR / "coverage.json").write_text(
        json.dumps(coverage, indent=1), encoding="utf-8")
    (RUN_DIR / "spec_quality.json").write_text(
        json.dumps(quality, indent=1), encoding="utf-8")
    log(f"      JSON      -> artifacts/runs/<stamp>/results.json")
    log(f"      Evidence  -> docs/findings/issues/Evidence/  ({len(results)} files)")

    vdc = Counter(r["verdict"] for r in results)
    lf = Counter(L for r in results for L in r["fail_layers"])
    log("\n" + "=" * 78)
    log(f"VERDICTS   PASS {vdc.get('PASS',0)}   WARN {vdc.get('WARN',0)}   FAIL {vdc.get('FAIL',0)}"
        f"   (of {len(results)})")
    log("LAYER FAILURES  " + "  ".join(f"{k}={v}" for k, v in sorted(lf.items())))
    log("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
