import { useEffect, useState } from 'react'
import { getDecisions } from '../services/api'

/**
 * ⚠️ THE THINNEST VIEW, and honestly so.
 *
 * What is missing and why: engage OVERWRITES state/engage/context.json on every
 * run, by design — the .gitignore records that decision explicitly, on the grounds
 * that the file is regenerable and tracking it would put churn in every commit. So
 * there is no archive of past analyses to draw a history from, and inventing one
 * would mean fabricating runs that were never recorded.
 *
 * What DOES accumulate, starting now: the two append-only journals this Control
 * Center writes — every decision made and every action executed. This page shows
 * those. It will be genuinely useful after a few sessions and is nearly empty
 * before then, which is the accurate state of affairs rather than a bug.
 */
export function History({ executions }) {
  const [decisions, setDecisions] = useState(null)
  const [err, setErr] = useState(null)

  useEffect(() => {
    getDecisions().then((d) => setDecisions(d.decisions || [])).catch(setErr)
  }, [])

  const rows = [
    ...(decisions || []).map((d) => ({ ...d, type: 'decision' })),
    ...(executions || []).map((e) => ({ ...e, type: 'execution' })),
  ].sort((a, b) => String(b.at || '').localeCompare(String(a.at || '')))

  const byDay = rows.reduce((acc, r) => {
    const day = String(r.at || '').slice(0, 10) || 'undated'
    acc[day] = acc[day] || []
    acc[day].push(r)
    return acc
  }, {})

  return (
    <>
      <header className="page-head">
        <h1>History</h1>
        <p className="lede">
          {rows.length} recorded event(s) across the decision and execution journals.
        </p>
      </header>

      <p className="note">
        ⚠️ <strong>Partial by construction.</strong> engage overwrites its context on every
        run, so there is no archive of past analyses to show — only what this Control Center
        has journalled since it was first used. Nothing before that exists to display.
      </p>

      {err ? <p className="warn">Could not read the decision journal: {String(err.message || err)}</p> : null}

      {rows.length === 0 ? (
        <p className="muted">
          Nothing journalled yet. Make a decision and press Execute, and it will appear here.
        </p>
      ) : (
        Object.entries(byDay).map(([day, list]) => (
          <section className="sec" key={day}>
            <h2>{day}</h2>
            <ul className="plain">
              {list.map((r, i) => (
                <li key={i}>
                  <span className="prov">{r.type}</span>{' '}
                  {r.type === 'decision'
                    ? <>{r.decision} — <code>{r.item}</code>{r.note ? ` · ${r.note}` : ''}</>
                    : <>{r.ok ? '✓' : '✗'} <code>{r.action}</code>{r.target ? ` ${r.target}` : ''}
                        {r.reason ? ` — ${r.reason}` : ''}</>}
                </li>
              ))}
            </ul>
          </section>
        ))
      )}
    </>
  )
}
