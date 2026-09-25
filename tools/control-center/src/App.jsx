import { useCallback, useEffect, useMemo, useState } from 'react'
import { ErrorState, Loading } from './components/States'
import { Shell } from './components/Shell'
import { SelectionBar } from './components/SelectionBar'
import { Applications } from './pages/Applications'
import { Approvals } from './pages/Approvals'
import { Execution } from './pages/Execution'
import { History } from './pages/History'
import { Overview } from './pages/Overview'
import { Recommendations } from './pages/Recommendations'
import { Tasks } from './pages/Tasks'
import { getContext, getExecutions, hasToken, postDecisions, postExecute } from './services/api'
import {
  applySuppressions, attentionItems, isSafeAction, pendingItems, rank, repoItems,
} from './utils/items'
import { useRoute } from './utils/router'

/**
 * The Control Center holds ONE piece of state that matters: the owner's pending
 * decisions, keyed by item. Nothing is sent until they press Execute, so the page
 * is a scratchpad up to that moment and there is no half-applied middle state.
 *
 * Selections live here rather than in each page so a decision made on Applications
 * is still there when you come back from Approvals.
 */
export default function App() {
  const { view } = useRoute()
  const [ctx, setCtx] = useState(null)
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState(null)
  const [decisions, setDecisions] = useState({})   // key -> decision verb
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)
  const [executions, setExecutions] = useState([])

  const load = useCallback(async (refresh = false) => {
    setStatus((s) => (s === 'ready' ? 'ready' : 'loading'))
    try {
      const c = await getContext({ refresh })
      setCtx(c)
      setError(null)
      setStatus('ready')
      try {
        setExecutions((await getExecutions()).executions || [])
      } catch { /* the journal is optional; its absence is not an error */ }
    } catch (e) {
      setError(e)
      setStatus('error')
    }
  }, [])

  useEffect(() => { load(false) }, [load])

  const runId = ctx?.started || 'unknown'

  /** All decidable items, worst-first, with recorded suppressions applied. */
  const items = useMemo(() => {
    if (!ctx) return { repos: [], attention: [], pending: [], all: [] }
    const sup = ctx._suppressions || {}
    const repos = applySuppressions(repoItems(ctx), sup, runId)
    const attention = applySuppressions(attentionItems(ctx), sup, runId)
      .sort((a, b) => rank(a.severity) - rank(b.severity))
    const pending = applySuppressions(pendingItems(ctx), sup, runId)
      .sort((a, b) => rank(a.severity) - rank(b.severity))
    return { repos, attention, pending, all: [...repos, ...attention, ...pending] }
  }, [ctx, runId])

  const actionsMeta = ctx?._actions || {}

  const setDecision = useCallback((key, verb) => {
    setDecisions((d) => {
      const next = { ...d }
      if (!verb || next[key] === verb) delete next[key]
      else next[key] = verb
      return next
    })
  }, [])

  const bulk = useCallback((mode) => {
    setDecisions((d) => {
      if (mode === 'none') return {}
      const next = { ...d }
      for (const it of items.all) {
        if (it.hidden) continue
        if (mode === 'safe' && isSafeAction(it, actionsMeta)) next[it.key] = 'accept'
        if (mode === 'high' && rank(it.severity) <= 1 && it.action && !it.needsConfirmation) {
          next[it.key] = 'accept'
        }
      }
      return next
    })
  }, [items.all, actionsMeta])

  /** What Execute will actually attempt, versus what is only being recorded. */
  const plan = useMemo(() => {
    const byKey = Object.fromEntries(items.all.map((i) => [i.key, i]))
    const executing = []
    const recording = []
    for (const [key, verb] of Object.entries(decisions)) {
      const it = byKey[key]
      if (!it) continue
      const row = { item: key, decision: verb, action: it.action, target: it.target,
                    fingerprint: it.fingerprint, label: it.name || it.text }
      if ((verb === 'accept' || verb === 'approve') && it.action) executing.push(row)
      else recording.push(row)
    }
    return { executing, recording, total: executing.length + recording.length }
  }, [decisions, items.all])

  const submit = useCallback(async () => {
    setBusy(true)
    try {
      // Record first. If execution then fails, the intent survives — the reverse
      // ordering would lose the decision on any error.
      if (plan.recording.length || plan.executing.length) {
        await postDecisions([...plan.recording, ...plan.executing], runId)
      }
      const res = plan.executing.length
        ? await postExecute(plan.executing, runId)
        : { results: [], refused: [], summary: { ok: 0, failed: 0, refused: 0 } }
      setResult(res)
      setDecisions({})
      await load(false)
      window.location.hash = '#/execution'
    } catch (e) {
      setResult({ error: String(e.message || e) })
    } finally {
      setBusy(false)
    }
  }, [plan, runId, load])

  if (!hasToken) {
    return (
      <Shell view={view} counts={null}>
        <div className="page">
          <ErrorState
            title="Opened without a token"
            detail={'This page must be opened from the URL that control_center.py prints, which '
              + 'carries a one-off token. Start it with: python tools/control_center.py --open'}
          />
        </div>
      </Shell>
    )
  }

  if (status === 'loading') {
    return (
      <Shell view={view} counts={null}>
        <div className="page"><Loading height={140} label="Reading the engage context" /></div>
      </Shell>
    )
  }

  if (status === 'error') {
    return (
      <Shell view={view} counts={null}>
        <div className="page">
          <ErrorState title="Could not read the context" detail={String(error?.message || error)} />
        </div>
      </Shell>
    )
  }

  const counts = {
    attention: items.attention.filter((i) => !i.hidden).length,
    repos: items.repos.length,
    pending: items.pending.filter((i) => !i.hidden).length,
    approvals: items.all.filter((i) => !i.hidden && i.needsConfirmation).length,
  }

  const pageProps = { ctx, items, decisions, setDecision, actionsMeta, executions, result }

  return (
    <Shell view={view} counts={counts} onRefresh={() => load(true)}>
      <div className="page">
        {view === 'applications' ? <Applications {...pageProps} />
          : view === 'tasks' ? <Tasks {...pageProps} />
          : view === 'approvals' ? <Approvals {...pageProps} />
          : view === 'recommendations' ? <Recommendations {...pageProps} />
          : view === 'history' ? <History {...pageProps} />
          : view === 'execution' ? <Execution {...pageProps} />
          : <Overview {...pageProps} />}
      </div>
      <SelectionBar plan={plan} busy={busy} onBulk={bulk} onSubmit={submit} />
    </Shell>
  )
}
