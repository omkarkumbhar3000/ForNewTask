import { Kpi } from '../components/Kpi'
import { rank } from '../utils/items'

/** Workspace health at a glance. Every number here is measured by engage. */
export function Overview({ ctx, items }) {
  const s = ctx.summary || {}
  const drift = ctx.drift || {}
  const tasks = ctx.scheduled_tasks || []
  const visible = items.attention.filter((i) => !i.hidden)
  const worst = visible.filter((i) => rank(i.severity) <= 1)

  const health = worst.length === 0
    ? 'healthy'
    : worst.some((i) => i.severity === 'critical') ? 'needs attention' : 'watch'

  const when = ctx.finished ? ctx.finished.slice(0, 16).replace('T', ' ') : 'recently'

  return (
    <>
      <header className="page-head">
        <h1>DevProjects</h1>
        <p className="lede">
          Analysed {when} in {ctx.elapsed ? `${ctx.elapsed}s` : 'unknown time'}
          {ctx.dry_run ? ' · dry run' : ''}
        </p>
      </header>

      <div className="grid grid-kpi">
        <Kpi title="Workspace" value={health} note={`${s.repos ?? items.repos.length} repositories`} />
        <Kpi title="Synchronised" value={s.pulled ?? 0} note="fast-forwarded this run" />
        <Kpi title="Need attention" value={s.attention_repos ?? 0} note="repositories" />
        <Kpi
          title="Open items"
          value={visible.length}
          note={`${s.critical ?? 0} critical · ${s.high ?? 0} high`}
        />
      </div>

      <section className="sec">
        <h2>Worst first</h2>
        {worst.length === 0 ? (
          <p className="muted">
            Nothing critical or high. The full list is under Approvals and Pending tasks.
          </p>
        ) : (
          <ul className="plain">
            {worst.map((i) => (
              <li key={i.key}>
                <span className={`sev sev-${i.severity}`}>{i.severity}</span>
                {' '}{i.text}{' '}
                <span className={i.source === 'detected' ? 'prov prov-measured' : 'prov'}>
                  {i.source}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="sec">
        <h2>Derived data and jobs</h2>
        <p>
          Drift: <strong>{drift.summary || 'not reported'}</strong>
          {typeof drift.open === 'number' ? ` · ${drift.open} open` : ''}
        </p>
        <ul className="plain">
          {tasks.map((t) => (
            <li key={t.name}>
              <strong>{t.name}</strong> — {t.state || 'unknown'}
              {t.result === 0 ? ' · last run OK' : t.result != null ? ` · last exit ${t.result}` : ''}
              {t.next ? ` · next ${String(t.next).slice(0, 16).replace('T', ' ')}` : ''}
            </li>
          ))}
        </ul>
      </section>
    </>
  )
}
