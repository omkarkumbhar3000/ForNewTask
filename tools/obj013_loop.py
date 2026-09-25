"""obj013_loop.py — the one entrypoint for the closed loop (OBJ-013 v0.1).

The SessionStart hook calls `check --brief`; a human calls the same script with the
same sub-commands. There is no separate hidden path, which is deliberate: the loop
must never be a black box you cannot reproduce by hand.

    python tools/obj013_loop.py check           # read-only, human output
    python tools/obj013_loop.py check --brief   # hook form, capped output
    python tools/obj013_loop.py check --json    # machine-readable
    python tools/obj013_loop.py report          # full report + write to disk
    python tools/obj013_loop.py fix             # delegates (still needs --apply)

⛔ `check` never writes to a tracked file and never touches the network.
⛔ `fix` is reachable only by a human; the hook can never invoke it.

The brief is hard-capped. CLAUDE.md already auto-loads ~36 KB and Objective.md adds
~7 KB on top of every single turn — a verbose drift dump would crowd out the very
guidance it is reporting on. Full detail goes to disk; only the headline reaches context.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import obj013_scan as scanner  # noqa: E402

ROOT = scanner.ROOT
BRIEF_CAP = 1500          # bytes of hook-injected context; hard ceiling
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _rank(f) -> tuple:
    return (SEV_ORDER.get(f.severity, 9), f.kind != "invariant", f.id)


def render_brief(findings, summary) -> str:
    """Hard-capped headline for SessionStart injection."""
    open_ = sorted((f for f in findings if f.is_open), key=_rank)
    if not open_:
        return "🟢 Workspace drift check: clean — every registered fact matches source."

    s = summary["by_severity"]
    head = (f"🔎 Workspace drift: {summary['open']} open "
            f"({s['critical']} critical, {s['high']} high, {s['medium']} medium) · "
            f"{summary['clean']} clean · {summary['auto_fixable']} auto-fixable")
    lines = [head]
    for f in open_:
        loc = f" ({f.file})" if f.file else ""
        if f.status == "mismatch":
            line = f"  · {f.id}{loc}: says {f.claimed}, is {f.measured}"
        elif f.status == "violated":
            # An invariant's title states the DESIRED state. Printing it bare under a
            # ⛔ reads as if it holds — the opposite of the truth. Say it fails.
            line = f"  · ⛔ FAILS: {f.title or f.id}"
        elif f.status.startswith("anchor"):
            line = f"  · {f.id}{loc}: {f.status} — re-anchor by hand"
        else:
            line = f"  · {f.id}: {f.status}"
        if len("\n".join(lines + [line]).encode()) > BRIEF_CAP - 120:
            lines.append(f"  … and {len(open_) - (len(lines) - 1)} more")
            break
        lines.append(line)
    lines.append("  → detail: state/drift/drift-report.json · "
                 "fix: obj013_fix.py --apply")
    out = "\n".join(lines)
    return out if len(out.encode()) <= BRIEF_CAP else out[:BRIEF_CAP - 3] + "..."


def git_provenance() -> dict:
    """Local-only freshness. ⛔ No fetch, no pull, no push, no merge, no checkout."""
    m = scanner.probes.run(["repo_state", "graph_root_marker",
                            "graph_indexes_validation_pkg"])
    prov = {"repos": m["repo_state"].detail if m["repo_state"].ok else {},
            "graph": {}}
    gr = m["graph_root_marker"]
    if gr.ok:
        prov["graph"]["declared_root"] = gr.detail.get("declared_root")
        prov["graph"]["REFUSE_REBUILD"] = gr.detail.get("REFUSE_REBUILD")
    gi = m["graph_indexes_validation_pkg"]
    if gi.ok:
        prov["graph"]["indexes_validation_pkg"] = not gi.detail.get("graph_is_stale")

    # RAG: REPORT ONLY. Q4 bars an unattended re-ingest, so the loop says how many
    # sources moved and leaves the rebuild to a human running --apply.
    try:
        import obj013_rag_ingest as rag          # noqa: PLC0415
        changed = rag.stale()
        prov["rag"] = {"changed_sources": len(changed),
                       "examples": changed[:5],
                       "rebuild": "python tools/obj013_rag_ingest.py --apply"}
    except Exception as e:                        # never let this break the check
        prov["rag"] = {"error": f"{type(e).__name__}: {e}"}
    return prov


def cmd_check(a) -> int:
    findings = scanner.scan()
    summary = scanner.summarise(findings)
    # Always persist. engage reads this file; a check that leaves it stale makes
    # engage confidently wrong. See write_report().
    write_report(findings, summary)

    if a.brief:
        print(render_brief(findings, summary))
        return 0                      # never fail a session start

    if a.json:
        print(json.dumps({"summary": summary, "provenance": git_provenance(),
                          "findings": [asdict(f) for f in findings]},
                         indent=1, ensure_ascii=False))
        return 1 if summary["open"] else 0

    prov = git_provenance()
    print("=" * 72)
    print("  WORKSPACE DRIFT CHECK — OBJ-013 closed loop v0.1")
    print("=" * 72)
    for name, r in (prov.get("repos") or {}).items():
        if "error" in r:
            print(f"  repo {name:11} !! {r['error']}")
            continue
        extra = ""
        if r.get("upstream"):
            extra = f" · {r['ahead']} ahead / {r['behind']} behind {r['upstream']}"
        else:
            extra = " · no upstream (local-only branch)"
        dirty = f" · {r['dirty_files']} uncommitted" if r["dirty_files"] else " · clean"
        stash = f" · {r['stashes']} stash" if r.get("stashes") else ""
        print(f"  repo {name:11} {r['branch']}@{r['head']}{dirty}{stash}{extra}")
    g = prov.get("graph", {})
    if g.get("REFUSE_REBUILD"):
        print(f"  graph            ⛔ REFUSE REBUILD — .graphify_root names "
              f"{g.get('declared_root')}")
    if g.get("indexes_validation_pkg") is False:
        print("  graph            ⚠ does not index com.arcon.utils.validation (stale)")
    r = prov.get("rag", {})
    if r.get("error"):
        print(f"  rag              !! {r['error']}")
    elif r.get("changed_sources"):
        ex = ", ".join(Path(x).name for x in r["examples"][:3])
        print(f"  rag              ⚠ {r['changed_sources']} source(s) changed since last "
              f"ingest ({ex}…) → {r['rebuild']}")
    else:
        print("  rag              current")
    print("-" * 72)

    for f in sorted((x for x in findings if x.is_open), key=_rank):
        tag = {"mismatch": "DIFF", "violated": "VIOL", "anchor-not-found": "ANCH",
               "anchor-ambiguous": "AMBG", "probe-error": "ERR "}.get(f.status, f.status)
        print(f"  [{tag}] {f.severity:8} {f.id}")
        if f.file:
            print(f"          {f.file}")
        if f.status == "mismatch":
            print(f"          says {f.claimed!r} · measured {f.measured!r}"
                  f"{'  [auto-fixable]' if f.fixable else ''}")
        elif f.status == "violated":
            print(f"          {f.measured}")
        if f.note:
            print(f"          {f.note[:160]}")
    s = summary
    print("-" * 72)
    print(f"  {s['clean']} clean · {s['waived']} waived · {s['open']} open "
          f"({s['by_severity']['critical']} critical, {s['by_severity']['high']} high) · "
          f"{s['auto_fixable']} auto-fixable")
    if s["auto_fixable"]:
        print("  → python tools/obj013_fix.py           (dry run)")
        print("  → python tools/obj013_fix.py --apply   (write, with backups)")
    print("=" * 72)
    return 1 if s["open"] else 0


def write_report(findings, summary) -> None:
    """Persist the full report, atomically.

    OBJ-027: this used to live only inside `cmd_report`, a subcommand nothing
    invoked automatically. `check` computed everything and threw it away, while
    engage.py READ drift-report.json to build its attention list — so engage was
    reporting whatever drift state someone had last written by hand. Measured: the
    file was a day stale and still claimed 11 authored issues where there were 12.
    `check` now always writes it, which removes the staleness class rather than
    documenting it.

    Writing this file is not a "fix": it is the loop's own output, not a document
    the loop corrects. The read-only guarantee is about the WORKSPACE.
    """
    scanner.DRIFT.mkdir(parents=True, exist_ok=True)
    payload = {"summary": summary, "provenance": git_provenance(),
               "findings": [asdict(f) for f in findings]}
    tmp = scanner.REPORT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=1, ensure_ascii=False),
                   encoding="utf-8", errors="strict")
    tmp.replace(scanner.REPORT)


def cmd_report(a) -> int:
    findings = scanner.scan()
    summary = scanner.summarise(findings)
    write_report(findings, summary)
    print(f"wrote {scanner.REPORT.relative_to(ROOT)}  "
          f"({summary['open']} open, {summary['clean']} clean)")
    return 0


def cmd_fix(a) -> int:
    """Delegate, so there is exactly one implementation of the write path."""
    cmd = [sys.executable, str(Path(__file__).with_name("obj013_fix.py"))]
    if a.apply:
        cmd.append("--apply")
    return subprocess.run(cmd).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="OBJ-013 closed loop — drift detection and repair.")
    sub = ap.add_subparsers(dest="cmd")

    c = sub.add_parser("check", help="read-only drift check")
    c.add_argument("--brief", action="store_true", help="capped output for the SessionStart hook")
    c.add_argument("--json", action="store_true")
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser("report", help="write state/drift/drift-report.json")
    r.set_defaults(fn=cmd_report)

    f = sub.add_parser("fix", help="apply mechanical corrections (dry-run without --apply)")
    f.add_argument("--apply", action="store_true")
    f.set_defaults(fn=cmd_fix)

    a = ap.parse_args()
    if not a.cmd:
        a = ap.parse_args(["check"])
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
