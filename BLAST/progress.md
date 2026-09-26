# Progress Log

> What was done, what broke, what was learned. Updated after every meaningful task. Append-only.
> Entries from the retired PAM runs (Run 1, the API chaining runs, the framework trial) are in git at
> `2a3298d:BLAST/progress.md`.

## Framework validation (trial run, carried forward)

A throwaway smoke test exercised all five phases end to end: Discovery → schema → live GROQ handshake →
3-layer build → run → teardown. The self-annealing loop fired on a real defect and resolved it. All three
failure paths (missing key, missing input, empty input) exited 1 with clear messages. Durable learnings
are in `findings.md`; trial code removed.

## OBJ-031 stage 1 — BLAST reset and New Task preparation

- Workspace cleaned of the Jira/PAM/CI project: 661 tracked files removed (all recoverable from
  `2a3298d`), leaving BLAST, the generic rules and a four-tool toolkit (`../tools/`).
- The objective-first rule is now enforced: `hooks/inject-objective.ps1` is wired as the
  `UserPromptSubmit` hook and was verified by running its command and parsing its JSON envelope.
- Memory files reset to the clean template, keeping the generic learnings.
- `../New Task/Current Project/` and `../New Task/Updated Project/` created, empty.

## Status

Awaiting stage 2: the owner uploads the current project, requirement and feedback into
`../New Task/Current Project/` and starts it. Protocol 0 applies from that point.

## OBJ-032 — framework extracted to NewProject_Framework

- The reusable, generalised version of this BLAST setup now lives in the separate repository
  `NewProject_Framework` (first commit `4bd37b0`): template, portable `sh` objective hook, `verify.py`
  self-check, pre-commit safety hook, optional tools and skills, bootstrap script.
- This folder is unchanged in behaviour; its hook stays the proven PowerShell one. Status above still holds.
