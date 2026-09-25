"""
Extract the data/sources PDFs into a greppable, page-cited text corpus.

Usage:  python tools/rag/extract.py
Output: artifacts/rag-corpus/<slug>.md          full text, one "## [p<N>]" marker per page
        artifacts/rag-corpus/corpus.jsonl       {"doc","page","text"} one object per page
        artifacts/rag-corpus/<slug>.headings.tsv  detected headings as  page \t level \t text

Re-run after replacing a PDF in "data/sources/". Deterministic - no network, no API cost.
"""

import json
import re
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent


def _workspace_root():
    """Locate the workspace root by marker, not by counting parents.

    Mirrors tools/paths.py, which is the canonical implementation.
    Duplicated rather than imported because this package is not a sibling of it;
    the markers are what matter and they are identical. See that module's
    docstring for why CLAUDE.md + .claude/ and not a content folder name."""
    for candidate in (HERE, *HERE.parents):
        if (candidate / "CLAUDE.md").is_file() and (candidate / ".claude").is_dir():
            return candidate
    raise SystemExit(f"cannot locate the workspace root above {HERE}")


ROOT = _workspace_root()
SRC = ROOT / "data" / "sources"
if not SRC.is_dir():
    # OBJ-025: was _find_source_dir("Company Documents") with ROOT = SRC.parent.
    # That derived the workspace root FROM the source folder, so nesting the
    # sources one level deeper silently made ROOT the wrong directory. ROOT is
    # now found independently and SRC hangs off it.
    raise SystemExit(f"PDF source directory is missing: {SRC}")
OUT = HERE / "corpus"

DOCS = {
    "client-manager": "Client Manager Guide.pdf",
    "pam-admin": "PAM Administrative Guide.pdf",
    # The internal API reference (Confluence export, added 2026-07-30). This is the only
    # source in the corpus that documents endpoints and payloads.
    "pam-api": "PAM API (Internal Team).pdf",
}

# Confluence/Scroll exports repeat the space title and a page number on every page.
NOISE = re.compile(
    r"^\s*(ARCON\s*\|\s*PAM|Client Manager Guide|PAM Administrative Guide|"
    r"PAM API \(Internal Team\)|PAM API|Internal Team|"
    r"Introduction to PAM|Client Guide|Page \d+ of \d+|\d+)\s*$",
    re.IGNORECASE,
)

# A heading: short line, no terminal period, not all-lowercase, not a bare number.
NUMBERED = re.compile(r"^\s*(\d+(?:\.\d+)*)[.)]?\s+(\S.*)$")


def clean(raw: str) -> str:
    lines = []
    for ln in raw.splitlines():
        ln = ln.rstrip()
        if not ln.strip():
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if NOISE.match(ln):
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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jsonl = (OUT / "corpus.jsonl").open("w", encoding="utf-8")
    totals = []

    for slug, fname in DOCS.items():
        path = SRC / fname
        if not path.exists():
            print(f"SKIP {slug}: {path} not found")
            continue
        reader = PdfReader(str(path))
        n = len(reader.pages)
        md = [f"# {fname}", "", f"Source: `data/sources/{fname}` - {n} pages.", ""]
        headings = []
        chars = 0

        for i, page in enumerate(reader.pages, start=1):
            try:
                txt = clean(page.extract_text() or "")
            except Exception as exc:  # noqa: BLE001 - keep going, report at the end
                txt = ""
                print(f"  ! {slug} p{i}: {exc}")
            chars += len(txt)
            md.append(f"## [p{i}]")
            md.append("")
            md.append(txt if txt else "_(no extractable text - likely a screenshot)_")
            md.append("")
            for ln in txt.splitlines():
                lvl = is_heading(ln)
                if lvl:
                    headings.append((i, lvl, ln.strip()))
            jsonl.write(json.dumps({"doc": slug, "page": i, "text": txt}, ensure_ascii=False) + "\n")
            if i % 100 == 0:
                print(f"  {slug}: {i}/{n}")

        (OUT / f"{slug}.md").write_text("\n".join(md), encoding="utf-8")
        with (OUT / f"{slug}.headings.tsv").open("w", encoding="utf-8") as fh:
            fh.write("page\tlevel\theading\n")
            for pg, lvl, h in headings:
                fh.write(f"{pg}\t{lvl}\t{h}\n")

        totals.append((slug, n, chars, len(headings)))
        print(f"DONE {slug}: {n} pages, {chars:,} chars, {len(headings):,} headings")

    jsonl.close()
    print("\nsummary")
    for slug, n, chars, h in totals:
        print(f"  {slug:16} {n:>5} pages  {chars:>10,} chars  {h:>6,} headings")


if __name__ == "__main__":
    main()
