import { useMemo, useState } from 'react'
import { PageHead, Select, Toolbar } from '../components/AppShell'
import { Card, CardBody, CardFoot, CardHead, Section } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { DataTable } from '../components/DataTable'
import { StatusBadge } from '../components/Indicators'
import { EmptyState } from '../components/States'
import { RunTrendLine } from '../charts/RunTrendLine'
import { getProjects, getRuns, getTrendSeries } from '../services/dataService'
import { c } from '../theme'
import { isNA, minutes, niceDate, num, pct, runLabel } from '../utils/format'
import { navigate } from '../utils/router'

/**
 * Execution history. Selecting any row opens that execution's management report.
 *
 * Probe and aborted runs are listed by default rather than filtered away — the retention
 * rule for this programme is that no run is ever deleted, and hiding the short ones would
 * make the history look tidier than it is. The filter lets you drop to full executions only.
 */
export function History() {
  const projects = getProjects()
  const [projectId, setProjectId] = useState(projects[0]?.id || 'PAM')
  const [scope, setScope] = useState('all')
  const [dateFilter, setDateFilter] = useState('all')

  const allRuns = getRuns({ projectId })

  const dates = useMemo(
    () => Array.from(new Set(allRuns.map((r) => r.date))).sort().reverse(),
    [allRuns],
  )

  const rows = useMemo(() => allRuns.filter((r) => {
    if (scope === 'substantive' && !r.substantive) return false
    if (dateFilter !== 'all' && r.date !== dateFilter) return false
    return true
  }), [allRuns, scope, dateFilter])

  const trend = getTrendSeries({ projectId })
  const withRate = allRuns.filter((r) => !isNA(r.successRate))

  const columns = [
    {
      key: 'date',
      header: 'Date',
      render: (r) => (
        <>
          {niceDate(r.date)}
          <span className="sub">{runLabel(r.id).split(', ')[1]}</span>
        </>
      ),
    },
    { key: 'projectId', header: 'Project' },
    {
      key: 'type',
      header: 'Execution type',
      render: (r) => (
        <>
          {r.type}
          {r.substantive && <span className="sub">full execution</span>}
        </>
      ),
    },
    { key: 'total', header: 'Total', num: true, render: (r) => num(r.total) },
    { key: 'passed', header: 'Passed', num: true, render: (r) => num(r.passed) },
    { key: 'failed', header: 'Failed', num: true, render: (r) => num(r.failed) },
    {
      key: 'successRate',
      header: 'Success rate',
      num: true,
      render: (r) => (isNA(r.successRate)
        ? <span className="na">N/A</span>
        : <strong>{pct(r.successRate)}</strong>),
    },
    {
      key: 'durationMin',
      header: 'Duration',
      num: true,
      render: (r) => (isNA(r.durationMin) ? <span className="na">N/A</span> : minutes(r.durationMin)),
      title: (r) => r.durationBasis,
    },
    { key: 'findings', header: 'Findings', num: true },
    { key: 'status', header: 'Status', render: (r) => <StatusBadge status={r.status} /> },
    {
      key: 'open',
      header: '',
      render: (r) => <span className="link-btn" aria-hidden="true">Report →</span>,
    },
  ]

  return (
    <div className="page">
      <PageHead
        title="Execution history"
        sub="Every execution ever run against this project, newest first. Select any row to open its management report. Runs are retained permanently — that retention is what made the previous-vs-current benchmark possible."
      />

      <Toolbar
        right={<span className="prov">{rows.length} of {allRuns.length} executions shown</span>}
      >
        <Select
          id="f-project"
          label="Project"
          value={projectId}
          onChange={setProjectId}
          options={projects.map((p) => ({ value: p.id, label: p.name }))}
        />
        <Select
          id="f-date"
          label="Date"
          value={dateFilter}
          onChange={setDateFilter}
          options={[{ value: 'all', label: 'All dates' }, ...dates.map((d) => ({ value: d, label: niceDate(d) }))]}
        />
        <Select
          id="f-scope"
          label="Show"
          value={scope}
          onChange={setScope}
          options={[
            { value: 'all', label: 'All executions' },
            { value: 'substantive', label: 'Full executions only' },
          ]}
        />
      </Toolbar>

      <Section>
        <Card>
          <CardHead
            title="Executions"
            note="A probe is a short generation or connectivity check. An aborted run wrote no results — it is listed so the history is complete."
          />
          <CardBody style={{ paddingTop: 4 }}>
            {rows.length === 0 ? (
              <EmptyState
                title="No executions match these filters"
                detail="Widen the date or scope filter above."
                inline
              />
            ) : (
              <DataTable
                columns={columns}
                rows={rows}
                onRowClick={(r) => navigate(`report/${r.id}`)}
                isHighlighted={(r) => r.isCurrent}
                rowKey={(r) => r.id}
              />
            )}
          </CardBody>
          <CardFoot>
            Derived from each run folder's <code>results.json</code> under{' '}
            <code>artifacts/runs/</code>. Duration for a resumed run comes from{' '}
            <code>segments.json</code>, since a resumed run's own metadata records only its
            last segment.
          </CardFoot>
        </Card>
      </Section>

      <Section title="Success rate across executions">
        <ChartCard
          title="Success rate by execution"
          note={`${withRate.length} executions produced a success rate. Short probe runs are included, so the line mixes 12-case checks with full 5,000-case executions — read the two full executions on the Benchmark page for the like-for-like comparison.`}
          available={trend.length > 0}
          emptyTitle="No execution has produced a success rate yet"
          tableColumns={[
            { key: 'runId', header: 'Execution', render: (r) => runLabel(r.runId) },
            { key: 'executed', header: 'Executed', num: true, render: (r) => num(r.executed) },
            { key: 'passed', header: 'Passed', num: true, render: (r) => num(r.passed) },
            { key: 'successRate', header: 'Success rate', num: true, render: (r) => pct(r.successRate) },
          ]}
          tableRows={trend}
          source="Only full executions are plotted; see the table for the underlying counts."
        >
          <RunTrendLine data={trend} />
        </ChartCard>
      </Section>

      <p className="prov" style={{ marginTop: 16, color: c.inkMuted }}>
        Two executions carry a full test-case breakdown. The rest are probes or were aborted
        before writing results, and are shown as N/A rather than zero.
      </p>
    </div>
  )
}
