# A2 — Positive API validation — what is covered, and what is never checked

**Scope:** every endpoint under positive testing · **Catalogue:** 1,306 endpoints · **Evidence:** `artifacts/runs/2026-07-29_181439/` (326 flows · 1,873 hops · 1,868 HTTP calls)
**Extractor:** `tools/obj007_positive_analysis.py` — zero HTTP requests, zero database queries
**Data:** `artifacts/analysis-data/positive-validation.json` (2,304 rows, all 1,306 endpoints) · `artifacts/analysis-data/envelope-shapes.json` · `artifacts/analysis-data/_a2-false-success.json`

---

## 1. Coverage — 870 of 1,306 measured, and two different definitions of "covered"

"Positive coverage" has two independent meanings here and they do not agree. The harness run is the only
source of **measured** request/response behaviour; the framework suites are the only thing that **ships**.

| Source | Endpoints | % of 1,306 | What it proves |
|---|---:|---:|---|
| **`harness-run`** — reached by a live call in `artifacts/runs/2026-07-29_181439/` | **870** | 66.6% | measured status, latency, body, L1–L7 verdicts |
| **`framework-suite`** — present in `API_Suites/Positive_All` data tables | **1,205** | 92.3% | a test row exists; **no verdict was captured in this evidence base** |
| **`both`** | **801** | 61.3% | ✅ the only endpoints with both a shipping test and measured behaviour |
| `harness-run` only | **69** | 5.3% | ⚠️ measured, but no framework test would ever exercise them |
| `framework-suite` only | **404** | 30.9% | ⚠️ a test row exists and nothing measured — `NOT EXECUTED — no evidence` |
| **`neither`** | **32** | 2.5% | ⛔ zero positive coverage of any kind |

**Reconciling 870 against 875.** Flows *name* 875 distinct endpoints; 5 were withheld before a request was
built by the destructive-endpoint guard (`meta.skipped` in `results.json`), so they issued no HTTP call:
`ADbridging/DeleteAdDomain`, `ADbridging/RemoveUserStatusDetails`, `ADbridgingV2/DeleteAdDomain`,
`ADbridgingV2/RemoveUserStatusDetails`, `RTSM/DeleteRTSMLog`. **870 = endpoints with an actual call**, which
is the brief's figure. It reproduces exactly.

**Row accounting** in `positive-validation.json` (2,304 rows, 1,306 distinct `endpoint_id`):

| Row class | Rows |
|---|---:|
| One per harness hop (`flow_id` + `hop_number` populated) | 1,873 |
| Endpoints with no harness hop, but a framework test row | 399 |
| Endpoints with no coverage at all (`source = neither`) | 32 |

### 1.1 The 32 endpoints with zero positive coverage

Concentrated almost entirely in one controller — **`UserDetailsV3` contributes 17 of the 32**, and it is the
only `UserDetails*` variant whose framework data table is nearly empty (4 of 71 endpoints, against 68 of 72
for `UserDetails`/`V2`/`V4`). The rest are the SCIM-style `/api/User/*` surface (`User/Delete`,
`User/Details`, `User/Edit`, `User/{id}` — the only PUT/DELETE verbs in the catalogue),
`UserDetailsV2/*FromAD` AD-lookup reads, the three `ServiceReferenceEvent` variants,
`ADbridging/DeleteRuleFromRuleId`, `UserLabels/GetErrorLogs`, `UserOnboarding/UpdatePamUser`, and
`UserRegistrationV2/UserExists`. Full list: filter `positive-validation.json` on `source == "neither"`.

⚠️ **9 of them are `teardown`/`update` writes** (`UserDetailsV3/DeleteUser`, `DisableUser`,
`EnableUsersbyUserGroup`, `UpdateUserDetails`, …). Uncovered destructive endpoints are the worst class of
gap: nothing asserts they refuse a bad request, and nothing asserts they succeed on a good one.

### 1.2 Per-controller split (top 30 by catalogue size)

`harness` = reached by a live call · `framework` = present in a `Positive_All` data table · `neither` = no coverage.

| Controller | Catalogue | harness | framework | neither |
|---|---:|---:|---:|---:|
| ServiceDetailsV2 | 132 | 100 | 130 | 1 |
| ServiceDetails | 126 | 88 | 124 | 1 |
| ServiceDetailsV3 | 123 | 93 | 120 | 1 |
| UserDetails | 72 | 55 | 68 | 0 |
| UserDetailsV2 | 72 | 36 | 68 | 4 |
| UserDetailsV4 | 72 | 45 | 68 | 0 |
| **UserDetailsV3** | **71** | **54** | **4** | **17** |
| ADbridging | 34 | 24 | 33 | 1 |
| ADbridgingV2 | 33 | 24 | 33 | 0 |
| ServicePasswordV2 | 26 | 19 | 26 | 0 |
| DeviceOnboarding | 21 | 13 | 16 | 0 |
| NotificationDetails | 20 | 11 | 20 | 0 |
| SIEM | 20 | 18 | 20 | 0 |
| RDPSServiceInsertV2 | 19 | 10 | 19 | 0 |
| RASyn | 18 | 9 | 18 | 0 |
| RDPSServiceInsert | 18 | 9 | 18 | 0 |
| UserOnboarding | 18 | 10 | 17 | 1 |
| ActivityLogs | 17 | 14 | 17 | 0 |
| ServicePassword | 17 | 14 | 17 | 0 |
| LobandService | 15 | 12 | 15 | 0 |
| Collaborations | 14 | 11 | 14 | 0 |
| FileServerDetail | 14 | 9 | 14 | 0 |
| Logs | 14 | 10 | 14 | 0 |
| ATSMapping | 13 | 6 | 13 | 0 |
| Configuration | 13 | 9 | 13 | 0 |
| ServicePasswordDependancy | 13 | 9 | 13 | 0 |
| UIAutomationData | 13 | 8 | 13 | 0 |
| UserRegistration | 13 | 8 | 13 | 0 |
| UserRegistrationV2 | 13 | 8 | 12 | 1 |
| **OfflineSync** | 10 | **1** | 10 | 0 |
| **Command** | 5 | **0** | 5 | 0 |

The full 70-row table is reproducible from `positive-validation.json`; the script prints it. Two entries are
worth flagging: `Command` (5 endpoints, **zero** harness calls) and `Se0rviceDetailsV3` — a **typo'd
controller name in `APIConfig.java`** that the catalogue faithfully carries as a real endpoint.

### 1.3 Three structural defects in the framework's positive layer

Found while resolving suite → class → data-provider → Excel table. All are static, all are certain.

| ⛔ | Finding | Evidence |
|---|---|---|
| ⛔ | **7 data providers point at Excel tables that do not exist.** `getTableArray` returns `null`, so the `@DataProvider` yields nothing and the test cannot run | `Kotak.kotak`, `UAGChallenge`, `UAGConfigure`, `UAGDashboard`, `UAGReports`, `UAGReview`, `UserDiscovery` — each names a `*_positive` table absent from sheet `AllApiPositiveScenarios` of `testdata/API_Automation_Test_Input_Data.xls` |
| ⚠️ | **9 of 79 positive test classes are in no `Positive_All` suite** — they can only ever run via `-Dtest=`, which disables the suite `<listeners>` and so produces no Excel report | `CaptureLogImage`, `DeviceOnboarding`, `Kotak`, `KotakSNOWApi`, `SNOWApi`, `ServicePassword`, `UAGConfigure`, `UAGReview`, `WebSM` (71 suite XMLs reference only 70 distinct classes) |
| ⚠️ | **210 endpoints in the positive Excel are absent from `APIConfig.java`** — the data workbook and the catalogue describe different surfaces | 1,415 distinct endpoints in the positive tables, 1,205 in the 1,306 catalogue. The 210 are mostly the SCIM surface (`Service/*` 86, `User/*` 64, `ServiceGroup/*` 22, `UserGroup/*` 18) plus lowercase typos such as `servicedetails/...` |

---

## 2. What is asserted today — the framework checks two things, the harness checked seven

### 2.1 The framework: status equality and a response-time budget. That is all.

All 71 `Positive_All` suites route to one method. Quoting it directly:

| Assertion | Location |
|---|---|
| HTTP status equality | `ApiHelper.java:1273` — `Assert.assertEquals(statusCode, expectedStatusCode, "Unexpected response status code:")` |
| Response time under budget | `ApiHelper.java:1276` — `Assert.assertTrue(responseTimeMs <= expectedTimeoutMs, ...)` |
| Response **body** validation | `ApiHelper.java:1286-1293` — **commented out.** The `validateApiResponseBody(response, sampleResponse)` call and its `Assert.fail` are dead code |

The identical pattern repeats in the sibling overload at `ApiHelper.java:1195` / `1198`, with its body check
dead at `ApiHelper.java:1208-1215`. **No positive test in this framework reads the response body.** Every
row in `positive-validation.json` whose `source` is `framework-suite` therefore carries
`missing_validation` beginning `envelope: …`, and its `validation_performed` records only status + latency.

⛔ **Consequence, stated plainly.** §2 of the brief establishes that a rejected PAM request is normally
HTTP 200 with an application-level error in the body. The framework's only positive assertion is
`statusCode == 200`. **A fully rejected request passes every positive test in the suite.** This is not a
theoretical risk — §4 below counts the instances in measured evidence.

### 2.2 The one envelope check that exists reads the wrong field names

`validateApiResponseWithResponseTime_ExcelBasedsettingnegative` (`ApiHelper.java:1425`) does inspect the
envelope, via `validateResponseErrorCode` (`ApiHelper.java:1492`) — but it is wired only to negative
suites, and it reads **camelCase** fields:

- `ApiHelper.java:1498` — `Assert.assertTrue(node.has("success"), "Response body missing 'success' field: " + responseBody)`
- `ApiHelper.java:1500-1503` — `node.path("success")`, `node.get("errorCode")`, `node.get("errorMessage")`, `node.get("message")`

**Measured across all 1,868 captured responses: `success` (lowercase) appears 0 times; `Success`
(PascalCase) appears 1,580 times; 161 bodies carry neither.** Jackson's `has`/`path`/`get` are
case-sensitive, so `ApiHelper.java:1498` fails on **every single response this API produces**. The only
envelope validation in the framework cannot succeed against the API it targets.

⚠️ **Trap confirmed, and the line numbers in the standing docs are stale.** A superseded copy of both
methods sits commented out immediately above the live ones — the dead block is
**`ApiHelper.java:1317-1422`**, with the live definitions at **`:1425`** and **`:1492`**. The root
`CLAUDE.md` and the brief cite "~1282–1394 … live at 1397 and 1464"; those are off by roughly 28–35 lines
against the current file. A grep still hits the dead block first, so the leading-`//` check remains
necessary — just at the corrected offsets.

### 2.3 The harness: seven layers, and what each one actually establishes

Tallies reproduced exactly from `results.json`; they match the brief with no disagreement.

| Layer | Check | PASS | FAIL | What it establishes — and its ceiling |
|---|---|---:|---:|---|
| L1 | `http-status` | 1,688 | 180 | transport reached the app. **Cannot** see an application-level rejection |
| L2 | `content-type` | 1,864 | 4 | body is JSON-typed. Says nothing about its structure |
| L3 | `envelope` | 1,278 | 590 | `Success` flag was found and is true. **Does not** validate `Result` |
| L4 | `message-semantics` | 1,410 | 458 | `Message` was read. Its 705 PASSes are `no Message field on this endpoint - not applicable`, and 134 more PASS on `Message="No HTTP resource was found…"` — i.e. **L4 passes on a 404 error string** |
| L5 | `chain-key-extracted` | 982 | **196** | a chain variable resolved. All 196 failures are the identical `resolved []; MISSING ['NEW_ID']` — no create returned an id |
| L6 | `record-exists` | **2** | **105** | API-side read-back. **Ran on only 107 of 1,873 hops and passed 2** |
| L7 | `latency` | 1,855 | 13 | a response-time budget |

**True pass rate.** 1,688 of 1,868 calls returned HTTP 200 (90.4%), but only **1,200 of 1,868 (64.2%)**
passed every layer that ran on them. The 26-point gap is the exact size of what a status-only assertion
hides. `validation_status` in `positive-validation.json`: 1,200 `PASS`, 668 `FAIL`, 5 `SKIPPED`,
431 `NOT EXECUTED`.

⛔ **Even L1–L7 is not a positive-test contract.** No layer validates a schema, a mandatory field, a data
type, a business rule, database persistence or an audit entry. L6 is an *API* read-back, not a DB read, and
`_AGENT-BRIEF.md` §4 records why no DB assertion has ever run (`db_*` blank in `QA_MsSQL.properties`,
`AutoConfigs.db_type` hardcoded `"mysql"` at `AutoConfigs.java:140`, `DBUtils` with zero callers).

---

## 3. The envelope-shape census — 31 shapes, 25 of them undocumented

Measured over **all 1,868 captured responses**. Two granularities, both in
`artifacts/analysis-data/envelope-shapes.json`.

**Granularity 1 — exact top-level structure (`shape_signature`).** Two calls share a signature only if one
generic parser could treat them identically: same top-level JSON type, same top-level key set, and same
type for `Result`.

> ### 31 distinct response shapes occur across 1,868 calls.
> **6** correspond to a shape documented before this session. **25 do not.**
> The Confluence export documents **1** response shape (`_AGENT-BRIEF.md` §5).

| Calls | Shape signature | Previously documented |
|---:|---|---|
| 677 | `object{DateTime,Program,Result,Success,Version}` + `Result:array` | ✅ S2 (no `Message`) |
| 467 | `object{DateTime,Message,Program,Result,Success,Version}` + `Result:array` | ✅ S1 |
| 269 | `object{DateTime,ErrorCode,ErrorMessage,Program,Success,Version}` + no `Result` | ✅ S5 (error on HTTP 200) |
| 158 | `object{Message}` + no `Result` | ⛔ NOT DOCUMENTED — bare ASP.NET error body |
| 114 | `bare-string (text/plain payload)` | ⛔ NOT DOCUMENTED |
| 47 | `object{DateTime,Message,Program,Result,Success,Version}` + **`Result:str`** | ⛔ NOT DOCUMENTED |
| 29 | `object{DateTime,ErrorCode,ErrorMessage,Program,Result,Success,Version}` + **`Result:bool`** | ⛔ NOT DOCUMENTED |
| 22 | `object{DateTime,Message,Program,Result,Success,Version}` + `Result:object` | ✅ S3 |
| 11 | `object{DateTime,ErrorCode,ErrorMessage,Program,Result,Success,Version}` + `Result:object` | ⛔ NOT DOCUMENTED |
| 10 | `object{DateTime,Message,Program,Success,Version}` + no `Result` | ⛔ NOT DOCUMENTED |
| 8 | `object{DateTime,Program,Result,Success,Version}` + `Result:object` | ✅ S3 |
| 7 | `object{DateTime,Program,Result,Success,Version}` + **`Result:str`** | ⛔ NOT DOCUMENTED |
| 7 | `object{DateTime,ErrorCode,ErrorMessage,Program,Result,Success,Version}` + `Result:array` | ⛔ NOT DOCUMENTED |
| 6 | `empty-string` | ⛔ NOT DOCUMENTED |
| 5 | `bare-array(of objects)` | ✅ S4 |
| 3 | `object{DateTime,ErrorCode,Program,Success,Version}` + no `Result` (**`ErrorCode` without `ErrorMessage`**) | ⛔ NOT DOCUMENTED |
| 3 | `object{DateTime,ErrorCode,ErrorMessage,Program,Result,Success,Version}` + **`Result:int`** | ⛔ NOT DOCUMENTED |
| 3 | `object{DateTime,Message,Program,Result,Success,Version}` + **`Result:bool`** | ⛔ NOT DOCUMENTED |
| 3 | `object{DateTime,Program,Success,Version}` + no `Result` (**no `Message`, no `Result`**) | ⛔ NOT DOCUMENTED |
| 3 | `object{DateTime,ErrorMessage,Program,Result,Success,Version}` + `Result:object` (**`ErrorMessage` without `ErrorCode`**) | ⛔ NOT DOCUMENTED |
| 3 | `object{ErrorCode,ErrorMessage,Success}` + no `Result` (**no `Program`/`Version`/`DateTime`**) | ⛔ NOT DOCUMENTED |
| 2 | **`bare-boolean`** — a naked `true` / `false` as the entire body | ⛔ NOT DOCUMENTED |
| 2 | `object{DateTime,Message,Program,Result,Success,Version}` + `Result:int` | ⛔ NOT DOCUMENTED |
| 2 | `object{DateTime,Program,Result,Success,Version}` + `Result:bool` | ⛔ NOT DOCUMENTED |
| 1 each (8 shapes) | `object{DateTime,ErrorMessage,Message,Program,Result,Success,Version}`+`Result:bool` · `object{Detail,Status,schemas}` · `object{DateTime,ErrorMessage,Program,Success,Version}` · **`object{aaData,aaData1,aaData11}`** · `object{DateTime,Program,Result,Success,Version}`+`Result:int` · `object{DateTime,ErrorCode,ErrorMessage,Message,Program,Result,Success,Version}`+`Result:array` · **`object{Output}`** | ⛔ NOT DOCUMENTED |

**Granularity 2 — the `PamEnvelope.Shape` classification.** The census reimplements
`com.arcon.utils.validation.PamEnvelope.of(String)` in Python (`pam_envelope_shape()` in the extractor) so
the count measures exactly what the new class will see at runtime.

> **All 8 `PamEnvelope.Shape` classes occur in the evidence. None is speculative.**

| `PamEnvelope.Shape` | Calls | % of 1,868 |
|---|---:|---:|
| `ENVELOPE_RESULT_ARRAY` | 1,144 | 61.24 |
| `ENVELOPE_ERROR` | 331 | 17.72 |
| `ENVELOPE_NO_RESULT` | 171 | 9.15 |
| `NOT_JSON` | 114 | 6.10 |
| `ENVELOPE_RESULT_OBJECT` | 92 | 4.93 |
| `EMPTY` | 6 | 0.32 |
| `BARE_ARRAY` | 5 | 0.27 |
| `BARE_OBJECT` | 5 | 0.27 |

### 3.1 Why 31 shapes defeats generic assertion

| Assumption a generic assertion would make | Calls that break it |
|---|---:|
| the body is JSON | **120** (114 non-JSON text + 6 empty) |
| the body is a JSON object | **127** (120 above + 5 bare arrays + 2 bare booleans) |
| a `Success` field exists | **288** (absent from 161 objects; a further 127 are not objects at all) |
| `Result` is an array when present | **139** of the 1,291 with a `Result` — typed `object` (44), `str` (54), `bool` (35) or `int` (6) |
| `Success:false` implies `ErrorCode` is set | **5** |
| `ErrorCode` implies `ErrorMessage` | **3** (`ErrorCode` alone); and **5** carry `ErrorMessage` with no `ErrorCode` |
| `Program`/`Version`/`DateTime` frame every response | **291** |
| field names are camelCase (what `ApiHelper.java:1498` reads) | **1,868 — all of them** |

An assertion hard-coded to any single shape is wrong on between 3 and 1,868 calls. This is the measured
justification for normalising through `PamEnvelope` rather than reading fields off a `JsonNode`: 31
structures collapse to 8 handled classes, and the reader stops needing to know which of the 31 it got.

---

## 4. `Success: true` that wrote nothing — 70 measured instances

**A status-and-flag assertion is unsound on this API.** Every call in this section returned **HTTP 200**,
and all but one carried **`Success: true`** — so both the framework's assertion (`status == 200`,
`ApiHelper.java:1273`) and the strongest thing the harness did (L3 `Success=True`) pass on all of them,
while the response text says nothing was written or nothing was found.

Full register: `artifacts/analysis-data/_a2-false-success.json`. Each is also flagged in-row in
`positive-validation.json` as `remarks` starting `FALSE-SUCCESS[<category>]`.

| Category | Count | What the green signal hides |
|---|---:|---|
| **A — `Already Exists`** | **6** | `Success:true` + `Message` says the record already existed. **Nothing was inserted** |
| B — write no-op | 0 | (subsumed by A and F) |
| **C — success with a validation error** | **4** | `Success:true` while `Message` reports a **rejected input** |
| **D — bare `false`** | **1** | HTTP 200, body is the naked literal `false`. No envelope, no flag, no message |
| **E — success with no data** | **48** | `Success:true` + `No Record Found` / `0 Records Found` — a read that returned nothing |
| **F — silent write** | **11** | write endpoint, `Success:true`, **no `Message` and no `Result`** — nothing in the response evidences a write |
| **Total** | **70** | 3.7% of all 1,868 calls |

⛔ **The seven-layer harness green-lit 56 of the 70.** Cross-referencing each instance against its own
`validation_performed` string:

| Category | Caught by L4 `message-semantics` | Passed **every** layer that ran |
|---|---:|---:|
| A — `Already Exists` | 2 | **4** |
| C — success with a validation error | 0 | **4** |
| D — bare `false` | 1 | 0 |
| E — success with no data | 0 | **48** |
| F — silent write | 11 | 0 |
| **Total** | **14** | **56** |

So the ranking is: the framework catches **0 of 70** (it never reads the body); the harness's L1–L7 catches
**14 of 70**; and **56 calls return HTTP 200 with `Success: true` and pass every check that was applied to
them** while the response text says nothing was written or nothing was found. L4 caught the two
`SetUserDetails` creates but not the four read-side `Already Exists` cases, and it caught none of the 48
`No Record Found` reads. **Message-semantics classification has to be role-aware and pattern-based, not a
per-endpoint allowlist.**

### 4.1 Category A — the named trap, all six instances

| Endpoint | Role | Flow · hop | `Message` | Evidence |
|---|---|---|---|---|
| `UserDetails/SetUserDetails` | create | `userdetails__setuserdetails` · 4 | `Already Exists` | `361_userdetails__setuserdetails_SetUserDetails.json` |
| `UserDetailsV3/SetUserDetails` | create | `userdetailsv3__setuserdetails` · 4 | `Already Exists` | `425_userdetailsv3__setuserdetails_SetUserDetails.json` |
| `ADbridging/validateUserRoleMappingDetails` | read | `adbridging__saveuserrolemappingdetails` · 5 | `Record Already Exists.` | `44_adbridging__saveuserrolemappingdetails_validateUserRoleMappingDetails__verify.json` |
| `ADbridgingV2/validateUserRoleMappingDetails` | read | `adbridgingv2__saveuserrolemappingdetails` · 5 | `Record Already Exists.` | `73_adbridgingv2__saveuserrolemappingdetails_validateUserRoleMappingDetails__verify.json` |
| `ADbridging/CheckRulesOnMappingID` | read | `adbridging__reads_1` · 10 | `Already Exists` | `499_adbridging__reads_1_CheckRulesOnMappingID.json` |
| `ADbridgingV2/CheckRulesOnMappingID` | read | `adbridgingv2__reads_1` · 12 | `Already Exists` | `519_adbridgingv2__reads_1_CheckRulesOnMappingID.json` |

⚠️ The brief names `POST /api/ServiceCreation/SetServiceDetails` as the exemplar. In **this** evidence base
the two `SetUserDetails` variants are the measured create instances; the `Message` string is not uniform
(`Already Exists` vs `Record Already Exists.`), so a semantic assertion must match a pattern, not a literal.

Note the second row of the `SetUserDetails` body: `Result: [{"UserId": 0, …}]` — `Success: true`,
`Message: "Already Exists"`, and the returned identifier is **`0`**. That single response defeats a status
check, a `Success` check, and a "`Result` is non-empty" check simultaneously. Only the `Message` semantics
and the `UserId == 0` sentinel reveal that no user was created — and the four read-side instances in the
table above passed **every** harness layer.

### 4.2 Category C — `Success: true` while the input was rejected

All four are `GetSecretKey`, one per `UserDetails` version, each returning **HTTP 200 · `Success:true` ·
`Message: "Invalid userId format."`**: `UserDetails/GetSecretKey`
(`1213_userdetails__reads_4_GetSecretKey.json`), `UserDetailsV2/GetSecretKey`
(`1240_…`), `UserDetailsV3/GetSecretKey` (`1290_…`), `UserDetailsV4/GetSecretKey` (`1329_…`). The API
signals both "succeeded" and "your input was invalid" in the same body. Note the harness's own L4 counted
these as PASS — reading the `Message` is not enough; its **semantics** must be classified.

### 4.3 Category D — a write that reports failure with no envelope at all

`ActivityLogs/InsertPsrBulkLogs` · flow `activitylogs__insertpsrbulklogs` hop 4 ·
`105_activitylogs__insertpsrbulklogs_InsertPsrBulkLogs.json` — **HTTP 200, body `false`.** There is no
`Success` field to read and no `Message`; the only signal that the bulk insert failed is the literal body.
Its sibling `FileServerDetail/InsertUploadedFileDetails` returns a bare `true` on the same shape, so the
boolean is meaningful — and unreachable by any assertion the framework currently has.

### 4.4 Category F — creates that evidence nothing

Eleven `create`-role endpoints returned `Success:true` with **no `Message` and no `Result`**:
`ActivityLogs/InsertSSMLogsNew`, `ActivityLogs/SaveSSMLogs`,
`ServiceDetails|V2|V3/SetRelativePath`, `ServiceDetails|V2|V3/SetVideoFileName`,
`UIAutomationData/InsertFileImagebyServiceId`, `UIAutomationData/InsertImagebyServiceId`,
`UIAutomationData/SaveUIAutomationDetails`. This is the same root cause as the **196 identical L5 failures**
(`resolved []; MISSING ['NEW_ID']`): PAM creates do not return the identifier they created, so neither a
chain nor an assertion can prove the write happened. It is also why **L6 ran on only 107 hops and passed 2**.

---

## 5. Per-endpoint: validated vs. should be validated

Every row carries `missing_validation` — the specific checks an industry-standard positive assertion would
make that were **not** made — computed from the endpoint's `role` (read / create / update / teardown /
other) minus the layers that actually ran. `missing_validation_count` gives the size of the gap.

| `missing_validation_count` | Rows | Who they are |
|---:|---:|---|
| 8 | 1,648 | executed reads — L1–L4 + L7 ran, so `http-status`, `content-type`, `envelope`, `message-semantics`, `latency` are satisfied |
| 10 | 220 | executed writes — same, plus `read-back` where L6 ran |
| 12 | 275 | `framework-suite` rows — only `http-status` and `latency` are satisfied |
| 14 | 124 | never-executed reads |
| 15 | 37 | never-executed writes — the widest gap in the catalogue |

**Never checked anywhere, for any of the 1,306 endpoints** — no row in this dataset is missing these from
its `missing_validation` list:

| Code | What is absent | Why it is absent |
|---|---|---|
| `schema` | response structure against a contract | no OpenAPI/Swagger covers this surface; the 37 Swagger specs describe a different one (~6% name overlap) |
| `mandatory-fields` | documented required response fields present and non-null | 3 `[Required]` properties across ~6,738 (`_AGENT-BRIEF.md` §5) |
| `field-types` | types, formats, ranges, enumerations | no length, format or pattern validation exists anywhere |
| `business-rules` | ownership, LOB scoping, state machine, referential integrity | never expressed as an assertion |
| `authorization` | response respects the caller's role and LOB scope | one bearer token, one identity, no role matrix |
| `error-code-domain` | `ErrorCode` against a complete known set | `KNOWN_ERROR_CODES = {"201","202","203"}` at `ApiHelper.java:1423` is incomplete — a live run captured `206-LC_GLD` |
| `persistence` · `audit` | the write reached a table; the action left an audit entry | `db_*` blank in `QA_MsSQL.properties`; `AutoConfigs.db_type` hardcoded `"mysql"` (`AutoConfigs.java:140`); `DBUtils` has zero callers |
| `idempotency` | re-invocation behaviour on writes | never attempted; the destructive-replay guard forbids it without a teardown story |
| `result-cardinality` · `pagination` | `Result` row count vs the `Message` count; paging/sorting/filtering | 319 calls returned `Message: "687 Records Found"` and no assertion compared 687 to `len(Result)` |

### 5.1 How to read a row

`positive-validation.json` — one JSON array, flat scalar values only (workbook-safe). Beyond the contracted
keys, five flattened helpers are provided so the workbook build need not re-parse `actual_response`:
`role`, `evidence_file`, `pam_envelope_shape`, `success_flag`, `message`, `error_code`, `result_type`,
`result_count`, `layers_run`, `layers_passed`, `missing_validation_count`.

| Key | Contents when measured | Contents when not |
|---|---|---|
| `source` | `both` · `harness-run` | `framework-suite` · `neither` |
| `payload` | exact request body sent, or `NONE (GET)`, or `{} (empty body sent)` | Excel `Payload` cell, or `NOT EXECUTED - no evidence` |
| `expected_response` | `HTTP 200; body contract: NOT DOCUMENTED - no OpenAPI/Swagger covers this endpoint (source-map sources=…)` | Excel `ExpectedStatus`, or `NOT EXECUTED - no evidence` |
| `actual_response` | `shape=… \| PamEnvelope.Shape=… \| Success=… \| Message=… \| ErrorCode=… \| Result=type(count) \| body=<400 chars>` | `NOT EXECUTED - no evidence` |
| `validation_performed` | `L1 http-status=PASS [expected 200, got 200]; L2 …` — only the layers that ran, with their detail strings | the framework's status+latency statement, or `NONE - no harness hop and no framework positive test` |
| `validation_status` | `PASS - all N layers passed` · `FAIL - L3,L4` | `SKIPPED - destructive teardown withheld` · `NOT EXECUTED - no evidence` |

⚠️ **`expected_response` is `NOT DOCUMENTED` for the whole catalogue.** 697 of 1,306 endpoints have no
documentation source at all in `source-map.json`; the remaining 609 have Confluence request payloads bound
**by page proximity** and **1** documented response shape. There is no artifact in this workspace that
states what a correct response *should* contain — which is why every `missing_validation` list opens with
`schema`. That is the finding, not a limitation of this extraction.

---

## 6. Disagreements with the brief

**Every authoritative tally in `_AGENT-BRIEF.md` reproduced exactly** — 1,306 endpoints, 326 flows,
1,873 hops, 1,868 calls, 870 endpoints exercised, and all fourteen L1–L7 PASS/FAIL figures. The extractor
asserts each one and would have printed a disagreement block; it printed none.

Four additions and corrections, none of which overturn a brief figure:

| # | Item | Detail |
|---:|---|---|
| 1 | **`ApiHelper` line numbers are stale in the standing docs** | Dead block is `ApiHelper.java:1317-1422`; live definitions at `:1425` and `:1492`. Root `CLAUDE.md` and the brief cite ~1282–1394 / 1397 / 1464 — off by ~28–35 lines. The trap itself is real and confirmed |
| 2 | **Five shapes documented, 31 measured** | Not a contradiction — the brief's five are all present. But the Confluence "1 of 9 response shapes" understates the problem: the real figure is **31 structural signatures**, of which 25 were undocumented |
| 3 | **`APIConfig.java` yields 1,308 distinct `Controller/Action`, not 1,306** | The two extra are `AzureKeyVault/GetDatabaseStatus` — a real endpoint dropped from the canonical count by a **double-slash typo at `APIConfig.java:188`** (`"//api/AzureKeyVault/GetDatabaseStatus"`) — and `User/`, the SCIM collection root `/api/User` declared three times for GET/POST/PUT. **1,306 is retained** as the canonical figure; these are catalogue defects, not a recount |
| 4 | **The `Already Exists` exemplar differs in this evidence base** | The brief cites `ServiceCreation/SetServiceDetails`; the measured create instances here are `UserDetails/SetUserDetails` and `UserDetailsV3/SetUserDetails`. Both statements can hold — they are different runs. A semantic assertion must pattern-match, since the string varies (`Already Exists` vs `Record Already Exists.`) |

---

## 7. Reproduction

```powershell
python tools\obj007_positive_analysis.py
```

Zero HTTP requests, zero DB queries, no network access. Reads only `source-map.json`, `APIConfig.java`,
`ApiHelper.java`, `API_DataProviderUtils.java`, the 71 `Positive_All` suite XMLs, the 79 test classes,
`testdata/API_Automation_Test_Input_Data.xls`, `artifacts/runs/2026-07-29_181439/results.json` and its 1,868
evidence files. Writes only into `data/analysis/`. Requires `xlrd` for the `.xls` test data.

The script self-checks every figure in `_AGENT-BRIEF.md` §3 and §5 and prints a
`!! DISAGREEMENT WITH docs/history/archive/document-agent-brief.md` block rather than silently overwriting a brief tally.
