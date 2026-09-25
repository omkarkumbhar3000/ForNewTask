# A3 — Negative-validation scenario matrix — what the API refuses, and what nobody checks

**Objective:** OBJ-007 item A3 · **Generator:** `tools/obj007_negative_matrix.py`
**Data:** `artifacts/analysis-data/negative-validation.json` · `artifacts/analysis-data/negative-coverage-summary.json`
**Scope:** all **1,306** endpoints × **8** scenarios = **10,448** rows across **19** categories
**HTTP requests issued:** 0 · **Database queries issued:** 0 — generated from static sources plus prior run evidence

---

## 1. The headline

| Measure | Value | Share |
|---|---:|---:|
| Scenario rows generated | **10,448** | 100% |
| …with **no documented expected outcome** (`UNKNOWN — contract undocumented`) | **7,664** | **73.4%** |
| …with an expected outcome **measured** from a real response | 172 | 1.6% |
| …with a framework-asserted expected outcome (401 / 405) | 2,612 | 25.0% |
| Endpoints with **zero runnable negative coverage** | **1,289** of 1,306 | **98.7%** |
| Endpoints with any runnable negative coverage at all | **17** | 1.3% |

**Seven thousand six hundred and sixty-four negative tests cannot be written**, not because nobody has
found time, but because **no artifact anywhere in the product states what the endpoint is supposed to do
when the input is wrong.** That is the finding. It is not a coverage backlog — it is a missing
specification, and it blocks the coverage backlog.

The three sources that would normally settle it each fail in a different way:

| Source | Why it cannot answer |
|---|---|
| The product code | **3** `[Required]` attributes across **~6,738** properties. No length, format, range or pattern validation exists at the model layer, so the intended rejection is not expressed in code |
| The Confluence API export (2,470 pp) | 3,194 payload examples but only **4 error codes** and **1 of 9** response shapes. It documents requests, not refusals |
| The two administrator guides (1,101 pp) | Access model and product concepts only — **no endpoints, schemas or error codes** |

## 2. What the framework asserts today — and why it is worth nothing here

### 2.1 On paper it looks like a negative suite exists

| Artifact | Count |
|---|---:|
| Negative test classes on disk (`tests/API/Negative_API/`) | 386 |
| `@Test` methods in them | 650 |
| Negative suite XMLs (`API_Suites/Negative/`) | 5 |
| Class entries those suites wire | 382 |
| Rows of negative test data in `testdata/Negative_API_Automation_Test_Input_Data.xls` | 3,652 |

### 2.2 Almost none of it can execute

| ⛔ Defect | Measurement |
|---|---|
| **199 of 279** `@DataProvider` names referenced by the negative classes **do not exist** | `API_DataProviderUtils.java` defines 145 providers; the negative classes reference 279. TestNG cannot resolve the other 199, so those `@Test` methods fail at initialisation — they never reach an assertion |
| The **80** that do resolve read the **positive** sheets | e.g. `MissingParameter/User.java` uses `dataProvider = "User"`, which resolves to `AllApiPositiveScenarios` → `User_positive`. A test named *MissingParameter* runs valid data |
| The **3,652-row negative workbook is loaded by nothing** | `AutoConfigs.java:37` declares `Negative_API_ExcelDataProviderFileName` and 6 environment files set it, but **no `@DataProvider` ever reads it.** Every provider reads `API_ExcelDataProviderFileName`. **3,049** rows carrying an expected status are unreachable |
| **Zero** of the 650 negative validator calls read the envelope | All **650** call `validateApiResponseWithResponseTime_ExcelBased`. The envelope-aware variant `…_ExcelBasedsettingnegative` is called **0** times from `Negative_API/` |

### 2.3 What actually runs

Three driver classes, and only these three, resolve a negative data provider at runtime:

| Driver | Providers | Rows | Endpoints | Asserts |
|---|---:|---:|---:|---|
| `Negative_API.KotakSNOWApi.*` | 3 | 98 | 18 | HTTP status only |
| `Negative_API.SNOWApi.*` | 2 | 16 | 8 | HTTP status only |
| `API_Dynamic.Settings` | 1 | 2,104 | 76 | HTTP 200 **+ `errorCode`** — but see below ⛔ |

⛔ **The framework's only envelope assertion could never have passed.**
`ApiHelper.validateResponseErrorCode` gated every body-level check on `node.has("success")` — **camelCase**.
Across the 1,868 captured responses, lowercase `success` appears in **0** and PascalCase `Success` in
**1,580**. The very first assertion in that method therefore failed on every real response it was ever given,
so it could never reach the `errorCode` comparison beneath it. *(Since fixed by delegating to a new
`PamEnvelope` class.)*

The consequence for this matrix: before that fix, **body-level negative coverage against the API was not
thin, it was zero.** The `Settings` track's 2,104 rows were the framework's only envelope-aware negative
tests, and the assertion they relied on could not execute. Nothing anywhere in the framework had ever
successfully compared a PAM `errorCode` against an expected value.

⚠️ **The "3 controllers" figure understates the gap two ways.** Measured precisely:

- The 114 loadable rows from KotakSNOW/SNOW map to **17** of the 1,306 catalogue endpoints (**1.3%**),
  spread over **5** controllers — `ServiceCreation`, `ServiceDetails`, `ServicePassword`,
  `ServicePasswordDependancy`, `UserDetails` — out of **70** controllers in the catalogue.
- `API_Dynamic.Settings` is the framework's **only** envelope-aware negative testing, asserting HTTP 200
  with `errorCode` 201 (545 rows) or 203 (1,559 rows). But its 76 endpoints are all
  `/AdminAPI/api/...` — and **0 of them are in the 1,306 `/api/` catalogue.** It is a different API
  surface. Against the catalogue it contributes nothing.

So the runnable negative assertion surface against 1,306 endpoints is **114 rows over 17 endpoints, none
of which check anything but a status code.**

### 2.4 The statuses those 114 rows assert

| Status | Rows |
|---:|---:|
| 400 | 61 |
| 405 | 26 |
| 401 | 26 |
| 404 | 1 |

Plus the 3,049 unreachable rows, which assert **405** (1,551), **401** (1,485) and **200** (13) — and
never an `errorCode`.

**Two of nineteen categories.** The entire 3,652-row negative corpus exercises only *wrong HTTP method*
and *invalid authentication*. The other **17** categories in this matrix have no test data at all, live or
dead.

## 3. Why a status-only assertion is worthless on this API

Most PAM endpoints return **HTTP 200 with an application-level error in the body.** A rejected request is
usually a 200. Therefore:

```
Assert.assertEquals(response.status(), 200);   // passes against a fully rejected request
```

This is not theoretical. From `artifacts/runs/2026-07-29_181439/results.json`, on **HTTP 200**:

| Measured response | Hops |
|---|---:|
| `ErrorMessage='System error has occurred'` | 55 |
| `ErrorMessage="Parameter error occurred-Required property 'UserId' not found in JSON. Path '', line 1, position 2."` | 18 |
| `ErrorMessage='Input parameter is null'` | 16 |
| `ErrorMessage='PageSize is required should be greater than 0.'` | 12 |
| `ErrorMessage='Parameter error occurred-Error converting value "AUTO40PC47" to type \'System.Int64\''` | 12 |
| `ErrorMessage='Validation error occurred - UserName is Mandatory'` | 7 |
| `Success=False` (envelope-level refusal) | 303 |

Every one of those is a refusal wearing a 200. The run's own layered checks show the scale: `http-status`
passed **1,688 / 1,868** while `envelope` passed only **1,278** and `message-semantics` only **1,410**.
**590 responses that a status assertion called healthy were refusals.**

Three further traps any generated assertion must survive:

| ⛔ Trap | Consequence |
|---|---|
| **`Success: true` is not evidence of a write** | `POST /api/ServiceCreation/SetServiceDetails` returns `Success: true` with `Message: "Already Exists"` — nothing inserted, status green, flag green. **70** measured responses carried `Success:true` while writing nothing. Create assertions must read **`Message` semantics** |
| **31 distinct response shapes** were measured, against **6** documented | Including a **bare array with no envelope** (`GET /api/DeviceOnboarding/GetLOBList`) and `Result` as an object not an array (`GetServiceDetails`). No generated assertion may assume a shape. The run recorded **126** bodies that were not JSON objects at all — 113 of them bare strings |
| **Casing is not stable enough to hard-code** | The envelope is PascalCase (`Success`) on live responses; the framework's own validator looked for `success` and matched nothing in 1,868 captures. Any assertion must read the envelope case-insensitively |
| **`KNOWN_ERROR_CODES = {"201","202","203"}`** is incomplete | `ApiHelper.java:1423`. A live run captured `ErrorCode: "206-LC_GLD"` on HTTP 200, which that set rejects as unknown |

## 4. What a correct assertion looks like, per category

Framework-level rejections (401, 405) are the **only** cases where a status check is legitimate — they are
refused before a handler runs, so there is no envelope to read. `ApiHelper.java:1425` encodes exactly this:
`validateResponseErrorCode` is invoked only when `expectedStatusCode == 200`.

| Category | Rows | Correct assertion | Expected outcome |
|---|---:|---|---|
| **invalid authentication** | 1,306 | Status **401** + assert the body carries no `Result` payload. A 200 means the endpoint is anonymous | ✅ 401, traceable |
| **wrong HTTP method** | 1,306 | Status **405** (`ExpectedMethodNotAllowedAPIStatusCode`, `Environments/QA_MsSQL.properties`). Tests routing, not safety — deletion here is `POST /api/<C>/Delete<Thing>` | ✅ 405, traceable |
| **invalid authorization** | 1,306 | Read the envelope: a refusal is `Success:false`, so a status check cannot separate "refused" from "served" | ⬜ Undocumented — no endpoint→role matrix exists anywhere |
| **SQL-injection string** | 1,306 | Three assertions, none a status check: refused-or-literal; **no** SQL error text / driver name / table name / stack frame in the body; row count does not exceed the unmutated request. A 500 is itself the defect | ⬜ Undocumented |
| **missing mandatory field** | 1,306 | HTTP 200 + `Success:false` + non-null `ErrorCode` + `ErrorMessage` **naming the missing property** | 🟡 Measured on 106 rows; 1,200 undocumented |
| **invalid business rule** (cross-LOB scope) | 387 | Assert **`Result[]` contents**, not `Success`. A scope leak is HTTP 200, `Success:true`, and simply too many rows — invisible to both status and envelope assertions | ⬜ Undocumented — and never exercised, so no measurement exists |
| **boundary condition** | 387 | Refusal naming the field for −1 / 0 / Int64-max. An overflow surfacing as 500 or as `'System error has occurred'` is a defect — 55 such generic errors already measured | 🟡 24 measured |
| **malformed JSON** | 387 | Parse failure that leaks **no** stack frame, .NET type name or line position. The product already leaks parser internals on *well-formed* input: `"…Path '', line 1, position 2."` reaches the client verbatim | ⬜ Undocumented |
| **missing/incorrect content-type** | 387 | Either 415 with no envelope, or 200 + `Success:false`. Silent acceptance is the defect | ⬜ Undocumented |
| **invalid combination** | 386 | Refusal enumerating **every** unsatisfied field — PAM does aggregate these (`'ServiceIP is required, ServiceUserName is required'`) | ⬜ Undocumented |
| **oversized payload** | 386 | The assertion that matters is the **follow-up**: the API must still answer a normal request. Availability, not the oversized call's status | ⬜ Undocumented |
| **null vs empty-string** | 211 | Assert `null` and `""` yield **identical** `Success`/`ErrorCode`. Divergence means undeclared nullability semantics | ⬜ Undocumented |
| **invalid length** | 211 | Refusal naming a limit, **or** a read-back proving the value was stored untruncated. Silent truncation defeats status *and* envelope assertions alike | ⬜ Undocumented |
| **invalid enumeration** | 210 | Refusal listing permitted values. The permitted set is documented nowhere, so the enum domain is itself an open question | ⬜ Undocumented |
| **invalid data type** | 209 | 200 + `Success:false` + `ErrorMessage` naming **that specific field**. A generic `'System error has occurred'` means the binder error was swallowed | 🟡 11 measured |
| **invalid object reference** | 209 | 200 + `Success:false` identifying the unresolvable reference. **`Success:true` with an empty `Result[]` is a defect** — "not found" must not be reported as success | 🟡 29 measured |
| **invalid data format** | 209 | Refusal naming the field and expected format, then a read-back proving nothing was stored | ⬜ Undocumented |
| **invalid relationship** | 208 | A **paired** assertion. Per-field validation that passes two ids independently while accepting an impossible pair is the defect | ⬜ Undocumented |
| **duplicate data** | 131 | Assert **`Message` semantics**: `"Inserted Successfully"` = inserted, `"Already Exists"` = no-op. Not status, not `Success` | 🟡 2 measured |

The pattern across that table: **for 13 of 19 categories the correct assertion is not a status code and not
even the `Success` flag — it is the content of `ErrorMessage` or of `Result[]`.** The framework asserts
neither, on any endpoint.

## 5. Where the measured evidence came from

`actual_response` is never invented. It carries one of exactly two things:

| Value | Rows |
|---|---:|
| `MEASURED (HTTP <n>): <verbatim detail>` + flow/hop citation + evidence filename | **172** |
| `NOT EXECUTED — no evidence` | 10,276 |

The run exercised **valid** requests, so a measured value appears only where the product's response to that
valid request *was itself the negative condition* — a missing-property rejection, a type-conversion
failure, an unresolvable reference. **452** endpoints produced at least one such rejection. Example row:

| Field | Value |
|---|---|
| `endpoint_id` | `Encryption/GetAESEncryptedText` |
| `scenario_category` | missing mandatory field |
| `expected_status` | `200` |
| `expected_error_message` | `MEASURED: 'Parameter error occurred-Text is Mandatory'` |
| `actual_response` | `MEASURED (HTTP 200): ErrorMessage='Parameter error occurred-Text is Mandatory' (HTTP 200)` |
| `evidence_ref` | `results.json#flows[encryption__reads_1].hops[4]; artifacts/runs/2026-07-29_181439/evidence/627_encryption__reads_1_GetAESEncryptedText.json` |

Where a row carries a measured expectation, `remarks` says so explicitly: it is **observed behaviour, not a
contract.** Every row also carries the valid-request baseline (status, content-type, envelope, body size)
in `remarks` where the run measured one — context for the mutation, never the mutation's own result.

⚠️ **80 endpoints answered an empty body with `'Required property … not found'`.** The framework's
*positive* tests send exactly that empty body. Those positive tests are passing against rejected
requests — a negative finding produced by the positive suite.

## 6. Safety classification — names, never verbs

Deletion on this API is `POST /api/<Controller>/Delete<Thing>`, so a verb guard is useless. Every row is
classified by endpoint **name** at generation time, before any request could be built.

| `automation_status` | Rows | Basis |
|---|---:|---|
| `NOT AUTOMATED — safe to execute` | 6,635 | read/other role, not blocklisted |
| `REQUIRES APPROVAL — write endpoint` | 2,500 | `create` / `update` role |
| ⛔ `DO NOT EXECUTE — takes API down` | **880** | 110 endpoints, see below |
| ⛔ `DO NOT EXECUTE — mutating` | 400 | 50 endpoints: `Delete*` / `Remove*` prefix or `teardown` role |
| `AUTOMATED — status-only assertion` | 33 | the 17 endpoints with live coverage |

**110 blocklisted endpoints**, in two tiers:

| Tier | Endpoints | Detail |
|---|---:|---|
| Named in the brief | **14** | `ActivityLogs/GetLogs`, `ActivityLogs/GetErrorLogs`, and 12 `GetAllActiveUserDetails*` variants across `UserDetails` V1–V4 |
| Same action name, other controllers (LH-08) | **96** | Every other `GetLogs` / `GetErrorLogs` in the catalogue |

✅ **Independent confirmation of LH-08.** Counting `GetLogs` + `GetErrorLogs` across all controllers gives
**98** endpoints — exactly the figure LH-08 quotes as at risk, derived here from the catalogue alone.

Corroborating evidence from the run: the 4 endpoints that were issued and returned **no response at all**
are `GetAllActiveUserDetailsMapping` on `UserDetails` V1–V4 — the blocklisted family, consistent with the
API being unavailable at that point.

## 7. Reconciliation — every count traced

### 7.1 Catalogue: 1,306

| Step | Count |
|---|---:|
| Route constants parsed from `APIConfig.java` (value begins `/`) | 1,322 |
| − surplus constants (11 paths declared by more than one constant name) | −13 |
| = distinct paths | 1,309 |
| − non-endpoint paths: `//api/AzureKeyVault/GetDatabaseStatus` (double-slash typo), `/api/Lob/Get/{id}`, `/api/User` (unbound route templates) | −3 |
| **= catalogue endpoints** | **1,306** ✅ |

✅ **This reconciles with the figures already documented in `.claude/rules/api-surface.md`**, which counts
on a `/api/` prefix rather than `/`. The single difference is the double-slash typo
`//api/AzureKeyVault/GetDatabaseStatus`, which a `/api/` filter excludes:

| Basis | `/api/` prefix (documented) | `/` prefix (this parse) |
|---|---:|---:|
| Declarations, duplicates included | 1,321 | **1,322** (+1 typo) |
| Distinct paths | 1,308 | **1,309** (+1 typo) |
| Distinct `(controller, action)` endpoints | **1,306** | **1,306** |

⚠️ **This is also where the stale `1,322` comes from** — it is the raw route-constant count, not an endpoint
count. `source-map.json` independently holds exactly 1,306 `Controller/Action` keys, and every constant it
references exists in `APIConfig.java`.

### 7.2 Run coverage: 870

| Step | Count |
|---|---:|
| Catalogue endpoints appearing in the run's hop list | 875 |
| − never issued, skipped as destructive (`meta.skipped`: `DeleteAdDomain` ×2, `RemoveUserStatusDetails` ×2, `DeleteRTSMLog` ×1) | −5 |
| **= endpoints exercised** | **870** ✅ |
| …of which returned no response (status null) | 4 |
| …of which returned a numeric HTTP status | 866 |

**431** of the 1,306 endpoints have no run evidence of any kind; 1 of 70 controllers was never touched.

## 8. Scenario selection — how 19 categories fit into 8 slots per endpoint

Every applicable scenario was generated first, then each endpoint keeps 8:

| Slot | Rule |
|---|---|
| 1–4 | The four universal categories — invalid authentication, wrong HTTP method, invalid authorization, SQL-injection string. They apply to every endpoint and are the highest-value tests on a privileged-access product |
| 5 | The single highest-value shape-driven scenario (normally *missing mandatory field*) |
| 6–8 | Filled preferring **globally under-represented** categories, tie-broken toward rows that carry measured evidence |

Naive top-8 truncation was tried first and starved the rare categories — *invalid relationship* scored **0
rows** and *invalid combination* 2, despite applying to hundreds of endpoints. The scarcity-aware pass is
what puts all 19 categories in the matrix. `description` on every row states **why that scenario applies
to that endpoint**, citing its field count, C# type, `required_hint`, or the absence of any documented body.

**731 of 1,306 endpoints have no documented request body in any of the four sources.** Those get
shape-appropriate scenarios instead — empty-body-against-undocumented-contract, non-JSON body, undeclared
query parameter — and their *missing mandatory field* row says plainly that whether the endpoint requires
input at all is unknown.

## 9. Honest limits

| Limit | Consequence |
|---|---|
| No request was issued and no database was queried | Every `expected_*` is either documented, framework-asserted, measured from the prior run, or `UNKNOWN`. Nothing was confirmed live |
| Mandatory-ness is **inferred** | Only **3** `[Required]` attributes exist product-wide. `required_hint` in `source-map.json` derives from a field appearing in every documented example — a hypothesis, not a contract, and `description` says so per row |
| Confluence payloads bind to endpoints **by page proximity** | Some field sets attributed to an endpoint will be wrong, so some `payload` values are wrong. The owner has confirmed the export is not current |
| The 172 measured expectations are **observed behaviour** | They record what the product did, not what it should do. A measured `'System error has occurred'` is evidence of a defect, not a contract to assert against |
| Measured evidence is attributed **only where the observed rejection matches the scenario** | A generic `Success=False` on a valid request proves a refusal happened, not *which* mutation would cause it. Such rows stay `NOT EXECUTED — no evidence` rather than borrowing an unrelated measurement — this deliberately lowered the measured count from 322 to 172 |
| The matrix caps at 8 scenarios per endpoint | 19 categories × applicability would yield more. Rows dropped were the lowest-weight applicable ones; `scenarios_applicable_per_category_before_cap` in the summary records what was generated before the cap |
| `oversized payload` and `invalid length` payloads are **descriptors** | Written as `<1048576-char 'A' string — materialise at execution time>` rather than literal megabytes |

## 10. What this unblocks, in order

| # | Action | Why first |
|---:|---|---|
| 1 | **Get an expected-outcome contract for the 7,664 undocumented rows** — start with the 1,306 *invalid authorization* rows | No test can be written without it. This is a specification request, not a testing task |
| 2 | **Fix the 199 unresolvable `@DataProvider` references** | 386 test classes and 650 `@Test` methods currently cannot run. Highest ratio of value to effort in the repo |
| 3 | **Wire `Negative_API_ExcelDataProviderFileName`** (`AutoConfigs.java:37`) | 3,049 rows of negative data are already written and unreachable |
| 4 | **Repoint the 650 negative validator calls** at `…_ExcelBasedsettingnegative` | Until then no negative test can detect a 200-with-error-body, which is how this API refuses. The camelCase defect that made that validator inert is now fixed (`PamEnvelope`), so this step finally buys something |
| 5 | **Extend `KNOWN_ERROR_CODES`** beyond `{201,202,203}` (`ApiHelper.java:1423`) | `206-LC_GLD` was measured live and the current set rejects it as unknown |
| 6 | **Assert against the 31 measured response shapes, not the 6 documented ones** | A generated assertion that assumes one envelope shape fails on 25 shapes nobody documented |
| 7 | **Enforce the 110-endpoint blocklist at planning time** | Two `ActivityLogs` endpoints stopped the IIS application pool in three sequential calls. LH-08 re-validation is forbidden, not merely skipped |

---

**Reproduce:** `python tools/obj007_negative_matrix.py` — deterministic, no network, no database.
