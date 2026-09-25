import { PageHead } from '../components/AppShell'
import { Card, CardBody, CardFoot, CardHead, Section } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { DataTable } from '../components/DataTable'
import { DeltaPill, HeroFigure, TrendBadge } from '../components/Indicators'
import { EmptyState } from '../components/States'
import { CompareBars } from '../charts/CompareBars'
import {
  getBenchmark, getBenchmarkGroups, getComparableMetrics, getImprovements, getRun, getScenarios,
} from '../services/dataService'
import { c } from '../theme'
import { isNA, num, pct, runLabel } from '../utils/format'

const SCALE_METRICS = ['Total flows', 'Test cases planned', 'Executed', 'Passed', 'Failed']
const LATENCY_METRICS = ['Latency mean (ms)', 'Latency median (ms)', 'Latency p95 (ms)']

/** Shorten a metric name for an axis tick without losing which metric it is. */
const shortLabel = (m) => {
  const s = m
    .replace('Test cases ', '')
    .replace('Latency ', '')
    .replace(' (ms)', '')
    .replace('Total ', '')
  return s.charAt(0).toUpperCase() + s.slice(1)
}

export function Benchmark() {
  const bench = getBenchmark()
  const groups = getBenchmarkGroups()
  const scenarios = getScenarios()
  const reg = bench.regression
  const improvements = getImprovements()
  const current = getRun(bench.currentRunId)
  const previous = getRun(bench.previousRunId)

  const scaleData = getComparableMetrics(SCALE_METRICS).map((m) => ({ ...m, metric: shortLabel(m.metric) }))
  const latencyData = getComparableMetrics(LATENCY_METRICS).map((m) => ({ ...m, metric: shortLabel(m.metric) }))
  const scenarioData = scenarios.map((s) => ({
    metric: s.scenario,
    previous: s.previousExecuted,
    current: s.executed,
    rate: s.successRate,
  }))

  const maxRow = bench.metrics.find((m) => m.metric === 'Latency max (ms)')

  return (
    <div className="page">
      <PageHead
        title="Execution benchmark — previous vs current"
        sub={`N-1 is ${runLabel(bench.previousRunId)}; N is ${runLabel(bench.currentRunId)}. Both ran live against ${current.environment} through the same engine, so the comparison is like-for-like.`}
        right={bench.trend
          ? <TrendBadge level={bench.trendLevel}>{bench.trend}</TrendBadge>
          : <span className="chip">Analysis pending for this execution</span>}
      />

      {/* ── hero: did the product move? ─────────────────────────────────── */}
      <HeroFigure
        label="Comparable test cases that came back unchanged"
        value={reg.unchanged}
        unit={`of ${num(reg.comparable)}`}
        delta={
          <p className="prose" style={{ marginTop: 9, maxWidth: '62ch' }}>
            One case moved each way — <strong>{num(reg.fixed)} fixed</strong> and{' '}
            <strong>{num(reg.regressed)} newly failing</strong> out of {num(reg.comparable)}. That is noise,
            not a trend: the product did not move between these two executions.
          </p>
        }
        note={`${num(reg.added)} test cases are new in this run and ${num(reg.retired)} were retired, so the rest of the comparison is about added coverage rather than changed behaviour.`}
      >
        <span className="chip">{num(reg.comparable)} comparable</span>
      </HeroFigure>

      <Section>
        <Card>
          <CardHead title="What happened, in one paragraph" />
          <CardBody>
            {bench.outcome ? (
              <p className="prose">{bench.outcome}</p>
            ) : (
              <EmptyState
                title="No authored summary for this execution"
                detail={`The narrative on record was written about run ${bench.authoredNarrativeFor}. Every measured figure on this page is current and comes from this run's own workbook; only the prose is withheld, because it describes a different execution.`}
                inline
              />
            )}
          </CardBody>
          <CardFoot>
            {bench.outcome ? 'Authored summary' : 'Measured figures'} — {bench.source}
          </CardFoot>
        </Card>
      </Section>

      {/* ── scale + latency: two charts, never two axes on one ──────────── */}
      <Section title="Execution and outcome comparison">
        <div className="grid grid-2">
          <ChartCard
            title="Scale and outcome"
            note="Volume of work and how it resolved. Counts only — latency is a separate chart because its scale is unrelated."
            legend={[
              { label: 'N-1 (previous)', color: c.series2 },
              { label: 'N (current)', color: c.series1 },
            ]}
            tableColumns={[
              { key: 'metric', header: 'Metric' },
              { key: 'previous', header: 'N-1', num: true, render: (r) => num(r.previous) },
              { key: 'current', header: 'N', num: true, render: (r) => num(r.current) },
              {
                key: 'delta',
                header: 'Change',
                num: true,
                render: (r) => <DeltaPill current={r.current} previous={r.previous} direction="up-good" showPct={false} />,
              },
            ]}
            tableRows={scaleData}
            source="Source: run workbook, sheet 'Execution Benchmark'"
          >
            <CompareBars data={scaleData} height={264} />
          </ChartCard>

          <ChartCard
            title="Response-time comparison (ms)"
            note={`Inter-call pacing differed between runs — 5,000 ms then 2,000 ms — so latency is comparable but throughput is not. Slowest single call: ${num(maxRow?.previousNum)} ms then ${num(maxRow?.currentNum)} ms.`}
            legend={[
              { label: 'N-1 (previous)', color: c.series2 },
              { label: 'N (current)', color: c.series1 },
            ]}
            tableColumns={[
              { key: 'metric', header: 'Statistic' },
              { key: 'previous', header: 'N-1 (ms)', num: true, render: (r) => num(r.previous) },
              { key: 'current', header: 'N (ms)', num: true, render: (r) => num(r.current) },
              {
                key: 'delta',
                header: 'Change',
                num: true,
                render: (r) => <DeltaPill current={r.current} previous={r.previous} direction="down-good" showPct={false} />,
              },
            ]}
            tableRows={latencyData}
            source="Source: run workbook, latency rows of 'Execution Benchmark'"
          >
            <CompareBars data={latencyData} height={264} />
          </ChartCard>
        </div>
      </Section>

      {/* ── scenario comparison ────────────────────────────────────────── */}
      <Section title="Coverage added by dimension">
        <ChartCard
          title="Test cases executed per dimension"
          note="Only the Chain dimension existed in the previous run. The other four are new — which is why the aggregate pass rate is flat while coverage nearly tripled."
          legend={[
            { label: 'N-1 (previous)', color: c.series2 },
            { label: 'N (current)', color: c.series1 },
          ]}
          tableColumns={[
            { key: 'metric', header: 'Dimension' },
            { key: 'previous', header: 'N-1', num: true, render: (r) => num(r.previous) },
            { key: 'current', header: 'N', num: true, render: (r) => num(r.current) },
            { key: 'rate', header: 'Pass rate (N)', num: true, render: (r) => pct(r.rate) },
          ]}
          tableRows={scenarioData}
          source="Source: run workbook, sheets 'Scenario Coverage' and 'Execution Benchmark'"
        >
          <CompareBars
            data={scenarioData}
            horizontal
            height={250}
            note={(row) => `${pct(row.rate)} of the current run's cases passed in this dimension`}
          />
        </ChartCard>
      </Section>

      {/* ── new vs resolved ────────────────────────────────────────────── */}
      <Section title="Newly identified, and resolved">
        <div className="grid grid-2">
          <Card>
            <CardHead
              title="Product movement between the two executions"
              note={reg.note}
            />
            <CardBody>
              <DataTable
                compact
                columns={[
                  { key: 'k', header: 'Measure' },
                  { key: 'v', header: 'Test cases', num: true, render: (r) => num(r.v) },
                ]}
                rows={[
                  { id: 'c', k: 'Comparable — same endpoint, verb and scenario', v: reg.comparable },
                  { id: 'u', k: 'Unchanged', v: reg.unchanged },
                  { id: 'f', k: 'Fixed (failed before, passes now)', v: reg.fixed },
                  { id: 'r', k: 'Newly failing (passed before, fails now)', v: reg.regressed },
                  { id: 'a', k: 'Newly added — absent from N-1', v: reg.added },
                  { id: 't', k: 'Retired since N-1', v: reg.retired },
                ]}
              />
            </CardBody>
            <CardFoot>
              The baseline was re-scored under the current validator before comparing — 1,868 hops
              re-judged from stored responses with zero HTTP calls, and no verdict changed.
            </CardFoot>
          </Card>

          <Card>
            <CardHead
              title={`Framework defects found and fixed during the run — ${improvements.frameworkDefectsFixed.length}`}
              note="Improvements to the test platform itself, not to the product under test."
            />
            <CardBody>
              <DataTable
                compact
                columns={[
                  { key: 'n', header: '#', width: '32px' },
                  { key: 'defect', header: 'Defect' },
                  { key: 'impact', header: 'Impact' },
                ]}
                rows={improvements.frameworkDefectsFixed}
                rowKey={(r) => r.n}
              />
            </CardBody>
            <CardFoot>Source: {improvements.source}</CardFoot>
          </Card>
        </div>
      </Section>

      {/* ── recommendations ────────────────────────────────────────────── */}
      <Section title="Recommended actions">
        <Card>
          <CardHead
            title={`${improvements.recommendations.length} recommendations, in the order they should be taken`}
            note="Ordered by the benchmark's own priority ranking."
          />
          <CardBody>
            <DataTable
              compact
              columns={[
                { key: 'priority', header: '#', width: '34px' },
                { key: 'action', header: 'Action' },
              ]}
              rows={improvements.recommendations}
              rowKey={(r) => r.priority}
            />
          </CardBody>
        </Card>
      </Section>

      {/* ── the full metric table ──────────────────────────────────────── */}
      <Section
        title="Every benchmark metric"
        hint="a metric the previous run never captured reads N/A — it is never dropped or back-filled"
      >
        <div className="stack">
          {groups.map((g) => (
            <Card key={g.group}>
              <CardHead title={g.group} as="h3" />
              <CardBody>
                <DataTable
                  compact
                  columns={[
                    {
                      key: 'metric',
                      header: 'Metric',
                      render: (r) => (
                        <span style={{ paddingLeft: r.indent ? 14 : 0, color: r.indent ? c.inkSecondary : undefined }}>
                          {r.metric}
                        </span>
                      ),
                    },
                    { key: 'previous', header: 'N-1 (previous)', num: true },
                    { key: 'current', header: 'N (current)', num: true },
                    {
                      key: 'delta',
                      header: 'Change',
                      num: true,
                      render: (r) => (isNA(r.delta) || !r.delta ? <span className="na">—</span> : r.delta),
                    },
                    { key: 'note', header: 'Note', render: (r) => <span style={{ color: c.inkSecondary }}>{r.note || '—'}</span> },
                  ]}
                  rows={g.rows}
                  rowKey={(r, i) => `${r.metric}-${i}`}
                />
              </CardBody>
            </Card>
          ))}
        </div>
      </Section>

      <p className="prov" style={{ marginTop: 16 }}>
        Baseline run folder <code>{previous.runFolder}</code> · current run folder{' '}
        <code>{current.runFolder}</code>
      </p>
    </div>
  )
}
