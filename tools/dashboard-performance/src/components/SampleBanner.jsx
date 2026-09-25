import { isSample, getSampleNote } from '../services/dataService'
import { c } from '../theme'

/**
 * Standing banner shown while the datasets are SAMPLE rather than measured. This is the honesty
 * guard: no illustrative latency in this dashboard may ever be mistaken for a real result. It
 * disappears automatically once the generator ingests a real k6 run (dataState = "measured").
 */
export function SampleBanner() {
  if (!isSample()) return null
  return (
    <div
      className="card"
      role="status"
      style={{ borderLeft: `3px solid ${c.warning}`, marginBottom: 16, padding: '11px 15px' }}
    >
      <p style={{ margin: 0, fontWeight: 640, fontSize: 13 }}>Sample data — not a real execution</p>
      <p style={{ margin: '4px 0 0', fontSize: 12.5, color: c.inkSecondary }}>
        {getSampleNote()} The Sanity scope (modules and check counts) is real; the timings are
        illustrative so the dashboard can be reviewed before the first run.
      </p>
    </div>
  )
}
