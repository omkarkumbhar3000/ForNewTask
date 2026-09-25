# Developer Brief — API Implementation Findings

**For:** the PAM development team · **From:** QA automation, from dynamic API integration work
**Basis:** two measured runs — **1,868 live API calls** across **870 endpoints** (`2026-07-29_181439`) and
**5,416 calls** across **1,388 endpoints** (`2026-08-05_114315`, OBJ-010) — plus static analysis of
`APIConfig.java`, the 66 payload helpers, `pam/PAM` (6,866 `.cs` files), and the 2,470-page Confluence
API reference. Every item below is measured, with an evidence file per call.
**Tone note:** these are engineering observations, not criticism. Several are historical accretion rather
than anyone's decision. They are listed because each one costs test reliability today.
**Findings:** 13 · **Last updated:** 2026-08-05 (added §13, corrected §5 against the newer run)

---

## 0. Priority summary

| # | Finding | Severity | Effort to fix |
|---:|---|---|---|
| 1 | HTTP 200 returned for application-level failures | 🔴 Critical | Medium |
| 2 | `Success: true` returned when nothing was created | 🔴 Critical | Low |
| 3 | **31** different response shapes on one API | 🔴 High | Medium |
| 4 | Error-code register incomplete and undocumented | 🔴 High | Low |
| 5 | **348 of 1,388** endpoints exercised return 404 | 🟠 Medium | Low |
| 6 | Mutation exposed over HTTP GET | 🟠 Medium | Medium |
| 7 | Field naming and types inconsistent across controllers | 🟠 Medium | High |
| 8 | Two endpoints stop the IIS application pool | 🔴 Critical | Medium |
| 9 | Service passwords returned in cleartext | 🟠 Review | Low |
| 10 | No validation attributes on request models | 🟠 Medium | High |
| 11 | Internal errors leaked in messages | 🟡 Low | Low |
| 12 | Endpoints return unfiltered full datasets | 🟡 Low | Medium |
| **13** | **An invalid auth token is accepted — HTTP 200, data returned, writes reachable** | 🔴 **Critical** | Medium |

---

## 1. 🔴 HTTP 200 for application-level failures

**Measured: 1,688 of 1,868 calls returned HTTP 200. Of those, 289 carried `Success: false`.**

```json
HTTP/1.1 200 OK
{ "Success": false, "ErrorCode": "902-ALC-ISSML", "ErrorMessage": "System error has occurred" }
```

**Why it matters:** any client — our tests, a UI, a partner integration — that checks the status code will
treat a hard failure as a success. A status-only test suite scored this run **90% green**; the true figure
is 64%.

**Ask:** use status codes semantically. `400` for a bad request, `401`/`403` for auth, `500` for a server
fault. If the envelope must stay for backward compatibility, at minimum make the status code agree with it.

---

## 2. 🔴 `Success: true` when nothing was created

`POST /api/ServiceCreation/SetServiceDetails` with an existing record returns:

```json
{ "Success": true, "Message": "Already Exists", "Result": [ { "ServiceId": "25338", ... } ] }
```

**Nothing was inserted, yet both the status code and the success flag are green.** The only way to know is
to parse the human-readable `Message` string. That makes correctness depend on English prose.

**Ask:** either return `201 Created` vs `200 OK`/`409 Conflict`, or add a machine-readable field
(`"created": true|false`). Do not require clients to string-match `"Inserted Successfully"` versus
`"Already Exists"`.

---

## 3. 🔴 31 response shapes on one API

**A full structural census of all 1,868 captured responses counts 31 distinct top-level shapes. Only 6 of
them match a shape documented anywhere.** The eight families below are the readable exemplars — they are
what a developer needs to recognise — but they are families, not the total. The complete census is
`artifacts/analysis-data/envelope-shapes.json`.

What defeats a fixed-shape client, with counts: **127** responses are not JSON objects at all · **288**
carry no `Success` field · **139** of 1,291 `Result` values are not arrays (object, string, bool, int) ·
**2** bodies are a naked `true`/`false` · **291** lack the `Program`/`Version`/`DateTime` frame.

| # | Shape family | Example endpoint |
|---:|---|---|
| 1 | `{Program, Version, DateTime, Success, Message, Result[]}` | `GetAllActiveUserList` |
| 2 | Same, but **no `Message`** | `GetLOBList` |
| 3 | Same, but `Result` is an **object**, not an array | `GetServiceDetails` |
| 4 | **Bare array**, no envelope | `GET /api/DeviceOnboarding/GetLOBList` |
| 5 | `{Success:false, ErrorCode, ErrorMessage}` at HTTP 200 | `InsertSSMLogs` |
| 6 | `{aaData, aaData1, aaData11}` — DataTables-shaped | `GetAccessControlLogs` |
| 7 | `{"Output": "1\|Parameter error occurred - ..."}` — error inside a delimited string | `SetPAMUserDetails` |
| 8 | Bare `false` boolean, or bare `""`, as the entire body | `InsertPsrBulkLogs` |

**Shapes 1 and 4 return the same LOB data** — one wrapped, one not. Shape 7 is the worst: the error is a
pipe-delimited string inside a JSON field, so a client must parse a string to find out it failed.

**Ask:** converge on one envelope. If that is too large a change, publish which endpoints use which shape,
and stop adding new ones. Shape 6 is a UI grid format leaking into an API contract.

**What this cost us.** Absorbing 31 shapes took a dedicated normalisation class
(`com.arcon.utils.validation.PamEnvelope`) before any assertion could be written at all. Field **casing**
also varies, and that turned out to be more than cosmetic: the framework's own envelope assertion read
`success` in camelCase, and across all 1,868 responses lowercase `success` appears in **0** while PascalCase
`Success` appears in **1,580** — so that assertion could never pass, and the body-validation layer had zero
real coverage while appearing to exist. One inconsistent letter silently disabled a whole validation layer.

---

## 4. 🔴 Error-code register incomplete

Our framework recognises `{201, 202, 203}`. Live traffic returned codes outside that set:

| Observed | Meaning | HTTP status |
|---|---|---|
| `902-ALC-ISSML` | `System error has occurred` | 200 |
| `206-LC_GLD` | `Parameter error occurred - Required property 'LogTypeId' not found` | 200 |

The 2,470-page Confluence reference documents **four** error codes in total.

**Ask:** publish a complete register — code, meaning, emitting endpoints, corrective action. This is the
single highest-value documentation change available and it unblocks automated negative testing entirely.

---

## 5. 🟠 348 of 1,388 endpoints exercised return 404

⚠️ **This finding was previously stated as "135 declared endpoints return 404". That figure was correct for
the run it came from and is now superseded by a wider measurement.** Both are kept so the history is
auditable:

| Basis | Endpoints returning 404 | Of endpoints exercised |
|---|---:|---:|
| `2026-07-29_181439` — 1,868 calls | **135** | 870 (15.5%) |
| **`2026-08-05_114315` — 5,416 calls** | **348** | **1,388 (25.1%)** |

The newer run reached 518 more endpoints, so it found proportionally more that are not served. **Quote
348 / 1,388 (25.1%)**; quote 135 only when citing the earlier run specifically.

Concentrated by module — 780 individual calls hit a 404:

| Module | Calls returning 404 |
|---|---:|
| `ServiceDetailsV2` | 129 |
| `ServiceDetails` | 120 |
| `ServiceDetailsV3` | 117 |
| `WebSM-Service` | 86 |
| `Collaborations` | 38 |
| `Access Control` | 36 |

This is also the largest single cause of apparent test failure: **340 of the 872** failures in the
positive data-parity dimension are 404s, not defects. Excluding endpoints that are simply not deployed,
that dimension scores **47.6%** rather than 35.6%.

Separately, only **132 of 1,306** catalogue actions appear as a method anywhere in `pam/PAM`, and **58 of
70** catalogue controllers have no corresponding `*Controller.cs` file in that snapshot.

Three sources disagree about what the API is: the test catalogue (1,306 endpoints), the shared Swagger specs
(690 operations, **~6% name overlap**), and the product snapshot.

**Ask:** confirm which endpoints are live per deployment, and which are deprecated. A route dump per build
would settle it permanently — and would let QA stop reporting 340 deployment gaps as test failures.

---

## 6. 🟠 Mutation exposed over HTTP GET

`SetStatus` is declared as **GET** on 49 controllers. `GetLogDetails` accepts a `LogTypeId` that changes what
is read. A name beginning `Set` served over GET is a state change over a safe verb.

Consequence for us: **verb-based safety guards are useless on this API.** Deletion is also expressed as
`POST /api/<Controller>/Delete<Thing>` rather than HTTP DELETE — the whole API declares only **2 PUT and
2 DELETE** endpoints against 992 POST and 325 GET. We guard on action **names** instead.

**Ask:** GET must be safe and idempotent. Move state changes to POST. This also matters for caching,
proxies, prefetch and browser retries.

---

## 7. 🟠 Field naming and types inconsistent

| Concept | Spellings observed |
|---|---|
| LOB identifier | `LobId` · `LOBID` · `LOBid` · `LobsId` |
| User identifier | `UserId` · `UserID` · `userid` |
| Service identifier | `ServiceId` — **string on create, integer on read** |

Also observed: `UserName` and `UserDisplayName` are silently **upper-cased** on write (`DemoUser` →
`DEMOUSER`), so a client that reads back what it wrote sees different data.

Our tooling compensates with case-insensitive matching and explicit casts. That is a workaround for a
contract problem.

**Ask:** a canonical field-name and type register, applied to new endpoints at minimum. Keep an id's type
stable across operations.

---

## 8. 🔴 Two endpoints stop the IIS application pool

`GetLogs` and `GetErrorLogs` (present on ~98 controller/version combinations) **hang for 30 seconds and
stop the application pool.** This took the QA environment down for a day. They are permanently blocklisted
in our harness, which means they are also permanently **untested**.

**Ask:** treat as a production-severity defect. An unauthenticated-reachable endpoint that halts the app
pool is a denial-of-service vector, not just a test problem.

---

## 9. 🟠 Service passwords returned in cleartext — please confirm intent

`POST /api/ServiceDetails/GetServiceDetails` returns:

```json
{ "Result": { "ServiceUsername": "UserName1", "ServicePassword": "NewPassword", ... } }
```

For a privileged-access-management product this warrants explicit confirmation. We understand the session
launcher may legitimately need it. Our harness redacts the field before writing evidence to disk.

**Ask:** confirm this is intended and access-controlled. If it is required, consider a
single-use/time-boxed token instead of the standing password, and confirm these responses are excluded from
logs.

---

## 10. 🟠 Request models carry almost no validation metadata

Scanned all **6,866 `.cs` files** in `pam/PAM`: **5,994 public classes** and **6,738 auto-properties**, but
only:

| Attribute | Occurrences |
|---|---:|
| `[Required]` | **3** |
| `[JsonProperty]` | 11 |
| `[DataMember]` | 4 |
| `[Range]` · `[StringLength]` · `[MaxLength]` · `[MinLength]` · `[RegularExpression]` · `Required.Always` | **0 each** |

⚠️ **Three figures in an earlier version of this table were wrong and are corrected above** — classes were
stated as 5,262, `[Range]` as 5 and `[JsonProperty]` as 7. Re-measured: **5,994**, **0** and **11**. The
headline `[Required]` = 3 and 6,738 auto-properties both reproduce exactly.

**The material correction, and it sharpens the finding rather than softening it.** 6,738 is the whole .NET
product, but `pam/PAM` implements only 48 of 1,306 endpoints. All three `[Required]` attributes sit on a
single class — `ProvisioningService/.../Entity.cs`, class `Request` (`targetHostType`, `rootUser`,
`rootpass`) — and there is no `Provisioning*` controller among the 70 under test. Those three property names
appear in **0 of 5,940** properties mapped to an endpoint. So **on the API surface actually under test the
declared-required count is 0 of 5,175, not 3 of 6,738.**

**The zero on `Required.Always` is the most informative number here.** The server demonstrably *does* run
Newtonsoft's required check — 123 rejections of that exact form were observed live. So the enforcing models
exist; they are simply not in the repository supplied. Corroboration from a third direction: **102 of 102**
archived Swagger-validated operations record "schema declares no required properties".

**Consequence:** nothing — not a client, not a generator, not a new developer — can determine which fields
are mandatory without calling the endpoint and reading the error prose. And that prose is not a contract:
across **126** endpoints it names **37** field names in **5** grammars and **41** distinct messages, with
the names not canonical (`UserId`/`UserID`/`UsrId`, `LOBId`/`LOBID`, `ServiceId`/`ServiceID`/`Service_ID`).
**185 of 217 create endpoints (85.3%) have no mandatory-field signal of any kind**, and **0 of 1,245** create
body properties carry a max-length, format or pattern. This is the direct cause of our worst number: **only
13 of 217 create endpoints can be driven successfully.**

It also removes the means of diagnosis, not just the means of construction: of 213 creates called, the server
named a missing property in **31** cases and stated **no cause in 150**.

**Ask:** annotate request models with `[Required]` and length/range constraints, starting with the most-used
create endpoints. This is the highest-leverage change for API usability, and it enables model-driven
validation server-side too. Where the enforcing models live outside `pam/PAM`, tell us where — that alone
unblocks a large amount of this.

---

## 11. 🟡 Internal detail leaked in error messages

```
"Parameter error occurred.-Required property 'LogTypeId' not found in JSON. Path '', line 1, position 2."
```

That is a serialiser exception surfaced to the caller — it leaks the parsing library's internals and the
input position. Useful in development, inadvisable externally.

**Ask:** return a stable code plus a safe message; keep the stack detail in server logs.

---

## 12. 🟡 Unfiltered full datasets

`GET /api/UserDetails/GetAllActiveUserList` returns **1.13 MB / ~47,400 lines** with **no filter or paging
parameter**. Any client wanting one user must download every user and filter locally. It grows with the user
population — and its sibling `GetAllActiveUserDetails` already hangs (§8).

**Ask:** add filter and paging parameters to the "GetAll…" family.

---

## 13. 🔴 An invalid authentication token is accepted — HTTP 200, data returned, writes reachable

**Measured on `2026-08-05_114315`. 57 endpoints answered HTTP 200 to a request carrying a deliberately
invalid bearer token.** The credential presented was the literal string
`Bearer invalid.token.obj010-unauthorized-probe` — no real credential was used, and `/arcontoken` was never
called.

| Class | Endpoints | Assessment |
|---|---:|---|
| `GetStatus` / `GetDatabaseStatus` health probes | 34 | 🟡 anonymous 200 is plausibly intentional |
| `ClientAuth` / `RegisterClient` (RDPS, `v1.0`) | 4 | 🟡 client bootstrap, plausibly intentional |
| **In scope for this finding** | **19** | ⛔ of which **6 are writes** and **8 returned business data** |

**What came back.** Verbatim from the retained evidence:

```
GET /api/FileDetails/GetFileSharedData
Authorization: Bearer invalid.token.obj010-unauthorized-probe

HTTP/1.1 200 OK
[{"OwnerUser":"RUSHI","SharedFileId":"35","SharedFileName":"User.txt",
  "SharedWith":"RUSHIKESH","SharedWithUserId":"49","SharedWithUserDomain":"ARCOSAUTH"}]
```

| Endpoint | Disclosed to an unauthenticated caller |
|---|---|
| `/api/Lob/Get` | **6,856 bytes** of LOB configuration |
| `/api/FileDetails/GetDetailsOfFilesOnFileServer` (+`WithCreatorAndDomain`) | File name, size, **content**, creator `Admin` |
| `/api/FileDetails/GetFileSharedData` | Real usernames, domain `ARCOSAUTH`, shared file ids |
| `/api/Encryption/GetAESEncryptedText` | A working encryption oracle |

**Write operations reachable with no valid credential** — the most serious entries:

- `/api/DualFactor/UpdateMobileOTPRegistrationDetails`
- `/api/FileServerDetail/InsertFileServerConfiguration`
- `/api/FileServerDetail/UpdateFileUploadConfiguration`
- `/api/FileDetails/UpdateDatabaseAfterDeletionOfFilesOnFileServer` (+`ByUser`)

⚠️ **Why no existing test caught this, and this part matters.** The suite already contains **1,153**
`*_UnauthorizedAccess` cases asserting HTTP 401. Those Excel rows carry **no token column**, and the test
class sends **the same valid token as every other test** — so the assertion can never exercise unauthorized
access. With a valid credential the endpoint answers 200 and the test simply fails; it could only ever
"pass" if the shared `ApiToken` happened to be expired, which is passing for the wrong reason. **1,153 test
cases were providing no assurance at all.** The dynamic framework now sends an invalid credential for
exactly those rows, which is what surfaced this.

**Ask:** make the authorization filter global and opt-out so no controller can be anonymous by omission;
reject a malformed or unverifiable bearer with 401 before any handler runs; publish an explicit allow-list
of the endpoints intended to be anonymous. And add a credential column to those 1,153 rows so the suite can
hold the line itself.

⛔ **Not replayed, deliberately.** Six of the in-scope endpoints are writes. Re-issuing them
unauthenticated to demonstrate the point would itself write to QA with no credential. The captured evidence
is decisive: `artifacts/loopholes/LH-13-endpoints-accept-invalid-auth-token/`.

---

## 14. Also observed — smaller items

| Item | Detail |
|---|---|
| Dead code in the test framework | ~246 commented-out lines in `ApiHelper`, plus a superseded copy of `validateResponseErrorCode` sitting directly above the live one |
| `APIConfigOld.java` still present | Duplicate endpoint constants, unused |
| Typo in a constant name | `Se0rviceDetailsV3` |
| Credentials in plaintext | All 20 `Environments/*.properties` files |
| No Swagger anywhere in `pam/PAM` | **0** files named `swagger`/`openapi` across 181 projects |
| Routing style is mixed | 105 `[Route(...)]` attributes and 119 `[Http*]` verb attributes coexist with 7 `App_Start/WebApiConfig.cs` convention templates — so route resolution differs per project |

---

## 15. If only three things get fixed

⚠️ **This ranking changed on 2026-08-05.** §13 did not exist when the original three were chosen, and it
outranks all of them: it is the only finding where an unauthenticated caller both reads business data and
reaches a write.

| Rank | Fix | Why this one |
|---:|---|---|
| **1** | **Reject an invalid bearer token** (§13) | 19 endpoints currently accept one; 6 are writes. Security, not test quality |
| **2** | **`[Required]` on request models** (§10) | Unblocks automated write coverage from 13/217. Largest measurable testing gain |
| **3** | **Publish the error-code register** (§4) | Without it, no client can reliably distinguish success from failure |

Displaced but still recommended: **fix `GetLogs`/`GetErrorLogs`** (§8) — a stability and availability
defect, not merely a testing obstacle.

---

## 16. Evidence

Every claim resolves to a file. Two runs, one evidence file per call, secrets redacted:

```
artifacts/runs/2026-07-29_181439/evidence/<nn>_<flow>_<hop>.json   1,868 files
artifacts/runs/2026-08-05_114315/evidence/<nn>_<flow>_<hop>.json   5,424 files  (OBJ-010)
artifacts/runs/2026-08-05_114315/QA_MsSQL_API_Execution.xlsx       execution + benchmark workbook
docs/management/summary/OBJ-010-Execution-Benchmark.md                   N-1 vs N benchmark
docs/management/summary/Full-Generated-Run-2026-07-29.md                 earlier aggregate figures
docs/findings/issues/                                                  11 formal defect write-ups
docs/briefs/document-gap.md                                        documentation findings
```

Reproduce:

```powershell
python tools\generate_flows.py            # chain flows from APIConfig + payload helpers
python tools\generate_data_flows.py       # negative / positive flows from the Excel corpus
python tools\chain_runner.py --dry-run    # plan only, zero API calls
python tools\chain_runner.py --execute --delay-ms 2000 --allow-verbs GET,POST,PUT,PATCH
python tools\obj010_collect.py artifacts/runs/<stamp>          # validation gate
python tools\obj010_build_workbook.py artifacts/runs/<stamp>   # workbook + benchmark
```
