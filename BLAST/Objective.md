# Objective.md — Active Instruction

> **This file holds one thing: what I want done right now.** Rewrite the §Instruction block below and
> save. The `UserPromptSubmit` hook (`hooks/inject-objective.ps1`) injects it on every prompt, so the
> change takes effect on the next message — no need to restate context or start a new session.
>
> **Keep it small** (the hook warns above 10,000 characters). Nothing historical belongs here.
> Decisions, prior objectives and findings live in [`../docs/history/`](../docs/history/README.md); the
> assistant reads them when needed and must **never copy them back into this file.**

**Owner:** Sudesh Sawant · **Updated:** 2026-09-27 · **Work area:** `../New Task/`

---

## Instruction

<!-- ▼▼▼ WRITE THE CURRENT REQUIREMENT HERE — replace everything between the markers ▼▼▼ -->

**`OBJ-034` — Enhance the Kids Learn / CleverCubs project into a simple, lightweight, secure,
child-friendly educational application with a Java backend.** This is stage 2 of `OBJ-031`.
Phases 1–3 ✅ · Blueprint approved (`D68`) · B0–B8 built ✅ · 🟡 **Completion run: verify, publish, deploy.**

The overnight run of 2026-09-26 (`D71`, `D72`) is done up to its first push (`3651d3b`: build, §1–§31
cross-check, baseline kept out of git). Its improvement push and the Vercel deployment remain.

### 🟡 Completion run (2026-09-27, amends `OBJ-034`) — end to end; stop only a step truly blocked

1. **Docker running**, then the full suite on **MySQL and PostgreSQL** and the E2E journeys against the
   current code. No reliance on earlier runs; fix what fails.
2. **Review every uncommitted change**; discard or overwrite nothing without checking it.
3. **Finish the code-side items** of `docs/06-review-summary.md` §8, and the deferred media fixes
   (`FUN-E29`, `FUN-E32`) unless they genuinely need a business decision.
4. **Docs and history:** record `D73`; correct the test count and the stale "publish to GitHub remaining";
   fix `Dockerfile.vercel`'s README reference; update anything else stale; re-check `CLAUDE.md`.
5. **Git:** status, diff, ignores, secrets, LFS; commit; push; the repository **public**; verify the remote.
6. **Vercel:** connect the cloud database once the owner accepts the Vercel/Neon terms; deploy to
   production; verify it and run the E2E journeys against it; fix and redeploy as needed.
7. **Final verification** (local, MySQL, PostgreSQL, GitHub, Vercel, cloud database, E2E, docs,
   security), a cross-check against the requirement, and a concise report.

**Owner decisions (2026-09-27):** the repository is public for now (`D74`) · the cloud database is the
assistant's choice, most consistent with the code and lowest in maintenance (`D73`: Neon PostgreSQL) ·
the owner accepts the Vercel/Neon terms when prompted · the production Super Admin signs in as the
owner's Gmail address; the Contact Us address stays unset for now (`INF-02` open) (`D75`).

Tokens supplied by the owner are used only from environment variables and never written to any file in the
repository or printed.

**The full requirement is authoritative and verbatim:**
[`../New Task/Updated Project/docs/00-source-requirement.md`](../New%20Task/Updated%20Project/docs/00-source-requirement.md)
(§1–§31 plus the owner's addendum). This block summarises it; where the two differ, the verbatim file wins.

### Summary

| Area | What is required (§ of the requirement) |
|---|---|
| Input and output | The baseline is `../New Task/Current Project/Kids_learn_project/`, the primary source of truth, never modified. The enhanced version goes in `../New Task/Updated Project/`. Missing artifacts are created there (addendum) |
| Goal | Child-friendly, simple, attractive, light theme, lightweight, secure, clear to parents, maintainable, mobile-ready. Purposeful animation only (§2, §24) |
| Principle | Ask before any decision that materially affects architecture, data model, security, roles, auth, parent–child relationships, course, quiz or reward logic, the database, the mobile design or existing functionality. Minor UI decisions follow industry practice and are documented (§3, §31) |
| Analysis first | The twelve points in §4. Plan before any structural change. Remove existing functionality only if it is obsolete, conflicts with the requirement, or is approved |
| Users | Several age groups, derived from the date of birth; the experience adapts to the group (§5) |
| Accounts | Parent registration plus child registration; mandatory, optional and recommended fields; data minimisation (§6). Parent → Child → Courses → Lessons → Quizzes → Progress; a secure escalation to the parent (§7) |
| Access | Authentication, sessions, expiry, logout, RBAC (Child, Parent, Super Admin). A protected URL without a session redirects to login, and authorization is enforced on the backend (§8) |
| Learning | Course cards, descriptions, progress, resume (§9). Progress is calculated on the backend and stays below 100% until the required quiz is passed (§10). At most 3 quiz attempts, enforced by the backend (§11) |
| Profile, rewards | Profile with username, display name, avatar, summaries and badges (§12). Rewards above 80%, no leaderboards (§13). Encouraging, age-appropriate tone (§14) |
| Parent and site | Parent feedback, visible to admins only (§15). A one-year completion summary for the parent, whose decision continuation remains (§16). Contact Us (§17). Terms & Conditions, flagged for legal review (§18) |
| Admin | A Super Admin dashboard with RBAC, protection for sensitive actions and an audit trail (§19) |
| Security | Mandatory: the §20 list, privacy by design, no compliance claim without verification |
| Technology | Java backend with a clean architecture and justified dependencies only (§21). A schema designed from the requirements and proposed before implementation (§22). Desktop first, responsive, APIs a mobile client could use (§23) |
| Quality | Measured performance work (§25), maintainability (§26), the five issue classes of §27, the tests listed in §28 |
| Workflow | Understand → Analyse → Plan → Build → Validate → Review (§29) |

### Points the requirement itself says to confirm, not invent

Age-group definitions (§5) · what happens after 3 failed attempts (§11) · what "above 80%" measures (§13) ·
the parent-escalation behaviour (§7) · the target jurisdiction and the legal/privacy review areas (§18,
§20) · the final registration field list (§6) · the database schema, proposed before implementation (§22).

### Standing constraints

- **Git:** before every commit, check large files and LFS, secrets, generated and temporary files (§30).
- **Protocol 0:** Discovery answered, schema in `LLM.md` §3, Blueprint approved (`D68`) — HALT lifted.
- **Skills:** use the installed skills that add real value, and report which ones helped (addendum).

### Owner decisions taken at intake (2026-09-26; detail in `docs/03-decisions.md`, history `D56`–`D67`)

| Topic | Decision |
|---|---|
| Stack | Spring Boot 4.1, and plain HTML/CSS/JS pages calling a versioned REST API |
| Database | MySQL 8 in Docker; Testcontainers for tests |
| Child sign-in | The parent signs in and picks the child; the parent area asks for the password again |
| Escalation | An in-app parent gate and request inbox; email later, by configuration |
| Lessons | A topic is a course of short lessons (about five items); one lesson per rhyme or story |
| Progress | Lessons make up 70%, passing the quiz adds 30%, calculated on the server |
| Pass mark | 70%, per quiz, editable by the admin |
| 3 attempts | Then the quiz locks, and the parent can grant 3 more (audited) |
| Rewards | A best quiz score of 80% or more |
| Year program | An admin-defined course list per age group, complete when all its courses reach 100% |
| Age groups | 2–3, 4–5 and 6–8, stored as editable data |
| Privacy | Jurisdiction undecided: the strictest common baseline; legal texts flagged for review |

<!-- ▲▲▲ WRITE THE CURRENT REQUIREMENT HERE ▲▲▲ -->

---

## How this gets executed

The assistant runs the instruction above using the whole workspace as context, without being told twice:

| Needs | Reads |
|---|---|
| Standing rules: objective-first workflow, edit scope, change control, validation, git | root `../CLAUDE.md` |
| Why something is the way it is: decisions, prior objectives | `../docs/history/README.md` |
| The protocol and its phases | `B.L.A.S.T.md`; memory in `LLM.md`, `task_plan.md`, `findings.md`, `progress.md` |
| The project being improved, its requirement and its feedback | `../New Task/Current Project/` |
| The work in progress and its documentation | `../New Task/Updated Project/` |
| Searchable PDFs, markdown → Word/Excel, API-testing onboarding | `../tools/rag/` · `../tools/render/` · `../tools/onboarding/` |

**On completion:** append what changed and what was learned to `../docs/history/` (narrative log, and a
decision record for each owner decision). When this file is rewritten, its outgoing instruction is
archived to the objective register first.
