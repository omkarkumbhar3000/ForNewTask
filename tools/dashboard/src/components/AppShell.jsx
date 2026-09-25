import { navigate } from '../utils/router'

const NAV = [
  {
    label: 'Overview',
    items: [
      { view: 'dashboard', icon: '▤', title: 'Dashboard' },
      { view: 'benchmark', icon: '⇄', title: 'Execution benchmark' },
    ],
  },
  {
    label: 'Detail',
    items: [
      { view: 'history', icon: '▦', title: 'Execution history', countKey: 'runs' },
      { view: 'reliability', icon: '◑', title: 'Execution reliability' },
      { view: 'projects', icon: '◫', title: 'Projects', countKey: 'projects' },
      { view: 'findings', icon: '⚑', title: 'Findings & risk', countKey: 'findings' },
    ],
  },
]

export function AppShell({ view, counts, children, footer }) {
  return (
    <div className="shell">
      <nav className="nav" aria-label="Main">
        <div className="brand">
          <div className="brand-mark">
            <span className="brand-dot" aria-hidden="true">PA</span>
            <span className="brand-title">PAM API Automation</span>
          </div>
          <span className="brand-sub">Execution &amp; benchmark</span>
        </div>

        {NAV.map((group) => (
          <div className="nav-group" key={group.label}>
            <span className="nav-label">{group.label}</span>
            {group.items.map((item) => {
              const active = view === item.view || (item.view === 'history' && view === 'report')
              return (
                <button
                  key={item.view}
                  className={`nav-item${active ? ' active' : ''}`}
                  onClick={() => navigate(item.view === 'dashboard' ? '' : item.view)}
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

/** Page title block. `right` carries the trend badge or a back link. */
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

/**
 * One filter row above everything it scopes — never a filter inside a chart card.
 * `children` are `<div className="field">` groups.
 */
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
