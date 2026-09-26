#!/usr/bin/env python3
"""Render a markdown document into Word (.docx) and Excel (.xlsx) beside it.

    python tools\\render\\md_to_docx_xlsx.py "New Task\\Updated Project\\docs\\report.md"
    python tools\\render\\md_to_docx_xlsx.py report.md --all-data
    python tools\\render\\md_to_docx_xlsx.py report.md --skip "Appendix" --skip "Glossary"

Word gets every section; Excel gets a Cover sheet plus one worksheet per section that
has a table. Numbers such as `1,234` and `12.3%` become typed, right-aligned cells.
Needs `python-docx` and `openpyxl` (tools/requirements.txt).

⛔ **The markdown is the source of truth.** Nothing is recalculated here. Edit the
markdown and re-render; a hand edit to the .docx or .xlsx is lost on the next render.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

try:
    import md_render as R                                                # noqa: E402
except ImportError as exc:
    raise SystemExit(f"{exc} - install the renderer's packages: pip install -r tools/requirements.txt")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown", type=Path, help="path to the markdown file to render")
    ap.add_argument("--all-data", action="store_true",
                    help="also build one sheet holding every table in order")
    ap.add_argument("--skip", action="append", default=[], metavar="HEADING",
                    help="section heading to leave out of the workbook (repeatable; "
                         "matched case-insensitively, ignoring leading numbering)")
    a = ap.parse_args()

    skip = frozenset(R.normalise_heading(h) for h in a.skip) or R.DEFAULT_XLSX_SKIP
    docx_path, xlsx_path = R.render(a.markdown, all_data=a.all_data, skip=skip)
    print(f"Source:  {a.markdown}")
    print(f"Word:    {docx_path}")
    print(f"Excel:   {xlsx_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
