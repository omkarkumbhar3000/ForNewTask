import { Kpi } from '../components/Kpi'
/**
 * What happened — both the last engage analysis run and the last batch this page
 * executed.
 *
 * Failures are shown with a reason and a next step rather than a status code,
 * because "it failed" without a cause is the thing that makes a person distrust a
 * tool. Refusals are shown separately from failures: a refused action did not go
 * wrong, it was never allowed, and conflating the two would hide a whitelist
 * mismatch behind a red mark.
 */
export function Execution({ ctx, result, executions }) {
  const steps = ctx.steps || []
  const recent = (executions || []).slice(-15).reverse()

  return (
    <>
      <header className="page-head">
        <h1>Execution results</h1>
        <p className="lede">
          {result ? 'Outcome of the batch you just submitted.' : 'No batch submitted in this session yet.'}
        </p>
      </header>

      {result?.error ? (
        <section className="sec">
          <p className="warn">
            The request itself failed: {result.error}
            <br />
            The decisions were recorded before execution was attempted, so nothing was lost.
            Check that control_center.py is still running, then submit again.
          </p>
        </section>
      ) : null}

      {result?.summary ? (
        <section className="sec">
          <h2>This batch</h2>
          <div className="grid grid-kpi">
            <Kpi title="Completed" value={result.summary.ok} tone="good" />
            <Kpi title="Failed" value={result.summary.failed} tone={result.summary.failed ? 'bad' : undefined} />
            <Kpi title="Refused" value={result.summary.refused} note="not failures — never allowed" />
          </div>

          {(result.results || []).map((r, i) => (
            <p key={i} className={r.ok ? '' : 'warn'}>
              {r.ok ? '✓' : '✗'} <code>{r.action}</code>{r.target ? ` ${r.target}` : ''} — {r.reason}
              {!r.ok && r.recomputed ? (
                <>
                  <br />
                  <span className="muted small">
                    The server re-derived the plan before acting and no longer agreed it was
                    safe. That is the guard working: the tree changed after this page rendered.
                  </span>
                </>
              ) : null}
            </p>
          ))}

          {(result.refused || []).length ? (
            <>
              <h3>Refused (not failures)</h3>
              <ul className="plain">
                {result.refused.map((r, i) => (
                  <li key={i}><code>{r.action || 'unknown'}</code> — {r.reason}</li>
                ))}
              </ul>
            </>
          ) : null}
        </section>
      ) : null}

      <section className="sec">
        <h2>Last engage analysis</h2>
        {steps.length === 0 ? (
          <p className="muted">The context recorded no steps.</p>
        ) : (
          <ul className="plain">
            {steps.map((s, i) => (
              <li key={i}>
                <span className="prov">{s.status}</span> <strong>{s.step}</strong>
                {s.detail ? ` — ${s.detail}` : ''}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="sec">
        <h2>Recent executions ({recent.length})</h2>
        {recent.length === 0 ? (
          <p className="muted">The execution journal is empty.</p>
        ) : (
          <ul className="plain">
            {recent.map((r, i) => (
              <li key={i}>
                {r.ok ? '✓' : '✗'} {String(r.at || '').slice(0, 16).replace('T', ' ')}{' '}
                <code>{r.action}</code>{r.target ? ` ${r.target}` : ''} — {r.reason}
              </li>
            ))}
          </ul>
        )}
      </section>
    </>
  )
}
