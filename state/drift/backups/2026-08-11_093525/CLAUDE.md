# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚡ Active instructions — read these first

@BLAST/Objective.md

The file above is the **single source of active instruction**. The owner rewrites it whenever the
requirement changes; it is imported here and re-injected on every prompt, so it is always current.
**Where it conflicts with anything below, `Objective.md` wins** — this file is standing operating guidance,
`Objective.md` is what to do right now.

Its permanent counterpart is `objective_original_origin.md` (workspace root) — **append-only** history of
every instruction, decision and measurement since Day 1. Consult it when you need to know *why* something
is the way it is; append to it when a requirement changes or a run produces a durable finding. Never edit
its existing entries.

## 🔁 Standard workflow — follow this for every CLI interaction

**Established 2026-08-03. Applies to all future sessions unless the owner explicitly says otherwise.**

`BLAST/Objective.md` is the single source of truth for the current task. Record the instruction there
*before* building anything — never start implementation against a request that exists only in the chat.

| Step | Action |
|---:|---|
| 1 | Owner gives an instruction |
| 2 | **Write it into `BLAST/Objective.md` first**, replacing the `## Instruction` block. Append the outgoing objective to `objective_original_origin.md` before overwriting — always, even if no work was done on it |
| 3 | Read it back and identify genuine ambiguities |
| 4 | If clarification is needed, **ask in MCQ form** (`AskUserQuestion`) before proceeding |
| 5 | Fold the answers into `BLAST/Objective.md` so the file matches what was agreed |
| 6 | Execute, using `BLAST/Objective.md` as the instruction and the workspace as context — `objective_original_origin.md` for history, plus `Reports/`, the repo, `graphify-out/`, `tools/rag/` |
| 7 | On completion, update the affected documentation and reports, and **append what changed and what was learned** to `objective_original_origin.md` |

**What triggers step 2.** Substantive task requests — build, analyse, fix, run, produce. **Not** questions
("is it done?"), conversational replies, or process/config changes like this workflow itself; writing those
into the file would overwrite a real objective with noise. A correction to the current task **amends** the
instruction already there rather than replacing it.

**Where a standing rule goes.** Process rules live *here*, in `CLAUDE.md` — not in `Objective.md`, which the
next instruction overwrites. If the owner states a durable way of working, record it in this file and log
the decision in `objective_original_origin.md`.

**Do not** copy historical content into `Objective.md` (§Markdown conventions), and do not ask the owner to
restate anything the workspace already records — read it.

### Objective lifecycle — archive before overwriting

⛔ **Never overwrite `BLAST/Objective.md` without archiving first.** Step 2 above expands into this:

1. Read the outgoing objective out of `BLAST/Objective.md`.
2. Add a record to **§0 Objective Register** — the summary row goes in the index
   `objective_original_origin.md`, the full record in `objective-history/01-objective-records.md`. Use the
   next sequential ID (the index states which). Ten fields, all mandatory — write `None`, never drop one:
   **Objective ID · Title · Status · Summary** (2–5 lines) **· Key Deliverables · Related Files · Reason
   for Archiving · Pending Work · Lessons Learned / Observations · Dependencies**.
3. Only then replace the `## Instruction` block with the new objective.

| Rule | Detail |
|---|---|
| **Status** | `Completed` · `In Progress` · `Superseded` · `Cancelled` |
| **⛔ No dates** | The sequential ID is the ordering. Never "archived on \<date\>" — say "superseded by OBJ-00N". **Exception: filesystem paths.** `Reports/Runs/2026-07-29_181439/` is an identifier; cite it exactly or traceability breaks |
| **Traceability** | Name the real artifacts — reports, workbooks, scripts, suite XMLs, graphs, Jira keys, ISSUE files, run folders. A record an auditor cannot follow has failed |
| **Unfinished work** | State what was completed, what remains, why it stopped, and whether to resume |
| **Multi-session** | An objective keeps its ID across sessions; update its **Status** in place until archived. That in-place edit is the *only* permitted exception to append-only |
| **Append-only** | Never delete, reword or reorder an existing record |

The register is the audit log; §1–§6 of that file remain the long-form narrative behind it.

## What this workspace is

This directory is **not a repository** — it is a workspace holding two unrelated git checkouts plus
supporting material. Know which one you are in before you touch anything.

| Path | What it is | Git |
|---|---|---|
| `Automation gitlab repo/pam_automation_bootstrap/` | QA automation framework — Playwright + Java + TestNG + Maven. **The only editable code.** | `Omkar.Kumbhar/pam_automation_bootstrap.git`, default branch `Dev`, work on `AI` |
| `pam/` | ARCON PAM product source (.NET) under `pam/PAM/`, plus `pam/AutomationTesting/` — a hand-copied snapshot of the same automation framework | `root/pam.git`, branch `35.8.29_Hotfix` |
| `workbench/` | All internal working material. Six subfolders: `scripts/` (**every harness script lives here**) · `onboarding/` (**the portable kit for a new project** — `OBJ-011`; profile schema, PAM profile as the worked example, `validate_profile.py` readiness gate, the `api-onboarding` skill. Holds **no** project facts by design) · `skills/` (`*.SKILL.md` specs — PAM-bound, and they target the *Java* framework) · `rag/` (product docs, extracted and queryable) · `react/` (internal component) · `archive/` (frozen planning set, incl. the former `approach/`) — plus six root-level briefs, see below | not versioned |
| `BLAST/` | The requirement intake framework — `Objective.md` (**auto-loaded**) + `B.L.A.S.T.md`. **Has its own `CLAUDE.md` and its own protocol** — read them before touching it. | not versioned |
| `document/` | **The `OBJ-007` deliverable set** — two multi-worksheet Excel workbooks, nine analysis reports, and `data/*.json` as their machine-readable source. Has its own `README.md`; read it before adding anything. **Only `obj007_build_workbooks.py` writes the `.xlsx`** — edit the JSON and re-run, never the workbook | not versioned |
| `document/BUSINESS-CONTEXT-DEMO.md` | ⭐ **The answer to "how do you give the AI business context?"**, short enough to walk in 5 minutes (`OBJ-009`). The 5-hop service-creation chain with measured values. **Use this one in a live demo** | not versioned |
| `document/BUSINESS-CONTEXT-STANDARD.md` | The full reference behind that demo — same example extended through the approval chain, 27 sections. **§0 is a reusable checklist: use it when briefing any new feature.** Its standard is absolute — every figure traceable, every gap labelled `UNKNOWN` with what would settle it | not versioned |
| `questions/` | **The project knowledge base** (`OBJ-008`) — `PAM-Project-Knowledge-Base.xlsx`, every question with answer + **evidence** + comments, sourced from `data/questions-*.json`. **Living document: when a new question arises, add it.** Built only by `build_knowledge_base.py`, which **fails the build on an uncited answer**. Read its `README.md` and `_AUTHORING-CONTRACT.md` first | not versioned |
| `Reports/` | Measured evidence. `Runs/<YYYY-MM-DD_HHMMSS>/` per execution — **retained, never deleted** — plus authored `Issues/*.md` (11) and `Summary/` | not versioned |
| `Developer-Loopholes/` | One folder per finding (`LH-01`…`LH-13`), each a raisable Jira ticket plus attachable evidence. **Generated, never hand-edited** — see its `README.md` §3. `LH-13` is the OBJ-010 auth-bypass finding and sources a different run | not versioned |
| `jira/` | Terminal Jira client for raising PAMIT tickets — `jira_client.py`, `create_lh01.py`, `jira.md` (field map + ADF traps). `.env` holds credentials, gitignored | not versioned |
| `required-context/` | What the data we have can and cannot answer, and what to request to close the gaps — `01-Data-Gap-Analysis.md`, `02-Data-Access-Requests.md` | not versioned |
| `writer/` | `writer.md` — the management-facing write-up of the whole effort — plus `PPT/`: `Prepare-1.pptx` (the 10-slide management deck, `OBJ-012`) and `QABuddy_AI_Test_Automation.pptx` (its style reference). **Only `obj012_build_ppt.py` writes `Prepare-1.pptx`** — edit the script and re-run, never the deck | not versioned |
| `Graphify/` | Graph output in three layers: `pam-scope/` (the .NET product, 112,628 nodes) · `api-graph/` (API surface + 1,680 chain candidates) · `dev-scope/` (marker only, not built) | not versioned |
| `Company Documents/` | Four sources: the two admin-guide PDFs, **`PAM API (Internal Team).pdf`** (2,470 pp — the payload reference, see §Consult these), and the Swagger link CSV | not versioned |

Every row below `pam/` in that table sits outside both git checkouts deliberately — nothing written there
can contaminate a product build.

`workbench/` also holds six root-level briefs, each written for a different reader: `overview.md` (the demo
document) · `developer-loopholes.md` (**source of truth for the 13 findings**) · `document-gap.md` (for the
documentation team) · `new-project-implementation.md` (**how to onboard a new project** — `OBJ-011`: the
onboarding workflow, both architecture approaches, the comparison and the recommendation. Its executable
half is `tools/onboarding/`) · `self-understanding.md` (plain-language personal reference) · `README.md`.

**The findings pipeline runs across three folders — know which stage you are in.** A finding is stated once
in `workbench/developer-loopholes.md`, packaged per-finding into `Developer-Loopholes/LH-NN-*/`, and raised
from `jira/`. `Reports/Issues/` is a parallel track, not a predecessor: same defects, internal-analysis
audience. Where a loophole and an issue overlap, **cross-reference rather than restate**.

**Path convention:** documents *inside* `workbench/` refer to their siblings by short path
(`rag/findings.md`, `skills/playwright-api.SKILL.md`) because they are siblings. Documents *outside* it —
this file, the root `README.md`, the automation repo's `AGENTS.md` — use the full `workbench/...` path.

Two nested guidance files own detail this one deliberately does not repeat:

- **`pam_automation_bootstrap/AGENTS.md`** — the repo's own reference: Graphify commands and automation,
  suite inventory, package layout, listeners, Jenkins pipeline. It defers workspace-level topics (edit
  scope, `JAVA_HOME`, the response envelope, the `workbench/` document set) back up to this file. Keep
  that split when editing either. **It is imported by `pam_automation_bootstrap/CLAUDE.md` (`@AGENTS.md`),
  so it loads automatically once you open a file in that repo** — Claude Code does not read `AGENTS.md` on
  its own. `.claude/rules/automation-repo.md` carries only the handful of things `AGENTS.md` omits.
- **`BLAST/CLAUDE.md`** — a different protocol entirely, including a hard "Protocol 0 HALT" that forbids
  writing code before a discovery checkpoint.

## ⛔ Edit scope

**Write only inside `Automation gitlab repo/pam_automation_bootstrap/`, on branch `AI`.**

`pam/` is reference-only. Read it freely for context; never modify it, never commit there, and leave it
with a clean `git status`. It is the developer's product repo — automation commits landing there mix test
code into the product build. `pam/AutomationTesting/` looks editable and is not: it is a plain copy the
owner refreshes by hand, with no git link to the bootstrap repo.

The release path is: develop on `AI` → owner reviews → owner merges to `Dev` → owner manually copies into
`pam/AutomationTesting/`. Only the first step is yours. Never push, never merge.

`AI` is **local-only** — there is no `origin/AI` and no upstream is configured, so a bare `git push` would
try to create the remote branch. The only remote branch is `origin/Dev`. Commit freely on `AI`; stop there.

Full rules: `BLAST/Objective.md` (§Constraints). The original standing instruction is archived at
`docs/history/archive/workbench-archive/approach/instruction.md` — frozen, item 8 is the edit-scope rule restated above.

## The BLAST workflow — how requirements enter this workspace

`BLAST/` is how the owner states new requirements. **`BLAST/Objective.md` is a dynamic blueprint, not a
fixed spec:** the owner rewrites it whenever the requirement changes. Expect its contents to differ
completely between sessions. Since 2026-08-03 it is **auto-loaded** (§Active instructions above), so you
already have its current contents at the top of every turn.

⚠️ **It is deliberately small — keep it that way.** It holds the active instruction and nothing else.
Do not write history, findings, run results, or a task backlog into it; do not restate context that
already exists elsewhere in the workspace. Two consequences that matter:

- **Fill the gaps yourself.** The owner will not repeat what the project already records. Read the rest of
  the workspace — this file, `objective_original_origin.md`, `Reports/`, the repo — before asking.
- **Append, never copy back.** When the instruction changes or a run produces a durable finding, append it
  to `objective_original_origin.md`. Never move historical content into `Objective.md`.

Size is functional, not cosmetic: at ~16 KB the file exceeded the hook's inline-injection limit and was
spilled to a side file with only a preview in context. Under that limit the whole thing lands every turn.

**Trigger.** A run is invoked with a prompt of the form:

> Run `Objective.md` by referring to `blast.md`, and give me the output.

`blast.md` means `BLAST/B.L.A.S.T.md`. That is a request to execute the whole protocol — Blueprint → Link →
Architect → Stylize → Trigger, starting at Protocol 0. Read both files in full before acting;
`B.L.A.S.T.md` assigns you the "System Pilot" role and constrains what you may do and when.

**Protocol 0 still halts, and the dynamic objective makes it matter more.** You are forbidden from writing
tools until the five Discovery questions are answered by the owner, the JSON data schema is in `LLM.md`, and
`task_plan.md` holds an approved Blueprint. Confirming your reading of an objective that already answers a
question is fine; skipping the checkpoint is not. Because the objective is rewritten between runs, a new one
can silently contradict the previous run's schema — the checkpoint is what catches that.

**Where output goes.** The objective changes, so the target is confirmed during Blueprint rather than fixed
here. The boundaries are fixed:

| Destination | Rule |
|---|---|
| `pam_automation_bootstrap/` on `AI` | **The deliverable.** Java 21 / Playwright / TestNG code, suite XMLs, Excel test data. |
| `BLAST/` | **Working space.** Protocol memory (`LLM.md`, `task_plan.md`, `findings.md`, `progress.md`), `architecture/` SOPs, `tools/` generators, `.tmp/` intermediates. Not a git repo — writes here touch no history. |
| `pam/` | **Never.** Reference data only; leave `git status` clean. |

**Per-run state.** Since `Objective.md` is overwritten, BLAST's memory files can carry state belonging to a
previous, unrelated objective. At Protocol 0, establish whether the run is a new objective or a continuation
of the last one. If new: treat the `LLM.md` schema and `task_plan.md` phases as stale and re-derive them;
keep `progress.md` append-only so the history of past runs survives.

**Precedence.** BLAST calls `LLM.md` "law". Within this workspace, this file outranks it:

| Where they conflict | Resolution |
|---|---|
| Phase 5 wants a cloud deploy plus cron/webhook triggers, and calls a project incomplete until the payload lands there | You never push and never merge. A run **ends committed on `AI`**; the owner takes it from there. The "trigger" here is the Jenkins pipeline (`jenkins.properties`) plus a suite XML, not a cloud cron. Say plainly that the run is complete at that boundary. |
| Phase 3 lets Layer 3 pick any language | Anything landing in the automation repo is Java 21 + Playwright + TestNG. Only generators kept in `BLAST/tools/` may be JS or Python. |
| Any generated assertion | The response-envelope rule below is absolute — never a status-only check. |

Record any such deviation in `LLM.md` so the next run inherits it.

## Build and test

### Fix `JAVA_HOME` first — every session

System `JAVA_HOME` points at `C:\Program Files\Java\jdk-26.0.1`, **which does not exist**. The `java` on
`PATH` is 26.x; `pom.xml` requires Java 21. Maven fails until you override it:

```powershell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot"
```

`mvn` resolves on the **PowerShell** `PATH` only, not in Bash. Use the PowerShell tool for Maven.

### Running suites

Execution is entirely Surefire + TestNG XML — there are no Maven profiles, no runner classes, and no
shell scripts.

```powershell
mvn clean test                                              # default: CICD_Suites/Demo.xml, env QA_MsSQL, chrome
mvn clean test -Denv=CICD -DsuiteFile=CICD_Suites/APISuite.xml
mvn clean test -DsuiteFile=API_Suites/Positive_All/<Module>.xml   # one API module (71 such files)
mvn -o clean test-compile -DskipTests                       # compile-only check
```

Add `-Dmaven.test.failure.ignore=true` when you need the reports written even though tests fail — that is
what Jenkins passes.

| Flag | Overrides |
|---|---|
| `-Denv` | Which `Environments/<env>.properties` loads (20 available) |
| `-DsuiteFile` | TestNG suite XML — default `CICD_Suites/Demo.xml` |
| `-DbrowserType` | `chrome` · `chromium` · `firefox` · `safari` · `edge` |
| `-DurlFromCmd` | `environmentUrl` from the env properties |

### Running a single test

```powershell
mvn clean test -Dtest=ActivityLogs
mvn clean test -Dtest=ActivityLogs#activityLogs
```

⚠️ `-Dtest` **overrides `suiteXmlFiles` entirely**, so the suite's `<listeners>` never register. For API
tests that means `TestListener` does not run, so `APIExcelReportUtil` is never initialised or saved and no
Excel report is produced. Use a suite XML when you need the report.

### Config resolution order

`Env_configs/Automation.Properties` (master switches) → `Environments/<env>.properties` (URLs,
credentials, DB, timeouts) → `-D` flags win over both. Surfaced as `public static` fields on
`com.arcon.autoconfigs.AutoConfigs`. Credentials are committed in plaintext across all 20 env files.

## Architecture

Detail is path-scoped so it loads only where it applies — see `.claude/rules/`:

| Rule file | Loads when you open | Covers |
|---|---|---|
| `automation-repo.md` | `Automation gitlab repo/**` | `BaseTest`/`ApiHelper`, the Excel→report API data flow, two known defects, suite layout, config detail, code conventions, Graphify usage |
| `api-surface.md` | `APIConfig.java`, `tools/**`, `Reports/**`, `Developer-Loopholes/**`, `pam/PAM/**` | The 1,306 count and its basis, verb distribution, why the API is not in `pam/PAM`, the harness scripts, Swagger and payload sources |
| `markdown-docs.md` | `**/*.md` | "Update MD files", the one-fact-one-home layer table, house style |

Three things you need **before** opening any of those files, so they stay here:

- **`pam/PAM` is not the API under test** — only 48 of 1,306 endpoints (3.7%) exist there. Do not plan
  around parsing it.
- **Quote 1,306** as the endpoint count. `1,336` and `1,322` are wrong or stale.
- **`GET` + `POST` is 99.7% of the surface.** Deletion is `POST /api/<C>/Delete<Thing>`, so a destructive
  call looks like an ordinary POST — **guard on names, not verbs.**

## ⚠️ The response envelope

Most PAM endpoints return **HTTP 200 with an application-level `errorCode` in the body**. A rejected
request is usually a 200, not a 4xx.

Never write or generate an assertion that checks only `response.status() == 200` — it passes against a
fully rejected request. `ApiHelper.validateResponseErrorCode(...)` handles the envelope; negative cases
need both an `ExpectedStatus` (often `200`) and an `ExpectedErrorCode`.

Two traps when you go looking for it in `ApiHelper`:

- It is **`private`**, so tests never call it directly. The public entry point is
  `validateApiResponseWithResponseTime_ExcelBasedsettingnegative(...)`, which invokes it only when
  `expectedStatusCode == 200` — framework-level rejections (401/405) carry no envelope.
- A **superseded copy of both methods sits commented out immediately above the live ones** — the dead
  block starts at **1319**, the live definitions are at **1432** and **1533**. A grep for
  `validateResponseErrorCode` hits the dead block first. Check for a leading `//` before concluding
  anything about the behaviour. *(These line numbers move whenever `ApiHelper` is edited — re-grep rather
  than trusting them. An earlier version of this file cited 1282–1394/1397/1464, which was ~30 lines off.)*

**Use `com.arcon.utils.validation` for anything new.** Since OBJ-007 the envelope logic lives there:
`PamEnvelope` normalises the shapes, `PamApiValidator` runs twelve layers, `ValidationReport` collects
them, `ErrorCodeRegistry` holds the codes, `DbPersistenceValidator` checks the database. `ApiHelper`'s
`validateResponseErrorCode` now delegates field access to `PamEnvelope`.

⛔ **Two measured facts about the old implementation, both worth knowing before trusting any green run
that predates OBJ-007:**

- It read **`node.has("success")` in camelCase, and Jackson is case-sensitive.** Across all 1,868
  captured responses, lowercase `success` appears in **0** and PascalCase `Success` in **1,580** — so the
  method's first assertion failed on every response this API can produce. Every negative case reaching it
  failed for the wrong reason.
- Recognised codes were hardcoded as `KNOWN_ERROR_CODES = {"201","202","203"}` and asserted hard, so the
  real, measured `ErrorCode: "206-LC_GLD"` (HTTP 200, `POST /api/Logs/GetLogDetails`) would have been
  reported as a broken test. `ErrorCodeRegistry` now matches on the numeric prefix and records an
  unrecognised code as an observation — the defect is the missing product registry, not the response.

### Response shapes — **31 distinct**, measured across all 1,868 captured calls

⚠️ **This section used to say "four". A full census under OBJ-007 counted 31 distinct top-level shapes,
of which only 6 match a documented one.** The exemplars below are the ones worth memorising, but treat the
list as illustrative, not exhaustive — the whole census is `document/data/envelope-shapes.json`.

What breaks a fixed-shape assertion, with counts: **127** calls are not JSON objects at all · **288**
carry no `Success` field · **139** of 1,291 `Result` values are not arrays (object, string, bool, int) ·
**2** bodies are a naked `true`/`false` · **291** lack the `Program`/`Version`/`DateTime` frame.

`PamEnvelope` exists to absorb all of this — all 8 of its `Shape` classes occur in the evidence, none is
speculative. The exemplars:

| Shape | Seen on |
|---|---|
| `{Program, Version, DateTime, Success, Message, Result[]}` | `GetAllActiveUserList`, most business endpoints |
| Same, but **no `Message` field** | `GetLOBList` |
| Same, but `Result` is an **object**, not an array | `GetServiceDetails` |
| **Bare array, no envelope at all** | `GET /api/DeviceOnboarding/GetLOBList` |
| Error form: `Success: false` + `ErrorCode` + `ErrorMessage`, still **HTTP 200** | `GetLogDetails` (missing param) |

⛔ **`Success: true` is not evidence of a write.** `POST /api/ServiceCreation/SetServiceDetails` returns
`Success: true` with `Message: "Already Exists"` when the record already exists — nothing was inserted, and
both the status code and the `Success` flag are green. A create assertion must check **`Message`
semantics**: `"Inserted Successfully"` means inserted, `"Already Exists"` means no-op.

### 🟢 Token generation WORKS again — `token_guard.py` owns the only call to it

⚠️ **This section previously said the account was locked and `/arcontoken` "no longer works". That is no
longer true, and the correction matters:** the account has been unlocked. Verified 2026-08-04 by a single
deliberate attempt — `POST /arcontoken` returned **HTTP 200** in 3,517 ms with an `access_token`
(`APIUserId: 2`, role `Default`, 24 h lifetime). The credentials in `Environments/QA_MsSQL.properties`
(`pam_APITokenUserName` / `pam_APITokenPassword`) are correct and unchanged — **the blocker was always the
lock, never the password.**

⛔ **The lockout risk has not gone away, and the rule that prevents it is unchanged.** `GenericScheduler`
is also the data-warehouse ETL service account, so a lockout reaches past testing. The 2026-07-28 lockout
was **not** caused by a wrong credential: the harness re-attempted `getToken()` **on every run by design**,
and accumulated failures tripped the lockout policy (`ISSUE-009` §4a). Retry-on-failure and account lockout
are fundamentally incompatible.

**`tools/token_guard.py` is now the single gate.** `chain_runner.get_token()` and
`run_qa_mssql.try_dynamic_token()` both delegate to it, so there is exactly one code path to `/arcontoken`:

```powershell
python tools\token_guard.py status        # report only, zero HTTP calls
python tools\token_guard.py refresh       # ONE attempt, only if the cache is expired
python tools\token_guard.py clear-latch   # human unblock, after fixing the cause
```

Resolution order is `$PAM_API_TOKEN` → valid cache → **one** live attempt. Setting the env var still
bypasses the endpoint entirely and is the safest option for an unattended run:

```powershell
$env:PAM_API_TOKEN = "<bearer token>"
```

| Rule | Why |
|---|---|
| **Never retry a failed token request** | A lockout deepens. Stop and report. `token_guard` enforces this — it does not rely on you remembering |
| **A failed attempt latches** | `.token_attempt_block.json` blocks every later attempt, in this run *and all future runs*, until a human clears it. Without this, "once per run" silently becomes "every run" — the original lockout |
| **Network faults latch too** | A timeout cannot be distinguished from a refused login, and guessing wrong costs an account |
| One token per run, cached to `tools/.token_cache.json` | Never schedule or loop token generation. No cron, no backoff |
| Do not blank `ApiToken=` in an env file | `ApiHelper.getToken()` (`ApiHelper.java:971`) returns it verbatim **with no expiry check** and only calls `/arcontoken` when it is empty. Since `getToken()` runs per test, a blank value means **one token request per test** across a whole suite |

⚠️ **`ApiToken=` is not auto-renewed.** Once it expires, Java API tests fail on auth rather than
regenerating — a confusing failure mode that reads as a product defect. Refresh it from `token_guard`.

Full account history and the re-validation workflow: `Developer-Loopholes/README.md` §6, `ISSUE-009`.

### ⛔ Three endpoints take the whole API down — never call them

`GET /api/ActivityLogs/GetErrorLogs` and `GET /api/ActivityLogs/GetLogs` hang for 30 s and **stop the IIS
application pool**. Three sequential requests were enough to take the entire API to `503` with no recovery
without intervention — this was not a load test. `GetAllActiveUserDetails` is blocklisted for the same
reason. `ISSUE-010` has the decisive capture; `LH-08` puts **98 endpoints** at risk and its live
re-validation is **forbidden**, not merely skipped.

Enforce the blocklist **at planning time**, before a request is built. Two related traps:

- **Verb guards do not work on this API.** Deletion is `POST /api/<C>/Delete<Thing>` — guard on *names*.
- **Never replay a call that would mutate.** The harness expresses this as `replay_filter`; 35 rows across
  LH-02 and LH-09 are withheld for exactly this reason.

## Markdown conventions

Path-scoped to `**/*.md` — see `.claude/rules/markdown-docs.md` for "Update MD files", the
one-fact-one-home layer table, the frozen-archive rule and house style.

## 📄 Large files — never let size hide information

Reading a large file returns the **first 2,000 lines and no error**. Nothing tells you the rest exists, so
a truncated read looks exactly like a complete one. **Treat any file over ~1,500 lines as truncated until
proven otherwise** — check with `wc -l` before reading something unfamiliar.

| Lines | Approach |
|---:|---|
| < 1,500 | Read normally |
| 1,500 – 5,000 | Page with explicit `offset`/`limit`, or Grep straight to the section |
| > 5,000 | Never read linearly. `grep -n "^## "` for the section map, then read only those ranges |

**Never read these directly — a query layer already exists and reading the file is the wrong access path:**

| File | Lines | Use instead |
|---|---:|---|
| `artifacts/rag-corpus/pam-api.md` | 101,803 | `python tools\rag\query.py find "<terms>"` · `page <doc> <N>` |
| `artifacts/rag-corpus/pam-admin.md` · `client-manager.md` | 18,560 · 9,611 | same |
| `Graphify/pam-scope/graphify-out/GRAPH_REPORT.md` | 13,312 | the `graphify` MCP tools |

⚠️ **`Reports/Runs/*/RUN_REPORT.md` is the live trap.** The `2026-07-29_181439` report is 8,566 lines and
its section **"5. Exclusions — nothing is silently skipped" begins at line 8,544.** A plain read stops
6,500 lines short of it and silently omits the one section recording what the run left out — the exact
failure this rule exists to prevent. Get the section map first, then read ranges.

**When authoring.** An archive that grows without bound gets an **index plus sequential parts**:
`objective_original_origin.md` + `objective-history/NN-slug.md` is the working example. Rules for that
pattern — the index must list **every** part and what it holds, so nothing becomes undiscoverable; split a
part once it passes ~600 lines; and keep a **stable citation scheme** (`§N`) that survives reorganisation,
so existing cross-references never break. Auto-loaded files (`CLAUDE.md`, `BLAST/Objective.md`,
`.claude/rules/*`) are held to a stricter budget — see §Standard workflow.

## Consult these before grepping

- **Knowledge graph** — `pam_automation_bootstrap/graphify-out/` indexes the Java sources as 17,275 nodes
  / 46,905 edges. The repo's `.mcp.json` registers a **`graphify` MCP server**, so prefer its native tools
  (`query_graph`, `get_neighbors`, `shortest_path`, `god_nodes`, …) over shelling out; the CLI equivalents
  are `graphify query "<question>"`, `graphify explain "<class>"`, `graphify affected "<class>" --depth 1`.
  Check freshness before trusting it: `GRAPH_REPORT.md` records `Built from commit: <sha>` — compare with
  `git rev-parse HEAD`, and run `graphify update .` if they diverge. Suite XMLs are **not** indexed —
  Graphify has no XML parser, so suite→test-class questions still need grep. `graphify-out/wiki/` does not
  exist despite the repo `CLAUDE.md` mentioning it; use `GRAPH_TREE.html` for browsing. Full command
  reference: `AGENTS.md`.
- **Manual test cases** — a user-global `pamit-testcases` MCP server (`search_test_cases`, `get_test_case`,
  `test_case_stats`) serves the hand-written PAMIT test-case corpus. It is **small and partial** — 63 cases,
  Login (50) and Dashboard (13) only — so absence there proves nothing about coverage. The server lives
  outside this workspace, at `E:\Omkar\AI\MCP\Custom_MCP_Vibe\Test_Case_Creator`.
- **Product documentation** — `tools/rag/` is the extracted, page-cited corpus.
  `python tools\rag\query.py find "<terms>"` or `page <doc> <N>`. Cite as `<doc>:p<N>`. Two different
  kinds of document live there, and conflating them wastes a search:
  - The **two administrator guides** (1,101 pp) cover the access model and product concepts. They contain
    **no endpoints, schemas, or error codes** — do not look for an API contract in them.
  - **`PAM API (Internal Team).pdf`** (2,470 pp, Confluence export → `rag/corpus/pam-api.md`) is a different
    asset entirely: **3,194 JSON payload examples**, of which **1,605–1,654 are bound to an endpoint** — the
    best request-body source available. *(The range is real: `build_source_map.py` counts 1,654 bound / 1,540
    orphaned; `document/reports/A7-…` §1 counts 1,605 / 1,589 / 440 unparseable. Both sum to 3,194 — the two
    definitions differ on unparseable examples. **Quote a figure with its basis, never bare.**)*
    Limits: 70% of the 1,306 endpoints are undocumented, only **3** error codes (two previously counted were
    IP-address fragments), **6 of the 31** measured response shapes, and payloads bind to endpoints **by page
    proximity**, so a binding can be wrong. The owner has confirmed it is **not up to date**. Gap analysis:
    `workbench/document-gap.md`; full correction list: `document/reports/A7-documentation-gap-analysis.md` §9.
- **Current state of the API validation work** — `Reports/Summary/API-Chaining-Feasibility-Demo.md` first
  (the executed three-flow demo), then the newest `Reports/Runs/<timestamp>/RUN_REPORT.md`, then
  `Reports/Issues/` for defects. `Reports/README.md` explains how to read a run report and how to
  re-execute; `workbench/overview.md` explains how dynamic generation works. Active requirement and backlog:
  `BLAST/Objective.md` (active instruction), `objective_original_origin.md` (history and former backlog).
- **Harness scripts** — every one lives in `tools/`, never in `Reports/`. All are
  deny-by-default: **a bare run issues zero HTTP calls**, `--execute` is required. Script inventory,
  the Swagger split, and the create-endpoint data gap: `.claude/rules/api-surface.md`.

## ⛔ "Execute everything" = the dynamic framework, never the bootstrap suite

**Standing rule, set by the owner (recorded under `OBJ-010`).** When the owner says *execute everything*,
*run the APIs*, or *run the suite*, that means the **AI-based dynamic API framework in
`tools/`** — generate flows → `chain_runner.py --execute` → validate → report.

`pam_automation_bootstrap/` is a **reference asset only**: read it to learn scenarios, payloads, expected
statuses and error codes, and to *generate* flow JSON from. **Never run its Java/TestNG API tests as the
deliverable** — no `mvn test`, no suite XMLs, no runner classes. This does not change §Edit scope; it
narrows what "execute" means. If a request genuinely needs Maven, say so and get it confirmed first.

## Conventions

- Jira project is `PAMIT`. Unresolvable items are marked `PAMIT-TODO` in place. Raising a real ticket has
  its own traps (v3 needs **ADF**, not wiki markup; `createmeta` under-reports 6 required fields and
  paginates at 50) — read `jira/jira.md` before composing one, and never attach `JIRA-TICKET.md` to its own
  ticket. One ticket exists so far: `PAMIT-42744` (LH-01); LH-02…13 are **drafted but deliberately held**.
  ⛔ **`LH-13` is a security finding** — 19 endpoints accept an invalid bearer token, 6 of them writes. Raising
  it is the owner's call and it has not been raised.
- Four user-invocable skills are installed globally, and two encode workspace rules you would otherwise
  have to reconstruct: **`/raise-the-jira-ticket`** (the `jira/` workflow above) and **`/go-go-go`** (the
  git sync/commit/push activity — note it targets the automation repo, and the never-push-`AI` rule in
  §Edit scope still governs). Also `/graphify` and `/give-me-a-prompt`.
- Code-level conventions (test IDs, `@BeforeMethod`/`@AfterMethod` pairs, logging, tabs, CI) are
  path-scoped — see `.claude/rules/automation-repo.md`.
