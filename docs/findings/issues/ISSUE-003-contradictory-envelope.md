# ISSUE-003 — Response envelope contradicts itself: `StatusCode: 401` with `Message: "Success"`

**Severity:** 🔴 High · **Type:** Runtime defect · **Raised:** 2026-07-28
**Affects:** 10 of 102 executed endpoints, across at least 5 microservices
**Independent of authentication:** ✅ yes — the contradiction is *within* the response body
**Evidence:** `Evidence/001_GET_api_AGWAURLGEN_getPulse.json` and 9 others
**Reproduce:** `python Reports\Scripts\run_validation.py`

---

## 1. Statement

Several services return a response envelope in which the status field reports **failure** and the message
field reports **success**, in the same payload:

```json
{
  "Program": "Arcon Micro Service API",
  "Version": "1.0.0.0",
  "StatusCode": 401,
  "Message": "Success",
  "Ticks": "185.899..."
}
```

`StatusCode: 401` (unauthorised) and `Message: "Success"` are mutually exclusive claims.

## 2. Evidence

| Measure | Count |
|---|---:|
| Responses with a non-2xx `StatusCode` **and** `Message: "Success"` | **10** |
| Distinct services exhibiting it | ≥ 5 — `AGWAURLGEN`, `ATSConfiguration`, `Sdk`, `Domain`, `DualAuth` |

Confirmed instances:

```
HTTP 401  /api/AGWAURLGEN/getPulse            StatusCode=401  Message="Success"
HTTP 401  /api/ATSConfiguration/getPulse      StatusCode=401  Message="Success"
HTTP 401  /api/Sdk/GetAllServiceTypes         StatusCode=401  Message="Success"
HTTP 401  /api/Domain                         StatusCode=401  Message="Success"
HTTP 401  /api/DualAuth                       StatusCode=401  Message="Success"
… see Results sheet, column L2_envelope = FAIL
```

The harness records this as:

```
L2_envelope: FAIL — StatusCode=401 but Message="Success"
```

## 3. Why this is worse than it looks

PAM's stated convention is that the **body envelope**, not the HTTP status, is the authoritative outcome
signal. That convention is documented in the workspace guidance and is the reason
`ApiHelper.validateResponseErrorCode(...)` exists in the automation framework.

If the authoritative signal is internally inconsistent, then **there is no reliable way for any consumer
to determine whether a call succeeded**:

| A consumer that reads… | Concludes | Correct? |
|---|---|---|
| HTTP status | failed | ✅ |
| `StatusCode` in body | failed | ✅ |
| `Message` in body | **succeeded** | ⛔ |
| `Message` only, which the convention encourages | **succeeded** | ⛔ |

`"Message"` appears to be a hardcoded literal rather than derived from the outcome — it reads `"Success"`
even on the failure path.

## 4. Consequence

| Area | Impact |
|---|---|
| **Consumer teams** | A message-based success check silently passes on every auth failure |
| **This QA effort** | The `L2_envelope` layer — the layer that matters most for PAM — cannot be trusted as a pass signal until fixed |
| **Support / triage** | Logs will record `"Success"` against failed calls, making incident reconstruction misleading |

## 5. Recommended fix

| # | Action |
|---|---|
| 1 | Derive `Message` from the actual outcome; never emit a hardcoded `"Success"` |
| 2 | Assert internally that `StatusCode` matches the HTTP status before the response is written |
| 3 | Add a unit test per service asserting the failure path emits a non-success message — this class of defect is trivially catchable in CI and was not caught, which is itself the point of ISSUE-004 |

## 6. Verification

Re-run the harness. `L2_envelope` should report PASS wherever the envelope is now self-consistent. The
harness already checks exactly this condition, so no test change is required.
