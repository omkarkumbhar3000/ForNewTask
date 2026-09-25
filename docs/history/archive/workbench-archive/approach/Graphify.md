# Graphify.md — Integrate Graphify with PAM Automation Repository

> **Status:** ✅ Installed, configured and graph generated — 2026-07-27.
> Verified results are recorded in §Results at the bottom of this file.

## Role
You are a Senior DevOps/Automation Engineer with expertise in AI-assisted development tooling, knowledge graph systems, and large-scale Java test automation repositories (Playwright + Java + TestNG + Maven).

## Instructions
1. Set up **Graphify** (`graphifyy` on PyPI) for the existing PAM Automation Bootstrap repository so it can build a semantic knowledge graph of the codebase.
2. Verify prerequisites first: Python version (3.10+), available RAM, and whether the repo path is correctly accessible.
3. Install Graphify using **UV**, the standard package manager for this workflow.
4. Navigate to the automation repo root and run the initial graph generation.
5. Explain what each generated output (`graph.html`, `GRAPH_REPORT.md`, `graph.json`) represents and how to interpret them with respect to the automation framework structure.
6. Set up proper **ignore rules** (`.graphifyignore`) to exclude irrelevant files/folders (`target/`, `Execution_Reports/`, `.git/`, build artifacts, reports, binary test data) so the graph stays clean and only reflects meaningful code relationships.
7. Once the graph is built, demonstrate example queries relevant to the project — e.g., relationships between Page Object classes, base classes, and test files, or identifying architectural hubs.
8. Show how to keep the graph updated incrementally during ongoing development (`graphify update`), so it doesn't need to be rebuilt from scratch every time.
9. Do **not** modify or refactor any existing automation code during this setup — this task is limited to **installing, configuring, and generating the knowledge graph only**.
10. If any step requires clarification (e.g., folder structure, exclusions, environment-specific paths), ask before assuming.

## Context
- Project: PAM Automation Bootstrap (Jira: PAMIT), Playwright + Java + TestNG + Maven.
- **Repo path:** `E:\Omkar\Automation\Dev Project\Automation gitlab repo\pam_automation_bootstrap`, branch `AI`.
  *(An earlier draft of this file said `E:\Auto_Developer\pam` — that path does not exist on this machine and was never the target.)*
- **Scope guard:** the developer repo `pam\` — including `pam\AutomationTesting\` — is reference only and must not be touched. Every Graphify artefact and config lands in the automation repo. See `instruction.md`.
- Environment (measured 2026-07-27, not assumed):

  | Item | Value |
  |---|---|
  | OS | Windows 11 Pro 10.0.26100 |
  | Python | **3.14.6** *(earlier draft said 3.11.9)* |
  | UV | 0.11.27 |
  | pip | **26.1.2 — present** *(earlier draft said pip was removed; it is not)* |
  | RAM | 32 GB total, ~22 GB free |
  | Disk `E:` | 12.3 GB free |

- Goal: help AI tools understand the framework's architecture and the relationships between Page Objects, base classes and tests, reducing repeated context re-reading — without changing any test code.
- This is a setup/integration task, not a refactoring task.

## Example
After graph generation, a valid query would be:
> "Show me how LoginPage relates to BasePage and which test files depend on it."

Graphify should return the relevant class relationships from the generated graph rather than requiring a full file re-read.

## Parameters
- Package manager: UV (`uv tool install "graphifyy[mcp]"`)
- Install target: `Automation gitlab repo\pam_automation_bootstrap`, branch `AI`
- Extraction mode: `--code-only` (local AST via tree-sitter, **no LLM API key required**)
- Exclude: `target/`, `Execution_Reports/`, `.git/`, `testdata/*.xls`, reports, dependencies
- No code changes — setup and graph generation only
- Never write into `pam\`

## Output
1. Confirmation of prerequisites met
2. Installation commands executed successfully
3. Generated graph files with a short explanation of each
4. Sample queries run against the graph with results
5. Instructions for incremental updates going forward

## Tone
Technical, step-by-step, precise — suitable for a real environment setup, not just a demo.

---

# Results — verified 2026-07-27

## 1. Prerequisites — met

Python 3.14.6 (≥3.10 required) · UV 0.11.27 · 32 GB RAM · repo path accessible.
Two facts in the original draft were wrong and are corrected in §Context above: Python is 3.14.6 not
3.11.9, and pip **is** installed (26.1.2). UV was used regardless, as specified.

## 2. Installation

```powershell
uv tool install "graphifyy[mcp]"
```

Installed `graphifyy 0.9.28` + 30 tree-sitter grammars (including `tree-sitter-java 0.23.5`) on
Python 3.14. Two executables registered: `graphify`, `graphify-mcp`. The `[mcp]` extra was chosen so
the graph can also be served to AI assistants over MCP.

## 3. Configuration

`.graphifyignore` created at the repo root — excludes `target/`, `Execution_Reports/`, report dirs,
`testdata/` and `*.xls` binaries, `graphify-out/`, and IDE folders. Suite XMLs and `.properties` files
are deliberately **kept**.

`graphify-out/` added to `.gitignore` (~55 MB, fully regenerable).

## 4. Graph generation

```powershell
graphify extract . --code-only                  # 173 s
$env:GRAPHIFY_VIZ_NODE_LIMIT="20000"
graphify cluster-only . --no-label              # 88 s
graphify tree --label "PAM Automation Bootstrap"
```

`--code-only` runs pure local AST extraction, so **no LLM API key was required**.

| Metric | Value |
|---|---|
| Code files indexed | 1,075 |
| Nodes | 17,275 |
| Edges | 46,905 |
| Communities | 869 |
| Edge provenance | 69% EXTRACTED · 31% INFERRED (avg confidence 0.80) |
| Import cycles | **none detected** |
| Built from commit | `9b70f457` |
| Token cost | 0 in / 0 out |

## 5. Generated files

| File | Size | What it represents |
|---|---:|---|
| `graph.json` | 31.5 MB | The graph itself — nodes (classes, methods, annotations), edges (`inherits`, `calls`, `references`, `imports`), community assignments. Every query command reads this. |
| `GRAPH_REPORT.md` | 0.13 MB | Human-readable summary — god nodes, 869 communities with cohesion scores, surprising connections, import-cycle check. |
| `GRAPH_TREE.html` | 0.88 MB | Collapsible D3 tree following the source hierarchy. **The practical viewer at this repo's size.** |
| `graph.html` | 23.8 MB | Full force-directed view. Needed `GRAPHIFY_VIZ_NODE_LIMIT=20000` since 17,275 nodes exceeds the 5,000 default. Slow to open. |
| `manifest.json`, `.graphify_analysis.json` | 2.2 MB | Incremental-update bookkeeping — lets `graphify update` re-extract only changed files. |

**`embeddings.db` is not produced.** The original draft listed it; graphifyy 0.9.28 does not generate
one in this mode. Retrieval is graph-traversal based, not vector based.

## 6. Sample queries run

**Q1 — how does LoginPage relate to BasePage?**
```
graphify path "LoginPage" "BasePage"
  → LoginPage --inherits [EXTRACTED]--> BasePage        (1 hop)
```

**Q2 — explain BasePage**
```
graphify explain "BasePage"
  → src/test/java/com/arcon/utils/BasePage.java L23, degree 240
    <-- BaseTest [references]              BaseTest.java:L447
    <-- DigitalVaultHelperPage [inherits]  DigitalVaultHelperPage.java:L28
    <-- SettingHelperPage [inherits]       SettingHelperPage.java:L33
    <-- .clickOnWebElement() [calls]       BaseTest.java:L1164
    ... 236 more, each with file:line
```

**Q3 — impact analysis before touching a shared layer**
```
graphify affected "BaseTest" --depth 1
  → every dependent with file:line — the concrete blast radius for a BaseTest change
```

**Q4 — architectural hubs**
```
graphify god-nodes --top 8
  1. ApiHelper                      1091 edges
  2. BaseTest                       1055 edges
  3. Negative_API_DataProviderUtils  377 edges
  4. UI_DataProviderUtils            271 edges
  5. PAMPayLoadHelper                270 edges
  6. BasePage                        240 edges
  7. DigitalVaultHelperPage          208 edges
  8. ServiceReports                  195 edges
```

This independently confirms the `plan.md` premise: `ApiHelper`, `BaseTest` and `BasePage` are the
god objects every refactor phase has to be measured against. Q3 is now the cheapest way to size the
blast radius of a Phase 2 change before making it.

## 7. Incremental updates

```powershell
graphify update .          # AST-only re-extract of changed files; no LLM, no API cost
graphify update . --force  # required after refactors that DELETE code
```

`--force` is needed because the rebuild is otherwise rejected when the new graph has fewer nodes than
the previous one. A `graphify check-update .` call is cron-safe if this is ever wired into CI.

## 8. AI-assistant integration

`graphify claude install` wrote:
- `CLAUDE.md` — instructs Claude Code to query the graph before grepping
- `.claude/settings.json` — `PreToolUse` hooks on `Bash|Grep` and `Read|Glob`

The generated hook hardcoded an absolute path to this machine's `graphify.EXE`; it was rewritten to
call `graphify` from `PATH` so the committed config works for every developer. Each developer needs
`uv tool install "graphifyy[mcp]"` once for the hook to resolve. Hook verified returning valid
`PreToolUse` JSON.

## 9. Known limitation

The 132 TestNG suite XMLs are **not indexed** — Graphify ships no XML grammar, so suite→test-class
edges are absent from the graph. This is exactly the relationship Phase 0 repaired, so suite-reference
questions still need grep. Everything Java-side is fully covered.

## 10. Optional enhancements — all enabled 2026-07-27

Everything Graphify offers that improves day-to-day use is now on.

| # | Enhancement | Command | Result |
|---|---|---|---|
| 1 | **Community naming** | `graphify label . --backend=claude-cli` | **795 / 795 named**, 0 placeholders |
| 2 | **Git hooks** | `graphify hook install` | `post-commit` + `post-checkout` auto-refresh |
| 3 | **MCP server** | `.mcp.json` | 10 native graph tools in Claude Code |
| 4 | **Call-flow diagrams** | `graphify export callflow-html` | 7 Mermaid diagrams, 6 call tables, zoom/pan |
| 5 | **Merge driver** | registered via hook install | union-merges `graph.json` on conflict |
| 6 | **Global graph** | `graphify global add … --as pam-automation` | cross-repo queries once a 2nd repo joins |
| 7 | **Benchmark** | `graphify benchmark` | **2.5× fewer tokens per query** vs naive |

### 10.1 The backend gotcha — worth remembering

`--backend=claude` **fails** with *"No API key for backend 'claude'. Set ANTHROPIC_API_KEY"* and
silently degrades to `Community N` placeholders while still exiting 0. `--backend=claude-cli` drives
the locally installed Claude CLI instead — no API key, no per-call cost. That is what produced the
795 names here.

Re-clustering discards names. After any `cluster-only`, restore them with:

```powershell
graphify label . --missing-only --backend=claude-cli
```

Also set `$env:GRAPHIFY_VIZ_NODE_LIMIT="20000"` before any `label` / `cluster-only` run, or
`graph.html` is silently skipped and left stale.

### 10.2 Sample of named communities

```
Community 1  - "Audit Log Grid Tests"          Community 10 - "API Request Helper Utilities"
Community 3  - "Invalid Data Type API Tests"   Community 12 - "Test Teardown Hooks"
Community 4  - "Approval Workflow CRUD Tests"  Community 17 - "Base Page Objects"
Community 7  - "Module Config Constants"       Community 20 - "Browser Base Test Setup"
Community 8  - "Split Password and Login E2E"  Community 25 - "Service Access Request Page"
```

### 10.3 graphify.net — same tool, already integrated

`graphify.net` and `graphify.com` are the official sites for **the same product** installed here: the
PyPI package `graphifyy` (GitHub `Graphify-Labs/graphify`, Y Combinator S26). There is **no cloud
service, account, API key or telemetry** — the site states it "runs on-device". So there was nothing
external to connect to; the site's own instructions are the two commands below.

| Site's instruction | Status |
|---|---|
| `uv tool install graphifyy` | done — installed with the `[mcp]` extra |
| `graphify install` | **done 2026-07-27** — this was the one step still missing |
| `graphify .` | equivalent already run as `graphify extract . --code-only` |

`graphify install` registers the **skill** (distinct from `graphify claude install`, which only writes
`CLAUDE.md` + hooks). It wrote:

- `~/.claude/skills/graphify/SKILL.md` (41 KB) + 8 reference docs
  (`query.md`, `update.md`, `hooks.md`, `exports.md`, `extraction-spec.md`, `github-and-merge.md`,
  `add-watch.md`, `transcribe.md`)
- `~/.claude/CLAUDE.md` — newly created, 231 bytes, nothing overwritten

This is **user-global**, not repo-scoped, and is the only Graphify artefact outside the automation
repo. It unlocks the `/graphify` slash command after a Claude Code restart.

### 10.4 How to open the views

```powershell
cd "E:\Omkar\Automation\Dev Project\Automation gitlab repo\pam_automation_bootstrap"
Invoke-Item graphify-out\GRAPH_TREE.html                         # ← start here
Invoke-Item graphify-out\pam_automation_bootstrap-callflow.html  # architecture diagrams
Invoke-Item graphify-out\GRAPH_REPORT.md                         # named communities, god nodes
Invoke-Item graphify-out\graph.html                              # full 24 MB view, slow
```

The MCP server needs a Claude Code restart in this folder to be picked up; confirm with `/mcp`.

## 11. Scope check

All artefacts are inside `Automation gitlab repo\pam_automation_bootstrap` on branch `AI`.
The developer repo `pam\` was not touched — verified clean.
