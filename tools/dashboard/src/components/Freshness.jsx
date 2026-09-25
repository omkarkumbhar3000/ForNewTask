import { getFreshness } from '../services/dataService'
import { c } from '../theme'

const TONE = {
  ok: c.good,
  failed: c.critical,
  never: c.neutral,
}

function ago(hours) {
  if (hours == null) return null
  if (hours < 1) return 'just now'
  if (hours < 24) return `${Math.round(hours)} h ago`
  const days = Math.round(hours / 24)
  return `${days} day${days === 1 ? '' : 's'} ago`
}

/**
 * Freshness line for the sidebar, plus a manual re-fetch.
 *
 * A daily job that fails silently is indistinguishable from one that succeeded — the dashboard
 * would keep showing yesterday's figures with nothing to say so. This is the thing that says so.
 */
export function FreshnessNote({ onRefetch, reloadedAt }) {
  const f = getFreshness()
  const when = f.when ? new Date(f.when) : null

  return (
    <div>
      <p style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 3 }}>
        <span
          style={{ width: 7, height: 7, borderRadius: '50%', flex: '0 0 7px', background: TONE[f.state] }}
          aria-hidden="true"
        />
        <span style={{ fontWeight: 600, color: f.state === 'failed' ? c.critical : c.inkSecondary }}>
          {f.label}
        </span>
      </p>
      {when && (
        <p title={when.toString()}>
          {when.toLocaleDateString()} {when.toLocaleTimeString()}
          {f.ageHours != null && <> · {ago(f.ageHours)}</>}
        </p>
      )}
      {f.state === 'never' && <p>Daily job has not run yet.</p>}
      {f.stale && f.state === 'ok' && (
        <p style={{ color: c.warning }}>Over 36 h old — the daily job may not be running.</p>
      )}
      <p style={{ marginTop: 5 }}>
        <button className="link-btn" onClick={onRefetch} style={{ fontSize: 11.5 }}>
          Re-fetch data
        </button>
        {reloadedAt && <span> · {reloadedAt}</span>}
      </p>
    </div>
  )
}

/**
 * Page-level banner. Rendered only when the last automatic refresh failed or is stale, so it
 * stays out of the way on a healthy day.
 */
export function FreshnessBanner() {
  const f = getFreshness()
  if (f.state === 'ok' && !f.stale) return null
  if (f.state === 'never') return null

  const bad = f.state === 'failed'
  return (
    <div
      className="card"
      style={{
        borderLeft: `3px solid ${bad ? c.critical : c.warning}`,
        marginBottom: 16,
        padding: '12px 15px',
      }}
      role="status"
    >
      <p style={{ margin: 0, fontWeight: 620, fontSize: 13 }}>
        {bad ? 'The last automatic data refresh failed' : 'This data may be out of date'}
      </p>
      <p style={{ margin: '4px 0 0', fontSize: 12.5, color: c.inkSecondary }}>
        {f.detail}
      </p>
      {f.failedSteps?.length > 0 && (
        <p className="prov" style={{ marginTop: 6 }}>
          Failed step{f.failedSteps.length === 1 ? '' : 's'}: {f.failedSteps.join(' · ')} — full log in{' '}
          <code>state/daily/daily.log</code>
        </p>
      )}
    </div>
  )
}
