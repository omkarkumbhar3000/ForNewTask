# Origin and Standing Constraints (§1–§2)

**Part of** [`../objective_original_origin.md`](../objective_original_origin.md) — the project's permanent, append-only archive. The founding instruction and when each standing constraint was established.

⛔ Append-only. Never delete, reword or reorder an entry. Section numbers (`§N`) are the stable citation scheme and do not change when files are reorganised.

---

## 1. Origin — the founding instruction

The project began as a **framework optimization** brief, not an API project. Preserved verbatim at
`workbench/archive/approach/instruction.md` (frozen). Its substance:

**Role assigned:** Senior SDET, 15+ years, Playwright + Java, framework architecture.

**The ten original instructions**, abbreviated:

| # | Instruction | Fate |
|---:|---|---|
| 1 | Apply the predefined `SKILL.md` structure to the automation code — the code conforms, not the skill | Standing |
| 2 | Audit `pam_automation_bootstrap` module-wise: replicate good generic patterns, remove dead code, enhance in place | Partly done; dead-code items became ISSUE-008 |
| 3 | Fix architectural violations — no base-page methods called directly from test files | Open |
| 4 | Assertions at **test level only** | Open |
| 5 | Use Playwright's built-in auto-waiting, not custom waits | Open |
| 6 | API testing validates status codes only — extend to **dynamic response-content validation**, Excel-driven, classified Positive / Negative / Other | ✅ **Became the whole project.** Grew into 7-layer validation |
| 7 | No test should skip without an explainable reason | Open |
| 8 | **Reference-only rule:** `pam/` may be read, never modified | ✅ **Still in force** — `BLAST/Objective.md` §Constraints |
| 9 | Maintain planning docs in `workbench/approach/` | Superseded — folder frozen to `workbench/archive/approach/` on 2026-07-28 |
| 10 | Ask clarifying questions rather than assuming | ✅ Still in force — `BLAST/Objective.md` §Output (MCQ form) |

**Why this matters:** instruction 6 is the seed of everything since. The observation that *"API validation
today = status code only"* turned out to be far more serious than a coverage gap — the product answers
HTTP 200 for rejected requests, so status-only validation was not merely thin, it was **reporting false
passes**. Every measurement after 2026-07-28 elaborates that one point.

---

## 2. Standing constraints, and when each was established

| Rule | Established | Source |
|---|---|---|
| `pam/` is reference-only; all edits in `pam_automation_bootstrap` on `AI` | Day 1 | Original instruction §8 |
| Never push, never merge — a run ends committed on `AI` | Day 1 | Original instruction §Context |
| Java 21 + Playwright + TestNG for repo deliverables | Day 1 | Original instruction §Parameters |
| Requirements live in one file; backlog separate | 2026-07-28 | Decision D4 |
| Never assert on status code alone | 2026-07-28 | Measured — the envelope trap |
| Deny-by-default on HTTP; `--execute` required | 2026-07-28 | Post-outage safety model |
| Endpoint blocklist enforced at planning time | 2026-07-28 | ISSUE-010 |
| One token per run, never retried, never looped | 2026-07-28 | ISSUE-009 — account lockout |
| Harness scripts live only in `workbench/scripts/` | 2026-07-29 | Standardization |
| Run output is retained, never auto-deleted | 2026-07-29 | Retention change |
| Generated evidence is never hand-edited | 2026-07-31 | LH pack contract |

---
