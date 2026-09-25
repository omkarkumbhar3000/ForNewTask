# PAM Automation Framework — Optimization Plan

**Framework:** PAM Automation Bootstrap · **Jira:** PAMIT
**Stack:** Playwright (Java) + TestNG + Maven · Java 21
**Editable scope:** `Automation gitlab repo/pam_automation_bootstrap/` only, on branch `AI`. The developer repo `pam/` — including `pam/AutomationTesting/` — is reference only, untouched; it receives the accepted code later by manual merge.
**Governing structure:** `../../skills/playwright-advance-e2e.SKILL.md` (8-layer architecture), with `../../skills/playwright-e2e.SKILL.md` and `../../skills/playwright-api.SKILL.md` as per-test style guides.

---

## 1. Assumptions

These were open questions. Decisions are recorded here so work can proceed; any of them can be reversed and the plan re-sequenced.

| # | Question | Decision taken | Rationale |
|---|----------|----------------|-----------|
| A1 | Which SKILL.md is the fixed structure? | `playwright-advance-e2e.SKILL.md` | It is the only skill that defines a full layered architecture plus a code-review checklist — the two things a conformance audit needs. |
| A2 | Does "assertions at test level only" include the `*HelperPage` layer? | **Pages: strip all assertions. Helpers: keep workflow assertions.** | In the 8-layer skill, Helpers *are* the Module (business-logic) layer, not the Page layer. Stripping all 559 Helper assertions would push them into 883 test classes and triple test verbosity for no architectural gain. Pages become pure locator + action + state-return, which is the actual violation being fixed. |
| A3 | Rollout strategy? | **Pilot two modules, then roll out module-by-module.** | A single sweep across ~1,000 files produces an unreviewable diff with no green baseline to prove nothing regressed. |
| A4 | Excel shape for API content validation? | **New columns on existing tables**; `InputType` already carries the classification. | The current workbooks already have an `InputType` column holding `Positive` / `MissingParameter` / `UnauthorizedAccess` etc. Adding sheets would duplicate endpoint and payload rows that already exist. |

**Additional standing rules**

- No behaviour change without a reason recorded in this plan.
- Every phase ends with `mvn clean compile` green; every module phase ends with its suite executed.
- Legacy code is *enhanced in place* wherever possible; rewrite only where the existing shape blocks the target structure.

---

## 2. Audit Baseline

Measured on the current `pam_automation_bootstrap` tree. These are the numbers every phase below is sized against.

### 2.1 Inventory

| Layer | Count |
|---|---|
| Test classes (`tests/`) | 883 |
| Page Objects (`pages/`) | 74 |
| Utilities + Helpers (`utils/`) | 25 |
| API payload helpers (`utils/apiPayload/`) | 66 |
| Suite XMLs | 101 |
| Environment property files | 20 |

### 2.2 Violations against the target structure

| Violation | Count | Skill rule broken |
|---|---|---|
| **Suite XMLs referencing a non-existent package** | **75 of 101** | — (blocks everything) |
| Assertions in `pages/` | 285 across 37 files | Pages are locator-only |
| Assertions in `tests/` | 5 files of 883 | Tests own assertions |
| Direct `BasePage` calls from test files | 266 across 33 files | Test → Page → Base hierarchy |
| `hardWait(int)` calls | 939 (652 in tests) | Use Playwright auto-waiting |
| `Thread.sleep` | 401 | Use Playwright auto-waiting |
| `waitForTimeout` | 121 | Use Playwright auto-waiting |
| `System.out.println` | 1,127 | Use SLF4J |
| `e.printStackTrace()` | 127 | Log and rethrow, or `Assert.fail` |
| Commented-out code lines | ~3,219 | Dead code |
| Test classes in no suite (orphaned) | 737 of 883 | Unreachable tests |
| `enabled = false` tests | 14 | Explainable skips only |

### 2.3 Critical finding — the API suites execute nothing

75 suite XMLs, including the CI entrypoint `CICD_Suites/APISuite.xml`, reference classes under
`com.arcon.tests.API_With_Excel.*`. **That package does not exist on disk.** It was renamed to
`com.arcon.tests.API.*` and the suite files were never updated. There are **345 active (uncommented)
broken class references**.

TestNG cannot instantiate a missing class, so those tests are reported as skipped or the suite aborts.
This is the direct, mechanical cause of instruction item 7 — *"tests get skipped without a valid,
explainable reason."*

**Consequence:** fixing this is Phase 0. Nothing else can be validated until suites actually run, and
no refactor can be proven safe without a green baseline.

### 2.4 Per-module violation profile

Sorted by remediation cost (violations ÷ files):

| Module | Files | hardWait | Thread.sleep | Assert | Direct base calls | Profile |
|---|---:|---:|---:|---:|---:|---|
| `UI/login` | 1 | 0 | 0 | 0 | 0 | **Reference pattern — already compliant** |
| `UI/CRUD/DigitalVault` | 1 | 0 | 0 | 0 | 0 | Clean |
| `UI/CRUD/autoOnboarding` | 1 | 0 | 0 | 0 | 0 | Clean |
| `UI/CRUD/PAMLogs` | 143 | 0 | 0 | 0 | 0 | Clean at test level |
| `API/All_API_Positive` | 79 | 0 | 0 | 0 | 0 | Clean; blocked by broken suites |
| `API/Negative_API` | 386 | 0 | 0 | 0 | 0 | Clean; blocked by broken suites |
| `UI/CRUD/SessionMonitoring` | 8 | 0 | 1 | 0 | 0 | Near-clean |
| `UI/CRUD/UserDiscovery` | 1 | 0 | 0 | 1 | 0 | Near-clean |
| `UI/Negative` | 6 | 5 | 0 | 0 | 0 | Light |
| `UI/CRUD/setting` | 20 | 5 | 2 | 0 | 1 | Light |
| `UI/CRUD/PasswordVault` | 8 | 0 | 25 | 1 | 0 | Sleep-heavy |
| `UI/CRUD/UAG` | 4 | 0 | 0 | 15 | 0 | Assertion-heavy |
| `UI/sanity` | 1 | 0 | 0 | 0 | 21 | **Hierarchy violation** |
| `UI/CRUD/ACMO` | 37 | 47 | 5 | 0 | 0 | Wait-heavy |
| `UI/CRUD/AccessControl` | 4 | 16 | 0 | 4 | 24 | Mixed, small |
| `UI/CRUD/AdministrativeConsole` | 10 | 36 | 0 | 1 | **138** | **Worst hierarchy violation density** |
| `UI/EndToEnd` | 86 | **413** | 10 | 0 | 77 | **Worst overall** |
| `other` | 40 | 1 | 1 | 0 | 2 | Light |

### 2.5 Page and Helper layer profile

| Page package | Files | Assertions to move | hardWait |
|---|---:|---:|---:|
| `pages/acmo` | 34 | **160** | 92 |
| `pages/setting` | 19 | 60 | 12 |
| `pages/password_vault` | 8 | 46 | 3 |
| `pages/administrativeConsole` | 9 | 19 | 1 |
| `pages/sessionMonitoring`, `digitalVault`, `autoOnboarding`, `UAG` | 4 | 0 | 0 |

| Helper (Module layer — assertions **retained** per A2) | Lines | Assert | hardWait |
|---|---:|---:|---:|
| `AcmoHelperPage` | 4,825 | 117 | 31 |
| `SettingHelperPage` | 4,264 | 89 | 14 |
| `PasswordVaultHelperPage` | 4,089 | 91 | 7 |
| `AdministrativeConsoleHelperPage` | 3,356 | 120 | 37 |
| `AccessControlHelperPage` | 2,566 | 77 | 18 |
| `DigitalVaultHelperPage` | 2,565 | 17 | 59 |
| `PAMLogsHelperPage` | 1,524 | 36 | 8 |
| `UAGHelper` | 1,357 | 3 | 0 |
| `SessionMonitoringHelperPage` | 493 | 9 | 0 |
| `BasePage` | 760 | 24 | 1 |

> `BasePage` holding 24 assertions is itself a violation — `validateElementOnPage`, `validateLabelOnPage`,
> `validateLocatorOnPage`, and `validateCount` assert inside the base layer. Addressed in Phase 2.

---

## 3. Target Architecture

Per `playwright-advance-e2e.SKILL.md`, mapped onto the existing tree. **No new top-level layout** — the
framework already has all eight layers; the work is making each layer obey its contract.

| Layer | Location | Contract |
|---|---|---|
| 1 · Configuration | `Env_configs/`, `Environments/`, `autoconfigs/`, `pom.xml` | Resolve once into `AutoConfigs`. No file reads in tests. |
| 2 · Pages | `pages/**` | Locators as named `String` fields + single UI actions. **No assertions. No cross-screen orchestration.** Return `this` or state. |
| 3 · Helpers (Modules) | `utils/*HelperPage.java` | Business workflows, conditional logic, `@Step`-annotated. May assert workflow outcomes. |
| 4 · Utilities | `utils/BasePage.java`, `ExcelUtils`, `DBUtils`, `DatePicker`, `FileUpload` | Reusable primitives. **No assertions in `BasePage`.** |
| 5 · API | `utils/ApiHelper.java`, `utils/apiPayload/**` | `APIRequestContext` only. Status + response-time + **content** validation. |
| 6 · Test Base | `utils/BaseTest.java` | `ThreadLocal` browser state, lazy accessors, `clearPage()` teardown. |
| 7 · Tests + Reporting | `tests/**`, listeners, suite XMLs | Tests own assertions and orchestrate Helpers. Every class registered in a suite. |
| 8 · CI/CD | `jenkins.properties` | Windows agents, `bat`, `-Dmaven.test.failure.ignore=true`. |

**Call-chain rule (instruction item 3):**
`Test → Helper → Page → BasePage → Playwright`
A test may call a Helper or a Page. A test may **never** call a `BasePage` primitive directly.

---

## 4. Phase Sequence

Phases are ordered by dependency, not by size. Each phase has a hard exit criterion; the next phase does
not start until it is met.

```
Phase 0  Restore executability      ── unblocks everything, zero refactor risk
Phase 1  Establish green baseline   ── the safety net every later phase is measured against
Phase 2  Fix the shared layers      ── BasePage + BaseTest; every module depends on these
Phase 3  Pilot two modules          ── prove the pattern end-to-end, get sign-off
Phase 4  Roll out module-by-module  ── 16 increments, easiest first
Phase 5  API content validation     ── new capability (instruction item 6)
Phase 6  Dead-code removal          ── safe only once suites and coverage are trustworthy
Phase 7  Conformance gate           ── lock the structure in so it cannot regress
```

---

### Phase 0 — Restore Executability

**Why first:** 75 of 101 suites point at a package that does not exist. Until this is fixed, no test
result means anything and no refactor can be validated.

| Step | Action | Files |
|---|---|---|
| 0.1 | Rewrite `com.arcon.tests.API_With_Excel.` → `com.arcon.tests.API.` across all suite XMLs | 75 XMLs, 345 active refs |
| 0.2 | Reconcile sub-package names — old `.Positive.` / `.Negative.` vs. actual `.All_API_Positive.` / `.Negative_API.<Mode>.` | same |
| 0.3 | Delete or correct refs to classes that exist nowhere (e.g. `AllAPIPositive`) | audit output |
| 0.4 | Re-run the orphan/broken-ref audit; both counts must reach zero for API suites | — |
| 0.5 | Register the 737 orphaned test classes, or record in `orphans.md` why each stays unregistered | 737 classes |

**Exit criterion:** zero suite entries referencing a missing class. `CICD_Suites/APISuite.xml` runs real tests.
**Risk:** very low — XML-only, no Java touched.

---

### Phase 1 — Green Baseline

**Why:** Without a known-good "before" result, no later phase can prove it broke nothing.

| Step | Action |
|---|---|
| 1.1 | `mvn clean compile` — record and fix any existing compile errors |
| 1.2 | Run each suite against a stable environment; capture pass/fail/skip per class |
| 1.3 | Record the baseline in `baseline.md` |
| 1.4 | Triage every skip into: broken ref (Phase 0), genuine `enabled=false`, environment/data, or flaky |
| 1.5 | Annotate each of the 14 `enabled = false` tests with a reason comment and a PAMIT ticket, or delete it |

**Exit criterion:** every skip has a documented, explainable cause (instruction item 7).
**Risk:** none — read-only measurement.

---

### Phase 2 — Shared Layers

**Why before modules:** all 12 UI modules inherit from `BasePage` and `BaseTest`. Fixing these first
means each module phase is a small delta rather than a re-litigation of the same problem.

| Step | Action | Detail |
|---|---|---|
| 2.1 | Remove the 24 assertions from `BasePage` | Split each `validateXxx` into a state-returning `getXxx`/`isXxx` in `BasePage`, plus an asserting wrapper in the relevant Helper. Keep the old method as a thin deprecated delegate for one phase so modules migrate incrementally. |
| 2.2 | Add auto-waiting primitives to `BasePage` | `waitForVisible`, `waitForEnabled`, `waitForText`, `waitForCondition(BooleanSupplier)` — all reading their budget from `Environments/<env>.Properties`. These are the sanctioned replacements for `hardWait`. |
| 2.3 | Deprecate `hardWait(int)` | `@Deprecated` + Javadoc pointing at the replacement. Do not delete yet — 939 call sites migrate per module. |
| 2.4 | Audit `BaseTest.clearPage()` | Confirm every lazy accessor has a matching null-out line. Missing entries cause cross-test failures. |
| 2.5 | Replace `System.out.println` and `printStackTrace()` in `BasePage`/`BaseTest` with SLF4J | 1,254 sites total across the tree; shared layers only in this phase |

**Exit criterion:** `BasePage` contains zero assertions; auto-wait primitives available; `mvn clean compile` green; Phase 1 baseline unchanged.
**Risk:** medium — shared blast radius. Mitigated by deprecated delegates rather than hard removal.

---

### Phase 3 — Pilot (2 modules)

Prove the full pattern on one already-good module and one bad one, then freeze it as the reference.

**Pilot A — `UI/login` (1 file, zero violations)**
Already the cleanest module and the pattern the instruction points to as the model. Work here is to
*document* it as the reference implementation and close the gaps against the skill: add TestNG groups,
`@Severity`/`@Description`, and move `LoginPage`'s 8 assertions up a layer.

**Pilot B — `UI/CRUD/AdministrativeConsole` (10 files, 138 direct base calls, 36 hardWait)**
Highest violation *density* in the tree, but only 10 files — the best ratio of lessons learned to risk.

Per-pilot steps:

1. Strip assertions from the module's Page Objects → state-returning methods.
2. Move workflow assertions into the module's Helper; move outcome assertions into the test.
3. Replace direct `BasePage` calls in tests with Page/Helper methods.
4. Replace `hardWait` / `Thread.sleep` with Phase 2 auto-wait primitives.
5. Replace `System.out.println` with SLF4J; fix swallowed exceptions.
6. Add TestNG groups (`P0`/`P1`/`P2` + feature) and `PAM_<MODULE>_###` descriptions.
7. Confirm suite registration; run the module suite; compare against Phase 1 baseline.

**Exit criterion:** both modules pass the skill's Code Review Checklist; results match baseline; pattern written up in `approach/reference-pattern.md`.
**Risk:** low — 11 files, fully reversible.

---

### Phase 4 — Module Rollout

One module per increment, easiest first, so the pattern is exercised repeatedly on low-risk targets
before reaching `UI/EndToEnd`. Each increment is independently reviewable and revertible.

| # | Module | Files | Primary work | Effort |
|---:|---|---:|---|---|
| 1 | `UI/CRUD/DigitalVault` | 1 | Conformance only (Helper has 59 hardWait) | S |
| 2 | `UI/CRUD/autoOnboarding` | 1 | Conformance only | S |
| 3 | `UI/CRUD/UserDiscovery` | 1 | 1 assertion | S |
| 4 | `UI/sanity` | 1 | 21 direct base calls → Page methods | S |
| 5 | `UI/CRUD/SessionMonitoring` | 8 | 1 `Thread.sleep` | S |
| 6 | `UI/CRUD/UAG` | 4 | 15 assertions relocate | S |
| 7 | `UI/CRUD/AccessControl` | 4 | 24 base calls + 16 hardWait + 4 assertions | M |
| 8 | `UI/Negative` | 6 | 5 hardWait | S |
| 9 | `UI/CRUD/PasswordVault` | 8 | 25 `Thread.sleep`; 46 Page assertions | M |
| 10 | `UI/CRUD/setting` | 20 | 60 Page assertions; light waits | M |
| 11 | `UI/CRUD/ACMO` | 37 | 47 hardWait; 160 Page assertions in `pages/acmo` | L |
| 12 | `UI/CRUD/PAMLogs` | 143 | Test level already clean — verify + register only | M |
| 13 | `other` | 40 | Light; decide keep vs. fold into owning modules | M |
| 14 | `API/All_API_Positive` | 79 | Conformance; feeds Phase 5 | M |
| 15 | `API/Negative_API` | 386 | Conformance; 5 failure-mode folders | L |
| 16 | **`UI/EndToEnd`** | 86 | **413 hardWait + 77 base calls** — deliberately last | **XL** |

`UI/EndToEnd` is last on purpose: it holds 44% of all `hardWait` calls, spans every module, and is the
most fragile. By the time it is reached, the auto-wait primitives will have been proven on 15 modules.

**Per-increment exit criterion:** module suite runs, result matches or beats baseline, Code Review Checklist passes.

---

### Phase 5 — API Dynamic Content Validation

Delivers instruction item 6. Today `ApiHelper` validates HTTP status and response time only.

**Design**

Extend the existing Excel tables rather than adding sheets — `InputType` already classifies each row.

| Existing columns | New columns |
|---|---|
| `InputType`, `ModuleName`, `RequestType`, `EndPoint`, `Payload`, `ExpectedStatus` | `ExpectedContent`, `MatchType`, `ExpectedErrorCode` |

`MatchType` values: `contains` · `equals` · `jsonPath` · `regex` · `notContains`.
`ExpectedContent` blank ⇒ content validation skipped, existing behaviour preserved.

**Classification** derives from `InputType`, which already carries `Positive`, `MissingParameter`,
`InvalidValue`, `InvalidDataType`, `UnauthorizedAccess`, `MethodNotAllowed`:

- **Positive** — `InputType = Positive`
- **Negative** — any of the five failure-mode values
- **Other** — anything else (informational, data-setup, exploratory rows)

**Critical domain constraint:** most PAM endpoints answer **HTTP 200 with an application-level
`errorCode` envelope**. A rejected request is usually a 200, not a 4xx. `ApiHelper` already handles this
via `validateResponseErrorCode(...)`. Content validation must assert the envelope, not only the status —
a status-only check passes against a rejected request.

| Step | Action |
|---|---|
| 5.1 | Add `validateResponseContent(APIResponse, String expectedContent, String matchType)` to `ApiHelper`, returning a structured result rather than asserting directly |
| 5.2 | Extend `validateApiResponseWithResponseTime_ExcelBased(...)` with the content parameters, keeping the current overload intact for backward compatibility |
| 5.3 | Add the three columns to `API_Automation_Test_Input_Data.xls` and `Negative_API_Automation_Test_Input_Data.xls` |
| 5.4 | Widen the affected `@DataProvider` methods and test signatures |
| 5.5 | Extend `APIExcelReportUtil` to emit a Positive / Negative / Other breakdown per module |
| 5.6 | Pilot on one module (`ActivityLogs`), then roll across the rest |

**Exit criterion:** one module fully content-validated with results classified three ways in the Excel report; existing status-only rows still pass unchanged.
**Risk:** low — additive, backward compatible.

---

### Phase 6 — Dead Code Removal

**Deliberately late.** Deleting code before Phase 0/1 risks removing something only *appears* unused
because its suite reference is broken.

| Step | Target | Count |
|---|---|---|
| 6.1 | `APIConfigOld.java` — confirm no references, delete | 1 file |
| 6.2 | `pages/acmo/api/API_BaseClass.java`, `APIServices.java` — the only REST Assured users; migrate or delete | 2 files |
| 6.3 | `src/main/java/com/arcon/tests/App.java` — Maven archetype stub | 1 file |
| 6.4 | Commented-out code blocks | ~3,219 lines |
| 6.5 | Duplicate/superseded methods (`getResponse` overloads, `createPlayWrightInstance` vs `…IgnoreHttpsErrors`, `createBrowserInstance`, `launchApp`) | ~8 methods |
| 6.6 | `Temp/` suites — promote to a real suite folder or delete | 3 XMLs |
| 6.7 | Unreferenced page/helper methods after the module rollout | TBD |
| 6.8 | Duplicated `gitignore` (root) vs `.gitignore` | 1 file |

**Exit criterion:** `mvn clean compile` green; full suite result matches Phase 1 baseline.
**Risk:** medium — mitigated entirely by doing it last.

---

### Phase 7 — Conformance Gate

Prevents regression back to the current state.

| Step | Action |
|---|---|
| 7.1 | Write `code-review-checklist.md` from the skill's checklist, adapted to PAM |
| 7.2 | Add a build-time check failing on `Thread.sleep`, `System.out.println`, or `printStackTrace` in `src/test/java` |
| 7.3 | Add a suite-integrity check failing the build on any `<class name>` that does not resolve |
| 7.4 | Add an orphan check reporting test classes in no suite |
| 7.5 | Document the "new module" recipe so future work starts compliant |

**Exit criterion:** a PR reintroducing a banned pattern or a broken suite reference fails the build.

---

## 5. Sequenced Backlog

The single ordered list. Work top to bottom; do not start an item until the one above meets its exit criterion.

| Seq | Phase | Item | Risk | Blocks |
|---:|---|---|---|---|
| 1 | 0 | Fix 345 broken suite refs across 75 XMLs | Very low | Everything |
| 2 | 0 | Resolve the 737 orphaned test classes | Very low | Baseline accuracy |
| 3 | 1 | Capture green baseline + triage every skip | None | All refactors |
| 4 | 2 | Strip 24 assertions from `BasePage` | Medium | All modules |
| 5 | 2 | Add auto-wait primitives; deprecate `hardWait` | Medium | All modules |
| 6 | 2 | Audit `clearPage()` completeness | Low | All modules |
| 7 | 3 | Pilot A — `UI/login` reference pattern | Low | Rollout |
| 8 | 3 | Pilot B — `UI/CRUD/AdministrativeConsole` | Low | Rollout |
| 9 | 3 | Publish `reference-pattern.md`; obtain sign-off | None | Rollout |
| 10–25 | 4 | 16 module increments, per the Phase 4 table | Low → XL | — |
| 26 | 5 | `validateResponseContent` + Excel columns | Low | — |
| 27 | 5 | Positive/Negative/Other reporting | Low | — |
| 28 | 5 | Roll content validation across API modules | Low | — |
| 29 | 6 | Dead-code removal (8 sub-steps) | Medium | — |
| 30 | 7 | Conformance gate + docs | Low | — |

---

## 6. Companion Documents

`plan.md` (this file) is the master sequence. These are produced as the phases they describe are reached:

| File | Content | Produced in |
|---|---|---|
| `baseline.md` | Pre-refactor suite results; skip triage | Phase 1 |
| `orphans.md` | The 737 unregistered classes, with a keep/register/delete decision each | Phase 0 |
| `reference-pattern.md` | The proven pattern from the pilots, as a copy-paste template | Phase 3 |
| `module-<name>.md` | One per module: before/after, decisions, deviations | Phase 4 |
| `api-content-validation.md` | Excel schema, match types, classification rules | Phase 5 |
| `code-review-checklist.md` | PAM-adapted conformance checklist | Phase 7 |
| `dynamic-api-generation.md` | Dynamic API validation and build-to-build differential — reflection-driven runner over `APIConfig` + payload helpers | Workstream `D` (parallel) |
| `../../rag/` | Indexed ARCON PAM product documentation (1,101 pages), queryable and page-cited — the evidence layer for Workstream `D` | Workstream `D` (parallel) |
| `../../skills/` | The `*.SKILL.md` specs this plan is written against — `playwright-advance-e2e` governs structure | Pre-existing input |
| `../../../README.md` | Workspace orientation: what every top-level folder is, for someone opening the project cold | Standardization, 2026-07-28 |

All files in this table are siblings inside `workbench/`, referenced by short relative path. The workspace
root holds only `README.md`, `CLAUDE.md`, and the five top-level folders — see the root `README.md`.

**Workstream `D`** runs in parallel to Phases 0–7. It does not block on the refactor phases, and its first
phase needs no environment. Its subject is the *product* build's stability, not the automation code's
conformance — see `dynamic-api-generation.md` §1.3 for the boundaries against Phases 5 and 7.

---

## 7. Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| No green baseline exists today (75 suites broken) | Cannot prove a refactor is safe | Phases 0 and 1 run before any Java change |
| Shared-layer changes break every module at once | High | Deprecated delegates, not hard removal; Phase 2 runs against the baseline |
| Removing `hardWait` exposes genuinely slow PAM screens | Tests fail that used to pass | Budgets move to `Environments/<env>.Properties`; tune per environment, not per test |
| 939 wait removals cause flakiness | Erodes trust in the suite | Module-by-module, each verified against baseline before moving on |
| Assertion relocation changes hundreds of method signatures | Large diff | Pages only (285 sites), not Helpers (559 retained) — per assumption A2 |
| Deleting "unused" code that is only unreachable via a broken suite | Silent coverage loss | Dead-code removal deferred to Phase 6, after suites are trustworthy |
| Excel schema change breaks existing API suites | API regression | New columns are optional; blank `ExpectedContent` preserves current behaviour |
| Scope creep into the developer repo `pam/` | Violates the hard constraint | Every phase above is confined to `pam_automation_bootstrap/`; `pam/` must end every session with a clean `git status` |

---

## 8. Status

> **Live status is tracked in [`status.md`](./status.md).** That file is updated as each phase
> completes and holds the current metrics, blockers, and open questions. This section is a summary only.

| Phase | State |
|---|---|
| Audit | **Complete** — Section 2 |
| Plan | **Complete** — this document |
| **Phase 0 — Restore executability** | **✅ Complete** — 341 → 0 broken refs; 737 → 218 orphans; 3 suites created; 0 Java files touched |
| **Phase 1 — Green baseline** | **🟡 Partial** — compile green (1,063 sources); suite execution blocked on environment access |
| Phases 2–7 | Not started |

**Phase 0 outcome:** 75 of 101 suite XMLs referenced `com.arcon.tests.API_With_Excel.*`, a package that
does not exist. This was the mechanical cause of instruction item 7. Also closed a coverage gap of 227
negative-API tests that had no suite at all. Full detail in [`orphans.md`](./orphans.md).

**Current blocker:** no reachable PAM environment, so the Phase 1 baseline run cannot complete. Phases
2–4 are refactors of shared classes inherited by all 883 test classes and must not start without a
baseline to measure against.

**Next action:** Phase 1.5 — annotate the 14 `enabled = false` tests. It is the only remaining Phase 1
step that does not require a live environment.
