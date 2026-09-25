/**
 * The only module that touches the performance datasets. Pages call selectors; they never fetch.
 * Mirrors the API dashboard's dataService so the two apps stay structurally identical — replacing
 * the sample JSON with real k6 output means editing the generator and this file, nothing else.
 *
 * Datasets live in public/data/ and are fetched once at runtime (cache: 'no-store', so a
 * regenerate is visible on refresh). Regenerate with:
 *   node tools/dashboard-performance/scripts/build-performance-data.mjs
 */

const REQUIRED = ['manifest', 'summary', 'login', 'sanity', 'api', 'ui', 'comparison',
  'executions', 'benchmark']

let store = null

function d(name) {
  if (!store) throw new Error('dataService: loadData() has not completed before a page rendered.')
  return store[name]
}

export const isLoaded = () => store !== null

export async function loadData({ signal } = {}) {
  const base = (import.meta.env.BASE_URL || '/') + 'data/'
  const entries = await Promise.all(
    REQUIRED.map(async (name) => {
      const res = await fetch(`${base}${name}.json`, { cache: 'no-store', signal })
      if (!res.ok) throw new Error(`Could not load dataset "${name}" (HTTP ${res.status}).`)
      return [name, await res.json()]
    }),
  )
  store = Object.fromEntries(entries)
  return store
}

// ── selectors ──────────────────────────────────────────────────────────────────────────────
export const getManifest = () => d('manifest')
export const getSummary = () => d('summary')
export const getLogin = () => d('login')
export const getSanity = () => d('sanity')
export const getApi = () => d('api')
export const getUi = () => d('ui')
export const getComparison = () => d('comparison')
export const getBenchmark = () => d('benchmark')

/** OBJ-020 - every k6 invocation, including attempts that produced no measurement. */
export const getExecutions = () => d('executions')

/** True when every figure is illustrative rather than measured. Drives the standing banner. */
export const isSample = () => {
  const m = d('manifest')
  return m.dataState === 'sample'
}
export const getSampleNote = () => d('manifest').sampleNote

/** Counts for the sidebar nav badges. */
export const getCounts = () => ({
  sanity: getSanity().totals?.modules ?? null,
})
