# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

The reusable **BLAST framework** plus the **`New Task/`** work area for the current development project.
It was a Jira/PAM/CI analysis workspace until `OBJ-031` retired that project; every removed file is
recoverable from checkpoint commit `2a3298d` (`git show 2a3298d:<path>`).

| Path | Is | Rule |
|---|---|---|
| `BLAST/` | The framework: protocol (`B.L.A.S.T.md`), the objective file, memory files, A.N.T. layer skeletons, the objective hook. Has its own `CLAUDE.md` | ⛔ Reusable only. No project data, names or keys |
| `New Task/Current Project/` | The project to improve, as the owner provides it, with its requirement and colleague feedback | ⛔ Baseline. Read and analyse; never modify |
| `New Task/Updated Project/` | The improved project: all new code, configuration, docs and deliverables | ✅ The only place development output goes |
| `tools/` | Reusable toolkit: `render/`, `rag/`, `onboarding/`, `paths.py` (§Toolkit) | A project's own tooling lives inside `Updated Project/`, not here |
| `docs/history/` | Append-only record: objective register, decisions `D-NN`, narrative | ⛔ Never edit an existing entry |
| `.claude/` | `settings.json` (objective hook, deny list) and `rules/markdown-docs.md` | ⛔ The deny list is the owner's to change |

Git: branch `main`, remote `github.com/omkarkumbhar3000/ForNewTask`.

## ⛔ The objective-first rule — the owner's rule; never remove it

**Every substantive CLI instruction (build, analyse, fix, run, produce) goes into `BLAST/Objective.md`
before any work starts, and that file then governs the work and its output.** The owner sometimes calls it
`object.md`; it is `BLAST/Objective.md`.

| Step | Action |
|---:|---|
| 1 | Archive the outgoing objective: its full ten-field record to `docs/history/01-objective-records.md`, its row in `docs/history/README.md` §3. Do this even if no work was done on it |
| 2 | Replace the `## Instruction` block of `BLAST/Objective.md` with the new instruction, faithfully and completely |
| 3 | Read it back and find genuine ambiguities. Fill gaps from the workspace first; never ask the owner to restate what is recorded |
| 4 | Ask what remains as **multiple-choice questions** (`AskUserQuestion`), recommending an option where one is better |
| 5 | Fold the answers into the file, so it matches what was agreed |
| 6 | Execute, with the file as the instruction and the workspace as context |
| 7 | On completion, update the affected docs and append what changed and what was learned to `docs/history/` (narrative; a `D-NN` record for each owner decision) |

- **Does not trigger it:** questions, conversational replies, and process or config changes. **A correction
  amends** the current instruction instead of replacing it.
- ⛔ **Never start implementation against a request that exists only in the chat.**
- **Delivery:** the `UserPromptSubmit` hook runs `BLAST/hooks/inject-objective.ps1`, which injects the rule
  and the file on every prompt. ⛔ Do not also `@`-import the file: an import goes stale after session
  start. If a turn arrives without the injected objective (the hook changed mid-session, or failed), read
  `BLAST/Objective.md` yourself before acting. Hooks are snapshotted at session start, so a hook edit takes
  effect in the next session.
- **Keep the file small** (the hook warns above 10,000 characters). History never goes back into it.
- A durable way of working the owner states belongs **here** and as a decision in `docs/history/02-decisions.md`,
  never only in the objective file, which the next instruction overwrites.

## ⛔ Stage gate and change control

- **Do not implement the new application until the owner has uploaded the material to
  `New Task/Current Project/` and explicitly started that stage.** Do not invent its requirements.
- **Protocol 0 HALT applies to `New Task/Updated Project/`:** no deliverable code until the Discovery
  questions are answered, the design and data shapes are recorded in `BLAST/LLM.md`, and `BLAST/task_plan.md`
  holds an approved Blueprint (`BLAST/CLAUDE.md`).
- **Analyse first, then plan, then build.** Findings go into `Updated Project/` documentation, not only chat.
- **Safe improvements** may be made directly. **Major, destructive or architectural changes** (replacing a
  framework, changing data shape or storage, removing a feature, breaking compatibility) are listed with
  their reason and **need the owner's approval** first.
- **Replace an existing technology only after weighing** the real benefit, the migration effort and
  compatibility, and never at the cost of working functionality.
- If the current project has a design system, extend it rather than adding a second one. Replacing it is a
  major change.

## ⛔ Standing rules

- **Nothing is finished until it is verified.** Say "done", "fixed", "tested" or "validated" only after
  running the check; report a failure with its output, and say plainly what was skipped.
- **Look at a file before deleting or overwriting it.** Edit markdown with the Edit tool only; never through
  PowerShell `Set-Content` or Python `write_text` (`.claude/rules/markdown-docs.md`).
- **Never invent a fact.** Where the source is silent, write one explicit sentinel (`TBD`,
  `Information Required`) and what would settle it.
- **Generated output is never hand-edited.** Fix the source and regenerate (for example a `.docx` rendered
  from markdown).
- **Secrets live in `.env` files**; only `.env.sample`/`.env.example` are tracked. Never print, log or
  commit a credential.
- **An HTTP 200 is not a pass** when an API reports errors in the response body. Assert the
  application-level result too.
- **Frontend quality floor:** responsive down to mobile, visible keyboard focus, `prefers-reduced-motion`
  respected, and an explicit `background` and `color` on the page root.
- **Use installed skills by relevance, not by habit.** For the development stage the likely ones are
  `frontend-design` (UI), `playwright` (browser verification), `test-driven-development`,
  `systematic-debugging` and `code-review`/`security-review` before completion. Jira and PAM workflows are
  not part of this project; `tools/onboarding/` is a dormant kit for API test automation only.

## Toolkit

No build, test suite or linter exists at the root; each tool is verified by running it. Python packages go
in a venv (a distribution-managed Python refuses a global install):

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r tools\requirements.txt      # python-docx, openpyxl, pypdf

.venv\Scripts\python tools\render\md_to_docx_xlsx.py <doc.md>       # -> <doc>.docx + <doc>.xlsx beside it
.venv\Scripts\python tools\rag\extract.py "New Task\Current Project" # PDFs -> .tmp\rag-corpus\ (page-cited)
python tools\rag\query.py find "<terms>"                            # stdlib; cite results as <doc>:p<N>
python tools\onboarding\validate_profile.py --all                   # stdlib; API-testing kit only
```

- **On the D: machine** `python` and `py` do not work; the interpreter is `python3.11` (3.11.9, no
  packages), so create the venv with `python3.11 -m venv .venv`. Under Bash set `PYTHONUTF8=1` and
  `PYTHONDONTWRITEBYTECODE=1`.
- ⛔ **`tools/paths.py` finds the root by searching upward for a directory holding both `CLAUDE.md` and
  `.claude/`.** Renaming either breaks every tool that imports it. Never count parent directories.
- Intermediates go to `.tmp/` (gitignored). A project's own dependencies and build live in
  `New Task/Updated Project/`.

## Environment and git notes

- **Primary shell is Windows PowerShell 5.1.** Paths contain spaces (`New Task`, `Current Project`,
  `Updated Project`, `VS Code`); always quote them.
- **`.claude/settings.json` denies `git merge` and `git remote set-url`** in both shells. A refused merge is
  that rule working; only the owner can change it.
- **PDFs are Git LFS objects** (`.gitattributes`); `git lfs` must be installed to clone them as files.
- **A nested `.git` in an uploaded project** is recorded as a pointer, not as files. See `New Task/README.md`.
- `mar.md` at the root is the owner's private Marathi companion to CLI sessions. It is gitignored; keep it
  that way.
