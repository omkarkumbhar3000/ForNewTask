# New Task — Working area for the current development project

**Governing instruction:** [`../BLAST/Objective.md`](../BLAST/Objective.md) (`OBJ-034` at the time of writing)
**Framework:** [`../BLAST/`](../BLAST/) — reusable; nothing project-specific is written there
**Current project:** CleverCubs, the enhanced Kids Learn application —
[`Updated Project/README.md`](Updated%20Project/README.md) (start, try, test) and
[`Updated Project/docs/06-review-summary.md`](Updated%20Project/docs/06-review-summary.md) (what was delivered)

> The uploaded baseline, `Current Project/Kids_learn_project/`, is **not in the repository** (`D72`): its
> 579 MB were migrated into `Updated Project/` (content JSON and `media/`, checked by sha256) and the folder
> is ignored by `../.gitignore`. It is kept on disk only to re-run `Updated Project/tools/extract_content.py`.

---

## 1. The two folders

| Folder | Role | Rule |
|---|---|---|
| `Current Project/` | **Input and baseline.** The existing project as the owner provides it: source, docs, configuration, requirement documents, assets, colleague feedback, additional requirements | ⛔ Read and analyse; do not modify. It is the reference the updated project is compared against |
| `Updated Project/` | **Output.** Every new or changed file for this task: code, configuration, architecture, documentation, generated files, final deliverables | ✅ All development happens here, and only once the owner starts that stage |

```text
                 BLAST (reusable framework)
                          │
                      New Task
              ┌───────────┴───────────┐
              ▼                       ▼
      Current Project          Updated Project
              │                       ▲
              ├── Requirement ────────┤
              ├── Feedback ───────────┤
              ├── Analysis ───────────┤
              └── Improvements ───────┘
```

## 2. Uploading the current project

- Copy the project **into** `Current Project/`, keeping its own folder structure.
- ⚠️ **Leave out its `.git` folder**, or say that it has one. Git records a nested repository as a single
  pointer, not as files, so its contents would not be versioned here.
- `node_modules/`, `.venv/`, build output and `.env` files are ignored by the root `.gitignore`. Real
  credentials never belong in this repository; share them through a `.env` file that stays local.
- Requirement documents, feedback notes and screenshots can go in `Current Project/` beside the code, or
  in a subfolder such as `Current Project/_inputs/`. Say which files are requirements and which are
  feedback when you hand them over.
- PDFs are stored through Git LFS (`../.gitattributes`). `../tools/rag/extract.py` makes them searchable
  with page citations.

## 3. What happens next

1. The owner uploads the material and gives the instruction. It is written into `BLAST/Objective.md` first.
2. Full analysis of the current project, the requirement and the feedback. Findings are written to
   `Updated Project/` as documentation, not kept in chat.
3. Plan, with safe improvements separated from major or destructive changes; the major ones need the
   owner's approval.
4. Build the updated project in `Updated Project/`, validate it, and keep its documentation in step.

`.gitkeep` files only keep the empty folders in git. Leave them or delete them once real files arrive.
