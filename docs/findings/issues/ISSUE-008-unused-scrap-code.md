# ISSUE-008 — Unused and scrap code in the automation framework and the product

**Severity:** 🟡 Low (no functional impact) · **Type:** Maintainability
**Raised:** 2026-07-28 · **Affects:** `pam_automation_bootstrap` and the product APIs
**Method:** every claim below is a measured reference count, not an impression

---

## 1. Unused Maven dependencies

Declared in `pom.xml`, with **zero references** anywhere in the 1,073 source files. Verified by recursive
search on both the package path and the primary type name, so a plain `import` and an unqualified usage
would both have been caught.

| Dependency | Version | References | Notes |
|---|---|---:|---|
| `com.influxdb:influxdb-client-java` | 6.11.0 | **0** | No `InfluxDB` type used anywhere |
| `org.apache.pdfbox:pdfbox` | 2.0.30 | **0 live** | `PDDocument`/`PDFTextStripper` appear **only inside commented-out code** — `AcmoHelperPage.java:2105-2106` |
| `org.json:json` | 20230227 | **0** | No `JSONObject`/`JSONArray`. Jackson is used instead |
| `net.java.dev.jna:jna` + `jna-platform` | 5.13.0 | **0** | No `Native.`/`Platform.` usage |
| `xml-apis:xml-apis` | 2.0.2 | **0** | Legacy XML shim, nothing references it |

**Deliberately excluded from this list** — these have zero `import` statements but are genuinely required:

| Dependency | Why it must stay |
|---|---|
| `com.mysql:mysql-connector-j` | Loaded at runtime by `DriverManager.getConnection(...)` — `DBUtils.java:27`, `ExtentReportListener.java:181` |
| `com.microsoft.sqlserver:mssql-jdbc` | Same — JDBC drivers are resolved by URL, never imported |
| `org.aspectj:aspectjweaver` | `runtime` scope, required by Allure |

## 2. Two competing HTTP stacks

| Stack | Usage | Verdict |
|---|---|---|
| Playwright `APIRequestContext` (via `ApiHelper`) | The whole API suite | ✅ The standard |
| **RestAssured** | **2 files only** — `pages/acmo/api/API_BaseClass.java`, `pages/acmo/api/APIServices.java` | 🟡 Legacy holdout |

RestAssured (`rest-assured` + `json-path`, 5.5.0) is carried as a dependency for two files. Either migrate
them to `ApiHelper` and drop both dependencies, or accept them and document why — but the current state
means two HTTP clients, two auth mechanisms and two assertion styles coexist in one framework.

## 3. Dead source files and blocks

| Item | Size | Evidence |
|---|---:|---|
| **`autoconfigs/APIConfigOld.java`** | 316 lines | Superseded by `APIConfig.java` (1,482 lines). Name declares its own obsolescence |
| **Commented-out code in `ApiHelper.java`** | **246 of 1,639 lines — 15.0%** | Includes a full superseded copy of `validateResponseErrorCode` and `validateApiResponseWithResponseTime_ExcelBasedsettingnegative` (~lines 1282–1394), sitting directly **above** the live versions |
| **`src/main/java/com/arcon/tests/App.java`** | 9 lines | Maven archetype "Hello World" stub. `src/main` is otherwise empty |
| **`logback.xml`** at repo root | 269 bytes | **Inert** — Logback is not on the classpath; logging is SLF4J → Log4j2 |
| **Orphaned test classes** | **218** | Exist under `tests/` but referenced by no suite XML, so TestNG never runs them. Down from 737. Catalogued in `../../docs/history/archive/workbench-archive/approach/orphans.md` |
| Commented-out `<class>` entries in suite XMLs | 3 | Against 781 active entries — minor |

**The commented-out block in `ApiHelper` is the most actively harmful item here.** A search for
`validateResponseErrorCode` returns the dead copy *first*, so anyone reading it draws conclusions about
behaviour from code that never executes.

## 4. A data defect in the endpoint catalogue

`APIConfig.java` declares a controller named **`Se0rviceDetailsV3`** — a typo for `ServiceDetailsV3`
(digit `0` substituted for the letter `r`). Every endpoint declared under it is unreachable, and it will
appear permanently in the excluded list of any reflection-driven runner.

## 5. Scrap on the product side

Cross-referenced from ISSUE-004, recorded here for completeness:

| Item | Evidence |
|---|---|
| `/WeatherForecast` — ASP.NET project-template sample endpoint | Live, **HTTP 200**, unauthenticated, on 3 published specs |
| 201 of 690 operations under the placeholder title `"Your API Name"` | 12 specs |

## 6. Recommended action

Order matters — item 1 is the only one with any real risk attached.

| # | Action | Risk |
|---|---|---|
| 1 | Delete the commented-out block in `ApiHelper.java` (~246 lines) | None — it is unreachable. Do this first; it actively misleads |
| 2 | Delete `APIConfigOld.java` after confirming no suite references it | None expected |
| 3 | Remove the 5 unused dependencies from `pom.xml`, then `mvn -o clean test-compile` to confirm | Low — verify, do not assume |
| 4 | Fix the `Se0rviceDetailsV3` typo | None |
| 5 | Delete `logback.xml` and `App.java` | None |
| 6 | Resolve the 218 orphans — register or delete, per `orphans.md` | Medium — needs a decision per class |
| 7 | Decide on RestAssound: migrate the 2 files or document the exception | Low |

Items 1–5 are mechanical and could be done in a single commit. Item 6 is the one that needs judgement and
is already sequenced as Phase 6 of the framework optimisation plan.

## 7. Note on scope

This issue is **maintainability only**. None of it affects test results or product behaviour. It is
recorded because the objective explicitly asked for unused/scrap code to be identified, and because items
1 and 4 cause active confusion rather than merely occupying space.
