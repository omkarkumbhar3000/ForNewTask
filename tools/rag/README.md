# rag — retrieval over the ARCON PAM product documentation

**Purpose:** make `data/sources/` queryable so that automation work can cite the product
documentation instead of guessing at PAM behaviour.
**Location:** `tools/rag/`, **outside both git repos**, so nothing here can violate the `pam/`
reference-only rule (stated in the root `CLAUDE.md` and `BLAST/Objective.md` §Constraints).
**Cost:** zero. No embeddings, no vector DB, no network, no API calls. Regex retrieval over extracted
text is sufficient at this corpus size (1.1M characters).
**Refresh:** replace the PDF in `data/sources/` and re-run `python tools/rag/extract.py`.
Deterministic. `extract.py` locates `data/sources/` by walking up the tree, so relocating this folder
does not break it.

---

## 1. What is indexed

| Document | Pages | Extracted | Headings | Slug |
|---|---:|---:|---:|---|
| `Client Manager Guide.pdf` | 399 | 388,265 chars | 1,564 | `client-manager` |
| `PAM Administrative Guide.pdf` | 702 | 726,027 chars | 4,111 | `pam-admin` |
| **Total** | **1,101** | **1,114,292 chars** | **5,675** | |

Both are Confluence spaces exported via Scroll PDF Exporter, ARCON copyright 2025, PAM version U10.

## 2. Layout

```
tools/rag/
  README.md                        this file — usage and scope
  findings.md                      the evidence layer: what the guides say, page-cited, plus the
                                   product ↔ APIConfig module mapping and coverage priority
  extract.py                       PDF → corpus. Re-run after replacing a PDF
  query.py                         retrieval CLI
  corpus/
    client-manager.md              full text, "## [pN]" marker per page
    pam-admin.md                   full text, "## [pN]" marker per page
    corpus.jsonl                   {"doc","page","text"} — one object per page
    <slug>.headings.tsv            page ⇥ level ⇥ heading
```

## 3. How to query

Run from the workspace root:

```powershell
python tools\rag\query.py find "web api registration"          # ranked pages containing all terms
python tools\rag\query.py find "access type" --doc client-manager
python tools\rag\query.py page pam-admin 447-455               # print a page range
python tools\rag\query.py toc pam-admin --level 2 --grep api   # filtered heading index
```

The `corpus/*.md` files are also plain markdown, so the `Grep` tool works directly on them and returns
line numbers. Use `query.py` when the page citation matters, `Grep` when scanning for a pattern.

**Every fact taken from these documents must be cited as `<doc>:p<N>`** — e.g. `client-manager:p102`.
That maps to the printed page in the PDF, so a reviewer can verify it in seconds.

## 4. ⚠️ What this corpus is *not*

These are **administrator and end-user guides. They are not API reference documentation.** Confirmed by
search across all 1,101 pages:

| Looked for | Result |
|---|---|
| Endpoint / route reference | ⛔ none |
| Request or response schemas | ⛔ none |
| **Error-code or status-code tables** | ⛔ **zero hits** for `error code`, `errorCode`, `status code`, `response code` |
| OpenAPI / Swagger | ⛔ none |
| API user & access-control model | ✅ yes — `client-manager:p99–107` |
| Web API configuration fields | ✅ yes — `pam-admin:p447–456` |
| Product module taxonomy | ✅ yes — `pam-admin:p9–13` |
| Domain entity vocabulary | ✅ yes — throughout |

So the guides **do not** supply an API contract. That gap is now filled from a different source — the 37
live Swagger specs the developers shared; see `../../docs/management/summary/Executive-Summary.md`. What the guides
do supply is the *access model, the module taxonomy, and
the domain vocabulary* — which is what the generator needs in order to authenticate and to build
meaningful seed data. See [`findings.md`](./findings.md).

## 5. Known extraction limits

- Screenshots carry the field labels in these guides; page text often reads as a bare field list with the
  surrounding narrative in the image. Pages that extracted nothing are marked
  `_(no extractable text - likely a screenshot)_`.
- Confluence numbered/bulleted list markers extract as orphaned `1.` `2.` `•` lines ahead of their content.
- Table cells extract in reading order, so a field table appears as `Field Name Description` followed by
  alternating label and description lines. Readable, but not machine-parseable as a table.
- `extract.py` strips repeated headers/footers and page numbers; the `www.arconnet.com|Copyright © 2025 N`
  line survives on some pages where it is glued to other text.
