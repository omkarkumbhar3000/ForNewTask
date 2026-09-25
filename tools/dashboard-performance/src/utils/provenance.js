import { getManifest } from '../services/dataService'

/**
 * The provenance line printed under every chart.
 *
 * ⛔ Why this exists: the chart footers were hardcoded to "Sample data." in nine places. Once a real
 * run was ingested, the dashboard rendered MEASURED numbers with a footer still calling them sample
 * data. Both directions of that mistake are damaging - illustrative figures read as real, or real
 * figures dismissed as fake in front of management. Provenance must be derived from the data, never
 * typed into a component.
 *
 * Pass the page's own dataset so a per-view state ('not-measured' for the API and comparison views)
 * beats the global one; falls back to the manifest.
 */
export function sourceLabel(ds) {
  const m = getManifest() || {}
  const state = (ds && ds.dataState) || m.dataState

  if (state === 'measured') {
    const run = (ds && ds.runId) || m.currentRunId
    const vus = (ds && ds.concurrentUsers) || m.concurrentUsers
    const parts = ['Measured']
    if (run) parts.push(`run ${run}`)
    if (vus) parts.push(`${vus} concurrent user${vus === 1 ? '' : 's'}`)
    if (m.environment) parts.push(m.environment)
    return parts.join(' · ')
  }

  if (state === 'not-measured') {
    return (ds && ds.reason) ? `Not measured · ${ds.reason}` : 'Not measured for this run.'
  }

  return 'Sample data · illustrative, not a real execution.'
}
