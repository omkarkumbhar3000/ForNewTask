# Objective.md — Active Instruction

> **This file holds one thing: what I want done right now.** Rewrite the §Instruction block below and
> save. The `UserPromptSubmit` hook (`hooks/inject-objective.ps1`) injects it on every prompt, so the
> change takes effect on the next message — no need to restate context or start a new session.
>
> **Keep it small** (the hook warns above 10,000 characters). Nothing historical belongs here.
> Decisions, prior objectives and findings live in [`../docs/history/`](../docs/history/README.md); the
> assistant reads them when needed and must **never copy them back into this file.**

**Owner:** Omkar Kumbhar · **Updated:** 2026-09-27 · **Work area:** `../New Task/`

---

## Instruction

<!-- ▼▼▼ WRITE THE CURRENT REQUIREMENT HERE — replace everything between the markers ▼▼▼ -->

**`OBJ-036` — Club-specific assignments, a second Super Admin, the contact emails, and removing the old
project.** Method: analyse → implement → test → cross-check → clean up → document → push → verify production.

| # | Requirement |
|---:|---|
| 1 | **Three distinct assignment sets**, one per club: Tiny Cubs (2–3), Little Cubs (4–5), Big Cubs (6–8). Today every club effectively gets the whole catalogue; that must end. Tiny gets only the simplest, lowest-criticality set (a few genuinely suitable extra simple activities allowed), never the full catalogue. Little and Big each get their own set, not an inherited "everything below plus more". The mapping is the assistant's decision from age suitability, difficulty, criticality, complexity, attention span, skills and appropriateness. First inspect the structure, list every assignment, show the current mapping and whether all clubs see everything, then propose, implement and verify (UI, backend, database). **A Tiny child must not reach Little or Big assignments**; Little and Big must get their intended sets. Delete no assignment: reassign it, or document it as pending if it fits no club. Tests, E2E, docs |
| 2 | **One additional Super Admin**, requested as username `admin` with a short password given in the chat (deliberately not recorded here), only if multiple Super Admins are safely supported. ⛔ The plaintext password is never committed, documented, logged or shown in screenshots; it is configured through the secure mechanism. Verify the new account signs in with Super Admin permissions and the existing admin still works. Follow the first-login password-change flow. If a security rule prevents it, do not bypass the model: explain, and implement the safest supported approach |
| 3 | **Remove the old project** (`New Task/Current Project/`) only after a complete dependency and migration audit: code, config, env vars, scripts, build, migrations, tests, E2E, media, docs, deployment, git, AI instructions, skills/rules, imports, relative paths, Vercel, GitHub, CI/CD. Preserve and move anything still needed, verify the updated project independently (tests, app, E2E, production), then delete. `New Task/` ends with only `Updated Project/`. Delete nothing on assumption |
| 4 | **Contact emails** `jagrutihivarekar@gmail.com` and `asmi.ptl14@gmail.com` via the existing `CC_CONTACT_EMAIL` mechanism: support both properly if the field holds one address. Verify the Contact page, the endpoint, the Vercel configuration and production |
| 5 | **Full regression**: club separation and no leakage; the existing and new Super Admin, a normal user, registration, access control; the main, assignment, dashboard, admin and contact pages; MySQL and PostgreSQL suites, E2E, build, production deployment, database connectivity, no broken references, no secrets |
| 6 | **Documentation**: update the central guide (clubs, distribution model, Super Admin management, contact configuration, old-project removal, any new setup step); tables; minimal files; never the plaintext password |
| 7 | **Git**: status, diff, secrets, `.gitignore`, tests, production build, docs, one complete commit, push to `main`, verify the remote, clean tree. Use the Git workflow skill where useful; no force-push |
| 8 | **Final report table** (the three clubs with counts and logic, both Super Admins, contact emails, audit, removal, tests, E2E, production, docs, push, secrets) |

**Findings and answers (2026-09-27):**
- **Clubs:** every club's program holds all 11 courses (the seeder cross-joins them), and the course, lesson,
  card and quiz endpoints never check the child's program. The mapping, disjoint with nothing deleted: Tiny =
  colours, animals, fruits, rhymes · Little = alphabets, numbers, body parts, vegetables · Big = birds,
  flowers, stories. Access is enforced by the child's program (`D78`).
- **Second admin:** sign-in is by email and the password policy refuses the requested password. Neither is weakened. The
  owner chose **`admin@clevercubs.test`**, created through a new, audited **"Add a Super Admin"** in the admin
  area that needs a password re-confirmation. A one-time temporary password is shown only to the creating
  admin, and the new admin chooses a strong password at first sign-in (`D79`).
- **Production amendment (2026-09-27):** the second admin was first created as `admin@gmail.com` (id 11). The
  flow itself worked. The owner chose to switch to the planned address: add `admin@clevercubs.test` the same
  way, then **disable** (not delete) `admin@gmail.com`, keeping its audit history. A real mail domain would
  receive this admin's mail once email is added (`INF-04`).
- **Old project:** after the audit, it goes to the **Windows Recycle Bin**, which keeps it recoverable (`D80`).

**Standing constraints:** the repository is public (`D74`) · secrets only in environment variables, Vercel
or a password manager, never printed · edit markdown with `Edit` · history is append-only · every SQL change
runs on MySQL and PostgreSQL, with a migration in both folders.

<!-- ▲▲▲ WRITE THE CURRENT REQUIREMENT HERE ▲▲▲ -->

---

## How this gets executed

The assistant runs the instruction above using the whole workspace as context, without being told twice:

| Needs | Reads |
|---|---|
| Standing rules: objective-first workflow, edit scope, change control, validation, git | root `../CLAUDE.md` |
| Why something is the way it is: decisions, prior objectives | `../docs/history/README.md` |
| The protocol and its phases | `B.L.A.S.T.md`; memory in `LLM.md`, `task_plan.md`, `findings.md`, `progress.md` |
| The project being improved, its requirement and its feedback | `../New Task/Current Project/` when a baseline is present (CleverCubs' was removed, `D80`); its requirement is `../New Task/Updated Project/docs/00-source-requirement.md` |
| The work in progress and its documentation | `../New Task/Updated Project/` |
| Searchable PDFs, markdown → Word/Excel, API-testing onboarding | `../tools/rag/` · `../tools/render/` · `../tools/onboarding/` |

**On completion:** append what changed and what was learned to `../docs/history/` (narrative log, and a
decision record for each owner decision). When this file is rewritten, its outgoing instruction is
archived to the objective register first.
