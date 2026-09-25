import {
  Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import { axisProps, gridProps, c, outcome } from '../theme'
import { compact } from '../utils/format'
import { ChartTooltip } from './ChartTooltip'

/**
 * Passed and failed stacked within each category, so the bar length is the category's
 * total and the split is visible inside it. Used for the scenario dimensions.
 *
 * The 2px stroke in the surface colour is the surface gap between segments — the skill's
 * separator. It is not a border drawn around the mark.
 */
export function StackedOutcomeBars({
  data,
  categoryKey = 'scenario',
  height = 250,
  axisWidth = 150,
  note,
}) {
  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: 4, right: 18, bottom: 4, left: 4 }}>
          <CartesianGrid {...gridProps} vertical horizontal={false} />
          <XAxis type="number" {...axisProps} tickFormatter={compact} />
          <YAxis type="category" dataKey={categoryKey} {...axisProps} width={axisWidth} />
          <Tooltip content={<ChartTooltip note={note} />} cursor={{ fill: 'rgba(11,11,11,0.035)' }} />
          <Bar
            dataKey="passed" name="Passed" stackId="o" fill={outcome.Passed}
            stroke={c.surface} strokeWidth={2} maxBarSize={24} isAnimationActive={false}
          />
          <Bar
            dataKey="failed" name="Failed" stackId="o" fill={outcome.Failed}
            stroke={c.surface} strokeWidth={2} maxBarSize={24} radius={[0, 4, 4, 0]}
            isAnimationActive={false}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
