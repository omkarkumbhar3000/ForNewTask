import { useState } from 'react'
import { Decide } from '../components/Decide'

const KINDS = { objective: 'Objective', resume: 'Resume point', todo: 'TODO' }

/**
 * Everything outstanding: in-progress objectives, resume points for paused work,
 * and source TODOs.
 *
 * These come from project data rather than a live measurement, and the provenance
 * chip on each item says so. That distinction matters here more than anywhere
 * else: an objective is "in progress" because a register file says it is.
 */
export function Tasks({ items, decisions, setDecision }) {
  const [kind, setKind] = useState('all')
  const [sev, setSev] = useState('all')

  const visible = items.pending
    .filter((i) => !i.hidden)
    .filter((i) => kind === 'all' || i.kind === kind)
    .filter((i) => sev === 'all' || i.severity === sev)

  return (
    <>
      <header className="page-head">
        <h1>Pending tasks</h1>
        <p className="lede">
          {visible.length} of {items.pending.length} shown.
        </p>
      </header>

      <div className="filters">
        <label>
          Type
          <select value={kind} onChange={(e) => setKind(e.target.value)}>
            <option value="all">all</option>
            {Object.entries(KINDS).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </label>
        <label>
          Priority
          <select value={sev} onChange={(e) => setSev(e.target.value)}>
            <option value="all">all</option>
            <option value="high">high</option>
            <option value="normal">normal</option>
            <option value="low">low</option>
          </select>
        </label>
      </div>

      {visible.length === 0 ? <p className="muted">Nothing matches this filter.</p> : null}

      {visible.map((i) => (
        <Decide key={i.key} item={i} decision={decisions[i.key]} onDecide={setDecision}>
          <p className="muted small">{KINDS[i.kind] || i.kind}</p>
        </Decide>
      ))}
    </>
  )
}
