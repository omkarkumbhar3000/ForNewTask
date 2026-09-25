# Layer 3 — Tools (Engines)

Deterministic scripts. Atomic, individually testable, one job each.

Rules:
- Business logic lives here, **not** in the LLM. The model produces content; these
  scripts own formatting, validation, and file I/O.
- Credentials come from `.env` — never hardcoded.
- Use `.tmp/` for intermediate files; `output/` for deliverables.
- Every tool maps to an SOP in `architecture/`.

> **Protocol 0 HALT:** nothing may be written here until Discovery is answered, the
> Data Schema is confirmed in `LLM.md` §3, and `task_plan.md` has an approved Blueprint.

_Empty — tools are built during Phase 3 (Architect)._
