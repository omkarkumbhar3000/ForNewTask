# B.L.A.S.T. Framework

A protocol for building deterministic, self-healing automation.
**B**lueprint → **L**ink → **A**rchitect → **S**tylize → **T**rigger, on top of the
**A.N.T.** 3-layer architecture.

This is a clean skeleton. No application code — that gets generated when you run the
protocol against an objective.

## How to use it

1. **Write your requirement** in `Objective.md`. Since 2026-08-03 it is loaded automatically on every
   prompt, so saving the file is enough — step 2 is optional.
2. **Hand the System Pilot both files:**
   ```
   @B.L.A.S.T.md @Objective.md
   Follow the BLAST protocol. Start at Protocol 0.
   ```
3. The Pilot halts at Phase 1 Discovery, asks its questions, and only starts building
   once the Data Schema is confirmed in `LLM.md`.

## Layout

```
B.L.A.S.T.md        # The protocol — the System Pilot's instructions
Objective.md        # ← YOU EDIT THIS. Active instruction only, kept small. Auto-loaded every prompt.
                    #   History lives in ../docs/history/README.md (append-only).
CLAUDE.md           # Guidance for Claude Code working in this repo
LLM.md              # Project Constitution — schema, rules, invariants. This is law.
task_plan.md        # Memory — phases and checklists
findings.md         # Memory — research, constraints, discoveries
progress.md         # Memory — what was done, what broke, what was learned
MCP-SETUP.md        # Jira MCP activation guide (currently standby)
architecture/       # Layer 1 — SOPs (the "how-to")
tools/              # Layer 3 — deterministic scripts (the "engines")
```

Layer 2 (Navigation) is the Pilot's own reasoning — it routes between SOPs and Tools
and is not a directory.

## Configuration

| What | Where | Status |
|---|---|---|
| GROQ API key | `.env` → `GROQ_KEY` | ✅ set |
| Jira connection | `.mcp.json.template` → see `MCP-SETUP.md` | ⬜ standby |

`.env` and `.mcp.json` are gitignored. `.env.sample` documents the expected shape.

To bring Jira online: add credentials to `.env`, then `cp .mcp.json.template .mcp.json`
and restart. Full instructions in `MCP-SETUP.md`.

## Runtime notes

No `package.json` yet — Phase 1 picks the stack and Phase 3 creates the tooling.
Verified available here: Node v24.18.0, Python 3.14.6, Windows 11.

If Node is chosen, credentials load natively — no `dotenv` needed:

```bash
node --env-file=.env <script>
```

The flag must be on every run command or `GROQ_KEY` will be undefined.

⚠️ **Never call `process.exit()` after an HTTP request.** On Windows it aborts with a
libuv assertion and exit code 127 even when the request succeeded. Use `process.exitCode`.
Details in `findings.md`.

## The rules that matter

- **Protocol 0 HALT** — no code in `tools/` until Discovery is answered and the schema
  is confirmed. This is the whole point of the framework.
- **`LLM.md` is law**, the planning files are memory.
- **Deterministic boundary** — the LLM generates content; code owns formatting and I/O.
- **Self-annealing** — a fix isn't done until the matching `architecture/` SOP records
  the learning.
