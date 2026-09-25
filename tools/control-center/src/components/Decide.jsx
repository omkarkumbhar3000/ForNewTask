import { decisionsFor, PROVENANCE, provenanceLabel } from '../utils/items'

const LABELS = {
  accept: 'Accept', approve: 'Approve', reject: 'Reject',
  ignore_once: 'Ignore this time', consider_next: 'Consider next time',
  not_interested: 'Not interested', defer: 'Defer', review: 'Review manually',
}

const SEV_CLASS = {
  critical: 'sev sev-critical', high: 'sev sev-high',
  normal: 'sev sev-normal', low: 'sev sev-low',
}

/**
 * One decidable item.
 *
 * Two things here are load-bearing rather than decorative:
 *
 *  - The provenance chip. engage separates what it MEASURED from what it read out
 *    of a project file that may be stale, and that distinction has to survive into
 *    the UI or the owner cannot tell a fact from a claim.
 *
 *  - The verb list comes from decisionsFor(item), so an item with no executable
 *    action never offers "Accept". Offering it would imply something would happen.
 */
export function Decide({ item, decision, onDecide, children }) {
  const verbs = decisionsFor(item)
  const isDestructiveish = item.needsConfirmation

  return (
    <div className={item.hidden ? 'item is-hidden' : 'item'}>
      <div className="item-head">
        <span className={SEV_CLASS[item.severity] || SEV_CLASS.normal}>
          {item.severity || 'normal'}
        </span>
        <span className="item-title">{item.name || item.text}</span>
        <span
          className={item.source === 'detected' ? 'prov prov-measured' : 'prov'}
          title={PROVENANCE[item.source] || 'provenance not stated by engage'}
        >
          {provenanceLabel(item.source)}
        </span>
        {item.carried ? <span className="chip chip-carried">carried over</span> : null}
        {item.suppressionLapsed ? (
          <span className="chip chip-lapsed" title="The state changed, so a previous dismissal expired">
            reappeared
          </span>
        ) : null}
      </div>

      {item.name && item.text ? <p className="item-body">{item.text}</p> : null}
      {children}

      {isDestructiveish ? (
        <p className="warn">
          ⚠ Needs explicit approval. {item.reason || 'engage flagged this as needing a human decision.'}
          {' '}It will not run on a bulk selection.
        </p>
      ) : null}

      {item.priorDecision && !item.suppressionLapsed ? (
        <p className="muted small">
          Previously: <strong>{LABELS[item.priorDecision] || item.priorDecision}</strong>
          {item.priorAt ? ` · ${item.priorAt.slice(0, 16).replace('T', ' ')}` : ''}
        </p>
      ) : null}

      <div className="verbs" role="group" aria-label="Decision">
        {verbs.map((v) => (
          <button
            key={v}
            type="button"
            className={decision === v ? 'verb is-on' : 'verb'}
            onClick={() => onDecide(item.key, v)}
          >
            {LABELS[v] || v}
          </button>
        ))}
        {item.action ? (
          <span className="verb-note" title="The action engage would run">
            → {item.action}
          </span>
        ) : (
          <span className="verb-note muted">records a decision only</span>
        )}
      </div>
    </div>
  )
}
