# Phase 0 — Discovery questionnaire

**Purpose:** the questions to answer before any code, any call, any estimate.
**Rule:** an unanswered question is recorded as an `UNKNOWN` with an owner. It is never guessed.

Send this as a form. Each answer maps to one profile field, named in the last column, so answering
the questionnaire *is* authoring the profile.

---

## 1. Access and safety — ask first, because a wrong answer here is expensive

| # | Question | Why it matters | Profile field |
|---:|---|---|---|
| 1.1 | Which non-production environment may automation write to? | Writes are issued. There is no read-only mode that still proves persistence | `environment.name` |
| 1.2 | Is that environment shared with anyone else, and who? | A shared QA environment turns a broken test into someone else's outage | `environment.notes` |
| 1.3 | Which host and port serve the **API**, as opposed to the UI? | A UI origin answers 404 to every `/api` call. This is the most common false "the endpoints don't exist" report | `environment.api_base`, `app_base` |
| 1.4 | Is the certificate valid, or self-signed? | Decides `verify_tls`, and stops a TLS error being read as an outage | `environment.verify_tls` |
| 1.5 | **Which endpoints are expensive, long-running, or capable of taking the environment down?** | The blocklist. Record "none known" if that is the answer — so the next person knows the question was asked | `safety.blocklist` |
| 1.6 | How is deletion expressed — a `DELETE` verb, or a named action? | Decides whether the destructive guard can key on verbs at all. On the reference project deletion is a `POST`, so verbs are useless | `safety.destructive_name_regex` |
| 1.7 | Are there documented rate limits? | Replaces a fixed throttle with limit-aware backoff | `safety.rate_limit` |
| 1.8 | How stable is the environment, historically? | Decides whether wait-and-resume is built before or after scaling up. It should be before | `environment.stability` |

## 2. Authentication — the first hard gate

| # | Question | Why it matters | Profile field |
|---:|---|---|---|
| 2.1 | How is a request authenticated? | ⛔ Hard blocker | `auth.kind` |
| 2.2 | Which endpoint issues the credential, and what does it need? | | `auth.token_endpoint`, `credential_keys` |
| 2.3 | **Does the account lock after failed attempts?** | ⛔ Governs everything about retry. Assume yes until told no | `auth.lockout_risk` |
| 2.4 | **Is that account used by anything other than testing?** | Decides the blast radius of a lockout. On the reference project the automation account was also the data-warehouse ETL identity | `auth.lockout_risk`, `notes` |
| 2.5 | How long does a credential live? | Decides cache expiry. One token per run, reused | `auth.token_lifetime_hours` |
| 2.6 | Can a token be supplied out-of-band for unattended runs? | The safest option: bypasses the credential endpoint entirely | `auth.env_var_override` |
| 2.7 | **Are there multiple roles, and can automation hold two identities?** | Without a second identity every authorization test is inert — it cannot fail. See `04-generation.md` §4 | `auth.roles` |
| 2.8 | Are extra headers required — API version, tenant, correlation id? | A missing static header presents as a blanket 400 | `auth.extra_headers` |

## 3. The catalogue — the second hard gate

| # | Question | Why it matters | Profile field |
|---:|---|---|---|
| 3.1 | **Is there an OpenAPI / Swagger document?** | The single biggest cost lever in the whole onboarding. With one, the catalogue *and* most payloads come free | `catalogue.adapter` |
| 3.2 | If not: a Postman collection? Recorded traffic? A route dump? Constants in an existing test project? | The fallback order, cheapest first | `catalogue.adapter`, `source` |
| 3.3 | How many endpoints should the adapter find, and **on what basis** was that counted? | A count with no basis is not verifiable. The reference project's one file yields four different totals depending on what is counted | `catalogue.expected_count`, `count_basis` |
| 3.4 | Which verbs are actually used, and in what proportion? | Reveals whether verb-based reasoning works | `catalogue.verb_distribution` |
| 3.5 | Which endpoints are deployed on the target environment but not documented — or documented but not deployed? | Prevents a deployment gap being reported as a test failure | `catalogue.exclude_patterns` |
| 3.6 | Is the spec current? Who maintains it? | An out-of-date spec is a *known* quantity; an unknown-age spec is not | `provenance` |

## 4. Payloads and data

| # | Question | Why it matters | Profile field |
|---:|---|---|---|
| 4.1 | Where does a valid request body for a create come from? | Absent, coverage is read-only | `payloads.adapter` |
| 4.2 | Which fields must be unique per run? | Otherwise the second run gets "already exists" instead of creating | `payloads.unique_fields` |
| 4.3 | Which fields are enum-like, where a wrong value breaks the call? | These must be preserved verbatim, never randomised | `payloads` (KEEP set) |
| 4.4 | **To create the simplest thing in this product, which ids must I already hold, and which call produces them?** | This is the prelude. The most commonly missed input | `identity_prelude` |
| 4.5 | Is there seed data automation may rely on, selectable by name? | Selecting by name discovers the id; selecting `[0]` silently picks the wrong record | `identity_prelude` |
| 4.6 | Is there a read-only database account for persistence checks? | Enables the strongest layer. Without it, "success" means "accepted", not "stored" | `validation.database` |

## 5. Response contract — do not accept an answer here without measuring it

| # | Question | Why it matters | Profile field |
|---:|---|---|---|
| 5.1 | **Does a rejected request return `4xx`, or `200` with an in-body error?** | The single most consequential fact. Ask, then *verify with one malformed request* | `envelope.status_is_authoritative` |
| 5.2 | How is success signalled in the body? | | `envelope.success_fields` |
| 5.3 | **Can a "success" response mean nothing was written?** | On the reference project yes — a create returns success with "Already Exists" | `envelope.noop_messages` |
| 5.4 | Is there a published error-code registry? | Match on prefix; record unknown codes as observations, never as test failures | `envelope.error_code_registry` |
| 5.5 | Do any endpoints answer with something other than a JSON object? | Bare arrays, bare booleans, empty strings and HTML error pages all occur in practice | `envelope.non_json_expected` |
| 5.6 | What is a realistic latency for a read, and for a write? | One budget tuned on reads fails every write | `validation.sla_ms` |
| 5.7 | Are there known open defects on this API? | So a product bug is not chased as a test bug | profile `notes` |

## 6. Operating expectations

| # | Question | Why it matters | Profile field |
|---:|---|---|---|
| 6.1 | Who receives the report, and what decision do they make with it? | Decides the reporting format. A management reader and a developer reader need different documents from the same run | `reporting` |
| 6.2 | How long must evidence be retained? | Retain forever unless there is a reason not to. A deleted baseline cannot be recovered | `reporting.retention` |
| 6.3 | Is this expected to run in CI, on a schedule, or on request? | Decides whether the credential must be supplied out-of-band | `auth.env_var_override` |
| 6.4 | What does "done" mean for the first milestone? | Prevents an open-ended engagement | — |

---

## Closing the round

Three outcomes, and all three are acceptable answers to give the user:

| Outcome | Next step |
|---|---|
| All hard gates answered | Proceed to Phase 1, author the profile |
| Hard gate unanswered | **Stop.** Report exactly which gate, who owns it, and what artifact would settle it |
| Soft gaps only | Proceed, and record each as an `unknowns[]` entry with `blocks: false` so the coverage limit is visible in the run report |

⛔ **Never convert an unanswered question into an assumption silently.** If you must proceed on an
assumption, write it into the profile's `notes` and state it in the report.
