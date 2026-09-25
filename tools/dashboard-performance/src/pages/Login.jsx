import {
  ResponsiveContainer, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from 'recharts'
import { PageHead } from '../components/AppShell'
import { Section } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { StatTile, StatRow } from '../components/StatTile'
import { SampleBanner } from '../components/SampleBanner'
import { getLogin } from '../services/dataService'
import { axisProps, gridProps, c, BAR_MAX, BAR_RADIUS } from '../theme'
import { pct } from '../utils/format'
import { sourceLabel } from '../utils/provenance'

export function Login() {
  const l = getLogin()
  const p = (o) => (o && typeof o === 'object' ? o : {})
  const ui = p(l.uiJourneyMs)
  const api = p(l.authApiMs)

  return (
    <>
      <PageHead title="Login performance" sub={l.authPath} />
      <SampleBanner />

      <StatRow>
        <StatTile label="UI journey p95" value={ui.p95} unit="ms" />
        <StatTile label="Auth API p95" value={api.p95} unit="ms" />
        <StatTile label="Browser overhead" value={l.browserOverheadMs} unit="ms" sub="UI auth − API auth" />
        <StatTile label="Success rate" value={l.successRate === 'N/A' ? 'N/A' : pct(l.successRate)} tone="good" />
        <StatTile label="Failure rate" value={l.failureRate === 'N/A' ? 'N/A' : pct(l.failureRate)} />
      </StatRow>

      <Section title="Login journey breakdown" hint="where the time goes in a browser login">
        <ChartCard
          title="Journey segments"
          note="Navigation → credential entry → authentication → landing render."
          available={Array.isArray(l.segments) && l.segments.length > 0}
          height={280}
          tableColumns={[{ key: 'segment', header: 'Segment' }, { key: 'ms', header: 'ms', num: true }]}
          tableRows={l.segments}
          source={sourceLabel(l)}
        >
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={l.segments} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="segment" {...axisProps} />
              <YAxis {...axisProps} width={48} />
              <Tooltip />
              <Bar dataKey="ms" maxBarSize={BAR_MAX} radius={BAR_RADIUS} isAnimationActive={false}>
                {l.segments.map((_, i) => (
                  <Cell key={i} fill={i === 2 ? c.series2 : c.series1} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>

      <Section title="Login trend" hint="UI journey vs auth API across runs">
        <ChartCard
          title="UI vs API over time"
          note="The gap between the lines is the browser/UI overhead on the same authentication."
          legend={[{ label: 'UI journey', color: c.series1, line: true }, { label: 'Auth API', color: c.series2, line: true }]}
          available={Array.isArray(l.trend) && l.trend.length > 0}
          height={260}
          tableColumns={[{ key: 'run', header: 'Run' }, { key: 'ui', header: 'UI (ms)', num: true }, { key: 'api', header: 'API (ms)', num: true }]}
          tableRows={l.trend}
          source={sourceLabel(l)}
        >
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={l.trend} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="run" {...axisProps} />
              <YAxis {...axisProps} width={48} />
              <Tooltip />
              <Line type="monotone" dataKey="ui" stroke={c.series1} strokeWidth={2.5} dot={{ r: 3 }} isAnimationActive={false} />
              <Line type="monotone" dataKey="api" stroke={c.series2} strokeWidth={2.5} dot={{ r: 3 }} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>
    </>
  )
}
