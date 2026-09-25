import { severityColor, c } from '../theme'
import { delta as computeDelta, isNA, num, pct } from '../utils/format'

/**
 * Signed change vs the previous execution.
 * Colour encodes *meaning* not sign — `direction` says which way is good — and the arrow
 * plus the number carry it too, so the pill never depends on colour alone.
 */
export function DeltaPill({ current, previous, direction = 'up-good', showPct = true, suffix = 'vs N-1' }) {
  const d = computeDelta(current, previous, direction)
  if (!d) return null
  return (
    <span className={`delta ${d.tone === 'flat' ? '' : d.tone}`} title={`${d.text} ${suffix}`}>
      {d.arrow && <span className="arrow" aria-hidden="true">{d.arrow}</span>}
      {d.diff === 0 ? 'no change' : d.text}
      {showPct && d.pctText && d.diff !== 0 && (
        <span style={{ opacity: 0.72, fontWeight: 550 }}>&nbsp;{d.pctText}</span>
      )}
    </span>
  )
}

/** Severity as a coloured dot beside ink text. Never the colour on its own. */
export function SeverityBadge({ severity, label, plain = false }) {
  const color = severityColor[severity] || c.neutral
  return (
    <span className={`badge${plain ? ' plain' : ''}`}>
      <span className="dot" style={{ background: color }} aria-hidden="true" />
      {label || severity}
    </span>
  )
}

const TREND_TONE = {
  good: c.good,
  caution: c.warning,
  bad: c.critical,
  neutral: c.neutral,
}

/** The authored overall-trend line from the benchmark document. */
export function TrendBadge({ level = 'neutral', children }) {
  return (
    <span className="trend-badge">
      <span className="dot" style={{ background: TREND_TONE[level] || c.neutral }} aria-hidden="true" />
      {children}
    </span>
  )
}

export function StatusBadge({ status }) {
  const tone = status === 'Raised' ? c.good
    : status === 'Complete' ? c.good
      : status === 'Aborted' ? c.critical
        : c.neutral
  return (
    <span className="badge">
      <span className="dot" style={{ background: tone }} aria-hidden="true" />
      {status}
    </span>
  )
}

/** A share-of-total bar. Track is a lighter step of the fill's own hue. */
export function Meter({ value, max, title }) {
  const w = max > 0 ? Math.min(100, (Number(value) / Number(max)) * 100) : 0
  return (
    <div className="meter" title={title} role="img" aria-label={title}>
      <span style={{ width: `${w}%` }} />
    </div>
  )
}

/**
 * KPI tile. `value` may be "N/A", in which case the tile says so rather than showing 0.
 */
export function KpiTile({ label, value, previous, unit = '', direction = 'neutral', hint }) {
  const absent = isNA(value)
  return (
    <div className="card tile">
      <span className="tile-label">{label}</span>
      <div className="tile-value-row">
        {absent ? (
          <span className="tile-na">Not available</span>
        ) : (
          <>
            <span className="tile-value">{unit === '%' ? pct(value) : num(value)}</span>
            {unit && unit !== '%' && <span className="tile-unit">{unit}</span>}
          </>
        )}
        {!absent && <DeltaPill current={value} previous={previous} direction={direction} />}
      </div>
      {hint && <p className="tile-hint">{hint}</p>}
    </div>
  )
}

/** The one hero figure per view. Proportional figures, same sans as everything else. */
export function HeroFigure({ label, value, unit, delta: d, note, children }) {
  return (
    <div className="card hero">
      <div>
        <p className="hero-label">{label}</p>
        <div className="hero-value">
          {isNA(value) ? 'Not available' : num(value)}
          {unit && <span className="hero-unit">{unit}</span>}
        </div>
        {d}
      </div>
      <div className="hero-meta">
        {children}
        {note && <p className="hero-note">{note}</p>}
      </div>
    </div>
  )
}

/** A single headline finding, stated as a number plus what it means. */
export function Callout({ label, value, unit, detail, source, tone = 'flag' }) {
  return (
    <div className={`card callout ${tone}`}>
      <div className="callout-value">
        {isNA(value) ? 'N/A' : num(value)}
        {unit && <span className="u">{unit}</span>}
      </div>
      <p className="callout-label">{label}</p>
      <p className="callout-detail">{detail}</p>
      {source && <p className="prov" style={{ marginTop: 2 }}>{source}</p>}
    </div>
  )
}
