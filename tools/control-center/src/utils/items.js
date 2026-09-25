/**
 * Turning engage's context into decidable items.
 *
 * engage was built to be READ, not clicked: its attention list carries
 * {action, priority, source, text} and no stable identifier, because a terminal
 * report never needed one. A decision UI does — "the user ignored THIS" is
 * meaningless without a key that survives the next run.
 *
 * So two things are derived here, and both are derived rather than invented:
 *
 *   key          stable across runs while the item is the same item. Built from
 *                the item's source and its text, so the same finding gets the
 *                same key tomorrow.
 *   fingerprint  changes when the item's material STATE changes. This is what
 *                makes "not interested" expire by itself instead of burying a
 *                finding for ever — the same trick the drift loop's waivers use,
 *                where a waiver is keyed to the evidence hash it was granted
 *                against.
 *
 * ⛔ Action types are NOT invented here. An item only offers an action if engage
 * itself said one was available (repositories[].action === 'pull'), or if the
 * action is a pure local re-derivation. Everything else is decision-only. The
 * server would refuse anything else anyway; this keeps the UI honest about it.
 */

/** Small stable string hash. Not cryptographic — it only needs to be consistent. */
function hash(s) {
  let h = 2166136261
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return (h >>> 0).toString(36)
}

/** Provenance, kept verbatim from engage. Never collapse these into one word. */
export const PROVENANCE = {
  detected: 'engage measured this just now',
  'project-data': 'read from a file the project maintains — may be stale',
}

export function provenanceLabel(source) {
  if (!source) return 'unknown'
  return source === 'detected' ? 'detected' : source
}

/** Priority order for sorting, worst first. */
const RANK = { critical: 0, high: 1, normal: 2, low: 3 }
export const rank = (p) => (p in RANK ? RANK[p] : 9)

/**
 * Decisions offered per item kind. Deliberately NOT the same list everywhere —
 * offering "Pull changes" on a documentation drift item would be noise, and
 * offering "Accept" on something with no executable action would be a lie.
 */
export function decisionsFor(item) {
  if (item.action) {
    return item.needsConfirmation
      ? ['approve', 'reject', 'review', 'defer']
      : ['accept', 'ignore_once', 'review', 'defer']
  }
  return ['ignore_once', 'consider_next', 'not_interested', 'review', 'defer']
}

/** Repositories → decidable items. */
export function repoItems(ctx) {
  return (ctx.repositories || []).map((r) => {
    const canPull = r.action === 'pull'
    const state = r.state || r.reason || 'unknown'
    return {
      kind: 'repository',
      name: r.name || r.rel,
      rel: r.rel,
      branch: r.branch || r.state_branch || null,
      state,
      reason: r.reason || '',
      severity: r.severity || (r.attention ? 'normal' : 'low'),
      needsConfirmation: Boolean(r.needs_confirmation),
      policy: r.policy || null,
      commits: r.commits || 0,
      files: r.files || 0,
      pulled: Boolean(r.pulled),
      known: r.known !== false,
      // Only offered when engage itself decided a fast-forward is safe.
      action: canPull ? 'repo.pull_ff_only' : null,
      target: r.rel,
      key: `repo:${r.rel}`,
      fingerprint: hash(`${r.rel}|${state}|${r.commits || 0}|${r.files || 0}`),
      source: 'detected',
    }
  })
}

/** Attention list → decidable items. */
export function attentionItems(ctx) {
  return (ctx.attention || []).map((a, i) => {
    const text = a.text || ''
    return {
      kind: 'attention',
      text,
      hint: a.action || '',
      severity: (a.priority || 'normal').toLowerCase(),
      source: a.source || 'unknown',
      needsConfirmation: /confirm|diverged|conflict|uncommitted/i.test(text),
      // Attention items are analysis, not operations. The one exception is stale
      // derived data, which a local re-derivation genuinely fixes.
      action: /stale|re-derive|refresh/i.test(text) ? 'data.refresh' : null,
      target: '',
      key: `att:${hash(`${a.source || ''}|${text.slice(0, 120)}`)}`,
      fingerprint: hash(text),
      index: i,
    }
  })
}

/** Open objectives, resume points and TODOs → the pending-work list. */
export function pendingItems(ctx) {
  const out = []
  for (const o of ctx.open_objectives || []) {
    out.push({
      kind: 'objective', name: o.id, text: o.title || '',
      severity: 'normal', source: 'project-data', action: null, target: '',
      key: `obj:${o.id}`, fingerprint: hash(`${o.id}|${o.title || ''}`),
    })
  }
  for (const r of ctx.resume_points || []) {
    out.push({
      kind: 'resume', name: (r.file || '').split(/[\\/]/).pop(), text: r.note || '',
      severity: 'high', source: 'project-data', action: null, target: '',
      key: `resume:${r.file}`, fingerprint: hash(`${r.file}|${r.note || ''}`),
    })
  }
  for (const t of ctx.todos || []) {
    out.push({
      kind: 'todo', name: `${(t.file || '').split(/[\\/]/).pop()}:${t.line || ''}`,
      text: t.text || '', severity: 'low', source: 'detected', action: null, target: '',
      key: `todo:${t.file}:${t.line}`, fingerprint: hash(t.text || ''),
    })
  }
  return out
}

/**
 * Apply recorded decisions. An item is hidden only when a suppression still
 * matches its CURRENT fingerprint — so if the underlying state moved, the item
 * comes back rather than staying buried.
 */
export function applySuppressions(items, suppressions, currentRun) {
  return items.map((it) => {
    const s = suppressions?.[it.key]
    if (!s) return it
    const stale = s.fingerprint && s.fingerprint !== it.fingerprint
    let hidden = false
    let carried = false
    if (!stale) {
      if (s.decision === 'not_interested') hidden = true
      if (s.decision === 'ignore_once') hidden = s.run === currentRun
      if (s.decision === 'consider_next' || s.decision === 'defer') carried = true
    }
    return {
      ...it,
      hidden,
      carried,
      priorDecision: s.decision,
      priorAt: s.at,
      suppressionLapsed: Boolean(stale),
    }
  })
}

/** "Safe actions" for bulk selection: reversible, safe, and not needing confirmation. */
export function isSafeAction(item, actionsMeta) {
  if (!item.action) return false
  if (item.needsConfirmation) return false
  const m = actionsMeta?.[item.action]
  return Boolean(m && m.reversible && m.safe)
}
