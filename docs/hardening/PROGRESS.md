# Hardening review — live progress record

> **Purpose.** This file exists so the review is a *continuable* activity. It records what has
> been done, what is in flight and what is left, precisely enough that a later session (or a
> different engineer) can resume without redoing finished work. The consolidated report lives
> beside it in [`README.md`](README.md); this file is the working state behind it.

**Started:** 2026-09-22 · **Scope:** the whole `Jira RCA/` folder · **Status:** ✅ **COMPLETE** for
everything inside this copy's authority; four items left open by design, each listed with the exact
decision needed in [`README.md`](README.md) §F.

## Baseline

Committed state = `cea4352`. Pre-change copies of the four report markdowns were taken from
`HEAD` before anything was regenerated, so every "before vs after" below is a real diff and not
a recollection.

## Ledger

| # | Item | State | Evidence |
|---|---|---|---|
| 1 | PAMIT §12 `Affected Milestone` published 100% `Not set` — `normalise()` never emitted `customfield_10092` | **FIXED + VERIFIED** | `jira_analysis_2026.py`; independent recount from the raw snapshot: 4,523/5,740 populated (78.8%) |
| 2 | CI sub-task count counted parent-presence, publishing 4,241 where 1,443 exist | **FIXED + VERIFIED** | `ci_analysis_2026.py`; `issuetype.subtask` and `issuetype.name` both give 1,443; 2,798 Epic children were swept in |
| 3 | PAMIT §12 footnote claimed 5,832 "milestone assignments"; only 4,615 exist — the 1,217 unpopulated tickets were counted as assignments | **FIXED + VERIFIED** | `multi_counter()` now shared by components / fix versions / milestones; §6 output provably unchanged |
| 4 | §11 and §12 stated no coverage, so an assignment count could not be told from a ticket count (`D46`) | **FIXED** | `coverage_line()`; both sections now state populated subset, assignments and distinct values |
| 5 | `--offline` silently fell through to a **live Jira fetch** when the snapshot was absent, and overwrote it | **FIXED + TESTED** | both census generators now exit 2 and name the path; tested by hiding each snapshot and restoring it |
| 6 | `main()` return codes were discarded by a bare `main()` call | **FIXED** | both generators now `sys.exit(main() or 0)` |
| 7 | Reports named no source data — untraceable to the snapshot they were built from | **FIXED** | `snapshot_provenance()` in `pamit_fmt.py`; header now carries filename + sha256; the validator recomputes it |
| 8 | No independent validation existed; `OBJ-030`'s gates could not detect a correctly-implemented, wrongly-named rule | **ADDED** | `tools/jira/validate_analysis.py` — 55 checks, all passing; proven to fail against the pre-fix reports |
| 9 | `tools/requirements.txt` omitted `python-docx` and misattributed `jsonschema`; counts and Python version stale | **FIXED** | re-censused by counting import lines across `tools/` |
| 10 | No preflight / health check; environment problems surfaced one traceback at a time | **ADDED** | `tools/jira/doctor.py` |
| 11 | An unparsable `created` date vanished from the weekly trend, leaving a Total below the population that still equalled the sum of its own rows | **FIXED + TESTED** | both generators state the drop; validator check `C5`, demonstrated firing |
| 12 | `comp_counter` built over all 5,740 tickets and never read; `adf_text` and `row` imported unused | **REMOVED** | proven unused by AST before removal; §6 output byte-identical after |
| 13 | Five ordered pipeline steps with no entry point — regenerating a report silently left the renders and client pack describing the previous edition | **ADDED** | `tools/jira/run_census.py`; success and failure paths both tested |
| 14 | The validator's own checks had never been shown capable of failing | **ADDED** | `validate_analysis.py --self-test`, six crafted cases |

## Verification commands

```powershell
python tools\jira\doctor.py                        # environment + freshness; exit 0 = ready
python tools\jira\run_census.py                    # the whole pipeline, ending in validation
python tools\jira\validate_analysis.py             # 57 checks against the snapshots; exit 0 = clean
python tools\jira\validate_analysis.py --self-test # prove the checks can fail
```

Last full run: **57 PASS · 0 FAIL · 3 INFO**, pipeline green in ~47s.

## Remaining

Four items, none blocking. See §F and §G of [`README.md`](README.md).
