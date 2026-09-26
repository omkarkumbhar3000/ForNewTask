"""
Extract PDFs into a greppable, page-cited text corpus.

Usage:
    python tools/rag/extract.py <pdf-or-folder> [<pdf-or-folder> ...] [--out DIR] [--noise REGEX]

    python tools/rag/extract.py "New Task/Current Project/requirements.pdf"
    python tools/rag/extract.py "New Task/Current Project" --out .tmp/rag-corpus

Output (default --out is <workspace>/.tmp/rag-corpus, which is gitignored):
    <slug>.md             full text, one "## [p<N>]" marker per page
    <slug>.headings.tsv   detected headings as  page <TAB> level <TAB> text
    corpus.jsonl          {"doc","page","text"}, one object per page, all documents

The slug is the file name, lower-cased, with runs of non-alphanumerics turned into "-".
A folder argument takes every *.pdf under it, recursively. Deterministic: no network,
no API cost. corpus.jsonl holds only the PDFs named in the current run; a document's
<slug>.md and .headings.tsv are overwritten when it is re-extracted, and left alone
otherwise. Pass every PDF you want searchable in one run.
"""

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from paths import RAG_CORPUS  # noqa: E402

# Lines that repeat on every page of most exports and carry no content.
DEFAULT_NOISE = r"^\s*(Page \d+ of \d+|\d+)\s*$"

# A heading: short line, no terminal period, not all-lowercase, not a bare number.
NUMBERED = re.compile(r"^\s*(\d+(?:\.\d+)*)[.)]?\s+(\S.*)$")


def slug_for(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-") or "doc"


def clean(raw: str, noise: re.Pattern) -> str:
    lines = []
    for ln in raw.splitlines():
        ln = ln.rstrip()
        if not ln.strip():
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if noise.match(ln):
            continue
        lines.append(ln)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def is_heading(ln: str) -> int:
    """Return a heading level 1-3, or 0 if the line is not a heading."""
    s = ln.strip()
    if not (3 <= len(s) <= 90):
        return 0
    if s.endswith((".", ",", ";", ":")):
        return 0
    if s[0].islower():
        return 0
    words = s.split()
    if len(words) > 12:
        return 0
    m = NUMBERED.match(s)
    if m:
        return min(1 + m.group(1).count("."), 3)
    # Title Case or ALL CAPS with no sentence punctuation
    letters = [w for w in words if w[:1].isalpha()]
    if not letters:
        return 0
    caps = sum(1 for w in letters if w[0].isupper())
    if caps / len(letters) >= 0.75:
        return 2
    return 0


def collect(inputs: list[str]) -> list[Path]:
    pdfs = []
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            pdfs.extend(sorted(p.rglob("*.pdf")))
        elif p.is_file() and p.suffix.lower() == ".pdf":
            pdfs.append(p)
        else:
            raise SystemExit(f"not a PDF or a folder: {p}")
    if not pdfs:
        raise SystemExit("no PDF found in: " + ", ".join(inputs))
    slugs = [slug_for(p) for p in pdfs]
    dupes = sorted({s for s in slugs if slugs.count(s) > 1})
    if dupes:
        raise SystemExit(f"two PDFs map to the same slug, rename one: {', '.join(dupes)}")
    return pdfs


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="PDF files or folders holding PDFs")
    ap.add_argument("--out", type=Path, default=RAG_CORPUS, help=f"output folder (default {RAG_CORPUS})")
    ap.add_argument("--noise", default=DEFAULT_NOISE,
                    help="regex for whole lines to drop, e.g. a header repeated on every page")
    a = ap.parse_args()

    try:
        from pypdf import PdfReader
    except ImportError:
        raise SystemExit("pypdf is not installed: pip install -r tools/requirements.txt")

    noise = re.compile(a.noise, re.IGNORECASE)
    pdfs = collect(a.inputs)
    a.out.mkdir(parents=True, exist_ok=True)
    totals = []

    with (a.out / "corpus.jsonl").open("w", encoding="utf-8") as jsonl:
        for path in pdfs:
            slug = slug_for(path)
            reader = PdfReader(str(path))
            n = len(reader.pages)
            md = [f"# {path.name}", "", f"Source: `{path.as_posix()}` - {n} pages.", ""]
            headings = []
            chars = 0

            for i, page in enumerate(reader.pages, start=1):
                try:
                    txt = clean(page.extract_text() or "", noise)
                except Exception as exc:  # noqa: BLE001 - keep going, report the page
                    txt = ""
                    print(f"  ! {slug} p{i}: {exc}")
                chars += len(txt)
                md += [f"## [p{i}]", "", txt or "_(no extractable text - likely a screenshot)_", ""]
                for ln in txt.splitlines():
                    lvl = is_heading(ln)
                    if lvl:
                        headings.append((i, lvl, ln.strip()))
                jsonl.write(json.dumps({"doc": slug, "page": i, "text": txt}, ensure_ascii=False) + "\n")
                if i % 100 == 0:
                    print(f"  {slug}: {i}/{n}")

            (a.out / f"{slug}.md").write_text("\n".join(md), encoding="utf-8")
            with (a.out / f"{slug}.headings.tsv").open("w", encoding="utf-8") as fh:
                fh.write("page\tlevel\theading\n")
                for pg, lvl, h in headings:
                    fh.write(f"{pg}\t{lvl}\t{h}\n")
            totals.append((slug, n, chars, len(headings)))
            print(f"DONE {slug}: {n} pages, {chars:,} chars, {len(headings):,} headings")

    print(f"\ncorpus: {a.out}")
    for slug, n, chars, h in totals:
        print(f"  {slug:24} {n:>5} pages  {chars:>10,} chars  {h:>6,} headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
