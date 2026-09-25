import { useCallback, useEffect, useState } from 'react'
import { AppShell } from './components/AppShell'
import { ErrorState, Loading } from './components/States'
import { Summary } from './pages/Summary'
import { Login } from './pages/Login'
import { Sanity } from './pages/Sanity'
import { Api } from './pages/Api'
import { Ui } from './pages/Ui'
import { Comparison } from './pages/Comparison'
import { Benchmark } from './pages/Benchmark'
import { getCounts, loadData } from './services/dataService'
import { useRoute } from './utils/router'
import { c } from './theme'

/** Datasets are fetched at runtime, so there is a real loading phase, exactly like the API app. */
export default function App() {
  const { view } = useRoute()
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState(null)

  const load = useCallback((signal) => {
    setStatus((s) => (s === 'ready' ? 'ready' : 'loading'))
    return loadData({ signal })
      .then(() => { setError(null); setStatus('ready') })
      .catch((err) => {
        if (err?.name === 'AbortError') return
        setError(err); setStatus('error')
      })
  }, [])

  useEffect(() => {
    const ac = new AbortController()
    load(ac.signal)
    return () => ac.abort()
  }, [load])

  if (status === 'loading') {
    return (
      <div className="shell">
        <div className="main"><Loading height={320} label="Loading performance data" /></div>
      </div>
    )
  }
  if (status === 'error') {
    return (
      <div className="shell">
        <div className="main">
          <ErrorState
            title="Could not load the performance datasets"
            detail={String(error?.message || error)}
            onRetry={() => load()}
          />
        </div>
      </div>
    )
  }

  const counts = getCounts()
  const page = { summary: Summary, dashboard: Summary, login: Login, sanity: Sanity,
    api: Api, ui: Ui, comparison: Comparison, benchmark: Benchmark }[view] || Summary
  const Page = page

  return (
    <AppShell
      view={view}
      counts={counts}
      footer={
        <div style={{ fontSize: 11, color: c.inkMuted, lineHeight: 1.5 }}>
          <p style={{ margin: 0, fontWeight: 600 }}>OBJ-021 · PAMIT</p>
          <p style={{ margin: '2px 0 0' }}>Login + Sanity · k6 v2.2.0</p>
        </div>
      }
    >
      <Page />
    </AppShell>
  )
}
