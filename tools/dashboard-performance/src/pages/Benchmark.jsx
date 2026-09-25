import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, ComposedChart, Cell, RadialBarChart, RadialBar, PolarAngleAxis,
} from 'recharts'
import { PageHead } from '../components/AppShell'
import { Section, Card, CardHead, CardBody } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { StatTile, StatRow } from '../components/StatTile'
import { getBenchmark, getManifest } from '../services/dataService'
import { axisProps, gridProps, c } from '../theme'
import { pct } from '../utils/format'
import { sourceLabel } from '../utils/provenance'

/**
 * N-1 vs N benchmark — the management view.
 *
 * Every value here comes from the two retained run summaries. Where a comparison cannot be made the
 * cell says so; nothing is estimated. `isAnimationActive={false}` on every series because Recharts
 * under StrictMode otherwise renders a stub at the first point only.
 */

// Token names matter: theme.js exposes inkMuted/critical/baseline - there is no c.muted or
// c.danger. Passing an undefined fill makes Recharts paint the bar BLACK, which is how the
// baseline series first rendered.
const GATE_TONE = { PASS: c.series1, WARN: c.warning, FAIL: c.critical,
  INFO: c.inkMuted, 'NO BASELINE': c.inkMuted }

function GateBadge({ gate }) {
  const tone = GATE_TONE[gate] || c.inkMuted
  return (
    <span className="badge plain" style={{ borderColor: tone }}>
      <span className="dot" style={{ background: tone }} />{gate}
    </span>
  )
}

/** A delta cell that states direction in words as well as sign — a bare "-19.9" is ambiguous. */
function deltaText(d, direction) {
  if (typeof d !== 'number') return '—'
  if (d === 0) return 'no change'
  const better = direction === 'higher-better' ? d > 0 : d < 0
  return `${d > 0 ? '+' : ''}${d}%  ${better ? 'better' : 'worse'}`
}

export function Benchmark() {
  const b = getBenchmark()
  const m = getManifest()

  const numeric = (b.metrics || []).filter(
    (x) => typeof x.current === 'number' && typeof x.baseline === 'number' && x.unit === 'ms',
  )
  const deltaBars = (b.metrics || [])
    .filter((x) => typeof x.deltaPct === 'number')
    .map((x) => ({ metric: x.metric, delta: x.deltaPct, gate: x.gate, direction: x.direction }))

  const vitalsMs = (b.vitals || []).filter((v) => v.unit === 'ms' && typeof v.ms === 'number')
  const cls = (b.vitals || []).find((v) => v.unit === 'score')

  const trend = b.moduleTrend || []
  const runKeys = trend.length
    ? Object.keys(trend[0]).filter((k) => k !== 'module')
    : []

  // Coverage gauge — modules measured out of scope, as a single honest ratio.
  const measured = (b.metrics || []).find((x) => x.metric === 'Modules measured')
  const totalMods = measured ? Number(String(measured.unit).replace('of ', '')) : null
  const gaugeData = (measured && totalMods)
    ? [{ name: 'measured', value: Math.round((Number(measured.current) / totalMods) * 100) }]
    : []

  return (
    <>
      <PageHead
        title="N-1 vs N benchmark"
        sub={`${m.baselineRunId} → ${m.currentRunId} · ${m.environment} · build ${m.buildTag || 'n/a'}`}
        right={<GateBadge gate={b.gate} />}
      />

      <Card>
        <CardHead title="Regression gate" hint={b.gateBasis} />
        <CardBody>
          <p style={{ margin: 0, fontSize: 14 }}>
            <strong>{b.gate}</strong> — {(b.gateReasons || []).join('; ')}.
          </p>
          {b.contaminationNote && (
            <p style={{ margin: '10px 0 0', fontSize: 13, color: c.inkMuted }}>
              ⚠️ {b.contaminationNote}
            </p>
          )}
        </CardBody>
      </Card>

      <StatRow>
        {(b.metrics || []).slice(0, 4).map((x) => (
          <StatTile
            key={x.metric}
            label={x.metric}
            value={x.current}
            unit={x.unit === 'ms' ? 'ms' : ''}
            sub={`N-1 ${x.baseline} · ${deltaText(x.deltaPct, x.direction)}`}
            tone={x.gate === 'FAIL' ? 'bad' : x.gate === 'PASS' ? 'good' : undefined}
          />
        ))}
      </StatRow>

      <Section title="Response time: N-1 against N" hint="Lower is better on every series here">
        <ChartCard
          title="Latency comparison"
          note="Each pair is the same measurement in the previous execution and the current one."
          available={numeric.length > 0}
          emptyTitle="No comparable latency metrics"
          emptyDetail="A comparison needs both executions to have measured the same segment."
          height={300}
          tableColumns={[
            { key: 'metric', header: 'Metric' },
            { key: 'baseline', header: 'N-1 (ms)', num: true },
            { key: 'current', header: 'N (ms)', num: true },
            { key: 'deltaPct', header: 'Change %', num: true },
            { key: 'gate', header: 'Gate' },
          ]}
          tableRows={b.metrics}
          source={sourceLabel(b)}
        >
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={numeric} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="metric" {...axisProps} interval={0} height={54} />
              <YAxis {...axisProps} width={64} unit="ms" />
              <Tooltip />
              <Legend />
              <Bar dataKey="baseline" name="N-1 (previous)" fill={c.baseline} isAnimationActive={false} />
              <Bar dataKey="current" name="N (current)" fill={c.series1} isAnimationActive={false} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>

      <Section title="Change per metric" hint="Bars below the axis are improvements">
        <ChartCard
          title="Percentage change, N vs N-1"
          note="Coloured by gate: blue passed, amber warning, red failed."
          available={deltaBars.length > 0}
          emptyTitle="No deltas available"
          emptyDetail="Deltas need a baseline execution."
          height={280}
          tableColumns={[
            { key: 'metric', header: 'Metric' },
            { key: 'delta', header: 'Change %', num: true },
            { key: 'gate', header: 'Gate' },
          ]}
          tableRows={deltaBars}
          source={sourceLabel(b)}
        >
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={deltaBars} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="metric" {...axisProps} interval={0} height={54} />
              <YAxis {...axisProps} width={56} unit="%" />
              <Tooltip />
              <Bar dataKey="delta" name="change %" isAnimationActive={false}>
                {deltaBars.map((row, i) => (
                  <Cell key={i} fill={GATE_TONE[row.gate] || c.series1} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>

      <Section title="Browser Web Vitals" hint="Captured by k6 during the browser phase">
        <ChartCard
          title="Core Web Vitals, N-1 against N"
          note="LCP, FCP and TTFB in milliseconds. CLS is a unitless score and is shown separately below."
          available={vitalsMs.length > 0}
          emptyTitle="Web Vitals not captured"
          emptyDetail="k6 emits browser_web_vital_* only for browser scenarios."
          height={280}
          tableColumns={[
            { key: 'metric', header: 'Vital' },
            { key: 'baseline', header: 'N-1', num: true },
            { key: 'ms', header: 'N', num: true },
            { key: 'p95', header: 'N p95', num: true },
            { key: 'deltaPct', header: 'Change %', num: true },
            { key: 'gate', header: 'Gate' },
          ]}
          tableRows={b.vitals}
          source={sourceLabel(b)}
        >
          <ResponsiveContainer width="100%" height={280}>
            <ComposedChart data={vitalsMs} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="metric" {...axisProps} />
              <YAxis {...axisProps} width={64} unit="ms" />
              <Tooltip />
              <Legend />
              <Bar dataKey="baseline" name="N-1 avg" fill={c.baseline} isAnimationActive={false} />
              <Bar dataKey="ms" name="N avg" fill={c.series1} isAnimationActive={false} />
              <Line type="monotone" dataKey="p95" name="N p95" stroke={c.series2}
                strokeWidth={2.5} dot={{ r: 3 }} isAnimationActive={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </ChartCard>
        {cls && (
          <Card>
            <CardHead title="Cumulative Layout Shift" hint="Unitless score — lower is better" />
            <CardBody>
              <StatRow>
                <StatTile label="CLS (N)" value={cls.ms} sub={`N-1 ${cls.baseline}`}
                  tone={cls.gate === 'FAIL' ? 'bad' : 'good'} />
                <StatTile label="CLS p95" value={cls.p95} />
                <StatTile label="Change" value={deltaText(cls.deltaPct, 'lower-better')} />
              </StatRow>
            </CardBody>
          </Card>
        )}
      </Section>

      <Section title="Module load trend" hint="Average load per module, per retained execution">
        <ChartCard
          title="Module load, N-1 against N"
          note="Only modules measured in the current execution appear. A module the sweep did not reach is absent rather than shown as zero."
          available={trend.length > 0 && runKeys.length > 0}
          emptyTitle="No module trend yet"
          emptyDetail="A trend needs at least one module measured in both retained executions."
          height={340}
          tableColumns={[{ key: 'module', header: 'Module' },
            ...runKeys.map((k) => ({ key: k, header: k, num: true }))]}
          tableRows={trend}
          source={sourceLabel(b)}
        >
          <ResponsiveContainer width="100%" height={340}>
            <BarChart data={trend} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
              <CartesianGrid {...gridProps} />
              <XAxis dataKey="module" {...axisProps} interval={0} height={70} angle={-30}
                textAnchor="end" />
              <YAxis {...axisProps} width={64} unit="ms" />
              <Tooltip />
              <Legend />
              {runKeys.map((k, i) => (
                <Bar key={k} dataKey={k} name={k}
                  fill={i === runKeys.length - 1 ? c.series1 : c.baseline}
                  isAnimationActive={false} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>

      <Section title="Regressions and improvements" hint="Baseline-relative, per module">
        <div className="grid grid-2">
          <ChartCard
            title="Slower than N-1"
            note={`Flagged above ${b.gateBasis ? '15%' : ''} — amber warning, red failure.`}
            available={(b.moduleRegressions || []).length > 0}
            emptyTitle="No module regressed"
            emptyDetail="No measured module was more than 15% slower than in N-1."
            height={240}
            tableColumns={[{ key: 'module', header: 'Module' },
              { key: 'baselineMs', header: 'N-1 (ms)', num: true },
              { key: 'currentMs', header: 'N (ms)', num: true },
              { key: 'deltaPct', header: 'Change %', num: true },
              { key: 'gate', header: 'Gate' }]}
            tableRows={b.moduleRegressions}
            source={sourceLabel(b)}
          >
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={b.moduleRegressions} layout="vertical"
                margin={{ top: 8, right: 16, bottom: 4, left: 8 }}>
                <CartesianGrid {...gridProps} />
                <XAxis type="number" {...axisProps} unit="%" />
                <YAxis type="category" dataKey="module" {...axisProps} width={132} />
                <Tooltip />
                <Bar dataKey="deltaPct" name="slower by %" isAnimationActive={false}>
                  {(b.moduleRegressions || []).map((row, i) => (
                    <Cell key={i} fill={GATE_TONE[row.gate] || c.warning} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard
            title="Faster than N-1"
            note="Modules at least 10% faster than the previous execution."
            available={(b.moduleImprovements || []).length > 0}
            emptyTitle="No module improved by 10% or more"
            emptyDetail="Improvements below the 10% threshold are not listed."
            height={240}
            tableColumns={[{ key: 'module', header: 'Module' },
              { key: 'baselineMs', header: 'N-1 (ms)', num: true },
              { key: 'currentMs', header: 'N (ms)', num: true },
              { key: 'deltaPct', header: 'Change %', num: true }]}
            tableRows={b.moduleImprovements}
            source={sourceLabel(b)}
          >
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={b.moduleImprovements} layout="vertical"
                margin={{ top: 8, right: 16, bottom: 4, left: 8 }}>
                <CartesianGrid {...gridProps} />
                <XAxis type="number" {...axisProps} unit="%" />
                <YAxis type="category" dataKey="module" {...axisProps} width={132} />
                <Tooltip />
                <Bar dataKey="deltaPct" name="change %" fill={c.series3} isAnimationActive={false} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>
      </Section>

      {gaugeData.length > 0 && (
        <Section title="Scope coverage" hint="Modules measured in the current execution">
          <Card>
            <CardHead title="Measured share of the sanity scope"
              hint={`${measured.current} of ${totalMods} modules. Coverage is reported, never inferred.`} />
            <CardBody>
              <ResponsiveContainer width="100%" height={200}>
                <RadialBarChart data={gaugeData} innerRadius="66%" outerRadius="100%"
                  startAngle={180} endAngle={0}>
                  <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
                  <RadialBar dataKey="value" cornerRadius={6} fill={c.series1}
                    isAnimationActive={false} background />
                </RadialBarChart>
              </ResponsiveContainer>
              <p style={{ margin: 0, textAlign: 'center', fontSize: 26, fontWeight: 700 }}>
                {gaugeData[0].value}%
              </p>
              <p style={{ margin: '4px 0 0', textAlign: 'center', fontSize: 13, color: c.inkMuted }}>
                {measured.current} of {totalMods} modules measured
              </p>
            </CardBody>
          </Card>
        </Section>
      )}
    </>
  )
}
