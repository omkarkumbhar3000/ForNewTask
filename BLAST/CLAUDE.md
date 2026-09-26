# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What BLAST is

**B.L.A.S.T.** (Blueprint → Link → Architect → Stylize → Trigger) is a reusable protocol for building
deterministic, self-healing software on the **A.N.T.** three-layer architecture. This folder is the
framework only: the protocol, the objective file, the memory templates and the layer skeletons. It holds
no project code and no project data. The root `../CLAUDE.md` owns the workspace rules and outranks
`LLM.md` wherever the two disagree.

The framework runs by being *executed as a prompt*. The owner's usual phrasing is *"Run `Objective.md` by
referring to `blast.md`, and give me the output"* (`blast.md` means `B.L.A.S.T.md`), or:

```
@B.L.A.S.T.md @Objective.md
Follow the BLAST protocol. Start at Protocol 0.
```

Read both files in full before acting. `B.L.A.S.T.md` assigns you the "System Pilot" role and constrains
what you may do and when.

## The objective file — `Objective.md`

`Objective.md` holds **what the owner wants done right now, and nothing else**. The owner sometimes calls
it `object.md`; it is this file. The objective-first workflow (archive the outgoing objective, write the
new instruction here, ask ambiguities, then work from it) is defined in the root `../CLAUDE.md`.

- **It arrives on every prompt.** `hooks/inject-objective.ps1`, wired as the `UserPromptSubmit` hook in
  `../.claude/settings.json`, injects the current file each turn, so an edit takes effect on the next
  message. ⛔ Do not also `@`-import it in any `CLAUDE.md`: an import resolves once at session start and
  goes stale, and two copies that disagree cannot be told apart.
- **Keep it small.** The hook warns above 10,000 characters, where only a preview may reach context.
  History, findings and results go to `../docs/history/`, never back into this file.
- **It is a dynamic blueprint.** Expect completely different contents between sessions; read it fresh.

## The single most important rule: Protocol 0 HALT

**You are forbidden from writing deliverable code until all three are true:**

1. The five Discovery questions have been asked *and answered by the owner*
2. The Data Schema (input/output shapes) is written into `LLM.md` §3
3. `task_plan.md` contains an approved Blueprint

"Deliverable code" means `tools/` in a self-contained BLAST build, and **`../New Task/Updated Project/`**
for a development objective in this workspace. Your default instinct, to start coding immediately,
directly violates this. When handed an objective, the correct first action is to **stop and ask the five
Discovery questions** (North Star · Integrations · Source of Truth · Delivery Payload · Behavioral
Rules), even when the objective seems to answer them already. Confirming your reading of them is
acceptable; skipping the checkpoint is not.

Halting is the framework working, not stalling. Say so plainly if it looks like delay.

## Architecture: A.N.T. 3 layers

The layering exists because LLMs are probabilistic and business logic must not be.

| Layer | Where | Rule |
|---|---|---|
| **1 — Architecture** | `architecture/*.md` | Markdown SOPs: goal, inputs, logic steps, edge cases, output shape. **Golden Rule: if logic changes, update the SOP before the code.** |
| **2 — Navigation** | a thin entry script (e.g. `run.js`) | Routing only. Reads input, calls Layer 3 tools in order, writes output. **No business logic, no direct API calls.** |
| **3 — Tools** | `tools/*` | Atomic, deterministic, individually testable. One job each. Credentials from `.env`. |

Layer 2 is **not a directory**; it is your reasoning layer, realised as one small entry script. For an
application built in `../New Task/Updated Project/`, the same separation applies inside that project:
documented design first, thin orchestration, deterministic units.

### The deterministic boundary

The LLM produces **content only**, always as JSON. Formatting, timestamps, file naming, table layout and
all I/O are deterministic code. Never let a model control formatting or file writes. Request
`response_format: { type: "json_object" }`, then defensively normalise every key (arrays → `[]`, strings
→ safe fallback, filter non-string array members) so schema drift degrades instead of crashing.

## Memory file discipline

Four files, and they are not interchangeable:

- **`LLM.md`** — the Project Constitution. **This is law.** Update it *only* when a schema changes, a rule
  is added, or the architecture is modified.
- **`task_plan.md`** — phases and checklists. Tick items as they complete.
- **`findings.md`** — research, constraints, environment facts, API gotchas.
- **`progress.md`** — what was done, what broke, what was learned. Append-only.

After any meaningful task, update `progress.md` and `findings.md`. Do **not** touch `LLM.md` for routine
progress. The objective changes between runs, so `LLM.md`'s schema and `task_plan.md`'s phases may belong
to the previous run: at Protocol 0, establish whether this is a new objective or a continuation, and
re-derive them if new. Entries from before `OBJ-031` are in git at commit `2a3298d`.

## Self-annealing (the repair loop)

When something fails, the fix is **not complete** until step 4:

1. **Analyze** — read the actual error. Do not guess.
2. **Patch** — fix the code.
3. **Test** — verify the fix.
4. **Update Architecture** — record the learning in the matching `architecture/*.md` SOP so the error
   cannot recur.

Skipping step 4 is the most common way to break this framework.

## Credentials and connectivity

| Service | State | Notes |
|---|---|---|
| **GROQ** (LLM) | ⬜ no key in this copy | `GROQ_KEY` in `.env`; shape in `.env.sample`. The API was verified live in the framework trial (`findings.md`) |
| **Jira** | ⬜ standby, never tested | Through an MCP server, not a hand-rolled client. See `MCP-SETUP.md` |

Only activate an integration the objective needs. `.env` and `.mcp.json` are gitignored; `.env.sample`
and `.mcp.json.template` document their shape. ⛔ Never print, log or commit a credential.

## Commands

**Inside `BLAST/` there are no build, test or lint commands and no `package.json`**, by design. Phase 3
creates whatever tooling an objective needs, and a development objective keeps its own build in
`../New Task/Updated Project/`. Do not invent scripts here.

When Node is the chosen stack, this pattern is established and dependency-free. Node 20.6+ loads `.env`
natively, so `dotenv` is unnecessary:

```bash
node --env-file=.env tools/handshake.js   # Phase 2: verify the Link
node --env-file=.env run.js               # full run
```

The `--env-file` flag must be on **every** run command or credentials will be undefined.

## Known platform trap

**Never call `process.exit()` in a Node script that has made an HTTP request.** On Windows it aborts with a
libuv assertion (`!(handle->flags & UV_HANDLE_CLOSING)`, `src\win\async.c:94`) and exit code **127**,
*even when the request fully succeeded*. Set `process.exitCode` and let the event loop drain. Details in
`findings.md`.

## Keeping BLAST reusable

- ⛔ **No project data in `BLAST/`.** Project facts live in `../New Task/` and in the objective. Keep example
  identifiers generic (`PROJ-123`, `your-domain.atlassian.net`); never reintroduce author names, project
  keys, ticket IDs or deployment targets.
- **To reuse BLAST in another project, use `NewProject_Framework`** (the sibling repository
  `github.com/omkarkumbhar3000/NewProject_Framework`): `python scripts/new_project.py <folder>` creates a
  project, or adopts the framework into an existing one. It carries the generalised version of this folder
  (a portable `sh` hook, a self-check, clean memory files). Improvements to BLAST belong there, so the next
  project starts with them.
- `gemini.md` in any inherited documentation means `LLM.md`. Do not recreate `gemini.md`.
