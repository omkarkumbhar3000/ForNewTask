/**
 * The confirmation summary and the one button that acts.
 *
 * Deliberately separates "will execute" from "will only be recorded", because the
 * owner asked for a final summary before anything runs and those two are not the
 * same commitment. A decision like "not interested" is a real choice worth saving
 * and involves no execution at all; conflating them would make Execute look
 * bigger and scarier than it is, or smaller and more dangerous.
 *
 * "Select all safe actions" is offered instead of a plain "select all", per the
 * owner's own suggestion: safe here means the server declared the action type both
 * reversible and safe AND the item does not need confirmation.
 */
export function SelectionBar({ plan, busy, onBulk, onSubmit }) {
  const nothing = plan.total === 0
  return (
    <div className="selbar" role="region" aria-label="Pending decisions">
      <div className="selbar-bulk">
        <button type="button" className="btn btn-quiet" onClick={() => onBulk('safe')}>
          Select safe actions
        </button>
        <button type="button" className="btn btn-quiet" onClick={() => onBulk('high')}>
          Select high priority
        </button>
        <button type="button" className="btn btn-quiet" onClick={() => onBulk('none')} disabled={nothing}>
          Clear
        </button>
      </div>

      <div className="selbar-summary">
        {nothing ? (
          <span className="muted">No decisions selected yet.</span>
        ) : (
          <>
            {plan.executing.length ? (
              <span className="chip chip-act">
                {plan.executing.length} will execute
              </span>
            ) : null}
            {plan.recording.length ? (
              <span className="chip">
                {plan.recording.length} recorded only
              </span>
            ) : null}
          </>
        )}
      </div>

      <button
        type="button"
        className="btn btn-primary"
        disabled={nothing || busy}
        onClick={onSubmit}
      >
        {busy ? 'Working…' : plan.executing.length
          ? `Engage & execute (${plan.executing.length})`
          : `Save ${plan.total} decision${plan.total === 1 ? '' : 's'}`}
      </button>
    </div>
  )
}
