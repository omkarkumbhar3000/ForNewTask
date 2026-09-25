#!/usr/bin/env python3
"""Assemble the dated PAM + CI delivery pack from the canonical census reports.

    python tools\\jira\\build_delivery_pack.py                 # uses the report date range
    python tools\\jira\\build_delivery_pack.py --date 21-09-2026

Produces, at the workspace root:

    21-09-2026/
    ├── PAM/  PAM_Analysis.md · PAM_Analysis.docx · PAM_Analysis.xlsx
    └── CI/   CI_Analysis.md  · CI_Analysis.docx  · CI_Analysis.xlsx

⛔ **The markdown is copied, never re-authored, and the Word and Excel files are rendered
from the copy that ships beside them** — not from the canonical report. So the three
files in each folder are provably the same analysis: `PAM_Analysis.docx` is derived from
`PAM_Analysis.md`, the file sitting next to it.

⚠️ The pack folder sits at the workspace root rather than under `artifacts/`, which is
where generated output normally lives. That is the owner's explicit layout for this
deliverable; it is still generated, so re-run this script rather than editing it.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from paths import workspace_root                                        # noqa: E402
from jira_analysis_2026 import RANGE_SLUG, DATE_TO                      # noqa: E402
import analysis_render as R                                             # noqa: E402

ROOT = workspace_root()
ANALYSIS = ROOT / "docs" / "analysis"

#: (folder, source markdown, delivered stem, build the All Data sheet)
PACK = [
    ("PAM", ANALYSIS / f"Jira_Analysis_{RANGE_SLUG}.md", "PAM_Analysis", True),
    ("CI", ANALYSIS / f"CI_Jira_Analysis_{RANGE_SLUG}.md", "CI_Analysis", False),
]


def default_date_folder() -> str:
    """`DD-MM-YYYY` taken from the report's own end date, not from the clock."""
    year, month, day = DATE_TO.split("-")
    return f"{day}-{month}-{year}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=default_date_folder(),
                    help="name of the dated folder (default: the report end date)")
    ap.add_argument("--out", type=Path, default=None,
                    help="parent directory for the dated folder (default: workspace root)")
    a = ap.parse_args()

    parent = a.out or ROOT
    base = parent / a.date
    missing = [str(src) for _, src, _, _ in PACK if not src.exists()]
    if missing:
        raise SystemExit("source markdown missing — regenerate the reports first:\n  "
                         + "\n  ".join(missing))

    print(f"Delivery pack: {base}")
    for folder, src, stem, all_data in PACK:
        dest_dir = base / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_md = dest_dir / f"{stem}.md"
        shutil.copyfile(src, dest_md)
        docx_path, xlsx_path = R.render(dest_md, all_data=all_data)
        print(f"  {folder}/")
        print(f"    {dest_md.name:<20} <- {src.relative_to(ROOT)}")
        print(f"    {docx_path.name:<20} <- {dest_md.name}")
        print(f"    {xlsx_path.name:<20} <- {dest_md.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
