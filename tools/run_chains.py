#!/usr/bin/env python3
"""
API CHAIN EXECUTOR — all request types: GET · POST · PUT · PATCH · DELETE.

Executes chained API flows discovered automatically by
`artifacts/graph/api-graph/build_api_graph.py`. Nothing about a chain is hand-written: the
sequence, the request bodies and the values passed between calls are all derived.

WHAT ONE CHAIN RUN DOES
    ctx = {}                                  # the chaining context
    for each hop in the plan:
        body = payload_template(hop)           # literal JSON from the payload helper
        body = inject(body, ctx)               # substitute values harvested upstream
        path = bind_path(hop.path, ctx)        # /api/User/{id} -> /api/User/42
        resp = call(hop.verb, path, body)      # GET/POST/PUT/PATCH/DELETE
        validate(resp)                          # the same 7 layers as the other runners
        ctx.update(harvest(resp))               # feed the next hop

⛔ SAFETY — this harness can issue writes, so it is deny-by-default
    * Plan-only unless --execute is passed. A bare run makes ZERO HTTP calls.
    * Verbs must be opted into: --allow-verbs GET,POST  (default: GET only)
    * Destructive action names are ALWAYS refused unless --allow-destructive AND
      --approver "<name>" are both supplied. The approver is recorded in the report.
    * Endpoint blocklist enforced during planning, so a blocked call is never built.
    * --delay-ms throttles every call (default 250 ms). The QA environment has stopped
      responding twice under sequential load; do not remove this.
    * CIRCUIT BREAKER: aborts the whole run after N consecutive 5xx/timeouts
      (default 3). The earlier GET runner ploughed through 322 straight 503s; that
      must not happen again.
    * --max-calls caps total requests (default 200).
    * A health probe runs first; the run refuses to start against a sick environment.

USAGE
    python Reports\\Scripts\\run_chains.py                          # plan only, no calls
    python Reports\\Scripts\\run_chains.py --depth 3                # A->B->C plans
    python Reports\\Scripts\\run_chains.py --execute                # GET-only chains
    python Reports\\Scripts\\run_chains.py --execute --allow-verbs GET,POST,PUT,PATCH
    python Reports\\Scripts\\run_chains.py --execute --allow-verbs GET,POST,PUT,PATCH,DELETE \\
           --allow-destructive --approver "S. Sawant"
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
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
from run_validation import validate                      # one definition of the 7 layers

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

REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
ENV_FILE = REPO / "Environments" / "QA_MsSQL.properties"
GRAPH = ROOT / "artifacts" / "graph" / "api-graph" / "out" / "api-graph.json"

# Every run gets its own dated folder. Nothing is ever overwritten or deleted.
RUN_STAMP = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d_%H%M%S")
RUN_DIR = REPORTS / "Runs" / f"{RUN_STAMP}_derived-chains"
RUN_REL = f"artifacts/runs/{RUN_STAMP}_derived-chains"

EVIDENCE = RUN_DIR / "evidence"
TOKEN_FILE = HERE / ".token"

ALL_VERBS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
BODY_CAP = 25 * 1024 * 1024
LATENCY_SLA_MS = 2000

# Never built into a request, whatever the flags say (ISSUE-010).
ENDPOINT_BLOCKLIST = {
    "GetErrorLogs": "hangs 30s and stops the IIS app pool (ISSUE-010)",
    "GetLogs": "hangs 30s and stops the IIS app pool (ISSUE-010)",
    "GetAllActiveUserDetails": "hung 30s on every version during the GET run",
}
# Require --allow-destructive + --approver.
DESTRUCTIVE = re.compile(
    r"^(delete|remove|drop|purge|reset|revoke|disable|deactivate|terminate|kill|wipe)",
    re.I)

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def log(m=""):
    print(m, flush=True)


# ------------------------------------------------------------------ environment
def load_env() -> dict:
    cfg = {}
    for line in ENV_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
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


def token_hours_left(tok: str) -> float:
    try:
        p = tok.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))
        return (claims.get("exp", 0) - int(time.time())) / 3600
    except Exception:                                                # noqa: BLE001
        return -1.0


# ------------------------------------------------------------- chain value plumbing
SCALAR = (str, int, float, bool)


def harvest(parsed) -> dict:
    """Flatten a response into {field_lower: scalar}. First occurrence wins."""
    out: dict[str, object] = {}

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, SCALAR) and v is not None:
                    out.setdefault(k.lower(), v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o[:5]:
                walk(v)

    walk(parsed)
    return out


def inject(template: str | None, ctx: dict) -> tuple[str | None, list[str]]:
    """Substitute chained values into a request body. Returns (body, fields_injected)."""
    if not template or not template.strip():
        return template, []
    used: list[str] = []
    try:
        obj = json.loads(template)
    except Exception:                                                # noqa: BLE001
        # not parseable JSON - fall back to textual key:value replacement
        body = template
        for k, v in ctx.items():
            pat = re.compile(r'("' + re.escape(k) + r'"\s*:\s*)("[^"]*"|[^,}\s]+)', re.I)
            if pat.search(body):
                body = pat.sub(lambda m: m.group(1) + json.dumps(v), body, count=1)
                used.append(k)
        return body, used

    def walk(o):
        if isinstance(o, dict):
            for k in list(o.keys()):
                lk = k.lower()
                if lk in ctx and isinstance(o[k], SCALAR):
                    o[k] = ctx[lk]
                    used.append(k)
                else:
                    walk(o[k])
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(obj)
    return json.dumps(obj), used


PATH_TOKEN = re.compile(r"\{(\w+)\}")


def bind_path(path: str, ctx: dict) -> tuple[str, list[str], list[str]]:
    """Bind {tokens} and ?query= values from ctx. Returns (path, bound, unbound)."""
    bound, unbound = [], []

    def sub(m):
        name = m.group(1)
        v = ctx.get(name.lower())
        if v is None:
            unbound.append(name)
            return m.group(0)
        bound.append(name)
        return urllib.parse.quote(str(v), safe="")

    out = PATH_TOKEN.sub(sub, path)

    if "?" in out:
        head, qs = out.split("?", 1)
        parts = []
        for kv in qs.split("&"):
            if "=" in kv:
                k, v = kv.split("=", 1)
                if k.lower() in ctx:
                    v = urllib.parse.quote(str(ctx[k.lower()]), safe="")
                    bound.append(k)
                parts.append(f"{k}={v}")
            else:
                parts.append(kv)
        out = head + "?" + "&".join(parts)
    return out, bound, unbound


# ------------------------------------------------------------------- planning
def plan_chains(eps: list[dict], chains: list[dict], depth: int,
                allow_verbs: set[str], allow_destructive: bool,
                min_conf: str) -> tuple[list[dict], list[dict]]:
    RANK = {"low": 1, "medium": 2, "high": 3}
    by_id = {e["id"]: e for e in eps}
    adj: dict[str, list[dict]] = defaultdict(list)
    for c in chains:
        if RANK[c["confidence"]] >= RANK[min_conf]:
            adj[c["from"]].append(c)

    def gate(ep: dict) -> str | None:
        if ep["action"] in ENDPOINT_BLOCKLIST:
            return f"blocked: {ENDPOINT_BLOCKLIST[ep['action']]}"
        if ep["verb"] not in allow_verbs:
            return f"verb {ep['verb']} not in --allow-verbs"
        if DESTRUCTIVE.match(ep["action"] or "") and not allow_destructive:
            return f"destructive action '{ep['action']}' - needs --allow-destructive + --approver"
        if ep["verb"] == "?":
            return "no verb declared in APIConfig"
        return None

    plans, rejected = [], []
    seen = set()
    for start in sorted(adj):
        # walk simple paths up to `depth` endpoints
        stack = [([start], [])]
        while stack:
            nodes, edges = stack.pop()
            if len(nodes) >= 2:
                sig = tuple(nodes)
                if sig not in seen:
                    seen.add(sig)
                    hops = [by_id[n] for n in nodes if n in by_id]
                    if len(hops) == len(nodes):
                        blocks = [(h, gate(h)) for h in hops]
                        bad = [(h, r) for h, r in blocks if r]
                        rec = {
                            "id": " -> ".join(n for n in nodes),
                            "hops": hops, "edges": edges,
                            "verbs": [h["verb"] for h in hops],
                            "fields": [e["field"] for e in edges],
                            "confidence": min((e["confidence"] for e in edges),
                                              key=lambda c: RANK[c]),
                            "cross_module": any(e["cross_module"] for e in edges),
                        }
                        if bad:
                            rec["reject_reason"] = "; ".join(
                                f"{h['verb']} {h['path']}: {r}" for h, r in bad)
                            rejected.append(rec)
                        else:
                            plans.append(rec)
            if len(nodes) < depth:
                for e in adj.get(nodes[-1], []):
                    if e["to"] not in nodes:
                        stack.append((nodes + [e["to"]], edges + [e]))
    return plans, rejected


# ------------------------------------------------------------------- execution
def call(base: str, verb: str, path: str, body: str | None, token: str,
         timeout: int) -> dict:
    url = base.rstrip("/") + path
    out = {"url": url, "error": None, "body_bytes": 0, "truncated": False}
    data = body.encode() if body else None
    t0 = time.time()

    def take(r):
        raw = r.read(BODY_CAP + 1)
        out["body_bytes"] = len(raw)
        if len(raw) > BODY_CAP:
            out["truncated"] = True
            return raw[:BODY_CAP]
        return raw

    try:
        req = urllib.request.Request(url, data=data, method=verb, headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as r:
            out.update(status=r.status, body=take(r),
                       content_type=(r.headers.get("Content-Type") or "").split(";")[0].strip())
    except urllib.error.HTTPError as e:
        raw = b""
        try:
            raw = take(e)
        except Exception:                                            # noqa: BLE001
            pass
        ct = e.headers.get("Content-Type") or "" if e.headers is not None else ""
        out.update(status=e.code, body=raw, content_type=ct.split(";")[0].strip())
    except Exception as exc:                                         # noqa: BLE001
        out.update(status=None, body=b"", content_type="",
                   error=f"{type(exc).__name__}: {exc}")
    out["latency_ms"] = int((time.time() - t0) * 1000)
    return out


class CircuitBreaker:
    """Stops the run when the environment starts failing. Learned the hard way."""

    def __init__(self, limit: int):
        self.limit, self.streak, self.tripped = limit, 0, False

    def record(self, status, error) -> bool:
        bad = error is not None or (isinstance(status, int) and status >= 500)
        self.streak = self.streak + 1 if bad else 0
        if self.streak >= self.limit:
            self.tripped = True
        return self.tripped


def health_ok(base: str, token: str) -> tuple[bool, str]:
    probe = "/api/ActivityLogs/GetDatabaseStatus"
    r = call(base, "GET", probe, None, token, 20)
    if r.get("status") == 200:
        return True, f"200 in {r['latency_ms']} ms"
    return False, f"status={r.get('status')} error={r.get('error')}"


# ---------------------------------------------------------------------- report
def write_report(plans, rejected, results, meta, args):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    HEAD = PatternFill("solid", fgColor="1F3864")
    HF = Font(bold=True, color="FFFFFF", size=10)
    GOOD = PatternFill("solid", fgColor="C6EFCE")
    BAD = PatternFill("solid", fgColor="FFC7CE")
    WARN = PatternFill("solid", fgColor="FFEB9C")
    NA = PatternFill("solid", fgColor="EDEDED")

    def hdr(ws, n, row=None):
        for c in range(1, n + 1):
            x = ws.cell(row=row or 1, column=c)
            x.fill, x.font = HEAD, HF
            x.alignment = Alignment(vertical="center", wrap_text=True)

    def fit(ws, mx=54):
        for col in ws.columns:
            L = get_column_letter(col[0].column)
            w = max((len(str(c.value)) for c in col if c.value is not None), default=8)
            ws.column_dimensions[L].width = min(max(w + 2, 9), mx)

    wb = Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "Summary"
    ws.append(["API Chain Execution — QA_MsSQL"])
    ws["A1"].font = Font(bold=True, size=14)
    ws.append([])
    for k, v in meta.items():
        ws.append([k, v])
    fit(ws)

    # ---- Chain plans
    ws = wb.create_sheet("Chain Plans")
    ws.append(["#", "Chain", "Hops", "Verbs", "Chained fields", "Confidence",
               "Cross-module", "Status", "Reject reason"])
    hdr(ws, 9)
    ws.freeze_panes = "A2"
    exec_by_id = {r["plan_id"]: r for r in results}
    for i, p in enumerate(plans + rejected, 1):
        r = exec_by_id.get(p["id"])
        if "reject_reason" in p:
            state = "REJECTED"
        elif r is None:
            state = "not executed (plan only)"
        else:
            state = r["verdict"]
        ws.append([i, " -> ".join(h["path"] for h in p["hops"]), len(p["hops"]),
                   " -> ".join(p["verbs"]), ", ".join(p["fields"]), p["confidence"],
                   "yes" if p["cross_module"] else "no", state,
                   p.get("reject_reason", "")[:220]])
        c = ws.cell(row=ws.max_row, column=8)
        c.fill = {"PASS": GOOD, "WARN": WARN, "FAIL": BAD, "REJECTED": NA}.get(state, NA)
    fit(ws)

    # ---- Hop detail
    ws = wb.create_sheet("Hop Detail")
    ws.append(["Chain", "Hop", "Verb", "Path (bound)", "HTTP", "Latency ms", "Resp KB",
               "Fields injected", "Path bound", "Path unbound", "Harvested", "Verdict",
               "Fail detail"])
    hdr(ws, 13)
    ws.freeze_panes = "A2"
    for r in results:
        for h in r["hops"]:
            ws.append([r["plan_id"][:60], h["n"], h["verb"], h["path"], h["status"],
                       h["latency_ms"], round(h.get("body_bytes", 0) / 1024, 1),
                       ", ".join(h["injected"]) or "-",
                       ", ".join(h["path_bound"]) or "-",
                       ", ".join(h["path_unbound"]) or "-",
                       h["harvested_count"], h["verdict"],
                       "; ".join(h["fail_layers"])[:180]])
            c = ws.cell(row=ws.max_row, column=12)
            c.fill = {"PASS": GOOD, "WARN": WARN, "FAIL": BAD}.get(h["verdict"], NA)
    fit(ws)

    # ---- Safety
    ws = wb.create_sheet("Safety")
    ws.append(["SAFETY CONFIGURATION FOR THIS RUN"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Setting", "Value"])
    hdr(ws, 2, ws.max_row)
    for k, v in [("Mode", "EXECUTE" if args.execute else "PLAN ONLY - no HTTP calls"),
                 ("Verbs allowed", ",".join(sorted(args.allow_verbs))),
                 ("Destructive allowed", str(args.allow_destructive)),
                 ("Approver", args.approver or "(none)"),
                 ("Delay between calls (ms)", args.delay_ms),
                 ("Max calls", args.max_calls),
                 ("Circuit breaker (consecutive failures)", args.breaker),
                 ("Chain depth", args.depth),
                 ("Min confidence", args.min_confidence)]:
        ws.append([k, v])
    ws.append([])
    ws.append(["Permanently blocked endpoints", "Reason"])
    hdr(ws, 2, ws.max_row)
    for a, why in ENDPOINT_BLOCKLIST.items():
        ws.append([a, why])
    fit(ws)

    out = RUN_DIR / "QA_MsSQL_Chain_Execution.xlsx"
    wb.save(out)
    return out


# ---------------------------------------------------------------------- driver
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--execute", action="store_true",
                    help="actually issue HTTP calls. Without it the run is plan-only.")
    ap.add_argument("--allow-verbs", default="GET",
                    help="comma list from GET,POST,PUT,PATCH,DELETE (default GET)")
    ap.add_argument("--allow-destructive", action="store_true")
    ap.add_argument("--approver", default="")
    ap.add_argument("--depth", type=int, default=2, help="endpoints per chain (>=2)")
    ap.add_argument("--min-confidence", choices=["low", "medium", "high"], default="medium")
    ap.add_argument("--delay-ms", type=int, default=250)
    ap.add_argument("--max-calls", type=int, default=200)
    ap.add_argument("--breaker", type=int, default=3,
                    help="abort after this many consecutive 5xx/timeouts")
    ap.add_argument("--limit", type=int, default=None, help="cap number of chains")
    args = ap.parse_args()

    args.allow_verbs = {v.strip().upper() for v in args.allow_verbs.split(",") if v.strip()}
    bad = args.allow_verbs - set(ALL_VERBS)
    if bad:
        log(f"unknown verb(s): {sorted(bad)}; valid: {ALL_VERBS}")
        return 2
    if args.allow_destructive and not args.approver:
        log("⛔ --allow-destructive requires --approver \"<name>\"")
        return 2

    started = datetime.now(timezone.utc)
    log("=" * 78)
    log("API CHAIN EXECUTOR - QA_MsSQL")
    log("=" * 78)
    log(f"\nmode          : {'EXECUTE' if args.execute else 'PLAN ONLY (no HTTP calls)'}")
    log(f"verbs allowed : {','.join(sorted(args.allow_verbs))}")
    log(f"destructive   : {args.allow_destructive}"
        + (f"  approver={args.approver!r}" if args.allow_destructive else ""))
    log(f"depth         : {args.depth}   min-confidence: {args.min_confidence}")
    log(f"throttle      : {args.delay_ms} ms   max-calls: {args.max_calls}   "
        f"breaker: {args.breaker}")

    if not GRAPH.exists():
        log(f"\n⛔ chain graph missing: {GRAPH}")
        log("   run: python tools/build_api_graph.py")
        return 1
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    eps, chains = g["endpoints"], g["chains"]
    log(f"\n[1/5] GRAPH  endpoints {len(eps)}  chain candidates {len(chains)}")

    plans, rejected = plan_chains(eps, chains, args.depth, args.allow_verbs,
                                  args.allow_destructive, args.min_confidence)
    if args.limit:
        plans = plans[:args.limit]
    log(f"\n[2/5] PLAN   executable chains {len(plans)}   rejected {len(rejected)}")
    vshape = Counter(" -> ".join(p["verbs"]) for p in plans)
    for k, v in vshape.most_common(8):
        log(f"      {v:>5}  {k}")
    rr = Counter(re.sub(r"^.*?: ", "", p["reject_reason"].split(";")[0])
                 for p in rejected)
    for k, v in rr.most_common(6):
        log(f"      rejected {v:>5}  {k[:66]}")

    cfg = load_env()
    base = cfg.get("pam_BaseAPIURL", "")
    results: list[dict] = []
    breaker = CircuitBreaker(args.breaker)
    calls = 0

    if not args.execute:
        log("\n[3/5] EXECUTE  skipped - plan-only mode")
        log("      pass --execute to issue calls (and widen --allow-verbs as needed)")
        log("\n      sample plans:")
        for p in plans[:12]:
            field = p["fields"][0] if p["fields"] else "-"
            log(f"        {' -> '.join(p['verbs']):<22} {field:<16} "
                + " -> ".join(h["path"][:34] for h in p["hops"]))
    else:
        token, src = get_token()
        if not token:
            log("\n⛔ no token. Set $PAM_API_TOKEN or create tools/.token")
            return 1
        hrs = token_hours_left(token)
        log(f"\n[3/5] TOKEN  {src}  valid {hrs:.2f} h")
        if hrs <= 0:
            log("⛔ token expired")
            return 1

        ok, detail = health_ok(base, token)
        log(f"      health probe: {detail}")
        if not ok:
            log("⛔ environment is not healthy - refusing to start. "
                "This is deliberate: two prior runs continued into an outage.")
            return 1

        # Evidence is RETAINED. This run writes into its own dated folder, so there is
        # nothing to clear and no earlier run can be destroyed.
        EVIDENCE.mkdir(parents=True, exist_ok=True)

        log(f"\n[4/5] EXECUTE {len(plans)} chains")
        for pi, p in enumerate(plans, 1):
            ctx: dict = {}
            hops_out = []
            for hi, ep in enumerate(p["hops"], 1):
                if calls >= args.max_calls:
                    log(f"      max-calls {args.max_calls} reached - stopping")
                    break
                body, injected = inject(ep.get("payload_template"), ctx) \
                    if ep["verb"] != "GET" else (None, [])
                path, pb, pu = bind_path(ep["path"], ctx)
                res = call(base, ep["verb"], path, body, token,
                           int(cfg.get("setAPIRequestTimeout_MS", 30000)) // 1000)
                calls += 1
                time.sleep(args.delay_ms / 1000)

                case = {"declared_codes": ["200"], "response_schema": None,
                        "_spec": {}, "_op": {}}
                val = validate(case, res)
                parsed = None
                try:
                    parsed = json.loads((res.get("body") or b"").decode("utf-8", "replace"))
                except Exception:                                    # noqa: BLE001
                    pass
                got = harvest(parsed) if parsed is not None else {}
                ctx.update(got)

                hops_out.append({
                    "n": hi, "verb": ep["verb"], "path": path,
                    "status": res.get("status"), "latency_ms": res.get("latency_ms"),
                    "body_bytes": res.get("body_bytes", 0),
                    "injected": injected, "path_bound": pb, "path_unbound": pu,
                    "harvested_count": len(got), "verdict": val["verdict"],
                    "fail_layers": val["fail_layers"],
                    "body_preview": (res.get("body") or b"")[:1200].decode("utf-8", "replace"),
                })
                if breaker.record(res.get("status"), res.get("error")):
                    log(f"      ⛔ CIRCUIT BREAKER: {args.breaker} consecutive failures - "
                        f"aborting to protect the environment")
                    break

            verdict = ("FAIL" if any(h["verdict"] == "FAIL" for h in hops_out)
                       else "WARN" if any(h["verdict"] == "WARN" for h in hops_out)
                       else "PASS" if hops_out else "NOT RUN")
            rec = {"plan_id": p["id"], "verdict": verdict, "hops": hops_out,
                   "fields": p["fields"], "verbs": p["verbs"],
                   "confidence": p["confidence"]}
            results.append(rec)
            (EVIDENCE / f"chain_{pi:04d}.json").write_text(
                json.dumps(rec, indent=2, default=str), encoding="utf-8")
            if pi % 10 == 0 or pi == len(plans):
                log(f"      {pi:>4}/{len(plans)}  last {verdict}")
            if breaker.tripped or calls >= args.max_calls:
                break

    log("\n[5/5] REPORT")
    lat = [h["latency_ms"] for r in results for h in r["hops"] if h["latency_ms"]]
    meta = {
        "Environment": "QA_MsSQL",
        "API base URL": base,
        "Generated (UTC)": started.strftime("%Y-%m-%d %H:%M:%S"),
        "Mode": "EXECUTE" if args.execute else "PLAN ONLY - no HTTP calls made",
        "Chain source": "artifacts/graph/api-graph/out/api-graph.json (auto-derived)",
        "Verbs allowed": ",".join(sorted(args.allow_verbs)),
        "Chain depth": args.depth,
        "Executable chains planned": len(plans),
        "Chains rejected by safety gate": len(rejected),
        "Chains executed": len(results),
        "HTTP calls made": calls,
        "Circuit breaker tripped": breaker.tripped,
        "Median hop latency ms": int(statistics.median(lat)) if lat else 0,
    }
    xlsx = write_report(plans, rejected, results, meta, args)
    log(f"      Excel -> {xlsx.relative_to(ROOT)}")
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    (RUN_DIR / "chain_results.json").write_text(
        json.dumps({"meta": meta,
                    "plans": [{k: v for k, v in p.items() if k != "hops"} | {
                        "paths": [h["path"] for h in p["hops"]]} for p in plans],
                    "results": results}, indent=1, default=str), encoding="utf-8")
    log("      JSON  -> artifacts/runs/<stamp>/chain_results.json")
    if results:
        log(f"      Evidence -> docs/findings/issues/Evidence/chains-qa_mssql/ ({len(results)})")

    log("\n" + "=" * 78)
    if args.execute:
        vd = Counter(r["verdict"] for r in results)
        log(f"CHAINS  PASS {vd.get('PASS',0)}  WARN {vd.get('WARN',0)}  "
            f"FAIL {vd.get('FAIL',0)}  of {len(results)}   ({calls} HTTP calls)")
        if breaker.tripped:
            log("!! run aborted early by the circuit breaker - results are partial")
    else:
        log(f"PLAN ONLY: {len(plans)} chains executable, {len(rejected)} rejected. "
            f"No HTTP calls were made.")
    log("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
