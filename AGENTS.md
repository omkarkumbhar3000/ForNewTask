# AGENTS.md — ForNewTask (BLAST framework + CleverCubs build)

`CLAUDE.md` is the operating guide — read it first. `BLAST/Objective.md` is the one active instruction and
overrides this file. This file holds only what an agent cannot infer from the file tree.

*Verified 2026-09-26 against the working tree by running it. The uncommitted work is newer than
`BLAST/task_plan.md`, the issue register and this file's own earlier revision — **the tree is the truth,
those files lag it** (§11).*

> ✅ **The application is complete (B0–B8) and verified** (2026-09-27): 219 tests, 0 failures, on MySQL
> **and** on PostgreSQL (`-Dclevercubs.test.db=postgresql`); Playwright journeys 6/6 at 1440 and 375 px,
> against the dev server and against the cloud image. The cloud copy runs on PostgreSQL from Neon (`D73`).
> The state, the requirement check and what is open are in
> `New Task/Updated Project/docs/06-review-summary.md`; the cloud deployment in `docs/07-deployment.md`.
> Sections §6, §10 and §11 below were updated for the finished build. Reading a nullable column: use an
> explicit type (`LocalDateTime`, `Long`) with `rs.getObject(i, Type.class)`, never `Object.class`.

## 1. Read the objective yourself — nothing injects it for you

Claude Code gets `BLAST/Objective.md` injected on every prompt by a `UserPromptSubmit` hook
(`.claude/settings.json` → `BLAST/hooks/inject-objective.ps1`). **OpenCode and every other agent must read it
manually**, at the start of every session and before every task.

For a substantive instruction (build, analyse, fix, run, produce): archive the outgoing objective to
`docs/history/01-objective-records.md` + its row in `docs/history/README.md` §3 → rewrite its `## Instruction`
block → ask genuine ambiguities as multiple-choice questions → execute → append what changed and what was
learned to `docs/history/`. Questions, chat replies and config changes do not trigger this; a correction
amends the current instruction instead of replacing it. Keep the file under 10,000 characters (the hook
truncates above that).

## 2. Boundaries

| Path | Rule |
|---|---|
| `BLAST/` | Reusable framework only. No project data, names or keys. Has its own `CLAUDE.md`. ⛔ Never `@`-import `Objective.md` anywhere — an import resolves once at session start and goes stale |
| `New Task/Current Project/Kids_learn_project/` | The owner's uploaded baseline, read-only, primary source of truth, never modify. 388 files / 577.6 MB — 44 flat HTML pages, 6 PHP endpoints, 1 `.pptx`, 337 media files, 0 `.js`/`.css`/`.sql`. **No SQL schema was ever supplied.** Its pre-existing breakage is catalogued in `Updated Project/docs/01-baseline-analysis.md` §9 — findings there are baseline issues, **not regressions** |
| `New Task/Updated Project/` | The only place development output goes. Single Maven module, not a multi-module build |
| `docs/history/` | Append-only. Never edit an existing entry (the live objective's Status row in README §3 is the one exception) |
| `tools/` | Root-level reusable toolkit. A project's own tooling lives inside `Updated Project/` |

## 3. Git: commit and push are allowed (`D72`, replacing the local-only `D55`)

- **Media goes through Git LFS.** `New Task/Updated Project/media/.gitattributes` routes every media file
  there to LFS. A new media file must be covered by an LFS rule **before** it is staged; moving a file to LFS
  afterwards means rewriting history. The largest file is 83 MB (GitHub's hard limit is 100 MB).
- **The baseline `New Task/Current Project/Kids_learn_project/` stays out of the repository** (`.gitignore`).
  Its content is migrated into `Updated Project/` (content JSON plus `media/`, sha256-checked); it remains
  on disk only for re-running `tools/extract_content.py`.
- Never commit secrets (`.env` is ignored at both levels; only `.env.example` is tracked) or generated files
  (`app/target/`, `.tmp/`, `node_modules/`, `e2e/test-results/`, `.playwright-mcp/`).

`.claude/settings.json` denies `git merge` and `git remote set-url` in both shells. A refused merge is that
rule working, not a bug.

## 4. Commands — exact, and they will fail if you guess

**`JAVA_HOME` is broken machine-wide.** It points at `jdk-26.0.1`, a folder that does not exist; the only
real JDK is `jdk-26.0.2`. `mvn` on `PATH` *and* `mvnw.cmd` both abort with *"The JAVA_HOME environment
variable is not defined correctly"* until you set it. Set it in the same command, every time. **`mvnw.cmd`
lives inside `app/`**, so `-f` alone is not enough.

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-26.0.2"      # required before ANY maven command
$app = ".\New Task\Updated Project\app"                   # run from the repository root

& "$app\mvnw.cmd" -f "$app\pom.xml" verify                            # the gate: 219 tests, GREEN
& "$app\mvnw.cmd" -f "$app\pom.xml" test "-Dclevercubs.test.db=postgresql"   # the same suite on PostgreSQL 17
& "$app\mvnw.cmd" -f "$app\pom.xml" test -Dtest=QuizAttemptTests      # one class
& "$app\mvnw.cmd" -f "$app\pom.xml" test -Dtest='SecurityConfigurationTests#unmappedPathStillRequiresASession'
& "$app\mvnw.cmd" -f "$app\pom.xml" spring-boot:run -Dspring-boot.run.profiles=dev   # then http://127.0.0.1:8080
powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\start-dev.ps1" -Restart   # db + build + start
```

`verify` is the **whole** backend gate: `pom.xml` declares no lint, formatter, typecheck or code generator.
Browser journeys: `cd "New Task\Updated Project\e2e"; npx playwright test` (the app must be running; uses the
installed Chrome). Page weights: `node measure.mjs` in the same folder.

- **Docker Desktop must be running** — Testcontainers starts a real MySQL 8.4. `docker version` first if in
  doubt; a cold run spends ~30 s booting the container, and that is not a hang.
- ⛔ **`spring-boot:run` forks a child JVM that outlives the wrapper.** `Stop-Process` on the `mvnw` process
  leaves the app holding **:8080**, and that child may refuse `Stop-Process`/`taskkill` with *Access is
  denied* from a tool session. Check `Get-NetTCPConnection -LocalPort 8080` before starting a second run.
- The `Mockito is currently self-attaching` / `byte-buddy-agent` / `EnableDynamicAgentLoading` warnings on
  every build are **benign JDK 26 noise**, not a failure.
- **Docker Compose only works from `New Task/Updated Project/`**, the only folder with a compose file.
  `CC_DB_*` values come from the sibling `.env`; compose **refuses to start** with
  `:?Set CC_DB_ROOT_PASSWORD in .env` if it is missing.
  `docker compose up -d` · `docker compose down` (keeps data) · `docker compose down -v` (deletes data).
- **Python:** `python` resolves to the failing WindowsApps stub and `py` does not exist; the interpreter is
  `python3.11` (3.11.9, no packages). Root `tools/` needs a venv (`python3.11 -m venv .venv`, then
  `.venv\Scripts\python -m pip install -r tools\requirements.txt` for python-docx, openpyxl, pypdf). The
  project's content extractor is stdlib-only, so it needs no venv:
  `python3.11 "New Task\Updated Project\tools\extract_content.py" --dry-run` (flags: `--baseline`,
  `--out-content`, `--out-media`, `--dry-run`).
- Boot check that proves more than a port: `GET /api/v1/public/health` runs `SELECT 1`, so `200
  {"status":"UP"}` means Flyway ran **and** the DB is reachable; `GET /parent/dashboard` answers `302
  /login?next=…`.
- ⛔ **`POST` without an `X-XSRF-TOKEN` header is 403 even on a `permitAll` route.** A hand-rolled
  `Invoke-WebRequest -Method Post` to `POST /api/v1/auth/register` returns **403, not the 404 you would
  expect** from the missing controller. Do not read that 403 as "CSRF is broken".

## 5. `app/` must stay a direct child of `Updated Project/` — three relative paths depend on it

Easy to break by moving the folder, and the failures look unrelated to the move:

| Consumer | Resolves | Breakage if `app/` moves |
|---|---|---|
| `TestDatabase` copies the init script from `../db/init/01-users.sh` (relative to Surefire's `${basedir}`) | `app/` | Testcontainers fails to start the database |
| `application.yml` dev profile does `spring.config.import: optional:file:../.env[.properties]` | `app/` | Silently no credentials — the `dev` boot fails on a missing `${CC_DB_APP_PASSWORD}` |
| `clevercubs.media-root` defaults to `../media` | `app/` | Media 404s |

## 6. How the security layer works — the rules every feature follows

`platform/security/` plus `account/` implement the approved Blueprint (`docs/04` §4.1). Every feature
package (`child`, `content`, `learning`, `quiz`, `reward`, `family`, `feedback`, `admin`) is built on it.
The rules below are what a change must respect; the historical notes marked *(earlier state)* describe
how the build got here and are kept because the reasoning still applies:

- **Identity comes from the server session only.** `SessionAuthentication` is the single source; no
  endpoint may trust a user or child ID sent by the browser. Services resolve the caller through
  `CurrentUser` (`session()`, `accountId()`, `activeChildId()`, `requireMode(Role)`) — never from a
  parameter. **Ownership is checked in the service layer, not the URL** (fixes `SEC-E04`).
- **Built and tested:** `POST /api/v1/auth/login`, `GET /api/v1/auth/me`, `POST /api/v1/auth/logout`,
  `POST /api/v1/auth/reauth`, **`POST /api/v1/auth/change-password`**, plus `AccountAuthenticationProvider`
  (bcrypt, generic refusal message, equalising hash so timing does not reveal whether an address exists,
  lock/disabled checks, audit of every refusal and sign-in), `ReauthenticationToken`/`ReauthenticationConfirmation`,
  `PasswordChangeService` and `PasswordChangeRequiredFilter`.
- **Now built (2026-09-27):** registration with consent (`RegistrationService`), the child/parent switch
  (`SessionModeController`), the account lock after five failures plus a per-address throttle
  (`AccountAuthenticationProvider`, `LoginThrottle`), one password rule for every path (`PasswordPolicy`,
  `DD-01` in full, applied to registration and password change), the recent-password guard for sensitive
  actions (`RecentAuthentication`, `DD-26`), and every learning, parent and admin endpoint (list in
  `Updated Project/README.md` §5). The bootstrap still only *warns* on a short password (`D69`).
- `PasswordChangeRequiredFilter` now guards **the data API only** (`/api/**`): page shells, scripts and styles
  load, so a flagged account can reach the change-password form; every data call is still refused.
- **The password-change route is deliberately narrow.** `PasswordChangeRequiredFilter`'s
  `ALLOWED_WHILE_FLAGGED` is an explicit list — `GET /me`, `POST /logout|login|reauth|change-password` and
  `/api/v1/public/**` — and nothing else. A `must_change_password` account is refused everywhere else.
  The list is closed: a route added to it later is refused until someone adds it, exactly like
  `SecurityConfig`. The bootstrapped Super Admin lands in this state (`D69`) and `change-password` is the
  way out of it.
- ⛔ **Two things in `PasswordChangeService` look like redundancy and are not.** (a) The current password is
  verified with `ReauthenticationToken`, **not** a plain `UsernamePasswordAuthenticationToken`: the provider
  treats the former as "not a sign-in" and therefore leaves `last_login_at` and `AUTH_LOGIN_SIGNED_IN`
  alone. Swapping it for the plain token silently turns every password change into a fake sign-in.
  (b) `AuthController.store(...)` is shared by `login` and `change-password` and does **not** rotate the
  session id; only `login` calls `request.changeSessionId()`, just above it. Adding a rotation to the shared
  helper would invalidate the session of a client that is mid-task. Invalidating *other* sessions after a
  change is a separate feature and is **not** built.
- **Admin bootstrap is built and idempotent** (`account/AdminBootstrap`, an `ApplicationRunner`, `D69`). It
  inserts one `SUPER_ADMIN` on startup only when **both** guards pass: the configured address has no account
  *and* no `SUPER_ADMIN` exists at all. It never updates or unlocks anything, writes one `ADMIN_BOOTSTRAPPED`
  audit row via `AuditLog` (actor `SYSTEM`) on creation only, and sets `must_change_password = true`. Needs
  no migration: `V1__schema.sql` has the columns and `afterMigrate.sql` already grants the insert.
  - ⛔ **`@SpringBootTest` runs `ApplicationRunner` beans, and the test profile shares this database.** A
    stray `SUPER_ADMIN` row left by a test makes every later bootstrap assertion silently pass for the wrong
    reason, because the guard refuses to create anything. Clean up by **email address** and register the
    address *before* the first use, never by an id that may not exist yet — this cost four tests once.
- **Child mode drops the parent's authority.** `SessionAuthentication.childMode(...)` replaces `ROLE_PARENT`
  with `ROLE_CHILD` + `activeChildId` (`D58`), so a child session is refused in `/parent/**` and `/admin/**`.
- **`SecurityConfig` is an explicit allow list ending in `anyRequest().authenticated()`** — a route added
  later is closed until someone opens it. Public openings: `OPTIONS /**`, `/api/v1/public/**`, `/login`, and
  `POST /api/v1/auth/register|login`. HTTP Basic, form login and the default logout are all disabled on
  purpose (`AuthController` owns all three).
- **Two refusals, chosen by path not by `Accept`:** unauthenticated API → `401`, unauthenticated page →
  `302 /login?next=…` (`next` rebuilt from the request's own URI and rejected unless local, so
  `//evil.example` and `/\evil.example` cannot turn the login page into an open redirect), wrong role → `403`.
- **Errors are RFC 9457 problem+json** with `type` = `urn:clevercubs:problem:<code>` and a stable `code`
  (`unauthenticated`, `forbidden`, `not-found`, `invalid-input`, `invalid-credentials`, `server-error`, …).
  Clients branch on `code`, never on text. Throw `ApiException` for anything a caller may be told about;
  anything else becomes a generic 500 with detail logged, never returned. `ApiProblemEntryPoint` reuses
  `ApiExceptionHandler.problem` to build the identical body *inside* the filter chain, bypassing the advice.
- **CSRF token rides in the `X-XSRF-TOKEN` header** (`DD-03`); the cookie is deliberately not `HttpOnly`
  (it is not a credential). The CSP forbids `unsafe-inline` and any third-party origin (`DD-11`, `DD-12`).
  Session cookie is `CCSESSION`, `HttpOnly`, `SameSite=Lax`, `Secure` unless the `dev` profile.

## 7. Database rules an agent will get wrong

- **Two users, never root.** `cc_migrator` owns the schema and runs Flyway; `cc_app` is the least-privilege
  user the application connects as. `db/init/01-users.sh` creates both and is reused **verbatim** by
  Testcontainers, so tests exercise the real grants. Don't add a root connection.
- **Migrations live in `app/src/main/resources/db/migration/mysql/` and `…/postgresql/`** (`D73`; Flyway
  picks the folder by database): `V1__schema.sql` = **27** tables, `V2__reference_data.sql`, `V3`, `V4` (the
  two Spring Session tables), `afterMigrate.sql`. Add schema as a new `V<N>__` file **in both folders**; never
  edit an applied one. `DatabaseSetupTests` asserts the **exact** table list, so a new table means updating
  that test too. Every SQL statement must run on both databases: the rules are in `CLAUDE.md`.
- ⛔ **A new table needs a matching `GRANT` in both `afterMigrate.sql` files in the same change**, or the
  application user hits `denied` at runtime even though the migration succeeded. `audit_event` is deliberately
  `SELECT, INSERT` only — the trail is append-only, which `DatabaseSetupTests` proves on both databases.
- **Admin-editable business rules live in the `system_setting` table, read through `Settings`**, never in
  config. Eight seeded keys (`V2__reference_data.sql`): `progress.lesson_weight_percent` 70,
  `quiz.max_attempts` 3, `quiz.grant_attempts` 3, `quiz.default_pass_mark_percent` 70,
  `reward.threshold_percent` 80, `session.child_idle_minutes` 30, `parent.reauth_minutes` 15,
  `consent.document_version` 2026-09-draft. `Settings.update` rejects unknown keys on purpose, so a new rule
  needs a migration first. Never hardcode these numbers. `CleverCubsProperties` is for deployment values
  (media root, contact email, admin bootstrap) only.
- Persistence is `JdbcClient` with **named `:parameters`** and text blocks — no ORM, no entity manager, no
  repository interfaces. `AuditLog` is the only writer of `audit_event`; details carry identifiers and
  outcomes, never passwords, names, email addresses or free text.

## 8. Spring Boot 4.1 and JDK 26 — stale Boot 2/3 knowledge is the trap

- **Jackson 3**: the packages are `tools.jackson.databind.*`, not `com.fasterxml.jackson.*` (see
  `ApiProblemEntryPoint`, `AuditLog`). Boot 4's `ObjectMapper` bean is Jackson 3's.
- **Starter renames**: no `spring-boot-starter-web` (it is `-webmvc`), no `-data-jdbc` (it is `-jdbc`),
  Flyway comes through `spring-boot-starter-flyway`, and there is no umbrella `spring-boot-starter-test` —
  one `-test` starter per area (`-webmvc-test`, `-jdbc-test`, `-flyway-test`, `-security-test`,
  `-validation-test`).
- `@AutoConfigureMockMvc` now lives in `org.springframework.boot.webmvc.test.autoconfigure`, not
  `org.springframework.boot.test.autoconfigure`.
- `@RestControllerAdvice` and `spring.mvc.problemdetails.enabled` are on; the advice is hand-written anyway.
- `pom.xml` targets Java 25 and builds under the local JDK 26.0.2. Jackson and AOP arrive transitively —
  declaring them is not the house style.

## 9. Testing conventions

- Unit = JUnit 5, **no Spring context** when the decision is a pure function (see
  `LoginRedirectEntryPointTests`). Integration = extend `org.clevercubs.support.IntegrationTest`
  (`@SpringBootTest` + `@AutoConfigureMockMvc` + `@ActiveProfiles("test")`); one shared `TestDatabase`
  container and one Spring context for the suite is what keeps it fast.
- The `test` profile never reads `.env`; `TestDatabase.register` injects the container URL and both users as
  dynamic properties. `application-test.yml` is the only test config.
- **Idiom for a route whose controller does not exist yet:** assert the request *passed the security layer*
  (`assertPassedSecurity` in `SecurityConfigurationTests` — status not in 401/403) and do not assert the 404
  that follows. It belongs to a later phase. Note the CSRF trap in §4: a POST needs
  `with(csrf())` or it is 403 for the wrong reason.
- An HTTP 200 is not a pass when the body carries an application error — assert the application-level result.
  Never claim done without running `verify`.
- ⛔ **The test database is shared and `@SpringBootTest` runs `ApplicationRunner` beans,** so a test that
  creates a `SUPER_ADMIN` poisons every later one: the bootstrap's own guard then correctly refuses, and the
  next test fails looking like a product bug. Register a row for cleanup at the moment you generate its
  **email**, and delete by that email — never by an id read before the insert. See §6 and
  `AdminBootstrapTests` for the shape that works.
- **Collision-free fixture rows** (the idiom in `PasswordChangeTests.createAccount`): a UUID in the address,
  `role.toLowerCase() + "-" + UUID + "@example.test"`. `Role` has only three values, so a fixed address per
  role collides the moment a second test picks the same one.

## 10. Not built, or waiting for the owner — never report these as working

Waiting for information (`docs/02-issue-register.md` §5): the contact address (`INF-02`), the legal review
(`INF-03`), an email provider and so self-service password reset (`INF-04`), content for 6–8 and a Year 2
(`INF-01`), the missing story video (`INF-09`), body-parts audio (`INF-10`), media licences (`INF-11`).
The contact address stays unset by the owner's choice (`D75`). Waiting for the owner's review: re-encoding
the videos themselves (the pictures and the MP4 indexes are already optimised, `DD-29`). Open by choice:
`SEC-R01` (registration reveals a taken email, `DD-22`).

## 11. Current state

`OBJ-034` is in its completion run (`BLAST/Objective.md`): **B0–B8 are complete and verified**
(`docs/06-review-summary.md`, `docs/04` §9 status column, `BLAST/task_plan.md`), and the build is published
on GitHub (`D72`, public by `D74`). The issue register §6 records every baseline issue against the build
with its test. **Production is live at https://clevercubs.vercel.app** (Vercel, Neon PostgreSQL; built
from GitHub on every push to `main`), verified on 2026-09-27 (`docs/07-deployment.md` §9). What still needs
the owner is in `docs/06-review-summary.md` §8.

## 12. Conventions

- **Issue register (`Updated Project/docs/02-issue-register.md`):** an issue never changes ID. `SEC-E`/`FUN-E`
  = in the baseline, `SEC-R`/`FUN-R` = introduced by this build, `INF-` = information still required. An `E`
  moves to **F only with the test that proves the fix**.
- **A new dependency needs its reason recorded in `docs/04` §3 first.** No JS or CSS framework, no Lombok, no
  ORM, no CDN scripts (`DD-12`). **When `docs/04` §3 and `pom.xml` disagree, `pom.xml` wins** — it is what
  builds. Owner decisions `DQ-nn` in `docs/03-decisions.md`; documented defaults `DD-nn`; both are cited by
  number in code comments.
- **Markdown:** use the Edit tool. Never rewrite a `.md` through PowerShell `Set-Content` or
  `Get-Content`+write — PS 5.1 reads UTF-8 as ANSI, so every em-dash and curly quote turns to `?` (this file
  and `BLAST/Objective.md` are full of them). Pass `-Encoding UTF8` when you must read one from the shell.
  Same for Python `write_text` (truncates before encoding — this destroyed 12.7 KB once). One fact lives in
  one layer; cross-reference instead of restating. Style: `# Subject — Purpose`, a bold metadata block,
  numbered `## N.` sections, tables over prose, `§N` cross-refs.
- Secrets only in `.env`; only `.env.sample`/`.env.example` are tracked. Never print or commit a credential.
- `tools/paths.py` finds the repo root by searching upward for a directory holding **both** `CLAUDE.md` and
  `.claude/`. Renaming either breaks every tool importing it; never count parent directories.
- Intermediates go to `.tmp/` (gitignored). A generated `.docx`/`.xlsx` is never hand-edited — fix the
  markdown and re-render.
- `mar.md` at the root is the owner's private Marathi companion to CLI sessions, gitignored — keep it that
  way, and do not commit or publish it.

## 13. Environment gotchas

- **PowerShell 5.1, not cmd/bash.** No `&&` — use `; if ($?) { … }`. `Select-String` has **no `-Recurse`**;
  pipe `Get-ChildItem -Recurse` into it or use the Grep tool. **Always quote paths**: `New Task`,
  `Current Project`, `Updated Project` and `VS Code` all contain spaces.
- ⛔ **Drive D: has ~5 GB free** (C: ~37 GB). The B2 media copy needs roughly 420 MB and Playwright's
  browsers download ~300 MB onto C:. Measure free space before any bulk copy (`docs/04` §11).
