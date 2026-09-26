"""Canonical workspace path resolution. Import the root from here; never count parents.

The root is the nearest directory above the caller that holds BOTH:

    CLAUDE.md     auto-loaded from the repository root by Claude Code
    .claude/      settings.json + rules/ are read from the root by the harness

Those two entries are pinned to the root by the harness itself, so no restructure can
rename them. That is why they are the markers and no content folder is.

Why this module exists: the workspace this framework came from once resolved its root
25 different ways. Eighteen counted parent directories (`parents[2]`, `.parent.parent`),
which silently point at the wrong folder the moment a script moves one level. Seven
searched for two content folder names, which broke seven scripts at once when one folder
was renamed. Neither failure raised; globs returned empty and callers reported success.

⛔ Do not reintroduce a depth count anywhere in this workspace.
⛔ Do not add a content folder to the markers. Content folders are free to move.
⛔ Renaming CLAUDE.md or .claude/ breaks every tool that imports this module.
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["workspace_root", "ROOT"]

_MARKER_FILE = "CLAUDE.md"
_MARKER_DIR = ".claude"


def workspace_root(start=None) -> Path:
    """Return the workspace root, found by searching upward from `start`.

    `start` may be a file (typically `__file__`) or a directory; it defaults to this
    module's own location. Raises SystemExit, loudly and by design, when the root
    cannot be found: carrying on with a guessed root is how scripts write to the wrong
    place while printing success.
    """
    here = Path(start).resolve() if start else Path(__file__).resolve()
    if here.is_file():
        here = here.parent
    for candidate in (here, *here.parents):
        if (candidate / _MARKER_FILE).is_file() and (candidate / _MARKER_DIR).is_dir():
            return candidate
    raise SystemExit(
        f"cannot locate the workspace root above {here} - "
        f"expected a directory containing both {_MARKER_FILE} and {_MARKER_DIR}/"
    )


ROOT = workspace_root()

# --- Named locations ---------------------------------------------------------
# Derived from ROOT only. When a folder moves, this block is the one place that changes.
# A Path is not a promise: check `.exists()` before relying on one.

CLAUDE_MD = ROOT / _MARKER_FILE
CLAUDE_DIR = ROOT / _MARKER_DIR

# The BLAST framework.
BLAST = ROOT / "BLAST"
OBJECTIVE = BLAST / "Objective.md"

# The working area for the current development task.
NEW_TASK = ROOT / "New Task"
CURRENT_PROJECT = NEW_TASK / "Current Project"   # input baseline - read, do not modify
UPDATED_PROJECT = NEW_TASK / "Updated Project"   # output - all new work lands here

# Framework drawers.
TOOLS = ROOT / "tools"
DOCS = ROOT / "docs"
HISTORY = DOCS / "history"
TMP = ROOT / ".tmp"                              # gitignored intermediates

# tools/
RAG = TOOLS / "rag"
RAG_CORPUS = TMP / "rag-corpus"                  # default output of tools/rag/extract.py
RENDER = TOOLS / "render"
ONBOARDING = TOOLS / "onboarding"
