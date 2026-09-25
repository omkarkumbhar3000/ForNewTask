#!/usr/bin/env python3
"""OBJ-010 - decide which credential the /AdminAPI surface accepts.

Why this is needed
------------------
2,104 of the 6,119 Excel-derived API rows target `/AdminAPI/...`. The reference test
class that drives them (`tests/API_Dynamic/Settings.java`) does NOT use the bearer JWT
from /arcontoken - it hardcodes a long ARCON-encrypted token. If the dynamic framework
sends the JWT to /AdminAPI and that surface wants the other credential, all 2,104 rows
return 401 and the whole negative dimension is wasted.

So: two calls, one per credential, against a deliberately safe target - a GET issued at
an endpoint whose only supported verb is POST. That is itself one of the QA team's
"wrong HTTP method" negative cases, so it mutates nothing.

  python tools/obj010_admin_auth_probe.py --execute

Deny-by-default: without --execute this prints the plan and issues zero HTTP calls.
Never calls /arcontoken - the JWT comes from the existing cache via token_guard.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import token_guard                                                   # noqa: E402
from chain_runner import REPO, SSL_CTX, load_env                     # noqa: E402

SETTINGS_JAVA = REPO / "src/test/java/com/arcon/tests/API_Dynamic/Settings.java"

# A GET against a POST-only endpoint: the reference suite's own method-mismatch case.
PROBE_PATH = ("/AdminAPI/api/AdvancedUtility/"
              "UpdateConvertAllServiceDomainNameToUppercaseService")


def settings_token() -> str | None:
    """The live (uncommented) hardcoded token in the reference Settings.java."""
    if not SETTINGS_JAVA.is_file():
        return None
    live = re.sub(r"(?m)^\s*//.*$", "", SETTINGS_JAVA.read_text(encoding="utf-8",
                                                                errors="replace"))
    m = re.search(r'token\s*=\s*"([^"]{200,})"\s*;', live)
    return m.group(1) if m else None


def probe(label: str, base: str, token: str) -> None:
    req = urllib.request.Request(base + PROBE_PATH, method="GET")
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Content-Type", "application/json")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=45, context=SSL_CTX) as r:
            body = r.read(400)
            ms = int((time.time() - t0) * 1000)
            print(f"  {label:9} HTTP {r.status} in {ms:>5} ms  "
                  f"{r.headers.get('Content-Type')}\n             body={body[:250]!r}")
    except urllib.error.HTTPError as e:
        ms = int((time.time() - t0) * 1000)
        print(f"  {label:9} HTTP {e.code} in {ms:>5} ms\n"
              f"             body={e.read(250)!r}")
    except Exception as exc:                                         # noqa: BLE001
        print(f"  {label:9} transport error: {exc!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true",
                    help="issue the two probe calls (default: plan only)")
    args = ap.parse_args()

    cfg = load_env()
    base = cfg.get("pam_BaseAPIURL", "").rstrip("/")
    stok = settings_token()
    jwt, src = token_guard.acquire(cfg, allow_network=False)

    print(f"base            : {base}")
    print(f"probe target    : GET {PROBE_PATH}")
    print(f"JWT             : {src}")
    print(f"Settings token  : {'found, %d chars' % len(stok) if stok else 'NOT FOUND'}")

    if not args.execute:
        print("\nplan only - 0 HTTP calls. Re-run with --execute.")
        return 0
    if not jwt:
        print("\n⛔ no cached JWT and this script never calls /arcontoken. Stopping.")
        return 2

    # /AdminAPI is not necessarily on pam_BaseAPIURL. The env file carries a
    # commented-out `pam_settingsapiurl=...:1302`, so the app port is a candidate.
    bases = [base]
    app = (cfg.get("environmentUrl") or "").rstrip("/")
    if app and app not in bases:
        bases.append(app)

    for b in bases:
        print(f"\nprobing {b} (2 calls):")
        probe("JWT", b, jwt)
        time.sleep(2)
        if stok:
            probe("SETTINGS", b, stok)
            time.sleep(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
