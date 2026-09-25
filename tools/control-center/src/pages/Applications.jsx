import { Decide } from '../components/Decide'

/**
 * Per-repository state, and the one action engage may offer for it.
 *
 * The pull option appears only where engage itself decided a fast-forward is safe:
 * policy allows it, tree clean, upstream exists, strictly behind rather than
 * diverged, and no merge or rebase in progress. Anywhere else the repository is
 * still reported but not actionable, and the reason is shown — an option that is
 * silently absent teaches nothing.
 */
export function Applications({ items, decisions, setDecision }) {
  return (
    <>
      <header className="page-head">
        <h1>Applications</h1>
        <p className="lede">
          {items.repos.length} repositories discovered. Rights differ per repository, so
          an action offered on one is not offered on another.
        </p>
      </header>

      {items.repos.map((r) => (
        <Decide key={r.key} item={r} decision={decisions[r.key]} onDecide={setDecision}>
          <dl className="kv">
            <div><dt>State</dt><dd>{r.state}</dd></div>
            <div>
              <dt>Policy</dt>
              <dd>{r.policy || (r.known ? 'classified' : 'unclassified')}</dd>
            </div>
            {r.commits ? <div><dt>New commits</dt><dd>{r.commits}</dd></div> : null}
            {r.files ? <div><dt>Local changes</dt><dd>{r.files} file(s)</dd></div> : null}
            {r.pulled ? <div><dt>This run</dt><dd>fast-forwarded</dd></div> : null}
          </dl>
          {r.reason ? <p className="item-body">{r.reason}</p> : null}
          {!r.known ? (
            <p className="warn">
              ⚠ Unclassified repository. engage fetches and reports it but will never pull
              it. The fix is to add it to engage_core.POLICIES with explicit rights —
              loosening the default is not the fix.
            </p>
          ) : null}
        </Decide>
      ))}
    </>
  )
}
