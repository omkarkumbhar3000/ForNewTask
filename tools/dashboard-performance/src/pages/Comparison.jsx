import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts'
import { PageHead } from '../components/AppShell'
import { Section, Card, CardHead, CardBody } from '../components/Card'
import { ChartCard } from '../components/ChartCard'
import { DataTable } from '../components/DataTable'
import { SampleBanner } from '../components/SampleBanner'
import { getComparison } from '../services/dataService'
import { axisProps, gridProps, c, BAR_MAX, BAR_RADIUS } from '../theme'
import { sourceLabel } from '../utils/provenance'

export function Comparison() {
  const cmp = getComparison()
  const data = (cmp.perModule || []).filter((m) => typeof m.ui === 'number' && typeof m.api === 'number')

  return (
    <>
      <PageHead
        title="API vs UI"
        sub="Where the bottleneck is — backend, frontend, or end-to-end"
        right={<span className="badge plain"><span className="dot" style={{ background: c.neutral }} />{cmp.verdict}</span>}
      />
      <SampleBanner />

      <Section title="Per-module: API vs UI" hint="grouped bars — the gap is the browser/frontend cost">
        <ChartCard
          title="UI load vs API load, by module"
          note="Where the UI bar towers over the API bar, the frontend dominates; where they are close, the backend does."
          legend={[{ label: 'UI (browser)', color: c.series2 }, { label: 'API (backend)', color: c.series1 }]}
          available={data.length > 0}
          height={Math.max(300, data.length * 34)}
          tableColumns={[
            { key: 'name', header: 'Module' },
            { key: 'ui', header: 'UI (ms)', num: true },
            { key: 'api', header: 'API (ms)', num: true },
          ]}
          tableRows={cmp.perModule}
          source={sourceLabel(cmp)}
        >
          <ResponsiveContainer width="100%" height={Math.max(300, data.length * 34)}>
            <BarChart data={data} layout="vertical" margin={{ top: 6, right: 20, bottom: 4, left: 8 }}>
              <CartesianGrid {...gridProps} vertical horizontal={false} />
              <XAxis type="number" {...axisProps} />
              <YAxis type="category" dataKey="name" {...axisProps} width={150} />
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="ui" name="UI (browser)" fill={c.series2} maxBarSize={BAR_MAX} radius={[0, 4, 4, 0]} isAnimationActive={false} />
              <Bar dataKey="api" name="API (backend)" fill={c.series1} maxBarSize={BAR_MAX} radius={[0, 4, 4, 0]} isAnimationActive={false} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </Section>

      <Section title="How to read the comparison" hint="the interpretation matrix from the objective">
        <Card>
          <CardHead title="Bottleneck reading guide" note="Pairing the API and UI signals points at the likely cause." />
          <CardBody>
            <DataTable
              columns={[
                { key: 'pattern', header: 'Observation' },
                { key: 'reading', header: 'Likely interpretation' },
              ]}
              rows={cmp.matrix}
            />
          </CardBody>
        </Card>
      </Section>
    </>
  )
}
