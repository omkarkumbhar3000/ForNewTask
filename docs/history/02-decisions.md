# Owner Decisions — D-NN register

**Index:** [`README.md`](README.md) · **Earlier decisions (`D1`–`D47`):**
`git show 2a3298d:docs/history/03-decisions.md`

⛔ Append-only. Each decision states what was decided, its basis and its consequence. Cite as `D-NN`.

---

| ID | Objective | Decision | Basis | Consequence |
|---|---|---|---|---|
| D48 | `OBJ-031` | **The work area lives inside this repository**: `New Task/Current Project/` (input) and `New Task/Updated Project/` (output) | Owner's choice at intake, over placing it beside the repository | The root `CLAUDE.md`, the objective hook and git apply to the development work without extra setup |
| D49 | `OBJ-031` | **Full cleanup of the Jira/PAM/CI project.** Keep BLAST, the generic rules and four tools: the `api-onboarding` kit, the markdown → Word/Excel renderer, the PDF → page-cited text extractor, the root-path resolver | Owner's choice at intake, over "data only, keep scripts" and "archive, don't delete". Every removed file is recoverable from `2a3298d` | 661 tracked files removed. The renderer moved to `tools/render/`; the profile template moved to `tools/onboarding/profiles/`, fixing a validator that looked there while the file sat in `data/profiles/` |
| D50 | `OBJ-031` | **Start a fresh history register at `OBJ-031`**; IDs continue from the old ones | Owner's choice at intake. The old register is PAM-specific; git keeps it whole | `docs/history/` holds only this project's record. The index points at `2a3298d` for `OBJ-001`–`OBJ-030` and `D1`–`D47` |
| D51 | `OBJ-031` | **Repair the objective hook, hooks only.** One `UserPromptSubmit` hook runs `BLAST/hooks/inject-objective.ps1`; the `permissions.deny` list is unchanged | Owner's choice at intake. Both previous hooks pointed at an `E:\` path that does not exist, so the objective-first rule depended on memory alone | `BLAST/Objective.md` reaches context on every prompt through one live path, with no `@`-import. The dead `SessionStart` drift hook was removed with it |
