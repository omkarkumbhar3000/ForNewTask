#!/usr/bin/env python3
"""validate_profile.py - the day-one readiness gate for a new project.

Answers one question: is this project's profile complete enough to execute against, and
if not, exactly what is missing and who can settle it.

It is deliberately dependency-free (Python standard library only), because the executor
it guards is dependency-free too. Adding jsonschema here would make the onboarding kit
harder to stand up than the thing being onboarded.

Two classes of check:

  STRUCTURE  - required keys, types, enums, patterns, from profile.schema.json.
  READINESS  - the checks a JSON Schema cannot express: a blocker field still reading
               "UNKNOWN", a production target, retry-on-a-lockable-account, an envelope
               section written without ever running a probe, a health probe that is
               itself blocklisted, an unexplained empty blocklist.

Exit codes: 0 ready to execute - 1 blocked - 2 bad usage.

Usage
-----
    python tools/onboarding/validate_profile.py profiles/_template.json   # exits 1: all UNKNOWN
    python tools/onboarding/validate_profile.py --all
    python tools/onboarding/validate_profile.py profiles/idev.json --quiet

Output is ASCII only, so it renders identically in PowerShell, cmd and CI logs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "profile.schema.json"
PROFILES = HERE / "profiles"

SENTINEL = "UNKNOWN"
JWT_LIKE = re.compile(r"^[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{10,}$")

# Every layer the solution defines. A profile may use a subset; it may not invent one.
KNOWN_LAYERS = {"L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10", "L11", "L12"}


class Findings:
    """Blockers stop execution. Warnings reduce coverage or invite a mistake."""

    def __init__(self) -> None:
        self.blockers: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []
        self.notes: list[tuple[str, str]] = []

    def block(self, where: str, why: str) -> None:
        self.blockers.append((where, why))

    def warn(self, where: str, why: str) -> None:
        self.warnings.append((where, why))

    def note(self, where: str, why: str) -> None:
        self.notes.append((where, why))


# --------------------------------------------------------------------- structure
def type_ok(value, declared: str) -> bool:
    if declared == "object":
        return isinstance(value, dict)
    if declared == "array":
        return isinstance(value, list)
    if declared == "string":
        return isinstance(value, str)
    if declared == "boolean":
        return isinstance(value, bool)
    if declared == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def check_node(value, spec: dict, path: str, f: Findings) -> None:
    """Validate one node against its schema fragment. Only the subset of JSON Schema the
    profile format actually uses - deliberately not a general implementation."""
    declared = spec.get("type")
    if declared and not type_ok(value, declared):
        f.block(path, f"expected {declared}, got {type(value).__name__}")
        return

    if "enum" in spec and value not in spec["enum"]:
        f.block(path, f"{value!r} is not one of {spec['enum']}")

    if "pattern" in spec and isinstance(value, str):
        if not re.match(spec["pattern"], value):
            f.block(path, f"{value!r} does not match {spec['pattern']}")

    if "minimum" in spec and isinstance(value, (int, float)) and value < spec["minimum"]:
        f.block(path, f"{value} is below the minimum {spec['minimum']}")

    if "maximum" in spec and isinstance(value, (int, float)) and value > spec["maximum"]:
        f.block(path, f"{value} is above the maximum {spec['maximum']}")

    if "minItems" in spec and isinstance(value, list) and len(value) < spec["minItems"]:
        f.block(path, f"needs at least {spec['minItems']} item(s), has {len(value)}")

    if isinstance(value, dict):
        for req in spec.get("required", []):
            if req not in value:
                f.block(f"{path}.{req}" if path else req, "required field is missing")
        for key, sub in spec.get("properties", {}).items():
            if key in value:
                check_node(value[key], sub, f"{path}.{key}" if path else key, f)

    if isinstance(value, list) and isinstance(spec.get("items"), dict):
        for i, item in enumerate(value):
            check_node(item, spec["items"], f"{path}[{i}]", f)


def blocker_paths(spec: dict, prefix: str = "") -> list[str]:
    """Every field the schema annotates x-blocker, as a dotted path."""
    out = []
    for key, sub in spec.get("properties", {}).items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(sub, dict):
            if sub.get("x-blocker"):
                out.append(path)
            out.extend(blocker_paths(sub, path))
    return out


def dig(doc, dotted: str):
    cur = doc
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


# --------------------------------------------------------------------- readiness
def check_readiness(p: dict, f: Findings) -> None:
    """The checks that matter operationally and that a schema cannot express."""

    # 1. A blocker field still carrying the sentinel is an unanswered question, not a value.
    for path in blocker_paths(json.loads(SCHEMA.read_text(encoding="utf-8"))):
        v = dig(p, path)
        if v == SENTINEL or (isinstance(v, str) and v.strip() == ""):
            f.block(path, "blocker field is still UNKNOWN - answer it before executing")

    env = p.get("environment", {})
    auth = p.get("auth", {})
    cat = p.get("catalogue", {})
    env_lope = p.get("envelope", {})
    safety = p.get("safety", {})
    val = p.get("validation", {})
    rep = p.get("reporting", {})

    # 2. Never point this at production. Not a warning - a refusal.
    if env.get("is_production") is not False:
        f.block("environment.is_production", "REFUSED: this solution issues writes. "
                                             "It targets a disposable environment only")

    # 3. Retry and account lockout are incompatible.
    risk = auth.get("lockout_risk")
    attempts = auth.get("max_token_attempts_per_run")
    if risk in ("high", SENTINEL, None) and attempts not in (1, None):
        f.block("auth.max_token_attempts_per_run",
                f"lockout_risk is {risk!r}; attempts must be 1. Repeated credential calls "
                "locked a shared service account on the reference project")
    if risk == SENTINEL:
        f.warn("auth.lockout_risk", "unknown lockout policy - assuming high. Ask the "
                                    "identity owner before an unattended run")
    if auth.get("latch_on_failure") is False and risk in ("high", "medium"):
        f.block("auth.latch_on_failure",
                "must be true at this lockout risk, or 'once per run' becomes 'every run'")
    if not auth.get("env_var_override"):
        f.warn("auth.env_var_override", "no env-var bypass defined; an unattended run has "
                                        "no way to supply a token without touching the "
                                        "credential endpoint")
    if not auth.get("roles"):
        f.warn("auth.roles", "no identities listed - authorization testing will be inert")
    if not auth.get("invalid_token_sample"):
        f.warn("auth.invalid_token_sample",
               "negative auth tests need a deliberately invalid credential. Asserting 401 "
               "while sending a VALID token is an assertion that cannot fail")

    # 4. Deny by default.
    if safety.get("default_mode") != "plan-only":
        f.block("safety.default_mode", "must be plan-only: a bare run issues zero HTTP calls")

    # 5. An empty blocklist must be a decision, not an oversight.
    if not safety.get("blocklist"):
        f.warn("safety.blocklist", "empty. Record the answer to 'which endpoints can take "
                                   "this environment down?' even if it is 'none known'")

    # 6. The destructive guard must compile, and must be name-based.
    rx = safety.get("destructive_name_regex")
    if rx:
        try:
            re.compile(rx)
        except re.error as exc:
            f.block("safety.destructive_name_regex", f"does not compile: {exc}")
    else:
        f.block("safety.destructive_name_regex", "missing - nothing guards a destructive call")

    # 7. The health probe must be safe, present, and not itself blocklisted.
    probe = safety.get("health_probe") or {}
    if not probe.get("path"):
        f.warn("safety.health_probe", "no probe defined - downtime detection and "
                                      "wait/resume cannot work")
    else:
        path = probe["path"]
        for key in (safety.get("blocklist") or {}):
            if key.lower() in path.lower():
                f.block("safety.health_probe",
                        f"probe path hits blocklisted '{key}' - the liveness check would "
                        "be the thing that kills the environment")
        action = path.split("?")[0].rstrip("/").split("/")[-1]
        if rx and re.match(rx, action, re.I):
            f.block("safety.health_probe", f"probe action {action!r} matches the "
                                           "destructive-name guard")

    # 8. An envelope section written without a probe is a guess.
    if not env_lope.get("shapes_measured"):
        f.block("envelope.shapes_measured",
                "0 - no probe has been run, so every assertion below is a guess. Probe "
                "10-20 read endpoints and record what came back")
    if env_lope.get("status_is_authoritative") is False and not env_lope.get("success_fields"):
        f.block("envelope.success_fields",
                "status is not authoritative and no success field is named, so nothing "
                "can distinguish a 200-shaped failure from a success")

    # 9. Layers must be known, and L3 is mandatory when status lies.
    layers = set(val.get("layers") or [])
    unknown_layers = layers - KNOWN_LAYERS
    if unknown_layers:
        f.block("validation.layers", f"unrecognised layer(s): {sorted(unknown_layers)}")
    if env_lope.get("status_is_authoritative") is False and "L3" not in layers:
        f.block("validation.layers",
                "L3 (envelope) is mandatory when status_is_authoritative is false - "
                "without it a rejected request scores as a pass")
    if "L11" in layers and (val.get("database") or {}).get("read_only") is not True:
        f.block("validation.database.read_only",
                "L11 is enabled without a read-only database account")
    if "L1" in layers and len(layers) == 1:
        f.block("validation.layers", "status-only validation. This is the failure mode the "
                                     "whole approach exists to prevent")

    # 10. Retention decides whether a benchmark is ever possible.
    if rep.get("retention") != "forever":
        f.warn("reporting.retention", f"{rep.get('retention')!r} - deleting prior runs "
                                      "destroys the N-1 baseline, and you find out when "
                                      "you need it")
    if not rep.get("evidence_per_call"):
        f.warn("reporting.evidence_per_call", "without per-call evidence a finding cannot "
                                              "be verified and a baseline cannot be "
                                              "re-scored offline")

    # 11. Coverage degradations, stated rather than discovered later.
    if cat.get("adapter") not in ("openapi", "postman", None, SENTINEL):
        f.note("catalogue.adapter", f"{cat.get('adapter')!r} - no published spec, so the "
                                    "catalogue is derived. Expect drift; assert "
                                    "expected_count so drift fails loudly")
    if not p.get("payloads", {}).get("adapter") or p["payloads"]["adapter"] in ("none", SENTINEL):
        f.warn("payloads.adapter", "no payload source - coverage degrades to read-only and "
                                   "creates cannot be generated")
    if not p.get("identity_prelude"):
        f.warn("identity_prelude", "empty - the most commonly missed input. Without it "
                                   "every payload is environment-bound and flows are not "
                                   "portable between environments")
    if not p.get("id_aliases") and p.get("identity_prelude"):
        f.warn("id_aliases", "a prelude discovers ids but nothing maps them onto payload "
                             "field names, so generated bodies keep their stale literals")

    # 12. Unknowns the author already flagged as blocking.
    for u in p.get("unknowns") or []:
        if u.get("blocks"):
            f.block(f"unknowns[{u.get('field')}]",
                    f"{u.get('question')} -> settled by: {u.get('settled_by')} "
                    f"(owner: {u.get('owner', 'UNKNOWN')})")

    # 13. A profile is not a secret store.
    for path, value in walk_strings(p):
        if JWT_LIKE.match(value):
            f.block(path, "looks like a real token. Profiles hold KEY NAMES, never secret "
                          "values - they are shared and reviewed")


def walk_strings(node, prefix: str = ""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{prefix}[{i}]")
    elif isinstance(node, str):
        yield prefix, node


# ------------------------------------------------------------------------ report
def validate(path: Path, quiet: bool = False) -> int:
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[BLOCK] {path.name}: cannot read as JSON - {exc}")
        return 1

    f = Findings()
    check_node(profile, json.loads(SCHEMA.read_text(encoding="utf-8")), "", f)
    check_readiness(profile, f)

    key = (profile.get("project") or {}).get("key", "?")
    name = (profile.get("project") or {}).get("name", "?")
    ready = not f.blockers

    print()
    print("=" * 78)
    print(f" {path.name}  -  project {key} ({name})")
    print("=" * 78)

    if f.blockers:
        print(f"\nBLOCKERS ({len(f.blockers)}) - execution is not permitted until these are answered:")
        for where, why in f.blockers:
            print(f"  [BLOCK] {where}")
            print(f"          {why}")
    if f.warnings and not quiet:
        print(f"\nWARNINGS ({len(f.warnings)}) - a run is possible; coverage or safety is reduced:")
        for where, why in f.warnings:
            print(f"  [WARN]  {where}")
            print(f"          {why}")
    if f.notes and not quiet:
        print(f"\nNOTES ({len(f.notes)}):")
        for where, why in f.notes:
            print(f"  [NOTE]  {where}: {why}")

    open_unknowns = len(profile.get("unknowns") or [])
    print(f"\nVERDICT: {'READY TO EXECUTE' if ready else 'BLOCKED'}"
          f"   blockers={len(f.blockers)} warnings={len(f.warnings)} "
          f"declared-unknowns={open_unknowns}")
    if ready and f.warnings:
        print("         Ready, with the reductions listed above stated in the run report.")
    print()
    return 0 if ready else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("profile", nargs="?", help="path to a profile JSON file")
    ap.add_argument("--all", action="store_true", help="validate every profile in profiles/")
    ap.add_argument("--quiet", action="store_true", help="blockers only")
    a = ap.parse_args()

    if not SCHEMA.exists():
        print(f"[BLOCK] schema not found at {SCHEMA}")
        return 2

    if a.all:
        files = sorted(x for x in PROFILES.glob("*.json") if not x.name.startswith("_"))
        if not files:
            print(f"[BLOCK] no profiles in {PROFILES}")
            return 2
        return max(validate(x, a.quiet) for x in files)

    if not a.profile:
        ap.print_help()
        return 2

    target = Path(a.profile)
    if not target.is_absolute() and not target.exists():
        target = HERE / a.profile
    if not target.exists():
        print(f"[BLOCK] no such profile: {a.profile}")
        return 2
    return validate(target, a.quiet)


if __name__ == "__main__":
    sys.exit(main())
