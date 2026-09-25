"""
Query the extracted data/sources corpus. No embeddings, no network, no API cost -
regex retrieval over page-cited text. Fast enough at this corpus size (1.1M chars).

Run from the workspace root:

  python tools/rag/query.py find "web api registration"        # ranked pages containing all terms
  python tools/rag/query.py find "api user" --doc pam-admin    # restrict to one document
  python tools/rag/query.py page pam-admin 633                 # print one page
  python tools/rag/query.py page pam-admin 633-637             # print a range
  python tools/rag/query.py toc pam-admin --level 2 --grep api # heading index, filtered

Every result is cited as <doc>:p<N>, which maps back to the printed guide page.
"""

import argparse
import json
import re
import sys
from pathlib import Path

CORPUS = Path(__file__).resolve().parent / "corpus"


def load(doc: str | None):
    rows = []
    with (CORPUS / "corpus.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if doc and r["doc"] != doc:
                continue
            rows.append(r)
    return rows


def cmd_find(a) -> None:
    terms = [t for t in re.split(r"\s+", a.terms.strip()) if t]
    pats = [re.compile(re.escape(t), re.IGNORECASE) for t in terms]
    hits = []
    for r in load(a.doc):
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
    for r in load(a.doc):
        if lo <= r["page"] <= hi:
            print(f"\n===== {r['doc']}:p{r['page']} =====")
            print(r["text"] or "_(no extractable text)_")


def cmd_toc(a) -> None:
    path = CORPUS / f"{a.doc}.headings.tsv"
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


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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

args = p.parse_args()
args.func(args)
