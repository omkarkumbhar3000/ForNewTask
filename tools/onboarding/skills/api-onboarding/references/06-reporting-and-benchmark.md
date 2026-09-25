# Phase 6 — Reporting and benchmarking

**Purpose:** produce evidence a reviewer can verify, and a run-over-run comparison a manager can act on.
**Test of success:** a stranger can pick any single claim in the report and check it against retained evidence.

---

## 1. The run folder

One dated folder per execution, **retained forever**, never overwritten:

```
artifacts/runs/<YYYY-MM-DD_HHMMSS>/
    RUN_REPORT.md        verdicts, coverage, failure detail, exclusions
    results.json         machine-readable, diffable against any other run
    checkpoint.json      resume point
    validation.json      the completion gates, each pass/fail
    evidence/*.json      one file per call: request, response, verdict - redacted
```

| Property | Why it is not optional |
|---|---|
| **Dated folder** | The only reason an N-1 baseline exists at all |
| **Retained forever** | Auto-deleting prior output destroys comparability, and the loss is discovered only when a baseline is needed |
| **Machine-readable results** | A markdown report cannot be diffed or re-scored |
| **Per-call evidence** | Makes a finding verifiable, and makes offline re-scoring possible — see §4 |
| **Redacted at write time** | Evidence files are shared |

One direction of flow: **machinery executes → writes into the run folder.** The run folder never
writes back. That separation is what makes a run reproducible — the machinery is inspectable, the
evidence immutable.

---

## 2. What the run report must contain

| Section | Content |
|---|---|
| Header | Environment, engine, profile, credential source, elapsed, baseline being compared against |
| Outcome | One paragraph a manager can read alone |
| Counts | Planned · executed · passed · failed · **blocked** · **not reached** |
| Per-layer results | Pass rate **per layer**, not one aggregate |
| Per-module results | So an owner can find their own area |
| Failures | Grouped by cause, with an evidence path per group |
| **Exclusions** | Every withheld item, its class, its count, its reason |
| Performance | Mean · median · p95, split read vs write |
| Environment stability | Pauses, minutes lost |
| Provenance | Every artifact path, so each figure is traceable |

### Three reporting rules that change what the numbers mean

**Report at the step level, not the flow level.** One failing hop fails an entire chain, so
flow-level percentages punish long chains and understate reality. On the reference project the same
run reads as **9.2%** at flow level and **64.2%** at case level. Both are arithmetically true; only
one is informative. Quote the case rate and show the flow rate beside it.

**Per-layer results are the point.** A run where the status check passes 1,688 times and the
persistence check passes twice is not a passing run, and only a layered result makes that visible.
An aggregate pass rate hides exactly the finding the layered model exists to expose.

**Distinguish four negative outcomes.** *Failed* (executed, assertion failed) · *Blocked* (withheld
deliberately, with a reason) · *Not reached* (an earlier hop stopped the chain) · *Aborted* (the run
gave up). Collapsing these into "not passed" makes the report unusable for deciding what to do next.

---

## 3. The benchmark — N-1 versus N

A single run is a snapshot. The value compounds when runs are comparable.

| Metric | Note |
|---|---|
| Flows · cases planned · executed | |
| Passed · failed · **blocked** · not reached | Blocked split by withheld-at-generation vs withheld-at-call |
| Case-level success rate | The headline. Flow-level shown beside it, labelled |
| Distinct endpoints reached | The coverage figure that matters |
| Newly added cases · retired cases | Explains a moved denominator |
| **Fixed** (fail → pass) · **new failures** (pass → fail) | Computed on the *comparable subset* only |
| Latency mean · median · p95 | |
| Elapsed · downtime pauses · minutes lost | |
| Credential requests | Should be 0 or 1 |

⛔ **A metric absent from N-1 is reported as `N/A`, never dropped.** Dropping it makes the comparison
look cleaner than the evidence supports.

⚠️ **Compare like with like.** If N added dimensions that N-1 lacked, the aggregate rates are not
comparable and saying so is part of the report. Compute the *comparable subset* — same endpoint, same
verb, same scenario — and quote both: the subset proves whether the product moved, the aggregate shows
whether coverage grew. On the reference project the comparable subset was 858 cases with 856
unchanged, one fixed and one regressed, while total coverage tripled. Those two facts together are the
finding; either alone is misleading.

---

## 4. When the validator changes between runs

A corrected validator makes N and N-1 incomparable — unless every response body was retained. Then
the fix is better than a caveat: **re-score the baseline offline, with zero HTTP calls.**

On the reference project re-scoring all 1,868 baseline hops under the corrected validator changed
**nothing** — same verdicts before and after. Two things followed from that: the benchmark carried no
caveat, and the generators were proven deterministic, since 1,868 of 1,868 hops matched their
regenerated specification a week later. Report three columns where this applies: *N-1 as published* ·
*N-1 re-scored* · *N*.

This is the single strongest argument for retaining per-call evidence. It converts "we changed the
scoring, so the comparison is soft" into a measurement.

---

## 5. Management summary

Separate document, one page, no implementation detail:

| Section | Content |
|---|---|
| Outcome | One paragraph, plus an explicit trend verdict |
| Headline table | N-1 vs N, deltas marked |
| Why the aggregate moved | Coverage growth versus product change, separated |
| Findings | What this run found that the previous one structurally could not |
| Regressions | On the comparable subset, named |
| Cost | Elapsed, and where the time actually went |
| Recommendations | Prioritised, each with an owner |
| Provenance | Paths, so any figure can be checked |

**Lead with what the run found, not with how it ran.** A finding that 19 endpoints accept an invalid
credential is what earns the next round of investment; the pass rate is context for it.

---

## 6. Exit gate

| ✅ | Condition |
|---|---|
| ☐ | Every planned case is accounted for: executed, blocked, or not-reached — the arithmetic closes |
| ☐ | Every exclusion carries a reason |
| ☐ | Every figure in the report is traceable to a retained artifact |
| ☐ | Rates are quoted at case level, with flow level labelled separately |
| ☐ | Metrics absent from the baseline are `N/A`, not omitted |
| ☐ | The management summary states the trend in one line |
