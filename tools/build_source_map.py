#!/usr/bin/env python3
"""B4 - holistic source analysis. Build one field/endpoint map from every source we have.

FOUR SOURCES, each contributing something different. None is sufficient alone.

  1. APIConfig.java              routes: controller, action, verb           (authoritative for WHAT exists)
  2. utils/apiPayload/*.java     literal request bodies as currently sent   (stale, but real field names)
  3. Confluence API reference    3,194 documented JSON payloads             (richest field source)
  4. pam/PAM model classes       property names + C# types                  (types, NOT mandatory-ness)

WHY THIS EXISTS
  Only 13 of 217 create endpoints can currently be driven, because the bodies in source 2 carry
  hardcoded foreign keys and omit required fields. No single source fixes that:
    - source 3 has the fields but does not mark which are mandatory
    - source 4 has the types but only 3 [Required] attributes exist across 6,866 files
    - source 1 has no field information at all
  So this script merges them and scores each field's confidence, which is what B3 then consumes.

OUTPUT
  tools/source-map.json    machine-readable, consumed by B3
  tools/SOURCE-MAP.md      human summary with coverage figures

  python tools/build_source_map.py
  python tools/build_source_map.py --endpoint SetUserDetails   # inspect one
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chain_runner import REPO, ROOT                                  # noqa: E402
from generate_flows import java_literal, WRITE_NEW, TEARDOWN, CHANGE, READ  # noqa: E402

APICONFIG = REPO / "src/test/java/com/arcon/autoconfigs/APIConfig.java"
PAYLOAD_DIR = REPO / "src/test/java/com/arcon/utils/apiPayload"
CORPUS = ROOT / "artifacts" / "rag-corpus" / "corpus.jsonl"
PAM = ROOT / "pam" / "PAM"
OUT_JSON = HERE / "source-map.json"
OUT_MD = HERE / "SOURCE-MAP.md"


def log(m=""):
    print(m, flush=True)


# ------------------------------------------------------------------ 1. endpoints
def load_endpoints() -> dict[str, dict]:
    src = APICONFIG.read_text(encoding="utf-8", errors="replace")
    decl = re.compile(
        r'public\s+static\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;(?:\s*//\s*(\w+))?')
    eps: dict[str, dict] = {}
    for const, path, verb in decl.findall(src):
        m = re.match(r"^/api/([^/]+)/([^/?]+)", path)
        if not m:
            continue
        ctrl, action = m.group(1), m.group(2)
        key = f"{ctrl}/{action}"
        role = ("create" if WRITE_NEW.match(action) else
                "teardown" if TEARDOWN.match(action) else
                "update" if CHANGE.match(action) else
                "read" if READ.match(action) else "other")
        eps.setdefault(key, {
            "controller": ctrl, "action": action, "path": path,
            "verb": (verb or "").upper() or "POST", "role": role,
            "consts": [], "fields": {}, "sources": [],
        })["consts"].append(const)
    return eps


# ------------------------------------------------ 2. payload helpers (as-sent)
def load_helper_bodies() -> dict[str, dict]:
    meth = re.compile(r"public\s+String\s+(\w+)\s*\(\s*\)\s*\{(.*?)\n\t?\}", re.S)
    prefix = re.compile(r"^(post|put|patch|delete|payload|body)", re.I)
    vsuf = re.compile(r"V(\d+)$", re.I)
    out: dict[str, dict] = {}
    for f in sorted(PAYLOAD_DIR.glob("*.java")):
        for name, blk in meth.findall(f.read_text(encoding="utf-8", errors="replace")):
            parsed = java_literal(blk)
            if not isinstance(parsed, dict):
                continue
            base = vsuf.sub("", name)
            for k in {name.lower(), prefix.sub("", name).lower(),
                      base.lower(), prefix.sub("", base).lower()}:
                out.setdefault(k, parsed)
    return out


# ----------------------------------------- 3. Confluence: payloads bound to routes
ROUTE_RE = re.compile(r"/api/([A-Za-z0-9_]+)/([A-Za-z0-9_]+)")
JSON_RE = re.compile(r"\{[^{}]*\"[A-Za-z_][A-Za-z0-9_]*\"\s*:[^{}]*\}", re.S)


def load_confluence(actions: set[str]) -> tuple[dict[str, list], Counter]:
    """Walk the corpus page by page, tracking the most recently mentioned endpoint, and
    attach every JSON object found to it. Documentation lists the route as a heading and
    the payload underneath, so proximity is the only available binding."""
    if not CORPUS.exists():
        return {}, Counter()

    bound: dict[str, list] = defaultdict(list)
    stats = Counter()
    ctx_key: str | None = None
    ctx_age = 99

    act_lower = {a.lower(): a for a in actions}

    for line in CORPUS.open(encoding="utf-8"):
        rec = json.loads(line)
        if rec.get("doc") != "pam-api":
            continue
        text = rec.get("text") or ""
        stats["pages"] += 1

        # strongest signal: an explicit route on this page
        route = ROUTE_RE.search(text)
        if route:
            ctx_key, ctx_age = f"{route.group(1)}/{route.group(2)}", 0
            stats["pages_with_route"] += 1
        else:
            # weaker: a bare action name we recognise
            hit = None
            for tok in re.findall(r"\b([A-Z][A-Za-z0-9_]{4,})\b", text[:600]):
                if tok.lower() in act_lower:
                    hit = act_lower[tok.lower()]
                    break
            if hit:
                ctx_key, ctx_age = f"?/{hit}", 0
                stats["pages_with_action_only"] += 1
            else:
                ctx_age += 1

        for blk in JSON_RE.findall(text):
            try:
                obj = json.loads(blk)
            except Exception:
                stats["json_unparseable"] += 1
                continue
            if not isinstance(obj, dict) or not obj:
                continue
            stats["json_parsed"] += 1
            if ctx_key and ctx_age <= 2:
                bound[ctx_key].append({"page": rec["page"], "body": obj})
                stats["json_bound"] += 1
            else:
                stats["json_orphaned"] += 1
    return dict(bound), stats


# --------------------------------------------- 4. pam/PAM model property types
PROP_RE = re.compile(
    r"\[\s*(Required|StringLength|MaxLength|MinLength|Range)[^\]]*\]\s*(?:\r?\n\s*)*"
    r"public\s+([\w<>?\[\],\s]+?)\s+(\w+)\s*\{\s*get;\s*set;\s*\}")
PLAIN_PROP_RE = re.compile(
    r"public\s+([\w<>?\[\],\s]+?)\s+(\w+)\s*\{\s*get;\s*set;\s*\}")


def load_pam_models() -> tuple[dict[str, str], set[str], Counter]:
    """field name (lowercased) -> C# type, plus the set marked [Required]."""
    types: dict[str, str] = {}
    required: set[str] = set()
    stats = Counter()
    if not PAM.is_dir():
        return types, required, stats
    for p in PAM.rglob("*.cs"):
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        stats["files"] += 1
        for attr, ctype, name in PROP_RE.findall(txt):
            if attr == "Required":
                required.add(name.lower())
            types.setdefault(name.lower(), ctype.strip())
            stats["annotated_props"] += 1
        for ctype, name in PLAIN_PROP_RE.findall(txt):
            types.setdefault(name.lower(), ctype.strip())
            stats["props"] += 1
    return types, required, stats


# --------------------------------------------------------------------- merge
GENERIC = {"status", "type", "data", "message", "result", "success", "program",
           "version", "datetime"}


def merge(eps, helpers, confl, ptypes, prequired):
    for key, ep in eps.items():
        action_l = ep["action"].lower()
        fields: dict[str, dict] = {}

        def add(name, source, value=None):
            f = fields.setdefault(name, {
                "sources": [], "example": None, "csharp_type": None,
                "required_hint": False,
            })
            if source not in f["sources"]:
                f["sources"].append(source)
            if value is not None and f["example"] is None:
                f["example"] = value

        hb = helpers.get(action_l)
        if isinstance(hb, dict):
            ep["sources"].append("payload-helper")
            for k, v in hb.items():
                add(k, "payload-helper", v)

        docs = confl.get(key) or confl.get(f"?/{ep['action']}") or []
        if docs:
            ep["sources"].append("confluence")
            ep["confluence_pages"] = sorted({d["page"] for d in docs})[:6]
            seen = Counter()
            for d in docs:
                for k, v in d["body"].items():
                    add(k, "confluence", v)
                    seen[k] += 1
            # a field present in every documented example is probably mandatory
            for k, n in seen.items():
                if len(docs) >= 2 and n == len(docs):
                    fields[k]["required_hint"] = True

        for name, f in fields.items():
            t = ptypes.get(name.lower())
            if t:
                f["csharp_type"] = t
                if "pam-model" not in f["sources"]:
                    f["sources"].append("pam-model")
            if name.lower() in prequired:
                f["required_hint"] = True
                f["sources"].append("pam-required")

        # confidence: how many independent sources agree this field belongs here
        for name, f in fields.items():
            n = len({s for s in f["sources"] if s != "pam-required"})
            f["confidence"] = "high" if n >= 2 else "medium" if n == 1 else "low"
            f["chainable"] = bool(re.search(r"id$", name, re.I)) \
                and name.lower() not in GENERIC

        ep["fields"] = fields
    return eps


# -------------------------------------------------------------------- report
def write_report(eps, confl_stats, pam_stats, ptypes, prequired):
    creates = {k: v for k, v in eps.items() if v["role"] == "create"}
    with_helper = [k for k, v in creates.items() if "payload-helper" in v["sources"]]
    with_doc = [k for k, v in creates.items() if "confluence" in v["sources"]]
    with_any = [k for k, v in creates.items() if v["fields"]]
    newly = sorted(set(with_doc) - set(with_helper))

    L, A = [], None
    A = L.append
    A("# Source Map — Holistic Analysis of All Four Sources (B4)")
    A("")
    A("**Generated by:** `tools/build_source_map.py` · "
      "**Consumed by:** B3 (payload repair)")
    A("**Sources merged:** `APIConfig.java` · payload helpers · Confluence API reference · "
      "`pam/PAM` models")
    A("")
    A("---")
    A("")
    A("## 1. What each source contributed")
    A("")
    A("| Source | Unit | Count |")
    A("|---|---|---:|")
    A(f"| `APIConfig.java` | endpoints | {len(eps)} |")
    A(f"| Confluence reference | pages scanned | {confl_stats.get('pages', 0)} |")
    A(f"| | pages naming a route | {confl_stats.get('pages_with_route', 0)} |")
    A(f"| | JSON objects parsed | {confl_stats.get('json_parsed', 0)} |")
    A(f"| | **JSON objects bound to an endpoint** | **{confl_stats.get('json_bound', 0)}** |")
    A(f"| | orphaned (no nearby endpoint) | {confl_stats.get('json_orphaned', 0)} |")
    A(f"| `pam/PAM` | `.cs` files scanned | {pam_stats.get('files', 0)} |")
    A(f"| | distinct property names → C# type | {len(ptypes)} |")
    A(f"| | properties marked `[Required]` | **{len(prequired)}** |")
    A("")
    A("## 2. Create-endpoint coverage — the B3 target")
    A("")
    A("| Measure | Count | Share |")
    A("|---|---:|---:|")
    n = max(1, len(creates))
    A(f"| Create endpoints | {len(creates)} | 100% |")
    A(f"| …with a payload-helper body (what we use today) | {len(with_helper)} | "
      f"{100*len(with_helper)//n}% |")
    A(f"| …with documented payloads | {len(with_doc)} | {100*len(with_doc)//n}% |")
    A(f"| **…with fields from ANY source** | **{len(with_any)}** | "
      f"**{100*len(with_any)//n}%** |")
    A(f"| **…newly covered by documentation alone** | **{len(newly)}** | "
      f"{100*len(newly)//n}% |")
    A("")
    A("The last row is the B3 opportunity: creates that have **no usable body in code** but "
      "**do** have documented payloads.")
    A("")
    if newly:
        A("## 3. Creates unlocked by documentation")
        A("")
        A("| Endpoint | Fields found | Likely mandatory | Doc pages |")
        A("|---|---:|---:|---|")
        for k in newly[:60]:
            v = eps[k]
            req = sum(1 for f in v["fields"].values() if f["required_hint"])
            pages = ", ".join(str(p) for p in (v.get("confluence_pages") or [])[:3])
            A(f"| `{k}` | {len(v['fields'])} | {req} | {pages} |")
        if len(newly) > 60:
            A(f"| … | | | +{len(newly)-60} more |")
        A("")
    A("## 4. Field confidence across all endpoints")
    A("")
    conf = Counter()
    chain = 0
    for v in eps.values():
        for f in v["fields"].values():
            conf[f["confidence"]] += 1
            chain += 1 if f["chainable"] else 0
    A("| Confidence | Meaning | Fields |")
    A("|---|---|---:|")
    A(f"| high | 2+ independent sources agree | {conf['high']} |")
    A(f"| medium | one source only | {conf['medium']} |")
    A(f"| **chainable** | id-shaped, candidate for carrying between hops | **{chain}** |")
    A("")
    A("## 5. Honest limits")
    A("")
    A("| Limit | Consequence |")
    A("|---|---|")
    A("| Documentation binds payloads to endpoints only by **page proximity** | Some bindings "
      "will be wrong. Treat `confidence: medium` as a hypothesis, not a contract |")
    A(f"| Only **{len(prequired)}** properties carry `[Required]` in the whole product | "
      "Mandatory-ness is *inferred* (present in every documented example), never asserted |")
    # 58, not 54. The old "54 of 70" was this very literal - never computed by any
    # code, yet it survived every regeneration and was inherited as fact by
    # docs/gaps/01-Data-Gap-Analysis.md. Derivation: docs/analysis/A6-developer-repo-analysis.md section 6.
    A("| `pam/PAM` supplies types, not routes | 58 of 70 catalogue controllers are absent "
      "from that snapshot |")
    A("| Swagger specs are **not** merged here | They describe a different surface "
      "(~6% name overlap) and need network access to fetch |")
    A("")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", help="print the merged map for one action and exit")
    args = ap.parse_args()

    log("[1/4] endpoints from APIConfig.java")
    eps = load_endpoints()
    log(f"      {len(eps)} distinct endpoints")

    log("[2/4] payload helper bodies")
    helpers = load_helper_bodies()
    log(f"      {len(helpers)} lookup keys")

    log("[3/4] Confluence payloads (this walks 2,470 pages, ~1 min)")
    confl, cstats = load_confluence({v["action"] for v in eps.values()})
    log(f"      {cstats.get('json_bound', 0)} payloads bound to "
        f"{len(confl)} endpoint keys; {cstats.get('json_orphaned', 0)} orphaned")

    log("[4/4] pam/PAM model property types")
    ptypes, prequired, pstats = load_pam_models()
    log(f"      {len(ptypes)} property types, {len(prequired)} marked [Required]")

    eps = merge(eps, helpers, confl, ptypes, prequired)

    if args.endpoint:
        want = args.endpoint.lower()
        for k, v in eps.items():
            if v["action"].lower() == want:
                print(json.dumps(v, indent=1, default=str))
        return 0

    OUT_JSON.write_text(json.dumps(eps, indent=1, default=str), encoding="utf-8")
    write_report(eps, cstats, pstats, ptypes, prequired)
    log("")
    log(f"wrote {OUT_JSON.name} and {OUT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
