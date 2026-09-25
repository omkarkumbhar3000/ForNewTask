import { Component } from 'react'

/**
 * Empty state. Used wherever a figure is "N/A" — the app never renders a zero in place of
 * a measurement that does not exist.
 */
export function EmptyState({ title = 'Not available', detail, icon = '—', inline = false }) {
  return (
    <div className={`state${inline ? ' inline' : ''}`}>
      <span className="ico" aria-hidden="true">{icon}</span>
      <h3>{title}</h3>
      {detail && <p>{detail}</p>}
    </div>
  )
}

/** Loading placeholder. Holds height so nothing jumps when the data arrives. */
export function Loading({ height = 220, label = 'Loading' }) {
  return (
    <div className="card-body" role="status" aria-label={label}>
      <div className="skeleton" style={{ height }} />
    </div>
  )
}

export function ErrorState({ title = 'Something went wrong', detail, onRetry }) {
  return (
    <div className="state">
      <span className="ico" aria-hidden="true">⚠</span>
      <h3>{title}</h3>
      {detail && <p>{detail}</p>}
      {onRetry && (
        <button className="link-btn" onClick={onRetry}>Try again</button>
      )}
    </div>
  )
}

/**
 * Catches a render error in one panel so a single bad dataset cannot blank the whole
 * dashboard — which matters when this is on screen in front of management.
 */
export class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error) {
    return { error }
  }

  componentDidCatch(error, info) {
    // eslint-disable-next-line no-console
    console.error('[dashboard] panel failed to render', error, info)
  }

  render() {
    if (this.state.error) {
      return (
        <ErrorState
          title={this.props.title || 'This panel could not be displayed'}
          detail={String(this.state.error.message || this.state.error)}
          onRetry={() => this.setState({ error: null })}
        />
      )
    }
    return this.props.children
  }
}
