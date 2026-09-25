#!/usr/bin/env python3
"""PAM API chain runner - executes declarative multi-hop API flows against a live PAM
environment, carrying real values from one response into the next request.

Design intent
-------------
Flows are DATA (flows/*.json), not code. The executor is generic. That is what lets
dynamic generation evolve independently: a generator emits more flow JSON, and this
runner executes it unchanged. Hand-written flows and generated flows are the same shape,
so nothing scripted is thrown away when generation arrives.

Token safety
------------
The token is generated ONCE per run and cached to .token_cache.json until it expires.
Repeated /arcontoken calls locked the GenericScheduler account on 2026-07-28 (ISSUE-009);
that account is also the data-warehouse ETL service account, so a lockout reaches beyond
testing. Never call the token endpoint in a loop.

Output
------
Every run writes its own dated folder under artifacts/runs/<YYYY-MM-DD_HHMMSS>/.
Nothing is ever deleted. Secrets are redacted before anything is written to disk.

Usage
-----
    python tools/chain_runner.py --dry-run        # plan only, zero HTTP
    python tools/chain_runner.py --execute        # run every flow
    python tools/chain_runner.py --execute --flow user_lifecycle
    python tools/chain_runner.py --probe          # discover response shapes
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import random
import re
import ssl
import string
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

HERE = Path(__file__).resolve().parent

# token_guard is a sibling module. Put HERE on the path so this works whether the file
# is run as a script or imported from elsewhere in the workspace.
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import token_guard                                                       # noqa: E402


def _workspace_root(start: Path) -> Path:
    """Delegate to the one canonical resolver (`OBJ-025`).

    This used to search for a directory holding both Reports/ and the automation
    repo. That made two *content* folder names part of the executable interface,
    so renaming either broke seven scripts at once. paths.workspace_root() keys
    on CLAUDE.md + .claude/ instead, which the harness pins to the root."""
    return workspace_root(start)


ROOT = _workspace_root(HERE)
REPORTS = ROOT / "artifacts"   # OBJ-025: runs live at artifacts/runs
REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
ENV_FILE = REPO / "Environments" / "QA_MsSQL.properties"
FLOW_DIR = HERE / "flows"
RUNS = REPORTS / "Runs"
TOKEN_CACHE = HERE / ".token_cache.json"

ENV_NAME = "QA_MsSQL"
LATENCY_SLA_MS = 5000          # PAM writes are slow; 2000 was tuned for reads only
HTTP_TIMEOUT = 45
THROTTLE_S = 0.25
MAX_CALLS = 200
BREAKER_LIMIT = 3              # consecutive 5xx/timeouts before abort
BODY_CAP = 8 * 1024 * 1024

# Never built into a request, whatever a flow asks for. See ISSUE-010.
ENDPOINT_BLOCKLIST = {
    "GetLogs": "hangs 30s and stops the IIS app pool (ISSUE-010)",
    "GetErrorLogs": "hangs 30s and stops the IIS app pool (ISSUE-010)",
    "GetAllActiveUserDetails": "hung 30s on every version during the GET run",
}
DESTRUCTIVE = re.compile(
    r"^(delete|remove|drop|purge|reset|revoke|disable|deactivate|terminate|kill|wipe)", re.I)

SECRET_KEY = re.compile(r"(password|passwd|token|secret|credential)", re.I)

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def log(m=""):
    print(m, flush=True)


# --------------------------------------------------------------------------- config
def load_env() -> dict:
    cfg = {}
    for line in ENV_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()
    return cfg


def jwt_claims(tok: str) -> dict:
    try:
        p = tok.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))
    except Exception:                                                    # noqa: BLE001
        return {}


def get_token(cfg: dict, allow_network: bool) -> tuple[str | None, str]:
    """Cached-first, then ONE attempt. Delegates to token_guard — see that module.

    The attempt-once-then-latch policy lives in token_guard so every script shares one
    gate. A failed attempt blocks all later attempts until a human clears the latch;
    that is what stops "once per run" from becoming "every run" (ISSUE-009 §4a).

    ⛔ On a None return, STOP and report. Never loop back into this function.
    """
    return token_guard.acquire(cfg, allow_network=allow_network)


# ----------------------------------------------------------------------- redaction
def redact(obj):
    if isinstance(obj, dict):
        return {k: ("***REDACTED***" if SECRET_KEY.search(str(k)) else redact(v))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj


# ------------------------------------------------------------------ value plumbing
PLACEHOLDER = re.compile(r"\$\{([A-Za-z0-9_.]+)\}")


def rand_suffix(n=6) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))


def seed_vars() -> dict:
    """Per-run unique data, so a create never collides with a previous run."""
    s = rand_suffix()
    octet = random.randint(20, 250)
    return {
        "RUN_SUFFIX": s,
        "NEW_USERNAME": f"AUTO{s}",
        "NEW_USER_EMAIL": f"auto{s.lower()}@test.local",
        "NEW_USER_MOBILE": f"9{random.randint(100000000, 999999999)}",
        "NEW_USER_PASSWORD": f"Aut0!{s}",
        "NEW_SERVICE_HOST": f"10.11.0.{octet}",
        "NEW_SERVICE_USER": f"SVC{s}",
        "NEW_SERVICE_PASSWORD": f"Svc0!{s}",
        "NEW_SERVICE_PORT": str(random.randint(1024, 65000)),
    }


def substitute(node, vars: dict):
    """Replace ${NAME} anywhere in a body/path. A whole-string placeholder keeps the
    variable's native type, so an int id stays an int instead of becoming "1455"."""
    if isinstance(node, str):
        m = PLACEHOLDER.fullmatch(node)
        if m:
            return vars.get(m.group(1), node)
        return PLACEHOLDER.sub(lambda x: str(vars.get(x.group(1), x.group(0))), node)
    if isinstance(node, dict):
        return {k: substitute(v, vars) for k, v in node.items()}
    if isinstance(node, list):
        return [substitute(v, vars) for v in node]
    return node


def select(doc, path: str):
    """Dotted selector with [n] indices, e.g. Result[0].UserId. Case-insensitive on keys,
    because PAM spells the same field UserId / UserID / userid across controllers."""
    cur = doc
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        if cur is None:
            return None
        if part.startswith("["):
            i = int(part[1:-1])
            if not isinstance(cur, list) or i >= len(cur):
                return None
            cur = cur[i]
        elif isinstance(cur, dict):
            hit = next((k for k in cur if k.lower() == part.lower()), None)
            if hit is None:
                return None
            cur = cur[hit]
        else:
            return None
    return cur


def walk_dicts(node, depth=0):
    """Yield every dict anywhere in the document. PAM is inconsistent about whether a
    payload is enveloped, a bare array, or nested, so the search must not assume."""
    if depth > 12:
        return
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk_dicts(v, depth + 1)
    elif isinstance(node, list):
        for v in node:
            yield from walk_dicts(v, depth + 1)


def find_in(doc, container: str, field: str, value) -> dict | None:
    """Locate an object by a case-insensitive, type-loose field match.

    Tries the declared container first; if that is not a list (enveloped vs bare array
    vs Result-as-object all occur in this API) it falls back to a deep walk. Returning
    the matched record - not just True - is what makes the evidence file reviewable.
    """
    want = str(value).strip().casefold()
    if want in ("", "none"):
        return None

    def scan(items):
        for item in items:
            if not isinstance(item, dict):
                continue
            got = select(item, field)
            if got is not None and str(got).strip().casefold() == want:
                return item
        return None

    arr = select(doc, container) if container else doc
    if isinstance(arr, list):
        hit = scan(arr)
        if hit:
            return hit
    return scan(walk_dicts(doc))


# ---------------------------------------------------------------------- execution
class Breaker(Exception):
    pass


class Runner:
    def __init__(self, base: str, token: str, dry: bool, *, delay_s: float = THROTTLE_S,
                 max_calls: int = MAX_CALLS, allow_verbs=("GET", "POST"),
                 allow_teardown: bool = False, include_unsafe: bool = False,
                 downtime_wait_s: int = 300, downtime_retries: int = 3):
        self.base, self.token, self.dry = base.rstrip("/"), token, dry
        self.delay_s = delay_s
        self.max_calls = max_calls
        self.allow_verbs = {v.upper() for v in allow_verbs}
        self.allow_teardown = allow_teardown
        self.include_unsafe = include_unsafe
        self.downtime_wait_s = downtime_wait_s
        self.downtime_retries = downtime_retries
        self.calls = 0
        self.consecutive_fail = 0
        self.skipped = Counter()
        self.downtime_events = []

    def call(self, verb: str, path: str, body, *, teardown: bool = False,
             auth: str | None = None) -> dict:
        # Strip the query FIRST. A query string can itself contain "/" - one Excel row
        # carries a date (07/08/2059) in its query - and splitting on "/" first made the
        # "action" mid-query garbage. That name feeds the blocklist and destructive-name
        # guards, so getting it wrong is a safety bug, not just a cosmetic one. Measured
        # impact on the current corpus: 1 row, no guard decision changed.
        action = path.split("?")[0].rstrip("/").split("/")[-1]
        # Substring, not equality. ISSUE-010 records GetAllActiveUserDetails as hanging
        # "on every version", and GetAllActiveUserDetailsNew / ...Mapping are that same
        # family. An exact-match guard let those variants through.
        hit = next((k for k in ENDPOINT_BLOCKLIST if k.lower() in action.lower()), None)
        if hit and not self.include_unsafe:
            self.skipped[f"blocklist:{action}"] += 1
            return {"skipped": f"blocked: {ENDPOINT_BLOCKLIST[hit]} "
                               f"(matched '{hit}')", "status": None}
        if verb.upper() not in self.allow_verbs:
            self.skipped[f"verb-not-allowed:{verb.upper()}"] += 1
            return {"skipped": f"verb {verb.upper()} not in --allow-verbs",
                    "status": None}
        if DESTRUCTIVE.match(action) and not (teardown and self.allow_teardown):
            self.skipped[f"destructive:{action}"] += 1
            reason = ("teardown hop, but --allow-teardown was not passed" if teardown
                      else "destructive action name")
            return {"skipped": f"blocked: {reason}", "status": None}
        if self.calls >= self.max_calls:
            raise Breaker(f"max calls per run reached ({self.max_calls})")
        if self.dry:
            return {"skipped": "dry-run: no HTTP issued", "status": None}

        url = self.base + path
        data = None
        if isinstance(body, dict) and "__raw__" in body and len(body) == 1:
            # A payload the QA team authored as malformed JSON, e.g. `{SsoApiRefId:1,}`.
            # ApiHelper hands the raw String to Playwright's setData, so the server sees
            # it malformed - which for a negative row is the whole point. Re-encoding it
            # through json.dumps would repair it and silently destroy the test.
            data = str(body["__raw__"]).encode()
        elif body is not None:
            data = json.dumps(body).encode()
        out = {"url": url, "verb": verb, "status": None, "error": None, "body_bytes": 0}
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if auth == "invalid":
            # The QA team's *_UnauthorizedAccess tables assert 401 but carry no token
            # column, and the reference class sends the SAME valid token - so as authored
            # those 1,153 rows can never exercise unauthorized access. Supplying a bogus
            # credential here is what turns the assertion into a real test. This is a
            # syntactically shaped but meaningless string: no real credential is used, and
            # /arcontoken is never touched, so there is no lockout exposure.
            headers["Authorization"] = "Bearer invalid.token.obj010-unauthorized-probe"
            out["auth_mode"] = "invalid-credential"
        elif auth == "none":
            out["auth_mode"] = "no-authorization-header"
        else:
            headers["Authorization"] = f"Bearer {self.token}"
        t0 = time.time()
        try:
            req = urllib.request.Request(url, data=data, method=verb, headers=headers)
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT, context=SSL_CTX) as r:
                raw = r.read(BODY_CAP)
                out.update(status=r.status, raw=raw, body_bytes=len(raw),
                           content_type=(r.headers.get("Content-Type") or "").split(";")[0].strip())
        except urllib.error.HTTPError as e:
            raw = b""
            try:
                raw = e.read(BODY_CAP)
            except Exception:                                            # noqa: BLE001
                pass
            ct = (e.headers.get("Content-Type") if e.headers else "") or ""
            out.update(status=e.code, raw=raw, body_bytes=len(raw),
                       content_type=ct.split(";")[0].strip())
        except Exception as exc:                                         # noqa: BLE001
            out.update(status=None, raw=b"", error=f"{type(exc).__name__}: {exc}")

        out["latency_ms"] = int((time.time() - t0) * 1000)
        self.calls += 1

        bad = out["status"] is None or out["status"] >= 500
        self.consecutive_fail = self.consecutive_fail + 1 if bad else 0
        if self.consecutive_fail >= BREAKER_LIMIT:
            # Environment looks down. Wait, probe, and resume from THIS hop rather than
            # aborting the run - the caller re-issues the same call on success.
            if self._wait_out_downtime():
                out["recovered_after_downtime"] = True
            else:
                raise Breaker(
                    f"environment did not recover after {self.downtime_retries} waits of "
                    f"{self.downtime_wait_s}s - run paused, resume with --resume")

        try:
            out["json"] = json.loads(out["raw"].decode("utf-8", "replace"))
        except Exception:                                                # noqa: BLE001
            out["json"] = None
            out["text_head"] = out["raw"][:300].decode("utf-8", "replace")
        time.sleep(self.delay_s)
        return out

    def _health_ok(self) -> bool:
        try:
            req = urllib.request.Request(
                self.base + "/api/ADbridging/GetLOBList", data=b"{}", method="POST",
                headers={"Authorization": f"Bearer {self.token}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as r:
                return r.status == 200
        except Exception:                                                # noqa: BLE001
            return False

    def _wait_out_downtime(self) -> bool:
        """Pause on an outage, then continue where it stopped. Never restarts the run."""
        for attempt in range(1, self.downtime_retries + 1):
            log(f"    environment unhealthy ({self.consecutive_fail} consecutive "
                f"failures) - waiting {self.downtime_wait_s}s "
                f"[attempt {attempt}/{self.downtime_retries}]")
            self.downtime_events.append(
                {"attempt": attempt, "waited_s": self.downtime_wait_s})
            time.sleep(self.downtime_wait_s)
            if self._health_ok():
                log("    environment healthy again - resuming from the paused hop")
                self.consecutive_fail = 0
                return True
        return False


# --------------------------------------------------------------------- assertions
CREATED_MESSAGES = ("inserted", "created", "added", "saved", "success")
NOOP_MESSAGES = ("already exists", "duplicate")

# OBJ-010: the old rule was `str(err) in ("201","202","203")`, asserted hard. The real,
# measured code `206-LC_GLD` (HTTP 200, POST /api/Logs/GetLogDetails) would therefore be
# reported as a broken test. Match on the numeric prefix instead and treat an
# unrecognised value as an observation - the defect is the missing product registry, not
# the response. Mirrors com.arcon.utils.validation.ErrorCodeRegistry.
CODE_PREFIX = re.compile(r"^\s*(\d+)")


def error_code_prefix(value) -> str | None:
    """'206-LC_GLD' -> '206'; '201.0' -> '201'; 'oops' -> None."""
    if value is None:
        return None
    m = CODE_PREFIX.match(str(value))
    return m.group(1) if m else None


def assess(hop: dict, res: dict, extracted: dict) -> list[dict]:
    """Seven layers. A status check alone is not a test - PAM answers 200 for rejections,
    and answers Success:true for a create that inserted nothing."""
    checks = []

    def add(layer, name, ok, detail):
        checks.append({"layer": layer, "check": name,
                       "verdict": "PASS" if ok else "FAIL", "detail": detail})

    expected = hop.get("expect_status", 200)
    negative = bool(hop.get("negative"))
    want_code = hop.get("expect_error_code")
    add("L1", "http-status", res.get("status") == expected,
        f"expected {expected}, got {res.get('status')}"
        + (" (negative case: rejection is the pass condition)" if negative else ""))

    ct = res.get("content_type", "")
    if expected != 200:
        # 401 / 405 / 404 are framework-level rejections handled before the application
        # layer, so they carry neither a JSON envelope nor a JSON content type. Asserting
        # application/json here would fail a correctly rejected request.
        add("L2", "content-type", True,
            f"not applicable - HTTP {expected} is a framework-level rejection; got "
            f"{ct or '(none)'}")
    else:
        add("L2", "content-type", ct == "application/json", ct or "(none)")

    doc = res.get("json")
    if expected != 200:
        add("L3", "envelope", True,
            f"not applicable - no application envelope on an expected HTTP {expected}")
        add("L4", "message-semantics", True,
            f"not applicable - expected HTTP {expected}")
    elif isinstance(doc, list) and hop.get("envelope") is False:
        add("L3", "envelope", True, f"bare array by design, {len(doc)} items, no envelope")
        add("L4", "message-semantics", True, "not applicable - endpoint returns a bare array")
    elif not isinstance(doc, dict):
        add("L3", "envelope", False,
            f"expected a JSON object, got {type(doc).__name__}")
        add("L4", "message-semantics", False, "no envelope to read")
    else:
        success = select(doc, "Success")
        err = select(doc, "errorCode")
        got_code = error_code_prefix(err)
        if want_code is not None:
            # A negative row that names the code it expects: that IS the assertion.
            wc = error_code_prefix(want_code)
            add("L3", "envelope", got_code is not None and got_code == wc,
                f"expected errorCode {wc}, got {err!r}")
        elif negative:
            # Rejection expected at the application layer: Success:false or any
            # well-formed errorCode both count as a correct rejection.
            rejected = success is False or got_code is not None
            add("L3", "envelope", rejected,
                f"expected a rejection; Success={success!r} errorCode={err!r}")
        elif success is not None:
            add("L3", "envelope", success is True, f"Success={success!r}")
        elif err is not None:
            add("L3", "envelope", got_code is not None,
                f"errorCode={err!r}"
                + ("" if got_code else " - no numeric prefix, unrecognised shape"))
        else:
            add("L3", "envelope", False,
                f"neither Success nor errorCode present; keys={list(doc)[:8]}")

        raw_msg = select(doc, "Message")
        err_msg = select(doc, "ErrorMessage")
        msg = str(raw_msg if raw_msg is not None else "")
        low = msg.casefold()
        if negative:
            # For a negative case an ErrorMessage is the expected outcome, not a failure.
            add("L4", "message-semantics", True,
                f"negative case - ErrorMessage={err_msg!r} Message={msg!r}")
        elif hop.get("expect_created"):
            noop = any(n in low for n in NOOP_MESSAGES)
            made = any(c in low for c in CREATED_MESSAGES)
            add("L4", "message-semantics", made and not noop,
                f"Message={msg!r}" + (" -> nothing was created" if noop else ""))
        elif err_msg:
            add("L4", "message-semantics", False,
                f"ErrorMessage={err_msg!r} (HTTP {res.get('status')})")
        elif raw_msg is None:
            add("L4", "message-semantics", True,
                "no Message field on this endpoint - not applicable")
        else:
            add("L4", "message-semantics", bool(msg), f"Message={msg!r}")

    want = set(hop.get("extract", {})) | set(hop.get("find_extract", {}).get("take", {}))
    if hop.get("extract_any_id"):
        want.add(hop["extract_any_id"])
    missing = [k for k in want if extracted.get(k) in (None, "", [])]
    if want:
        add("L5", "chain-key-extracted", not missing,
            f"resolved {sorted(want - set(missing))}"
            + (f"; MISSING {missing}" if missing else ""))

    if hop.get("verify_present"):
        v = hop["verify_present"]
        add("L6", "record-exists", bool(res.get("_found")),
            f"searched {v['in']} for {v['match_field']}={v.get('_wanted')!r}"
            f" -> {'found' if res.get('_found') else 'NOT FOUND'}")
    elif hop.get("verify_value_anywhere"):
        add("L6", "record-exists", bool(res.get("_found")),
            f"{res.get('_verify_label', '')} -> "
            f"{'found' if res.get('_found') else 'NOT FOUND'}")

    lat = res.get("latency_ms", 0)
    sla = hop.get("sla_ms", LATENCY_SLA_MS)
    add("L7", "latency", lat <= sla, f"{lat} ms (SLA {sla} ms)")
    return checks


# --------------------------------------------------------------------------- flows
def load_flows(only: str | None = None, tier: int | None = None,
               controller: str | None = None) -> list[dict]:
    """Load every flow definition under flows/, including generated/ subdirectories.

    A file may hold a single flow object or a list of them, so a generator can emit one
    file per controller instead of hundreds of files.
    """
    flows = []
    for f in sorted(FLOW_DIR.rglob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        for d in (doc if isinstance(doc, list) else [doc]):
            d["_file"] = str(f.relative_to(FLOW_DIR))
            if only and d.get("id") != only:
                continue
            if tier is not None and int(d.get("tier", 1)) != tier:
                continue
            if controller and d.get("controller", "").lower() != controller.lower():
                continue
            flows.append(d)
    # hand-written flows first, then generated, tier order within
    flows.sort(key=lambda d: (bool(d.get("generated")), int(d.get("tier", 1)),
                              d.get("_file", ""), d.get("id", "")))
    return flows


ID_FIELD = re.compile(r"id$", re.I)


def any_id(doc):
    """First scalar field whose name ends in 'id', from Result[0] or Result.

    Generated flows cannot know whether a create returns UserId, ServiceId, LobId or
    MappingId, so the runner resolves it at execution time.
    """
    for container in ("Result[0]", "Result", ""):
        node = select(doc, container) if container else doc
        if isinstance(node, list):
            node = node[0] if node and isinstance(node[0], dict) else None
        if isinstance(node, dict):
            for k, v in node.items():
                if ID_FIELD.search(k) and isinstance(v, (str, int)) and str(v).strip():
                    return v, k
    return None, None


def value_anywhere(doc, value) -> dict | None:
    """Deep search for any object holding a scalar equal to `value`.

    The existence assertion for generated chains, where the field name carrying the id in
    the read-back is not known in advance.
    """
    want = str(value).strip().casefold()
    if want in ("", "none"):
        return None
    for node in walk_dicts(doc):
        for k, v in node.items():
            if isinstance(v, (str, int, float)) and str(v).strip().casefold() == want:
                return {"matched_field": k, "record": node}
    return None


def run_flow(flow: dict, runner: Runner, vars: dict, evidence_dir: Path, seq: list) -> dict:
    vars = dict(vars)
    result = {"id": flow["id"], "title": flow.get("title", ""), "hops": [],
              "verdict": "PASS", "note": ""}

    for i, hop in enumerate(flow["hops"], 1):
        path = substitute(hop["path"], vars)
        body = substitute(hop.get("body"), vars) if hop.get("body") is not None else None
        rec = {"n": i, "name": hop["name"], "verb": hop["verb"], "path": path,
               "extracted": {}, "checks": []}

        try:
            res = runner.call(hop["verb"], path, body,
                              teardown=bool(hop.get("teardown")),
                              auth=hop.get("auth"))
        except Breaker as b:
            rec["skipped"] = str(b)
            result["hops"].append(rec)
            result["verdict"] = "ABORTED"
            result["note"] = str(b)
            return result

        if res.get("skipped"):
            rec["skipped"] = res["skipped"]
            result["hops"].append(rec)
            # A skipped optional hop must not condemn the whole flow - only a skipped
            # mandatory hop does. Teardown and sweep hops are optional by construction.
            if hop.get("stop_on_fail", True) and not hop.get("teardown"):
                result["verdict"] = "BLOCKED"
                result["note"] = res["skipped"]
                return result
            result.setdefault("skipped_hops", []).append(
                {"hop": hop["name"], "reason": res["skipped"]})
            continue

        rec.update(status=res.get("status"), latency_ms=res.get("latency_ms"),
                   body_bytes=res.get("body_bytes"), error=res.get("error"),
                   content_type=res.get("content_type"))

        doc = res.get("json")
        casts = hop.get("cast", {})

        def store(name, val):
            if val is not None and casts.get(name) == "int":
                try:
                    val = int(str(val).strip())
                except (TypeError, ValueError):
                    pass
            if val is not None:
                vars[name] = val
            rec["extracted"][name] = val

        for name, sel in hop.get("extract", {}).items():
            store(name, select(doc, sel) if doc is not None else None)

        # extract_any_id: generated flows do not know whether the create returns UserId,
        # ServiceId or MappingId, so resolve the first id-shaped field at run time.
        if hop.get("extract_any_id") and doc is not None:
            val, field = any_id(doc)
            store(hop["extract_any_id"], val)
            rec["id_field_used"] = field

        # find_extract: locate a row in an array by a field match, then pull fields off it.
        # This is what makes a real join possible - e.g. the user group whose LOBName
        # equals the LOB name carried from the previous hop.
        fe = hop.get("find_extract")
        if fe and doc is not None:
            arr = select(doc, fe.get("in", "Result"))
            row = None
            if isinstance(arr, list):
                wanted = {k: str(substitute(v, vars)).strip().casefold()
                          for k, v in fe["where"].items()}
                for item in arr:
                    if not isinstance(item, dict):
                        continue
                    if all(str(select(item, k) or "").strip().casefold() == v
                           for k, v in wanted.items()):
                        row = item
                        break
            rec["matched_row"] = redact(row)
            rec["match_criteria"] = fe["where"]
            for name, field in fe["take"].items():
                store(name, select(row, field) if row else None)

        if hop.get("verify_present") and doc is not None:
            v = hop["verify_present"]
            wanted = substitute(v["value"], vars)
            v["_wanted"] = wanted
            hit = find_in(doc, v.get("in", ""), v["match_field"], wanted)
            res["_found"] = hit is not None
            rec["found_record"] = redact(hit) if hit else None

        # verify_value_anywhere: same assertion, but without needing the field name
        if hop.get("verify_value_anywhere") and doc is not None:
            v = hop["verify_value_anywhere"]
            wanted = substitute(v["value"], vars)
            hit = value_anywhere(doc, wanted)
            res["_found"] = hit is not None
            res["_verify_label"] = f"{v.get('label', 'value')}={wanted!r}"
            rec["found_record"] = redact(hit["record"]) if hit else None
            rec["matched_field"] = hit["matched_field"] if hit else None

        rec["checks"] = assess(hop, res, rec["extracted"])
        if any(c["verdict"] == "FAIL" for c in rec["checks"]):
            result["verdict"] = "FAIL"

        seq.append(1)
        # A hop name derived from an Excel endpoint cell can carry anything - query
        # strings, ':', '&', '%', even an embedded newline. Windows rejects those in a
        # filename with OSError 22, which killed a 3.5-hour run at hop 3391. The evidence
        # file must never be able to fail on the shape of a test's name.
        safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", str(hop["name"]))[:80]
        ev = evidence_dir / f"{len(seq):02d}_{flow['id']}_{safe_name}.json"
        ev.write_text(json.dumps({
            "flow": flow["id"], "hop": hop["name"], "verb": hop["verb"], "url": res.get("url"),
            "request_body": redact(body), "status": res.get("status"),
            "latency_ms": res.get("latency_ms"), "content_type": res.get("content_type"),
            "response": redact(doc) if doc is not None else res.get("text_head"),
            "transport_error": res.get("error"),
            "extracted": redact(rec["extracted"]), "checks": rec["checks"],
        }, indent=1, default=str), encoding="utf-8")
        rec["evidence"] = ev.name
        result["hops"].append(rec)

        if hop.get("stop_on_fail", True) and result["verdict"] == "FAIL":
            result["note"] = f"stopped after hop {i} ({hop['name']}) failed"
            return result

    result["vars"] = redact(vars)
    return result


# --------------------------------------------------------------------------- probe
PROBE = [
    ("POST", "/api/Logs/GetLogDetails", {"LogTypeId": 1}),
    ("POST", "/api/Logs/GetLogDetails", {"LogTypeId": 2}),
    ("POST", "/api/Logs/GetLogDetails", {"LogTypeId": 3}),
]

# Envelope fields are reported by VALUE, not by type - the value is the finding.
KEEP_VALUE = re.compile(
    r"^(Program|Version|Success|Message|ErrorCode|ErrorMessage|errorCode|StatusCode)$", re.I)


def shape(doc, depth=0):
    if isinstance(doc, dict):
        out = {}
        for k, v in list(doc.items())[:14]:
            out[k] = v if (KEEP_VALUE.match(str(k)) and not isinstance(v, (dict, list))) \
                else shape(v, depth + 1)
        return out
    if isinstance(doc, list):
        return [shape(doc[0], depth + 1), f"...{len(doc)} items"] if doc else []
    return type(doc).__name__


def probe(runner: Runner, out_dir: Path) -> list[dict]:
    rows = []
    for verb, path, body in PROBE:
        try:
            res = runner.call(verb, path, body)
        except Breaker as b:
            rows.append({"path": path, "verb": verb, "note": str(b)})
            break
        row = {"verb": verb, "path": path, "status": res.get("status"),
               "latency_ms": res.get("latency_ms"), "bytes": res.get("body_bytes"),
               "skipped": res.get("skipped"), "error": res.get("error")}
        doc = res.get("json")
        row["message"] = select(doc, "Message") if isinstance(doc, dict) else None
        row["shape"] = shape(redact(doc)) if doc is not None else res.get("text_head")
        rows.append(row)
        log(f"  {verb:4} {path:58} {row['status']}  {row['latency_ms']}ms  "
            f"{row.get('message')}")
    (out_dir / "probe.json").write_text(json.dumps(rows, indent=1, default=str),
                                       encoding="utf-8")
    return rows


# -------------------------------------------------------------------------- report
def write_report(run_dir: Path, meta: dict, results: list[dict], probe_rows: list) -> None:
    L = []
    A = L.append
    total = len(results)
    tally = Counter(r["verdict"] for r in results)
    icon = {"PASS": "✅ PASS", "FAIL": "⛔ FAIL", "BLOCKED": "🟡 BLOCKED",
            "ABORTED": "⚠️ ABORTED"}
    hops = [h for r in results for h in r["hops"]]
    executed = [h for h in hops if not h.get("skipped")]
    endpoints = {h["path"].split("?")[0] for h in executed}
    layer_fail = Counter(c["check"] for h in executed for c in h.get("checks", [])
                         if c["verdict"] == "FAIL")

    A("# API Chain Execution — Run Report")
    A("")
    A(f"**Run:** `{meta['stamp']}` · **Environment:** `{meta['env']}` — {meta['base']}")
    A(f"**Mode:** {meta['mode']} · **Token:** {meta['token_src']} · "
      f"**Elapsed:** {meta.get('elapsed_s', 0) // 60} min {meta.get('elapsed_s', 0) % 60} s")
    A(f"**Verbs:** {', '.join(meta.get('verbs', []))} · "
      f"**Teardown:** {'enabled' if meta.get('teardown_allowed') else 'disabled'} · "
      f"**Unsafe endpoints:** {'included' if meta.get('unsafe_included') else 'excluded'}")
    A(f"**Flows:** {total} · **Hops:** {len(hops)} ({len(executed)} executed) · "
      f"**HTTP calls:** {meta['calls']} · **Distinct endpoints reached:** {len(endpoints)}")
    A("")
    A("---")
    A("")
    A("## 1. Verdict")
    A("")
    A("| Verdict | Flows |")
    A("|---|---:|")
    for k in ("PASS", "FAIL", "BLOCKED", "ABORTED"):
        if tally.get(k):
            A(f"| {icon[k]} | {tally[k]} |")
    A(f"| **Total** | **{total}** |")
    A("")
    if layer_fail:
        A("**Failures by layer** — which check caught them:")
        A("")
        A("| Layer check | Hops failing |")
        A("|---|---:|")
        for k, v in layer_fail.most_common():
            A(f"| `{k}` | {v} |")
        A("")

    A("## 2. Coverage by controller")
    A("")
    by_ctrl = defaultdict(lambda: {"flows": 0, "pass": 0, "hops": 0, "eps": set()})
    for r in results:
        c = r.get("controller") or r["id"].split("__")[0]
        by_ctrl[c]["flows"] += 1
        by_ctrl[c]["pass"] += 1 if r["verdict"] == "PASS" else 0
        for h in r["hops"]:
            by_ctrl[c]["hops"] += 1
            if not h.get("skipped"):
                by_ctrl[c]["eps"].add(h["path"].split("?")[0])
    A("| Controller | Flows | Passed | Hops | Endpoints reached |")
    A("|---|---:|---:|---:|---:|")
    for c, v in sorted(by_ctrl.items()):
        A(f"| `{c}` | {v['flows']} | {v['pass']} | {v['hops']} | {len(v['eps'])} |")
    A("")

    A("## 3. Flow results")
    A("")
    A("| Flow | Tier | Hops | Verdict | Note |")
    A("|---|---:|---:|---|---|")
    for r in results:
        A(f"| `{r['id']}` | {r.get('tier', 1)} | {len(r['hops'])} | "
          f"{icon.get(r['verdict'], r['verdict'])} | {(r.get('note') or '—')[:70]} |")
    A("")

    failed = [r for r in results if r["verdict"] in ("FAIL", "ABORTED")]
    A(f"## 4. Failure detail ({len(failed)} flows)")
    A("")
    if not failed:
        A("No flow failed.")
        A("")
    for r in failed:
        A(f"### `{r['id']}` — {r.get('title', '')}")
        A("")
        A("| Hop | Verb | Endpoint | Status | ms | Failing layers | Evidence |")
        A("|---:|---|---|---:|---:|---|---|")
        for h in r["hops"]:
            if h.get("skipped"):
                A(f"| {h['n']} | {h['verb']} | `{h['path']}` | — | — | "
                  f"{h['skipped']} | — |")
                continue
            f = [c for c in h.get("checks", []) if c["verdict"] == "FAIL"]
            A(f"| {h['n']} | {h['verb']} | `{h['path']}` | {h.get('status')} | "
              f"{h.get('latency_ms')} | "
              f"{', '.join(f'`{c[chr(99)+chr(104)+chr(101)+chr(99)+chr(107)]}`' for c in f) or '—'} | "
              f"`{h.get('evidence', '—')}` |")
        A("")
        for h in r["hops"]:
            f = [c for c in h.get("checks", []) if c["verdict"] == "FAIL"]
            if not f:
                continue
            A(f"**Hop {h['n']} — {h['name']}**")
            A("")
            A("| Layer | Check | Detail |")
            A("|---|---|---|")
            for c in f:
                A(f"| {c['layer']} | `{c['check']}` | {c['detail']} |")
            A("")

    A("## 5. Exclusions — nothing is silently skipped")
    A("")
    sk = meta.get("skipped") or {}
    if sk:
        A("| Reason | Hops |")
        A("|---|---:|")
        for k, v in sorted(sk.items(), key=lambda t: -t[1]):
            A(f"| `{k}` | {v} |")
    else:
        A("No hop was excluded.")
    A("")
    if meta.get("downtime_events"):
        A(f"**Downtime pauses:** {len(meta['downtime_events'])} — the run waited and "
          f"resumed from the paused hop rather than restarting.")
        A("")

    if probe_rows:
        A("## 6. Shape probe")
        A("")
        A("| Verb | Endpoint | Status | ms | Message |")
        A("|---|---|---:|---:|---|")
        for p in probe_rows:
            A(f"| {p.get('verb')} | `{p.get('path')}` | {p.get('status')} | "
              f"{p.get('latency_ms')} | {p.get('message') or p.get('skipped') or '—'} |")
        A("")
        A("Full shapes in `probe.json`.")
        A("")

    A("## 7. Provenance")
    A("")
    A("| | |")
    A("|---|---|")
    A("| Runner | `tools/chain_runner.py` |")
    A("| Hand-written flows | `tools/flows/*.json` |")
    A("| Generated flows | `tools/flows/generated/*.json`, from "
      "`generate_flows.py` |")
    A("| Machine-readable results | `results.json` in this folder |")
    A("| Checkpoint | `checkpoint.json` — resume with `--execute --resume <folder>` |")
    A("| Evidence | `evidence/` — one JSON per hop, secrets redacted |")
    A("| Retention | This folder is never deleted or overwritten |")
    A("")
    A("Secrets (`password`, `token`, `secret`, `credential` keys) are replaced with "
      "`***REDACTED***` before anything reaches disk.")

    (run_dir / "RUN_REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--execute", action="store_true", help="issue real HTTP calls")
    g.add_argument("--dry-run", action="store_true", help="plan only (default)")
    ap.add_argument("--probe", action="store_true",
                    help="also probe reference endpoints and record their shapes")
    ap.add_argument("--flow", help="run a single flow by id")
    ap.add_argument("--tier", type=int, help="run only flows of this tier")
    ap.add_argument("--controller", help="run only flows for this controller")
    ap.add_argument("--delay-ms", type=int, default=5000,
                    help="pause between calls (default 5000)")
    ap.add_argument("--budget-seconds", type=int,
                    help="if set, the delay is recomputed each hop to finish inside this "
                         "window, with a 250 ms floor")
    ap.add_argument("--max-calls", type=int, default=20000)
    ap.add_argument("--allow-verbs", default="GET,POST",
                    help="comma-separated verbs to permit (default GET,POST)")
    ap.add_argument("--allow-teardown", action="store_true",
                    help="permit teardown hops, which remove records this run created")
    ap.add_argument("--allow-preexisting-teardown", action="store_true",
                    help="DANGEROUS: also permit destructive calls against records this "
                         "run did not create. Not needed for coverage")
    ap.add_argument("--include-unsafe", action="store_true",
                    help="include GetLogs/GetErrorLogs/GetAllActiveUserDetails, which "
                         "stop the IIS application pool (ISSUE-010)")
    ap.add_argument("--downtime-wait", type=int, default=300,
                    help="seconds to wait for recovery before resuming (default 300)")
    ap.add_argument("--resume", help="run folder to resume; completed flows are skipped")
    ap.add_argument("--wait-for-env", type=int, default=0, metavar="MINUTES",
                    help="before starting, poll until the environment answers, for up to "
                         "this many minutes. Lets a run be queued while the host is down")
    args = ap.parse_args()
    dry = not args.execute

    cfg = load_env()
    base = cfg.get("pam_BaseAPIURL", "")
    if args.resume:
        run_dir = Path(args.resume)
        if not run_dir.is_absolute():
            run_dir = RUNS / args.resume
        if not run_dir.is_dir():
            log(f"⛔ resume folder not found: {run_dir}")
            return 2
        stamp = run_dir.name
    else:
        stamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d_%H%M%S")
        run_dir = RUNS / stamp
    evidence = run_dir / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)

    ckpt_file = run_dir / "checkpoint.json"
    done: dict[str, dict] = {}
    if args.resume and ckpt_file.exists():
        ckpt = json.loads(ckpt_file.read_text(encoding="utf-8")).get("flows", [])
        # An ABORTED flow reached the checkpoint without executing - the environment never
        # came back inside 3 waits. Treating it as "done" would skip it permanently on
        # resume, which silently loses coverage. Re-queue it instead.
        aborted = [r["id"] for r in ckpt if r.get("verdict") == "ABORTED"]
        done = {r["id"]: r for r in ckpt if r.get("verdict") != "ABORTED"}
        log(f"resuming {stamp}: {len(done)} flows already complete, they will be skipped")
        if aborted:
            log(f"  re-queueing {len(aborted)} ABORTED flow(s) - they never executed: "
                f"{aborted[:8]}")

    log(f"PAM chain runner — {ENV_NAME} — {base}")
    log(f"mode: {'DRY-RUN (no HTTP)' if dry else 'EXECUTE'}   run folder: "
        f"{run_dir.relative_to(ROOT)}")
    log("")

    token, src = get_token(cfg, allow_network=not dry)
    if not dry and not token:
        log(f"⛔ no token: {src}")
        return 2
    log(f"token: {src}")
    if token:
        c = jwt_claims(token)
        log(f"  role={c.get('http://schemas.microsoft.com/ws/2008/06/identity/claims/role')} "
            f"APIUserId={c.get('APIUserId')} exp={c.get('exp')}")
    log("")

    runner = Runner(base, token or "", dry,
                    delay_s=args.delay_ms / 1000.0,
                    max_calls=args.max_calls,
                    allow_verbs=[v.strip() for v in args.allow_verbs.split(",") if v.strip()],
                    allow_teardown=args.allow_teardown or args.allow_preexisting_teardown,
                    include_unsafe=args.include_unsafe,
                    downtime_wait_s=args.downtime_wait)
    if args.allow_preexisting_teardown:
        global DESTRUCTIVE
        DESTRUCTIVE = re.compile(r"^(?!)")          # matches nothing: all names permitted
        log("⚠️  --allow-preexisting-teardown: destructive calls are NOT restricted to "
            "records this run created")
    log(f"verbs: {sorted(runner.allow_verbs)}   teardown: {runner.allow_teardown}   "
        f"delay: {args.delay_ms} ms   unsafe endpoints: {runner.include_unsafe}")

    if not dry and args.wait_for_env:
        deadline = time.time() + args.wait_for_env * 60
        waited = 0
        while not runner._health_ok():
            if time.time() >= deadline:
                log(f"⛔ environment still unreachable after {args.wait_for_env} min "
                    f"- nothing was executed. Re-run when the host is back.")
                return 3
            log(f"    environment unreachable, waited {waited // 60} min of "
                f"{args.wait_for_env} - probing again in 60s")
            time.sleep(60)
            waited += 60
        if waited:
            log(f"    environment answered after {waited // 60} min - starting")
    vars = seed_vars()
    log("per-run seed data:")
    for k, v in vars.items():
        log(f"  {k:20} {v}")
    log("")

    probe_rows = []
    if args.probe:
        log("shape probe:")
        probe_rows = probe(runner, run_dir)
        log("")

    flows = (load_flows(args.flow, args.tier, args.controller)
             if FLOW_DIR.exists() else [])
    if not flows and not args.probe:
        log(f"⛔ no flow definitions found in {FLOW_DIR}")
        return 2

    pending = [f for f in flows if f.get("id") not in done]
    total_hops = sum(len(f["hops"]) for f in pending)
    log(f"flows: {len(flows)} loaded, {len(done)} already done, {len(pending)} to run "
        f"({total_hops} hops)")
    log("")

    results, seq = list(done.values()), []
    started = time.time()
    hops_done = 0

    def checkpoint():
        ckpt_file.write_text(json.dumps(
            {"stamp": stamp, "updated_after_flows": len(results), "flows": results},
            indent=1, default=str), encoding="utf-8")

    for i, fl in enumerate(pending, 1):
        # Dynamic pacing: keep the whole run inside --budget-seconds if one was given.
        if args.budget_seconds and hops_done:
            left_hops = max(1, total_hops - hops_done)
            left_time = args.budget_seconds - (time.time() - started)
            per_hop = left_time / left_hops
            observed = (time.time() - started) / hops_done - runner.delay_s
            runner.delay_s = max(0.25, min(30.0, per_hop - max(0.0, observed)))

        log(f"[{i}/{len(pending)}] {fl['id']} — {fl.get('title', '')}"
            + (f"   (delay {runner.delay_s:.2f}s)" if args.budget_seconds else ""))
        try:
            r = run_flow(fl, runner, vars, evidence, seq)
        except Breaker as b:
            log(f"  ⛔ run paused: {b}")
            checkpoint()
            log(f"  resume with: --execute --resume {stamp}")
            break
        hops_done += len(r["hops"])
        for h in r["hops"]:
            fails = [c for c in h.get("checks", []) if c["verdict"] == "FAIL"]
            log(f"  hop {h['n']} {h['verb']:4} {h['path'][:52]:52} "
                f"{h.get('status') or h.get('skipped', '')}  "
                f"{'' if not fails else '⛔ ' + ', '.join(c['check'] for c in fails)}")
        log(f"  verdict: {r['verdict']}  {r['note']}")
        log("")
        results.append(r)
        checkpoint()

    meta = {"stamp": stamp, "env": ENV_NAME, "base": base, "token_src": src,
            "calls": runner.calls,
            "mode": "DRY-RUN (no HTTP issued)" if dry else "EXECUTE (live)",
            "elapsed_s": int(time.time() - started),
            "verbs": sorted(runner.allow_verbs),
            "teardown_allowed": runner.allow_teardown,
            "unsafe_included": runner.include_unsafe,
            "delay_ms_final": int(runner.delay_s * 1000),
            "skipped": dict(runner.skipped),
            "downtime_events": runner.downtime_events}
    (run_dir / "results.json").write_text(
        json.dumps({"meta": meta, "seed": redact(vars), "flows": results},
                   indent=1, default=str), encoding="utf-8")
    write_report(run_dir, meta, results, probe_rows)

    log(f"report:   {(run_dir / 'RUN_REPORT.md').relative_to(ROOT)}")
    log(f"evidence: {len(list(evidence.glob('*.json')))} files")
    if dry:
        return 0                       # a plan is not a failure
    return 0 if all(r["verdict"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
