import { useMemo, useState } from 'react'
import { PageHead, Select, Toolbar } from '../components/AppShell'
import { Card, CardBody, CardFoot, CardHead, Section } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { DataTable } from '../components/DataTable'
import { KpiTile, SeverityBadge } from '../components/Indicators'
import { EmptyState } from '../components/States'
import { RankedBars } from '../charts/RankedBars'
import { getFindingSets, getSeverityMapping, getSeverityOrder } from '../services/dataService'
import { c } from '../theme'

/**
 * Findings and risk.
 *
 * The surface stays deliberately thin — a severity distribution, counts, and one line per
 * finding. The technical detail (impact, remediation, evidence path) is behind a row click,
 * because it is what a developer needs and what would make this page unreadable to anyone else.
 *
 * Severity is a single-series bar with the tier named on the axis, not three coloured fills.
 * Red/amber/yellow as adjacent fills failed the palette checks twice over — yellow leaves the
 * lightness band and yellow-against-amber is below the normal-vision separation floor. Status
 * colour survives only as the small dot in each badge, always beside its text label.
 */
export function Findings() {
  const sets = getFindingSets()
  const order = getSeverityOrder()
  const mapping = getSeverityMapping()

  const [setId, setSetId] = useState(sets[0]?.id)
  const [severity, setSeverity] = useState('all')
  const [openId, setOpenId] = useState(null)

  const set = sets.find((s) => s.id === setId) || sets[0]

  const rows = useMemo(() => {
    if (!set) return []
    const list = severity === 'all' ? set.items : set.items.filter((i) => i.severity === severity)
    return list.slice().sort((a, b) => order.indexOf(a.severity) - order.indexOf(b.severity))
  }, [set, severity, order])

  if (!set) {
    return (
      <div className="page">
        <PageHead title="Findings &amp; risk" />
        <Card><EmptyState title="No finding sets available" /></Card>
      </div>
    )
  }

  const severityRows = set.severityRollup.map((s) => ({ name: s.severity, value: s.count }))
  const actionable = set.severityRollup
    .filter((s) => s.severity === 'Critical' || s.severity === 'High')
    .reduce((t, s) => t + s.count, 0)

  return (
    <div className="page">
      <PageHead
        title="Findings &amp; risk"
        sub="Everything the automated execution and the supporting analysis surfaced, grouped by how badly it affects correctness, availability or trust. Select any row for the detail."
      />

      <Toolbar right={<span className="prov">{rows.length} of {set.total} shown</span>}>
        <Select
          id="fs-set"
          label="Finding set"
          value={setId}
          onChange={(v) => { setSetId(v); setSeverity('all'); setOpenId(null) }}
          options={sets.map((s) => ({ value: s.id, label: `${s.name} (${s.total})` }))}
        />
        <Select
          id="fs-sev"
          label="Severity"
          value={severity}
          onChange={setSeverity}
          options={[
            { value: 'all', label: 'All severities' },
            ...order
              .filter((o) => set.severityRollup.find((s) => s.severity === o)?.count > 0)
              .map((o) => ({ value: o, label: `${o} (${set.severityRollup.find((s) => s.severity === o).count})` })),
          ]}
        />
      </Toolbar>

      <Card style={{ marginBottom: 14 }}>
        <CardBody>
          <p className="prose" style={{ margin: 0 }}>{set.description}</p>
        </CardBody>
      </Card>

      <Section>
        <div className="grid grid-kpi">
          <KpiTile label="Findings in this set" value={set.total} hint={set.name} />
          <KpiTile
            label="Critical or high"
            value={actionable}
            direction="down-good"
            hint="The tiers that warrant action before the next release."
          />
          <KpiTile
            label="Raised in Jira"
            value={set.raised}
            hint={`${set.total - set.raised} are evidenced and packaged but not yet raised — that is an owner decision.`}
          />
        </div>
      </Section>

      <Section title="Severity distribution">
        <div className="grid grid-2">
          <ChartCard
            title="Findings by severity"
            note="Tiers are ordered most to least severe. A tier with no findings still shows, so a zero is visibly a measurement rather than an omission."
            tableColumns={[
              { key: 'name', header: 'Severity' },
              { key: 'value', header: 'Findings', num: true },
            ]}
            tableRows={severityRows}
            source={`Source: ${set.source}`}
          >
            <RankedBars
              data={severityRows}
              categoryKey="name"
              valueKey="value"
              valueName="Findings"
              height={210}
              axisWidth={112}
            />
          </ChartCard>

          <Card>
            <CardHead
              title="How severity is assigned"
              note="Each source document uses its own wording. The original wording is kept on every finding; only the chart bucket is normalised."
            />
            <CardBody>
              <DataTable
                compact
                columns={[
                  { key: 'from', header: 'Source wording' },
                  { key: 'to', header: 'Bucket used for charts' },
                ]}
                rows={Object.entries(mapping.map).map(([from, to]) => ({ id: from, from, to }))}
              />
            </CardBody>
            <CardFoot>{mapping.note}</CardFoot>
          </Card>
        </div>
      </Section>

      <Section title="All findings" hint="select a row for impact, remediation and evidence">
        <Card>
          <CardBody style={{ paddingTop: 4 }}>
            {rows.length === 0 ? (
              <EmptyState title="No findings at this severity" detail="Change the severity filter above." inline />
            ) : (
              <DataTable
                columns={[
                  { key: 'id', header: 'ID', width: '78px', render: (r) => <span className="chip mono">{r.id}</span> },
                  { key: 'priority', header: 'Priority', width: '76px' },
                  {
                    key: 'title',
                    header: 'Finding',
                    render: (r) => (
                      <>
                        <span style={{ fontWeight: 570 }}>{r.title}</span>
                        {openId === r.id && <FindingDetail finding={r} />}
                      </>
                    ),
                  },
                  {
                    key: 'severity',
                    header: 'Severity',
                    render: (r) => <SeverityBadge severity={r.severity} label={r.severityLabel || r.severity} />,
                  },
                  { key: 'effort', header: 'Effort', width: '92px' },
                  { key: 'scope', header: 'Measured scope' },
                  {
                    key: 'status',
                    header: 'Status',
                    render: (r) => (r.jira
                      ? <span className="chip">{r.jira}</span>
                      : <span className="na">{r.status}</span>),
                  },
                ]}
                rows={rows}
                rowKey={(r) => r.id}
                onRowClick={(r) => setOpenId(openId === r.id ? null : r.id)}
              />
            )}
          </CardBody>
          <CardFoot>Source: <code>{set.source}</code></CardFoot>
        </Card>
      </Section>
    </div>
  )
}

/** Drill-down detail, revealed only on request — never on the surface. */
function FindingDetail({ finding }) {
  const fields = [
    ['Impact', finding.impact],
    ['Recommended action', finding.remediation],
    ['Evidence', finding.evidence],
    ['Layer', finding.layer],
    ['Owner / raised by', finding.statusDetail],
  ].filter(([, v]) => v && String(v).trim() && String(v) !== 'N/A')

  if (fields.length === 0) {
    return (
      <p className="prov" style={{ marginTop: 7 }}>
        No further detail is recorded for this finding in its source document.
      </p>
    )
  }

  return (
    <dl
      className="kv"
      style={{
        marginTop: 9, paddingTop: 9, borderTop: `1px solid ${c.border}`,
        maxWidth: '86ch',
      }}
    >
      {fields.map(([k, v]) => (
        <div key={k} style={{ display: 'contents' }}>
          <dt>{k}</dt>
          <dd style={{ fontWeight: 400, color: c.inkSecondary }}>{v}</dd>
        </div>
      ))}
    </dl>
  )
}
