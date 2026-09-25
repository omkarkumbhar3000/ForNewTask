import { navigate } from '../utils/router'

/**
 * Performance dashboard navigation. Same shell and visual language as the API dashboard
 * (AppShell), re-labelled for the performance scope: Executive → Login → Sanity → API → UI →
 * Comparison, matching the drill-down the objective asks for.
 */
const NAV = [
  {
    label: 'Overview',
    items: [
      { view: 'summary', icon: '▤', title: 'Executive summary' },
      { view: 'benchmark', icon: '⇅', title: 'N-1 vs N benchmark' },
      { view: 'comparison', icon: '⇄', title: 'API vs UI' },
    ],
  },
  {
    label: 'Scenarios',
    items: [
      { view: 'login', icon: '⏻', title: 'Login performance' },
      { view: 'sanity', icon: '▦', title: 'Sanity performance', countKey: 'sanity' },
    ],
  },
  {
    label: 'Layers',
    items: [
      { view: 'api', icon: '⚙', title: 'API performance' },
      { view: 'ui', icon: '◱', title: 'UI / experience' },
    ],
  },
]

export function AppShell({ view, counts, children, footer }) {
  return (
    <div className="shell">
      <nav className="nav" aria-label="Main">
        <div className="brand">
          <div className="brand-mark">
            <span className="brand-dot" aria-hidden="true">PP</span>
            <span className="brand-title">PAM Performance</span>
          </div>
          <span className="brand-sub">Login + Sanity · API + UI · k6</span>
        </div>

        {NAV.map((group) => (
          <div className="nav-group" key={group.label}>
            <span className="nav-label">{group.label}</span>
            {group.items.map((item) => {
              const active = view === item.view || (view === 'dashboard' && item.view === 'summary')
              return (
                <button
                  key={item.view}
                  className={`nav-item${active ? ' active' : ''}`}
                  onClick={() => navigate(item.view === 'summary' ? '' : item.view)}
                  aria-current={active ? 'page' : undefined}
                >
                  <span className="ico" aria-hidden="true">{item.icon}</span>
                  {item.title}
                  {item.countKey && counts?.[item.countKey] != null && (
                    <span className="count">{counts[item.countKey]}</span>
                  )}
                </button>
              )
            })}
          </div>
        ))}

        <div className="nav-foot">{footer}</div>
      </nav>

      <main className="main">{children}</main>
    </div>
  )
}

export function PageHead({ title, sub, right }) {
  return (
    <header className="page-head">
      <div>
        <h1>{title}</h1>
        {sub && <p className="sub">{sub}</p>}
      </div>
      {right && <div>{right}</div>}
    </header>
  )
}

export function Toolbar({ children, right }) {
  return (
    <div className="toolbar">
      {children}
      {right && <div className="spacer">{right}</div>}
    </div>
  )
}

export function Select({ label, value, onChange, options, id }) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <select id={id} value={value} onChange={(e) => onChange(e.target.value)}>
        {options.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </div>
  )
}
