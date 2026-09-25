import { num, pct } from '../utils/format'

/**
 * Shared tooltip. Every chart in the app uses this one so hover reads identically
 * everywhere. Tooltips enhance — they never gate a value, because the Table toggle on each
 * chart card carries the same numbers.
 *
 * @param {(row:object)=>string} [note] Extra line drawn from the hovered row.
 */
export function ChartTooltip({ active, payload, label, unit = '', asPercent = false, note, title }) {
  if (!active || !payload || payload.length === 0) return null
  const row = payload[0]?.payload || {}
  return (
    <div className="tip">
      <div className="tip-title">{title ? title(row) : label}</div>
      {payload.map((p) => (
        <div className="tip-row" key={p.dataKey}>
          <span className="k">
            <span className="sw" style={{ background: p.color || p.fill }} aria-hidden="true" />
            {p.name}
          </span>
          <span className="v">
            {asPercent ? pct(p.value) : num(p.value)}{!asPercent && unit ? ` ${unit}` : ''}
          </span>
        </div>
      ))}
      {note && <div className="tip-note">{note(row)}</div>}
    </div>
  )
}
