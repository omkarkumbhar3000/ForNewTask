#!/usr/bin/env python3
"""OBJ-010 - generate negative / boundary / input-validation flows from the QA team's
own Excel scenario data.

Why a second generator
----------------------
`generate_flows.py` derives chains from APIConfig.java + the payload helpers. Everything
it emits is POSITIVE: lifecycle (create -> read back -> update) and read sweeps. It has
no notion of an expected rejection, so negative, boundary, input-validation and
error-handling scenarios were entirely absent from the dynamic framework.

The bootstrap repo already holds those scenarios as data - 6,119 rows across three
workbooks, each row carrying verb, endpoint, payload and, for the 2,104 negative rows,
both `ExpectedHTTPStatus` and `ExpectedErrorCode`. That is a real, authored expectation,
unlike the OBJ-007 static matrix where 73.4% of rows have no known outcome. So this
generator reads those rows as a REFERENCE ASSET and emits flow JSON in the identical
shape `chain_runner.py` already executes. No Java is run.

Exclusions are computed here, at planning time, not discovered mid-run - and every
withheld row is written out with its reason so the run report can show it as Blocked
rather than silently missing.

  python tools/generate_data_flows.py           # generate
  python tools/generate_data_flows.py --stats   # report only, write nothing
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import shutil
import sys
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chain_runner import DESTRUCTIVE, ENDPOINT_BLOCKLIST              # noqa: E402
from obj010_datatables import load_api_rows                           # noqa: E402

OUT_DIR = HERE / "flows" / "generated-data"
DIAG_DIR = workspace_root(__file__) / "state" / "obj010"

HOPS_PER_FLOW = 12
TIER = 4                       # tier 1-3 are generate_flows.py's; 4 is data-driven
SLA_MS = 25000

# Measured by obj010_admin_auth_probe.py: GET /AdminAPI/... returns HTTP 404 on BOTH
# https://u16hf.arconnet.com:6302 and :1302, with the bearer JWT and with the hardcoded
# token the reference Settings.java uses. The surface is not deployed on QA_MsSQL, so
# the reference tests would 404 too. Withheld as Blocked, with the measurement as reason.
ADMIN_API_REASON = ("/AdminAPI surface is not deployed on QA_MsSQL - measured HTTP 404 "
                    "on :6302 and :1302 with both the bearer JWT and the reference "
                    "Settings.java token (obj010_admin_auth_probe.py)")

PLACEHOLDER = {"", "-", "na", "n/a", "null", "none"}


def normalise_path(ep: str) -> tuple[str | None, str | None]:
    """Return (path, blocked_reason). Only same-origin /... paths are executable."""
    ep = (ep or "").strip()
    if not ep:
        return None, "empty endpoint cell"
    if ep.lower().startswith(("http://", "https://")):
        return None, (f"absolute URL pins a host this run does not target ({ep[:60]}) - "
                      "the row hardcodes a developer machine, not QA_MsSQL")
    if not ep.startswith("/"):
        ep = "/" + ep
    if ep.lstrip("/").lower().startswith("adminapi"):
        return None, ADMIN_API_REASON
    if not ep.startswith("/api/"):
        return None, f"endpoint is not an /api/ path ({ep[:60]})"
    return ep, None


def action_of(path: str) -> str:
    """Strip the query BEFORE splitting on '/'.

    A query string can contain '/' - one row carries the date 07/08/2059 in its query - so
    splitting on '/' first returns mid-query garbage as the action name. That name is what
    the blocklist and destructive guards inspect, and what the evidence filename is built
    from. Measured on this corpus: 1 row differs, and no guard decision changes.
    """
    return path.split("?")[0].rstrip("/").split("/")[-1]


def blocklist_reason(action: str) -> str | None:
    """Substring match, deliberately wider than chain_runner's historic exact match.

    ISSUE-010 records GetAllActiveUserDetails as hanging "on every version", and LH-08
    puts 98 endpoints at risk. GetAllActiveUserDetailsNew / ...Mapping are exactly that
    family, so the guard has to catch the variants, not just the base name.
    """
    for key, why in ENDPOINT_BLOCKLIST.items():
        if key.lower() in action.lower():
            return f"{why} (matched blocklist entry '{key}')"
    return None


def scenario_of(row: dict) -> str:
    """The QA team's own taxonomy, taken from the named table rather than invented.

    Measured suffixes across the negative corpus: MethodNotAllowed (1,263),
    UnauthorizedAccess (1,153), InvalidQueryParams (18), plain '_Negative' (2,104).
    """
    table = row.get("table") or ""
    for tag in ("MethodNotAllowed", "UnauthorizedAccess", "InvalidQueryParams",
                "InvalidDataType", "BoundaryValue", "MissingMandatory"):
        if table.endswith(tag) or f"_{tag}" in table:
            return tag
    if row["kind"] == "negative":
        return "NegativeValidation"
    return "Positive"


def parse_body(payload: str):
    """Mirror what the reference does: the Payload cell goes to the wire as authored.

    ApiHelper.getResponse passes the raw String to Playwright's setData, so a malformed
    payload like `{SsoApiRefId:1,}` is sent malformed - which for a negative row is the
    point of the test. Parse when we can, send verbatim when we cannot.
    """
    p = (payload or "").strip()
    if p.lower() in PLACEHOLDER:
        return None
    try:
        return json.loads(p)
    except Exception:                                                 # noqa: BLE001
        return {"__raw__": p}          # chain_runner sends __raw__ bodies byte-for-byte


def build():
    rows, diag = load_api_rows()
    blocked: list[dict] = []
    keep: list[dict] = []

    for r in rows:
        path, why = normalise_path(r["endpoint"])
        if why or path is None:
            why = why or "endpoint could not be normalised"
            blocked.append({**r, "blocked_reason": why, "blocked_class": (
                "surface-not-deployed" if "AdminAPI" in why
                else "unreachable-host" if "absolute URL" in why
                else "malformed-endpoint")})
            continue
        action = action_of(path)
        bl = blocklist_reason(action)
        if bl:
            blocked.append({**r, "endpoint": path, "blocked_reason": bl,
                            "blocked_class": "safety-blocklist"})
            continue
        if DESTRUCTIVE.match(action):
            blocked.append({**r, "endpoint": path, "blocked_class": "destructive",
                            "blocked_reason": (
                                f"destructive action name '{action}' and teardown is "
                                "disabled for this run (OBJ-010 Q8) - it would delete "
                                "records this run did not create")})
            continue
        keep.append({**r, "endpoint": path, "action": action})

    # group into flows: one family per (kind, module), batched so a flow stays reviewable
    groups: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for r in keep:
        groups[(r["kind"], r["module"] or r["provider"])].append(r)

    files: dict[str, list] = collections.defaultdict(list)
    for (kind, module), items in sorted(groups.items()):
        slug = re.sub(r"[^a-z0-9]+", "_", f"{module}".lower()).strip("_") or "unknown"
        for i in range(0, len(items), HOPS_PER_FLOW):
            chunk = items[i:i + HOPS_PER_FLOW]
            hops = []
            for r in chunk:
                hop = {
                    "name": r["action"],
                    "verb": r["verb"],
                    "path": r["endpoint"],
                    "sla_ms": SLA_MS,
                    "stop_on_fail": False,
                    "note": (f"{r['kind']} row from {r['workbook']} / "
                             f"{r['sheet']} / {r['table']} row {r['row_index']} "
                             f"(provider {r['provider']})"),
                }
                body = parse_body(r["payload"])
                if body is not None:
                    hop["body"] = body
                if r["expect_status"]:
                    try:
                        hop["expect_status"] = int(r["expect_status"])
                    except ValueError:
                        pass
                hop["scenario"] = scenario_of(r)
                if hop["scenario"] == "UnauthorizedAccess":
                    # The table name states the intent, but the row carries no token
                    # column and the reference class sends the same VALID token - so as
                    # authored these 1,153 rows assert 401 while presenting valid
                    # credentials, and can only ever fail (or pass for the wrong reason
                    # if the shared ApiToken happens to be expired). Supplying a bogus
                    # credential is what makes the assertion mean what it says.
                    hop["auth"] = "invalid"
                    hop["note"] += ("; dynamic framework supplies an INVALID credential "
                                    "- the source row does not, so the reference test "
                                    "cannot exercise unauthorized access")
                if r["kind"] == "negative":
                    hop["negative"] = True
                    if r["expect_error_code"]:
                        hop["expect_error_code"] = r["expect_error_code"]
                hops.append(hop)
            files[f"{kind}_{slug}"].append({
                "id": f"data_{kind}_{slug}_{i // HOPS_PER_FLOW + 1}",
                "title": f"{module} - {kind} data-driven batch {i // HOPS_PER_FLOW + 1}",
                "why": ("Executes the QA team's authored " + kind + " scenarios through "
                        "the dynamic framework. Each hop is one Excel row, sent as "
                        "authored, and asserted against the expected status"
                        + (" and error code." if kind == "negative" else ".")),
                "generated": True,
                "data_driven": True,
                "kind": kind,
                "tier": TIER,
                "controller": module,
                "hops": hops,
            })
    return files, keep, blocked, diag


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    files, keep, blocked, diag = build()
    flows = sum(len(v) for v in files.values())
    hops = sum(len(f["hops"]) for v in files.values() for f in v)
    kinds = collections.Counter(r["kind"] for r in keep)
    bclass = collections.Counter(b["blocked_class"] for b in blocked)

    print(f"providers resolved      : {diag['resolved']} of {diag['providers']}")
    print(f"executable API rows     : {len(keep) + len(blocked)}")
    print(f"  -> generated as hops  : {len(keep)}  {dict(kinds)}")
    print(f"  -> withheld as Blocked: {len(blocked)}")
    for k, n in bclass.most_common():
        print(f"       {k:<24} {n}")
    print()
    print(f"flow files              : {len(files)}")
    print(f"total flows             : {flows}")
    print(f"total hops              : {hops}")

    if args.stats:
        print("\n--stats: nothing written")
        return 0

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, fl in sorted(files.items()):
        (OUT_DIR / f"{name}.json").write_text(json.dumps(fl, indent=1), encoding="utf-8")

    # Diagnostics live OUTSIDE flows/ - chain_runner rglobs that tree for flow JSON.
    DIAG_DIR.mkdir(exist_ok=True)
    (DIAG_DIR / "blocked-rows.json").write_text(
        json.dumps({"blocked": blocked,
                    "summary": dict(bclass),
                    "unresolved_providers": diag["unresolved"]}, indent=1),
        encoding="utf-8")
    print(f"\nwritten to {OUT_DIR}")
    print(f"blocked rows -> {DIAG_DIR / 'blocked-rows.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
