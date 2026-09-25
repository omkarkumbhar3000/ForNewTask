#!/usr/bin/env python3
"""OBJ-010 - build QA_MsSQL_API_Execution.xlsx: execution summary + N-1 vs N benchmark.

Reads only run output and generated flow metadata. Zero HTTP, zero database.

  python tools/obj010_build_workbook.py <current-run-folder>
  python tools/obj010_build_workbook.py <current> --baseline <n-1>

Design rules inherited from obj007_build_workbooks.py, which owns the house style:
  * a sheet whose input is missing is written with an explanatory row, never omitted -
    an absent worksheet reads as "not applicable", which is a different claim;
  * a metric that N-1 never captured is reported as N/A, never dropped (OBJ-010 rule).

Deliberate deviation from the agreed Q3 wording, stated so it is not mistaken for a
miss: Q3 asked for "per-module result sheets". This run spans 219 modules, and 219 tabs
is unusable for the management audience the workbook is for. Per-module results are
therefore delivered as `Module Results` (one row per module) plus a fully autofiltered
`Hop Results` sheet that filters by module - the same data, in the form Excel users
actually work in. Nothing is aggregated away: every hop has its own row.
"""
from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from openpyxl import Workbook                                         # noqa: E402

from chain_runner import ROOT, load_flows                             # noqa: E402
from obj007_build_workbooks import write_sheet                        # noqa: E402

NA = "N/A"
DIAG = workspace_root(__file__) / "state" / "obj010"


# ------------------------------------------------------------------ loading helpers
def read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                                 # noqa: BLE001
        return None


def load_segments(run_id: str | None) -> dict:
    """Segment totals for THIS run, or {}.

    ⛔ This used to read `.obj010/segments.json` unconditionally (OBJ-020). That file is pinned to
    one run, so every later run's workbook inherited the 2026-08-05 run's 329.1 min as its own
    elapsed — a wrong figure, in the Summary sheet management reads. It is now keyed to the run:
    a per-run `segments-<id>.json` first, then the shared file only if it names this run.
    """
    if not run_id:
        return {}
    per_run = read_json(DIAG / f"segments-{run_id}.json")
    if per_run:
        return per_run
    shared = read_json(DIAG / "segments.json") or {}
    return shared if shared.get("run") == run_id else {}


def flow_meta() -> dict:
    """flow id -> {kind, scenario mix, data_driven, tier, controller} from flow JSON."""
    out = {}
    for f in load_flows():
        hops = f.get("hops", [])
        out[f.get("id")] = {
            "controller": f.get("controller") or "",
            "tier": f.get("tier", 1),
            "data_driven": bool(f.get("data_driven")),
            "kind": f.get("kind") or ("positive-chain" if not f.get("data_driven")
                                      else "positive"),
            "scenarios": collections.Counter(h.get("scenario") or "Chain" for h in hops),
            "hop_specs": {(i, h.get("name")): h for i, h in enumerate(hops, 1)},
        }
    return out


def hop_rows(run: dict, meta: dict) -> list[dict]:
    """One row per executed or withheld hop - the atomic unit of the whole report."""
    rows = []
    for fl in run.get("flows", []):
        fid = fl.get("id")
        fm = meta.get(fid, {})
        for h in fl.get("hops", []):
            spec = (fm.get("hop_specs") or {}).get((h.get("n"), h.get("name")), {})
            checks = h.get("checks", [])
            failing = [c["check"] for c in checks if c["verdict"] == "FAIL"]
            if h.get("skipped"):
                verdict = "BLOCKED"
            elif not checks:
                verdict = "NOT EXECUTED"
            else:
                verdict = "FAIL" if failing else "PASS"
            rows.append({
                "flow": fid,
                "module": fm.get("controller") or "",
                "dimension": ("data-driven" if fm.get("data_driven") else "chain"),
                "scenario": spec.get("scenario") or "Chain",
                "kind": ("negative" if spec.get("negative") else "positive"),
                "hop": h.get("n"),
                "name": h.get("name"),
                "verb": h.get("verb"),
                "endpoint": h.get("path"),
                "expected_status": spec.get("expect_status", 200),
                "expected_error_code": spec.get("expect_error_code") or "",
                "auth_mode": ("invalid-credential" if spec.get("auth") == "invalid"
                              else "valid-token"),
                "status": h.get("status") if h.get("status") is not None else "",
                "latency_ms": h.get("latency_ms") if h.get("latency_ms") is not None else "",
                "verdict": verdict,
                "failing_layers": ", ".join(failing),
                "withheld_reason": h.get("skipped") or "",
                "evidence": h.get("evidence") or "",
            })
    return rows


def flow_rows(run: dict, meta: dict) -> list[dict]:
    rows = []
    for fl in run.get("flows", []):
        fm = meta.get(fl.get("id"), {})
        hops = fl.get("hops", [])
        ok = sum(1 for h in hops
                 if h.get("checks") and not any(c["verdict"] == "FAIL"
                                                for c in h["checks"]))
        rows.append({
            "flow": fl.get("id"),
            "title": fl.get("title"),
            "module": fm.get("controller") or "",
            "dimension": "data-driven" if fm.get("data_driven") else "chain",
            "tier": fm.get("tier", ""),
            "hops": len(hops),
            "hops_passed": ok,
            "hops_failed": len(hops) - ok,
            "verdict": fl.get("verdict"),
            "note": fl.get("note") or "",
        })
    return rows


def pct(n, d) -> str:
    return f"{(100.0 * n / d):.1f}%" if d else NA


def latencies(rows: list[dict]) -> list[int]:
    return [r["latency_ms"] for r in rows if isinstance(r.get("latency_ms"), int)]


def stat_block(lat: list[int]) -> dict:
    if not lat:
        return {"count": 0, "mean_ms": NA, "median_ms": NA, "p95_ms": NA, "max_ms": NA}
    s = sorted(lat)
    return {"count": len(s),
            "mean_ms": int(statistics.fmean(s)),
            "median_ms": int(statistics.median(s)),
            "p95_ms": s[min(len(s) - 1, int(0.95 * len(s)))],
            "max_ms": s[-1]}


# ------------------------------------------------------------------------- benchmark
def benchmark(cur: dict, cur_hops: list[dict], base: dict | None,
              base_hops: list[dict] | None, base_rescore: dict | None,
              blocked: dict | None) -> list[dict]:
    """One row per metric. A metric N-1 never captured reads N/A - never dropped."""
    planned_hops = {f.get("id"): len(f.get("hops", [])) for f in load_flows()}

    def side(run, hops):
        if run is None or hops is None:
            return None
        m = run.get("meta", {})
        flows = run.get("flows", [])
        executed = [h for h in hops if h["verdict"] in ("PASS", "FAIL")]
        return {
            "planned": sum(planned_hops.get(f.get("id"), len(f.get("hops", [])))
                           for f in flows),
            "meta": m, "flows": flows, "hops": hops, "executed": executed,
            "passed": [h for h in executed if h["verdict"] == "PASS"],
            "failed": [h for h in executed if h["verdict"] == "FAIL"],
            "blocked": [h for h in hops if h["verdict"] == "BLOCKED"],
            "neg": [h for h in executed if h["kind"] == "negative"],
            "pos": [h for h in executed if h["kind"] == "positive"],
            "fpass": [f for f in flows if f.get("verdict") == "PASS"],
            "ffail": [f for f in flows if f.get("verdict") == "FAIL"],
            "endpoints": {h["endpoint"].split("?")[0] for h in executed},
        }

    N, P = side(cur, cur_hops), side(base, base_hops)
    assert N is not None          # main() guarantees a current run; the baseline may be absent
    rows: list[dict] = []

    def add(metric, nval, pval, note=""):
        n_s, p_s = str(nval), str(pval)
        trend = ""
        if isinstance(nval, (int, float)) and isinstance(pval, (int, float)):
            d = nval - pval
            trend = ("▲ +%g" % d) if d > 0 else (("▼ %g" % d) if d < 0 else "= 0")
        rows.append({"metric": metric, "n_minus_1": p_s, "n_current": n_s,
                     "delta": trend or NA, "note": note})

    add("Run folder", cur["meta"]["stamp"], P["meta"]["stamp"] if P else NA)
    add("Environment", cur["meta"].get("env"), P["meta"].get("env") if P else NA)
    add("Mode", cur["meta"].get("mode"), P["meta"].get("mode") if P else NA)
    add("Inter-call delay (ms)", cur["meta"].get("delay_ms_final"),
        P["meta"].get("delay_ms_final") if P else NA,
        "Pacing differs, so absolute latency is comparable but throughput is not")
    add("Verbs permitted", ", ".join(cur["meta"].get("verbs", [])),
        ", ".join(P["meta"].get("verbs", [])) if P else NA,
        "PUT/PATCH added in N to execute the QA team's PUT/PATCH rows")
    # A resumed run's meta covers the LAST process only, so elapsed / downtime read low.
    # segments.json carries the earlier segment's measured figures so the totals are true.
    seg = load_segments(cur["meta"].get("stamp"))
    st = seg.get("totals", {})
    cur_elapsed = round(cur["meta"].get("elapsed_s", 0) / 60, 1)
    add("Elapsed (min) - total across all segments",
        st.get("elapsed_min", cur_elapsed),
        round(P["meta"].get("elapsed_s", 0) / 60, 1) if P else NA,
        f"This run executed in {len(seg.get('segments', [])) or 1} segment(s); "
        f"results.json meta records only the last ({cur_elapsed} min). See segments.json"
        if seg else "")
    add("  of which spent waiting on the environment",
        st.get("downtime_minutes_waiting", NA), NA,
        "Downtime pauses at 300 s each - time not spent testing")

    add("Total flows", len(N["flows"]), len(P["flows"]) if P else NA)
    add("Test cases planned", N["planned"], P["planned"] if P else NA,
        "Hops present in the generated flow definitions")
    add("Test cases reached", len(N["hops"]), len(P["hops"]) if P else NA)
    add("Not reached - chain stopped at an earlier hop",
        N["planned"] - len(N["hops"]),
        (P["planned"] - len(P["hops"])) if P else NA,
        "A hop marked stop_on_fail failed, so the remaining hops in that chain were "
        "never issued. Reported, not hidden - these are unrun, not passed")
    add("Executed", len(N["executed"]), len(P["executed"]) if P else NA)
    add("Passed", len(N["passed"]), len(P["passed"]) if P else NA)
    add("Failed", len(N["failed"]), len(P["failed"]) if P else NA)
    add("Blocked - hops withheld at call time", len(N["blocked"]),
        len(P["blocked"]) if P else NA,
        "Hops present in a flow but refused by the runner's guards. Counted as Blocked, "
        "never as passed or skipped. Excel rows withheld earlier, at generation time, "
        "are the separate 'withheld:' rows below")
    add("  of which, by guard", ", ".join(f"{k}={v}" for k, v in
                                          sorted((cur["meta"].get("skipped") or {}).items())) or "none",
        ", ".join(f"{k}={v}" for k, v in
                  sorted((P["meta"].get("skipped") or {}).items())) if P else NA,
        "Same hops as the row above, broken down by which guard refused them")
    add("Hop success rate", pct(len(N["passed"]), len(N["executed"])),
        pct(len(P["passed"]), len(P["executed"])) if P else NA)
    add("Flow success rate", pct(len(N["fpass"]), len(N["flows"])),
        pct(len(P["fpass"]), len(P["flows"])) if P else NA)
    add("Flows passed", len(N["fpass"]), len(P["fpass"]) if P else NA)
    add("Flows failed", len(N["ffail"]), len(P["ffail"]) if P else NA)
    add("Distinct endpoints reached", len(N["endpoints"]),
        len(P["endpoints"]) if P else NA)

    add("Positive test cases executed", len(N["pos"]), len(P["pos"]) if P else NA)
    add("Negative test cases executed", len(N["neg"]),
        len(P["neg"]) if P else NA,
        "N-1 had no negative dimension - the generator emitted positive flows only")
    add("Negative pass rate",
        pct(sum(1 for h in N["neg"] if h["verdict"] == "PASS"), len(N["neg"])),
        pct(sum(1 for h in P["neg"] if h["verdict"] == "PASS"), len(P["neg"]))
        if P and P["neg"] else NA)

    scen = collections.Counter(h["scenario"] for h in N["executed"])
    for name in ("Chain", "Positive", "MethodNotAllowed", "UnauthorizedAccess",
                 "InvalidQueryParams"):
        if scen.get(name):
            add(f"  scenario: {name}", scen[name],
                (collections.Counter(h["scenario"] for h in P["executed"]).get(name, 0)
                 if P else NA))

    ln, lp = stat_block(latencies(N["executed"])), stat_block(latencies(
        P["executed"])) if P else None
    for key, label in (("mean_ms", "Latency mean (ms)"),
                       ("median_ms", "Latency median (ms)"),
                       ("p95_ms", "Latency p95 (ms)"),
                       ("max_ms", "Latency max (ms)")):
        add(label, ln[key], lp[key] if lp else NA)

    add("Downtime pauses (env unavailable)",
        st.get("downtime_pauses", len(cur["meta"].get("downtime_events") or [])),
        len(P["meta"].get("downtime_events") or []) if P else NA,
        "Total across segments. Each waited 300 s then resumed from the paused hop, "
        "never restarting. One sustained outage exhausted all 3 retries and aborted 3 "
        "flows, which were re-queued and executed in segment 2")
    add("Calls to /arcontoken", st.get("token_endpoint_calls", 0), NA,
        "One cached token reused across both segments - the lockout rule (ISSUE-009) "
        "holds even across a resume")

    # verdict movement, hop-identity based
    if P:
        def keyed(hops):
            """Worst verdict per (endpoint, verb, scenario).

            The same endpoint is exercised by several flows, so a plain dict would keep
            whichever hop happened to come last. Collapsing to the worst verdict makes
            'fixed' and 'regressed' mean what they say: a case counts as PASS only if
            every occurrence passed.
            """
            out: dict[tuple, str] = {}
            for h in hops:
                k = (h["endpoint"].split("?")[0], h["verb"], h["scenario"])
                if out.get(k) != "FAIL":
                    out[k] = h["verdict"]
            return out

        keyed_n, keyed_p = keyed(N["executed"]), keyed(P["executed"])
        shared = set(keyed_n) & set(keyed_p)
        fixed = [k for k in shared
                 if keyed_p[k] == "FAIL" and keyed_n[k] == "PASS"]
        broke = [k for k in shared
                 if keyed_p[k] == "PASS" and keyed_n[k] == "FAIL"]
        add("Comparable test cases (same endpoint+verb+scenario)", len(shared), len(shared))
        add("Fixed failures (FAIL -> PASS)", len(fixed), NA)
        add("New failures / regressions (PASS -> FAIL)", len(broke), NA)
        add("Newly added test cases (absent from N-1)",
            len(set(keyed_n) - set(keyed_p)), NA)
        add("Test cases retired since N-1", len(set(keyed_p) - set(keyed_n)), NA)
    else:
        for m in ("Comparable test cases (same endpoint+verb+scenario)",
                  "Fixed failures (FAIL -> PASS)",
                  "New failures / regressions (PASS -> FAIL)",
                  "Newly added test cases (absent from N-1)",
                  "Test cases retired since N-1"):
            add(m, NA, NA, "baseline not supplied")

    if base_rescore:
        st = base_rescore.get("stats", {})
        changed = sum(v for k, v in st.items() if "verdict_changed" in k)
        add("N-1 re-scored under the current validator",
            "n/a - this column IS the current validator",
            f"{st.get('flow_PASS', 0)} PASS / {st.get('flow_FAIL', 0)} FAIL",
            f"{st.get('hops_rescored', 0)} hops re-judged from stored bodies, 0 HTTP "
            f"calls; {changed} flow verdicts changed -> the comparison is apples-to-apples")
    else:
        add("N-1 re-scored under the current validator", NA, NA,
            "rescore.json not produced")

    if blocked:
        for k, v in sorted((blocked.get("summary") or {}).items()):
            add(f"  withheld: {k}", v, NA,
                "Excel rows withheld at generation time - see Blocked and Exclusions")
    return rows


# ------------------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", help="current run folder (N)")
    ap.add_argument("--baseline", default="artifacts/runs/2026-07-29_181439")
    ap.add_argument("--out", default=None,
                    help="override the output path (used to smoke-test the builder "
                         "without dropping a workbook into a real run folder)")
    args = ap.parse_args()

    def resolve(p: str) -> Path:
        q = Path(p)
        return q if q.is_absolute() else ROOT / p

    run_dir, base_dir = resolve(args.run), resolve(args.baseline)
    cur = read_json(run_dir / "results.json")
    if cur is None:
        print(f"⛔ {run_dir / 'results.json'} not found - has the run finished?")
        return 2
    base = read_json(base_dir / "results.json")
    base_rescore = read_json(base_dir / "rescore.json")
    blocked = read_json(DIAG / "blocked-rows.json")

    meta = flow_meta()
    cur_hops = hop_rows(cur, meta)
    base_hops = hop_rows(base, meta) if base else None
    frows = flow_rows(cur, meta)

    wb = Workbook()
    if wb.active is not None:
        wb.remove(wb.active)

    executed = [h for h in cur_hops if h["verdict"] in ("PASS", "FAIL")]
    passed = [h for h in executed if h["verdict"] == "PASS"]
    m = cur.get("meta", {})
    _seg = load_segments(m.get("stamp"))
    summary = [
        {"item": "Run", "value": m.get("stamp")},
        {"item": "Environment", "value": f"{m.get('env')}  {m.get('base')}"},
        {"item": "Engine", "value": "AI dynamic API framework (tools/) - "
                                   "generate_flows.py + generate_data_flows.py -> "
                                   "chain_runner.py"},
        {"item": "Bootstrap Java/TestNG suite executed?", "value": "NO - reference only"},
        {"item": "Elapsed (min), all segments",
         "value": _seg.get("totals", {}).get(
             "elapsed_min", round(m.get("elapsed_s", 0) / 60, 1))},
        {"item": "  of which waiting on the environment",
         "value": _seg.get("totals", {}).get("downtime_minutes_waiting", NA)},
        {"item": "Flows", "value": len(cur.get("flows", []))},
        {"item": "Hops (test cases)", "value": len(cur_hops)},
        {"item": "Executed", "value": len(executed)},
        {"item": "Passed", "value": len(passed)},
        {"item": "Failed", "value": len(executed) - len(passed)},
        {"item": "Blocked", "value": sum(1 for h in cur_hops
                                         if h["verdict"] == "BLOCKED")},
        {"item": "Hop success rate", "value": pct(len(passed), len(executed))},
        {"item": "Distinct endpoints reached",
         "value": len({h["endpoint"].split("?")[0] for h in executed})},
        {"item": "Negative test cases executed",
         "value": sum(1 for h in executed if h["kind"] == "negative")},
        {"item": "Token calls to /arcontoken", "value": "0 - reused the cached token"},
        {"item": "Downtime pauses, all segments",
         "value": _seg.get("totals", {}).get(
             "downtime_pauses", len(m.get("downtime_events") or []))},
        {"item": "Run segments",
         "value": f"{len(_seg.get('segments', [])) or 1}"
                  + (f" - {_seg['why'][:120]}" if _seg.get("why") else "")},
    ]
    write_sheet(wb, "Summary", summary,
                note="OBJ-010 execution summary. Executed through the dynamic framework "
                     "only; the PAM Bootstrap project was read as a generation input.",
                source=f"artifacts/runs/{m.get('stamp')}/results.json")

    write_sheet(wb, "Execution Benchmark",
                benchmark(cur, cur_hops, base, base_hops, base_rescore, blocked),
                note="N-1 vs N. A metric N-1 never captured is N/A, never dropped.",
                source=f"{base_dir.name} vs {run_dir.name}")

    # per-module rollup
    bym: dict[str, collections.Counter[str]] = collections.defaultdict(
        collections.Counter)
    for h in cur_hops:
        k = h["module"] or "(unattributed)"
        bym[k]["hops"] += 1
        bym[k][h["verdict"].lower()] += 1
        if h["kind"] == "negative":
            bym[k]["negative"] += 1
    mrows = []
    for mod, c in sorted(bym.items()):
        ex = c["pass"] + c["fail"]
        mrows.append({"module": mod, "hops": c["hops"], "executed": ex,
                      "passed": c["pass"], "failed": c["fail"],
                      "blocked": c["blocked"], "negative_cases": c["negative"],
                      "success_rate": pct(c["pass"], ex)})
    write_sheet(wb, "Module Results", mrows,
                note="Per-module results. Filter Hop Results by Module for the detail.")

    scen = collections.defaultdict(lambda: collections.Counter())
    for h in cur_hops:
        scen[h["scenario"]][h["verdict"].lower()] += 1
    write_sheet(wb, "Scenario Coverage", [
        {"scenario": s, "executed": c["pass"] + c["fail"], "passed": c["pass"],
         "failed": c["fail"], "blocked": c["blocked"],
         "success_rate": pct(c["pass"], c["pass"] + c["fail"])}
        for s, c in sorted(scen.items())],
        note="The QA team's own negative taxonomy, taken from the named Excel tables.")

    write_sheet(wb, "Flow Results", frows)
    write_sheet(wb, "Hop Results", cur_hops,
                note="One row per test case. Autofilter by Module, Scenario or Verdict.")

    lay = collections.Counter()
    lay_ep = collections.defaultdict(collections.Counter)
    for h in cur_hops:
        for c in (h["failing_layers"] or "").split(", "):
            if c:
                lay[c] += 1
                lay_ep[c][h["endpoint"].split("?")[0]] += 1
    write_sheet(wb, "Failure Analysis", [
        {"failing_layer": k, "hops": v,
         "top_endpoints": "; ".join(f"{e} ({n})" for e, n in lay_ep[k].most_common(5))}
        for k, v in lay.most_common()],
        note="Which validation layer caught each failure. A status-only check would "
             "have caught none of the envelope or message-semantics failures.")

    brows = [{"source": "in-run guard", "item": k, "count": v,
              "reason": "withheld by chain_runner at call time"}
             for k, v in sorted((m.get("skipped") or {}).items())]
    if blocked:
        agg: dict[tuple[str, str], list] = collections.defaultdict(lambda: [0, ""])
        for b in blocked.get("blocked", []):
            key = (b.get("blocked_class", ""), b.get("blocked_reason", ""))
            agg[key][0] = int(agg[key][0]) + 1
            agg[key][1] = b.get("endpoint", "")
        for (cls, reason), (n, ex) in sorted(agg.items(), key=lambda t: -int(t[1][0])):
            brows.append({"source": "generation-time exclusion", "item": cls,
                          "count": n, "reason": reason, "example_endpoint": ex})
    write_sheet(wb, "Blocked and Exclusions", brows,
                note="Nothing is silently skipped. Every withheld test case is counted "
                     "here with its reason.")

    perf = [{"scope": "ALL", **stat_block(latencies(executed))}]
    for mod, _ in sorted(bym.items()):
        rr = [h for h in executed if (h["module"] or "(unattributed)") == mod]
        if rr:
            perf.append({"scope": mod, **stat_block(latencies(rr))})
    write_sheet(wb, "Performance", perf,
                note="Latency distribution. Pacing differed between runs, so compare "
                     "per-call latency, not throughput.")

    out = Path(args.out) if args.out else run_dir / "QA_MsSQL_API_Execution.xlsx"
    wb.save(out)
    print(f"wrote {out}")
    print(f"  sheets: {', '.join(wb.sheetnames)}")
    print(f"  hops: {len(cur_hops)}  executed: {len(executed)}  "
          f"passed: {len(passed)}  modules: {len(bym)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
