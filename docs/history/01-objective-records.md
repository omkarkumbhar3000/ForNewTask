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

---

### OBJ-032 — Documentation correction, and the `NewProject_Framework` repository

**Objective ID.** `OBJ-032`

**Title.** Correct the repository documentation, then extract the reusable framework into the new
`NewProject_Framework` repository.

**Status.** Superseded by `OBJ-033`. ✅ Completed before it was superseded.

**Summary.** Part 1 corrected the folder-level `..\CLAUDE.md`: it now says this repository is a git
repository, and eight further statements the restructure had made wrong were fixed. It also corrected one
sentence of the global `~/.claude/CLAUDE.md`. Part 2 built the generic framework as a product in the sibling
repository `..\NewProject_Framework`. It has a clean `template/`, optional `tools/` and `skills/`, a
generalised `global/` setup, a bootstrap script `scripts/new_project.py` (create or adopt, never overwrite)
and a verification gate `scripts/verify.py`.

**Key Deliverables.**
1. `..\CLAUDE.md` corrected in place (not versioned; backed up first).
2. `~/.claude/CLAUDE.md`: one sentence corrected, verified by diff against a backup (`D54`).
3. `NewProject_Framework` 1.0.0, first commit `4bd37b0`, pushed to `main` and verified equal to the remote.
   It passed the 15-check gate, five deliberate negative tests and a fresh-clone run.
4. Owner decisions `D52`–`D54`.

**Related Files.** `..\CLAUDE.md` · `~/.claude/CLAUDE.md` · `..\NewProject_Framework\` ·
`BLAST/CLAUDE.md` §Keeping BLAST reusable · `docs/history/02-decisions.md` ·
`docs/history/03-narrative-log.md` §OBJ-032.

**Reason for Archiving.** The owner issued `OBJ-033` (identify, document and address the security issues of
the uploaded current project, which is stored locally with no git push or pull).

**Pending Work.** None for `OBJ-032` itself. Stage 2 of `OBJ-031` stays pending as recorded there.

**Lessons Learned / Observations.**
- A gate that passed first time still needed a negative test. A project created with a subset of tools
  failed its own link check, and only a deliberately broken project exposed it.
- A stored denylist of old-project names would itself be baggage. The framework keeps generic checks only.
- A pasted credential was never needed. The machine's existing git credentials sufficed; the token was not
  used or stored, and the owner was advised to revoke it.

**Dependencies.** `OBJ-031` · `D52`–`D54`.

---

### OBJ-033 — Security issues of the current project, stored locally

**Objective ID.** `OBJ-033`

**Title.** Identify, document and address the security issues of the uploaded current project
(`Kids_learn_project`), which is stored locally with no git push or pull.

**Status.** Superseded by `OBJ-034` at intake. Nothing was built.

**Summary.** The owner asked for every security issue to be identified, documented and addressed to
standard practice, and said the project stays local with no git push or pull for now. Intake wrote the
instruction and a Discovery reading, and began a read-only audit. The intake questions (login architecture,
how to verify without PHP, media copy, report format) were withdrawn when the owner supplied the full
enhancement requirement.

**Key Deliverables.** None built. The audit's early observations were carried into `OBJ-034`: two login
systems, plain-text passwords in `localStorage`, a login gate that exists only in the browser, SQL
injection in `feedback.php` and `progres.php`, and hard-coded database credentials.

**Related Files.** `BLAST/Objective.md` · `New Task/Current Project/Kids_learn_project/`.

**Reason for Archiving.** The owner supplied the full Kids Learn enhancement requirement, which includes
security as a mandatory section (its §20) and specifies a Java backend. The security-only scope was folded
into `OBJ-034`.

**Pending Work.** None separately. Every security item is carried in `OBJ-034`.

**Lessons Learned / Observations.**
- A narrow instruction that arrives just before a full requirement is best held at intake. Questions asked
  against the narrow scope (such as fixing the PHP backend in place) would have been answered for a stack
  the full requirement then replaced.

**Dependencies.** `OBJ-031` stage 2 · `D55`.
