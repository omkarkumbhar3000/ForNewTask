---
paths:
  - "Automation gitlab repo/**"
  - "**/pam_automation_bootstrap/**"
  - "pam/AutomationTesting/**"
---

# Automation repo — what `AGENTS.md` does not tell you

⚠️ **`pam_automation_bootstrap/CLAUDE.md` is the authority for this repo** — it is the file that actually
auto-loads. It imports `AGENTS.md` (`@AGENTS.md`), which loads as its appendix and owns layout, run
commands, config order, TestNG suites, project structure, listeners and Jenkins. **Do not restate either
here or in the root `CLAUDE.md`.**

*Corrected under `OBJ-013`.* This file previously named `AGENTS.md` as the authority "because it is
imported by `pam_automation_bootstrap/CLAUDE.md`" — **that import did not exist**, so the designated
authority never loaded, while the file that did load told you to prefer itself. Three files disagreed.
The import is now real and the precedence is stated once, here and in the repo file. Where they disagree
on a number, neither wins: `state/drift/facts.json` is the tiebreaker.

This file holds only what `AGENTS.md` omits, plus the two workspace-level facts that matter before you
touch the code.

## Two latent defects — grep confirms neither is in `AGENTS.md`

Both are harmless at today's test counts and bite as soon as you scale up:

- **`APIExcelReportUtil` has a data race.** It increments a `static int rowIndex` with no synchronisation
  while API suites run `parallel="classes"`. Rows can overwrite each other in `Api_Report.xlsx`.
- **`ApiHelper` leaks Playwright instances.** It calls `Playwright.create()` per request and never closes
  them. At 1,300+ requests this is a real resource problem.

Fix both before building anything that reflects over the full endpoint catalogue.

## Do not add RestAssured

API tests use Playwright's `APIRequestContext`. RestAssured is declared in `pom.xml` but effectively
unused — two legacy holdouts remain in `pages/acmo/api/`. The repo's own `README.md` still advertises
"Playwright (UI) + REST Assured (API)"; that is unedited GitLab template boilerplate. Ignore it in favour
of `AGENTS.md`.

## `src/main` is dead

All 1,073 source files live under `src/test/java/com/arcon/`. `src/main/java` holds nothing but the Maven
archetype's `com/arcon/tests/App.java` Hello-World stub. **Do not migrate code into it.**

## The two highest-blast-radius files

- **`utils/BaseTest`** (~1,300 lines) — thread-local Playwright/browser/page state, `launchApplication()`,
  ~40 lazy page-object getters. Every UI test extends it.
- **`utils/ApiHelper`** (~1,640 lines) — **extends `BaseTest`**, so API tests inherit browser machinery
  they never use. Holds the HTTP client, `getToken()`, 66 payload-helper getters and the
  `validateApiResponseWithResponseTime_*` family.

Changing either touches nearly every test in the repo. Check the graph (`graphify affected "<class>"`)
before editing.
