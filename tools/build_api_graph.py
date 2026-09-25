#!/usr/bin/env python3
"""
API Graph builder — the API-side layer of Graphify.

Builds a graph of the PAM API surface and, critically, the **chaining relationships**
between endpoints: which endpoint's response supplies a field that another endpoint's
request needs. Everything is derived, nothing is hand-listed.

THREE INPUTS, all already in the repo or already captured:
  1. APIConfig.java                  -> 1,322 endpoints: module, controller, action, verb, model
  2. utils/apiPayload/*.java          -> the literal JSON each endpoint SENDS  (input fields)
  3. docs/findings/issues/Evidence/**.json  -> real captured responses               (output fields)

CHAINING EDGE RULE
  producer --field--> consumer   when   field in producer.outputs
                                  and   field in consumer.inputs
                                  and   producer != consumer

  Confidence is graded, because a name match is evidence, not proof:
     high    field is an identifier (ends in Id/Guid/Code/Key/Token/Name) AND the
             producer's output was OBSERVED in a real response
     medium  identifier match, but the producer's output is declared-only (not observed)
     low     non-identifier field name (e.g. "Status", "Type") - likely coincidence

OUTPUT (all into ./out/)
  api-graph.json        nodes + edges, machine readable
  api-graph.html        self-contained interactive visualisation, no external assets
  chaining-report.md    the chain candidates as a reviewable table

USAGE
  python artifacts/graph/api-graph/build_api_graph.py
  python artifacts/graph/api-graph/build_api_graph.py --min-confidence high
"""
from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
def _workspace_root():
    """Locate the workspace root by marker, not by counting parents (`OBJ-025`).

    Mirrors tools/paths.py. Was `HERE.parent.parent`, correct only while this
    script sat at artifacts/graph/api-graph/; it now lives in tools/."""
    for candidate in (HERE, *HERE.parents):
        if (candidate / "CLAUDE.md").is_file() and (candidate / ".claude").is_dir():
            return candidate
    raise SystemExit(f"cannot locate the workspace root above {HERE}")


ROOT = _workspace_root()
# OBJ-025: output stays with the graph it describes, not beside this script.
OUT = ROOT / "artifacts" / "graph" / "api-graph" / "out"

REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
APICONFIG = REPO / "src/test/java/com/arcon/autoconfigs/APIConfig.java"
PAYLOAD_DIR = REPO / "src/test/java/com/arcon/utils/apiPayload"
# OBJ-025 REPAIR. These two paths have pointed at nothing since 2026-07-29,
# when the Evidence folders were moved into _archive-pre-2026-07-29/. Nothing
# raised: load_outputs() iterates an absent directory and silently contributes
# no evidence, so the graph has been built from a smaller corpus than it claims
# for four weeks. This is the exact precedent the OBJ-025 plan was designed
# against - a reorganisation that broke a generator quietly - and it is the
# reason every root resolver now keys on a marker instead of a folder name.
EVIDENCE_DIRS = [
    ROOT / "artifacts" / "runs-archive" / "Evidence" / "legacy-qa_mssql",
    ROOT / "artifacts" / "runs-archive" / "Evidence" / "swagger-devint",
]
for _d in EVIDENCE_DIRS:
    if not _d.is_dir():
        raise SystemExit(f"evidence directory missing: {_d}")

IDENTIFIER = re.compile(
    r"(Id|Ids|Guid|Uuid|Code|Key|Token|Name|Username|Email|Path|Url|Ip|Mac|"
    r"GroupId|LobId|ServiceId|UserId|SessionId|RequestId)$", re.I)

# Field names too generic to imply a real dependency.
NOISE = {"status", "type", "message", "success", "result", "data", "value", "count",
         "total", "page", "size", "index", "flag", "active", "enabled", "date",
         "datetime", "time", "program", "version", "ticks", "errorcode", "error"}


def log(m=""):
    print(m, flush=True)


# ------------------------------------------------------------------ 1. endpoints
SECTION = re.compile(r"^\s*//\s*([A-Za-z][\w &./-]*?)\s*$", re.M)
DECL = re.compile(r'public\s+static\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;(?:\s*//\s*(\w+))?')
VERSION = re.compile(r"^(.*?)(V\d+(?:\.\d+)?)$")


def split_model(controller: str) -> tuple[str, str]:
    m = VERSION.match(controller)
    return (m.group(1), m.group(2)) if m and m.group(1) else (controller, "V1")


def load_endpoints() -> list[dict]:
    text = APICONFIG.read_text(encoding="utf-8", errors="replace")
    marks = [(m.start(), m.group(1).strip()) for m in SECTION.finditer(text)]

    def module_at(pos):
        cur = "(unsectioned)"
        for p, n in marks:
            if p < pos:
                cur = n
            else:
                break
        return cur

    eps = []
    for m in DECL.finditer(text):
        field, path, verb = m.group(1), m.group(2), (m.group(3) or "").lower()
        if not path.startswith("/"):
            continue
        seg = re.match(r"^/api/(?:(v[\d.]+)/)?([^/?]+)(?:/([^/?]+))?", path, re.I)
        controller = seg.group(2) if seg else "(unparsed)"
        action = (seg.group(3) or "") if seg else ""
        family, model = split_model(controller)
        eps.append({
            "id": field, "path": path, "verb": (verb or "?").upper(),
            "module": module_at(m.start()), "controller": controller, "action": action,
            "family": family, "model": model,
            "inputs": [], "outputs": [], "observed": False,
            "payload_template": None,   # the literal JSON the helper sends, verbatim
            "payload_helper": None,     # which <Module>PayLoadHelper supplied it
            "has_template_path": "{" in path,
            "status": None, "latency_ms": None,
        })
    return eps


# --------------------------------------------------- 2. inputs from payload helpers
def java_string_literals(body: str) -> str:
    """Reassemble a Java concatenated string literal into its runtime value."""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', body)
    s = "".join(parts)
    return (s.replace("\\r", "").replace("\\n", "").replace("\\t", "")
             .replace('\\"', '"').replace("\\\\", "\\"))


def json_keys(text: str) -> set[str]:
    """Keys from a JSON-ish blob. Falls back to a regex when it will not parse."""
    keys: set[str] = set()
    try:
        obj = json.loads(text)

        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    keys.add(k)
                    walk(v)
            elif isinstance(o, list):
                for v in o[:3]:
                    walk(v)
        walk(obj)
    except Exception:                                                # noqa: BLE001
        keys |= set(re.findall(r'"([A-Za-z_][A-Za-z0-9_]{1,42})"\s*:', text))
    return keys


def load_inputs(eps: list[dict]) -> int:
    by_id = {e["id"]: e for e in eps}
    method = re.compile(
        r"public\s+(?:static\s+)?String\s+(\w+)\s*\([^)]*\)\s*\{(.*?)\n\t?\}",
        re.S)
    found = 0
    for f in sorted(PAYLOAD_DIR.glob("*.java")):
        src = f.read_text(encoding="utf-8", errors="replace")
        for m in method.finditer(src):
            name, body = m.group(1), m.group(2)
            lit = java_string_literals(body)
            if not lit.strip():
                continue
            if name in by_id:
                # keep the template verbatim - the chain executor needs it to build a
                # request body, not just to know which field names exist
                by_id[name]["payload_template"] = lit
                by_id[name]["payload_helper"] = f.stem
                ks = {k for k in json_keys(lit) if k.lower() not in NOISE}
                if ks:
                    by_id[name]["inputs"] = sorted(ks)
                found += 1
    return found


# ------------------------------------------- 3. outputs from captured real responses
def load_outputs(eps: list[dict]) -> int:
    by_path = defaultdict(list)
    for e in eps:
        by_path[e["path"].split("?")[0].lower()].append(e)

    seen = 0
    for d in EVIDENCE_DIRS:
        if not d.exists():
            continue
        for f in d.glob("*.json"):
            try:
                ev = json.loads(f.read_text(encoding="utf-8", errors="replace"))
            except Exception:                                        # noqa: BLE001
                continue
            req = ev.get("request") or {}
            url = req.get("url") or ""
            mpath = re.search(r"(/api/[^?]*)", url, re.I)
            if not mpath:
                continue
            targets = by_path.get(mpath.group(1).lower())
            if not targets:
                continue
            resp = ev.get("response") or {}
            if resp.get("status") != 200:
                for t in targets:
                    t["status"] = resp.get("status")
                    t["latency_ms"] = resp.get("latency_ms")
                continue
            ks = {k for k in json_keys(resp.get("body_preview") or "")
                  if k.lower() not in NOISE}
            for t in targets:
                t["outputs"] = sorted(set(t["outputs"]) | ks)
                t["observed"] = True
                t["status"] = resp.get("status")
                t["latency_ms"] = resp.get("latency_ms")
            seen += 1
    return seen


# ------------------------------------------------------------------- 4. chaining
def confidence(field: str, producer: dict) -> str:
    ident = bool(IDENTIFIER.search(field))
    if ident and producer["observed"]:
        return "high"
    if ident:
        return "medium"
    return "low"


SUFFIX = re.compile(r"(Ids?|Guid|Uuid|Code|Key|Token|Name|No|Number)$", re.I)
LISTY = re.compile(r"^(GetAll|GetList|Get|List|Fetch|Search|Insert|Add|Create|Save|Register)", re.I)


def entity_of(field: str) -> str:
    """ServiceId -> Service ; LobIds -> Lob ; UserName -> User."""
    return SUFFIX.sub("", field) or field


def infer_producers(eps: list[dict]) -> dict[str, list[dict]]:
    """Producers inferred from naming, for fields whose source has not been observed.

    An endpoint is a candidate producer of `<Entity>Id` when its controller or action
    names that entity and the action reads or creates it. Heuristic and clearly labelled
    as such - it exists so the graph is useful before every endpoint has been executed.
    """
    out: dict[str, list[dict]] = defaultdict(list)
    fields = {f for e in eps for f in e["inputs"]}
    for f in fields:
        ent = entity_of(f)
        if len(ent) < 3:
            continue
        el = ent.lower()
        for e in eps:
            if not e["action"] or not LISTY.match(e["action"]):
                continue
            ctrl, act = e["controller"].lower(), e["action"].lower()
            # entity must be named by the controller or the action
            if el not in ctrl and el not in act:
                continue
            # a GET that lists the entity, or a write that creates it
            if e["verb"] == "GET" or re.match(r"^(insert|add|create|save|register)", act):
                out[f.lower()].append(e)
    return out


def build_chains(eps: list[dict]) -> list[dict]:
    observed = defaultdict(list)
    for e in eps:
        for f in e["outputs"]:
            observed[f.lower()].append(e)
    inferred = infer_producers(eps)

    edges, seen = [], set()
    for consumer in eps:
        for f in consumer["inputs"]:
            key = f.lower()
            # observed producers win; fall back to name-inferred ones
            src = [(p, "observed") for p in observed.get(key, [])]
            if not src:
                src = [(p, "inferred") for p in inferred.get(key, [])[:6]]
            for producer, basis in src:
                if producer["id"] == consumer["id"]:
                    continue
                sig = (f.lower(), producer["id"], consumer["id"])
                if sig in seen:
                    continue
                seen.add(sig)
                conf = (confidence(f, producer) if basis == "observed"
                        else ("medium" if IDENTIFIER.search(f) else "low"))
                edges.append({
                    "field": f, "basis": basis,
                    "from": producer["id"], "from_path": producer["path"],
                    "from_module": producer["module"], "from_verb": producer["verb"],
                    "to": consumer["id"], "to_path": consumer["path"],
                    "to_module": consumer["module"], "to_verb": consumer["verb"],
                    "confidence": conf,
                    "cross_module": producer["module"] != consumer["module"],
                })
    return edges


# ----------------------------------------------------------------------- 5. render
RANK = {"high": 3, "medium": 2, "low": 1}


def write_html(eps, edges, stats):
    mods = sorted({e["module"] for e in eps})
    # keep the page tractable: only endpoints that participate in a chain
    involved = {e["from"] for e in edges} | {e["to"] for e in edges}
    nodes = [e for e in eps if e["id"] in involved]
    nidx = {n["id"]: i for i, n in enumerate(nodes)}
    payload = {
        "nodes": [{"id": n["id"], "p": n["path"], "m": n["module"], "v": n["verb"],
                   "mo": n["model"], "ob": n["observed"],
                   "ni": len(n["inputs"]), "no": len(n["outputs"])} for n in nodes],
        "edges": [{"s": nidx[e["from"]], "t": nidx[e["to"]], "f": e["field"],
                   "c": e["confidence"], "x": e["cross_module"]}
                  for e in edges if e["from"] in nidx and e["to"] in nidx],
        "modules": mods,
    }

    rows = []
    for e in sorted(edges, key=lambda x: (-RANK[x["confidence"]], x["from_module"], x["field"])):
        rows.append(
            f"<tr class='c-{e['confidence']}'><td>{html.escape(e['confidence'])}</td>"
            f"<td><code>{html.escape(e['field'])}</code></td>"
            f"<td>{html.escape(e['from_verb'])} <code>{html.escape(e['from_path'])}</code></td>"
            f"<td>{html.escape(e['to_verb'])} <code>{html.escape(e['to_path'])}</code></td>"
            f"<td>{'cross' if e['cross_module'] else 'same'}</td></tr>")

    stat_rows = "".join(
        f"<div class='stat'><b>{v}</b><span>{html.escape(k)}</span></div>"
        for k, v in stats.items())

    doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>PAM API Graph &mdash; chaining</title>
<style>
:root{{--bg:#0f1115;--fg:#e6e6e6;--mut:#9aa0a6;--line:#2a2f3a;--hi:#4ade80;--md:#fbbf24;--lo:#6b7280}}
*{{box-sizing:border-box}}
body{{margin:0;font:13px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg)}}
header{{padding:14px 18px;border-bottom:1px solid var(--line)}}
h1{{margin:0 0 4px;font-size:16px}} .sub{{color:var(--mut);font-size:12px}}
.stats{{display:flex;gap:18px;flex-wrap:wrap;padding:12px 18px;border-bottom:1px solid var(--line)}}
.stat{{display:flex;flex-direction:column}} .stat b{{font-size:18px}} .stat span{{color:var(--mut);font-size:11px}}
.bar{{display:flex;gap:10px;align-items:center;padding:10px 18px;flex-wrap:wrap;border-bottom:1px solid var(--line)}}
select,input,button{{background:#171a21;color:var(--fg);border:1px solid var(--line);border-radius:5px;padding:5px 8px;font:inherit}}
#wrap{{position:relative;height:60vh;border-bottom:1px solid var(--line)}}
canvas{{display:block;width:100%;height:100%}}
#tip{{position:absolute;pointer-events:none;background:#11141a;border:1px solid var(--line);
     border-radius:6px;padding:7px 9px;font-size:12px;display:none;max-width:380px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
th,td{{text-align:left;padding:5px 9px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{position:sticky;top:0;background:#141821}}
code{{font:11px/1.4 ui-monospace,Consolas,monospace;color:#a5b4fc;word-break:break-all}}
.c-high td:first-child{{color:var(--hi)}} .c-medium td:first-child{{color:var(--md)}}
.c-low td:first-child{{color:var(--lo)}}
.tblwrap{{max-height:34vh;overflow:auto}}
.legend{{display:flex;gap:14px;color:var(--mut);font-size:11px}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}}
</style></head><body>
<header><h1>PAM API Graph &mdash; endpoint chaining</h1>
<div class="sub">Auto-derived from <code>APIConfig.java</code>, the payload helpers and captured responses.
Nothing hand-listed. An edge means the source endpoint returns a field the target endpoint needs.</div></header>
<div class="stats">{stat_rows}</div>
<div class="bar">
  <label>module <select id="mod"><option value="">all</option>
    {''.join(f'<option>{html.escape(m)}</option>' for m in mods)}</select></label>
  <label>min confidence <select id="conf">
    <option value="1">low+</option><option value="2" selected>medium+</option><option value="3">high only</option>
  </select></label>
  <label><input type="checkbox" id="xonly"> cross-module only</label>
  <input id="q" placeholder="filter field or path&hellip;" size="26">
  <button id="re">re-layout</button>
  <span class="legend">
    <span><i class="dot" style="background:var(--hi)"></i>high</span>
    <span><i class="dot" style="background:var(--md)"></i>medium</span>
    <span><i class="dot" style="background:var(--lo)"></i>low</span>
  </span>
</div>
<div id="wrap"><canvas id="cv"></canvas><div id="tip"></div></div>
<div class="tblwrap"><table><thead><tr>
<th>conf</th><th>field</th><th>producer (response)</th><th>consumer (request)</th><th>scope</th>
</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<script>
const DATA = {json.dumps(payload)};
const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),tip=document.getElementById('tip');
const COL={{high:'#4ade80',medium:'#fbbf24',low:'#6b7280'}},RK={{high:3,medium:2,low:1}};
let N=[],E=[],hover=null,dpr=window.devicePixelRatio||1;
function size(){{const r=cv.parentElement.getBoundingClientRect();
  cv.width=r.width*dpr;cv.height=r.height*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);}}
function filt(){{
  const m=document.getElementById('mod').value,mc=+document.getElementById('conf').value,
        xo=document.getElementById('xonly').checked,q=document.getElementById('q').value.toLowerCase();
  E=DATA.edges.filter(e=>{{
    if(RK[e.c]<mc)return false; if(xo&&!e.x)return false;
    const s=DATA.nodes[e.s],t=DATA.nodes[e.t];
    if(m&&s.m!==m&&t.m!==m)return false;
    if(q&&!(e.f.toLowerCase().includes(q)||s.p.toLowerCase().includes(q)||t.p.toLowerCase().includes(q)))return false;
    return true;}});
  const keep=new Set(); E.forEach(e=>{{keep.add(e.s);keep.add(e.t);}});
  N=[...keep].map(i=>({{i,...DATA.nodes[i],x:0,y:0,vx:0,vy:0}}));
  const pos=new Map(N.map((n,k)=>[n.i,k]));
  E=E.map(e=>({{...e,a:pos.get(e.s),b:pos.get(e.t)}}));
  const w=cv.width/dpr,h=cv.height/dpr;
  N.forEach((n,k)=>{{const a=k/N.length*Math.PI*2;
    n.x=w/2+Math.cos(a)*Math.min(w,h)*0.34;n.y=h/2+Math.sin(a)*Math.min(w,h)*0.34;}});
}}
function step(){{
  const w=cv.width/dpr,h=cv.height/dpr;
  for(let i=0;i<N.length;i++){{const p=N[i];
    for(let j=i+1;j<N.length;j++){{const q2=N[j];
      let dx=p.x-q2.x,dy=p.y-q2.y,d2=dx*dx+dy*dy||1;
      if(d2<40000){{const f=420/d2;p.vx+=dx*f;p.vy+=dy*f;q2.vx-=dx*f;q2.vy-=dy*f;}}}}}}
  E.forEach(e=>{{const a=N[e.a],b=N[e.b];if(!a||!b)return;
    const dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,f=(d-110)*0.006;
    a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;}});
  N.forEach(n=>{{n.vx+=(w/2-n.x)*0.0012;n.vy+=(h/2-n.y)*0.0012;
    n.vx*=0.86;n.vy*=0.86;n.x+=n.vx;n.y+=n.vy;
    n.x=Math.max(22,Math.min(w-22,n.x));n.y=Math.max(22,Math.min(h-22,n.y));}});
}}
function draw(){{
  const w=cv.width/dpr,h=cv.height/dpr;ctx.clearRect(0,0,w,h);
  E.forEach(e=>{{const a=N[e.a],b=N[e.b];if(!a||!b)return;
    ctx.strokeStyle=COL[e.c];ctx.globalAlpha=e.x?0.5:0.22;ctx.lineWidth=e.x?1.3:0.8;
    ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}});
  ctx.globalAlpha=1;
  N.forEach(n=>{{const r=n.no>0?6:4;
    ctx.fillStyle=n.ob?'#60a5fa':'#475569';
    ctx.beginPath();ctx.arc(n.x,n.y,r,0,7);ctx.fill();
    if(n===hover){{ctx.strokeStyle='#fff';ctx.lineWidth=1.5;ctx.stroke();}}}});
}}
function loop(){{step();draw();requestAnimationFrame(loop);}}
cv.addEventListener('mousemove',ev=>{{
  const r=cv.getBoundingClientRect(),mx=ev.clientX-r.left,my=ev.clientY-r.top;
  hover=N.find(n=>Math.hypot(n.x-mx,n.y-my)<9)||null;
  if(hover){{tip.style.display='block';tip.style.left=(mx+12)+'px';tip.style.top=(my+12)+'px';
    tip.innerHTML='<b>'+hover.v+' '+hover.p+'</b><br>module: '+hover.m+' &middot; model: '+hover.mo+
      '<br>inputs: '+hover.ni+' &middot; outputs: '+hover.no+
      '<br>'+(hover.ob?'response observed':'not observed - declared only');}}
  else tip.style.display='none';}});
['mod','conf','xonly','q'].forEach(id=>document.getElementById(id)
  .addEventListener('input',()=>{{filt();}}));
document.getElementById('re').addEventListener('click',()=>filt());
window.addEventListener('resize',()=>{{size();filt();}});
size();filt();loop();
</script></body></html>"""
    (OUT / "api-graph.html").write_text(doc, encoding="utf-8")


def write_md(eps, edges, stats):
    L = ["# API Chaining — auto-derived candidates", "",
         "**Generated by:** `artifacts/graph/api-graph/build_api_graph.py` · **Regenerate:** re-run it",
         "**Method:** producer/consumer field-name identity. No chain is hand-written.", ""]
    L += ["| Metric | Value |", "|---|---:|"]
    L += [f"| {k} | {v} |" for k, v in stats.items()]
    L += ["", "## How an edge is inferred", "",
          "```",
          "producer --field--> consumer",
          "  when field appears in the producer's RESPONSE",
          "   and field appears in the consumer's REQUEST payload",
          "```", "",
          "| Confidence | Meaning |", "|---|---|",
          "| **high** | identifier-shaped field (`*Id`, `*Guid`, `*Code`, `*Token`, `*Name`) **and** the "
          "producer's response was actually observed in a captured run |",
          "| **medium** | identifier-shaped, but the producer's output is inferred rather than observed |",
          "| **low** | non-identifier field name — treat as coincidence until reviewed |", "",
          "Generic field names (`status`, `type`, `data`, `message`, `result`, …) are excluded outright; "
          "they match everywhere and mean nothing.", ""]

    hi = [e for e in edges if e["confidence"] == "high"]
    L += [f"## High-confidence chains ({len(hi)})", ""]
    if hi:
        L += ["| Field | Producer | Consumer | Scope |", "|---|---|---|---|"]
        for e in sorted(hi, key=lambda x: (x["field"].lower(), x["from_path"]))[:200]:
            L.append(f"| `{e['field']}` | `{e['from_verb']} {e['from_path']}` | "
                     f"`{e['to_verb']} {e['to_path']}` | "
                     f"{'cross-module' if e['cross_module'] else 'same module'} |")
        if len(hi) > 200:
            L.append(f"\n*… {len(hi)-200} more; see `api-graph.json`.*")
    else:
        L.append("*None yet — high confidence needs observed producer responses. Capture more "
                 "endpoints (currently only GET has been executed) and re-run.*")

    L += ["", "## Most connected fields — the natural chaining keys", "",
          "| Field | Chains | Confidence spread |", "|---|---:|---|"]
    byf = defaultdict(list)
    for e in edges:
        byf[e["field"]].append(e)
    for f, lst in sorted(byf.items(), key=lambda kv: -len(kv[1]))[:25]:
        cs = Counter(x["confidence"] for x in lst)
        L.append(f"| `{f}` | {len(lst)} | " +
                 " · ".join(f"{k} {v}" for k, v in cs.most_common()) + " |")

    L += ["", "## ⚠️ Limits, stated plainly", "",
          "- A name match is **evidence of a possible chain, not proof of one**. Every `high` edge still "
          "needs a human to confirm the semantics before a test depends on it.",
          "- Outputs are only known for endpoints that have actually been **called**. Only GET has run so "
          "far, so POST-produced identifiers are invisible and real chains are being missed.",
          "- Response bodies were sampled from the evidence files' `body_preview` (first 2,000 chars), so "
          "fields deep in a large response may be absent.",
          "- Path templates such as `/api/User/{id}` are declared unresolved in `APIConfig`; a chain into "
          "them cannot be executed until the template is bound.", ""]
    (OUT / "chaining-report.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-confidence", choices=["low", "medium", "high"], default="low")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    log("=" * 74)
    log("API GRAPH BUILDER - Graphify api-graph layer")
    log("=" * 74)

    eps = load_endpoints()
    log(f"\n[1] endpoints from APIConfig.java      : {len(eps)}")
    log(f"    modules {len({e['module'] for e in eps})} · controllers "
        f"{len({e['controller'] for e in eps})} · models "
        f"{dict(Counter(e['model'] for e in eps))}")

    n_in = load_inputs(eps)
    log(f"\n[2] request payloads parsed            : {n_in}")
    log(f"    endpoints with >=1 input field     : {sum(1 for e in eps if e['inputs'])}")
    log(f"    distinct input field names         : {len({f for e in eps for f in e['inputs']})}")

    n_obs = load_outputs(eps)
    log(f"\n[3] captured responses matched         : {n_obs}")
    log(f"    endpoints with observed output     : {sum(1 for e in eps if e['observed'])}")
    log(f"    distinct output field names        : {len({f for e in eps for f in e['outputs']})}")

    edges = build_chains(eps)
    edges = [e for e in edges if RANK[e["confidence"]] >= RANK[args.min_confidence]]
    cc = Counter(e["confidence"] for e in edges)
    log(f"\n[4] chaining candidates                : {len(edges)}")
    log(f"    high {cc.get('high',0)} · medium {cc.get('medium',0)} · low {cc.get('low',0)}")
    log(f"    cross-module                       : {sum(1 for e in edges if e['cross_module'])}")

    bc = Counter(e["basis"] for e in edges)
    log(f"    basis: observed {bc.get('observed',0)} · inferred {bc.get('inferred',0)}")
    stats = {
        "Endpoints declared": len(eps),
        "Modules": len({e["module"] for e in eps}),
        "Endpoints with a parsed request payload": sum(1 for e in eps if e["inputs"]),
        "Endpoints with an observed response": sum(1 for e in eps if e["observed"]),
        "Chaining candidates": len(edges),
        "…from observed responses": bc.get("observed", 0),
        "…from name inference": bc.get("inferred", 0),
        "…high confidence": cc.get("high", 0),
        "…medium": cc.get("medium", 0),
        "…low": cc.get("low", 0),
        "Cross-module chains": sum(1 for e in edges if e["cross_module"]),
    }

    (OUT / "api-graph.json").write_text(json.dumps(
        {"stats": stats, "endpoints": eps, "chains": edges}, indent=1), encoding="utf-8")
    write_html(eps, edges, stats)
    write_md(eps, edges, stats)

    log("\n[5] written")
    for f in sorted(OUT.iterdir()):
        log(f"    {f.relative_to(ROOT)}  ({f.stat().st_size/1024:.0f} KB)")
    log("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
