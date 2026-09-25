# Documentation Gap Analysis — what the PAM API documentation does not say

**Subject:** `data/sources/PAM API (Internal Team).pdf` — 2,470 pages, Confluence export — plus the two
administrator guides (1,101 pp), assessed against the 1,306-endpoint catalogue and 1,868 executed calls.
**Verdict:** 🟡 The export is the **best payload source available and the only one worth investing in** —
and it cannot answer the one question validation depends on: *did this call succeed?*
**Headline:** **912 of 1,306 endpoints (69.8%) undocumented** · **3** error-code values in 2,470 pages ·
**0** pages stating an ordering constraint · **351 of 358** `ErrorCode` examples are `null`.
**Method:** static analysis only. **Zero HTTP requests, zero database queries.** Product docs were read
through the query layer (`tools/rag/query.py`), never by opening the corpus directly.
**Script:** `tools/measure_doc_gap.py` · **Row data:** `artifacts/analysis-data/doc-gap-coverage.json`
(one row per controller, 70 rows) · **Solutions:** `data/analysis/solutions-A6A7.json` (`A7-*`)
**Extends:** `docs/briefs/document-gap.md` and `docs/gaps/01-Data-Gap-Analysis.md` — §9 lists the
figures in those documents that this analysis corrects.

---

## 1. What was measured, and how

One pass over `artifacts/rag-corpus/corpus.jsonl` (the page-cited extraction of the 2,470-page export),
compared against `APIConfig.java` and `tools/source-map.json`.

| Corpus measure | Value |
|---|---:|
| Pages scanned (`pam-api`) | **2,470** |
| Pages naming an `/api/<Controller>/<Action>` route | **1,051** |
| Pages naming only a bare action, no route | 191 |
| Pages naming a route **not in the catalogue** | 62 |
| Distinct routes cited anywhere in the document | **452** |
| JSON objects parsed | **3,194** |
| …bound to an endpoint by page proximity | **1,605** |
| …orphaned — no endpoint near enough to bind | **1,589** |
| JSON blocks that would not parse | 440 |

**Two definitions of "documented" are used deliberately**, because they answer different questions:

| Definition | Measure | Used for |
|---|---:|---|
| **Exact-route** — the literal `/api/<Controller>/<Action>` appears in the export | **394 / 1,306** | `endpoints_documented_confluence` in the JSON. Deterministic and page-citable |
| **Proximity-bound** — a JSON payload sits close enough to be attached to the endpoint | 424 / 1,306 | `payload_examples_available`. A hypothesis, not a contract |

⚠️ Proximity binding is the export's structural weakness, not a tooling choice: the document lists a route
as a heading and the payload beneath it, so **nearness is the only available signal**. Some bindings are
therefore wrong. Anything derived from the 1,605 bound payloads must be treated as a candidate.

---

## 2. Missing information — the four questions the documentation cannot answer

| Question a tester must answer | Documented? | Measure |
|---|---|---:|
| What endpoints exist? | 🟡 Partially | 394 of 1,306 (30.2%) |
| What does a request body look like? | 🟡 Partially | 1,605 payloads, proximity-bound |
| **Which fields are mandatory?** | ⛔ **Not at all** | **0** — no field is marked mandatory anywhere |
| **What does a failure look like?** | ⛔ **Almost not at all** | **3** code values in 2,470 pages |
| **Which HTTP status means what?** | ⛔ **Not at all** | 104 incidental status mentions, no semantics |
| **In what order must calls be made?** | ⛔ **Not at all** | **0 of 2,470 pages** |
| Did a write persist? | ⛔ Not addressable | out of scope for documentation |

The mandatory-field row is the load-bearing one. It is absent from **every** source simultaneously — the
export marks nothing mandatory, and the product declares **3 `[Required]` attributes across 6,738
properties**, none of them on a catalogue endpoint (`A6-developer-repo-analysis.md` §4.1). Mandatory-ness
is currently *inferred* from "appears in every documented example": of 56 such inferred hints in the merged
map, **0 are backed by a declaration**, and only **1 of 217 create endpoints** has even one.

**Consequence for validation:** a generated create body is a guess. 204 of 217 creates fail, and the
failures are overwhelmingly `Validation error occurred - <Field> is Mandatory` and
`Could not convert string to integer` — requirements that exist only in server-side procedural code.

---

## 3. Coverage gaps

### 3.1 The 70% headline

| Measure | Value | Share |
|---|---:|---:|
| Catalogue endpoints | 1,306 | 100% |
| **Documented — exact route present** | **394** | **30.2%** |
| ⛔ **Undocumented** | **912** | **69.8%** |
| Documented routes **not** in the catalogue | 58 of 452 | — |

Controller-level coverage, from `artifacts/analysis-data/doc-gap-coverage.json`:

| Controllers | Count | Meaning |
|---|---:|---|
| With at least one documented page | **52 / 70** | Some documentation exists |
| ⛔ With **no** documented endpoint at all | **18 / 70** | Entirely invisible to documentation |
| With no implementation in `pam/PAM` | 58 / 70 | see `A6` §6 |

**Gap severity distribution** (`gap_severity`, derived from coverage, payload availability and repo presence):

| Severity | Controllers | Endpoints |
|---|---:|---:|
| ⛔ critical | **17** | **410** |
| 🔴 high | 13 | — |
| 🟡 medium | 19 | — |
| ✅ low | 21 | — |

### 3.2 ⛔ The versioned families — the single largest cliff

This is the most important coverage finding in the report, and it was not previously stated.

| Group | Controllers | Endpoints | Documented | In `pam/PAM` | Payload examples |
|---|---:|---:|---:|---:|---:|
| **Versioned (`…V2`/`V3`/`V4`)** | **10** | **562 (43.0%)** | ⛔ **1 (0.2%)** | 1 | 10 |
| Unversioned | 60 | 744 (57.0%) | 393 (52.8%) | 47 | 1,595 |

| Controller | Endpoints | Documented | In repo |
|---|---:|---:|---:|
| `ServiceDetailsV2` | 132 | **0** | 1 |
| `ServiceDetailsV3` | 123 | **0** | 0 |
| `UserDetailsV2` | 72 | 1 | 0 |
| `UserDetailsV4` | 72 | **0** | 0 |
| `UserDetailsV3` | 71 | **0** | 0 |
| `ADbridgingV2` | 33 | **0** | 0 |
| `ServicePasswordV2` | 26 | **0** | 0 |
| `RDPSServiceInsertV2` | 19 | **0** | 0 |
| `UserRegistrationV2` | 13 | **0** | 0 |

**43% of the API surface has one documented endpoint between all of it.** These are not fringe controllers —
`ServiceDetailsV2` and `ServiceDetailsV3` are the two largest in the catalogue. The unversioned originals
*are* documented (`ServiceDetails` 70/126, `UserDetails` 48/72, `ADbridging` 33/34), so the pattern is
clear: **each version bump shipped without documentation, and the documentation still describes v1.**

**Consequence for validation:** the endpoints most likely to be current are the least documented. A tester
following the documentation validates the *superseded* surface.

### 3.3 The catalogue is not a clean baseline either

Documentation cannot be reconciled against a catalogue that itself contains defects. Measured:

| Anomaly | Count | Detail |
|---|---:|---|
| ⛔ Typo'd controller producing a hard 404 | 1 | `/api/Se0rviceDetailsV3/SetServiceSessionLogoutV2` — `APIConfig.java:893` *(supplied)* |
| ⛔ Double-slash typo hiding a real endpoint | 1 | `AzureKeyVault/GetDatabaseStatus` — `APIConfig.java:188` *(supplied)* |
| A version segment parsed as a controller | 3 | `/api/v1.0/GetConfig`, `/RegisterClient`, `/ClientAuth` — `APIConfig.java:496-498` |
| Unsubstituted `{placeholder}` in the declared path | **4** | `/api/Logs/GetAuditLog/{ID}`, `/api/User/{id}`, `/api/User/Details/{id}`, `/api/User/Delete/{id}` |
| Hardcoded environment-specific query strings | **7** | `?filname=5764`, `?LobId=2`, `?TicketId=LAMTest123`, plus 4 literal GUIDs |
| **Endpoints in the positive Excel absent from `APIConfig.java`** | **210** | mostly the SCIM `Service/*` and `User/*` surface *(supplied)* |
| Declared endpoints returning HTTP 404 live | **135** | `results.json` L1 |

`APIConfig.java` yields **1,308** distinct `Controller/Action` pairs; the two extras are the double-slash
`AzureKeyVault/GetDatabaseStatus` and the SCIM root `User/` (declared three times). **1,306 remains the
number to quote.**

**Consequence:** four artefacts disagree about what the API is — catalogue 1,306, documentation 452 routes,
Swagger 690 operations with ~6% name overlap *(prior)*, product snapshot 48 — and **none is authoritative**.
The 210 Excel-only endpoints mean even the test suite's own data files describe a surface the catalogue does
not declare.

---

## 4. Missing response models

| What exists | What is absent |
|---|---|
| **159** envelope-shaped JSON examples (5.0% of the 3,194 parsed) | Any *declared* response schema. Not one endpoint has a typed response contract |
| **37 of 70** controllers have at least one response-shaped example | **33 of 70** have none at all |
| Response examples show the shape implicitly | No statement of which fields are always present, nullable, or typed how |

**How measured:** a documented JSON object counts as a response model if ≥2 of its keys are envelope keys
(`Program`, `Version`, `DateTime`, `Success`, `Message`, `Result`, `ErrorCode`, `ErrorMessage`, `aaData`,
`Output`). Recorded per controller as `response_model_documented`.

### ⛔ 31 shapes in reality, 6 of them documented

**31 distinct response shapes** were measured across the 1,868 executed calls; only **6** match a shape the
documentation describes *(supplied)*. The export presents the envelope as though it were uniform.

Five shapes worth naming, because each defeats a different naive assertion:

| Shape | Defeats |
|---|---|
| `{Program, Version, DateTime, Success, Message, Result[]}` | — the assumed baseline |
| Same, but **no `Message`** field | any assertion that reads `Message` unconditionally |
| Same, but `Result` is an **object**, not an array | any assertion that indexes `Result[0]` |
| **Bare array**, no envelope at all | every envelope-based assertion |
| `{"Output": "1\|Parameter error occurred - …"}` | JSON-path assertions — the error is inside a pipe-delimited string |

**Consequence for validation:** no generated assertion may assume a fixed shape, so every check must be
shape-tolerant and probe defensively. This is exactly what the L3 `envelope` layer measures, and it failed
**590** times against 1,278 passes — the largest single failure class in the run after L4.

---

## 5. Missing error codes — the highest-value gap

This is where the documentation is weakest, and the previously reported figure was itself too generous.

### 5.1 What the 2,470 pages actually contain

| Measure | Value |
|---|---:|
| `ErrorCode` field occurrences in documented examples | **358** |
| …explicitly `null` — the success path | ⛔ **351 (98.0%)** |
| …carrying a string value | **7** |
| …of those, placeholders (`Error1` ×3, the string `"null"` ×1) | 4 |
| **Distinct real error-code values documented** | ⛔ **3** |
| …in ARCON `NNN-XXX-YYY` format | **2** |
| Distinct `ErrorCode` values observed live | **108** *(prior)* |
| Codes recognised by the framework (`KNOWN_ERROR_CODES`) | 3 — `201`, `202`, `203`, hardcoded |
| **Controllers with any documented error code** | ⛔ **2 of 70** |

The three documented values, in full:

| Code | Page | Note |
|---|---|---|
| `203-SDC-GSDSI` | `pam-api:p714` | ARCON format |
| `203-SDC-GSDBSID` | `pam-api:p1092` | ARCON format |
| `APA:UR0021` | `pam-api:p2441` | A **different, undocumented format** — no numeric prefix |

### 5.2 ⚠️ Correcting the previously reported "4 documented error codes"

`docs/briefs/document-gap.md` §2 and `docs/gaps/01-Data-Gap-Analysis.md` list **four** codes:
`203-SDC-GSDSI`, `203-SDC-GSDBSID`, `190-SSH`, `100-SSH`.

**Two of those four are false positives.** `190-SSH` and `100-SSH` are fragments of
`ServiceDisplayName` values — IP address followed by a hyphen and the service type:

```
pam-api:p1065   "ServiceDisplayName": "10.11.10.190@preeti:10.11.10.190-SSH LINUX"
pam-api:p1066   "ServiceDisplayName": "10.10.170.100@preeti:10.10.170.100-SSH LINUX"
```

A code-shaped regex matches `190-SSH` and `100-SSH` inside the final octet. A third such artefact,
`214-SSH`, appears at `pam-api:p1064` and was never reported. The fix is a negative lookbehind
(`(?<![\d.])`), documented at `measure_doc_gap.py:196`. Both prior documents also **miss** `APA:UR0021`.

**Corrected position: 3 documented code values, 2 in ARCON format, against 108 observed live — not 4.**
The gap is wider than previously stated, and 98% of documented examples show `ErrorCode: null`.

### 5.3 Status-code semantics

| Status | Mentions across 2,470 pages |
|---|---:|
| 200 | 46 |
| 400 | 21 |
| 401 | 12 |
| 500 | 11 |
| 201 | 5 |
| 404 · 503 | 3 each |
| 403 | 2 |
| 405 | 1 |

**104 incidental mentions in 2,470 pages**, and nowhere a statement of what any status *means* for this API.

**Consequence for validation — the decisive one:** this API signals failure in the response **body** at HTTP
200. Without a code register and without status semantics, a rejected request is indistinguishable from an
accepted one. Measured: L4 `message-semantics` failed **458** times; **289 of 1,868 calls returned HTTP 200
with `Success: false`** *(prior)*; and `0` of 3,317 existing negative test rows carry an `ExpectedErrorCode`,
because there is no documented value to assert.

---

## 6. Missing examples

The export's real strength, and its three consumability defects.

| What exists | Measure |
|---|---:|
| Parseable JSON examples | **3,194** |
| …bound to an endpoint | **1,605** |
| …orphaned | **1,589** |
| Distinct field names covered | 1,097 *(prior)* |

This is richer than the automation framework's own payload helpers and is the best request-body source
available. Three problems stop it being consumed automatically:

| # | Problem | Measure | Consequence |
|---:|---|---:|---|
| 1 | **Payloads are not bound to their endpoint** — binding is by page proximity | 1,589 of 3,194 orphaned (49.7%) | A parser cannot reliably tell which body belongs to which route. Every binding is a hypothesis |
| 2 | ⛔ **Mandatory vs optional is never marked** | 0 fields marked | The direct cause of 204 of 217 creates failing |
| 3 | **No field types, lengths, formats or patterns** | 0 constraints | Cannot distinguish an id from free text; cannot generate a boundary case |

### 6.1 Where examples are missing entirely

| Measure | Value |
|---|---:|
| Create endpoints | **217** |
| …with fields from **any** source | 138 |
| ⛔ …with **no** fields from any source | **79** |
| …with any mandatory-field hint | ⛔ **1** |
| …that successfully insert a record | **13** *(prior)* |
| **Creates in controllers with zero payload examples** | ⛔ **83**, across 16 controllers |

The 16 controllers with creates but no example at all are dominated by the versioned families:
`ServiceDetailsV2` (16 creates), `ServiceDetailsV3` (15), `UserDetailsV3` (15), `UserDetailsV4` (15),
`ADbridgingV2` (6), `UserRegistrationV2` (4), `RDPSServiceInsertV2` (3), plus 9 controllers with one each.

⚠️ **`docs/gaps/01-Data-Gap-Analysis.md` §3.1 is internally inconsistent here**: it states 217
creates, 138 with a body from any source, and 101 with no body derivable — but 138 + 101 = 239 > 217.
Recomputed from `source-map.json`: **79**, not 101. The same 101 is repeated in `docs/briefs/document-gap.md` §5.

---

## 7. Missing workflows

| What exists | What is absent |
|---|---|
| Endpoints documented individually, page by page | ⛔ **Any statement of ordering, dependency or prerequisite** |

**How measured:** all 2,470 `pam-api` pages were scanned for ordering language — `must first`,
`before calling`, `before you`, `after creating`, `prerequisite`, `in the following order`, `step 1`,
`first call`, `depends on the`, `returned by the previous`, `obtained from the`, and six further variants.

> ⛔ **Result: 0 of 2,470 pages contain any ordering or prerequisite phrase.**

Nor is the producer→consumer relationship implicit: **1,680** chain candidates were derived, every one by
**field-name matching**, and **0 of 1,680** came from documentation or an observed producer response *(prior)*.

**Consequence for validation — this is the root of the chaining failure.** Because no dependency is
declared, the harness must guess that the `ServiceId` returned by one endpoint is the `ServiceId` another
consumes. When the producing create fails, the guess cannot be tested at all:

| Layer | Result |
|---|---|
| L5 `chain-key-extracted` | 982 pass · ⛔ **196 fail — every one `resolved []; MISSING ['NEW_ID']`** |
| L6 `record-exists` | ⛔ **2 pass · 105 fail** of 107 attempted |
| Flow verdicts | 30 PASS · **296 FAIL** of 326 |

The mechanism itself is sound — one chain was proven to **5 hops** with no hardcoded values *(prior)*. What
is missing is the declaration of which endpoint feeds which.

---

## 8. Missing business rules

| What exists | Measure |
|---|---:|
| Controllers whose pages contain any rule-shaped language | **28 of 70** |
| ⛔ Controllers with none | **42 of 70** |

**How measured:** pages bound to a controller were scanned for constraint language — `is mandatory`,
`must be`, `must not`, `cannot be`, `is required`, `not allowed`, `should not`, `maximum length`,
`minimum length`, `valid range`, `already exists`, `duplicate`, and further variants. Recorded per
controller as `business_rules_documented`. ⚠️ This is a **presence** measure, not a completeness one: it
detects that constraint language occurs somewhere on the page, not that the rule is stated per field. The
true per-field rule coverage is **UNKNOWN** and would be settled only by a field-level specification.

Rules demonstrably enforced by the product but stated nowhere:

| Rule the server enforces | How we know | Documented |
|---|---|---|
| `Port is Mandatory` on service creation | live rejection text *(prior)* | ⛔ No |
| `LogTypeId` required on `GetLogDetails` | `ErrorCode: 206-LC_GLD` at HTTP 200 *(prior)* | ⛔ No |
| `ServiceId` is a **string** on create, **integer** on read | 7 spellings, type flips *(prior)* | ⛔ No |
| ⛔ **`Success: true` + `Message: "Already Exists"` means nothing was inserted** | `POST /api/ServiceCreation/SetServiceDetails` *(prior)* | ⛔ No |

**Consequence for validation — the most dangerous single item in this report.** The last rule means a
create assertion that checks the status code *and* the `Success` flag still passes when no record was
written. Correctness depends on reading `Message` semantics: `"Inserted Successfully"` means inserted,
`"Already Exists"` means no-op. That distinction is enforced by the product, relied on by the harness, and
**documented nowhere**. Any team writing assertions without it produces false green results.

---

## 9. ⚠️ Existing documents that need correcting

Every item was re-measured this session. Figures marked *(supplied)* were measured by a parallel agent in
the same session.

| Document | Location | Currently says | Should say |
|---|---|---|---|
| `docs/briefs/document-gap.md` | §2 | **4** documented error codes, incl. `190-SSH`, `100-SSH` | **3** code values (`203-SDC-GSDSI`, `203-SDC-GSDBSID`, `APA:UR0021`). The two `-SSH` entries are IP-address fragments — §5.2 |
| `docs/briefs/document-gap.md` | §5 | **101** creates with no usable body | **79** |
| `docs/briefs/document-gap.md` | §0, §3 | **8** distinct response shapes | **31** shapes measured, **6** documented *(supplied)* |
| `docs/briefs/developer-loopholes.md` | §3 / response-shape claim | **8** response shapes | **31** *(supplied)* |
| `docs/briefs/developer-loopholes.md` | :107 | `54 of 70` controllers lack a `*Controller.cs` | **58 of 70** — `A6` §6 |
| `docs/gaps/01-Data-Gap-Analysis.md` | :30 | `54 of 70 controllers absent` | **58 of 70 have no implementation** |
| `docs/gaps/01-Data-Gap-Analysis.md` | §3.1 | 138 with a body **and** 101 without (= 239 > 217) | 138 with, **79** without |
| `docs/gaps/01-Data-Gap-Analysis.md` | §1 row 2, §5 | **4** error codes | **3** |
| `tools/build_source_map.py` | :333 | hardcoded string `54 of 70` | compute it, or cite `doc-gap-coverage.json` |
| `tools/SOURCE-MAP.md` | :80 | `54 of 70` | **58 of 70** (regenerate) |
| `BLAST/findings.md` | :61 | `23 / 70` absent | **58 / 70**; keep 22 only if relabelled "name appears nowhere in any `.cs` text" |
| `artifacts/loopholes/LH-05-*/` | `EVIDENCE.md:31`, `JIRA-TICKET.md:72` | `23 of 70 controllers absent entirely` | **58 of 70**. Hardcoded at `lh_specs_run.py:944,1046` — fix and regenerate |
| `.claude/rules/api-surface.md` | :29-30 | records 23-vs-54 as unresolved | Settled: **58**. The 23 is now explained (it measured text presence), not merely uncited |
| `docs/findings/issues/ISSUE-005-api-coverage-gap.md` | §2, §3, §4, §6 | **1,322** endpoints | **1,306** — add a superseding note |

⛔ `docs/history/archive/workbench-archive/approach/dynamic-api-generation.md:378` also carries `23 / 70`. It is in the **frozen
archive** and must **not** be edited.

---

## 10. Recommendations — what artifact should exist, who owns it, what it must contain

Ranked by measured unblocking value. Full trade-off analysis with a second option for each:
`data/analysis/solutions-A6A7.json`.

| # | Artifact | Owner | Unblocks (measured) |
|---:|---|---|---|
| **1** | **Error-code register** | Development | Negative testing end to end. 108 codes observed, **3** documented, **0** of 3,317 negative rows assertable today |
| **2** | **OpenAPI 3.1 spec generated from the running API** | Development (Swashbuckle on the API host) | Every gap in §2–§8 at once. Replaces 4 disagreeing artefacts with one |
| **3** | **Per-endpoint field table with mandatory flags** | Development, or recovered from the DB schema | Creates from **13 of 217** upward — the highest-leverage single change |
| **4** | **Response-envelope specification** | Development + Architecture | 590 L3 and 458 L4 failures become assertable. 31 shapes, 6 documented |
| **5** | **Route dump per build** | Development / CI | Eliminates 135 false 404s permanently, and is the only ask that stops its problem recurring |
| **6** | **Workflow / dependency map** | Development + QA | 196 `MISSING ['NEW_ID']`; 0 of 1,680 chain candidates are declared |
| **7** | **Documented status-code decision** | Architecture | Makes every assertion non-provisional. A decision, not a document |
| **8** | **Version and status each endpoint** | Documentation team | The 562 versioned endpoints with 1 documented between them (§3.2) |

### 10.1 The primary recommendation, specified

⭐ **Generate an OpenAPI 3.1 specification from the running API and publish it per build.** Item 2 subsumes
items 1, 3, 4, 5 and 8. It is a build-pipeline change, not a writing project, so it cannot rot — which is
the failure mode that produced the current situation. To be *sufficient* it must carry, per operation:

| Element | Requirement | Closes |
|---|---|---|
| Route, verb, controller | complete for all 1,306 | §3 — 912 undocumented |
| **Request schema per property**: `required` · `type` · `maxLength` · `format` · `pattern` · `enum` | mandatory-ness **declared**, never inferred | §2, §6 — the create blocker |
| **Response schema per status**, including every envelope variant | which of the 31 shapes this operation returns | §4 |
| **Error responses**: every `errorCode` the operation can emit, with meaning and client action | ⛔ must state that **HTTP 200 does not imply success** | §5 |
| Worked request **and** response example, bound to the operation | replaces proximity binding | §6 — 1,589 orphans |
| `deprecated` flag and version | which of `V1`/`V2`/`V3`/`V4` is current | §3.2 |
| Declared dependencies — what must exist first, what id is returned | producer→consumer made explicit | §7 |

### 10.2 If item 2 is refused, the minimum viable set

| Artifact | Owner | Why it is the floor |
|---|---|---|
| Error-code register (one table: code · meaning · emitting endpoints · client action · client-vs-server) | Development | Without it success cannot be determined at all. **We have already derived all 108 codes** — `artifacts/loopholes/LH-04-*/EVIDENCE.xlsx`. It needs *confirmation*, not authoring. Please also normalise the 17 malformed codes |
| `INFORMATION_SCHEMA` dump — columns, `NOT NULL`, lengths, FKs, `CHECK` constraints | DBA | Recovers mandatory-ness, types and lengths without granting access or touching code. **A one-off CSV export delivers most of item 3's value at near-zero risk** |
| One paragraph, prominently placed: *HTTP 200 does not indicate success; read `Success` and `ErrorCode`* | Documentation team | Prevents an entire class of false-green testing. Lowest effort item in this report |

### 10.3 What is deliberately **not** requested

So the asks stay narrow and credible: no write access to any database; no production or preprod access; no
microservice source behind `ARCONAPIGateway`; no additional documentation *pages* — there are already 3,571,
and volume is not the problem; and no tooling, licence or infrastructure. The harness works. **What is
missing is information the product already has and has not published.**

---

## 11. Reproducing every figure

```powershell
python tools\measure_doc_gap.py
#   -> artifacts\analysis-data\doc-gap-coverage.json      70 rows, one per controller
#   -> tools\.doc-gap-summary.json  every headline figure

python tools\rag\query.py find "<terms>"    # page-cited search
python tools\rag\query.py page pam-api 714  # verify an error-code citation
```

⛔ Never read `artifacts/rag-corpus/pam-api.md` directly — it is 101,803 lines. Use the query layer and
cite as `pam-api:p<N>`.

| Column in `doc-gap-coverage.json` | Definition |
|---|---|
| `endpoints_documented_confluence` | exact `/api/<Controller>/<Action>` route present in the export |
| `payload_examples_available` | JSON objects bound to the controller by page proximity — a hypothesis |
| `response_model_documented` | a bound example carries ≥2 envelope keys |
| `error_codes_documented` | distinct real code values on the controller's pages, placeholders excluded |
| `business_rules_documented` | constraint language present on a bound page — presence, not completeness |
| `coverage_pct` | `endpoints_documented_confluence / endpoints_total` |
| `gap_severity` | `critical` = no documentation **and** no implementation; `high` = <25% or creates with no payload; `medium` = <60% or no response model; else `low` |
