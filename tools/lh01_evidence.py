#!/usr/bin/env python3
"""LH-01 evidence builder - HTTP 200 returned for application-level failures.

Extracts every call from a completed chain_runner run that returned HTTP 200 while
carrying an application-level failure in the body, classifies each one against the
server's own error-code taxonomy, and emits the Jira evidence pack.

Why a separate script rather than a report tweak
------------------------------------------------
This is the template for the remaining 11 developer loopholes. The selector (what
counts as "affected") is the only loophole-specific part; everything below the
SELECTOR section is generic and is meant to be reused unchanged.

Optional live re-validation (--revalidate) replays a representative sample against
the live environment to confirm the defect is still present today. It reuses
chain_runner.get_token, so the token is fetched ONCE and cached - repeated
/arcontoken calls locked the GenericScheduler service account on 2026-07-28
(ISSUE-009). Never put this in a loop.

Usage
-----
    python tools/lh01_evidence.py                  # build pack, zero HTTP
    python tools/lh01_evidence.py --revalidate     # + live re-check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chain_runner import (  # noqa: E402
    ENDPOINT_BLOCKLIST, DESTRUCTIVE, SSL_CTX, ROOT, REPORTS,
    get_token, load_env, redact,
)

RUN_ID = "2026-07-29_181439"
RUN_DIR = REPORTS / "Runs" / RUN_ID
OUT_DIR = ROOT / "artifacts" / "loopholes" / "LH-01-http-200-application-failures"
DATA_DIR = OUT_DIR / "data"

REVALIDATE_MAX_CALLS = 24        # default sample; --full replays every affected call
REVALIDATE_THROTTLE_S = 0.35
HTTP_TIMEOUT = 45

# The server's own error-code prefix taxonomy, recovered from live traffic.
# This is the heart of the finding: the API already classifies every failure,
# the classification simply never reaches the HTTP status line.
TAXONOMY = {
    "103": ("Input parameter null/missing", "400 Bad Request"),
    "104": ("Input parameter invalid", "400 Bad Request"),
    "201": ("Validation error", "400 Bad Request"),
    "203": ("Parameter error", "400 Bad Request"),
    "204": ("No record found", "404 Not Found"),
    "206": ("Parameter error", "400 Bad Request"),
    "902": ("System error", "500 Internal Server Error"),
    "903": ("System error / database exception", "500 Internal Server Error"),
    "NONE": ("Failure with no ErrorCode emitted", "400 Bad Request"),
    "NONNUMERIC": ("Failure with unparseable ErrorCode", "400 Bad Request"),
}
# Leaked-internals detector: .NET stack frames, build-server paths, assembly info.
LEAK = re.compile(
    r"(System\.[A-Za-z]+Exception|\bat\s+[A-Za-z]+(\.[A-Za-z0-9_]+)+\s*\(|"
    r"[A-Z]:\\\\?Jenkins\\|StackTrace|InnerException|Culture=neutral)", re.I)


def prefix_of(code) -> str:
    if code is None or str(code).strip() == "":
        return "NONE"
    m = re.match(r"\s*(\d{3})", str(code))
    return m.group(1) if m else "NONNUMERIC"


def malformed(code) -> str:
    """Formatting defects in the code itself - these block a machine-readable register."""
    if code is None or str(code).strip() == "":
        return "absent"
    s = str(code)
    flaws = []
    if s != s.strip():
        flaws.append("leading/trailing whitespace")
    if "\n" in s or len(s) > 40:
        flaws.append("stack trace concatenated into the code")
    if re.match(r"^\s*\d{3}[A-Za-z]", s):
        flaws.append("missing separator after numeric prefix")
    if re.match(r"^\s*\d{3}\s+-", s) or re.match(r"^\s*\d{3}\s", s.rstrip()):
        flaws.append("space inside the prefix separator")
    if s.rstrip().endswith("-"):
        flaws.append("trailing separator")
    if not re.match(r"^\s*\d{3}", s):
        flaws.append("no numeric prefix")
    return "; ".join(flaws) or "well-formed"


# ------------------------------------------------------------------- SELECTOR (LH-01)
def is_affected(hop: dict, response) -> bool:
    """LH-01: HTTP 200 on the wire, application-level failure in the body."""
    if hop.get("status") != 200:
        return False
    return any(c["check"] == "envelope" and "Success=False" in c["detail"]
               for c in hop.get("checks", []))


# ------------------------------------------------------------------------ extraction
def load_evidence(name):
    p = RUN_DIR / "evidence" / name if name else None
    if not p or not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except Exception:                                                    # noqa: BLE001
        return {}


def extract() -> list[dict]:
    results = json.loads((RUN_DIR / "results.json").read_text(encoding="utf-8"))
    rows = []
    for flow in results["flows"]:
        for hop in flow["hops"]:
            ev = load_evidence(hop.get("evidence"))
            resp = ev.get("response")
            if not is_affected(hop, resp):
                continue
            r = resp if isinstance(resp, dict) else {}
            code = r.get("ErrorCode", r.get("errorCode"))
            msg = r.get("ErrorMessage", r.get("errorMessage"))
            pfx = prefix_of(code)
            checks = {c["check"]: c for c in hop.get("checks", [])}
            path = hop.get("path", "")
            parts = path.split("/")
            rows.append({
                "flow": flow["id"],
                "flow_title": flow.get("title", ""),
                "hop": hop.get("n"),
                "controller": parts[2] if len(parts) > 2 else "",
                "action": hop.get("name", ""),
                "verb": hop.get("verb", ""),
                "path": path,
                "http_status": hop.get("status"),
                "success_flag": False,
                "error_code": None if code is None else str(code).split("\n")[0][:80],
                "error_code_raw_len": 0 if code is None else len(str(code)),
                "error_class": pfx,
                "error_class_meaning": TAXONOMY.get(pfx, ("unclassified", "400 Bad Request"))[0],
                "correct_http_status": TAXONOMY.get(pfx, ("", "400 Bad Request"))[1],
                "code_format": malformed(code),
                "error_message": (str(msg).replace("\r", " ").replace("\n", " ")[:300]
                                  if msg is not None else None),
                "leaks_internals": bool(LEAK.search(str(code) + " " + str(msg))),
                "latency_ms": hop.get("latency_ms"),
                "body_bytes": hop.get("body_bytes"),
                "content_type": hop.get("content_type"),
                "l3_envelope": checks.get("envelope", {}).get("verdict"),
                "l4_message": checks.get("message-semantics", {}).get("verdict"),
                "request_body": ev.get("request_body"),
                "url": ev.get("url"),
                "evidence_file": hop.get("evidence"),
            })
    return rows


# ----------------------------------------------------------------- live re-validation
def pick_sample(rows: list[dict], full: bool = False) -> list[dict]:
    """One representative per error class, then widen by controller, honouring the
    blocklist and refusing anything whose action name reads destructive.

    With full=True every affected call is replayed. That is safe here specifically
    because each of these requests already FAILED on 2026-07-29 - they are rejected
    on validation or fault before touching state, so replaying them reproduces the
    rejection rather than mutating anything. The blocklist and the destructive-name
    guard still apply."""
    def safe(r):
        return (r["action"] not in ENDPOINT_BLOCKLIST
                and not DESTRUCTIVE.match(r["action"])
                and r["verb"] in ("GET", "POST"))

    pool = [r for r in rows if safe(r)]
    if full:
        return pool

    chosen, seen_ctrl = [], set()
    for cls in sorted({r["error_class"] for r in pool}):
        for r in pool:
            if r["error_class"] == cls:
                chosen.append(r)
                seen_ctrl.add(r["controller"])
                break
    for r in pool:
        if len(chosen) >= REVALIDATE_MAX_CALLS:
            break
        if r["controller"] not in seen_ctrl:
            chosen.append(r)
            seen_ctrl.add(r["controller"])
    return chosen[:REVALIDATE_MAX_CALLS]


def call(url: str, verb: str, body, token: str) -> dict:
    # Headers must match chain_runner.call() exactly, including Content-Type on a
    # bodyless GET. Omitting it makes six ADbridging GETs answer 415 instead of the
    # 200 they returned in the source run - a replay artifact that would read as a
    # fix. Fidelity to the original request is the whole point of a re-validation.
    data = None if body is None else json.dumps(body).encode()
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json",
               "Accept": "application/json"}
    req = urllib.request.Request(url, data=data, method=verb, headers=headers)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT, context=SSL_CTX) as r:
            raw = r.read().decode("utf-8", "replace")
            status, ctype = r.status, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        status, ctype = e.code, e.headers.get("Content-Type", "")
    except Exception as exc:                                             # noqa: BLE001
        return {"transport_error": f"{type(exc).__name__}: {exc}",
                "latency_ms": int((time.time() - t0) * 1000)}
    out = {"status": status, "content_type": ctype,
           "latency_ms": int((time.time() - t0) * 1000)}
    try:
        out["response"] = json.loads(raw)
    except Exception:                                                    # noqa: BLE001
        out["response"] = raw[:1000]
    return out


def revalidate(rows: list[dict], full: bool = False) -> dict:
    cfg = load_env()
    token, src = get_token(cfg, allow_network=True)
    if not token:
        return {"ok": False, "reason": f"token unavailable - {src}"}
    print(f"  token: {src}")

    sample = pick_sample(rows, full=full)
    skipped = len(rows) - len(sample)
    print(f"  replaying {len(sample)} calls"
          + (f" (FULL - {skipped} skipped by blocklist/destructive guard)" if full
             else f" (representative sample, cap {REVALIDATE_MAX_CALLS})") + "\n")
    out = []
    for i, r in enumerate(sample, 1):
        res = call(r["url"], r["verb"], r["request_body"], token)
        resp = res.get("response")
        rd = resp if isinstance(resp, dict) else {}
        succ = rd.get("Success", rd.get("success"))
        code = rd.get("ErrorCode", rd.get("errorCode"))
        still = res.get("status") == 200 and succ is False
        out.append({
            "controller": r["controller"], "action": r["action"], "verb": r["verb"],
            "path": r["path"], "error_class": r["error_class"],
            "then_status": 200, "then_code": r["error_code"],
            "now_status": res.get("status"), "now_success": succ,
            "now_code": None if code is None else str(code).split("\n")[0][:80],
            "now_message": (str(rd.get("ErrorMessage", rd.get("errorMessage", "")))
                            .replace("\n", " ")[:200] or None),
            "still_reproduces": still,
            "latency_ms": res.get("latency_ms"),
            "transport_error": res.get("transport_error"),
            "raw_response": redact(resp) if isinstance(resp, (dict, list)) else resp,
        })
        flag = "REPRODUCED" if still else f"changed -> HTTP {res.get('status')}"
        print(f"  [{i:2d}/{len(sample)}] {r['controller']}/{r['action']:<34s} {flag}")
        time.sleep(REVALIDATE_THROTTLE_S)

    repro = sum(1 for o in out if o["still_reproduces"])
    changed = [o for o in out if not o["still_reproduces"]]
    return {"ok": True, "token_src": src, "mode": "full" if full else "sample",
            "attempted": len(out), "reproduced": repro,
            "not_reproduced": len(changed), "skipped_by_guard": skipped,
            "attempted_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "calls": out}


# --------------------------------------------------------------------------- writers
def md_escape(s) -> str:
    if s is None:
        return "—"
    return str(s).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip() or "—"


def write_evidence_md(payload: dict) -> Path:
    rows = payload["rows"]
    reval = payload.get("revalidation")
    by_class = Counter(r["error_class"] for r in rows)
    by_ctrl = Counter(r["controller"] for r in rows)
    # A code is only "real" if it is present and non-blank; 5 responses emit null and
    # 2 emit "", and counting those as distinct codes would inflate the register.
    codes = Counter(r["error_code"] for r in rows if r["error_code"])
    no_code = sum(1 for r in rows if not r["error_code"])
    four = sum(v for k, v in by_class.items()
               if TAXONOMY.get(k, ("", "4"))[1].startswith(("400", "404")))
    five = len(rows) - four
    lat = sorted(r["latency_ms"] for r in rows if r["latency_ms"] is not None)
    leaks = [r for r in rows if r["leaks_internals"]]

    L = []
    a = L.append
    a("# LH-01 Evidence — HTTP 200 Returned for Application-Level Failures")
    a("")
    a(f"**Loophole:** 1 of 12 · **Severity:** 🔴 Critical · **Environment:** `QA_MsSQL` — "
      f"`https://u16hf.arconnet.com:6302`")
    a(f"**Source run:** `{payload['source_run']}` — 1,868 live calls, 2026-07-29 · "
      f"**Evidence:** one JSON file per call, retained")
    a(f"**Affected:** **{payload['affected_calls']} calls** across "
      f"**{payload['distinct_endpoints']} distinct endpoints** in "
      f"**{payload['distinct_controllers']} controllers**")
    a(f"**Generated:** {payload['generated_utc']}")
    a("")
    a("---")
    a("")
    a("## 1. The defect")
    a("")
    a("The API returns **HTTP 200 OK** on the wire while the response body reports a hard "
      "application-level failure. The transport layer and the application layer disagree.")
    a("")
    a("```http")
    a("HTTP/1.1 200 OK")
    a("Content-Type: application/json")
    a("")
    a('{ "Program": "ARCON PAM API", "Version": "1.0", "DateTime": "29/Jul/2026 07:13:24",')
    a('  "Success": false, "ErrorCode": "103-ADB-SGL", "ErrorMessage": "Input parameter is null" }')
    a("```")
    a("")
    a("Any client that branches on the status code — our test suite, the PAM UI, a partner "
      "integration, a load balancer health check, an APM tool — records this as a success.")
    a("")
    a("| Measure | Value |")
    a("|---|---:|")
    a("| Calls in the run | 1,868 |")
    a("| Returned HTTP 200 | 1,688 |")
    a(f"| …of which carried `Success: false` | **{payload['affected_calls']}** |")
    a(f"| Distinct endpoints affected | **{payload['distinct_endpoints']}** |")
    a(f"| Distinct controllers affected | **{payload['distinct_controllers']}** |")
    a(f"| Distinct `ErrorCode` values observed | **{len(codes)}** |")
    a(f"| …plus responses emitting no usable `ErrorCode` | {no_code} |")
    a("| Status-only suite would score this run | **90% green** |")
    a("| True pass rate under full validation | **64%** |")
    a("")
    a("---")
    a("")
    a("## 2. The server already classifies every failure")
    a("")
    a("This is the key finding, and it is what makes the fix mechanical rather than a redesign. "
      "Every `ErrorCode` carries a **three-digit prefix that already encodes the failure class**. "
      "That classification is computed server-side and then discarded before the status line is "
      "written.")
    a("")
    a("| Prefix | Meaning (from observed messages) | Calls | Correct HTTP status |")
    a("|---|---|---:|---|")
    for cls in sorted(by_class, key=lambda c: (-by_class[c], c)):
        meaning, correct = TAXONOMY.get(cls, ("unclassified", "400 Bad Request"))
        label = "*(none emitted)*" if cls == "NONE" else (
            "*(unparseable)*" if cls == "NONNUMERIC" else f"`{cls}`")
        a(f"| {label} | {meaning} | {by_class[cls]} | `{correct}` |")
    a("")
    a(f"**Collapsed:** {four} calls should be **4xx** (client error), {five} should be "
      f"**5xx** (server fault). No call in this set is a legitimate 200.")
    a("")
    a("A single mapping applied where the envelope is serialised resolves all "
      f"{payload['affected_calls']} — the taxonomy above is the whole specification.")
    a("")
    a("---")
    a("")
    a("## 3. Blast radius by controller")
    a("")
    a("| Controller | Affected calls | Share |")
    a("|---|---:|---:|")
    for c, n in by_ctrl.most_common():
        a(f"| `{c}` | {n} | {n / len(rows) * 100:.1f}% |")
    a("")
    fam = sum(1 for r in rows if r["controller"].startswith(("ServiceDetails", "UserDetails")))
    a(f"The `ServiceDetails*` and `UserDetails*` families account for **{fam} of the "
      f"{len(rows)}** affected calls ({fam / len(rows) * 100:.0f}%). Those are the "
      "highest-traffic controllers in the product, and each exists in up to four versioned "
      "copies that behave identically — so a fix at the envelope layer covers all versions "
      "at once.")
    a("")
    a("---")
    a("")
    a("## 4. Secondary defects found inside the same responses")
    a("")
    a(f"### 4.1 Internal server detail leaked to the caller ({len(leaks)} calls)")
    a("")
    a("Some failures return a full .NET stack trace, including **build-server absolute paths**, "
      "source file names, line numbers and assembly versions — at HTTP 200, to any "
      "authenticated caller.")
    a("")
    if leaks:
        a("```")
        sample = str(leaks[0]["error_message"])[:400]
        a(sample)
        a("```")
        a("")
        a("| Controller | Action | Leaked content |")
        a("|---|---|---|")
        for r in leaks:
            what = []
            blob = f"{r['error_code']} {r['error_message']}"
            if "Jenkins" in blob:
                what.append("build path")
            if "System." in blob:
                what.append("exception type")
            if re.search(r"\.cs:line", blob):
                what.append("source line")
            if "Culture=neutral" in blob:
                what.append("assembly version")
            a(f"| `{r['controller']}` | `{r['action']}` | {', '.join(what) or 'stack frame'} |")
        a("")
    a("One of these is a genuine deployment fault, not a data problem: "
      "`ServicePassword/GetTargetDeviceOpenSSHKey` reports "
      "`Could not load file or assembly 'ChilkatDotNet47, Version=9.5.0.86'` — a **missing "
      "binary on the QA server**, returned as HTTP 200.")
    a("")
    a("### 4.2 The `ErrorCode` field is not machine-readable")
    a("")
    a(f"{len(codes)} distinct codes were observed, and a further {no_code} responses failed "
      "while emitting no usable code at all (5 `null`, 2 empty string). The framework "
      "recognises three (`201`, `202`, `203`); the Confluence reference documents four. "
      "Beyond the volume, the codes are not consistently formed:")
    a("")
    a("| Format defect | Calls | Example |")
    a("|---|---:|---|")
    fmt = Counter(r["code_format"] for r in rows)
    for k, n in fmt.most_common():
        if k == "well-formed":
            continue
        ex = next(r["error_code"] for r in rows if r["code_format"] == k)
        a(f"| {k} | {n} | `{md_escape(ex)}` |")
    a(f"| well-formed | {fmt.get('well-formed', 0)} | `203-ULC-GUL` |")
    a("")
    a("Variants observed for what appear to be the same class: `201-UDC-…`, `201SDC-GSDBI` "
      "(no separator), `203 -ULC-GUL` (space), `203-ACC-GAC-` (trailing dash), "
      "`GSAPLR` (no numeric prefix). A client cannot parse these with one rule.")
    a("")
    a("### 4.3 Message punctuation is unstable")
    a("")
    a("`\"System error has occurred\"` and `\"System error has occurred.\"` are both emitted for "
      "the same condition, as are `\"Parameter error occurred-\"` and "
      "`\"Parameter error occurred - \"`. Clients that string-match — which this contract forces "
      "them to do — break on the difference.")
    a("")
    a("---")
    a("")
    a("## 5. Performance note")
    a("")
    a(f"These failures are not fast rejections. Median latency **{lat[len(lat)//2]} ms**, "
      f"p95 **{lat[int(len(lat)*.95)]} ms**, max **{lat[-1]} ms**. The server does the full "
      "work, fails, and then reports success.")
    a("")
    a("---")
    a("")
    a("## 6. Live re-validation")
    a("")
    if reval and reval.get("ok"):
        full = reval.get("mode") == "full"
        when = str(reval.get("attempted_utc", ""))[:10]
        a(f"Replayed **every affected call** against live `QA_MsSQL` on **{when}**, using the "
          "same request body, verb and headers as the source run."
          if full else
          f"Re-ran a representative sample against `QA_MsSQL` on {when}.")
        a("")
        n, tot = reval["reproduced"], reval["attempted"]
        a(f"### ✅ {n} of {tot} still reproduce ({n / tot * 100:.1f}%)")
        a("")
        a("| Measure | Result |")
        a("|---|---|")
        a(f"| Calls replayed | {tot} |")
        a(f"| Still returning HTTP 200 with `Success: false` | **{n}** |")
        a(f"| No longer reproducing | {reval.get('not_reproduced', 0)} |")
        same = sum(1 for c in reval["calls"] if c["then_code"] == c["now_code"])
        a(f"| Returning the identical `ErrorCode` two days later | {same} of {tot} |")
        a("")
        drift = [c for c in reval["calls"] if c["then_code"] != c["now_code"]]
        if drift:
            a("**Error-code drift.** The same request now reports a different code on "
              f"{len(drift)} endpoint(s) — the failure is unchanged, only its label moved. "
              "That is further evidence the code register is not stable enough to branch on:")
            a("")
            a("| Endpoint | 2026-07-29 | Now |")
            a("|---|---|---|")
            for c in drift:
                a(f"| `{c['controller']}/{c['action']}` | `{md_escape(c['then_code'])}` | "
                  f"`{md_escape(c['now_code'])}` |")
            a("")
        a("**The platform is capable of correct status codes.** During an earlier replay pass "
          "that omitted `Content-Type: application/json`, six of these same endpoints answered "
          "**HTTP 415 Unsupported Media Type** — correctly. The framework returns a proper 4xx "
          "for a transport-level problem and a 200 for an application-level failure. The 200 is "
          "therefore an application-layer choice, not a platform constraint.")
        a("")
        a("Per-call detail below, and in the `Re-validation` sheet of the workbook.")
        a("")
        a("| Controller | Action | Class | Then | Now | Reproduces |")
        a("|---|---|---|---|---|---|")
        for c in reval["calls"]:
            now = (f"HTTP {c['now_status']} / Success={c['now_success']}"
                   if not c["transport_error"] else c["transport_error"])
            a(f"| `{c['controller']}` | `{c['action']}` | `{c['error_class']}` | "
              f"HTTP 200 / Success=false | {now} | "
              f"{'✅ yes' if c['still_reproduces'] else '🟡 changed'} |")
    else:
        reason = (reval or {}).get("reason", "not attempted in this build")
        a("⛔ **Blocked — not re-validated live.**")
        a("")
        a(f"> `{md_escape(reason)}`")
        a("")
        a("The `GenericScheduler` service account used for API token generation is **locked** "
          "(ISSUE-009). Exactly **one** token request was issued and no retry was attempted: "
          "that account is also the data-warehouse ETL service account, so repeated attempts "
          "reach past testing.")
        a("")
        a("This does not weaken the finding. All figures above come from **1,868 captured "
          "responses** taken on 2026-07-29 against this same environment, each retained as an "
          "individual evidence file. Re-validation is a freshness check, not the basis of the "
          "claim.")
        a("")
        a("**To complete it once the account is unlocked** — a single command, one token, "
          "24 calls, read-only:")
        a("")
        a("```powershell")
        a("python tools\\lh01_evidence.py --revalidate")
        a("```")
    a("")
    a("---")
    a("")
    a("## 7. Full affected-call register")
    a("")
    a(f"All {payload['affected_calls']} calls, grouped by failure class. `Evidence` names the "
      f"retained response file under `artifacts/runs/{payload['source_run']}/evidence/`.")
    a("")
    for cls in sorted(by_class, key=lambda c: (-by_class[c], c)):
        meaning, correct = TAXONOMY.get(cls, ("unclassified", "400 Bad Request"))
        head = (f"Class `{cls}` — {meaning}" if cls not in ("NONE", "NONNUMERIC")
                else meaning)
        n = by_class[cls]
        a(f"### {head} → should be `{correct}` ({n} call{'s' if n != 1 else ''})")
        a("")
        a("| # | Controller | Action | Verb | ErrorCode | ErrorMessage | ms | Evidence |")
        a("|---:|---|---|---|---|---|---:|---|")
        for i, r in enumerate([x for x in rows if x["error_class"] == cls], 1):
            a(f"| {i} | `{r['controller']}` | `{r['action']}` | {r['verb']} | "
              f"`{md_escape(r['error_code'])}` | {md_escape(r['error_message'])[:150]} | "
              f"{r['latency_ms']} | `{md_escape(r['evidence_file'])}` |")
        a("")
    a("---")
    a("")
    a("## 8. Reproducing this evidence")
    a("")
    a("```powershell")
    a("# rebuild this pack from the retained run - zero HTTP calls")
    a("python tools\\lh01_evidence.py")
    a("")
    a("# add a live re-check of a 24-call sample (needs an unlocked service account)")
    a("python tools\\lh01_evidence.py --revalidate")
    a("```")
    a("")
    a(f"Raw extract: `data/lh01-affected-calls.json` · "
      f"Source responses: `artifacts/runs/{payload['source_run']}/evidence/`")
    a("")

    p = OUT_DIR / "EVIDENCE.md"
    p.write_text("\n".join(L), encoding="utf-8")
    return p


def write_evidence_xlsx(payload: dict) -> Path:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    rows = payload["rows"]
    HDR = PatternFill("solid", fgColor="1F3864")
    HF = Font(color="FFFFFF", bold=True, size=10)
    TITLE = Font(bold=True, size=13, color="1F3864")
    RED = PatternFill("solid", fgColor="FCE4E4")
    AMBER = PatternFill("solid", fgColor="FFF2CC")
    wb = Workbook()

    def sheet(name, headers, data, widths, note=None):
        ws = wb.create_sheet(name)
        r0 = 1
        if note:
            ws.cell(1, 1, note).font = Font(italic=True, size=9, color="666666")
            r0 = 2
        for c, h in enumerate(headers, 1):
            cell = ws.cell(r0, c, h)
            cell.fill, cell.font = HDR, HF
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        for i, row in enumerate(data, r0 + 1):
            for c, v in enumerate(row, 1):
                ws.cell(i, c, v).alignment = Alignment(vertical="top", wrap_text=(c == len(row)))
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w
        ws.freeze_panes = ws.cell(r0 + 1, 1)
        ws.auto_filter.ref = (f"A{r0}:{get_column_letter(len(headers))}"
                              f"{r0 + len(data)}")
        ws.row_dimensions[r0].height = 30
        return ws

    # ---- Summary
    ws = wb.active
    ws.title = "Summary"
    ws["A1"] = "LH-01 — HTTP 200 Returned for Application-Level Failures"
    ws["A1"].font = TITLE
    meta = [
        ("Loophole", "1 of 12"), ("Severity", "Critical"),
        ("Environment", "QA_MsSQL — https://u16hf.arconnet.com:6302"),
        ("Source run", payload["source_run"]),
        ("Run date", "2026-07-29"), ("Generated", payload["generated_utc"]),
        ("", ""),
        ("Calls in run", 1868), ("Returned HTTP 200", 1688),
        ("…carrying Success: false", payload["affected_calls"]),
        ("Distinct endpoints affected", payload["distinct_endpoints"]),
        ("Distinct controllers affected", payload["distinct_controllers"]),
        ("Distinct ErrorCode values", len({r["error_code"] for r in rows if r["error_code"]})),
        ("Responses with no usable ErrorCode", sum(1 for r in rows if not r["error_code"])),
        ("Responses leaking internals", sum(1 for r in rows if r["leaks_internals"])),
        ("", ""),
        ("Status-only suite would score", "90% green"),
        ("True pass rate (7-layer)", "64%"),
        ("", ""),
        ("Should be 4xx", sum(1 for r in rows
                              if r["correct_http_status"].startswith(("400", "404")))),
        ("Should be 5xx", sum(1 for r in rows
                              if r["correct_http_status"].startswith("500"))),
    ]
    for i, (k, v) in enumerate(meta, 3):
        ws.cell(i, 1, k).font = Font(bold=True, size=10)
        ws.cell(i, 2, v)
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 52

    # ---- Taxonomy
    by_class = Counter(r["error_class"] for r in rows)
    tx = [(c if c not in ("NONE", "NONNUMERIC") else f"({c.lower()})",
           TAXONOMY.get(c, ("unclassified", ""))[0], by_class[c],
           TAXONOMY.get(c, ("", "400 Bad Request"))[1])
          for c in sorted(by_class, key=lambda x: (-by_class[x], x))]
    w = sheet("Taxonomy & Fix", ["Code prefix", "Meaning", "Calls", "Correct HTTP status"],
              tx, [16, 42, 10, 30],
              note="The server already classifies every failure. This mapping is the "
                   "complete specification for the fix.")
    for i in range(len(tx)):
        w.cell(i + 3, 4).fill = RED if str(tx[i][3]).startswith("500") else AMBER

    # ---- Affected calls
    hdr = ["#", "Controller", "Action", "Verb", "Path", "HTTP", "Correct HTTP",
           "Class", "ErrorCode", "Code format", "ErrorMessage", "Leaks internals",
           "Latency ms", "Bytes", "Flow", "Hop", "Evidence file"]
    data = [[i, r["controller"], r["action"], r["verb"], r["path"], r["http_status"],
             r["correct_http_status"], r["error_class"], r["error_code"], r["code_format"],
             r["error_message"], "YES" if r["leaks_internals"] else "", r["latency_ms"],
             r["body_bytes"], r["flow"], r["hop"], r["evidence_file"]]
            for i, r in enumerate(rows, 1)]
    w = sheet("Affected Calls", hdr, data,
              [5, 20, 34, 6, 46, 7, 24, 8, 22, 30, 66, 14, 11, 9, 30, 6, 46],
              note=f"All {len(rows)} calls that returned HTTP 200 with an "
                   f"application-level failure in the body.")
    for i, r in enumerate(rows):
        if r["leaks_internals"]:
            w.cell(i + 3, 12).fill = RED

    # ---- Error code register
    reg = defaultdict(lambda: {"n": 0, "eps": set(), "msg": "", "cls": "", "fmt": ""})
    for r in rows:
        k = r["error_code"] or "(none)"
        e = reg[k]
        e["n"] += 1
        e["eps"].add(f"{r['controller']}/{r['action']}")
        e["cls"] = r["error_class"]
        e["fmt"] = r["code_format"]
        if not e["msg"]:
            e["msg"] = r["error_message"]
    regrows = [[k, v["cls"], TAXONOMY.get(v["cls"], ("", "400 Bad Request"))[1], v["n"],
                len(v["eps"]), v["fmt"], v["msg"], ", ".join(sorted(v["eps"])[:6])]
               for k, v in sorted(reg.items(), key=lambda kv: -kv[1]["n"])]
    sheet("Error Code Register",
          ["ErrorCode", "Class", "Correct HTTP status", "Calls", "Endpoints",
           "Format defect", "Sample message", "Emitting endpoints (first 6)"],
          regrows, [30, 9, 26, 8, 11, 34, 60, 70],
          note="Every distinct ErrorCode observed. The framework recognises only "
               "201/202/203; the Confluence reference documents four codes in total.")

    # ---- By controller
    bc = Counter(r["controller"] for r in rows)
    ctrl = [[c, n, f"{n / len(rows) * 100:.1f}%",
             len({r["action"] for r in rows if r["controller"] == c}),
             ", ".join(sorted({r["error_class"] for r in rows if r["controller"] == c}))]
            for c, n in bc.most_common()]
    sheet("By Controller",
          ["Controller", "Affected calls", "Share", "Distinct actions", "Classes seen"],
          ctrl, [30, 15, 10, 17, 30])

    # ---- Leaked internals
    lk = [[r["controller"], r["action"], r["path"], r["error_code"],
           (r["error_message"] or "")[:300]]
          for r in rows if r["leaks_internals"]]
    if lk:
        sheet("Leaked Internals",
              ["Controller", "Action", "Path", "ErrorCode", "Leaked message (truncated)"],
              lk, [22, 34, 48, 30, 110],
              note="Responses exposing .NET exception types, build-server paths, source "
                   "file line numbers or assembly versions — at HTTP 200.")

    # ---- Reproduction
    rep = []
    for cls in sorted(by_class, key=lambda c: (-by_class[c], c)):
        r = next(x for x in rows if x["error_class"] == cls)
        body = json.dumps(r["request_body"]) if r["request_body"] is not None else "(no body)"
        rep.append([cls, TAXONOMY.get(cls, ("", ""))[0], r["verb"], r["path"],
                    body[:300], "200", r["error_code"], r["correct_http_status"],
                    r["evidence_file"]])
    sheet("Reproduction",
          ["Class", "Meaning", "Verb", "Path", "Request body", "Observed HTTP",
           "ErrorCode", "Expected HTTP", "Evidence file"],
          rep, [9, 34, 6, 46, 60, 14, 24, 26, 46],
          note="One reproducible case per failure class. Send the body to the path with a "
               "valid bearer token; observe HTTP 200 with Success:false.")

    # ---- Revalidation
    reval = payload.get("revalidation")
    if reval and reval.get("ok"):
        rv = [[c["controller"], c["action"], c["error_class"], "HTTP 200 / Success=false",
               f"HTTP {c['now_status']} / Success={c['now_success']}", c["now_code"],
               c["now_message"], "YES" if c["still_reproduces"] else "changed",
               c["latency_ms"]] for c in reval["calls"]]
        sheet("Re-validation",
              ["Controller", "Action", "Class", "2026-07-29", "Live now", "ErrorCode now",
               "Message now", "Reproduces", "ms"], rv,
              [22, 34, 9, 26, 30, 24, 60, 13, 8],
              note=f"Live replay. {reval['reproduced']} of {reval['attempted']} reproduce.")
    else:
        ws = wb.create_sheet("Re-validation")
        ws["A1"] = "Live re-validation — BLOCKED"
        ws["A1"].font = TITLE
        ws["A3"] = "Reason"
        ws["A3"].font = Font(bold=True)
        ws["B3"] = (reval or {}).get("reason", "not attempted")
        ws["A4"] = "Detail"
        ws["A4"].font = Font(bold=True)
        ws["B4"] = ("The GenericScheduler API service account is locked (ISSUE-009). One "
                    "token request was issued; no retry was attempted because that account "
                    "is also the data-warehouse ETL service account.")
        ws["A5"] = "Impact on this finding"
        ws["A5"].font = Font(bold=True)
        ws["B5"] = ("None. All figures come from 1,868 captured responses (2026-07-29), each "
                    "retained as an individual evidence file.")
        ws["A6"] = "To complete"
        ws["A6"].font = Font(bold=True)
        ws["B6"] = "python tools\\lh01_evidence.py --revalidate"
        ws.column_dimensions["A"].width = 24
        ws.column_dimensions["B"].width = 100
        for r_ in range(3, 7):
            ws.cell(r_, 2).alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r_].height = 46

    p = OUT_DIR / "EVIDENCE.xlsx"
    wb.save(p)
    return p


# ----------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--revalidate", action="store_true",
                    help="replay against the live environment")
    ap.add_argument("--full", action="store_true",
                    help="with --revalidate, replay every affected call instead of a "
                         "representative sample")
    args = ap.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"LH-01 evidence builder\n  source run: {RUN_ID}")
    rows = extract()
    print(f"  affected calls: {len(rows)}")
    print(f"  distinct endpoints: {len({(r['controller'], r['action']) for r in rows})}")

    payload = {
        "loophole": "LH-01",
        "title": "HTTP 200 returned for application-level failures",
        "source_run": RUN_ID,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "affected_calls": len(rows),
        "distinct_endpoints": len({(r["controller"], r["action"]) for r in rows}),
        "distinct_controllers": len({r["controller"] for r in rows}),
        "by_error_class": dict(sorted(Counter(r["error_class"] for r in rows).items())),
        "rows": rows,
    }

    # A prior attempt is retained on disk so its outcome survives a rebuild. Without
    # this, re-running without --revalidate would silently drop the record of a blocked
    # attempt, and the only way to restore it would be another token call.
    attempt_file = DATA_DIR / "revalidation-attempt.json"
    if args.revalidate:
        print("\nLive re-validation against QA_MsSQL")
        result = revalidate(rows, full=args.full)
        attempt_file.write_text(json.dumps(result, indent=1, default=str), encoding="utf-8")
        payload["revalidation"] = result
    elif attempt_file.exists():
        payload["revalidation"] = json.loads(attempt_file.read_text(encoding="utf-8"))
        print(f"  re-validation: loaded prior attempt "
              f"({'ok' if payload['revalidation'].get('ok') else 'BLOCKED'})")

    (DATA_DIR / "lh01-affected-calls.json").write_text(
        json.dumps(payload, indent=1, default=str), encoding="utf-8")

    md = write_evidence_md(payload)
    xl = write_evidence_xlsx(payload)
    print("\nwrote:")
    for p in (DATA_DIR / "lh01-affected-calls.json", md, xl):
        print(f"  {p.relative_to(ROOT)}  ({p.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
