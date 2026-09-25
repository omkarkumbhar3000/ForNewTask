import { useState } from 'react'
import { Card, CardBody, CardHead, CardFoot } from './Card'
import { DataTable } from './DataTable'
import { EmptyState, ErrorBoundary } from './States'

/**
 * A chart panel with a Chart / Table toggle.
 *
 * The table view is not a nicety — it is the accessibility twin. Several of the palette's
 * light-surface hues sit below 3:1 contrast, and the rule for those is that the value must
 * also be reachable without relying on colour. The toggle is that route, and it doubles as
 * the way someone reads an exact figure off a chart.
 *
 * @param {object}   props
 * @param {string}   props.title
 * @param {string}  [props.note]        One line on what the panel shows.
 * @param {Array}   [props.legend]      [{ label, color, line? }] — present whenever ≥2 series.
 * @param {Array}    props.tableColumns Column spec for the table twin.
 * @param {Array}    props.tableRows
 * @param {string}  [props.source]      Provenance line for the footer.
 * @param {boolean} [props.available]   False renders the empty state instead of the chart.
 */
export function ChartCard({
  title,
  note,
  legend,
  children,
  tableColumns,
  tableRows,
  source,
  available = true,
  emptyTitle,
  emptyDetail,
  height,
}) {
  const [view, setView] = useState('chart')
  const canTable = Boolean(tableColumns && tableRows)

  return (
    <Card>
      <CardHead
        title={title}
        note={note}
        right={canTable && available ? (
          <div className="chart-toggle" role="group" aria-label={`${title} view`}>
            <button className={view === 'chart' ? 'on' : ''} onClick={() => setView('chart')} aria-pressed={view === 'chart'}>
              Chart
            </button>
            <button className={view === 'table' ? 'on' : ''} onClick={() => setView('table')} aria-pressed={view === 'table'}>
              Table
            </button>
          </div>
        ) : null}
      />
      <CardBody>
        {!available ? (
          <EmptyState title={emptyTitle || 'Not measured for this execution'} detail={emptyDetail} inline />
        ) : (
          <ErrorBoundary title={`"${title}" could not be rendered`}>
            {view === 'chart' ? (
              <>
                {legend && legend.length > 1 && (
                  <ul className="legend">
                    {legend.map((l) => (
                      <li key={l.label}>
                        <span className={`key${l.line ? ' line' : ''}`} style={{ background: l.color }} aria-hidden="true" />
                        {l.label}
                      </li>
                    ))}
                  </ul>
                )}
                <div style={height ? { height } : undefined}>{children}</div>
              </>
            ) : (
              <DataTable columns={tableColumns} rows={tableRows} compact />
            )}
          </ErrorBoundary>
        )}
      </CardBody>
      {source && <CardFoot>{source}</CardFoot>}
    </Card>
  )
}
