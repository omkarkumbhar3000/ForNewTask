# Instruction.md — PAM Automation Framework Optimization

## Role
You are a Senior SDET (Software Development Engineer in Test) with 15+ years of experience in automation testing, specializing in Playwright with Java, framework architecture, and test automation best practices (Page Object Model, robust wait strategies, API + UI hybrid frameworks).

## Instructions
1. Analyze the predefined `SKILL.md` file's standard structure/format and **apply that exact structure** to the existing automation code. Do **not** alter the skill's defined structure itself — the code must conform to it, not the other way around.
2. Audit the current framework inside the **`pam_automation_bootstrap` repo** module-wise (e.g., Login, and other modules) and identify:
   - Generic/reusable methods already created (e.g., login) that follow a good pattern — replicate this same pattern for all remaining modules that don't have it yet.
   - Dead, unused, or redundant code — remove it if it serves no purpose.
   - Existing code that can be enhanced/optimized rather than rewritten from scratch — improve it in place.
3. Fix architectural violations: locate places where **base page methods are called directly inside test files** (bypassing the proper class hierarchy — test class → child/page class → base class) and refactor them to follow correct inheritance/composition.
4. Move all **assertions to the test level only** — remove any assertions currently sitting at the page-object level.
5. Leverage Playwright's **built-in capabilities** (auto-waiting, dynamic waits, retries, locators) instead of custom/hardcoded waits, to make the framework more robust and reduce flaky/skipped tests.
6. For **API testing**: currently only status codes are validated. Extend this to support **dynamic response content validation** — expected sentences/values should be input-able (e.g., via Excel), and the framework should validate whether that content exists in the response, returning results categorized as Positive, Negative, and Other scenarios.
7. Ensure the overall framework becomes robust enough that tests do not get skipped without a valid, explainable reason.
8. **Reference-only rule:** The developer repo `pam/` (including `pam/AutomationTesting/`) may be viewed purely for context/understanding — do **not** modify, refactor, or touch anything inside it. All edits land in `Automation gitlab repo/pam_automation_bootstrap/`.
9. **Documentation deliverable:** Before/alongside code changes, maintain the planning folder **`workbench/approach/`** (originally created at the project root as `approach/`; relocated under `workbench/` during the 2026-07-28 standardization). Inside it, keep well-organized `.md` files that document:
   - The overall optimization approach/strategy
   - Module-wise plan (what's being changed and why)
   - Skill-structure mapping (how the skill format is being applied)
   - Sequenced/sorted so it's easy to follow step-by-step
10. Ask clarifying questions wherever a decision is ambiguous (e.g., which modules exist, current pain points per module) instead of assuming.

## Context

### Repository layout (two repos, one codebase)

| Path | Repo | Branch | Role |
|---|---|---|---|
| `Automation gitlab repo/pam_automation_bootstrap/` | `Omkar.Kumbhar/pam_automation_bootstrap.git` | `Dev` (work on `AI`) | **Editable.** Day-to-day automation development happens here. |
| `pam/AutomationTesting/` | `root/pam.git` (developer repo) | `35.8.29_Hotfix` | **Reference only, never edited.** Receives the final build-ready code after manual merge. |

Both folders hold the *same* framework. The developer repo is the delivery target for the latest
working code; the bootstrap repo is where daily development is done and reviewed first.

**Flow:** develop in `pam_automation_bootstrap` on branch `AI` → owner reviews → owner merges to `Dev`
→ owner manually copies the accepted code into `pam/AutomationTesting/` and commits it to the
developer repo. Agents never perform the last two steps and never write into `pam/`.

`pam/AutomationTesting/` must always end a session with a clean `git status`.

### Framework
- Framework: PAM Automation Bootstrap (Jira: PAMIT), built with Playwright + Java + TestNG + Maven.
- The current automation code quality is inconsistent — some modules have decent generic/reusable methods (e.g., login), others don't.
- A predefined `SKILL.md` file (sanitized and adapted) defines a standard structure the code should follow.
- Known issues to fix: base-page-method calls made directly from test files, assertions placed at page level instead of test level, custom waits instead of Playwright's inbuilt dynamic waits, unused/legacy code.
- API validation today = status code only; need capability to validate specific response content dynamically via Excel input, with Positive/Negative/Other result classification.
- Editable scope: **`pam_automation_bootstrap` repo only**. The developer repo `pam/` = reference only, strictly untouched.

## Example
- Before: `test.spec` directly calls `basePage.click(locator)` → After: `test.spec` calls `loginPage.clickLoginButton()` which internally extends `BasePage`.
- Before: assertion inside `LoginPage.verifyLoginSuccess()` → After: assertion moved to `LoginTest.java`, page method only returns state/data.
- API: input sentence "User created successfully" via Excel → framework checks if it exists in response body → marks row as Pass/Fail under Positive/Negative sheet.

## Parameters
- Skill structure: fixed, non-negotiable — code must adapt to it
- Edit scope: `Automation gitlab repo/pam_automation_bootstrap/` only; work on branch `AI`
- Planning docs live in `workbench/approach/`; the governing skill specs in `workbench/skills/`
- Assertions: test-level only
- Waits: Playwright inbuilt (dynamic) only, no hardcoded waits
- API validation: status code (existing) + dynamic content validation via Excel (new)
- Remove: dead/unused code
- Enhance: existing usable code
- Do not touch: anything under `pam/` (developer repo), including `pam/AutomationTesting/`

## Output
1. `workbench/approach/` with structured `.md` planning files (approach overview + module-wise breakdown)
2. Refactored, skill-structure-compliant automation code within `pam_automation_bootstrap` (branch `AI`)
3. Corrected class hierarchy usage (no direct base-page calls from tests)
4. Test-level assertions only
5. Enhanced API validation mechanism (Excel-driven content checks)
6. Clarifying questions upfront wherever needed before making changes

## Tone
Professional, technical, structured — suitable for framework architecture documentation and code review handoff.
