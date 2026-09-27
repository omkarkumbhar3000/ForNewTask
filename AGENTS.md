# AGENTS.md — Fresh-clone bootstrap for AI coding agents

**How to use:** after cloning, open your AI agent in the repository and say **"Read `AGENTS.md` and follow
it."** · **Repository:** https://github.com/omkarkumbhar3000/ForNewTask (public, branch `main`) · **Owner:**
Omkar Kumbhar · **Guide for people:** [`README.md`](README.md) · **Development rules:** [`CLAUDE.md`](CLAUDE.md)

You are setting up **CleverCubs** (Java 25 / Spring Boot 4.1, MySQL in Docker locally, Neon PostgreSQL on
Vercel in production) so that it runs on this machine and opens in Chrome, with as little help from the person
as possible. Work through §2 in order. Report at the end with §5.

---

## 1. Ground rules

| Rule | Detail |
|---|---|
| ⛔ Secrets never leave their store | The repository is public. Never print, log, commit or paste a password, token or key. Local secrets live only in `New Task/Updated Project/.env` (gitignored): write them there, never show their values |
| Never invent values | No made-up emails, credentials or URLs. A missing value is reported as a manual step |
| Ask before anything destructive or outward-facing | `docker compose down -v` (deletes local data), deleting files or accounts, force-push, `git reset --hard`, `git clean`, and any change to Vercel, Neon or production |
| Leave these alone | `docs/history/` entries (append-only), `BLAST/` except `BLAST/Objective.md`. `New Task/Current Project/` would hold a future project's untouched baseline; CleverCubs' baseline was removed after its migration audit (`D80`) |
| Use the project's scripts first | `setup.ps1`, `start-dev.ps1`, `stop-dev.ps1` in `New Task/Updated Project/` already solve the known traps |
| Skills are optional | Use an installed skill only when it helps, for example a Git workflow skill such as `go-go-go` for §6, or a browser skill to look at the page. Never run skills just because they exist |
| Verify before claiming | Say *done* only after the check in the table's last column has passed |

## 2. Bootstrap steps

`$p` means `New Task\Updated Project` (quote it: the path has spaces).

| # | Step | How | Done when |
|---:|---|---|---|
| 1 | Inspect the repository | `git status -sb` · `git remote -v` (origin must be `omkarkumbhar3000/ForNewTask`) · `git log --oneline -5` · list the root. If `git status` lists every file as deleted, the checkout failed on Windows' 260-character path limit: `git config core.longpaths true; git restore --source=HEAD --staged --worktree :/` | You know the branch, the remote and whether the tree is clean |
| 2 | Read the documentation | `README.md` in full, then `CLAUDE.md` §"The application being built" | You can name the local URL, the ports and the three scripts |
| 3 | Detect the OS and tools | Windows: `powershell -ExecutionPolicy Bypass -File "$p\setup.ps1" -CheckOnly`. Other OS: check `git`, `git lfs`, `java -version` (25+), `docker info`, `node -v` (20+), Chrome | You have a table of what is present, missing or not running |
| 4 | Install missing software where safe | Windows: `setup.ps1` installs Git, Git LFS, Temurin JDK 25, Chrome and Node LTS with `winget`. **Docker Desktop needs administrator rights and a restart: report it, do not force it.** Other OS: use the platform's package manager only if the person agrees | Re-running step 3 shows no missing required item |
| 5 | Inspect the project | `$p\app` (Maven module, `mvnw` inside), `$p\media` (Git LFS), `$p\e2e` (browser tests), `$p\docs` (`04` = architecture) | — |
| 6 | Read the configuration | `$p\.env.example`, `$p\docker-compose.yml`, `$p\app\src\main\resources\application.yml` (profiles `dev`, `test`, `cloud`) | You know which variables exist; nothing is copied from production |
| 7 | Prepare local configuration | `setup.ps1` creates `.env` and fills **only empty** values with random passwords. Never overwrite an existing value: the MySQL volume keeps the passwords it was created with. Optional local admin: `-AdminEmail <address>` | `.env` exists and is ignored (`git check-ignore -v "$p/.env"`) |
| 8 | Install project dependencies | Media: `git lfs pull` (`setup.ps1` does it). Maven: comes with the first build. Browser tests: `npm ci` in `$p\e2e` | `$p\media\alphabets\apple.png` is a real picture (tens of KB, not a 130-byte pointer) |
| 9 | Start supporting services | Docker Desktop running; MySQL via `docker compose up -d` in `$p` (the start script does it) | `docker ps` shows `clevercubs-mysql` healthy |
| 10 | Start the application | `setup.ps1` without switches (it calls `start-dev.ps1`). ⚠️ From an agent's tool call, **do not pipe or redirect** `start-dev.ps1`'s output: the started JVM inherits the handle and the call never returns. Start it in its own window instead: `Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',"$p\start-dev.ps1"`, then poll step 11. Check port 8080 first (`Get-NetTCPConnection -LocalPort 8080`) | Port 8080 answers |
| 11 | Health checks | `Invoke-RestMethod http://127.0.0.1:8080/api/v1/public/health` → `status: UP` (Flyway ran and the database answers). `http://127.0.0.1:8080/parent/` without a session → `302` to `/login?next=…` | Both answers as stated |
| 12 | Run the relevant tests | Backend gate: `& "$p\app\mvnw.cmd" -f "$p\app\pom.xml" verify` (228 tests, Docker needed). ⚠️ `verify` rebuilds the jar that `start-dev.ps1` runs, and Windows locks it: run it **before** step 10, or stop the app first (`stop-dev.ps1`). If `mvnw` rejects `JAVA_HOME`, set it to the JDK that `setup.ps1` reported. Browser journeys (app running): `cd "$p\e2e"; npx playwright test` | `Tests run: 219, Failures: 0` and `6 passed` |
| 13 | Open the application in Chrome | `start-dev.ps1` opens a **new Chrome window** itself; otherwise `Start-Process chrome "--new-window http://127.0.0.1:8080"`. With browser tools, open a dedicated tab | The CleverCubs welcome page is showing |
| 14 | Verify access | Create a family at `/register` (a throw-away `…@example.test` address), open a lesson, then delete the account on the Account page. Or rely on step 12's journeys, which do exactly this | The journey works end to end |
| 15 | Report | The table in §5 plus every manual step left | The person knows what is done and what is theirs to do |
| 16 | Keep the docs true | If a step differed from `README.md` (a new requirement, a changed command, a new trap), fix `README.md`, or `CLAUDE.md` for development rules, and commit through §6 | The next person meets no surprise |

## 3. Not on Windows

The scripts are PowerShell for Windows. On macOS or Linux, follow `README.md` §5 "Manual steps": install
Git, Git LFS, a JDK 25+, Docker and Chrome → `git lfs pull` → create `.env` from `.env.example` (generate each
password with `openssl rand -base64 24 | tr -dc A-Za-z0-9`) → `docker compose up -d` →
`./app/mvnw -f app/pom.xml -DskipTests package` → `java -jar app/target/clevercubs-1.0.0-SNAPSHOT.jar --spring.profiles.active=dev`
(run from `app/`, because the `dev` profile reads `../.env` and `../media`).

## 4. Production is read-only for a bootstrap

Production is https://clevercubs.vercel.app (Vercel + Neon). It does not depend on any developer's machine.
A bootstrap only **checks** it (`/api/v1/public/health` → `UP`, which can take about 15 s on a cold start).
Never change Vercel or Neon settings, and never pull production secrets onto the machine unless the owner asks.
If you do, keep them outside the repository and delete them afterwards. Deployments happen by pushing to
`main` (§6); the runbook is `New Task/Updated Project/docs/07-deployment.md`.

## 5. Report template

| Item | Status | Details |
|---|---|---|
| Required software | ✅/❌ | versions found; what was installed |
| Local configuration | ✅/❌ | `.env` created or already complete (no values shown) |
| Media | ✅/❌ | real files / pointers |
| Application | ✅/❌ | health `UP` at http://127.0.0.1:8080 |
| Backend tests | ✅/❌ | `Tests run: N, Failures: F` |
| Browser journeys | ✅/❌ | `N passed` |
| Chrome | ✅/❌ | opened / not found |
| Production | ✅/❌ | health `UP` at https://clevercubs.vercel.app |
| Manual steps left | — | e.g. install Docker Desktop and restart |

## 6. Git workflow

Follow this for every pull and push. A Git skill such as `go-go-go`, when installed, performs the same steps.

| # | Step | Command / rule |
|---:|---|---|
| 1 | Inspect | `git status -sb` · `git fetch origin` · `git rev-list --left-right --count "@{u}...HEAD"` (behind / ahead) |
| 2 | Pull and reconcile | `git pull --ff-only`. If the branches diverged: read `git log --oneline HEAD..@{u}`, then integrate (`git pull --rebase`), keeping the valid changes from **both** sides. Never blindly take "ours" or "theirs"; remove every conflict marker; ask the person when the right behaviour is unclear |
| 3 | Update the docs | Setup or access changed → `README.md`; development rules → `CLAUDE.md`; behaviour or design → `New Task/Updated Project/docs/`; history is append-only |
| 4 | Verify | The tests from §2 step 12 that the change touches. SQL or migration changed → both backend suites (MySQL and `-Dclevercubs.test.db=postgresql`) |
| 5 | Nothing secret or generated staged | `git diff --cached --name-only` · `git diff --cached -U0 \| Select-String -Pattern 'password\|secret\|token\|api[_-]?key\|PRIVATE KEY'` must show only field names, not values. Ignored on purpose: `.env`, `.env.local`, `.vercel/`, `app/target/`, `.tmp/`, `e2e/node_modules/`, `e2e/test-results/`, `*.log`, `mar.md` |
| 6 | Media | A new picture, sound or video in `media/` must match an LFS rule in `media/.gitattributes` **before** it is staged (the largest file is 83 MB; GitHub refuses 100 MB) |
| 7 | Commit | One meaningful message per logical change (not "update") |
| 8 | Push | `git push origin main` (if LFS stalls, run `git lfs push origin main` first). ⛔ Never force-push |
| 9 | Verify the push | `git rev-parse HEAD` equals `git ls-remote origin refs/heads/main`. A push to `main` deploys production: check its health (§4) |

In a Claude Code session, `.claude/settings.json` refuses `git merge` and `git remote set-url`. That rule is
working as intended: integrate with `git pull --rebase`, or ask the owner.

## 7. Working on the code afterwards

- **Development rules** (architecture, security, SQL that must run on MySQL *and* PostgreSQL, tests,
  conventions, code-level traps) are in `CLAUDE.md`. Every agent should read it before changing code.
- **The active instruction** is `BLAST/Objective.md`. Claude Code gets it injected on every prompt; **every
  other agent must read it at the start of each session.** A substantive instruction is written there first:
  archive the outgoing one to `docs/history/`, ask ambiguities as multiple-choice questions, then work, and
  append what changed to `docs/history/`.
- Design and state live in `New Task/Updated Project/docs/` (map: `README.md` §13).

## 8. Windows traps

| Trap | Handling |
|---|---|
| PowerShell 5.1 | No `&&` (use `; if ($?) { … }`); always quote paths: `New Task`, `Updated Project` and `VS Code` contain spaces |
| Git Bash | Rewrites `/paths` passed to `docker` or `vercel api`: prefix with `MSYS_NO_PATHCONV=1` |
| Captured output in PowerShell 5.1 | Redirecting a native tool's output inside a session (`*> log`) turns its stderr progress lines into error records; with `$ErrorActionPreference = 'Stop'` they end a script. The project scripts use `Continue` and check exit codes; do the same in your own commands |
| A broken `JAVA_HOME` | The scripts find a JDK 25+ themselves; for `mvnw`, set `$env:JAVA_HOME` in the same command |
| Markdown | Edit `.md` files with an editor or an edit tool, never with `Set-Content` (PowerShell 5.1 re-encodes UTF-8 and breaks the dashes and quotes) |
| Vercel CLI | `vercel link` / `integration add` write a token file (`.env.local`), append a broad `.env*` rule to `.gitignore` and may add vendor "agent skills" folders. Check `git status` afterwards and keep none of it |
