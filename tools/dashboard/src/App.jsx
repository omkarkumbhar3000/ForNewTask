import { useCallback, useEffect, useState } from 'react'
import { AppShell } from './components/AppShell'
import { ErrorState, ErrorBoundary, Loading } from './components/States'
import { FreshnessNote } from './components/Freshness'
import { Benchmark } from './pages/Benchmark'
import { Dashboard } from './pages/Dashboard'
import { Findings } from './pages/Findings'
import { History } from './pages/History'
import { Projects } from './pages/Projects'
import { Reliability } from './pages/Reliability'
import { Report } from './pages/Report'
import {
  getGaps, getManifest, getPrimaryFindingSet, getProjects, getRuns, loadData,
} from './services/dataService'
import { useRoute } from './utils/router'

/**
 * The datasets are fetched at runtime (OBJ-016), so the app has a real loading phase.
 *
 * Everything loads once here and the selectors in dataService stay synchronous — that was the
 * deliberate trade: one async bootstrap instead of threading promises through every page.
 */
export default function App() {
  const { view, param } = useRoute()
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState(null)
  const [reloadedAt, setReloadedAt] = useState(null)

  const load = useCallback((signal) => {
    setStatus((s) => (s === 'ready' ? 'ready' : 'loading'))
    return loadData({ signal })
      .then(() => {
        setError(null)
        setStatus('ready')
      })
      .catch((err) => {
        if (err?.name === 'AbortError') return
        setError(err)
        setStatus('error')
      })
  }, [])

  useEffect(() => {
    const ac = new AbortController()
    load(ac.signal)
    return () => ac.abort()
  }, [load])

  /** Re-fetch without a page reload — the daily job may have rewritten the files since open. */
  const refetch = useCallback(async () => {
    await load()
    setReloadedAt(new Date().toLocaleTimeString())
  }, [load])

  if (status === 'loading') {
    return (
      <AppShell view={view} counts={null} footer={<p>Loading datasets…</p>}>
        <div className="page">
          <Loading height={120} label="Loading dashboard data" />
          <div className="grid grid-kpi" style={{ marginTop: 14 }}>
            {Array.from({ length: 6 }, (_, i) => (
              <div className="card tile" key={i}>
                <div className="skeleton" style={{ height: 54 }} />
              </div>
            ))}
          </div>
        </div>
      </AppShell>
    )
  }

  if (status === 'error') {
    return (
      <AppShell view={view} counts={null} footer={<p>Data could not be loaded.</p>}>
        <div className="page">
          <div className="card">
            <ErrorState
              title="The dashboard datasets could not be loaded"
              detail={String(error?.message || error)}
              onRetry={refetch}
            />
            <div className="card-foot">
              The app reads its datasets from <code>public/data/</code> at runtime. If that folder
              is empty, regenerate it:{' '}
              <code>python tools\obj015_build_dashboard_data.py</code>
            </div>
          </div>
        </div>
      </AppShell>
    )
  }

  const counts = {
    runs: getRuns().length,
    projects: getProjects().length,
    findings: getPrimaryFindingSet().total,
  }
  const manifest = getManifest()
  const gaps = getGaps()

  return (
    <AppShell
      view={view}
      counts={counts}
      footer={
        <>
          <FreshnessNote onRefetch={refetch} reloadedAt={reloadedAt} />
          <p style={{ marginTop: 8 }}>
            Built from {manifest.sources.length} measured source files.
            {' '}{gaps.length} known data gap{gaps.length === 1 ? '' : 's'}, listed on the dashboard.
          </p>
          <p>No figure on this dashboard is estimated.</p>
        </>
      }
    >
      <ErrorBoundary title="This view could not be displayed">
        {renderView(view, param)}
      </ErrorBoundary>
    </AppShell>
  )
}

function renderView(view, param) {
  switch (view) {
    case 'benchmark':
      return <Benchmark />
    case 'history':
      return <History />
    case 'reliability':
      return <Reliability />
    case 'projects':
      return <Projects />
    case 'findings':
      return <Findings />
    case 'report':
      return <Report runId={param} />
    case 'dashboard':
    default:
      return <Dashboard />
  }
}
