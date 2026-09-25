#!/usr/bin/env python3
"""OBJ-010 - re-score a completed run's stored responses under the CURRENT validator.

Why
---
OBJ-010 compares N-1 (2026-07-29_181439) with N. Between the two runs the validator was
corrected, so a raw comparison would measure the scoring change as if it were a product
change. Every one of N-1's 1,868 hops kept its full response body in `evidence/`, so the
old run can be re-judged under the new rules with ZERO HTTP calls.

What is and is not re-judged - this matters for honesty
------------------------------------------------------
Re-computed from the stored response:  L1 http-status · L2 content-type · L3 envelope ·
                                       L4 message-semantics · L7 latency
Carried forward unchanged:             L5 chain-key-extracted · L6 record-exists

L5 and L6 depend on run-time chain state (which id was extracted, which record was then
found), not on the rules that changed, and they cannot be honestly recomputed from a
stored body alone. Carrying them forward is therefore both correct and conservative: the
re-score isolates exactly the rules that were edited.

  python tools/obj010_rescore.py artifacts/runs/2026-07-29_181439
  python tools/obj010_rescore.py <run> --out rescore.json
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chain_runner import ROOT, assess, load_flows                     # noqa: E402

RECOMPUTED = {"http-status", "content-type", "envelope", "message-semantics", "latency"}
CARRIED = {"chain-key-extracted", "record-exists"}


def hop_specs() -> dict:
    """(flow id, hop name) -> hop spec, from the flow definitions on disk.

    The generators are deterministic over APIConfig.java + the payload helpers, so the
    flow set regenerates identically. Any hop we cannot match is REPORTED, never guessed.
    """
    out = {}
    for f in load_flows():
        for i, h in enumerate(f.get("hops", []), 1):
            out[(f.get("id"), i, h.get("name"))] = h
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", help="run folder to re-score")
    ap.add_argument("--out", default=None, help="where to write the JSON (default: "
                                                "<run>/rescore.json)")
    args = ap.parse_args()

    run_dir = Path(args.run)
    if not run_dir.is_absolute():
        run_dir = ROOT / args.run
    results_f = run_dir / "results.json"
    if not results_f.is_file():
        print(f"⛔ {results_f} not found")
        return 2
    ev_dir = run_dir / "evidence"

    data = json.loads(results_f.read_text(encoding="utf-8"))
    specs = hop_specs()

    stats = collections.Counter()
    layer_delta = collections.Counter()
    flows_out = []
    unmatched: list[str] = []

    for fl in data.get("flows", []):
        fid = fl.get("id")
        new_hops = []
        for h in fl.get("hops", []):
            old_checks = h.get("checks", [])
            rec = {"n": h.get("n"), "name": h.get("name"), "path": h.get("path"),
                   "verb": h.get("verb"), "status": h.get("status"),
                   "latency_ms": h.get("latency_ms")}
            if h.get("skipped"):
                rec["skipped"] = h["skipped"]
                rec["checks"] = old_checks
                stats["hops_skipped"] += 1
                new_hops.append(rec)
                continue

            spec = specs.get((fid, h.get("n"), h.get("name")))
            ev_name = h.get("evidence")
            ev = None
            if ev_name and (ev_dir / ev_name).is_file():
                try:
                    ev = json.loads((ev_dir / ev_name).read_text(encoding="utf-8"))
                except Exception:                                     # noqa: BLE001
                    ev = None

            if spec is None or ev is None:
                unmatched.append(f"{fid}#{h.get('n')} {h.get('name')} "
                                 f"(spec={'yes' if spec else 'NO'}, "
                                 f"evidence={'yes' if ev else 'NO'})")
                rec["checks"] = old_checks
                rec["rescored"] = False
                stats["hops_not_rescorable"] += 1
                new_hops.append(rec)
                continue

            res = {"status": ev.get("status"),
                   "content_type": ev.get("content_type") or "",
                   "json": ev.get("response"),
                   "latency_ms": ev.get("latency_ms") or 0}
            fresh = assess(spec, res, ev.get("extracted") or {})

            # splice: recomputed layers from `fresh`, chain-state layers from the original
            merged = [c for c in fresh if c["check"] in RECOMPUTED]
            merged += [c for c in old_checks if c["check"] in CARRIED]
            rec["checks"] = merged
            rec["rescored"] = True
            stats["hops_rescored"] += 1

            oldmap = {c["check"]: c["verdict"] for c in old_checks}
            for c in merged:
                if c["check"] in RECOMPUTED and c["check"] in oldmap:
                    if oldmap[c["check"]] != c["verdict"]:
                        layer_delta[f"{c['check']}: "
                                    f"{oldmap[c['check']]}->{c['verdict']}"] += 1
            new_hops.append(rec)

        old_verdict = fl.get("verdict")
        failed = any(c["verdict"] == "FAIL"
                     for hh in new_hops for c in hh.get("checks", []))
        aborted = old_verdict == "ABORTED"
        new_verdict = "ABORTED" if aborted else ("FAIL" if failed else "PASS")
        stats[f"flow_{new_verdict}"] += 1
        if old_verdict != new_verdict:
            stats[f"flow_verdict_changed_{old_verdict}_to_{new_verdict}"] += 1
        flows_out.append({"id": fid, "title": fl.get("title"),
                          "verdict_original": old_verdict,
                          "verdict_rescored": new_verdict,
                          "hops": new_hops})

    payload = {
        "source_run": run_dir.name,
        "rescored_by": "tools/obj010_rescore.py",
        "network_calls_issued": 0,
        "recomputed_layers": sorted(RECOMPUTED),
        "carried_forward_layers": sorted(CARRIED),
        "stats": dict(stats),
        "layer_verdict_changes": dict(layer_delta),
        "unmatched_hops": unmatched[:200],
        "unmatched_hop_count": len(unmatched),
        "flows": flows_out,
    }
    out = Path(args.out) if args.out else run_dir / "rescore.json"
    out.write_text(json.dumps(payload, indent=1), encoding="utf-8")

    print(f"run                  : {run_dir.name}")
    print(f"HTTP calls issued    : 0")
    print(f"hops re-scored       : {stats['hops_rescored']}")
    print(f"hops not re-scorable : {stats['hops_not_rescorable']} "
          f"(unmatched spec or missing evidence)")
    print(f"hops skipped in run  : {stats['hops_skipped']}")
    print()
    print("flow verdicts after re-score:")
    for k in ("flow_PASS", "flow_FAIL", "flow_ABORTED"):
        if stats[k]:
            print(f"  {k[5:]:<9} {stats[k]}")
    changed = {k: v for k, v in stats.items() if "verdict_changed" in k}
    print(f"\nflow verdict changes : {sum(changed.values())}")
    for k, v in sorted(changed.items()):
        print(f"  {k.replace('flow_verdict_changed_', '')}: {v}")
    print("\nlayer verdict changes (the isolated effect of the rule fix):")
    if layer_delta:
        for k, v in layer_delta.most_common():
            print(f"  {v:>5}  {k}")
    else:
        print("  none")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
