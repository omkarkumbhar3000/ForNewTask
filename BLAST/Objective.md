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

**`OBJ-031` — Make this workspace a clean, reusable BLAST framework, and prepare `New Task/` for the
next development project.** 🟡 **In progress — stage 1 (preparation) ✅ complete; stage 2 waits for the
owner to upload the current project and start it.**

### Stage 1 — now

1. **Analyse** the whole BLAST framework and workspace. Classify everything as: reusable framework
   capability · project-specific or obsolete · old Jira/PAM/CI/Payments analysis data · rules, skills,
   tools and structures to preserve for future projects.
2. **Keep the objective-first rule and make the structure enforce it.** Every CLI instruction is first
   analysed and written into this file, and this file then governs the work and its output. Owner's
   words: *"first analyze and update the `object.md` file present inside the BLAST folder as required.
   Then use the updated `object.md` as the governing context."* `object.md` is this file.
3. **Remove obsolete Jira/PAM/CI/Payments material** without damaging any reusable capability. Never
   delete something only because it is old; decide first whether it is framework or project data.
4. **Create `New Task/Current Project/`**: the input and baseline. The owner uploads the current project,
   source, docs, configuration, requirements, assets and colleague feedback here. Do not modify it
   unnecessarily.
5. **Create `New Task/Updated Project/`**: the output. All new development, generated files, docs,
   configuration and final deliverables for this task go here.
6. Leave the framework ready for stage 2. ⛔ **Do not implement the new application, and do not invent
   its requirements.**

### Stage 2 — only when the owner uploads the material and explicitly starts it

Analyse the current project in full: architecture, frontend, backend, APIs, data handling, structure,
dependencies, configuration, UI/UX, performance, security, maintainability, scalability, code quality,
error handling, validation, user flows, documentation, deployment readiness, limitations, technical debt,
missing functionality and opportunities. Then build the improved product:
**Updated Project = BLAST + Current Project + Requirement + Colleague Feedback + Improvements.**

| Direction | Rule |
|---|---|
| Primary goal | **User experience.** Simple, crisp, clear, lightweight, fast, responsive, modern, smooth, robust, easy to understand and maintain, future-proof. Improve beyond the stated requirement where it has a clear purpose; no complexity for its own sake |
| UI | **Light theme.** Clean layout, good spacing, clear hierarchy, simple navigation, intuitive flows, responsive, smooth transitions, subtle purposeful animation, useful loading states, clear success and error feedback, consistent components, accessible, minimal clutter. Apple-style quality as inspiration, never a copy; keep the product's own identity |
| Technology | Modern, future-proof and as lightweight as practical. Replace an existing technology only after weighing the real benefit, migration effort and compatibility, and never at the cost of working functionality |
| Change control | Safe improvements may be made directly. A major, destructive or architectural change is identified explicitly and needs the owner's permission |
| Mindset | Senior developer and architect: understand the product and requirement first, plan, implement only once started, validate, keep documentation in step, never claim unverified completion |
| Skills and tools | Reuse the relevant BLAST and installed skills. Do not force Jira, PAM or CI workflows onto this project |

### Owner decisions taken at intake

| Question | Decision |
|---|---|
| Where `New Task/` lives | **Inside this repository**: `New Task/Current Project/` and `New Task/Updated Project/`, so the objective rule, `CLAUDE.md` and the hook apply there |
| How far the cleanup goes | **Full.** Delete all PAM/Jira/CI data, reports, snapshots, the PAM API harness, the Jira census scripts, the PAM dashboards and the old docs. Keep BLAST, the generic rules, and four reusable tools: the `api-onboarding` skill kit, the markdown → Word/Excel renderer, the PDF → page-cited text extractor, and the root-path resolver. Everything deleted stays recoverable from git |
| The old history register | **Start a fresh register** at `OBJ-031`. `OBJ-001`–`OBJ-030` stay in git history, and the new index points at the commit that holds them |
| The objective hook | **Repair it**, hooks only: one `UserPromptSubmit` hook injects this file on every prompt through a wrapper script. The `permissions.deny` list in `.claude/settings.json` stays exactly as it is |

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
