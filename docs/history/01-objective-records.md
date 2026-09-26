# Objective Records — Full ten-field record of every archived objective

**Index:** [`README.md`](README.md) §3 · **Earlier records (`OBJ-001`–`OBJ-030`):**
`git show 2a3298d:docs/history/01-objective-records.md`

⛔ Append-only. A record is added when its objective leaves `BLAST/Objective.md`.

---

### OBJ-031 — Clean, reusable BLAST framework, and the `New Task/` work area

**Objective ID.** `OBJ-031`

**Title.** Make this workspace a clean, reusable BLAST framework, and prepare `New Task/` for the next
development project.

**Status.** Superseded by `OBJ-032`. Stage 1 (preparation) ✅ completed; stage 2 (analyse and build the
updated application) was never started, because it waits for the owner's upload.

**Summary.** The workspace held a retired Jira/PAM/CI analysis project. Stage 1 removed it without damaging
the reusable framework, made the objective-first rule structural through a `UserPromptSubmit` hook, reset
BLAST's memory files, generalised four tools, created `New Task/Current Project/` (input baseline) and
`New Task/Updated Project/` (output), and started a fresh history register.

**Key Deliverables.**
1. Commit `2a3298d`: checkpoint of the complete old project plus the `OBJ-030` record.
2. Commit `1dab83b`: 661 obsolete files removed; `BLAST/hooks/inject-objective.ps1` wired in
   `.claude/settings.json`; `tools/render/`, `tools/rag/`, `tools/onboarding/`, `tools/paths.py`
   generalised; `New Task/` created; `CLAUDE.md`, `README.md`, `AGENTS.md`, `BLAST/*` rewritten.
3. Owner decisions `D48`–`D51`.

**Related Files.** `BLAST/Objective.md` · `BLAST/hooks/inject-objective.ps1` · `.claude/settings.json` ·
`New Task/README.md` · `docs/history/02-decisions.md` · `docs/history/03-narrative-log.md` §OBJ-031.

**Reason for Archiving.** The owner issued `OBJ-032` (correct the repository documentation and extract the
reusable framework into `NewProject_Framework`) before uploading the stage-2 material.

**Pending Work.** Stage 2, unchanged: when the owner uploads the current project, requirement and feedback
into `New Task/Current Project/` and starts it, analyse the project in full and build the improved product
in `New Task/Updated Project/`. The standing direction recorded for it — user experience first, light
theme, lightweight modern technology, safe versus major changes, senior-developer mindset — is in this
objective's text at commit `1dab83b` (`git show 1dab83b:BLAST/Objective.md`) and should be carried into
the objective that starts stage 2.

**Lessons Learned / Observations.**
- A hook is verified by running its command and parsing its output, including the failure path; a silent
  hook looks exactly like a healthy one.
- `find … -prune` combined with `-delete` ignores the prune and deletes nothing; check a cleanup after it runs.
- A tool can keep pointing at a folder an earlier restructure emptied (the onboarding validator).

**Dependencies.** `OBJ-030` (the retired project) · `D48`–`D51`.
