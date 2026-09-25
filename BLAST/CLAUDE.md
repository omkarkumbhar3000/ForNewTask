# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not an application** — it is a clean skeleton of the **B.L.A.S.T. framework**, a
protocol for building deterministic automation. There is no application code, no build, and
no tests, because nothing has been built yet. That is the intended state.

The framework works by being *executed as a prompt*. The user fills in `Objective.md`, then
hands you two files together:

```
@B.L.A.S.T.md @Objective.md
Follow the BLAST protocol. Start at Protocol 0.
```

`B.L.A.S.T.md` is the protocol you follow. `Objective.md` is the requirement you fulfil.
Read both in full before acting — `B.L.A.S.T.md` assigns you the "System Pilot" role and
constrains what you are allowed to do and when.

The owner's habitual phrasing is *"Run `Objective.md` by referring to `blast.md`, and give me
the output"* — same thing, and `blast.md` means `B.L.A.S.T.md`.

⚡ **Since 2026-08-03, `Objective.md` loads itself.** The root `CLAUDE.md` imports it and a
`UserPromptSubmit` hook re-injects it on every prompt, so the owner's edits take effect
immediately — you will already have its current contents before being handed anything.
Historical context lives in `../docs/history/README.md`, which is **append-only**:
consult it for *why* a rule exists, and append to it when a requirement changes or a run
produces a durable finding. Never edit its existing entries.

## This directory is not standalone — read the parent CLAUDE.md

`BLAST/` sits inside the **ARCON PAM automation workspace** (`E:\Omkar\Automation\Dev Project`).
The parent `../CLAUDE.md` owns the workspace rules and **outranks `LLM.md`** wherever the two
disagree. Load it before starting a run. The three that bite hardest:

| Rule | Effect on a BLAST run |
|---|---|
| **Edit scope** | Deliverables land in `../Automation gitlab repo/pam_automation_bootstrap/` on branch `AI`. `../pam/` is reference data — never write to it. |
| **Never push, never merge** | Phase 5 cannot deploy. A run ends *committed on `AI`*; the owner merges and releases. The real "trigger" is the Jenkins pipeline plus a TestNG suite XML, not a cloud cron. |
| **The response envelope** | PAM returns HTTP 200 with an app-level `errorCode`. Never generate an assertion that checks status alone. |

`Objective.md` is a **dynamic blueprint** — the owner rewrites it per requirement and reruns.
Read it fresh every time. Because it changes, treat `LLM.md`'s schema and `task_plan.md`'s phases
as belonging to whichever objective was last run: establish at Protocol 0 whether this is a new
objective or a continuation, and re-derive them if new. `progress.md` stays append-only.

Deliverables in the automation repo are **Java 21 + Playwright + TestNG + Maven**, so the stack
is not a free choice there — see "Commands" below for what that does and does not settle.

## The single most important rule: Protocol 0 HALT

**You are forbidden from writing anything in `tools/` until all three are true:**

1. The five Discovery questions have been asked *and answered by the user*
2. The Data Schema (input/output JSON shapes) is written into `LLM.md` §3
3. `task_plan.md` contains an approved Blueprint

Your default instinct — start coding immediately — directly violates this. When handed an
objective, the correct first action is to **stop and ask the five Discovery questions**
(North Star · Integrations · Source of Truth · Delivery Payload · Behavioral Rules), even
when the objective seems to already answer them. Confirming your reading of them is
acceptable; skipping the checkpoint is not.

Halting is the framework working, not stalling. Say so plainly if it looks like delay.

## Architecture: A.N.T. 3 layers

The layering exists because LLMs are probabilistic and business logic must not be.

| Layer | Where | Rule |
|---|---|---|
| **1 — Architecture** | `architecture/*.md` | Markdown SOPs: goal, inputs, logic steps, edge cases, output shape. **Golden Rule: if logic changes, update the SOP before the code.** |
| **2 — Navigation** | a thin entry script (e.g. `run.js`) | Routing only. Reads input, calls Layer 3 tools in order, writes output. **No business logic, no direct API calls.** |
| **3 — Tools** | `tools/*.js` | Atomic, deterministic, individually testable. One job each. Credentials from `.env`. |

Layer 2 is **not a directory** — it is your reasoning layer, realized as one small entry
script. Do not create a `navigation/` folder.

### The deterministic boundary

The LLM produces **content only**, always as JSON. Formatting, timestamps, file naming,
table layout, and all I/O are deterministic code. Never let a model control formatting or
file writes. In practice: request `response_format: { type: "json_object" }`, then
defensively normalize every key (arrays → `[]`, strings → safe fallback, filter non-string
array members) so schema drift degrades instead of crashing.

## Memory file discipline

Four files, and they are not interchangeable:

- **`LLM.md`** — the Project Constitution. **This is law.** Update it *only* when a schema
  changes, a rule is added, or the architecture is modified.
- **`task_plan.md`** — phases and checklists. Tick items as they complete.
- **`findings.md`** — research, constraints, environment facts, API gotchas.
- **`progress.md`** — what was done, what broke, what was learned.

After any meaningful task, update `progress.md` and `findings.md`. Do **not** touch
`LLM.md` for routine progress — that is what the planning files are for.

## Self-annealing (the repair loop)

When something fails, the fix is **not complete** until step 4:

1. **Analyze** — read the actual error. Do not guess.
2. **Patch** — fix the script in `tools/`.
3. **Test** — verify the fix.
4. **Update Architecture** — record the learning in the matching `architecture/*.md` so the
   error cannot recur.

Skipping step 4 is the most common way to break this framework.

## Credentials and connectivity

| Service | State | Notes |
|---|---|---|
| **GROQ** | ✅ live, verified | `GROQ_KEY` in `.env`. Model used previously: `openai/gpt-oss-120b`. |
| **Jira** | ⬜ standby, never tested | Config structure only. See `MCP-SETUP.md`. |

Jira is reached through an **MCP server**, not a hand-rolled REST client. To activate:
`cp .mcp.json.template .mcp.json`, then restart. The template targets Atlassian's remote
MCP server (browser OAuth, no token on disk). A token-based alternative for Jira
Server/Data Center is documented in `MCP-SETUP.md` with its package name deliberately
unpinned — resolve it against the user's actual deployment, since env-var names differ
between servers.

`.env` and `.mcp.json` are gitignored. `.env.sample` documents the expected shape.

## Commands

**Inside `BLAST/`** there are still **no build, test, or lint commands and no `package.json`** —
Phase 3 creates whatever tooling a given objective needs. Do not assume Node or invent scripts here.

**The deliverable side does have a build.** When a run produces automation code, it is compiled and
run with Maven from the automation repo, and `JAVA_HOME` must be overridden first because the system
value points at a JDK that does not exist. Both are documented in `../CLAUDE.md` — follow it rather
than reconstructing the commands.

Verified on this machine: **Node v24.18.0** (npm 11.18.0), **Python 3.14.6**, Windows 11.

When Node is the chosen stack, this pattern is established and dependency-free — Node 20.6+
loads `.env` natively, so `dotenv` is unnecessary:

```bash
node --env-file=.env tools/handshake.js   # Phase 2: verify the Link
node --env-file=.env run.js               # full run
```

The `--env-file` flag must be on **every** run command or credentials will be undefined.
Quoted values in `.env` are unquoted automatically.

## Known platform trap

**Never call `process.exit()` in a script that has made an HTTP request.** On Windows it
aborts with a libuv assertion (`!(handle->flags & UV_HANDLE_CLOSING)`, `src\win\async.c:94`)
and exit code **127** — *even when the request fully succeeded*. Undici's keep-alive socket
is still closing during teardown.

Set `process.exitCode` and let the event loop drain. This was found the hard way; see
`findings.md`.

## Provenance

This is a de-identified fork of an open-source framework. The original author's identity,
deployment URLs, and Jira project references were deliberately removed, along with the
example application that shipped with it. **Do not reintroduce author-specific data,
hardcoded project keys, ticket IDs, or deployment targets.** Keep example identifiers
generic (`PROJ-123`, `your-domain.atlassian.net`).

Note that `gemini.md` in any inherited documentation means `LLM.md` — the file was renamed
and all references updated. Do not recreate `gemini.md`.
