# ISSUE-004 — SDLC adherence gaps evidenced in shipped API artefacts

**Severity:** 🟠 Medium (individually) / 🔴 High (as a pattern) · **Type:** Process
**Raised:** 2026-07-28 · **Affects:** the API development lifecycle, not one component
**Evidence:** `../Execution/spec_quality.json` · `../Execution/specs/` (37 cached specs) · `Evidence/*.json`

---

## 1. Statement

No single item below is severe. Taken together they indicate that API artefacts reach a shared
environment without a definition-of-done covering documentation, scaffold removal, or error handling.
Each is objectively verifiable from artefacts the development team themselves published.

## 2. Evidence table

| # | Observation | Measurement | What it implies |
|---|---|---:|---|
| **A** | **ASP.NET scaffold code is live** — `/WeatherForecast`, the default Visual Studio project template endpoint, responds **HTTP 200** | 3 live instances | New services are created from the template and shipped without removing sample code. No review step catches it |
| **B** | **Swagger metadata never configured** — 201 of 690 operations sit under the literal placeholder title `"Your API Name"` | **201 / 690 = 29.1%**, across 12 specs | Swagger was enabled but never filled in. Documentation is not part of done |
| **C** | **No `operationId` anywhere** | **0 / 690** | Blocks every standard client-generation and contract-testing tool. Suggests generated docs are never consumed by tooling |
| **D** | **No error response declared anywhere** | **0 / 690** | See ISSUE-001. The contract documents only the happy path |
| **E** | **Error handling inconsistent between services** — some return a JSON envelope, others bare text | 47 / 102 bare text | No shared middleware or cross-service standard; each team solved it differently or not at all |
| **F** | **Self-contradictory payloads reach a shared environment** | 10 / 102 (ISSUE-003) | `StatusCode: 401` with `Message: "Success"` is catchable by one unit test. None exists |
| **G** | **Health endpoints time out** | 11 endpoints returned nothing in 20 s | `getPulse` exists as a health check but is not itself monitored — see ISSUE-006 |
| **H** | **Version string is a placeholder** | Every envelope reports `"Version":"1.0.0.0"` | Build version is not stamped, so no response can be attributed to a build |
| **I** | **The hand-off artefact is unreviewed** | 45/98 rows duplicate; 7 malformed URLs; 1 row marked `Done` whose comment says no Swagger exists | See ISSUE-007 |

## 3. The `/WeatherForecast` finding in detail

`/WeatherForecast` is the sample endpoint Visual Studio generates in every new ASP.NET Core Web API
project. It returns randomised fake weather data and has no business purpose.

```
HTTP 200   ARCON PAM SCIM API   GET /WeatherForecast
HTTP 200   ARCON PAM SCIM API   GET /WeatherForecast
HTTP 200   ARCON PAM SCIM API   GET /WeatherForecast
```

It is **documented in the published Swagger specification**, meaning it is a deliberate part of the
declared API surface rather than merely an un-routed leftover. It is reachable **without
authentication** — 200, not 401 — while genuine business endpoints on the same services correctly
return 401.

That combination — unauthenticated, documented, live, purposeless — is the clearest single piece of
evidence for this issue.

## 4. What is *not* being claimed

This is not a competence judgement, and it is not a claim that the API does not work. The functional
endpoints behave sensibly, and the microservice decomposition is coherent. Every item above is a
**process** gap — the absence of a checklist that would have caught cheap, mechanical problems before
they reached a shared environment.

## 5. Recommended fix — a definition of done for an API change

| # | Gate | Catches |
|---|---|---|
| 1 | Swagger title, version and description are set; no placeholder text | B, H |
| 2 | Every operation declares `operationId` and at least one error response | C, D |
| 3 | No template/scaffold routes remain (`/WeatherForecast`, sample controllers) | A |
| 4 | Error path returns the shared JSON envelope with `Content-Type` | E |
| 5 | One unit test per service asserts the failure path emits a non-success message | F |
| 6 | `/getPulse` responds under 1 s, monitored | G |
| 7 | Build version stamped into the envelope from CI | H |

Gates 1–5 are static checks and could be enforced in CI against the generated `swagger.json` without any
manual review effort.

## 6. Suggested handling

Raise under `PAMIT` as a process item with the seven gates as the acceptance criteria, and attach this
folder as evidence. The per-module developer owners are listed in the shared Swagger sheet
(`data/sources/Automation PAM Endpoints Details_Shared(Swagger_JSON Links).csv`, columns 10–13).
