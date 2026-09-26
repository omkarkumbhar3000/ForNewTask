# LLM.md — Project Constitution

> Single source of architectural truth. `LLM.md` is **law**; the planning files
> (`task_plan.md`, `findings.md`, `progress.md`) are **memory**.
>
> **Status: AWAITING BLUEPRINT.** This file is populated during BLAST Phase 1.
> Per Protocol 0, no scripts may be written in `tools/` until §3 below is filled in
> and `task_plan.md` carries an approved Blueprint.

---

## 1. Mission
<!-- One paragraph. Derived from Objective.md → North Star. -->
_TBD — define in Phase 1._

## 2. Integrations
<!-- One row per external service. -->

| Service | Use | Endpoint / Transport | Auth | Status |
|---|---|---|---|---|
| Jira | _TBD_ | MCP (see `MCP-SETUP.md`) | OAuth or API token | ⬜ standby |
| GROQ | _TBD_ | `POST https://api.groq.com/openai/v1/chat/completions` | `Bearer GROQ_KEY` | ⬜ no key in this copy; link verified in the framework trial |

## 3. Data Schema (Input / Output) — ⬜ NOT CONFIRMED
<!-- The Data-First Rule. Coding begins only once these shapes are confirmed. -->

### 3a. Input shape
```json
{}
```

### 3b. Output shape (the "Payload")
```json
{}
```

## 4. Behavioral Rules
<!-- Derived from Objective.md → Behavioral Rules. -->
- **Do Not fabricate:** where the source is silent, emit `TBD` or raise it as an open
  question. Never invent specifics.
- **Deterministic boundary:** the LLM produces *content* (JSON); formatting, business
  logic, and file I/O are deterministic code in `tools/`.
- **Fail loudly:** missing credentials or malformed responses produce a clear error and
  a non-zero exit — never a silent empty artifact.
- **Secrets:** credentials live in `.env` only; never logged, printed, or committed.

## 5. Architectural Invariants (A.N.T. 3-layer)
- **Layer 1 — Architecture (`architecture/`):** Markdown SOPs. If logic changes, the SOP
  is updated before the code.
- **Layer 2 — Navigation:** routes data between SOPs and Tools. No business logic,
  no direct API calls.
- **Layer 3 — Tools (`tools/`):** atomic, deterministic, individually testable scripts.
- `.tmp/` for intermediates; `output/` for deliverables.

## 6. Maintenance Log
- Framework validated end-to-end by a trial run (all 5 phases, self-anneal loop, and
  all failure paths). Environment facts and the Windows `process.exit()` rule are
  carried forward in `findings.md`.
- Awaiting `Objective.md` and Phase 1 Discovery for the real requirement.
- **On record (`OBJ-031`):** `Objective.md` reaches context through one live path, the
  `UserPromptSubmit` hook `hooks/inject-objective.ps1` (no `@`-import). Durable history lives in
  `../docs/history/` (append-only). Development deliverables for the current task land in
  `../New Task/Updated Project/`, not in `tools/`.
