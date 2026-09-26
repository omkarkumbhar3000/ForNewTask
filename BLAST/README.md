# B.L.A.S.T. Framework

A reusable protocol for building deterministic, self-healing software:
**B**lueprint → **L**ink → **A**rchitect → **S**tylize → **T**rigger, on top of the **A.N.T.** 3-layer
architecture. This folder is the framework only; the work it drives lives in `../New Task/`.

## How to use it

1. **Give an instruction.** For any substantive request it is written into `Objective.md` first, and the
   outgoing objective is archived to `../docs/history/`. You can also edit `Objective.md` yourself.
2. **It loads itself.** `hooks/inject-objective.ps1` injects `Objective.md` on every prompt (wired in
   `../.claude/settings.json`), so an edit takes effect on the next message.
3. **To run the full protocol**, hand the System Pilot both files:
   ```
   @B.L.A.S.T.md @Objective.md
   Follow the BLAST protocol. Start at Protocol 0.
   ```
   The Pilot halts at Discovery, asks its five questions, and builds nothing until the data schema is
   confirmed in `LLM.md` and the Blueprint in `task_plan.md` is approved.

## Layout

```
B.L.A.S.T.md        The protocol: the System Pilot's instructions
Objective.md        The active instruction only, kept small. Injected on every prompt
CLAUDE.md           Guidance for Claude Code working in this folder
LLM.md              Project Constitution: schema, rules, invariants. This is law
task_plan.md        Memory: phases and checklists
findings.md         Memory: research, constraints, discoveries
progress.md         Memory: what was done, what broke, what was learned (append-only)
MCP-SETUP.md        Jira MCP activation guide (standby)
hooks/              inject-objective.ps1, the UserPromptSubmit hook behind step 2
architecture/       Layer 1: SOPs (the "how-to")
tools/              Layer 3: deterministic scripts (the "engines")
```

Layer 2 (Navigation) is the Pilot's own reasoning; it routes between SOPs and tools and is not a
directory.

## Configuration

| What | Where | Status |
|---|---|---|
| LLM key (GROQ) | `.env` → `GROQ_KEY` | ⬜ not present in this copy |
| Jira connection | `.mcp.json.template` → see `MCP-SETUP.md` | ⬜ standby |

`.env` and `.mcp.json` are gitignored. `.env.sample` documents the expected shape. Activate only what an
objective needs.

## The rules that matter

- **Objective first.** No work starts from an instruction that exists only in the chat.
- **Protocol 0 HALT.** No deliverable code until Discovery is answered and the schema is confirmed.
- **`LLM.md` is law**; the planning files are memory.
- **Deterministic boundary.** The LLM generates content; code owns formatting and I/O.
- **Self-annealing.** A fix isn't done until the matching `architecture/` SOP records the learning.
- **No project data here.** BLAST stays reusable; project material lives in `../New Task/`.
