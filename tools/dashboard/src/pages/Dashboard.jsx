import { PageHead } from '../components/AppShell'
import { Card, CardBody, CardFoot, CardHead, Section } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import {
  Callout, DeltaPill, HeroFigure, KpiTile, SeverityBadge, TrendBadge,
} from '../components/Indicators'
import { DataTable } from '../components/DataTable'
import { FreshnessBanner } from '../components/Freshness'
import { EmptyState } from '../components/States'
import { OutcomeDonut } from '../charts/OutcomeDonut'
import { RankedBars } from '../charts/RankedBars'
import { StackedOutcomeBars } from '../charts/StackedOutcomeBars'
import {
  getBenchmark, getExecution, getFailures, getGaps, getGates, getKpis, getManifest,
  getPrimaryFindingSet, getRefresh, getRun, getScenarios,
} from '../services/dataService'
import { c } from '../theme'
import { minutes, num, pct, runLabel } from '../utils/format'
import { navigate } from '../utils/router'

/**
 * The 30-second view. Reading top to bottom answers: what did we execute, how much of it
 * passed, how does that compare with last time, and what did it find.
 */
export function Dashboard() {
  const kpis = getKpis()
  const bench = getBenchmark()
  const scenarios = getScenarios()
  const failures = getFailures()
  const gates = getGates()
  const findingSet = getPrimaryFindingSet()
  const current = getRun(kpis.currentRunId)
  const previous = getRun(kpis.previousRunId)
  const gaps = getGaps()
  const manifest = getManifest()
  const refresh = getRefresh()
  const execution = getExecution()

  const heroTile = kpis.tiles.find((t) => t.id === 'executed')
  const otherTiles = kpis.tiles.filter((t) => t.id !== 'executed')

  const severityRows = findingSet.severityRollup.map((s) => ({ name: s.severity, value: s.count }))
  const layerRows = failures.layers.map((l) => ({ name: l.layer, value: l.hops, top: l.topEndpoints }))

  return (
    <div className="page">
      <PageHead
        title="Execution dashboard"
        sub={`Latest full execution of the PAM API surface — ${runLabel(current.id)} on ${current.environment}. Generated, executed and validated by the dynamic framework with no hand-written test code.`}
        right={bench.trend
          ? <TrendBadge level={bench.trendLevel}>{bench.trend}</TrendBadge>
          : <span className="chip">Analysis pending for this execution</span>}
      />

      {/* Shown only when the automatic refresh failed or the data is stale. */}
      <FreshnessBanner />

      {/* ── the one hero figure ─────────────────────────────────────────── */}
      <HeroFigure
        label="Test cases executed in the latest run"
        value={heroTile.value}
        delta={
          <div style={{ marginTop: 9, display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
            <DeltaPill current={heroTile.value} previous={heroTile.previous} direction="up-good" />
            <span className="prov">
              against {num(previous.executed)} in the previous execution
            </span>
          </div>
        }
        note={`Across ${num(current.flows)} generated flows, reaching ${num(current.distinctEndpoints)} distinct endpoints. ${gates.passed} of ${gates.total} run-validation gates passed.`}
      >
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', justifyContent: 'flex-end' }}>
          <span className="chip">{pct(current.successRate)} passed</span>
          <span className="chip">{minutes(current.durationMin)}</span>
          <button className="link-btn" onClick={() => navigate(`report/${current.id}`)}>
            Open full report →
          </button>
        </div>
      </HeroFigure>

      {/* ── KPI tiles ───────────────────────────────────────────────────── */}
      <Section>
        <div className="grid grid-kpi">
          {otherTiles.map((t) => (
            <KpiTile
              key={t.id}
              label={t.label}
              value={t.value}
              previous={t.previous}
              unit={t.unit}
              direction={t.direction}
              hint={t.hint}
            />
          ))}
        </div>
      </Section>

      {/* ── outcome & coverage ──────────────────────────────────────────── */}
      <Section title="Where this execution landed">
        <div className="grid grid-2">
          <ChartCard
            title="Outcome of every test case"
            note={`${num(current.executed)} executed. Blocked cases were withheld by a safety guard and are counted separately — never as passes.`}
            legend={[
              { label: 'Passed', color: c.series1 },
              { label: 'Failed', color: c.critical },
              { label: 'Blocked (withheld)', color: c.neutral },
            ]}
            tableColumns={[
              { key: 'name', header: 'Outcome' },
              { key: 'value', header: 'Test cases', num: true, render: (r) => num(r.value) },
            ]}
            tableRows={kpis.statusSplit}
            source="Source: artifacts/runs/2026-08-05_114315 — results.json, validated by validation.json"
          >
            <OutcomeDonut data={kpis.statusSplit} />
          </ChartCard>

          <ChartCard
            title="Coverage by test dimension"
            note="Four of these five dimensions did not exist in the previous execution, so the aggregate rate mixes new work with the baseline."
            legend={[
              { label: 'Passed', color: c.series1 },
              { label: 'Failed', color: c.critical },
            ]}
            tableColumns={[
              { key: 'scenario', header: 'Dimension' },
              { key: 'executed', header: 'Executed', num: true, render: (r) => num(r.executed) },
              { key: 'passed', header: 'Passed', num: true, render: (r) => num(r.passed) },
              { key: 'failed', header: 'Failed', num: true, render: (r) => num(r.failed) },
              { key: 'successRate', header: 'Rate', num: true, render: (r) => pct(r.successRate) },
              { key: 'previousExecuted', header: 'N-1', num: true, render: (r) => num(r.previousExecuted) },
            ]}
            tableRows={scenarios}
            source="Source: run workbook, sheet 'Scenario Coverage' — the QA team's own negative taxonomy"
          >
            <StackedOutcomeBars
              data={scenarios}
              height={250}
              note={(row) => `${pct(row.successRate)} passed · ${num(row.previousExecuted)} in the previous run`}
            />
          </ChartCard>
        </div>
      </Section>

      {/* ── what it found ──────────────────────────────────────────────── */}
      <Section
        title="What this execution found"
        hint={kpis.headlinesApply ? 'the three results that changed the picture' : undefined}
      >
        {kpis.headlinesApply ? (
          <div className="grid grid-3">
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
        ) : (
          /* The headline findings were authored about one specific execution. Reattaching them to
             a newer run would assert measurements that run never produced. */
          <Card>
            <CardBody>
              <EmptyState
                title="No authored findings for this execution yet"
                detail={`The headline findings on record were measured in run ${kpis.headlinesFor}, not in this one. They are withheld rather than reattached, because they are results of a specific execution and not standing properties of the API. The measured figures above are complete and current.`}
                inline
              />
            </CardBody>
          </Card>
        )}
      </Section>

      {/* ── risk ───────────────────────────────────────────────────────── */}
      <Section title="Findings and risk">
        <div className="grid grid-2">
          <ChartCard
            title={`Findings by severity — ${findingSet.total} total`}
            note={`${findingSet.name}. ${findingSet.raised} raised in Jira; the rest are evidenced and awaiting a decision.`}
            tableColumns={[
              { key: 'name', header: 'Severity' },
              { key: 'value', header: 'Findings', num: true },
            ]}
            tableRows={severityRows}
            source={`Source: ${findingSet.source}`}
          >
            <RankedBars
              data={severityRows}
              categoryKey="name"
              valueKey="value"
              valueName="Findings"
              height={200}
              axisWidth={112}
            />
          </ChartCard>

          <ChartCard
            title="Which validation layer caught each failure"
            note="A status-code-only assertion would have caught none of the envelope or message-semantics failures."
            tableColumns={[
              { key: 'name', header: 'Failing layer' },
              { key: 'value', header: 'Test cases', num: true, render: (r) => num(r.value) },
            ]}
            tableRows={layerRows}
            source="Source: run workbook, sheet 'Failure Analysis'"
          >
            <RankedBars
              data={layerRows}
              categoryKey="name"
              valueKey="value"
              valueName="Failures"
              height={228}
              axisWidth={150}
              note={(row) => (row.top?.length ? `Most affected: ${row.top[0]}` : undefined)}
            />
          </ChartCard>
        </div>
      </Section>

      <Section title="Top severity findings">
        <Card>
          <CardHead
            title="The four highest-priority findings"
            note="Full detail, all severities and the other finding sets are on the Findings & risk page."
            right={<button className="link-btn" onClick={() => navigate('findings')}>See all {findingSet.total} →</button>}
          />
          <CardBody>
            {findingSet.items.length === 0 ? (
              <EmptyState title="No findings recorded" inline />
            ) : (
              <div className="stack" style={{ gap: 10 }}>
                {findingSet.items.slice(0, 4).map((f) => (
                  <div
                    key={f.id}
                    style={{
                      display: 'flex', gap: 12, alignItems: 'flex-start',
                      paddingBottom: 10, borderBottom: `1px solid ${c.border}`,
                    }}
                  >
                    <span className="chip mono" style={{ marginTop: 1 }}>{f.id}</span>
                    <div style={{ flex: '1 1 auto', minWidth: 0 }}>
                      <div style={{ fontWeight: 600, fontSize: 13 }}>{f.title}</div>
                      <div style={{ color: c.inkSecondary, fontSize: 12, marginTop: 2 }}>{f.scope}</div>
                    </div>
                    <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                      <SeverityBadge severity={f.severity} label={f.severityLabel} />
                      {f.jira ? <span className="chip">{f.jira}</span> : <span className="chip">Not raised</span>}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardBody>
        </Card>
      </Section>

      {/* ── what this dashboard cannot tell you ─────────────────────────── */}
      <Section
        title="Data coverage"
        hint="what is measured, and what is not"
      >
        <div className="grid grid-2">
          <Card>
            <CardHead
              title={`${gaps.length} known data gaps`}
              note="Anything not measured shows as N/A across this dashboard rather than as a zero. These are the gaps, and what would close each one."
            />
            <CardBody style={{ paddingTop: 4 }}>
              <DataTable
                compact
                columns={[
                  { key: 'item', header: 'Not available' },
                  { key: 'why', header: 'Why' },
                  { key: 'wouldClose', header: 'What would produce it' },
                ]}
                rows={gaps}
                rowKey={(g, i) => i}
              />
            </CardBody>
          </Card>

          <Card>
            <CardHead
              title={`Built from ${manifest.sources.length} measured source files`}
              note={manifest.principle}
            />
            <CardBody style={{ paddingTop: 4 }}>
              <DataTable
                compact
                columns={[
                  { key: 'path', header: 'Source', render: (s) => <code style={{ fontSize: 10.5 }}>{s.path}</code> },
                  { key: 'provides', header: 'Provides' },
                ]}
                rows={manifest.sources}
                rowKey={(s) => s.path}
              />
            </CardBody>
            <CardFoot>
              Regenerate with <code>python tools\obj015_build_dashboard_data.py</code> —
              it issued {manifest.httpCallsIssued} HTTP calls.
            </CardFoot>
          </Card>
        </div>
      </Section>

      {/* ── the scheduled jobs ──────────────────────────────────────────── */}
      <Section title="Weekly execution" hint="Sundays 10:00 — the only thing that moves the figures above">
        <Card>
          {execution ? (
            <>
              <CardHead
                title={
                  execution.aborted ? 'Last weekly execution did not start'
                    : execution.ok ? `Last weekly execution completed — ${num(execution.executed)} test cases`
                      : 'Last weekly execution FAILED or was incomplete'
                }
                note={`${new Date(execution.lastAttempt).toLocaleString()} · ${execution.schedule}`}
                right={execution.runId && !execution.aborted
                  ? <button className="link-btn" onClick={() => navigate(`report/${execution.runId}`)}>Its report →</button>
                  : null}
              />
              <CardBody style={{ paddingTop: 4 }}>
                {execution.abortedFlows > 0 && (
                  <p className="prov" style={{ marginBottom: 9, color: c.critical }}>
                    ⚠ {num(execution.abortedFlows)} flow(s) remained aborted after one resume — this
                    execution is incomplete and its coverage is partial.
                  </p>
                )}
                <DataTable
                  compact
                  columns={[
                    {
                      key: 'status',
                      header: 'Result',
                      width: '92px',
                      render: (s) => (
                        <span className="badge">
                          <span
                            className="dot"
                            style={{
                              background: s.status === 'ok' ? c.good
                                : s.status === 'failed' || s.status === 'aborted' ? c.critical
                                  : s.status === 'skipped' ? c.warning : c.neutral,
                            }}
                            aria-hidden="true"
                          />
                          {s.status}
                        </span>
                      ),
                    },
                    { key: 'step', header: 'Step' },
                    { key: 'detail', header: 'Detail' },
                  ]}
                  rows={execution.steps || []}
                  rowKey={(s, i) => `${s.step}-${i}`}
                />
              </CardBody>
              <CardFoot>
                The job probes the environment without a credential first, so a token is never spent
                against a host that cannot answer. Log: <code>state/weekly/weekly.log</code>
              </CardFoot>
            </>
          ) : (
            <>
              <CardHead
                title="The weekly execution has not run yet"
                note="Scheduled for Sundays at 10:00. Until it runs, the figures above come from the last manual execution."
              />
              <CardBody>
                <EmptyState
                  title="No weekly execution recorded"
                  detail="Once it has run once, its per-step result and the run it produced appear here."
                  inline
                />
              </CardBody>
              <CardFoot>
                Check it without running anything:{' '}
                <code>python tools\obj017_weekly_execution.py</code> — a bare run issues
                no HTTP at all.
              </CardFoot>
            </>
          )}
        </Card>
      </Section>

      {/* ── the daily refresh job ───────────────────────────────────────── */}
      <Section title="Automatic refresh" hint="what the daily job did, and what it deliberately left alone">
        <Card>
          {refresh ? (
            <>
              <CardHead
                title={refresh.ok ? 'Last daily refresh succeeded' : 'Last daily refresh FAILED'}
                note={`Started ${new Date(refresh.lastAttempt).toLocaleString()}. The job pulls and re-derives; it does not execute the API suite.`}
              />
              <CardBody style={{ paddingTop: 4 }}>
                <DataTable
                  compact
                  columns={[
                    {
                      key: 'status',
                      header: 'Result',
                      width: '92px',
                      render: (s) => (
                        <span className="badge">
                          <span
                            className="dot"
                            style={{
                              background: s.status === 'ok' ? c.good
                                : s.status === 'failed' ? c.critical
                                  : s.status === 'skipped' ? c.warning : c.neutral,
                            }}
                            aria-hidden="true"
                          />
                          {s.status}
                        </span>
                      ),
                    },
                    { key: 'step', header: 'Step' },
                    { key: 'detail', header: 'Detail' },
                  ]}
                  rows={refresh.steps || []}
                  rowKey={(s, i) => `${s.step}-${i}`}
                />
              </CardBody>
              <CardFoot>
                A <strong>skipped</strong> step is a safety guard working, not a fault — most often the
                automation repo being refused because its working tree is dirty. Full log:{' '}
                <code>state/daily/daily.log</code>
              </CardFoot>
            </>
          ) : (
            <>
              <CardHead
                title="The daily job has not run yet"
                note="These figures come from the last manual generation."
              />
              <CardBody>
                <EmptyState
                  title="No automatic refresh recorded"
                  detail="Once the scheduled task has run once, its per-step result appears here."
                  inline
                />
              </CardBody>
              <CardFoot>
                Run it by hand with{' '}
                <code>python tools\obj016_daily_refresh.py --execute</code> — a bare run is a
                dry run and changes nothing.
              </CardFoot>
            </>
          )}
        </Card>
      </Section>
    </div>
  )
}
