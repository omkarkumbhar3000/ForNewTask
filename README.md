# ForNewTask — BLAST framework and the New Task work area

**What this is:** a reusable framework (BLAST) for running development work through a written objective,
plus the work area for the current project.
**Active objective:** see [`BLAST/Objective.md`](BLAST/Objective.md) · **History:** [`docs/history/`](docs/history/README.md)
**Current project:** CleverCubs — [`New Task/Updated Project/README.md`](New%20Task/Updated%20Project/README.md)
**Audience:** anyone opening this repository cold, whether to review it or to work in it.

---

## 1. What is in here

| Folder | What it is | May I change it? |
|---|---|---|
| **`BLAST/`** | The framework: the B.L.A.S.T. protocol, `Objective.md` (the one active instruction), the planning memory files and the hook that loads the objective on every prompt | ✅ `Objective.md` is the input; keep the rest generic |
| **`New Task/Current Project/`** | The existing project to improve, with its requirement and colleague feedback, as provided | ⛔ Reference only |
| **`New Task/Updated Project/`** | The improved project and everything produced for it | ✅ All development happens here |
| **`tools/`** | Reusable toolkit: markdown → Word/Excel (`render/`), searchable PDFs with page citations (`rag/`), an API-testing onboarding kit (`onboarding/`) | ✅ |
| **`docs/history/`** | Append-only record of every objective, owner decision and lesson | ⚠️ Append only |
| `CLAUDE.md` | Operating rules for the AI assistant, including the objective-first rule | ✅ |

## 2. How work flows

```text
 instruction ──► BLAST/Objective.md ──► analysis ──► plan ──► build ──► validate ──► docs/history
                 (written first,         of Current   (major     in Updated
                  questions asked)       Project +    changes    Project/
                                         requirement  approved)
                                         + feedback
```

1. Give the instruction. It is written into `BLAST/Objective.md` first, the previous objective is archived,
   and anything ambiguous comes back as a multiple-choice question.
2. The current project is analysed in full before anything is built.
3. Safe improvements are made directly; major or destructive changes are proposed and wait for approval.
4. The result is validated before it is called done, and the history records what changed.

## 3. Starting the next project

Put the current project, the requirement document and the colleague feedback into
`New Task/Current Project/` (without the project's own `.git` folder), then say so. Details:
[`New Task/README.md`](New%20Task/README.md).

## 4. Reusing BLAST elsewhere

Copy `BLAST/`, the rules in `CLAUDE.md`, the `UserPromptSubmit` hook entry in `.claude/settings.json`, and
whichever tools the project needs. The hook finds the workspace root by looking for `CLAUDE.md` and
`.claude/`, so it works in any folder that has both.

## 5. Previous project

This repository used to hold a Jira/PAM/CI analysis workspace. `OBJ-031` retired it; the complete tree is
recoverable from commit `2a3298d`.
