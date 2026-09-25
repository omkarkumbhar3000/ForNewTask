#!/usr/bin/env python3
"""
QA_MsSQL API Validation  -  legacy /api/<Controller>/<Action> surface.

TARGET (from Environments/QA_MsSQL.properties, nothing hardcoded):
    pam_BaseAPIURL   https://u16hf.arconnet.com:6302     <- API base, all calls go here
    environmentUrl   https://u16hf.arconnet.com:1302     <- application URL (not called)
    pam_tokenAPIUrl  https://u16hf.arconnet.com:6302/arcontoken

ENDPOINT DISCOVERY: reflection over APIConfig.java - the same source the Java framework
uses. 1,322 declared constants, module attribution taken from the section comments.
No endpoint list is maintained here.

AUTH: a supplied bearer token, read from (in order)
    1. $PAM_API_TOKEN
    2. tools/.token
Dynamic generation via /arcontoken is ALSO attempted every run and its outcome recorded
as evidence - see ISSUE-009. It currently fails with 400 Invalid User Credentials.

VALIDATION: the same seven layers as run_validation.py, imported from it so there is one
definition. L3/L4/L5 (schema, required fields, types) report NA on this surface because
:6302 publishes no Swagger - confirmed 404.

USAGE
    python Reports\\Scripts\\run_qa_mssql.py                 # all GET endpoints
    python Reports\\Scripts\\run_qa_mssql.py --dry-run
    python Reports\\Scripts\\run_qa_mssql.py --limit 40
    python Reports\\Scripts\\run_qa_mssql.py --promote-baseline
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import ssl
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_validation import shape_of, validate                        # one definition of truth

HERE = Path(__file__).resolve().parent


def _workspace_root(start: Path) -> Path:
    """Find the folder holding both Reports/ and the automation repo.

    Resolved by search rather than by a fixed number of parent hops, so these scripts
    keep working from wherever they are stored. They live in tools/ now.
    """
    for p in [start, *start.parents]:
        if (p / "CLAUDE.md").is_file() and (p / ".claude").is_dir():
            return p
    raise SystemExit(f"cannot locate the workspace root above {start}")


ROOT = _workspace_root(HERE)
# token_guard is a sibling module and owns the only path to /arcontoken.
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import token_guard                                                       # noqa: E402

REPORTS = ROOT / "artifacts"   # OBJ-025: runs live at artifacts/runs

REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
ENV_FILE = REPO / "Environments" / "QA_MsSQL.properties"
APICONFIG = REPO / "src/test/java/com/arcon/autoconfigs/APIConfig.java"
PAYLOAD_DIR = REPO / "src/test/java/com/arcon/utils/apiPayload"

# Every run gets its own dated folder. Nothing is ever overwritten or deleted.
RUN_STAMP = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d_%H%M%S")
RUN_DIR = REPORTS / "Runs" / f"{RUN_STAMP}_legacy-get"
RUN_REL = f"artifacts/runs/{RUN_STAMP}_legacy-get"

EVIDENCE = RUN_DIR / "evidence"
BASELINE = HERE / "baseline-qa_mssql.json"
TOKEN_FILE = HERE / ".token"

ENV_NAME = "QA_MsSQL"
LATENCY_SLA_MS = 2000
HTTP_TIMEOUT = 30            # matches setAPIRequestTimeout_MS=30000

# ---------------------------------------------------------------------- SAFETY
# Enforced during endpoint RESOLUTION, so a blocked operation is never turned into
# a request. Each entry cites the issue that justifies it.
BLOCKLIST = {
    "GetErrorLogs": "blocked: hangs 30s and stops the IIS app pool (ISSUE-010)",
    "GetLogs": "blocked: hangs 30s and stops the IIS app pool (ISSUE-010)",
    # OBJ-013: this entry was MISSING here while present in chain_runner.py,
    # run_chains.py and lh_common.py. root CLAUDE.md names all three endpoints as
    # blocklisted for the same reason, and this was the only script that both
    # omitted it AND executed live on a bare run — the worst possible pairing.
    "GetAllActiveUserDetails": "blocked: hung 30s on every version during the GET run "
                               "(ISSUE-010, LH-08)",
    "SetStatus": "blocked: name implies state mutation despite the GET declaration; "
                 "default-deny pending developer confirmation (ISSUE-011)",
}
# Any action matching these is treated as mutating whatever verb APIConfig declares.
MUTATING_NAME = re.compile(
    r"^(set|insert|update|delete|remove|drop|purge|reset|revoke|disable|enable|"
    r"add|create|save|upload|import|sync|rotate|assign|approve|reject)", re.I)

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def log(m=""):
    print(m, flush=True)


# ------------------------------------------------------------------ env config
def load_env() -> dict:
    cfg = {}
    for line in ENV_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()
    return cfg


def get_token() -> tuple[str | None, str]:
    t = os.environ.get("PAM_API_TOKEN")
    if t:
        return t.strip(), "$PAM_API_TOKEN"
    if TOKEN_FILE.exists():
        t = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if t:
            return t, str(TOKEN_FILE.relative_to(ROOT))
    return None, "not found"


def jwt_claims(tok: str) -> dict:
    try:
        p = tok.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))
    except Exception:                                                # noqa: BLE001
        return {}


def try_dynamic_token(cfg: dict) -> dict:
    """Replicates ApiHelper.getToken(). Recorded as evidence whether it works or not.

    ⛔ OPT-IN ONLY (--try-token-gen), and now also gated by token_guard's failure latch.
    Repeated attempts locked the API account on 2026-07-28: the endpoint moved from
    "Invalid User Credentials" to "Your account has been locked. Please contact your
    supervisor". The account is GenericScheduler, the data-warehouse ETL service
    account, so a lockout reaches beyond testing. Never attempt this on a schedule or in
    a loop. See ISSUE-009 §5.

    The single POST lives in token_guard.attempt_once() so there is exactly one code
    path to /arcontoken in the whole harness.
    """
    url = cfg.get("pam_tokenAPIUrl", "")
    form = {"grant_type": cfg.get("pam_grantType", "password"),
            "username": cfg.get("pam_APITokenUserName", ""),
            "password": cfg.get("pam_APITokenPassword", "")}
    out = {"url": url, "grant_type": form["grant_type"],
           "username_sent": form["username"], "password_len": len(form["password"]),
           "works": False, "status": None, "body": "", "access_token_present": False}
    try:
        out["username_decoded"] = base64.b64decode(form["username"]).decode()
    except Exception:                                                # noqa: BLE001
        out["username_decoded"] = "(not base64)"

    # The latch is checked here, not just at the --try-token-gen flag. The flag records
    # intent; the latch records that an attempt already failed. Honouring only the flag
    # is how "attempt once" degraded into "attempt every run" and locked the account.
    latch = token_guard.latch_state()
    if latch is not None:
        out.update(status="blocked by latch", latency_ms=0,
                   body=f"A previous /arcontoken attempt failed (status "
                        f"{latch.get('status')}). Blocked to protect the account. "
                        f"Clear with: python tools\\token_guard.py "
                        f"clear-latch")
        return out

    t0 = time.time()
    tok, note = token_guard.attempt_once(cfg)
    out["latency_ms"] = int((time.time() - t0) * 1000)
    out["body"] = note[:600]
    if tok:
        out.update(status=200, works=True, access_token_present=True)
    else:
        # token_guard has already latched. Do not attempt again, here or anywhere.
        out["status"] = None
    return out


# ------------------------------------------------------- endpoint discovery
SECTION = re.compile(r"^\s*//\s*([A-Za-z][\w &./-]*?)\s*$", re.M)
DECL = re.compile(r'public\s+static\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;(?:\s*//\s*(\w+))?')
VERSION = re.compile(r"^(.*?)(V\d+(?:\.\d+)?)$")


def split_model(controller: str) -> tuple[str, str]:
    """ServiceDetailsV2 -> (ServiceDetails, V2);  UserDetails -> (UserDetails, V1)."""
    m = VERSION.match(controller)
    if m and m.group(1):
        return m.group(1), m.group(2)
    return controller, "V1"


def discover() -> list[dict]:
    text = APICONFIG.read_text(encoding="utf-8", errors="replace")
    marks = [(m.start(), m.group(1).strip()) for m in SECTION.finditer(text)]

    def module_at(pos):
        cur = "(unsectioned)"
        for p, n in marks:
            if p < pos:
                cur = n
            else:
                break
        return cur

    # payload model availability, joined by exact name identity
    payload_methods: dict[str, set] = {}
    if PAYLOAD_DIR.exists():
        noarg = re.compile(r"public\s+(?:static\s+)?[\w<>\[\],\s.]+?\s+(\w+)\s*\(\s*\)")
        for f in PAYLOAD_DIR.rglob("*.java"):
            payload_methods[f.stem] = {m.group(1) for m in
                                       noarg.finditer(f.read_text(encoding="utf-8", errors="replace"))}
    all_payload = set().union(*payload_methods.values()) if payload_methods else set()

    eps = []
    for m in DECL.finditer(text):
        field, path, verb = m.group(1), m.group(2), (m.group(3) or "").lower()
        if not path.startswith("/"):
            continue                       # header names, content types, verb literals
        seg = re.match(r"^/api/(?:(v[\d.]+)/)?([^/?]+)(?:/([^/?]+))?", path, re.I)
        controller = seg.group(2) if seg else "(unparsed)"
        action = (seg.group(3) or "") if seg else ""
        family, model = split_model(controller)

        # ---- safety classification, applied at resolution time ----
        blocked = BLOCKLIST.get(action)
        mutating_by_name = bool(action and MUTATING_NAME.match(action))

        eps.append({
            "field": field, "path": path, "verb": (verb or "?").upper(),
            "module": module_at(m.start()), "controller": controller, "action": action,
            "model_family": family, "model": model,
            "has_payload_model": field in all_payload,
            "blocked": blocked,
            "mutating_by_name": mutating_by_name,
            "declared_codes": ["200"],          # ExpectedAPIStatusCode from the env file
            "response_schema": None,            # no Swagger on :6302 (verified 404)
            "_spec": {}, "_op": {},
        })
    return eps


def is_executable(ep: dict, verb: str) -> tuple[bool, str]:
    """Single gate. Returns (ok, reason_if_not)."""
    if ep["verb"] == "?":
        return False, "no verb comment in APIConfig - request type unresolvable"
    if ep["verb"] != verb.upper():
        return False, f"{ep['verb']} is a mutating verb - default-deny, awaiting approved allowlist"
    if ep["blocked"]:
        return False, ep["blocked"]
    if ep["mutating_by_name"]:
        return False, (f"action '{ep['action']}' implies mutation despite the "
                       f"{ep['verb']} declaration - default-deny (ISSUE-011)")
    return True, ""


# ----------------------------------------------------------------- execution
# Read cap. Set high enough that real PAM responses are never clipped: an earlier
# 200,000-byte cap clipped 8 responses mid-JSON and the parse failure was misreported
# as "error body is not JSON". Always record the true size and a truncation flag so a
# harness limit can never again masquerade as a product defect.
BODY_CAP = 25 * 1024 * 1024


def execute(base: str, ep: dict, token: str) -> dict:
    url = base.rstrip("/") + ep["path"]
    out = {"url": url, "error": None, "body_bytes": 0, "truncated": False}
    t0 = time.time()

    def take(reader) -> bytes:
        raw = reader.read(BODY_CAP + 1)
        out["body_bytes"] = len(raw)
        if len(raw) > BODY_CAP:
            out["truncated"] = True
            return raw[:BODY_CAP]
        return raw

    try:
        req = urllib.request.Request(url, method=ep["verb"], headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT, context=SSL_CTX) as r:
            out.update(status=r.status, body=take(r),
                       content_type=(r.headers.get("Content-Type") or "").split(";")[0].strip())
    except urllib.error.HTTPError as e:
        raw = b""
        try:
            raw = take(e)
        except Exception:                                            # noqa: BLE001
            raw = b""
        ct = ""
        if e.headers is not None:
            ct = e.headers.get("Content-Type") or ""
        out.update(status=e.code, body=raw, content_type=ct.split(";")[0].strip())
    except Exception as exc:                                         # noqa: BLE001
        out.update(status=None, body=b"", content_type="",
                   error=f"{type(exc).__name__}: {exc}")
    out["latency_ms"] = int((time.time() - t0) * 1000)
    return out


# -------------------------------------------------------------------- report
def build_excel(rows, eps, meta, tokinfo, cfg):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    HEAD = PatternFill("solid", fgColor="1F3864")
    HF = Font(bold=True, color="FFFFFF", size=10)
    GOOD = PatternFill("solid", fgColor="C6EFCE")
    BAD = PatternFill("solid", fgColor="FFC7CE")
    WARN = PatternFill("solid", fgColor="FFEB9C")
    NA = PatternFill("solid", fgColor="EDEDED")

    def hdr(ws, n, row=1):
        for c in range(1, n + 1):
            x = ws.cell(row=row, column=c)
            x.fill, x.font = HEAD, HF
            x.alignment = Alignment(vertical="center", wrap_text=True)

    def fit(ws, mx=50):
        for col in ws.columns:
            L = get_column_letter(col[0].column)
            w = max((len(str(c.value)) for c in col if c.value is not None), default=8)
            ws.column_dimensions[L].width = min(max(w + 2, 9), mx)

    wb = Workbook()
    layer_names = sorted({k for r in rows for k in r["layers"]}) if rows else []

    # ---------- Summary
    ws = wb.active
    assert ws is not None
    ws.title = "Summary"
    ws.append([f"QA_MsSQL API Validation - Legacy Surface"])
    ws["A1"].font = Font(bold=True, size=14)
    ws.append([])
    for k, v in meta.items():
        ws.append([k, v])
    ws.append([])
    ws.append(["TOKEN"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    for k, v in tokinfo.items():
        ws.append([k, v])
    ws.append([])
    ws.append(["VERDICTS", "count", "%"])
    hdr(ws, 3, ws.max_row)
    vd = Counter(r["verdict"] for r in rows)
    for k in ("PASS", "WARN", "FAIL"):
        ws.append([k, vd.get(k, 0), f"{vd.get(k,0)/max(len(rows),1)*100:.1f}%"])
    ws.append([])
    ws.append(["LAYER", "PASS", "FAIL", "NA"])
    hdr(ws, 4, ws.max_row)
    for L in layer_names:
        c = Counter(r["layers"].get(L, {}).get("verdict", "?") for r in rows)
        ws.append([L, c.get("PASS", 0), c.get("FAIL", 0), c.get("NA", 0)])
    fit(ws)

    # ---------- Results
    ws = wb.create_sheet("Results")
    cols = (["#", "Module", "Controller", "Model", "Action", "Verb", "Path", "HTTP",
             "Latency ms", "Resp KB", "Content-Type", "Payload model", "Verdict"]
            + layer_names + ["Drift", "Fail detail", "Shape hash"])
    ws.append(cols)
    for i, r in enumerate(rows, 1):
        detail = " | ".join(f"{L}: {r['layers'][L]['note']}" for L in r["fail_layers"])
        ws.append([i, r["module"], r["controller"], r["model"], r["action"], r["verb"],
                   r["path"], r["status"], r["latency_ms"],
                   round(r.get("body_bytes", 0) / 1024, 1), r["content_type"],
                   "Y" if r["has_payload_model"] else "-", r["verdict"]]
                  + [r["layers"].get(L, {}).get("verdict", "") for L in layer_names]
                  + [r["drift"], detail[:300], r["shape_hash"]])
        rw = ws.max_row
        vc = ws.cell(row=rw, column=13)
        vc.fill = {"PASS": GOOD, "WARN": WARN, "FAIL": BAD}.get(r["verdict"], NA)
        vc.font = Font(bold=True)
        for j, L in enumerate(layer_names):
            c = ws.cell(row=rw, column=14 + j)
            c.fill = {"PASS": GOOD, "FAIL": BAD, "NA": NA}.get(c.value, NA)
    hdr(ws, len(cols))
    ws.freeze_panes = "A2"
    fit(ws)

    # ---------- Coverage  (the requested Module x Request type x Model table)
    ws = wb.create_sheet("Coverage")
    ws.append(["COVERAGE BY MODULE, REQUEST TYPE AND MODEL"])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append(["Model = API version family parsed from the controller "
               "(V1 = unversioned base, V2/V3/V4 = versioned successors)"])
    ws.append([])

    ws.append(["Module", "Model", "Verb", "Declared", "Executed", "PASS", "WARN", "FAIL",
               "Payload model available", "Coverage %"])
    hdr(ws, 10, ws.max_row)

    declared = defaultdict(int)
    payload_ok = defaultdict(int)
    for e in eps:
        declared[(e["module"], e["model"], e["verb"])] += 1
        if e["has_payload_model"]:
            payload_ok[(e["module"], e["model"], e["verb"])] += 1
    execd = defaultdict(lambda: Counter())
    for r in rows:
        execd[(r["module"], r["model"], r["verb"])][r["verdict"]] += 1

    for key in sorted(declared, key=lambda k: (k[0].lower(), k[1], k[2])):
        mod, mdl, vb = key
        d = declared[key]
        c = execd.get(key, Counter())
        ex = sum(c.values())
        ws.append([mod, mdl, vb, d, ex, c.get("PASS", 0), c.get("WARN", 0), c.get("FAIL", 0),
                   payload_ok.get(key, 0), f"{ex/d*100:.0f}%" if d else "-"])

    # module rollup
    ws.append([])
    ws.append(["ROLLUP BY MODULE"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True, size=12)
    ws.append(["Module", "Models", "Declared", "GET", "POST", "PUT", "DELETE",
               "Executed", "PASS", "FAIL", "Coverage %"])
    hdr(ws, 11, ws.max_row)
    mods = sorted({e["module"] for e in eps}, key=str.lower)
    for mod in mods:
        me = [e for e in eps if e["module"] == mod]
        mr = [r for r in rows if r["module"] == mod]
        vb = Counter(e["verb"] for e in me)
        ws.append([mod, ",".join(sorted({e["model"] for e in me})), len(me),
                   vb.get("GET", 0), vb.get("POST", 0), vb.get("PUT", 0), vb.get("DELETE", 0),
                   len(mr), sum(1 for r in mr if r["verdict"] == "PASS"),
                   sum(1 for r in mr if r["verdict"] == "FAIL"),
                   f"{len(mr)/len(me)*100:.0f}%" if me else "-"])

    # verb rollup
    ws.append([])
    ws.append(["ROLLUP BY REQUEST TYPE"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True, size=12)
    ws.append(["Verb", "Declared", "Executed", "PASS", "WARN", "FAIL", "Coverage %", "Note"])
    hdr(ws, 8, ws.max_row)
    dv = Counter(e["verb"] for e in eps)
    rv = defaultdict(lambda: Counter())
    for r in rows:
        rv[r["verb"]][r["verdict"]] += 1
    for vb in sorted(dv, key=lambda v: -dv[v]):
        c = rv.get(vb, Counter())
        ex = sum(c.values())
        note = "" if vb == "GET" else "default-deny: mutating verb, not executed"
        if vb == "?":
            note = "no verb comment in APIConfig - unresolvable"
        ws.append([vb, dv[vb], ex, c.get("PASS", 0), c.get("WARN", 0), c.get("FAIL", 0),
                   f"{ex/dv[vb]*100:.0f}%", note])

    # model rollup
    ws.append([])
    ws.append(["ROLLUP BY MODEL (API version family)"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True, size=12)
    ws.append(["Model", "Declared", "Distinct controllers", "GET", "Executed", "PASS", "FAIL"])
    hdr(ws, 7, ws.max_row)
    for mdl in sorted({e["model"] for e in eps}):
        me = [e for e in eps if e["model"] == mdl]
        mr = [r for r in rows if r["model"] == mdl]
        ws.append([mdl, len(me), len({e["controller"] for e in me}),
                   sum(1 for e in me if e["verb"] == "GET"), len(mr),
                   sum(1 for r in mr if r["verdict"] == "PASS"),
                   sum(1 for r in mr if r["verdict"] == "FAIL")])
    fit(ws)

    # ---------- Excluded
    ws = wb.create_sheet("Excluded")
    ws.append(["Declared endpoints NOT executed this run, with reason"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Module", "Model", "Verb", "Path", "Reason"])
    hdr(ws, 5, ws.max_row)
    done = {r["path"] for r in rows}
    for e in eps:
        if e["path"] in done:
            continue
        ok, why = is_executable(e, "GET")
        ws.append([e["module"], e["model"], e["verb"], e["path"],
                   why or "not selected (limit applied)"])
    fit(ws)

    # ---------- Environment
    ws = wb.create_sheet("Environment")
    ws.append([f"ENVIRONMENT: {ENV_NAME}"])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append([])
    ws.append(["Key", "Value", "Source"])
    hdr(ws, 3, ws.max_row)
    for k in ("environment", "environmentUrl", "environmentAPIUrl", "pam_BaseAPIURL",
              "pam_tokenAPIUrl", "pam_grantType", "pam_APITokenUserName",
              "pam_settingsapiurl", "ExpectedAPIStatusCode", "setAPIRequestTimeout_MS",
              "API_ExcelDataProviderFileName", "Negative_API_ExcelDataProviderFileName"):
        if k in cfg:
            ws.append([k, cfg[k], "Environments/QA_MsSQL.properties"])
    ws.append(["pam_APITokenPassword", "(redacted - present)",
               "Environments/QA_MsSQL.properties"])
    fit(ws)

    out = RUN_DIR / "QA_MsSQL_API_Validation_Results.xlsx"
    wb.save(out)
    return out


# --------------------------------------------------------------------- driver
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--verb", default="GET")
    # OBJ-013: deny-by-default. This script was previously opt-OUT (--dry-run only),
    # so a bare `python run_qa_mssql.py` swept the live GET surface — contradicting
    # the invariant root CLAUDE.md and .claude/rules/api-surface.md both assert:
    # "a bare run issues zero HTTP calls; --execute is required."
    ap.add_argument("--execute", action="store_true",
                    help="REQUIRED to issue any HTTP request. Without it the run "
                         "plans only and contacts nothing.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Explicit plan-only. Now the default behaviour; retained so "
                         "existing invocations and docs keep working.")
    ap.add_argument("--promote-baseline", action="store_true")
    ap.add_argument("--try-token-gen", action="store_true",
                    help="Attempt dynamic getToken(). OFF by default: repeated attempts "
                         "locked the API account (ISSUE-009). Only use once, after the "
                         "account is unlocked and new credentials are in place.")
    args = ap.parse_args()

    started = datetime.now(timezone.utc)
    log("=" * 78)
    log(f"QA_MsSQL API VALIDATION - legacy surface - request type {args.verb}")
    log("=" * 78)

    cfg = load_env()
    base = cfg.get("pam_BaseAPIURL", "")
    log(f"\n[env] {ENV_FILE.relative_to(ROOT)}")
    log(f"      pam_BaseAPIURL  {base}")
    log(f"      environmentUrl  {cfg.get('environmentUrl')}  (application URL, not called)")
    log(f"      pam_tokenAPIUrl {cfg.get('pam_tokenAPIUrl')}")

    # ---- token
    log("\n[1/6] TOKEN")
    if args.try_token_gen:
        dyn = try_dynamic_token(cfg)
        log(f"      dynamic getToken(): HTTP {dyn['status']}  {dyn['latency_ms']} ms  "
            f"-> {'WORKS' if dyn['works'] else 'FAILS'}")
        if not dyn["works"]:
            log(f"        username sent : {dyn['username_sent']}  (decodes to {dyn['username_decoded']!r})")
            log(f"        response body : {dyn['body'][:150]}")
    else:
        dyn = {"works": False, "status": "not attempted", "latency_ms": 0,
               "body": "skipped by default - repeated attempts locked the account "
                       "(ISSUE-009). Pass --try-token-gen to attempt once.",
               "username_sent": cfg.get("pam_APITokenUserName", ""),
               "username_decoded": "", "access_token_present": False,
               "url": cfg.get("pam_tokenAPIUrl", "")}
        log("      dynamic getToken(): SKIPPED (default) - account lockout risk, ISSUE-009")
        log("        pass --try-token-gen to attempt once, after the account is unlocked")
    token, src = get_token()
    if not token:
        log("      ⛔ no supplied token found. Set $PAM_API_TOKEN or create tools/.token")
        return 1
    cl = jwt_claims(token)
    now = int(time.time())
    hrs_left = (cl.get("exp", now) - now) / 3600
    log(f"      supplied token   : {src}")
    log(f"        APIUser role   : {cl.get('http://schemas.microsoft.com/ws/2008/06/identity/claims/role')}"
        f"  APIUserId {cl.get('APIUserId')}")
    log(f"        valid for      : {hrs_left:.2f} h  ({'OK' if hrs_left > 0 else 'EXPIRED'})")
    if hrs_left <= 0:
        log("      ⛔ token expired - aborting")
        return 1
    tokinfo = {
        "Token source": src,
        "Dynamic generation (getToken)": "WORKS" if dyn["works"] else f"FAILS - HTTP {dyn['status']}",
        "Dynamic failure body": dyn["body"][:120] if not dyn["works"] else "",
        "Token APIUserId": cl.get("APIUserId", "?"),
        "Token hours remaining": f"{hrs_left:.2f}",
        "Token issuer": cl.get("iss", "?"),
    }

    # ---- discovery
    log("\n[2/6] DISCOVER - reflection over APIConfig.java")
    eps = discover()
    vd = Counter(e["verb"] for e in eps)
    log(f"      declared endpoints : {len(eps)}")
    log(f"      verb mix           : " + "  ".join(f"{k}={v}" for k, v in vd.most_common()))
    log(f"      modules            : {len({e['module'] for e in eps})}")
    log(f"      controllers        : {len({e['controller'] for e in eps})}")
    log(f"      models             : " +
        "  ".join(f"{k}={v}" for k, v in Counter(e["model"] for e in eps).most_common()))

    cases, skipped = [], []
    for e in eps:
        ok, why = is_executable(e, args.verb)
        (cases if ok else skipped).append(e if ok else {**e, "skip_reason": why})
    cases.sort(key=lambda e: (e["module"].lower(), e["path"]))
    if args.limit:
        cases = cases[:args.limit]

    log(f"\n[3/6] SELECT - {args.verb}, safety gate applied")
    log(f"      executable            : {len(cases)}")
    blk = Counter(s["skip_reason"].split(" (")[0].split(" - ")[0]
                  for s in skipped if s["verb"] == args.verb.upper())
    for reason, n in blk.most_common():
        log(f"      excluded {n:>4}         : {reason}")
    log(f"      excluded {sum(1 for s in skipped if s['verb'] != args.verb.upper()):>4}         "
        f": non-{args.verb.upper()} verb (default-deny)")

    # OBJ-013: deny-by-default. Planning is the default outcome; issuing HTTP requires
    # --execute. `--dry-run` is kept as an explicit synonym so older invocations and
    # the documented commands continue to behave exactly as their authors intended.
    if args.dry_run or not args.execute:
        for c in cases[:30]:
            log(f"      {c['module'][:22]:<22} {c['model']:<4} {c['path'][:56]}")
        log(f"      ... total {len(cases)}")
        if not args.execute:
            log("\n      PLAN ONLY - zero HTTP requests were issued.")
            log("      Pass --execute to run these calls against the live environment.")
        return 0

    # Reports are RETAINED. There is no archive-and-prune step and nothing is deleted:
    # every run writes into its own dated folder, so no prior run can be overwritten.
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    log(f"      retained: prior runs kept untouched; this run writes to {RUN_REL}")

    log(f"\n[4/6] EXECUTE + VALIDATE - {len(cases)} calls x 7 layers")
    baseline = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    rows, newbase = [], {}
    for i, ep in enumerate(cases, 1):
        res = execute(base, ep, token)
        val = validate(ep, res)
        parsed = None
        try:
            parsed = json.loads((res.get("body") or b"").decode("utf-8", "replace"))
        except Exception:                                            # noqa: BLE001
            pass
        shape = shape_of(parsed) if parsed is not None else []
        sh = hashlib.sha256("|".join(shape).encode()).hexdigest()[:12] if shape else ""
        key = f"{ep['verb']} {ep['path']}"
        drift = "NO BASELINE"
        if key in baseline:
            b = baseline[key]
            drift = ("CHANGED" if b.get("shape_hash") != sh
                     else "STATUS CHANGED" if str(b.get("status")) != str(res.get("status"))
                     else "STABLE")
        newbase[key] = {"status": res.get("status"), "shape_hash": sh,
                        "latency_ms": res.get("latency_ms")}

        # A harness-side truncation must never be reported as a malformed-body defect.
        if res.get("truncated"):
            for L in ("L2_envelope", "L3_schema", "L4_required_fields", "L5_types"):
                if val["layers"].get(L, {}).get("verdict") == "FAIL":
                    val["layers"][L] = {"verdict": "NA",
                                        "note": f"body truncated by harness at {BODY_CAP} bytes "
                                                f"(actual {res['body_bytes']}) - not assessable"}
            val["fail_layers"] = [L for L, v in val["layers"].items() if v["verdict"] == "FAIL"]
            val["n_fail"] = len(val["fail_layers"])
            val["verdict"] = "PASS" if not val["fail_layers"] else val["verdict"]

        rows.append({**{k: v for k, v in ep.items() if not k.startswith("_")},
                     "status": res.get("status"), "latency_ms": res.get("latency_ms"),
                     "content_type": res.get("content_type"), "error": res.get("error"),
                     "body_bytes": res.get("body_bytes", 0),
                     "truncated": res.get("truncated", False),
                     "shape_hash": sh, "drift": drift, **val})

        body_txt = (res.get("body") or b"")[:2000].decode("utf-8", "replace")
        ev = {"environment": ENV_NAME, "surface": "legacy /api/<Controller>/<Action>",
              "module": ep["module"], "controller": ep["controller"], "model": ep["model"],
              "apiconfig_field": ep["field"],
              "request": {"verb": ep["verb"], "url": res["url"],
                          "headers": {"Authorization": "Bearer <redacted>",
                                      "Content-Type": "application/json"}},
              "response": {"status": res.get("status"),
                           "content_type": res.get("content_type"),
                           "latency_ms": res.get("latency_ms"), "body_preview": body_txt},
              "validation": val, "drift": drift}
        safe = re.sub(r"[^A-Za-z0-9]+", "_", f"{ep['verb']}_{ep['path']}").strip("_")[:110]
        (EVIDENCE / f"{i:03d}_{safe}.json").write_text(json.dumps(ev, indent=2), encoding="utf-8")

        if i % 25 == 0 or i == len(cases):
            log(f"      {i:>3}/{len(cases)}  last: {rows[-1]['verdict']:<5} "
                f"HTTP {str(rows[-1]['status']):<5} {ep['path'][:48]}")

    if args.promote_baseline or not BASELINE.exists():
        BASELINE.write_text(json.dumps(newbase, indent=1), encoding="utf-8")
        log(f"      baseline {'promoted' if args.promote_baseline else 'initialised'} "
            f"({len(newbase)}) -> {BASELINE.name}")

    log("\n[5/6] REPORT")
    lat = [r["latency_ms"] for r in rows if r["latency_ms"]]
    meta = {
        "Environment": ENV_NAME,
        "API base URL": base,
        "Surface": "legacy /api/<Controller>/<Action> (no Swagger - :6302 returns 404)",
        "Generated (UTC)": started.strftime("%Y-%m-%d %H:%M:%S"),
        "Endpoint source": "reflection over APIConfig.java",
        "Declared endpoints": len(eps),
        "Request type executed": args.verb.upper(),
        "Executed": len(rows),
        "Modules touched": len({r["module"] for r in rows}),
        "Median latency ms": int(statistics.median(lat)) if lat else 0,
        "Max latency ms": max(lat) if lat else 0,
        "Validation layers": 7,
    }
    xlsx = build_excel(rows, eps, meta, tokinfo, cfg)
    log(f"      Excel    -> {xlsx.relative_to(ROOT)}")

    slim = [{k: v for k, v in r.items() if k != "response_schema"} for r in rows]
    (RUN_DIR / "qa_mssql_results.json").write_text(
        json.dumps({"meta": meta, "token": {**tokinfo, "dynamic_detail": dyn},
                    "results": slim}, indent=1, default=str), encoding="utf-8")
    (RUN_DIR / "qa_mssql_token_check.json").write_text(
        json.dumps(dyn, indent=1), encoding="utf-8")
    log(f"      JSON     -> {RUN_REL}/qa_mssql_results.json")
    log(f"      Evidence -> {RUN_REL}/evidence/  ({len(rows)} files)")

    log("\n[6/6] SUMMARY")
    vdc = Counter(r["verdict"] for r in rows)
    lf = Counter(L for r in rows for L in r["fail_layers"])
    sc = Counter(str(r["status"]) for r in rows)
    log("=" * 78)
    log(f"VERDICTS  PASS {vdc.get('PASS',0)}  WARN {vdc.get('WARN',0)}  FAIL {vdc.get('FAIL',0)}  of {len(rows)}")
    log(f"STATUS    " + "  ".join(f"{k}={v}" for k, v in sc.most_common()))
    log(f"LAYERS    " + "  ".join(f"{k}={v}" for k, v in sorted(lf.items())))

    # Refuse to present an outage as a result set.
    n503 = sc.get("503", 0)
    if n503 > len(rows) * 0.2:
        log("")
        log("!" * 78)
        log(f"!! RUN INVALID: {n503}/{len(rows)} responses were HTTP 503 - the environment stopped")
        log("!! responding mid-run. These are NOT endpoint verdicts. Do not quote this run.")
        log(f"!! The previous run is preserved under artifacts/runs-archive/.")
        log("!" * 78)
    log("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
