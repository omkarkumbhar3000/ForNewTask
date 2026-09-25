import { Decide } from '../components/Decide'

/**
 * Items engage marked as needing a human decision, and then everything else it
 * raised.
 *
 * Both live on one page on purpose. Nothing that needs confirmation should be
 * reachable only through a filter — a diverged branch or an uncommitted tree is
 * exactly the thing that must not be missed, and a filter is how it gets missed.
 */
export function Approvals({ items, decisions, setDecision }) {
  const needing = items.all.filter((i) => !i.hidden && i.needsConfirmation)
  const rest = items.attention.filter((i) => !i.hidden && !i.needsConfirmation)

  return (
    <>
      <header className="page-head">
        <h1>Approvals</h1>
        <p className="lede">
          {needing.length} item(s) need an explicit decision. Bulk selection never
          includes these, however safe the rest of the batch looks.
        </p>
      </header>

      {needing.length === 0 ? (
        <p className="muted">Nothing is waiting on an explicit approval.</p>
      ) : (
        needing.map((i) => (
          <Decide key={i.key} item={i} decision={decisions[i.key]} onDecide={setDecision} />
        ))
      )}

      <section className="sec">
        <h2>Also raised ({rest.length})</h2>
        <p className="muted">
          Reported by engage but not blocking. Deciding here is how an item stops
          reappearing — Recommendations explains what each verb commits you to.
        </p>
        {rest.map((i) => (
          <Decide key={i.key} item={i} decision={decisions[i.key]} onDecide={setDecision} />
        ))}
      </section>
    </>
  )
}
