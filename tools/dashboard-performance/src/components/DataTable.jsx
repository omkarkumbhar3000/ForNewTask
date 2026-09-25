import { isNA } from '../utils/format'

/**
 * The table used everywhere, including as every chart's table-view twin.
 *
 * `columns` is an array of:
 *   { key, header, num?, width?, render?(row), title? }
 * `num` right-aligns and applies tabular figures — the one place equal-width digits belong.
 *
 * An absent value renders as "N/A" in muted ink, never as an empty cell or a zero.
 */
export function DataTable({
  columns,
  rows,
  onRowClick,
  rowKey = (r, i) => r.id ?? i,
  isHighlighted,
  compact = false,
  emptyLabel = 'Nothing to show',
}) {
  if (!rows || rows.length === 0) {
    return <p className="prov" style={{ padding: '10px 0' }}>{emptyLabel}</p>
  }

  return (
    <div className="table-wrap">
      <table className={`dt${compact ? ' compact' : ''}`}>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key} className={col.num ? 'num' : undefined} style={col.width ? { width: col.width } : undefined}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => {
            const clickable = Boolean(onRowClick)
            return (
              <tr
                key={rowKey(row, i)}
                className={[
                  clickable ? 'clickable' : '',
                  isHighlighted?.(row) ? 'is-current' : '',
                ].filter(Boolean).join(' ')}
                onClick={clickable ? () => onRowClick(row) : undefined}
                tabIndex={clickable ? 0 : undefined}
                role={clickable ? 'button' : undefined}
                onKeyDown={clickable ? (e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    onRowClick(row)
                  }
                } : undefined}
              >
                {columns.map((col) => {
                  const raw = row[col.key]
                  const absent = isNA(raw) && !col.render
                  return (
                    <td
                      key={col.key}
                      className={[col.num ? 'num' : '', absent ? 'na' : ''].filter(Boolean).join(' ')}
                      title={col.title ? col.title(row) : undefined}
                    >
                      {col.render ? col.render(row) : absent ? 'N/A' : String(raw)}
                    </td>
                  )
                })}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
