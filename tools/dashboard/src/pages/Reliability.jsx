import { useMemo, useState } from 'react'
import { PageHead, Select, Toolbar } from '../components/AppShell'
import { Card, CardBody, CardFoot, CardHead, Section } from '../components/Card'
import { DataTable } from '../components/DataTable'
import { Meter } from '../components/Indicators'
import { getReliability } from '../services/dataService'
import { c } from '../theme'
import { isNA, niceDate, num, runLabel } from '../utils/format'

/**
 * Execution reliability — OBJ-020.
 *
 * Why this page exists: the Sunday 2026-08-16 execution was terminated by a timeout, and the
 * dashboard showed nothing at all. Declining to PROMOTE a partial run to N is correct — its
 * figures are not comparable and must not be presented as a result. Declining to SHOW it is not:
 * "no run happened" and "a run was interrupted at 43%" are completely different facts for anyone
 * deciding whether the programme is on track.
 *
 * So every execution appears here with its terminal state and where it stopped, whether or not it
 * produced a workbook. Nothing is filtered away for tidiness.
 */

const STATE_TONE = {
  Completed: c.series1,
  'Incomplete - interrupted': c.critical,
  'Incomplete - no report': c.warning,
  'No result recorded': c.neutral,
}

function StateBadge({ state }) {
  return (
    <span className="badge">
      <span className="dot" style={{ background: STATE_TONE[state] || c.neutral }} aria-hidden="true" />
      {state}
    </span>
  )
}

/** Live supervisor panel. Absent until an unattended resume has been launched at least once. */
function SupervisorPanel({ sup, policy }) {
  if (!sup) {
    return (
      <Card>
        <CardHead title="Unattended resume" note="No supervised resume has been launched." />
        <CardBody>
          <p className="prov">
            {policy?.rule}
          </p>
        </CardBody>
      </Card>
    )
  }

  const attempts = sup.attempts || []
  const tone = sup.status === 'completed' ? c.series1
    : sup.status === 'abandoned' ? c.critical
      : sup.status === 'refused' ? c.warning : c.series3

  return (
    <Card>
      <CardHead
        title="Unattended resume"
        note={`Run ${sup.run} · ${attempts.length} attempt${attempts.length === 1 ? '' : 's'}`}
        right={(
          <span className="badge">
            <span className="dot" style={{ background: tone }} aria-hidden="true" />
            {sup.status}
          </span>
        )}
      />
      <CardBody>
        <div className="grid grid-kpi" style={{ marginBottom: 12 }}>
          <div className="kpi">
            <span className="kpi-label">Budget per attempt</span>
            <span className="kpi-value">{(sup.policy?.budgetSecondsPerAttempt || 0) / 3600}<span className="unit"> h</span></span>
          </div>
          <div className="kpi">
            <span className="kpi-label">Retry interval</span>
            <span className="kpi-value">{(sup.policy?.retryWaitSeconds || 0) / 60}<span className="unit"> min</span></span>
          </div>
          <div className="kpi">
            <span className="kpi-label">Minimum retries</span>
            <span className="kpi-value">{sup.policy?.minRetries}</span>
          </div>
          <div className="kpi">
            <span className="kpi-label">Give up after</span>
            <span className="kpi-value">{(sup.policy?.maxContinuousFailureSeconds || 0) / 3600}<span className="unit"> h</span></span>
          </div>
        </div>

        {attempts.length > 0 && (
          <DataTable
            compact
            columns={[
              { key: 'n', header: '#', num: true },
              { key: 'at', header: 'At', render: (r) => String(r.at).replace('T', ' ').slice(0, 19) },
              {
                key: 'ok',
                header: 'Result',
                render: (r) => (
                  <span className="badge">
                    <span className="dot" style={{ background: r.ok ? c.series1 : c.critical }} aria-hidden="true" />
                    {r.ok ? 'completed' : 'failed'}
                  </span>
                ),
              },
              {
                key: 'flows',
                header: 'Flows recorded',
                num: true,
                render: (r) => num(r.flowState?.flowsRecorded),
              },
              { key: 'detail', header: 'Detail', render: (r) => <span className="sub">{r.detail}</span> },
            ]}
            rows={attempts}
            rowKey={(r) => r.n}
          />
        )}
      </CardBody>
      <CardFoot>
        <p className="prov">
          <strong>Token safety.</strong> {policy?.tokenSafety}
        </p>
      </CardFoot>
    </Card>
  )
}

export function Reliability() {
  const rel = getReliability()
  const [scope, setScope] = useState('all')

  const rows = useMemo(() => (rel.runs || []).filter((r) => {
    if (scope === 'interrupted') return r.terminalState.startsWith('Incomplete')
    if (scope === 'completed') return r.terminalState === 'Completed'
    return true
  }), [rel.runs, scope])

  const columns = [
    {
      key: 'date',
      header: 'Execution',
      render: (r) => (
        <>
          {niceDate(r.date)}
          <span className="sub">{runLabel(r.id).split(', ')[1]}</span>
        </>
      ),
    },
    {
      key: 'terminalState',
      header: 'Terminal state',
      render: (r) => <StateBadge state={r.terminalState} />,
    },
    {
      key: 'completionPct',
      header: 'Flows completed',
      num: true,
      render: (r) => (
        isNA(r.completionPct) ? <span className="na">N/A</span> : (
          <>
            {num(r.flowsRecorded)} of {num(r.plannedFlows)}
            <Meter value={r.flowsRecorded} max={r.plannedFlows} title={`${r.completionPct}%`} />
            <span className="sub">{r.completionPct}%</span>
          </>
        )
      ),
    },
    { key: 'evidenceFiles', header: 'Evidence', num: true, render: (r) => num(r.evidenceFiles) },
    {
      key: 'abortedFlows',
      header: 'Aborted',
      num: true,
      render: (r) => (r.abortedFlows ? <strong style={{ color: c.critical }}>{r.abortedFlows}</strong> : '0'),
    },
    {
      key: 'promotedToCurrent',
      header: 'On the dashboard',
      render: (r) => (
        <>
          {r.promotedToCurrent ? 'Yes — this is run N' : 'No'}
          <span className="sub">{r.promotedNote}</span>
        </>
      ),
    },
    {
      key: 'whyItStopped',
      header: 'Where it stopped',
      render: (r) => <span className="sub">{r.whyItStopped}</span>,
    },
  ]

  const s = rel.summary || {}

  return (
    <div className="page">
      <PageHead
        title="Execution reliability"
        sub={rel.purpose}
      />

      <div className="grid grid-kpi">
        <div className="kpi">
          <span className="kpi-label">Executions on record</span>
          <span className="kpi-value">{num(s.totalRuns)}</span>
          <span className="kpi-hint">Runs are retained, never deleted.</span>
        </div>
        <div className="kpi">
          <span className="kpi-label">Completed</span>
          <span className="kpi-value">{num(s.completed)}</span>
          <span className="kpi-hint">Wrote both results.json and a run report.</span>
        </div>
        <div className="kpi">
          <span className="kpi-label">Interrupted</span>
          <span className="kpi-value" style={{ color: c.critical }}>{num(s.interrupted)}</span>
          <span className="kpi-hint">Terminated before a result could be written.</span>
        </div>
        <div className="kpi">
          <span className="kpi-label">Substantive</span>
          <span className="kpi-value">{num(s.substantive)}</span>
          <span className="kpi-hint">Large enough to serve as a benchmark baseline.</span>
        </div>
      </div>

      <Section
        title="Every execution and what became of it"
        hint="Interrupted runs are listed, not hidden. An interrupted run is a fact about the programme."
      >
        <Toolbar>
          <div className="field">
            <Select
              id="rel-scope"
              label="Show"
              value={scope}
              onChange={setScope}
              options={[
                { value: 'all', label: 'All executions' },
                { value: 'completed', label: 'Completed only' },
                { value: 'interrupted', label: 'Interrupted only' },
              ]}
            />
          </div>
        </Toolbar>

        <Card>
          <CardBody>
            <DataTable columns={columns} rows={rows} emptyLabel="No executions match this filter." />
          </CardBody>
          <CardFoot>
            <p className="prov">
              <strong>Flows completed</strong> is measured against {num(rel.plannedFlows)} flows.
              {' '}{rel.plannedBasis}
            </p>
          </CardFoot>
        </Card>
      </Section>

      <Section title="Interruption handling" hint="What happens when an execution is cut short.">
        <SupervisorPanel sup={rel.activeSupervisor} policy={rel.retryPolicy} />
      </Section>

      {(rel.weeklyJobHistory || []).length > 0 && (
        <Section
          title="Scheduled job history"
          hint="Every invocation of the weekly execution, step by step."
        >
          {rel.weeklyJobHistory.slice().reverse().map((job) => (
            <Card key={job.startedAt} style={{ marginBottom: 12 }}>
              <CardHead
                title={String(job.startedAt).replace('T', ' ').slice(0, 19)}
                note={`run ${job.run}`}
                right={(
                  <span className="badge">
                    <span
                      className="dot"
                      style={{ background: job.result === 'OK' ? c.series1 : c.critical }}
                      aria-hidden="true"
                    />
                    {job.result}
                  </span>
                )}
              />
              <CardBody>
                <DataTable
                  compact
                  columns={[
                    {
                      key: 'status',
                      header: 'Step',
                      width: '90px',
                      render: (r) => (
                        <span className="badge">
                          <span
                            className="dot"
                            style={{
                              background: r.status === 'failed' ? c.critical
                                : r.status === 'ok' ? c.series1 : c.neutral,
                            }}
                            aria-hidden="true"
                          />
                          {r.status}
                        </span>
                      ),
                    },
                    { key: 'text', header: 'Detail' },
                  ]}
                  rows={job.steps}
                  rowKey={(r, i) => i}
                />
              </CardBody>
            </Card>
          ))}
        </Section>
      )}
    </div>
  )
}
