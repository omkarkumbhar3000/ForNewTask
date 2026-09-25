# PAM Performance Dashboard

**`OBJ-019`** · React + Vite dashboard for the Login + Sanity performance work (k6, API + UI, correlated).
Sibling of the API dashboard in `tools/dashboard/`; same Theme 1 design language, adapted for
performance analysis.

**To run it manually, see [`HOW-TO-RUN.md`](HOW-TO-RUN.md).** Quick start:
`npm install` then `npm run dev` → <http://localhost:5174/>.

## Views

| View | Shows |
|---|---|
| Executive summary | Overall status, scenario counts, avg/p95/p99, throughput, error rate, active VUs, trend |
| Login performance | Auth API vs UI journey, segment breakdown, success rate, trend |
| Sanity performance | The 13 modules / 211 checks from `SanityChecks.xml`, per-module UI+API load, bottleneck attribution, the 6 excluded modules |
| API performance | Requests, req/s, latency percentiles, HTTP status distribution, error rate, checks, trend |
| UI / experience | Page/module/navigation/submodule load, Web Vitals, UI failures, trend |
| API vs UI | Per-module grouped bars (UI vs backend) + the bottleneck interpretation matrix |

## Architecture

Deliberately identical to the API dashboard so the two stay consistent:

- `src/theme.js` — the shared, CVD-validated palette (copied verbatim; Passed is blue, not green).
- `src/components/` — `AppShell`, `Card`, `ChartCard` (with a Chart/Table accessibility twin),
  `DataTable`, `StatTile`, `States`, `Indicators`, `SampleBanner`.
- `src/services/dataService.js` — the ONLY module that fetches. Pages call selectors; they never fetch.
- `src/pages/` — one file per view.
- `public/data/*.json` — datasets, fetched at runtime (`cache: 'no-store'`), written only by
  `scripts/build-performance-data.mjs`.

## Data state

Every figure is currently **SAMPLE** (a standing banner says so on every page) because no k6 execution
has produced real results yet — that is blocked on a working QA_MsSQL credential (see
`state/perf/OBJ-019-STATE.md`). The **Sanity scope is real**: modules and check counts are read
from `performance/data/sanity-modules.json`. When a real run lands, point the generator at
`performance/reports/<runId>/`, rerun it, and the dashboard shows measured numbers with no code change.
