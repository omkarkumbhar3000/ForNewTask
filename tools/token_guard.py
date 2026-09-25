"""token_guard.py — the single gate in front of POST /arcontoken.

WHY THIS EXISTS
---------------
The API service account `GenericScheduler` was locked on 2026-07-28 (ISSUE-009 §4a).
The cause was not a wrong password: the harness re-attempted `getToken()` on **every
run by design**, so a run of failures accumulated enough consecutive bad logins to trip
the lockout policy. That account is also the data-warehouse ETL service account, so the
lockout reached past testing.

Retry-on-failure and account lockout are fundamentally incompatible. This module makes
that impossible to get wrong by accident:

    1. A valid cached token is reused. No network call.
    2. When the cache is expired or absent, ONE attempt is made.
    3. A failed attempt writes a LATCH file. While the latch exists, no further attempt
       is made by any script, in this run or any future run, until a human clears it.
    4. At most one attempt per process, enforced separately from the latch, so no code
       path can call twice inside a single run.

Rule 3 is the important one. Without it, "attempt once per run" still becomes "attempt
every run" the moment failures persist — which is precisely how the account locked.

⛔ Never add a retry, a backoff loop, or a scheduled/cron token refresh to this file.
   If generation fails, the correct behaviour is to STOP and tell the owner.

USAGE (CLI)
-----------
    python tools\\token_guard.py status           # report, zero HTTP calls
    python tools\\token_guard.py refresh          # ONE attempt if needed
    python tools\\token_guard.py refresh --force   # ONE attempt even if cached
    python tools\\token_guard.py clear-latch      # human unblock, after a fix

`--force` overrides the CACHE, never the SAFETY: it is still latch-gated and still
limited to one attempt per process.

USAGE (library)
---------------
    import token_guard
    tok, note = token_guard.acquire(cfg, allow_network=True)
    if not tok:
        log(f"no token: {note}")   # then STOP. Do not loop.
"""

from __future__ import annotations

import base64
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

HERE = Path(__file__).resolve().parent

TOKEN_CACHE = HERE / ".token_cache.json"
ATTEMPT_LATCH = HERE / ".token_attempt_block.json"

# Reuse a cached token until this much life remains. 5 min matches chain_runner's
# original behaviour and leaves room for a long run to finish on one token.
SAFETY_MARGIN_S = 300

HTTP_TIMEOUT = 45

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Per-process guard. Belt and braces alongside the on-disk latch: even if the latch
# write fails (read-only disk, permissions), one process still cannot attempt twice.
_ATTEMPTED_THIS_PROCESS = False


# ------------------------------------------------------------------ token inspection
def jwt_claims(tok: str) -> dict:
    try:
        p = tok.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))
    except Exception:                                                    # noqa: BLE001
        return {}


def token_expiry(tok: str) -> int:
    try:
        return int(jwt_claims(tok).get("exp", 0))
    except Exception:                                                    # noqa: BLE001
        return 0


def seconds_left(tok: str) -> int:
    exp = token_expiry(tok)
    return int(exp - time.time()) if exp else 0


# ----------------------------------------------------------------------- the latch
def latch_state() -> dict | None:
    """The recorded failure that is currently blocking attempts, or None."""
    if not ATTEMPT_LATCH.exists():
        return None
    try:
        return json.loads(ATTEMPT_LATCH.read_text(encoding="utf-8"))
    except Exception:                                                    # noqa: BLE001
        # An unreadable latch still blocks. Failing open would defeat the purpose.
        return {"status": "unknown", "body": "(latch file unreadable)"}


def record_failure(status, body: str, username_sent: str = "") -> None:
    ATTEMPT_LATCH.write_text(json.dumps({
        "blocked": True,
        "status": status,
        "body": (body or "")[:600],
        "username_sent": username_sent,
        "attempted_at_epoch": int(time.time()),
        "why": "One /arcontoken attempt failed. Further attempts are blocked to protect "
               "the GenericScheduler account from lockout (ISSUE-009 §4a).",
        "to_clear": "Fix the credential or unlock the account, then run: "
                    "python tools\\token_guard.py clear-latch",
    }, indent=2), encoding="utf-8")


def clear_latch() -> bool:
    if ATTEMPT_LATCH.exists():
        ATTEMPT_LATCH.unlink()
        return True
    return False


# ------------------------------------------------------------------------- the cache
def read_cache() -> tuple[str | None, str]:
    if not TOKEN_CACHE.exists():
        return None, "no cache file"
    try:
        c = json.loads(TOKEN_CACHE.read_text(encoding="utf-8"))
        tok = c.get("access_token")
        if not tok:
            return None, "cache has no access_token"
        left = seconds_left(tok)
        if left > SAFETY_MARGIN_S:
            return tok, f"cache ({left // 60} min left)"
        return None, f"cache expired ({left // 60} min)" if left else "cache expired"
    except Exception as exc:                                             # noqa: BLE001
        return None, f"cache unreadable: {type(exc).__name__}"


def write_cache(payload: dict) -> None:
    TOKEN_CACHE.write_text(json.dumps(payload, indent=1), encoding="utf-8")


# --------------------------------------------------------------- the single attempt
def attempt_once(cfg: dict) -> tuple[str | None, str]:
    """Exactly one POST /arcontoken. Latches on failure. Never retries."""
    global _ATTEMPTED_THIS_PROCESS

    latch = latch_state()
    if latch is not None:
        return None, (
            f"BLOCKED by failure latch - previous attempt returned "
            f"{latch.get('status')}: {str(latch.get('body'))[:160]!r}. "
            f"Clear it with: python tools\\token_guard.py clear-latch"
        )

    if _ATTEMPTED_THIS_PROCESS:
        return None, "already attempted once in this process - refusing a second call"
    _ATTEMPTED_THIS_PROCESS = True

    url = cfg.get("pam_tokenAPIUrl", "")
    # Credentials may be supplied out of band via the environment, which is how a rotated password
    # is used without writing it into Environments/<env>.properties -- that file is git-tracked, so
    # editing it would commit a live credential. Env wins; the file is the fallback.
    username = os.environ.get("PAM_API_TOKEN_USER") or cfg.get("pam_APITokenUserName", "")
    password = os.environ.get("PAM_API_TOKEN_PASS") or cfg.get("pam_APITokenPassword", "")
    cred_src = ("env $PAM_API_TOKEN_USER/$PAM_API_TOKEN_PASS"
                if os.environ.get("PAM_API_TOKEN_PASS") else "Environments properties file")
    print(f"   credentials from: {cred_src}")
    body = urllib.parse.urlencode({
        "grant_type": cfg.get("pam_grantType", "password").strip(),
        "username": username,
        "password": password,
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/x-www-form-urlencoded"})

    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT, context=SSL_CTX) as r:
            payload = json.loads(r.read().decode("utf-8", "replace"))
        tok = payload.get("access_token")
        if not tok:
            record_failure(r.status, f"no access_token in response: {list(payload)}",
                           username)
            return None, f"no access_token in response: {list(payload)}"
        write_cache(payload)
        return tok, "generated fresh (one attempt, cached for reuse)"
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read()[:600].decode("utf-8", "replace")
        except Exception:                                                # noqa: BLE001
            pass
        record_failure(e.code, detail, username)
        return None, f"HTTP {e.code}: {detail}"
    except Exception as exc:                                             # noqa: BLE001
        # Network/TLS/timeout faults are latched too. We cannot tell a refused
        # login from a dropped connection, and guessing wrong costs an account.
        record_failure(None, f"{type(exc).__name__}: {exc}", username)
        return None, f"{type(exc).__name__}: {exc}"


# ------------------------------------------------------------------- the entry point
def acquire(cfg: dict, allow_network: bool = True) -> tuple[str | None, str]:
    """Resolution order: $PAM_API_TOKEN -> valid cache -> ONE live attempt.

    Returns (None, reason) rather than raising. Callers must STOP on None, never loop.
    """
    env = os.environ.get("PAM_API_TOKEN")
    if env:
        return env.strip(), "$PAM_API_TOKEN"

    tok, note = read_cache()
    if tok:
        return tok, note

    if not allow_network:
        return None, f"{note}; network calls not permitted"

    return attempt_once(cfg)


# ---------------------------------------------------------------------------- CLI
def _load_cfg() -> dict:
    """Read QA_MsSQL.properties without importing a heavier harness module."""
    root = workspace_root(HERE)   # OBJ-025: was an inline Reports/ + repo probe
    env_file = (root / "Automation gitlab repo" / "pam_automation_bootstrap"
                / "Environments" / "QA_MsSQL.properties")
    cfg = {}
    for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    return cfg


def _status() -> int:
    print(f"cache file : {TOKEN_CACHE}")
    tok, note = read_cache()
    print(f"cache      : {note}")
    if tok:
        c = jwt_claims(tok)
        print(f"  APIUserId: {c.get('APIUserId')}   exp epoch: {c.get('exp')}")
    latch = latch_state()
    print(f"latch file : {ATTEMPT_LATCH}")
    if latch is None:
        print("latch      : none - one attempt is permitted if the cache is expired")
    else:
        print(f"latch      : [BLOCKED] status {latch.get('status')}")
        print(f"             {str(latch.get('body'))[:200]}")
        print("             clear with: python tools\\token_guard.py clear-latch")
    print(f"$PAM_API_TOKEN: {'set' if os.environ.get('PAM_API_TOKEN') else 'not set'}")
    return 0


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"

    if cmd == "status":
        return _status()

    if cmd == "clear-latch":
        print("latch cleared - ONE attempt is now permitted"
              if clear_latch() else "no latch present, nothing to clear")
        return 0

    if cmd == "refresh":
        # --force skips the cache and generates a new token even though the current one
        # is still valid. Legitimate when a long run must not straddle an expiry, or when
        # the account has just been confirmed healthy by hand. Still latch-gated and
        # still one-attempt-per-process: --force overrides the CACHE, never the SAFETY.
        force = "--force" in argv
        cfg = _load_cfg()
        tok, note = (attempt_once(cfg) if force
                     else acquire(cfg, allow_network=True))
        if tok:
            print(f"OK: token available: {note}")
            print(f"   {seconds_left(tok) // 60} min of life remaining")
            return 0
        print(f"FAILED: NO TOKEN: {note}")
        print()
        print("   Not retrying. Tell the owner and stop - a repeated attempt is what")
        print("   locked GenericScheduler on 2026-07-28 (ISSUE-009 section 4a).")
        return 2

    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
