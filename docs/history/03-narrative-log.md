# Narrative Log — What changed and what was learned

**Index:** [`README.md`](README.md) · **Earlier narrative:** `git show 2a3298d:docs/history/04-narrative-log.md`

⛔ Append-only. One section per objective, added to as the work proceeds.

---

## OBJ-031 — Clean, reusable BLAST framework and the `New Task/` work area

### Stage 1 — preparation

**What the workspace was.** A pared-down copy of the PAM API-automation workspace, focused on Jira ticket
analysis: 700 tracked files, about 200 MB, most of it PAM run data, Jira snapshots, census reports, a PAM
API harness that could not run here (its target repositories were absent), and three dashboards reading
PAM data. The BLAST folder inside it carried the retired PAM run's plan, findings and progress, and the
objective hook pointed at a drive this machine does not have.

**Order of work, and why.** The completed `OBJ-030` was archived to the old register first; it had never
received its full record. The owner's instruction was then written into `BLAST/Objective.md` as `OBJ-031`
before any change. Four ambiguities were asked as multiple-choice questions and folded back in (`D48`–
`D51`). A checkpoint commit, `2a3298d`, captured the complete old workspace plus the `OBJ-030` record
before anything was deleted, so every removed file stays one `git show` away.

**What was kept, and why each item is reusable.**

| Kept | Why |
|---|---|
| `BLAST/` protocol, objective, memory templates, layer skeletons | The framework itself. Memory files reset to the template, keeping only generic learnings |
| `BLAST/hooks/inject-objective.ps1` (new) | Makes the objective-first rule structural instead of remembered |
| `tools/paths.py` | Marker-based root resolution; its PAM locations replaced by BLAST and `New Task/` ones |
| `tools/render/` | Markdown → `.docx`/`.xlsx`, generic apart from three census section names, now removed |
| `tools/rag/` | PDF → page-cited text and search. Rewritten to take any PDFs and write to `.tmp/rag-corpus/`. Both scripts had used `tools/rag/corpus/`, while the corpus itself had been moved to `artifacts/rag-corpus/`, so search found nothing |
| `tools/onboarding/` | The `api-onboarding` skill kit, project-agnostic by design; references to retired files now point into `2a3298d` |
| `.claude/rules/markdown-docs.md` | House style and the editing-safety rules, with PAM paths removed |

**What was removed.** All Jira/PAM/CI data and deliverables (`artifacts/`, `state/`, `data/analysis/`,
`21-09-2026/`, the census reports, briefs, findings, gaps, hardening review, knowledge base), the PAM API
harness (`obj0NN_*`, `chain_runner`, `engage`, `token_guard` and the rest), the Jira census scripts, the
three PAM dashboards and the control centre, `CLAUDE.full-workspace.md`, two PAM-only rule files, and the
old history. One ignored file, the client workbook, was deleted after confirming an identical copy in
`omkar_internal/Jira RCA/`.

**Lessons.**
- **A hook that prints nothing looks exactly like a healthy one.** The wrapper script prints a visible
  warning when the root or the objective is missing, and it was verified by running its command and
  parsing the JSON, including the failure path.
- **`find … -prune` combined with `-delete` silently ignores the prune.** GNU find turns on `-depth`, warns
  and then deletes nothing. A cleanup step must be checked after it runs, not assumed.
- **A moved folder can leave a tool pointing at the old place.** The onboarding validator had looked in
  `tools/onboarding/profiles/` ever since an earlier restructure moved the template to `data/profiles/`.
  Moving the kit's data back beside its code fixed it.

**Stage 2** starts when the owner uploads the current project, the requirement and colleague feedback into
`New Task/Current Project/` and gives the instruction.

---

## OBJ-032 — Documentation correction, and the `NewProject_Framework` repository

**Why.** Each new project had meant rebuilding the rules, workflow, hooks, tools and habits of the last one.
The owner created a blank repository to hold that framework once, separately from any project.

**Part 1 — documentation.** This repository's own docs were already correct. The folder-level
`..\CLAUDE.md` (not versioned; backed up first) still said no git repository existed anywhere, and eight
further statements had gone stale: `ForNewTask` described as byte-identical to `omkar_internal/Jira RCA`,
the census commands listed as runnable here, the objective "never auto-injected", and the absent-directory,
artifact-size and backup-copy notes. Each was corrected in place and the Jira facts re-pointed at
`omkar_internal/Jira RCA`. One sentence of the global `~/.claude/CLAUDE.md` was corrected (`D54`).

**Part 2 — the framework.** Built in `..\NewProject_Framework`, a sibling folder, as a product rather than a
copy: a clean `template/` (the mandatory core), optional `tools/` and `skills/`, a generalised `global/`,
`scripts/new_project.py` (create, or adopt without overwriting) and `scripts/verify.py` (the gate), six
guides, a changelog and CI. Generalised on the way: the onboarding schema's 29 PAM-specific descriptions
rewritten as anonymous lessons, the rule set's placeholders resolved and its old-project sections removed,
the objective hook re-implemented in POSIX `sh` so one script serves Windows, macOS and Linux, git rights
aligned with the owner's standing preferences. New: a `pre-commit` hook that blocks credentials,
secret-shaped strings, conflict markers and oversized files, and a project self-check `BLAST/verify.py`.

**Validation.** The 15-check gate passed; five deliberately broken project states were each caught; a fresh
clone of the pushed repository passed the gate again. First commit `4bd37b0`, pushed to `main` and verified
equal to the remote.

**Lessons.**
- **A gate that passed first time still needed a negative test.** Breaking a generated project on purpose
  exposed a real defect the smoke test had missed: a project created with a *subset* of tools failed its
  own link check, because `tools/README.md` linked to tools it had not installed. The fix was plain paths,
  plus a partial-install case added to the smoke test.
- **A stored denylist of old-project names would itself be baggage.** The framework's permanent checks are
  generic (secrets, home paths, placeholders, links); the old-project scan was run once and not kept.
- **The pasted GitHub token was never needed.** The machine's existing credentials reached the new
  repository; the token was not used, stored or written anywhere, and the owner was advised to revoke it.

---

## OBJ-034 — CleverCubs rebuild, build phase B1

### The initial Super Admin bootstrap (2026-09-26)

**The gap.** `CC_ADMIN_EMAIL` and `CC_ADMIN_INITIAL_PASSWORD` were in `.env`, `application.yml` bound them
as `clevercubs.admin.bootstrap-*`, `CleverCubsProperties.Admin` even masked the password in its own
`toString` — and **no code read any of it**. A fresh deployment had the `user_account` table and no way to
put an account in it: no registration endpoint, and the admin APIs that would follow do not exist.

**What was built.** One class, `account/AdminBootstrap`: an `ApplicationRunner` with one method
(`createIfAbsent`) plus the thin `run` that feeds it the two configured values. It inserts a single
`SUPER_ADMIN` row — `status = ACTIVE`, `must_change_password = true`, `failed_logins = 0`, no lock — hashing
with the existing BCrypt `PasswordEncoder` bean. **No migration was needed**: `V1__schema.sql` already
carries every column, and the `afterMigrate.sql` grant on `user_account` already permits the insert, so the
test's real least-privilege `cc_app` user proves the grant instead of assuming it.

**The design decisions were the owner's (`D69`).** Three were asked rather than assumed, because the
instruction and the existing documentation disagreed:

| Question | The conflict | Chosen |
|---|---|---|
| What makes it skip? | The instruction keyed on the configured email; the javadoc and `.env.example` said "created only if no Super Admin exists yet" | **Both guards.** A stale `.env` line cannot quietly mint a second admin |
| Audit it? | `DD-14` audits every administrative change; the instruction said "smallest" | **One `audit_event` row** on creation, through `AuditLog` |
| A short configured password? | `DD-01` sets 12 characters, but no check exists anywhere in the code | **Warn, do not refuse.** `must_change_password` forces the change, and refusing would leave a deployment with no way in at all |

**Validation.** `mvnw verify` green: **82 tests, up from 73** — `AdminBootstrapTests` 9, and the other 73
unchanged and still passing, which is the proof that authentication, re-authentication, the temporary-password
filter, CSRF and sessions were not touched. The nine cover creation; BCrypt-only storage, with the plaintext
checked against *every* column of the created row and not just `password_hash`; `must_change_password = true`;
no overwrite on a rerun, proven against an account whose owner had since changed the password, cleared the
flag and disabled it; no second admin; blank configuration doing nothing; the runner and property-binding
wiring; and the password never reaching the log.

**Lessons.**
- **The first version of the tests failed for a reason that was in the tests, not the product, and the run
  is what proved it.** Cleanup tracked account *ids* but registered them *before* the account existed, so
  `idOf` returned `0`, a real `SUPER_ADMIN` row survived teardown, and the next test's "a Super Admin
  already exists" guard correctly refused to create anything — four tests failed looking like product bugs.
  The fix is to track *addresses* and register them inside `unusedEmail()`, so cleanup cannot be defeated by
  a test's own statement order. A shared mutable fixture in a suite whose order is not fixed is a real trap.
- **`@SpringBootTest` does invoke `ApplicationRunner` beans,** so a bootstrap wired into the test profile
  fires on every context start. It is harmless here only because `application-test.yml` leaves both values
  empty, which is now asserted directly rather than assumed.
- **`must_change_password = true` is honest, but currently terminal.** The bootstrapped admin can sign in and
  read `/api/v1/auth/me`, and `PasswordChangeRequiredFilter` refuses everything else with
  `password-change-required` — but no endpoint changes a password yet, so the account cannot get out of that
  state on its own. Left exactly as found, because the fail-closed rule is not the bootstrap's to weaken, and
  it is the clearest argument for building password change next.
- **`JdbcClient`'s key-holder overload is `update(KeyHolder, String...)`,** not the `GeneratedKeyHolder`
  function the `NamedParameterJdbcTemplate` style suggests. The compiler settled it in four seconds.

**Not done, deliberately.** No endpoint, no registration, no password reset, no email or SMS, no UI, and no
admin account management. The bootstrap makes one configured account exist; nothing else about it.

### Password change, and the bootstrap becoming usable (2026-09-26)

**The gap this closed.** `D69` made the bootstrapped Super Admin's password temporary on purpose, and left
it unable to do anything with it: `PasswordChangeRequiredFilter` holds a `must_change_password` account to
`GET /me` and the auth calls, and **no endpoint changed a password**. A fresh deployment had an
administrator who could sign in, read itself, and stop. That was reported rather than papered over, and it
is the reason this slice exists.

**What was built.** `POST /api/v1/auth/change-password` (`{currentPassword, newPassword}` → `204`), a thin
method on `AuthController`, and `account/PasswordChangeService` holding the work. The route was added to
`PasswordChangeRequiredFilter`'s allow list — the one route whose purpose is to end that state, and it
grants nothing merely by being reached.

**Two decisions were inherited rather than invented, and both are load-bearing.**

- **The current password is proved with `ReauthenticationToken`**, the token `POST /auth/reauth` already
  uses, not with a plain `UsernamePasswordAuthenticationToken`. The provider treats the former as "not a
  sign-in", so `last_login_at` and `AUTH_LOGIN_SIGNED_IN` are left alone. The reauth endpoint was not
  reused for the whole operation — that would have cleared nothing — but its *credential check* is exactly
  the right one, and reusing it brought the constant-time equalising hash, the lock and disabled checks and
  the secret-free `AUTH_LOGIN_REFUSED` audit along for free. There is now **no** path that verifies a
  password any other way.
- **The session's principal is replaced** through the `AccountPrincipal.withPasswordChanged()` and
  `SessionAuthentication.withPrincipal(...)` that already existed and had no caller. Clearing only the
  column would have left the filter reading a stale principal and refusing the very next request from an
  account that had just chosen a password. The session id is **not** reissued: a client part-way through a
  task keeps its place. `AuthController.store(...)` is shared by `login` and `change-password` precisely so
  that decision is written down once.

**Validation.** `mvnw verify` green: **109 tests**, `PasswordChangeTests` 27 of them, and all 82
pre-existing tests still passing — the proof that the filter's allow list, the reauth contract, CSRF and
role enforcement were not disturbed by opening one new route. Among the 27: a Super Admin in exactly the
state `AdminBootstrap` produces is refused at the admin area, changes its password, and reaches it; the
old password stops working and the new one starts; `last_login_at` and the sign-in count are unchanged;
role, status, `failed_logins` and `locked_until` are untouched; and neither password, nor the BCrypt hash,
nor the address appears in any log line or audit row on either path.

**Lessons.**
- **A NULL column read as `Object.class` is not `null`.** The one test that failed was asserting
  `locked_until` was still NULL after a password change. It was — and MySQL Connector/J hands back a
  placeholder `Object` instance for a NULL when that is the type you asked for, so `optional()` returned a
  present value. The expectation was right and the *read* was wrong. Three smaller failures in the same run
  were the same lesson in three costumes: `isEqualTo` against a `String` for a value the driver typed its
  own way, and two comparisons of a stored hash to a fresh `passwords.encode(...)` — **BCrypt is salted, so
  that comparison can never be equal** and must be `passwords.matches(...)`. Each looked like a product bug
  and was a test bug.
- **An empty audit `details` map is stored as `NULL`**, by `AuditLog`'s own design. A test that reads the
  column back gets a null row, which is the correct outcome and not a missing row — assert on
  `optional().orElse("")` rather than expecting JSON.
- **The honest scope of "reuse the existing validator" is worth stating.** `DD-01` asks for a 12-character
  minimum **and** a common-password check, and the 71 KB list is already in the jar. The owner's
  instruction said the *minimum* policy where none exists, so that is what shipped (`D70`) and the list is
  still wired to nothing. A gap closed honestly and reported beats a gap closed quietly.

**Not done, deliberately.** `common-passwords.txt` is still unused (`DD-01`). Other sessions are not
invalidated after a change, so a second session that was open before it keeps working — a session registry
is its own piece of work. No registration, no reset, no email, no UI. And `BCryptPasswordEncoder` runs at
its own default cost, not `DD-01`'s cost 12, which was already the case before this slice.

### B1–B8 completed under open execution permission (2026-09-26 → 27, `D71`)

**What changed.** The owner re-issued the requirement after a usage limit and an OpenCode attempt that did
not give proper results, with open execution permission. The approved stack, schema and decisions were
kept, and everything still missing was built in one pass: registration with consent, the child/parent
switch, the account lock and address throttle, the full password policy (the gaps `D70` left are closed),
the content seeder over the extracted content, the learning engine (progress, quizzes, rewards, the year),
the parent area, the admin dashboard, and the whole frontend (≈20 pages, one design system, self-hosted
fonts). Media (305 files, 423 MB) now lives in `Updated Project/media/`, so the application never reads the
baseline. Evidence: 212 JUnit tests, 6 Playwright journeys, a measured 99% cut in the heaviest page. Detail:
`Updated Project/docs/06-review-summary.md`; every baseline issue against the build: `02-issue-register.md` §6.

**What was learned.**

- **spring-security-test's `csrf()` is not local to a request.** It replaces the shared `CsrfFilter`'s token
  repository for the rest of the Spring context, so 33 existing tests that expected the real `XSRF-TOKEN`
  cookie failed only because a new test class ran first. The new tests send a real double-submit token
  instead (`Journeys.realCsrf`).
- **Java text blocks strip trailing spaces**, so `"""...WHERE """ + where` produced `WHEREr.id`.
- **Jackson 3 refuses missing primitives** in request records; optional flags must be `Boolean`.
- **MySQL REPEATABLE READ hides a just-committed row from a transaction that waited on a lock**, so two
  simultaneous quiz starts opened two attempts. The start and answer transactions now run READ COMMITTED
  with an exclusive upsert; a test starts four at once.
- **Browser tests found what unit tests could not**: the quiz page used a try just by being opened, a
  suggested username contained the child's own name, Enter in a dialog meant "Cancel", and a celebration
  widened phones by 3 px. All fixed and recorded as `FUN-R01`–`FUN-R04`.
- **A modifier class named `empty` collided with the empty-state component**, turning every 0% progress bar
  into a 64 px pill. Component modifiers are now `is-…`.

**Decisions.** `D71` (open execution permission), `D72` (publish and deploy; replaces the local-only `D55`).
Documented defaults `DD-20`–`DD-26` added for owner review.

### The completion run: both databases, lighter media, publish (2026-09-27)

**What changed.** The owner asked for the remaining work end to end, with no reliance on earlier results.
Docker was started and the whole suite was re-run on the uncommitted work: 217 of 217 on MySQL 8.4 and on
PostgreSQL 17. That uncommitted work, the PostgreSQL port (`D73`), database sessions (`DD-28`) and the
improvement pass, was reviewed file by file and kept whole. The local browser run found one failure, fixed
in the test. The two deferred media issues were closed with a new tool, `tools/optimize_media.py` (`DD-29`),
which resizes 17 heavy pictures (4.78 MB lighter) and moves the index of 110 MP4/M4A files first, without
renaming anything; `MediaWeightTests` now guards both (seen failing on a restored original, then passing),
so the suite is 219 tests. The owner confirmed the public repository (`D74`), left the cloud database to the
assistant (Neon PostgreSQL, `D73`), and chose the production admin address and an unset contact address
(`D75`).

**What was learned.**

- **`isVisible()` does not wait.** The phone journey's menu helper asked whether the menu button was visible
  right after a navigation, before `layout.js` had drawn the header (it waits for the session), so it never
  opened the menu. It passed before only by timing. The helper now waits for the header first.
- **Optimised copies of generated files must be recorded, or the generator undoes them.** `extract_content.py`
  checks every media file against its source by sha256, so an in-place optimisation would be reverted and
  reported. The optimiser writes `media/OPTIMISED.csv`, and the extractor accepts exactly those results.
- **`vercel link` writes a token file (`.env.local`) and appends a broad `.env*` rule** to the project's
  `.gitignore`, which also matched the tracked `.env.example`; the rule was narrowed to `.env.local`.
- **Git Bash rewrites container paths**: `docker run -w /work` became a Windows path until
  `MSYS_NO_PATHCONV=1` was set.

**Decisions.** `D73` (Neon PostgreSQL in the cloud, MySQL locally), `D74` (public repository),
`D75` (production admin address; contact address unset). Documented default `DD-29` (lighter media) and
owner decision `DQ-12` in `Updated Project/docs/03-decisions.md`.

### The Vercel production deployment (2026-09-27)

**What changed.** The completion-run commit `16243b6` was pushed and verified on the public repository.
The Vercel project `clevercubs` was created, with its variables set from stdin and never printed, and Neon
was attached once the owner had accepted the Marketplace terms. A laptop upload stalled on the home
connection, so the project was connected to GitHub (root `New Task/Updated Project`, Git LFS on), and every
push to `main` now deploys it. **Production is live at https://clevercubs.vercel.app.** The checks:

- health, HSTS and the security headers, redirects, 401 problem+json, media behind sign-in, and CSRF all
  pass;
- the six browser journeys pass (6 of 6);
- a read-only query on Neon found V1–V4, 11 courses, 53 lessons and 189 cards, one Super Admin, and no
  test data left behind (`Updated Project/docs/07-deployment.md` §9).

Commits: `809dd62` (build setup), `72ac44c` (`FUN-R07`).

**What was learned.**

- **On a GitHub build Vercel applies `.vercelignore` from the repository root.** The anchored allow-list
  (`/*`) removed the whole repository and `.git`, and the ignore command's `git diff` then exited 129, which
  failed the deployment. It is now a deny-list of unanchored patterns, and the ignore command ends in
  `|| exit 1`, so an error means "build".
- **The live site found a defect the local run could not** (`FUN-R07`): on a slower connection the sign-in
  and registration buttons worked before their page script had attached, so the browser submitted the form
  itself as a GET, putting the typed fields in the address. The buttons now ship disabled and the forms
  declare `method="post"`.
- **A serverless target needs test timeouts sized for a cold start.** An idle instance takes about 15 s to
  start, longer than the 5 s assertion timeout; the suite allows 30 s when the address is remote.
- **Marketplace terms cannot be accepted on the owner's behalf,** and the CLI reports them as pending until
  the owner finishes the acceptance in the browser under the right team.
- **The Vercel CLI changes files unasked:** a token file, a broad `.env*` ignore rule, and vendor agent
  skills. Each was found in `git status` and removed before a commit.

**Decisions.** None new; the owner's remaining actions are in `Updated Project/docs/06-review-summary.md` §8.
