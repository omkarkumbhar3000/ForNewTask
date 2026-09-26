"""
Query a corpus built by extract.py. No embeddings, no network, no API cost: regex
retrieval over page-cited text, which is fast enough for a few thousand pages.

  python tools/rag/query.py find "login timeout"               # ranked pages containing all terms
  python tools/rag/query.py find "api user" --doc admin-guide  # restrict to one document
  python tools/rag/query.py page admin-guide 63                # print one page
  python tools/rag/query.py page admin-guide 63-67             # print a range
  python tools/rag/query.py toc admin-guide --level 2 --grep api
  python tools/rag/query.py docs                               # list the documents in the corpus

Every result is cited as <doc>:p<N>, which maps back to the printed PDF page.
--corpus defaults to <workspace>/.tmp/rag-corpus, where extract.py writes.
"""

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from paths import RAG_CORPUS  # noqa: E402


def load(corpus: Path, doc: str | None):
    path = corpus / "corpus.jsonl"
    if not path.is_file():
        sys.exit(f"no corpus at {corpus} - run tools/rag/extract.py first, or pass --corpus")
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if doc and r["doc"] != doc:
                continue
            rows.append(r)
    if doc and not rows:
        sys.exit(f"no document '{doc}' in {corpus} - see: query.py docs")
    return rows


def cmd_find(a) -> None:
    terms = [t for t in re.split(r"\s+", a.terms.strip()) if t]
    pats = [re.compile(re.escape(t), re.IGNORECASE) for t in terms]
    hits = []
    for r in load(a.corpus, a.doc):
        counts = [len(p.findall(r["text"])) for p in pats]
        if all(c > 0 for c in counts):
            hits.append((sum(counts), r))
    hits.sort(key=lambda x: -x[0])
    if not hits:
        print("no page contains all terms; try fewer terms")
        return
    print(f"{len(hits)} page(s) contain all of: {', '.join(terms)}\n")
    for score, r in hits[: a.limit]:
        first = pats[0].search(r["text"])
        start = max(0, (first.start() if first else 0) - a.context)
        snippet = r["text"][start : start + a.context * 2].replace("\n", " ")
        print(f"  {r['doc']}:p{r['page']}  (score {score})")
        print(f"    ...{snippet}...\n")


def cmd_page(a) -> None:
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", a.pages)
    if not m:
        sys.exit("pages must be N or N-M")
    lo = int(m.group(1))
    hi = int(m.group(2) or m.group(1))
    for r in load(a.corpus, a.doc):
        if lo <= r["page"] <= hi:
            print(f"\n===== {r['doc']}:p{r['page']} =====")
            print(r["text"] or "_(no extractable text)_")


def cmd_toc(a) -> None:
    path = a.corpus / f"{a.doc}.headings.tsv"
    if not path.is_file():
        sys.exit(f"no heading index at {path}")
    pat = re.compile(a.grep, re.IGNORECASE) if a.grep else None
    with path.open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            pg, lvl, head = line.rstrip("\n").split("\t", 2)
            if a.level and int(lvl) > a.level:
                continue
            if pat and not pat.search(head):
                continue
            print(f"  p{pg:>4}  {'  ' * (int(lvl) - 1)}{head}")


def cmd_docs(a) -> None:
    pages = {}
    for r in load(a.corpus, None):
        pages[r["doc"]] = pages.get(r["doc"], 0) + 1
    for doc, n in sorted(pages.items()):
        print(f"  {doc:24} {n:>5} pages")


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--corpus", type=Path, default=RAG_CORPUS, help=f"corpus folder (default {RAG_CORPUS})")
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("find", help="ranked pages containing all terms")
    f.add_argument("terms")
    f.add_argument("--doc")
    f.add_argument("--limit", type=int, default=15)
    f.add_argument("--context", type=int, default=180)
    f.set_defaults(func=cmd_find)

    g = sub.add_parser("page", help="print a page or range")
    g.add_argument("doc")
    g.add_argument("pages")
    g.set_defaults(func=cmd_page)

    t = sub.add_parser("toc", help="heading index")
    t.add_argument("doc")
    t.add_argument("--level", type=int, default=0)
    t.add_argument("--grep")
    t.set_defaults(func=cmd_toc)

    d = sub.add_parser("docs", help="list the documents in the corpus")
    d.set_defaults(func=cmd_docs)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
