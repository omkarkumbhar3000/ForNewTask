/**
 * Chart and UI tokens.
 *
 * These hexes are not a taste call — the categorical and status slots come from a
 * validated palette and the combinations actually used here were re-run through
 * dataviz/scripts/validate_palette.js against the card surface. Three results drove
 * the choices below and should not be undone without re-validating:
 *
 *   1. good-green vs critical-red FAILS CVD separation (ΔE 4.1 deutan) — the classic
 *      red/green trap. So "Passed" is BLUE, never green, wherever it sits beside "Failed".
 *   2. critical + serious + warning as three adjacent chart fills FAILS twice (yellow
 *      leaves the lightness band; yellow↔orange normal-vision ΔE 13.6, under the 15
 *      floor). So severity is never encoded as three large fills — the severity chart
 *      is a single-series bar with the tier named on the axis.
 *   3. blue / orange / aqua PASSES all-pairs, so that is the categorical order.
 *
 * Status colors appear only as small dots beside ink text, never as the sole carrier
 * of meaning — warning and serious are deliberately sub-3:1 on a light surface.
 */

export const c = {
  // surfaces & ink
  surface: '#fcfcfb',
  page: '#f9f9f7',
  inkPrimary: '#0b0b0b',
  inkSecondary: '#52514e',
  inkMuted: '#898781',
  grid: '#e1e0d9',
  baseline: '#c3c2b7',
  border: 'rgba(11,11,11,0.10)',

  // categorical — fixed order, never cycled
  series1: '#2a78d6', // blue
  series2: '#eb6834', // orange
  series3: '#1baf7a', // aqua

  // status — small marks + label only
  good: '#0ca30c',
  warning: '#fab219',
  serious: '#ec835a',
  critical: '#d03b3b',
  neutral: '#898781',

  // deltas
  deltaGood: '#006300',
  deltaBad: '#d03b3b',
}

/** Outcome colors. Passed is blue, not green — see note 1 above. */
export const outcome = {
  Passed: c.series1,
  Failed: c.critical,
  Blocked: c.neutral, // a deliberate neutral: blocked is not an outcome, it is an absence of one
}

/** Severity → status dot. Used beside a text label, never alone. */
export const severityColor = {
  Critical: c.critical,
  High: c.serious,
  Medium: c.warning,
  Low: c.good,
  Informational: c.neutral,
}

/** Recharts shared props so every chart gets the same recessive chrome. */
export const axisProps = {
  tick: { fill: c.inkMuted, fontSize: 12 },
  stroke: c.baseline,
  tickLine: false,
}

export const gridProps = {
  stroke: c.grid,
  strokeDasharray: '0', // solid hairlines, never dashed
  vertical: false,
}

export const BAR_MAX = 24 // px — cap bar thickness, let the band's leftover be air
export const BAR_RADIUS = [4, 4, 0, 0] // rounded data-end, square at the baseline
export const BAR_RADIUS_H = [0, 4, 4, 0]
