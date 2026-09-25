import {
  ResponsiveContainer, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
} from 'recharts'
import { PageHead } from '../components/AppShell'
import { Section } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { StatTile, StatRow } from '../components/StatTile'
import { SampleBanner } from '../components/SampleBanner'
import { getUi } from '../services/dataService'
import { axisProps, gridProps, c, BAR_MAX, BAR_RADIUS } from '../theme'
import { sourceLabel } from '../utils/provenance'

export function Ui() {
  const u = getUi()
  const p = (o) => (o && typeof o === 'object' ? o : {})
  // CLS is a unitless score (~0.18); charting it beside LCP/FCP/TTFB in milliseconds makes it an
  // invisible bar and makes the axis meaningless. It stays in the table and on the benchmark view.
  const vitalsMs = Array.isArray(u.webVitals)
    ? u.webVitals.filter((v) => v.unit !== 'score' && typeof v.ms === 'number')
    : []

  return (
    <>
      <PageHead title="UI / user experience" sub="What the user actually experiences under load — real browser timings" />
      <SampleBanner />

      <StatRow>
        <StatTile label="Page load p95" value={p(u.pageLoadMs).p95} unit="ms" />
        <StatTile label="Module load p95" value={p(u.moduleLoadMs).p95} unit="ms" />
        <StatTile label="Navigation p95" value={p(u.navigationMs).p95} unit="ms" />
        <StatTile label="Submodule p95" value={p(u.submoduleLoadMs).p95} unit="ms" />
        <StatTile label="Perceived p95" value={p(u.perceivedMs).p95} unit="ms" />
        <StatTile label="UI failures" value={u.uiFailures} tone={u.uiFailures === 0 ? 'good' : undefined} />
      </StatRow>

      <div style={{ display: 'grid', gap: 16, gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))' }}>
        <ChartCard
          title="Browser Web Vitals"
          note="LCP, FCP and TTFB — the standard user-experience timings."
          available={vitalsMs.length > 0}
          height={250}
          emptyTitle="Web Vitals not captured in this run"
          emptyDetail="k6 emits browser_web_vital_* for browser scenarios only."
          tableColumns={[{ key: 'metric', header: 'Vital' }, { key: 'ms', header: 'avg', num: true },
            { key: 'p95', header: 'p95', num: true }, { key: 'unit', header: 'Unit' }]}
          tableRows={u.webVitals}
          source={sourceLabel(u)}
        >
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={vitalsMs} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="metric" {...axisProps} />
              <YAxis {...axisProps} width={48} />
              <Tooltip />
              <Bar dataKey="ms" fill={c.series1} maxBarSize={BAR_MAX} radius={BAR_RADIUS} isAnimationActive={false} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard
          title="Module load trend"
          note="Page/module load p95 across runs."
          available={Array.isArray(u.trend) && u.trend.length > 0}
          height={250}
          tableColumns={[{ key: 'run', header: 'Run' }, { key: 'ms', header: 'ms', num: true }]}
          tableRows={u.trend}
          source={sourceLabel(u)}
        >
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={u.trend} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="run" {...axisProps} />
              <YAxis {...axisProps} width={48} />
              <Tooltip />
              <Line type="monotone" dataKey="ms" stroke={c.series1} strokeWidth={2.5} dot={{ r: 3 }} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </>
  )
}
