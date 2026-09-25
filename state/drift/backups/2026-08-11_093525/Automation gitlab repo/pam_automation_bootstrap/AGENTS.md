# PAM Automation Bootstrap

Test automation framework for ARCON PAM product. Playwright + TestNG + Maven, Java 21.

UI **and** API both run on Playwright — API tests use `APIRequestContext` via `utils/ApiHelper`. REST Assured
is declared in `pom.xml` but effectively unused (two legacy holdouts in `pages/acmo/api/`); do not add more.

Workspace-level guidance — edit scope, the `JAVA_HOME` fault, the response envelope, and the `workbench/`
document set (`approach/`, `skills/`, `rag/`) — lives in the workspace root's `CLAUDE.md`, two levels up.
The workspace root also has a `README.md` that orients you to every folder.

## Where this repo sits — read first

The same automation codebase lives in two places. They are **not** interchangeable.

| Checkout | Remote | Branch | Role |
|---|---|---|---|
| `Automation gitlab repo/pam_automation_bootstrap/` | `Omkar.Kumbhar/pam_automation_bootstrap.git` | `Dev`; feature work on `AI` | **This repo. Editable.** All day-to-day automation development happens here. |
| `pam/AutomationTesting/` | `root/pam.git` (developer repo) | `35.8.29_Hotfix` | **Reference only.** Holds the latest build-ready code. Read it for context; never write to it. |

`pam/AutomationTesting/` has no git link to this project — it is a plain copy that the owner refreshes
by hand. Committing automation work there mixes it into the product build.

**Workflow**

1. Develop here, on branch `AI` (cut from `Dev`).
2. Owner reviews the `AI` branch.
3. Owner merges `AI` → `Dev`.
4. Owner manually copies the accepted code into `pam/AutomationTesting/` and commits it to the
   developer repo.

Agents do steps 1 only. Steps 2–4 are manual and owner-driven. Never push, never merge, and never
write into `pam/` — leave that checkout with a clean `git status`.

## Knowledge graph (Graphify)

This repo is indexed by [Graphify](https://github.com/Graphify-Labs/graphify). Query the graph before
grepping — it answers structural questions in a fraction of the tokens a raw search costs.

```bash
graphify query "which tests depend on LoginPage?"   # BFS over the graph
graphify path "LoginPage" "BasePage"                # shortest relationship path
graphify explain "BasePage"                         # a node and its neighbours, with file:line
graphify affected "BaseTest" --depth 1              # reverse impact — what breaks if this changes
graphify god-nodes --top 10                         # most-connected nodes (architectural hubs)
```

**Keeping it current** — after changing code:

```bash
graphify update .        # incremental AST re-extract, no LLM, no API key
```

Use `graphify update . --force` after refactors that *delete* code, otherwise the rebuild is rejected
for having fewer nodes than the previous graph.

**Rebuilding from scratch:**

```bash
graphify extract . --code-only                       # AST only, no API key needed
$env:GRAPHIFY_VIZ_NODE_LIMIT="20000"                 # this graph exceeds the 5,000-node viz default
graphify cluster-only . --no-label                   # regenerate GRAPH_REPORT.md + graph.html
```

Output lands in `graphify-out/` (gitignored, ~153 MB, regenerable):

| File | What it is |
|---|---|
| `graph.json` | The graph itself — every query command reads this |
| `GRAPH_REPORT.md` | Human-readable summary: god nodes, 865 communities (808 **named**, 57 thin omitted), import cycles |
| `GRAPH_TREE.html` | Collapsible D3 tree — **start here**, the practical viewer at this repo's size |
| `pam_automation_bootstrap-callflow.html` | Mermaid architecture / call-flow diagrams with zoom-pan |
| `graph.html` | Full force-directed view; 24 MB, slow to open |

**Open a view:**

```powershell
Invoke-Item graphify-out\GRAPH_TREE.html                        # recommended
Invoke-Item graphify-out\pam_automation_bootstrap-callflow.html
```

**Community names** come from `graphify label . --backend=claude-cli`, which drives the local Claude
CLI — no `ANTHROPIC_API_KEY` and no per-call cost. `--backend=claude` is a different path and *does*
demand an API key; it fails to `Community N` placeholders without one. Use `claude-cli`.

Re-clustering resets names, so after any `cluster-only` run re-label with:

```powershell
graphify label . --missing-only --backend=claude-cli
```

## Graph automation

| Thing | State | Effect |
|---|---|---|
| Git hooks | installed | `post-commit` and `post-checkout` refresh the graph automatically |
| MCP server | `.mcp.json` | Claude Code gets 10 native graph tools — no shelling out |
| Merge driver | `.gitattributes` | union-merges `graph.json` if the graph is ever committed |
| Global graph | registered as `pam-automation` | enables cross-repo queries once a second repo is added |

MCP tools exposed: `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`,
`graph_stats`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.

Live rebuild while developing (optional, runs in the foreground):

```powershell
graphify watch .
```

Exclusions live in `.graphifyignore`. Suite XMLs under `*_Suites/` are **not** indexed — Graphify has
no XML parser, so suite→test-class edges are absent from the graph. Use grep for those.

`.claude/settings.json` registers a `PreToolUse` hook that reminds Claude Code to consult the graph
before searching. It calls `graphify` from `PATH`, so each developer needs
`uv tool install "graphifyy[mcp]"` for the hook to resolve.

## Run tests

Default suite is `CICD_Suites/Demo.xml` (from `pom.xml`), default env is `QA_MsSQL` and default browser is
`chrome` (both from `Env_configs/Automation.Properties`).

```bash
mvn clean test -Denv=<env> -DsuiteFile=<suite> -DbrowserType=<browser> -Dmaven.test.failure.ignore=true
```

Examples:
```bash
mvn clean test   # runs Demo suite against hf10_mssql in chrome
mvn clean test -Denv=CICD -DsuiteFile=CICD_Suites/APISuite.xml
```

## Config loading (order matters)

1. `Env_configs/Automation.Properties` — master config (env selection, browser, headless, ZAP toggle)
2. `Environments/<env>.Properties` — env-specific config (URLs, credentials, DB, API tokens)
3. CLI `-D` flags override the properties file values

| System prop | What it overrides |
|-------------|------------------|
| `-Denv` | Environment config file (e.g. `CICD`, `hf10_mssql`, `QA_MySQL`) |
| `-DbrowserType` | Browser: `chrome`, `chromium`, `firefox`, `safari`, `edge` |
| `-DsuiteFile` | TestNG suite XML path |
| `-DurlFromCmd` | Overrides `environmentUrl` from env properties |

Set `headlessMode=true` in `Automation.Properties` for CI runs.

## TestNG suites

`CICD_Suites/` holds the CI entrypoints — `Demo.xml` (Login smoke, the default), `APISuite.xml`,
`SanityChecks.xml`, `DigitalVault.xml`. In `APISuite.xml` most classes are commented out; only
`ActivityLogs` is active.

Also present: `API_Suites/Positive_All/` (71 XMLs, one per module — the way to run a single API module),
`API_Suites/Negative/` (5 failure-mode suites), `CRUD_Suites/` (12), `E2E_Suites/` (8), `Temp/` (3).

⚠️ **There IS a root `testng.xml`** — it arrived git-tracked in the upstream `Dev` merge (commit `4a40b81`).
This file previously said there was none. It runs a single class, `ActivityLogs`, and has **no `<listeners>`
block**, so `TestListener` never registers and no Excel report is produced.

⛔ **Treat it as a hazard.** IDEs pick up a root `testng.xml` by convention, and `ActivityLogs`' Excel data
contains `/api/ActivityLogs/GetLogs` and `/api/ActivityLogs/GetErrorLogs` — the two endpoints that stop the
IIS application pool. Pressing *Run* on the project can therefore take the whole API down. See `OBS-047`
and `MF-16` in `document/data/`.

## Project structure

`src/main/java` is empty — all sources live under `src/test/java`.

```
src/test/java/com/arcon/
  tests/           — TestNG classes (API/All_API_Positive, API/Negative_API, API_Dynamic, API_UI, UI, other)
  pages/           — Page Objects (acmo, administrativeConsole, autoOnboarding, digitalVault,
                     password_vault, sessionMonitoring, setting, UAG)
  utils/           — BaseTest, ApiHelper, ExcelUtils, APIExcelReportUtil, PropertiesUtils, DBUtils,
                     listeners, ZapHelperPage, apiPayload/ (66 payload helpers)
  autoconfigs/     — AutoConfigs, APIConfig (~1,336 endpoint constants), module-specific configs
  dataprovider/    — TestNG DataProviders for Excel-driven tests
testdata/          — .xls test data (Automation_Test_Input_Data.xls, API_Automation_Test_Input_Data.xls)
Execution_Reports/ — Allure, Extent, Excel, ZAP reports (gitignored)
```

`ApiHelper` extends `BaseTest`, so API tests inherit browser machinery they never use. Both are ~1,300–1,600
lines and are the highest-blast-radius files in the repo — check `graphify affected` before changing either.

## Test conventions

- Test classes extend `BaseTest` and use Playwright thread-local instances (`getPage()`, `getBrowser()`)
- `@BeforeMethod` → `launchApplication(AutoConfigs.applicationUrl)`
- `@AfterMethod` → `clearPage()` (closes browser, nulls page helpers)
- Test IDs in `@Test(description = "PAM_XXX_###", ...)`
- Data-driven tests use `@Test(dataProviderClass = DataProviderUtils.class, dataProvider = "...")` with Excel data
- `SoftAssert` used via `getSoftAssert()`

## Reporting & listeners

- `ExtentReportListener` (ITestListener) — generates `Execution_Reports/Extent_Report/TestExecutionReport.html`
- `TestListener` — used by API suite
- Allure configured via `pom.xml` `<allure.results.directory>` property
- ZAP reports generated if `enableZapProxy=true` in `Automation.Properties`

## Jenkins CI

Pipeline is defined in `jenkins.properties` (loaded as a Groovy properties file by Jenkins). It:
1. Loads properties (branch, git URL, env, suiteFile, browserType, reportPath, mail)
2. Dynamically labels agent via `AGENT_LABEL`
3. Runs `mvn clean test` with `-Dmaven.test.failure.ignore=true`
4. Emails `TestExecutionReport.html` on success/failure

No GitLab CI, GitHub Actions, or other CI configs present.

## Notes

- Git default branch is `Dev`, not `main`/`master`
- This is a single-module Maven project (not a multi-module monorepo)
- No code generation, no migration steps, no build artifacts beyond Maven target/
- Allure and Extent reports write to `Execution_Reports/` (gitignored)
- Lombok is **not** used — getters/setters are written explicitly
