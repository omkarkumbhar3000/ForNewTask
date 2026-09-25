#!/usr/bin/env python3
"""DevProjects Control Center — the local decision server behind the `engage` UI (`OBJ-027`).

    engage discovers and analyses  ->  the UI presents decisions
    ->  the owner approves         ->  engage executes safely

This process is the third arrow's only door. It exists because a static page
cannot execute anything, and the owner asked for one button rather than a page
plus a manual CLI step.

⛔ THE FRONTEND IS A DECISION INTERFACE, NEVER A SECURITY BOUNDARY.
Assume every request is forged. Nothing here trusts the browser:

  * The browser never sends a command. It sends an action TYPE plus a target,
    both of which are looked up in `ACTIONS` below. An unknown type is refused
    by name. There is no path from request data to a shell string, ever.
  * Every action that touches git goes through `engage_core.run_git`, which
    holds its own allow-list, and through `engage_core.policy_for`, which holds
    the per-repository rights from `D28`. This server cannot widen either. If
    the CLI would refuse an action, so does this.
  * Bound to 127.0.0.1 only. A random per-process token is required on every
    request. No token, no service - and the token is never written to disk.
  * Read endpoints are separated from the one write endpoint, so "show me" and
    "do it" cannot be confused for one another.

⛔ ZERO PRODUCT HTTP. This server never calls `/arcontoken`, never runs the API
suite, and never touches a blocklisted endpoint. It has no HTTP client at all.

⚠️ Safe-by-default rather than deny-by-default, extending `D31`'s reasoning from
`engage` to its frontend. Starting the server executes nothing; it only listens.
Every action it can perform is non-destructive by construction - a fast-forward
pull that cannot run against a dirty tree, or a re-derivation of local data. The
`--execute` convention that guards the rest of `tools/` guards scripts that can
issue HTTP to a shared environment; this one cannot.

Usage:

    python tools/control_center.py                 # serve, print the tokenised URL
    python tools/control_center.py --open          # ...and open Chrome at it
    python tools/control_center.py --port 8760
    python tools/control_center.py --read-only     # refuse /api/execute entirely
    python tools/control_center.py --selftest      # no socket; exercise the guards
"""

from __future__ import annotations

import argparse
import json
import secrets
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from paths import workspace_root

ROOT = workspace_root(__file__)
TOOLS = ROOT / "tools"
UI_DIST = TOOLS / "control-center" / "dist"
UI_DEV_NOTE = "tools/control-center — run `npm install && npm run build` to produce dist/"

STATE = ROOT / "state" / "control-center"
DECISIONS = STATE / "decisions.jsonl"       # append-only journal
RUNS_LOG = STATE / "executions.jsonl"       # append-only execution record
ENGAGE_CONTEXT = ROOT / "state" / "engage" / "context.json"

HOST = "127.0.0.1"                          # never 0.0.0.0. Not configurable on purpose.
DEFAULT_PORT = 8760
MAX_BODY = 256 * 1024                       # a decision payload is small; cap it hard


# --------------------------------------------------------------------------- #
# Decision vocabulary
#
# The owner asked for these specific verbs. Each needs defined behaviour, or
# "ignore" quietly becomes "never show me this defect again".
# --------------------------------------------------------------------------- #

DECISIONS_VOCAB = {
    "accept":        "Execute now, this run.",
    "approve":       "Execute now. Used where the item needed explicit confirmation.",
    "reject":        "Do not execute. Recorded, and offered again next run.",
    "ignore_once":   "Skip for THIS run only. Reappears next time, unchanged.",
    "consider_next": "Do not execute now; surface it again next run, marked as carried over.",
    "not_interested": (
        "Suppress until the underlying condition materially CHANGES. Keyed to a "
        "fingerprint of the item's state, so the suppression expires by itself when "
        "the facts move - the same mechanism the drift loop's waivers use. This is "
        "why it is not 'hide for ever'."
    ),
    "defer":         "Do not execute now; carry forward with an explicit note.",
    "review":        "Do not execute. Flag for manual inspection.",
    "always_approve": (
        "Pre-approve this action type in future runs. ⛔ Permitted ONLY for action "
        "types declared reversible AND safe. Refused for anything else - a "
        "potentially destructive operation must never become silently automatic."
    ),
    "always_ask":    "Require explicit approval every run. The default.",
}

EXECUTING_DECISIONS = {"accept", "approve"}


# --------------------------------------------------------------------------- #
# The server-side action whitelist
#
# This dict IS the security model. The browser can only ask for a key that
# appears here; everything else is refused by name. Note what is absent and will
# stay absent: push, merge, rebase, reset, checkout, clean, stash, conflict
# resolution, credential edits, deletion, and anything that issues product HTTP.
# --------------------------------------------------------------------------- #

def _act_pull(target: str) -> dict:
    """Fast-forward a repository, re-using engage's own decision path.

    Deliberately re-derives the plan server-side instead of trusting the plan the
    browser was looking at. The tree may have changed since the page rendered, and
    a stale 'safe to pull' is exactly how uncommitted work gets overwritten.
    """
    import engage_core as core

    repos = {rel: p for p, rel in core.discover_repos(ROOT)}
    if target not in repos:
        return {"ok": False, "reason": f"not a discovered repository: {target!r}"}

    path = repos[target]
    pol, known = core.policy_for(target)
    st = core.inspect_repo(path, target)
    plan = core.classify(st, pol, known)

    if plan.action != "pull":
        return {"ok": False, "reason": f"engage would not pull this now: {plan.reason}",
                "recomputed": True}

    code, out = core.run_git(path, "pull", "--ff-only")
    # Truncate rather than sanitise: run_git output is git's own text, and the one
    # thing that must never reach the browser is a credential. git does not print
    # them here, and the cap bounds anything unexpected.
    return {"ok": code == 0, "detail": out[:2000],
            "reason": "fast-forwarded" if code == 0 else f"git exited {code}"}


def _act_refresh(_target: str) -> dict:
    """Re-derive drift, the evidence index and the dashboard datasets.

    Calls obj016_daily_refresh with --skip-git: the git half is what the pull
    action covers, and doing it twice would fetch twice for no reason.
    """
    script = TOOLS / "obj016_daily_refresh.py"
    if not script.is_file():
        return {"ok": False, "reason": f"missing: {script}"}
    env = None
    try:
        import obj016_daily_refresh as daily
        env = daily.child_env()
    except Exception:
        pass
    r = subprocess.run([sys.executable, str(script), "--execute", "--skip-git"],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=1800, env=env)
    tail = "\n".join((r.stdout or "").strip().splitlines()[-12:])
    return {"ok": r.returncode == 0, "detail": tail, "reason": f"exit {r.returncode}"}


def _act_note(target: str) -> dict:
    """Record a decision only. Changes nothing on disk except the journal."""
    return {"ok": True, "reason": "recorded", "detail": target}


ACTIONS = {
    # key                handler       reversible  safe   auto-approvable
    "repo.pull_ff_only": (_act_pull,    True,      True,  True),
    "data.refresh":      (_act_refresh, True,      True,  True),
    "decision.note":     (_act_note,    True,      True,  True),
}

#: Action types a client may ever name. Anything else is refused by name, so a
#: forged request produces a clear audit line rather than a silent no-op.
ALLOWED_ACTIONS = frozenset(ACTIONS)

#: Words that must never appear in an action key. A belt-and-braces assertion
#: rather than a filter: if one ever shows up, the table is wrong, not the input.
BANNED_IN_KEYS = ("push", "merge", "rebase", "reset", "clean", "checkout",
                  "stash", "force", "delete", "token", "arcontoken", "suite")


def audit_action_table() -> list[str]:
    """Structural self-check on ACTIONS. Returns a list of problems; empty is good."""
    problems = []
    for key, (fn, reversible, safe, auto) in ACTIONS.items():
        for bad in BANNED_IN_KEYS:
            if bad in key.lower():
                problems.append(f"{key}: contains banned word {bad!r}")
        if auto and not (reversible and safe):
            problems.append(f"{key}: auto-approvable but not both reversible and safe")
        if not callable(fn):
            problems.append(f"{key}: handler is not callable")
    return problems


def may_always_approve(action: str) -> bool:
    """`always_approve` is only ever granted to a reversible AND safe action."""
    spec = ACTIONS.get(action)
    return bool(spec) and spec[1] and spec[2] and spec[3]


# --------------------------------------------------------------------------- #
# Journals — append-only, so a decision history cannot be quietly rewritten
# --------------------------------------------------------------------------- #

_lock = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def append_jsonl(path: Path, row: dict) -> None:
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path, limit: int = 500) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue          # a torn last line must not lose the whole journal
    return rows[-limit:]


def suppression_state() -> dict:
    """Fold the decision journal into what should be hidden or carried forward.

    `not_interested` is keyed to the item's fingerprint: when the fingerprint
    changes the suppression stops matching, so an important item cannot be
    permanently buried by one dismissal. `ignore_once` is scoped to the run it
    was made in and never outlives it.
    """
    out: dict[str, dict] = {}
    for row in read_jsonl(DECISIONS, limit=5000):
        key = row.get("item")
        if not key:
            continue
        out[key] = {
            "decision": row.get("decision"),
            "fingerprint": row.get("fingerprint"),
            "run": row.get("run"),
            "at": row.get("at"),
            "note": row.get("note"),
        }
    return out


# --------------------------------------------------------------------------- #
# Context
# --------------------------------------------------------------------------- #

def load_context(refresh: bool = False) -> dict:
    """Return engage's context, optionally re-running it read-only first."""
    if refresh:
        script = TOOLS / "engage.py"
        if script.is_file():
            subprocess.run([sys.executable, str(script), "--dry-run", "--quiet"],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=600)
    if not ENGAGE_CONTEXT.is_file():
        return {"error": "no engage context yet", "hint": "run: python tools/engage.py"}
    try:
        ctx = json.loads(ENGAGE_CONTEXT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {"error": f"context.json is not valid JSON: {e}"}
    ctx["_suppressions"] = suppression_state()
    ctx["_vocabulary"] = DECISIONS_VOCAB
    ctx["_actions"] = {k: {"reversible": v[1], "safe": v[2], "autoApprovable": v[3]}
                       for k, v in ACTIONS.items()}
    return ctx


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #

class Handler(BaseHTTPRequestHandler):
    server_version = "DevProjectsControlCenter/1.0"
    token = ""
    read_only = False

    # --- plumbing ---------------------------------------------------------- #

    def log_message(self, fmt, *args):        # quieter than the default
        sys.stderr.write("  [cc] %s\n" % (fmt % args))

    def _send(self, code: int, payload, ctype="application/json"):
        body = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        # This page is served to one local browser; nothing should embed or cache it.
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'")
        self.end_headers()
        self.wfile.write(body)

    def _authed(self, q: dict) -> bool:
        supplied = (q.get("t") or [""])[0] or self.headers.get("X-CC-Token", "")
        return bool(self.token) and secrets.compare_digest(supplied, self.token)

    # --- routes ------------------------------------------------------------ #

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._authed(q):
            return self._send(403, {"error": "bad or missing token"})

        if u.path == "/api/context":
            return self._send(200, load_context(refresh=(q.get("refresh") or [""])[0] == "1"))
        if u.path == "/api/decisions":
            return self._send(200, {"decisions": read_jsonl(DECISIONS)})
        if u.path == "/api/executions":
            return self._send(200, {"executions": read_jsonl(RUNS_LOG)})
        if u.path == "/api/health":
            return self._send(200, {"ok": True, "readOnly": self.read_only,
                                    "actions": sorted(ALLOWED_ACTIONS),
                                    "auditProblems": audit_action_table()})
        return self._serve_ui(u.path)

    def do_POST(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._authed(q):
            return self._send(403, {"error": "bad or missing token"})

        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self._send(413, {"error": "payload too large"})
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._send(400, {"error": "body is not valid JSON"})

        if u.path == "/api/decide":
            return self._send(200, self._decide(body))
        if u.path == "/api/execute":
            if self.read_only:
                return self._send(403, {"error": "server started with --read-only"})
            return self._send(200, self._execute(body))
        return self._send(404, {"error": "no such endpoint"})

    # --- handlers ---------------------------------------------------------- #

    def _decide(self, body: dict) -> dict:
        """Record decisions. Never executes anything."""
        recorded, refused = [], []
        for item in body.get("items") or []:
            key = item.get("item")
            decision = item.get("decision")
            if not key or decision not in DECISIONS_VOCAB:
                refused.append({"item": key, "reason": f"unknown decision {decision!r}"})
                continue
            if decision == "always_approve" and not may_always_approve(item.get("action", "")):
                refused.append({"item": key, "reason":
                                "always_approve is only granted to a reversible, safe action type"})
                continue
            row = {"at": _now(), "item": key, "decision": decision,
                   "action": item.get("action"), "fingerprint": item.get("fingerprint"),
                   "run": body.get("run"), "note": item.get("note")}
            append_jsonl(DECISIONS, row)
            recorded.append(row)
        return {"recorded": len(recorded), "refused": refused}

    def _execute(self, body: dict) -> dict:
        """Execute only whitelisted action types, only for accept/approve."""
        results, refused = [], []
        for item in body.get("items") or []:
            action = item.get("action")
            target = item.get("target") or ""
            decision = item.get("decision")

            if decision not in EXECUTING_DECISIONS:
                refused.append({"action": action, "target": target,
                                "reason": f"decision {decision!r} does not execute"})
                continue
            if action not in ALLOWED_ACTIONS:
                refused.append({"action": action, "target": target,
                                "reason": f"action type {action!r} is not in the server whitelist"})
                continue
            if not isinstance(target, str) or len(target) > 300:
                refused.append({"action": action, "reason": "target must be a short string"})
                continue

            fn = ACTIONS[action][0]
            try:
                res = fn(target)
            except Exception as e:                      # never leak a traceback to the browser
                res = {"ok": False, "reason": f"{type(e).__name__}: {e}"}
            row = {"at": _now(), "action": action, "target": target, **res}
            append_jsonl(RUNS_LOG, row)
            results.append(row)

        return {"results": results, "refused": refused,
                "summary": {"ok": sum(1 for r in results if r.get("ok")),
                            "failed": sum(1 for r in results if not r.get("ok")),
                            "refused": len(refused)}}

    def _serve_ui(self, path: str):
        """Serve the built React app, or a plain message if it has not been built."""
        rel = "index.html" if path in ("/", "") else path.lstrip("/")
        target = (UI_DIST / rel).resolve()
        try:
            target.relative_to(UI_DIST.resolve())       # no traversal out of dist/
        except ValueError:
            return self._send(403, {"error": "path outside the UI directory"})
        if not target.is_file():
            if not UI_DIST.is_dir():
                return self._send(503, {"error": "UI not built", "hint": UI_DEV_NOTE})
            target = UI_DIST / "index.html"             # SPA fallback
            if not target.is_file():
                return self._send(404, {"error": "not found"})
        ctypes = {".html": "text/html; charset=utf-8", ".js": "text/javascript",
                  ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml",
                  ".woff2": "font/woff2", ".ico": "image/x-icon"}
        self._send(200, target.read_bytes(), ctypes.get(target.suffix, "application/octet-stream"))


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def selftest() -> int:
    """Exercise the guards without opening a socket."""
    checks: list[tuple[str, bool]] = []

    problems = audit_action_table()
    checks.append(("action table is structurally sound", not problems))

    for banned in ("repo.push", "repo.merge", "repo.reset", "repo.clean", "suite.run"):
        checks.append((f"{banned} is NOT whitelisted", banned not in ALLOWED_ACTIONS))

    checks.append(("every action is reversible", all(v[1] for v in ACTIONS.values())))
    checks.append(("every action is safe", all(v[2] for v in ACTIONS.values())))
    checks.append(("always_approve refused for an unknown action", not may_always_approve("repo.push")))
    checks.append(("always_approve granted for a safe action", may_always_approve("data.refresh")))
    checks.append(("host is loopback", HOST == "127.0.0.1"))
    checks.append(("body cap is set", 0 < MAX_BODY <= 1024 * 1024))
    checks.append(("every vocabulary verb is documented",
                   all(isinstance(v, str) and v for v in DECISIONS_VOCAB.values())))
    checks.append(("only accept/approve execute", EXECUTING_DECISIONS == {"accept", "approve"}))

    # ⛔ LESSON, recorded so it is not repeated: the first two versions of these
    # checks grepped this file for forbidden literals, and BOTH were wrong for the
    # same reason - a source grep matches its own needles, and then it matched a
    # comment that says the server never binds to a wildcard address. Neither a
    # needle nor a comment is a bind or a shell call. Test BEHAVIOUR instead.

    def refused(body: dict) -> list:
        return Handler._execute(None, body).get("refused", [])

    forged = refused({"items": [{"action": "repo.push", "target": ".", "decision": "accept"}]})
    checks.append(("a forged action type is refused by name",
                   len(forged) == 1 and "whitelist" in forged[0]["reason"]))

    nonexec = refused({"items": [{"action": "data.refresh", "target": "", "decision": "ignore_once"}]})
    checks.append(("a non-executing decision never runs an action",
                   len(nonexec) == 1 and "does not execute" in nonexec[0]["reason"]))

    huge = refused({"items": [{"action": "data.refresh", "target": "x" * 5000, "decision": "accept"}]})
    checks.append(("an over-long target is refused", len(huge) == 1))

    empty = Handler._execute(None, {"items": []})
    checks.append(("an empty payload executes nothing",
                   empty["summary"] == {"ok": 0, "failed": 0, "refused": 0}))

    bad_auto = Handler._decide(None, {"items": [
        {"item": "x", "decision": "always_approve", "action": "repo.push"}]})
    checks.append(("always_approve on an unsafe action is refused at decide time",
                   bad_auto["recorded"] == 0 and len(bad_auto["refused"]) == 1))

    width = max(len(n) for n, _ in checks)
    failed = 0
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name.ljust(width)}")
        failed += 0 if ok else 1
    for p in problems:
        print(f"         problem: {p}")
    print(f"\n  {len(checks) - failed} passed, {failed} failed")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--open", action="store_true", help="open the tokenised URL in a browser")
    ap.add_argument("--read-only", action="store_true", help="refuse /api/execute entirely")
    ap.add_argument("--selftest", action="store_true", help="exercise the guards, open no socket")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    problems = audit_action_table()
    if problems:
        for p in problems:
            print(f"  refusing to start - {p}")
        return 2

    Handler.token = secrets.token_urlsafe(24)
    Handler.read_only = a.read_only
    url = f"http://{HOST}:{a.port}/?t={Handler.token}"

    srv = ThreadingHTTPServer((HOST, a.port), Handler)
    print("=" * 74)
    print("  DevProjects Control Center")
    print("=" * 74)
    print(f"  {url}")
    print(f"  bound to   : {HOST} only (never 0.0.0.0)")
    print(f"  mode       : {'READ-ONLY' if a.read_only else 'decisions may execute'}")
    print(f"  actions    : {', '.join(sorted(ALLOWED_ACTIONS))}")
    print(f"  journals   : {DECISIONS.relative_to(ROOT)} · {RUNS_LOG.relative_to(ROOT)}")
    if not UI_DIST.is_dir():
        print(f"  ⚠ UI not built - {UI_DEV_NOTE}")
    print("  Ctrl+C to stop")
    print("=" * 74)
    if a.open:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
