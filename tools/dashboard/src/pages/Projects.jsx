import { useState } from 'react'
import { PageHead, Select, Toolbar } from '../components/AppShell'
import { Card, CardBody, CardFoot, CardHead, Section } from '../components/Card'
import { DataTable } from '../components/DataTable'
import { DeltaPill, KpiTile, Meter, SeverityBadge } from '../components/Indicators'
import { EmptyState } from '../components/States'
import {
  getBenchmark, getFindingSet, getProjects, getRun, getRuns,
} from '../services/dataService'
import { minutes, num, pct, runLabel } from '../utils/format'
import { navigate } from '../utils/router'

/**
 * Project view. One project has executions today; the selector and the per-project shape
 * exist so a second one is a data change rather than a redesign — which is the whole point
 * of the onboarding kit referenced at the bottom of this page.
 */
export function Projects() {
  const projects = getProjects()
  const [projectId, setProjectId] = useState(projects[0]?.id || 'PAM')
  const project = projects.find((p) => p.id === projectId) || projects[0]
  const bench = getBenchmark()
  const findings = getFindingSet('api')

  if (!project) {
    return (
      <div className="page">
        <PageHead title="Projects" />
        <Card><EmptyState title="No project profile found" detail="Expected at least one profile under data/profiles/." /></Card>
      </div>
    )
  }

  const runs = getRuns({ projectId: project.id })
  const latest = getRun(project.latestRunId)
  const baseline = getRun(bench.previousRunId)

  return (
    <div className="page">
      <PageHead
        title={project.name}
        sub={project.notes}
        right={<span className="chip">Tracker: {project.tracker}</span>}
      />

      <Toolbar right={<span className="prov">{projects.length} project{projects.length === 1 ? '' : 's'} onboarded</span>}>
        <Select
          id="p-project"
          label="Project"
          value={projectId}
          onChange={setProjectId}
          options={projects.map((p) => ({ value: p.id, label: `${p.name} (${p.id})` }))}
        />
      </Toolbar>

      <Section>
        <div className="grid grid-kpi">
          <KpiTile
            label="Executions retained"
            value={project.totalRuns}
            hint={`${project.substantiveRuns} full executions, the rest probes or aborted. None are ever deleted.`}
          />
          <KpiTile
            label="Latest execution"
            value={latest?.executed}
            hint={`${runLabel(project.latestRunId)} · ${minutes(latest?.durationMin)}`}
          />
          <KpiTile
            label="Success rate"
            value={project.latestSuccessRate}
            previous={baseline?.successRate}
            unit="%"
            direction="up-good"
            hint="Test-case level, latest execution against the previous one."
          />
          <KpiTile
            label="Endpoints reached"
            value={project.endpointsReached}
            previous={baseline?.distinctEndpoints}
            direction="up-good"
            hint={`${num(project.endpointsInCatalogue)} of these are declared in the catalogue — ${pct(project.coveragePct)} coverage.`}
          />
          <KpiTile
            label="Findings"
            value={project.findings}
            unit=""
            direction="down-good"
            hint={`${project.findingsRaised} raised in ${project.tracker}.`}
          />
        </div>
      </Section>

      <Section title="Endpoint coverage">
        <Card>
          <CardHead
            title={`${num(project.endpointsInCatalogue)} of ${num(project.catalogueEndpoints)} declared endpoints covered`}
            note="Coverage counts only endpoints the catalogue actually declares — see the note below for why that is not the same as the number reached."
          />
          <CardBody>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14, flexWrap: 'wrap' }}>
              <div style={{ flex: '1 1 260px', minWidth: 220 }}>
                <Meter
                  value={project.endpointsInCatalogue}
                  max={project.catalogueEndpoints}
                  title={`${num(project.endpointsInCatalogue)} of ${num(project.catalogueEndpoints)} declared endpoints`}
                />
              </div>
              <span style={{ fontWeight: 660, fontSize: 20, letterSpacing: '-0.5px' }}>
                {pct(project.coveragePct)}
              </span>
              <DeltaPill
                current={project.endpointsInCatalogue}
                previous={baseline?.endpointsInCatalogue}
                direction="up-good"
              />
            </div>

            <DataTable
              compact
              columns={[
                { key: 'k', header: 'Measure' },
                { key: 'v', header: 'Endpoints', num: true, render: (r) => num(r.v) },
              ]}
              rows={[
                { id: 'r', k: 'Distinct endpoints exercised by the latest execution', v: project.endpointsReached },
                { id: 'i', k: '— of which declared in the endpoint catalogue', v: project.endpointsInCatalogue },
                { id: 'o', k: '— of which NOT declared in the catalogue', v: project.endpointsOutsideCatalogue },
                { id: 'c', k: 'Endpoints declared in the catalogue', v: project.catalogueEndpoints },
              ]}
            />

            <p className="prov" style={{ marginTop: 11 }}>
              <strong>Why coverage is not simply reached ÷ declared:</strong> {project.coverageBasis}
            </p>
            <p className="prov" style={{ marginTop: 6 }}>
              Catalogue basis: {project.catalogueBasis}
            </p>
          </CardBody>
        </Card>
      </Section>

      <Section title="Latest benchmark">
        <Card>
          <CardHead
            title="Previous vs current, at a glance"
            note={bench.trend}
            right={<button className="link-btn" onClick={() => navigate('benchmark')}>Full benchmark →</button>}
          />
          <CardBody>
            <DataTable
              compact
              columns={[
                { key: 'k', header: 'Measure' },
                { key: 'prev', header: 'Previous', num: true, render: (r) => num(r.prev) },
                { key: 'cur', header: 'Current', num: true, render: (r) => num(r.cur) },
                {
                  key: 'd',
                  header: 'Change',
                  num: true,
                  render: (r) => <DeltaPill current={r.cur} previous={r.prev} direction={r.dir} showPct={false} />,
                },
              ]}
              rows={[
                { id: 'e', k: 'Test cases executed', prev: baseline?.executed, cur: latest?.executed, dir: 'up-good' },
                { id: 'p', k: 'Passed', prev: baseline?.passed, cur: latest?.passed, dir: 'up-good' },
                { id: 'f', k: 'Failed', prev: baseline?.failed, cur: latest?.failed, dir: 'down-good' },
                { id: 'r', k: 'Success rate (%)', prev: baseline?.successRate, cur: latest?.successRate, dir: 'up-good' },
                { id: 'n', k: 'Endpoints reached', prev: baseline?.distinctEndpoints, cur: latest?.distinctEndpoints, dir: 'up-good' },
                { id: 'l', k: 'Median response time (ms)', prev: baseline?.latencyMedianMs, cur: latest?.latencyMedianMs, dir: 'down-good' },
              ]}
            />
            <p className="prov" style={{ marginTop: 10 }}>
              Performance trend: {project.performanceTrend} — mean improved while the median rose,
              because the current run's pacing was faster and its mix included far more short
              negative calls.
            </p>
          </CardBody>
        </Card>
      </Section>

      <Section title="Executions">
        <Card>
          <CardHead title={`All ${runs.length} executions for this project`} right={<button className="link-btn" onClick={() => navigate('history')}>Full history →</button>} />
          <CardBody style={{ paddingTop: 4 }}>
            <DataTable
              compact
              columns={[
                { key: 'id', header: 'Execution', render: (r) => runLabel(r.id) },
                { key: 'type', header: 'Type' },
                { key: 'executed', header: 'Executed', num: true, render: (r) => num(r.executed) },
                { key: 'successRate', header: 'Rate', num: true, render: (r) => pct(r.successRate) },
                { key: 'findings', header: 'Findings', num: true },
              ]}
              rows={runs}
              rowKey={(r) => r.id}
              onRowClick={(r) => navigate(`report/${r.id}`)}
              isHighlighted={(r) => r.isCurrent}
            />
          </CardBody>
        </Card>
      </Section>

      <Section title="Open findings for this project">
        <Card>
          <CardHead
            title={`${findings.total} findings · ${findings.raised} raised`}
            right={<button className="link-btn" onClick={() => navigate('findings')}>Findings &amp; risk →</button>}
          />
          <CardBody>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {findings.severityRollup.filter((s) => s.count > 0).map((s) => (
                <SeverityBadge key={s.severity} severity={s.severity} label={`${s.severity} · ${s.count}`} />
              ))}
            </div>
          </CardBody>
        </Card>
      </Section>

      <Section title="Adding another project">
        <Card>
          <CardHead
            title="This view is built to take more than one project"
            note="Nothing here is PAM-specific in structure — a second project needs a profile and at least one execution, not a UI change."
          />
          <CardBody>
            <ol className="bullets">
              <li>
                Author a profile in <code>{project.onboardingKit}profiles/</code> against{' '}
                <code>profile.schema.json</code>, using <code>pam.json</code> as the worked example.
              </li>
              <li>
                Pass the readiness gate: <code>python tools\onboarding\validate_profile.py</code>.
              </li>
              <li>Generate flows and execute, which writes a new folder under <code>artifacts/runs/</code>.</li>
              <li>
                Re-run <code>python tools\obj015_build_dashboard_data.py</code>. The new
                project and its executions appear in this dashboard automatically.
              </li>
            </ol>
          </CardBody>
          <CardFoot>
            Project profile read from <code>{project.profileSource}</code>
          </CardFoot>
        </Card>
      </Section>
    </div>
  )
}
