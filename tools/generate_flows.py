#!/usr/bin/env python3
"""Generate chain flow definitions from the framework's own assets.

Nothing here is hand-listed. Three inputs, all already in the repo:

  1. APIConfig.java              1,318 endpoint declarations - controller, action, verb
  2. utils/apiPayload/*.java     1,289 zero-arg methods holding the literal request JSON
  3. a small set of context rules  which fields are chainable ids vs per-run identity

Output is flow JSON in the same shape as the hand-written flows, one file per
controller, written to tools/flows/generated/. The executor
(chain_runner.py) is unchanged - that is the point: generated and hand-written flows
are the same artifact.

  python tools/generate_flows.py            # generate
  python tools/generate_flows.py --stats    # report only, write nothing
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chain_runner import REPO, ENDPOINT_BLOCKLIST          # noqa: E402

APICONFIG = REPO / "src/test/java/com/arcon/autoconfigs/APIConfig.java"
PAYLOAD_DIR = REPO / "src/test/java/com/arcon/utils/apiPayload"
OUT_DIR = HERE / "flows" / "generated"

# ---------------------------------------------------------------- classification
WRITE_NEW = re.compile(r"^(set|insert|create|add|save)", re.I)
READ = re.compile(r"^(get|fetch|list|view|check|validate|search|is|has)", re.I)
CHANGE = re.compile(r"^(update|modify|edit|enable|map|assign|approve|reject|resend)", re.I)
TEARDOWN = re.compile(r"^(delete|remov|drop|purge|revoke|unmap|disable|deactivate)", re.I)

# Fields whose value must come from an earlier hop, not from the stale literal payload.
CONTEXT = {
    "lobid": "${LOB_ID}", "lob_id": "${LOB_ID}", "lobsid": "${LOB_ID}",
    "usergroupid": "${USER_GROUP_ID}", "user_group_id": "${USER_GROUP_ID}",
    "servergroupid": "${SERVER_GROUP_ID}",
    "servicegroupid": "${SERVICE_GROUP_ID}",
}
# Fields that must be unique per run or the create collides with a previous run.
IDENTITY = {
    "username": "${NEW_USERNAME}", "userid": "${NEW_USERNAME}",
    "userdisplayname": "${NEW_USERNAME}", "displayname": "${NEW_USERNAME}",
    "loginid": "${NEW_USERNAME}", "name": "${NEW_USERNAME}",
    "emailid": "${NEW_USER_EMAIL}", "email": "${NEW_USER_EMAIL}",
    "mobileno": "${NEW_USER_MOBILE}", "mobilenumber": "${NEW_USER_MOBILE}",
    "password": "${NEW_USER_PASSWORD}",
    "hostname": "${NEW_SERVICE_HOST}", "ipaddress": "${NEW_SERVICE_HOST}",
    "serverip": "${NEW_SERVICE_HOST}", "serverhostname": "${NEW_SERVICE_HOST}",
    "servicousername": "${NEW_SERVICE_USER}", "serviceusername": "${NEW_SERVICE_USER}",
    "servicepassword": "${NEW_SERVICE_PASSWORD}",
    "port": "${NEW_SERVICE_PORT}",
}
# Never randomise or rewrite these - they are enum-ish and a wrong value breaks the call.
KEEP = {"usertypeid", "dualfactortypeid", "servicetypeid", "domain", "domainname",
        "logtypeid", "objecttypeid", "parameter", "allowpasswordchange",
        "vault_password_immediately", "instancename", "dbinstancename"}

# The LOB prelude every generated flow starts from, so no id is hardcoded.
PRELUDE = [
    {"name": "GetLOBList", "verb": "POST", "path": "/api/ADbridging/GetLOBList",
     "body": {},
     "find_extract": {"in": "Result", "where": {"LobName": "AUTOMATION_TEST_LOB"},
                      "take": {"LOB_ID": "LobId", "LOB_NAME": "LobName"}},
     "sla_ms": 8000},
    {"name": "GetUserGroupList", "verb": "GET",
     "path": "/api/UserDetails/GetUserGroupListWithoutMandateValue",
     "find_extract": {"in": "Result", "where": {"LOBName": "${LOB_NAME}"},
                      "take": {"USER_GROUP_ID": "UserGroupId",
                               "USER_GROUP_NAME": "UserGroupName"}},
     "sla_ms": 12000},
    {"name": "GetServerGroupList", "verb": "POST",
     "path": "/api/ADbridging/GetServerGroupList", "body": {"LobId": "${LOB_ID}"},
     "extract": {"SERVER_GROUP_ID": "Result[0].ServerGroupId"},
     "stop_on_fail": False, "sla_ms": 8000},
]


# ------------------------------------------------------------------- java parsing
def java_literal(block: str):
    """Concatenate the double-quoted literals in a method body and parse as JSON."""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', block)
    if not parts:
        return None
    s = "".join(parts)
    for a, b in (('\\"', '"'), ("\\n", "\n"), ("\\t", "\t"), ("\\r", ""), ("\\\\", "\\")):
        s = s.replace(a, b)
    s = s.strip()
    if not s.startswith("{") and not s.startswith("["):
        return None                      # legitimately empty - the endpoint takes no body
    try:
        return json.loads(s)
    except Exception:                                                # noqa: BLE001
        pass
    repaired = re.sub(r",(\s*[}\]])", r"\1", s)          # trailing commas
    repaired = re.sub(r"[\x00-\x1f]", " ", repaired)     # stray control characters
    try:
        return json.loads(repaired)
    except Exception:                                                # noqa: BLE001
        return None


def load_endpoints() -> list[dict]:
    src = APICONFIG.read_text(encoding="utf-8", errors="replace")
    decl = re.compile(
        r'public\s+static\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;(?:\s*//\s*(\w+))?')
    out, seen = [], set()
    for name, path, verb in decl.findall(src):
        m = re.match(r"^/api/([^/]+)/([^/?]+)", path)
        if not m:
            continue
        key = (m.group(1), m.group(2), path)
        if key in seen:
            continue
        seen.add(key)
        act = m.group(2)
        role = ("create" if WRITE_NEW.match(act) else "teardown" if TEARDOWN.match(act)
                else "update" if CHANGE.match(act) else "read" if READ.match(act)
                else "other")
        out.append({"const": name, "path": path, "controller": m.group(1),
                    "action": act, "verb": (verb or "").upper() or "POST",
                    "role": role, "templated": "{" in path})
    return out


def load_payloads() -> dict[str, object]:
    """action-name (lowercased, version-stripped variants included) -> parsed JSON body."""
    meth = re.compile(r"public\s+String\s+(\w+)\s*\(\s*\)\s*\{(.*?)\n\t?\}", re.S)
    prefix = re.compile(r"^(post|put|patch|delete|payload|body)", re.I)
    vsuf = re.compile(r"V(\d+)$", re.I)
    out: dict[str, object] = {}
    for f in sorted(PAYLOAD_DIR.glob("*.java")):
        body = f.read_text(encoding="utf-8", errors="replace")
        for name, blk in meth.findall(body):
            parsed = java_literal(blk)
            if parsed is None:
                continue
            keys = {name.lower(), prefix.sub("", name).lower()}
            base = vsuf.sub("", name)
            keys |= {base.lower(), prefix.sub("", base).lower()}
            for k in keys:
                out.setdefault(k, parsed)
    return out


# ------------------------------------------------------------------ body rewriting
def rewrite(body, notes: list[str]):
    """Replace chainable ids with placeholders and identity fields with per-run values."""
    if isinstance(body, list):
        return [rewrite(v, notes) for v in body]
    if not isinstance(body, dict):
        return body
    out = {}
    for k, v in body.items():
        lk = k.lower()
        if isinstance(v, (dict, list)):
            out[k] = rewrite(v, notes)
        elif lk in CONTEXT:
            out[k] = CONTEXT[lk]
            notes.append(f"{k} <- {CONTEXT[lk]}")
        elif lk in KEEP:
            out[k] = v
        elif lk in IDENTITY:
            out[k] = IDENTITY[lk]
            notes.append(f"{k} <- {IDENTITY[lk]}")
        else:
            out[k] = v
    return out


def entity_of(action: str) -> str:
    """SetUserDetails -> user ; InsertLOBDetails -> lob. Used to pick the read-back."""
    a = WRITE_NEW.sub("", action)
    a = re.sub(r"(Details|Detail|Info|Data|Mapping|New|V\d+)$", "", a)
    return a.lower()


def pick_readback(entity: str, reads: list[dict]) -> dict | None:
    """Prefer a list endpoint naming the same entity, needing no body of its own."""
    def ok(e):
        return e["action"] not in ENDPOINT_BLOCKLIST and not e["templated"]

    cands = [e for e in reads if ok(e)]
    if not cands:
        return None
    scored = []
    for e in cands:
        a = e["action"].lower()
        s = 0
        if entity and entity in a:
            s += 10
        if "all" in a:
            s += 3
        if "list" in a:
            s += 3
        if "active" in a:
            s += 2
        if e["verb"] == "GET":
            s += 1
        scored.append((s, len(e["action"]), e))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return scored[0][2]


# ------------------------------------------------------------------------- emit
def build(endpoints: list[dict], payloads: dict) -> tuple[dict[str, list], dict]:
    by_ctrl = defaultdict(list)
    for e in endpoints:
        by_ctrl[e["controller"]].append(e)

    files: dict[str, list] = {}
    stats = defaultdict(int)
    stats["controllers"] = len(by_ctrl)

    for ctrl, eps in sorted(by_ctrl.items()):
        creates = [e for e in eps if e["role"] == "create"]
        reads = [e for e in eps if e["role"] == "read"]
        updates = [e for e in eps if e["role"] == "update"]
        downs = [e for e in eps if e["role"] == "teardown"]
        flows = []

        # ---- lifecycle flows: one per create endpoint that has a parseable body
        for c in creates:
            if c["action"] in ENDPOINT_BLOCKLIST:
                stats["skipped_blocklist"] += 1
                continue
            body = payloads.get(c["action"].lower())
            bodyless = body is None
            if bodyless:
                # No request body is defined anywhere in the framework for this create.
                # Still exercise it, with an empty body, so the gap is recorded with
                # evidence instead of silently dropped. Tier 3, no create expectation.
                stats["create_without_body"] += 1
                body = {}
            notes: list[str] = []
            rb = rewrite(body, notes)
            entity = entity_of(c["action"])
            back = pick_readback(entity, reads)

            hops = [dict(h) for h in PRELUDE]
            hops.append({
                "name": c["action"], "verb": c["verb"], "path": c["path"], "body": rb,
                "expect_created": not bodyless, "extract_any_id": "NEW_ID",
                "sla_ms": 20000, "stop_on_fail": not bodyless,
                "note": "generated from " + c["const"]
                        + ("; NO request body defined in the framework - called with {} "
                           "to record the gap" if bodyless else "")
                        + ("; chained: " + ", ".join(notes) if notes else ""),
            })
            if back:
                hop = {"name": f"{back['action']}__verify", "verb": back["verb"],
                       "path": back["path"], "sla_ms": 25000, "stop_on_fail": False,
                       "verify_value_anywhere": {"value": "${NEW_ID}",
                                                 "label": "created record id"},
                       "note": f"read-back chosen for entity '{entity}'"}
                if back["verb"] != "GET":
                    hop["body"] = payloads.get(back["action"].lower()) or {}
                    if isinstance(hop["body"], dict):
                        hop["body"] = rewrite(hop["body"], [])
                hops.append(hop)
                stats["with_readback"] += 1

            # ---- update hop, against the record this flow just created
            up = next((u for u in updates
                       if entity and entity in u["action"].lower()
                       and u["action"] not in ENDPOINT_BLOCKLIST), None)
            if up:
                ub = payloads.get(up["action"].lower())
                if isinstance(ub, dict):
                    hops.append({
                        "name": up["action"], "verb": up["verb"], "path": up["path"],
                        "body": rewrite(ub, []), "sla_ms": 20000, "stop_on_fail": False,
                        "note": "update against the record created above",
                    })
                    stats["with_update"] += 1

            # ---- teardown hop: self-created only, and opt-in at run time
            dn = next((d for d in downs
                       if entity and entity in d["action"].lower()
                       and d["action"] not in ENDPOINT_BLOCKLIST), None)
            if dn:
                db = payloads.get(dn["action"].lower())
                if isinstance(db, dict):
                    hops.append({
                        "name": dn["action"], "verb": dn["verb"], "path": dn["path"],
                        "body": rewrite(db, []), "sla_ms": 20000, "stop_on_fail": False,
                        "teardown": True,
                        "note": "removes the record this flow created; requires "
                                "--allow-teardown",
                    })
                    stats["with_teardown"] += 1

            flows.append({
                "id": f"{ctrl}__{c['action']}".lower(),
                "title": f"{ctrl} lifecycle - {c['action']}"
                         + (" (no body defined)" if bodyless else ""),
                "why": "Generated lifecycle chain: discover LOB context, create, read the "
                       "record back, then optionally update and remove it."
                       + (" This create has no payload defined in the framework, so it is "
                          "probed with an empty body to document the gap." if bodyless
                          else ""),
                "generated": True, "tier": 3 if bodyless else 1,
                "controller": ctrl, "hops": hops,
            })
            stats["lifecycle_flows" if not bodyless else "bodyless_probe_flows"] += 1
            stats["lifecycle_hops"] += len(hops)

        # ---- read-sweep flows: every remaining read endpoint, batched behind the prelude
        covered = {h["path"] for fl in flows for h in fl["hops"]}
        rest = [r for r in reads
                if r["path"] not in covered
                and r["action"] not in ENDPOINT_BLOCKLIST
                and not r["templated"]]
        BATCH = 10
        for i in range(0, len(rest), BATCH):
            chunk = rest[i:i + BATCH]
            hops = [dict(h) for h in PRELUDE]
            for r in chunk:
                hop = {"name": r["action"], "verb": r["verb"], "path": r["path"],
                       "sla_ms": 25000, "stop_on_fail": False,
                       "note": "read sweep; LOB context supplied by the prelude"}
                if r["verb"] != "GET":
                    pb = payloads.get(r["action"].lower())
                    hop["body"] = rewrite(pb, []) if isinstance(pb, dict) else {}
                hops.append(hop)
            flows.append({
                "id": f"{ctrl}__reads_{i // BATCH + 1}".lower(),
                "title": f"{ctrl} read sweep {i // BATCH + 1}",
                "why": "Exercises read endpoints inside a chain, so each one is called "
                       "with real LOB context rather than in isolation.",
                "generated": True, "tier": 2, "controller": ctrl, "hops": hops,
            })
            stats["read_flows"] += 1
            stats["read_hops"] += len(hops)

        if flows:
            files[ctrl] = flows
    return files, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    eps = load_endpoints()
    pl = load_payloads()
    files, stats = build(eps, pl)

    total_flows = sum(len(v) for v in files.values())
    total_hops = sum(len(f["hops"]) for v in files.values() for f in v)

    print(f"endpoints parsed        : {len(eps)}")
    print(f"payload bodies parsed   : {len(set(id(v) for v in pl.values()))} distinct "
          f"({len(pl)} lookup keys)")
    print()
    for k in ("controllers", "lifecycle_flows", "bodyless_probe_flows", "with_readback",
              "with_update", "with_teardown", "read_flows", "create_without_body",
              "skipped_blocklist"):
        print(f"  {k:22} {stats[k]}")
    print()
    print(f"flow files              : {len(files)}")
    print(f"total flows             : {total_flows}")
    print(f"total hops              : {total_hops}")

    if args.stats:
        print("\n--stats: nothing written")
        return 0

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)          # regenerating the PLAN is fine; run output is not
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for ctrl, flows in sorted(files.items()):
        (OUT_DIR / f"{ctrl}.json").write_text(
            json.dumps(flows, indent=1), encoding="utf-8")
    print(f"\nwritten to {OUT_DIR.relative_to(workspace_root(__file__))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
