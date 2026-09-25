#!/usr/bin/env python3
"""
OBJ-023 - failure reproducibility analysis.

Compares two executions hop by hop and classifies every test case by what its verdict DID between
them. The question it answers: of the failures in the baseline, which are real and reproducible, and
which did not happen again?

    python obj023_reproducibility.py <baseline-run> <rerun>          # print the summary
    python obj023_reproducibility.py <baseline-run> <rerun> --json   # machine-readable
    python obj023_reproducibility.py <baseline-run> <rerun> --write  # + write report + dataset

Run ids or folder paths both work. Zero HTTP, zero database - it reads stored results only.

Why hop-level and not flow-level:
    A flow is a chain; one failing hop marks the whole flow FAIL, so a flow-level comparison cannot
    tell "the same hop failed again" from "a different hop failed this time". The unit of a test case
    here is a hop, keyed on (flow, hop number, hop name).

⛔ What this deliberately does NOT do:
    It does not call a non-reproduced failure "environmental". Not reproducing once is evidence of
    instability, not proof of a cause - the hop may be order-dependent, data-dependent, or genuinely
    intermittent in the product. The classification says `not-reproduced`, and the cause column
    states the HTTP signature that was actually observed, so a reader can judge it.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
RUNS = ROOT / "artifacts" / "runs"
OUT_DATA = ROOT / "tools" / "dashboard" / "public" / "data"

# HTTP signatures that are plausibly infrastructure rather than contract. Used only to describe a
# failure, never to reclassify one.
TRANSIENT_STATUS = {500, 502, 503, 504, None}


def resolve(spec: str) -> Path:
    p = Path(spec)
    if p.is_dir():
        return p
    p = RUNS / spec
    if p.is_dir():
        return p
    sys.exit(f"run folder not found: {spec}")


def verdict_of(hop: dict) -> str:
    if hop.get("skipped"):
        return "BLOCKED"
    checks = hop.get("checks") or []
    if not checks:
        return "NOT EXECUTED"
    return "FAIL" if any(c.get("verdict") == "FAIL" for c in checks) else "PASS"


def index_hops(results: dict) -> dict[tuple, dict]:
    """(flow, hop n, hop name) -> hop record. That triple is the test-case identity."""
    out = {}
    for flow in results.get("flows", []):
        fid = flow.get("id")
        for hop in flow.get("hops", []):
            key = (fid, hop.get("n"), hop.get("name"))
            out[key] = {
                "flow": fid,
                "hop": hop.get("n"),
                "name": hop.get("name"),
                "verb": hop.get("verb"),
                "path": hop.get("path"),
                "status": hop.get("status"),
                "latency_ms": hop.get("latency_ms"),
                "verdict": verdict_of(hop),
                "failing": [c.get("check") for c in (hop.get("checks") or [])
                            if c.get("verdict") == "FAIL"],
            }
    return out


def signature(hop: dict) -> str:
    """A short, factual description of how this hop failed - not an attribution of cause."""
    st = hop.get("status")
    layers = hop.get("failing") or []
    if st is None:
        return "no response (timeout or connection failure)"
    if st == 404:
        return "HTTP 404 - endpoint not present"
    if st in TRANSIENT_STATUS:
        return f"HTTP {st} - server-side error"
    if st == 200:
        return f"HTTP 200 but checks failed: {', '.join(layers[:3]) or 'unspecified'}"
    return f"HTTP {st} - checks failed: {', '.join(layers[:3]) or 'unspecified'}"


def analyse(base_dir: Path, rerun_dir: Path) -> dict:
    base = json.loads((base_dir / "results.json").read_text(encoding="utf-8"))
    rerun = json.loads((rerun_dir / "results.json").read_text(encoding="utf-8"))
    b, r = index_hops(base), index_hops(rerun)

    transitions: dict[str, list[dict]] = collections.defaultdict(list)
    matrix: collections.Counter = collections.Counter()

    for key, bh in b.items():
        rh = r.get(key)
        if rh is None:
            matrix[(bh["verdict"], "ABSENT")] += 1
            transitions[f"{bh['verdict']}->ABSENT"].append({**bh, "rerunStatus": None})
            continue
        matrix[(bh["verdict"], rh["verdict"])] += 1
        transitions[f"{bh['verdict']}->{rh['verdict']}"].append({
            "flow": bh["flow"], "hop": bh["hop"], "name": bh["name"],
            "verb": bh["verb"], "path": bh["path"],
            "baselineStatus": bh["status"], "rerunStatus": rh["status"],
            "baselineSignature": signature(bh) if bh["verdict"] == "FAIL" else None,
            "rerunSignature": signature(rh) if rh["verdict"] == "FAIL" else None,
            "baselineFailingLayers": bh["failing"],
            "rerunFailingLayers": rh["failing"],
        })

    new_in_rerun = [k for k in r if k not in b]

    base_failed = sum(1 for h in b.values() if h["verdict"] == "FAIL")
    ff = matrix[("FAIL", "FAIL")]
    fp = matrix[("FAIL", "PASS")]
    f_absent = matrix[("FAIL", "ABSENT")]
    f_other = base_failed - ff - fp - f_absent
    pf = matrix[("PASS", "FAIL")]
    pp = matrix[("PASS", "PASS")]

    # Reproducible rate is computed over failures that were actually re-observed. A failure whose
    # hop never ran again is neither confirmed nor cleared, and is excluded from the denominator
    # rather than silently counted as one or the other.
    reobserved = ff + fp
    confirmed_rate = round(100 * ff / reobserved, 1) if reobserved else "N/A"

    # Of the non-reproduced failures, how many had looked infrastructure-shaped in the baseline.
    fp_transient = sum(1 for t in transitions.get("FAIL->PASS", [])
                       if t["baselineStatus"] in TRANSIENT_STATUS)

    return {
        "generatedBy": "tools/obj023_reproducibility.py",
        "objective": "OBJ-023",
        "baseline": base_dir.name,
        "rerun": rerun_dir.name,
        "unit": "hop (one test case), keyed on (flow, hop number, hop name)",
        "counts": {
            "baselineHops": len(b),
            "rerunHops": len(r),
            "hopsComparable": sum(1 for k in b if k in r),
            "hopsOnlyInBaseline": len(b) - sum(1 for k in b if k in r),
            "hopsOnlyInRerun": len(new_in_rerun),
        },
        "summary": {
            "totalFailedInBaseline": base_failed,
            "failedAgain": ff,
            "passedOnRerun": fp,
            "notReObserved": f_absent + max(0, f_other),
            "confirmedReproducibleFailures": ff,
            "confirmedReproducibleRatePctOfReobservedFailures": confirmed_rate,
            "nonReproducedFailures": fp,
            "ofWhichHadTransientSignature": fp_transient,
            "newlyFailing": pf,
            "stablePasses": pp,
        },
        "matrix": {f"{a}->{c}": n for (a, c), n in sorted(matrix.items())},
        "transitions": {k: v for k, v in transitions.items()},
    }


def render(a: dict) -> str:
    s, c = a["summary"], a["counts"]
    L = []
    L.append("=" * 78)
    L.append("  OBJ-023 FAILURE REPRODUCIBILITY")
    L.append(f"  baseline {a['baseline']}   vs   re-run {a['rerun']}")
    L.append(f"  unit: {a['unit']}")
    L.append("=" * 78)
    L.append(f"  comparable test cases : {c['hopsComparable']} "
             f"(baseline {c['baselineHops']}, re-run {c['rerunHops']})")
    L.append("")
    L.append("  THE ANSWER")
    L.append(f"    failed in the first execution        {s['totalFailedInBaseline']:>6}")
    L.append(f"    failed again  (CONFIRMED)            {s['failedAgain']:>6}")
    L.append(f"    passed on re-run (NOT reproduced)    {s['passedOnRerun']:>6}")
    L.append(f"    not re-observed (hop did not run)    {s['notReObserved']:>6}")
    L.append(f"    confirmed reproducible failure rate  {s['confirmedReproducibleRatePctOfReobservedFailures']:>6}%"
             "   of failures that were re-observed")
    L.append(f"    of the non-reproduced, transient-shaped in the baseline: "
             f"{s['ofWhichHadTransientSignature']}")
    L.append("")
    L.append("  THE OTHER DIRECTION - what a failed-only re-run could not have seen")
    L.append(f"    passed before, failed now (NEWLY FAILING) {s['newlyFailing']:>6}")
    L.append(f"    passed both times                         {s['stablePasses']:>6}")
    L.append("")
    L.append("  FULL TRANSITION MATRIX")
    for k, n in a["matrix"].items():
        L.append(f"    {k:<26} {n:>6}")
    L.append("=" * 78)
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("baseline")
    ap.add_argument("rerun")
    ap.add_argument("--json", action="store_true", help="emit the full analysis as JSON")
    ap.add_argument("--write", action="store_true",
                    help="also write the dashboard dataset and a markdown report")
    args = ap.parse_args()

    bd, rd = resolve(args.baseline), resolve(args.rerun)
    for d in (bd, rd):
        if not (d / "results.json").exists():
            sys.exit(f"{d.name} has no results.json - has that run finished?")

    a = analyse(bd, rd)

    if args.json:
        print(json.dumps(a, indent=1))
    else:
        print(render(a))

    if args.write:
        # The dataset carries the counts and a capped sample of each transition; the full lists
        # would make the dashboard payload enormous for no reader benefit.
        slim = {k: v for k, v in a.items() if k != "transitions"}
        slim["transitionSamples"] = {k: v[:50] for k, v in a["transitions"].items()}
        slim["transitionSampleNote"] = ("Each list is capped at 50 rows for the dashboard payload; "
                                        "the full detail is in the report next to the run.")
        OUT_DATA.mkdir(parents=True, exist_ok=True)
        (OUT_DATA / "reproducibility.json").write_text(
            json.dumps(slim, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"\n  wrote {(OUT_DATA / 'reproducibility.json').relative_to(ROOT).as_posix()}")

        rep = rd / "REPRODUCIBILITY.md"
        lines = [f"# Failure reproducibility — {a['rerun']} vs {a['baseline']}", "",
                 f"**Unit:** {a['unit']} · **Generated by:** `{a['generatedBy']}`", "",
                 "```", render(a), "```", "",
                 "## Confirmed reproducible failures (FAIL → FAIL)", "",
                 "| Flow | Hop | Name | Verb | Endpoint | Baseline | Re-run |",
                 "|---|---:|---|---|---|---|---|"]
        for t in a["transitions"].get("FAIL->FAIL", [])[:400]:
            lines.append(f"| {t['flow']} | {t['hop']} | {t['name']} | {t['verb']} | "
                         f"`{t['path']}` | {t['baselineSignature']} | {t['rerunSignature']} |")
        lines += ["", "## Not reproduced (FAIL → PASS)", "",
                  "| Flow | Hop | Name | Endpoint | How it failed in the baseline |",
                  "|---|---:|---|---|---|"]
        for t in a["transitions"].get("FAIL->PASS", []):
            lines.append(f"| {t['flow']} | {t['hop']} | {t['name']} | `{t['path']}` | "
                         f"{t['baselineSignature']} |")
        lines += ["", "## Newly failing (PASS → FAIL)", "",
                  "| Flow | Hop | Name | Endpoint | How it fails now |",
                  "|---|---:|---|---|---|"]
        for t in a["transitions"].get("PASS->FAIL", []):
            lines.append(f"| {t['flow']} | {t['hop']} | {t['name']} | `{t['path']}` | "
                         f"{t['rerunSignature']} |")
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  wrote {rep.relative_to(ROOT).as_posix()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
