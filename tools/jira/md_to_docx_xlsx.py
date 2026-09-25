#!/usr/bin/env python3
"""Render any Jira analysis markdown into Word (.docx) and Excel (.xlsx).

    python tools\\jira\\md_to_docx_xlsx.py docs\\analysis\\CI_Jira_Analysis_01Jan26-21Sep26.md
    python tools\\jira\\md_to_docx_xlsx.py <report.md> --keep-all-sheets

This is the CI census renderer and the general-purpose one. It differs from
`convert_analysis.py` only in having no consolidated `All Data` sheet; both share
`analysis_render`, so the two workbooks format identically.

⛔ **The markdown is the source of truth.** Nothing is recalculated here.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import analysis_render as R                                             # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("markdown", type=Path,
                    help="path to the analysis markdown to render")
    ap.add_argument("--keep-all-sheets", action="store_true",
                    help="render every section as a worksheet, including the ones "
                         "normally excluded from the workbook")
    ap.add_argument("--all-data", action="store_true",
                    help="also build the consolidated All Data sheet")
    a = ap.parse_args()

    skip = frozenset() if a.keep_all_sheets else R.DEFAULT_XLSX_SKIP
    docx_path, xlsx_path = R.render(a.markdown, all_data=a.all_data, skip=skip)
    print(f"Source:  {a.markdown}")
    print(f"Word:    {docx_path}")
    print(f"Excel:   {xlsx_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
