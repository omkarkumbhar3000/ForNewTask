# ISSUE-005 — Two disjoint API surfaces; the entire microservices surface has no automated coverage

**Severity:** 🟠 Medium–High · **Type:** Test coverage gap · **Raised:** 2026-07-28
**Affects:** QA coverage strategy · **Owner:** QA, with a documentation dependency on development
**Evidence:** `../Coverage/coverage.json` · `../Coverage/coverage-by-request-type.md`

> ⚠️ **Superseding note — the endpoint count in this issue is stale.** Every `1,322` below should read
> **`1,306`**. `1,322` is the count of *route constants* in `APIConfig.java`; removing 13 surplus (11 paths
> declared by more than one constant) and 3 non-endpoints gives the canonical **1,306 distinct
> `(controller, action)` endpoints**. The figures are left as written because this issue is a dated record —
> read `1,306` wherever `1,322` appears. The derived percentage in §3 (`73 / 1,322 = 5.5%`) becomes
> `73 / 1,306 = 5.6%`, which changes no conclusion. Basis:
> `docs/analysis/A3-negative-validation.md` reconciliation · `.claude/rules/api-surface.md`.

---

## 1. Statement

The API surface the automation framework targets and the API surface the developers have documented in
Swagger are **almost entirely different APIs**. Only ~6% of operation names appear in both.

Consequence: roughly **690 documented, live operations have effectively no automated test coverage**, and
this was invisible until the Swagger links were shared.

## 2. The two surfaces

| | Legacy surface | Microservices surface |
|---|---|---|
| **Path shape** | `/api/<Controller>/<Action>` | `/api/<Service>/<Action>` behind `ARCONAPIGateway` |
| **Host/port** | `devint.arconnet.com:1602` | `devint.arconnet.com:1302` and `:555` |
| **Endpoint count** | **1,322** declared in `APIConfig.java` | **690** discovered from 37 live specs |
| **Swagger** | ⛔ None — Postman collection only | ✅ Yes, live and reachable |
| **Automated coverage today** | 465 test classes (79 positive + 386 negative) | ⛔ **≈ zero** |
| **Present in `pam/PAM` source** | 3.7% | not assessed — served by separate services |

## 3. Evidence of disjointness

Measured by comparing operation names between `APIConfig.java` and all 37 fetched specs:

| Measure | Result |
|---|---:|
| Distinct operation names in `APIConfig.java` | 542 |
| Distinct operation names in Swagger specs | 513 |
| Names appearing in **both** | **33** |
| …as % of Swagger names | **6.4%** |
| …as % of `APIConfig` names | **6.1%** |
| `APIConfig` endpoints whose name is documented in Swagger | 73 / 1,322 — **5.5%** |

Corroborating structural evidence: the shared Swagger sheet's own rows 94–98 list the legacy
`/api/ServiceDetails/…`, `/api/Configuration/…`, `/api/ActivityLogs/…` endpoints — the ones `APIConfig`
declares — on port **1602**, each marked:

> `Unavailable — No Swagger Links are available for this Module, Postman Collection is available`

So the developers' own sheet confirms the split: the legacy surface has no Swagger, the microservices do.

## 4. Coverage position

| Surface | Endpoints | Documented | Automated | Gap |
|---|---:|---|---:|---|
| Legacy (1602) | 1,322 | ⛔ | 465 test classes | Documentation gap — no contract to validate against |
| Microservices (1302/555) | 690 | ✅ | **102 after this run** (GET only) | **588 remaining**, all documented |
| **Combined** | **~2,012** | partial | — | — |

The microservices gap is the more tractable of the two: the contract exists, so validation is generatable.
This run has already taken it from 0 to 102.

## 5. Consequence

| Area | Impact |
|---|---|
| **Release risk** | An entire product surface — Vault, SCIM, UAG, Access Control, Digital Vault, Web Server Manager, User Discovery — ships without automated API regression coverage |
| **Reported coverage** | Any coverage figure quoted against `APIConfig` silently excludes 690 live endpoints, overstating true coverage |
| **Effort** | The gap is generatable, not hand-writable: 690 endpoints would be prohibitive manually and are routine by reflection over the specs |

## 6. Recommended action

| # | Action | State |
|---|---|---|
| 1 | Extend the harness to the remaining GET tier (+121, optional params only) | Ready — `--tier extended` |
| 2 | Add authentication so results reflect real behaviour, not 401s | ⬜ Blocked on a token |
| 3 | Extend to POST/PUT/PATCH/DELETE behind a default-deny allowlist | ⬜ Needs approval (341 POST) |
| 4 | Build the reflection runner over `APIConfig.java` for the legacy surface | ⬜ Designed |
| 5 | Ask development whether the legacy 1602 surface is **deprecated** | ⬜ **Do this first** — it may make item 4 unnecessary |

**Item 5 is the highest-value question in this issue.** If the 1,322-endpoint legacy surface is being
retired in favour of the microservices, the correct strategy is to invest in the documented surface and
freeze legacy coverage where it is. If it is *not* being retired, then 1,322 undocumented endpoints are a
standing risk that needs its own remediation plan.
