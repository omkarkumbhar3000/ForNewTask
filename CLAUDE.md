# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

The reusable **BLAST framework** plus the **`New Task/`** work area for the current development project.
It was a Jira/PAM/CI analysis workspace until `OBJ-031` retired that project; every removed file is
recoverable from checkpoint commit `2a3298d` (`git show 2a3298d:<path>`).

| Path | Is | Rule |
|---|---|---|
| `BLAST/` | The framework: protocol (`B.L.A.S.T.md`), the objective file, memory files, A.N.T. layer skeletons, the objective hook. Has its own `CLAUDE.md` | ⛔ Reusable only. No project data, names or keys |
| `New Task/Current Project/` | The project to improve, as the owner provides it, with its requirement and colleague feedback | ⛔ Baseline. Read and analyse; never modify |
| `New Task/Updated Project/` | The improved project: all new code, configuration, docs and deliverables | ✅ The only place development output goes |
| `tools/` | Reusable toolkit: `render/`, `rag/`, `onboarding/`, `paths.py` (§Toolkit) | A project's own tooling lives inside `Updated Project/`, not here |
| `docs/history/` | Append-only record: objective register, decisions `D-NN`, narrative | ⛔ Never edit an existing entry |
| `.claude/` | `settings.json` (objective hook, deny list) and `rules/markdown-docs.md` | ⛔ The deny list is the owner's to change |
| `AGENTS.md` | The guide for agents other than Claude Code, and the most detailed record of what the build has and lacks | Read §6, §10 and §11 before assuming a feature exists |

Git: branch `main`, remote `github.com/omkarkumbhar3000/ForNewTask`.

This repository is for the **current application's work**. The reusable framework it grew into lives in a
separate repository, `NewProject_Framework` (sibling folder `..\NewProject_Framework`). ⛔ Never put this
project's code or data there; generic improvements to BLAST, rules or tools go there instead of being
rebuilt per project (its `docs/maintaining.md`).

## ⛔ The objective-first rule — the owner's rule; never remove it

**Every substantive CLI instruction (build, analyse, fix, run, produce) goes into `BLAST/Objective.md`
before any work starts, and that file then governs the work and its output.** The owner sometimes calls it
`object.md`; it is `BLAST/Objective.md`.

| Step | Action |
|---:|---|
| 1 | Archive the outgoing objective: its full ten-field record to `docs/history/01-objective-records.md`, its row in `docs/history/README.md` §3. Do this even if no work was done on it |
| 2 | Replace the `## Instruction` block of `BLAST/Objective.md` with the new instruction, faithfully and completely |
| 3 | Read it back and find genuine ambiguities. Fill gaps from the workspace first; never ask the owner to restate what is recorded |
| 4 | Ask what remains as **multiple-choice questions** (`AskUserQuestion`), recommending an option where one is better |
| 5 | Fold the answers into the file, so it matches what was agreed |
| 6 | Execute, with the file as the instruction and the workspace as context |
| 7 | On completion, update the affected docs and append what changed and what was learned to `docs/history/` (narrative; a `D-NN` record for each owner decision) |

- **Does not trigger it:** questions, conversational replies, and process or config changes. **A correction
  amends** the current instruction instead of replacing it.
- ⛔ **Never start implementation against a request that exists only in the chat.**
- **Delivery:** the `UserPromptSubmit` hook runs `BLAST/hooks/inject-objective.ps1`, which injects the rule
  and the file on every prompt. ⛔ Do not also `@`-import the file: an import goes stale after session
  start. If a turn arrives without the injected objective (the hook changed mid-session, or failed), read
  `BLAST/Objective.md` yourself before acting. Hooks are snapshotted at session start, so a hook edit takes
  effect in the next session.
- **Keep the file small** (the hook warns above 10,000 characters). History never goes back into it.
- A durable way of working the owner states belongs **here** and as a decision in `docs/history/02-decisions.md`,
  never only in the objective file, which the next instruction overwrites.

## ⛔ Stage gate and change control

- **Do not implement the new application until the owner has uploaded the material to
  `New Task/Current Project/` and explicitly started that stage.** Do not invent its requirements.
- **Protocol 0 HALT applies to `New Task/Updated Project/`:** no deliverable code until the Discovery
  questions are answered, the design and data shapes are recorded in `BLAST/LLM.md`, and `BLAST/task_plan.md`
  holds an approved Blueprint (`BLAST/CLAUDE.md`).
- **Analyse first, then plan, then build.** Findings go into `Updated Project/` documentation, not only chat.
- **Safe improvements** may be made directly. **Major, destructive or architectural changes** (replacing a
  framework, changing data shape or storage, removing a feature, breaking compatibility) are listed with
  their reason and **need the owner's approval** first.
- **Replace an existing technology only after weighing** the real benefit, the migration effort and
  compatibility, and never at the cost of working functionality.
- If the current project has a design system, extend it rather than adding a second one. Replacing it is a
  major change.

## The current project — `Kids_learn_project` (CleverCubs)

It was uploaded to `New Task/Current Project/Kids_learn_project/` on 2026-09-26. `BLAST/Objective.md` and
`docs/history/README.md` record the current stage; this file does not.

- **The requirement** came through the CLI, not the upload. It is stored verbatim in
  `New Task/Updated Project/docs/00-source-requirement.md`. It asks for a rebuild with a **Java backend**,
  parent, child and Super Admin roles, backend-tracked progress, a three-attempt quiz limit, rewards and a
  light child-friendly UI.
- `CleverCubs.pptx` is the authors' project deck.
- **The project documents are in `New Task/Updated Project/docs/`:**
  - `01-baseline-analysis.md`;
  - `02-issue-register.md`, which uses `SEC-E`/`FUN-E` for baseline issues, `SEC-R`/`FUN-R` for issues
    this build introduces and `INF-` for information still required;
  - `03-decisions.md`, with owner decisions `DQ` and documented defaults `DD`;
  - `04-architecture-and-plan.md` and `05-data-model.md`.

  Read them before changing the design. An issue that is already in the register is a baseline issue, not a
  regression.

- **Shape:** a toddler learning site in one flat folder, with 44 hand-written HTML pages (inline `<style>`
  and `<script>`), 6 PHP endpoints and 337 media files (579 MB). It has no build, package manifest or tests,
  and no separate `.js` or `.css` files. The only external script is `canvas-confetti` from jsDelivr. Code
  comments are Marathi written in Latin script.
- **Page flow:** `index.php` (login and register) → `fisrt_page.html` → `second_page.html` (the lesson hub)
  → `<topic>_voice.html` (a lesson) → `<topic>_quize.html` (its quiz).
  - `quize_page.html` is a second hub, over the `<topic>_qq.html` quizzes, which report back through
    `sessionStorage.lastCompleted`.
  - Nothing links to the `<topic>_q.html` pages.
  - The filenames are misspelt and inconsistent, so match them exactly. Examples: `frutis_`, `fisrt_`,
    `progres_`, `animal_qq` beside `animals_q`, and `vegitables voice.html`, which contains a space.
- **State lives in two places.** The browser keeps `loggedIn`, `username`, `password` and `progress` in
  `localStorage`, and the hub pages lock their cards unless `loggedIn === "true"`. MySQL keeps the users
  and the feedback, and the lesson pages also post progress to it.
- **Backend:**
  - `db.php` connects to MySQL on `localhost` as `root` with an empty password, database `kidslearn`.
    `feedback.php` and `progres.php` open their own connection instead of including it.
  - The tables are `stds` (users, with hashed passwords), `stds2` (feedback) and `std3` (one row per user
    and one column per subject; the posted `subject` names the column).
  - **No schema or SQL dump was supplied.** That is Information Required before the backend can run.
- **Running it here:** PHP and MySQL are not installed on this machine, so only the static pages run.
  - `python3.11 -m http.server 8765 --directory "New Task/Current Project/Kids_learn_project"` serves them,
    including the names with spaces.
  - It serves `index.php` as a download. Start at `fisrt_page.html` instead, and set
    `localStorage.loggedIn = "true"` to unlock the hubs.
  - The login, register, progress and feedback calls fail without PHP.
- **Already broken in the baseline**, so these are not regressions if you find them later:
  - Links to files that were never uploaded: `get_progress.php`, `progress.html`, `learning.html`,
    `index.html` and `body_quiz.html`.
  - Absolute `C:\Users\…` paths from the authors' machines, in `maths_lesson_page.html` and in one video
    source in `frutis_voice.html`.
- **Git (`D72`, which replaced the local-only rule `D55`):** commit, pull and push are allowed. Before
  every commit, check large files, secrets and generated files.
  - `New Task/Updated Project/media/` is committed through **Git LFS** (its own `.gitattributes`). Any new
    media file must be matched by an LFS rule **before** it is staged. The largest file is 83 MB; GitHub's
    hard limit is 100 MB.
  - The baseline `New Task/Current Project/Kids_learn_project/` (579 MB) is **kept out of the repository**
    (`.gitignore`). Its content lives on in `Updated Project/` (content JSON and `media/`, checked by
    sha256). It stays on disk only so `tools/extract_content.py` can be re-run.
  - Never commit `.env`, `target/`, `.tmp/`, `node_modules/`, `e2e/test-results/` or `.playwright-mcp/`.

## The application being built — `New Task/Updated Project/`

A Spring Boot 4.1 modular monolith: one Maven module in `app/`, Java 25 bytecode built on the local JDK 26,
MySQL 8.4 in Docker and Flyway migrations. The pages are plain HTML, CSS and JS modules
(`app/src/main/resources/static/`) calling a versioned JSON API under `/api/v1`, with no frontend framework
and no build step. **B0–B8 are built and verified**; the state and what is open are in
`docs/06-review-summary.md`, the cloud deployment in `docs/07-deployment.md`.

- **The design is `docs/04-architecture-and-plan.md`:** §2 the folder layout, §3 the reason for every
  dependency, §4 security and §9 the build phases. **The schema is `docs/05-data-model.md`** (V3 in §8).
- **`README.md` in `Updated Project/`** is the team's guide: start, try, test, the API list.

### Commands

`JAVA_HOME` is wrong machine-wide: it names a `jdk-26.0.1` that doesn't exist. `mvnw.cmd` fails until you
set it, so set it in the same command. Docker Desktop must be running, because the tests start a real MySQL
through Testcontainers. A cold start takes about 30 seconds; that is not a hang.

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-26.0.2"     # before ANY maven command
$app = ".\New Task\Updated Project\app"                  # from the repository root; mvnw.cmd is in app/

& "$app\mvnw.cmd" -f "$app\pom.xml" verify                                                 # the whole gate
& "$app\mvnw.cmd" -f "$app\pom.xml" test -Dtest=AuthenticationTests                        # one class
& "$app\mvnw.cmd" -f "$app\pom.xml" test "-Dtest=LoginRedirectEntryPointTests#rejectsNull" # one method
& "$app\mvnw.cmd" -f "$app\pom.xml" spring-boot:run -Dspring-boot.run.profiles=dev         # :8080

powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\start-dev.ps1" -Restart   # db + build + start + Chrome
powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\stop-dev.ps1"
cd "New Task\Updated Project\e2e"; npx playwright test      # browser journeys (app must be running)
node measure.mjs                                            # page weights (in e2e/)
```

- **`verify` is the whole backend gate** (212 tests). No linter, formatter or type check is configured.
  The Mockito "self-attaching" and `EnableDynamicAgentLoading` warnings are JDK 26 noise, not a failure.
- **`start-dev.ps1`** finds a working JDK itself, starts MySQL, builds, and starts the jar detached with its
  log in `Updated Project/.tmp/app.log`. ⛔ Do not pipe its output (`| Select-Object`) in a tool call: the
  started JVM inherits the pipe and the call never returns.
- **In the `dev` profile, pages, scripts and styles are served from `src/main/resources/static/`**, so a
  frontend edit needs only a refresh; Java changes need a restart. A browser that cached files from an
  older build may need a hard refresh.
- ⛔ **Check port 8080 before starting another instance** with `Get-NetTCPConnection -LocalPort 8080`.
  `spring-boot:run` forks a child JVM that keeps the port after `mvnw` stops. The team may be using the
  running instance.
- **The database:**
  - Start it with `docker compose up -d` from `New Task/Updated Project/`, which holds the only compose file.
  - Compose refuses to start without the `.env` in that folder, copied from `.env.example`.
  - ⛔ `docker compose down -v` deletes all local data.
- **Boot check:** `GET /api/v1/public/health` runs `SELECT 1`, so `200 {"status":"UP"}` proves that Flyway
  ran and the database answers.
- **Content extraction:** `python3.11 "New Task\Updated Project\tools\extract_content.py" --dry-run`. It uses
  the standard library only.

### Architecture rules that span several files

- **Package by feature** under `org.clevercubs`, with cross-cutting code in `platform/` (security, web
  errors, settings, config). Business rules are plain Java classes, testable without Spring or a database,
  and controllers stay thin (`DD-15`).
- **Identity comes only from the server session.**
  - `SessionAuthentication` is the one source, and services get the caller from `CurrentUser`.
  - Never trust a user or child ID sent by the browser, and check ownership in the service layer
    (`SEC-E04`).
  - Child mode swaps `ROLE_PARENT` for `ROLE_CHILD` (`D58`).
- **Every route is closed until it is opened.** `SecurityConfig` is an explicit allow list ending in
  `anyRequest().authenticated()`, and `PasswordChangeRequiredFilter` keeps its own closed list. A new route
  must be added to them deliberately.
  - An API call without a session gets `401`, a page gets `302 /login?next=…`, and the wrong role gets
    `403`.
  - A `POST` without the `X-XSRF-TOKEN` header is `403`, even on a public route. In tests, use
    `with(csrf())`.
- **Errors are RFC 9457 problem+json with a stable `code`,** and clients branch on that code, not on the
  message.
  - Throw `ApiException` for anything the caller may be told.
  - Anything else becomes a generic 500: its detail goes to the log and is never returned.
- **Persistence is `JdbcClient`** with named `:parameters` and text blocks. There is no ORM or JPA, and there
  are no repository interfaces.
- **Two database users, never root.** `cc_migrator` runs Flyway, and the application connects as the
  least-privilege `cc_app`. `db/init/01-users.sh` creates both and Testcontainers reuses it, so the tests
  run under the real grants.
  - A schema change is a new `V<N>__*.sql` file in `app/src/main/resources/db/migration/`. Never edit a
    migration that has already been applied.
  - ⛔ **A new table also needs its `GRANT` in `afterMigrate.sql`,** or `cc_app` is denied at runtime even
    though the migration succeeded. It also needs adding to the exact table list in `DatabaseSetupTests`.
  - `audit_event` is append-only (`SELECT, INSERT`). Only `AuditLog` writes to it, and it never holds
    passwords, names, email addresses or free text.
- **Admin-editable business rules live in the `system_setting` table and are read through `Settings`.**
  - They include the progress weight, pass mark, attempt limits and reward threshold.
  - Never hardcode them or put them in `application.yml`. A new rule needs a migration first.
  - `CleverCubsProperties` holds deployment values only.
- ⛔ **`app/` must stay directly inside `Updated Project/`.** Three paths are relative to it:
  - `TestDatabase` copies `../db/init/01-users.sh`;
  - the `dev` profile imports `../.env`;
  - `clevercubs.media-root` defaults to `../media`.
- **This is Spring Boot 4 with Jackson 3, not Boot 2 or 3.**
  - Jackson's packages are `tools.jackson.*`.
  - The starters are `-webmvc`, `-jdbc` and `-flyway`, and there is one `-test` starter per area.
  - `@AutoConfigureMockMvc` lives in `org.springframework.boot.webmvc.test.autoconfigure`.
- **A new dependency needs its reason recorded in `docs/04` §3 first.** That section also lists what was
  deliberately left out, such as Lombok, JS and CSS frameworks, and an ORM. There are no CDN scripts
  (`DD-12`). Where `docs/04` §3 and `pom.xml` disagree, `pom.xml` is what builds.

### Tests

- **Integration tests extend `org.clevercubs.support.IntegrationTest`,** which sets `@SpringBootTest`,
  MockMvc and the `test` profile. One MySQL container and one Spring context serve the whole suite, and the
  `test` profile never reads `.env`. A pure decision gets a plain JUnit 5 test with no Spring context.
- ⛔ **The test database is shared, and `@SpringBootTest` runs `ApplicationRunner` beans such as
  `AdminBootstrap`.**
  - Give each fixture row a collision-free email, with a UUID in the address, and clean up by that email.
  - A leftover `SUPER_ADMIN` row makes later bootstrap tests pass or fail for the wrong reason.
- **Drive journeys through `org.clevercubs.support.Journeys`** (register a family, sign in, child mode,
  finish lessons, answer a quiz) and clean up with `journeys.cleanUp()` in `@AfterEach`.
- ⛔ **Never use spring-security-test's `csrf()` post-processor.** It swaps the shared `CsrfFilter`'s token
  repository for a session-based one, which breaks the real `XSRF-TOKEN` cookie for every later test in
  the same context (33 unrelated failures once). Use `Journeys.realCsrf()` or `Journeys.json(...)`.
- ⛔ **Text blocks strip trailing spaces:** `"""...WHERE """ + where` produces `WHEREr.id`. Add the space
  in the concatenation.
- **Jackson 3 refuses a missing primitive** in a request record (an "unreadable" 400, not field errors):
  use `Boolean`/`Integer` for optional fields.
- **For a route whose controller isn't built yet,** assert only that the request got through security
  (`assertPassedSecurity`), not the 404 that follows.
- **An issue moves from `E` to `F` in the issue register only with the test that proves the fix.**

## ⛔ Standing rules

- **Nothing is finished until it is verified.** Say "done", "fixed", "tested" or "validated" only after
  running the check; report a failure with its output, and say plainly what was skipped.
- **Look at a file before deleting or overwriting it.** Edit markdown with the Edit tool only; never through
  PowerShell `Set-Content` or Python `write_text` (`.claude/rules/markdown-docs.md`).
- **Never invent a fact.** Where the source is silent, write one explicit sentinel (`TBD`,
  `Information Required`) and what would settle it.
- **Generated output is never hand-edited.** Fix the source and regenerate (for example a `.docx` rendered
  from markdown).
- **Secrets live in `.env` files**; only `.env.sample`/`.env.example` are tracked. Never print, log or
  commit a credential.
- **An HTTP 200 is not a pass** when an API reports errors in the response body. Assert the
  application-level result too.
- **Frontend quality floor:** responsive down to mobile, visible keyboard focus, `prefers-reduced-motion`
  respected, and an explicit `background` and `color` on the page root.
- **Use installed skills by relevance, not by habit.** For the development stage the likely ones are
  `frontend-design` (UI), `playwright` (browser verification), `test-driven-development`,
  `systematic-debugging` and `code-review`/`security-review` before completion. Jira and PAM workflows are
  not part of this project; `tools/onboarding/` is a dormant kit for API test automation only.

## Toolkit

No build, test suite or linter exists at the root; each tool is verified by running it. Python packages go
in a venv (a distribution-managed Python refuses a global install):

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r tools\requirements.txt      # python-docx, openpyxl, pypdf

.venv\Scripts\python tools\render\md_to_docx_xlsx.py <doc.md>       # -> <doc>.docx + <doc>.xlsx beside it
.venv\Scripts\python tools\rag\extract.py "New Task\Current Project" # PDFs -> .tmp\rag-corpus\ (page-cited)
python tools\rag\query.py find "<terms>"                            # stdlib; cite results as <doc>:p<N>
python tools\onboarding\validate_profile.py --all                   # stdlib; API-testing kit only
powershell.exe -NoProfile -ExecutionPolicy Bypass -File BLAST\hooks\inject-objective.ps1  # one JSON object
```

- `validate_profile.py --all` exits 2 with `[BLOCK] no profiles` until a profile exists beside
  `profiles/_template.json`. That is expected, not a broken kit.

- **On the D: machine** `python` and `py` do not work; the interpreter is `python3.11` (3.11.9, no
  packages), so create the venv with `python3.11 -m venv .venv`. Under Bash set `PYTHONUTF8=1` and
  `PYTHONDONTWRITEBYTECODE=1`.
- ⛔ **`tools/paths.py` finds the root by searching upward for a directory holding both `CLAUDE.md` and
  `.claude/`.** Renaming either breaks every tool that imports it. Never count parent directories.
- Intermediates go to `.tmp/` (gitignored). A project's own dependencies and build live in
  `New Task/Updated Project/`.

## Environment and git notes

- **Primary shell is Windows PowerShell 5.1.** Paths contain spaces (`New Task`, `Current Project`,
  `Updated Project`, `VS Code`); always quote them.
- **`.claude/settings.json` denies `git merge` and `git remote set-url`** in both shells. A refused merge is
  that rule working; only the owner can change it.
- **PDFs are Git LFS objects** (`.gitattributes`); `git lfs` must be installed to clone them as files.
- **A nested `.git` in an uploaded project** is recorded as a pointer, not as files. See `New Task/README.md`.
- `mar.md` at the root is the owner's private Marathi companion to CLI sessions. It is gitignored; keep it
  that way.
