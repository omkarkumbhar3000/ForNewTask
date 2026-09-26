# Narrative Log — What changed and what was learned

**Index:** [`README.md`](README.md) · **Earlier narrative:** `git show 2a3298d:docs/history/04-narrative-log.md`

⛔ Append-only. One section per objective, added to as the work proceeds.

---

## OBJ-031 — Clean, reusable BLAST framework and the `New Task/` work area

### Stage 1 — preparation

**What the workspace was.** A pared-down copy of the PAM API-automation workspace, focused on Jira ticket
analysis: 700 tracked files, about 200 MB, most of it PAM run data, Jira snapshots, census reports, a PAM
API harness that could not run here (its target repositories were absent), and three dashboards reading
PAM data. The BLAST folder inside it carried the retired PAM run's plan, findings and progress, and the
objective hook pointed at a drive this machine does not have.

**Order of work, and why.** The completed `OBJ-030` was archived to the old register first; it had never
received its full record. The owner's instruction was then written into `BLAST/Objective.md` as `OBJ-031`
before any change. Four ambiguities were asked as multiple-choice questions and folded back in (`D48`–
`D51`). A checkpoint commit, `2a3298d`, captured the complete old workspace plus the `OBJ-030` record
before anything was deleted, so every removed file stays one `git show` away.

**What was kept, and why each item is reusable.**

| Kept | Why |
|---|---|
| `BLAST/` protocol, objective, memory templates, layer skeletons | The framework itself. Memory files reset to the template, keeping only generic learnings |
| `BLAST/hooks/inject-objective.ps1` (new) | Makes the objective-first rule structural instead of remembered |
| `tools/paths.py` | Marker-based root resolution; its PAM locations replaced by BLAST and `New Task/` ones |
| `tools/render/` | Markdown → `.docx`/`.xlsx`, generic apart from three census section names, now removed |
| `tools/rag/` | PDF → page-cited text and search. Rewritten to take any PDFs and write to `.tmp/rag-corpus/`. Both scripts had used `tools/rag/corpus/`, while the corpus itself had been moved to `artifacts/rag-corpus/`, so search found nothing |
| `tools/onboarding/` | The `api-onboarding` skill kit, project-agnostic by design; references to retired files now point into `2a3298d` |
| `.claude/rules/markdown-docs.md` | House style and the editing-safety rules, with PAM paths removed |

**What was removed.** All Jira/PAM/CI data and deliverables (`artifacts/`, `state/`, `data/analysis/`,
`21-09-2026/`, the census reports, briefs, findings, gaps, hardening review, knowledge base), the PAM API
harness (`obj0NN_*`, `chain_runner`, `engage`, `token_guard` and the rest), the Jira census scripts, the
three PAM dashboards and the control centre, `CLAUDE.full-workspace.md`, two PAM-only rule files, and the
old history. One ignored file, the client workbook, was deleted after confirming an identical copy in
`omkar_internal/Jira RCA/`.

**Lessons.**
- **A hook that prints nothing looks exactly like a healthy one.** The wrapper script prints a visible
  warning when the root or the objective is missing, and it was verified by running its command and
  parsing the JSON, including the failure path.
- **`find … -prune` combined with `-delete` silently ignores the prune.** GNU find turns on `-depth`, warns
  and then deletes nothing. A cleanup step must be checked after it runs, not assumed.
- **A moved folder can leave a tool pointing at the old place.** The onboarding validator had looked in
  `tools/onboarding/profiles/` ever since an earlier restructure moved the template to `data/profiles/`.
  Moving the kit's data back beside its code fixed it.

**Stage 2** starts when the owner uploads the current project, the requirement and colleague feedback into
`New Task/Current Project/` and gives the instruction.

---

## OBJ-032 — Documentation correction, and the `NewProject_Framework` repository

**Why.** Each new project had meant rebuilding the rules, workflow, hooks, tools and habits of the last one.
The owner created a blank repository to hold that framework once, separately from any project.

**Part 1 — documentation.** This repository's own docs were already correct. The folder-level
`..\CLAUDE.md` (not versioned; backed up first) still said no git repository existed anywhere, and eight
further statements had gone stale: `ForNewTask` described as byte-identical to `omkar_internal/Jira RCA`,
the census commands listed as runnable here, the objective "never auto-injected", and the absent-directory,
artifact-size and backup-copy notes. Each was corrected in place and the Jira facts re-pointed at
`omkar_internal/Jira RCA`. One sentence of the global `~/.claude/CLAUDE.md` was corrected (`D54`).

**Part 2 — the framework.** Built in `..\NewProject_Framework`, a sibling folder, as a product rather than a
copy: a clean `template/` (the mandatory core), optional `tools/` and `skills/`, a generalised `global/`,
`scripts/new_project.py` (create, or adopt without overwriting) and `scripts/verify.py` (the gate), six
guides, a changelog and CI. Generalised on the way: the onboarding schema's 29 PAM-specific descriptions
rewritten as anonymous lessons, the rule set's placeholders resolved and its old-project sections removed,
the objective hook re-implemented in POSIX `sh` so one script serves Windows, macOS and Linux, git rights
aligned with the owner's standing preferences. New: a `pre-commit` hook that blocks credentials,
secret-shaped strings, conflict markers and oversized files, and a project self-check `BLAST/verify.py`.

**Validation.** The 15-check gate passed; five deliberately broken project states were each caught; a fresh
clone of the pushed repository passed the gate again. First commit `4bd37b0`, pushed to `main` and verified
equal to the remote.

**Lessons.**
- **A gate that passed first time still needed a negative test.** Breaking a generated project on purpose
  exposed a real defect the smoke test had missed: a project created with a *subset* of tools failed its
  own link check, because `tools/README.md` linked to tools it had not installed. The fix was plain paths,
  plus a partial-install case added to the smoke test.
- **A stored denylist of old-project names would itself be baggage.** The framework's permanent checks are
  generic (secrets, home paths, placeholders, links); the old-project scan was run once and not kept.
- **The pasted GitHub token was never needed.** The machine's existing credentials reached the new
  repository; the token was not used, stored or written anywhere, and the owner was advised to revoke it.
