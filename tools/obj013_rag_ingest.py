"""obj013_rag_ingest.py — index the workspace's authored evidence for retrieval.

Q3 scope, as the owner set it: the measured evidence alongside the three extracted
PDFs — docs/findings/issues (12), the artifacts/loopholes packs (13), docs/analysis (9),
docs/management/summary, and the objective history. ⛔ NOT the Java framework source (Graphify
already indexes it) and NOT the pam/ product source.

⛔ SIBLING INDEX, BY DESIGN. This writes workspace.jsonl / workspace.manifest.json
next to the PDF corpus and never opens corpus.jsonl, never imports extract.py, never
touches corpus/*.md. Two reasons:

  1. extract.py is structurally PDF-only — PdfReader(path) is hard-bound at its
     ingestion point, so it cannot read markdown at all.
  2. extract.py opens corpus.jsonl in 'w' mode before doing any work and writes each
     corpus/<slug>.md through Path.write_text — the exact truncate-before-encode
     pattern that already destroyed ~12.7 KB of docs/gaps/02 in this workspace.
     Adding a second writer to that file would double the exposure for no benefit.

Generated artifacts are deliberately excluded: LH-*/EVIDENCE.md and EVIDENCE.xlsx are
rebuilt by build_lh_pack.py, so indexing them would index a derivative rather than the
authored analysis. The JIRA-TICKET.md in each pack IS the authored layer.

    python obj013_rag_ingest.py                    # dry run — what would be indexed
    python obj013_rag_ingest.py --apply            # build the index
    python obj013_rag_ingest.py search "app pool"  # query it
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import obj013_probes as probes  # noqa: E402

ROOT = probes.ROOT
RAG = ROOT / "artifacts" / "rag-corpus"
INDEX = RAG / "workspace.jsonl"
MANIFEST = RAG / "workspace.manifest.json"

# ⛔ Never read or write these — they belong to the PDF pipeline.
FORBIDDEN = {"corpus.jsonl", "pam-api.md", "pam-admin.md", "client-manager.md"}


@dataclass
class Source:
    group: str
    path: Path
    label: str


def discover() -> list[Source]:
    """Exactly the Q3 scope. Anything not listed here is deliberately out."""
    out: list[Source] = []

    for p in sorted((ROOT / "docs" / "findings" / "issues").glob("ISSUE-*.md")):
        out.append(Source("issues", p, p.stem))

    for pack in sorted((ROOT / "artifacts" / "loopholes").glob("LH-*")):
        if not pack.is_dir():
            continue
        # Authored layer only. EVIDENCE.md / EVIDENCE.xlsx / data/ are generated.
        t = pack / "JIRA-TICKET.md"
        if t.exists():
            out.append(Source("loopholes", t, pack.name))

    for p in sorted((ROOT / "docs" / "analysis").glob("A*.md")):
        out.append(Source("analysis", p, p.stem))

    for p in sorted((ROOT / "docs" / "management" / "summary").glob("*.md")):
        out.append(Source("summary", p, p.stem))

    for p in sorted((ROOT / "docs" / "history").glob("*.md")):
        out.append(Source("history", p, p.stem))

    briefs = ["developer-loopholes.md", "document-gap.md", "overview.md",
              "new-project-implementation.md"]
    for name in briefs:
        p = ROOT / "docs" / "briefs" / name
        if p.exists():
            out.append(Source("brief", p, p.stem))

    return [s for s in out if s.path.name not in FORBIDDEN]


_H = re.compile(r"^(#{1,4})\s+(.*)$")


def chunk(text: str, label: str) -> list[dict]:
    """Split on markdown headings. A section is the retrievable unit — it keeps a
    finding with its evidence, which a fixed-width window would cut apart."""
    chunks, heading, buf, start = [], "(preamble)", [], 1
    for i, line in enumerate(text.splitlines(), 1):
        m = _H.match(line)
        if m:
            body = "\n".join(buf).strip()
            if body:
                chunks.append({"heading": heading, "line": start, "text": body})
            heading, buf, start = m.group(2).strip(), [], i
        else:
            buf.append(line)
    body = "\n".join(buf).strip()
    if body:
        chunks.append({"heading": heading, "line": start, "text": body})
    return [c | {"source": label} for c in chunks]


def build(apply: bool) -> int:
    sources = discover()
    if not sources:
        print("No sources found — check the workspace layout.")
        return 1

    records, manifest = [], {}
    for s in sources:
        raw = s.path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        cs = chunk(text, s.label)
        rel = str(s.path.relative_to(ROOT)).replace("\\", "/")
        manifest[rel] = {
            "group": s.group, "label": s.label,
            "sha256": hashlib.sha256(raw).hexdigest()[:16],
            "bytes": len(raw), "lines": text.count("\n") + 1, "sections": len(cs),
        }
        for c in cs:
            records.append(c | {"file": rel, "group": s.group})

    by_group: dict[str, int] = {}
    for s in sources:
        by_group[s.group] = by_group.get(s.group, 0) + 1

    print(f"{'BUILDING' if apply else 'DRY RUN — nothing will be written'}")
    print(f"  sources  : {len(sources)}  {by_group}")
    print(f"  sections : {len(records)}")
    print(f"  index    : {INDEX.relative_to(ROOT)}")
    print(f"  manifest : {MANIFEST.relative_to(ROOT)}")
    print(f"  ⛔ untouched: corpus.jsonl, pam-api.md, pam-admin.md, client-manager.md")

    if not apply:
        print("\nRe-run with --apply to build.")
        return 0

    RAG.mkdir(parents=True, exist_ok=True)
    # temp + replace: an encoding failure leaves any existing index intact.
    tmp = INDEX.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8", errors="strict", newline="\n") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(INDEX)

    tmp = MANIFEST.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(
        {"_schema": "obj013-workspace-index/1",
         "_note": "Sibling to the PDF corpus. Rebuild: obj013_rag_ingest.py --apply",
         "sources": len(sources), "sections": len(records),
         "by_group": by_group, "files": manifest},
        indent=1, ensure_ascii=False), encoding="utf-8", errors="strict")
    tmp.replace(MANIFEST)

    print(f"\nwrote {len(records)} sections from {len(sources)} sources.")
    return 0


def stale() -> list[str]:
    """Which indexed sources changed since the last build. Cheap enough for the hook."""
    if not MANIFEST.exists():
        return ["(never built)"]
    man = json.loads(MANIFEST.read_text(encoding="utf-8")).get("files", {})
    changed = []
    for s in discover():
        rel = str(s.path.relative_to(ROOT)).replace("\\", "/")
        rec = man.get(rel)
        cur = hashlib.sha256(s.path.read_bytes()).hexdigest()[:16]
        if rec is None:
            changed.append(f"{rel} (new)")
        elif rec.get("sha256") != cur:
            changed.append(rel)
    for rel in man:
        if not (ROOT / rel).exists():
            changed.append(f"{rel} (removed)")
    return changed


def search(terms: list[str], limit: int) -> int:
    if not INDEX.exists():
        print(f"No index yet — run: python {Path(__file__).name} --apply")
        return 1
    pats = [re.compile(re.escape(t), re.I) for t in terms]
    hits = []
    for line in INDEX.open(encoding="utf-8"):
        r = json.loads(line)
        blob = f"{r['heading']}\n{r['text']}"
        score = sum(len(p.findall(blob)) for p in pats)
        if score and all(p.search(blob) for p in pats):
            hits.append((score, r))
    hits.sort(key=lambda x: -x[0])
    if not hits:
        print(f"No section matches all of: {' '.join(terms)}")
        return 1
    for score, r in hits[:limit]:
        print(f"\n── {r['file']}:{r['line']}  [{r['group']}]  (score {score})")
        print(f"   § {r['heading']}")
        body = " ".join(r["text"].split())
        print(f"   {body[:300]}{'…' if len(body) > 300 else ''}")
    print(f"\n{len(hits)} matching section(s); showing {min(limit, len(hits))}.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Index workspace evidence for retrieval (sibling to the PDF corpus).")
    ap.add_argument("--apply", action="store_true", help="write the index (otherwise dry run)")
    ap.add_argument("--stale", action="store_true", help="list sources changed since the last build")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("search", help="query the index")
    s.add_argument("terms", nargs="+")
    s.add_argument("--limit", type=int, default=6)
    a = ap.parse_args()

    if a.cmd == "search":
        return search(a.terms, a.limit)
    if a.stale:
        ch = stale()
        print("\n".join(ch) if ch else "index is current")
        return 1 if ch else 0
    return build(a.apply)


if __name__ == "__main__":
    sys.exit(main())
