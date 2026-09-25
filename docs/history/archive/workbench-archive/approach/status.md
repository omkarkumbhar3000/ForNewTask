# PAM Automation Framework — Execution Status

**Companion to:** `plan.md` · **Scope:** `Automation gitlab repo/pam_automation_bootstrap/` only
**Repo:** `Omkar.Kumbhar/pam_automation_bootstrap.git` · **Branch:** `AI` (cut from `Dev`)
**Developer repo `pam/` (branch `35.8.29_Hotfix`):** reference only — must stay clean
**Last updated:** 2026-07-28, adding parallel Workstream `D` (dynamic API validation) and the `rag/` evidence layer

---

## 1. Phase Status

| Phase | Description | Status | Evidence |
|---|---|---|---|
| **0** | Restore executability | **✅ COMPLETE** | 0 broken refs; 104 suites well-formed |
| **1** | Green baseline | **🟡 PARTIAL** | 1.1 + 1.5 done; 1.2–1.4 blocked on environment — see §5 |
| **2** | Shared layers (`BasePage` / `BaseTest`) | ⬜ Not started | |
| **3** | Pilot 2 modules | ⬜ Not started | Blocked by Phase 1 |
| **4** | Module rollout (16 increments) | ⬜ Not started | Blocked by Phase 3 |
| **5** | API content validation | ⬜ Not started | |
| **6** | Dead-code removal | ⬜ Not started | Deliberately last |
| **7** | Conformance gate | ⬜ Not started | |
| **`D`** | Dynamic API validation (parallel workstream) | ⬜ Not started | Design complete — `dynamic-api-generation.md`. P1 needs no environment |

Workstream `D` is not a phase in the 0–7 refactor ladder: its input is the product build rather than the
automation code, and it runs in parallel. Listed here so that one table shows all live work.

---

## 2. Phase 0 — Restore Executability · COMPLETE

| Step | Action | Status | Result |
|---|---|---|---|
| 0.1 | Rewrite `API_With_Excel` → `API` across suite XMLs | ✅ | 374 refs in 75 files |
| 0.2 | Reconcile sub-package names | ✅ | `.Positive.` → `.All_API_Positive.` (40 refs) |
| 0.3 | Correct or disable refs to non-existent classes | ✅ | 65 corrected, 2 disabled with `PAMIT-TODO` |
| 0.4 | Re-run audit to zero | ✅ | **341 → 0 broken refs** |
| 0.5 | Resolve orphaned classes | ✅ | **737 → 218**; documented in `orphans.md` |

### 2.1 Before / After

| Metric | Before | After | Δ |
|---|---:|---:|---|
| Broken suite references | 341 | **0** | −341 |
| Suite XMLs with a dead package | 75 | **0** | −75 |
| Orphaned test classes | 737 | **218** | −519 |
| Classes reachable from a suite | 146 | **665** | +519 |
| Suite XML files | 101 | **104** | +3 |
| Malformed XML | 0 | **0** | — |
| Test sources compiling | — | **1,063** | BUILD SUCCESS |

### 2.2 What was actually wrong

75 of 101 suite XMLs — including the CI entrypoint `CICD_Suites/APISuite.xml` — referenced
`com.arcon.tests.API_With_Excel.*`. That package does not exist; it was renamed to
`com.arcon.tests.API.*` and the suites were never updated. TestNG cannot instantiate a missing class,
so those suites reported skips or aborted.

**This was the mechanical cause of instruction item 7 — "tests skipped without a valid, explainable reason."**

Three further dead packages were found and fixed in the same pass: `com.arcon.tests.CRUD.AdminConsole.*`,
`com.arcon.tests.E2E.*`, and `com.arcon.tests.UI.EndToEnd.AccessControl.*`.

`E2E.*` could not be fixed with a prefix rule — several classes referenced as `E2E.ACMO.manager.*`
actually live under `UI.CRUD.ACMO.*`. Each of the 67 remaining refs was resolved individually by
matching the simple class name against the real tree: 63 unique, 2 disambiguated by path, 2 unresolvable.

### 2.3 Coverage gap closed

Three negative-API failure modes had test classes but **no suite XML whatsoever** — 227 tests that had
never executed:

| New suite | Classes |
|---|---:|
| `API_Suites/Negative/InvalidDataType.xml` | 76 |
| `API_Suites/Negative/InvalidValue.xml` | 76 |
| `API_Suites/Negative/MissingParameter.xml` | 75 |

⚠️ **These 227 tests have never run.** First-execution failures reflect genuine untested behaviour, not
regressions from this work. Triage in Phase 1 before treating any as a defect.

### 2.4 Files changed

| Change | Count |
|---|---:|
| Suite XMLs modified | 75 |
| Suite XMLs created | 3 |
| **Java files modified** | **0** |
| Files touched outside the automation tree | **0** |

Phase 0 was XML-only by design — zero refactor risk, fully revertible.

**Cumulative file changes across Phases 0 + 1:**

| Change | Count |
|---|---:|
| Suite XMLs modified | 75 |
| Suite XMLs created | 3 |
| Java files modified | 1 *(comment only — `VaultPasswordTest`)* |
| Files touched outside the automation tree | **0** |
| Compile status after every change | **BUILD SUCCESS** |

### 2.6 Repo migration — 2026-07-27

Phases 0 and 1.5 were originally carried out in the developer repo at `pam/AutomationTesting/`. That
was the wrong home: the developer repo is the *delivery target*, not the development surface. All
86 changed files were relocated to the bootstrap repo and the developer repo was restored.

| Step | Result |
|---|---|
| Branch `AI` cut from `Dev` in `pam_automation_bootstrap` | ✅ |
| 83 modified + 3 new files copied across | ✅ |
| Baseline check — bootstrap content vs `pam` HEAD, all 83 files | ✅ identical, so the transfer carried the changes and nothing else |
| Diff equivalence — `git diff --numstat` in both repos | ✅ identical: 83 files, +461 / −448 |
| `pam/AutomationTesting/` reverted (`checkout` + `clean -fdx`) | ✅ `git status` clean, including ignored `target/` and `Execution_Reports/` |
| Backup of the pre-revert tree (2,897 files, 20.6 MB) | ✅ session scratchpad `bk_AT/` |

From here on, all work happens in `pam_automation_bootstrap` on branch `AI`.

### 2.7 Graphify knowledge graph — 2026-07-27

`graphifyy 0.9.28` installed via UV and indexed against the automation repo. Full record in
`Graphify.md`. Setup only — no automation code was changed.

| | |
|---|---|
| Indexed | 1,075 Java files → 17,275 nodes / 46,905 edges / 869 communities |
| Cost | 0 tokens — `--code-only` AST extraction, no LLM key |
| Import cycles | none detected |
| Artefacts | `graphify-out/` (gitignored, ~55 MB) |
| Claude Code | `CLAUDE.md` + `PreToolUse` hooks in `.claude/settings.json` |
| Not indexed | the 132 suite XMLs — no XML grammar in Graphify |

God-node ranking independently confirms the refactor targets already named in `plan.md`:
`ApiHelper` (1,091 edges), `BaseTest` (1,055), `BasePage` (240).

**Use it for Phase 2 sizing.** `graphify affected "BaseTest" --depth 1` gives the concrete blast
radius of a shared-layer change with `file:line` precision — cheaper and more complete than grep,
and available now despite blocker B1.

### 2.5 Incidental findings (queued, not actioned)

| Finding | Detail | Queued for |
|---|---|---|
| Suite XML inside the Java source tree | `src/test/java/com/arcon/tests/UI/CRUD/AdministrativeConsole/WebSM_Other.xml` is a TestNG suite living in a Java package directory. It held a dead `E2E.AdminConsole.PAMLogs.LOBLogsTest` reference, now corrected. It should move to `CRUD_Suites/` — a duplicate already exists at `Temp/WebSM_Other.xml`. | Phase 6 |
| `CRUD_Suites/SessionMonitoring.xml` exists but all 8 `UI.CRUD.SessionMonitoring` classes are orphaned | The suite does not reference the module's own test classes | Phase 4, increment 5 |
| 13 dead `@Test` blocks reference a deleted `DataProviderUtils` class | Unrecoverable — the class exists nowhere in the repo | Phase 6 |
| `Temp/` holds near-duplicates of real suites | `Temp/WebSM_Other.xml` vs the misplaced `src/.../WebSM_Other.xml` | Phase 6 |

---

## 3. Phase 1 — Green Baseline · PARTIAL

| Step | Action | Status | Result |
|---|---|---|---|
| 1.1 | `mvn clean test-compile` | ✅ | **BUILD SUCCESS** — 1,063 sources, 26.7 s |
| 1.2 | Execute each suite, capture pass/fail/skip | ⛔ **BLOCKED** | See §5 |
| 1.3 | Record baseline in `baseline.md` | ⛔ Blocked by 1.2 | |
| 1.4 | Triage every skip | ⛔ Blocked by 1.2 | |
| 1.5 | Annotate disabled tests with a reason | ✅ | **Baseline metric was wrong — see §3.2** |

### 3.2 Correction: 1 disabled test, not 14

The audit reported 14 `enabled = false` occurrences. On inspection **13 of those are inside
commented-out `@Test` lines** — the grep counted dead comment text, not live annotations.

There is exactly **one** genuinely disabled test:

| Test | Reason |
|---|---|
| `UI.EndToEnd.PasswordVault.VaultPasswordTest.updateRequiredApplicationList` | Environment provisioning, not a regression test. It calls `deleteAllEntries(...)` on the ACMO Application List and re-creates every entry from the current environment's URLs — it mutates shared environment state rather than asserting product behaviour. Running it inside a suite would wipe the application list for every concurrent test. |

Annotated in place with that rationale plus a `PAMIT-TODO` asking the module owner to confirm and,
if agreed, relocate it out of `tests/` into a provisioning utility so it stops counting as a skip.

**Related dead-code finding:** all 13 commented-out `@Test` blocks reference
`DataProviderUtils.class`, a class that **does not exist anywhere in the repo** (the real providers are
`UI_DataProviderUtils`, `API_DataProviderUtils`, `Negative_API_DataProviderUtils`). They are
unrecoverable dead code — queued for Phase 6.

They sit in:
`NotificationTest`, and the 6 `OneTimeServiceAccessRequest*LevelTest` + 6 `TimeBaseServiceAccessRequest*LevelTest` classes.

### 3.1 Build environment note

`mvn` is installed at `C:\Program Files\apache-maven-3.9.15-bin\apache-maven-3.9.15\bin\mvn.cmd` but is
**not on the Bash PATH** — it is reachable from PowerShell only.

`JAVA_HOME` points at `C:\Program Files\Java\jdk-26.0.1`, **which does not exist** on this machine
(only `jdk-26.0.2` is installed). Maven therefore fails immediately with
*"The JAVA_HOME environment variable is not defined correctly."*

This is a pre-existing machine configuration fault, not something introduced by this work.

**Workaround used** (session-scoped, no system change):

```powershell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot"
mvn -o clean test-compile -DskipTests
```

JDK 21 was chosen because `pom.xml` declares `<java.version>21</java.version>`. Fixing the system
`JAVA_HOME` permanently is outside the editable scope and is a machine/CI-agent action.

---

## 4. Cumulative Metrics

Tracked against the Phase 0 audit baseline. Only rows Phase 0 touched have moved.

| Metric | Baseline | Current | Target |
|---|---:|---:|---:|
| Broken suite references | 341 | **0** ✅ | 0 |
| Orphaned test classes | 737 | **218** | 0 (or documented) |
| Assertions in `pages/` | 285 | 285 | 0 |
| Assertions in `BasePage` | 24 | 24 | 0 |
| Assertions in `tests/` | 5 files | 5 files | all |
| Direct `BasePage` calls from tests | 266 | 266 | 0 |
| `hardWait(int)` calls | 939 | 939 | 0 |
| `Thread.sleep` | 401 | 401 | 0 |
| `waitForTimeout` | 121 | 121 | 0 |
| `System.out.println` | 1,127 | 1,127 | 0 |
| `e.printStackTrace()` | 127 | 127 | 0 |
| API endpoints under automated validation | 0 | 0 | 1,161 |
| Endpoints excluded for want of a payload/seed | — | 175 | 0 |
| Build-to-build drift detection | none | none | per build |
| Commented-out code lines | ~3,219 | ~3,219 | 0 |
| `enabled = false` without a reason | 1 *(not 14 — see §3.2)* | **0** ✅ | 0 |
| Dead `@Test` blocks citing a deleted `DataProviderUtils` | 13 | 13 | 0 (Phase 6) |
| API content validation | none | none | Excel-driven |

---

## 5. Blockers

| # | Blocker | Impact | Needed to clear |
|---|---|---|---|
| **B1** | No PAM environment reachable from this machine to execute suites | Phase 1.2–1.4 cannot complete, so there is no green baseline. Phases 2–4 are refactors that **must** be measured against a baseline. | An environment name from `Environments/` that is currently up, plus network access to it. |
| **B2** | System `JAVA_HOME` points at a non-existent JDK | Any `mvn` invocation fails unless `JAVA_HOME` is overridden per-session | Machine/CI-agent fix — outside editable scope |

**B1 is the gating item.** Proceeding into Phase 2 without a baseline means shared-layer changes to
`BasePage` and `BaseTest` — which every one of the 883 test classes inherits — would be unverifiable.

---

## 6. Decisions Taken

Recorded in `plan.md` §1. Unchanged so far.

| # | Decision | Status |
|---|---|---|
| A1 | Governing structure = `playwright-advance-e2e.SKILL.md` | Active |
| A2 | Strip assertions from Pages (285); retain in Helpers (559) | Active — not yet applied |
| A3 | Pilot `UI/login` + `UI/CRUD/AdministrativeConsole`, then roll out | Active |
| A4 | API content validation via new columns on existing Excel tables | Active |

---

## 7. Open Questions for the Owner

| # | Question | Blocks |
|---|---|---|
| Q1 | Which environment should the baseline run against? | Phase 1.2 — **critical path** |
| Q2 | `PAMLogs.All` vs `All_New` — does `All_New` supersede `All`? | 127 orphans, Phase 6 |
| Q3 | Two `PAMIT-TODO` refs — restore the class or delete the entry? | `orphans.md` §3 |
| Q4 | Are `SNOWApi` / `KotakSNOWApi` deliberately excluded from regression? | 4 orphans |
| Q5 | Confirm A2 (Helpers keep assertions) before Phase 3 starts | Phase 3 sizing |

---

## 8. Next Action

Every step that can be completed without a live PAM environment is now done. Phases 0 and 1.1/1.5 are
closed; the compile is green after each change.

**Blocked on B1** — answer Q1 (which environment to baseline against) and Phase 1.2 can run, which then
unblocks Phase 2.

**Available now without an environment**, if you want work to continue in parallel:

| Option | Phase | Risk | Notes |
|---|---|---|---|
| Add auto-wait primitives to `BasePage` (additive only; deprecate `hardWait`) | 2.2 / 2.3 | Low | Purely additive — nothing calls them until a module migrates |
| Remove the 13 dead `@Test` blocks citing the deleted `DataProviderUtils` | 6.4 | Very low | Provably unrecoverable; compile-verifiable |
| Delete `APIConfigOld.java` and the archetype stub `App.java` | 6.1 / 6.3 | Very low | Compile-verifiable |
| Write `reference-pattern.md` from the `UI/login` module | 3 | None | Documentation only |
| Build the suite-integrity and banned-pattern build checks | 7.2 / 7.3 | Low | Would have caught the Phase 0 defect automatically |

Recommended: **7.2/7.3 first** — a suite-integrity check would have caught the 341 broken references
before they reached CI, and it is verifiable without an environment.
