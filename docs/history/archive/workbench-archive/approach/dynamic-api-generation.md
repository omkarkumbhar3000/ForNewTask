# Dynamic API Validation — Build-Stability Harness

**Objective:** one script that validates the PAM API and returns results automatically on execution, with
**no manual coding per endpoint**. Build-stability signal, not authored test cases.
**Editable scope:** `Automation gitlab repo/pam_automation_bootstrap/` only, on branch `AI`. `pam/` is
reference-only (`instruction.md` item 8).
**Evidence layer:** [`rag/findings.md`](../../rag/findings.md) — product-documentation facts, page-cited. This
document cites it rather than restating it.
**Related:** `../skills/api-test-suite-generator.SKILL.md` (spec → suite generation, relevant to §9) ·
`plan.md` Phase 5 (content assertion — boundary in §1.3).
**Status:** ⬜ Design. Recommendation revised after the measurement in §2.

---

## 1. Verdict

### 1.1 Feasible — and cheaper than first scoped

| Capability | Feasible | How |
|---|---|---|
| Discover the API surface with no hand-authoring | ✅ | Already declared in `APIConfig.java` — 1,336 constants (§2) |
| Derive a request body per endpoint automatically | ✅ | Already written in the 66 `*PayLoadHelper` classes (§2) |
| Execute everything and return results on one command | ✅ | Reuses `ApiHelper` + Playwright `APIRequestContext` |
| Report to Excel automatically | ✅ | Reuses `APIExcelReportUtil` |
| Detect that a build broke an endpoint | ✅ | Differential model (§5) |
| Zero new code per endpoint, forever | ✅ | Reflection, not code generation (§3) |
| Cover endpoints nobody has catalogued yet | 🟡 | Needs source-side discovery — §9, optional, later |
| Assert business correctness | ⛔ | Out of scope by design — §1.3 |

### 1.2 ⚠️ The one reframing that makes this work

> **Do not build a correctness harness. Build a differential one.**
> Nothing can infer that `AddUser` *should* create a home directory at `/home/x` — that is business
> knowledge, and it lives in the authored test cases you explicitly do not want. But build stability does
> not need it. The question is not *"is this response right?"* but *"is this response different from the
> last known-good build?"* Difference is computable. Correctness is not.

### 1.3 Boundaries

**Against `plan.md` Phase 5** — Phase 5 asserts *content* for hand-written Excel-driven tests using
human-supplied expectations. This asserts *difference* against a recorded baseline. No overlap in method;
they meet only at the Excel output.

**Against `plan.md` Phase 7** — Phase 7 gates the *automation code* for conformance. This gates the
*product build* for stability.

**Against authored testing generally** — this harness will never tell you a feature is wrong. It tells you
something changed. That is the correct and sufficient scope for a build gate.

---

## 2. 🔑 The measurement that changes the approach

The original plan was to parse the .NET source with Roslyn and generate an OpenAPI spec. Measuring the
existing framework first shows most of that work is unnecessary — **the API surface is already declared in
machine-readable form inside the automation repo.**

Measured across `autoconfigs/APIConfig.java` and `utils/apiPayload/`:

| Measurement | Result |
|---|---:|
| Endpoint constants declared | **1,336** |
| Distinct module blocks | 69 |
| Constants carrying an inline verb comment (`// get`, `// post`) | **1,321 — 98%** |
| Verb distribution | `post` 992 · `get` 325 · `put` 2 · `delete` 2 |
| Module blocks with a matching `<Module>PayLoadHelper` class | **65 / 68** |
| No-arg payload methods available | 1,291 |
| Non-`GET` constants | 996 |
| …with a **same-named** no-arg payload method | **836 — 83%** |

The three artefacts join on **exact name identity**, with no mapping table required:

```
APIConfig.insertFileWatcherLogs          = "/api/ActivityLogs/InsertFileWatcherLogs";  // post
         └── field name ──┐                                                             └─ verb
                          │
ActivityLogsPayLoadHelper.insertFileWatcherLogs()   → the JSON body
         └── module ──┘   └── same name ──┘
```

**Therefore, executable today with no new per-endpoint code:**

| Class | Count |
|---|---:|
| `GET` — no payload required | 325 |
| Non-`GET` — payload method present | 836 |
| **Immediately executable** | **1,161 of 1,336 — 87%** |
| Non-`GET`, no payload method | 160 |
| No verb hint | 15 |

The remaining 175 are reported as `EXCLUDED` with a machine-readable reason, not silently skipped — and
that count is a metric to drive down, not a defect.

**Re-measured 2026-07-28** — figures reproduced independently, with two refinements:

| Measurement | Result |
|---|---:|
| Path-like constants in `APIConfig` (excluding headers, verbs, content types) | **1,322** |
| Verb distribution | `post` 991 · `get` 325 · `put` 2 · `delete` 2 · none 2 |
| Payload helper classes · distinct no-arg methods | **66** · **1,099** |
| Payload methods **requiring arguments** | **0** — every helper is callable with no seed data |
| GET (no body needed) | 325 |
| Non-GET with a same-named no-arg payload method | 835 |
| **Immediately executable, zero new per-endpoint code** | **1,160 / 1,322 — 87.7 %** |
| Non-GET with no payload method at all | 160 |

That every payload method is no-arg matters more than the headline percentage: it means body derivation
needs **no seed fixture at all** to reach 87.7 % execution. Y5 gates *meaningful* responses, not execution.

⚠️ **Data-quality defect found while measuring:** `APIConfig` declares a controller `Se0rviceDetailsV3` —
a typo for `ServiceDetailsV3`. Any endpoint under it is unreachable. Grep for it before baselining.

### 2.1 The negative-case taxonomy already exists

Not previously recorded here, and it changes what §1.3's boundary means in practice:

| Asset | Size |
|---|---:|
| `API_Suites/Negative/` suites — `InvalidDataType`, `InvalidValue`, `MethodNotAllowed`, `MissingParameter`, `UnauthorizedAccess` | 5 |
| Test classes under `tests/API/Negative_API/` | **386** |
| `Negative_API_DataProviderUtils.java` `@DataProvider` methods | **376** (158 KB) |
| `API_DataProviderUtils.java` `@DataProvider` methods | 146 (49 KB) |
| `testdata/Negative_API_Automation_Test_Input_Data.xls` | 928 KB |

The five categories are exactly the negative taxonomy a generator would want to produce. They already
exist as **hand-curated Excel expectations** — which is direct evidence that the expected `errorCode` per
negative case is *human-supplied knowledge*, not something derivable from source. A generator can
manufacture the *stimulus* mechanically; it cannot manufacture the *expectation*.

> **Consequence:** the deliverable is **one runner class**, not a code generator. Nothing is emitted to
> disk, so nothing can go stale, and adding an endpoint to `APIConfig` automatically puts it under test.

---

## 3. Recommended design — one runner, zero per-endpoint code

A single TestNG class plus a listener, both inside the existing framework.

```
BuildStabilityRunner  (one @Test, one DataProvider)
  1. reflect over APIConfig            → 1,336 (field, path, verb) triples
  2. resolve <Module>PayLoadHelper     → invoke same-named no-arg method for the body
  3. apply allowlist / blocklist       → drop destructive ops (§7)
  4. bind credential by module         → Access Type scope, per rag/findings.md §2
  5. ApiHelper.getResponse(...)        → existing client, existing token handling
  6. compare to baseline               → verdict (§5)
  7. BuildStabilityListener.onFinish() → write the workbook (§6)
```

**Everything in steps 5–7 already exists.** Steps 1–4 and the comparison are the build — one class of
perhaps 300–400 lines, plus a listener.

### Why reflection beats code generation here

| | Reflection runner | Code generator |
|---|---|---|
| New code per endpoint | none, ever | a class + payload + Excel row each |
| Goes stale | cannot — reads the live source of truth | yes, needs regeneration discipline |
| Files added to the repo | 2 | thousands |
| Works today | ✅ | needs the missing API source (§9) |
| Finds *uncatalogued* endpoints | ⛔ no | ✅ yes |

The generator's one genuine advantage — discovering endpoints nobody has catalogued — is real but
secondary, and currently blocked (§9). Take it as a later layer.

### Invocation

```powershell
mvn clean test -Denv=<env> -DsuiteFile=CICD_Suites/BuildStability.xml -DbuildId=<id>
```

One command, no arguments beyond the environment and a build label. That is the whole user-facing surface.

---

## 4. What is required, and from whom

### 4.1 Required from the developer — **nothing**

This is the point of the design. The runner reads assets that already exist inside the QA repo and calls the
API over HTTP exactly as any client would. **No developer change is needed to start.**

The only genuine dependency is one that is not code:

| # | Need | Nature |
|---|---|---|
| D1 | A build deployed to a testable environment | Already happens |

### 4.2 Optional on the developer side — each one makes this better

None of these block delivery. Roughly in value order:

| # | Ask | What it buys |
|---|---|---|
| O1 | **A `/version` or `/health` endpoint** returning build number + commit SHA | Results become attributable to a build automatically. Without it, the build ID is passed in by hand and can be wrong. **Highest value per unit of effort in this table.** |
| O2 | **Notify QA of intentional contract changes** — a line in the release note is enough | Turns a `CHANGED` verdict from an investigation into an acknowledgement. Pure process, zero code |
| O3 | Add **Swashbuckle/NSwag** to the API projects so each build publishes `swagger.json` | Removes §9 entirely — coverage becomes automatic and complete, including endpoints QA has never catalogued |
| O4 | Access to the **ARCON PAM API source repository** | Enables §9 without O3. See §9 for why this matters |
| O5 | Keep returning the `errorCode` envelope **consistently** | The envelope is the primary signal (§5.1); inconsistency weakens every verdict |
| O6 | A **seed/reset script** for the test environment | Makes runs idempotent and lets write-endpoints be tested safely |
| O7 | Stable operation names — avoid silent renames | A rename is indistinguishable from a deletion plus an addition |

> **If only one is granted, ask for O1.** If two, add O2. Both are trivial for the developer and remove the
> two biggest sources of manual effort on the QA side.

### 4.3 Required from your side

These are the real prerequisites, and most are one-time. Sources for the first three are in
[`rag/findings.md`](../../rag/findings.md).

| # | Action | Why | When |
|---|---|---|---|
| Y1 | Nominate a **disposable, non-production environment** | §7 — the surface includes unauthenticated SQL execution. This is non-negotiable | Before any execution |
| Y2 | Provision an **API User covering all three Access Types** (or three users) | One credential cannot reach the whole surface — `rag/findings.md` §2 | One-time per environment |
| Y3 | **Register the CI agent's IP + MAC** under Settings → API → Registered Machines | Password endpoints refuse unregistered hosts — `rag/findings.md` §3 | One-time; repeat if the agent is recycled |
| Y4 | Confirm **transport consistency** and the **Application List URL** | Both-HTTPS or both-HTTP; URL must match `pam_BaseAPIURL` — `rag/findings.md` §4 | One-time |
| Y5 | Harvest a **seed fixture** — one Access Logs row yields most of it | Endpoints need real IDs; without them they are excluded, not guessed | One-time per environment |
| Y6 | **Declare one build green** to baseline against | Defines "known good"; everything is measured from it | Once, then on approved change |
| Y7 | **Approve the write-endpoint allowlist** | Default-deny on mutating verbs; each exception needs a named approver | Once, then as needed |
| Y8 | **Own triage of `CHANGED` and `NEW`** verdicts | Mechanical verdicts need nobody; these two need a human | Ongoing, low volume |

Y1–Y5 are a single afternoon's environment setup. After that the harness is unattended.

### 4.4 Enhancements — better experience, easier objective

Ranked by benefit relative to cost.

| # | Enhancement | Benefit |
|---|---|---|
| E1 | **One-page HTML summary** beside the workbook — build ID, pass rate, regression list, red or green at a glance | Excel is the record; nobody wants to open it to learn "did the build pass?" |
| E2 | **Verdict line in the Jenkins email subject** — `PAM build 1234: 3 REGRESSED, 12 CHANGED` | Most consumers never open the artefact |
| E3 | **Trend sheet** — pass rate and latency per build over the last N runs | Turns point-in-time results into a stability signal; catches slow degradation |
| E4 | **Guided baseline promotion** — a `-DpromoteBaseline` run that produces a reviewable diff | Makes Y6 repeatable and safe rather than a manual file edit |
| E5 | **Coverage sheet driving the exclusion count down** — list the 175 not-yet-executable endpoints with reasons | Converts an unknown into a visible, shrinking backlog |
| E6 | **Module priority tags** so failures sort by business criticality — `rag/findings.md` §9 | Three regressions in Password Vault ≠ three in a reporting endpoint |
| E7 | **Teams/Slack webhook** on `REGRESSED` | Shortens time-to-notice from hours to seconds |
| E8 | **`--dry-run` mode** printing the plan without calling anything | Makes the allowlist and exclusions auditable before a real run |
| E9 | **Per-module suite XMLs** generated from the module list | Lets a developer re-run just their module after a fix |

E1 and E2 are small and disproportionately improve how this is perceived. E3 is what turns it from a test
into a stability instrument.

---

## 5. The differential model

### 5.1 Baseline record, per endpoint

| Field | Why |
|---|---|
| `httpStatus` | the obvious signal |
| `errorCode` | ⚠️ the **real** signal — see below |
| `success` | envelope flag |
| `shapeHash` | structural fingerprint of the response |
| `latencyMedian`, `latencyP95` | rolling over the last *N* green builds |
| `contentType` | catches HTML error pages served as 200 |

> ⚠️ **Most PAM endpoints answer HTTP 200 with an application-level `errorCode`.** A rejected request is
> usually a 200, not a 4xx. A harness asserting `status == 200` would report a fully green build while every
> endpoint rejects every request. `ApiHelper.validateResponseErrorCode(...)` already handles this; the
> baseline records `errorCode` as a first-class field, never the status alone.

**Shape hash:** normalise the response to a sorted list of `path:type` leaf descriptors, discard values,
SHA-256. Stable across data changes, sensitive to contract changes. `DataTable`/`DataSet` responses are
exempt — their structure is data-dependent and would produce permanent false regressions.

### 5.2 Verdicts

| Verdict | Condition | Build impact |
|---|---|---|
| ✅ `STABLE` | status, `errorCode`, shape all match; latency in band | pass |
| 🆕 `NEW` | present now, absent from baseline | pass — prompts baseline update |
| ⛔ `REGRESSED` | 5xx where baseline was not; `success` true→false; required field vanished | **fail** |
| ⛔ `GONE` | in baseline, absent now | **fail** — a removed endpoint breaks live clients |
| ⚠️ `CHANGED` | shape differs, not obviously worse | warn, triage |
| 🟡 `SLOW` | latency > baseline p95 × 2 | warn |
| ⬜ `EXCLUDED` | blocklisted, or no payload/seed available | reported, not counted as pass |

---

## 6. Output

One workbook, `Execution_Reports/Excel_Report/Build_Stability_<buildId>.xlsx`, written by
`BuildStabilityListener.onFinish()` using the existing POI plumbing.

| Sheet | Contents |
|---|---|
| **Summary** | Build ID · environment · totals · pass rate · verdict distribution · duration |
| **Results** | One row per endpoint — module, verb, path, payload, status, `errorCode`, latency, verdict, baseline comparison |
| **Regressions** | `REGRESSED` + `GONE` only — the triage worklist |
| **Excluded** | Every skipped endpoint **with its reason** |
| **Coverage** | Executed vs declared vs excluded, by module |
| **Trend** *(E3)* | Pass rate and latency across recent builds |

The `Results` sheet keeps `APIExcelReportUtil`'s existing 11 columns in order so nothing downstream breaks,
then appends the differential columns.

> The exact column set is not fixed — if a column earns nothing in practice, drop it. The Summary and
> Regressions sheets are what people will actually read.

---

## 7. ⛔ Safety

The PAM API contains operations that will damage a real system if sent plausible data.

| Operation | Risk |
|---|---|
| `ARCOSWebDT.ReturnDataTable(USPName, serializedHashTable)` | **Unauthenticated stored-procedure execution** |
| `ARCOSWebDT.CallInlineQuery(commandText)` | **Unauthenticated arbitrary SQL** |
| All 9 `ARCONProvisioningWebAPI` operations | Create/delete/unlock real accounts on real AD, Unix and Windows targets |
| `OfflineSync` (24 ops) | Mutates synchronised state |
| Names matching `(?i)^(delete\|remove\|drop\|purge\|reset\|revoke\|disable)` | Destructive by name |

**Rules:**

1. **Default-deny on mutating verbs.** `GET` auto-included; every write needs an allowlist entry with a
   named approver (Y7).
2. **Never point at production** (Y1).
3. Enforce the blocklist **in the runner's endpoint resolution**, so a blocked operation is never
   materialised into a request.
4. The unauthenticated SQL endpoints are a **product finding, not a test finding** — raise separately
   under PAMIT.

---

## 8. Phases

```
P1  Runner + dry-run          ── no environment needed; proves resolution and the exclusion list
P2  Baseline capture          ── needs Y1–Y6; defines "known good"
P3  Verdicts + workbook       ── the deliverable
P4  CI gate + summary/email   ── unattended, per build
P5  Enhancements              ── E3, E5, E7 as appetite allows
```

| Phase | Steps | Effort | Environment |
|---|---|---|---|
| **P1** | Reflect `APIConfig`; resolve payload helpers; apply blocklist; `--dry-run` prints the plan and the 175 exclusions with reasons | **S** | ⬜ no |
| **P2** | Provision Y1–Y5; execute once against an approved build; commit `baselines/<env>-<build>.json` | **M** | ✅ yes |
| **P3** | Verdict engine; `BuildStabilityListener`; workbook. Fix the two defects below | **M** | ✅ yes |
| **P4** | Jenkins stage; fail on `REGRESSED`/`GONE`; HTML summary (E1); email subject line (E2) | **S** | ✅ yes |
| **P5** | Trend sheet, coverage burn-down, webhook | **S–M** | ✅ yes |

**Two defects to fix in P3**, both in reused code and both bite at 1,336 requests: `APIExcelReportUtil`
increments a static `rowIndex` without synchronisation under `parallel="classes"`, and `ApiHelper` calls
`Playwright.create()` per request without closing it.

**Exit criterion (P1):** `--dry-run` lists 1,161 executable endpoints and 175 exclusions, each with a reason.
**Risk:** None — no environment, no calls.
**Exit criterion (P3):** one command produces a workbook with a non-trivial verdict distribution.
**Risk:** Low–Medium.

---

## 9. Coverage expansion — optional, later

The runner covers what `APIConfig` declares. It cannot find endpoints nobody has catalogued. Closing that
needs a source-side pass, and there is an obstacle:

> ⛔ **The API the QA suite tests is not in the developer repo.** Measured across the full surface
> (2026-07-28), not spot-checked.

### 9.1 The overlap, measured

`APIConfig` declares **1,306** `/api/<Controller>/<Action>` pairs over **70** controllers. `pam/PAM` holds
**6,866** `.cs` files (110.9 M chars, 127,741 distinct identifiers) and **25** controller classes. Three
independent measures of how much of the declared surface that source actually contains:

| Measure | Result | What it counts |
|---|---:|---|
| Controller class **and** action method both present | **48 / 1,306 · 3.7 %** | Strict — a real implementation |
| Literal `"<Controller>/<Action>"` substring present | **99 / 1,306 · 7.6 %** | The route as written appears somewhere |
| Both identifiers appear anywhere in any `.cs` text | **351 / 1,306 · 26.9 %** | Deliberately generous upper bound — counts comments, client call sites, and coincidental collisions on common words (`User`, `Base`, `Policy`) |

| Also | |
|---|---:|
| Declared controllers absent from `pam/PAM` entirely | **23 / 70** |
| Distinct action names absent from all 110.9 M chars | **328 / 541 · 60.6 %** |

Absent controllers include every versioned family the suite exercises most —
`ServiceDetailsV2`, `ServiceDetailsV3`, `UserDetailsV2/V3/V4`, `UserRegistrationV2`, `ServicePasswordV2`,
`ServiceCreation`, `UserDelegation`, `TicketRequestDetails`.

`ActivityLogs` is the clearest case: **17** endpoints declared, **1** (`InsertSSMLogs`) implemented in
`OfflineAPI\Controllers\ActivityLogsController.cs`. The other 16 exist nowhere in `pam/`.
*(An earlier revision of this section said "6 declared, 1 implemented" — the declared count was
undercounted; the conclusion is unchanged and the ratio is worse.)*

Corroborating: the guides describe "ARCON PAM API" as a separately hosted component
(`client-manager:p104`), `pam_BaseAPIURL` targets a server rather than OfflineAPI's localhost Kestrel, and
`OfflineMultiTabService\...\PAMAPISync\` is a *client* of that remote API.

**Conclusion:** parsing `pam/PAM` cannot enumerate the API under test — it would discover under 8 % of it
and would mislead on the rest. The ten HTTP projects present are largely **not** the ones under test.
Three ways forward, in cost order:

| Option | Cost | Outcome |
|---|---|---|
| **O3 — developer adds Swashbuckle** | Small, theirs | Complete, automatic, permanent. The right answer |
| **O4 — obtain the API source**, then Roslyn-parse it | Medium, ours | Complete but needs maintenance |
| **Call-site harvest** — extract URL/verb/payload/response from `PAMAPISync\*.cs` and `ApiControllerConstant.cs` | Small, ours | Partial; recovers only what the product itself calls |

None is needed for §3 to deliver. Revisit after P4.

---

## 10. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Payload helpers contain stale or invalid bodies | Endpoints reject; results look uniformly bad | The differential model absorbs this — a consistent rejection baselines as normal, and only *change* is reported |
| Status-only assertion masks total failure | Catastrophic false confidence | §5.1 — `errorCode` is a first-class baseline field |
| Single credential used throughout | Whole module groups refused as 200 + `errorCode` | Y2 — bind credential by Access Type |
| CI agent IP/MAC unregistered | Every password test fails, with no log explaining why | Y3; re-register on agent recycle |
| Baseline encodes a bug as normal | Regressions become invisible | Promotion requires owner approval and a reviewable diff (E4) |
| Reflection silently misses a module | Coverage gap | P1 dry-run asserts 69 modules and 1,336 constants resolve; the count is itself a test |
| Fuzzing or writes corrupt the environment | Lost environment | §7 default-deny; Y1 disposable target |
| Guides mistaken for an API contract | Fabricated expectations | They contain no endpoints, schemas or error codes — `rag/findings.md` §6 |

---

## 11. Open questions

| # | Question | Blocks |
|---|---|---|
| Q1 | Which environment is the disposable target (Y1)? | P2 |
| Q2 | Who provisions the API User and registers the agent IP/MAC (Y2, Y3)? | P2 |
| Q3 | Will the developer add a `/version` endpoint (O1)? | Build attribution in P4 |
| Q4 | On `REGRESSED`, fail the build or warn only while the baseline settles? | P4 |
| Q5 | Who owns `CHANGED` / `NEW` triage (Y8)? | P4 |
| Q6 | Is O3 (Swashbuckle) worth raising with the developer, or is §9 deferred indefinitely? | §9 |
| Q7 | Should the harness replace `GenericScheduler` immediately, or after P3? — `rag/findings.md` §5 | P2 |

---

## 12. Registration

| Target | Change |
|---|---|
| `plan.md` §6 | Add: `` `dynamic-api-generation.md` `` — dynamic API validation and build-stability differential — Workstream `D` |
| `plan.md` §6 | Add: `` `rag/` `` — indexed product documentation, page-cited evidence layer |
| `status.md` §1 | Add a workstream `D` row |
| `status.md` §4 | Add `API endpoints under automated validation \| 0 \| 0 \| 1,161` and `Build-to-build drift detection \| none \| none \| per build` |
| `status.md` §5 | Note that blocker `B1` gates P2+ but **not** P1 |
| `status.md` §7 | Carry `Q1`–`Q7` forward |
