# Archived Requirements and Backlog (§5–§6)

**Part of** [`../objective_original_origin.md`](../objective_original_origin.md) — the project's permanent, append-only archive. The requirement detail retired from Objective.md, and the full contents of the retired pending-tasks-in-queue.md.

⛔ Append-only. Never delete, reword or reorder an entry. Section numbers (`§N`) are the stable citation scheme and do not change when files are reorganised.

---

## 5. Archived — requirement detail retired from `Objective.md` on 2026-08-03

The active requirement at the time was **API chaining, auto-generated**, on `QA_MsSQL` only, run type
*Continuation*. Role: automation architect assistant within BLAST. Target: `pam_automation_bootstrap` on
`AI` for framework code, `Reports/` for evidence, `Graphify/` for graph output, `pam/` never written to.

**Goal.** Chain APIs automatically — take a value from one endpoint's response and feed it into the next
endpoint's request, following the application's real flow. Fully auto-generated; no manual scripting per
chain.

**Why it is not a scripting job.** A hand-written chain is a fixture: it encodes one path through the API
and rots when the API moves. Chaining had to be derived the same way the rest of the framework is.

**How a chain is derived.** `producer --field--> consumer`, where the field appears in the producer's
*response* and in the consumer's *request* payload. Three inputs, none hand-listed: `APIConfig.java`
(endpoints), `utils/apiPayload/*.java` (input fields), captured responses (output fields).

**Confidence grading — a name match is evidence, not proof:**

| Grade | Basis | Usable? |
|---|---|---|
| high | identifier-shaped **and** producer response observed in a real run | ✅ after human confirmation |
| medium | identifier-shaped, producer inferred from naming | 🟡 review first |
| low | non-identifier field name | ⛔ coincidence |

Generic fields (`status`, `type`, `data`, `message`, `result`) were excluded — they match everywhere and
mean nothing.

**State at retirement:** 1,680 chain candidates derived (1,514 cross-module), 80 producers × 173
consumers, **0 observed** — all name-inferred. Built by `Graphify/api-graph/build_api_graph.py`.

**Tasks — script development was complete for all request types:**

| # | Task | Status |
|---|---|---|
| 1 | Derive chain candidates from payloads + responses | ✅ 1,680 |
| 2 | Interactive graph visualisation | ✅ `Graphify/api-graph/out/api-graph.html` |
| 3 | Capture request payload **templates**, not just field names | ✅ 257 templates |
| 4 | Chain executor — producer → extract → inject → consumer → validate | ✅ (now `workbench/scripts/run_chains.py`) |
| 5 | All five verbs | ✅ |
| 6 | Multi-hop depth A→B→C | ✅ depth 3 plans 7,357 chains |
| 7 | Path-template binding `/api/User/{id}` → `/api/User/42` | ✅ 6 templated paths |
| 8 | Chain results as their own Excel sheets | ✅ |
| 9 | Capture **observed** responses so chains stop being name-inferred | ⬜ blocked — environment |
| 10 | Port the chain runner to Java/TestNG | ⬜ deferred |

Plan volumes: depth 2 → 1,353 executable / 204 refused; depth 3 → 7,357 / 303. Verb shapes at depth 3 were
dominated by `GET→POST→POST` (2,350) and `POST→POST→POST` (2,165).

**⛔ Safety model — deny by default, because chaining can write.** Plan-only unless `--execute`; verb
opt-in via `--allow-verbs` (GET only by default); destructive names refused without `--allow-destructive`
*and* a named `--approver` recorded in the report; endpoint blocklist (`GetLogs`, `GetErrorLogs`,
`GetAllActiveUserDetails`) enforced at planning; 250 ms throttle; circuit breaker after 3 consecutive
5xx/timeouts; 200 calls max per run; pre-flight health probe. **The breaker and probe exist because the
earlier GET runner continued through 322 consecutive 503s during an outage.**

**Definition of done (met):** one command executes chained flows discovered automatically from the
catalogue, injects real values between calls, binds path templates, validates each hop across seven
layers, and reports every chain attempted *and* every chain declined with its reason.

**Supporting requirement — API graph visualisation**, three layers: `pam-scope/` (✅ 112,628 nodes),
`dev-scope/` (⬜ marker only, never built), `api-graph/` (✅ built). Output is stored under `Graphify/`,
not inside `pam/`, because writing there would dirty the reference repo.

**Constraints as stated then** — all still in force and now carried by the root `CLAUDE.md`: Playwright
Java + TestNG + Maven (Java 21) for framework deliverables; Python for the evidence harness, deliberately,
so reports regenerate without a Maven build; no manual test scripting; default-deny on mutating verbs;
never point at production; ⛔ never push, never merge.

**Output per run:** `Reports/Summary/*.md`, `Reports/Runs/<timestamp>/`, `Reports/Issues/*.md`, and
clarifying questions in MCQ form.

The five BLAST parameter tables that also sat in this file (phases, Protocol 0 gates, Discovery questions,
memory files, architecture layers) are **not duplicated here** — they are the framework's own definition
and live in `BLAST/B.L.A.S.T.md` and `BLAST/LLM.md`.

---

## 6. Archived — `pending-tasks-in-queue.md`, retired 2026-08-03

Final contents of the backlog file before deletion. Nothing here was in active scope.

### 6.1 Blocked on the owner

| # | Item | Blocks |
|---|---|---|
| B1 | **API token/credential for `devint` `ARCONAPIGateway`** + header name and scheme | Phase 1b entirely; 57 of 102 endpoints return 401. **Highest-value item in the file** |
| B2 | Confirm the approved **disposable target** for mutating verbs | Phase 3 |
| B3 | Approve the **write-endpoint allowlist** (default-deny is in force) | Phase 3 |
| B4 | Register the CI agent's **IP + MAC** under Settings → API → Registered Machines | Password-module endpoints refuse unregistered hosts |
| B5 | Decide whether the **legacy `:1602` surface is deprecated** | Whether Phase 4 is worth building |
| B6 | Is `u16hf` in scope, or devint-only? | Sheet spans two environments |

### 6.2 Ready to run — no blockers

| # | Item | Value |
|---|---|---|
| R1 | Extended GET tier, `--tier extended` (+121 operations) | Swagger GET coverage 35.9% → 78.5% |
| R2 | Re-run to settle whether ~20 s `getPulse` responses are cold-start or persistent | Decides whether ISSUE-006 escalates |
| R3 | Seed fixture for the 61 GETs with required parameters | GET coverage → 100% of 284 |

### 6.3 Deferred phases

- **Phase 3 — mutating verbs** (341 POST · 26 PATCH · 24 PUT · 15 DELETE). Needs B2 + B3.
  ⛔ **Safety non-negotiable:** the legacy surface includes `ARCOSWebDT.CallInlineQuery` (unauthenticated
  arbitrary SQL), `ARCOSWebDT.ReturnDataTable` (unauthenticated stored-procedure execution), and 9
  `ARCONProvisioningWebAPI` operations that create/delete real accounts on live AD, Unix and Windows
  targets. The blocklist must be enforced during endpoint *resolution*, so a blocked operation is never
  materialised into a request.
- **Phase 4 — legacy reflection runner.** Java/TestNG over `APIConfig.java`, joined by exact name identity
  to the 66 payload helpers; 87.7% executable immediately, differential verdicts only. **Fix first:**
  `APIExcelReportUtil`'s unsynchronised `static int rowIndex` under `parallel="classes"`, and `ApiHelper`
  calling `Playwright.create()` per request without closing it. Gated by B5.
- **Phase 5 — CI gate and trend reporting.** Jenkins stage; fail on `REGRESSED`/`GONE`; HTML summary,
  verdict line in the email subject, trend sheet, webhook on regression, reviewable baseline diff.
- **Phase 6 — negative and edge generation.** Stimuli are mechanical (drop field, type-swap, empty/zero/
  negative/overlong, wrong verb, absent/malformed token). **Expectations are not derivable** — no spec
  declares an error code — so verdicts come from the differential baseline. Also decide whether the 386
  hand-written negative classes are left alone or replaced.
- **Phase 7 — framework cleanup (ISSUE-008).** One commit: delete 246 commented lines in `ApiHelper.java`,
  delete `APIConfigOld.java`, drop 5 unused Maven dependencies, fix the `Se0rviceDetailsV3` typo, delete
  the inert `logback.xml` and the `App.java` stub. Separately: 218 orphaned test classes, 2 RestAssured
  holdouts.

### 6.4 Asks of the development team

Ordered by value per unit of their effort; items 1–5 are hours of work.

| # | Ask | Fixes |
|---|---|---|
| 1 | Declare real response codes in Swagger (400/401/404/500 minimum, with an error schema) | ISSUE-001 — removes most of the 66.7% L1 failure rate |
| 2 | Return JSON for every error, always, with `Content-Type` | ISSUE-002 |
| 3 | Make the envelope self-consistent — never `StatusCode: 401` with `Message: "Success"` | ISSUE-003 |
| 4 | Add `operationId` to every operation (currently 0 of 690) | Enables standard client/test generation |
| 5 | Remove `/WeatherForecast`; set real Swagger titles (201 of 690 are under `"Your API Name"`) | ISSUE-004 |
| 6 | A `/version` endpoint returning build number + commit SHA | `Version` is hardcoded `1.0.0.0` |
| 7 | Publish a Swagger aggregation endpoint on the gateway, replacing the shared CSV | ISSUE-007 permanently |
| 8 | Swagger for the legacy `:1602` surface, or confirm deprecation | ISSUE-005 · relates to B5 |
| 9 | Notify QA of intentional contract changes — one line in the release note | Turns `CHANGED` from an investigation into an acknowledgement |
| 10 | Profile `getPulse` — a health check should not block for 20 s | ISSUE-006 |

### 6.5 Open questions not yet decided

| # | Question | Needed for |
|---|---|---|
| Q1 | On `REGRESSED`, fail the Jenkins build or warn only while the baseline settles? | Phase 5 |
| Q2 | Who owns triage of `CHANGED` / `NEW` verdicts? | Phase 5 |
| Q3 | Should `LLM.md` accumulate one shared constitution across objectives, or be re-derived per objective? | BLAST hygiene |
| Q4 | Output filename — `result.xlsx` or `PAM_API_Validation_Results.xlsx`? | Cosmetic |
| Q5 | Port the harness to Java/TestNG, or keep the Python evidence generator separate? | Architecture |

### 6.6 Known limitations of the harness

| Limitation | Impact |
|---|---|
| Runs unauthenticated | 57 of 102 endpoints return 401. B1 fixes this |
| 20 s HTTP timeout | 11 endpoints yield no result; indistinguishable from a dead service |
| 53 of 102 operations declare **no response schema** | Layers L3/L4/L5 report `NA`, not `PASS` — coverage is honest but thinner than the endpoint count suggests |
| One spec unreachable (`AGWAPI_LINUX`) | Needs `10.10.2.24 devintagwpamu25.arconnet.com` in the hosts file |
| Baseline is first-run-wins | Whatever the first run saw became "known good". Re-baseline once authenticated |
| Python, not Java | Reports regenerate without a Maven build — deliberate — but a second toolchain. See Q5 |

### 2026-08-03 (later still) — standard CLI workflow defined

**Instructed:** define the workflow for all future CLI interactions. On a new instruction: write it into
`BLAST/Objective.md` first, review for ambiguity, ask any clarifications as MCQ, finalise the file, then
execute using `Objective.md` + this file + the rest of the workspace, and update documentation, reports
and history afterwards. `Objective.md` is the single source of truth for the current task.

**Decided:** D12, D13, D14 above. Two ambiguities were put to the owner as MCQs and answered:
substantive task requests trigger the write (not questions or process changes), and the outgoing
objective is always archived here first, even when superseded before any work happened.

**Done:** written into `CLAUDE.md` as §Standard workflow, placed immediately after §Active instructions
so it is read before anything else.

**Judgement recorded — why the workflow is not in `Objective.md`.** The obvious reading of the owner's
own rule ("write every new instruction into `Objective.md`") would put this workflow there. That is
self-defeating: `Objective.md` is overwritten by the next instruction, so a standing process rule stored
in it would delete itself the first time it was applied. **Standing rules belong in `CLAUDE.md`, which
loads every session; `Objective.md` carries only the current task.** D13 encodes this as a general
carve-out rather than a one-off exception.

**Also confirmed:** with `Objective.md` at ~2.2 KB the `UserPromptSubmit` hook now injects the file
**inline and in full** — verified on a live prompt. At 16.5 KB it had been spilling to a side file with
only a preview reaching context, so the slimming in the previous entry is what made the mechanism
actually work end to end.

<!-- ▼ APPEND NEW ENTRIES BELOW THIS LINE ▼ -->
