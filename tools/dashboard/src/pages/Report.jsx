import { Card, CardBody, CardFoot, CardHead, Section } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { DataTable } from '../components/DataTable'
import {
  Callout, DeltaPill, SeverityBadge, StatusBadge, TrendBadge,
} from '../components/Indicators'
import { EmptyState } from '../components/States'
import { CompareBars } from '../charts/CompareBars'
import { OutcomeDonut } from '../charts/OutcomeDonut'
import { RankedBars } from '../charts/RankedBars'
import {
  getBenchmark, getExclusions, getFailures, getGates, getImprovements, getKpis,
  getPrimaryFindingSet, getReport, getRun, getRunCapabilities, getSlowestModules,
  getModulesByFailures, getScenarios,
} from '../services/dataService'
import { c } from '../theme'
import { isNA, minutes, niceDate, num, pct, runLabel } from '../utils/format'
import { navigate } from '../utils/router'

/**
 * The management report for one execution.
 *
 * Every section degrades honestly: a run that never produced module-level or benchmark data
 * shows an empty state naming what is missing, rather than an empty chart or a zero.
 */
export function Report({ runId }) {
  const report = getReport(runId)
  const run = getRun(runId)

  if (!report || !run) {
    return (
      <div className="page">
        <Card>
          <CardBody>
            <EmptyState
              title="No such execution"
              detail={`No run folder named "${runId}" is recorded. Pick one from the execution history.`}
              icon="?"
            />
            <div style={{ textAlign: 'center' }}>
              <button className="link-btn" onClick={() => navigate('history')}>← Execution history</button>
            </div>
          </CardBody>
        </Card>
      </div>
    )
  }

  const cap = getRunCapabilities(runId)
  const bench = getBenchmark()
  const kpis = getKpis()
  const gates = getGates()
  const failures = getFailures()
  const exclusions = getExclusions()
  const improvements = getImprovements()
  const findingSet = getPrimaryFindingSet()
  const scenarios = getScenarios()
  const baseline = getRun(bench.previousRunId)
  const isCurrent = run.isCurrent

  return (
    <div className="page">
      <button className="link-btn" onClick={() => navigate('history')} style={{ marginBottom: 12 }}>
        ← Execution history
      </button>

      {/* ── report header ───────────────────────────────────────────────── */}
      <Card>
        <div className="report-head">
          <div>
            <h1>Execution report — {niceDate(report.date)}</h1>
            <dl className="kv" style={{ marginTop: 8 }}>
              <dt>Project</dt><dd>{report.projectName}</dd>
              <dt>Execution</dt><dd>{runLabel(run.id)}</dd>
              <dt>Environment</dt><dd>{report.scope.environment}</dd>
              <dt>Type</dt><dd>{report.scope.type}</dd>
              <dt>Result</dt><dd><StatusBadge status={report.overallResult} /></dd>
            </dl>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 9, alignItems: 'flex-end' }}>
            {isCurrent && bench.trend && <TrendBadge level={bench.trendLevel}>{bench.trend}</TrendBadge>}
            <span className="chip">{num(report.evidenceFiles)} evidence files retained</span>
            {cap.hasResults && <span className="chip">{gates.passed} of {gates.total} validation gates passed</span>}
          </div>
        </div>
      </Card>

      {/* ── scope ──────────────────────────────────────────────────────── */}
      <Section title="Scope">
        <Card>
          <CardBody>
            <dl className="kv" style={{ gridTemplateColumns: 'minmax(150px, auto) 1fr' }}>
              <dt>Engine</dt><dd style={{ fontWeight: 400 }}>{report.scope.engine}</dd>
              <dt>Java / TestNG suite run?</dt>
              <dd style={{ fontWeight: 400 }}>
                No — the bootstrap project was read as a generation input only.
              </dd>
              <dt>Mode</dt><dd style={{ fontWeight: 400 }}>{report.scope.mode}</dd>
              <dt>Flows generated</dt><dd style={{ fontWeight: 400 }}>{num(report.scope.flows)}</dd>
              <dt>Distinct endpoints reached</dt><dd style={{ fontWeight: 400 }}>{num(report.scope.endpointsReached)}</dd>
              <dt>Run folder</dt><dd style={{ fontWeight: 400 }}><code>{report.runFolder}</code></dd>
            </dl>
          </CardBody>
        </Card>
      </Section>

      {/* ── summary ────────────────────────────────────────────────────── */}
      <Section title="Execution summary">
        {!cap.hasResults ? (
          <Card>
            <CardBody>
              <EmptyState
                title="This execution produced no test-case results"
                detail={report.note || 'The run aborted before writing a results file. It is retained so the history is complete.'}
                inline
              />
            </CardBody>
          </Card>
        ) : (
          <>
            <div className="grid grid-kpi" style={{ marginBottom: 14 }}>
              <SummaryTile label="Test cases reached" value={report.summary.total} />
              <SummaryTile label="Executed" value={report.summary.executed} />
              <SummaryTile label="Passed" value={report.summary.passed} previous={isCurrent ? baseline?.passed : null} direction="up-good" />
              <SummaryTile label="Failed" value={report.summary.failed} previous={isCurrent ? baseline?.failed : null} direction="down-good" />
              <SummaryTile label="Blocked (withheld)" value={report.summary.blocked} />
              <SummaryTile label="Success rate" value={report.summary.successRate} unit="%" previous={isCurrent ? baseline?.successRate : null} direction="up-good" />
            </div>

            <div className="grid grid-2">
              <ChartCard
                title="Outcome"
                note="Blocked test cases were withheld by a safety guard, and are never counted as passes."
                legend={[
                  { label: 'Passed', color: c.series1 },
                  { label: 'Failed', color: c.critical },
                  { label: 'Blocked', color: c.neutral },
                ]}
                tableColumns={[
                  { key: 'name', header: 'Outcome' },
                  { key: 'value', header: 'Test cases', num: true, render: (r) => num(r.value) },
                ]}
                tableRows={[
                  { name: 'Passed', value: report.summary.passed },
                  { name: 'Failed', value: report.summary.failed },
                  { name: 'Blocked', value: report.summary.blocked },
                ]}
              >
                <OutcomeDonut
                  data={[
                    { name: 'Passed', value: report.summary.passed },
                    { name: 'Failed', value: report.summary.failed },
                    { name: 'Blocked', value: report.summary.blocked },
                  ]}
                />
              </ChartCard>

              <Card>
                <CardHead title="Duration and stability" />
                <CardBody>
                  <DataTable
                    compact
                    columns={[
                      { key: 'k', header: 'Measure' },
                      { key: 'v', header: 'Value', num: true },
                    ]}
                    rows={[
                      { id: 'd', k: 'Elapsed', v: minutes(report.summary.durationMin) },
                      { id: 'f', k: 'Flows passed', v: num(report.summary.flowsPassed) },
                      { id: 'g', k: 'Flows failed', v: num(report.summary.flowsFailed) },
                      {
                        id: 'p',
                        k: 'Environment downtime pauses',
                        v: isNA(report.summary.downtimePauses) ? 'N/A' : num(report.summary.downtimePauses),
                      },
                    ]}
                  />
                  <p className="prov" style={{ marginTop: 10 }}>
                    Duration basis: {report.summary.durationBasis}.
                  </p>
                </CardBody>
              </Card>
            </div>
          </>
        )}
      </Section>

      {/* ── benchmark ──────────────────────────────────────────────────── */}
      <Section title="Benchmark comparison">
        {!cap.hasBenchmark ? (
          <Card>
            <CardBody>
              <EmptyState
                title="No benchmark for this execution"
                detail="A previous-vs-current benchmark exists only for the latest full execution, which is the only run with a like-for-like baseline behind it."
                inline
              />
              <div style={{ textAlign: 'center' }}>
                <button className="link-btn" onClick={() => navigate('benchmark')}>See the current benchmark →</button>
              </div>
            </CardBody>
          </Card>
        ) : (
          <ChartCard
            title="Previous execution vs this one"
            note={`Baseline: ${runLabel(bench.previousRunId)}. Both ran live through the same engine against the same environment.`}
            legend={[
              { label: 'N-1 (previous)', color: c.series2 },
              { label: 'N (this run)', color: c.series1 },
            ]}
            tableColumns={[
              { key: 'metric', header: 'Measure' },
              { key: 'previous', header: 'Previous', num: true, render: (r) => num(r.previous) },
              { key: 'current', header: 'This run', num: true, render: (r) => num(r.current) },
            ]}
            tableRows={[
              { metric: 'Executed', previous: baseline?.executed, current: run.executed },
              { metric: 'Passed', previous: baseline?.passed, current: run.passed },
              { metric: 'Failed', previous: baseline?.failed, current: run.failed },
              { metric: 'Endpoints', previous: baseline?.distinctEndpoints, current: run.distinctEndpoints },
            ]}
            source={`Full detail on the Benchmark page. ${bench.source}`}
          >
            <CompareBars
              data={[
                { metric: 'Executed', previous: baseline?.executed, current: run.executed },
                { metric: 'Passed', previous: baseline?.passed, current: run.passed },
                { metric: 'Failed', previous: baseline?.failed, current: run.failed },
                { metric: 'Endpoints', previous: baseline?.distinctEndpoints, current: run.distinctEndpoints },
              ]}
              currentName="N (this run)"
              height={250}
            />
          </ChartCard>
        )}
      </Section>

      {/* ── performance ────────────────────────────────────────────────── */}
      <Section title="Performance">
        {!cap.hasPerformance ? (
          <Card><CardBody><EmptyState title="No response times captured for this execution" inline /></CardBody></Card>
        ) : (
          <div className="grid grid-2">
            <Card>
              <CardHead title="Response time" note="Measured on every executed call." />
              <CardBody>
                <DataTable
                  compact
                  columns={[
                    { key: 'k', header: 'Statistic' },
                    { key: 'v', header: 'ms', num: true, render: (r) => num(r.v) },
                    {
                      key: 'd',
                      header: isCurrent ? 'vs N-1' : '',
                      num: true,
                      render: (r) => (isCurrent && r.p != null
                        ? <DeltaPill current={r.v} previous={r.p} direction="down-good" showPct={false} />
                        : null),
                    },
                  ]}
                  rows={[
                    { id: 'm', k: 'Mean', v: report.performance.meanMs, p: isCurrent ? baseline?.latencyMeanMs : null },
                    { id: 'd', k: 'Median', v: report.performance.medianMs, p: isCurrent ? baseline?.latencyMedianMs : null },
                    { id: 'p', k: '95th percentile', v: report.performance.p95Ms, p: isCurrent ? baseline?.latencyP95Ms : null },
                  ]}
                />
              </CardBody>
            </Card>

            <ChartCard
              title="Slowest modules by 95th percentile"
              note="Modules with at least three executed calls. The 95th percentile is the figure users actually feel."
              available={cap.hasModuleBreakdown}
              emptyTitle="No module breakdown for this execution"
              emptyDetail="The per-module workbook is produced only for the latest full execution."
              tableColumns={[
                { key: 'module', header: 'Module' },
                { key: 'count', header: 'Calls', num: true },
                { key: 'medianMs', header: 'Median ms', num: true, render: (r) => num(r.medianMs) },
                { key: 'p95Ms', header: 'p95 ms', num: true, render: (r) => num(r.p95Ms) },
              ]}
              tableRows={getSlowestModules(12)}
              source="Source: run workbook, sheet 'Performance'"
            >
              <RankedBars
                data={getSlowestModules(10).map((m) => ({ name: m.module, value: m.p95Ms, count: m.count }))}
                valueName="p95"
                unit="ms"
                height={276}
                axisWidth={168}
                note={(row) => `${num(row.count)} calls measured`}
              />
            </ChartCard>
          </div>
        )}
      </Section>

      {/* ── findings ───────────────────────────────────────────────────── */}
      <Section title="Findings">
        {isCurrent && kpis.headlinesApply && (
          <div className="grid grid-3" style={{ marginBottom: 14 }}>
            {kpis.headlines.map((h) => (
              <Callout
                key={h.label}
                label={h.label}
                value={h.value}
                unit={h.unit}
                detail={h.detail}
                source={h.source}
                tone={h.label.includes('Environment') ? 'warn' : 'flag'}
              />
            ))}
          </div>
        )}

        <div className="grid grid-2">
          <Card>
            <CardHead
              title={`${report.findingsCount} finding${report.findingsCount === 1 ? '' : 's'} sourced from this execution's evidence`}
              note="A finding is attributed to the run whose retained responses prove it."
            />
            <CardBody>
              {report.findingsCount === 0 ? (
                <EmptyState
                  title="No finding is sourced from this execution"
                  detail="Findings are pinned to the run that evidences them; this run's evidence does not underpin one."
                  inline
                />
              ) : (
                <DataTable
                  compact
                  columns={[
                    { key: 'id', header: 'ID', render: (r) => <span className="chip mono">{r.id}</span> },
                    { key: 'title', header: 'Finding' },
                    { key: 'severity', header: 'Severity', render: (r) => <SeverityBadge severity={r.severity} label={r.severityLabel} /> },
                  ]}
                  rows={findingSet.items.filter((f) => (report.findingIds || []).includes(f.id))}
                  rowKey={(r) => r.id}
                />
              )}
            </CardBody>
            <CardFoot>
              <button className="link-btn" onClick={() => navigate('findings')}>All findings and severities →</button>
            </CardFoot>
          </Card>

          <ChartCard
            title="Which validation layer caught each failure"
            note="Twelve layers exist; these are the ones that fired. A status-code-only check would have caught none of the envelope failures."
            available={isCurrent}
            emptyTitle="No layer breakdown for this execution"
            emptyDetail="The failure analysis is produced for the latest full execution."
            tableColumns={[
              { key: 'layer', header: 'Failing layer' },
              { key: 'hops', header: 'Test cases', num: true, render: (r) => num(r.hops) },
            ]}
            tableRows={failures.layers}
            source="Source: run workbook, sheet 'Failure Analysis'"
          >
            <RankedBars
              data={failures.layers.map((l) => ({ name: l.layer, value: l.hops }))}
              valueName="Failures"
              height={252}
              axisWidth={150}
            />
          </ChartCard>
        </div>
      </Section>

      {/* ── improvements ───────────────────────────────────────────────── */}
      {isCurrent && (
        <Section title="Improvements identified">
          <div className="grid grid-2">
            <Card>
              <CardHead
                title="Where the failures concentrate"
                note="The ten modules carrying the most failures — the shortest path to a higher pass rate."
              />
              <CardBody>
                <DataTable
                  compact
                  columns={[
                    { key: 'module', header: 'Module' },
                    { key: 'executed', header: 'Executed', num: true },
                    { key: 'failed', header: 'Failed', num: true },
                    { key: 'successRate', header: 'Rate', num: true, render: (r) => pct(r.successRate) },
                  ]}
                  rows={getModulesByFailures(10)}
                  rowKey={(r) => r.module}
                />
              </CardBody>
            </Card>

            <Card>
              <CardHead
                title={`Framework defects fixed during this run — ${improvements.frameworkDefectsFixed.length}`}
                note="Found and corrected in the test platform while the run was in progress."
              />
              <CardBody>
                <DataTable
                  compact
                  columns={[
                    { key: 'n', header: '#', width: '30px' },
                    { key: 'defect', header: 'Defect' },
                  ]}
                  rows={improvements.frameworkDefectsFixed}
                  rowKey={(r) => r.n}
                />
              </CardBody>
            </Card>
          </div>
        </Section>
      )}

      {/* ── exclusions ─────────────────────────────────────────────────── */}
      {isCurrent && (
        <Section title="What was deliberately not executed" hint="nothing is silently skipped">
          <ChartCard
            title={`${num(exclusions.withheldAtGenerationTime)} test rows withheld before the run, ${num(exclusions.withheldAtCallTime)} refused during it`}
            note={exclusions.note}
            tableColumns={[
              { key: 'item', header: 'Class' },
              { key: 'count', header: 'Test rows', num: true, render: (r) => num(r.count) },
            ]}
            tableRows={exclusions.byClass}
            source="Source: run workbook, sheet 'Blocked and Exclusions'"
          >
            <RankedBars
              data={exclusions.byClass.map((x) => ({ name: x.item, value: x.count }))}
              valueName="Test rows"
              height={196}
              axisWidth={168}
            />
          </ChartCard>
        </Section>
      )}

      {/* ── observations & conclusion ──────────────────────────────────── */}
      <Section title="Key observations and conclusion">
        <Card>
          <CardBody>
            {report.outcome ? (
              <>
                <p className="prose">{report.outcome}</p>
                <ul className="bullets" style={{ marginTop: 12 }}>
                  {(report.observations || []).map((o) => <li key={o}>{o}</li>)}
                </ul>
                {report.conclusion && (
                  <p className="prose" style={{ marginTop: 12, fontWeight: 550 }}>
                    Conclusion: {report.conclusion}
                  </p>
                )}
              </>
            ) : (
              <EmptyState
                title="No authored narrative for this execution"
                detail={
                  cap.hasResults
                    ? 'Only the latest full execution has an authored summary. The measured figures above are complete.'
                    : report.note || 'This run wrote no results.'
                }
                inline
              />
            )}
          </CardBody>
          {isCurrent && (
            <CardFoot>
              Validation gates: {report.gatesPassed} passed · scenario coverage across{' '}
              {scenarios.length} dimensions · {num(report.evidenceFiles)} retained evidence files.
            </CardFoot>
          )}
        </Card>
      </Section>
    </div>
  )
}

function SummaryTile({ label, value, unit = '', previous, direction = 'neutral' }) {
  return (
    <div className="card tile">
      <span className="tile-label">{label}</span>
      <div className="tile-value-row">
        {isNA(value)
          ? <span className="tile-na">N/A</span>
          : <span className="tile-value">{unit === '%' ? pct(value) : num(value)}</span>}
        {previous != null && !isNA(previous) && (
          <DeltaPill current={value} previous={previous} direction={direction} showPct={false} />
        )}
      </div>
    </div>
  )
}
