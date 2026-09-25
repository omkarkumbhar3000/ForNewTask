"""OBJ-025 migration helper — rewrite a path prefix across the workspace, safely.

The restructure moves 14 top-level entries. Each move invalidates every place the
old path was written down, and the measured count is large: 1,924 backticked path
references across 143 markdown files, plus 26 code sites, plus JSON evidence
strings and rule globs. Hand-editing that nine times is how a reference gets
missed, and a missed markdown reference is exactly the kind of silent rot this
objective exists to remove.

⛔ What this tool refuses to touch, and why each one matters:

  docs/history/0*.md      APPEND-ONLY by the workspace's own absolute rule.
  docs/history/README.md These hold 436 backticked citations to old paths.
                              Rewriting history to match a new layout would
                              falsify the audit log. The translation key lives in
                              docs/history/README.md instead - a recorded old->new
                              prefix map, so a reader of an old record can resolve
                              a stale path without the record ever being altered.

  .claude/settings.json        The assistant is blocked from editing these by
  .claude/settings.local.json  design: an agent must not widen its own
                              permissions. Hook paths here are the owner's edit.
                              Reported, never written.

  state/drift/backups/    Backups of previous states. Rewriting a backup
                              destroys the thing it is a backup of.

  pam/, Automation gitlab repo/  Immovable nested repos (D28). Never written.

Usage (dry run is the default, as everywhere in this directory):

    python tools/obj025_repath.py <old-prefix> <new-prefix>
    python tools/obj025_repath.py <old-prefix> <new-prefix> --apply
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from paths import workspace_root

ROOT = workspace_root(__file__)

# Never written. See the module docstring for the reasoning behind each entry.
REFUSE_PREFIXES = (
    # The whole archive: the five numbered parts plus the index (was
    # objective_original_origin.md, now README.md inside it).
    "docs/history/",
    ".claude/settings.json",
    ".claude/settings.local.json",
    "state/drift/backups/",
    # A point-in-time audit of drift findings: 180 confirmed + 12 refuted, each
    # citing evidence by file AND line ("...01-Data-Gap-Analysis.md:57"). Those
    # citations record where the evidence was when the finding was made, so
    # rewriting them falsifies the record. Contrast data/questions/*.json and the
    # docs/analysis/*.md, which are LIVING documents whose citations must still
    # resolve for a reader - those are rewritten.
    "state/drift/register.json",
    "pam/",
    "Automation gitlab repo/",
)

TEXT_SUFFIXES = {
    ".md", ".py", ".json", ".ps1", ".mjs", ".js", ".jsx", ".css", ".html",
    ".txt", ".csv", ".yml", ".yaml", ".xml", ".properties", ".gitignore",
    ".gitattributes", ".sample", ".template",
}


def tracked_text_files() -> list[Path]:
    import subprocess
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    files = []
    for rel in out.split("\0"):
        if not rel:
            continue
        if any(rel.startswith(p) for p in REFUSE_PREFIXES):
            continue
        p = ROOT / rel
        if p.suffix.lower() in TEXT_SUFFIXES or p.name in (".gitignore", ".gitattributes"):
            files.append(p)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--apply", action="store_true",
                    help="write the changes (default is a dry run)")
    a = ap.parse_args()

    # Both slash flavours: markdown prose and .py use '/', PowerShell and Windows
    # prose use '\'. A rewrite that handles only one leaves half the references.
    variants = [(a.old, a.new)]
    if "/" in a.old:
        variants.append((a.old.replace("/", "\\"), a.new.replace("/", "\\")))

    hits, changed, refused, backslash_skipped = 0, [], [], []
    for f in tracked_text_files():
        try:
            s = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        o = s
        n = 0
        # The backslash variant is NOT applied to Python sources. It once rewrote
        # a display string into a path containing an invalid escape sequence, which
        # py_compile then rejected. Missing a backslash-spelled path inside a .py is
        # a reported miss; corrupting the file is a defect.
        use = variants if f.suffix.lower() != '.py' else variants[:1]
        for old, new in use:
            n += s.count(old)
            s = s.replace(old, new)
        if len(use) < len(variants) and variants[1][0] in s:
            backslash_skipped.append(f.relative_to(ROOT).as_posix())
        if s != o:
            hits += n
            rel = f.relative_to(ROOT).as_posix()
            changed.append((rel, n))
            if a.apply:
                f.write_text(s, encoding="utf-8", newline="\n")

    # Report what carries the old path but is deliberately not rewritten.
    import subprocess
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    for rel in out.split("\0"):
        if rel and any(rel.startswith(p) for p in REFUSE_PREFIXES):
            p = ROOT / rel
            if p.suffix.lower() in TEXT_SUFFIXES and p.exists():
                try:
                    if any(v[0] in p.read_text(encoding="utf-8") for v in variants):
                        refused.append(rel)
                except (UnicodeDecodeError, OSError):
                    pass

    mode = "APPLIED" if a.apply else "DRY RUN"
    print(f"  {mode}: {a.old!r} -> {a.new!r}")
    print(f"  {hits} reference(s) in {len(changed)} file(s)")
    for rel, n in sorted(changed, key=lambda x: -x[1]):
        print(f"    {n:4}  {rel}")
    if refused:
        print(f"\n  ⛔ {len(refused)} protected file(s) still carry the old path, "
              f"deliberately (append-only, owner-owned, or a backup):")
        for rel in refused:
            print(f"         {rel}")
    if backslash_skipped:
        print("")
        print("  WARN " + str(len(backslash_skipped)) + " Python file(s) spell this "
              "path with backslashes; left alone to avoid creating an invalid escape. "
              "Check by hand:")
        for rel in backslash_skipped:
            print(f"         {rel}")
    if not a.apply:
        print("\n  Nothing written. Re-run with --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
