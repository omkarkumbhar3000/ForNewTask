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
