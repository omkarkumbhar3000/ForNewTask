# AGENTS.md — Guidance for AI agents other than Claude Code

`CLAUDE.md` is the authoritative operating guide for this repository; read it first. This file restates
the parts an agent that does not load `CLAUDE.md` or run its hooks (for example OpenCode) must know.

## 1. Read the objective yourself

Claude Code receives `BLAST/Objective.md` on every prompt through a hook. **You do not.** Read
`BLAST/Objective.md` at the start of every session and before every task: it is the one active
instruction and it overrides general guidance for the current task.

For every substantive instruction (build, analyse, fix, run, produce):

1. Archive the outgoing objective to `docs/history/01-objective-records.md` (all ten fields) and update its
   row in `docs/history/README.md`.
2. Write the new instruction into the `## Instruction` block of `BLAST/Objective.md`.
3. Ask about genuine ambiguities as multiple-choice questions, and fold the answers into the file.
4. Only then do the work. Afterwards, append what changed and what was learned to `docs/history/`.

Questions and conversational replies do not rewrite the file. A correction amends it.

## 2. Where things go

| Path | Rule |
|---|---|
| `BLAST/` | Reusable framework only. No project data |
| `New Task/Current Project/` | The owner's baseline. Read it; never modify it |
| `New Task/Updated Project/` | All new development output |
| `docs/history/` | Append-only |

## 3. Hard rules

- Do not implement the new application until the owner uploads the current project and starts that stage.
- Major, destructive or architectural changes need the owner's approval first.
- Never claim something is done or tested without running the check.
- Never print, log or commit a credential. Edit markdown in place; never rewrite it through a script.
