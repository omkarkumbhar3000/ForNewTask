import { Card, CardHead, CardBody, Section } from './Card'
import { DataTable } from './DataTable'
import { getExecutions } from '../services/dataService'
import { c } from '../theme'

/**
 * Execution attempts — OBJ-020.
 *
 * The owner's rule, set after an interrupted API execution went unshown: an execution that was
 * blocked or terminated is still an execution, and omitting it makes a dashboard misleading in
 * the one direction that matters. Here it does double duty — with sample figures on screen, this
 * panel is the reader's only proof of what has and has not actually been run against the product.
 */
export function ExecutionAttempts() {
  const data = getExecutions()
  if (!data) return null
  const { blocker, executions } = data

  const rows = (executions || []).map((e) => ({
    ...e,
    phaseLabel: e.phases.length
      ? e.phases.map((p) => `${p.phase}/${p.journey}`).join(', ')
      : 'none completed',
    vus: e.phases.length ? e.phases[0].targetVus : 'N/A',
    rejections: e.phases.length ? e.phases[0].rejections : 'N/A',
  }))

  return (
    <Section
      title="Execution attempts against the product"
      hint="Every k6 invocation, including the ones that produced no measurement. Nothing is omitted."
    >
      {blocker?.active && (
        <div
          className="card"
          role="status"
          style={{ borderLeft: `3px solid ${c.critical}`, marginBottom: 14, padding: '11px 15px' }}
        >
          <p style={{ margin: 0, fontWeight: 640, fontSize: 13 }}>
            Live execution is blocked — {blocker.attemptsMade} attempt
            {blocker.attemptsMade === 1 ? '' : 's'} made, none authenticated
          </p>
          <p style={{ margin: '4px 0 0', fontSize: 12.5, color: c.inkSecondary }}>
            {blocker.summary}
          </p>
          <p style={{ margin: '8px 0 0', fontSize: 12.5, color: c.inkSecondary }}>
            <strong>Accounts tried:</strong> {blocker.accountsTried.join(' · ')}
          </p>
          <p style={{ margin: '6px 0 0', fontSize: 12.5, color: c.inkSecondary }}>
            <strong>Unblocks on any one of:</strong> {blocker.unblocks.join(' · ')}
          </p>
          <p style={{ margin: '8px 0 0', fontSize: 12, color: c.inkMuted }}>
            {blocker.safetyNote}
          </p>
        </div>
      )}

      <Card>
        <CardHead
          title="Attempt log"
          note={data.purpose}
        />
        <CardBody>
          <DataTable
            columns={[
              { key: 'runId', header: 'Run id' },
              {
                key: 'terminalState',
                header: 'Terminal state',
                render: (r) => (
                  <span className="badge">
                    <span
                      className="dot"
                      style={{ background: r.measurementValid ? c.series1 : c.critical }}
                    />
                    {r.terminalState}
                  </span>
                ),
              },
              { key: 'phaseLabel', header: 'Phases' },
              { key: 'vus', header: 'VUs', num: true },
              { key: 'rejections', header: 'Rejections' },
              { key: 'whyItStopped', header: 'Where it stopped' },
            ]}
            rows={rows}
            rowKey={(r) => r.runId}
            emptyLabel="No execution has been attempted yet."
          />
        </CardBody>
      </Card>
    </Section>
  )
}
