# ISSUE-006 — Health endpoints time out at 20 seconds

**Severity:** 🟠 Medium · **Type:** Runtime / performance defect · **Raised:** 2026-07-28
**Affects:** 27 of 102 endpoints breached the 2 s SLA; 11 returned nothing at all
**Independent of authentication:** ✅ yes — a timeout is not an auth outcome
**Evidence:** `Evidence/*.json` (`response.latency_ms`) · `../Excel/…xlsx` → Results, `L7_latency`

---

## 1. Statement

`getPulse` is the health-check endpoint pattern used across the microservices. Several instances **do not
respond within 20 seconds**, which is the harness timeout. A health check that cannot answer is worse than
no health check — it will fail any orchestrator liveness probe and cannot be used for readiness gating.

## 2. Evidence

| Measure | Result |
|---|---:|
| Fastest response | **39 ms** |
| Slowest observed | **20,483 ms** |
| Breached the 2,000 ms SLA | **27 / 102 — 26.5%** |
| Returned nothing within 20 s (no response at all) | **11 / 102 — 10.8%** |

Slowest eight, all at or beyond the 20 s timeout ceiling:

```
20,483 ms   GET /api/Review/getPulse
20,124 ms   GET /api/ServiceGroup/getPulse
20,095 ms   GET /api/UserDiscovery/getPulse
20,084 ms   GET /api/Envelope/ScheduledPasswordEnvelope
20,080 ms   GET /api/Dashboard/getPulse
20,080 ms   GET /api/CommandLogs/getPulse
20,077 ms   GET /api/Reports/getPulse
20,043 ms   GET /api/CustomCommand/getCustomPasswordTags
```

**Six of the eight slowest are `getPulse` health endpoints.**

For contrast, `getPulse` on other services answers immediately:

```
     3 ms … 560 ms   /api/SSHCertificate/getPulse, /api/WindowsCertificate/getPulse,
                     /api/DigitalVault/getPulse, /api/Sdk/getPulse
```

So the pattern is implemented efficiently in some services and pathologically in others.

## 3. Interpretation — stated with appropriate caution

The clustering at ~20,000 ms means these calls hit the harness timeout rather than returning a slow
success. The harness cannot distinguish between:

- the service being genuinely unresponsive,
- a cold-start penalty on a shared dev environment,
- a network path issue to that particular service, or
- the service waiting on a downstream dependency that is itself down.

**This should be confirmed against a warmed environment before being escalated to the development team.**
What is certain is that 11 endpoints produced no response in 20 seconds on a dev environment, and that
41 `getPulse` endpoints exist of which only 25 returned a healthy result.

Because latency is now recorded per endpoint per run, a second run will show immediately whether this is
cold-start or persistent — that is the cheapest way to settle it.

## 4. Consequence

| Area | Impact |
|---|---|
| **Orchestration** | A 20 s health check fails standard liveness/readiness probes; containers would be killed and restarted in a loop |
| **Monitoring** | Health cannot be polled at any sensible interval |
| **This QA effort** | Latency baselining is unreliable until this settles; 11 endpoints yield no validation result at all |

## 5. Recommended action

| # | Action | Owner |
|---|---|---|
| 1 | Re-run against a warmed environment to separate cold start from a persistent fault | QA — one command |
| 2 | If persistent: profile why `getPulse` blocks; a health check should not touch a database or a downstream service | Development |
| 3 | Set an explicit SLA for `getPulse` (suggest < 500 ms) and monitor it | Development |
| 4 | Confirm whether the 11 non-responders are deployed at all on devint | Development |

Action 1 costs nothing and should precede any escalation.
