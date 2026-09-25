# ISSUE-002 — Error responses return plain text with no `Content-Type` header

**Severity:** 🔴 High · **Type:** Runtime defect · **Raised:** 2026-07-28
**Affects:** 47 of 102 executed endpoints · multiple microservices
**Independent of authentication:** ✅ yes — this is about the *format* of the response, not its status
**Evidence:** `Evidence/002_GET_api_Configure_GetCurrentDate.json` and 46 others
**Reproduce:** `python Reports\Scripts\run_validation.py`

---

## 1. Statement

When these services reject a request they return:

- a body that is **not JSON** — the bare string `Unauthorized Access.`
- **no `Content-Type` header at all**

despite the specification declaring `application/json` for the operation. A JSON client receives an
unparseable body and no indication of what it received.

## 2. Evidence

| Measure | Count | % of 102 |
|---|---:|---:|
| Responses whose body is **not parseable JSON** | **47** | **46.1%** |
| Responses with **no `Content-Type` header** | **58** | **56.9%** |
| Responses with `Content-Type: application/json` | 44 | 43.1% |

Verbatim body, from `Evidence/002_GET_api_Configure_GetCurrentDate.json`:

```
Unauthorized Access.
```

Twenty characters. No JSON. No `Content-Type`. The parse failure recorded by the harness:

```
L2_envelope: FAIL — body is not JSON: Expecting value: line 1 column 1 (char 0)
```

Affected endpoints include:

```
GET /api/Configure/GetCurrentDate
GET /api/Dashboard/GetActiveReviewCount
GET /api/Dashboard/GetConfiguredReviewsStatus
GET /api/Dashboard/GetReviewersConfiguredCount
GET /api/Dashboard/GetReviewersWithMostActionsTaken
GET /api/Dashboard/GetReviewersWithMostOpenReviews
GET /api/CertificateManager/GetAllCertificates
GET /api/CertificateManager/GetCertificateTypes
GET /api/DigitalVault/GetAllDigitalVaultUsers
GET /api/DigitalVault/GetOldApiUsers
GET /api/DigitalVault/GetAppType
… 36 more — see the Results sheet, column L6_content_type = FAIL
```

## 3. ⚠️ The aggravating factor — two formats for one error

The **same logical error** is returned in **two incompatible formats** depending on which service is
called:

| Service group | Body for an unauthorised call |
|---|---|
| `AGWAURLGEN`, `ATSConfiguration`, `Sdk`, `Domain`, `DualAuth` | JSON envelope: `{"Program":"…","StatusCode":401,"Message":"Success",…}` |
| `Configure`, `Dashboard`, `CertificateManager`, `DigitalVault` | Bare text: `Unauthorized Access.` |

A consumer therefore **cannot write a single error handler** for the PAM API. It must branch on which
microservice it happens to be talking to, and that branching is undocumented.

## 4. Consequence

| Area | Impact |
|---|---|
| **Consumer teams** | `JSON.parse()` throws. The client sees a parse exception, not an auth error, and cannot surface a useful message |
| **Logging / monitoring** | Error taxonomy cannot be built — the failure reason is unstructured text in some services and structured in others |
| **Automated validation** | Schema validation cannot even begin; the response is not JSON |
| **Security posture** | `Unauthorized Access.` with no `WWW-Authenticate` header gives a client no machine-readable way to know how to authenticate |

## 5. Recommended fix

| # | Action |
|---|---|
| 1 | Return a **JSON error envelope for every error path**, in every microservice, using one shared shape |
| 2 | Always set `Content-Type: application/json; charset=utf-8` — including on error paths |
| 3 | Standardise the error envelope across all services (`{ statusCode, errorCode, message, traceId }` or similar) and declare it in Swagger as the `400`/`401`/`500` response schema — closes ISSUE-001 item 1 at the same time |
| 4 | Add `WWW-Authenticate` on 401 responses |

This is likely a missing global exception filter / middleware registration in the affected services —
the ones returning the JSON envelope already have the pattern the others lack.

## 6. Verification

Re-run the harness. `L6_content_type` and the parse component of `L2_envelope` should both reach PASS on
all 102 endpoints without touching the harness.
