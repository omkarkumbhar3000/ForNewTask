import {
  ResponsiveContainer, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from 'recharts'
import { PageHead } from '../components/AppShell'
import { Section } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { StatTile, StatRow } from '../components/StatTile'
import { SampleBanner } from '../components/SampleBanner'
import { getApi } from '../services/dataService'
import { axisProps, gridProps, c, BAR_MAX, BAR_RADIUS } from '../theme'
import { pct } from '../utils/format'
import { sourceLabel } from '../utils/provenance'

export function Api() {
  const a = getApi()
  const perc = a.percentiles && typeof a.percentiles === 'object' ? a.percentiles : {}
  const percentileData = [
    { name: 'p90', ms: perc.p90 }, { name: 'p95', ms: perc.p95 }, { name: 'p99', ms: perc.p99 },
  ].filter((d) => typeof d.ms === 'number')

  return (
    <>
      <PageHead title="API performance" sub="Backend scalability at the HTTP layer, isolated from the browser" />
      <SampleBanner />

      <StatRow>
        <StatTile label="Requests" value={a.requests} />
        <StatTile label="Req/sec" value={a.requestsPerSec} />
        <StatTile label="Avg latency" value={a.avgLatencyMs} unit="ms" />
        <StatTile label="Median" value={a.medianLatencyMs} unit="ms" />
        <StatTile label="Error rate" value={a.errorRate === 'N/A' ? 'N/A' : pct(a.errorRate)} tone={a.errorRate !== 'N/A' && a.errorRate < 0.01 ? 'good' : undefined} />
        <StatTile label="Checks pass" value={a.checksPassRate === 'N/A' ? 'N/A' : pct(a.checksPassRate)} tone="good" />
      </StatRow>

      <div style={{ display: 'grid', gap: 16, gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))' }}>
        <ChartCard
          title="Latency percentiles"
          note="p90 / p95 / p99 of API response time."
          available={percentileData.length > 0}
          height={260}
          tableColumns={[{ key: 'name', header: 'Percentile' }, { key: 'ms', header: 'ms', num: true }]}
          tableRows={percentileData}
          source={sourceLabel(a)}
        >
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={percentileData} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="name" {...axisProps} />
              <YAxis {...axisProps} width={48} />
              <Tooltip />
              <Bar dataKey="ms" fill={c.series1} maxBarSize={BAR_MAX} radius={BAR_RADIUS} isAnimationActive={false} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard
          title="HTTP status distribution"
          note="A 302 is auth success; a 200 is a page render or a rejected login re-render."
          available={Array.isArray(a.statusDistribution) && a.statusDistribution.length > 0}
          height={260}
          tableColumns={[{ key: 'code', header: 'Code' }, { key: 'label', header: 'Meaning' }, { key: 'count', header: 'Count', num: true }]}
          tableRows={a.statusDistribution}
          source={sourceLabel(a)}
        >
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={a.statusDistribution} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="code" {...axisProps} />
              <YAxis {...axisProps} width={48} />
              <Tooltip />
              <Bar dataKey="count" maxBarSize={BAR_MAX} radius={BAR_RADIUS} isAnimationActive={false}>
                {a.statusDistribution.map((s, i) => (
                  <Cell key={i} fill={s.code === '302' ? c.series1 : s.code === '200' ? c.series3 : c.critical} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <Section title="API latency trend" hint="p95 across runs">
        <ChartCard
          title="p95 over time"
          available={Array.isArray(a.trend) && a.trend.length > 0}
          height={240}
          tableColumns={[{ key: 'run', header: 'Run' }, { key: 'p95', header: 'p95 (ms)', num: true }]}
          tableRows={a.trend}
          source={sourceLabel(a)}
        >
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={a.trend} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="run" {...axisProps} />
              <YAxis {...axisProps} width={48} />
              <Tooltip />
              <Line type="monotone" dataKey="p95" stroke={c.series1} strokeWidth={2.5} dot={{ r: 3 }} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>
    </>
  )
}
