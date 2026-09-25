#!/usr/bin/env python3
"""Run the whole census pipeline in order, and refuse to call it done unless it validates.

    python tools\\jira\\run_census.py                # offline: rebuild everything from the snapshots
    python tools\\jira\\run_census.py --live         # re-fetch from Jira first (overwrites the snapshots)
    python tools\\jira\\run_census.py --project CI   # one project, plus the pack and validation
    python tools\\jira\\run_census.py --dry-run      # print the commands without running them

Exit code: 0 = every step ran and every figure validated, 1 = a step failed, 2 = could not start.

Why one command
---------------
The pipeline is five steps and they are order-dependent in a way that fails *quietly*: regenerating
a report leaves the `.docx`, the `.xlsx` and the `21-09-2026/` client pack describing the previous
edition. Nothing about those files looks wrong — they open, they are formatted, they carry
plausible numbers — they simply describe a report that no longer exists. That is exactly the state
this workspace was found in on 2026-09-22.

So the steps are sequenced here rather than in a person's memory, and the run **ends with
`validate_analysis.py`**, whose exit code becomes this script's. A green run is a claim that the
published documents and the source data agree; there is no way to get a green run without that.

Each step shells out to the script that already owns it. Nothing is reimplemented here, so there is
no second copy of the logic to drift.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from paths import workspace_root                                        # noqa: E402

ROOT = workspace_root()
ANALYSIS = ROOT / "docs" / "analysis"

#: Stems are derived from the generators, never hardcoded, so the window can move in one place.
try:
    from jira_analysis_2026 import RANGE_SLUG
except Exception as exc:                                                # noqa: BLE001
    print("cannot import the PAMIT generator: {}".format(exc), file=sys.stderr)
    raise SystemExit(2)

PAMIT_MD = ANALYSIS / "Jira_Analysis_{}.md".format(RANGE_SLUG)
CI_MD = ANALYSIS / "CI_Jira_Analysis_{}.md".format(RANGE_SLUG)


def steps(projects: list, live: bool) -> list:
    """(label, argv) in dependency order. Generate -> render -> pack -> validate."""
    out = []
    offline = [] if live else ["--offline"]
    if "PAMIT" in projects:
        out.append(("generate PAMIT", ["jira_analysis_2026.py"] + offline))
    if "CI" in projects:
        out.append(("generate CI", ["ci_analysis_2026.py"] + offline))
    if "PAMIT" in projects:
        # convert_analysis.py derives its own path; md_to_docx_xlsx.py requires one.
        out.append(("render PAMIT", ["convert_analysis.py"]))
    if "CI" in projects:
        out.append(("render CI", ["md_to_docx_xlsx.py", str(CI_MD)]))
    # The pack always copies BOTH canonical reports, so it is rebuilt whichever project ran -
        # otherwise a one-project run would leave half the pack describing the previous edition.
    out.append(("build delivery pack", ["build_delivery_pack.py"]))
    out.append(("validate", ["validate_analysis.py"]))
    return out


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(
        description="Run the census pipeline end to end and validate the result.")
    ap.add_argument("--live", action="store_true",
                    help="re-fetch from Jira instead of reusing the snapshots "
                         "(overwrites them; the default issues zero HTTP)")
    ap.add_argument("--project", choices=["PAMIT", "CI", "all"], default="all")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the commands in order without running them")
    a = ap.parse_args()

    projects = ["PAMIT", "CI"] if a.project == "all" else [a.project]
    plan = steps(projects, a.live)

    print("Census pipeline - {} project(s), {}".format(
        len(projects), "LIVE fetch" if a.live else "offline (zero HTTP)"))
    print("=" * 72)

    if a.dry_run:
        for i, (label, argv) in enumerate(plan, 1):
            print("  {}. {:<22} python tools\\jira\\{}".format(
                i, label, " ".join(argv)))
        print("\nDry run - nothing was executed.")
        return 0

    started = time.time()
    for i, (label, argv) in enumerate(plan, 1):
        print("\n[{}/{}] {}".format(i, len(plan), label))
        print("-" * 72)
        cmd = [sys.executable, str(HERE / argv[0])] + argv[1:]
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            print("\n" + "=" * 72)
            print("STOPPED at step {} ({}) - exit {}.".format(
                i, label, result.returncode))
            if argv[0] == "validate_analysis.py":
                print("The documents were rebuilt but do NOT agree with the source data.")
                print("Fix the generator and run this again. Never hand-edit the markdown.")
            else:
                print("Later steps were not run, so the outputs on disk are now a mix of")
                print("editions. Re-run this command once the cause above is fixed.")
            return 1

    print("\n" + "=" * 72)
    print("DONE in {:.0f}s - reports, renders and the delivery pack are rebuilt and "
          "validated.".format(time.time() - started))
    print("  {}".format(PAMIT_MD.relative_to(ROOT)))
    print("  {}".format(CI_MD.relative_to(ROOT)))
    print("  {}".format((ROOT / "21-09-2026").relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
