# ISSUE-011 — `SetStatus` is a state-changing operation exposed over HTTP GET, on 49 controllers

**Severity:** 🟠 Medium (correctness + security posture) · **Type:** API design defect
**Raised:** 2026-07-28 · **Environment:** `QA_MsSQL` (declaration is environment-independent)
**Evidence:** `APIConfig.java` verb comments · `../Excel/QA_MsSQL_API_Validation_Results.xlsx` → Coverage
**Found by:** the Module × Request-type × Model coverage analysis, not by execution

---

## 1. Statement

`SetStatus` — by name and by the symmetry of the `GetStatus`/`SetStatus` pair, an operation that **changes
server state** — is declared and exercised as **HTTP GET** on **49 controllers**.

From `APIConfig.java`:

```java
public static String getStatus = "/api/ActivityLogs/GetStatus";   // get
public static String setStatus = "/api/ActivityLogs/SetStatus";   // get     <-- mutation over GET
```

The `// get` comment is the framework's verb declaration, and it is what the runner dispatches on.

## 2. Scale

| Action | Controllers | Declared verb |
|---|---:|---|
| `GetStatus` | 49 | GET — appropriate |
| **`SetStatus`** | **49** | **GET — inappropriate** |

49 of the 325 declared GET endpoints (15%) are `SetStatus`.

## 3. Why it matters

HTTP GET is defined as **safe** and **idempotent**. Infrastructure everywhere relies on that guarantee:

| Mechanism | Assumption it makes | Consequence when GET mutates |
|---|---|---|
| Browser / proxy / CDN caching | GET responses are cacheable | A cached `SetStatus` silently stops taking effect, or replays |
| Prefetch and link preview | GET is free to speculatively fetch | State changes triggered without user intent |
| Retry on timeout | GET is safe to repeat | A timed-out mutation is retried, applying twice |
| CSRF protection | Mutations use POST/PUT/DELETE with a token | A GET mutation is trivially triggerable cross-site via `<img src>` |
| Server logs | Query strings are logged in full | Any parameters to the mutation land in access logs |
| Read-only test policy | GET is safe to execute freely | **A "GET-only" validation run silently mutates state** |

The last row applies directly to this project. Our own default-deny policy auto-includes GET as read-only —
but 49 of those GETs are mutations. **The Phase 1 GET run was not, in fact, entirely read-only.**

## 4. ⚠️ What actually happened in this run

`SetStatus` was included in the 325-endpoint GET run. In practice **no mutation occurred**, because the
application pool had already stopped and every `SetStatus` call returned IIS `503` before reaching
application code — confirmed in `Evidence/legacy-qa_mssql/`.

That is luck, not design. On a healthy environment the same run would have invoked 49 state changes while
believing itself read-only.

## 5. Cannot be confirmed against the source

The implementing controllers are not in the developer snapshot — `pam/PAM` contains 3.7% of this API
(ISSUE-005), and no `SetStatus` action appears in it. So what `SetStatus` actually changes, and whether it
requires a parameter, cannot be determined here.

**Two possibilities, and they need different responses:**

| If… | Then |
|---|---|
| `SetStatus` genuinely mutates state | 🔴 It must become `POST`/`PUT`, and the harness must treat it as mutating |
| `SetStatus` is a misnomer that only *reads* a status | 🟡 Rename it, or document it — but it should not be called `Set*` |

**The developer must confirm which.** Until then the harness assumes the first, which is the safe reading.

## 6. Harness change made in response

`SetStatus` is now treated as **mutating regardless of its declared verb** and is excluded from GET runs
under default-deny. It is reported as
`EXCLUDED — name implies mutation; default-deny pending developer confirmation (ISSUE-011)`.

This costs 49 endpoints of apparent GET coverage. That is the correct trade: coverage that mutates state
while claiming to be read-only is worse than no coverage.

## 7. Required action

| # | Action | Owner |
|---|---|---|
| 1 | **Confirm whether `SetStatus` mutates state** — one answer settles 49 endpoints | Development |
| 2 | If it mutates: change to `POST`, update `APIConfig.java`'s verb comments, and treat as mutating everywhere | Development + QA |
| 3 | If it only reads: rename to `GetXxx` or document explicitly | Development |
| 4 | Audit the remaining catalogue for other `Set*`/`Update*`/`Insert*`/`Delete*` actions declared `// get` | QA — mechanical check |
| 5 | Re-affirm the read-only guarantee for GET runs once resolved | QA |

## 8. Related

- `ISSUE-010` — the app-pool crash, which masked the mutations in this run
- `ISSUE-005` — why the implementing source cannot be inspected
- `ISSUE-001` — the same catalogue declares only `200` and no error codes
