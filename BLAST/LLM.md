# LLM.md — Project Constitution

> Single source of architectural truth. `LLM.md` is **law**; the planning files
> (`task_plan.md`, `findings.md`, `progress.md`) are **memory**.
>
> **Status (`OBJ-034`): Blueprint approved (`D68`); B0–B8 built and deployed.** Discovery is answered
> (`D56`–`D67`). The project's design lives in `../New Task/Updated Project/docs/`; this file records only
> what is law for the run and points there for detail.

---

## 1. Mission

Rebuild the CleverCubs toddler-learning site (`../New Task/Current Project/Kids_learn_project/`) as a simple,
lightweight, secure, child-friendly educational application. It has a Java (Spring Boot 4.1) backend,
parent, child and Super Admin roles, backend-calculated progress, a three-attempt quiz limit, rewards, and a
light, responsive UI that adapts to the child's age group. It keeps all of the baseline's learning content.
Requirement: `../New Task/Updated Project/docs/00-source-requirement.md`.

## 2. Integrations

| Service | Use | Endpoint / Transport | Auth | Status |
|---|---|---|---|---|
| MySQL 8 | Application database | JDBC; Docker for development, Testcontainers for tests | `cc_app` / `cc_migrator` from `.env` | ⬜ not yet started (Docker engine stopped) |
| Email / SMS | Parent notification, password reset | — | — | ⬜ none; in-app only until configured (`D59`, `INF-04`) |
| Jira, GROQ | — | — | — | Not used by `OBJ-034` |

## 3. Data Schema (Input / Output) — 🟡 proposed in full in `../New Task/Updated Project/docs/05-data-model.md`

### 3a. Input shape: extracted baseline content (one JSON file per course)
```json
{
  "slug": "alphabets", "title": "Alphabets", "kind": "TOPIC", "icon": "🔤",
  "description": "…", "ageGroups": ["TINY", "LITTLE"],
  "lessons": [
    { "title": "A to E", "items": [
      { "label": "A", "word": "Apple", "image": "alphabets/apple.png",
        "audio": "alphabets/apple-audio.mp4", "video": null, "alt": "A red apple" } ] } ],
  "quiz": { "passMarkPercent": 70, "questions": [
    { "prompt": "Which letter comes after A?", "options": ["B","C","D","E"], "answerIndex": 0 } ] },
  "reserveQuestions": [ ],
  "source": { "page": "alphabets_voice.html", "quizPage": "alphabets_quize.html" }
}
```

### 3b. Output shape (the "Payload"): what the server returns, for example `GET /api/v1/learn/home`
```json
{
  "child": { "displayName": "Mia", "avatar": "lion", "uiProfile": "PRESCHOOL" },
  "resume": { "courseSlug": "animals", "lessonId": 31, "title": "Farm friends" },
  "courses": [
    { "slug": "alphabets", "title": "Alphabets", "icon": "🔤", "progressPercent": 70,
      "lessonsDone": 6, "lessonsTotal": 6,
      "quiz": { "state": "AVAILABLE", "attemptsLeft": 2, "bestScorePercent": 60, "passed": false },
      "badgeEarned": false } ],
  "message": "Great work! Shall we try the quiz?"
}
```
Progress, attempts, scores and badges are always computed by the server; the browser never sends them.

## 4. Behavioral Rules
<!-- Derived from Objective.md → Behavioral Rules. -->
- **Do Not fabricate:** where the source is silent, emit `TBD` or raise it as an open
  question. Never invent specifics.
- **Deterministic boundary:** the LLM produces *content* (JSON); formatting, business
  logic, and file I/O are deterministic code in `tools/`.
- **Fail loudly:** missing credentials or malformed responses produce a clear error and
  a non-zero exit — never a silent empty artifact.
- **Secrets:** credentials live in `.env` only; never logged, printed, or committed.
- **`OBJ-034` business rules are law until the owner changes them:** progress is 70% lessons and 30% for
  passing the quiz; the pass mark is 70%; 3 attempts, then the parent grants 3 more; a reward needs ≥ 80%;
  a year program is complete when all its courses reach 100%; age groups are 2–3, 4–5 and 6–8 (`D60`–`D66`).
  Server-side only.
- **Issues are classified** as existing, fixed existing, new enhancement, new issue, or information
  required (requirement §27), in `../New Task/Updated Project/docs/02-issue-register.md`.

## 5. Architectural Invariants (A.N.T. 3-layer)

For an application in `../New Task/Updated Project/`, the layers map to:

- **Layer 1:** `docs/04-architecture-and-plan.md` and `05-data-model.md` (and their updates) are the SOPs.
  If a rule changes, the doc changes first.
- **Layer 2:** thin controllers that route only.
- **Layer 3:** domain classes and services, deterministic and unit-tested.

The generic invariants:
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
- **`OBJ-034`:** Discovery answered. Mission, integrations, data shapes and business rules recorded above.
  Architecture and schema proposed in `../New Task/Updated Project/docs/04-architecture-and-plan.md` and
  `05-data-model.md`.
