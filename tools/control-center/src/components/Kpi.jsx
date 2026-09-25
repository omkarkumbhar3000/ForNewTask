/**
 * One headline figure.
 *
 * Its own component rather than reusing the dashboards' Card, which is a panel
 * shell taking children — passing it title/value/note would have rendered nothing
 * and looked like a data problem.
 */
export function Kpi({ title, value, note, tone }) {
  return (
    <section className={tone ? `kpi kpi-${tone}` : 'kpi'}>
      <div className="kpi-t">{title}</div>
      <div className="kpi-v">{value}</div>
      {note ? <div className="kpi-n">{note}</div> : null}
    </section>
  )
}
