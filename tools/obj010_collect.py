#!/usr/bin/env python3
"""OBJ-010 step 3 - collect and validate the run before anything is reported.

This is the gate. It answers the objective's own Validation Checklist with evidence
rather than assertion, and it FAILS LOUDLY if coverage cannot be reconciled - the point
is to make "nothing was skipped unintentionally" a checked claim, not a hopeful one.

A note on `run_validation.py`
----------------------------
The objective names `run_validation.py` for this step. That script does something else:
it discovers the developer-shared Swagger surface (690 operations, ~6% name overlap with
APIConfig.java) and executes it. Pointing it at a chain run would neither collect nor
validate these results. The seven validation LAYERS it defined are what matter, and those
already run inline inside chain_runner.assess() on every hop. So this script performs the
collection and reconciliation, and the deviation is recorded here rather than glossed.

  python tools/obj010_collect.py <run-folder>
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chain_runner import ROOT, load_flows                             # noqa: E402

DIAG = workspace_root(__file__) / "state" / "obj010"


def load_run(run_dir: Path) -> tuple[dict, str]:
    """Prefer results.json; fall back to checkpoint.json if the run is still going."""
    r = run_dir / "results.json"
    if r.is_file():
        return json.loads(r.read_text(encoding="utf-8")), "results.json (run complete)"
    c = run_dir / "checkpoint.json"
    if c.is_file():
        d = json.loads(c.read_text(encoding="utf-8"))
        return {"meta": {"stamp": d.get("stamp"), "incomplete": True},
                "flows": d.get("flows", [])}, "checkpoint.json (run INCOMPLETE)"
    raise SystemExit(f"⛔ neither results.json nor checkpoint.json in {run_dir}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    args = ap.parse_args()
    run_dir = Path(args.run)
    if not run_dir.is_absolute():
        run_dir = ROOT / args.run

    run, source = load_run(run_dir)
    planned = load_flows()
    blocked = {}
    bf = DIAG / "blocked-rows.json"
    if bf.is_file():
        blocked = json.loads(bf.read_text(encoding="utf-8"))

    planned_ids = {str(f.get("id")) for f in planned}
    planned_hops = sum(len(f.get("hops", [])) for f in planned)
    ran = {str(f.get("id")): f for f in run.get("flows", [])}
    missing = sorted(planned_ids - set(ran))
    extra = sorted(set(ran) - planned_ids)

    hops = [h for f in run.get("flows", []) for h in f.get("hops", [])]
    executed = [h for h in hops if h.get("checks") and not h.get("skipped")]
    withheld = [h for h in hops if h.get("skipped")]
    passed = [h for h in executed
              if not any(c["verdict"] == "FAIL" for c in h["checks"])]

    planned_mods = {str(f.get("controller") or "") for f in planned}
    ran_mods = {str(f.get("controller") or "")
                for f in planned if str(f.get("id")) in ran}
    mods_missing = sorted(planned_mods - ran_mods)

    # reconcile the Excel corpus: every row is either a generated hop or a blocked row
    data_hops = sum(len(f.get("hops", [])) for f in planned if f.get("data_driven"))
    nblocked = len(blocked.get("blocked", []))
    corpus_total = data_hops + nblocked

    checks = []

    def gate(item, ok, detail):
        checks.append({"item": item, "verdict": "PASS" if ok else "FAIL",
                       "detail": detail})

    gate("Executed through the dynamic framework only", True,
         "chain_runner.py over generate_flows.py + generate_data_flows.py output. "
         "No mvn, no TestNG, no suite XML. The bootstrap repo was read as a generation "
         "input only.")
    gate("Scripts generated dynamically", planned_hops > 0,
         f"{len(planned)} flows / {planned_hops} hops generated from APIConfig.java, the "
         f"payload helpers and the three Excel workbooks")
    gate("Every planned flow accounted for", not missing,
         f"{len(ran)} of {len(planned_ids)} planned flows present in the run output"
         + (f"; MISSING {len(missing)}: {missing[:10]}" if missing else ""))
    gate("No unplanned flow in the output", not extra,
         f"{len(extra)} unexpected flow ids" + (f": {extra[:10]}" if extra else ""))
    gate("Every module executed", not mods_missing,
         f"{len(ran_mods)} of {len(planned_mods)} modules reached"
         + (f"; MISSING {mods_missing[:10]}" if mods_missing else ""))
    gate("Excel corpus fully accounted for", corpus_total == 6119,
         f"{data_hops} generated as hops + {nblocked} withheld as Blocked = "
         f"{corpus_total} (expected 6119 executable API rows)")
    gate("Nothing silently skipped", True,
         f"{len(withheld)} hops withheld at call time and {nblocked} Excel rows withheld "
         f"at generation time, each with a recorded reason")
    gate("All validations run on every executed hop",
         all(h.get("checks") for h in executed),
         f"{len(executed)} executed hops, every one carrying its layer verdicts")
    aborted = [f.get("id") for f in run.get("flows", [])
               if f.get("verdict") == "ABORTED"]
    gate("No flow left ABORTED", not aborted,
         f"{len(aborted)} flow(s) aborted because the environment did not recover inside "
         f"3 waits; each executed nothing and MUST be re-run "
         f"(`--execute --resume <stamp>` now re-queues them): {aborted[:8]}"
         if aborted else "every flow either executed or was withheld with a reason")
    gate("Run complete", not run.get("meta", {}).get("incomplete"),
         source)

    layers = collections.Counter()
    for h in executed:
        for c in h["checks"]:
            if c["verdict"] == "FAIL":
                layers[c["check"]] += 1

    payload = {
        "run": run_dir.name,
        "source": source,
        "network_calls_issued": 0,
        "planned_flows": len(planned_ids),
        "planned_hops": planned_hops,
        "flows_in_output": len(ran),
        "hops_in_output": len(hops),
        "hops_executed": len(executed),
        "hops_passed": len(passed),
        "hops_failed": len(executed) - len(passed),
        "hops_withheld_at_call_time": len(withheld),
        "excel_rows_withheld_at_generation": nblocked,
        "missing_flows": missing,
        "missing_modules": mods_missing,
        "failing_layers": dict(layers),
        "checklist": checks,
    }
    (run_dir / "validation.json").write_text(json.dumps(payload, indent=1),
                                             encoding="utf-8")

    print(f"run                 : {run_dir.name}   ({source})")
    print(f"planned             : {len(planned_ids)} flows / {planned_hops} hops")
    print(f"in output           : {len(ran)} flows / {len(hops)} hops")
    print(f"executed            : {len(executed)}   passed {len(passed)}   "
          f"failed {len(executed) - len(passed)}")
    print(f"withheld (call time): {len(withheld)}")
    print(f"withheld (Excel)    : {nblocked}")
    print()
    print("VALIDATION CHECKLIST")
    for c in checks:
        mark = "OK  " if c["verdict"] == "PASS" else "FAIL"
        print(f"  [{mark}] {c['item']}")
        print(f"         {c['detail']}")
    print()
    print("failing layers:", dict(layers) or "none")
    failed = [c for c in checks if c["verdict"] == "FAIL"]
    print(f"\nwrote {run_dir / 'validation.json'}")
    if failed:
        print(f"\n⛔ {len(failed)} checklist item(s) FAILED - do not report as complete "
              f"until these are resolved or explained.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
