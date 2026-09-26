# Objective.md — Active Instruction

> **This file holds one thing: what I want done right now.** Rewrite the §Instruction block below and
> save. The `UserPromptSubmit` hook (`hooks/inject-objective.ps1`) injects it on every prompt, so the
> change takes effect on the next message — no need to restate context or start a new session.
>
> **Keep it small** (the hook warns above 10,000 characters). Nothing historical belongs here.
> Decisions, prior objectives and findings live in [`../docs/history/`](../docs/history/README.md); the
> assistant reads them when needed and must **never copy them back into this file.**

**Owner:** Sudesh Sawant · **Updated:** 2026-09-26 · **Work area:** `../New Task/`

---

## Instruction

<!-- ▼▼▼ WRITE THE CURRENT REQUIREMENT HERE — replace everything between the markers ▼▼▼ -->

**`OBJ-032` — Correct the repository documentation, then extract the reusable framework into the new
`NewProject_Framework` repository.** ✅ **Complete** — framework first commit `4bd37b0`, pushed and verified.
⛔ **Not** the application: stage 2 of `OBJ-031`
(build the updated project in `../New Task/Updated Project/`) stays pending in this repository.

### Part 1 — documentation correction (this repository and its folder)

`ForNewTask` **is** a git repository. Correct the statement "this folder has no git repository" wherever it
appears in relevant `.md` files, documentation or configuration, and correct anything else the repository
restructure made inaccurate. No unrelated changes.

### Part 2 — `NewProject_Framework`: do the setup once, reuse it for every future project

Target: `https://github.com/omkarkumbhar3000/NewProject_Framework.git`, a blank repository; this is its
**first commit**. It holds **only** the generic, reusable framework. The current application keeps using
`ForNewTask`.

1. **Migrate what is genuinely reusable**, generalised where needed: BLAST and the `Objective.md`
   objective-first mechanism; `CLAUDE.md`/`AGENTS.md` templates; generic, safe-editing, documentation and
   git rules; git hooks and the objective auto-load hook with its wrapper script; development, testing,
   validation, error-handling and verification practices; coding and code-quality conventions; reusable
   skills; generic tools (project-root detection, document conversion, PDF processing, API-testing
   onboarding); templates and onboarding docs. Include anything from recent work that took real effort to
   build.
2. **Exclude project baggage**: Jira/PAM/CI/Payments data, client data, snapshots, reports, dashboards,
   spreadsheets, project test scripts, requirements, the current application, temporary or generated files,
   credentials or private data, machine-specific paths and environment assumptions.
3. **Make it a product, not a copy**: portable hooks, repository-independent scripts, configurable paths,
   documented prerequisites and setup, how to start a new project, mandatory versus optional components,
   how `Objective.md` is initialised, how git/GitHub fits, how skills are selected, how the framework is
   updated over time. Future projects start with a **clean objective and history**
   (framework capability ≠ project history).
4. **Review as a senior architect**: maintainability, portability, security, developer experience,
   automation, git practice, CI readiness, cross-machine use, documentation, testing, onboarding.
   Simple + clean + lightweight + robust + maintainable + reusable; no complexity for its own sake.
5. **Validate before pushing**: completeness, stale paths, project-specific references, hooks, scripts,
   docs, markdown links, configuration, secrets, Jira/PAM/CI baggage, reuse as a real starting point, and
   the final file list.
6. **Git**: check status, branch and remote; commit only reviewed framework content; push; synchronise and
   verify local against remote. ⛔ No force-push without explicit approval.
7. **Report** which skills are available and which were actually useful.

### Owner decisions taken at intake

| Question | Decision |
|---|---|
| How a future project is created | **Template + bootstrap.** The framework repository holds a clean `template/` plus `scripts/new_project.py`, which copies only project files, fills placeholders, adds the chosen optional tools and skills, initialises git with safety hooks, and can adopt the framework into an existing project without overwriting anything |
| User-level setup | **Include it, generalised**: `global/CLAUDE.md` (the CLI operating rules and skill policy, as a template to install on a new machine) and the `go-go-go` git-sync skill. No names, machine paths or dates; owner preferences become marked settings |
| The global `~/.claude/CLAUDE.md` | **One targeted edit**: the sentence "No objective-file hook works on this machine" becomes accurate (the hook works where a repository wires it). Nothing else in that file changes |
| The GitHub token pasted in the instruction | **Not used and not stored.** The machine's existing git credentials reach the new repository. The owner should revoke the token |

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
