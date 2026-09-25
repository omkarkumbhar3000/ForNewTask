import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
} from 'recharts'
import { PageHead } from '../components/AppShell'
import { Section, Card, CardHead, CardBody } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { StatTile, StatRow } from '../components/StatTile'
import { SampleBanner } from '../components/SampleBanner'
import { ExecutionAttempts } from '../components/ExecutionAttempts'
import { getSummary, getManifest } from '../services/dataService'
import { axisProps, gridProps, c } from '../theme'
import { pct } from '../utils/format'

export function Summary() {
  const s = getSummary()
  const m = getManifest()
  const sampleSub = s.sampleCount && s.sampleCount !== 'N/A'
    ? `n = ${s.sampleCount} sample${s.sampleCount === 1 ? '' : 's'}`
    : undefined

  return (
    <>
      <PageHead
        title="Executive summary"
        sub={`${m.environment} · ${m.tool} · Login + Sanity performance`}
        right={<span className="badge plain"><span className="dot" style={{ background: c.warning }} />{s.overallStatus}</span>}
      />
      <SampleBanner />
      <ExecutionAttempts />

      <StatRow>
        <StatTile
          label="Scenarios"
          value={s.scenarios.total}
          sub={[
            `${s.scenarios.passed} passed`,
            s.scenarios.degraded ? `${s.scenarios.degraded} degraded` : null,
            `${s.scenarios.failed} failed`,
            s.scenarios.notExecuted ? `${s.scenarios.notExecuted} not executed` : null,
          ].filter(Boolean).join(' · ')}
        />
        {/* Sample count sits ON the percentile tiles. At n=1 the median and p95 are the same value -
            true, meaningless, and indistinguishable from a bug unless n is visible beside it. */}
        <StatTile label="Login journey median" value={s.avgResponseMs} unit="ms" sub={sampleSub} />
        <StatTile label="Login journey p95" value={s.p95Ms} unit="ms" sub={sampleSub} />
        <StatTile label="Login journey p99" value={s.p99Ms} unit="ms" sub={sampleSub} />
        {/* Two error rates, never one. A green login rate next to failing modules is the most
            misleading thing this page could show. */}
        <StatTile
          label="Login error rate"
          value={s.loginErrorRate === 'N/A' || s.loginErrorRate == null ? 'N/A' : pct(s.loginErrorRate)}
          sub={`${s.concurrentUsers || s.activeVus} user${(s.concurrentUsers || s.activeVus) === 1 ? '' : 's'} · authentication only`}
          tone={s.loginErrorRate !== 'N/A' && s.loginErrorRate < 0.01 ? 'good' : 'bad'}
        />
        <StatTile
          label="Check failure rate"
          value={s.checkFailureRate === 'N/A' || s.checkFailureRate == null ? 'N/A' : pct(s.checkFailureRate)}
          sub="all validations, login + modules"
          tone={s.checkFailureRate !== 'N/A' && s.checkFailureRate < 0.01 ? 'good' : 'bad'}
        />
        <StatTile label="Concurrent users" value={s.concurrentUsers || s.activeVus} sub="ceiling 3" />
      </StatRow>

      <Section title="Overall performance trend" hint="p95 across recent executions">
        <ChartCard
          title="p95 response time by run"
          note="Lower is better. Populated from real executions once the suite runs."
          available={Array.isArray(s.trend) && s.trend.length > 0}
          emptyTitle="No executions yet"
          emptyDetail="The trend fills in as weekly executions accumulate."
          height={260}
          tableColumns={[{ key: 'run', header: 'Run' }, { key: 'p95', header: 'p95 (ms)', num: true }]}
          tableRows={s.trend}
          source={s.trendNote || 'A trend needs two or more comparable runs at the same profile.'}
        >
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={s.trend} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="run" {...axisProps} />
              <YAxis {...axisProps} width={48} />
              <Tooltip />
              <Line type="monotone" dataKey="p95" stroke={c.series1} strokeWidth={2.5} dot={{ r: 3 }} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>

      <Section title="What this dashboard covers">
        <Card>
          <CardHead title="Scope" note="The performance scope mirrors the functional Sanity suite." />
          <CardBody>
            <p style={{ margin: 0, color: c.inkSecondary, fontSize: 13.5, lineHeight: 1.6 }}>
              Two scenario families: <strong>Login</strong> (the authentication journey, browser and API)
              and <strong>Sanity</strong> (the {getSummary().scenarios.total - 1} modules from{' '}
              <code>CICD_Suites/SanityChecks.xml</code>). Each is measured at the UI layer (real browser)
              and the API layer (HTTP), then correlated to locate the bottleneck. Load is capped at 3
              virtual users on the shared QA account.
            </p>
          </CardBody>
        </Card>
      </Section>
    </>
  )
}
