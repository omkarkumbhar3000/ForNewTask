import {
  Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import { axisProps, gridProps, c, BAR_MAX } from '../theme'
import { compact } from '../utils/format'
import { ChartTooltip } from './ChartTooltip'

/**
 * Two series side by side — the previous execution against the current one.
 *
 * One axis only. Recharts will happily take a second YAxis and it is never used here:
 * two scales on one plot invent a relationship the data does not contain. Where two
 * measures differ in scale they get two charts instead.
 *
 * Blue (slot 1) is the current run, orange (slot 2) the baseline — a validated
 * all-pairs-safe pairing. A legend is always drawn by the enclosing ChartCard.
 */
export function CompareBars({
  data,
  previousKey = 'previous',
  currentKey = 'current',
  previousName = 'N-1 (previous)',
  currentName = 'N (current)',
  categoryKey = 'metric',
  height = 260,
  horizontal = false,
  note,
}) {
  if (horizontal) {
    return (
      <div style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 4, right: 26, bottom: 4, left: 4 }} barGap={2}>
            <CartesianGrid {...gridProps} vertical horizontal={false} />
            <XAxis type="number" {...axisProps} tickFormatter={compact} />
            <YAxis type="category" dataKey={categoryKey} {...axisProps} width={148} />
            <Tooltip content={<ChartTooltip note={note} />} cursor={{ fill: 'rgba(11,11,11,0.035)' }} />
            <Bar dataKey={previousKey} name={previousName} fill={c.series2} maxBarSize={BAR_MAX} radius={[0, 4, 4, 0]} isAnimationActive={false} />
            <Bar dataKey={currentKey} name={currentName} fill={c.series1} maxBarSize={BAR_MAX} radius={[0, 4, 4, 0]} isAnimationActive={false} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    )
  }

  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 8, right: 8, bottom: 4, left: 0 }} barGap={2}>
          <CartesianGrid {...gridProps} />
          <XAxis dataKey={categoryKey} {...axisProps} interval={0} height={46} tickMargin={8} />
          <YAxis {...axisProps} tickFormatter={compact} width={52} />
          <Tooltip content={<ChartTooltip note={note} />} cursor={{ fill: 'rgba(11,11,11,0.035)' }} />
          <Bar dataKey={previousKey} name={previousName} fill={c.series2} maxBarSize={BAR_MAX} radius={[4, 4, 0, 0]} isAnimationActive={false} />
          <Bar dataKey={currentKey} name={currentName} fill={c.series1} maxBarSize={BAR_MAX} radius={[4, 4, 0, 0]} isAnimationActive={false} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
