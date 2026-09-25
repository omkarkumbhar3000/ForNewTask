/**
 * What engage suggests, plus what each decision verb actually commits you to.
 *
 * ⚠️ PARTIAL, and the gap is stated rather than papered over. engage emits its
 * recommendations as plain strings with no machine-readable distinction between
 * "this is a measurement" and "this is a suggestion". So they are shown verbatim
 * and labelled as recommendations wholesale. Splitting fact from suggestion needs
 * engage to carry that flag per item — until it does, inferring it here would be
 * exactly the fabrication this project forbids.
 */
export function Recommendations({ ctx }) {
  const recs = ctx.recommended || []
  const vocab = ctx._vocabulary || {}
  const actions = ctx._actions || {}

  return (
    <>
      <header className="page-head">
        <h1>Recommendations</h1>
        <p className="lede">
          {recs.length} suggested next step(s) from the last analysis.
        </p>
      </header>

      <section className="sec">
        <h2>Suggested next</h2>
        {recs.length === 0 ? (
          <p className="muted">engage had nothing to suggest on the last run.</p>
        ) : (
          <ol className="numbered">
            {recs.map((r, i) => (
              <li key={i}>
                <span className="prov">recommendation</span> {String(r)}
              </li>
            ))}
          </ol>
        )}
        <p className="note">
          ⚠️ These are <strong>recommendations, not measurements</strong>. engage does not
          yet tag them individually, so they are labelled as a group. Anything on Overview
          or Applications marked <span className="prov prov-measured">detected</span> was
          measured; nothing on this page was.
        </p>
      </section>

      <section className="sec">
        <h2>What each decision means</h2>
        <p className="muted">
          Defined behaviour, not loose labels — otherwise &ldquo;ignore&rdquo; quietly
          becomes &ldquo;never show me this defect again&rdquo;.
        </p>
        <dl className="kv kv-wide">
          {Object.entries(vocab).map(([verb, meaning]) => (
            <div key={verb}>
              <dt>{verb}</dt>
              <dd>{meaning}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section className="sec">
        <h2>Actions this server will perform</h2>
        <p className="muted">
          The whitelist is held server-side. Anything not on this list is refused by name,
          however the request is shaped.
        </p>
        <ul className="plain">
          {Object.entries(actions).map(([name, m]) => (
            <li key={name}>
              <code>{name}</code>
              {m.reversible ? ' · reversible' : ' · NOT reversible'}
              {m.safe ? ' · safe' : ' · NOT safe'}
              {m.autoApprovable ? ' · may be always-approved' : ' · always asks'}
            </li>
          ))}
        </ul>
      </section>
    </>
  )
}
