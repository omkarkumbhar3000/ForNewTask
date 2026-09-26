# Task Plan

> Status legend: `[ ]` todo · `[~]` in progress · `[x]` done
>
> **Run: `OBJ-034`, the enhanced Kids Learn / CleverCubs application** (stage 2 of `OBJ-031`).
> The Blueprint is `../New Task/Updated Project/docs/04-architecture-and-plan.md` (§9 build phases) and
> `05-data-model.md`. ✅ **Blueprint approved (`D68`, 2026-09-26).** The previous run's plan (PAM,
> retired) is in git at `2a3298d:BLAST/task_plan.md`.

## Phase 0 — Initialization
- [x] Memory files created (`task_plan.md`, `findings.md`, `progress.md`)
- [x] `LLM.md` initialized as Project Constitution
- [x] **HALT** lifted: Discovery answered, schema recorded, Blueprint approved

## Phase 1 — B: Blueprint
- [x] Requirement stored verbatim (`docs/00-source-requirement.md`)
- [x] Baseline understood and analysed (`docs/01-baseline-analysis.md`; two inventory passes, spot-verified)
- [x] Existing issues registered: 26 security, 32 functional, 10 information (`docs/02-issue-register.md`)
- [x] Discovery: 5 questions answered through the 12 intake decisions (`D56`–`D67`, `docs/03-decisions.md`)
- [x] Data-First: input and output shapes in `LLM.md` §3; full schema proposed (`docs/05-data-model.md`)
- [x] Tech stack chosen with reasons (Spring Boot 4.1, MySQL 8, plain JS; `docs/04` §3)
- [x] **Owner approves the Blueprint, including the changes to existing behaviour (`docs/04` §10)** (`D68`)

## Phase 2 — L: Link (Connectivity) = build phase B0
- [x] Docker Desktop started; MySQL 8 running from `docker-compose.yml`
- [x] `.env` created locally from `.env.example` (never committed)
- [x] Handshake: the application starts, Flyway applies V1–V3, and a health check answers

## Phase 3 — A: Architect (3-layer) = build phases B1–B5
- [x] B1 Accounts and security: registration and consent, login, logout, sessions, CSRF, headers, throttle and lock, child mode, re-auth, RBAC, admin bootstrap, audit
- [x] B2 Content: extraction tool, content JSON, media library, seeder, age groups, programs, content APIs
- [x] B3 Learning engine: item views, lessons, progress 70/30, resume, attempts and allowance, scoring, lock, grant, badges ≥ 80%, certificates, program completion
- [x] B4 Parent area APIs: children, requests, feedback, year summary, export and delete
- [x] B5 Admin APIs: management, reports, settings, audit viewer, re-auth for sensitive actions

## Phase 4 — S: Stylize = build phase B6
- [x] Design system (tokens, type, components, motion with reduced-motion)
- [x] Every page in `docs/04` §6, with age-group adaptation
- [x] Responsive at 1440 / 1024 / 768 / 375 px; keyboard and a11y checks

## Phase 5 — T: Trigger = build phases B7–B8
- [x] B7 Validation: unit, integration, security, Playwright E2E, performance; register moved E → F with evidence
- [x] B8 Review summary (requirement §29 Phase 6) delivered (`docs/06-review-summary.md`)
- [ ] Publish (`D72`): commit and push with media through LFS; improvement and performance passes
- [ ] Deploy to Vercel and test the production URL (`docs/07-deployment.md`)

## Done-when

Every §28 test area passes against real MySQL and in a real browser at four widths. Every `SEC-E` issue is
either moved to **F** with the test that proves it, or explicitly carried as remaining with its reason.
The owner has the review summary.
