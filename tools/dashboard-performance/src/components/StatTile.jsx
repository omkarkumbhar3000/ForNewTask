import { isNA } from '../utils/format'
import { c } from '../theme'

/**
 * A KPI tile. Value large, label above, optional unit and sub-note. "N/A" renders as a muted
 * dash — the dashboard never shows a fabricated 0 where a measurement does not exist.
 */
export function StatTile({ label, value, unit, sub, tone }) {
  const na = isNA(value) || value === undefined || value === null
  const color = tone === 'good' ? c.deltaGood : tone === 'bad' ? c.critical : c.inkPrimary
  return (
    <div className="card" style={{ padding: '15px 17px', minWidth: 0 }}>
      <p style={{ margin: 0, fontSize: 12, fontWeight: 600, color: c.inkMuted, textTransform: 'uppercase', letterSpacing: 0.3 }}>
        {label}
      </p>
      <p style={{ margin: '7px 0 0', fontSize: 26, fontWeight: 680, lineHeight: 1.1, color: na ? c.inkMuted : color }}>
        {na ? '—' : value}
        {!na && unit && <span style={{ fontSize: 14, fontWeight: 560, color: c.inkMuted }}>&nbsp;{unit}</span>}
      </p>
      {sub && <p style={{ margin: '5px 0 0', fontSize: 12, color: c.inkSecondary }}>{sub}</p>}
    </div>
  )
}

/** A responsive row of stat tiles. */
export function StatRow({ children }) {
  return (
    <div style={{ display: 'grid', gap: 12, gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', marginBottom: 16 }}>
      {children}
    </div>
  )
}
