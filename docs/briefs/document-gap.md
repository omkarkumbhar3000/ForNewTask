# Documentation Gaps — `PAM API (Internal Team)` Confluence Export

**For:** the documentation team · **Source:** `data/sources/PAM API (Internal Team).pdf` — 2,470 pages
**Cross-checked against:** `APIConfig.java` (1,306 endpoints), the 37 shared Swagger specs, and **5,416 live
API calls** executed on 2026-07-29 against `QA_MsSQL`
**Method:** the PDF was extracted to page-cited text (`artifacts/rag-corpus/pam-api.md`) and compared
programmatically. Every figure below is measured, not sampled.
**Status of the source:** confirmed by the owner as **not up to date** — still the best payload and logic
reference available, so the goal here is to improve it, not replace it.
**Last updated:** 2026-08-05

---

## 0. Summary

| Finding | Measure |
|---|---:|
| Endpoints in the automation catalogue **not documented at all** | **914 of 1,306 (70%)** |
| Endpoints documented **but absent from the catalogue** | 60 |
| Overlap — documented **and** tested | 392 (30%) |
| Action names appearing anywhere in the text | 391 of 541 (72%) |
| **ARCON error codes documented** | **4** |
| **ARCON error codes the framework recognises** | 3 (`201`, `202`, `203`) |
| **Distinct response shapes found live** | **31** *(re-measured — this row said 8)* |
| **Response shapes the document describes** | **6** of the 31 *(this row said "effectively 1")* |
| Parseable JSON payload examples in the document | **3,194** (1,097 distinct fields) — the document's greatest strength |

**One-line verdict:** the document is strong on **request payloads** and weak on everything needed to know
whether a call *succeeded* — error codes, response envelopes, and status-code semantics.

---

## 1. ⛔ Gap 1 — 70% of the API is undocumented

914 of the 1,306 endpoints declared in `APIConfig.java` have no `/api/<Controller>/<Action>` reference
anywhere in the 2,470 pages. The document cites 452 distinct routes; the catalogue declares 1,306.

**Why it matters:** every undocumented endpoint is one where a tester has to guess the payload, and where a
generated test cannot be derived at all.

**Ask:** publish at least the route, verb, and request shape for the missing 914. A one-line-per-endpoint
table would be more useful than prose.

---

## 2. ⛔ Gap 2 — error codes are almost entirely absent

The document contains **four** ARCON-style error codes in 2,470 pages:

| Documented | |
|---|---|
| `203-SDC-GSDSI` · `203-SDC-GSDBSID` · `APA:UR0021` | ⚠️ **Three, not four.** `190-SSH` and `100-SSH` were listed here and are **not error codes** — they are fragments of IP addresses that the extraction matched as codes. Re-measured: `docs/analysis/A7-documentation-gap-analysis.md` §5.2 |

Live execution found codes the document never mentions, including:

| Observed live | Meaning returned | HTTP status |
|---|---|---|
| `902-ALC-ISSML` | `"System error has occurred"` | **200** |
| `206-LC_GLD` | `"Parameter error occurred - Required property 'LogTypeId' not found"` | **200** |

**Why it matters most:** this product signals failure in the response **body**, not the status code. Without
a documented error-code catalogue, nobody — human or automated — can tell a real failure from a success.
**1,022 of our 5,416 latest-run cases returned HTTP 200 while failing validation** (289 of 1,868 on the
earlier run carried `Success: false`). None of those codes are documented.

**Ask:** a complete error-code register — code, meaning, which endpoints emit it, and the corrective action.
This is the single highest-value addition the documentation team can make.

---

## 3. ⛔ Gap 3 — the response envelope is not described, and there are eight of them

The document implies a single response shape. Live execution found **eight**:

| # | Shape | Example endpoint | Documented? |
|---:|---|---|---|
| 1 | `{Program, Version, DateTime, Success, Message, Result[]}` | `GetAllActiveUserList` | Partially |
| 2 | Same, but **no `Message` field** | `GetLOBList` | ⛔ No |
| 3 | Same, but `Result` is an **object**, not an array | `GetServiceDetails` | ⛔ No |
| 4 | **Bare array**, no envelope at all | `DeviceOnboarding/GetLOBList` | ⛔ No |
| 5 | `{Success: false, ErrorCode, ErrorMessage}` at **HTTP 200** | `InsertSSMLogs` | ⛔ No |
| 6 | `{aaData, aaData1, aaData11}` — DataTables style | `GetAccessControlLogs` | ⛔ No |
| 7 | `{"Output": "1\|Parameter error occurred - ..."}` — error inside a string | `SetPAMUserDetails` | ⛔ No |
| 8 | Bare `false` boolean, or bare `""`, as the whole body | `InsertPsrBulkLogs` | ⛔ No |

**Ask:** document each envelope, which endpoints use which, and — critically — **how to determine success**
for each. Shape 7 is the worst case: the error is embedded in a pipe-delimited string inside a JSON field.

---

## 4. ⛔ Gap 4 — status-code semantics are undefined

Across 2,470 pages the document mentions HTTP statuses only in passing:

| Status | Mentions |
|---|---:|
| 200 | 46 |
| 400 | 21 |
| 401 | 12 |
| 500 | 11 |
| 201 | 5 |
| 404 | 3 |
| 503 | 3 |
| 403 | 2 |
| 405 | 1 |

For an API reference of this size that is close to silent. **Measured reality:** 90% of live calls returned
200 regardless of outcome, and 135 returned 404 for endpoints the catalogue declares.

**Ask:** state explicitly, once and prominently, that **HTTP 200 does not indicate success**, and specify
which statuses are used deliberately versus incidentally.

---

## 5. 🟡 Gap 5 — payload examples are the strong point, but unlabelled

The document's best asset is **3,194 parseable JSON objects** covering **1,097 distinct field names** —
far richer than the automation framework's own payload helpers.

Most-documented fields: `ServiceType` (747), `HostName` (638), `ServiceTypeId` (591), `ServiceId` (586),
`ServiceUserName` (528), `ServiceDomain` (516), `Port` (496), `IpAddress` (451).

Three problems that stop them being consumed automatically:

| Problem | Effect |
|---|---|
| Payloads are not consistently bound to the endpoint they belong to | A parser cannot tell which body goes with which route |
| **Mandatory vs optional is not marked** | The main reason generated creates fail — **79** of 217 create endpoints have no usable body anywhere (this read `101`, which was wrong: 138 with a body + 101 without exceeds the 217 total. Corrected under `OBJ-007`) |
| No field types or value constraints | Cannot distinguish an id from a free-text field |

**Ask:** for each endpoint, a small table — field · type · mandatory? · example · constraint. That single
change would convert this document from a reading reference into a machine-consumable contract.

---

## 6. 🟡 Gap 6 — field naming is inconsistent, and the document mirrors it

The same logical field appears under many spellings, in both the document and the code:

| Concept | Spellings observed |
|---|---|
| LOB identifier | `LobId` · `LOBID` · `LOBid` · `LobsId` |
| User identifier | `UserId` · `UserID` · `userid` |
| Service identifier | `ServiceId` (integer on read, **string on create**) |

Our tooling compensates with case-insensitive matching and explicit type casts, but that is a workaround.

**Ask:** publish a canonical field-name and type register, and flag the deviations as known defects.

---

## 7. 🟡 Gap 7 — 60 documented endpoints are not in the catalogue

60 routes appear in the documentation but not in `APIConfig.java`. These are either newer than the test
framework or deprecated and never removed from the docs. **They currently have zero test coverage.**

**Ask:** mark each documented endpoint with a status — active, deprecated, or planned — and a version.

---

## 8. ⛔ Gap 8 — the catalogue and the deployment disagree, and the docs settle nothing

Live execution returned **135 × HTTP 404** for endpoints that `APIConfig.java` declares. The documentation
does not indicate which endpoints exist on which build, so it cannot arbitrate.

Separately, the 37 shared Swagger specs (690 operations) describe a **different API surface** — roughly
**6% name overlap** with `APIConfig.java`. Three sources, three different pictures of the same product.

**Ask:** state which surface is authoritative per deployment, and version the documentation against a PAM
release so a reader knows what applies to the build in front of them.

---

## 9. Consolidated request to the documentation team

| Priority | Ask | Why it is ranked here |
|---|---|---|
| **1** | Complete error-code register | Without it, success cannot be determined at all |
| **2** | Document all **31** measured response shapes and how to detect success in each — only **6** are documented today | Same reason; 289 silent failures observed |
| **3** | Per-endpoint field tables with **mandatory** flags and types | Unblocks generated write coverage — currently 13 of 217 creates work |
| **4** | Route/verb/payload for the missing 914 endpoints | 70% of the API is invisible to documentation |
| **5** | State plainly that HTTP 200 ≠ success | One paragraph, prevents a whole class of false-green testing |
| **6** | Canonical field-name and type register | Removes the need for case-insensitive workarounds |
| **7** | Version the document and mark endpoint status | Lets a reader know what applies to their build |

---

## 10. Reproducing these figures

```powershell
python tools\rag\extract.py                       # re-index data/sources
python tools\rag\query.py find "<terms>"          # page-cited search
```

Comparison figures come from `artifacts/rag-corpus/pam-api.md` (page-cited) against
`APIConfig.java`. Live evidence: `artifacts/runs/2026-08-05_114315/` — 5,424 evidence files, one per call
(earlier run: `artifacts/runs/2026-07-29_181439/`, 1,868 files).
Cite documentation as `pam-api:p<N>`.
