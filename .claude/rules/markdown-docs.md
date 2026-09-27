---
paths:
  - "**/*.md"
---

# Documentation — layering and house style

Loads when you open any markdown file. The objective-file workflow and the append-only history rule are
governance and live in the root `CLAUDE.md`.

## "Update MD files" is a defined instruction

When the owner says it, update **every markdown file currently in effect**, not just the one last
touched: the root `CLAUDE.md`, `README.md` and `AGENTS.md`, everything in `BLAST/`, the `README.md` of each
`tools/` folder, and the documentation inside `New Task/Updated Project/docs/`. Check each is still accurate
and consistent with the others. Do not add a new small Markdown file for one topic (`D77`): extend the
central guide or the matching `docs/` file.

**Excluded:** `New Task/Current Project/` (the owner's baseline, never edited), `docs/history/` entries
(append-only), and anything generated (a `.docx`/`.xlsx` rendered from markdown; a corpus in `.tmp/`).

## One fact, one home

A fact belongs in exactly one layer; the others cross-reference it.

| Layer | Where | Holds |
|---|---|---|
| **Requirement — active** | `BLAST/Objective.md` | The single active objective. Injected every prompt; kept small |
| **Requirement — history** | `docs/history/` | **Append-only.** Objective register, decisions, narrative |
| **Protocol memory** | `BLAST/LLM.md`, `task_plan.md`, `findings.md`, `progress.md` | Schema and law, phases, discoveries, run history |
| **Project baseline** | `New Task/Current Project/` | The project, requirement and feedback as provided |
| **Project output** | `New Task/Updated Project/` | The improved project and its own documentation |
| Operating guidance | root `CLAUDE.md` | How to work in this workspace: development rules, conventions |
| Central guide and orientation | root `README.md` | Setup, access, credentials reference, tests, deployment, troubleshooting, and what each folder is |
| AI bootstrap | root `AGENTS.md` | What an AI agent does after a fresh clone, and the Git workflow |

Before adding a section, check whether a layer already owns the topic. **Prefer merging over creating.**
A document that asserts the state of another document goes stale; point at the source instead.

## House style

`# Subject — Purpose`, a bold `**Key:** value` metadata block, `---`, then numbered `## N.` sections.
Tables over prose, numerics right-aligned. Status as `✅ 🟡 ⬜ ⛔ ⚠️` in table cells, never checkboxes
(the `[ ]` checklists in `BLAST/task_plan.md` are the protocol's own format and stay). Sections
cross-referenced as `§N`. No YAML front-matter outside rule files. A project in `New Task/Updated Project/`
may follow its own documentation conventions.

## ⛔ Editing safety

**Never rewrite an existing markdown file through PowerShell `Set-Content` or Python `write_text`.**

| Incident | Mechanism |
|---|---|
| PowerShell `Set-Content` | PS 5.1 reads UTF-8 as ANSI → mojibake |
| A data-access requests document, in the workspace this framework came from | `Path.write_text()` truncates in `w` mode, then the write aborted on `UnicodeEncodeError: surrogates not allowed`. About 12.7 KB of authored prose was destroyed and unrecoverable |

1. **Use `Edit` for markdown changes.** A targeted `old_string` → `new_string` cannot truncate a file.
   `Write` is only for a new file, or for a file deliberately replaced wholesale.
2. **A partial write is worse than no write.** `write_text` truncates *before* it encodes, so an encoding
   error leaves the file destroyed rather than unchanged.
3. **Emoji outside the BMP need `\U0001F534`-style escapes in Python**, not surrogate pairs. Better: paste
   the character itself, or avoid emoji in scripted edits.

Git shortens the blast radius (`git restore <path>` recovers the last commit) but does not make a
whole-file write safe: recovery reaches only the last commit, needs someone to notice, and cannot restore
an ignored file.
