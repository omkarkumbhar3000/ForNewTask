/**
 * The only channel between this page and the machine.
 *
 * Everything goes through control_center.py, which holds the server-side action
 * whitelist. This module therefore sends an action TYPE and a target, never a
 * command — there is deliberately no function here that could express one.
 *
 * The token arrives in the URL (?t=…) because the server mints a fresh one per
 * process and never writes it to disk. It is kept in memory only; putting it in
 * localStorage would outlive the server that issued it.
 */

const token = new URLSearchParams(window.location.search).get('t') || ''

/** True when the page was opened without the server's token. */
export const hasToken = Boolean(token)

async function call(path, { method = 'GET', body } = {}) {
  const sep = path.includes('?') ? '&' : '?'
  const res = await fetch(`${path}${sep}t=${encodeURIComponent(token)}`, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  })
  const text = await res.text()
  let data
  try {
    data = text ? JSON.parse(text) : {}
  } catch {
    // A non-JSON body means something upstream failed in a way the server did not
    // shape. Surface the status and the first line rather than "unexpected token".
    throw new Error(`${res.status} ${res.statusText} — ${text.slice(0, 200)}`)
  }
  if (!res.ok) throw new Error(data.error || `${res.status} ${res.statusText}`)
  return data
}

export const getHealth = () => call('/api/health')
export const getContext = ({ refresh = false } = {}) =>
  call(`/api/context${refresh ? '?refresh=1' : ''}`)
export const getDecisions = () => call('/api/decisions')
export const getExecutions = () => call('/api/executions')

/** Record decisions without executing anything. */
export const postDecisions = (items, run) =>
  call('/api/decide', { method: 'POST', body: { items, run } })

/**
 * Execute. Only items whose decision is accept/approve run, and only if their
 * action type is whitelisted server-side — the server re-derives each plan rather
 * than trusting what this page was showing, so a stale "safe to pull" cannot
 * overwrite work committed since the page rendered.
 */
export const postExecute = (items, run) =>
  call('/api/execute', { method: 'POST', body: { items, run } })
