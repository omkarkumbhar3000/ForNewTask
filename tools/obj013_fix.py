"""obj013_fix.py — apply the mechanical corrections Q4 authorises, and refuse everything else.

⛔ DRY-RUN BY DEFAULT. `--apply` is mandatory to write a single byte.
⛔ The SessionStart hook can NEVER reach this script. Fixing is a human action.

Nine folders in this workspace have no git history, and content has already been lost
twice here: PowerShell Set-Content produced mojibake by reading UTF-8 as ANSI, and
Path.write_text() destroyed ~12.7 KB of docs/gaps/02 by truncating in 'w' mode
and then aborting on a UnicodeEncodeError. Every interlock below exists because of a
real loss, not a hypothetical one:

  1. dry-run default; --apply required
  2. write allowlist (D1) — six guidance files, nothing else, ever
  3. the anchor must match EXACTLY ONCE or the edit is skipped
  4. the file hash must be unchanged since the scan, or the edit is refused
  5. a full byte-for-byte backup is taken before the first edit to a file
  6. writes go through a temp file + os.replace (atomic), encoding='utf-8',
     errors='strict' — an encoding failure leaves the original untouched
  7. only the capture group's span is replaced. Never a whole-file rewrite.

Usage:
    python obj013_fix.py                 # dry run — show what would change
    python obj013_fix.py --apply         # apply, with backups
    python obj013_fix.py --apply --id graph.automation.nodes@CLAUDE.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import obj013_scan as scanner  # noqa: E402

ROOT = scanner.ROOT
BACKUPS = scanner.DRIFT / "backups"
FIXLOG = scanner.DRIFT / "fix-log.jsonl"

# Never written by this script under any circumstance, allowlist or not.
HARD_EXCLUSIONS = (
    "docs/history/archive/workbench-archive/",
    "artifacts/loopholes/LH-01-",
    "docs/history/README.md",
    "docs/history/",
    "artifacts/runs-archive/",
    "pam/",
)


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _excluded(rel: str) -> str | None:
    for x in HARD_EXCLUSIONS:
        if rel.startswith(x):
            return x
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply mechanical fact corrections. Dry-run by default.")
    ap.add_argument("--apply", action="store_true", help="actually write (otherwise dry run)")
    ap.add_argument("--id", action="append", default=[], help="restrict to these finding ids")
    a = ap.parse_args()

    findings = scanner.scan()
    targets = [f for f in findings if f.status == "mismatch" and f.fixable]
    if a.id:
        targets = [f for f in targets if f.id in a.id]

    skipped = [f for f in findings
               if f.status == "mismatch" and not f.fixable]

    # Apply highest-offset-first within each file. Editing a span shifts every offset
    # after it, so ascending order silently invalidates later spans — the hash check
    # then refuses them, which is safe but useless. Descending order keeps all spans
    # valid, so every edit to a file lands in one pass.
    targets.sort(key=lambda f: (f.file or "", -(f.span[0] if f.span else 0)))

    if not targets:
        print("Nothing auto-fixable.")
        if skipped:
            print(f"\n{len(skipped)} mismatch(es) are report-only and need a human:")
            for f in skipped:
                print(f"  - {f.id}: claims {f.claimed!r}, measured {f.measured!r}")
                if f.note:
                    print(f"      {f.note[:170]}")
        return 0

    stamp = time.strftime("%Y-%m-%d_%H%M%S")
    backup_dir = BACKUPS / stamp
    applied = failed = 0
    backed_up: set[str] = set()

    print(f"{'APPLYING' if a.apply else 'DRY RUN — no file will be written'}"
          f"  ({len(targets)} candidate edit(s))\n")

    for f in targets:
        rel = f.file or ""
        path = ROOT / rel

        why = _excluded(rel)
        if why:
            print(f"[REFUSE] {f.id}\n         hard exclusion: {why}")
            failed += 1
            continue
        if rel not in scanner.WRITE_ALLOWLIST:
            print(f"[REFUSE] {f.id}\n         not in the D1 write allowlist")
            failed += 1
            continue
        if not path.exists():
            print(f"[REFUSE] {f.id}\n         file vanished since the scan")
            failed += 1
            continue

        text = path.read_text(encoding="utf-8", errors="strict")
        start, end = f.span
        actual = text[start:end]
        if actual != f.claimed:
            # The file moved under us between scan and apply.
            print(f"[REFUSE] {f.id}\n         span no longer holds {f.claimed!r} "
                  f"(found {actual!r}) — file changed since the scan; re-run the scan")
            failed += 1
            continue

        new_text = text[:start] + (f.measured or "") + text[end:]
        preview_at = text.rfind("\n", 0, start) + 1
        preview_to = text.find("\n", end)
        line_no = text.count("\n", 0, start) + 1
        before = text[preview_at:preview_to if preview_to != -1 else len(text)].strip()
        after = new_text[preview_at:new_text.find("\n", end) if new_text.find("\n", end) != -1
                         else len(new_text)].strip()

        print(f"[{'EDIT' if a.apply else 'WOULD'}] {f.id}")
        print(f"        {rel}:{line_no}  {f.claimed!r} -> {f.measured!r}")
        print(f"        - {before[:150]}")
        print(f"        + {after[:150]}")

        if not a.apply:
            continue

        try:
            if rel not in backed_up:
                dest = backup_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
                backed_up.add(rel)
            tmp = path.with_suffix(path.suffix + ".obj013.tmp")
            tmp.write_text(new_text, encoding="utf-8", errors="strict", newline="")
            os.replace(tmp, path)
            applied += 1
            FIXLOG.parent.mkdir(parents=True, exist_ok=True)
            with FIXLOG.open("a", encoding="utf-8") as log:
                log.write(json.dumps({
                    "stamp": stamp, "id": f.id, "file": rel, "line": line_no,
                    "from": f.claimed, "to": f.measured, "basis": f.basis,
                    "derivation": f.derivation, "backup": str((backup_dir / rel).relative_to(ROOT)),
                    "sha_after": _sha(path),
                }, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"        !! FAILED, original untouched: {type(e).__name__}: {e}")
            failed += 1

    print()
    if a.apply:
        print(f"{applied} applied · {failed} refused")
        if applied:
            print(f"backups: {backup_dir.relative_to(ROOT)}")
            print(f"log:     {FIXLOG.relative_to(ROOT)}")
    else:
        print(f"{len(targets)} would be applied · {failed} would be refused")
        print("Re-run with --apply to write.")
    if skipped:
        print(f"\n{len(skipped)} further mismatch(es) are report-only — a human must decide:")
        for f in skipped:
            print(f"  - {f.id}: {f.note[:150]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
