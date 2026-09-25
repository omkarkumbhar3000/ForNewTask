import {
  Bar, BarChart, CartesianGrid, LabelList, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import { axisProps, gridProps, c, BAR_MAX } from '../theme'
import { compact, num } from '../utils/format'
import { ChartTooltip } from './ChartTooltip'

/**
 * One series, ranked, horizontal. Used for severity tiers, failing validation layers,
 * slowest modules and failures by module.
 *
 * Every bar is the SAME colour on purpose. Shading each bar darker-where-bigger would
 * double-encode length as hue, spend the only free channel on information the bar length
 * already carries, and — for nominal categories like modules — is simply wrong. Identity
 * comes from the category label on the axis, so no legend is needed for a single series.
 */
export function RankedBars({
  data,
  categoryKey = 'name',
  valueKey = 'value',
  valueName = 'Count',
  height = 260,
  color = c.series1,
  axisWidth = 150,
  unit = '',
  showLabels = true,
  note,
  title,
}) {
  if (!data || data.length === 0) return null

  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 4, right: showLabels ? 52 : 12, bottom: 4, left: 4 }}
        >
          <CartesianGrid {...gridProps} vertical horizontal={false} />
          <XAxis type="number" {...axisProps} tickFormatter={compact} />
          <YAxis type="category" dataKey={categoryKey} {...axisProps} width={axisWidth} />
          <Tooltip
            content={<ChartTooltip unit={unit} note={note} title={title} />}
            cursor={{ fill: 'rgba(11,11,11,0.035)' }}
          />
          <Bar
            dataKey={valueKey}
            name={valueName}
            fill={color}
            maxBarSize={BAR_MAX}
            radius={[0, 4, 4, 0]}
            isAnimationActive={false}
          >
            {/* value at the tip, outside the bar — never clipped by a short bar */}
            {showLabels && (
              <LabelList
                dataKey={valueKey}
                position="right"
                formatter={(v) => `${num(v)}${unit ? ` ${unit}` : ''}`}
                style={{ fill: c.inkSecondary, fontSize: 11.5, fontWeight: 600 }}
              />
            )}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
