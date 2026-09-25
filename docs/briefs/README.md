# workbench — internal working material

Everything the team produces *around* the automation code, kept in one place so the workspace root
stays short. **Nothing here is versioned** — `workbench/` sits outside both git checkouts, so no file
in it can contaminate a product build.

| Subfolder | Holds | Start at |
|---|---|---|
| `scripts/` | **Every harness script**, plus `flows/` (hand-written and generated). Writes into `artifacts/runs/`, never the other way | `chain_runner.py` (the executor) |
| `onboarding/` | **The portable kit for a new project** (`OBJ-011`) — profile schema, PAM profile, readiness gate, the `api-onboarding` skill. Deliberately holds **no** project facts | `README.md`, then `../new-project-implementation.md` |
| `skills/` | `*.SKILL.md` specs defining the target test architecture. ⚠️ PAM-bound, and they target the **Java/TestNG** framework, not the dynamic harness | `playwright-advance-e2e.SKILL.md` (governing) |
| `rag/` | The ARCON PAM product guides, extracted to queryable page-cited text | `README.md` |
| `react/` | Internal React component | ⬜ empty placeholder |
| `archive/` | Superseded planning documents (the former `approach/` set) | ⛔ frozen — `README.md` explains what moved where |

Six root-level briefs sit alongside them, each for a different reader: `overview.md` (demo) ·
`developer-loopholes.md` (findings) · `document-gap.md` (documentation team) ·
`new-project-implementation.md` (onboarding a new project) · `self-understanding.md` · this file.

**Requirements and status no longer live here.** As of 2026-07-28 the active requirement is
`BLAST/Objective.md`, the history and former backlog are in `docs/history/README.md`, and status is in
`Reports/`. `approach/` was archived to stop two parallel sets of planning docs drifting apart.

## Path convention

Documents **inside** `workbench/` reference each other by short relative path — `../rag/findings.md`,
`../skills/playwright-api.SKILL.md` — because they are siblings. Documents **outside** it (the root
`README.md` and `CLAUDE.md`, the automation repo's `AGENTS.md`) use the full `workbench/...` path.

## Document layering

Everything is maintained under a **one fact, one home** rule: a fact belongs in exactly one place and the
others cross-reference it. The full layer table is in the root `CLAUDE.md`. Within `workbench/`, only one
layer remains:

| Layer | File | Holds |
|---|---|---|
| Evidence — documentary | `rag/findings.md` | What the product guides say, cited `<doc>:p<N>` |

Measured evidence lives in `Reports/`; requirements in `BLAST/`. House style is in the root `CLAUDE.md`.
