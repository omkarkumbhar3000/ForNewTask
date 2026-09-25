# Graphify — graph representations of the code and the API

**Location:** workspace root, parallel to `BLAST/` · **Not versioned** — outside both git checkouts
**Purpose:** make relationships visible — across the product code, the whole workspace, and the API surface
**Last built:** 2026-07-28

---

## 1. The three layers

| Layer | Scope | Folder | State |
|---|---|---|---|
| **PAM scope** | `pam/PAM` — the .NET product only | `pam-scope/graphify-out/` | ✅ Built · 112,628 nodes · 269,879 edges · 4,895 communities |
| **Dev-project scope** | the whole workspace, so relationships trace across both repos | `dev-scope/graphify-out/` | ⬜ **Marker only — not built.** See §4 |
| **API scope** *(new)* | the API surface and its **chaining relationships** | `api-graph/out/` | ✅ Built · 1,322 endpoints · 1,680 chain candidates |

The first two are code graphs produced by the `graphify` tool. The third is the new API-side component and
is built by a script kept here, because no off-the-shelf tool knows what an endpoint chain is.

## 2. ⚠️ Why nothing lives inside `pam/`

The request was to place PAM-related items inside the PAM folder. **I did not do that, deliberately.**

`pam/` is the developer's product repository and the standing rule — set in `CLAUDE.md`, restated in
`BLAST/Objective.md`, and reaffirmed several times — is that it must never be modified and must always end a
session with a clean `git status`. Writing a 200 MB graph into `pam/artifacts/graph/` would dirty that repo and
risk graph artefacts reaching a product commit.

So the **scope** is PAM-only, exactly as asked, but the **output** is stored here:

```
artifacts/graph/pam-scope/graphify-out/     <- indexes pam/PAM, writes nothing into it
```

Its `.graphify_root` still reads `E:\...\pam\PAM`, so every path in the graph resolves against the product
tree. Nothing is lost by keeping the output outside. If you want it inside `pam/` anyway, say so — it needs
an explicit exception to the edit-scope rule, and `pam/.gitignore` would need a `artifacts/graph/` entry first.

Dev-project items are under `dev-scope/` here rather than in `workbench/`, so that all three layers sit
together and are found in one place. `workbench/graphify-pam/` has been consolidated into `pam-scope/` and
no longer exists.

## 3. API scope — the new component

Builds a graph of the API and, the point of it, **which endpoint's response feeds which endpoint's request**.

```powershell
python artifacts\graph\api-graph\build_api_graph.py
python artifacts\graph\api-graph\build_api_graph.py --min-confidence high
```

| Output | What it is |
|---|---|
| `out/api-graph.html` | Self-contained interactive graph — filter by module, confidence, cross-module; hover for detail. No external assets, opens offline |
| `out/api-graph.json` | Machine-readable nodes + chains, for the framework to consume |
| `out/chaining-report.md` | The chain candidates as a reviewable table |

### How chains are derived — three inputs, nothing hand-listed

| # | Input | Gives |
|---|---|---|
| 1 | `APIConfig.java` | 1,322 endpoints: module, controller, action, verb, model |
| 2 | `utils/apiPayload/*.java` | the literal JSON each endpoint **sends** → **input** fields (303 payloads parsed, 442 distinct fields) |
| 3 | `docs/findings/issues/Evidence/**` | real captured responses → **output** fields |

An edge is `producer --field--> consumer` when the field appears in the producer's response *and* in the
consumer's request.

| Confidence | Basis |
|---|---|
| **high** | identifier-shaped field **and** the producer's response was actually observed in a run |
| **medium** | identifier-shaped, producer inferred from naming (not yet observed) |
| **low** | non-identifier field — treat as coincidence until reviewed |

Generic names (`status`, `type`, `data`, `message`, `result`, …) are excluded outright.

### Current numbers, and the honest caveat

| | |
|---|---:|
| Chain candidates | **1,680** |
| …cross-module | **1,514** |
| …from **observed** responses | **0** |
| …from **name inference** | **1,680** |
| Distinct producers · consumers | 80 · 173 |

**Every chain is currently name-inferred, not observed.** Only GET has ever been executed, and the only GET
responses captured so far are the diagnostic endpoints (`GetStatus`, `GetDatabaseStatus`) whose fields are
all generic and correctly filtered out. So there is no observed output data to match against yet.

Spot-checked examples that look right:

```
LobId      POST /api/ADbridging/InsertLOBDetails      -> POST /api/ADbridging/UpdateLOBDetails
GroupId    GET  /api/UserDetails/GetUserGroupList...  -> POST /api/ServiceDetails/GetActiveServicesByLOBIdAndGroupId
ServiceId  POST /api/LobandService/CreatePamService   -> POST /api/ADbridging/UpdateRuleAssocUserStatus
```

**What promotes them to `high`:** one healthy run that captures real business-endpoint responses. Re-run the
builder afterwards and the observed edges replace the inferred ones automatically.

**A data-quality observation from the same parse:** the payload helpers spell the same field inconsistently
— `UserId` (226) vs `UserID` (168), `LobId` (48) vs `LOBId` (92) vs `LOBID` (54). Matching is
case-insensitive so chains still form, but the inconsistency is worth fixing.

## 4. Dev-project scope is not built

`dev-scope/graphify-out/` holds only `.graphify_root` and `.graphify_python` — no `graph.json`, no report.
Its root marker points at the whole workspace.

Building it would index `pam/`, the automation repo, `Reports/`, `data/sources/` and this folder as one
graph. That is what makes cross-repo tracing possible, and also what makes it expensive. It has not been
built because it was never requested until now and the cost is real.

To build it:

```powershell
graphify extract . --code-only          # AST only, no API key, no token cost
$env:GRAPHIFY_VIZ_NODE_LIMIT="200000"   # the default 5,000 is far too low here
graphify cluster-only . --no-label
```

⚠️ Run it from `artifacts/graph/dev-scope/`, not from the workspace root — a root-level `.graphify_root` would make
any stray `graphify` command target everything.

## 5. Regenerating

| Layer | Command | Cost |
|---|---|---|
| PAM | `graphify update .` from `pam-scope/` | 0 tokens — AST only |
| Dev project | see §4 | 0 tokens — AST only |
| API | `python artifacts\graph\api-graph\build_api_graph.py` | 0 — pure parsing |

None of the three calls an LLM or needs an API key.

## 6. Not wired to MCP

The only `.mcp.json` in the workspace is in the automation repo and points at *its* `graphify-out/graph.json`
by relative path — so the native graphify MCP tools serve the **automation-repo** graph only. Querying the
PAM graph means the CLI against `pam-scope/`. Wiring more graphs to MCP needs one server entry per graph.
