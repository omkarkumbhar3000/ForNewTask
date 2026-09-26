# onboarding — the portable kit for standing this solution up on a new project

**Purpose:** everything project-agnostic, in one folder, so a new project needs a profile rather than a fork.
**Origin:** built under `OBJ-011` from a PAM reference implementation (`OBJ-010`). That project, its run
evidence, its worked-example profile and the long-form guide were retired by `OBJ-031`; they are
recoverable from commit `2a3298d` (`git show 2a3298d:data/profiles/pam.json`,
`git show 2a3298d:docs/briefs/new-project-implementation.md`).
**Scope:** dynamic API test generation. It is a dormant, reusable kit: use it only when an objective is
about API test automation.

---

## 1. What is here

| Path | What it is | Edit? |
|---|---|---|
| `profile.schema.json` | The contract. Every field is a place the PAM harness currently hardcodes a PAM fact | ✅ versioned by `schema_version` |
| `profiles/_template.json` | What a new project copies. Every `UNKNOWN` is a real question with an owner | ⛔ never edit in place — copy it |
| `validate_profile.py` | The readiness gate. Structure + the operational checks a schema cannot express. **Zero HTTP calls** | ✅ |
| `skills/api-onboarding/SKILL.md` | The portable skill: seven phases, each with an exit criterion | ✅ |
| `skills/api-onboarding/references/` | Six phase guides, loaded on demand | ✅ |

## 2. Using it

```powershell
# Start a new project: copy the template, then run the gate on the copy
Copy-Item tools\onboarding\profiles\_template.json tools\onboarding\profiles\idev.json
python tools\onboarding\validate_profile.py profiles/idev.json    # exits 1, lists what is missing

# Every profile at once
python tools\onboarding\validate_profile.py --all
```

Exit codes: `0` ready to execute · `1` blocked · `2` usage error. Every mode is offline.

## 3. The two things this folder is careful about

**It contains no project facts.** The skill and the schema name no product, no endpoint, no
credential. Project facts live in a profile; that separation is the entire reusability claim, and it
is checkable — grep the skill for a product name and you should find none outside a labelled
*reference project* citation.

**It documents couplings; it does not drive a harness.** The PAM harness this kit was distilled from
(OBJ-010's 5,416-case run) was retired by `OBJ-031`. A profile describes a project's facts; wiring an
executor to read one is the next increment, scoped in §8 of the retired guide (`2a3298d`).

## 4. Dependencies

Python 3.11+ standard library only. `openpyxl` is needed for the optional Excel workbook and nothing
else. The kit is deliberately no harder to stand up than the harness it onboards.

## 5. Related

| Need | Read |
|---|---|
| The full onboarding guide, both architecture options, the recommendation | `git show 2a3298d:docs/briefs/new-project-implementation.md` |
| The worked-example profile (PAM) | `git show 2a3298d:data/profiles/pam.json` |
| How to brief the AI on a *feature*'s business context (a different problem) | `git show 2a3298d:docs/business-context/BUSINESS-CONTEXT-STANDARD.md` |
