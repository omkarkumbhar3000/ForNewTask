# Business Context — the 5-minute demo

**Question this answers:** *"How do you provide business context to the AI?"*
**Answer:** you give it these five things. Here is one real, measured example.
**Evidence:** run `artifacts/runs/2026-07-29_160155/` · flow `service_lifecycle` · verdict **PASS**

> Need the full version? `BUSINESS-CONTEXT-STANDARD.md` — same example, 27 sections. This file is the
> walkthrough; that one is the reference.

---

## 1. The business goal, in one line

Create a privileged-access service inside a Line of Business, then **prove the product actually registered
it** — not merely that the API accepted the request.

## 2. What the AI was told

Five things. Nothing else was needed.

| # | Context given | Concretely |
|---:|---|---|
| 1 | **The goal** | Create a service in a LOB and prove it is registered |
| 2 | **The sequence** | 5 API calls, in this order, each feeding the next |
| 3 | **What carries forward** | `LobId` → `ServerGroupId` → `ServiceId` |
| 4 | **What "success" means here** | ⚠️ Not the HTTP status — see §5 |
| 5 | **The proof step** | Go back to the LOB and confirm the service is in its active list |

## 3. The chain — 5 levels, real measured values

```
1  GetLOBList                      →  LobId 108        (AUTOMATION_TEST_LOB)
2  GetServerGroupList(108)         →  ServerGroupId 282
3  SetServiceDetails(...)          →  ServiceId 25339  "Inserted Successfully"
4  GetServiceDetails(25339)        →  ServiceSessionId 75277
5  GetActiveServicesByLOBId(108)   →  ServiceId 25339  FOUND
```

| # | Endpoint | Sends | Gets back | Time |
|---:|---|---|---|---:|
| 1 | `POST /api/ADbridging/GetLOBList` | `{}` | `LobId 108` | 88 ms |
| 2 | `POST /api/ADbridging/GetServerGroupList` | `LobId: 108` | `ServerGroupId 282` | 31 ms |
| 3 | `POST /api/ServiceCreation/SetServiceDetails` | `LOBID: 108`, `ServerGroupId: 282`, + service details | **`ServiceId 25339`** · `Message: "Inserted Successfully"` | 6,452 ms |
| 4 | `POST /api/ServiceDetails/GetServiceDetails` | `ServiceId: 25339` | `ServiceSessionId 75277`, `Hostname 10.11.0.236` | 2,306 ms |
| 5 | `POST /api/ServiceDetails/GetActiveServicesByLOBId` | `LOBID: 108` | `Message: "16 - Records Found"` · **`ServiceId 25339` present** | 1,090 ms |

**Step 5 is the whole point.** It returns to the LOB the chain started from and proves the service was
*registered against it*. Steps 1–4 could all pass while the product had stored nothing usable.

## 4. How the AI knew what to pass forward

Three lines of declarative config — no code. From `tools/flows/03_service_lifecycle.json`:

```jsonc
"find_extract": { "in": "Result", "where": {"LobName": "AUTOMATION_TEST_LOB"},
                  "take": {"LOB_ID": "LobId"} }        // find the row, don't assume Result[0]

"extract": { "NEW_SERVICE_ID": "Result[0].ServiceId" },
"cast":    { "NEW_SERVICE_ID": "int" }                 // returns a string; step 4 needs a number

"verify_present": { "in": "Result", "match_field": "ServiceId",
                    "value": "${NEW_SERVICE_ID}" }     // step 5's independent proof
```

## 5. ⚠️ The one trap you must tell the AI about

**On this API, a rejected request still returns HTTP 200.** The rejection is inside the response body.

Worse: `SetServiceDetails` can return `Success: true` with `Message: "Already Exists"` — **nothing was
written**, and both the status code and the success flag are green.

| So a create is judged on… | Not on… |
|---|---|
| `Message = "Inserted Successfully"` ✅ | `HTTP 200` ⛔ |
| An actual `ServiceId` coming back ✅ | `Success: true` ⛔ |
| Reading it back in step 5 ✅ | — |

Measured across the full run: **90%** of calls looked green on status alone; the true pass rate across all
checks was **64%**.

This is why the flow randomises the hostname, IP, service user and port on every run — so step 3 is a
genuine insert and not a silent no-op.

## 6. What was checked at each step

| Layer | Check | Result here |
|---|---|---|
| `L1` | HTTP status | 200 × 5 ✅ |
| `L2` | Content type is JSON | ✅ |
| `L3` | `Success: true` in the body | ✅ |
| `L4` | **Message means what we need** | `"Inserted Successfully"` ✅ |
| `L5` | An id was actually extractable | `ServiceId 25339` ✅ |
| `L6` | **The record reads back** | `ServiceId 25339` **found** ✅ |
| `L7` | Within time budget | slowest 6,452 ms of 8,000 ms ✅ |

Flow verdict: **PASS** — all five levels, every check.

## 7. Where the proof lives

| Artifact | Path |
|---|---|
| The flow definition | `tools/flows/03_service_lifecycle.json` |
| The measured result | `artifacts/runs/2026-07-29_160155/results.json` → flow `service_lifecycle` |
| Raw request/response per call | `artifacts/runs/2026-07-29_160155/evidence/13…15_service_lifecycle_*.json` |
| The written-up demo | `docs/management/summary/API-Chaining-Feasibility-Demo.md` |
| Full context standard | `docs/business-context/BUSINESS-CONTEXT-STANDARD.md` |

---

## The takeaway for management

Providing business context is not "give the AI the API list". It is these five, and the fourth is the one
teams forget:

1. **The business goal** — what outcome proves the feature works
2. **The sequence** — which calls, in which order
3. **The links** — what each step hands to the next
4. **⚠️ What success actually looks like** — here, *not* the HTTP status
5. **The proof step** — an independent read-back, not a restatement of the write

Give those five and the AI produces a chain that catches real defects. Omit the fourth and it produces a
suite that is **90% green and 64% true**.
