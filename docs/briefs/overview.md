# Overview — PAM Dynamic API Automation

**Purpose:** one document covering everything built so far, for the demo.
**Workspace:** `E:\Omkar\Automation\Dev Project` · **Jira:** `PAMIT` · **Environment:** `QA_MsSQL` — `https://u16hf.arconnet.com:6302`
**Latest execution (N):** `2026-08-05_114315` — **747 flows · 5,430 cases · 5,416 executed · 1,388 endpoints ·
5 h 29 m** (`OBJ-010`)
**Previous (N-1):** `2026-07-29_181439` — 326 flows · 1,868 calls · 870 endpoints · 3 h 11 m
**Benchmark:** `docs/management/summary/OBJ-010-Execution-Benchmark.md`
**Last updated:** 2026-08-05

---

## 0. The one-paragraph version

We generate API test chains instead of writing them. A generator reads the automation framework's own
endpoint catalogue and payload helpers, emits multi-step flow definitions as data, and a generic executor
runs them against the live PAM API — carrying real values from each response into the next request. Every
call is assessed on seven layers rather than its status code, because this product answers **HTTP 200 for
rejected requests**. The latest full run made **5,416 calls across 1,388 endpoints** and found **1,022 cases
(18.9%) that returned HTTP 200 while failing validation** — every one of which a status-only suite would call
green. It also found **19 endpoints that accept an invalid bearer token**, 6 of them writes.

---

## 1. Why this exists — the finding that drives the design

| | |
|---|---:|
| | 2026-08-05 (N) | 2026-07-29 (N-1) |
|---|---:|---:|
| Calls issued | **5,416** | 1,868 |
| Returned HTTP 200 | 2,714 (50%) | **1,688 (90%)** |
| **HTTP 200 yet failed validation** | **1,022 (18.9%)** | 289 + 115 + 4 |
| **Passed all layers** | **3,459 (63.9%)** | **1,204 (64%)** |

The pass rate barely moved while coverage nearly tripled — and the dimension the two runs share scored
**63.9% against 64.2%**.

A conventional status-code suite would have reported that run as **90% green**. The 26-point gap is 406
calls that failed while returning 200. This is measured, with one evidence file per call.

---

## 2. The five folders

The workspace is **not a repository** — it holds two independent git checkouts plus unversioned working
material.

| Folder | What it is | Editable? |
|---|---|---|
| `Automation gitlab repo/pam_automation_bootstrap/` | The QA automation framework — Java 21 · Playwright · TestNG · Maven. **The only editable code**, on branch `AI` | ✅ |
| `pam/` | The developer's product repository (.NET). Reference only | ⛔ Never |
| `workbench/` | All internal working material, **including every harness script** | ✅ |
| `BLAST/` | Requirement intake framework — how work is commissioned | ✅ |
| `Reports/` | Measured evidence, one dated folder per execution | 🔄 Generated |
| `artifacts/graph/` | Graph views of the code and the API surface | 🔄 Generated |
| `data/sources/` | Source PDFs, the Swagger link CSV, the Confluence API reference | ✅ Add only |

Release path: **develop on `AI` → owner reviews → owner merges to `Dev` → owner copies into
`pam/AutomationTesting/`.** Only the first step is ours. Never push, never merge.

---

## 3. The automation framework (developer-repo automation)

Single-module Maven project. **1,073 Java files**, all under `src/test/java` — `src/main` holds only an
unused archetype stub.

| Component | Detail |
|---|---|
| `utils/BaseTest` | ~1,300 lines — thread-local Playwright state, ~40 page-object getters. Every UI test extends it |
| `utils/ApiHelper` | ~1,640 lines — **extends `BaseTest`**, so API tests inherit browser machinery they never use. HTTP client, `getToken()`, 66 payload getters |
| `autoconfigs/APIConfig` | **1,307 unique endpoint declarations** across 70 controllers |
| `utils/apiPayload/` | 66 payload helpers, 1,289 zero-arg methods holding literal request JSON |
| Suites | `API_Suites/` (78) · `CICD_Suites/` (4) · `CRUD_Suites/` (12) · `E2E_Suites/` (8). No root `testng.xml` |
| Environments | 20 `Environments/*.properties` files |

API tests use Playwright's `APIRequestContext`, **not** REST Assured (declared but effectively unused).

**Verb reality:** the API declares **POST 992 · GET 325 · PUT 2 · DELETE 2 · PATCH 0**. So GET + POST
covers 99.7% of the surface — "all request types" is essentially those two.

### Two known defects in the Java path

1. `APIExcelReportUtil` increments a static `rowIndex` without synchronisation while suites run
   `parallel="classes"`.
2. `ApiHelper` calls `Playwright.create()` per request without closing it.

---

## 4. The dynamic generation pipeline — the core of the work

```
APIConfig.java  (1,307 endpoints)  ─┐
utils/apiPayload/*.java (1,289)    ─┼─►  generate_flows.py  ──►  flows/generated/*.json
Environments/QA_MsSQL.properties   ─┘         (derives)              (326 flows, 2,067 hops)
                                                                            │
                                          chain_runner.py  ◄────────────────┘
                                          (generic executor)
                                                 │
                    substitute → call → extract → assert → carry forward
                                                 │
                              artifacts/runs/<timestamp>/  (report + evidence)
```

**The key design decision: flows are data, the executor is code.** The runner knows nothing about users,
services or LOBs. A generator that emits more flow JSON needs no runner change, and hand-written flows keep
working unchanged — so nothing built by hand is discarded when generation expands.

### What each script does

| Script (`tools/`) | Role |
|---|---|
| `generate_flows.py` | Derives flow definitions from the catalogue + payload helpers |
| `chain_runner.py` | Executes flows, asserts seven layers, writes evidence |
| `run_qa_mssql.py` | Legacy surface sweep, GET tier |
| `run_validation.py` | Swagger surface, schema-based. The other two import its validator |
| `run_chains.py` | Chains derived from the API graph |

### How a value is chained

| Mechanism | Example |
|---|---|
| `extract` — dotted selector | `Result[0].ServerGroupId` |
| `find_extract` — filtered row join | find the user group whose `LOBName` equals the LOB name from hop 1 |
| `extract_any_id` — resolved at run time | generated flows don't know if a create returns `UserId` or `ServiceId` |
| `verify_present` / `verify_value_anywhere` | prove the created record exists downstream |

Field lookups are case-insensitive because the API spells the same field `UserId`, `UserID`, `LobId`,
`LOBID` and `LOBid` across controllers.

### The proven five-level chain

```
GetLOBList → LobId 108   ·   GetServerGroupList → ServerGroupId 282
  → SetServiceDetails → ServiceId 25339 "Inserted Successfully"
  → GetServiceDetails → ServiceSessionId 75277
  → GetActiveServicesByLOBId → ServiceId 25339 FOUND under LOB 108
```

The user chain closed the loop by itself: the created user's record came back carrying
`UserLOBId: 108` and `UserGroupId: 199` — the exact values discovered in hops 1–2.

---

## 5. The seven validation layers

| Layer | Check | Why |
|---|---|---|
| **L1** `http-status` | Actual vs expected | Weakest. Never sufficient alone |
| **L2** `content-type` | JSON declared ⇒ JSON returned | Catches HTML/plaintext error pages |
| **L3** `envelope` | `Success` true, or `errorCode` known-good | **The one that matters here** |
| **L4** `message-semantics` | `Message` confirms the intent | `Success: true` + `"Already Exists"` created nothing |
| **L5** `chain-key-extracted` | The next hop's value was found | A chain silently losing its key would otherwise pass |
| **L6** `record-exists` | The created record is in a later read | Proves persistence, not mere acceptance |
| **L7** `latency` | Within the per-hop budget | Writes take 5–7 s here |

### Eight response shapes — measured, not assumed

| # | Shape | Example |
|---:|---|---|
| 1 | `{Program, Version, DateTime, Success, Message, Result[]}` | `GetAllActiveUserList` |
| 2 | Same, no `Message` | `GetLOBList` |
| 3 | Same, `Result` an object | `GetServiceDetails` |
| 4 | Bare array, no envelope | `DeviceOnboarding/GetLOBList` |
| 5 | `{Success:false, ErrorCode, ErrorMessage}` at HTTP 200 | `InsertSSMLogs` — `902-ALC-ISSML` |
| 6 | `{aaData, aaData1, aaData11}` DataTables style | `GetAccessControlLogs` |
| 7 | `{"Output": "1\|Parameter error occurred..."}` | `SetPAMUserDetails` |
| 8 | Bare `false`, or bare `""` | `InsertPsrBulkLogs` |

The framework's `KNOWN_ERROR_CODES = {201,202,203}` is **materially incomplete** — `206-LC_GLD` and
`902-ALC-ISSML` were both observed.

---

## 6. Safety model — deny by default

| Control | Setting |
|---|---|
| **Plan-only default** | A bare run issues **zero** HTTP calls; `--execute` required |
| Blocklist | `GetLogs`, `GetErrorLogs`, `GetAllActiveUserDetails` — never built into a request |
| Destructive names | Refused unless explicitly permitted |
| Throttle | 5 s between calls (configurable, dynamic pacing available) |
| Circuit breaker | Pause after 3 consecutive 5xx/timeouts |
| Downtime | Wait 300 s, probe, **resume from the paused hop** — never restart |
| Checkpointing | After every flow; `--resume <folder>` skips completed work |
| Token | Generated **once** per run, cached 24 h |
| Secrets | Redacted before any disk write |

`GetLogs`/`GetErrorLogs` hang 30 s and **stop the IIS application pool** (ISSUE-010). The token rule exists
because repeated `/arcontoken` calls **locked the service account** on 2026-07-28.

**Proven in the last run:** the environment went down **three times**; each time the runner waited, probed,
and resumed from the paused hop. Zero restarts, zero lost work.

---

## 7. BLAST — how requirements enter

`BLAST/` is the intake framework. The owner writes the requirement in `Objective.md` and runs:

> Run `Objective.md` by referring to `blast.md`, and give me the output.

Since 2026-08-03 that file is **auto-loaded** — imported by the root `CLAUDE.md` and re-injected on every
prompt — so saving an edit is enough; the run command is optional.

Five phases: **B**lueprint → **L**ink → **A**rchitect → **S**tylize → **T**rigger.

| Rule | Effect |
|---|---|
| **Protocol 0 HALT** | No tool-writing until the five Discovery questions are answered, the schema is in `LLM.md`, and `task_plan.md` holds an approved Blueprint |
| `Objective.md` is dynamic | Rewritten per requirement. Auto-loaded every prompt. Always read fresh — never assume last run's objective |
| `docs/history/README.md` | **Append-only** history of every instruction, decision and measurement since Day 1 (workspace root) |
| Memory files | `LLM.md` (law) · `task_plan.md` (phases) · `findings.md` (discoveries) · `progress.md` (append-only history) |
| Precedence | The workspace `CLAUDE.md` outranks `LLM.md`. A run **ends committed on `AI`** — never pushed |

Parameter reference: `BLAST/Objective.md` §Parameters.

---

## 8. Graphify — three graph layers

| Layer | Scope | State |
|---|---|---|
| `pam-scope/` | `pam/PAM` product code | ✅ 112,628 nodes · 269,879 edges |
| `api-graph/` | API surface + chaining candidates | ✅ 1,322 endpoints · 1,680 candidates |
| `dev-scope/` | Whole workspace, cross-repo | ⬜ Marker only, not built |

Plus the automation repo's own graph at `pam_automation_bootstrap/graphify-out/` — **17,275 nodes ·
46,905 edges**, exposed through a `graphify` MCP server. All graphs are AST-only: **zero token cost.**

⚠️ The 1,680 chain candidates are **name-inferred** (a field name appearing in two places) and were **not**
used by the generator — it pairs create→read structurally instead, which is more reliable. Suite XMLs are
not indexed; Graphify has no XML parser.

---

## 9. Reports — the evidence layer

```
Reports/
  Runs/<YYYY-MM-DD_HHMMSS>/     one folder per execution, RETAINED FOREVER
      RUN_REPORT.md             verdicts, coverage, failure detail
      results.json              machine-readable, diffable between runs
      checkpoint.json           resume point
      evidence/*.json           one file per hop: request, response, verdict (redacted)
  Summary/                      management-facing, authored
  Issues/                       11 defect write-ups with citable evidence
  _archive-pre-2026-07-29/      everything from before the retention change
```

**Nothing is deleted or overwritten.** Auto-delete was removed from every harness on 2026-07-29. Run-folder
suffixes name the producer: no suffix = `chain_runner`, `_legacy-get`, `_swagger`, `_derived-chains`.

---

## 10. Workbench — the working layer

```
workbench/
  scripts/          EVERY harness script + flows/ (hand-written and generated/)
  rag/              data/sources extracted to page-cited text + query.py
  skills/           *.SKILL.md target-architecture specs
  archive/          frozen superseded planning material
  react/            placeholder
  overview.md       this file
```

### How Reports and Workbench work together

| | Workbench | Reports |
|---|---|---|
| Holds | The **machinery** — scripts, flow definitions, indexed docs | The **evidence** — what happened when it ran |
| Lifecycle | Edited deliberately | Generated per run, never edited |
| Retention | Version-free working material | Every run retained forever |

One direction of flow: **`tools/` executes → writes into `artifacts/runs/<timestamp>/`.**
Reports never writes back into Workbench. That separation is what makes a run reproducible: the machinery
is inspectable, the evidence is immutable.

---

## 11. Knowledge sources indexed

| Source | Size | What it gives |
|---|---:|---|
| `PAM API (Internal Team).pdf` | **2,470 pp** | The API reference — **3,194 parseable JSON payloads**, 1,097 distinct fields |
| `PAM Administrative Guide.pdf` | 702 pp | Access model, module taxonomy. No endpoints |
| `Client Manager Guide.pdf` | 399 pp | Client behaviour. No endpoints |
| Swagger link CSV | 37 specs, 690 ops | A **different** API surface — ~6% name overlap with `APIConfig.java` |

Query: `python tools\rag\query.py find "<terms>"`. Cite as `<doc>:p<N>`.

---

## 12. Where the work stands

| Area | State |
|---|---|
| Chaining proven end to end | ✅ 5 levels, user + service created and verified |
| Generation at scale | ✅ **747 flows, 5,590 cases, 1,388 endpoints**, 122 of 122 modules |
| **Negative / boundary generation** | ✅ New under `OBJ-010` — `generate_data_flows.py`, **2,124 negative cases** from the QA team's authored Excel scenarios. `generate_flows.py` emits positive flows only |
| Seven-layer validation | ✅ Operating in the harness; **31** response shapes catalogued *(was stated as 8)* |
| **Twelve-layer validation in the framework** | ✅ New under `OBJ-007` — `com.arcon.utils.validation`, 15 tests passing against real captured responses |
| Retention + resume + safety | ✅ Survived **17** downtime pauses and a mid-run crash; resumed from the checkpoint, re-queued 3 aborted flows, lost nothing |
| **Create payloads** | 🟡 **13 of 217 work** — stale literals; **79** have no body at all *(was stated as 101; 138 + 101 exceeded the 217 total)* |
| **Endpoint catalogue accuracy** | 🟡 **348 of 1,388 endpoints exercised return 404** (25.1%) — declares endpoints the deployment does not serve. Measured as 135 on the narrower N-1 run |
| ⛔ **Authentication** | 🔴 **19 endpoints accept an invalid bearer token**, 6 of them writes — `LH-13`. The 1,153 existing `*_UnauthorizedAccess` tests were all inert because they sent a *valid* token |
| **Documentation** | 🟡 **70% of endpoints undocumented**; only **3** error codes documented *(was stated as 4 — two were IP-address fragments)* |
| **Database validation** | ✅ Proven possible under `OBJ-007`; the API's writes do land in `ARCOSDB_U16SP2_WEBSM_QA`. Gated on a least-privilege account |
| **Blocklist in the Java framework** | ⛔ **Absent** — 102 rows across 50 controllers target app-pool-killing action names. See `OBS-047` / `MF-16` |
| Teardown / DELETE coverage | ⬜ Not bound to created ids yet — 5 hops excluded |
| Swagger surface (690 ops) | ⬜ Untested by the chaining run |
| Java/TestNG port | ⬜ Deferred — flows run under Python |

**Next highest-value action:** mine the 3,194 documented payloads to lift create coverage from 13/217.
