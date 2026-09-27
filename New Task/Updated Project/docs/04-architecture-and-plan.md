# Architecture and Plan — How the enhanced CleverCubs is built

**Objective:** `OBJ-034` · **Requirement:** [`00-source-requirement.md`](00-source-requirement.md) · **Inputs:**
[`01-baseline-analysis.md`](01-baseline-analysis.md), [`02-issue-register.md`](02-issue-register.md),
[`03-decisions.md`](03-decisions.md), [`05-data-model.md`](05-data-model.md) · **Status:** ✅ Blueprint
approved (`D68`); ✅ built and verified (see [`06-review-summary.md`](06-review-summary.md))

---

## 1. Shape of the system

```text
 Browser (desktop first, responsive)                Spring Boot 4.1 application (Java 25 bytecode)
 ┌──────────────────────────────────┐   HTTPS    ┌────────────────────────────────────────────────┐
 │ Plain HTML pages + one CSS design │  session   │ Security filter chain                          │
 │ system + small ES modules         │  cookie +  │  (authentication, CSRF, RBAC, headers, throttle)│
 │ (no build step, no framework)     │  CSRF hdr  │ /api/v1/**  JSON REST, problem+json errors     │
 │                                   │ ─────────► │ /, /login, /parent/**, /learn/**, /admin/**    │
 │ Public · Parent · Learn · Admin   │            │   (pages, served only to the right role)       │
 └──────────────────────────────────┘            │ /media/**   course media, byte-range streaming  │
                                                  │ Feature modules → domain rules → repositories  │
                                                  └───────────────┬────────────────────────────────┘
                                                                  │ JDBC (cc_app, least privilege)
                                                           MySQL 8 (Docker) · Flyway migrations
```

- **One deployable application.** A modular monolith, packaged by feature (`DD-15`). It has no
  microservices, no message broker and no SPA framework: the requirement asks for lightweight and
  maintainable (§21, §26).
- **The browser is a client of the same versioned API that a mobile app would use later** (§23, `D56`).
  Pages hold no business rules.

## 2. Folder layout of `Updated Project/`

```text
Updated Project/              (the setup and access guide is the repository's root README.md)
├── setup.ps1                 first setup: checks and installs software, prepares .env, starts, opens Chrome
├── start-dev.ps1, stop-dev.ps1   daily start (MySQL + build + run + Chrome) and stop
├── docs/                     00 requirement … 05 data model, 06 review summary, 07 deployment
├── app/                      the Spring Boot application (Maven)
│   ├── pom.xml
│   └── src/
│       ├── main/java/…/clevercubs/
│       │   ├── account/      parent registration, login support, re-authentication, child mode
│       │   ├── child/        child profiles, username rules, age-group derivation
│       │   ├── content/      age groups, programs, courses, lessons, items, messages, seeding
│       │   ├── learning/     item views, lesson completion, progress, resume
│       │   ├── quiz/         quizzes, allowances, attempts, scoring
│       │   ├── reward/       badges, certificates, program completion
│       │   ├── family/       parent requests (escalation), year summary, export and delete
│       │   ├── feedback/
│       │   ├── admin/        admin APIs: users, content, reports, settings
│       │   ├── audit/
│       │   └── platform/     security config, errors, validation, settings, media
│       ├── main/resources/
│       │   ├── db/migration/ Flyway, one folder per database: mysql/ and postgresql/ (V1–V4, afterMigrate grants)
│       │   ├── content/      course JSON produced by the extraction tool
│       │   ├── static/       pages, css/, js/, img/, fonts/
│       │   └── application.yml  profiles dev, test and cloud (test settings also in test/resources)
│       └── test/java/…       unit, integration (Testcontainers MySQL or PostgreSQL), security tests
├── media/                    course media (Git LFS), organised by course; MEDIA-MAP.csv, OPTIMISED.csv
├── db/init/                  creates the two least-privilege MySQL users on the first start
├── tools/                    content extraction (baseline HTML → content JSON + media map), media optimisation
├── e2e/                      browser tests (Playwright), a development dependency only
├── docker-compose.yml        MySQL 8.4 for development
├── Dockerfile.vercel         the cloud image; vercel.json, .vercelignore and .dockerignore beside it
└── .env.example              every variable, no values (the real .env is gitignored)
```

## 3. Dependencies, each with its reason (§21: justified dependencies only)

| Dependency | Why it is needed | What it replaces |
|---|---|---|
| `spring-boot-starter-webmvc` | HTTP, JSON, static pages, byte-range media | PHP endpoints |
| `spring-boot-starter-security` | Sessions, CSRF, RBAC, bcrypt, redirect to login: the controls the baseline lacked | Hand-written, missing controls |
| `spring-boot-starter-validation` | Declarative input validation on every request | No validation (`SEC-E10`) |
| `spring-boot-starter-jdbc` | Simple aggregate persistence with parameterised SQL. Lighter than JPA, with no lazy-loading surprises | String-built SQL (`SEC-E01`, `SEC-E02`) |
| `spring-boot-starter-flyway` + `flyway-mysql` | A versioned, reviewable schema | No schema at all |
| `mysql-connector-j` | The database driver | `mysqli` |
| `postgresql` + `flyway-database-postgresql` | The hosted deployment: Vercel offers no MySQL, only PostgreSQL databases (`D73`, [`07-deployment.md`](07-deployment.md)). MySQL stays the development and default test database | — |
| `spring-boot-starter-session-jdbc` | Sessions kept in the database, so a sign-in survives a restart and works across several instances (the cloud host stops idle instances) | In-memory sessions |
| Test only: `spring-boot-starter-webmvc-test`, `spring-boot-starter-jdbc-test`, `spring-boot-starter-flyway-test`, `spring-boot-starter-security-test`, `spring-boot-starter-validation-test`, `spring-boot-testcontainers`, `testcontainers-junit-jupiter`, `testcontainers-mysql`, `testcontainers-postgresql` | Real-database integration tests on both databases, security tests, and the test support each area needs | No tests |
| Development only: Playwright (Node, in `e2e/`) | Browser flows and responsive checks (§28) | No tests |
| Development only: Pillow and ffmpeg, in a throw-away image (`tools/mediatool.Dockerfile`) | `tools/optimize_media.py`: resize heavy pictures, move MP4 indexes first (`DD-29`). Never installed, never shipped | Hand-optimised media |

**Artifact names follow `app/pom.xml`.** Spring Boot 4 renamed `spring-boot-starter-web` to
`spring-boot-starter-webmvc` and `spring-boot-starter-data-jdbc` to `spring-boot-starter-jdbc`, ships
Flyway through the `spring-boot-starter-flyway` starter instead of a direct `flyway-core` dependency, and
replaced the single `spring-boot-starter-test` / `spring-security-test` pair with one `-test` starter per
area (`spring-boot-starter-webmvc-test`, `-jdbc-test`, `-flyway-test`, `-security-test`,
`-validation-test`); the table above carries the names actually declared. The Flyway starter pulls
`flyway-core` in transitively, so the library is still on the classpath — only the declared dependency
differs. Where this table and `pom.xml` ever disagree, `pom.xml` is the source of truth — it is what builds.

**Not added:** a JS framework, a CSS framework, Lombok, an ORM (persistence is plain `JdbcClient`), a rate-limit
library (a small throttle class is enough), OpenAPI generators (the API is documented in `docs/`), and CDN
scripts (`DD-12`).

## 4. Security design (requirement §8, §20)

### 4.1 Sessions and roles

| Situation | Session authorities | Can reach |
|---|---|---|
| Not signed in | none | Public pages; `POST /api/v1/auth/*`; the public API |
| Parent signed in | `ROLE_PARENT` | `/parent/**`, `/api/v1/parent/**` (own children only) |
| Parent picked a child (`D58`) | `ROLE_CHILD` + `activeChildId`; **`ROLE_PARENT` is dropped** | `/learn/**`, `/api/v1/learn/**`, for that child only |
| Back to the parent area | Password required again; the session ID is rotated | as a parent |
| Super Admin | `ROLE_SUPER_ADMIN`; a recent password confirmation for sensitive actions | `/admin/**`, `/api/v1/admin/**` |

- **Unauthenticated page request:** a `302` to `/login?next=…`, where `next` is checked to be a local path.
- **Unauthenticated API call:** `401` with problem+json.
- **Wrong role:** `403` (§8).
- **Every entity access checks ownership in the service layer**, not only the URL. For example, a parent
  can load `child/{id}` only if it is theirs. This fixes `SEC-E04`.

### 4.2 How each existing security issue is closed

| Issue | Control in the new build |
|---|---|
| `SEC-E01`, `-E02` SQL injection | `JdbcClient` with bound parameters only. No SQL is built from input. Column names come from code, never from requests. A test sends the baseline's own payloads |
| `SEC-E03`, `-E15`, `-E22` no session; browser-only gate; cosmetic logout | Server sessions (`DD-02`): the page routes themselves are protected on the server, and logout invalidates the session |
| `SEC-E04`, `-E23` IDOR | The identity comes from the session (`activeChildId`), never from a parameter; ownership checks everywhere |
| `SEC-E05` root with empty password | Two least-privilege database users, and credentials from the environment (`05-data-model.md` §7) |
| `SEC-E06`, `-E11` error disclosure | One `@RestControllerAdvice` returns generic problem+json; details go only to the server log. `server.error.include-*` is off |
| `SEC-E07`, `-E08`, `-E09` enumeration, brute force, weak passwords | A generic login message; account lock and per-IP throttle (`DD-05`); a 12-character minimum and a common-password check (`DD-01`) |
| `SEC-E10`, `-E19` validation, unencoded bodies | Bean Validation on every DTO; JSON bodies built with `JSON.stringify` |
| `SEC-E12` CSRF | Spring Security CSRF tokens, sent in a header by the fetch wrapper (`DD-03`) |
| `SEC-E13` duplicate usernames | `UNIQUE` constraints on email and username |
| `SEC-E14` charset | `utf8mb4` everywhere |
| `SEC-E16` plain-text passwords in the browser | Nothing sensitive is kept in `localStorage`; it holds only harmless UI preferences |
| `SEC-E17` browser-decided progress | The server computes everything (`05-data-model.md` §5) |
| `SEC-E18` XSS | Output is written with `textContent` and DOM APIs, never `innerHTML` with data. A strict CSP without `'unsafe-inline'` (`DD-11`) is the second line of defence |
| `SEC-E20` headers, HTTPS | CSP, `nosniff`, `frame-ancestors 'none'`, `Referrer-Policy`; HSTS and `Secure` cookies in the production profile (`INF-05`) |
| `SEC-E21` third-party code | No runtime third-party requests: a local celebration animation and self-hosted fonts |
| `SEC-E24`, `-E25` exposed paths and the deck | The media library has relative paths only; the `.pptx` never enters `Updated Project/` or the web root |
| `SEC-E26` children's privacy | Consent records, data minimisation, parent export and delete, no tracking, legal texts flagged (`D67`) |
| New: unsafe uploads, path traversal (§20) | **No uploads at all** (`DD-06`). Media paths are validated as relative, normalised and inside the media root |

## 5. API surface (resource-oriented, `/api/v1`, JSON)

The endpoints as built (all JSON under `/api/v1`; errors are RFC 9457 problem+json with a stable `code`):

| Area | Endpoints |
|---|---|
| Public | `GET public/health` · `GET public/session` · `GET public/courses` · `GET public/contact` · `GET public/avatars` · `GET public/ages` · `GET public/username-suggestion` |
| Auth | `POST auth/register` (parent + first child + consent) · `POST auth/login` · `POST auth/logout` · `GET auth/me` · `POST auth/reauth` · `POST auth/change-password` |
| Session mode | `POST session/child {childId}` (parent) · `POST session/parent {password}` (child) |
| Child | `GET learn/me` · `GET learn/home` · `GET learn/courses/{slug}` · `GET learn/lessons/{id}` · `PUT learn/items/{id}/view` · `GET learn/quizzes/{id}` · `POST learn/quizzes/{id}/attempts` · `GET learn/attempts/{id}` · `PUT learn/attempts/{id}/answers/{questionId}` · `GET learn/profile` · `GET/POST learn/requests` |
| Parent | `GET parent/overview` · `GET/POST parent/children` · `GET/PATCH/DELETE parent/children/{id}` · `GET parent/children/{id}/year-summary` · `POST parent/children/{id}/next-year` · `GET parent/children/{id}/export` · `POST parent/children/{id}/quizzes/{quizId}/grant` · `GET parent/requests` · `POST parent/requests/{id}/approve\|decline` · `GET/POST parent/feedback` · `GET/PATCH/DELETE parent/account` |
| Admin | `GET admin/overview` · `GET admin/reports/courses` · `GET admin/accounts` · `POST admin/accounts/{id}/status` · `POST admin/accounts/{id}/temporary-password` · `GET admin/children` · `GET admin/children/{id}/progress` · `GET/PATCH admin/courses[/{id}]` · `PATCH admin/lessons/{id}` · `PATCH admin/items/{id}` · `GET/PATCH admin/quizzes/{id}` · `PATCH admin/questions/{id}` · `GET admin/programs` · `PUT admin/programs/{id}/courses` · `GET/PATCH admin/age-groups[/{id}]` · `GET/PATCH admin/badges[/{id}]` · `GET/POST/PATCH admin/messages[/{id}]` · `GET/PATCH admin/feedback[/{id}]` · `GET admin/settings` · `PUT admin/settings/{key}` · `GET admin/audit` · `GET admin/audit/actions` |

Every state-changing call needs the `X-XSRF-TOKEN` header carrying the value of the `XSRF-TOKEN` cookie.
Deleting or exporting a child, deleting an account, and admin changes to accounts, settings, programs and
age groups need the password confirmed within the last 15 minutes (`POST auth/reauth`); otherwise the answer
is `403 reauth-required`.

**Conventions:**

- Plural nouns, and the HTTP methods keep their meaning.
- Every list is paginated (`?page=&size=`, size at most 100).
- Errors use RFC 9457 problem+json with a stable `type` and no internals.
- Responses are DTOs, never tables.

## 6. Frontend

### 6.1 Pages

| Area | Pages |
|---|---|
| Public | Welcome (what CleverCubs is, for parents) · Log in · Register (parent, then first child, then consent) · Terms · Privacy · Contact |
| Parent | Dashboard (children, progress at a glance, pending requests) · Child detail (courses, lessons, quiz attempts, badges) · Add or edit child · Requests · Feedback · Year summary · Account (password, export, delete) |
| Learn | "Who is learning?" · Home (course cards, resume, encouragement) · Course (lessons, quiz state, attempts left) · Lesson (item cards: tap to hear, see or watch) · Quiz (one question at a time, friendly feedback) · Result · My profile (avatar, display name, badges, certificates) |
| Admin | Overview (counts, activity) · Accounts · Children · Courses → lessons → items · Quizzes → questions · Programs · Age groups · Badges · Messages · Feedback · Settings · Audit log |

### 6.2 Design system (§24)

- **Tokens:** CSS custom properties in one stylesheet.
- **Light theme:** a warm off-white background with explicit `background` and `color` on the root.
- **Colour:** the baseline's green (`#2f6f4e`) kept as the brand colour, with a small, controlled set of
  friendly accents (sunny yellow, sky, coral, lavender), one per course. All text meets WCAG AA contrast.
- **Type:** a rounded display face for headings and a highly legible reading face designed for early
  readers. Both are self-hosted, open-licensed and subset to keep them small.
- **Components:** buttons, cards, a progress ring and bar, badges, dialogs, forms with inline validation,
  toasts, and empty states. All are keyboard-reachable with a visible focus ring.
- **Motion:** short, purposeful transitions and one small celebration on success. All of it is disabled
  under `prefers-reduced-motion`.

### 6.3 Age-group adaptation (§5, `D66`)

The child's age group comes from the server as a `ui_profile`. The same pages then adapt, driven by data
rather than separate code paths.

| Aspect | Toddler (2–3) | Pre-school (4–5) | Early primary (6–8) |
|---|---|---|---|
| Navigation | One level: big course pictures, no text menus | Pictures and short labels | Pictures, labels and course descriptions |
| Instructions | Icons plus an optional "🔊 Read to me" (the browser's built-in speech; no service) | Short sentences, plus read-aloud | Sentences |
| Targets | Extra-large touch targets | Large | Standard (still at least 44 px) |
| Quiz | Picture-first options, sound on | Picture and text | Text-first, with the score shown as "8 of 10" |
| Feedback and rewards | Stars and a sticker, no numbers | Stars and short praise | Praise, percentage and badge details |
| Wording | `ui_message` rows for the group | same | same |

### 6.4 Responsive and accessible (§23, §24)

- Mobile first, with no fixed widths and touch-friendly controls.
- A viewport meta tag and doctype on every page.
- Semantic buttons, never clickable `div`s; `alt` on every image, from `lesson_item.alt_text`.
- Checked at 1440, 1024, 768 and 375 px.

## 7. Media (§25)

- **Copied from the baseline into `media/<course>/`,** with normalised names (lower case, hyphens, no
  spaces). The extraction tool writes a map from each old name to its new one. The baseline stays untouched.
- **Only the media the content uses is copied.** The 20 orphan files and the unused `.pptx` are left out.
- Served with byte-range support (videos start at once), long cache headers, `preload="none"` or
  `metadata`, poster frames and `loading="lazy"`.
- **The autoplaying background videos are dropped** (149 MB, `FUN-E26`). This is a change to existing
  behaviour, listed in §10 for approval.
- **Card images are resized** to at most twice their display size, and sound and video files keep their
  index before their data ("faststart"), both by `tools/optimize_media.py` (`DD-29`). It runs Pillow and
  ffmpeg from a throw-away Docker image (`tools/mediatool.Dockerfile`), so nothing is installed and the
  application gains no dependency; file names never change. `MediaWeightTests` guards both. Re-encoding the
  videos themselves changes what a child sees and hears, so it waits for the owner (§12).

## 8. Testing (requirement §28)

| Level | What | Tool |
|---|---|---|
| Domain unit | Age group, progress formula (70/30, media courses), pass mark, attempt allowance, the ≥ 80% reward rule, program completion, username rules | JUnit 5, no Spring |
| Integration | Every API against real MySQL: registration, login, lockout, child mode, ownership, attempts (including two simultaneous starts), grants, rewards, feedback visibility, admin RBAC, audit rows | Spring Boot Test + Testcontainers |
| Security | Unauthenticated access, redirect to login, 403 on the wrong role, IDOR across parents, CSRF rejection, the baseline SQL-injection payloads, stored-XSS strings shown as text, headers and CSP present, no stack traces in errors, no password or hash in any response | MockMvc + `spring-security-test` |
| End to end | The §28 flows in a real browser: register, log in, pick a child, lessons, quiz (pass, fail, lock, grant), badge, profile, parent feedback, admin | Playwright |
| Responsive and accessibility | The key pages at four widths; keyboard-only walk-through; automated a11y checks | Playwright |
| Performance | Page weight and request counts before and after (baseline figures in `01-baseline-analysis.md` §11); API timings | Playwright metrics, logs |

Nothing is reported as done without its test run. The register moves an issue from **E** to **F** only
with the test that proves the fix.

## 9. Build phases

Each phase ends with its checks passing. Progress is tracked in `BLAST/task_plan.md`.

| Phase | Delivers | Done when | Status (2026-09-27) |
|---|---|---|---|
| B0 Scaffold | Maven project, Docker MySQL, Flyway V1 schema, profiles, `.env.example`, README | `mvn verify` passes, and the application starts against MySQL | ✅ |
| B1 Accounts and security | Registration with consent, login and logout, sessions, CSRF, headers, throttle and lock, child mode and re-auth, RBAC, admin bootstrap, audit | The auth and security integration tests pass | ✅ |
| B2 Content | The extraction tool, content JSON, media library, seeder, age groups, programs, content APIs | All 11 courses load, and the content tests pass | ✅ |
| B3 Learning engine | Item views, lessons, progress, resume, quiz attempts and allowance, scoring, lock, grant, badges, certificates, program completion | The domain and integration tests for every §10, §11 and §13 rule pass | ✅ |
| B4 Parent area | Dashboard, children, requests, feedback, year summary, export and delete | Parent integration tests pass | ✅ |
| B5 Admin | Dashboard, management screens, reports, settings, audit viewer, re-auth for sensitive actions | Admin RBAC and audit tests pass | ✅ |
| B6 Frontend | The design system and every page in §6, with the age adaptation, accessibility and responsive layout | Playwright flows pass at four widths | ✅ (public pages at four widths, full journeys at 1440 and 375 px) |
| B7 Validation | The full suite, security review, a11y and performance measurements | All green; the register updated E → F | ✅ (`02-issue-register.md` §6) |
| B8 Review | The §29 Phase 6 summary: changed, preserved, fixed, remaining, questions, assumptions, recommendations | Delivered to the owner | ✅ [`06-review-summary.md`](06-review-summary.md) |

## 10. Changes to existing behaviour that need approval (root `CLAUDE.md` §Stage gate)

| Change | Reason |
|---|---|
| **The PHP backend is replaced by Java** | Directed by the requirement (§21); nothing of the PHP code is reusable safely |
| **The autoplaying background videos are removed** | 149 MB, the heaviest single cost on every page (`FUN-E26`); they conflict with §24 ("avoid … heavy visual effects") and §25. Replaced by a light illustrated background |
| **Nine obsolete pages are not carried forward**: the six `_q` prototypes, `great_job_page`, `demo_login`, `progres_page.php` | Unreachable duplicates (`01-baseline-analysis.md` §9). Their content is either in live pages or is test scaffolding |
| **The 44 pages become about 25 data-driven pages** | The content moves into data. Every topic, item, rhyme, story and question is kept |
| **The media is reorganised and renamed** in the new project's media library | Spaces and misspellings in URLs; the map from each old name to its new one is kept |
| **No baseline user, feedback or progress data is migrated** | None was uploaded, and what the deck shows is test data including plain-text passwords (`SEC-E25`) |
| **The hub-quiz questions become a reserve bank**, with one quiz per course | Ends the three-way inconsistency (`FUN-E02`, `DD-18`) |

## 11. Risks and how they are handled

| Risk | Handling |
|---|---|
| Drive D: is 99% full (5.1 GB free); the media copy needs about 420 MB | Copy only the referenced media, without the background videos; measure the free space before and after |
| The Docker engine is stopped | Start Docker Desktop before B0; the tests need it (Testcontainers) |
| `JAVA_HOME` points at a missing JDK | The scripts find a JDK 25+ themselves; a bare Maven run sets `JAVA_HOME` first (root `README.md` §10) |
| Playwright browsers download about 300 MB on C: (48 GB free) | Fine; installed under `e2e/` only |
| No `ffmpeg` on the machine | `tools/optimize_media.py` runs ffmpeg and Pillow from a throw-away Docker image (`tools/mediatool.Dockerfile`); video re-encoding stays deferred (§7) |
| The size of the build | Phased, with each phase verified before the next, so a pause at any point leaves working, tested code |

## 12. Recommendations beyond this build (§31)

- A PWA with offline lessons (the authors' own future scope).
- Localisation, including Marathi and Hindi (the authors' future scope; the UI text is already in data).
- TOTP two-factor authentication for Super Admins.
- An email provider for password reset and requests (`INF-04`).
- Spring Session JDBC once more than one server instance runs.
- Measured video re-encoding and a CDN for media.
- A privacy-policy and terms review by counsel in the chosen jurisdiction (`INF-03`).
