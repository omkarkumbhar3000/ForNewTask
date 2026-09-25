/** Card shell. Every panel in the app is one of these, so spacing stays consistent. */
export function Card({ children, className = '', ...rest }) {
  return (
    <section className={`card ${className}`} {...rest}>
      {children}
    </section>
  )
}

/**
 * Card header. `title` is required; `note` is the one-line explanation of what the panel
 * shows, and `right` holds controls (a chart/table toggle, a link).
 */
export function CardHead({ title, note, right, as: Tag = 'h2' }) {
  return (
    <header className="card-head">
      <div style={{ minWidth: 0 }}>
        <Tag>{title}</Tag>
        {note && <p className="note">{note}</p>}
      </div>
      {right && <div style={{ flex: '0 0 auto' }}>{right}</div>}
    </header>
  )
}

export function CardBody({ children, style }) {
  return <div className="card-body" style={style}>{children}</div>
}

export function CardFoot({ children }) {
  return <div className="card-foot">{children}</div>
}

/** A titled block of the page, above the cards it groups. */
export function Section({ title, hint, children }) {
  return (
    <div className="section">
      {title && (
        <h2>
          {title}
          {hint && <span className="hint">{hint}</span>}
        </h2>
      )}
      {children}
    </div>
  )
}
