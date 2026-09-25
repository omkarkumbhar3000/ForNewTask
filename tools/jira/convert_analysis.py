#!/usr/bin/env python3
"""Render the PAMIT census markdown into Word (.docx) and Excel (.xlsx).

    python tools\\jira\\convert_analysis.py
    python tools\\jira\\convert_analysis.py --keep-all-sheets   # do not drop any worksheet

The date range is imported from `jira_analysis_2026` so the filename can never drift
from the report it renders — the 03 Sep edition was renamed by hand after generation and
the two disagreed, which is the failure `RANGE_SLUG` exists to prevent.

⛔ **This script never recalculates.** The markdown is the source of truth; every figure
written here is the figure parsed out of a markdown cell. Fix the analysis in
`jira_analysis_2026.py` and re-run it, then re-run this.

All the rendering lives in `analysis_render`, shared with the CI renderer
(`md_to_docx_xlsx.py`) so both workbooks come out formatted identically. The only PAMIT
difference is the consolidated `All Data` sheet, switched on below.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from paths import workspace_root                                        # noqa: E402
from jira_analysis_2026 import RANGE_SLUG                               # noqa: E402
import analysis_render as R                                             # noqa: E402

ROOT = workspace_root()
MD_FILE = ROOT / "docs" / "analysis" / f"Jira_Analysis_{RANGE_SLUG}.md"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--keep-all-sheets", action="store_true",
                    help="render every section as a worksheet, including the ones "
                         "normally excluded from the workbook")
    ap.add_argument("--md", type=Path, default=MD_FILE,
                    help="markdown to render (defaults to the current PAMIT census)")
    a = ap.parse_args()

    skip = frozenset() if a.keep_all_sheets else R.DEFAULT_XLSX_SKIP
    docx_path, xlsx_path = R.render(a.md, all_data=True, skip=skip)
    print(f"Source:  {a.md}")
    print(f"Word:    {docx_path}")
    print(f"Excel:   {xlsx_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
