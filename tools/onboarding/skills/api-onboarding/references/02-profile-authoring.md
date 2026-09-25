# Phase 1 — Authoring the profile

**Purpose:** how to fill `profiles/<key>.json`, and what each field actually decides.
**Contract:** `profile.schema.json` · **Worked example:** `profiles/pam.json` · **Gate:** `validate_profile.py`

The profile is the whole point of the design. It is the boundary between *generic machinery* and
*one project's facts* — everything the reference implementation hardcodes appears here as a field.

---

## 1. Rules that apply to every field

| Rule | Detail |
|---|---|
| **Key names, never secret values** | `credential_keys` maps a logical credential to the *key name* in the environment's config file. A profile is shared and reviewed; the validator refuses a value that looks like a real token |
| **`UNKNOWN` is a legitimate value** | It is an unanswered question with an owner, and the validator will tell you which ones block execution. Deleting the sentinel to make the gate pass is the one genuinely dishonest move available here |
| **Measured, or labelled** | Any count carries the artifact it came from. `count_basis` exists because a bare number cannot be re-derived |
| **One environment per profile** | Copy the file for a second environment. Environments differ in ways that matter — deployed surface, stability, seed data |
| **Notes carry the *why*** | Every non-obvious setting gets a `notes` entry. `verify_tls: false` with no reason is indistinguishable from carelessness |

---

## 2. The order to fill it in

Each section is only answerable once the one above it is. Filling out of order produces a profile
that validates and is still wrong.

| Order | Section | Depends on |
|---:|---|---|
| 1 | `project`, `workspace` | Nothing |
| 2 | `environment` | An owner decision about which environment |
| 3 | `auth` | One successful authenticated call |
| 4 | `envelope` | **A probe run** — Phase 2, not documentation |
| 5 | `catalogue` | The catalogue source existing |
| 6 | `safety` | The developers' answer on harmful endpoints |
| 7 | `identity_prelude`, `id_aliases` | Understanding one create end to end |
| 8 | `payloads` | A body source, if any |
| 9 | `validation`, `reporting` | Everything above |

---

## 3. The fields that decide the most

### `environment.is_production`

Must be `false`. The validator treats anything else as a refusal rather than a warning, because
this solution issues writes and no amount of care makes that safe against production.

### `auth.lockout_risk` and `max_token_attempts_per_run`

Set `lockout_risk` from an answer, not an assumption; while it is `UNKNOWN`, treat it as `high`.
When it is `high`, attempts must be `1` and `latch_on_failure` must be `true`.

**The latch is the part that is easy to skip and expensive to omit.** A failed attempt must block
every later attempt — in this run *and future runs* — until a human clears it. Without a persistent
latch, "one attempt per run" becomes "one attempt per run, forever", which is arithmetically
identical to a retry loop across a week of CI. That is precisely how the reference project's shared
service account was locked.

### `catalogue.adapter`

The single biggest cost lever in onboarding:

| Adapter | Relative cost | Notes |
|---|---|---|
| `openapi` | Lowest | Catalogue and payload schemas both come free |
| `postman` | Low | Real bodies, real headers; coverage limited to what someone collected |
| `har` / `recorded-traffic` | Medium | Real payloads, exact shapes; only covers exercised paths |
| `csv` / `router-dump` | Medium | Paths but no bodies |
| `java-constants` (or any in-code catalogue) | Highest | What the reference project needed. Custom parser, and drift is silent |

⚠️ **Whatever the adapter, assert `expected_count`.** A catalogue that silently yields fewer
endpoints than last time reads as a clean run with less coverage.

### `envelope.status_is_authoritative`

Only set `true` when a deliberately malformed request has been *observed* returning `4xx`. Default
`false` — the cost asymmetry is stark: assuming honesty when the API returns `200` for rejections
makes every assertion decorative, while assuming dishonesty on an honest API merely adds a
redundant check.

### `safety.blocklist`

An empty blocklist is a claim that no endpoint can harm the environment. Sometimes true — but it
must be a recorded answer, not an omission. The validator warns on empty precisely so the question
gets asked once rather than discovered during a run.

Two properties matter: it is enforced at **planning time**, before a request is constructed, and it
matches on **action names**, because deletion is frequently expressed as a `POST`.

### `identity_prelude`

The hops that discover context ids. Two mechanics make it worth writing carefully:

| Mechanic | Instead of | Because |
|---|---|---|
| `find_extract` — select the row *where* a field matches, then take ids from it | `Result[0]` | The first row is rarely the right one. On the reference project row 0 is a record with no child data, so blind first-row chaining fails |
| Join on whatever key the *next* endpoint exposes | Assuming one id everywhere | Endpoints frequently expose a *name* where their sibling expects an *id* |

### `validation.layers`

Start with `L1` status, `L2` content-type, `L3` envelope, `L5` chain-key, `L7` latency. Add `L4`
message-semantics once you know what a real success message says, `L6` record-exists once a create
can be read back, `L11` db-persistence once a read-only account exists.

⛔ `L1` alone is refused by the validator. Status-only validation is the exact failure mode this
whole approach exists to prevent.

---

## 4. Running the gate

```
python tools/onboarding/validate_profile.py profiles/<key>.json    # one profile
python tools/onboarding/validate_profile.py --all                  # every profile
```

Exit `0` ready · `1` blocked · `2` usage error. Zero HTTP calls in every mode, so it is safe to run
in CI and safe to run repeatedly.

| Class | Meaning |
|---|---|
| `[BLOCK]` | Execution is not permitted. An unanswered question, an unsafe setting, or a validation set that cannot detect failure |
| `[WARN]` | A run is possible with reduced coverage or a latent hazard. **State each one in the run report** rather than letting it pass unmentioned |
| `[NOTE]` | Context worth knowing, no action required |

**A clean profile is not a correct profile.** The validator checks completeness and internal
consistency; only the probe in Phase 2 can tell you whether the `envelope` section describes
reality. `profiles/pam.json` validates with zero blockers and still carries five open `unknowns` —
that is the intended steady state, not a failure.
