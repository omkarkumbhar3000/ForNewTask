# New Project Implementation Guide — onboarding the dynamic API solution onto any project

**Purpose:** how to stand this solution up on a project that does not have it, and how to make it reusable rather than PAM-specific.
**Audience:** whoever onboards the next project, plus the manager who approves it. Assumes no knowledge of this workspace.
**Reference implementation:** PAM — `tools/` + `artifacts/runs/2026-08-05_114315` · **747 flows · 5,590 test cases · 1,388 endpoints · zero hand-written tests**
**Portable kit:** `tools/onboarding/` — profile schema, worked example, readiness gate, onboarding skill
**Objective:** `OBJ-011` · **First target:** `IDEV` — see §15, which is deliberately all `UNKNOWN`
**Last updated:** 2026-08-05 *(supersedes the 2026-07-30 version, which quoted the retired 326-flow / 1,868-call figures)*

---

## How to read this document

| Reading for | Sections |
|---|---|
| **Approving it** — the recommendation, the evidence behind it, what is being asked for | §12 → §11 → §15 |
| **Doing it** — onboarding a project next week | §1 → §2 → §3 → §4, then `tools/onboarding/` |
| **Deciding the architecture** | §8 → §10 → §11 → §12 |
| **Avoiding what bit us** | §5 → §13 |
| **Checking a figure** | §17 |

Every number in this document is measured and cited. Where something is not established it says
`UNKNOWN` and names what would settle it — the standard set by
`docs/business-context/BUSINESS-CONTEXT-STANDARD.md`. An AI given a plausible-sounding invention will build on it
confidently, which is the specific failure this convention exists to prevent.

---

## 0. What actually transfers

The reusable asset is **not** the flow definitions or the endpoint lists — those are PAM-specific.
What transfers is the pattern, and now also the kit that carries it.

| Transfers as-is | Must be established per project |
|---|---|
| The generic executor — substitute → call → extract → assert → carry | The endpoint catalogue source |
| The declarative flow schema (`extract`, `find_extract`, `extract_any_id`, `verify_present`) | The payload source |
| The layered assertion model | How success and failure are signalled |
| Safety scaffolding — deny-by-default, blocklist, breaker, throttle, checkpoint/resume | The blocklist contents |
| Dated retained run folders, per-call redacted evidence | The auth mechanism and its lockout policy |
| The generator's *structure* — classify → pair → emit | The classification rules and the context prelude |
| **New:** the profile schema, the readiness gate, the onboarding skill | The profile itself |

**Rule of thumb:** anything naming a business noun (LOB, user group, service) is project-specific and
belongs in a profile. Anything naming only HTTP and JSON transfers.

**Measured size of what transfers:** the four core scripts are `chain_runner.py` (984 lines),
`generate_flows.py` (347), `generate_data_flows.py` (232) and `token_guard.py` (243) — **1,806 lines
of Python**, standard library only. `openpyxl` is required for the optional Excel workbook and
nothing else. There is no framework to install, no service to host, and no license to buy.

---

## 1. Prerequisites — the five inputs, and which of them are hard gates

Nothing starts until these exist. Run this against a new project on day one.

| # | Input | PAM's answer | If missing |
|---:|---|---|---|
| 1 | **Machine-readable endpoint catalogue** | `APIConfig.java` — 1,306 distinct `(controller, action)` pairs | ⛔ **Hard blocker.** Nothing to generate from. Fallback order: OpenAPI → Postman → recorded traffic → route dump → constants in an existing test project |
| 2 | **A working auth mechanism** | `POST /arcontoken`, bearer, 24 h | ⛔ **Hard blocker** |
| 3 | **A safe, disposable environment** | `QA_MsSQL` | ⛔ **Hard blocker.** Never production — this issues writes |
| 4 | **Request payload bodies** | 66 payload helpers, 1,289 literal-JSON methods | 🟡 Degrades to read-only. Creates cannot be generated |
| 5 | **A context prelude** — how the ids everything else needs are discovered | LOB → user group → server group | 🟡 Every payload becomes environment-bound and flows stop being portable |

**Input 5 is the one people miss.** In PAM nearly every write needs a LOB id and a group id. Ask it
in this form on day one: *to create the simplest thing in this product, which ids must I already
hold, and which call produces them?* The answer determines whether generated flows are portable or
brittle.

⚠️ **Input 1's quality matters more than its existence.** PAM has a catalogue and it is imperfect:
**348 endpoints (25.1% of those exercised) return 404**, and **2,104 authored test rows** target an
`/AdminAPI` surface that is not deployed. Assert an expected endpoint count so drift fails loudly —
a catalogue that silently yields less reads as a clean run with unexplained coverage.

---

## 2. Prerequisites — technical, operational and human

§1 is about the API. This is about everything else, and it is where onboarding actually stalls.

### 2.1 Technical

| Requirement | Detail | PAM |
|---|---|---|
| Python | 3.11+ (3.14.6 in use). Standard library only for the execution path | ✅ |
| `openpyxl` | Only for the optional `.xlsx` workbook | ✅ 3.1.5 |
| Network route | The runner host must reach the API host and port directly | ✅ |
| TLS posture | A self-signed QA certificate needs an explicit, *recorded* decision | 🟡 `verify_tls: false`, reason recorded |
| Disk | Per-call evidence, retained forever. PAM's last run wrote **5,424 files** | ✅ |
| Reference repo access | Read-only. Read as a *generation input*, never executed | ✅ |
| Optional: DB read access | Least-privilege, read-only, for the persistence layer | 🟡 Proven, gated on an account |
| ⬜ Not required | Java, Maven, TestNG, a CI server, a graph database, an AI API key | — |

### 2.2 Operational

| Requirement | Why it is a prerequisite, not a detail |
|---|---|
| **A named environment owner** | Someone must answer "may automation write here?" and "why is it down?" 26% of PAM's last run was spent waiting for the environment |
| **A credential issued to automation** | With its lockout policy stated. Not a developer's personal account |
| **An answer on harmful endpoints** | Even if the answer is "none known" — so the next person knows the question was asked |
| **Agreement that evidence is retained** | Retention is what makes run-over-run comparison possible at all |
| **A defect route** | Where a finding goes. This solution finds product defects, not just test failures — PAM's run produced two material ones |
| **A decision on teardown** | Whether the harness may delete what it created. Default: it may not |

### 2.3 Human

| Role | Time needed | What only they can answer |
|---|---|---|
| Product/dev contact | A few hours, front-loaded | Which endpoints are harmful, how deletion is expressed, whether a spec exists and is current |
| Environment owner | Ongoing, low | Access, stability, seed data |
| Identity owner | One conversation | Lockout policy, and whether the account is shared |
| Onboarding engineer | The bulk | Everything else |
| Reviewer | One pass per phase gate | Whether the flows test anything worth testing |

⛔ **The single most expensive missing prerequisite is a second identity.** Without two roles, every
authorization test is inert — it cannot fail. PAM had 1,153 such cases asserting `401` while sending
a *valid* token. Fixing that one input converted them into real tests and surfaced **57 endpoints
answering HTTP 200 to an invalid bearer token**; after classifying 34 health probes and 4
client-registration entry points as plausibly by design, **19 required security review — 6 of them
writes and 8 returning business data** (`LH-13`). Ask for the second identity on day one.

---

## 3. The onboarding workflow

Seven phases, each with an exit criterion. **The ordering is not stylistic** — it is what prevents
building assertions on guesses. The full procedure is
`tools/onboarding/skills/api-onboarding/SKILL.md` plus its six phase references; this is the map.

| # | Phase | Produces | Exit criterion | Typical effort |
|---:|---|---|---|---|
| 0 | **Discover** | Answers, or `UNKNOWN`s with owners | Every hard gate in §1 answered | 1 form + 1 conversation |
| 1 | **Profile** | `profiles/<key>.json` | `validate_profile.py` reports only *expected* blockers | Hours |
| 2 | **Probe** | The response-shape census | You can name every shape the API uses, and whether status is authoritative | Hours |
| 3 | **One chain by hand** | One flow, 3–5 hops | A real value passes forward and is verified downstream | Hours |
| 4 | **Generate** | Flow JSON + a manifest | Flows load and dry-run cleanly, zero HTTP calls | Days |
| 5 | **Execute** | A run folder | A full run completes, survives an outage, skips nothing silently | Hours per run |
| 6 | **Report** | Report + benchmark | A reviewer can verify any single claim | Hours |

### The two phases that get skipped, and what skipping them costs

⚠️ **Phase 2, the probe.** Documentation describes an intent; the API exhibits a behaviour. On PAM
they diverged sharply — documentation covers **6** response shapes and the API produces **31**, of
which **127 responses are not JSON objects at all**. An assertion designed from documentation is a
guess with good grammar. Write the profile's envelope section from the census, never from a document.

⚠️ **Phase 3, one chain by hand.** This is where the subtleties surface, and they generalise to every
generated flow afterwards. On PAM this phase is where it emerged that a create can return
`Success: true` with `Message: "Already Exists"` having inserted nothing — a rule that then governed
hundreds of generated flows. Discovering it after generating is a rework of everything.

### Phase gates are the mechanism, not the ceremony

Each gate is an **observed outcome**, never "the code for it is written". `validate_profile.py`
enforces Phase 1's gate mechanically; the others are enforced by a reviewer asking for the artifact.

---

## 4. Configuration — what must be set, and where it lives

One file per project: `data/profiles/<key>.json`, validated against
`profile.schema.json`. Ten sections, in the order they become answerable.

| Section | Decides | Hard-gated fields |
|---|---|---|
| `project` | Report headers, evidence paths, defect routing | owner must be named |
| `workspace` | Where the runner finds things — by marker search, not a fixed path | — |
| `environment` | The target, and the TLS posture | `name`, `api_base`, **`is_production` must be `false`** |
| `auth` | Credential mechanism, **lockout policy**, roles, the invalid-credential sample | `kind`, `lockout_risk`, `max_token_attempts_per_run` |
| `catalogue` | Adapter, source, expected count **and its basis**, allowed verbs | `adapter` |
| `payloads` | Body source, unique fields, enum-like fields to leave alone | — (degrades) |
| `envelope` | **How success and failure are signalled** | `status_is_authoritative`, `shapes_measured` |
| `identity_prelude` + `id_aliases` | How context ids are discovered and substituted | — (degrades) |
| `safety` | Blocklist, destructive names, throttle, breaker, downtime, redaction | `default_mode`, `blocklist`, `destructive_name_regex` |
| `validation` + `reporting` | Which layers apply; where evidence goes and for how long | `layers`, `retention` |

**Two rules make the profile safe to share:** it holds *key names*, never secret values — the
validator refuses a value that looks like a real token — and `UNKNOWN` is a legitimate entry, being
an unanswered question with an owner rather than a gap to paper over.

### The readiness gate

```powershell
python tools\onboarding\validate_profile.py profiles/pam.json     # exit 0 - ready
python tools\onboarding\validate_profile.py profiles/idev.json    # exit 1 - lists what is missing
python tools\onboarding\validate_profile.py --all
```

Structure comes from the schema; the operational checks are the ones a schema cannot express —
a production target, retry against a lockable account, a validation set that cannot detect failure,
an envelope section written without a probe, a health probe that is itself blocklisted.

**Measured, as built:** `profiles/pam.json` exits `0` with 0 blockers, 0 warnings and 5 declared open
unknowns. `profiles/_template.json` exits `1` with **13 blockers and 6 warnings**, each naming the
question and who settles it. That difference *is* the onboarding worklist — the gate turns "are we
ready?" from a judgement call into a command.

---

## 5. Project-specific considerations to evaluate before starting

Answer these before writing anything. Each was a surprise on PAM, and each has a cost.

| # | Area | The question | PAM's answer, and what it forced |
|---:|---|---|---|
| 1 | **Success signalling** | HTTP status, or an in-body envelope? | Envelope. **1,022 of 5,416 cases (18.9%) returned HTTP 200 while genuinely failing.** A status-only suite would call them all green |
| 2 | **No-op success** | Can "success" mean nothing was written? | Yes — `Success: true` + `"Already Exists"`. Create assertions must read message semantics |
| 3 | **Response shape stability** | One shape, or many? | **31 measured.** 288 responses carry no success field; 139 of 1,291 `Result` values are not arrays; 2 bodies are a naked boolean |
| 4 | **Field casing** | Is the parser's casing the API's casing? | PascalCase `Success` appears **1,580** times, camelCase `success` **0**. A case-sensitive lookup for the wrong one fails on *every* response the API can produce |
| 5 | **Auth lifetime and lockout** | Can repeated credential calls lock the account? Is it shared? | **They did**, and it was also the data-warehouse ETL account. One attempt per run, persistent latch on failure |
| 6 | **Destructive-call detection** | Is deletion a `DELETE`? | No — `POST /api/<C>/Delete<Thing>`. **Verb guards are useless; guard on names** |
| 7 | **Verb distribution** | Which verbs are real? | POST 992 · GET 325 · PUT 2 · DELETE 2 · PATCH 0 — GET+POST is **99.7%** |
| 8 | **Write latency** | Do writes cost more than reads? | 5–7 s. A read-tuned SLA fails every write |
| 9 | **Response size** | Is there an unfiltered bulk endpoint? | One returns 1.1 MB with no filter parameter. Cap bodies |
| 10 | **Environment stability** | How often does it drop? | 17 pauses, **85 of 329 minutes** waiting. Build wait-and-resume *before* scaling |
| 11 | **Idempotency** | What happens on a repeat create? | `"Already Exists"`. Randomise identity fields per run |
| 12 | **Harmful endpoints** | Can any call take the service down? | Three can. Three sequential calls took the whole API to `503` with no recovery — and that was not a load test |
| 13 | **Documentation trust** | Is the spec current, and how were payloads bound? | 70% of endpoints undocumented; 3 error codes documented; payloads bound **by page proximity**, so some bindings are wrong |
| 14 | **Spec vs reality** | Does the published spec describe *this* surface? | PAM's 37 Swagger specs (690 ops) describe a **different** surface — ~6% name overlap — and **0 of 690** declare any 4xx or 5xx |
| 15 | **Product source as contract** | Can the catalogue be derived from the product code? | No. Only **48 of 1,306** endpoints (3.7%) exist in the product snapshot; 58 of 70 controllers are absent |

---

## 6. What to skip, and what is non-negotiable

Honest guidance on where the PAM implementation is heavier than a new project needs.

| Component | Verdict |
|---|---|
| **Knowledge-graph layers** | 🟡 **Skip initially.** Useful for understanding a large unfamiliar codebase; contributed nothing to generation. The 1,680 graph-derived chain candidates were never consumed — structural create→read pairing proved more reliable |
| **A RAG documentation corpus** | 🟡 **Skip unless documentation is your only payload source.** It mattered for PAM only because 79 create endpoints have no body anywhere in code |
| **A requirement-intake framework** | 🟡 Optional. Its real value is a halt that forces requirements to be answered before code. Any equivalent discipline works |
| **Excel reporting** | 🟡 **Optional.** Markdown + JSON is more diffable; the workbook earns its place only when management consumes it directly |
| **Product-source analysis** | ⛔ **Skip.** Measured a dead end on PAM — 3.7% coverage |
| **Porting PAM's envelope handling** | ⛔ **Do not.** Measure the new API's own shapes; assume nothing |
| **The layered assertion model** | ✅ **Keep.** This is the core value. Drop L3/L4 *only* if a malformed request provably returns 4xx |
| **Deny-by-default safety** | ✅ **Keep.** Non-negotiable if the harness can write |
| **Checkpoint / resume / dated retention** | ✅ **Keep.** Cheap to build; saved a multi-hour PAM run repeatedly |
| **One-credential-per-run with a latch** | ✅ **Keep.** The cheapest control here, guarding the most expensive failure |

**Minimum viable version:** §1's five inputs, a generic executor, four layers (status, content-type,
envelope, extraction), deny-by-default, and dated run folders. Roughly 400 lines of Python — and the
1,806 lines already written are a superset, so this is a subtraction exercise, not a build.

---

## 7. Design decisions worth copying

### Flows are data; the executor is code

The executor knows nothing about the business domain. Adding coverage means emitting more JSON, not
writing more code — and hand-written and generated flows are the *same artifact*, so nothing built by
hand in Phase 3 is discarded when generation arrives.

### Resolve field names at run time, not generation time

A generator cannot know whether a create returns `UserId`, `ServiceId` or `MappingId`. Two mechanisms
solve this generically: `extract_any_id` takes the first field whose name ends in `id`, and
`verify_value_anywhere` searches the whole response for the value regardless of which field carries
it. Without them, every generated flow would need per-endpoint knowledge — which is the hand-written
approach with extra steps.

### Be liberal in matching, strict in asserting

Field lookups are case-insensitive and type-loose (PAM spells one field `LobId`, `LOBID` and `LOBid`;
an id is a string on create and an integer on read). The *assertions* stay strict. Loose matching
prevents false failures; strict assertion prevents false passes. They operate on different things, so
there is no tension.

### Select context records by name, never by position

`find_extract` picks the row *where* a field matches and takes ids from it. PAM's first list row is a
record with no child data, so `Result[0]` chaining fails — silently, as a join that finds nothing.

### Log every exclusion, with a reason and a count

If the harness withholds something — blocklisted, destructive, undeployed, unreachable — it is
**Blocked** with a per-item reason. Never *skipped*, never absent. PAM's last run withheld **2,610
cases** across six classes, each counted. Silent truncation reads as "covered everything".

### Report at the step level

One failing hop fails a whole chain, so flow-level rates punish long chains. The same PAM run reads
as **9.2%** at flow level and **64.2%** at case level. Both are true; only one is informative.

### Retain everything, so the baseline can be re-scored rather than caveated

When PAM's validator was corrected between runs, all **1,868** baseline hops were re-judged offline
from retained bodies with **zero HTTP calls**. Nothing changed — which removed any caveat from the
benchmark *and* proved the generators deterministic, 1,868 of 1,868 hops matching a week later.

---

## 8. Making it reusable — the coupling inventory

This is the answer to *"how do we stop it being PAM-specific?"* The couplings are few, named, and
local — which is why a profile boundary is credible rather than aspirational.

| Where | What is PAM-specific today | Profile field |
|---|---|---|
| `chain_runner.py:70-76` | `REPO`, `ENV_FILE`, `ENV_NAME` | `workspace.*`, `environment.*` |
| `chain_runner.py:77-82` | Latency SLA, timeout, throttle, call cap, breaker limit, body cap | `safety.*`, `validation.sla_ms` |
| `chain_runner.py:85-91` | `ENDPOINT_BLOCKLIST`, `DESTRUCTIVE` regex | `safety.blocklist`, `safety.destructive_name_regex` |
| `chain_runner.py:373` | Health probe `POST /api/ADbridging/GetLOBList` | `safety.health_probe` |
| `chain_runner.py:398` | `CREATED_MESSAGES` | `envelope.created_messages` |
| `chain_runner.py:458-480` | `Success` / `errorCode` field lookups | `envelope.success_fields`, `error_code_fields` |
| `generate_flows.py:37-40` | Action-name classification regexes | generator rules (per project) |
| `generate_flows.py:43-66` | `CONTEXT`, `IDENTITY`, `KEEP` field maps | `id_aliases`, `payloads.unique_fields` |
| `generate_flows.py:69-85` | The hardcoded LOB prelude | `identity_prelude` |
| `token_guard.py:170-175` | `pam_tokenAPIUrl`, `pam_APITokenUserName`, … | `auth.credential_keys` |
| `generate_data_flows.py` | Java data-provider parsing | `catalogue.adapter` = a different adapter |

**That is the whole surface.** Everything else in 1,806 lines is HTTP, JSON, assertion and safety
logic that transfers untouched.

### The three-layer separation

| Layer | Holds | Reused across projects? |
|---|---|---|
| **Machinery** — executor, layers, safety, reporting | HTTP and JSON only | ✅ Unchanged |
| **Adapters** — one per catalogue/payload source | Parsing one *format*, not one *project* | ✅ One per format, forever. An OpenAPI adapter written once serves every project that has a spec |
| **Profile** — one JSON file per project | Every project fact | ⬜ New per project, by design |

**Status, stated honestly:** the profile schema, the PAM profile, the template, the validator and the
skill exist and work (§4). The scripts do **not yet read** the profile — they still hold the constants
in the table above. The profile currently *documents* the couplings; wiring them is the next
increment, and it is deliberately not done in this objective because `chain_runner.py` and
`generate_flows.py` produced OBJ-010's 5,416-case run and changing them requires a parity re-run to
re-verify. **The kit is the design plus the gate; the refactor is a scoped follow-on.**

### The refactor, when it is approved

| Step | Change | Risk |
|---:|---|---|
| 1 | Add a profile loader; keep every current constant as its default | None — behaviour identical |
| 2 | Re-run PAM's chain dimension and diff against `results.json` | Parity is provable from retained evidence |
| 3 | Move the constants into `profiles/pam.json` and delete the literals | Caught immediately by the parity diff |
| 4 | Write the second adapter (`openapi`) against the second project | The adapter interface is proven by having two |

⚠️ **One adapter is not an abstraction.** The interface is only validated when a second project uses
it. Budget for the second onboarding to modify the machinery a little; budget for the third not to.

---

## 9. Reducing manual effort — where the time actually goes

Ranked by hours removed per project.

| # | Opportunity | Effort today | With the change | State |
|---:|---|---|---|---|
| 1 | **Payload data quality** — the largest single cost on PAM, and still open (13 of 217 creates work) | Days, per project | An OpenAPI/Postman source removes it almost entirely | ⬜ Depends on the project |
| 2 | **Discovery Q&A** — iterative chasing of facts | Days of round-trips | One form, answered once: `references/01-discovery.md` | ✅ Built |
| 3 | **"Did we forget anything?" reviews** | A review per phase | `validate_profile.py`, exit code 0/1 | ✅ Built |
| 4 | **Transcribing the probe into the profile** by hand | Hours, and error-prone | A `probe_to_profile.py` that emits the `envelope` section from a probe run | ⬜ **Highest-value remaining build.** Small |
| 5 | **Adapter per project** | A parser per project | An adapter per *format*, reused | 🟡 Designed; one exists |
| 6 | **Re-deriving procedure from documents** | Re-read, re-interpret | The skill loads the phase in use, on demand | ✅ Built |
| 7 | **Portable seed data** — named automation records per environment | Preludes break between environments | A naming convention, agreed once | 🟡 Convention exists on PAM |
| 8 | **Profile rot** | Discovered at the next run | Run the validator in CI; a profile cannot silently decay | ⬜ One CI step |

⛔ **Budget for payload data quality, not for tooling.** The tooling was the easy part on PAM: the
executor, generator and safety scaffolding are 1,806 lines and worked; **204 of 217 create endpoints
still cannot be driven** because nothing supplies a valid request body. This is the single most
reliable prediction in this document — and it is why §1's Input 1 is worth negotiating hard for.

---

## 10. Two architecture approaches

Both approaches make the same assets available. They differ in **what carries the procedure**, and
therefore in how it is triggered, maintained and enforced.

### Approach 1 — AI Skill-based

Package onboarding as an **AI Skill**: a folder with a `SKILL.md` whose frontmatter description makes
the agent load it when the work matches, plus reference files loaded on demand.

**Structure — as built, in `tools/onboarding/`:**

```
skills/api-onboarding/
  SKILL.md                        entry - Rule 0, the seven phases, exit gates            107 lines
  references/                     loaded on demand, one per phase                         566 total
    01-discovery.md               the questionnaire, each question -> a profile field       73
    02-profile-authoring.md       field by field, fill order, what each decides             93
    03-probe-protocol.md          probe protocol + the one-chain-by-hand gate               82
    04-generation.md              flow schema, classify->pair->emit, negative dimensions   120
    05-safety-and-operations.md   deny-by-default, credential latch, downtime, hygiene      91
    06-reporting-and-benchmark.md run folder, report rules, N-1 vs N                       107
profile.schema.json               the data contract                                       285
profiles/pam.json                 the worked example                                      182
profiles/_template.json           what a new project copies                               140
validate_profile.py               the enforcement gate                                    315
```

**Inputs it requires:** a project key; the profile (which it also helps author); read access to the
catalogue source and the reference repo; the environment's config file for *key names* only; and the
answers to Phase 0 that only a human can give. Nothing else — and notably no product facts, which is
what makes it portable.

**How reuse works across `IDEV`, PAM and future projects:** the skill is invoked with a project key
and reads that project's profile. Reusability is *checkable*: grep the skill for a product name and
there should be none outside a labelled "reference project" citation.

| ✅ Advantages | ⛔ Disadvantages |
|---|---|
| **Triggers itself.** Description-matched, so nobody has to remember which document to read | **A skill instructs; it does not enforce.** Nothing stops an operator ignoring it. Enforcement needs the validator, deny-by-default code and hooks |
| **Progressive disclosure.** **107 lines** load; the **566 lines** of references load only when their phase is active | **Triggering is probabilistic.** An unusual phrasing may not load it. `/api-onboarding` explicitly is reliable; implicit matching is not |
| **Encodes ordering**, which is the thing that actually goes wrong — phases with exit gates, not a list of topics | **Drift is silent and confident.** If the skill and the scripts disagree, the skill is authoritatively wrong. Needs an owner and a review trigger |
| **Composable** with the four skills already installed here, and distributable as a plugin or repo | **Distribution and versioning are manual** — global vs project vs plugin, with no dependency pinning |
| **Reusable by construction** if it holds no project facts, and that property is greppable | **Assumes an AI agent in the loop.** A human without the tooling gets instructions for a tool they do not have |
| Precedent exists in this environment: `graphify` is 578 lines + 8 references and is used routinely | **Holds no state.** Each invocation re-derives context; the profile is what carries continuity |
| Plain markdown — a human can read it directly | Six files to keep consistent rather than one |

### Approach 2 — Template / instruction-based

Make a standardised instruction document the source of truth — **this file** — and have the AI consume
it to produce a new project's artifacts, prerequisites, configuration and recommendations.

**How the AI consumes it:** the document is referenced or pasted into the session; the AI reads §1–§5
to determine prerequisites, §4 to produce the profile, §3 to sequence the work, §5 and §14 to
anticipate project-specific traps, and emits the artifacts. Effectively: prompt-with-a-long-document.

| ✅ Advantages | ⛔ Disadvantages |
|---|---|
| **Zero infrastructure.** Any agent, any tool, any human. Sendable by email | **Nothing triggers it.** It must be remembered, found and deliberately read, every time |
| **One artifact to review and approve.** Auditable, and management can read it | **Context cost is all-or-nothing** — and a long file read partially looks exactly like a complete read. This workspace already documents that trap for files over ~1,500 lines |
| **Natural home for the *why*** — evidence, provenance, measured figures | **Prose invites interpretation.** Two engineers reading it produce two different onboardings, both defensible |
| **Everyone can already edit it.** No new format, no adoption cost | **No gate.** Nothing stops progressing with unanswered questions — the exact failure mode §4's validator exists to catch |
| **Correcting a fact is one edit** in one place | **Drifts back to project-specific.** As it accumulates worked examples it re-acquires PAM flavour; the previous version of this file was 132 lines and had already gone stale by a whole objective |
| Survives tooling changes — it depends on nothing | **Cannot be executed.** It produces recommendations, not artifacts. A document cannot refuse a production target |
| Best possible *first* deliverable: cheap, and it forces the thinking | Maintenance grows with every project onboarded, in one file, with no per-project isolation |

---

## 11. Comparison

| Axis | Approach 1 — AI Skill | Approach 2 — Template | Verdict |
|---|---|---|---|
| **Scalability** — 1 project → 10 | ✅ **Strong.** Machinery + adapters + one profile per project. Marginal cost per project is a profile, and the skill never changes | 🟡 **Weak.** One document accumulates every project's specifics, or forks per project and diverges | **1** |
| **Maintainability** | 🟡 **Mixed.** Six files plus a schema, and drift against the scripts is silent — but each file has one job, and the validator catches profile drift mechanically | 🟡 **Mixed.** One file, trivially editable — but no mechanism detects that it has gone stale. The previous version was stale by a full objective and nothing said so | **1**, narrowly — the validator is the difference |
| **Ease of adoption** | 🟡 Needs an agent that supports skills, and a one-time placement decision (global / project / plugin) | ✅ **Strongest.** Send a link. No adoption step at all | **2** |
| **Long-term support** | ✅ **Strong.** Procedure, data and enforcement are separable, so each can be owned and versioned independently. Adapters accumulate as assets | 🟡 **Fragile.** Support means re-reading a growing document and hoping it is current. Nothing is executable, so nothing can be tested | **1** |
| **Determinism** | ✅ Phase gates, exit criteria, and an exit-code gate | ⛔ Interpretation-dependent by construction | **1** |
| **Enforcement** | 🟡 Only via the validator and the deny-by-default machinery — the skill itself cannot enforce | ⛔ None | **1**, and both need the validator |
| **Management legibility** | 🟡 A skill is not a document to present | ✅ **Strongest.** This is what a manager can read and approve | **2** |
| **Time to first onboarded project** | 🟡 Kit already built, so: days | ✅ Hours — but the *outcome* takes just as long, and is less repeatable | **2** on speed, **1** on outcome |
| **Cost to onboard project #5** | ✅ A profile plus an adapter if the format is new | 🟡 A full re-read and re-interpretation, every time | **1** |

**Where they are equal, and it matters:** neither can enforce anything by itself. Enforcement comes
from `validate_profile.py` and deny-by-default machinery, and both approaches need it. **The gate is
the load-bearing component, not the prose.**

---

## 12. Recommendation

**Adopt Approach 1 — the AI Skill — as the delivery vehicle, with this document retained as its
human-facing specification and one of its inputs, not as the mechanism.**

That is one recommendation, not a hedge, and the division of labour is exact:

| Asset | Role | Owner reads it |
|---|---|---|
| **The skill** (`skills/api-onboarding/`) | *How* onboarding is executed. Procedure, ordering, gates | The AI, per phase |
| **The profile** (`profiles/<key>.json`) | *What* is true about one project | The AI and the reviewer |
| **The validator** (`validate_profile.py`) | *Whether* it is safe to proceed. Exit code 0/1 | CI and the reviewer |
| **This document** | *Why* — evidence, options, cost, the management case | People |

### Why this way round

1. **The recurring cost is procedure, and procedure is what a skill carries.** Onboarding project #5
   should cost a profile, not a re-interpretation of a growing document.
2. **The failure mode is ordering, not ignorance.** Every expensive PAM mistake was a step done
   before the step that would have informed it — assertions before the probe, generation before one
   hand-written chain, a credential retry before the lockout policy was known. Phase gates address
   that directly; prose cannot.
3. **Separating procedure from data is what makes reuse checkable** rather than aspirational. Grep the
   skill for a product name: if there is one, reuse has already broken.
4. **The document remains genuinely necessary** — for approval, for the evidence, and for anyone
   without the tooling. Approach 2 is not discarded; it is demoted from mechanism to specification,
   which is the role it is actually good at.
5. **Neither works without the gate.** `validate_profile.py` is what converts good intentions into a
   refusal, and it is already built and demonstrated (§4).

### What to say to management

> We built dynamic API test generation for PAM. It produced **5,590 test cases across 1,388
> endpoints with no hand-written tests**, and it found two things a conventional suite could not:
> **1,022 cases that returned HTTP 200 while actually failing**, and **19 endpoints that accept an
> invalid authentication token** — **6 of them writes, 8 returning real business data**.
>
> The machinery is 1,806 lines of dependency-free Python, and it is generic. Only a short, named list
> of facts is PAM-specific, and those now live in a single JSON profile with an automated readiness
> gate. Onboarding a project such as IDEV means answering a one-page questionnaire, filling that
> profile, and running the gate. **It is materially less work than PAM required**, because the
> executor, the safety controls, the reporting and now the onboarding kit are already built and
> transfer unchanged — and the remaining effort is concentrated in **one risk rather than many**:
> whether IDEV can supply valid request bodies. If IDEV publishes an OpenAPI specification, that risk
> largely disappears.
>
> ⚠️ We are not quoting a date yet. Ten facts about IDEV are still unknown, and the first phase exists
> to establish them — it produces a costed go/no-go, not a guess.
>
> What we need: a QA environment we may write to, two automation credentials with different
> privilege levels, a named product contact for a few hours, and an answer on whether an API
> specification exists.

### Sequenced ask

| Step | Ask | Cost |
|---:|---|---|
| 1 | Approve the four prerequisites above for `IDEV` | Access and a few hours of a product contact |
| 2 | Run Phase 0–1 on `IDEV` — questionnaire, profile, gate | Days. Produces a go/no-go with a costed worklist |
| 3 | On green: probe, one chain, generate, first run | Weeks — **sized by step 2's outcome, not estimated ahead of it** |
| 4 | Approve the profile-driven refactor (§8) with a PAM parity re-run | Small, and it is what makes project #3 cheap |

---

## 13. Pitfalls we hit, so the next project need not

| # | Pitfall | Cost | Avoidance |
|---:|---|---|---|
| 1 | Assumed a single response envelope | Rework mid-project | Probe first. Record every shape before designing assertions |
| 2 | Trusted the product source as the API contract | Wasted analysis — 3.7% coverage | Verify the source *serves* the API before mining it |
| 3 | Repeated credential calls | **Locked a shared service account** | Cache; one attempt per run; **persistent** latch on failure |
| 4 | Blind first-row chaining (`Result[0]`) | Silent join failures | Select context records by name and discover the id |
| 5 | Auto-deleting prior report output | Lost comparability | Dated folders, retain everything, from day one |
| 6 | Latency SLA tuned on reads | False failures on every write | Per-hop budgets, split read vs write |
| 7 | Quoting flow-level pass rates | Misleading — one bad hop fails a ten-hop flow | Report at the **step** level |
| 8 | Negative cases that could not fail | 1,153 inert assertions; a real security finding sat undetected | A negative case must send something genuinely invalid |
| 9 | Hardcoded allowlist of known error codes | A correct product response scored as a broken test | Match on prefix; record an unknown code as an observation |
| 10 | Case-sensitive envelope field lookup | The check failed on **every** response the API can produce | Match field names case-insensitively |
| 11 | Splitting a path before stripping its query | Garbage action name feeding the **safety guards**, and a crash 3 h 54 m into a run | Strip the query first. Sanitise anything that becomes a filename |
| 12 | Checkpoint treating "gave up" as "done" | Would have silently dropped coverage on resume | Distinguish aborted from complete; add a gate so it cannot recur |
| 13 | Trusting a resumed run's own metadata | 94.9 minutes reported against 329.1 actual | Reconstruct totals across segments |
| 14 | Substring matching on config keys | 376 providers read the wrong workbook; ~2,450 rows written off | Longest-key-wins, and assert the total |
| 15 | Rewriting UTF-8 text files through PowerShell | Corrupted two files | Use a proper editor or file API, not shell redirection |

---

## 14. Effort reference

Relative effort actually spent on PAM, as a planning baseline.

| Phase | Effort | Note |
|---|---|---|
| Probing shapes and auth | Small | |
| First hand-written chain | Small | Highest value per hour of anything here |
| Generator | Medium | Would be **Small** with an OpenAPI source |
| Executor + assertion layers | Medium | Now reusable — **near zero** on project #2 |
| Safety, checkpoint, resume, retention | Medium | Now reusable — **near zero** on project #2 |
| **Payload data quality** | **Largest single cost, still unresolved** | 13 of 217 creates work |
| Reporting | Small | Now reusable |
| **Onboarding kit** (this objective) | Medium, one-off | Amortised across every future project |

**Execution cost, measured:** PAM's full run was **329.1 minutes** for 5,416 cases — of which **85
minutes were spent waiting for the environment**, not testing. Environment stability, not test
volume, is the dominant runtime cost.

**Estimated reduction for a project with a real OpenAPI spec:** the generator shrinks substantially —
no in-code catalogue parsing, no payload-helper mining, no documentation mining. The executor, safety
scaffolding, reporting and now the onboarding kit all port unchanged. Expect roughly **60–70% less
work than PAM required**, with the residual concentrated in §9's item 1.

---

## 15. `IDEV` readiness — every entry is currently `UNKNOWN`

⚠️ **The workspace holds no information about `IDEV`.** Nothing here is an assessment; it is the
worklist for Phase 0. Filling this table *is* the go/no-go decision, and no figure in it may be
guessed.

| # | Input | Gate | `IDEV` status | What settles it |
|---:|---|---|---|---|
| 1 | Endpoint catalogue | ⛔ Hard | `UNKNOWN` | An OpenAPI/Swagger URL, a Postman export, or a route dump |
| 2 | Auth mechanism | ⛔ Hard | `UNKNOWN` | One successful authenticated call |
| 3 | Safe environment | ⛔ Hard | `UNKNOWN` | An owner's decision plus a URL, confirmed non-production |
| 4 | Payload bodies | 🟡 Degrades | `UNKNOWN` | Spec schemas, a Postman collection, or recorded traffic |
| 5 | Context prelude | 🟡 Degrades | `UNKNOWN` | One walkthrough of creating the simplest record |
| 6 | Lockout policy | ⛔ Hard | `UNKNOWN` | The identity owner. **Assume high risk until answered** |
| 7 | Harmful endpoints | ⛔ Hard | `UNKNOWN` | The development team. "None known" is a valid answer; silence is not |
| 8 | Status authoritative? | ⛔ Hard | `UNKNOWN` | One deliberately malformed request |
| 9 | Second identity for authorization tests | 🟡 Degrades | `UNKNOWN` | Provisioning, or a statement that only one exists |
| 10 | Environment stability | 🟡 Informational | `UNKNOWN` | Observation during the probe |

**Start here:**

```powershell
Copy-Item data\profiles\_template.json data\profiles\idev.json
python tools\onboarding\validate_profile.py profiles/idev.json
```

The gate will list 13 blockers. Each one is a question in `references/01-discovery.md` with an owner.
When it exits `0`, `IDEV` is ready to probe.

⛔ **Do not assume `IDEV` resembles PAM.** The two most consequential PAM facts — an in-body error
envelope and deletion expressed as `POST` — are product-specific accidents, not industry norms. Both
are measured in Phase 2, never inherited.

---

## 16. Assumptions

Stated so they can be challenged. Each is an assumption, not a finding.

| # | Assumption | If wrong |
|---:|---|---|
| 1 | `IDEV` exposes an HTTP/JSON API | The catalogue, envelope and flow model need rethinking; the safety and reporting layers still transfer |
| 2 | A non-production `IDEV` environment exists that automation may write to | Onboarding stops at §1's gate 3. There is no read-only variant that still proves persistence |
| 3 | Python 3.11+ is permitted on whatever host runs it | The 1,806 lines would need porting; the design would not |
| 4 | Onboarding is done by someone with an AI agent that supports Skills | Approach 2 becomes the fallback, with the costs in §10 |
| 5 | Evidence may be retained indefinitely | Benchmarking degrades to same-run reporting only |
| 6 | The reference repo may be read as a generation input | Generation falls back to spec-only, which is usually *better* |
| 7 | PAM's measured figures are representative of *risk classes*, not of magnitudes | The classes are what transfer (200-shaped failures, no-op successes, name-based deletion); every number must be re-measured per project |

---

## 17. Provenance

| Claim class | Source |
|---|---|
| Run figures — 747 flows, 5,590 cases, 5,416 executed, 3,459 passed, 1,388 endpoints, 122 modules, 329.1 min, 85 min downtime, 17 pauses | `docs/management/summary/OBJ-010-Execution-Benchmark.md` §2, §8, §10 · `artifacts/runs/2026-08-05_114315/` |
| 1,022 cases HTTP 200 while failing (18.9%) | same, §4 |
| 57 endpoints accepting an invalid token → 19 requiring review, 6 writes, 8 returning business data | `docs/briefs/developer-loopholes.md` §13 (source of truth) · `artifacts/loopholes/LH-13-endpoints-accept-invalid-auth-token/` · `docs/management/summary/OBJ-010-Execution-Benchmark.md` §5. ⚠️ That summary's §1 and §5 *heading* say "23" while its own table sums 34 + 4 + 19 = 57 — quote **57 → 19**, per `LH-13` |
| Exclusions — 2,610 cases in six classes | same, §7 |
| Offline re-score — 1,868 hops, 0 changes | same, §6 · `artifacts/runs/2026-07-29_181439/rescore.json` |
| N-1 baseline — 326 flows, 1,868 calls, 870 endpoints, 64.2%, 191.7 min | `artifacts/runs/2026-07-29_181439/` · `docs/management/summary/Full-Generated-Run-2026-07-29.md` |
| Catalogue — 1,306 endpoints, verb distribution, 99.7% | `.claude/rules/api-surface.md` · `APIConfig.java` |
| 31 response shapes and the shape breakdown | root `CLAUDE.md` §Response shapes · `artifacts/analysis-data/envelope-shapes.json` |
| `Success` casing — 1,580 PascalCase vs 0 camelCase | root `CLAUDE.md` §The response envelope |
| Creates — 13 of 217 working, 79 with no body | `docs/gaps/01-Data-Gap-Analysis.md` · `docs/briefs/overview.md` §12 |
| Documentation limits — 70% undocumented, 3 error codes, page-proximity binding | `docs/analysis/A7-documentation-gap-analysis.md` |
| Swagger — 37 specs, 690 ops, ~6% overlap, 0 declaring 4xx/5xx | `.claude/rules/api-surface.md` |
| Product source — 48 of 1,306, 58 of 70 controllers | `.claude/rules/api-surface.md` · `docs/analysis/A6-developer-repo-analysis.md` §6 |
| Token lockout history | `docs/findings/issues/ISSUE-009` · root `CLAUDE.md` |
| App-pool blocklist — 3 endpoints, 503 with no recovery | `docs/findings/issues/ISSUE-010` · `artifacts/loopholes/LH-08` |
| Coupling line references (§8) | `chain_runner.py`, `generate_flows.py`, `token_guard.py` — ⚠️ line numbers move when those files are edited; re-grep rather than trusting them |
| Script sizes — 984 / 347 / 232 / 243 lines, stdlib only | measured directly from the files |
| Kit behaviour — pam.json exits 0; _template.json exits 1 with 13 blockers, 6 warnings | `validate_profile.py`, run against both |

**Related, and deliberately not duplicated here:**

| Need | Read |
|---|---|
| The kit itself | `tools/onboarding/README.md` |
| PAM's measured run and its findings | `docs/management/summary/OBJ-010-Execution-Benchmark.md` |
| How the PAM pipeline works, for a demo | `docs/briefs/overview.md` |
| Briefing an AI on one *feature*'s business context — a different problem | `docs/business-context/BUSINESS-CONTEXT-STANDARD.md` §0 |
| PAM's Java/TestNG target architecture — **not** this framework | `docs/specs/*.SKILL.md` |
