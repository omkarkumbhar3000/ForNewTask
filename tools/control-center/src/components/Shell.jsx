import { navigate } from '../utils/router'

/**
 * Seven routes. Four carry real data; three say plainly what they still need.
 *
 * The stubs are labelled in the nav rather than hidden, because a missing view a
 * reader was promised is more confusing than a view that explains its own absence.
 */
const NAV = [
  { id: 'overview', label: 'Overview', count: null },
  { id: 'applications', label: 'Applications', count: 'repos' },
  { id: 'tasks', label: 'Pending tasks', count: 'pending' },
  { id: 'approvals', label: 'Approvals', count: 'approvals' },
  { id: 'recommendations', label: 'Recommendations', count: null },
  { id: 'history', label: 'History', count: null, partial: true },
  { id: 'execution', label: 'Execution results', count: null },
]

export function Shell({ view, counts, onRefresh, children }) {
  const active = NAV.some((n) => n.id === view) ? view : 'overview'
  return (
    <div className="shell">
      <nav className="nav" aria-label="Control Center sections">
        <div className="nav-head">
          <strong>Control Center</strong>
          <span className="nav-sub">DevProjects · engage</span>
        </div>
        <ul>
          {NAV.map((n) => {
            const c = n.count && counts ? counts[n.count] : null
            return (
              <li key={n.id}>
                <a
                  href={`#/${n.id}`}
                  className={active === n.id ? 'nav-link is-active' : 'nav-link'}
                  onClick={(e) => { e.preventDefault(); navigate(n.id) }}
                >
                  <span>{n.label}</span>
                  {c ? <span className="nav-count">{c}</span> : null}
                  {n.partial ? <span className="nav-flag" title="Limited data source">partial</span> : null}
                </a>
              </li>
            )
          })}
        </ul>
        {onRefresh ? (
          <button type="button" className="btn btn-quiet nav-refresh" onClick={onRefresh}>
            Re-analyse workspace
          </button>
        ) : null}
        <p className="nav-note">
          Decisions are held here until you press Execute. Nothing runs before that.
        </p>
      </nav>
      <main className="main">{children}</main>
    </div>
  )
}
