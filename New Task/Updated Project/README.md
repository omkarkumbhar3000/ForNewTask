# CleverCubs — the enhanced Kids Learn application

**What it is:** a secure, child-friendly early-learning web application for children aged 2 to 8, with a
parent area and a Super Admin dashboard · **Backend:** Java 25 / Spring Boot 4.1 · **Database:** MySQL 8.4
(Docker) for development; PostgreSQL in the cloud ([`docs/07-deployment.md`](docs/07-deployment.md)) ·
**Frontend:** plain HTML, CSS and JavaScript modules (no framework, no build step) ·
**Status:** usable build for team validation (see [`docs/06-review-summary.md`](docs/06-review-summary.md))

Everything the application needs lives in this folder. It does **not** read the original project in
`Current Project/`; that folder was used once, by `tools/extract_content.py`, to migrate the content.

---

## 1. Start it

**Once:** Docker Desktop running, a JDK 25 or newer installed, and `.env` filled in.

```powershell
Copy-Item ".env.example" ".env"      # then fill in every value in .env (never commit it)
```

`.env` holds the three database passwords and the first Super Admin's email and temporary password. The
admin is created on the first start and must choose a new password at the first sign-in.

**Every time** (from the repository root or anywhere):

```powershell
powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\start-dev.ps1"             # db + build + start + browser
powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\start-dev.ps1" -Restart    # replace a running instance
powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\stop-dev.ps1"              # stop (add -Database to stop MySQL)
```

The script finds a JDK even when `JAVA_HOME` is wrong, starts MySQL with `docker compose`, builds the jar,
starts the app on **http://127.0.0.1:8080** with the `dev` profile and opens Chrome. The log is in
`.tmp/app.log`. In the `dev` profile, pages, styles and scripts are served straight from
`app/src/main/resources/static/`, so a frontend edit shows on the next refresh; Java changes need a
restart.

Manual equivalent:

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-26.0.2"
docker compose up -d                                           # in New Task\Updated Project
.\app\mvnw.cmd -f app\pom.xml -DskipTests package
cd app; java -jar target\clevercubs-1.0.0-SNAPSHOT.jar --spring.profiles.active=dev
```

## 2. Try it

| Who | How |
|---|---|
| **Parent** | *Create a family account* on the start page: your details, your first child (first name and date of birth), and the three consents. You land in the parent area |
| **Child** | In the parent area press **Start learning as …**. The session becomes the child's: courses, lessons, quizzes and badges only. **Grown-ups** (top right) asks for the parent's password to return |
| **Super Admin** | Sign in with the address from `.env`, choose a new password, and the dashboard opens at `/admin/` |

Things worth trying: finish a lesson (the course moves by 70% ÷ lessons), open the quiz after the last
lesson, fail it three times (it locks; the child can **Ask a grown-up**), approve the request in the parent
area, pass with 80% or more (a badge), finish every course (the year is complete: certificate, year summary
and the next-year decision).

## 3. Test it

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-26.0.2"
.\app\mvnw.cmd -f app\pom.xml verify                                       # the whole suite (Docker must run)
.\app\mvnw.cmd -f app\pom.xml test "-Dclevercubs.test.db=postgresql"       # the same suite on PostgreSQL 17
.\app\mvnw.cmd -f app\pom.xml test -Dtest=QuizAttemptTests                 # one class
.\app\mvnw.cmd -f app\pom.xml test "-Dtest=QuizAttemptTests#threeAttemptsThenLocked"   # one test
```

The integration tests start their own MySQL 8.4 (or PostgreSQL 17) through Testcontainers (the development
database is not touched). Run both before pushing a change to SQL or to a migration: the cloud copy runs on
PostgreSQL. Browser flows: `e2e/` (see its README).

## 4. Where things are

```text
Updated Project/
├── app/                         Spring Boot application (one Maven module)
│   ├── src/main/java/org/clevercubs/
│   │   ├── account/             sign-in, registration, password change, child/parent switch, admin bootstrap
│   │   ├── child/               child profiles, age groups, username rules, avatars
│   │   ├── content/             content seeder, public catalogue
│   │   ├── learning/            home, courses, lessons, progress rules, age-appropriate messages
│   │   ├── quiz/                attempts, scoring, the three-try limit
│   │   ├── reward/              badges, certificates, year completion
│   │   ├── family/              parent area, requests from children, year summary, export and delete
│   │   ├── feedback/            parent feedback
│   │   ├── admin/               Super Admin API
│   │   ├── audit/               append-only audit trail
│   │   └── platform/            security, errors, settings, configuration, web routing, db (SqlDialect)
│   ├── src/main/resources/
│   │   ├── db/migration/        Flyway, one folder per database: mysql/ and postgresql/ (V1–V4, afterMigrate grants)
│   │   ├── content/             11 course files (JSON) made by tools/extract_content.py
│   │   └── static/              pages (public, parent/, learn/, admin/), css/, js/, img/, fonts/
│   └── src/test/java/           unit, integration (Testcontainers) and security tests
├── media/                       course pictures, sounds and videos (417 MB, 305 files) + MEDIA-MAP.csv, OPTIMISED.csv
├── db/init/01-users.sh          creates the two least-privilege database users
├── docs/                        00 requirement … 06 review summary, 07 deployment
├── tools/extract_content.py     one-time content migration from the original project
├── tools/optimize_media.py      lighter pictures and fast-start sound/video, same file names (mediatool.Dockerfile)
├── e2e/                         browser tests (Playwright, development only)
├── docker-compose.yml           MySQL for development
├── Dockerfile.vercel            the cloud image; .dockerignore, .vercelignore and vercel.json beside it
└── start-dev.ps1 / stop-dev.ps1
```

## 5. API (all JSON under `/api/v1`, errors as RFC 9457 problem+json with a stable `code`)

| Area | Endpoints |
|---|---|
| Public | `GET public/health` · `GET public/session` · `GET public/courses` · `GET public/contact` · `GET public/avatars` · `GET public/ages` · `GET public/username-suggestion` |
| Auth | `POST auth/register` · `POST auth/login` · `POST auth/logout` · `GET auth/me` · `POST auth/reauth` · `POST auth/change-password` |
| Session mode | `POST session/child {childId}` (parent) · `POST session/parent {password}` (child) |
| Child | `GET learn/me` · `GET learn/home` · `GET learn/courses/{slug}` · `GET learn/lessons/{id}` · `PUT learn/items/{id}/view` · `GET learn/quizzes/{id}` · `POST learn/quizzes/{id}/attempts` · `GET learn/attempts/{id}` · `PUT learn/attempts/{id}/answers/{questionId}` · `GET learn/profile` · `GET/POST learn/requests` |
| Parent | `GET parent/overview` · `GET/POST parent/children` · `GET/PATCH/DELETE parent/children/{id}` · `GET parent/children/{id}/year-summary` · `POST parent/children/{id}/next-year` · `GET parent/children/{id}/export` · `POST parent/children/{id}/quizzes/{quizId}/grant` · `GET parent/requests` · `POST parent/requests/{id}/approve\|decline` · `GET/POST parent/feedback` · `GET/PATCH/DELETE parent/account` |
| Admin | `GET admin/overview` · `GET admin/reports/courses` · `GET admin/accounts` · `POST admin/accounts/{id}/status` · `POST admin/accounts/{id}/temporary-password` · `GET admin/children` · `GET admin/children/{id}/progress` · `GET/PATCH admin/courses[/{id}]` · `PATCH admin/lessons/{id}` · `PATCH admin/items/{id}` · `GET/PATCH admin/quizzes/{id}` · `PATCH admin/questions/{id}` · `GET admin/programs` · `PUT admin/programs/{id}/courses` · `GET/PATCH admin/age-groups[/{id}]` · `GET/PATCH admin/badges[/{id}]` · `GET/POST/PATCH admin/messages[/{id}]` · `GET/PATCH admin/feedback[/{id}]` · `GET admin/settings` · `PUT admin/settings/{key}` · `GET admin/audit` · `GET admin/audit/actions` |

Every state-changing call needs the `X-XSRF-TOKEN` header with the value of the `XSRF-TOKEN` cookie.
Deleting or exporting a child, deleting an account, and admin changes to accounts, settings, programs and
age groups need the password confirmed within the last 15 minutes (`POST auth/reauth`); otherwise the
answer is `403 reauth-required`.

## 6. Rules the owner decided (docs/03-decisions.md)

Age groups 2–3, 4–5, 6–8 (editable) · a course is short lessons of about five cards · lessons are 70% of a
course and passing its quiz the last 30% · pass mark 70% · three tries, then the quiz locks until a parent
grants three more · a badge needs a best quiz score of 80% or more · a year is complete when every course
in the child's program is at 100% · the parent signs in and picks the child; the child has no password.

## 7. Before any commit

The project is in git (`D72`). `media/` (423 MB of video, audio and pictures) goes through Git LFS, by the
rules in `media/.gitattributes`; a new media file needs `git lfs install` once on the machine. `.env`,
`app/target/`, `.tmp/` and `e2e/node_modules/` are ignored by `.gitignore`. Run both test suites (§3) and
check the staged files for secrets before committing.

## 8. The cloud copy

**Live at https://clevercubs.vercel.app** — a container on Vercel with PostgreSQL from Neon (`D73`). Every
push to `main` deploys it. How it is built, configured, deployed and checked is in
[`docs/07-deployment.md`](docs/07-deployment.md); the browser journeys run against it with
`$env:CLEVERCUBS_URL = "https://clevercubs.vercel.app"; npx playwright test` (from `e2e/`).
