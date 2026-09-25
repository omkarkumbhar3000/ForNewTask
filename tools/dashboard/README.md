# react — Management Execution & Benchmark Dashboard

**Status:** ✅ **Built** (`OBJ-015`) · **data refreshes daily and is read at runtime** (`OBJ-016`)
**Stack:** React 18 · Vite 5 · Recharts 2 — four runtime dependencies, no backend
**Audience:** management. The target is *understand overall status in 30–60 seconds*
**Data:** `public/data/*.json`, generated from measured run artifacts by
`tools/obj015_build_dashboard_data.py` and refreshed daily by
`tools/obj016_daily_refresh.py`

---

## 1. Commands

```powershell
cd "E:\Omkar\Automation\Dev Project\workbench\react"
npm install        # once — 102 packages
npm run dev        # http://localhost:5173, opens automatically
npm run build      # production bundle into dist/
npm run preview    # serve the built bundle on :4173
```

Verified on **Node v24.18.0 / npm 11.18.0**. `npm install` emits an `allow-scripts` warning about
`esbuild`'s postinstall; the build works regardless, so no action is needed.

Routing is hash-based, so **`dist/index.html` opens straight from the filesystem** — no server
rewrite rules, which matters if the deck is being shown from a laptop with no dev server running.

## 2. The data refreshes itself daily

A Windows scheduled task, **`PAM-Dashboard-Daily-Refresh`**, runs at 08:30 daily and does the whole
chain. Because the app fetches its datasets at runtime, a browser refresh then shows the new figures —
**no `npm run build`**.

```powershell
cd "E:\Omkar\Automation\Dev Project"
python tools\obj016_daily_refresh.py             # DRY RUN — changes nothing
python tools\obj016_daily_refresh.py --execute    # the full chain
python tools\obj016_daily_refresh.py --execute --skip-git   # re-derive only

Start-ScheduledTask -TaskName PAM-Dashboard-Daily-Refresh     # run the scheduled task now
powershell -ExecutionPolicy Bypass -File tools\obj016_register_task.ps1 -At 21:00
powershell -ExecutionPolicy Bypass -File tools\obj016_register_task.ps1 -Remove
```

What the job does, and deliberately does not: see §10.

To regenerate only the datasets:

```powershell
python tools\obj015_build_dashboard_data.py            # build + verify
python tools\obj015_build_dashboard_data.py --verify   # verify only, writes nothing
```

The generator is **read-only on the workspace and issues zero HTTP calls**. The only directory it
writes is `public/data/`. It cross-checks ten derived figures against the run workbook's own authored
`Summary` sheet and exits non-zero on any mismatch, so a silent drift in the data layer fails loudly.

| Rule | Why |
|---|---|
| ⛔ **Never hand-edit `public/data/*.json`** | Regenerated wholesale on the next run; edits are lost |
| ⛔ **Exactly one copy of the data** | It lives in `public/data/` only. A leftover `src/data/` would be a second, silently diverging source |
| ⛔ **No figure is estimated** | Anything unmeasured is the string `"N/A"` and is listed in `gaps.json` |
| Provenance is mandatory | `manifest.json` names every source file and what it provided |
| Freshness is visible | `refresh.json` drives the sidebar stamp and a banner. A failed job says so on screen rather than quietly serving yesterday's numbers |

## 3. Views

| Route | View | What it answers |
|---|---|---|
| `#/` | Dashboard | What did we execute, what passed, how does it compare, what did it find |
| `#/benchmark` | Execution benchmark | N-1 vs N in full — 46 metrics, scenario coverage, regression, recommendations |
| `#/history` | Execution history | Every retained execution; select a row for its report |
| `#/projects` | Project view | Per-project rollup, endpoint coverage, how to add a second project |
| `#/findings` | Findings & risk | Four finding sets by severity, with drill-down |
| `#/report/<runId>` | Report | The management report for one execution |

## 4. Architecture

Data is separated from presentation so real reports can replace the snapshot without touching a
component:

```
public/
└── data/        generated JSON — 14 datasets + refresh.json. SERVED, not bundled
src/
├── services/    dataService.js — the ONLY module that fetches; pages call selectors
├── charts/      Recharts wrappers, one per chart form
├── components/  Card, ChartCard, DataTable, KpiTile, Freshness, badges, states, shell
├── pages/       one file per view
├── utils/       format.js (N/A-aware formatting), router.js (30-line hash router)
├── types/       JSDoc typedefs — the contract the generator emits
├── theme.js     colour tokens, with the validation results that chose them
└── App.jsx      async bootstrap: loads every dataset, then renders
```

**No page fetches anything.** `App.jsx` calls `loadData()` once and the selectors in
`dataService.js` stay synchronous — that was the deliberate trade, one async bootstrap instead of
threading promises through six pages. Swapping the static files for a real API means rewriting
`dataService.js` and nothing else.

⚠️ **`cache: 'no-store'` on every fetch is load-bearing.** Without it the browser serves a cached
`runs.json` after a regenerate, which defeats the entire mechanism and looks exactly like "the data
didn't change".

`react-router` was deliberately not added — six views and one parameterised route do not justify a
dependency, and hash routing is what makes the built bundle openable from disk.

## 5. Colour — the three results that constrain it

Chart colour here is not a taste call. The palette combinations actually used were run through the
`dataviz` skill's `validate_palette.js` against the card surface, and three failures shaped the design.
**Re-validate before changing any of them:**

| Finding | Consequence in the UI |
|---|---|
| good-green vs critical-red **fails** CVD separation (ΔE 4.1, deuteranopia) | **"Passed" is blue, never green**, wherever it sits beside "Failed" |
| critical + serious + warning as three adjacent fills **fails twice** — yellow leaves the lightness band, and yellow↔amber normal-vision ΔE 13.6 is under the 15 floor | Severity is **never three coloured fills**. The severity chart is a single-series bar with the tier named on the axis |
| blue / orange / aqua **passes** all-pairs in both modes | That is the categorical order — orange is always N-1, blue always N |

Status colours survive only as **small dots beside ink text**, never as the sole carrier of meaning:
amber and orange are deliberately sub-3:1 on a light surface, and the icon-plus-label pairing is the
documented mitigation. Every chart also has a **Table** toggle — that is the accessibility twin, not a
nicety, and it is how an exact figure is read off any chart.

Light theme only, by request. There is no dark palette.

## 6. Two traps the data layer already handles

Both would have produced a confidently wrong number on screen:

| Trap | What goes wrong | How it is handled |
|---|---|---|
| **A resumed run's own metadata undercounts it** | `results.json` `meta.elapsed_s` and `meta.calls` cover only the **last** process. Run N reads 94.9 min instead of 329.1 — a 234-minute understatement | Duration comes from `tools/.obj010/segments.json` for a resumed run. Every row carries `durationBasis` naming its source |
| **Endpoints reached ÷ endpoints declared is not coverage** | Run N reached **1,388** endpoints against a **1,306** catalogue — 106%. Measured cause: **248** of those endpoints are not declared in `APIConfig.java` at all; they come from the QA team's Excel corpus | Coverage is `endpointsInCatalogue / 1,306` = **87.3%**. All four figures are shown side by side on the Projects page with the reason |

A third is worth knowing when reading the code: **`results.json` has no hop verdict field.** A test
case's verdict is the AND of its check layers, and a hop with no checks was withheld — never a pass
and never a fail. `hop_verdict()` in the generator implements this, and it reproduces the published
3,459 / 1,957 / 14 and 1,200 / 668 / 5 exactly.

## 7. Adding a project

The view is data-driven, so this needs no UI change:

1. Author a profile in `data/profiles/` against `profile.schema.json`, using
   `pam.json` as the worked example.
2. Pass the readiness gate — `python tools\onboarding\validate_profile.py`.
3. Generate and execute; the run writes its own folder under `artifacts/runs/`.
4. Re-run the generator. The project and its executions appear automatically.

## 8. Known data gaps

Eight, listed in `src/data/gaps.json` and surfaced on the dashboard under **Data coverage** — each with
why it is missing and what would close it. The substantive ones:

| Gap | Why |
|---|---|
| Per-module and performance breakdown for N-1 | `obj010_build_workbook.py` only ever ran against run N |
| N-1 negative-dimension pass rate | That run's generator emitted positive flows only — a genuine property of the baseline |
| A second project | Only `pam.json` exists; no other project has been onboarded or executed |
| A single endpoint-coverage percentage | The two populations differ by 248 endpoints (§6) |
| Findings attributed per run beyond LH-01…13 | Findings are pinned to a source run by `LoopholeSpec.run_id`, and only two runs are cited |

⚠️ Three of the eleven retained executions wrote no `results.json` at all. They are listed in the
history as **Aborted** with `N/A` figures rather than hidden — the retention rule for this programme
is that no run is ever deleted.

## 9. Notes for whoever maintains this

- `workbench/` is **not versioned**. `node_modules/` and `dist/` are gitignored anyway; if this
  component needs history, `git init` **inside this folder** — never add it to
  `pam_automation_bootstrap` or `pam`.
- The bundle is ~57 KB gzipped for the app and ~156 KB for Recharts, split into separate chunks so a
  data rebuild does not invalidate the chart vendor chunk.
- Unrelated to the Java framework — this shares no build with Maven, Playwright or TestNG.

## 10. The daily job — what it does, and what it refuses to do

`tools/obj016_daily_refresh.py`, deny-by-default like every harness script here: a bare
run performs no fetch, no pull and no write.

| Step | Behaviour |
|---|---|
| **Pull `pam/`** | `git pull --ff-only`, so it can never create a merge commit. **Skipped if the tree is dirty** — it will not stash, reset or checkout to get its work done. Logs the packfile growth, because `OBJ-014` measured a routine pull adding 1.1 GB to that repository |
| **Fetch the automation repo** | `git fetch origin --prune`, then reports how far `AI` is behind `origin/Dev`. **Never a pull and never a merge** — `AI` has no upstream and merging `Dev` into it is the owner's decision |
| **Drift check** | `obj013_loop.py check --json`, read-only and offline |
| **RAG evidence index** | `obj013_rag_ingest.py --apply` |
| **Dashboard datasets** | the `OBJ-015` generator, including its self-verification |
| **Refresh stamp** | `public/data/refresh.json` — what the UI reads to show freshness |

⛔ **What it will never do**, guarded structurally by an allow-list in `run_git()` rather than by
convention: push · merge · rebase · reset · checkout · stash-mutate · clean · gc · prune · branch
surgery. It also **does not execute the API suite** (a decision taken explicitly — fresh source
changes no KPI, and a daily 5.5 h run against an environment that lost 85 of 329 minutes to app-pool
downtime would produce a daily false alarm), **does not call any PAM endpoint or `/arcontoken`**, and
**does not apply drift auto-fixes** (`obj013_fix.py` writes to `CLAUDE.md`, `README.md` and
`.claude/rules/*` in folders with no git history — drift is reported daily, applied by a human).

Exit code 0 means every step succeeded or was safely skipped; 1 means at least one failed. State is in
`state/daily/last-run.json`, the append-only log in `state/daily/daily.log`.

### The weekly execution (`OBJ-017`) — the only thing that moves the KPIs

`PAM-Weekly-API-Execution`, **Sundays 10:00**, runs `obj017_weekly_execution.py --execute`. The daily job
refreshes what is *derived*; this one produces a new execution, which is what changes the headline figures.

```powershell
python tools\obj017_weekly_execution.py            # DRY RUN - zero HTTP, not even the probe
python tools\obj017_weekly_execution.py --execute   # ~5.5 h
Start-ScheduledTask -TaskName PAM-Weekly-API-Execution
```

Chain: token-latch check → unauthenticated env probe → generate flows → `chain_runner --execute` (6 h
budget) → **one** resume if any flow aborted → validation gate → workbook against the resolved previous
run → dashboard datasets → `execution.json`. Its result shows in the dashboard's **Weekly execution** panel.

| Rule | Detail |
|---|---|
| ⛔ Never `--allow-teardown` / `--allow-preexisting-teardown` / `--include-unsafe` | Asserted absent in code, not merely omitted |
| ⛔ One token attempt, latched | Decision **D24** relaxes the no-scheduled-token rule for this job only. The host is probed **unauthenticated and first**, so no token is spent against a dead host; one attempt; a failure latches for ever |
| ⛔ The probe cannot be delegated to `--wait-for-env` | `chain_runner` takes the token *before* that probe, and the probe needs the token. The pre-flight must stay in the weekly job |
| One resume, then stop | A partial run is kept and flagged incomplete, never promoted to current |

⛔ **N and N-1 are resolved at run time.** Drop a new run folder in and it becomes current — that is what
makes the weekly schedule meaningful. **Authored analysis is pinned separately**: the narrative, the trend
line and the three headline findings belong to `AUTHORED_ANALYSIS_RUN` in the generator and are withheld
when N moves, with the UI saying *analysis pending*. After a weekly run, author an analysis and update that
constant — otherwise it stays pending for ever, which is correct but unhelpful.

⛔ **Two traps that only appear under the scheduler**, both already handled — do not undo them:

| Trap | What happened |
|---|---|
| **No console means cp1252** | Task Scheduler gives the child Python no console, so it picks the ANSI codepage for stdout. Several scripts here print `⛔`, so the first scheduled run died with `UnicodeEncodeError: 'charmap' codec can't encode character '⛔'` — a failure that never reproduces from an interactive shell. `child_env()` forces `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` |
| **PowerShell 5.1 reads UTF-8 as ANSI** | `obj016_register_task.ps1` is **7-bit ASCII on purpose**. An em-dash decodes to three cp1252 characters ending in a right double quotation mark, which PowerShell accepts as a string delimiter — opening an unterminated string and failing the whole script at parse time. Keep that file ASCII |
