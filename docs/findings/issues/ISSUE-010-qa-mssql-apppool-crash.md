# ISSUE-010 — 🔴 CRITICAL: two GET requests hang for 30 s and stop the IIS application pool

**Severity:** 🔴 **Critical** · **Type:** Availability / stability defect · **Raised:** 2026-07-28
**Environment:** `QA_MsSQL` — `https://u16hf.arconnet.com:6302`
**Status at time of writing:** ⛔ **environment DOWN and DEGRADING** — see §3.1
**Evidence:** `Evidence/legacy-qa_mssql/001..003_*.json` (the three decisive calls) + 322 × 503
**Reproduce:** ⚠️ **do not reproduce casually** — it takes the environment down. See §6.

---

## 1. Statement

Two read-only GET endpoints hang indefinitely. Calling them in sequence causes the IIS application pool
serving the PAM API to **stop**, after which the entire API returns `503 Service Unavailable` and does not
recover without intervention.

**Three requests were enough to take down the whole API.** This was not a load test — requests were issued
strictly sequentially, one at a time, with no concurrency.

## 2. The exact sequence

| # | Endpoint | HTTP | Latency | Outcome |
|---:|---|---|---:|---|
| 1 | `GET /api/ActivityLogs/GetDatabaseStatus` | **200** | 614 ms | ✅ Healthy. Body: `"Success": true, "Message": "Database Connected, ARCOSDB : True ALT Db: True"` |
| 2 | `GET /api/ActivityLogs/GetErrorLogs` | **none** | **30,020 ms** | ⛔ Hung — no response, client timeout |
| 3 | `GET /api/ActivityLogs/GetLogs` | **none** | **30,170 ms** | ⛔ Hung — no response, client timeout |
| 4 | `GET /api/ActivityLogs/GetSsmVideoPath?filname=5764` | **503** | 82 ms | ⛔ Pool stopped |
| 5–325 | *everything else* | **503** | 17–82 ms | ⛔ Pool stopped |

Call #1 proves the API and its database connection were **healthy** immediately before the failure.
Calls #2 and #3 each consumed the full 30 s client timeout. From #4 onward the API was gone.

## 3. Why this is an application-pool stop, not overload

| Observation | What it rules out |
|---|---|
| 503 responses return in **17–82 ms** | Not saturation — a loaded server responds slowly, it does not refuse instantly |
| 503 body is an **IIS HTML page** (`<TITLE>Service Unavailable</TITLE>`), not an application response | The request never reached application code — IIS itself is refusing |
| Requests were **strictly sequential**, never concurrent | Not a connection-pool or thread-pool exhaustion from parallelism |
| Only **3** requests preceded the failure | Not cumulative load |
| Still 503 on isolated probes **long after** the run finished | Not transient; the pool has not auto-recovered |

This is the signature of IIS **rapid-fail protection**: the worker process crashed repeatedly within the
failure interval, so IIS stopped the pool and now refuses all requests at the front door.

### 3.1 ⛔ It then degraded further — both ports now refuse TCP

The environment did not stay at 503. Timeline of observed states:

| Time | `:6302` (API) | `:1302` (application + Swagger) |
|---|---|---|
| Before the run | ✅ HTTP 200, 1,055 ms | ✅ HTTP 200, Swagger served |
| Calls #2–#3 | ⛔ hung, 30 s each | not probed |
| Calls #4–#325 | ⛔ HTTP 503 (IIS HTML), 17–82 ms | not probed |
| After the run | ⛔ HTTP 503, still IIS answering | not probed |
| **Latest probe** | ⛔ **TCP connection refused** (`WinError 10061`) | ⛔ **TCP connection refused** |

The progression **503 → connection refused** matters: at 503 IIS was still listening and rejecting; now
**nothing is listening on either port**. So this is no longer confined to the API application pool — the
IIS site(s), or the web stack on `u16hf`, are stopped.

`:1302` was serving the application URL *and* the ARCONAPIGateway Swagger specs before the run and is now
also gone, so the impact extends past the endpoints that were called.

**This raises severity from "one pool needs restarting" to "the host's web services need investigation."**
Whether the second-stage failure is a consequence of the first, or someone intervened mid-way, cannot be
determined from the client side — §7 item 2 (the event log) is the only way to settle it.

## 4. Probable cause — stated with its evidence and its limits

**Evidence-backed:** `GetLogs` and `GetErrorLogs` accept **no parameters at all** — no page, no page size,
no date range, no row limit. Verified across the whole catalogue:

```
/api/ActivityLogs/GetErrorLogs      (no query string)
/api/ActivityLogs/GetLogs           (no query string)
```

An unparameterised log-retrieval endpoint can only mean *return everything*. Against a log table of any
realistic size on a long-lived QA environment, that produces an unbounded query and an unbounded
serialisation — which will exhaust the worker process. Two such calls back-to-back crashing the pool is
consistent with that.

**What cannot be confirmed from here:** the implementing source is **not in the developer snapshot**. The
`ActivityLogs` controller in `pam/PAM` (`OfflineMultiTabService/OfflineAPI/Controllers/ActivityLogsController.cs`)
implements only `InsertSSMLogs` — `GetLogs` and `GetErrorLogs` are absent, consistent with the
96%-not-in-repo finding in ISSUE-005. So the query itself cannot be inspected. **The developer must confirm
the root cause from the IIS/application event log** (see §7).

Correlating artefacts that *are* in the repo, for orientation:

| Artefact | Path | Relevance |
|---|---|---|
| `DBScripts.GetDatabaseStatus(...)` returning a `DataTable` | `ARCON_Services/DBSyncService/ARCOSDBSyncCommon/ARCOSDBSync/DBScripts.cs:103` | Shows the codebase's prevailing pattern: return a whole `DataTable`, unbounded |
| `ActivityLogsController` | `OfflineMultiTabService/OfflineAPI/Controllers/` | The controller family exists; the two failing actions do not |

## 5. ⚠️ Blast radius — this is not two endpoints

The five actions `GetDatabaseStatus`, `GetErrorLogs`, `GetLogs`, `GetStatus`, `SetStatus` are a **shared
diagnostic pattern repeated across ~49 controllers**:

| Action | Controllers exposing it | Declared GET |
|---|---:|---:|
| `GetDatabaseStatus` | 48 | 48 |
| `GetErrorLogs` | **49** | **49** |
| `GetLogs` | **49** | **49** |
| `GetStatus` | 49 | 49 |
| `SetStatus` | 49 | 49 |

Consequences:

- **98 `GetLogs`/`GetErrorLogs` endpoints have no query parameter** and therefore carry the same
  unbounded-query risk. Two of them are confirmed to hang.
- **245 of the 325 declared GET endpoints (75%)** are this shared pattern. The QA_MsSQL GET surface is
  three-quarters repeated diagnostic scaffolding.
- If the cause is in a shared base controller, **one fix addresses all 98**. If each is separately
  implemented, 98 need fixing.

## 6. ⚠️ Reproduction — handle with care

```
GET https://u16hf.arconnet.com:6302/api/ActivityLogs/GetErrorLogs
Authorization: Bearer <token>
```

**One request is expected to be sufficient to hang a worker.** Two stopped the pool. Do **not** run this
against any shared or production environment. To reproduce safely, isolate a single instance, attach a
profiler or capture the SQL, and be prepared to restart the pool.

The validation harness now has this endpoint family on its blocklist — see §8.

## 7. Required action

| # | Action | Owner | Priority |
|---|---|---|---|
| 1 | **Restart the application pool** on `u16hf:6302` to restore QA_MsSQL | Infrastructure / QA | 🔴 Immediate — the environment is unusable |
| 2 | Retrieve the **IIS application event log** and the **worker-process crash dump** for the window around the failure. This gives the actual exception and settles §4 | Development | 🔴 High |
| 3 | Capture the **SQL executed** by `GetLogs` / `GetErrorLogs` (SQL Profiler / Extended Events) and check for a missing `TOP`/`OFFSET FETCH` | Development | 🔴 High |
| 4 | Add **mandatory paging parameters** (`pageNumber`, `pageSize`, with a server-side maximum) to `GetLogs` and `GetErrorLogs` across all 49 controllers | Development | 🔴 High |
| 5 | Add a **server-side query timeout** and a **row cap** so no single request can exhaust a worker | Development | 🟠 Medium |
| 6 | Confirm whether the five diagnostic actions come from a **shared base controller** — determines whether this is a 1-line fix or 98 | Development | 🟠 Medium — answer first, it changes the plan |
| 7 | Enable **IIS pool auto-recovery** / health monitoring so a crash does not leave the API dead indefinitely | Infrastructure | 🟠 Medium |

## 8. Harness change made in response

`GetLogs` and `GetErrorLogs` are now **blocked in endpoint resolution** for QA_MsSQL, so no future run can
take the environment down again. They are reported as `EXCLUDED — blocked: known to hang and stop the app
pool (ISSUE-010)`, never silently skipped.

Once §7 item 4 is delivered, remove the block and the 98 endpoints re-enter coverage automatically.

## 9. Impact on this run's results

**The QA_MsSQL validation results are not a usable assessment of API quality.** Only 1 of 325 endpoints
returned a real response; 322 returned IIS 503 and 2 timed out. Those 503s say nothing about the endpoints
that received them.

The run's value is this defect. Coverage figures will be regenerated once the environment is restored.
