"""Canonical workspace path resolution — the single re-point site (`OBJ-025`).

Before this module existed the workspace root was resolved 25 different times, in
four incompatible idioms, and every one of them was a silent-failure hazard:

  * 18 sites counted parent directories — `parents[2]`, `.parent.parent`,
    `os.path.join(HERE, "..", "..")`, `$PSScriptRoot '..\\..'`. A fixed-depth
    resolver cannot tell right from wrong. Move the script one level deeper and
    ROOT silently becomes `workbench/`; flatten it and ROOT overshoots above the
    workspace entirely. Neither raises. Globs just return empty and `.exists()`
    guards fall through, so the caller reports success having done nothing.

  * 7 sites searched upward for a directory containing BOTH `Reports/` and
    `Automation gitlab repo/` (one used `Reports/` + `document/`). That is
    depth-proof but name-brittle: it makes two *content* folder names part of the
    executable interface, so renaming either one breaks seven scripts at once.
    Three of the seven were inline copies rather than calls, so grepping for the
    function name found only four of them.

Both idioms are replaced by `workspace_root()` below, which searches for the two
entries the harness itself guarantees are root-pinned and which therefore cannot
be renamed by any future restructure:

    CLAUDE.md     auto-loaded from the repository root by Claude Code
    .claude/      settings.json + rules/ are read from the root by the harness

⛔ Do not reintroduce a depth count anywhere in this workspace. If a script needs
the root, import it from here.

⛔ Do not add `Reports`, `document`, or any other content folder to `_MARKERS`.
The whole point is that content folders are free to move; the markers are not.
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["workspace_root", "ROOT"]

# The two root-pinned entries. See the module docstring before changing these.
_MARKER_FILE = "CLAUDE.md"
_MARKER_DIR = ".claude"


def workspace_root(start=None) -> Path:
    """Return the workspace root, found by searching upward from `start`.

    `start` may be a file (typically `__file__`) or a directory; it defaults to
    this module's own location. Raises SystemExit — loudly, by design — when the
    root cannot be found, because every historical failure in this area was a
    script that carried on with a wrong root and wrote to the wrong place.
    """
    here = Path(start).resolve() if start else Path(__file__).resolve()
    if here.is_file():
        here = here.parent
    for candidate in (here, *here.parents):
        if (candidate / _MARKER_FILE).is_file() and (candidate / _MARKER_DIR).is_dir():
            return candidate
    raise SystemExit(
        f"cannot locate the workspace root above {here} — "
        f"expected a directory containing both {_MARKER_FILE} and {_MARKER_DIR}/"
    )


ROOT = workspace_root()

# --- Named locations ---------------------------------------------------------
# Everything below is derived from ROOT and nothing else. When OBJ-025 moves a
# folder, this block is the ONLY place that changes; no caller needs editing.

# Immovable nested checkouts — gitignored, own remotes, cannot be relocated (D28).
PAM = ROOT / "pam"
AUTOMATION_REPO = ROOT / "Automation gitlab repo"
BOOTSTRAP = AUTOMATION_REPO / "pam_automation_bootstrap"

# Root-pinned governance.
CLAUDE_MD = ROOT / _MARKER_FILE
CLAUDE_DIR = ROOT / _MARKER_DIR
BLAST = ROOT / "BLAST"
OBJECTIVE = BLAST / "Objective.md"

# Content locations — the v0.3 layout (`OBJ-025`). Five drawers by kind:
#   docs/       prose a human reads          data/       authored machine input
#   tools/      everything executable        artifacts/  everything a tool made
#   state/      job state + audit logs
TOOLS = ROOT / "tools"
DOCS = ROOT / "docs"
DATA = ROOT / "data"
ARTIFACTS = ROOT / "artifacts"
STATE = ROOT / "state"

# tools/
RAG = TOOLS / "rag"
ONBOARDING = TOOLS / "onboarding"
DASHBOARD = TOOLS / "dashboard"
DASHBOARD_PERF = TOOLS / "dashboard-performance"
DASHBOARD_DATA = DASHBOARD / "public" / "data"
JIRA = TOOLS / "jira"

# data/ — authored input
DATA_SOURCES = DATA / "sources"
ANALYSIS_AUTHORED = DATA / "analysis"
QUESTIONS = DATA / "questions"
PROFILES = DATA / "profiles"

# docs/ — authored prose
ANALYSIS = DOCS / "analysis"
BUSINESS_CONTEXT = DOCS / "business-context"
BRIEFS = DOCS / "briefs"
FINDINGS = DOCS / "findings"
ISSUES = FINDINGS / "issues"
GAPS = DOCS / "gaps"
HISTORY = DOCS / "history"
REGISTER = HISTORY / "README.md"
MANAGEMENT = DOCS / "management"
SUMMARY = MANAGEMENT / "summary"
SPECS = DOCS / "specs"
WRITER = MANAGEMENT          # writeup.md - kept as an alias for older callers

# artifacts/ — generated
RUNS = ARTIFACTS / "runs"
RUNS_ARCHIVE = ARTIFACTS / "runs-archive"
ANALYSIS_GENERATED = ARTIFACTS / "analysis-data"
WORKBOOKS = ARTIFACTS / "workbooks"
DECK = ARTIFACTS / "deck"
LOOPHOLES = ARTIFACTS / "loopholes"
REPO_ISSUES = ARTIFACTS / "repo-issues"
GRAPH = ARTIFACTS / "graph"
RAG_CORPUS = ARTIFACTS / "rag-corpus"

# state/ — tracked on purpose: these are the only evidence an unattended job ran.
STATE_DAILY = STATE / "daily"
STATE_WEEKLY = STATE / "weekly"
STATE_DRIFT = STATE / "drift"
STATE_PERF = STATE / "perf"
STATE_ENGAGE = STATE / "engage"    # gitignored - per-invocation, regenerable
STATE_OBJ010 = STATE / "obj010"
TOKEN_DIR = TOOLS   # .token* sit beside token_guard.py; ignored via **/ patterns

FLOWS = ARTIFACTS / "flows"
FLOWS_GENERATED = FLOWS / "generated"
FLOWS_GENERATED_DATA = FLOWS / "generated-data"
