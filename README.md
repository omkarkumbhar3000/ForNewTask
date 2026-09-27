# CleverCubs — Setup, access and deployment guide

**Owner:** Omkar Kumbhar · **Production:** https://clevercubs.vercel.app · **Status:** ✅ live ·
**Updated:** 2026-09-27

One guide for installing, configuring, running, testing, accessing and deploying CleverCubs, a secure,
child-friendly early-learning web application for children aged 2 to 8, with a parent area and a Super
Admin dashboard.

> **Fastest start:** clone the repository, open your AI coding agent in it and say **"Read `AGENTS.md` and
> follow it."** The agent installs what it safely can, starts the application, opens it in Chrome and tells
> you what is left. Without an agent, run the setup script (§5).

---

## 1. Project information

| Information | Value / location |
|---|---|
| Project name | CleverCubs (the enhanced *Kids Learn* project) |
| Owner | Omkar Kumbhar |
| GitHub repository | https://github.com/omkarkumbhar3000/ForNewTask (public), branch `main` |
| Production URL | https://clevercubs.vercel.app |
| Local URL | http://127.0.0.1:8080 |
| Production database | PostgreSQL 18 on **Neon** (Vercel Marketplace), Singapore region (`ap-southeast-1`) |
| Local database | **MySQL 8.4** in Docker (`docker-compose.yml`) |
| Deployment platform | **Vercel**: a container built from `Dockerfile.vercel` on every push to `main` |
| Technology | Java 25 · Spring Boot 4.1 · Maven (wrapper included) · Flyway · plain HTML, CSS and JavaScript modules (no framework, no build step) |
| Application folder | `New Task/Updated Project/` (everything the application needs is in this folder) |
| Admin access | One Super Admin; the sign-in address and where its password lives are in §9. No password is in this repository |
| Test access | Self-registration at `/register` (no shared account); automated tests create and delete their own data (§9) |
| Contact email | ⏳ **Pending business input** (`INF-02`): not set on purpose, and the Contact page says so. Set `CC_CONTACT_EMAIL` when an address is chosen (§9) |

## 2. Quick start

| You have | Do this |
|---|---|
| An AI coding agent (Claude Code, Codex, Cursor, Copilot, Gemini CLI…) | Clone, then tell it: **"Read `AGENTS.md` and follow it."** |
| Windows, no agent | `git clone -c core.longpaths=true https://github.com/omkarkumbhar3000/ForNewTask.git` · `cd ForNewTask` · `powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\setup.ps1"` |
| Only a browser | Open https://clevercubs.vercel.app and create a family account |
| macOS or Linux | The scripts are for Windows; follow the manual steps in §5 |

## 3. Software requirements

Only what the project uses. **Not needed:** a Maven install (the wrapper `app/mvnw` downloads it), a local
MySQL or PostgreSQL server (Docker provides both), and any frontend build tool.

| Software | Version | Purpose | Install · verify |
|---|---|---|---|
| Windows | 10 (22H2) or 11 | The setup and start scripts are PowerShell | — |
| PowerShell | 5.1 (built in) or 7 | Runs `setup.ps1`, `start-dev.ps1`, `stop-dev.ps1` | `$PSVersionTable.PSVersion` |
| Git | 2.40+ (tested 2.55) | Clone, update, push | `winget install --id Git.Git -e` · `git --version` |
| Git LFS | 3.x (tested 3.7) | **Required**: the 305 course media files (≈420 MB) are stored with LFS | Included with Git for Windows · `git lfs version` |
| Java JDK | **25 or newer** (tested 26) | Builds and runs the application (bytecode level 25) | `winget install --id EclipseAdoptium.Temurin.25.JDK -e` · `java -version` |
| Docker Desktop | 4.x with WSL 2 (tested engine 29.6) | Local MySQL, and the throw-away test databases (Testcontainers) | `winget install --id Docker.DockerDesktop -e` (administrator, restart) · `docker info` |
| Google Chrome | Current stable (tested 154) | Opens the application; the browser tests drive it | `winget install --id Google.Chrome -e` |
| Node.js + npm | 20+ (tested 24.16 / 11.13) | **Only** for the browser tests in `e2e/` (Playwright uses the installed Chrome, no browser download) | `winget install --id OpenJS.NodeJS.LTS -e` · `node -v` |
| Vercel CLI | Latest (tested 56.3) | **Maintainers only**: environment variables, logs, deployments | `npm i -g vercel` · `vercel whoami` |
| Python | 3.11 | **Maintainers only**: re-running the one-time content extraction | Optional |

## 4. System recommendations

Measured on the development machine: the application uses about 350 MB of memory, MySQL about 500 MB,
Docker's virtual machine about 650 MB; a fresh clone is about 0.9 GB.

| Category | Minimum | Recommended | Notes |
|---|---|---|---|
| OS | Windows 10 22H2, 64-bit | Windows 11 | macOS/Linux work with the manual steps (§5) |
| RAM | 8 GB | 16 GB | Docker Desktop, MySQL, the application, a Maven build and Chrome run together |
| CPU | 2 cores | 4+ cores | The full test suite takes about 1 minute on 8 threads (warm) |
| Storage | 6 GB free | 10 GB free | Clone 0.9 GB · MySQL image 1.1 GB · PostgreSQL test image 0.4 GB · Maven cache ≈0.5 GB · JDK 0.3 GB · Docker Desktop itself |
| Internet | Broadband for the first setup (≈3 GB of downloads) | Same | Afterwards only for `git pull` and deployments. Using production needs only a browser |
| Chrome | Any current version | Latest stable | Also the browser for the automated journeys |
| Docker | Docker Desktop 4.x, WSL 2 backend | Latest | Must be **running** for local start and for the backend tests |

## 5. Setup script

`New Task/Updated Project/setup.ps1` does the whole first setup and is safe to run again: nothing that
exists is overwritten.

| Step | What it does |
|---:|---|
| 1 | Checks Git and Git LFS, and installs them with `winget` if missing |
| 2 | Uses the project next to the script, or clones the repository first (`-CloneTo <folder>`) |
| 3 | Makes sure the course media are real files, not LFS pointers (`git lfs pull`) |
| 4 | Finds a JDK 25+ (even when `JAVA_HOME` is wrong), or installs Temurin 25 |
| 5 | Checks Docker Desktop and starts it if it is installed but not running (installing it needs administrator rights and a restart, so that stays manual) |
| 6 | Finds Chrome, or installs it |
| 7 | Installs the browser-test packages (`npm ci` in `e2e/`) when Node.js 20+ is present |
| 8 | Creates `.env` from `.env.example` and fills **only empty** values with random local passwords. Values are never printed; `.env` is gitignored |
| 9 | Starts MySQL, builds, starts the application and opens it in a **new Chrome window** (via `start-dev.ps1`) |
| 10 | Prints a summary table and anything left to do by hand |

| Switch | Effect |
|---|---|
| `-CheckOnly` | Report only: install nothing, write nothing, start nothing |
| `-NoInstall` | Never install software; list what is missing |
| `-NoStart` / `-NoBrowser` | Prepare but do not start / start but do not open Chrome |
| `-AdminEmail you@example.com` | Also create a **local** Super Admin; its temporary password is written only to `.env` |
| `-CloneTo C:\work\CleverCubs` | Run the script on its own: it clones the repository into that folder first |

**Manual steps** (any OS, from `New Task/Updated Project/`): install the software in §3 → `git lfs pull` →
copy `.env.example` to `.env` and fill every value (letters and digits, 24+ characters) → `docker compose up -d`
→ `./app/mvnw -f app/pom.xml -DskipTests package` → `cd app && java -jar target/clevercubs-1.0.0-SNAPSHOT.jar --spring.profiles.active=dev`
→ open http://127.0.0.1:8080.

## 6. Running and access

Commands run in PowerShell from the repository root. `$p` is shorthand for the project folder.

```powershell
$p = "New Task\Updated Project"
```

| Scenario | Action |
|---|---|
| Open production | https://clevercubs.vercel.app |
| First setup | `powershell -ExecutionPolicy Bypass -File "$p\setup.ps1"` |
| Start locally (daily) | `powershell -ExecutionPolicy Bypass -File "$p\start-dev.ps1"`: MySQL, build, start on :8080, new Chrome window (log: `$p\.tmp\app.log`) |
| Restart after a Java change | `... start-dev.ps1 -Restart` (add `-SkipBuild` to reuse the last build) |
| Frontend change | Edit `$p\app\src\main\resources\static\…` and refresh; the `dev` profile serves pages, CSS and JS from source. There is no separate frontend server |
| Backend only | `& "$p\app\mvnw.cmd" -f "$p\app\pom.xml" spring-boot:run "-Dspring-boot.run.profiles=dev"` |
| Supporting services | `docker compose up -d` in `$p` (MySQL only) · `docker compose stop` · ⛔ `docker compose down -v` deletes all local data |
| Stop | `powershell -ExecutionPolicy Bypass -File "$p\stop-dev.ps1"` (add `-Database` to stop MySQL too) |
| Open in Chrome | `Start-Process chrome "--new-window http://127.0.0.1:8080"` (`start-dev.ps1` does it for you) |
| Health check | `Invoke-RestMethod http://127.0.0.1:8080/api/v1/public/health` → `status: UP` means Flyway ran and the database answers |
| Run tests | §10 |
| Deploy to production | Push to `main`; Vercel builds and deploys (§11) |
| Get the latest code | `git pull --ff-only` (the full Git workflow is in `AGENTS.md` §6) |

## 7. Using the application

| Role | How |
|---|---|
| **Parent** | *Create a family account*: your details, your first child (first name and date of birth) and three consents. You land in the parent area: children, progress, requests, feedback, year summary, data export and deletion |
| **Child** | In the parent area press **Start learning as …**. The child sees only courses, lessons, quizzes and badges; **Grown-ups** (top right) asks for the parent's password to return |
| **Super Admin** | Sign in at `/login`; the dashboard at `/admin/` manages accounts, children, courses, lessons, quizzes, programs, age groups, badges, wording, feedback, settings and the audit trail |

**Rules** (`docs/03-decisions.md`): age groups 2–3, 4–5, 6–8 · a course is short lessons of about five cards
· lessons make up 70% of a course and passing its quiz the last 30% · pass mark 70% · three tries, then the
quiz locks until a parent grants three more · a badge needs a best score of 80% or more · a year is complete
when every course in the child's program reaches 100%.

## 8. Environments: local and production are separate

| Environment | Depends on my PC? | Database | Access |
|---|---|---|---|
| Local development | **Yes**: runs on this PC with Docker | MySQL 8.4 in Docker (data in the `clevercubs-mysql` volume) | http://127.0.0.1:8080, this PC only |
| Production | **No**: runs on Vercel | Neon PostgreSQL (cloud, Singapore) | https://clevercubs.vercel.app, anyone |

**Verified on 2026-09-27:** with the local application and local MySQL stopped, production still answered
its health check and served the course catalogue from Neon. The Vercel project has no setting that points
at this PC. Production keeps working with the laptop switched off, for as long as Vercel, Neon and GitHub are
up. Local data and production data are never shared.

| Free-plan limit (Vercel Hobby, Neon Free, GitHub Free) | Effect |
|---|---|
| An idle instance stops after 5 minutes | The first visit after a quiet spell waits about **15 s** while the application starts |
| Neon's free database pauses when idle | The first query after a pause takes a moment longer |
| Each deployment downloads the media from Git LFS | Builds are skipped when nothing under `app/`, `media/` or the deployment files changed, to save the monthly LFS bandwidth |
| One build at a time; a request may run up to 300 s | Rarely noticeable |

## 9. Accounts and credentials

⛔ **The repository is public. No password, token or key is written in it.** This table says where each secret
lives and who can retrieve it.

| Account / secret | Username | Password / secret | Stored in | How an authorised person gets or sets it |
|---|---|---|---|---|
| **Super Admin (production)** | The owner's private email address, held in the Vercel variable `CC_ADMIN_EMAIL` | `[owner's password manager]`, chosen by the owner at the first sign-in (2026-09-27) | The owner's password manager only; the temporary password was deleted from Vercel | Owner: sign in at https://clevercubs.vercel.app/login. A second Super Admin can issue a temporary password under **Admin → Accounts**. With a single admin, recovery needs database access through Neon: ask the owner |
| **Super Admin (local)** | The address passed as `setup.ps1 -AdminEmail` | `[local .env: CC_ADMIN_INITIAL_PASSWORD]` | `New Task/Updated Project/.env` (gitignored) | Read it from your own `.env`, sign in, choose your own password when asked, then clear the value in `.env` |
| **Team trial (production)** | Each tester's own email | `[tester's own password manager]` | Nowhere shared | Register at https://clevercubs.vercel.app/register; delete the account from **Account** when done. There is deliberately no shared trial account |
| **Test data (automated)** | `e2e-…@example.test`, created per run | Generated by the test | Nowhere (deleted at the end of each run) | Automatic. The JUnit suite uses throw-away Testcontainers databases whose fixed test passwords are not real secrets |
| **Production database** | Neon owner role (`PGUSER`) · application role `cc_app` | `[Vercel: PGPASSWORD, CC_DB_APP_PASSWORD]` | Vercel → project `clevercubs` → Settings → Environment Variables (`PG*` managed by the Neon integration; `CC_DB_APP_PASSWORD` is write-only) | A Vercel team member, in the dashboard or with `vercel env ls`. Rotate `CC_DB_APP_PASSWORD` by setting a new value and redeploying |
| **Local database** | `root`, `cc_migrator`, `cc_app` | `[local .env: CC_DB_*_PASSWORD]` | `.env` (gitignored), generated by `setup.ps1` | Only on your PC. Never reuse production values locally |
| **GitHub** | Your own GitHub account | `[Git Credential Manager]` | Windows Credential Manager | Collaborators push with their own sign-in; the repository needs no token |
| **Vercel** | Members of the team "OM's projects" | `[Vercel login]` | Vercel CLI login (`vercel login`) | Invitation by the owner. `.vercel/` and `.env.local`, which `vercel link` writes, are gitignored |

**Contact email** (`CC_CONTACT_EMAIL`): ⏳ pending business input (`INF-02`, `D77`). Where it would appear:
the **Contact us** page (`/contact`, from `GET /api/v1/public/contact`). To set it: Vercel → project
`clevercubs` → Settings → Environment Variables → add `CC_CONTACT_EMAIL` for Production, then redeploy
(locally: the same key in `.env`, then restart).

## 10. Testing

| Suite | Command (from the repository root) | Needs | Takes |
|---|---|---|---|
| Backend on MySQL (**the gate**, 219 tests) | `& "$p\app\mvnw.cmd" -f "$p\app\pom.xml" verify` | Docker running | ≈1 min warm (first run downloads images) |
| The same on PostgreSQL 18 (production's version) | `& "$p\app\mvnw.cmd" -f "$p\app\pom.xml" test "-Dclevercubs.test.db=postgresql"` | Docker running | ≈1 min warm |
| One class / one test | `... test -Dtest=QuizAttemptTests` · `... test "-Dtest=QuizAttemptTests#threeAttemptsThenLocked"` | Docker | seconds |
| Browser journeys, local (6) | `cd "$p\e2e"; npx playwright test` (desktop 1440 px and phone 375 px) · one size: `--project=mobile` · last report: `npx playwright show-report` | App running, Node, Chrome | ≈20 s |
| Browser journeys, production | `$env:CLEVERCUBS_URL = "https://clevercubs.vercel.app"; npx playwright test` (assertions wait up to 30 s for a cold start) | Node, Chrome | ≈2 min |
| Page weights | `node measure.mjs` in `$p\e2e` | App running | seconds |

If `mvnw` says *JAVA_HOME is not defined correctly*, point it at your JDK 25+ first
(`$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-25…"`); `setup.ps1` prints the JDK it found. Run
both backend suites before pushing a change to SQL or a migration, because production runs on PostgreSQL.
Each browser run registers a throw-away family and deletes it at the end.

## 11. Deployment and Git workflow

| Step | What happens |
|---|---|
| 1. Update | `git pull --ff-only`; resolve conflicts by keeping both sides' valid changes, never by overwriting |
| 2. Change and test | §10; update this guide or `docs/` when setup or behaviour changes |
| 3. Check before committing | `git status`; nothing secret staged (`.env`, `.env.local`, `.vercel/`, logs, `target/`, `.tmp/` are ignored); new media files go through Git LFS |
| 4. Commit and push | `git push origin main` |
| 5. Deploy | Vercel builds `Dockerfile.vercel` from GitHub `main` (project root `New Task/Updated Project`, Git LFS on) and deploys to production. The build is skipped when nothing under `app/`, `media/` or the deployment files changed |
| 6. Verify | https://clevercubs.vercel.app/api/v1/public/health → `UP`; the browser journeys against production (§10) |
| Roll back | Vercel dashboard → Deployments → an earlier one → **Promote to Production** |

The full cloud runbook (configuration, first deployment, operations, verification record) is
[`docs/07-deployment.md`](New%20Task/Updated%20Project/docs/07-deployment.md). The step-by-step Git checklist
for AI agents is in [`AGENTS.md`](AGENTS.md) §6.

## 12. Troubleshooting

| Problem | Possible cause | Solution |
|---|---|---|
| The application does not start | Missing or old JDK, Docker not running, no `.env` | Run `setup.ps1 -CheckOnly` to see what is missing; read `$p\.tmp\app.log` |
| *JAVA_HOME is not defined correctly* | `JAVA_HOME` points at a JDK that does not exist | Set it to a JDK 25+ folder for the session (§10); the scripts find one themselves |
| Database connection fails | Docker Desktop stopped; or `.env` passwords differ from the ones the existing MySQL volume was created with | Start Docker Desktop. If `.env` was recreated: `docker compose down -v` (⛔ deletes local data), then start again |
| *Set CC_DB_ROOT_PASSWORD in .env* | No `.env`, or empty values | Run `setup.ps1` |
| Pictures or sounds missing | Media are Git LFS pointers | `git lfs install`, then `git lfs pull` (or run `setup.ps1`) |
| Clone says *checkout failed* or *Filename too long* | The clone folder is deep: its path plus the repository's longest path (110 characters) passes Windows' 260-character limit | Clone into a short folder such as `C:\dev`, or, inside the clone, `git config core.longpaths true` then `git restore --source=HEAD --staged --worktree :/` |
| Port 8080 already in use | An instance is still running (`spring-boot:run` leaves a child JVM) | `start-dev.ps1 -Restart`, or `stop-dev.ps1`; check with `Get-NetTCPConnection -LocalPort 8080` |
| Chrome does not open | Chrome not installed, or not in a standard folder | `winget install --id Google.Chrome -e`, or open http://127.0.0.1:8080 in any browser |
| Git pull conflict | Local changes overlap remote ones | Commit or stash your work, `git pull`, resolve the files keeping valid changes from both sides, run the tests, commit. Never force-push |
| Vercel deployment fails | Build error, or `.vercelignore` removing needed files | `vercel inspect <deployment-url> --logs`; keep `.vercelignore` a deny-list of unanchored patterns (`docs/07-deployment.md` §7); roll back if needed |
| Production is slow to open | Cold start after 5 idle minutes | Wait about 15 s; normal on the free plan |
| Sign-in fails | Wrong password; 5 failures lock the account for 15 minutes | Wait 15 minutes, or a Super Admin unlocks it under **Admin → Accounts**. Forgotten password: a Super Admin issues a temporary one, which must be changed at the next sign-in |
| Browser tests fail at once | The application is not running, or `CLEVERCUBS_URL` points elsewhere | Start the application, or clear the variable: `Remove-Item Env:CLEVERCUBS_URL` |

## 13. Repository and documentation map

| Path | What it is |
|---|---|
| `New Task/Updated Project/` | **The application**: `app/` (Spring Boot, Maven), `media/` (LFS), `db/init/`, `e2e/` (browser tests), `tools/` (content extraction, media optimisation), `docs/`, the scripts, Docker and Vercel files |
| `New Task/Current Project/` | The original baseline project. Kept out of git; only its migrated content is in the repository |
| `AGENTS.md` | Bootstrap for AI coding agents after a fresh clone, including the Git workflow |
| `CLAUDE.md` | Development rules for AI assistants and developers (architecture, database, tests, conventions) |
| `BLAST/` | The objective-first working framework (`BLAST/Objective.md` holds the active instruction) |
| `docs/history/` | Append-only record of objectives, owner decisions and lessons |
| `tools/` | Reusable workspace tools (markdown rendering, PDF search, an API-testing onboarding kit) |

| Need | Document (in `New Task/Updated Project/docs/`) |
|---|---|
| The original requirement, verbatim | `00-source-requirement.md` |
| What the baseline had and lacked | `01-baseline-analysis.md` |
| Every issue, with the test that proves its fix | `02-issue-register.md` |
| Owner decisions and documented defaults | `03-decisions.md` |
| Architecture, security design and the API list | `04-architecture-and-plan.md` |
| Database schema | `05-data-model.md` |
| What was delivered and what still needs the owner | `06-review-summary.md` |
| Cloud deployment runbook | `07-deployment.md` |

**How work is done here (BLAST):** every substantive instruction is first written into
`BLAST/Objective.md` and the previous one is archived to `docs/history/`. Ambiguities come back as
multiple-choice questions. The work is then analysed, planned, built and validated, and the history records
what changed. A new project to improve goes into `New Task/Current Project/`, without its own `.git` folder:
git would record a nested repository as a single pointer, not as files. The reusable framework is also kept
as its own repository, `NewProject_Framework`. The workspace's earlier Jira/PAM analysis project is
recoverable from commit `2a3298d`.
