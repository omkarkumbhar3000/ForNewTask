# archive — frozen, not maintained

**Frozen:** 2026-07-28 · **Reason:** requirement content consolidated into `BLAST/Objective.md`
**Status:** ⛔ **Do not update anything in here.** It is kept for reference and traceability only.

---

## Why this exists

The project moved to a single-source-of-requirement model: `BLAST/Objective.md` holds the active
requirement, `BLAST/pending-tasks-in-queue.md` holds the backlog. Maintaining a parallel set of planning
documents in `approach/` would reintroduce exactly the drift that change was meant to remove.

Nothing was deleted — the content below either moved to a live home or is retained because it is
reference data rather than a requirement.

## Where each file's content lives now

| Archived file | Live home |
|---|---|
| `approach/instruction.md` | Role, constraints and edit-scope rules → `BLAST/Objective.md`. Edit-scope rule also in the root `CLAUDE.md` |
| `approach/plan.md` | Phase sequence → the deferred blocks in `BLAST/Objective.md` and `BLAST/pending-tasks-in-queue.md` §3 |
| `approach/status.md` | Live status → `BLAST/task_plan.md` and `BLAST/progress.md`; metrics → `Reports/` |
| `approach/dynamic-api-generation.md` | Design absorbed into `BLAST/pending-tasks-in-queue.md` §3 (Phase 4) and `BLAST/findings.md`. **Its measurements were superseded** — see below |
| `approach/orphans.md` | Still the only catalogue of the 218 orphaned test classes. Cited by `docs/findings/issues/ISSUE-008-unused-scrap-code.md` |
| `approach/Graphify.md` | Tooling reference for the knowledge graph. Operational guidance is in the automation repo's `AGENTS.md` |

## ⚠️ Superseded content — do not cite these files as current

`dynamic-api-generation.md` was written before the developers shared their Swagger links. Two of its
central conclusions have been overtaken by measurement:

| It said | Now known |
|---|---|
| No Swagger/OpenAPI exists anywhere | **37 live Swagger specs exist**, covering 690 operations. Shared 2026-07-28 and verified reachable |
| `APIConfig.java` is the only viable source of truth | It is the only source for the **legacy** surface. The Swagger specs are the source for a **second, disjoint** surface that `APIConfig` does not describe |

Its still-valid contributions: the differential-verdict model, the safety/blocklist rules, and the
measurement that 1,160 of 1,322 legacy endpoints are executable with no new per-endpoint code.

**For anything current, read `Reports/` and `BLAST/`.**

## If you want this gone

Nothing here is referenced by running code. `orphans.md` is cited by ISSUE-008 and `Graphify.md` is a
useful tooling reference; the other four are historical. Deleting the folder loses traceability of how the
approach evolved but breaks nothing.
