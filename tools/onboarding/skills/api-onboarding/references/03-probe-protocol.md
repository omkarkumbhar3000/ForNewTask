# Phases 2 and 3 — Probe, then one chain by hand

**Purpose:** establish what the API actually does before designing anything that asserts against it.
**Rule:** these two phases produce *knowledge*, not coverage. Resist the pull toward scale.

Skipping either is the most common way this onboarding fails, and the failure is delayed: hundreds
of generated flows all assert the wrong thing, and they do it consistently enough to look right.

---

## 1. Why probe at all

The documentation describes an intent. The API exhibits a behaviour. Where they differ, only the
behaviour matters — and on the reference project they differed sharply: documentation covered 6
response shapes, the API produced **31**, of which **127 responses were not JSON objects at all**.

An assertion designed from documentation is a guess with good grammar.

---

## 2. Probe protocol

**Scope:** 10–20 endpoints, **reads only**, spread across different functional areas. Not a load
test, not a coverage attempt.

| Step | Action | Records |
|---:|---|---|
| 1 | Confirm the API origin answers at all | That `api_base` is the API, not the UI |
| 2 | Obtain one credential, once, and cache it | `auth` is correct and `token_lifetime_hours` is real |
| 3 | Call each read endpoint, save the **raw body verbatim** | The shape census |
| 4 | Reduce each body to its top-level shape and count distinct shapes | `envelope.shapes_measured`, `shape_census` |
| 5 | Send **one deliberately malformed** request | `envelope.status_is_authoritative` — the decisive test |
| 6 | Send **one request with a deliberately invalid credential** | Whether unauthenticated access is actually refused |
| 7 | Record min / median / p95 latency per endpoint class | `validation.sla_ms`, split read vs write |

### What to write down, per response

Body verbatim (redacted), HTTP status, content-type, top-level key set, where the payload rows live,
how success is signalled, and — if it failed — how the failure was expressed.

### The five questions the probe must answer

| # | Question | Consequence of getting it wrong |
|---:|---|---|
| 1 | Does a rejected request return `4xx`? | Every assertion is decorative if the answer is no and you assumed yes |
| 2 | How is success signalled, and in what **casing**? | A case-sensitive lookup for the wrong casing fails on every response the API can produce — this happened on the reference project, where PascalCase appears 1,580 times and camelCase 0 |
| 3 | Can success mean nothing happened? | A create assertion passes against a no-op |
| 4 | Do all endpoints share one shape? | A fixed-shape parser throws on the first bare array |
| 5 | Is an unauthenticated request refused? | Authorization tests may be asserting against a valid session without knowing it |

⚠️ **Question 6, implicitly: is an error code that you do not recognise a test failure?** No. It is
an observation, and the defect is the missing product registry. A hardcoded allowlist of known codes
turns every undocumented product code into a red test — the reference project's original
implementation asserted an allowlist of three and would have failed a genuine, correct response.

---

## 3. Recording the outcome

Write the `envelope` section of the profile **from the census**, then re-run the validator. If
`shapes_measured` is still `0`, the probe has not been done, whatever else exists.

The census is an artifact, not a note in a chat: a file listing each distinct shape with one example
endpoint. It is what the assertion design is reviewed against, and what the next person reads
instead of re-probing.

---

## 4. Phase 3 — one chain, by hand

**One flow, 3–5 hops, hand-written, end to end.** The exit criterion is narrow and specific: a real
value produced by one call is used by the next and then *verified downstream*.

| Hop | Purpose |
|---:|---|
| 1 | Discover a context id **by name**, not by position |
| 2 | Use it in a second read that requires it |
| 3 | Create something, with every unique field randomised for this run |
| 4 | Read the created thing back and confirm the id and the values |
| 5 | Confirm it appears in a *list* endpoint under the right parent |

### Why by hand, and why before generating

Because this is where the subtleties surface, and they generalise:

| What surfaces | What it becomes |
|---|---|
| A success flag accompanying a create that created nothing | The `noop_messages` rule, applied to every generated create |
| The first row of a list being the wrong record | `find_extract` instead of `Result[0]`, everywhere |
| A sibling endpoint exposing a *name* where this one wants an *id* | The join key in the prelude |
| A write taking far longer than a read | Split latency budgets |
| An id arriving as a string on create and an integer on read | Type-loose matching, strict asserting |

Each of these was learned once, by hand, on the reference project and then applied to hundreds of
generated flows. Discovering them *after* generating is a rework of everything.

### Be liberal in matching, strict in asserting

Field lookups should be case-insensitive and type-loose, because the same field is spelled several
ways across controllers and changes type between operations. The *assertions* stay strict. Loose
matching prevents false failures; strict assertion prevents false passes. The two are not in
tension — they operate on different things.

---

## 5. Exit gate

Do not proceed to generation until all four hold:

| ✅ | Condition |
|---|---|
| ☐ | Every response shape the probe saw is named in the profile |
| ☐ | You can state, from observation, how this API expresses a rejection |
| ☐ | One hand-written chain passes a real value forward and verifies it downstream |
| ☐ | The latency budgets distinguish reads from writes |
