#!/usr/bin/env python3
"""OBJ-007 items 11 & 12 - measure the developer-repo shortfall and the documentation gap.

ZERO HTTP CALLS. ZERO DB QUERIES. Static analysis only, over sources already on disk:

  1. APIConfig.java                   the 1,306-endpoint catalogue (what we target)
  2. pam/PAM/**/*.cs                  the developer product snapshot (what we were given)
  3. artifacts/rag-corpus/corpus.jsonl  the 2,470-page Confluence export, page-cited
  4. tools/source-map.json  the prior 4-source merge (payload binding)
  5. artifacts/runs/2026-07-29_181439/results.json   measured consequences

WHY THIS EXISTS
  Two documents disagree about how many of the 70 declared controllers are absent from pam/PAM:
  23 (BLAST/findings.md, docs/history/archive/workbench-archive/.../dynamic-api-generation.md, LH-05 pack) versus
  54 (docs/gaps/01-Data-Gap-Analysis.md, tools/SOURCE-MAP.md). The 54 in
  SOURCE-MAP.md is a HARDCODED STRING in build_source_map.py:333 - not a computed value. This
  script computes every candidate definition of "absent" so the number can be settled by
  definition rather than by assertion.

OUTPUT
  artifacts/analysis-data/doc-gap-coverage.json   one row per controller (the deliverable)
  <scratch>/measure-doc-gap-summary.json  every headline figure, for the report author

  python tools/measure_doc_gap.py
  python tools/measure_doc_gap.py --out-summary <path>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
APICONFIG = REPO / "src/test/java/com/arcon/autoconfigs/APIConfig.java"
PAM = ROOT / "pam" / "PAM"
CORPUS = ROOT / "artifacts" / "rag-corpus" / "corpus.jsonl"
SOURCE_MAP = HERE / "source-map.json"
RESULTS = ROOT / "artifacts" / "runs" / "2026-07-29_181439" / "results.json"
OUT_ROWS = ROOT / "artifacts" / "analysis-data" / "doc-gap-coverage.json"

# Verbatim from tools/generate_flows.py:37-40 so the role counts here are
# identical to the ones the 2026-07-29 run and SOURCE-MAP.md were built on (217 creates).
WRITE_NEW = re.compile(r"^(set|insert|create|add|save)", re.I)
READ = re.compile(r"^(get|fetch|list|view|check|validate|search|is|has)", re.I)
CHANGE = re.compile(r"^(update|modify|edit|enable|map|assign|approve|reject|resend)", re.I)
TEARDOWN = re.compile(r"^(delete|remov|drop|purge|revoke|unmap|disable|deactivate)", re.I)


def log(m=""):
    print(m, flush=True)


def role_of(action: str) -> str:
    if WRITE_NEW.match(action):
        return "create"
    if TEARDOWN.match(action):
        return "teardown"
    if CHANGE.match(action):
        return "update"
    if READ.match(action):
        return "read"
    return "other"


# --------------------------------------------------------------- 1. catalogue
def load_catalogue() -> dict[str, dict]:
    src = APICONFIG.read_text(encoding="utf-8", errors="replace")
    decl = re.compile(r'public\s+static\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;(?:\s*//\s*(\w+))?')
    eps: dict[str, dict] = {}
    for const, path, verb in decl.findall(src):
        m = re.match(r"^/api/([^/]+)/([^/?]+)", path)
        if not m:
            continue
        ctrl, action = m.group(1), m.group(2)
        key = f"{ctrl}/{action}"
        eps.setdefault(key, {
            "controller": ctrl, "action": action, "path": path,
            "verb": (verb or "").upper() or "POST", "role": role_of(action),
            "consts": [],
        })["consts"].append(const)
    return eps


# ------------------------------------------------------------ 2. pam/PAM scan
CLASS_RE = re.compile(r"\bclass\s+([A-Za-z_]\w*)")
METHOD_RE = re.compile(
    r"\bpublic\s+(?:async\s+)?(?:static\s+)?(?:virtual\s+)?(?:override\s+)?"
    r"[\w<>?\[\],\s\.]+?\s+([A-Za-z_]\w*)\s*\(")


def scan_pam(controllers: set[str], actions: set[str]) -> dict:
    """One pass over every .cs file under pam/PAM. Read-only."""
    ctrl_lc = {c.lower(): c for c in controllers}
    act_lc = {a.lower(): a for a in actions}

    # word-boundary alternations, longest first so ServiceDetailsV2 wins over ServiceDetails
    ctrl_alt = re.compile(r"\b(" + "|".join(
        re.escape(c) for c in sorted(controllers, key=len, reverse=True)) + r")\b")
    act_alt = re.compile(r"\b(" + "|".join(
        re.escape(a) for a in sorted(actions, key=len, reverse=True)) + r")\b")

    st = Counter()
    controller_files: dict[str, list[str]] = defaultdict(list)   # controller name -> file paths
    controller_classes: set[str] = set()                          # every *Controller class found
    methods_in_controller: dict[str, set[str]] = defaultdict(set)  # controller -> method names
    methods_anywhere: set[str] = set()
    ctrl_name_in_text: set[str] = set()
    act_name_in_text: set[str] = set()
    route_literals: set[str] = set()          # "Controller/Action" substrings seen verbatim
    http_projects: set[str] = set()

    for p in PAM.rglob("*.cs"):
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            st["unreadable"] += 1
            continue
        st["cs_files"] += 1
        st["chars"] += len(txt)
        rel = str(p.relative_to(PAM)).replace("\\", "/")

        # --- controller classes
        is_ctrl_file = p.name.lower().endswith("controller.cs")
        classes = CLASS_RE.findall(txt)
        ctrl_classes_here = [c for c in classes if c.lower().endswith("controller")]
        for c in ctrl_classes_here:
            controller_classes.add(c)
            base = c[: -len("Controller")]
            if base.lower() in ctrl_lc:
                controller_files[ctrl_lc[base.lower()]].append(rel)
        if is_ctrl_file:
            st["controller_files"] += 1
            http_projects.add(rel.split("/")[0])
            base = p.stem[: -len("Controller")] if p.stem.lower().endswith("controller") else p.stem
            meths = set(METHOD_RE.findall(txt))
            if base.lower() in ctrl_lc:
                methods_in_controller[ctrl_lc[base.lower()]] |= meths
            for c in ctrl_classes_here:
                b2 = c[: -len("Controller")]
                if b2.lower() in ctrl_lc:
                    methods_in_controller[ctrl_lc[b2.lower()]] |= meths

        # --- every public method name anywhere
        for m in METHOD_RE.findall(txt):
            if m.lower() in act_lc:
                methods_anywhere.add(act_lc[m.lower()])

        # --- generous "appears anywhere in text" measures
        for c in set(ctrl_alt.findall(txt)):
            ctrl_name_in_text.add(c)
        for a in set(act_alt.findall(txt)):
            act_name_in_text.add(a)

        # --- verbatim route literal
        for m in re.finditer(r"([A-Za-z][A-Za-z0-9_]{2,})/([A-Za-z][A-Za-z0-9_]{2,})", txt):
            c, a = m.group(1), m.group(2)
            if c.lower() in ctrl_lc and a.lower() in act_lc:
                route_literals.add(f"{ctrl_lc[c.lower()]}/{act_lc[a.lower()]}")

    st["csproj"] = sum(1 for _ in PAM.rglob("*.csproj"))
    return {
        "stats": st,
        "controller_files": dict(controller_files),
        "controller_classes": sorted(controller_classes),
        "methods_in_controller": {k: sorted(v) for k, v in methods_in_controller.items()},
        "methods_anywhere": sorted(methods_anywhere),
        "ctrl_name_in_text": sorted(ctrl_name_in_text),
        "act_name_in_text": sorted(act_name_in_text),
        "route_literals": sorted(route_literals),
        "http_projects": sorted(http_projects),
    }


# --------------------------------------------------------- 3. Confluence scan
ROUTE_RE = re.compile(r"/api/([A-Za-z0-9_]+)/([A-Za-z0-9_]+)")
JSON_RE = re.compile(r"\{[^{}]*\"[A-Za-z_][A-Za-z0-9_]*\"\s*:[^{}]*\}", re.S)
# Error codes are measured two ways, both deliberately conservative.
#   (a) the value of an ErrorCode/errorCode field in a documented JSON example
#   (b) an ARCON-shaped code standing alone in prose
# (?<![\d.]) is load-bearing: without it, ServiceDisplayName values such as
# "10.10.1.214@root:10.10.1.214-SSH LINUX" match as "214-SSH". That false positive is why
# docs/briefs/document-gap.md reports 4 documented codes - two of its four (190-SSH, 100-SSH)
# are IP-address fragments on pam-api:p1065 and p1066, not error codes.
ERRCODE_FIELD_RE = re.compile(r'"[Ee]rror[Cc]ode"\s*:\s*"([^"]+)"')
ERRCODE_NULL_RE = re.compile(r'"[Ee]rror[Cc]ode"\s*:\s*null')
ERRCODE_PROSE_RE = re.compile(r"(?<![\d.])\b(\d{3})-([A-Z][A-Z0-9_]{1,12})(?:-([A-Z][A-Z0-9_]{1,14}))?\b")
# placeholders and broken examples that are not real codes
ERRCODE_PLACEHOLDER = {"error1", "null", "string", "n/a", "na", "-", ""}
ENVELOPE_KEYS = {"success", "result", "message", "program", "version", "datetime",
                 "errorcode", "errormessage", "aadata", "output"}
RULE_RE = re.compile(
    r"\b(is mandatory|are mandatory|mandatory field|must be|must not|cannot be|can not be|"
    r"is required|not allowed|should not|maximum length|minimum length|max length|"
    r"valid range|prerequisite|pre-requisite|only if|not be empty|should be unique|"
    r"already exists|duplicate)\b", re.I)
# noise the error-code regex would otherwise pick up (versions, dates, sizes)


def scan_confluence(controllers: set[str], actions: set[str]) -> dict:
    st = Counter()
    pages_by_ctrl: dict[str, set[int]] = defaultdict(set)
    payloads_by_ctrl: Counter = Counter()
    errcodes_by_ctrl: dict[str, set[str]] = defaultdict(set)
    envelope_by_ctrl: dict[str, set[int]] = defaultdict(set)
    rules_by_ctrl: dict[str, set[int]] = defaultdict(set)
    routes_seen: set[str] = set()
    catalogue_routes_in_doc: set[str] = set()
    route_pages: dict[str, list[int]] = defaultdict(list)
    all_errcodes: dict[str, int] = Counter()
    errcode_pages: dict[str, list[int]] = defaultdict(list)
    status_mentions: Counter = Counter()

    ctrl_lc = {c.lower(): c for c in controllers}
    act_lc = {a.lower(): a for a in actions}
    ctx_ctrl: str | None = None
    ctx_age = 99

    for line in CORPUS.open(encoding="utf-8"):
        rec = json.loads(line)
        if rec.get("doc") != "pam-api":
            continue
        text = rec.get("text") or ""
        page = rec.get("page")
        st["pages"] += 1

        # every route on the page, for the distinct-route and exact-route-coverage measures
        for c_raw, a_raw in ROUTE_RE.findall(text):
            routes_seen.add(f"{c_raw}/{a_raw}")
            ck, ak = ctrl_lc.get(c_raw.lower()), act_lc.get(a_raw.lower())
            if ck and ak:
                key = f"{ck}/{ak}"
                catalogue_routes_in_doc.add(key)
                if len(route_pages[key]) < 6:
                    route_pages[key].append(page)

        # the FIRST route on the page sets the proximity context for payload binding
        route = ROUTE_RE.search(text)
        if route:
            c_raw, a_raw = route.group(1), route.group(2)
            ctx_ctrl = ctrl_lc.get(c_raw.lower())
            ctx_age = 0
            st["pages_with_route"] += 1
            if ctx_ctrl is None:
                st["pages_route_not_in_catalogue"] += 1
        else:
            hit = None
            for tok in re.findall(r"\b([A-Z][A-Za-z0-9_]{4,})\b", text[:600]):
                if tok.lower() in act_lc:
                    hit = act_lc[tok.lower()]
                    break
            if hit:
                ctx_age = 0
                st["pages_with_action_only"] += 1
            else:
                ctx_age += 1

        live = ctx_ctrl if (ctx_ctrl and ctx_age <= 2) else None
        if live:
            pages_by_ctrl[live].add(page)

        # HTTP status mentions
        for s in re.findall(r"\b(200|201|400|401|403|404|405|500|503)\b", text):
            status_mentions[s] += 1

        # error codes - field values and prose mentions, placeholders excluded
        st["errorcode_field_null"] += len(ERRCODE_NULL_RE.findall(text))
        found: set[str] = set()
        for raw in ERRCODE_FIELD_RE.findall(text):
            code = raw.strip()
            st["errorcode_field_valued"] += 1
            if code.lower() in ERRCODE_PLACEHOLDER:
                st["errorcode_placeholder"] += 1
                continue
            found.add(code)
        for m in ERRCODE_PROSE_RE.finditer(text):
            found.add("-".join(g for g in m.groups() if g))
        for code in found:
            all_errcodes[code] += 1
            if page not in errcode_pages[code]:
                errcode_pages[code].append(page)
            if live:
                errcodes_by_ctrl[live].add(code)

        # payload examples + envelope-shaped JSON
        for blk in JSON_RE.findall(text):
            try:
                obj = json.loads(blk)
            except Exception:
                st["json_unparseable"] += 1
                continue
            if not isinstance(obj, dict) or not obj:
                continue
            st["json_parsed"] += 1
            keys_lc = {k.lower() for k in obj}
            envelope_like = len(keys_lc & ENVELOPE_KEYS) >= 2
            if live:
                payloads_by_ctrl[live] += 1
                st["json_bound"] += 1
                if envelope_like:
                    envelope_by_ctrl[live].add(page)
            else:
                st["json_orphaned"] += 1
            if envelope_like:
                st["json_envelope_like"] += 1

        if live and RULE_RE.search(text):
            rules_by_ctrl[live].add(page)

    return {
        "stats": st,
        "pages_by_ctrl": {k: sorted(v) for k, v in pages_by_ctrl.items()},
        "payloads_by_ctrl": dict(payloads_by_ctrl),
        "errcodes_by_ctrl": {k: sorted(v) for k, v in errcodes_by_ctrl.items()},
        "envelope_by_ctrl": {k: sorted(v) for k, v in envelope_by_ctrl.items()},
        "rules_by_ctrl": {k: sorted(v) for k, v in rules_by_ctrl.items()},
        "routes_seen": sorted(routes_seen),
        "catalogue_routes_in_doc": sorted(catalogue_routes_in_doc),
        "route_pages": dict(route_pages),
        "all_errcodes": dict(all_errcodes),
        "errcode_pages": dict(errcode_pages),
        "status_mentions": dict(status_mentions),
    }


# ------------------------------------------------------- 4. run consequences
def scan_run() -> dict:
    """Controller is taken from each hop's own path, so the catalogue is not needed here."""
    if not RESULTS.exists():
        return {}
    data = json.loads(RESULTS.read_text(encoding="utf-8", errors="replace"))
    per_ctrl = defaultdict(Counter)
    tot = Counter()
    for flow in data.get("flows", []):
        for hop in flow.get("hops", []):
            path = hop.get("path") or ""
            m = re.match(r"^/api/([^/?]+)/([^/?]+)", path)
            ctrl = m.group(1) if m else "?"
            per_ctrl[ctrl]["hops"] += 1
            tot["hops"] += 1
            sc = hop.get("status")
            if sc == 404:
                per_ctrl[ctrl]["http_404"] += 1
                tot["http_404"] += 1
            for chk in hop.get("checks", []) or []:
                layer, verdict = chk.get("layer"), chk.get("verdict")
                key = f"{layer}_{'pass' if verdict == 'PASS' else 'fail'}"
                per_ctrl[ctrl][key] += 1
                tot[key] += 1
                if layer == "L5" and verdict == "FAIL":
                    per_ctrl[ctrl]["missing_new_id"] += 1
                    tot["missing_new_id"] += 1
                    if "MISSING ['NEW_ID']" in (chk.get("detail") or ""):
                        tot["missing_new_id_exact"] += 1
    return {"per_ctrl": {k: dict(v) for k, v in per_ctrl.items()}, "totals": dict(tot),
            "meta": data.get("meta", {}), "flow_count": len(data.get("flows", []))}


# ---------------------------------------------------------------- 5. assemble
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-summary", default=str(HERE / ".doc-gap-summary.json"))
    args = ap.parse_args()

    log("[1/5] catalogue from APIConfig.java")
    eps = load_catalogue()
    controllers = sorted({v["controller"] for v in eps.values()})
    actions = sorted({v["action"] for v in eps.values()})
    log(f"      {len(eps)} endpoints · {len(controllers)} controllers · {len(actions)} distinct actions")

    log("[2/5] pam/PAM static scan (read-only, ~7k files)")
    pam = scan_pam(set(controllers), set(actions))
    log(f"      {pam['stats']['cs_files']} .cs files · {pam['stats']['controller_files']} *Controller.cs "
        f"· {len(pam['controller_classes'])} controller classes")

    log("[3/5] Confluence corpus scan (2,470 pages)")
    confl = scan_confluence(set(controllers), set(actions))
    log(f"      {confl['stats']['json_bound']} payloads bound · "
        f"{len(confl['all_errcodes'])} error-code-shaped tokens")

    log("[4/5] source-map.json (prior 4-source merge)")
    smap = json.loads(SOURCE_MAP.read_text(encoding="utf-8", errors="replace")) if SOURCE_MAP.exists() else {}
    documented_smap = {k for k, v in smap.items() if "confluence" in (v.get("sources") or [])}
    log(f"      {len(documented_smap)} of {len(smap)} endpoints carry a confluence binding")

    log("[5/5] run consequences from results.json")
    run = scan_run()
    log(f"      {run.get('flow_count', 0)} flows · {run.get('totals', {}).get('hops', 0)} hops")

    # ---- the four candidate definitions of "controller absent from pam/PAM"
    have_ctrl_file = set(pam["controller_files"])                       # *Controller.cs matching the name
    name_in_text = set(pam["ctrl_name_in_text"])                        # name appears anywhere in any .cs
    have_impl_endpoint = set()                                          # strict: class + action method
    strict_endpoints = set()
    for key, ep in eps.items():
        c, a = ep["controller"], ep["action"]
        if c in pam["methods_in_controller"] and a in set(pam["methods_in_controller"][c]):
            strict_endpoints.add(key)
            have_impl_endpoint.add(c)
    method_anywhere_actions = set(pam["methods_anywhere"])
    endpoints_action_method_anywhere = {k for k, v in eps.items() if v["action"] in method_anywhere_actions}
    endpoints_route_literal = set(pam["route_literals"])
    endpoints_both_names_in_text = {
        k for k, v in eps.items()
        if v["controller"] in name_in_text and v["action"] in set(pam["act_name_in_text"])}

    defs = {
        "D1_no_matching_controller_cs_file": {
            "definition": "no <Controller>Controller.cs class exists anywhere under pam/PAM",
            "absent": sorted(set(controllers) - have_ctrl_file),
        },
        "D2_no_implemented_endpoint": {
            "definition": "controller class may exist, but not one catalogue action of it is a public "
                          "method of that class",
            "absent": sorted(set(controllers) - have_impl_endpoint),
        },
        "D3_name_absent_from_all_cs_text": {
            "definition": "the controller name does not appear as a whole word in any .cs file "
                          "(comments and call sites included)",
            "absent": sorted(set(controllers) - name_in_text),
        },
    }
    for d in defs.values():
        d["absent_count"] = len(d["absent"])
        d["present_count"] = len(controllers) - len(d["absent"])

    endpoint_measures = {
        "M1_strict_class_and_method": len(strict_endpoints),
        "M2_action_method_anywhere": len(endpoints_action_method_anywhere),
        "M3_route_literal_verbatim": len(endpoints_route_literal),
        "M4_both_names_in_any_text": len(endpoints_both_names_in_text),
        "total": len(eps),
    }

    # ---- per-controller rows
    rows = []
    ep_by_ctrl = defaultdict(list)
    for k, v in eps.items():
        ep_by_ctrl[v["controller"]].append(k)

    exact_doc = set(confl["catalogue_routes_in_doc"])
    for c in controllers:
        keys = ep_by_ctrl[c]
        total = len(keys)
        in_repo = sum(1 for k in keys if k in strict_endpoints)
        # "documented" = the exact /api/<Controller>/<Action> route appears verbatim in the
        # 2,470-page export. Deterministic and page-citable, unlike proximity binding.
        doc = sum(1 for k in keys if k in exact_doc)
        doc_payload_bound = sum(1 for k in keys if k in documented_smap)
        payloads = confl["payloads_by_ctrl"].get(c, 0)
        errc = confl["errcodes_by_ctrl"].get(c, [])
        env_pages = confl["envelope_by_ctrl"].get(c, [])
        rule_pages = confl["rules_by_ctrl"].get(c, [])
        doc_pages = confl["pages_by_ctrl"].get(c, [])
        rc = run.get("per_ctrl", {}).get(c, {})
        cov = round(100.0 * doc / total, 1) if total else 0.0

        creates = sum(1 for k in keys if eps[k]["role"] == "create")
        if cov == 0 and in_repo == 0:
            sev = "critical"
        elif cov < 25 or (creates and payloads == 0):
            sev = "high"
        elif cov < 60 or not env_pages:
            sev = "medium"
        else:
            sev = "low"

        notes = []
        notes.append(f"{creates} create endpoint(s)")
        notes.append(f"{doc_payload_bound} endpoint(s) with a proximity-bound payload")
        if in_repo == 0:
            src = ("no matching *Controller.cs" if c not in have_ctrl_file
                   else "controller class present but no catalogue action implemented")
            notes.append(src)
        else:
            notes.append(f"impl file(s): {', '.join(pam['controller_files'].get(c, [])[:2])}")
        if doc_pages:
            notes.append(f"doc pages e.g. pam-api:p{doc_pages[0]}")
        if rc.get("hops"):
            notes.append(f"{rc['hops']} hops in 2026-07-29 run")
            if rc.get("http_404"):
                notes.append(f"{rc['http_404']} x HTTP 404")
            if rc.get("missing_new_id"):
                notes.append(f"{rc['missing_new_id']} x L5 MISSING NEW_ID")
        else:
            notes.append("not exercised in the 2026-07-29 run")

        rows.append({
            "controller": c,
            "endpoints_total": total,
            "endpoints_in_pam_repo": in_repo,
            "endpoints_documented_confluence": doc,
            "payload_examples_available": payloads,
            "response_model_documented": bool(env_pages),
            "error_codes_documented": len(errc),
            "business_rules_documented": bool(rule_pages),
            "coverage_pct": cov,
            "gap_severity": sev,
            "notes": " · ".join(notes),
        })

    rows.sort(key=lambda r: (-r["endpoints_total"], r["controller"]))
    OUT_ROWS.parent.mkdir(parents=True, exist_ok=True)
    OUT_ROWS.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    log(f"\nwrote {OUT_ROWS}")

    summary = {
        "catalogue": {
            "endpoints": len(eps), "controllers": len(controllers),
            "distinct_actions": len(actions),
            "roles": dict(Counter(v["role"] for v in eps.values())),
            "verbs": dict(Counter(v["verb"] for v in eps.values())),
        },
        "pam_repo": {
            "cs_files": pam["stats"]["cs_files"], "chars": pam["stats"]["chars"],
            "csproj": pam["stats"]["csproj"],
            "controller_cs_files": pam["stats"]["controller_files"],
            "controller_classes_total": len(pam["controller_classes"]),
            "controller_classes": pam["controller_classes"],
            "http_projects_with_controllers": pam["http_projects"],
            "catalogue_controllers_with_file": sorted(have_ctrl_file),
        },
        "controller_absence_definitions": defs,
        "endpoint_presence_measures": endpoint_measures,
        "confluence": {
            "stats": dict(confl["stats"]),
            "distinct_routes_in_doc": len(confl["routes_seen"]),
            "catalogue_routes_documented_exact": len(confl["catalogue_routes_in_doc"]),
            "catalogue_routes_undocumented_exact": len(eps) - len(confl["catalogue_routes_in_doc"]),
            "errcodes_found": confl["all_errcodes"],
            "errcode_pages": confl["errcode_pages"],
            "status_mentions": confl["status_mentions"],
            "controllers_with_any_doc_page": len(confl["pages_by_ctrl"]),
            "controllers_with_envelope_example": len(confl["envelope_by_ctrl"]),
            "controllers_with_rule_language": len(confl["rules_by_ctrl"]),
            "controllers_with_errcode": len(confl["errcodes_by_ctrl"]),
        },
        "source_map": {
            "endpoints": len(smap),
            "documented_confluence": len(documented_smap),
            "undocumented": len(smap) - len(documented_smap),
        },
        "run": {"totals": run.get("totals", {}), "flows": run.get("flow_count", 0)},
        "row_rollup": {
            "controllers": len(rows),
            "endpoints_total": sum(r["endpoints_total"] for r in rows),
            # declared endpoints whose exact route is documented. Lower than
            # catalogue_routes_documented_exact because that set also contains name-valid
            # pairs the catalogue never declares.
            "endpoints_documented": sum(r["endpoints_documented_confluence"] for r in rows),
            "endpoints_undocumented": sum(
                r["endpoints_total"] - r["endpoints_documented_confluence"] for r in rows),
            "endpoints_in_pam_repo": sum(r["endpoints_in_pam_repo"] for r in rows),
            "sev": dict(Counter(r["gap_severity"] for r in rows)),
            "zero_doc_controllers": sum(1 for r in rows if r["endpoints_documented_confluence"] == 0),
            "zero_repo_controllers": sum(1 for r in rows if r["endpoints_in_pam_repo"] == 0),
            "with_response_model": sum(1 for r in rows if r["response_model_documented"]),
            "with_business_rules": sum(1 for r in rows if r["business_rules_documented"]),
            "with_error_codes": sum(1 for r in rows if r["error_codes_documented"]),
            "payload_examples_total": sum(r["payload_examples_available"] for r in rows),
        },
    }
    Path(args.out_summary).write_text(json.dumps(summary, indent=1), encoding="utf-8")
    log(f"wrote {args.out_summary}")

    log("\n=== controller absence, by definition ===")
    for name, d in defs.items():
        log(f"  {name:38s} absent {d['absent_count']:3d} / {len(controllers)}")
    log("\n=== endpoint presence in pam/PAM ===")
    for k, v in endpoint_measures.items():
        log(f"  {k:32s} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
