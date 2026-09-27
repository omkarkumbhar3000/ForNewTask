# Deployment — CleverCubs on Vercel

**Objective:** `OBJ-034` (overnight run, step 6; completion run) · **Decision:** `D73` (Neon PostgreSQL, `DQ-12`) ·
**Date:** 2026-09-27 · **Status:** ✅ live at **https://clevercubs.vercel.app**, built from GitHub `main`;
verified in §9

---

## 1. What runs where

| Part | Where | Notes |
|---|---|---|
| Application | A container on Vercel (Functions, container image), region `sin1` (Singapore) | Built from `Dockerfile.vercel` on every deployment. 2 GB memory, 1 vCPU on the Hobby plan |
| Database | PostgreSQL 17 from **Neon**, added through the Vercel Marketplace, same region | Free plan. The Neon integration puts the connection settings into the project's environment |
| Lesson media (423 MB) | Inside the image, at `/app/media` | Served by the application behind sign-in, exactly as in development (`/media/**`, byte ranges, a week's private cache) |
| Sessions | In the database (Spring Session JDBC, tables from `V4`) | Vercel stops an idle instance after 5 minutes and may run several at once; a sign-in survives both |
| Source | GitHub `omkarkumbhar3000/ForNewTask`, branch `main`, project root `New Task/Updated Project` | Connected to the project (§5); every push to `main` deploys. Git LFS is switched on for the project, so the media files arrive as files |
| Address | **https://clevercubs.vercel.app** (production) | Team "OM's projects" (`om-projects11`), project `clevercubs` |

Development and the default test run keep **MySQL 8.4** (`DQ-02`, `D67`). Nothing about local work changes.

## 2. Why this shape (`D73`)

| Finding | Evidence | Consequence |
|---|---|---|
| Vercel has no MySQL | The Marketplace's databases are Neon, Supabase, Prisma Postgres, Nile, Amazon Aurora PostgreSQL and Aurora DSQL (all PostgreSQL), plus DynamoDB, Convex, Turso, MotherDuck and Redis (`vercel integration discover`, 2026-09-27) | The application now also runs on PostgreSQL. MySQL stays the reference for development and tests |
| Container images work on this Hobby team | A probe project was built and served from `Dockerfile.vercel`, then deleted | The Spring Boot application runs unchanged, with no rewrite into functions |
| A container can stream large files | The probe served an 83 MB file in full (`200`) and by byte range (`206`); the 4.5 MB body limit of ordinary functions did not apply | The media can stay inside the image and behind sign-in; no separate public file store is needed |
| Idle instances stop after 5 minutes | Vercel documentation (container images, scale-in) | In-memory sessions would sign everyone out; sessions moved to the database |
| Vercel overwrites `X-Forwarded-For` | Vercel documentation (request headers) | The client address can be taken from the proxy headers, so the per-address sign-in limit still works |
| Every Marketplace database needs its terms accepted by the account owner in a browser | `vercel integration add neon` answered `integration_terms_acceptance_required` | The owner accepts once (§5); nobody accepts legal terms on the owner's behalf |

**Alternative, if the owner prefers to stay on MySQL everywhere:** a managed MySQL outside Vercel (for
example TiDB Cloud or Aiven for MySQL) connected through `CC_DB_URL`. It needs an account with that
provider and brings a second vendor; the PostgreSQL support could then be removed again (§8).

## 3. How the application supports both databases

| Where | What |
|---|---|
| `db/migration/mysql/` | The original migrations, unchanged (they only moved folder, so existing databases validate) plus `V4` for sessions |
| `db/migration/postgresql/` | The same schema for PostgreSQL. Flyway picks the folder by database (`locations: classpath:db/migration/{vendor}`) |
| `platform/db/SqlDialect` | The only SQL written differently: insert-or-skip, insert-or-lock, and case-insensitive comparison of email addresses and usernames |
| `platform/db/Timestamps`, `Rows` | Time is written and read as UTC without a zone on both; rows returned as maps have the same value types on both |
| Email addresses and usernames | MySQL compares them without regard to case; PostgreSQL uses `CITEXT` columns and a cast parameter for the same behaviour |
| Least privilege | MySQL: `db/init/01-users.sh`. PostgreSQL: the Flyway callback creates the `cc_app` role with `CC_DB_APP_PASSWORD` and grants it exactly the MySQL rights |
| Tests | `mvnw test` runs on MySQL; `mvnw test -Dclevercubs.test.db=postgresql` runs the same suite on PostgreSQL 17 |

## 4. Configuration

Every value lives in the Vercel project's environment; nothing secret is in the repository or the image.

| Variable | Set by | Kind | Purpose |
|---|---|---|---|
| `PGHOST_UNPOOLED`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` | Neon integration | secret | The database; the owner role runs the migrations |
| `CC_DB_APP_PASSWORD` | Project setup, random | sensitive | The application's own least-privilege role (`cc_app`) |
| `CC_ADMIN_EMAIL` | Project setup | plain | The first Super Admin's sign-in address |
| `CC_ADMIN_INITIAL_PASSWORD` | Project setup, random | secret, readable by the owner | The first sign-in only; the account must change it at once. Remove it afterwards (§7) |
| `PORT` | Project setup | plain | `8080`: where Vercel sends traffic (the image runs without root) |
| `CC_CONTACT_EMAIL` | Owner, later | plain | The Contact Us address (`INF-02`) |

The image sets `SPRING_PROFILES_ACTIVE=cloud`, which reads the variables above (`application.yml`).

## 5. First deployment

What was done on 2026-09-27, in order. Anyone with the Vercel CLI signed in to the team can repeat it.

| Step | Command or action (from `New Task/Updated Project`) | Note |
|---:|---|---|
| 1 | `vercel link --yes --project clevercubs --scope om-projects11` | Creates the project. Writes `.vercel/` and `.env.local` (a `VERCEL_OIDC_TOKEN`), both gitignored |
| 2 | `vercel env add PORT production --value 8080`, the same for `CC_ADMIN_EMAIL`; `CC_DB_APP_PASSWORD` (`--sensitive`) and `CC_ADMIN_INITIAL_PASSWORD` from stdin | Passwords generated at random, piped in, never printed or written to a file (`D75`) |
| 3 | **Owner, once:** accept the Neon Marketplace terms at `https://vercel.com/om-projects11/~/integrations/accept-terms/neon?source=cli`, team "OM's projects" selected | Until then the next step answers `integration_terms_acceptance_required` |
| 4 | `vercel integration add neon --name clevercubs-db -m region=sin1 -e production -e preview` | Adds `PGHOST_UNPOOLED`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` (and others the application ignores) |
| 5 | `vercel git connect https://github.com/omkarkumbhar3000/ForNewTask.git --yes` | Builds come from GitHub, not from a laptop upload (§7) |
| 6 | `vercel api /v9/projects/clevercubs -X PATCH -F "rootDirectory=New Task/Updated Project" -F gitLFS=true` | Without the root directory Vercel would build the repository root; without LFS the media would arrive as pointer files |
| 7 | The first production deployment: `vercel api /v13/deployments -X POST` with a `gitSource` for `main`; afterwards every push to `main` deploys | Under Git Bash, prefix `vercel api` with `MSYS_NO_PATHCONV=1` |

⚠️ **The CLI changes files it was not asked to.** `vercel link` and `vercel integration add` append a broad
`.env*` rule to this folder's `.gitignore`, which would also hide `.env.example`, and `integration add neon`
installs vendor "agent skills" into `.agents/`, `.claude/skills/` and `skills-lock.json`. Those were removed
and the `.gitignore` restored; check `git status` after any such command.

Then check the production address: the welcome page, register a family, a lesson with a video, a quiz,
the parent area and the admin sign-in (`e2e/`: `$env:CLEVERCUBS_URL = "<address>"; npx playwright test`).

## 6. Checking an image locally

```powershell
docker build -f Dockerfile.vercel -t clevercubs:local .
# a throwaway PostgreSQL, then the image against it with the cloud profile
docker run -d --name cc-pg -e POSTGRES_DB=clevercubs -e POSTGRES_USER=owner -e POSTGRES_PASSWORD=<pw> -p 55432:5432 postgres:17-alpine
docker run --rm -p 8090:8080 -e PGHOST_UNPOOLED=host.docker.internal:55432 -e PGDATABASE=clevercubs `
  -e PGUSER=owner -e PGPASSWORD=<pw> -e CC_DB_APP_PASSWORD=<16+ chars> -e CC_COOKIE_SECURE=false `
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://host.docker.internal:55432/clevercubs clevercubs:local
```

`SPRING_DATASOURCE_URL` replaces the cloud URL only because the local database has no TLS;
`CC_COOKIE_SECURE=false` only because the local address is plain `http`.

## 7. Operating it

| Task | How |
|---|---|
| Deploy a change | Push to `main`; Vercel builds from GitHub. The build is skipped when nothing under `app/`, `media/` or the deployment files changed (`vercel.json` `ignoreCommand`; its `\|\| exit 1` makes any git error mean "build" rather than a failed deployment). A `vercel deploy` from a laptop uploads the 417 MB media instead and stalled on a home connection, so it is not the way to deploy |
| `.vercelignore` | Vercel applies it from the **repository root** on a GitHub build, so it is a deny-list of unanchored patterns; an allow-list beginning with `/*` removed the whole repository, `.git` included, in the first attempt |
| Roll back | Vercel dashboard → Deployments → an earlier one → Promote to Production |
| Logs | Vercel dashboard → the project → Logs (the container's output) |
| After the first admin sign-in | Delete `CC_ADMIN_INITIAL_PASSWORD` from the project; the bootstrap never runs again once a Super Admin exists (`D69`) |
| Rotate the database password | Change `CC_DB_APP_PASSWORD` and redeploy; the Flyway callback resets the role's password at start-up |

**Limits to know (Hobby and free plans):** a request may run for at most 300 s; an idle instance stops after
5 minutes, so the first visit after a quiet spell waits for the application to start; GitHub's free Git LFS
bandwidth is limited, and every build downloads the media once, which is why builds are skipped when
nothing relevant changed; Neon's free database pauses when idle and wakes on the first query.

## 8. Open items

| Item | Needed from |
|---|---|
| **First Super Admin sign-in:** reveal `CC_ADMIN_INITIAL_PASSWORD` (Vercel → project `clevercubs` → Settings → Environment Variables), sign in at `/login` with the owner's address, set a new password when asked, then delete the variable (§7) | Owner |
| The repository is **public**, and so are the media files in it; their licences are unconfirmed (`INF-11`, accepted for now by `D74`) | Owner |
| The Contact Us address: set `CC_CONTACT_EMAIL` on the project and redeploy when one should be shown (`INF-02`, `D75`) | Owner |
| A custom domain, if wanted | Owner |

The Neon terms are accepted and `D73` is decided, so both are closed.

## 9. Production verification (2026-09-27)

| Check | Result |
|---|---|
| Boot: `GET /api/v1/public/health` | ✅ `200 {"status":"UP"}`: the container started, Flyway migrated Neon, and the application answered as `cc_app` (15.7 s on a cold start) |
| Security headers on `/` | ✅ `Strict-Transport-Security: max-age=31536000; includeSubDomains`, the CSP, `nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: same-origin`; the `XSRF-TOKEN` cookie is `Secure` |
| A protected page without a session | ✅ `302` to `https://clevercubs.vercel.app/login?next=%2Fparent%2F` (the scheme and host come through the proxy headers) |
| The API without a session | ✅ `401 application/problem+json`, `code: unauthenticated` |
| Media without a session | ✅ `302` to sign-in |
| A `POST` without the CSRF token | ✅ `403` |
| Weak password at registration (API) | ✅ `400 weak-password`, field `parent.password`, identical to local |
| Browser journeys (`e2e/`, `CLEVERCUBS_URL=https://clevercubs.vercel.app`) | ✅ 6 of 6 at 1440 and 375 px (commit `72ac44c`): public pages at four widths, protected URLs, and register → child mode → lesson → ask a grown-up → parent gate → requests → progress → feedback → delete the account. The first run found `FUN-R07` (fixed) and a too-short assertion timeout for a cold-starting instance (the suite now allows 30 s when the address is remote) |
| The cloud database (read-only query as the Neon owner role) | ✅ 4 Flyway migrations (V1–V4); 11 courses, 53 lessons, 189 cards, 134 quiz questions; 1 Super Admin (the bootstrap); the `cc_app` role present; server sessions stored; 0 test accounts left behind |

How the database was queried without exposing a secret: `vercel env pull <file outside the repository>
--environment=production`, only the four `PG*` values passed to a throw-away `postgres:17-alpine` container
(`psql` with `PGSSLMODE=require`), and both files deleted straight after.
