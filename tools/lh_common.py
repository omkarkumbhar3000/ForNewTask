#!/usr/bin/env python3
"""Shared engine for the artifacts/loopholes evidence packs (LH-02 … LH-12).

LH-01 was built by lh01_evidence.py, one bespoke script. That does not scale to twelve,
so everything that was generic in it lives here and each loophole supplies only what is
genuinely specific: a selector, a classification table, and its narrative.

What is generic
---------------
    RunData        load results.json + evidence/*.json once, share the cache
    Safety         blocklist / destructive-name guard / replay caps
    replay()       live re-validation, token from PAM_API_TOKEN, never /arcontoken
    MD             small markdown document builder
    Xlsx           workbook builder with consistent styling
    build_pack()   orchestrates: select -> classify -> replay -> write

What each loophole supplies (see lh_specs.py)
---------------------------------------------
    LoopholeSpec.select(hop, response)  -> bool
    LoopholeSpec.classify(row)          -> class key
    LoopholeSpec.TAXONOMY               -> {class: (meaning, expected behaviour)}
    LoopholeSpec.narrative(ctx, md)     -> writes the prose sections
    LoopholeSpec.sheets(ctx)            -> extra workbook sheets

⛔ Safety. Some loopholes must never be replayed live - LH-08 stops the IIS application
pool. A spec declares revalidate="forbidden" and replay() refuses regardless of flags.
"""
from __future__ import annotations

import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based
from typing import Callable

HERE = Path(__file__).resolve().parent


def _workspace_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "CLAUDE.md").is_file() and (p / ".claude").is_dir():
            return p
    raise SystemExit(f"cannot locate the workspace root above {start}")


ROOT = _workspace_root(HERE)
REPORTS = ROOT / "artifacts"   # OBJ-025: runs live at artifacts/runs
REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
PACKS = ROOT / "artifacts" / "loopholes"
RUN_ID = "2026-07-29_181439"
RUN_DIR = REPORTS / "Runs" / RUN_ID

ENVIRONMENT = "QA_MsSQL"
API_BASE = "https://u16hf.arconnet.com:6302"
APP_BASE = "https://u16hf.arconnet.com:1302"
BUILD = "35.8.29 hf12"

HTTP_TIMEOUT = 45
REPLAY_THROTTLE_S = 0.35
REPLAY_BODY_CAP = 2 * 1024 * 1024        # one response is 8 MB; do not hold it all

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Mirrors chain_runner. Never built into a request, whatever a spec asks for.
ENDPOINT_BLOCKLIST = {
    "GetLogs": "hangs 30s and stops the IIS app pool (ISSUE-010)",
    "GetErrorLogs": "hangs 30s and stops the IIS app pool (ISSUE-010)",
    "GetAllActiveUserDetails": "hung 30s on every version during the GET run",
}
DESTRUCTIVE = re.compile(
    r"^(delete|remove|drop|purge|reset|revoke|disable|deactivate|terminate|kill|wipe)", re.I)
# Actions that change state despite a safe-looking verb. LH-06 exists because of these.
MUTATING_NAME = re.compile(
    r"^(set|insert|add|create|update|save|edit|modify|assign|import|upload|generate|"
    r"approve|reject|map|unmap)", re.I)
SECRET_KEY = re.compile(r"(password|passwd|pwd|token|secret|credential|privatekey|sshkey)", re.I)
LEAK = re.compile(
    r"(System\.[A-Za-z]+Exception|\bat\s+[A-Za-z][\w.]+\s*\(|[A-Z]:\\+Jenkins\\|"
    r"StackTrace|InnerException|Culture=neutral|\.cs:line)", re.I)


def redact(obj):
    if isinstance(obj, dict):
        return {k: ("***REDACTED***" if SECRET_KEY.search(str(k)) else redact(v))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj


# --------------------------------------------------------------------------- run data
class RunData:
    """Loads the source run once. Evidence files are ~1,868 small JSONs; reading them
    per-loophole would mean twelve full passes, so the cache is shared."""

    _instances: dict[str, "RunData"] = {}

    def __init__(self, run_id: str = RUN_ID):
        self.run_id = run_id
        run_dir = REPORTS / "Runs" / run_id
        self.results = json.loads((run_dir / "results.json").read_text(encoding="utf-8"))
        self.hops = []
        for flow in self.results["flows"]:
            for hop in flow["hops"]:
                self.hops.append((flow, hop))
        self._ev: dict[str, dict] = {}
        for _, hop in self.hops:
            name = hop.get("evidence")
            if not name or name in self._ev:
                continue
            p = run_dir / "evidence" / name
            if p.exists():
                try:
                    self._ev[name] = json.loads(p.read_text(encoding="utf-8",
                                                            errors="replace"))
                except Exception:                                        # noqa: BLE001
                    self._ev[name] = {}

    @classmethod
    def get(cls, run_id: str = RUN_ID) -> "RunData":
        """Cached per run id. LH-01…12 are pinned to 2026-07-29_181439 so their published
        figures stay reproducible; LH-13 sources OBJ-010's run instead."""
        if run_id not in cls._instances:
            cls._instances[run_id] = cls(run_id)
        return cls._instances[run_id]

    def evidence(self, hop) -> dict:
        return self._ev.get(hop.get("evidence") or "", {})

    def response(self, hop):
        return self.evidence(hop).get("response")


def controller_of(path: str) -> str:
    parts = (path or "").split("/")
    return parts[2] if len(parts) > 2 else ""


def base_row(flow, hop, ev) -> dict:
    """Fields every pack wants, so no spec has to re-derive them."""
    checks = {c["check"]: c for c in hop.get("checks", [])}
    return {
        "flow": flow["id"],
        "flow_title": flow.get("title", ""),
        "hop": hop.get("n"),
        "controller": controller_of(hop.get("path", "")),
        "action": hop.get("name", ""),
        "verb": hop.get("verb", ""),
        "path": hop.get("path", ""),
        "url": ev.get("url"),
        "http_status": hop.get("status"),
        "latency_ms": hop.get("latency_ms"),
        "body_bytes": hop.get("body_bytes"),
        "content_type": hop.get("content_type"),
        "request_body": ev.get("request_body"),
        "l1": checks.get("http-status", {}).get("verdict"),
        "l3": checks.get("envelope", {}).get("verdict"),
        "l4": checks.get("message-semantics", {}).get("verdict"),
        "evidence_file": hop.get("evidence"),
    }


# ----------------------------------------------------------------------- live replay
def _token() -> tuple[str | None, str]:
    t = os.environ.get("PAM_API_TOKEN", "").strip()
    if t:
        return t, "$PAM_API_TOKEN"
    return None, ("no token - set $PAM_API_TOKEN. /arcontoken is NOT used: the "
                  "GenericScheduler service account is locked (ISSUE-009)")


def call(url: str, verb: str, body, token: str) -> dict:
    """Headers match chain_runner exactly, including Content-Type on a bodyless GET -
    omitting it makes some endpoints answer 415 instead of the 200 they really return."""
    data = None if body is None else json.dumps(body).encode()
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json",
               "Accept": "application/json"}
    req = urllib.request.Request(url, data=data, method=verb, headers=headers)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT, context=SSL_CTX) as r:
            raw = r.read(REPLAY_BODY_CAP)
            status, ctype = r.status, r.headers.get("Content-Type", "")
            truncated = len(raw) >= REPLAY_BODY_CAP
    except urllib.error.HTTPError as e:
        raw = e.read(REPLAY_BODY_CAP)
        status, ctype, truncated = e.code, e.headers.get("Content-Type", ""), False
    except Exception as exc:                                             # noqa: BLE001
        return {"transport_error": f"{type(exc).__name__}: {exc}",
                "latency_ms": int((time.time() - t0) * 1000)}
    out = {"status": status, "content_type": ctype, "body_bytes": len(raw),
           "truncated": truncated, "latency_ms": int((time.time() - t0) * 1000)}
    text = raw.decode("utf-8", "replace")
    try:
        out["response"] = json.loads(text)
    except Exception:                                                    # noqa: BLE001
        out["response"] = text[:2000]
    return out


def replay(spec: "LoopholeSpec", rows: list[dict], limit: int | None) -> dict:
    """Live re-validation. Refuses outright when the spec forbids it."""
    if spec.revalidate == "forbidden":
        return {"ok": False, "refused": True,
                "reason": f"live replay is FORBIDDEN for {spec.lh_id}: "
                          f"{spec.revalidate_note}"}
    if spec.revalidate == "static":
        return {"ok": False, "static": True,
                "reason": f"{spec.lh_id} is derived from static analysis; there is "
                          f"nothing to call"}

    token, src = _token()
    if not token:
        return {"ok": False, "reason": src}

    def safe(r):
        if r["action"] in ENDPOINT_BLOCKLIST:
            return False
        if DESTRUCTIVE.match(r["action"]):
            return False
        if spec.replay_excludes_mutating and MUTATING_NAME.match(r["action"]):
            return False
        if spec.replay_filter and not spec.replay_filter(r):
            return False
        return r["verb"] in ("GET", "POST")

    pool = [r for r in rows if safe(r)]
    skipped = len(rows) - len(pool)
    if limit:
        pool = pool[:limit]
    print(f"  token: {src}")
    print(f"  replaying {len(pool)} of {len(rows)} "
          f"({skipped} withheld by the safety guard)\n")

    out = []
    redacted_bodies = 0
    for i, r in enumerate(pool, 1):
        body = r.get("request_body")
        # Evidence files are redacted at capture, so a replayed body can carry
        # ***REDACTED*** where the original had a real value. Track it: such a replay
        # is NOT byte-identical to the original request and its verdict is weaker.
        body_redacted = "***REDACTED***" in json.dumps(body) if body is not None else False
        redacted_bodies += bool(body_redacted)
        res = call(r["url"] or (API_BASE + r["path"]), r["verb"], body, token)
        verdict = spec.reproduces(r, res)
        out.append({
            "controller": r["controller"], "action": r["action"], "verb": r["verb"],
            "path": r["path"], "klass": r.get("klass"),
            "then_status": r["http_status"], "now_status": res.get("status"),
            "now_bytes": res.get("body_bytes"), "latency_ms": res.get("latency_ms"),
            "transport_error": res.get("transport_error"),
            "still_reproduces": verdict,
            "body_was_redacted": body_redacted,
            "now_summary": spec.replay_summary(res),
            "raw_response": redact(res.get("response"))
            if isinstance(res.get("response"), (dict, list)) else res.get("response"),
        })
        print(f"  [{i:3d}/{len(pool)}] {r['controller']}/{r['action']:<38s} "
              f"{'REPRODUCED' if verdict else 'changed'}")
        time.sleep(REPLAY_THROTTLE_S)

    rep = sum(1 for o in out if o["still_reproduces"])
    return {"ok": True, "token_src": src, "attempted": len(out), "reproduced": rep,
            "not_reproduced": len(out) - rep, "withheld_by_guard": skipped,
            "replayed_with_redacted_body": redacted_bodies,
            "attempted_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "calls": out}


# --------------------------------------------------------------------- md / xlsx
def esc(s) -> str:
    if s is None:
        return "—"
    return str(s).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip() or "—"


class MD:
    def __init__(self):
        self.lines: list[str] = []

    def __call__(self, s=""):
        self.lines.append(s)
        return self

    def h(self, level, s):
        return self(f"{'#' * level} {s}")("")

    def p(self, s):
        return self(s)("")

    def rule(self):
        return self("---")("")

    def table(self, headers, rows, align=None):
        self("| " + " | ".join(str(h) for h in headers) + " |")
        self("|" + "|".join(align or ["---"] * len(headers)) + "|")
        for r in rows:
            self("| " + " | ".join(str(c) for c in r) + " |")
        return self("")

    def code(self, s, lang=""):
        return self(f"```{lang}")(s)("```")("")

    def text(self) -> str:
        return "\n".join(self.lines)


class Xlsx:
    HDR_FILL = "1F3864"
    RED = "FCE4E4"
    AMBER = "FFF2CC"
    GREEN = "E2EFDA"

    def __init__(self):
        from openpyxl import Workbook
        self.wb = Workbook()
        self._first = True

    def summary(self, title: str, pairs: list[tuple]):
        from openpyxl.styles import Font
        ws = self.wb.active
        ws.title = "Summary"
        ws["A1"] = title
        ws["A1"].font = Font(bold=True, size=13, color="1F3864")
        for i, (k, v) in enumerate(pairs, 3):
            ws.cell(i, 1, k).font = Font(bold=True, size=10)
            ws.cell(i, 2, v)
        ws.column_dimensions["A"].width = 36
        ws.column_dimensions["B"].width = 62
        self._first = False
        return ws

    def sheet(self, name, headers, rows, widths, note=None, wrap_last=True):
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter
        ws = self.wb.create_sheet(name[:31])
        r0 = 1
        if note:
            ws.cell(1, 1, note).font = Font(italic=True, size=9, color="666666")
            r0 = 2
        for c, h in enumerate(headers, 1):
            cell = ws.cell(r0, c, h)
            cell.fill = PatternFill("solid", fgColor=self.HDR_FILL)
            cell.font = Font(color="FFFFFF", bold=True, size=10)
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        for i, row in enumerate(rows, r0 + 1):
            for c, v in enumerate(row, 1):
                if isinstance(v, (dict, list)):
                    v = json.dumps(v)[:2000]
                cell = ws.cell(i, c, v)
                cell.alignment = Alignment(
                    vertical="top", wrap_text=(wrap_last and c == len(row)))
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w
        ws.freeze_panes = ws.cell(r0 + 1, 1)
        if rows:
            ws.auto_filter.ref = (f"A{r0}:{get_column_letter(len(headers))}"
                                  f"{r0 + len(rows)}")
        ws.row_dimensions[r0].height = 30
        return ws

    def note_sheet(self, name, title, pairs):
        from openpyxl.styles import Alignment, Font
        ws = self.wb.create_sheet(name[:31])
        ws["A1"] = title
        ws["A1"].font = Font(bold=True, size=13, color="1F3864")
        for i, (k, v) in enumerate(pairs, 3):
            ws.cell(i, 1, k).font = Font(bold=True)
            ws.cell(i, 2, v).alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[i].height = 46
        ws.column_dimensions["A"].width = 26
        ws.column_dimensions["B"].width = 104
        return ws

    def save(self, path: Path):
        self.wb.save(path)


# ------------------------------------------------------------------------- the spec
@dataclass
class LoopholeSpec:
    num: str
    slug: str
    title: str
    severity: str
    priority: str
    effort: str
    jira_summary: str
    one_liner: str
    revalidate: str = "safe"            # safe | forbidden | static | partial
    revalidate_note: str = ""
    replay_excludes_mutating: bool = False
    replay_limit: int | None = None
    source: str = "run"                 # run | catalogue | static | incident
    run_id: str | None = None           # None -> RUN_ID. Set to source a different run.
    cross_refs: list = field(default_factory=list)
    TAXONOMY: dict = field(default_factory=dict)

    # supplied by each concrete spec module
    select: Callable | None = None
    classify: Callable | None = None
    narrative: Callable | None = None
    sheets: Callable | None = None
    rows_static: Callable | None = None   # for catalogue/static loopholes
    reproduces: Callable | None = None
    replay_summary: Callable | None = None
    # Extra per-spec guard applied before anything is called. Use it to exclude rows
    # whose replay would MUTATE data - e.g. LH-02's 28 successful inserts, which would
    # create fresh records on every re-validation.
    replay_filter: Callable | None = None
    # Ticket content that cannot be derived: reproduction steps, the expected/actual
    # pair, the severity argument, the fix table and the acceptance criteria.
    TICKET: dict = field(default_factory=dict)

    @property
    def lh_id(self) -> str:
        return f"LH-{self.num}"

    @property
    def folder(self) -> Path:
        return PACKS / f"LH-{self.num}-{self.slug}"


def default_reproduces(row, res) -> bool:
    return res.get("status") == row.get("http_status")


def default_replay_summary(res) -> str:
    if res.get("transport_error"):
        return res["transport_error"]
    r = res.get("response")
    if isinstance(r, dict):
        s = r.get("Success", r.get("success"))
        c = r.get("ErrorCode", r.get("errorCode"))
        bits = [f"HTTP {res.get('status')}"]
        if s is not None:
            bits.append(f"Success={s}")
        if c:
            bits.append(f"code={str(c).splitlines()[0][:40]}")
        return " / ".join(bits)
    return f"HTTP {res.get('status')} / {type(r).__name__}"


# --------------------------------------------------------------------- orchestration
def collect_rows(spec: LoopholeSpec) -> list[dict]:
    if spec.rows_static:
        rows = spec.rows_static()
    else:
        run = RunData.get(spec.run_id or RUN_ID)
        rows = []
        for flow, hop in run.hops:
            ev = run.evidence(hop)
            resp = ev.get("response")
            if not spec.select(hop, resp):
                continue
            r = base_row(flow, hop, ev)
            r["response"] = resp
            rows.append(r)
    for r in rows:
        r["klass"] = spec.classify(r) if spec.classify else ""
    return rows


def build_pack(spec: LoopholeSpec, do_replay: bool = False) -> dict:
    out = spec.folder
    (out / "data").mkdir(parents=True, exist_ok=True)
    print(f"\n=== {spec.lh_id} — {spec.title}")
    rows = collect_rows(spec)
    print(f"  occurrences      : {len(rows)}")
    eps = {(r['controller'], r['action']) for r in rows}
    print(f"  distinct endpoints: {len(eps)}")

    payload = {
        "loophole": spec.lh_id,
        "title": spec.title,
        "severity": spec.severity,
        "source_run": (spec.run_id or RUN_ID) if spec.source == "run" else spec.source,
        "environment": ENVIRONMENT,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "occurrences": len(rows),
        "distinct_endpoints": len(eps),
        "distinct_controllers": len({r["controller"] for r in rows if r["controller"]}),
        "by_class": dict(sorted(Counter(r["klass"] for r in rows).items())),
        "rows": rows,
    }

    attempt_file = out / "data" / "revalidation-attempt.json"
    if do_replay:
        print(f"  live re-validation ({spec.revalidate}):")
        res = replay(spec, rows, spec.replay_limit)
        if not res.get("ok"):
            print(f"    -> {res.get('reason')}")
        attempt_file.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
        payload["revalidation"] = res
    elif attempt_file.exists():
        payload["revalidation"] = json.loads(attempt_file.read_text(encoding="utf-8"))
        print("  re-validation    : loaded prior attempt "
              f"({'ok' if payload['revalidation'].get('ok') else 'not run'})")

    slim = json.loads(json.dumps(payload, default=str))
    (out / "data" / f"lh{spec.num}-occurrences.json").write_text(
        json.dumps(slim, indent=1), encoding="utf-8")

    md = MD()
    spec.narrative(payload, md)
    (out / "EVIDENCE.md").write_text(md.text(), encoding="utf-8")

    xl = Xlsx()
    spec.sheets(payload, xl)
    _revalidation_sheet(payload, xl)
    xl.save(out / "EVIDENCE.xlsx")

    write_jira_ticket(spec, payload)

    for f in ("EVIDENCE.md", "EVIDENCE.xlsx", "JIRA-TICKET.md"):
        print(f"  wrote {(out / f).relative_to(ROOT)} "
              f"({(out / f).stat().st_size / 1024:.0f} KB)")
    return payload


def _revalidation_sheet(payload: dict, xl: Xlsx):
    rv = payload.get("revalidation")
    if rv and rv.get("ok"):
        rows = [[c["controller"], c["action"], c.get("klass"), c["verb"],
                 f"HTTP {c['then_status']}", c["now_summary"],
                 "YES" if c["still_reproduces"] else "changed", c["latency_ms"]]
                for c in rv["calls"]]
        xl.sheet("Re-validation",
                 ["Controller", "Action", "Class", "Verb", "Then", "Live now",
                  "Reproduces", "ms"], rows, [22, 36, 14, 6, 14, 46, 12, 8],
                 note=(f"Live replay {str(rv.get('attempted_utc'))[:10]} against "
                       f"{ENVIRONMENT}. {rv['reproduced']} of {rv['attempted']} "
                       f"reproduce; {rv.get('withheld_by_guard', 0)} withheld by the "
                       f"safety guard."))
    else:
        reason = (rv or {}).get("reason", "not attempted")
        xl.note_sheet("Re-validation", "Live re-validation — not performed", [
            ("Reason", reason),
            ("Impact on this finding",
             "None. Every figure derives from the retained source run, one evidence "
             "file per call."),
            ("To run",
             "$env:PAM_API_TOKEN = \"<bearer>\"; "
             "python tools\\build_lh_pack.py --lh <NN> --revalidate"),
        ])


# ------------------------------------------------------------- shared md components
def header_block(md: MD, payload: dict, spec: LoopholeSpec):
    md.h(1, f"{spec.lh_id} Evidence — {spec.title}")
    md(f"**Loophole:** {spec.num.lstrip('0')} of 12 · **Severity:** {spec.severity} · "
       f"**Effort to fix:** {spec.effort}")
    md(f"**Environment:** `{ENVIRONMENT}` — API `{API_BASE}` · app `{APP_BASE}` · "
       f"build `{BUILD}`")
    src = (f"Dynamic API validation run `{RUN_ID}` — 1,868 live calls, 2026-07-29"
           if spec.source == "run" else
           "Static analysis of `pam/PAM`" if spec.source == "static" else
           "`APIConfig.java` catalogue + payload helpers" if spec.source == "catalogue"
           else "Incident record — `docs/findings/issues/ISSUE-010`")
    md(f"**Source:** {src}")
    md(f"**Scope:** **{payload['occurrences']}** occurrences across "
       f"**{payload['distinct_endpoints']}** distinct endpoints in "
       f"**{payload['distinct_controllers']}** controllers")
    md(f"**Generated:** {payload['generated_utc']}")
    md("")
    md.rule()


def revalidation_section(md: MD, payload: dict, spec: LoopholeSpec, n: int):
    md.h(2, f"{n}. Live re-validation")
    rv = payload.get("revalidation")
    if rv and rv.get("ok") and rv.get("attempted", 0) == 0:
        md.p("⚠️ **Nothing was replayed — every occurrence was withheld by the safety "
             "guard.**")
        md.table(["Measure", "Result"], [
            ["Occurrences in scope", len(payload["rows"])],
            ["Withheld by the safety guard", rv.get("withheld_by_guard", 0)],
            ["Actually called", "**0**"],
        ])
        md.p("That is the intended outcome for this finding, not a failure: "
             f"{spec.revalidate_note or 'the endpoints in scope mutate state'}. The "
             "evidence is the declaration in the endpoint catalogue, which needs no "
             "execution to verify.")
    elif rv and rv.get("ok"):
        when = str(rv.get("attempted_utc", ""))[:10]
        md.p(f"Replayed against live `{ENVIRONMENT}` on **{when}**, using the same verb, "
             f"body and headers as the source run.")
        md.h(3, f"✅ {rv['reproduced']} of {rv['attempted']} still reproduce "
                f"({rv['reproduced'] / max(rv['attempted'], 1) * 100:.1f}%)")
        md.table(["Measure", "Result"], [
            ["Occurrences in scope", len(payload["rows"])],
            ["Calls replayed", rv["attempted"]],
            ["Still reproducing", f"**{rv['reproduced']}**"],
            ["No longer reproducing", rv["not_reproduced"]],
            ["Withheld by the safety guard", rv.get("withheld_by_guard", 0)],
        ])
        changed = [c for c in rv["calls"] if not c["still_reproduces"]]
        if changed:
            md.p("Calls whose behaviour changed:")
            md.table(["Controller", "Action", "Then", "Now", "Body was redacted?"],
                     [[f"`{c['controller']}`", f"`{c['action']}`",
                       f"HTTP {c['then_status']}", esc(c["now_summary"]),
                       "⚠️ yes" if c.get("body_was_redacted") else "no"]
                      for c in changed])
        nred = rv.get("replayed_with_redacted_body", 0)
        if nred:
            md.p(f"⚠️ **Replay fidelity caveat — {nred} of {rv['attempted']} replayed "
                 "requests did not carry a byte-identical body.**")
            md.p("Evidence files are redacted at capture, so any request field whose "
                 "*name* matches `password|token|secret|credential` was stored as "
                 "`***REDACTED***` and replayed with that literal. The redaction is "
                 "deliberately over-broad: it also catches booleans such as "
                 "`AllowPasswordChange` and `Vault_Password_Immediately`, which then "
                 "fail type conversion on the server.")
            md.p("Where a replay verdict depends on such a request, treat it as weaker "
                 "than the original captured evidence. The captured response remains the "
                 "primary evidence; the replay is a freshness check.")
    elif rv and rv.get("refused"):
        md.p("⛔ **Live replay is forbidden for this finding and was not attempted.**")
        md("> " + esc(rv["reason"]))
        md("")
        md.p("The evidence below comes entirely from the retained incident record and "
             "the endpoint catalogue. Reproducing it would repeat the outage.")
    elif rv and rv.get("static"):
        md.p("Not applicable — this finding is derived from static analysis of the "
             "product source. There is nothing to call.")
    else:
        reason = (rv or {}).get("reason", "not attempted in this build")
        md.p("⬜ **Not re-validated live.**")
        md("> " + esc(reason))
        md("")
        md.p("Every figure above derives from the retained source run, one evidence file "
             "per call. Re-validation is a freshness check, not the basis of the claim.")
        md.code(f'$env:PAM_API_TOKEN = "<bearer token>"\n'
                f'python tools\\build_lh_pack.py --lh {spec.num} '
                f'--revalidate', "powershell")


def write_jira_ticket(spec: LoopholeSpec, payload: dict) -> Path:
    """Generate the ticket draft. Same nine-section contract as LH-01's, which was
    hand-written; everything derivable comes from the dataset so the numbers in the
    ticket cannot drift from the numbers in the evidence."""
    t = spec.TICKET
    rv = payload.get("revalidation") or {}
    md = MD()
    md.h(1, f"JIRA TICKET DRAFT — {spec.lh_id}")
    md("**Status:** 🟡 **DRAFT — not raised.** Awaiting owner validation of the evidence.")
    md(f"**Drafted:** {payload['generated_utc'][:10]} · **Drafted by:** QA automation")
    md("**Paste the fenced blocks below straight into the matching Jira fields.** Prose "
       "outside a fenced block is guidance for whoever raises it.")
    md("")
    md.rule()

    md.h(2, "1. Field values")
    md.table(["Jira field", "Value"], [
        ["**Project**", "`PAMIT`"],
        ["**Issue type**", "Bug"],
        ["**Summary**", "see §2"],
        ["**Severity**", f"{spec.severity} → `{severity_field(spec)}`"],
        ["**Priority**", f"`{spec.priority}`"],
        ["**Component**", "ARCON PAM API (`ARCONPAMAPI`)"],
        ["**Affects version / milestone**", f"`{BUILD}`"],
        ["**Fix version**", f"`{BUILD}`"],
        ["**Environment**", f"`{ENVIRONMENT}` — app `{APP_BASE}` · API `{API_BASE}`"],
        ["**Database Type**", "`MSSQL`"],
        ["**Hosting Environment**", "`Windows`"],
        ["**Task Complexity**", f"`{spec.effort}`"],
        ["**Department Of Created By**", "`Automation Team`"],
        ["**Primary Client**", "`Internal (ARCON)`"],
        ["**Labels**", " ".join(f"`{x}`" for x in ticket_labels(spec))],
        ["**Attachments**", "`EVIDENCE.xlsx`, `EVIDENCE.md`, evidence `.zip` "
                            "(excluding `JIRA-TICKET.md`)"],
    ])
    md.rule()

    md.h(2, '2. Summary *(Jira "Summary" field)*')
    md.code(spec.jira_summary)

    md.h(2, '3. Description *(Jira "Description" field)*')
    body = MD()
    body("h2. What happens")
    body("")
    body(t.get("what", spec.one_liner))
    body("")
    body("h2. Environment")
    body("")
    body("|| Item || Value ||")
    for k, v in [("Environment", ENVIRONMENT), ("Application URL", APP_BASE),
                 ("API URL", API_BASE), ("Build", BUILD), ("Database", "MSSQL")]:
        body(f"| {k} | {v} |")
    body("")
    body("h2. Measured scope")
    body("")
    body("|| Measure || Value ||")
    src = (f"Dynamic API validation run {RUN_ID} - 1,868 live calls, 2026-07-29"
           if spec.source == "run" else
           "Static analysis of the pam/PAM product source" if spec.source == "static" else
           "APIConfig.java catalogue (1,306 endpoints)" if spec.source == "catalogue"
           else "Incident record - ISSUE-010")
    body(f"| Basis | {src} |")
    # A spec may override the headline count where the raw selection is wider than the
    # defect - LH-02 selects 552 Success:true responses but the defect is 2 write no-ops.
    label = t.get("occurrence_label", "Occurrences")
    value = t.get("occurrence_value", payload["occurrences"])
    body(f"| {label} | *{value}* |")
    if not t.get("hide_endpoint_counts"):
        body(f"| Distinct endpoints | *{payload['distinct_endpoints']}* |")
        if payload["distinct_controllers"]:
            body(f"| Distinct controllers | *{payload['distinct_controllers']}* |")
    for k, v in t.get("scope_rows", []):
        body(f"| {k} | {v} |")
    body("")
    if t.get("example"):
        body("Captured verbatim:")
        body("")
        body("{code:json}")
        body(t["example"])
        body("{code}")
        body("")
    for section in t.get("sections", []):
        body(f"h2. {section[0]}")
        body("")
        body(section[1])
        body("")
    body("h2. Re-validation")
    body("")
    if rv.get("ok") and rv.get("attempted", 0) == 0:
        body(f"Not executed by design - all {rv.get('withheld_by_guard', 0)} occurrences "
             f"were withheld by the harness safety guard, because "
             f"{spec.revalidate_note or 'calling them would change state'}. The evidence "
             f"is the catalogue declaration, which needs no execution.")
    elif rv.get("ok"):
        body(f"Replayed against {ENVIRONMENT} on "
             f"{str(rv.get('attempted_utc'))[:10]}: *{rv['reproduced']} of "
             f"{rv['attempted']} still reproduce*.")
        if rv.get("withheld_by_guard"):
            body(f"A further {rv['withheld_by_guard']} occurrences were withheld by the "
                 f"safety guard because replaying them would have mutated data.")
        if rv.get("replayed_with_redacted_body"):
            body(f"Caveat: {rv['replayed_with_redacted_body']} replayed requests did not "
                 f"carry a byte-identical body - credential-named fields are redacted at "
                 f"capture. See EVIDENCE.md.")
    elif rv.get("refused"):
        body("*Deliberately not re-validated.* " + spec.revalidate_note.capitalize() +
             ". The evidence is the retained incident record.")
    elif rv.get("static"):
        body("Not applicable - this finding is derived from static analysis.")
    else:
        body("Not re-validated live in this build. All figures derive from retained "
             "evidence, one file per call.")
    body("")
    body("h2. Evidence")
    body("")
    body("Full per-occurrence register, per-controller breakdown and reproduction table "
         "are in the attached EVIDENCE.xlsx and EVIDENCE.md.")
    md.code(body.text())

    md.h(2, '4. Steps to reproduce *(Jira "Steps to Reproduce" field)*')
    if t.get("repro"):
        md.code(t["repro"])
    else:
        md.p("⚠️ Not applicable — this finding is established by inspection rather than "
             "execution. See §3 and the attached evidence.")

    md.h(2, "5. Expected vs actual")
    md.code(f"EXPECTED: {t.get('expected', '—')}\n\n"
            f"ACTUAL:   {t.get('actual', '—')}")

    md.h(2, "6. Severity justification")
    md.p("Not for pasting — this exists so the rating survives triage.")
    md.table(["Criterion", "Assessment"], t.get("severity_rows", []))
    md.p(f"**Rating: {spec.severity}.** {t.get('severity_argument', '')}")

    md.h(2, "7. Proposed fix")
    md.table(["#", "Action", "Effort", "Effect"], t.get("fix_rows", []))
    if t.get("fix_note"):
        md.p(t["fix_note"])

    md.h(2, "8. Acceptance criteria")
    md.code(t.get("acceptance", "—"))
    md.p("**QA verification:**")
    md.code(f"python tools\\build_lh_pack.py --lh {spec.num}\n"
            f"# 'occurrences' must report {t.get('target', '0')}", "powershell")

    md.h(2, "9. Evidence and provenance")
    md.table(["Artifact", "Path"], [
        ["Full evidence write-up", f"`artifacts/loopholes/{spec.folder.name}/EVIDENCE.md`"],
        ["Evidence workbook", f"`artifacts/loopholes/{spec.folder.name}/EVIDENCE.xlsx`"],
        ["Machine-readable extract",
         f"`.../data/lh{spec.num}-occurrences.json`"],
        ["Source run — 1,868 responses", f"`artifacts/runs/{RUN_ID}/evidence/`"],
        ["Aggregate run report",
         "`docs/management/summary/Full-Generated-Run-2026-07-29.md`"],
        # Count-agnostic on purpose: it read "all 12 findings" and went stale the moment
        # LH-13 was added. The brief states its own count in its header.
        ["Developer brief, every finding", "`docs/briefs/developer-loopholes.md`"],
    ])
    if spec.cross_refs:
        md.p("**Related findings:** " + " · ".join(spec.cross_refs))
    md.p("⛔ **This ticket has not been raised.** LH-01 (`PAMIT-42744`) is the only "
         "loophole currently in Jira. Raise this only after the owner has validated the "
         "evidence — see `docs/findings/README.md`.")

    p = spec.folder / "JIRA-TICKET.md"
    p.write_text(md.text(), encoding="utf-8")
    return p


def severity_field(spec: LoopholeSpec) -> str:
    """PAMIT Severity is Sev-0..Sev-3; the brief uses Critical/High/Medium/Low."""
    s = spec.severity
    if "Critical" in s:
        return "Sev-1"
    if "High" in s:
        return "Sev-1"
    if "Medium" in s or "Review" in s:
        return "Sev-2"
    return "Sev-3"


def ticket_labels(spec: LoopholeSpec) -> list:
    base = ["api-contract", "qa-automation", f"developer-loophole-{spec.num}"]
    extra = spec.TICKET.get("labels", [])
    return base[:1] + extra + base[1:]


def reproduce_footer(md: MD, spec: LoopholeSpec, n: int):
    md.rule()
    md.h(2, f"{n}. Reproducing this evidence")
    md.code(f"# rebuild from retained run data - zero HTTP calls\n"
            f"python tools\\build_lh_pack.py --lh {spec.num}\n\n"
            f"# add a live re-check\n"
            f'$env:PAM_API_TOKEN = "<bearer token>"\n'
            f"python tools\\build_lh_pack.py --lh {spec.num} --revalidate",
            "powershell")
    md.p(f"Raw extract: `data/lh{spec.num}-occurrences.json` · "
         f"Source responses: `artifacts/runs/{RUN_ID}/evidence/`")
    if spec.cross_refs:
        md.p("**Related findings:** " + " · ".join(spec.cross_refs))
