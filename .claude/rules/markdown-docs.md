---
paths:
  - "**/*.md"
---

# Documentation — layering and house style

Loads when you open any markdown file. The objective-file rules (`BLAST/Objective.md` is the owner's;
`docs/history/README.md` is append-only) are governance and live in the root `CLAUDE.md`.

## "Update MD files" is a defined instruction

When the owner says it, update **every markdown file currently in effect** — not just the one last
touched. At minimum: the root `CLAUDE.md` and `README.md`, everything in `BLAST/`, `docs/findings/issues/`,
`workbench/` (root briefs and `rag/`), `docs/gaps/`, `writer/`, and the `README.md`/`PLAN.md` of
`artifacts/loopholes/` plus `tools/jira/jira.md`. Check each is still accurate and consistent with the others.

**Excluded:** `pam/` (reference-only), `docs/history/archive/workbench-archive/` (frozen), and **anything generated** —
`artifacts/loopholes/LH-*/EVIDENCE.md`, `EVIDENCE.xlsx` and `data/` are rebuilt by `build_lh_pack.py`.

## One fact, one home

A fact belongs in exactly one layer; the others cross-reference it.

| Layer | Where | Holds |
|---|---|---|
| **Requirement — active** | `BLAST/Objective.md` | The single active objective. Auto-loaded every prompt; kept small |
| **Requirement — history** | `docs/history/README.md` | **Append-only.** §0 Objective Register (`OBJ-NNN` audit log) + §1–§6 narrative |
| ~~Backlog~~ | — | Retired. No separate backlog file; the former queue is archived at `docs/history/README.md` §6 |
| **Protocol memory** | `BLAST/LLM.md`, `task_plan.md`, `findings.md`, `progress.md` | Schema/law, phases, discoveries, run history |
| **Evidence — measured** | `artifacts/runs/`, `docs/findings/issues/` | Execution results, coverage, defect write-ups with citable proof |
| **Evidence — documentary** | `tools/rag/findings.md` | What the product guides say, page-cited `<doc>:p<N>` |
| **Findings — stated** | `docs/briefs/developer-loopholes.md` | The 13 findings in one brief. **Source of truth for the list** |
| **Findings — packaged** | `artifacts/loopholes/LH-NN-*/` | One raisable ticket + evidence per finding. Generated |
| **Data sufficiency** | `docs/gaps/` | What each source can and cannot answer; what to request |
| **Narrative** | `docs/management/writeup.md`, `docs/briefs/overview.md` | Management-facing and demo write-ups |
| Operating guidance | root `CLAUDE.md` | How to work in this workspace |
| Orientation | root `README.md` | What each folder is, for someone opening the project cold |

Before adding a section, check whether a layer already owns the topic. **Prefer merging over creating.**

⛔ **`docs/history/archive/workbench-archive/approach/` is frozen.** It holds the superseded planning set — do not update it or
cite it as current; two of its central conclusions were overtaken by measurement. `docs/history/archive/workbench-archive/README.md`
records what moved where. Two files there remain useful: `orphans.md` (the 218-orphan catalogue) and
`Graphify.md`.

## House style

`# Subject — Purpose`, a bold `**Key:** value` metadata block, `---`, then numbered `## N.` sections.
Tables over prose, numerics right-aligned. Status as `✅ 🟡 ⬜ ⛔ ⚠️` in table cells, never checkboxes.
Sections cross-referenced as `§N`. No YAML front-matter.

⚠️ **Use the Edit tool for text files.** Rewriting through PowerShell `Get-Content`/`Set-Content` corrupted
UTF-8 into mojibake once already — PS 5.1 reads as ANSI.

⛔ **Never rewrite a markdown file with a whole-file write, and never through Python `write_text`.**
This rule has now cost real content twice, the second time destructively:

| Incident | Mechanism |
|---|---|
| PowerShell `Set-Content` | PS 5.1 reads UTF-8 as ANSI → mojibake |
| **`docs/gaps/02-Data-Access-Requests.md`, 2026-08-05** | **`Path.write_text()` truncates in `w` mode, then the write aborted on `UnicodeEncodeError: surrogates not allowed`. ~12.7 KB of authored prose was destroyed and was unrecoverable — the folder is not versioned, there were no shadow copies, and it was not in the Recycle Bin.** The file now carries a loss notice instead of its content |

Three rules follow, and they are not negotiable:

1. **Use `Edit` for every markdown change.** A targeted `old_string` → `new_string` cannot truncate a file.
   `Write` is only for a file that does not yet exist, or one being replaced wholesale on purpose.
2. **A partial write is worse than no write.** `write_text` truncates *before* it encodes, so any encoding
   error leaves the file destroyed rather than unchanged. There is no atomic-rename safety net here.
3. **Emoji outside the BMP need `\U0001F534`-style escapes, not surrogate pairs.** `"🔴"` is two
   lone surrogates in Python and raises on encode. This is what triggered the incident above. Better still:
   paste the character itself, or avoid emoji in scripted edits entirely.

⚠️ **This no longer says "a destructive edit is permanent" — `OBJ-024` changed that.** The workspace root
is now a git repository (`dynamic-api-validator`, `main`), so `docs/gaps/`, `workbench/`,
`artifacts/`, `docs/`, `data/`, `BLAST/`, `tools/` and `workbench/` **do** have
history to restore from: `git restore <path>` recovers the last committed version, and `git log -p` shows
what changed.

**The three rules above still stand unchanged**, for three reasons. Recovery only reaches the **last
commit** — anything authored since is still lost outright. It requires *noticing*, and a truncation that
silently succeeds may not be noticed for days. And `.gitignore` deliberately excludes the live token
files, so nothing there is recoverable at all. Version control shortens the blast radius; it does not
make a whole-file write safe.
