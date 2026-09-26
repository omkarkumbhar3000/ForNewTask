---
name: api-onboarding
description: "Stand up dynamic API test generation on a new project — discovery, profile authoring, probing, first chain, generation, execution and reporting. Use when the user says 'onboard <project>', 'set this up for IDEV', 'replicate the PAM approach', 'new project implementation', or asks how to apply the dynamic API framework to another product. Project-agnostic: every project fact comes from a profile, never from this file."
---

# /api-onboarding

Stand up the dynamic API validation approach on a project that does not have it yet.

**The deliverable is not tests. It is a validated profile plus a first executed run**, from which
tests generate themselves. Every project-specific fact lives in
`tools/onboarding/profiles/<key>.json`; this skill contains no project facts at all, which is
what makes it reusable.

The narrative version of everything here — with the measured evidence, the two architecture
options and the management case — was `docs/briefs/new-project-implementation.md`, retired with the
reference project and recoverable with `git show 2a3298d:docs/briefs/new-project-implementation.md`.
Read this file to *do* the work; read that one to *understand or present* it.

## Usage

```
/api-onboarding IDEV              # full onboarding, stops at each gate for answers
/api-onboarding IDEV --discover   # phase 0 only: produce the questionnaire, write nothing else
/api-onboarding IDEV --profile    # author or update the profile, then validate it
/api-onboarding --validate        # readiness gate on every existing profile, zero HTTP calls
```

---

## ⛔ Rule 0 — the four things this skill may never do

| Never | Why |
|---|---|
| **Target production** | This solution issues writes. `environment.is_production: true` is a refusal, not a warning. |
| **Retry a failed credential call** | Retry and account lockout are incompatible. One attempt, then latch and stop. On the reference project repeated calls locked a service account that was also the data-warehouse ETL identity. |
| **Call an endpoint before the blocklist exists** | The guard is enforced at *planning* time, before a request is built. On the reference project three sequential calls to one endpoint took the whole API to `503` with no recovery. |
| **Write an assertion on HTTP status alone** | Until proven otherwise, assume a rejected request returns `200`. It did on the reference project: 1,022 of 5,416 cases returned `200` while genuinely failing. |

These hold even when the user asks for speed. Say so plainly and continue with the safe path.

---

## The seven phases

Each phase has an exit criterion. **Do not start a phase until the previous one's criterion is
met** — the ordering is not stylistic, it is what prevents building assertions on guesses.

| # | Phase | Exit criterion | Reference |
|---:|---|---|---|
| 0 | **Discover** | Every question in `references/01-discovery.md` is answered or recorded as an `UNKNOWN` with an owner | `01-discovery.md` |
| 1 | **Profile** | `validate_profile.py` reports the remaining blockers, and they are the *expected* ones | `02-profile-authoring.md` |
| 2 | **Probe** | You can name every response shape the API uses, and whether status is authoritative | `03-probe-protocol.md` |
| 3 | **One chain by hand** | A real value passes from one call into the next and is verified downstream | `03-probe-protocol.md` §4 |
| 4 | **Generate** | Generated flows load and dry-run cleanly, with zero HTTP calls | `04-generation.md` |
| 5 | **Execute** | A full run completes, survives an outage, and skips nothing silently | `05-safety-and-operations.md` |
| 6 | **Report** | A reviewer can verify any single claim from retained evidence | `06-reporting-and-benchmark.md` |

### Phase 0 — Discover

Produce the questionnaire from `references/01-discovery.md`, send it, and **wait**. Do not fill a
gap with a plausible answer; an invented fact is worse than a blank one because it is built upon
confidently. Record each gap in the profile's `unknowns[]` with the artifact or person that
settles it.

Five inputs decide whether this project can be onboarded at all:

| Input | Missing ⇒ |
|---|---|
| Machine-readable endpoint catalogue | ⛔ Hard blocker — nothing to generate from |
| Working auth mechanism | ⛔ Hard blocker |
| Safe, disposable environment | ⛔ Hard blocker |
| Request payload bodies | 🟡 Degrades to read-only coverage |
| Context prelude — how the ids everything needs are discovered | 🟡 Flows become environment-bound |

**The prelude is the one people miss.** Ask early: *to create the simplest thing in this product,
which ids must I already hold, and which call produces them?*

### Phase 1 — Profile

Copy `profiles/_template.json` to `profiles/<key>.json` and fill it in the order the template's
`_comment` gives. Then:

```
python tools/onboarding/validate_profile.py profiles/<key>.json
```

Blockers are unanswered questions, not lint. The worked example is the retired PAM profile
(`git show 2a3298d:data/profiles/pam.json`) — read it beside the template when a field's intent is
unclear. Field-by-field guidance:
`references/02-profile-authoring.md`.

### Phase 2 — Probe

⚠️ **Write the `envelope` section from what you observed, never from documentation.** On the
reference project the documentation described 6 shapes and the API produced 31.

Probe 10–20 **read** endpoints, then answer three questions in the profile:
whether a bad request returns `4xx` (`status_is_authoritative`), how success is signalled
(`success_fields`, `created_messages`, `noop_messages`), and how many distinct shapes exist
(`shapes_measured`). Protocol: `references/03-probe-protocol.md`.

### Phase 3 — One chain by hand

⚠️ **Do not skip this to get to generation faster.** Hand-writing one chain is what surfaces the
assertion subtleties that then apply to every generated flow. On the reference project this phase
is where it emerged that a success flag can accompany a create that created nothing — a rule that
subsequently governed hundreds of generated flows.

### Phase 4 — Generate

Classify → pair → emit. Read the catalogue, classify each endpoint by name, pair each create with
a read that can confirm it, and emit flow JSON. **Flows are data; the executor is code** — adding
coverage means emitting more JSON, never editing the runner. `references/04-generation.md`.

### Phase 5 — Execute

Deny-by-default, throttled, breaker-armed, checkpointed, resumable. A bare run makes zero HTTP
calls. `references/05-safety-and-operations.md`.

### Phase 6 — Report

Dated run folder, retained forever, one evidence file per call, every exclusion counted with a
reason. `references/06-reporting-and-benchmark.md`.

---

## What transfers, and what must be rebuilt

| Transfers unchanged | Rebuilt per project |
|---|---|
| The executor — substitute → call → extract → assert → carry | The endpoint catalogue source |
| The declarative flow schema | The payload source |
| The layered assertion model | How success and failure are signalled |
| Safety scaffolding — deny-by-default, blocklist, breaker, throttle, checkpoint/resume | The blocklist contents |
| Dated retained run folders, redacted evidence | The auth mechanism |
| The generator's *structure* (classify → pair → emit) | The classification rules and the prelude |

**Rule of thumb:** anything naming a business noun is project-specific and belongs in the profile.
Anything naming only HTTP and JSON transfers.

---

## Reporting progress to the user

State the phase, its exit criterion, and what is blocking. Never report a phase complete on the
strength of having written the code for it — the criterion is an observed outcome.

⛔ **Every exclusion is reported with a reason and a count.** Silent truncation reads as "covered
everything" when it did not. If something is withheld — blocklisted, destructive, undeployed,
unreachable — it is **Blocked** with a per-item reason, never skipped.
