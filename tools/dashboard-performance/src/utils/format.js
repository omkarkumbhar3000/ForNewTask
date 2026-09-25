/** Formatting helpers. The one rule: a value that was never measured stays "N/A". */

export const NA = 'N/A'

/** True when a value is absent rather than zero. Zero is a real measurement. */
export function isNA(v) {
  return v === null || v === undefined || v === '' || v === NA || v === 'n/a'
}

/** 5416 -> "5,416". Absent -> "N/A". */
export function num(v) {
  if (isNA(v)) return NA
  const n = typeof v === 'number' ? v : Number(String(v).replace(/,/g, ''))
  return Number.isFinite(n) ? n.toLocaleString('en-US') : String(v)
}

/** 5416 -> "5.4K". For axis ticks and tight tiles only. */
export function compact(v) {
  if (isNA(v)) return NA
  const n = Number(v)
  if (!Number.isFinite(n)) return String(v)
  if (Math.abs(n) >= 1_000_000) return `${(n / 1_000_000).toFixed(1).replace(/\.0$/, '')}M`
  if (Math.abs(n) >= 1_000) return `${(n / 1_000).toFixed(1).replace(/\.0$/, '')}K`
  return n.toLocaleString('en-US')
}

/**
 * ⛔ THE ONE FILE THAT MUST NOT BE HOISTED INTO A SHARED PACKAGE (`OBJ-027`).
 *
 * The two dashboards are fed OPPOSITE data contracts, measured:
 *   tools/dashboard/public/data/          successRate 63.6, coveragePct 87.3   -> 0-100
 *   tools/dashboard-performance/.../data/ checkRate 0.7619, successRate 1      -> 0-1
 *
 * Nine files are byte-identical between the two apps, including Indicators.jsx, which
 * imports `pct` by RELATIVE path. Hoist those into one package without reading this and
 * whichever app loses the coin toss silently rescales every percentage by 100x - in the
 * safe-looking direction, which is why the performance app once showed a 100% success
 * rate as "1.0%".
 *
 * So the contract is now NAMED rather than implied. Both functions below are identical in
 * both apps; only the `pct` alias differs, and that single line is the entire difference
 * between the two files. If you hoist the shared components, pass the formatter IN as a
 * prop - do not let a shared module import one app's `pct`.
 */
export function pctFromPercent(v, digits = 1) {
  // Input is ALREADY a percentage: 63.6 -> "63.6%"
  if (isNA(v)) return NA
  const n = Number(v)
  return Number.isFinite(n) ? `${n.toFixed(digits)}%` : String(v)
}

export function pctFromFraction(v, digits = 1) {
  // Input is a FRACTION: 0.636 -> "63.6%", 1 -> "100.0%"
  if (isNA(v)) return NA
  const n = Number(v)
  return Number.isFinite(n) ? `${(n * 100).toFixed(digits)}%` : String(v)
}

//: THIS APP's contract: datasets carry 0-1 fractions. See the header before changing.
export const pct = pctFromFraction

/** 329.1 minutes -> "5 h 29 m". Keeps the raw figure available separately. */
export function minutes(v) {
  if (isNA(v)) return NA
  const n = Number(v)
  if (!Number.isFinite(n)) return String(v)
  if (n < 60) return `${n.toFixed(1)} min`
  const h = Math.floor(n / 60)
  const m = Math.round(n - h * 60)
  return `${h} h ${m} m`
}

/** "2026-08-05" -> "05 Aug 2026". */
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export function niceDate(iso) {
  if (isNA(iso)) return NA
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(iso))
  if (!m) return String(iso)
  return `${m[3]} ${MONTHS[Number(m[2]) - 1]} ${m[1]}`
}

/** "2026-08-05_114315" -> "05 Aug 2026, 11:43". */
export function runLabel(runId) {
  const m = /^(\d{4})-(\d{2})-(\d{2})_(\d{2})(\d{2})/.exec(String(runId || ''))
  if (!m) return String(runId || NA)
  return `${m[3]} ${MONTHS[Number(m[2]) - 1]} ${m[1]}, ${m[4]}:${m[5]}`
}

/**
 * Signed change between two measurements.
 * `direction` says which way is good, so the colour is about meaning, not sign.
 * Returns null when either side was never measured — no delta is invented.
 */
export function delta(current, previous, direction = 'up-good') {
  if (isNA(current) || isNA(previous)) return null
  const a = Number(current)
  const b = Number(previous)
  if (!Number.isFinite(a) || !Number.isFinite(b)) return null
  const diff = a - b
  if (diff === 0) return { diff: 0, tone: 'flat', arrow: '', text: 'no change', pctText: null }
  const up = diff > 0
  const good = direction === 'neutral' ? 'flat' : (up === (direction === 'up-good') ? 'good' : 'bad')
  const pctChange = b !== 0 ? (diff / Math.abs(b)) * 100 : null
  // A percentage that rounds to zero says nothing and reads as an error ("−0%"), so drop it
  // and let the absolute figure carry the change on its own.
  const pctText = pctChange !== null && Math.abs(pctChange) >= 0.5
    ? `${up ? '+' : '−'}${Math.abs(pctChange).toFixed(0)}%`
    : null
  return {
    diff,
    tone: good,
    arrow: up ? '▲' : '▼',
    text: `${up ? '+' : '−'}${num(Math.abs(Number(diff.toFixed(1))))}`,
    pctText,
  }
}

/** Sort helper that always pushes N/A to the bottom regardless of direction. */
export function byNumber(key, dir = 'desc') {
  return (a, b) => {
    const av = a[key]
    const bv = b[key]
    if (isNA(av) && isNA(bv)) return 0
    if (isNA(av)) return 1
    if (isNA(bv)) return -1
    return dir === 'desc' ? Number(bv) - Number(av) : Number(av) - Number(bv)
  }
}
