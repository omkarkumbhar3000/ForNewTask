import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import { outcome, c } from '../theme'
import { num, pct } from '../utils/format'
import { ChartTooltip } from './ChartTooltip'

/**
 * Passed / failed / blocked as part-to-whole. Three segments, far apart in value — the two
 * cases where a donut is legitimate.
 *
 * Passed is BLUE, not green. Green beside the failure red fails colourblind separation
 * (ΔE 4.1 under deuteranopia), so the pairing was re-stepped to blue↔red, which passes.
 * Blocked is a deliberate neutral grey: it is the absence of an outcome, not an outcome.
 * Every segment is also direct-labelled in the centre list, so colour is never load-bearing.
 */
export function OutcomeDonut({ data, height = 210 }) {
  const total = data.reduce((s, d) => s + Number(d.value || 0), 0)

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 18, flexWrap: 'wrap' }}>
      <div style={{ width: 190, height, flex: '0 0 190px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius="62%"
              outerRadius="92%"
              paddingAngle={2}          /* the 2px surface gap, as an angle */
              stroke={c.surface}
              strokeWidth={2}
              isAnimationActive={false}
            >
              {data.map((d) => (
                <Cell key={d.name} fill={outcome[d.name] || c.neutral} />
              ))}
            </Pie>
            <Tooltip
              content={<ChartTooltip />}
              formatter={(v) => num(v)}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* direct labels — the value is readable without the tooltip */}
      <dl style={{ margin: 0, display: 'grid', gap: 9, minWidth: 150, flex: '1 1 150px' }}>
        {data.map((d) => (
          <div key={d.name} style={{ display: 'flex', alignItems: 'baseline', gap: 9 }}>
            <span
              style={{
                width: 9, height: 9, borderRadius: 3, flex: '0 0 9px',
                background: outcome[d.name] || c.neutral, marginTop: 4,
              }}
              aria-hidden="true"
            />
            <dt style={{ color: c.inkSecondary, fontSize: 12.5, flex: '1 1 auto' }}>{d.name}</dt>
            <dd style={{ margin: 0, fontWeight: 650, fontVariantNumeric: 'tabular-nums' }}>
              {num(d.value)}
              <span style={{ color: c.inkMuted, fontWeight: 500, marginLeft: 6, fontSize: 11.5 }}>
                {total > 0 ? pct((Number(d.value) / total) * 100, 1) : ''}
              </span>
            </dd>
          </div>
        ))}
      </dl>
    </div>
  )
}
