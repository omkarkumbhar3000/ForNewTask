# Framework Validation Enhancement — What Changed and Why

**Objective:** `OBJ-007` items 7, 8, 10 · **Repo:** `Automation gitlab repo/pam_automation_bootstrap`, branch `AI`
**State:** compiles clean (`mvn -o clean test-compile`), 15 new tests pass, **nothing committed — awaiting approval**
**Verification:** `mvn -o clean test -Dtest=PamValidationLayerTest` → `Tests run: 15, Failures: 0, Errors: 0`

---

## 1. The problem, stated as measurement

The framework validated HTTP status codes on an API where **the status code is not the answer**.

| Measured | Value |
|---|---:|
| Calls returning HTTP 200 | 1,688 of 1,868 |
| …of which carried an application-level failure | 289 |
| Status-only pass rate on the 2026-07-29 run | **90%** |
| True pass rate across all layers | **64%** |
| Responses where `Success: true` accompanied no write | **70** |
| …caught by the framework | **0** |
| Distinct response shapes measured | **31** (6 documented) |
| Endpoints with runnable negative coverage | **17 of 1,306** |

Three defects made this worse than "shallow":

1. **The one envelope assertion could never pass.** `ApiHelper.validateResponseErrorCode` read
   `node.has("success")` in camelCase. Across all 1,868 captured responses, lowercase `success` occurs in
   **0** and PascalCase `Success` in **1,580**. Jackson is case-sensitive, so the method's first assertion
   failed on every response this API can produce. Body-level coverage was not thin — it was **zero**.
2. **The error-code set was hardcoded and asserted hard.** `KNOWN_ERROR_CODES = {"201","202","203"}` would
   have failed the test for the real, measured `206-LC_GLD` returned on HTTP 200 — reporting a legitimate
   product response as a broken test.
3. **Database validation had never run and could not have.** Three independent faults, §4.

---

## 2. What was built — `com.arcon.utils.validation`

**Seven** classes, 1,568 lines. The design principle throughout: **a check that could not run is never
reported as a pass.**

| Class | Responsibility |
|---|---|
| `PamApiValidator` | The orchestrator — the fluent entry point every test calls. Configures expectations, runs every layer, returns the report |
| `PamEnvelope` | Normalises every measured response shape behind one accessor set. Resolves both field casings, unwraps a one-element array **only when it really is an envelope**, and classifies into 8 shape classes — all 8 occur in the evidence, none is speculative |
| `ValidationLayer` | The twelve layers, `L1`–`L12`. `L1`–`L7` match the chaining harness so a framework result and a harness result compare layer for layer; `L8`–`L12` are what the harness could not do |
| `ValidationOutcome` | One check result, with `PASS` / `FAIL` / `NOT_APPLICABLE` / `NOT_RUN` as **first-class** verdicts |
| `ValidationReport` | Collects every layer, then asserts once. Names all failures together, and counts the `NOT_RUN` gap separately |
| `ErrorCodeRegistry` | Prefix-matched, extensible. An unrecognised code is an **observation, not a failure** |
| `DbPersistenceValidator` | `L11` checks as composable lambdas over the rewritten `DBUtils` |

### The twelve layers

| Layer | Check | Why it exists here |
|---|---|---|
| `L1` | `http-status` | Retained, but its pass message says outright that status alone proves nothing on this API |
| `L2` | `content-type` | 127 measured responses are not JSON objects at all |
| `L3` | `envelope` | The rejection is in the body. **This is the layer that matters most** |
| `L4` | `message-semantics` | The only way to tell `"Inserted Successfully"` from `"Already Exists"` |
| `L5` | `chain-key-extracted` | Reproduces the `MISSING ['NEW_ID']` failure mode as a first-class check |
| `L6` | `record-exists` | Read-back |
| `L7` | `latency` | SLA |
| `L8` | `schema` | Field presence and type |
| `L9` | `mandatory-fields` | Present **and** non-empty |
| `L10` | `business-rule` | A domain assertion, not merely that the call returned |
| `L11` | `db-persistence` | Did the row actually land |
| `L12` | `security` | Leaked stack traces, SQL exceptions, connection strings |

### Why `NOT_RUN` is the most important design decision

`L9`–`L12` mostly cannot run today, because the metadata they need does not exist. The temptation is to
omit them; that would report a two-layer suite as complete.

Instead each records `NOT_RUN` **with a reason**, and `ValidationReport.notRun()` makes the gap countable —
so a report says "5 layers could not run: no mandatory field set supplied — only 3 of ~6,738 properties are
declared required" rather than silently claiming coverage. `NOT_RUN` does not fail the build: a missing
contract is a documentation defect, not a test failure.

This is not theoretical. The **exact opposite** mistake produced the most misleading number in the previous
run: 105 of 107 `L6` read-backs were recorded `FAIL` when 97 of them had searched each response for the
literal string `${NEW_ID}` and could never have passed. Those verdicts carried no information, and were
being read as product failures.

### Usage

```java
// Positive - a create. Note that expectSuccess() alone is not enough.
new PamApiValidator("POST", endpoint, response, elapsedMs)
    .expectStatus(200).expectJson().expectSuccess()
    .expectInserted()                                  // Message semantics, not the flag
    .expectFields("ServiceId", "ServiceName")
    .expectMandatory("ServiceId")
    .expectChainKey("ServiceId")
    .expectPersisted(DbPersistenceValidator.recordExistsById("sso_services", "sas_id", "ServiceId"))
    .expectNoServerInternals()
    .withinMs(5000)
    .validate().assertAll();

// Negative - the expected status is 200, not 400. That is the product's contract.
new PamApiValidator("POST", endpoint, response, elapsedMs)
    .expectStatus(200).expectJson()
    .expectRejection("202")
    .expectErrorMessageContains("mandatory")
    .validate().assertAll();
```

---

## 3. What changed in existing code

| File | Change |
|---|---|
| `utils/ApiHelper.java` | `validateResponseErrorCode` rewritten onto `PamEnvelope`. Fixes the casing defect; a shape with no envelope is now **reported, not failed**; an unrecognised error code is recorded rather than asserted. `KNOWN_ERROR_CODES` removed in favour of `ErrorCodeRegistry` |
| `autoconfigs/AutoConfigs.java` | DB property keys fixed (§4), `db_type` read from the environment, `isDatabaseConfigured()` added |
| `utils/DBUtils.java` | Rewritten — §4 |

**Deliberately not changed:** the commented-out superseded block in `ApiHelper` (~line 1319) was left in
place. Deleting it is correct but is an unrelated change, and it is the kind of edit that should not be
mixed into a functional one. It is recorded as `OBS-011`.

---

## 4. `DBUtils` — rewritten (item 10)

### Three faults, each independently sufficient to prevent any DB assertion

1. **The config keys were wrong.** `AutoConfigs.db_name` read the property `"databaseName"` and
   `db_user_name` read `"db_user"` — **neither key existed in any environment file**, which declared
   `db_name` and `db_user_name`. Both resolved to `null` even in a fully populated environment. *This is the
   mechanical reason no DB assertion has ever run in this framework.*
2. **`db_type` was the hardcoded literal `"mysql"`** while `DBUtils` built a `jdbc:sqlserver` URL and logged
   "Connecting to MSSQL" — three different databases described in one code path.
3. **Nothing could consume a result.** Every method returned `void` or printed to `System.out`.
   `executQuerry` returned a `ResultSet` over a connection opened separately and closed elsewhere. The
   utility had **zero callers**, and was unusable for assertion rather than merely unused.

### What it does now

| Concern | Before | After |
|---|---|---|
| Dialect | `jdbc:mysql` URL, MySQL driver, MSSQL log message | Derived from `db_type`; URL, driver and log agree. SQL Server and MySQL/MariaDB both handled |
| Results | printed to stdout | `query()` returns `List<Map<String,Object>>`; `count()`, `exists()`, `queryScalar()`, `queryFirstRow()` are assertion-shaped |
| Connections | opened per call, never closed | try-with-resources; closed before `query()` returns |
| Parameters | string concatenation (`getOtpQuerry`) | `PreparedStatement` binding throughout |
| Safety | none | **read-only by default** — any non-`SELECT` statement is refused unless `allowMutations()` is called explicitly |
| Unconfigured env | attempted connection, logged an exception | detected up front; `L11` records `NOT_RUN` |
| Timeouts | none | query timeout 60 s, login timeout 20 s, both configurable |

Backward compatibility kept for `getConnection()`, `executeQueryAndPrint()` and `runRequiredQueries()`.
`executQuerry(String, String)` is retained `@Deprecated` returning rows — the old `ResultSet` return could
not have worked. `getOtp`/`getOtpQuerry` had already been removed upstream; both were MySQL-schema-specific
(`myvaultdb`) and had no callers.

The read-only guard is a **safety control, not a preference**: the supplied `devops` login is `sysadmin` and
`dbcreator` over 30 databases, several of them not QA.

### Verified end to end

The exact JDBC URL the framework builds was executed against the QA database:

```
jdbc:sqlserver://10.10.0.194:1433;databaseName=ARCOSDB_U16SP2_WEBSM_QA;encrypt=true;trustServerCertificate=true;loginTimeout=20
CONNECTED  readOnlyAccepted=true
parameterised count for sls_id=1 -> 1
```

Driver-level read-only is **accepted** by the SQL Server driver, so the guard operates at two levels.

---

## 5. Verification — `PamValidationLayerTest`

15 tests, **all passing**, over response bodies taken from
`artifacts/runs/2026-07-29_181439/evidence/`. Real bodies matter: a normalisation layer tested only against
fixtures its author invented proves nothing, and the whole reason the layer exists is that the real shapes
exceed any specification.

**No network calls, no database access** — it runs anywhere, needs no bearer token, and cannot trip the
endpoint blocklist.

| Test | What it pins down |
|---|---|
| `PAM_VAL_001` | All 8 shape classes classify correctly, including non-JSON and empty bodies |
| `PAM_VAL_002` | **PascalCase `Success` is read** — the regression that disabled body validation entirely |
| `PAM_VAL_003` | Result rows normalise across array, object and bare-array shapes |
| `PAM_VAL_004` | Field lookup is case-insensitive (identifier casing varies by controller) |
| `PAM_VAL_005` | A bare array is not mistaken for an envelope, but a wrapped envelope still unwraps |
| `PAM_VAL_006` | `"Already Exists"` **fails** the insert assertion in both measured wordings, while `L1` and `L3` pass — the trap, demonstrated |
| `PAM_VAL_007` | Rejection at HTTP 200 is caught, with `L1` passing to prove a status-only assertion would not have |
| `PAM_VAL_008` | An expected rejection passes, and `206-LC_GLD` is recognised |
| `PAM_VAL_009` | The `MISSING ['NEW_ID']` mode is reported at `L5` with `L3` passing — a contract gap, not a test bug |
| `PAM_VAL_010` | A bare-array endpoint does **not** fail merely for lacking an envelope |
| `PAM_VAL_011` | Non-JSON and naked-boolean bodies produce a `FAIL`, never an exception |
| `PAM_VAL_012` | Unconfigured layers report `NOT_RUN` **with a reason**, are countable, and do not fail the build |
| `PAM_VAL_013` | An empty `ServiceId` on a successful create is caught at `L9` |
| `PAM_VAL_014` | A leaked `SqlException` and server address is caught at `L12` |
| `PAM_VAL_015` | Every failing layer is named at once, not just the first |

---

## 6. What this does not fix

Stated plainly, because a framework change can create the impression that a coverage problem is solved.

| Limitation | Why |
|---|---|
| **`L9`/`L10` mostly stay `NOT_RUN`** | On the surface under test the declared-required count is **0 of 5,175**. No framework can assert a mandatory field nobody has declared |
| **`L11` needs a least-privilege account before CI use** | ⚠️ *This row previously said `L11` was "unproven" because no DB row appeared newer than 2025-10-01. **That was wrong** — see `OBS-012`/`OBS-045`. The newest row is `2026-08-03 15:29:18`, and the API's writes demonstrably land in `ARCOSDB_U16SP2_WEBSM_QA`, confirmed three ways.* `L11` works; what gates enabling it in CI is replacing the `sysadmin` login — `MF-08` |
| **Business-name lookups cannot work** | Name columns are AES-encrypted at rest. Validate by integer key; `recordExistsByName` reports `INCONCLUSIVE` rather than a false negative |
| **The 76 existing API suites are not migrated** | The package is in place and verified; re-pointing the suites is the remaining QA-side work |
| **The negative suite needs rewiring first** | 199 of 279 referenced data providers do not exist, and the 80 that resolve read *positive* sheets — `MF-12`. Better assertions on data that tests the wrong thing changes nothing |
| **Two latent defects untouched** | `APIExcelReportUtil`'s unsynchronised row index and `ApiHelper`'s unclosed Playwright instances — `OBS-015`. Both must be fixed before any full-catalogue run |

---

## 7. Recommended sequence

| # | Step | Owner | Depends on |
|---:|---|---|---|
| 1 | Fix `APIExcelReportUtil` synchronisation and `ApiHelper` Playwright leak | QA Automation | — |
| 2 | Triage the negative suite: delete dead, re-point mis-wired | QA Automation | — |
| 3 | Migrate positive suites onto `PamApiValidator`, controller by controller | QA Automation | 1 |
| 4 | Confirm the QA API's database write target | Development / DBA | — |
| 5 | Replace the `sysadmin` login with a QA-scoped `SELECT`-only account | IT Ops / DBA | — |
| 6 | Enable `L11` persistence assertions | QA Automation | 4, 5 |
| 7 | Populate `L9`/`L10` as the contract is published | QA Automation | `MF-01`, `MF-13` |

Steps 1–3 need **no developer dependency** and can start immediately.
