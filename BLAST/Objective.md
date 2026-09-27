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

**`OBJ-035` — Consolidate the CleverCubs documentation and onboarding: simple, automated, minimal files.**
Goal: someone clones the repository, gives the AI/CLI bootstrap file to their agent, lets it install and
configure what can safely be automated, the application opens in Chrome, and the central guide covers
any remaining manual step.

**Ownership (owner's statement, 2026-09-27):** **Omkar Kumbhar is the project owner.** Sudesh Sawant's account
was used only for trial and testing; never name Sudesh Sawant as owner in any documentation.

| # | Requirement |
|---:|---|
| 1 | **One central `.md` guide** (setup, installation, configuration, run, test, access, deployment, usage). Inspect first; consolidate existing content instead of duplicating it. Tables wherever possible |
| 2 | **Project information table**: name, owner, GitHub URL, production URL, local URL/port, production database (Neon PostgreSQL), local database (MySQL), platform (Vercel), technology (detected), admin access and test access (explained securely), contact email (the configured one, never invented) |
| 3 | **Requirements table** (software, version, purpose, install/verify): only what the project actually needs, detected from the repository |
| 4 | **One PowerShell setup script**: check software and versions, report what is missing, install what is safe, clone or set up, install project dependencies, prepare local configuration without exposing secrets, start the application, open it in Chrome. Safe to re-run. No hard-coded secret |
| 5 | **One AI/CLI bootstrap file** (committed): inspect the repository, read the guide, detect the OS and tools, check/install software, read configuration, prepare local environment config without exposing secrets, install dependencies, start services and the application, run health checks and relevant tests, open Chrome, verify access, report manual steps, update docs if setup changes. Use project skills when useful (Git workflow skill included); never force every skill |
| 6 | **Git workflow in the bootstrap**: status, pull and reconcile, review conflicts, update docs, verify tests/build, no secrets staged, sensitive files ignored, meaningful commit, push to the right branch, verify. Never blindly overwrite remote work |
| 7 | **Access/running table**: production URL, run locally, tests, frontend, backend, supporting services, stop, open in Chrome, production deployment, Git update |
| 8 | **Credentials reference table** (Super Admin, admin username, test username/credentials, production access, team trial access): where each secret is stored and how an authorised person retrieves or configures it. ⛔ No real secret in the public repository; no fake credentials presented as real; a test account only through the app's own mechanism |
| 9 | **Contact email**: configure the one previously provided; never invent one. If intentionally unset, show it as a pending business input. Verify where it appears |
| 10 | **Production independence**, verified technically: production (Vercel + Neon) does not depend on the owner's PC; local and production are separate (table: environment, depends on my PC, database, access). Free-plan limits (cold start) |
| 11 | **System recommendations table** (OS, RAM, CPU, storage, internet, Chrome, Docker), based on the actual application |
| 12 | **Troubleshooting table** (start failure, DB connection, Chrome, port in use, pull conflict, Vercel build, login) |
| 13 | **Consolidation**: inspect every `.md`; find duplicate, outdated and conflicting content; keep the number of files minimal; preserve useful information before removing anything |
| 14 | **Final validation**: simulate a fresh clone; verify commands, the script, the bootstrap, production URL, local start, tests, Chrome launch, Git and Vercel information, no secrets in git, `.gitignore`; check all docs for stale URLs, names and owner information; record final verified values |
| 15 | **Commit and push** after verification: update docs, status, secret check, tests, commit, push to the right repository, verify the remote, clean tree |
| 16 | **Final report table** (docs, bootstrap, script, production URL, local start, tests, Chrome, credentials, contact email, push, Vercel, cleanup) plus what still needs the owner |

**Owner's answers (2026-09-27):** the central guide is the root **`README.md`**, absorbing
`Updated Project/README.md`, `New Task/README.md` and `e2e/README.md` · the AI/CLI bootstrap is a rewritten
**`AGENTS.md`** (development rules stay in `CLAUDE.md`) · the contact email stays **unset, a pending business
input** · team trial access is **self-registration**, with no shared account (`D76`–`D77`).

**Standing constraints:** the repository is public (`D74`) · secrets only in environment variables, Vercel
or a password manager, never printed · edit markdown with `Edit` · history is append-only · check large
files, LFS, secrets and generated files before every commit.

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
