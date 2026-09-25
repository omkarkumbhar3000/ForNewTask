# onboarding — the portable kit for standing this solution up on a new project

**Purpose:** everything project-agnostic, in one folder, so a new project needs a profile rather than a fork.
**Objective:** `OBJ-011` · **Reference implementation:** PAM (`OBJ-010`, `artifacts/runs/2026-08-05_114315`)
**Read first:** [`../new-project-implementation.md`](../new-project-implementation.md) — the guide this folder serves.

---

## 1. What is here

| Path | What it is | Edit? |
|---|---|---|
| `profile.schema.json` | The contract. Every field is a place the PAM harness currently hardcodes a PAM fact | ✅ versioned by `schema_version` |
| `profiles/pam.json` | **The worked example** — PAM's entire project-specific surface, filled in from the working scripts | ✅ update when PAM changes |
| `profiles/_template.json` | What a new project copies. Every `UNKNOWN` is a real question with an owner | ⛔ never edit in place — copy it |
| `validate_profile.py` | The readiness gate. Structure + the operational checks a schema cannot express. **Zero HTTP calls** | ✅ |
| `skills/api-onboarding/SKILL.md` | The portable skill: seven phases, each with an exit criterion | ✅ |
| `skills/api-onboarding/references/` | Six phase guides, loaded on demand | ✅ |

## 2. Using it

```powershell
# Readiness gate on the worked example - exits 0
python tools\onboarding\validate_profile.py profiles/pam.json

# Start a new project
Copy-Item data\profiles\_template.json data\profiles\idev.json
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

**It changes nothing that already works.** `tools/` produced OBJ-010's 5,416-case run and
is untouched by this folder. The profile currently *documents* the couplings rather than *driving*
them; wiring the scripts to read a profile is the next increment, scoped in
`../new-project-implementation.md` §8.

## 4. Dependencies

Python 3.11+ standard library only. `openpyxl` is needed for the optional Excel workbook and nothing
else. The kit is deliberately no harder to stand up than the harness it onboards.

## 5. Related

| Need | Read |
|---|---|
| The full onboarding guide, both architecture options, the recommendation | `../new-project-implementation.md` |
| What the PAM implementation measured | `../../docs/management/summary/OBJ-010-Execution-Benchmark.md` |
| How to brief the AI on a *feature*'s business context (a different problem) | `../../docs/business-context/BUSINESS-CONTEXT-STANDARD.md` §0 |
| The PAM-specific target architecture specs (Java/TestNG, not this framework) | `../skills/*.SKILL.md` |
