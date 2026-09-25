# Self-Understanding — What Each Piece Actually Is

**Purpose:** personal reference. Plain language, no jargon, for recalling how this fits together.
**Not for distribution** — `docs/briefs/overview.md` is the version for other people.
**Last updated:** 2026-08-05

---

## The whole thing in one sentence

We read the test framework's own list of API endpoints, automatically write test scripts from it, run them
against the live PAM API passing real values from one call into the next, and save proof of every call —
because this API says "200 OK" even when it has failed.

---

## 1. BLAST — what it is and why we use it

**What it is:** a way of *commissioning* work, not a way of doing it. Five stages: **B**lueprint,
**L**ink, **A**rchitect, **S**tylize, **T**rigger.

**Why we use it:** it forces the requirement to be pinned down *before* any code is written. Its single most
valuable rule is **Protocol 0 HALT** — nothing gets built until three things are true:

1. The five Discovery questions are answered **by me**, not guessed by the assistant
2. The data shape is written down in `LLM.md`
3. An approved plan exists in `task_plan.md`

**How I actually use it:** I rewrite `BLAST/Objective.md` with whatever I want next, then say *"Run
Objective.md by referring to blast.md, and give me the output."* Since 2026-08-03 that file is loaded
automatically on every prompt, so editing and saving it is all I actually have to do — the run command is
just a nudge.

**The thing to remember:** `Objective.md` is a **rewritable form**, not a permanent record. It holds
today's request only. The history lives elsewhere:

| File | Holds |
|---|---|
| `docs/history/README.md` (root) | **Every instruction and decision since Day 1 — append-only.** The place to look first |
| `LLM.md` | The rules and data shapes — treated as law |
| `task_plan.md` | The phases for the current request |
| `findings.md` | Things discovered along the way |
| `progress.md` | What happened, in date order — **never overwritten** |

If I want to know what happened last week, `docs/history/README.md` or `progress.md` is the answer.
Never `Objective.md`.

---

## 2. Company Documents — what it is and its purpose

**What it is:** the raw source material, exactly as received. Four files:

| File | Size | What it actually gives us |
|---|---:|---|
| `PAM API (Internal Team).pdf` | 2,470 pp | **The API reference.** The only source with endpoints and payloads — 3,194 example request bodies |
| `PAM Administrative Guide.pdf` | 702 pp | How PAM is administered. No endpoints |
| `Client Manager Guide.pdf` | 399 pp | How the client behaves. No endpoints |
| `Automation PAM Endpoints Details_Shared(Swagger_JSON Links).csv` | — | Links to 37 live Swagger specs, 690 operations |

**Purpose:** it is the **input pile**. Nothing here is edited — documents are dropped in, and the tooling
reads them.

**Why it matters more than expected:** **79** of our create endpoints have no request body defined anywhere in
the code. The 3,194 payload examples in the API PDF are the only place that information exists. That PDF is
the route to fixing our worst number (13 of 217 creates working).

**The catch:** it is confirmed out of date, and it documents only 30% of our endpoints — but it is still the
best payload reference available.

---

## 3. Graph files — what they are and their purpose

**What they are:** a map of how code connects. Instead of reading 1,073 files to learn what depends on
`BaseTest`, the graph answers it directly.

Four graphs exist:

| Graph | Covers | Size |
|---|---|---|
| `pam_automation_bootstrap/graphify-out/` | Our test framework | 17,275 nodes · 46,905 edges |
| `artifacts/graph/pam-scope/` | The .NET product | 112,628 nodes · 269,879 edges |
| `artifacts/graph/api-graph/` | The API surface and possible chains | 1,322 endpoints · 1,680 candidates |
| `artifacts/graph/dev-scope/` | Whole workspace | Not built |

**Purpose:** answer structural questions cheaply. *What breaks if I change `ApiHelper`?* — ask the graph
rather than grepping. They cost **zero tokens** (pure code parsing, no AI).

**The honest bit worth remembering:** the graph did **not** contribute to the API chaining. Its 1,680
"chain candidates" were guesses based on two endpoints sharing a field *name* — which doesn't mean one feeds
the other. The real chains were built by pairing create→read endpoints structurally. **The graph is a
code-comprehension tool, not a test-generation tool.**

---

## 4. Reports folder — what it is and its purpose

**What it is:** the **evidence locker**. What happened, when, and proof.

```
Reports/
  Runs/2026-07-29_181439/       one folder per execution
      RUN_REPORT.md             the readable report
      results.json              the same data, machine-readable
      checkpoint.json           where to resume if interrupted
      evidence/  (5,424 files)  one file per API call: request, response, verdict
  Summary/                      reports written for people, by me
  Issues/                       11 formal defect write-ups
  _archive-pre-2026-07-29/      everything from before we stopped deleting
```

**Purpose:** so any claim can be checked. If I say "289 calls failed while returning 200", there is a file
per call proving it.

**The rule that matters:** **nothing here is ever deleted.** Every run keeps its own dated folder. It used to
auto-delete the previous run, which meant two runs could never be compared. That was removed on 2026-07-29.

**Never hand-edit anything under `Runs/`** — it is machine output. `Summary/` and `Issues/` are mine to write.

---

## 5. Workbench folder — what it is and its purpose

**What it is:** the **workshop**. Everything I build and use, none of it part of any product.

```
workbench/
  scripts/     the actual machinery + flows/ (the test definitions)
  rag/         the PDFs turned into searchable text
  skills/      target-architecture specs
  archive/     old planning docs, frozen
  react/       placeholder
  overview.md, document-gap.md, new-project-implementation.md,
  developer-loopholes.md, self-understanding.md (this file)
```

**Purpose:** a place to build that can never contaminate a product build. It sits outside both git
repositories deliberately.

**Why all scripts live here:** they used to live in `Reports/Scripts/`, which mixed the machinery in with
the evidence. Now the separation is clean.

---

## 6. How Reports and Workbench work together

The simplest way to hold it:

> **Workbench is the kitchen. Reports is the photograph of the meal.**

```
tools/          →  runs  →  artifacts/runs/<timestamp>/
(the machinery)                         (the evidence)
```

| | Workbench | Reports |
|---|---|---|
| Contains | Tools, test definitions, indexed documents | Results and proof |
| Who writes it | Me, deliberately | The scripts, automatically |
| Changes when | I improve something | Every execution |
| Retention | Current version only | **Every run, forever** |

**One-directional.** Workbench writes into Reports. Reports never writes back. That is what makes a run
reproducible: the machinery is inspectable and the evidence is untouched.

**The practical consequence:** to change *what gets tested*, edit `tools/flows/`. To find out
*what happened*, read `artifacts/runs/`. I never confuse the two.

---

## 7. The five folders, one line each

| Folder | One line |
|---|---|
| `Automation gitlab repo/` | The real test framework. **The only code I may edit**, on branch `AI` |
| `pam/` | The developers' product source. **Read only, never touch** |
| `workbench/` | My workshop — scripts, flows, indexed docs |
| `Reports/` | The evidence locker — one dated folder per run, never deleted |
| `artifacts/graph/` | Code maps, for understanding structure |
| `BLAST/` | How I commission new work |
| `data/sources/` | The raw input pile |
| `writer/` | The management write-up |

---

## 8. The three facts that explain everything else

**1. This API says 200 when it fails.** On the latest run, **1,022 of 5,416 cases (18.9%) returned HTTP 200
and still failed validation.** That single fact is why we check seven things per call instead of one — a normal
test suite would have called every one of those 1,022 a pass.

**2. Test scripts are data, not code.** Each test chain is a JSON file listing steps. One generic runner
executes any of them. So adding coverage means generating more JSON — not writing more code — and the
hand-written ones keep working unchanged.

**3. Our weak point is data, not tooling.** Only 13 of 217 create endpoints work, because the request bodies
in the framework are stale hand-written literals and **79** endpoints have no body at all. On top of that,
**348 of the 1,388 endpoints we exercised (25.1%) are not deployed at all** and return 404. The machinery is
fine. The data and the deployment are the problem.

**4. A test that cannot fail for the right reason is worse than no test.** The suite had **1,153** tests
asserting "unauthorized access returns 401" — all sending a *valid* token, so none of them could ever prove
anything. Making them send an invalid one found **19 endpoints that accept a bad token**, 6 of them writes.

---

## 9. Two things not to get wrong

**Don't quote the flow-level pass rate.** The latest run reads 579 failed / 168 passed flows, but a flow
fails if *any* of its steps fails, and some flows bundle twelve endpoints — one bad endpoint fails eleven good
ones. The honest number is **case level: 63.9%** (N-1 was 64.2%).

**Don't call the token endpoint twice.** Repeated `/arcontoken` calls **locked the shared service account**,
which is also used by a data-warehouse job. The runner generates one token per run and caches it for 24
hours. The 2026-08-05 run made **zero** `/arcontoken` calls across all 5,416 requests — and the cached token
survived a mid-run crash and resume, which is exactly the case where a careless harness would ask for a new
one.
