# The Developer Repository — why `pam/PAM` cannot serve as the API contract

**Question answered:** is the PAM developer repository sufficient to derive, generate and validate the API
under test? · **Verdict:** ⛔ No — it contains **48 of 1,306 endpoints (3.7%)**, and the repository is a
*client* of the API under test rather than its implementation.
**Method:** static analysis only. **Zero HTTP requests, zero database queries.** `pam/` was read and left
with a clean `git status`.
**Script:** `tools/measure_doc_gap.py` · **Row data:** `artifacts/analysis-data/doc-gap-coverage.json`
**Evidence base:** `APIConfig.java` (1,306 endpoints) · `pam/PAM` (6,866 `.cs`, 110.9 M chars) ·
`artifacts/runs/2026-07-29_181439/results.json` (326 flows · 1,873 hops)

---

## 1. What `pam/PAM` actually is, measured

Every figure in this table is produced by a single pass over `pam/PAM/**/*.cs`.

| Measure | Value | How counted |
|---|---:|---|
| `.csproj` projects | **181** | `rglob("*.csproj")` |
| `.cs` source files | **6,866** | `rglob("*.cs")` |
| Total C# source volume | **110,900,909 chars** | sum of file lengths |
| Files named `*Controller.cs` | **33** | filename suffix |
| Distinct `*Controller` classes | **25** | `class (\w+Controller)` declarations |
| …that match a declared catalogue controller | **12** | case-insensitive name match |
| …that do **not** appear in the catalogue | **13** | remainder |
| Projects containing any controller | **8** | of 181 |
| Public `{ get; set; }` properties | **6,738** | property regex |
| Properties carrying **any** validation attribute | **3** | `[Required]`/`[StringLength]`/`[MaxLength]`/`[MinLength]`/`[Range]` |

**The eight projects that contain controllers at all:** `ARCONLDAPAuthenticator`, `ARCON_ACM`,
`ARCON_ACMO`, `ARCON_ACM_Common`, `ARCON_ASM`, `ARCON_Common`, `ARCON_Services`,
`OfflineMultiTabService`. The other 173 projects contain no HTTP surface.

### 1.1 Thirteen of the 25 controller classes are not the API at all

`ARCOSAPISyn` · `Hello` · `Help` · `Home` · `MultiTabData` · `PAMADAuthenticator` · `ProxyTest` ·
`SaveAPIOutput` · `ServerProxyTest` · `Socket` · `Token` · `Values` · `frm`

⚠️ `HelloController`, `ValuesController` and `HomeController` are **ASP.NET project-template scaffolding**,
not product surface. Counting "controllers in the repo" without inspecting them overstates the API presence
by roughly half.

---

## 2. Why only 3.7% is there — and where the other 96.3% lives

### 2.1 Four ways of asking "is this endpoint in the repo?"

The 3.7% headline is the *strict* measure. Three looser measures are reported alongside it so the figure
cannot be dismissed as an artefact of a harsh definition — every measure lands far below usable.

| # | Definition | Result | Share |
|---:|---|---:|---:|
| **M1** | **Controller class *and* action both present as a public method — a real implementation** | **48 / 1,306** | **3.7%** |
| M3 | The literal `"<Controller>/<Action>"` string appears anywhere | 39 / 1,306 | 3.0% |
| M2 | The action name is a public method *somewhere* in the 110.9 M chars | 344 / 1,306 | 26.3% |
| M4 | Both names appear anywhere in any `.cs` text — deliberately generous upper bound | 352 / 1,306 | 27.0% |

M2 and M4 are **not** evidence of implementation. They collide on common words and on methods of unrelated
classes; M4 counts comments and call sites. The honest range is **3.0%–3.7%**, and the 27% upper bound
exists only to show that even the most generous reading leaves 73% unaccounted for.

### 2.2 Even the 12 "present" controllers are mostly absent

| Controller | Implemented | Declared | Share |
|---|---:|---:|---:|
| `OfflineSync` | 10 | 10 | **100%** |
| `ServiceDetails` | 17 | 126 | 13% |
| `Configuration` | 4 | 13 | 31% |
| `UIAutomationData` | 4 | 13 | 31% |
| `UserDetails` | 4 | 72 | 6% |
| `Logs` | 3 | 14 | 21% |
| `Command` | 1 | 5 | 20% |
| `CaptureLogImage` | 1 | 6 | 17% |
| `VideoLog` | 1 | 6 | 17% |
| `ActivityLogs` | 1 | 17 | 6% |
| `RASyn` | 1 | 18 | 6% |
| `ServiceDetailsV2` | 1 | 132 | **0.8%** |

`OfflineSync` is the only controller in the whole catalogue that is fully present — and it is the local
offline-sync component, not the product API. `ServiceDetailsV2` declares **132 endpoints**, the largest
controller in the catalogue, and the snapshot implements **one**.

### 2.3 ⛔ Where the other 96.3% lives — the repository is a *client*, not the server

This is the decisive finding, and it reframes the whole question.

| Evidence | What it shows |
|---|---|
| `APIParam.PAMAPIURL` referenced **123** times; `PAMAPIToken` **54** times | The product reads the PAM API's address and bearer token from configuration — it is calling a remote service |
| `pam/PAM/ARCON_ACM/ARCOSFrameworkCM/CommonFunctionsCM.cs:17026`<br>`aPIWrapper.GetAPIResponse(APIParam.PAMAPIURL, "api/Command/SessionDetails", "POST", "application/json", json, Token)` | A **call site**: the route is a string literal passed to an HTTP wrapper against a configured base URL |
| `pam/PAM/ARCON_ACM/ARCOSFrameworkCM/CommonFunctionsCM.cs:17063`<br>`APIParam.PAMAPIURL = Convert.ToString(appSettings.Rows[0]["URL"])` | The base URL is loaded from a settings table at runtime — the API is wherever that row points |
| `pam/PAM/OfflineMultiTabService/WindowsService/OfflineMultiTabService/PAMAPISync/` | A dedicated **sync client** of the PAM API (`OfflineSync.cs`, `APIOutputForMultiTab.cs`) |
| `ISSUE-005` §2 | Two disjoint surfaces: legacy `/api/<Controller>/<Action>` on port **1602**, microservices behind **`ARCONAPIGateway`** on **1302/555** |

**This explains M3 exactly.** The 39 verbatim `"<Controller>/<Action>"` literals in the repository are
**client call sites**, not server route registrations. The repository tells you which endpoints the product
*consumes*; it does not define what the API *serves*.

> **Implication, stated plainly:** the API surface under test is not the source tree we were given. The
> 1,306-endpoint legacy surface is served by components outside this snapshot. Parsing `pam/PAM` to
> enumerate, schema-derive or generate tests for the API cannot work — it would discover under 4% of the
> surface and would mislead on the rest, because what it does contain are outbound calls rather than
> contracts.

There is also no route metadata to parse: no Swagger/Swashbuckle registration and no route attributes in
the Framework projects, so even the 48 present endpoints yield no machine-readable contract.

---

## 3. ✅ What the repository *is* good for — do not discard it

The repository is genuinely valuable, just not as the API contract. It should be kept and used for exactly
these four things.

| # | Asset | Measure | Use it for |
|---:|---|---:|---|
| 1 | **C# property names → types** | **2,674** distinct properties mapped | Resolving `ServiceId` string-vs-int ambiguity; choosing the right JSON type when generating a body. Already consumed by `build_source_map.py` |
| 2 | **Client call sites** | 39 verbatim routes, 123 `PAMAPIURL` references | Showing *how* the product itself calls the API — real header, auth and body construction, observed rather than documented |
| 3 | **Prevailing code and naming patterns** | 127,741 distinct identifiers *(prior)* | Predicting field spellings (`LobId`/`LOBID`/`LobsId`) and stored-procedure naming |
| 4 | **Where validation is *not*** | 3 attributes / 6,738 properties | Positive proof that mandatory-ness is enforced in procedural code or the database, not in the models — which is what redirects the ask to a schema dump |

Item 4 is a real finding rather than a consolation: the absence is itself evidence, and it is what makes
"give us the DB schema" the correct request instead of "annotate the models" alone.

---

## 4. ⛔ What is missing

| Information | Present in `pam/PAM`? | Measured basis |
|---|---|---|
| **Route definitions / API surface** | ⛔ 3.7% | M1 = 48 / 1,306 |
| **Request schemas** — which fields, which are mandatory | ⛔ Effectively none | 3 `[Required]` in 6,738 properties |
| **Field length / format / pattern constraints** | ⛔ **Zero** | 0 × `StringLength`, `MaxLength`, `MinLength`, `Range` in 110.9 M chars |
| **Response models** | ⛔ None derivable | No DTO bound to a route; no envelope type. **31** distinct shapes observed live, **6** documented |
| **Error codes** | ⛔ No register | 108 codes observed live *(prior)*; none enumerated in the snapshot |
| **Business rules** | ⛔ Not in models | Rules such as `"Port is Mandatory"` originate in procedural/DB code |
| **Workflow / ordering constraints** | ⛔ None | No declared dependency between create → read → map operations |
| **Machine-readable contract** | ⛔ None | No Swagger/Swashbuckle; no route attributes in Framework projects |

### 4.1 The validation gap at its sharpest

All **3** validation attributes in the entire product snapshot are `[Required]`, and all three live in
**one file**:

```
pam/PAM/ARCON_Services/ProvisioningService/ProvisioningDataAccessLayer/Models/Entity.cs
    [Required] targetHostType : MachineType
    [Required] rootUser       : string
    [Required] rootpass       : string
```

⛔ **None of the three belongs to any of the 1,306 catalogue endpoints.** Measured against
`source-map.json`: of the 56 fields flagged `required_hint` across the whole merged map, **0 come from a
`[Required]` attribute** — all 56 are *inferred* from appearing in every documented example. And only
**1 of 217 create endpoints** has even one such hint.

So the product's own declared mandatory-field metadata contributes **nothing** to any endpoint we test.
That is not a partial gap; it is a total one.

---

## 5. The risks this creates, tied to measured consequences

Each risk below is bound to a number from `artifacts/runs/2026-07-29_181439/results.json`, not asserted.

| # | Risk | Measured consequence | Evidence |
|---:|---|---|---|
| 1 | **Writes cannot be driven** — no mandatory-field metadata means no valid request body | **196** L5 failures, every one carrying the identical detail `resolved []; MISSING ['NEW_ID']`; only **13 of 217** creates drivable *(prior)* | `results.json` L5 |
| 2 | **Persistence cannot be verified** — a create that fails returns no id, so there is nothing to read back | L6 `record-exists` ran on 107 hops and passed **2**; **105** failed | `results.json` L6 |
| 3 | **Chains cannot exceed depth 1 at scale** — the produced id is the chain key | 326 flows, **30 PASS / 296 FAIL**; deepest proven chain 5 hops *(prior)* | `results.json` flow verdicts |
| 4 | **Silent rejection passes as success** — no error-code register and no response model, so only the status can be asserted | L3 `envelope` **590** fail · L4 `message-semantics` **458** fail — 1,048 body-level failures a status-only suite scores green | `results.json` L3/L4 |
| 5 | **The catalogue cannot be reconciled against the build** — no route dump, no authoritative surface | **135** declared endpoints returned HTTP 404; L1 **180** fail | `results.json` L1 |
| 6 | **Negative expectations cannot be derived, only frozen** | **0** of 3,317 negative data rows carry an `ExpectedErrorCode` *(prior)* | `docs/gaps/01` §2 |
| 7 | **Destructive calls are indistinguishable from reads by verb** | Deletion is `POST /api/<C>/Delete<Thing>`; catalogue declares **982 POST / 321 GET / 2 DELETE / 1 PUT** | measured this session |

### 5.1 The causal chain — one root cause, not seven problems

```
no mandatory-field metadata in pam/PAM  (3 attributes, 0 of them ours)
  → a generated create body is invalid          → 204 of 217 creates fail
    → no identifier is returned                 → L5 fails 196x, all MISSING ['NEW_ID']
      → the chain cannot advance past hop 1     → 296 of 326 flows FAIL
        → nothing exists to read back           → L6 passes 2 of 107
          → no write is provably persisted       → persistence coverage ~0
```

**Risks 1–3 are one defect wearing three faces.** That matters for remediation: supplying mandatory-field
metadata — from the DB schema or from model annotations — collapses all three at once, and it is the single
highest-leverage item in this report.

---

## 6. ⚠️ Settling the 23-vs-54 controller contradiction

**The recorded contradiction:** `BLAST/findings.md:61`, `artifacts/loopholes/LH-05-*/EVIDENCE.md:31` and
`JIRA-TICKET.md:72` say **23 of 70** controllers are absent from `pam/PAM`.
`docs/gaps/01-Data-Gap-Analysis.md:30` and `tools/SOURCE-MAP.md:80` say **54 of 70**.

### 6.1 Method

The dispute is a **definition** collision, not an arithmetic error. So all three defensible definitions
were computed over the same single pass of `pam/PAM/**/*.cs` (`measure_doc_gap.py`, `scan_pam()`), with
case-insensitive name matching and longest-name-first alternation so `ServiceDetailsV2` cannot be swallowed
by `ServiceDetails`:

| Def | Question it answers | Absent | Present |
|---|---|---:|---:|
| **D1** | Is there a `<Controller>Controller.cs` class anywhere in the snapshot? | **58** | 12 |
| **D2** | Is even one declared action of it a public method of that class? | **58** | 12 |
| **D3** | Does the controller name appear as a whole word *anywhere* in 110.9 M chars — comments and call sites included? | **22** | 48 |

D1 and D2 agree at 58 on the same 12 controllers, which is a useful internal check: there is no controller
class present-but-empty. A controller either has an implementation or has nothing.

### 6.2 Verdict

| Claim | Status | Finding |
|---|---|---|
| **58 of 70** | ✅ **The correct answer** | Controllers with **no implementation** in `pam/PAM`. Only **12** have one. Corroborated by the independently-derived strict endpoint measure M1 = 48/1,306, which reproduces the established 3.7% exactly |
| **23 of 70** | 🟡 **Nearly right, but answers a different question** | It measures D3 — the name appearing *nowhere in any text*. Recomputed as **22**; the 1-endpoint delta is a word-boundary-versus-substring detail. D3 is **not** "absent from the repo" in any sense that matters: a name can appear only in a comment or an outbound call site |
| **54 of 70** | ⛔ **Unsupported — it was never measured** | `SOURCE-MAP.md:80` is generated by `build_source_map.py`, and line **333** emits the string `"54 of 70 catalogue controllers are absent from that snapshot"` as a **hardcoded literal**. No code computes 54. `docs/gaps/01-Data-Gap-Analysis.md` inherited it from that generated file |

> **Root cause of the contradiction:** a narrative sentence was hardcoded into a generator's output, where
> it acquired the authority of a measured figure. `SOURCE-MAP.md` is auto-generated, so the number survived
> every regeneration without ever being recomputed — which is precisely why it looked trustworthy.

### 6.3 Documents that need correcting

| File | Current | Change to |
|---|---|---|
| `tools/build_source_map.py:333` | hardcoded `54 of 70` | compute it, or cite `artifacts/analysis-data/doc-gap-coverage.json` |
| `tools/SOURCE-MAP.md:80` | `54 of 70` | **58 of 70** (regenerate after fixing the script) |
| `docs/gaps/01-Data-Gap-Analysis.md:30` | `54 of 70 controllers absent` | **58 of 70 have no implementation** |
| `docs/briefs/developer-loopholes.md:107` | `54 of 70 ... no corresponding *Controller.cs` | **58 of 70** — the wording was already the right definition; only the number was wrong |
| `BLAST/findings.md:61` | `23 / 70` | **58 / 70 absent (D1)**; keep 22 only if relabelled "name appears nowhere in any `.cs` text" |
| `artifacts/loopholes/LH-05-*/EVIDENCE.md:31`, `JIRA-TICKET.md:72` | `23 of 70 controllers absent entirely` | **58 of 70**. Regenerate via `tools/lh_specs_run.py:944,1046` — the string is hardcoded there too |
| `.claude/rules/api-surface.md:29-30` | records the contradiction as open | Replace with the settled 58, and drop the note that "the 23 has no locatable citation" — it is now located (D3) |

⚠️ `docs/history/archive/workbench-archive/approach/dynamic-api-generation.md:378` also carries `23 / 70`. It is in the **frozen
archive** and must **not** be edited — the archive rule stands. Its 23 is now explained rather than corrected.

---

## 7. Contradictions found between the existing analyses

Four, all reported rather than silently reconciled.

| # | Contradiction | Resolution |
|---:|---|---|
| 1 | **Controller absence: 23 vs 54** | Settled in §6 — **58**. Both prior figures are wrong; 23 measured a different question, 54 was never measured |
| 2 | ⛔ **`docs/gaps/01-Data-Gap-Analysis.md` §3.1 does not add up.** It states 217 creates, **138 (63%)** with a body from any source, and **101** with no body derivable anywhere. **138 + 101 = 239 > 217** | Recomputed from `source-map.json`: **138** creates have fields from at least one source, **79** have none. **79 is correct; 101 is wrong.** The same 101 is repeated in `docs/briefs/document-gap.md` §5 |
| 3 | **Documented error codes: 4** | Only **3** distinct code values appear in 2,470 pages, and only **2** are ARCON-format. Two of the four previously listed are false positives — see `A7-documentation-gap-analysis.md` §5 |
| 4 | **Endpoint count 1,322 vs 1,306** | `docs/findings/issues/ISSUE-005` uses **1,322** throughout (§2, §3, §4, §6). The authoritative count is **1,306**; ISSUE-005 predates the correction and should carry a note |
| 5 | **Response shapes: 8** | **31** distinct shapes were measured across the 1,868 calls, only **6** of them documented *(supplied)*. This supersedes the 8 in `docs/briefs/developer-loopholes.md` and `docs/briefs/document-gap.md` §0/§3 |

Contradiction 2 is the one that matters operationally: it understates the recoverable create population by
22 endpoints and misstates the size of the hardest tier of the create problem.

A full list of every affected document and location is consolidated in
`A7-documentation-gap-analysis.md` §9.

---

## 8. Conclusion

| Question | Answer |
|---|---|
| Is `pam/PAM` sufficient to derive the API under test? | ⛔ **No.** 3.7% strict, 27% on the most generous reading |
| Is it sufficient to derive request schemas? | ⛔ **No.** 3 validation attributes in 6,738 properties, none on a catalogue endpoint |
| Is it sufficient to derive response models or error codes? | ⛔ **No.** Neither exists in the snapshot |
| Should it be discarded? | ✅ **No** — keep it for C# types (2,674 properties), client call sites, and naming patterns (§3) |
| What *is* it? | A snapshot of the product that **consumes** the PAM API, plus supporting services. The API itself is hosted separately and is not in this tree |
| What would make it sufficient? | Swashbuckle/OpenAPI on the actual API host, plus model annotations or a DB schema dump. Costed in `data/analysis/solutions-A6A7.json` (`A6-*`) |

**One-line verdict:** the repository was provided to answer *"what is the API?"* and it answers a different
question — *"what does the product call?"* Both are useful; only one was asked for.

---

## 9. Reproducing every figure in this report

```powershell
python tools\measure_doc_gap.py
#   -> artifacts\analysis-data\doc-gap-coverage.json      one row per controller
#   -> tools\.doc-gap-summary.json  every headline figure
```

Read-only over `APIConfig.java`, `pam/PAM/**/*.cs`, `artifacts/rag-corpus/corpus.jsonl`,
`tools/source-map.json` and `artifacts/runs/2026-07-29_181439/results.json`. It issues **no HTTP
request and no database query**, and writes nothing into `pam/`, `Reports/` or the automation repo.

| Figure | Where it comes from |
|---|---|
| Controller absence D1/D2/D3 | script stdout, `controller_absence_definitions` in the summary |
| Endpoint presence M1–M4 | script stdout, `endpoint_presence_measures` |
| Per-controller implementation counts | `artifacts/analysis-data/doc-gap-coverage.json` → `endpoints_in_pam_repo` |
| L1–L7 check tallies | `results.json`, reproduced in the summary's `run.totals` |
| The 3 `[Required]` properties | `pam/PAM/ARCON_Services/ProvisioningService/ProvisioningDataAccessLayer/Models/Entity.cs` |
