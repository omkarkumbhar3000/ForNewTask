import {
  CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import { axisProps, gridProps, c } from '../theme'
import { runLabel } from '../utils/format'
import { ChartTooltip } from './ChartTooltip'

/**
 * Success rate across executions, oldest to newest.
 *
 * ⚠ Read this with the point count in mind. With only two substantive runs retained, two
 * points is a *comparison*, not a trend — the Benchmark view is the honest place for that
 * question. This chart earns its name once more full executions land, and it includes the
 * short probe runs so the history is complete rather than flattering.
 *
 * 2px line, ≥8px markers with a 2px surface ring so they stay legible where they overlap.
 */
export function RunTrendLine({ data, height = 240 }) {
  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
          <CartesianGrid {...gridProps} />
          <XAxis dataKey="date" {...axisProps} tickMargin={8} />
          <YAxis {...axisProps} domain={[0, 100]} tickFormatter={(v) => `${v}%`} width={44} />
          <Tooltip
            content={
              <ChartTooltip
                asPercent
                title={(row) => runLabel(row.runId)}
                note={(row) => `${row.passed?.toLocaleString()} passed of ${row.executed?.toLocaleString()} executed`}
              />
            }
            cursor={{ stroke: c.baseline, strokeWidth: 1 }}
          />
          <Line
            type="linear"
            dataKey="successRate"
            name="Success rate"
            stroke={c.series1}
            strokeWidth={2}
            strokeLinejoin="round"
            strokeLinecap="round"
            dot={{ r: 4.5, fill: c.series1, stroke: c.surface, strokeWidth: 2 }}
            activeDot={{ r: 6, fill: c.series1, stroke: c.surface, strokeWidth: 2 }}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
