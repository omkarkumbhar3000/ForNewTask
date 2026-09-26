# Task Plan

> Status legend: `[ ]` todo · `[~]` in progress · `[x]` done
>
> **Awaiting Blueprint.** Stage 2 of `OBJ-031` (the development project in `../New Task/`) starts
> Protocol 0 here once the owner uploads the current project and starts it. Phases 1–5 are filled in then.
> The previous run's plan (PAM, retired) is in git at `2a3298d:BLAST/task_plan.md`.

## Phase 0 — Initialization
- [x] Memory files created (`task_plan.md`, `findings.md`, `progress.md`)
- [x] `LLM.md` initialized as Project Constitution
- [ ] **HALT** — no deliverable code until Discovery + Schema are confirmed

## Phase 1 — B: Blueprint
- [ ] Discovery — 5 questions answered (North Star · Integrations · Source of Truth · Delivery Payload · Behavioral Rules)
- [ ] Data-First — Input/Output schema confirmed in `LLM.md` §3
- [ ] Research — prior art reviewed, constraints logged in `findings.md`
- [ ] Tech stack chosen and recorded, with the reason for any replacement of an existing technology

## Phase 2 — L: Link (Connectivity)
- [ ] `.env` credentials in place for the services the objective needs
- [ ] Integrations activated (e.g. Jira MCP, see `MCP-SETUP.md`) — only those the objective needs
- [ ] Handshake verified — every external service responds

## Phase 3 — A: Architect (3-layer)
- [ ] Layer 1 — SOPs written in `architecture/`
- [ ] Layer 2 — navigation / routing defined
- [ ] Layer 3 — atomic tools built and tested

## Phase 4 — S: Stylize
- [ ] Payload formatted for professional delivery
- [ ] UI/UX applied (if the project has a frontend)
- [ ] Results presented for owner feedback

## Phase 5 — T: Trigger
- [ ] Deployed to its target environment, or stopped at the boundary the objective sets
- [ ] Execution triggers configured (cron / webhook / listener), if any
- [ ] Maintenance Log finalized in `LLM.md`

## Done-when
<!-- The single acceptance test that proves the objective is met. -->
_TBD — define in Phase 1._
