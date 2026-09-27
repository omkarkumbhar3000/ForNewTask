# Deployment — CleverCubs on Vercel

**Objective:** `OBJ-034` (overnight run, step 6; completion run) · **Decision:** `D73` (Neon PostgreSQL, `DQ-12`) ·
**Date:** 2026-09-27 · **Status:** 🟡 prepared and verified locally; the first cloud deployment waits for
**one owner action** (§5)

---

## 1. What runs where

| Part | Where | Notes |
|---|---|---|
| Application | A container on Vercel (Functions, container image), region `sin1` (Singapore) | Built from `Dockerfile.vercel` on every deployment. 2 GB memory, 1 vCPU on the Hobby plan |
| Database | PostgreSQL 17 from **Neon**, added through the Vercel Marketplace, same region | Free plan. The Neon integration puts the connection settings into the project's environment |
| Lesson media (423 MB) | Inside the image, at `/app/media` | Served by the application behind sign-in, exactly as in development (`/media/**`, byte ranges, a week's private cache) |
| Sessions | In the database (Spring Session JDBC, tables from `V4`) | Vercel stops an idle instance after 5 minutes and may run several at once; a sign-in survives both |
| Source | GitHub `omkarkumbhar3000/ForNewTask`, project root `New Task/Updated Project` | Git LFS is switched on for the project, so the media files arrive as files |

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

**Owner, once:** sign in to Vercel and accept the Neon Marketplace terms at
`https://vercel.com/om-projects11/~/integrations/accept-terms/neon?source=cli`.

**Then (the assistant, or anyone with the Vercel CLI signed in to the team):**

```powershell
# from "New Task/Updated Project", linked to the project (vercel link --project clevercubs)
vercel integration add neon --name clevercubs-db -m region=sin1 -e production -e preview
vercel deploy --prod
```

Then check the production address: the welcome page, register a family, a lesson with a video, a quiz,
the parent area and the admin sign-in (`e2e/`: `CLEVERCUBS_URL=<address> npx playwright test`).

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
| Deploy a change | Push to `main`. The build is skipped when nothing under `app/`, `media/` or the deployment files changed (`vercel.json` `ignoreCommand`) |
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
| Accept the Neon terms (§5) | Owner |
| Confirm `D73` (PostgreSQL in the cloud, MySQL locally), or choose a managed MySQL instead (§2) | Owner |
| The repository is **public**, and so are the media files in it; their licences are unconfirmed (`INF-11`) | Owner |
| A custom domain, if wanted | Owner |
