#!/usr/bin/env python3
"""Preflight check: can this machine run the Jira analysis, and is it up to date?

    python tools\\jira\\doctor.py            # human-readable
    python tools\\jira\\doctor.py --json     # machine-readable

Exit code: 0 = ready for offline work, 1 = something required is missing or stale.

Run this first on a new machine, or when a script fails in a way that looks
environmental. It answers, in one screen, the questions a newcomer otherwise
discovers one traceback at a time:

  * is the interpreter and every third-party package present, and at what version
  * are the credentials configured (names only — this never prints a secret value)
  * are the snapshots on disk, so `--offline` will work at all
  * are the reports and their .docx/.xlsx renders present and mutually current
  * which of the tooling in this folder cannot work in this copy, and why

⛔ It issues **no HTTP**. Credential presence is checked by reading key names out of
`.env`; whether those credentials are *valid* is a live question this deliberately does
not ask, because answering it would contact Jira.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from paths import workspace_root                                        # noqa: E402

ROOT = workspace_root()
ANALYSIS = ROOT / "docs" / "analysis"
ENV_FILE = HERE / ".env"

MIN_PYTHON = (3, 11)

#: (import name, distribution name, what stops working without it)
PACKAGES = [
    ("openpyxl", "openpyxl", "every .xlsx builder and reader"),
    ("docx", "python-docx", "every .docx render, including the client delivery pack"),
    ("pptx", "python-pptx", "obj012_build_ppt.py only - not needed for Jira analysis"),
    ("xlrd", "xlrd", "the legacy .xls test-data workbooks - not needed for Jira analysis"),
    ("pypdf", "pypdf", "tools/rag/extract.py - not needed for Jira analysis"),
    ("jsonschema", "jsonschema", "tools/run_validation.py, which cannot run in this copy"),
]

#: Packages the Jira analysis genuinely cannot proceed without.
REQUIRED = {"openpyxl", "docx"}

REQUIRED_ENV_KEYS = ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY")

DATASETS = [
    ("PAMIT", ROOT / "artifacts" / "client-tickets" / "snapshots"
              / "jira-analysis-2026-01-01-to-2026-09-21.json",
     ANALYSIS / "Jira_Analysis_01Jan26-21Sep26.md",
     ROOT / "21-09-2026" / "PAM" / "PAM_Analysis.md"),
    ("CI", ROOT / "artifacts" / "snapshots"
           / "ci-analysis-2026-01-01-to-2026-09-21.json",
     ANALYSIS / "CI_Jira_Analysis_01Jan26-21Sep26.md",
     ROOT / "21-09-2026" / "CI" / "CI_Analysis.md"),
]

#: Present, importable, and unable to do anything here. Listed so a newcomer does not
#: spend an afternoon on a script whose absence of a target is by design.
INERT = [
    ("tools/obj0*.py, engage.py, chain_runner.py, token_guard.py",
     "target 'Automation gitlab repo/' and artifacts/runs/, neither of which exists "
     "in this copy"),
    ("tools/control_center.py + tools/control-center/",
     "approves git actions against repositories this copy does not contain"),
    ("tools/rag/query.py",
     "reads tools/rag/corpus/ while extract.py writes artifacts/rag-corpus/ - a "
     "one-line upstream defect; grep the corpus files directly"),
    (".claude/settings.json hooks",
     "hard-coded to E:\\Omkar\\Automation\\Dev Project\\..., which does not exist here, "
     "so BLAST/Objective.md is NOT auto-injected - read it explicitly"),
]


class Report:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add(self, group: str, item: str, ok, detail: str) -> None:
        self.rows.append({"group": group, "item": item,
                          "state": "INFO" if ok is None else
                                   ("OK" if ok else "MISSING"),
                          "detail": detail})

    @property
    def problems(self) -> int:
        return sum(1 for r in self.rows if r["state"] == "MISSING")


def check_python(rep: Report) -> None:
    v = sys.version_info
    ok = (v.major, v.minor) >= MIN_PYTHON
    rep.add("interpreter", "python", ok,
            "{}.{}.{} at {}".format(v.major, v.minor, v.micro, sys.executable)
            + ("" if ok else "  <- needs >= {}.{}".format(*MIN_PYTHON)))


def check_packages(rep: Report) -> None:
    for module, dist, why in PACKAGES:
        try:
            m = importlib.import_module(module)
        except ImportError:
            required = module in REQUIRED
            rep.add("packages", dist, not required,
                    ("REQUIRED - " if required else "optional here - ") + why
                    + "  ->  python -m pip install " + dist)
            continue
        # Ask the package metadata first: several distributions now emit a
        # DeprecationWarning for `__version__`, and a warning printed by a health check
        # reads exactly like the problem the check was run to find.
        try:
            import importlib.metadata as md
            version = md.version(dist)
        except Exception:                                        # noqa: BLE001
            version = getattr(m, "__version__", None) or "unknown version"
        rep.add("packages", dist, True, "{}  ({})".format(version, why))


def check_credentials(rep: Report) -> None:
    """Names only. This never reads or prints a secret's value."""
    if not ENV_FILE.exists():
        rep.add("credentials", ".env", None,
                "absent at {} - offline work is unaffected; a live fetch needs it "
                "(copy .env.sample)".format(ENV_FILE))
        return
    present = set()
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            if value.strip():
                present.add(key.strip())
    missing = [k for k in REQUIRED_ENV_KEYS if k not in present]
    rep.add("credentials", ".env", not missing,
            "all {} Jira keys set (values not read)".format(len(REQUIRED_ENV_KEYS))
            if not missing else "set but missing: {}".format(", ".join(missing)))


def check_data(rep: Report) -> None:
    for name, snapshot, report_md, pack_md in DATASETS:
        if snapshot.exists():
            mb = snapshot.stat().st_size / (1024 * 1024)
            rep.add("data", name + " snapshot", True,
                    "{}  ({:.1f} MB) - --offline will work".format(snapshot.name, mb))
        else:
            rep.add("data", name + " snapshot", False,
                    "absent: {} - --offline refuses; run once without it".format(
                        snapshot))

        if not report_md.exists():
            rep.add("data", name + " report", False, "absent: {}".format(report_md))
            continue
        stale = []
        for ext in (".docx", ".xlsx"):
            sib = report_md.with_suffix(ext)
            if not sib.exists():
                stale.append(sib.name + " missing")
            elif sib.stat().st_mtime < report_md.stat().st_mtime:
                stale.append(sib.name + " older than the markdown")
        if pack_md.exists() and pack_md.read_bytes() != report_md.read_bytes():
            stale.append("delivery pack differs from the canonical report")
        elif not pack_md.exists():
            stale.append("delivery pack missing")
        rep.add("data", name + " report", not stale,
                "{} and its renders are current".format(report_md.name) if not stale
                else "; ".join(stale) + "  ->  re-run convert_analysis.py / "
                                        "md_to_docx_xlsx.py, then build_delivery_pack.py")


def check_inert(rep: Report) -> None:
    for what, why in INERT:
        rep.add("cannot work here", what, None, why)


def run() -> Report:
    rep = Report()
    rep.add("workspace", "root", True, str(ROOT))
    check_python(rep)
    check_packages(rep)
    check_credentials(rep)
    check_data(rep)
    check_inert(rep)
    return rep


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Preflight check for the Jira analysis.")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()

    rep = run()
    if a.json:
        print(json.dumps({"problems": rep.problems, "checks": rep.rows}, indent=2))
        return 1 if rep.problems else 0

    # Width per group, not per document: one long entry under "cannot work here" would
    # otherwise push every other line's detail off the right edge of the terminal.
    group, width = None, 0
    for r in rep.rows:
        if r["group"] != group:
            group = r["group"]
            width = max(len(x["item"]) for x in rep.rows if x["group"] == group)
            print("\n" + group)
            print("-" * len(group))
        print("  [{:<7}] {:<{}}  {}".format(r["state"], r["item"], width, r["detail"]))

    print("\n" + "=" * 72)
    if rep.problems:
        print("NOT READY - {} item(s) above need attention.".format(rep.problems))
        return 1
    print("READY - the Jira analysis can be run offline on this machine.")
    print("Next:  python tools\\jira\\validate_analysis.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
