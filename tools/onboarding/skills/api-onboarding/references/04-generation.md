# Phase 4 — Generation

**Purpose:** turn a catalogue plus a prelude into executable flow definitions, with no hand-written tests.
**Invariant:** flows are **data**; the executor is **code**. A generator that needs the runner changed is wrong.

---

## 1. The invariant, and why it carries the whole design

The executor knows nothing about the domain. It substitutes variables, issues a call, extracts values,
asserts layers, and carries results forward. Everything domain-specific arrives as JSON.

Three consequences, all of them load-bearing:

| Consequence | Effect |
|---|---|
| Adding coverage means emitting more JSON | No code review, no regression risk in the runner |
| Hand-written and generated flows are the **same artifact** | Nothing built by hand in Phase 3 is thrown away when generation arrives |
| A generator can be replaced wholesale | Swapping an in-code catalogue for an OpenAPI spec changes the generator only |

---

## 2. The flow schema

A flow is an id, a title, a **`why`**, and an ordered list of hops. The `why` is not decoration: it
is what a reviewer reads to decide whether the flow tests anything worth testing.

```json
{
  "id": "service_lifecycle",
  "title": "Create a service under a discovered parent, then confirm it exists",
  "why": "Proves a write persists and is visible through a second, independent read path.",
  "hops": [
    {
      "name": "GetParentList", "verb": "POST", "path": "/api/<C>/GetParentList", "body": {},
      "find_extract": {"in": "Result", "where": {"ParentName": "AUTOMATION_PARENT"},
                       "take": {"PARENT_ID": "ParentId", "PARENT_NAME": "ParentName"}},
      "note": "Selected BY NAME so the id is discovered, never hardcoded.",
      "sla_ms": 8000
    },
    {
      "name": "SetThing", "verb": "POST", "path": "/api/<C>/SetThing",
      "body": {"ParentId": "${PARENT_ID}", "Name": "${NEW_NAME}"},
      "extract_any_id": "THING_ID",
      "expect_message": "created"
    },
    {
      "name": "GetThing", "verb": "POST", "path": "/api/<C>/GetThing",
      "body": {"ThingId": "${THING_ID}"},
      "verify_value_anywhere": "${NEW_NAME}",
      "stop_on_fail": false
    }
  ]
}
```

| Hop key | Purpose |
|---|---|
| `extract` | Dotted selector — `Result[0].GroupId` |
| `find_extract` | Filtered row join: select *where* a field matches, then take ids from that row |
| `extract_any_id` | **Resolved at run time** — take the first field whose name ends in `id` |
| `verify_present` / `verify_value_anywhere` | Prove the created record is really there, whatever field carries it |
| `expect_status`, `expect_error_code`, `expect_message` | Per-hop expectations, including for negative cases |
| `envelope: false` | This endpoint returns a bare array — do not look for an envelope |
| `sla_ms` | Per-hop latency budget |
| `stop_on_fail` | Whether the rest of the chain is attempted. A hop that does not stop the chain must still be *counted* |

### Two mechanisms that make generation possible at all

A generator cannot know whether a create returns `UserId`, `ServiceId` or `MappingId`, and cannot know
which field will carry a value on read-back. Without run-time resolution, every generated flow would
need per-endpoint knowledge — which is the hand-written approach with extra steps.

- **`extract_any_id`** — take the first field whose name ends in `id`.
- **`verify_value_anywhere`** — search the whole response for the value, whatever field holds it.

---

## 3. The generator's structure — classify, pair, emit

Project-independent structure; project-specific rules.

| Stage | What it does | Profile field |
|---:|---|---|
| **Classify** | Bucket every catalogue entry by action name: read · create · change · teardown | generator rules |
| **Filter** | Drop blocklisted, templated, and excluded endpoints — **before** anything is built | `safety.blocklist`, `catalogue.exclude_patterns`, `templated_marker` |
| **Pair** | For each create, find the read most likely to confirm it (same noun, read classification) | — |
| **Prelude** | Prefix every flow with the context-discovery hops | `identity_prelude` |
| **Substitute** | Replace context fields with prelude variables; randomise identity fields; leave enum-like fields alone | `id_aliases`, `payloads.unique_fields` |
| **Emit** | One JSON file per flow, plus a manifest of what was generated and what was withheld | `workspace.flows_dir` |

⚠️ **Pair structurally, not by name inference.** Name-based chain inference — "this field name appears
in two places, therefore they chain" — generates plausible flows that do not hold. On the reference
project 1,680 such candidates were derived from a graph and ultimately not used; structural
create → read pairing on the same noun proved more reliable.

### The three substitution classes

| Class | Rule | Failure if wrong |
|---|---|---|
| **Context** (`ParentId`, `GroupId`) | Replace with the prelude variable | The flow is bound to one environment's data |
| **Identity** (name, email, host) | Randomise per run, with a run-scoped suffix | Second run returns "already exists" instead of creating |
| **Enum-like** (type ids, domains, flags) | **Leave verbatim** | A randomised type id fails the call for an uninteresting reason |

Keep the enum-like set explicit in the profile. It is small, and it is discovered by getting it wrong
once.

---

## 4. Generating negative cases

Positive-only generation covers the easier half of the surface. Three negative dimensions generate
cheaply from the same catalogue:

| Dimension | Method | Expectation |
|---|---|---|
| **Wrong method** | Call a `POST` endpoint with `GET` | The API's documented method-not-allowed behaviour |
| **Unauthenticated** | Send `auth.invalid_token_sample` | Refusal — **and if it is not refused, that is a finding, not a test failure** |
| **Invalid input** | Malform one parameter at a time | The rejection form the probe established |

⛔ **A negative case must be able to fail.** On the reference project 1,153 authored
unauthorized-access cases asserted `401` while sending a *valid* token — unfalsifiable by
construction. Sending a deliberately invalid credential instead converted them into real tests and
surfaced **57 endpoints answering HTTP 200 to an invalid bearer**; after classifying 34 health probes
and 4 client-registration entry points as plausibly by design, **19 required security review**,
several of them writes. That was the single highest-value change in the whole exercise, and it cost
one line of generation logic.

**Where authored expectations already exist** — an existing test suite's data tables, carrying real
expected statuses and error codes — prefer them over synthesised ones. A generated expectation is a
guess; an authored one is a contract someone signed.

---

## 5. Exit gate

```
<generator> --dry-run     # emit flows, zero HTTP calls
<runner>    --dry-run     # load and plan every flow, zero HTTP calls
```

| ✅ | Condition |
|---|---|
| ☐ | Every generated flow loads and plans without error |
| ☐ | Zero HTTP calls were made |
| ☐ | The manifest accounts for **every** catalogue entry: generated, or withheld with a reason |
| ☐ | No blocklisted or destructive action appears in any emitted flow |
| ☐ | Every flow carries a `why` a reviewer can evaluate |
| ☐ | Counts are stated: flows, hops, endpoints reached, endpoints withheld and why |

⛔ **Silent truncation is the failure to guard against here.** If generation covers 800 of 1,300
endpoints, the manifest says so and says why for each of the 500. A generator that quietly emits less
reads as a clean run with unexplained coverage — and nobody notices, because nothing failed.
