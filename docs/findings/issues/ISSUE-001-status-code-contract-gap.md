# ISSUE-001 — HTTP status codes are not used semantically, and no error contract is declared

**Severity:** 🔴 High · **Type:** API contract / documentation defect · **Raised:** 2026-07-28
**Affects:** all 37 reachable Swagger specifications · all 690 documented operations
**Owner:** development team (per-module owners listed in the shared Swagger sheet)
**Evidence:** `Evidence/*.json` (all 102 files) · `../Execution/spec_quality.json`
**Reproduce:** `python Reports\Scripts\run_validation.py`

---

## 1. Statement

Two related defects:

1. **No specification declares any failure outcome.** Across all 690 operations, `200` is the only
   declared response code. There is no 400, 401, 403, 404, 409 or 500 anywhere.
2. **HTTP status is not used semantically.** The product signals application-level failure inside a
   `200` envelope, while genuine transport-level failures return codes the spec never mentions.

The original estimate raised internally was *"approximately 80% of transactions do not use proper
200-series status codes."* The measured position is more specific and more serious: **100% of operations
declare only `200`, and 0% declare any error code at all.**

## 2. Evidence A — from the developers' own specifications

Measured across every operation in all 37 fetched specs. Not a sample.

| Measure | Count | % of 690 |
|---|---:|---:|
| Declares `200` | 690 | **100.0%** |
| Declares any 4xx or 5xx | **0** | **0.0%** |
| Declares a granular 2xx (`201`, `202`, `204`) | **0** | **0.0%** |
| Declares only `200` and nothing else | 690 | **100.0%** |
| Carries an `operationId` | **0** | **0.0%** |

Implications, concretely:

- Resource-creating `POST` operations do not return `201 Created`.
- No operation returns `202 Accepted`, so no operation is documented as asynchronous.
- `DELETE` operations do not return `204 No Content`.
- **No consumer can discover from the specification that a call can fail.**

## 3. Evidence B — from live execution

102 GET operations executed against `devint`. Note §5 — this run was unauthenticated.

| Measure | Count | % of 102 |
|---|---:|---:|
| Returned a status **not declared** in its own spec | **68** | **66.7%** |
| Returned `401` (undeclared) | 57 | 55.9% |
| Returned `200` (declared) | 34 | 33.3% |
| Returned nothing within 20 s | 11 | 10.8% |

Every non-200 response is, by construction, undocumented — because `200` is the only code any spec
declares.

## 4. Evidence C — the envelope is the real signal, and it is unreliable

The product's own convention is to answer `200` and place the outcome in the body. That makes the
envelope the authoritative signal — but it is not kept consistent with the HTTP status:

| Body pattern | Incidence |
|---|---:|
| Body `StatusCode` disagrees with the HTTP status | see ISSUE-003 |
| `StatusCode: 401` alongside `Message: "Success"` | 10 / 102 |
| Error body is not JSON at all | 47 / 102 (see ISSUE-002) |

Verbatim, from `Evidence/001_GET_api_AGWAURLGEN_getPulse.json`:

```json
{"Program":"Arcon Micro Service API","Version":"1.0.0.0",
 "StatusCode":401,"Message":"Success","Ticks":"185.899..."}
```

Returned with HTTP status **401**, declaring itself both a failure (`StatusCode: 401`) and a success
(`Message: "Success"`).

## 5. ⚠️ What this issue does *not* claim

This run supplied **no authentication token**. The 57 × `401` responses are therefore the API behaving
**correctly**. This issue does **not** allege that returning 401 is wrong.

The defect is that **the specification does not document the 401** — and would not document it however the
call were authenticated. Evidence A is drawn purely from the specifications and is entirely independent of
authentication.

## 6. Consequence

| Area | Impact |
|---|---|
| **Consumer teams** | Cannot write correct error handling from the contract; must discover failure modes empirically |
| **Automated validation** | Standard spec-driven tools (Schemathesis, Dredd, Pact) cannot generate negative cases — there is nothing to assert against |
| **This QA effort** | Negative and edge-case *expectations* cannot be derived. Only differential comparison is possible — the direct cause of the limitation recorded in `../Summary/Executive-Summary.md` §7 |
| **Integration risk** | A consumer that checks only `response.status == 200` will treat every rejected request as successful |

## 7. Recommended fix

| # | Action | Effort |
|---|---|---|
| 1 | Declare `400`, `401`, `403`, `404`, `500` per operation in Swagger, with a response schema for the error envelope | Small — annotation work |
| 2 | Return `201` from creating operations, `204` from deletes, `202` where processing is asynchronous | Medium — touches behaviour |
| 3 | Add `operationId` to every operation | Trivial |
| 4 | Make the HTTP status and the envelope `StatusCode` agree, always | Small — see ISSUE-003 |

Item 1 alone would eliminate most of the 66.7% L1 failure rate, because the responses the API already
returns would become documented.

## 8. Verification

After the fix, re-run the harness. The `L1_http_status` column in
`../Excel/PAM_API_Validation_Results.xlsx` should move to PASS for every endpoint whose real status is now
declared, with no change to the harness itself.
