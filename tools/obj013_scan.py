"""obj013_scan.py — diff what the documents CLAIM against what the probes MEASURED.

Read-only. Writes nothing except (optionally) the drift report JSON under
state/drift/. Correcting a document is obj013_fix.py's job, never this one.

Three failure classes, deliberately kept apart because they need different handling:

  mismatch          the anchor was found and the value is wrong  -> auto-fixable
  anchor-not-found  the document moved or was reworded           -> REPORT, never guess
  anchor-ambiguous  the pattern matched more than once           -> REFUSE, an edit
                                                                    could hit the wrong site

A waiver closes an item, but is keyed to the evidence hash it was granted against,
so it expires the moment the underlying measurement changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import obj013_probes as probes  # noqa: E402

ROOT = probes.ROOT
DRIFT = ROOT / "state" / "drift"
FACTS = DRIFT / "facts.json"
WAIVERS = DRIFT / "waivers.json"
REPORT = DRIFT / "drift-report.json"

# D1 (v0.1): the only files obj013_fix.py may ever write. Everything else is
# report-only no matter what policy a fact declares.
WRITE_ALLOWLIST = {
    "CLAUDE.md",
    "README.md",
    ".claude/rules/automation-repo.md",
    ".claude/rules/api-surface.md",
    ".claude/rules/markdown-docs.md",
    "Automation gitlab repo/pam_automation_bootstrap/CLAUDE.md",
    "Automation gitlab repo/pam_automation_bootstrap/AGENTS.md",
}


@dataclass
class Finding:
    id: str
    kind: str                 # fact | invariant
    status: str               # ok | mismatch | anchor-not-found | anchor-ambiguous
                              # | probe-error | violated | waived
    severity: str = "medium"
    title: str = ""
    file: str | None = None
    claimed: str | None = None
    measured: str | None = None
    basis: str = ""
    derivation: str = ""
    fixable: bool = False
    in_write_allowlist: bool = False
    evidence_hash: str = ""
    note: str = ""
    span: list[int] = field(default_factory=list)   # [start, end] of the capture group

    @property
    def is_open(self) -> bool:
        return self.status not in ("ok", "waived")


def _norm(p: str) -> str:
    return p.replace("\\", "/").strip("/")


def _resolve(measurement: probes.Measurement, path: str | None) -> Any:
    """Resolve a dotted path into value, falling back to detail.

    Keys may themselves contain dots (file paths are used as keys), so at each step
    the LONGEST matching key wins rather than splitting naively on '.'.
    """
    if not path:
        return measurement.value
    for source in (measurement.value, measurement.detail):
        cur, rest = source, path
        ok = True
        while rest:
            if not isinstance(cur, dict):
                ok = False
                break
            key = next((k for k in sorted(cur, key=len, reverse=True)
                        if rest == k or rest.startswith(k + ".")), None)
            if key is None:
                ok = False
                break
            cur = cur[key]
            rest = rest[len(key):].lstrip(".")
        if ok:
            return cur
    return None


def _render(value: Any, template: str) -> str:
    try:
        return template.format(value=value)
    except (ValueError, TypeError, KeyError):
        return str(value)


def _ev_hash(*parts: Any) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:16]


def _load_json(p: Path, default):
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[warn] {p.name} is not valid JSON ({e}); treating as empty", file=sys.stderr)
        return default


def scan() -> list[Finding]:
    cfg = _load_json(FACTS, {"facts": [], "invariants": []})
    waivers = {w["id"]: w for w in _load_json(WAIVERS, {"waivers": []}).get("waivers", [])}

    wanted = {f["probe"] for f in cfg.get("facts", [])}
    wanted |= {i["probe"] for i in cfg.get("invariants", [])}
    measured = probes.run(sorted(wanted))

    out: list[Finding] = []

    # ---- facts: does every document quoting this number quote the right one?
    for fact in cfg.get("facts", []):
        m = measured.get(fact["probe"])
        if m is None or not m.ok:
            out.append(Finding(
                id=fact["id"], kind="fact", status="probe-error", severity="high",
                title=fact.get("title", ""), basis=fact.get("basis", ""),
                note=(m.error if m else "probe did not run") or ""))
            continue

        value = _resolve(m, fact.get("path"))
        expected = _render(value, fact.get("render", "{value}"))
        policy = fact.get("policy", "report-only")

        for site in fact.get("sites", []):
            rel = _norm(site["file"])
            path = ROOT / rel
            base = Finding(
                id=f'{fact["id"]}@{rel}', kind="fact", title=fact.get("title", ""),
                file=rel, measured=expected, basis=fact.get("basis", ""),
                derivation=m.derivation, status="ok",
                in_write_allowlist=rel in WRITE_ALLOWLIST)

            if not path.exists():
                base.status, base.severity = "anchor-not-found", "high"
                base.note = "declared site does not exist on disk"
                out.append(base)
                continue

            text = path.read_text(encoding="utf-8", errors="replace")
            hits = list(re.finditer(site["pattern"], text))
            if len(hits) == 0:
                base.status, base.severity = "anchor-not-found", "medium"
                base.note = ("pattern no longer matches — the document was reworded. "
                             "Re-anchor by hand; the loop will not guess a location.")
            elif len(hits) > 1:
                base.status, base.severity = "anchor-ambiguous", "medium"
                base.note = f"pattern matched {len(hits)} times; refusing to edit any of them"
            else:
                h = hits[0]
                claimed = h.group(1)
                base.claimed, base.span = claimed, [h.start(1), h.end(1)]
                if claimed == expected:
                    base.status, base.severity = "ok", "low"
                else:
                    base.status = "mismatch"
                    base.severity = "high"
                    base.fixable = (policy == "autofix" and base.in_write_allowlist)
                    if policy != "autofix":
                        base.note = fact.get("_why_report_only", "policy: report-only")
                    elif not base.in_write_allowlist:
                        base.note = "outside the D1 write allowlist — report-only in v0.1"

            base.evidence_hash = _ev_hash(base.id, base.claimed, base.measured, base.status)
            out.append(base)

        if not fact.get("sites"):
            out.append(Finding(
                id=fact["id"], kind="fact", status="ok", severity="low",
                title=fact.get("title", ""), measured=expected,
                basis=fact.get("basis", ""), derivation=m.derivation,
                note=fact.get("_why_report_only", "tracked, no document site declared")))

    # ---- invariants: safety and governance properties that must hold
    for inv in cfg.get("invariants", []):
        m = measured.get(inv["probe"])
        f = Finding(id=inv["id"], kind="invariant", title=inv.get("title", ""),
                    severity=inv.get("severity", "medium"), note=inv.get("statement", ""),
                    status="ok")
        if m is None or not m.ok:
            f.status, f.severity = "probe-error", "high"
            f.note = (m.error if m else "probe did not run") or ""
            out.append(f)
            continue
        f.derivation = m.derivation
        holds = True
        details = []
        for key, want in (inv.get("expect") or {}).items():
            got = m.value if key == "value" else _resolve(m, key.removeprefix("detail."))
            details.append(f"{key}={got!r} (want {want!r})")
            if got != want:
                holds = False
        f.measured = "; ".join(details)
        f.claimed = json.dumps(inv.get("expect"), ensure_ascii=False)
        f.status = "ok" if holds else "violated"
        f.evidence_hash = _ev_hash(f.id, f.measured, f.status)
        out.append(f)

    # ---- waivers, keyed to the evidence they were granted against
    for f in out:
        w = waivers.get(f.id)
        if w and f.is_open:
            if w.get("evidence_hash") == f.evidence_hash:
                f.status = "waived"
                f.note = f'waived: {w.get("reason", "no reason given")}'
                f.fixable = False
            else:
                f.note = (f.note + " | ⚠ a waiver exists but its evidence hash no longer "
                                   "matches — the measurement moved, so the waiver expired.").strip(" |")
    return out


def summarise(findings: list[Finding]) -> dict:
    open_ = [f for f in findings if f.is_open]
    by_sev = {s: sum(1 for f in open_ if f.severity == s)
              for s in ("critical", "high", "medium", "low")}
    return {
        "checked": len(findings),
        "clean": sum(1 for f in findings if f.status == "ok"),
        "waived": sum(1 for f in findings if f.status == "waived"),
        "open": len(open_),
        "by_severity": by_sev,
        "by_status": {s: sum(1 for f in open_ if f.status == s)
                      for s in sorted({f.status for f in open_})},
        "auto_fixable": sum(1 for f in open_ if f.fixable),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Diff document claims against measured reality.")
    ap.add_argument("--json", action="store_true", help="print the full report as JSON")
    ap.add_argument("--write", action="store_true",
                    help=f"also write {REPORT.relative_to(ROOT)}")
    ap.add_argument("--open-only", action="store_true", help="hide clean and waived items")
    a = ap.parse_args()

    findings = scan()
    summary = summarise(findings)
    report = {"summary": summary, "findings": [asdict(f) for f in findings]}

    if a.write:
        DRIFT.mkdir(parents=True, exist_ok=True)
        tmp = REPORT.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(report, indent=1, ensure_ascii=False),
                       encoding="utf-8", errors="strict")
        tmp.replace(REPORT)

    if a.json:
        print(json.dumps(report, indent=1, ensure_ascii=False))
        return 1 if summary["open"] else 0

    icon = {"ok": "ok  ", "waived": "wv  ", "mismatch": "DIFF", "violated": "VIOL",
            "anchor-not-found": "ANCH", "anchor-ambiguous": "AMBG", "probe-error": "ERR "}
    for f in findings:
        if a.open_only and not f.is_open:
            continue
        loc = f" {f.file}" if f.file else ""
        print(f"[{icon.get(f.status, f.status)}] {f.id}{loc}")
        if f.status == "mismatch":
            print(f"        claims {f.claimed!r} -> measured {f.measured!r}"
                  f"{'  [auto-fixable]' if f.fixable else ''}")
        elif f.status == "violated":
            print(f"        {f.measured}")
        if f.note and f.status != "ok":
            print(f"        {f.note[:190]}")

    s = summary
    print(f"\n{s['clean']} clean · {s['waived']} waived · {s['open']} open "
          f"({s['by_severity']['critical']} critical, {s['by_severity']['high']} high) · "
          f"{s['auto_fixable']} auto-fixable")
    return 1 if s["open"] else 0


if __name__ == "__main__":
    sys.exit(main())
