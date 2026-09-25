/**
 * The only module that touches the datasets.
 *
 * Pages never fetch — they call the selectors here. That keeps the presentation layer free of
 * data shape and transport, so replacing the static files with a real API means editing this
 * file and nothing else.
 *
 * ── OBJ-016: the data is fetched at runtime, not bundled ──────────────────────────────────
 * The datasets live in `public/data/` and are loaded once by `loadData()` before the app
 * renders. Consequence, and the point of the change: the daily job regenerates those files
 * and a browser refresh shows the new figures — no `npm run build`.
 *
 * `cache: 'no-store'` on every request is load-bearing. Without it the browser happily serves
 * a cached `runs.json` after a regenerate, which would silently defeat the whole mechanism and
 * look exactly like "the data didn't change".
 *
 * Regenerate with:
 *     python tools\obj016_daily_refresh.py --execute     (or the generator alone)
 *     python tools\obj015_build_dashboard_data.py
 */
import { isNA, byNumber } from '../utils/format'

/** Every dataset the app requires. A missing one is a hard failure — the UI must not guess. */
const REQUIRED = [
  'manifest', 'projects', 'runs', 'kpis', 'benchmark', 'findings',
  'modules', 'performance', 'failures', 'exclusions', 'gates', 'improvements',
  'reports', 'reliability', 'gaps',
]

/**
 * Written by the scheduled jobs. Absent until each has run once — that is not an error.
 *   refresh   — the daily pull-and-refresh job (OBJ-016)
 *   execution — the weekly full API execution (OBJ-017)
 */
const OPTIONAL = ['refresh', 'execution']

let store = null

/** Resolved dataset store, or throw if the app somehow rendered before loading finished. */
function d(name) {
  if (!store) {
    throw new Error(
      'dataService: loadData() has not completed. A page rendered before the data was ready.',
    )
  }
  return store[name]
}

export const isLoaded = () => store !== null

/**
 * Fetch every dataset in parallel. Call once, before rendering any page.
 * @param {{signal?: AbortSignal}} [opts]
 * @returns {Promise<object>} the store
 */
export async function loadData({ signal } = {}) {
  const base = `${import.meta.env.BASE_URL}data/`

  const get = async (name) => {
    const res = await fetch(`${base}${name}.json`, { cache: 'no-store', signal })
    if (!res.ok) throw new Error(`${name}.json — HTTP ${res.status} ${res.statusText}`)
    return res.json()
  }

  const required = await Promise.all(
    REQUIRED.map(async (name) => {
      try {
        return [name, await get(name)]
      } catch (err) {
        throw new Error(
          `Could not load ${name}.json from ${base} — ${err.message}. ` +
          'Regenerate it with: python workbench\\scripts\\obj015_build_dashboard_data.py',
        )
      }
    }),
  )

  const optional = await Promise.all(
    OPTIONAL.map(async (name) => {
      try {
        return [name, await get(name)]
      } catch {
        return [name, null]
      }
    }),
  )

  store = Object.fromEntries([...required, ...optional])
  return store
}

/* ── freshness ─────────────────────────────────────────────────────────────
   The dashboard must be able to say how old its own figures are. A daily job that failed
   silently would otherwise look identical to one that succeeded — yesterday's numbers, no
   indication they are yesterday's.                                                        */

/** @returns {{lastAttempt:string, ok:boolean, failedSteps:string[], steps:object[]}|null} */
export const getRefresh = () => d('refresh')

/**
 * Last weekly API execution, or null if the job has never run.
 * @returns {{lastAttempt:string, ok:boolean, aborted:boolean, runId:string|null,
 *            executed:number|null, abortedFlows:number|null, steps:object[],
 *            failedSteps:string[], schedule:string}|null}
 */
export const getExecution = () => d('execution')

/**
 * Freshness in a form the UI can render directly.
 * `state` is one of: 'never' (the job has not run), 'ok', 'failed'.
 */
export function getFreshness() {
  const r = d('refresh')
  if (!r) {
    return {
      state: 'never',
      label: 'Not yet refreshed automatically',
      detail: 'The daily job has not run. These figures are from the last manual generation.',
      ok: null,
      when: null,
    }
  }
  const when = r.lastAttemptFinished || r.lastAttempt
  const ageHours = when ? (Date.now() - new Date(when).getTime()) / 36e5 : null
  return {
    state: r.ok ? 'ok' : 'failed',
    ok: Boolean(r.ok),
    when,
    ageHours,
    stale: ageHours !== null && ageHours > 36,
    failedSteps: r.failedSteps || [],
    steps: r.steps || [],
    label: r.ok ? 'Data refreshed' : 'Last refresh failed',
    detail: r.ok
      ? (r.note || '')
      : `Failed: ${(r.failedSteps || []).join(', ') || 'see state/daily/daily.log'}. `
        + 'The figures below may be out of date.',
  }
}

/* ── projects ──────────────────────────────────────────────────────────── */

export const getProjects = () => d('projects')

export const getProject = (id) => d('projects').find((p) => p.id === id) || d('projects')[0] || null

/* ── runs ──────────────────────────────────────────────────────────────── */

/** Every run, newest first. Probes and aborted runs are included — they are real history. */
export function getRuns({ projectId, substantiveOnly = false } = {}) {
  let list = d('runs')
  if (projectId) list = list.filter((r) => r.projectId === projectId)
  if (substantiveOnly) list = list.filter((r) => r.substantive)
  return list
}

export const getRun = (id) => d('runs').find((r) => r.id === id) || null

export const getCurrentRun = () => d('runs').find((r) => r.isCurrent) || null

export const getBaselineRun = () => d('runs').find((r) => r.isBaseline) || null

/**
 * Runs that carry enough measurement to plot a trend, oldest first.
 * A two-point "trend" is a comparison, not a trend — callers should say which they mean.
 */
export function getTrendSeries({ projectId } = {}) {
  return getRuns({ projectId, substantiveOnly: true })
    .filter((r) => !isNA(r.successRate))
    .slice()
    .reverse()
    .map((r) => ({
      runId: r.id,
      date: r.date,
      successRate: Number(r.successRate),
      executed: Number(r.executed),
      passed: Number(r.passed),
      failed: Number(r.failed),
    }))
}

/* ── dashboard ─────────────────────────────────────────────────────────── */

export const getKpis = () => d('kpis')

export const getHeadlines = () => d('kpis').headlines

/* ── benchmark ─────────────────────────────────────────────────────────── */

export const getBenchmark = () => d('benchmark')

/** Benchmark rows grouped in the order the groups are declared. Empty groups are dropped. */
export function getBenchmarkGroups() {
  const b = d('benchmark')
  return b.groups
    .map((g) => ({ group: g, rows: b.metrics.filter((m) => m.group === g) }))
    .filter((g) => g.rows.length > 0)
}

/** Only the rows where both sides are numeric — the ones a bar chart can honestly show. */
export function getComparableMetrics(names) {
  return d('benchmark').metrics
    .filter((m) => names.includes(m.metric) && m.previousNum !== null && m.currentNum !== null)
    .map((m) => ({ metric: m.metric, previous: m.previousNum, current: m.currentNum, note: m.note }))
}

export const getScenarios = () => d('benchmark').scenarios

export const getRegression = () => d('benchmark').regression

/* ── findings ──────────────────────────────────────────────────────────── */

export const getFindingSets = () => d('findings').sets

export const getFindingSet = (id) => {
  const f = d('findings')
  return f.sets.find((s) => s.id === id) || f.sets.find((s) => s.id === f.primarySetId)
}

export const getPrimaryFindingSet = () => getFindingSet(d('findings').primarySetId)

export const getSeverityOrder = () => d('findings').severityOrder

export const getSeverityMapping = () => d('findings').severityMapping

/* ── detail ────────────────────────────────────────────────────────────── */

export const getModules = () => d('modules')

/** Modules ranked by failures, for the "where is it failing" view. */
export const getModulesByFailures = (limit) => {
  const sorted = d('modules').filter((m) => m.failed > 0).sort(byNumber('failed'))
  return limit ? sorted.slice(0, limit) : sorted
}

export const getPerformance = () => d('performance')

/** Slowest modules by p95, which is the figure that actually bites. */
export const getSlowestModules = (limit = 12) =>
  d('performance').byModule.filter((m) => m.count >= 3).sort(byNumber('p95Ms')).slice(0, limit)

export const getFailures = () => d('failures')

export const getExclusions = () => d('exclusions')

export const getGates = () => d('gates')

/** OBJ-020 — every execution's terminal state, including the ones that were interrupted. */
export const getReliability = () => d('reliability')

export const getImprovements = () => d('improvements')

/* ── reports ───────────────────────────────────────────────────────────── */

export const getReport = (runId) => d('reports')[runId] || null

export const hasReport = (runId) => Boolean(d('reports')[runId])

/* ── provenance & gaps ─────────────────────────────────────────────────── */

export const getManifest = () => d('manifest')

export const getGaps = () => d('gaps')

/** Sources actually present on disk when the datasets were built. */
export const getSources = () => d('manifest').sources

/**
 * A run-scoped view of what is and is not available, so a page can choose an empty state
 * instead of rendering a misleading zero.
 */
export function getRunCapabilities(runId) {
  const run = getRun(runId)
  if (!run) return { exists: false }
  return {
    exists: true,
    hasResults: !isNA(run.executed),
    hasBenchmark: Boolean(run.isCurrent),
    hasModuleBreakdown: Boolean(run.isCurrent),
    hasPerformance: !isNA(run.latencyMedianMs),
    hasEvidence: run.evidenceFiles > 0,
    substantive: run.substantive,
  }
}
