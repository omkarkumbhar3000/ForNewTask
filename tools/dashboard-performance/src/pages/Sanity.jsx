import { useState } from 'react'
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from 'recharts'
import { PageHead, Toolbar, Select } from '../components/AppShell'
import { Section, Card, CardHead, CardBody } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { DataTable } from '../components/DataTable'
import { StatTile, StatRow } from '../components/StatTile'
import { SampleBanner } from '../components/SampleBanner'
import { getSanity } from '../services/dataService'
import { axisProps, gridProps, c, BAR_MAX, BAR_RADIUS_H } from '../theme'
import { isNA } from '../utils/format'

const ATTR_COLOR = {
  'Frontend/UI-dominated': c.series2,
  'Backend-dominated': c.series1,
  Mixed: c.series3,
}

export function Sanity() {
  const sn = getSanity()
  const [attr, setAttr] = useState('all')

  const modules = sn.modules.filter((m) => attr === 'all' || m.attribution === attr)
  const chartData = [...modules]
    .filter((m) => !isNA(m.uiLoadMs))
    .sort((a, b) => b.uiLoadMs - a.uiLoadMs)

  const columns = [
    { key: 'name', header: 'Module' },
    { key: 'checks', header: 'Checks', num: true },
    { key: 'navType', header: 'Nav' },
    { key: 'uiLoadMs', header: 'UI load (ms)', num: true },
    { key: 'apiLoadMs', header: 'API (ms)', num: true },
    { key: 'attribution', header: 'Attribution',
      render: (r) => (
        <span className="badge plain">
          <span className="dot" style={{ background: ATTR_COLOR[r.attribution] || c.neutral }} />
          {r.attribution}
        </span>
      ) },
    { key: 'status', header: 'Status' },
  ]

  return (
    <>
      <PageHead
        title="Sanity performance"
        sub={`${sn.totals.modules} modules · ${sn.totals.checks} checks · source: ${sn.source}`}
      />
      <SampleBanner />

      <StatRow>
        <StatTile label="Modules" value={sn.totals.modules} sub="from SanityChecks.xml" />
        <StatTile label="Element checks" value={sn.totals.checks} />
        <StatTile label="Excluded" value={sn.totals.excluded} sub="commented out in the suite" />
      </StatRow>

      <Toolbar>
        <Select
          id="attr" label="Attribution" value={attr} onChange={setAttr}
          options={[
            { value: 'all', label: 'All modules' },
            { value: 'Frontend/UI-dominated', label: 'Frontend-dominated' },
            { value: 'Backend-dominated', label: 'Backend-dominated' },
            { value: 'Mixed', label: 'Mixed' },
          ]}
        />
      </Toolbar>

      <Section title="Module load time" hint="p95, slowest first">
        <ChartCard
          title="UI load by module"
          note="Bar colour is the bottleneck attribution — frontend, backend, or mixed."
          legend={[
            { label: 'Frontend-dominated', color: c.series2 },
            { label: 'Backend-dominated', color: c.series1 },
            { label: 'Mixed', color: c.series3 },
          ]}
          available={chartData.length > 0}
          height={Math.max(260, chartData.length * 30)}
          tableColumns={columns}
          tableRows={modules}
          source="Sample timings; module scope is real."
        >
          <ResponsiveContainer width="100%" height={Math.max(260, chartData.length * 30)}>
            <BarChart data={chartData} layout="vertical" margin={{ top: 6, right: 20, bottom: 4, left: 8 }}>
              <CartesianGrid {...gridProps} vertical horizontal={false} />
              <XAxis type="number" {...axisProps} />
              <YAxis type="category" dataKey="name" {...axisProps} width={150} />
              <Tooltip />
              <Bar dataKey="uiLoadMs" maxBarSize={BAR_MAX} radius={BAR_RADIUS_H} isAnimationActive={false}>
                {chartData.map((m, i) => <Cell key={i} fill={ATTR_COLOR[m.attribution] || c.neutral} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>

      <Section title="All modules">
        <Card>
          <CardHead title="Sanity module detail" note="UI and API load, check count, and bottleneck attribution per module." />
          <CardBody>
            <DataTable columns={columns} rows={modules} />
          </CardBody>
        </Card>
      </Section>

      {sn.excluded?.length > 0 && (
        <Section title="Excluded from scope" hint="commented out in DevOpsSanityCheck.java">
          <Card>
            <CardBody>
              <DataTable
                columns={[{ key: 'name', header: 'Module' }, { key: 'reason', header: 'Reason' }]}
                rows={sn.excluded}
                compact
              />
            </CardBody>
          </Card>
        </Section>
      )}
    </>
  )
}
