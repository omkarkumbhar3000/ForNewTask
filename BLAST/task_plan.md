# Task Plan

> Status legend: `[ ]` todo · `[~]` in progress · `[x]` done
>
> **Run 1 — Dynamic API validation script generation (PAM).** Objective received 2026-07-28.
> Phase 1 analysis delivered; **Blueprint not yet approved.** HALT remains in effect.

## Phase 0 — Initialization
- [x] Memory files created (`task_plan.md`, `findings.md`, `progress.md`)
- [x] `LLM.md` initialized as Project Constitution
- [~] **HALT** — still in effect. No scripts in `tools/` until Discovery answers land and `LLM.md` §3
  carries a data schema.

## Phase 1 — B: Blueprint
- [x] Objective read; existing workspace decision doc loaded (`docs/history/archive/workbench-archive/approach/dynamic-api-generation.md`)
- [x] Research — developer repo measured, constraints logged in `findings.md` F1–F6
- [x] **Premise check — the objective's stated input source is not viable** (F1: under 8 % overlap).
      Alternative input identified and measured (F2: 87.7 % executable today)
- [x] Feasibility verdict delivered to the owner: ⚠️ **Partially feasible** — intent yes, stated method no
- [ ] **Discovery — 5 questions answered** ← *blocking*
      · North Star · Integrations · Source of Truth · Delivery Payload · Behavioral Rules
- [ ] Owner decides the input source (Q1) and pass/fail semantics (Q3)
- [ ] Data-First — Input/Output JSON schema confirmed in `LLM.md` §3 ← *blocking*
- [ ] Blueprint approved by the owner

## Phase 2 — L: Link (Connectivity)
- [ ] Disposable non-production environment nominated (Y1)
- [ ] API User provisioned covering all three Access Types (Y2)
- [ ] CI agent IP + MAC registered under Settings → API → Registered Machines (Y3)
- [ ] Transport consistency and Application List URL confirmed (Y4)
- [ ] Handshake — `getToken(...)` succeeds and one GET returns a parseable envelope

> Jira MCP is **not** part of this objective. Leave `.mcp.json.template` untouched.

## Phase 3 — A: Architect (3-layer)
- [ ] Layer 1 — SOP in `architecture/` for endpoint resolution, mutation generation, verdict rules
- [ ] Layer 2 — routing: resolve → filter → execute → compare → report
- [ ] Layer 3 — the runner. **Note:** the deliverable is Java inside
      `pam_automation_bootstrap` on branch `AI`, *not* a script in `BLAST/tools/`.
      Confirm this target with the owner before building (see Q1).
- [ ] Fix the two reuse defects first (`findings.md` F6)
- [ ] `--dry-run` proves resolution and prints every exclusion with a reason

## Phase 4 — S: Stylize
- [ ] Consolidated Excel workbook — Summary · Results · Regressions · Excluded · Coverage
- [ ] One-page HTML summary beside the workbook
- [ ] Results presented for owner feedback

## Phase 5 — T: Trigger
- [ ] Jenkins stage wired via `jenkins.properties`; suite XML committed
- [ ] ⛔ **Terminates at "committed on branch `AI`".** No push, no merge, no cloud deploy — the owner
      merges `AI` → `Dev` and copies into `pam/AutomationTesting/`. Deviation from B.L.A.S.T. Phase 5,
      required by the workspace `CLAUDE.md`.
- [ ] Maintenance Log finalized in `LLM.md`

## Done-when

One command — `mvn clean test -DsuiteFile=CICD_Suites/BuildStability.xml -Denv=<env>` — produces a single
consolidated Excel file covering positive, negative and edge cases across the declared endpoint surface,
with **zero test code authored per endpoint**, and every non-executed endpoint listed with a machine-readable
reason rather than silently skipped.

**Explicitly not claimed:** that the harness proves any endpoint is *correct*. It reports difference from a
recorded baseline. Correctness requires expectations, which are not derivable (F3).
