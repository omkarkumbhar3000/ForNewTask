# Data Access Requests — ⛔ CONTENT LOST, RECONSTRUCTION REQUIRED

**Status:** ⛔ **This document was destroyed on 2026-08-05. Only its skeleton survives.**
**Do not treat anything below as the original text.** Sections 0–10 are gone. What is preserved is the
section map and the one table that had been read verbatim into the session before the loss.
**Last updated (original):** 2026-07-31 · **Damaged:** 2026-08-05

---

## ⛔ What happened, precisely

An assistant edit used Python's `Path.write_text()` to append a new section. `write_text` opens the file in
`w` mode, which **truncates it before writing**. The write then aborted part-way with
`UnicodeEncodeError: surrogates not allowed` — caused by emitting `🔴` as two lone surrogate escapes
(`🔴`) instead of `\U0001F534`. The file was left truncated, and a second append then landed on top
of the truncated remains.

**Recovery was attempted and failed on every available path:** `docs/gaps/` is deliberately not
versioned, there are no Volume Shadow Copies on this host, the file is not in the Recycle Bin, and no copy
exists anywhere else in the workspace.

⚠️ **One recovery path remains, and it is the owner's to try.** If this file is or was open in VS Code, its
**Timeline / Local History** (right-click the file → *Open Timeline*) may still hold a pre-truncation
revision. That is the only known route back to the original text. **Try that before rebuilding.**

⛔ **The lost body has deliberately NOT been reconstructed from memory.** This workspace's standard is that
every figure is measured and traceable, or labelled `UNKNOWN` with what would settle it. Inventing plausible
prose for eight authored access requests would be a worse failure than the data loss.

**Root cause, for the record:** `.claude/rules/markdown-docs.md` already carries the rule that was broken —
*"⚠️ Use the Edit tool for text files."* It was written after PowerShell mojibake corrupted a file once
before. The same rule covers this case: never rewrite a markdown file with a whole-file write when a targeted
edit will do.

---

## 1. The section map that existed

Recovered from a directory listing taken before the loss. Titles and line numbers are exact; the bodies are
gone.

| § | Title | Original line |
|---|---|---:|
| 0 | Summary — eight asks, ranked | 11 |
| 1 | 🔴 Unlock the API service account — blocking today | 28 |
| 2 | 🔴 Read-only database access to the QA schema | 54 |
| 3 | 🔴 Error-code register | 108 |
| 4 | 🔴 Mandatory-field metadata | 144 |
| 5 | 🟠 Route dump per build | 163 |
| 6 | 🟠 A known, restorable test dataset | 176 |
| 7 | 🟠 A decision on status-code semantics | 195 |
| 8 | 🟡 A non-shared environment window | 213 |
| 9 | What we are **not** asking for | 232 |
| 10 | Proposed sequencing | 247 |
| 11 | Decisions needed from the owner | 262 |

Two internal cross-references also survived: §2 offered a **"schema dump" alternative at §2.3**, and §7's
status-code proposal was recorded as living **inside `PAMIT-42744`**.

---

## 2. §11 — Decisions needed from the owner (**verbatim, survived**)

Read into the session before the loss, so this table is exact.

| # | Question | Options |
|---:|---|---|
| 1 | Do we request read-only DB credentials, or the **schema dump** alternative (§2.3)? | Credentials give ongoing verification; the dump is lower friction and closes the create gap |
| 2 | Who owns the error-code register ask — QA proposing from our derived 108, or development authoring it? | We have the derived table ready either way |
| 3 | Is a dedicated automation service account obtainable, or do we continue with manual tokens? | Determines whether scheduled runs are viable |
| 4 | Should the status-code decision (§7) be raised as its own ticket, or handled inside `PAMIT-42744`? | It is currently a proposal inside that ticket |
| 5 | Do we rebuild the 3,317 negative rows against real error codes once §3 lands, or start a fresh generated set? | Rebuilding preserves the module structure; generating is cleaner |

**Added by `OBJ-010` — new, not recovered:**

| # | Question | Options |
|---:|---|---|
| 6 | Is `/AdminAPI` expected to be deployed on `QA_MsSQL`? | It returns 404 on both `:6302` and `:1302`, with both credentials. If yes, it is a deployment gap; if no, **2,104 authored test rows target a surface that will never exist there** and should be retired or repointed |
| 7 | Do we raise `LH-13` (invalid token accepted) now, or hold it with LH-02…12? | A security finding — 19 endpoints, 6 of them writes. Held pending this decision; the evidence pack is complete |

---

## 3. Added by `OBJ-010` — two new asks (**new content, not recovered**)

Both come from the 2026-08-05 run — `docs/management/summary/OBJ-010-Execution-Benchmark.md`.

### 3.1 🔴 A ruling on `/AdminAPI`

**Ask:** confirm whether the `/AdminAPI/*` surface is meant to be served on `QA_MsSQL`.

**Why it matters.** Every one of the **2,104** authored test rows carrying a real `ExpectedErrorCode` — the
only rows in the entire corpus with a documented expected failure — targets `/AdminAPI/...`. Measured:
**HTTP 404 on both `:6302` and `:1302`, with both the bearer JWT and the hardcoded token the reference
`Settings.java` uses**. The reference Java tests would 404 too.

Until this is answered those 2,104 cases are reported as **Blocked / surface-not-deployed**, and the negative
dimension has **no error-code assertions at all** — it can only assert 405 and 401.

### 3.2 🟠 A route dump per build — restated with a larger number

The original §5 already asked for this. The newer run strengthens the case: **348 of the 1,388 endpoints
exercised return 404 (25.1%)**, up from 135 on the narrower run. **340 of the 872** failures in the positive
dimension are those 404s — so QA is currently reporting deployment gaps as test failures. A route dump would
let them be marked **Blocked** instead of **Failed**, which is the difference between a meaningful pass rate
and a misleading one.

---

## 4. How to rebuild this document

`01-Data-Gap-Analysis.md` is **intact** and covers the overlapping ground — what each source can and cannot
answer. It is the right starting point, together with:

| Source | What it supplies |
|---|---|
| `01-Data-Gap-Analysis.md` | The gap analysis these asks were derived from |
| `docs/findings/issues/ISSUE-009-*.md` | The service-account lockout behind §1 |
| `docs/briefs/developer-loopholes.md` §4 | The error-code register ask (§3) |
| `docs/briefs/developer-loopholes.md` §10 | Mandatory-field metadata (§4) |
| `docs/briefs/developer-loopholes.md` §5 | Route dump and the 404 measurement (§5) |
| `docs/management/summary/OBJ-010-Execution-Benchmark.md` §11 | The current recommendation set |

Rebuild it as authored prose the owner reviews — not as an assistant's recollection.
