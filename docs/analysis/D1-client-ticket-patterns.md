# Client-raised PAMIT ticket analysis — the full picture

**Generated:** 2026-09-03 21:21
**Updated:** 2026-09-03 21:21

**Current build:** `35.8.29 HF13` · **Source:** Jira `PAMIT`, read-only · **Objective:** `OBJ-029` *(engine, population rules D38-D41 and taxonomy from OBJ-028)*

> **`Generated`** is when the Jira data behind these figures was captured. **`Updated`** is when this file was last written. They differ whenever the report is re-rendered from a cached capture (`--offline`) — which is precisely when a reader needs to know that the figures are older than the file they are reading.

> Four populations, four denominators, never mixed: the **build line** (2040 client tickets across 20 versions), the **focus builds** (192 client / 120 defects), the **last 30 days** (409), and **Query C** (167). Linked tickets outside a window are evidence only, never population (`D39`).

## 0. Build-wise methodology — which Jira field, and why

**The build axis is `Affected Milestone` (`customfield_10092`). Not `Fix versions`. Not `Milestone`.** Owner ruling `D42`.

| Question | Field | Populated | What it actually means |
| --- | --- | ---: | --- |
| **Where was the defect found?** ← the build-wise axis | `Affected Milestone` (`cf[10092]`) | **97.3%** (1,346/1,384) | The build the **client was running** when they hit it. A build's count is therefore *the defects that escaped into it* |
| Where was the fix shipped? | `Fix versions` (native) | 100% of the versioned slice | The release the fix **lands in**. A hotfix accumulates fixes for defects found on earlier builds, so this counts release content, not build quality |
| *(no usable field)* | the `Milestone`-named fields | 0–9% | Every milestone-shaped field in this instance was measured and rejected — §0.2 has the table |

### 0.1 Why the previous methodology was wrong

Until this revision every build-wise count keyed on `fixVersion`. That was **incorrect**, and the error changes conclusions rather than decimal places:

| Measured on the same 20 versions | By `fixVersion` | By `Affected Milestone` |
| --- | ---: | --- |
| Client tickets placed on the build line | 1,384 | **2,010** (+45%) |
| Tickets the other field cannot see | 38 carry a fix version and no Affected Milestone | **1,369** carry an Affected Milestone and *no fix version at all* — structurally invisible to the old query |
| Heaviest build | `base` (262) | `HF6` (399) and `HF1` (388) — `base` is only 69 |
| The two newest released-line builds HF12 / HF13 | 55 / 27 | **3 / 2** — almost nothing has been *reported against* them yet |

The last row is the one that matters operationally. Under the old methodology the current build `HF13` appeared to carry **27 client tickets**; that figure was *27 fixes scheduled into HF13*, and it was being read as *27 client problems found in HF13*. The Affected-Milestone count for HF13 is **2**.

*The `fixVersion` figures in the table above are quoted from the superseded revision of this report, which enumerated that basis directly. They are **not** the `Fixed here (same pop.)` column in §2 — that column re-counts the Affected-Milestone population by fix version and is a different, smaller set by construction.*

The root cause is recorded so it cannot be repeated. The previous revision checked the **native** `affectedVersion` field, measured it at 0% project-wide, and concluded that no field records the build a client was on — then recovered the fact from build tokens clients had typed into ticket titles. PAMIT does record it, in a custom field, on 97% of the population. §7 is the cost of that miss: **9** escaped defects found by the title heuristic against **367** measured from the field.

### 0.2 The `Milestone` fields — all of them, measured

⚠ **Three fields in this Jira instance are named `Affected Milestone`-something and two of them are empty on PAMIT.** Selecting one of those returns an empty build line, which reads as a clean result rather than as a wrong query — so the whole set is recorded here.

| Field | Name as shown in Jira | On the PAMIT client population | Verdict |
| --- | --- | ---: | --- |
| `customfield_10092` | `Affected Milestone.` *(trailing period)* | **1,346 / 1,384 — 97.3%** | ✅ **the axis** |
| `customfield_10214` | `Affected Milestone` | 0 / 1,384 | ⛔ not on the PAMIT screen |
| `customfield_10219` | `Affected Milestone` | 0 / 1,384 | ⛔ not on the PAMIT screen |
| `customfield_10143` · `customfield_10174` | `Custom Affected Milestone (**Only use if …)` | 0 / 1,384 | ⛔ free-text escape hatch, unused |
| `versions` | `Affects versions` *(native)* | 0 / 1,384 | ⛔ unused project-wide — **this is the field the old analysis checked** |
| `customfield_10100` | `Release Milestone.` | 9% | ⛔ legacy — values are unrelated old lines (`35.8.13 HF 7`, `4.8.5.0_U16SP2_B35.8.21`), all singletons |
| `customfield_10238` | `Forward Merge Milestone` | 63% | ⛔ **344 of 388 values are the literal string `None`** — no signal |
| `customfield_10131` · `10221` · `10223` | `Release Milestone` · `PAM_Release Milestone` · `CI_Release_Milestone` | 0% | ⛔ unused |

**Conclusion on `Milestone`: PAMIT has no usable `Milestone` axis.** The only two build fields carrying data are `Affected Milestone` (found) and `Fix versions` (fixed). Every build-wise count in this report keys on the first; the second appears only as the second axis of escape latency.

### 0.3 Multi-value and out-of-family handling

`Affected Milestone` is a multiselect. Measured on the 2,010-ticket population: **1,955** tickets carry one value, **49** carry two, **6** carry three or more, and **41** carry a value from a different build line alongside an in-family one. Three rules, applied consistently:

- **A ticket is attributed to the *earliest* in-family build it names.** A defect reported against both HF5 and HF9 escaped from HF5. Crediting HF9 would blame the later build for an inherited defect and understate the escape gap.
- **Out-of-family values are reported, never silently dropped.** A ticket affecting `35.8.28` and `35.8.29 HF6` sits on the HF6 row, and its other value travels with it into the workbook.
- **Per-build counts sum above the ticket total** where one ticket names two in-family builds. The de-duplicated ticket total is the population figure, and it is the one quoted as the denominator.

## 1. Release-date context

**Current build:** `35.8.29 HF13` — owner-stated. **Previous:** `35.8.29 HF12`.

> ⚠️ Jira `releaseDate` is a planned date, not confirmed client availability. In this project it is non-monotonic against build number and none of the in-flight builds is flagged released, so ordering and grouping use the build/fix version, never the date.

| Build | Jira release date | Flagged released | Client tickets | Defects | First client ticket | Latest client ticket |
| --- | --- | --- | ---: | ---: | --- | --- |
| `35.8.29 HF12` | 2026-07-31 | **no** | 3 | 3 | 2026-06-11 | 2026-07-29 |
| `35.8.29 HF13` ← current | 2026-06-22 | **no** | 2 | 1 | 2026-08-12 | 2026-08-24 |

The `releaseDate` values are **not** in build order (`HF12` 2026-07-31 vs `HF13` 2026-06-22), which is why every table below is ordered by build number and the date is reported as context only.

## 2. The whole build line

| Build | Jira release date | Rel. | Found (AM) | Fixed here (same pop.) | Defects | SS | Clients | Reg. stated | Reg. confirmed | Reopen=Yes | First ticket | Latest ticket | Top module | Top named category | Uncat. |
| --- | --- | :-: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | ---: |
| `base` | 2025-10-18 | ✅ | 69 | 9 | 44 | 17 | 30 | 0 | 0 | 0 | 2025-08-06 | 2026-04-23 | ACMO | Session Recording & Audit Ev | 36.4% |
| `HF1` | 2025-11-10 | ✅ | 388 | 23 | 293 | 72 | 61 | 27 | 13 | 2 | 2025-09-23 | 2026-09-02 | Connector | Third-Party Tool & Platform  | 20.5% |
| `HF2` | 2025-11-26 | ✅ | 293 | 39 | 217 | 81 | 48 | 19 | 7 | 5 | 2025-09-23 | 2026-08-28 | Connector | Reporting & Scheduling | 24.9% |
| `HF3` | 2026-02-06 | ✅ | 89 | 30 | 75 | 20 | 27 | 7 | 2 | 1 | 2025-10-16 | 2026-08-11 | Connector | Third-Party Tool & Platform  | 25.3% |
| `HF4` | 2026-02-11 | ✅ | 46 | 43 | 34 | 10 | 6 | 0 | 0 | 0 | 2026-02-05 | 2026-07-01 | PAM API | API & Integration | 35.3% |
| `HF5` | 2026-03-05 | ✅ | 274 | 52 | 228 | 73 | 23 | 71 | 23 | 11 | 2025-09-02 | 2026-09-03 | Connector | Session Recording & Audit Ev | 27.6% |
| `HF6` | 2026-03-30 | ✅ | 404 | 89 | 284 | 92 | 46 | 102 | 41 | 12 | 2025-12-29 | 2026-09-03 | ACMO | Third-Party Tool & Platform  | 25.7% |
| `HF7` | 2026-03-05 | ✅ | 145 | 47 | 108 | 37 | 35 | 44 | 21 | 4 | 2025-12-09 | 2026-09-01 | Connector | Third-Party Tool & Platform  | 29.6% |
| `HF8` | 2026-05-20 | ✅ | 17 | 46 | 12 | 6 | 5 | 6 | 2 | 0 | 2026-05-06 | 2026-09-02 | All Modules | Session Recording & Audit Ev | 8.3% |
| `HF9` | 2026-05-25 | ✅ | 125 | 23 | 86 | 26 | 36 | 70 | 35 | 3 | 2024-10-21 | 2026-09-03 | Connector | Authentication & Identity In | 22.1% |
| `HF9 Patch1` | 2026-08-06 | ✅ | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | — | — | — |
| `HF9 P2` | 2026-09-25 | 🟡 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | — | — | — |
| `HF10` | 2026-07-07 | ✅ | 27 | 34 | 21 | 7 | 9 | 21 | 9 | 3 | 2026-04-27 | 2026-09-02 | Connector | Reporting & Scheduling | 38.1% |
| `HF11` | 2026-07-15 | ✅ | 172 | 32 | 130 | 36 | 44 | 156 | 108 | 7 | 2026-04-22 | 2026-09-03 | Server Manager | Third-Party Tool & Platform  | 23.8% |
| `HF11 P2` | 2026-08-21 | 🟡 | 0 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | — | — | — |
| `HF11 P3` | — | 🟡 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | — | — | — |
| `HF12` | 2026-07-31 | 🟡 | 3 | 49 | 3 | 0 | 2 | 3 | 0 | 0 | 2026-06-11 | 2026-07-29 | Connector | Access Control, Workflow & A | 0.0% |
| `HF13` **← current** | 2026-06-22 | 🟡 | 2 | 18 | 1 | 0 | 2 | 1 | 1 | 0 | 2026-08-12 | 2026-08-24 | Server Manager | Service & Asset Management ( | 0.0% |
| `HF14` | 2026-07-10 | 🟡 | 1 | 50 | 1 | 0 | 1 | 1 | 0 | 0 | 2026-08-12 | 2026-08-12 | Server Manager | Session Recording & Audit Ev | 0.0% |
| `HF15` | 2026-09-25 | 🟡 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | — | — | — |

*⛔ **`Found (AM)` is the build-wise count** — tickets whose `Affected Milestone` names this build, i.e. where the client **found** the defect (`D42`).*

*⚠ **`Fixed here (same pop.)` is not the old build line.** It counts tickets **within this same Affected-Milestone population** whose fix version names this build — so the two columns describe the same 2,010 tickets from both ends, which is what makes the found-vs-fixed divergence visible per row. It is **not** the standalone `fixVersion` population the superseded methodology used: that was a different 1,384-ticket set, and its figures are in §0.1, not in this column.*

*`Reg. stated` / `Reg. confirmed` / `Reopen=Yes` come from the three regression fields, which sit at ~25% population. `Reg. stated` **is** the denominator for `Reg. confirmed` — never the `Found (AM)` count.*

*`Uncat.` is the share of that build's defects the derived taxonomy could not name. It is a **coverage figure, not a finding**. It runs higher on the released builds for two measured reasons: the trend query fetches light records without the description fallback, and the taxonomy was derived from current-build tickets, so older vocabulary is under-covered.*

**Reported deliberately:** `HF9 P2`, `HF11 P2`, `HF11 P3`, `HF15` currently carries **zero** client tickets. An empty release is information; omitting the row would hide it.

## 3. Focus builds — overall summary

| Metric | Count | Percentage | Observation |
| --- | ---: | ---: | --- |
| Tickets on focus builds, all clients | 391 | — |  |
| **Client-raised** | **192** | 100% (base) | `Primary Client` is 100% populated; no ticket is lost to an empty field |
| Internal | 199 | 50.9% | Excluded |
| **Client-raised defects** | **120** | 62.5% | The defect denominator (`D38`) |
| Non-defects | 71 | 37.0% | Story / Task / Sub-task |
| `Duplicate`, held out | 1 | 0.5% | Same defect counted twice |
| In a multi-ticket repeat group | 47 | 39.2% | 23 group(s) |
| Cross-release lineage | 12 | 10.0% | Clone family spans 2+ hotfixes |
| Clone-tracked only | 52 | 43.3% | Workflow, **not** recurrence |
| One-time | 9 | 7.5% | No lineage, single report |
| Context tickets read outside the windows | 152 | — | Evidence only |

## 4. Module-wise — every module

| Module | Tickets | Percentage | Major pattern | Repeat frequency | Clients | SS |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| `Connector` | 37 | 30.8% | Third-Party Tool & Platform Compat | 5 group(s) | 25 | 12 |
| `Server Manager` | 26 | 21.7% | Service & Asset Management (CRUD/B | 6 group(s) | 8 | 5 |
| `ACMO` | 16 | 13.3% | Access Control, Workflow & Approva | 2 group(s) | 11 | 8 |
| `Password Vault` | 12 | 10.0% | Password & Credential Lifecycle | 4 group(s) | 6 | 1 |
| `Settings` | 11 | 9.2% | Input Validation & Error Handling | 4 group(s) | 5 | 3 |
| `Application & Audit Logs` | 6 | 5.0% | Session Recording & Audit Evidence | 1 group(s) | 2 | 0 |
| `Password` | 4 | 3.3% | Password & Credential Lifecycle | 1 group(s) | 3 | 3 |
| `All Modules` | 3 | 2.5% | Security Hardening & Exposure | — | 2 | 2 |
| `Arcon Service / Agent` | 3 | 2.5% | Password & Credential Lifecycle | 1 group(s) | 2 | 0 |
| `PAM API` | 2 | 1.7% | Session Lifecycle & Connectivity | — | 2 | 1 |
| `Access Control` | 2 | 1.7% | Input Validation & Error Handling | 1 group(s) | 1 | 0 |
| `User Discovery` | 2 | 1.7% | Service & Asset Management (CRUD/B | — | 2 | 0 |
| `SSO` | 2 | 1.7% | Authentication & Identity Integrat | — | 2 | 1 |
| `UAG` | 2 | 1.7% | Platform Services, Agent & Gateway | — | 2 | 1 |
| `Report / Dashboard` | 1 | 0.8% | Reporting & Scheduling | — | 1 | 0 |
| `VA` | 1 | 0.8% | Security Hardening & Exposure | — | 1 | 0 |
| `Auto onboarding` | 1 | 0.8% | Service & Asset Management (CRUD/B | — | 1 | 0 |
| `PYCLI` | 1 | 0.8% | Session Lifecycle & Connectivity | — | 1 | 1 |
| `AGW` | 1 | 0.8% | Session Recording & Audit Evidence | — | 1 | 0 |
| `Browser Plugin` | 1 | 0.8% | Authentication & Identity Integrat | — | 1 | 0 |
| `RTSM` | 1 | 0.8% | Session Recording & Audit Evidence | — | 1 | 1 |
| `Workflow` | 1 | 0.8% | Access Control, Workflow & Approva | — | 1 | 1 |

## 5. Issue category — every category

| Issue category | Count | Percentage | Clients | Modules | SS | Sample tickets |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Password & Credential Lifecycle | 18 | 15.0% | 6 | 5 | 5 | `PAMIT-42115` `PAMIT-42168` `PAMIT-42369` |
| Service & Asset Management (CRUD/Bulk) | 17 | 14.2% | 6 | 4 | 2 | `PAMIT-38793` `PAMIT-39917` `PAMIT-40505` |
| Session Recording & Audit Evidence | 17 | 14.2% | 11 | 7 | 4 | `PAMIT-41273` `PAMIT-41749` `PAMIT-41944` |
| Session Lifecycle & Connectivity | 12 | 10.0% | 9 | 8 | 6 | `PAMIT-39276` `PAMIT-40583` `PAMIT-41949` |
| Third-Party Tool & Platform Compatibility | 12 | 10.0% | 10 | 2 | 6 | `PAMIT-40903` `PAMIT-41274` `PAMIT-41958` |
| Access Control, Workflow & Approval | 11 | 9.2% | 8 | 5 | 3 | `PAMIT-41384` `PAMIT-42054` `PAMIT-42189` |
| Authentication & Identity Integration | 9 | 7.5% | 7 | 6 | 3 | `PAMIT-39984` `PAMIT-40770` `PAMIT-41129` |
| Input Validation & Error Handling | 8 | 6.7% | 3 | 5 | 1 | `PAMIT-39694` `PAMIT-39696` `PAMIT-42492` |
| Reporting & Scheduling | 4 | 3.3% | 3 | 4 | 0 | `PAMIT-26092` `PAMIT-42594` `PAMIT-42886` |
| Security Hardening & Exposure | 4 | 3.3% | 4 | 3 | 1 | `PAMIT-33981` `PAMIT-37067` `PAMIT-41055` |
| Platform Services, Agent & Gateway | 3 | 2.5% | 3 | 3 | 1 | `PAMIT-42059` `PAMIT-42514` `PAMIT-42895` |
| Performance & Responsiveness | 2 | 1.7% | 2 | 2 | 1 | `PAMIT-40271` `PAMIT-42623` |
| API & Integration | 1 | 0.8% | 1 | 1 | 0 | `PAMIT-42463` |
| Uncategorised | 1 | 0.8% | 1 | 1 | 0 | `PAMIT-42478` |
| UI Field & Control Defects | 1 | 0.8% | 1 | 1 | 0 | `PAMIT-42878` |

## 6. Recurring patterns — every qualifying group

| Pattern | Tickets | n | Modules | Clients | Release | Older linked | Classification |
| --- | --- | ---: | --- | --- | --- | ---: | --- |
| ITD-MC Delta Image Capture Issue Third-Party Connector (Mo | `PAMIT-42577` `PAMIT-42793` `PAMIT-43057` | 3 | `Application & Audit Logs`, `Connector` | ITD-MC | ? | 0 | repeated in scope; cross-module; release-specific (?) |
| P2 - ICICI Bank IPC Service Not Triggering Password Closur | `PAMIT-42115` `PAMIT-42942` | 2 | `Arcon Service / Agent` | ICICI Bank | ?/HF12 | 3 | repeated in scope; cross-release; config/environment-sensitive |
| ICICI Bank Bulk import failed with large values in paramet | `PAMIT-40505` `PAMIT-43186` | 2 | `Server Manager` | ICICI Bank | ?/HF12 | 2 | repeated in scope; cross-release; config/environment-sensitive |
| BM - Issue with dbeaver connection | `PAMIT-40903` `PAMIT-43013` | 2 | `Connector` | Bank Muscat | HF12/HF13 | 2 | repeated in scope; cross-release; client-reopened |
| Session Extension Workflow | `PAMIT-41384` `PAMIT-42677` | 2 | `Connector` | Catholic Syrian Bank | ?/HF12 | 2 | repeated in scope; cross-release; config/environment-sensitive |
| ICICI Bank U16SP2 Unable to Modify or Create Service Due t | `PAMIT-42754` `PAMIT-43182` | 2 | `Server Manager` | ICICI Bank | ?/HF12 | 2 | repeated in scope; cross-release |
| Kotak Bank New Modify Service Type Missing 26 Available Co | `PAMIT-43091` `PAMIT-43111` | 2 | `Connector` | Kotak Bank | ? | 2 | repeated in scope; release-specific (?); config/environment-sensitive |
| ICICI Bank U16SP2 VA Application accepts special character | `PAMIT-39696` `PAMIT-43191` | 2 | `Access Control`, `Password Vault` | ICICI Bank | ?/HF12 | 1 | repeated in scope; cross-module; cross-release |
| 29HF12 - ICICI Bank U16SP2 Error (System.OutOfMemoryExcept | `PAMIT-42369` `PAMIT-42917` | 2 | `Password Vault` | ICICI Bank | ?/HF12 | 1 | repeated in scope; cross-release |
| Renew Unexpected Script Detected error while updating sche | `PAMIT-42594` `PAMIT-42898` | 2 | `Settings` | Renew | ?/HF12 | 1 | repeated in scope; cross-release |
| DILIGENTA SLOC 29HF6 PASSWORD ROTATION/CHANGE NOT WORKING | `PAMIT-42931` `PAMIT-43084` | 2 | `Password` | Diligenta Limited | ?/HF13 | 1 | repeated in scope; cross-release; config/environment-sensitive |
| ICICI Bank U16SP2 Incorrect Password Update Behavior for A | `PAMIT-42941` `PAMIT-43178` | 2 | `Server Manager` | ICICI Bank | ?/HF12 | 1 | repeated in scope; cross-release |
| IIFL SSMS Studio not working Ver PAM Ver. 29_HF11 | `PAMIT-42988` `PAMIT-43030` | 2 | `Connector` | IIFL | ?/HF12 | 1 | repeated in scope; cross-release |
| ICICI Bank U16SP2 Unable to view service details when sele | `PAMIT-42999` `PAMIT-43175` | 2 | `Server Manager` | ICICI Bank | ?/HF12 | 1 | repeated in scope; cross-release; config/environment-sensitive; client-reopened |
| TCS CSP U16SP2 Unable to apply command profiler from Setti | `PAMIT-43207` `PAMIT-43209` | 2 | `Settings` | TCS Cyber Security | ?/HF12 | 1 | repeated in scope; cross-release; config/environment-sensitive |
| ICICI Bank U16SP2 Server Manager fails to launch from end- | `PAMIT-42689` `PAMIT-43183` | 2 | `ACMO` | ICICI Bank | ?/HF12 | 0 | repeated in scope; cross-release; config/environment-sensitive |
| Muscat - Thales HSM iintegration with PAM | `PAMIT-42711` `PAMIT-43007` | 2 | `Password Vault` | Bank Muscat | ?/HF13 | 0 | repeated in scope; cross-release; config/environment-sensitive |
| ICICI Bank U16SP2 Bulk Password Update Does Not Accept <DN | `PAMIT-42751` `PAMIT-42756` | 2 | `Server Manager` | ICICI Bank | ? | 0 | repeated in scope; release-specific (?); config/environment-sensitive |
| ICICI Bank U16SP2 Unable to Add or Edit Gateway Configurat | `PAMIT-42795` `PAMIT-43181` | 2 | `Settings` | ICICI Bank | ?/HF12 | 0 | repeated in scope; cross-release; config/environment-sensitive |
| ICICI BANK Unable to Modify Service Parameters from Server | `PAMIT-42920` `PAMIT-43179` | 2 | `Server Manager` | ICICI Bank | ?/HF12 | 0 | repeated in scope; cross-release; config/environment-sensitive; client-reopened |
| ICICI Bank User is unexpectedly logged out when clicking o | `PAMIT-42977` `PAMIT-43176` | 2 | `ACMO` | ICICI Bank | ?/HF12 | 0 | repeated in scope; cross-release; config/environment-sensitive |
| ICICI BANK VPC Service issue | `PAMIT-43154` `PAMIT-43224` | 2 | `Password Vault` | ICICI Bank | ?/HF13 | 0 | repeated in scope; cross-release |
| UNABLE TO SCHEDULE IDLE USERS REPORT | `PAMIT-43295` `PAMIT-43403` | 2 | `Settings` | PSS | ?/HF13 | 0 | repeated in scope; cross-release; config/environment-sensitive |
| Mashreq Bank Issue with User Discovery Functionality – Dup | `PAMIT-41302` | 1 | `User Discovery` | MashreqBank | HF12 | 3 | cross-release lineage; release-specific (HF12) |
| Paytm Payments PYCLI ssh not working | `PAMIT-39276` | 1 | `ACMO`, `PAM API` | Paytm Payment Services Ltd - PPSL | ? | 2 | cross-release lineage; cross-module; release-specific (?); config/environment-sensitive |
| ICICI Bank Child Services Missing in Rotate Tab API Change | `PAMIT-42168` | 1 | `PAM API` | ICICI Bank | HF12 | 2 | cross-release lineage; release-specific (HF12) |
| Kotak Bank New Import Server Connection Validation Restric | `PAMIT-42492` | 1 | `Server Manager` | Kotak Bank | ? | 2 | cross-release lineage; release-specific (?); client-reopened |
| Kotak Bank New Issue with Bulk User Service Mapping for In | `PAMIT-42528` | 1 | `Server Manager` | Kotak Bank | ? | 2 | cross-release lineage; release-specific (?) |
| Kotak Bank New Server Manger performance issue. | `PAMIT-42623` | 1 | `Server Manager` | Kotak Bank | ? | 2 | cross-release lineage; release-specific (?) |
| CCIL Envelope Module Displays 500 Internal Server Error U1 | `PAMIT-42886` | 1 | `Password`, `Password Vault` | CCIL | ? | 2 | cross-release lineage; cross-module; release-specific (?); config/environment-sensitive |
| Video logs issue with web gateway | `PAMIT-42889` | 1 | `All Modules` | Bank Muscat | HF12 | 2 | cross-release lineage; release-specific (HF12); config/environment-sensitive |
| ICICI Bank U16SP2 Dormant User Report | `PAMIT-26092` | 1 | `Report / Dashboard` | ICICI Bank | ? | 1 | cross-release lineage; release-specific (?) |
| ICICI Bank Facing slowness issue on RA instances | `PAMIT-40271` | 1 | `ACMO` | ICICI Bank | ? | 1 | cross-release lineage; release-specific (?); config/environment-sensitive |
| BM - issue with SIEM logs | `PAMIT-42946` | 1 | `Application & Audit Logs` | Bank Muscat | HF13 | 1 | cross-release lineage; release-specific (HF13) |
| BM - Unable to access (one time and time based) service th | `PAMIT-43020` | 1 | `ACMO`, `Workflow` | Bank Muscat | HF12 | 1 | cross-release lineage; cross-module; release-specific (HF12); config/environment-sensitive |

## 7. Escape latency — found-on build vs fixed-in build

### 7.1 The census

*`Affected Milestone` says which build the client was running; `fixVersion` says which build the fix shipped in. The gap is how many hotfixes the defect survived undetected. Both are fields, so this is a **census over the tickets carrying both**, not a sample.*

| Measure | Tickets | Note |
| --- | ---: | --- |
| Carry an in-family `Affected Milestone` **and** an in-family `fixVersion` | **492** | the population this section can measure |
| **Escaped** — fixed in a *later* hotfix than reported against | **367** | the finding |
| Reported and fixed in the same hotfix | 122 | caught within the release — no escape |
| Fix version *earlier* than the affected build | 3 | data anomaly, not an escape — listed in the workbook for correction |

⛔ **The previous revision reported 9 rows here.** It recovered the found-on build from build tokens clients had typed into ticket titles, which fired on 9 tickets and was labelled *"a floor, not a census"*. The field gives 367 — 41x the sample. Where both methods fire they agree (`PAMIT-41274`: found HF1, fixed HF12, +11 on each), so the heuristic was accurate and simply blind.

**Hotfix-gap distribution** — how many releases each defect survived:

| Hotfixes late | Defects | Reading |
| ---: | ---: | --- |
| **0** (same release) | 122 | caught before shipping onward |
| **+1** | 51 | one release missed |
| **+2** | 83 | survived 2 releases undetected |
| **+3** | 67 | survived 3 releases undetected |
| **+4** | 47 | survived 4 releases undetected |
| **+5** | 42 | survived 5 releases undetected |
| **+6** | 28 | survived 6 releases undetected |
| **+7** | 20 | survived 7 releases undetected |
| **+8** | 9 | survived 8 releases undetected |
| **+9** | 15 | survived 9 releases undetected |
| **+10** | 1 | survived 10 releases undetected |
| **+11** | 4 | survived 11 releases undetected |

**Worst escapes** — every row is traceable in the workbook `Escape Latency` sheet:

| Ticket | Client | Module | Category | Priority | Found on | Fixed in | Late | Regression signal | Title |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| `PAMIT-39276` | Paytm Payment Services Ltd - PPSL | `ACMO` | Session Lifecycle & Conn | ShowStopper | 35.8.29 HF3 | HF14 | +11 | unstated | Paytm Payments PYCLI ssh not working |
| `PAMIT-41274` | Piramal Finance | `Connector` | Third-Party Tool & Platf | High | 35.8.29 HF1 | HF12 | +11 | unstated | Piramal Finance U16 SP2 SSH MYSQL service not ac |
| `PAMIT-41949` | IIBX | `Connector` | Session Lifecycle & Conn | High | 35.8.29 HF1 | HF12 | +11 | not-a-regression | IIBX getting all connectors logged out after som |
| `PAMIT-43035` | NSDL | `Connector` | Uncategorised | High | 35.8.29 HF3 | HF14 | +11 | not-a-regression | NSDL PB Service Access Issue U16SP235.8.29HF3 |
| `PAMIT-41588` | TATA Motors CV,PV | `Connector` | Session Lifecycle & Conn | High | 35.8.29 HF1 | HF11 | +10 | unstated | TATA MOTORS CV-PV Issue with Image Size Despite  |
| `PAMIT-37134` | MashreqBank | `Password Vault` | Password & Credential Li | High | 35.8.29 HF1 | HF10 | +9 | unstated | Mashreq Password change not successful through R |
| `PAMIT-37411` | Star Health & Allied Insurance Company Limited | `Server Manager` | Performance & Responsive | High | 35.8.29 HF1 | HF10 | +9 | unstated | Star Health Slowness in Command Profile |
| `PAMIT-39917` | ICICI Bank | `User Discovery` | Service & Asset Manageme | High | 35.8.29 HF5 | HF14 | +9 | unstated | ICICI Bank U16SP2 Error during User Discovery |
| `PAMIT-40772` | Piramal Finance | `Report / Dashboard` | Reporting & Scheduling | High | 35.8.29 HF1 | HF10 | +9 | unstated | Piramal Finance U16 SP2 Duplicate Entries of Use |
| `PAMIT-41015` | ERNET | `Administrative Console` | Session Lifecycle & Conn | High | 35.8.29 HF1 | HF10 | +9 | unstated | ERNET Command restriction is not working |
| `PAMIT-41141` | Star Health & Allied Insurance Company Limited | `Connector` | Third-Party Tool & Platf | High | 35.8.29 HF1 | HF10 | +9 | unstated | Star Health .29HF1 Issue while accessing MySql W |
| `PAMIT-41363` | SBI Life Insurance co Ltd | `Connector` | Session Lifecycle & Conn | High | 35.8.29 HF2 | HF11 | +9 | unstated | SBI LIFE - U16 SP2 - SFTP FILE TRANSFER DOWNLOAD |
| `PAMIT-41389` | Kotak Bank | `Server Manager` | Service & Asset Manageme | High | 35.8.29 HF5 | HF14 | +9 | unstated | Kotak Bank - U16 SP2 Issue with Auto-Mapping Fea |
| `PAMIT-41749` | Kotak Bank | `Server Manager` | Session Recording & Audi | High | 35.8.29 HF5 | HF14 | +9 | unstated | Kotak Bank New Inconsistent Audit Log Entries fo |
| `PAMIT-42492` | Kotak Bank | `Server Manager` | Input Validation & Error | Medium | 35.8.29 HF5 | HF14 | +9 | not-a-regression | Kotak Bank New Import Server Connection Validati |
| `PAMIT-42528` | Kotak Bank | `Server Manager` | Uncategorised | High | 35.8.29 HF5 | HF14 | +9 | not-a-regression | Kotak Bank New Issue with Bulk User Service Mapp |
| `PAMIT-42623` | Kotak Bank | `Server Manager` | Performance & Responsive | High | 35.8.29 HF5 | HF14 | +9 | confirmed-regression | Kotak Bank New Server Manger performance issue. |
| `PAMIT-42884` | Royal Hashemite Court, Jordan | `RTSM` | Session Recording & Audi | ShowStopper | 35.8.29 HF5 | HF14 | +9 | not-a-regression | RHC U16 SP2 ThickClient terminates while closing |
| `PAMIT-43091` | Kotak Bank | `Connector` | Service & Asset Manageme | High | 35.8.29 HF5 | HF14 | +9 | confirmed-regression | Kotak Bank New Modify Service Type Missing 26 Av |
| `PAMIT-43111` | Kotak Bank | `Connector` | Service & Asset Manageme | High | 35.8.29 HF5 | HF14 | +9 | confirmed-regression | Kotak Bank New Modify Service Type Missing 26 Av |
| `PAMIT-39984` | ICICI Bank | `ACMO` | Authentication & Identit | ShowStopper | 35.8.29 HF6 | HF14 | +8 | unstated | ICICI Bank U16SP2 SSH SSO via RA fails when SSH  |
| `PAMIT-40124` | State Bank of Mauritius (India) | `Password` | Password & Credential Li | High | 35.8.29 HF1 | HF9 | +8 | unstated | State Bank of Mauritius (India) U16 SP2 Getting  |
| `PAMIT-40344` | Royal Hashemite Court, Jordan | `ACMO` | Session Recording & Audi | ShowStopper | 35.8.29 | HF8 | +8 | unstated | RHC U16 SP2 B. Filter Button On Session Monitori |
| `PAMIT-40556` | Star Health & Allied Insurance Company Limited | `Connector` | Third-Party Tool & Platf | High | 35.8.29 HF1 | HF9 | +8 | unstated | Star Health Connection history showing while acc |
| `PAMIT-40876` | Indian Bank Ltd | `Connector` | Platform Services, Agent | High | 35.8.29 HF2 | HF10 | +8 | unstated | Indian Bank Request for Restrict Multiple Tab Ac |

*25 of 367 shown. All 367 are in the workbook — §15 states the traceability rule.*

### 7.2 Regression signal — the three client-facing fields

*The owner asked for `Is reopen from customer`, `Functionality working in previous version` and `Previous working version` to be brought into the analysis. All three exist; all three are select fields. The first was already captured but never used in a view, the other two are new here.*

| Field | ID | Populated on the build line | What it means | How it is used |
| --- | --- | ---: | --- | --- |
| `Is reopen from customer` | `customfield_10780` | 534 / 2040 | The customer re-opened the ticket after a delivered fix. A `Yes` is a **failed fix**, not a new defect | Escalates the weak spot that produced it; already used as a `client-reopened` tag on recurring groups |
| `Functionality working in previous version` | `customfield_11253` | 521 / 2040 | `Yes` = the feature worked before, so the defect is a **regression**. `No` = pre-existing or never worked | The regression gate. `Yes` promotes a ticket into the regression population |
| `Previous working version` | `customfield_11254` | 377 / 2040 *(naming a real version)* | The last build where it worked. Bounds the breakage to the interval `(previous working, affected milestone]` | Turns a regression into a **bisect range** — the actionable form for a developer |

⛔ **The three regression fields are populated on ~25% of the build line, so every regression figure is quoted over the **populated subset** with that subset's size beside it, never over the full population. An `unstated` ticket is not evidence of 'no regression' — it is evidence of an unfilled field, and the two must never be merged.**

⚠ **`Previous working version` is a select field whose option list includes the literal string `None`.** That is a real value meaning *there is no previously working version* — not an empty field. 491 tickets carry something, of which **130 carry `None`**, so the figure above counts the 361 that name an actual version. Counting `None` as populated overstates coverage; treating it as a version corrupts every bisect range, because `None` has no position in the build order.

| Regression class | Tickets | Share of *stated* | Meaning |
| --- | ---: | ---: | --- |
| `unstated` | 1512 | — | None of the three fields is populated |
| `confirmed-regression` | 262 | 49.6% | Worked in a previous version and that version is named |
| `not-a-regression` | 236 | 44.7% | Did not work in the previous version — pre-existing or new feature gap |
| `likely-regression` | 23 | 4.4% | Worked in a previous version; the version is not named |
| `customer-reopen` | 7 | 1.3% | Reopened by the customer, regression status not stated |

**528 of 2040 tickets (25.9%) state a regression signal at all**, and of those **262 (49.6% of stated)** are confirmed regressions with a named previous working version. **48** tickets are customer re-opens.

**Where confirmed regressions were last working** — the build that broke is the one *after* this:

| Previous working version | Confirmed regressions |
| --- | ---: |
| `35.8.29 HF6` | 44 |
| `35.8.29 HF1` | 24 |
| `35.8.29 HF5` | 17 |
| `35.8.29 HF7` | 15 |
| `35.8.29 HF9` | 13 |
| `35.8.29 HF10` | 12 |
| `35.8.24` | 11 |
| `4.8.5.0_U16SP2_B35.8.23` | 11 |
| `35.8.29 HF2` | 8 |
| `4.8.5.0_U16SP2_B35.8.16` | 7 |
| `35.8.28` | 7 |
| `35.8.29 HF3` | 6 |

**Confirmed regressions by testing area** — a regression is a *coverage* failure by definition: the feature worked, so a test that existed and ran would have caught it.

⚠ **`«unmapped»` is the largest row and that is a measurement limit, not a finding.** The build line is fetched with light records to keep 2,010 tickets affordable, so it carries no `description` — and the testing-area axis matches on title **plus** description. On the build line it therefore runs on the title alone and maps fewer tickets. The area figures to quote are the ones in §11, which are computed over the three full-record pools. Read this table as *the relative shape of confirmed regressions*, not as area counts comparable with §11.

| Testing area | Confirmed regressions |
| --- | ---: |
| «unmapped» | 107 |
| Authentication / Authorization | 37 |
| Environment Compatibility | 30 |
| Third-Party Compatibility | 21 |
| Configuration | 13 |
| Boundary Testing | 13 |
| API / Integration | 12 |
| Session Recording | 12 |
| UI / Browser Compatibility | 11 |
| Negative Testing | 8 |
| Logging / Monitoring | 8 |
| Upgrade / Migration | 8 |

### 7.3 Root cause — Jira's own taxonomy, 81% populated

⛔ **This report previously stated that Jira held no root-cause categorisation. That was wrong, and wrong in the same way §0.1 was.** §13 read *"`Root Cause` … 0 / 376 … Jira holds no categorisation to cross-check it against"* — having measured `customfield_10113` (*Root Cause*, 0.2%) and `customfield_10199` (*Root cause*, 0.1%). Neither is the live field. **`customfield_10245` (*RCA*) is 81.1% populated** — 1655 of 2040 tickets — with a structured taxonomy of 33 values in 14 families. It is the most populated analytical field in the project and it had never been used.

**By family:**

| RCA family | Tickets | Share of stated | Reading |
| --- | ---: | ---: | --- |
| Code | 450 | 27.2% | product code |
| Environment | 373 | 22.5% | environment / deployment, not the product binary |
| Others | 311 | 18.8% | closed without a product change |
| Requests | 208 | 12.6% | **not a defect** — enhancement or information request |
| Analysis | 150 | 9.1% | **analysis / design / coverage failure** |
| Documentation | 91 | 5.5% | documentation, not code |
| Not a bug | 34 | 2.1% |  |
| Missing Code / DB Scripts | 22 | 1.3% |  |
| Insufficient Unit Test case | 5 | 0.3% |  |
| Deployment Issue | 3 | 0.2% |  |
| Miscommunication | 3 | 0.2% |  |
| Data Issue | 3 | 0.2% |  |
| Code not checked-in | 1 | 0.1% |  |
| Insufficient Data | 1 | 0.1% |  |

**Every RCA value:**

| RCA | Tickets | Class |
| --- | ---: | :-: |
| Code - Logic Issue | 303 | product-defect |
| Others - Resolved Issue | 229 | product-defect |
| Environment - Misconfiguration | 188 | product-defect |
| Analysis - Inadequate Technical Design | 113 | testing-failure |
| Requests - Enhancement | 104 | non-defect |
| Others - Working as expected | 82 | non-defect |
| Documentation - Administrator / User Guide | 73 | product-defect |
| Environment - 3rd Party compatibility | 67 | product-defect |
| Requests - APEM Tool | 64 | non-defect |
| Environment - Non replicated | 52 | testing-failure |
| Environment- Env unavailable | 48 | product-defect |
| Code - Packaging Issue | 34 | product-defect |
| Not a bug | 34 | non-defect |
| Code - Incorrect Standards | 28 | product-defect |
| Code - Performance Issue | 27 | product-defect |
| Requests - Information Request | 25 | non-defect |
| Code - Security Issue | 24 | product-defect |
| Missing Code / DB Scripts | 22 | product-defect |
| Analysis - Incomplete Requirement | 19 | testing-failure |
| Code - Code Merge | 19 | product-defect |
| Analysis - Inadequate Test Coverage | 18 | testing-failure |
| Documentation - Deployment Guide Inadequate | 18 | product-defect |
| Code - UI/UX Issue | 15 | product-defect |
| Requests - Script Request | 15 | non-defect |
| Environment - Network | 11 | product-defect |
| Insufficient Unit Test case | 5 | testing-failure |
| Environment - Resource Unavailability | 5 | product-defect |
| Deployment Issue | 3 | product-defect |
| Miscommunication | 3 | non-defect |
| Data Issue | 3 | product-defect |
| Environment - Hardware failure | 2 | product-defect |
| Code not checked-in | 1 | product-defect |
| Insufficient Data | 1 | product-defect |

Two consequences worth acting on:

- ⛔ **327 tickets are classified by the product team as *not a product defect*** — `Requests - Enhancement`, `Requests - Information Request`, `Requests - APEM Tool`, `Requests - Script Request`, `Others - Working as expected`, `Not a bug`, `Miscommunication`. A testing weak spot attributed to one of those is a **false finding**. ⚠ This is **reported, not silently applied**: the defect population stays keyed on issue type (`D38`), because re-cutting a denominator on a field that is 19% empty would be a worse error than the one it corrects. The workbook flags every such ticket so a reader can exclude them deliberately.
- ✅ **207 tickets name a testing or analysis failure as the root cause** — `Analysis - Inadequate Test Coverage`, `Insufficient Unit Test case`, `Analysis - Incomplete Requirement`, `Analysis - Inadequate Technical Design`, `Environment - Non replicated`. **This is the strongest evidence in the analysis for a testing gap**, because the product team recorded the cause — this report did not infer it.

**Why fixes failed** — `Reopen RCA`, populated on 149 tickets:

| Reopen RCA | Tickets | Reading |
| --- | ---: | --- |
| Code Fix | 48 | the fix itself was wrong |
| Dependency failure | 29 | an upstream component broke it |
| Audit | 25 |  |
| Hosting Issue | 22 | environment, not the fix |
| Tester Understanding | 17 | **a QA misunderstanding, not a product failure** |
| Data Issue | 8 |  |

`ReOpen Date` is set on **82** tickets, and `ReOpen Time Spent` totals **0 hours** of recorded rework across this population.

⚠ **507 tickets carry an RCA while the derived category axis could not name them.** Those are the clearest targets for improving the derived taxonomy, because an authored answer already exists to check against.

### 7.4 Regression facts Jira cannot supply

⛔ **Owner requirement: where a regression field or fact is not available in Jira, say so explicitly rather than leaving it ambiguous or inferring it.** The sentinel used throughout this report and the workbook is **`Info not available in JIRA`**. It is never replaced by a blank cell, a dash, or a derived guess.

| Question | Why it cannot be answered | Consequence |
| --- | --- | --- |
| Defect injection phase | `Phase` (`cf 10164`) exists but is 0% populated | Cannot say whether a defect was introduced in requirements, design, code or test. Deriving it from the RCA family would be an inference presented as a fact — `Code - *` is where the defect was *found in code*, not necessarily where it was *introduced* |
| Reopen count per ticket | `ReopenCount` (`cf 11018`) exists but is 0% | A reopen is visible as a boolean (`Is reopen from customer`, `ReOpen Date`), not as a count. 'Reopened three times' is not answerable |
| Regression test executed / suite name | no such field exists in PAMIT | Cannot link a defect to the test that should have caught it, so 'was this covered?' is answered by the derived testing-area axis, not by Jira |
| Requirement or user-story link | no requirement link field is populated | Scenario gaps cannot cite a requirement, which is why the gap provenance table marks requirements as NOT USED |
| Detected-by / found-in-testing stage | no such field exists in PAMIT | Every ticket in this population is client-raised by definition, so internal-vs-external detection ratio is not measurable here |

Fields that **exist in the Jira schema but are never populated**, so any value derived from them would be invented:

| Field | ID | Populated | Verdict |
| --- | --- | ---: | --- |
| Root Cause | `customfield_10113` | 5 (0.2%) | ⛔ Effectively empty — and this is the field whose emptiness was previously read as 'Jira holds no root-cause categorisation'. Use RCA (10245) |
| Root cause | `customfield_10199` | 3 (0.1%) | ⛔ Effectively empty. A second same-named decoy alongside 10113 |
| Hotfix Release Date | `customfield_10147` | 1 (0.0%) | ⛔ One value, dated 2022. Unusable |
| ReopenCount | `customfield_11018` | 0 (0.0%) | ⛔ EXISTS BUT IS NEVER POPULATED. A reopen count must be derived from ReOpen Date / Reopen RCA presence instead |
| Phase | `customfield_10164` | 0 (0.0%) | ⛔ EXISTS BUT IS NEVER POPULATED. Defect-injection phase (requirement / design / code / test) is therefore NOT ANSWERABLE from Jira |
| Module | `customfield_10065` | 0 (0.0%) | ⛔ Never populated |
| Category | `customfield_10051` | 0 (0.0%) | ⛔ Never populated |

**Every regression-shaped field measured, in population order:**

| Field | ID | Populated | Available | Role |
| --- | --- | ---: | :-: | --- |
| RCA | `customfield_10245` | 1622 (80.7%) | ✅ | Structured root-cause taxonomy — 33 values in 15 families. THE most populated analytical field in the project and previously unused |
| RCA Details (Impact Analysis) | `customfield_10567` | 1591 (79.2%) | ✅ | Free-text impact analysis behind the RCA value |
| Fixed Date | `customfield_10249` | 1026 (51.0%) | ✅ | When the fix was recorded — the second half of a fix-latency measure |
| Is reopen from customer | `customfield_10780` | 512 (25.5%) | ✅ | A Yes is a FAILED FIX, not a new defect |
| Functionality working in previous version | `customfield_11253` | 499 (24.8%) | ✅ | The regression gate |
| Previous working version | `customfield_11254` | 491 (24.4%) | ✅ | The last working build. 130 of these carry the literal string 'None', leaving 361 that name a real version |
| Reopen RCA details | `customfield_10600` | 152 (7.6%) | ✅ | Free text on why a reopen happened |
| Reopen RCA | `customfield_10741` | 147 (7.3%) | ✅ | Why the fix failed — Code Fix (48), Dependency failure (29), Audit (23), Hosting Issue (22), Tester Understanding (17), Data Issue (8) |
| Reopen Original Ticket ID | `customfield_10781` | 142 (7.1%) | ✅ | The original ticket a reopen descends from. ⚠️ 64 of 142 values are junk ('No', 'NONE', 'na') — see FIELD_SENTINELS |
| ReOpen Date | `customfield_10236` | 82 (4.1%) | ✅ | When the reopen happened |
| ReOpen Time Spent | `customfield_10235` | 72 (3.6%) | ✅ | Hours spent on the reopen — rework cost |
| RCA Category / Description updated? | `customfield_11353` | 25 (1.2%) | ✅ | RCA review hygiene flag. Too sparse for a rate |
| RCA Review Remarks | `customfield_11355` | 24 (1.2%) | ✅ | Reviewer commentary on the RCA. Too sparse for a rate |
| Affected QA Build | `customfield_10136` | 9 (0.4%) | ✅ | Near-empty; all nine read 'Build 35.8.29' |
| QA Build/Drop | `customfield_10150` | 9 (0.4%) | ✅ | Near-empty |
| Root Cause | `customfield_10113` | 5 (0.2%) | ⛔ | ⛔ Effectively empty — and this is the field whose emptiness was previously read as 'Jira holds no root-cause categorisation'. Use RCA (10245) |
| Root cause | `customfield_10199` | 3 (0.1%) | ⛔ | ⛔ Effectively empty. A second same-named decoy alongside 10113 |
| Hotfix Release Date | `customfield_10147` | 1 (0.0%) | ⛔ | ⛔ One value, dated 2022. Unusable |
| ReopenCount | `customfield_11018` | 0 (0.0%) | ⛔ | ⛔ EXISTS BUT IS NEVER POPULATED. A reopen count must be derived from ReOpen Date / Reopen RCA presence instead |
| Phase | `customfield_10164` | 0 (0.0%) | ⛔ | ⛔ EXISTS BUT IS NEVER POPULATED. Defect-injection phase (requirement / design / code / test) is therefore NOT ANSWERABLE from Jira |
| Module | `customfield_10065` | 0 (0.0%) | ⛔ | ⛔ Never populated |
| Category | `customfield_10051` | 0 (0.0%) | ⛔ | ⛔ Never populated |

⚠ **These fields do not change any count in §§2–12.** They classify tickets already in the population; they never add or remove one. Nothing in the build-wise, module, category or weak-spot analysis needed restating because of them — the restatement in this revision comes entirely from the `fixVersion` → `Affected Milestone` axis change (§0.1).

## 8. Client concentration

| Client | Tickets | % of client base | of which defects | Modules touched | Dominant category |
| --- | ---: | ---: | ---: | ---: | --- |
| ICICI Bank | 50 | 26.0% | 36 | 14 | Password & Credential Lifecycl |
| Kotak Bank | 22 | 11.5% | 10 | 7 | Session Recording & Audit Evid |
| ITD-MC | 14 | 7.3% | 10 | 7 | Authentication & Identity Inte |
| Bank Muscat | 11 | 5.7% | 9 | 9 | Password & Credential Lifecycl |
| Canara Bank | 6 | 3.1% | 3 | 5 | Third-Party Tool & Platform Co |
| TCS Cyber Security | 5 | 2.6% | 5 | 3 | Access Control, Workflow & App |
| MashreqBank | 4 | 2.1% | 3 | 4 | Password & Credential Lifecycl |
| Renew | 3 | 1.6% | 2 | 2 | Reporting & Scheduling |
| IIFL | 3 | 1.6% | 3 | 2 | Third-Party Tool & Platform Co |
| Edelweiss | 2 | 1.0% | 1 | 2 | Access Control, Workflow & App |
| Bangladesh Election Commission | 2 | 1.0% | 0 | 1 | Connector Development & New In |
| Ujjivan Financial Services | 2 | 1.0% | 1 | 1 | Session Lifecycle & Connectivi |
| HDB Financial Services Limited | 2 | 1.0% | 1 | 2 | Access Control, Workflow & App |
| IDFC | 2 | 1.0% | 1 | 3 | Access Control, Workflow & App |
| Banque Libano-Française(Lebanon) | 2 | 1.0% | 0 | 1 | Service & Asset Management (CR |

## 9. Last 30 days — the current client picture

*Basis: 409 client tickets created since 2026-08-04, any fix version, any status.*

| Issue / pattern | Count | Modules | First reported | Latest reported | Current status | Version state | Commonest state |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| Third-Party Tool & Platform Compatibility | 48 | ACMO, AGW, Connector | 2026-08-05 | 2026-08-31 | 31 open / 48 | 40 unversioned | Closed |
| Password & Credential Lifecycle | 29 | ACMO, All Modules, Arcon Service / Agent | 2026-08-05 | 2026-09-02 | 23 open / 29 | 16 unversioned | Awaiting Response |
| Session Recording & Audit Evidence | 29 | ACMO, AGW, All Modules | 2026-08-05 | 2026-09-02 | 24 open / 29 | 22 unversioned | Awaiting Response |
| Service & Asset Management (CRUD/Bulk) | 24 | ACMO, AGW, Connector | 2026-08-05 | 2026-09-02 | 12 open / 24 | 14 unversioned | Closed |
| Reporting & Scheduling | 22 | ACMO, AGW, Arcon Service / Agent | 2026-08-05 | 2026-09-03 | 18 open / 22 | 19 unversioned | Awaiting Response |
| Uncategorised | 20 | ACMO, AGW, Arcon Service / Agent | 2026-08-06 | 2026-09-02 | 14 open / 20 | 18 unversioned | Awaiting Response |
| Access Control, Workflow & Approval | 20 | ACMO, Connector, Mobile Application | 2026-08-07 | 2026-09-01 | 15 open / 20 | 14 unversioned | Development Analys |
| Vulnerability Assessment (VA / VAPT) | 19 | ACMO, All Modules, VA | 2026-08-05 | 2026-09-01 | 13 open / 19 | 19 unversioned | Open |
| Session Lifecycle & Connectivity | 16 | ACMO, AGW, All Modules | 2026-08-04 | 2026-09-02 | 10 open / 16 | 11 unversioned | Closed |
| Input Validation & Error Handling | 16 | ACMO, Access Control, Arcon Service / Agent | 2026-08-04 | 2026-09-02 | 12 open / 16 | 12 unversioned | Development Analys |
| Authentication & Identity Integration | 16 | ACMO, AGW, Application & Audit Logs | 2026-08-07 | 2026-09-03 | 9 open / 16 | 14 unversioned | Closed |
| Performance & Responsiveness | 11 | ACMO, All Modules, Connector | 2026-08-05 | 2026-09-02 | 9 open / 11 | 11 unversioned | Awaiting Response |
| Platform Services, Agent & Gateway | 10 | AGW, Connector, UAG | 2026-08-05 | 2026-08-31 | 8 open / 10 | 9 unversioned | Awaiting Response |
| Security Hardening & Exposure | 6 | All Modules, Arcon Service / Agent, Research | 2026-08-05 | 2026-09-02 | 4 open / 6 | 6 unversioned | Closed |
| UI Field & Control Defects | 3 | Connector, Server Manager, UI | 2026-08-05 | 2026-09-02 | 3 open / 3 | 2 unversioned | Development Analys |
| API & Integration | 3 | Arcon Service / Agent, PAM API, Password | 2026-08-12 | 2026-08-28 | 2 open / 3 | 2 unversioned | Awaiting Response |
| LOB / Organisation Mapping | 2 | Server Manager | 2026-08-06 | 2026-08-12 | 0 open / 2 | 2 unversioned | Closed |
| Log Viewing & Audit Reports | 1 | Connector | 2026-08-10 | 2026-08-10 | 0 open / 1 | 1 unversioned | Closed |

**Module split (30-day defects):**

| Module | Tickets | Percentage | Major pattern | Repeat frequency | Clients | SS |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| `Connector` | 78 | 26.4% | Third-Party Tool & Platform Compat | — | 53 | 19 |
| `Server Manager` | 53 | 18.0% | Service & Asset Management (CRUD/B | — | 31 | 22 |
| `ACMO` | 41 | 13.9% | Access Control, Workflow & Approva | — | 30 | 17 |
| `Password Vault` | 25 | 8.5% | Password & Credential Lifecycle | — | 16 | 10 |
| `VA` | 17 | 5.8% | Vulnerability Assessment (VA / VAP | — | 15 | 4 |
| `All Modules` | 15 | 5.1% | Vulnerability Assessment (VA / VAP | — | 14 | 7 |
| `AGW` | 14 | 4.7% | Platform Services, Agent & Gateway | — | 10 | 4 |
| `Arcon Service / Agent` | 12 | 4.1% | Session Recording & Audit Evidence | — | 10 | 6 |
| `Report / Dashboard` | 12 | 4.1% | Reporting & Scheduling | — | 10 | 2 |
| `Settings` | 11 | 3.7% | Access Control, Workflow & Approva | — | 7 | 7 |

## 10. Query C — 167 open client defects with no fix version

*These are structurally invisible to any release-scoped query: nothing has scheduled them into a build. Own denominator throughout.*

| Cut | Breakdown |
| --- | --- |
| By module | `Connector` 40 · `ACMO` 27 · `Server Manager` 25 · `VA` 13 · `Report / Dashboard` 11 · `All Modules` 10 · `Password Vault` 10 · `AGW` 9 · `Arcon Service / Agent` 8 · `Workflow` 6 |
| By category | Third-Party Tool & Platform Compatibility 27 · Session Recording & Audit Evidence 18 · Reporting & Scheduling 17 · Password & Credential Lifecycle 14 · Vulnerability Assessment (VA / VAPT) 13 · Uncategorised 12 · Access Control, Workflow & Approval 12 · Input Validation & Error Handling 9 |
| By priority | High 89 · ShowStopper 66 · Medium 6 · Low 6 |
| By status | Awaiting Response 85 · Development Analysis 31 · Open 24 · Awaiting Session 13 · Under Observation (No Code Change) 9 · Patch Shared 3 · Business Analysis 2 |
| By client | ICICI Bank 7 · Indusind Bank Ltd 6 · ITD-MC 6 · Union Bank Of India 5 · Bharti Airtel 5 · Vodafone 4 · Kotak Bank 4 · Moro Hub 4 |
| Created span | 2026-08-04 → 2026-09-03 |

## 11. Testing weak spots — every area

| Testing area | Tickets | Share | Focus/30d/QC | Clients | Modules | ShowStopper | Shape | Gap identified | Priority | Confidence |
| --- | ---: | ---: | :-: | ---: | ---: | ---: | :-: | --- | :-: | --- |
| Authentication / Authorization | 103 | 28.4% | 15/36/52 | 60 | 20 | 31 (30%) | broad | Federated identity and privilege boundaries are not in the regression suite | **High** | measured |
| Environment Compatibility | 101 | 27.8% | 13/33/55 | 63 | 22 | 36 (36%) | broad | One reference environment; client OS/DB/deployment variants untested | **High** | measured |
| Configuration | 94 | 25.9% | 15/32/47 | 58 | 20 | 36 (38%) | broad | Configuration screens tested on defaults only | **High** | measured |
| Logging / Monitoring | 52 | 14.3% | 12/16/24 | 40 | 19 | 18 (35%) | narrow | Log content is not asserted, only that the action completed | Medium | measured |
| Session Recording | 46 | 12.7% | 11/14/21 | 33 | 9 | 15 (33%) | narrow | Recording asserted as session-opened, not as evidence-correct-and-retrievable | Medium | measured |
| UI / Browser Compatibility | 42 | 11.6% | 6/13/23 | 28 | 11 | 19 (45%) | acute | Single-browser UI coverage | **High** | measured |
| Boundary Testing | 41 | 11.3% | 9/15/17 | 21 | 10 | 17 (41%) | narrow | Field limits and bulk volumes are not exercised | Medium | measured |
| Third-Party Compatibility | 41 | 11.3% | 10/15/16 | 28 | 10 | 17 (41%) | narrow | No client-tool/OS version matrix in the regression suite | Medium | measured |
| Upgrade / Migration | 34 | 9.4% | 3/16/15 | 24 | 11 | 15 (44%) | narrow | No post-upgrade regression pass on an upgraded instance | Medium | measured |
| API / Integration | 28 | 7.7% | 6/8/14 | 21 | 12 | 7 (25%) | narrow | API assertions check transport, not application semantics | Medium | measured |
| Negative Testing | 26 | 7.2% | 5/9/12 | 22 | 11 | 9 (35%) | narrow | Invalid and unexpected input is under-tested; raw exceptions reach the user | Medium | measured |
| Workflow / Approval | 24 | 6.6% | 5/6/13 | 20 | 7 | 11 (46%) | acute | Approval paths tested on the happy path only | **High** | measured |
| Performance | 22 | 6.1% | 3/6/13 | 17 | 8 | 13 (59%) | acute | No load or endurance testing on the affected journeys | **High** | measured |
| Security | 21 | 5.8% | 5/5/11 | 18 | 11 | 6 (29%) | narrow | Security findings arrive from client audits rather than internal scans | Low | measured |
| Data Integrity / Consistency | 16 | 4.4% | 6/7/3 | 12 | 8 | 5 (31%) | narrow | Reads asserted for success, not for agreement with the source of truth | Low | measured |

*Share is of the 363 distinct tickets across all three pools. Areas are multi-label, so shares sum past 100% — a ticket that is both a boundary and a compatibility failure is counted in both, because both kinds of testing would have had to catch it.*

## 12. Test scenario gaps

| Observed client issue | Testing area | Evidence | Recommended scenario | Priority |
| --- | --- | --- | --- | :-: |
| Federated identity and privilege boundaries are not  | Authentication / Authorization | `PAMIT-26092` `PAMIT-39696` `PAMIT-39917` | SAML/Azure AD login, JIT provisioning, AD-bridging toggle, and a negative privilege test per role | **High** |
| One reference environment; client OS/DB/deployment v | Environment Compatibility | `PAMIT-38793` `PAMIT-39696` `PAMIT-39917` | Matrix the supported OS and deployment shapes for the affected journeys | **High** |
| Configuration screens tested on defaults only | Configuration | `PAMIT-39276` `PAMIT-39694` `PAMIT-39984` | Save and reload each configuration page, including duplicate-name and already-exists paths | **High** |
| Log content is not asserted, only that the action co | Logging / Monitoring | `PAMIT-37067` `PAMIT-39276` `PAMIT-39984` | Assert log presence, correctness and SIEM forwarding for each audited action | Medium |
| Recording asserted as session-opened, not as evidenc | Session Recording | `PAMIT-41055` `PAMIT-41273` `PAMIT-41274` | Per connector type: assert the artefact exists, plays, maps to the correct session, and displays the banner | Medium |
| Single-browser UI coverage | UI / Browser Compatibility | `PAMIT-41958` `PAMIT-41990` `PAMIT-42168` | Run the core journeys across the supported browser set and assert rendering, not just navigation | **High** |
| Field limits and bulk volumes are not exercised | Boundary Testing | `PAMIT-38793` `PAMIT-40505` `PAMIT-41389` | Oversized parameter values, bulk import/update at client volume, and min/max boundaries per field | Medium |
| No client-tool/OS version matrix in the regression s | Third-Party Compatibility | `PAMIT-39694` `PAMIT-40583` `PAMIT-40903` | Pin a supported matrix (DBeaver, WinSCP, SSMS, Chrome driver, RDP post-patch, HSM) and run the launch plus core journey per entry every hotfix | Medium |
| No post-upgrade regression pass on an upgraded insta | Upgrade / Migration | `PAMIT-40271` `PAMIT-42686` `PAMIT-42689` | Upgrade a seeded instance from N-2, then run the core journeys against the migrated data | Medium |
| API assertions check transport, not application sema | API / Integration | `PAMIT-42117` `PAMIT-42168` `PAMIT-42189` | Assert the application-level errorCode and payload semantics; never status==200 alone | Medium |
| Invalid and unexpected input is under-tested; raw ex | Negative Testing | `PAMIT-39694` `PAMIT-39696` `PAMIT-42492` | Negative matrix per input, asserting a product error code rather than a framework exception string | Medium |
| Approval paths tested on the happy path only | Workflow / Approval | `PAMIT-41384` `PAMIT-42054` `PAMIT-42189` | Time-based and one-time grants, delegation add/approve, revocation at expiry | **High** |
| No load or endurance testing on the affected journey | Performance | `PAMIT-40271` `PAMIT-42576` `PAMIT-42623` | Memory and endurance runs on vault load and bulk operations at client data volumes | **High** |
| Security findings arrive from client audits rather t | Security | `PAMIT-33981` `PAMIT-37067` `PAMIT-39696` | Add cipher/TLS posture, direct-object and unauthenticated-resource checks to the pre-release gate | Low |
| Reads asserted for success, not for agreement with t | Data Integrity / Consistency | `PAMIT-38793` `PAMIT-41302` `PAMIT-41749` | Cross-check list, report and counter values against the database after each mutating action | Low |

## 13. Data-quality limitations

*Each measured, not assumed. These bound what the analysis can claim.*

| Limitation | Measured | Consequence |
| --- | ---: | --- |
| ⛔ **`Root Cause` — THIS ROW WAS WRONG.** `Module`, `Category`, `Sub-Category` and `Product/Operational categorization` are genuinely unpopulated, but **`RCA` (`cf 10245`) is 80.7% populated** with a 33-value taxonomy | 0 for `cf 10113`/`10199` · **1,622 for `cf 10245`** | The previous wording — *"the whole taxonomy is derived from ticket text; Jira holds no categorisation to cross-check it against"* — measured two decoy fields and missed the live one. Jira **does** hold an authored root-cause classification, and §7.3 now uses it. The derived text taxonomy remains, with a cross-check it never had |
| **`affectedVersion` (native) unused — but `Affected Milestone` (`cf[10092]`) is not** | 0 native / **97.3%** custom | ⛔ **This row previously read "no field records the build a client was on" and was wrong.** The native field is empty; the custom field carries the fact on 97.3% of the population and is now the build axis (`D42`, §0) |
| `Severity` sparsely populated | 69 / 391 | `priority` (100%) is used for impact; severity-based views unavailable |
| `environment` and `resolution` never set | 0 / 391 | Environment classification leans on `Hosting Environment` (238/391) and title text |
| `Primary Client` holds alias duplicates | — | ICICI splits across two values (21 + 4); TCL Global and ITD-MC likewise. Merged by rule — unmerged, 'most affected client' is wrong |
| Clone-driven workflow displaces dates | — | Most focus-build summaries begin with `CLONE`, so `created` is when the clone was cut for the hotfix, not when the client reported. This is why the 30-day view exists as a separate population |
| Jira `releaseDate` is planned, and non-monotonic | — | HF13 2026-06-22 < HF14 2026-07-10 < HF11 2026-07-15 < HF12 2026-07-31, and no in-flight build is flagged released. Ordering uses build number |
| `/search/approximate-count` is inaccurate | 190 vs 201 | A 5.5% undercount on this population. Every figure here comes from full enumeration |
| `All Modules` used as a component | 54 / 391 | A non-answer for module attribution; those tickets cannot be assigned |
| Fix-version scope is a small slice of client reporting | 19,296 unversioned | Client tickets with no fix version, all time. Build-based analysis covers **fix-scheduled** defects, not everything clients report |

## 14. How this was produced

Read-only Jira enumeration through `tools/jira/jira_query.ReadOnlyJira`, which permits GET on a fixed path list plus POST to the two search endpoints and refuses everything else — 16 guard assertions cover it, including `GET /transitions`. Classification rules, client aliases and the testing-area axis are in `tools/jira/pamit_analysis_rules.py`; grouping is union-find over explicit clone links plus word-boundary title-signature similarity. Rendering is `tools/jira/pamit_report.py`.

```powershell
python tools\jira\pamit_client_analysis.py            # fetch, analyse, write
python tools\jira\pamit_client_analysis.py --no-write # analyse only
python tools\jira\pamit_client_analysis.py --offline  # zero HTTP, last capture
python tools\jira\pamit_workbook.py                   # build the workbook
python tools\jira\pamit_workbook.py --refetch         # re-query Jira first
```

## 15. Ticket-level traceability — no count without its tickets

**Owner ruling `D43`: every reported count must be traceable to the individual tickets behind it.** A total, a percentage and a summary are not an answer on their own — if the analysis says *Environment Compatibility: 101 tickets*, all 101 keys must be listed.

How that is enforced rather than promised:

| Mechanism | Where | What it guarantees |
| --- | --- | --- |
| **Sheet `04 Ticket Details`** | the workbook | One row per ticket in the union of every counted pool, with each pool and each testing area as a Yes/No column. **Filtering that sheet reproduces any reported figure exactly** — the count is a view over the data, not a separate assertion |
| **Sheet `09 Count Reconciliation`** | the workbook | Every headline count restated as a live `COUNTIFS` over sheet 04, beside the value this analysis computed, beside a `PASS`/`FAIL` comparison. **Excel recomputes it on open**, so the reader verifies the totals without trusting the generator |
| **`verify()` gate** | `tools/jira/pamit_workbook.py` | Reconciles every pool count and every area count against the ticket universe *before* the workbook is declared good, and exits non-zero on any mismatch. A figure that cannot be reproduced from its tickets fails the build instead of shipping |
| **`members` on every area row** | `pamit_client_analysis.py` | Each testing area carries **every** backing key, not a sample of six. The sample is still shown in §12 for readability; the full list is in the workbook |

⚠ **Two places where counts legitimately do not add up, and why.** Both are stated wherever the figure appears:

- **Per-build counts sum above the ticket total.** `Affected Milestone` is a multiselect and 55 tickets name two in-family builds. The de-duplicated ticket total is the population; the per-build sum is not.
- **Testing-area counts sum past 100%.** The area axis is multi-label — a defect that is both a boundary failure and a compatibility failure is a gap in both kinds of testing, so it is counted in both. Sheet 01 therefore has more rows than distinct tickets, and both figures are reported.

## 16. The consolidated workbook

**Owner ruling `D44`: one workbook, many worksheets.** All ticket-level detail lands in a single file and a new analysis area becomes a **new worksheet in it**, never a new `.xlsx`.

`artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx`

| Sheet | Holds | How its counts are verified |
| --- | --- | --- |
| `00 README` | Methodology, headline totals, sheet manifest, the rules the workbook obeys | — |
| `01 Testing Weak Spots` | **One row per ticket per weak spot** with the full 20-column JIRA-oriented structure: ticket, gap, description, module, build, severity, priority, impact, root cause, existing and missing coverage, precaution, solution, PAM-specific recommendation, suggested coverage, automation, evidence, JIRA link, status | Filter by *Testing Weak Spot* → row count equals the reported area count |
| `02 Weak Spot Summary` | One row per testing area with the same recommendation columns aggregated | *Tickets* column reconciles against sheet 01 and sheet 09 |
| `03 Test Scenario Gaps` | One row per gap with expected behaviour, existing and missing coverage, risk, **source of identification** and **derivation method** | *Related Ticket Number(s)* lists every backing key |
| `04 Ticket Details` | **The source data** — every ticket, every analysis field, every pool and area flag | Every other sheet's count is a filter over this one |
| `05 Build-wise` | Per build: found-count beside fixed-count, defects, ShowStoppers, regression signal | *Found here* reconciles via `COUNTIF` on sheet 04 |
| `06 Escape Latency` | Every ticket whose affected build precedes its fix build | One row per ticket; the gap is measured, not estimated |
| `07 Regression Signal` | The three client-facing fields per ticket, the derived class, and the bisect range | One row per ticket stating any signal |
| `08 Module & Category` | Module-wise and category-wise counts | Both reconcile via `COUNTIF` on sheet 04 |
| `09 Count Reconciliation` | **Every headline count beside a live `COUNTIFS` and a `PASS`/`FAIL`** | This sheet *is* the validation |
| `10 Field Audit` | Every milestone-shaped and regression-shaped field measured, with population and verdict | Explains why `cf[10092]` is the axis and the rest are not |

⛔ **Do not create a second file for a new analysis.** Add a `sheet_*` builder to `build()` in `tools/jira/pamit_workbook.py` and a matching row to the manifest in `sheet_readme()`, and the analysis becomes a worksheet here. ⚠ Those two are hand-kept in step — add the builder and forget the manifest row and sheet `00 README` will describe a workbook that is not the one on disk.

## 17. Methodology for the two derived axes

### 17.1 Testing weak spots

A weak spot is **derived, not authored**. Four ordered steps:

1. Every client ticket in the three full-record pools is matched against the testing-area axis in `pamit_analysis_rules.testing_areas()` — a **word-boundary** term match over title plus the first 1,500 characters of description, multi-label.
2. An area qualifies at **≥3 tickets from ≥2 distinct clients** (`confidence = measured`). One client's tickets are an incident, not a coverage gap. Areas below the threshold are reported as *insufficient evidence* rather than dropped.
3. Priority is **density-based, not volume-based**: High at ≥15% share, or ≥10 tickets with ≥45% ShowStopper. An absolute-count rule marked every area High, because ShowStopper is not rare in this data.
4. The gap statement and recommended scenario come from `AREA_GAP`; the root cause, existing and missing coverage, precaution, PAM-specific recommendation, suggested coverage and automation advice come from `AREA_DETAIL`. Both are keyed on the area, so a filtered view of sheet 01 is self-contained.

⛔ **Word boundaries are load-bearing.** Substring matching tagged *"Login with SAML"* as a **Logging** issue (`log` ⊂ `login`); the word-boundary fix then silently dropped plurals (`cipher` misses *ciphers*). Both are fixed and both are the kind of defect that produces a confident wrong answer.

### 17.2 Test scenario gaps — and where each one came from

Every gap names its **source of identification**, because a gap whose provenance cannot be traced is an opinion:

| Source of identification | Used? | Detail |
| --- | :-: | --- |
| **Client-raised JIRA tickets** (production / customer issues) | ✅ **primary** | The population itself, placed on builds by `Affected Milestone`. Every gap row carries its backing keys and the client count |
| **Previous build/version behaviour** | ✅ secondary | The three regression fields, where populated. A confirmed regression is the strongest possible evidence of a coverage gap: the feature demonstrably worked before |
| **Existing automation coverage** | ✅ tertiary | The bootstrap suite inventory — specifically the gap between what the framework *can* do (20 environment files, five browser targets, a k6 harness) and what it is actually *run* with |
| **Defect recurrence** | ✅ supporting | Union-find grouping over clone links plus title-signature similarity. ⛔ A clone edge alone is **not** recurrence here: cloning is how a fix is carried into a hotfix, so only families spanning 2+ hotfixes count |
| Requirements · user stories · functional specifications | ⛔ **not used** | PAMIT holds no requirement links, and the product documentation is confirmed not up to date (70% of endpoints undocumented). A gap claiming a requirements source would be unfounded, so none does |
| Existing manual test cases | ⛔ not used as a denominator | The available manual corpus is 63 cases covering Login and Dashboard only. Absence there proves nothing about coverage, so it is not treated as evidence either way |

## 18. The daily process

**Owner ruling `D45`: the master workbook is refreshed as part of the daily run, in place. A second `.xlsx` is never created.**

The scheduled task **`PAM-Client-Ticket-Analysis`** runs at **09:00 daily** and now performs all four steps in one process:

| Step | What happens | Output |
| :-: | --- | --- |
| 1 | Read-only Jira enumeration of all four populations | `artifacts/client-tickets/snapshots/_raw-latest.json` |
| 2 | Analyse — build line on `Affected Milestone`, escape latency, regression signal, RCA, testing areas | in memory |
| 3 | Write the report and the dated summary | **this file** (`Updated` timestamp moves) · `summary/summary_<date>.md` · `<date>.json` · the CSVs |
| 4 | **Refresh the master workbook in place** | `artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` |

⚠️ **Step 4 lives inside the analysis script, not in a second scheduled task.** That is deliberate: two tasks could run at different times and leave the workbook describing yesterday's analysis while the report described today's. One process cannot drift from itself.

⚠️ **A workbook failure never fails the analysis.** The report, the snapshot and the CSVs are written first and are the primary deliverable. The likeliest failure is the file being open in Excel — a desk-level problem, not an analysis problem — so it is reported loudly and the exit code is unchanged. Rebuild with `python tools\jira\pamit_workbook.py`.

### 18.1 History across daily refreshes

The workbook is **overwritten** each day, so history cannot live in its sheets. It lives where it cannot be lost:

| What | Where | Retention |
| --- | --- | --- |
| Per-day headline counts and full ticket state | `artifacts/client-tickets/snapshots/<date>.json` | **Never deleted.** The history's source of truth |
| Per-day narrative summary | `docs/analysis/summary/summary_<date>.md` | Never overwritten across days; a same-day re-run replaces only that day's file |
| Day-over-day deltas, read at a glance | workbook sheet `12 Daily History` | **Derived** from the snapshots on every refresh |
| What changed since the last run | §*What changed* in the dated summary | Computed against the previous snapshot |

⛔ **Sheet 12 is derived, not appended.** An appended sheet would be lost the first time the workbook was rebuilt from scratch, and could silently disagree with the snapshots. A break in its date sequence means the job did not run that day — the gap is shown rather than smoothed over.

### 18.2 `Info not available in JIRA`

**Owner ruling: never leave an unavailable fact ambiguous, and never infer one without labelling it.** The sentinel is used in three distinct situations, all of which a blank cell would have flattened into one:

| Situation | Example | Where it shows |
| --- | --- | --- |
| The field does not exist in PAMIT | regression-test-executed, requirement link, detected-by | §7.4 and workbook sheet `10 Field Audit` |
| The field exists but is **never** populated | `Phase` (`cf 10164`) · `ReopenCount` (`cf 11018`) · `Module` · `Category` | an explicit workbook column reading the sentinel all the way down — a *missing* column would read as 'not analysed' |
| The field is populated in general but empty on **this ticket** | `RCA` on 486 of 2,169 · `Previous working version` on 1,744 | that ticket's cell on sheet `04 Ticket Details` |

⛔ **Nothing in this report infers a value for an unavailable field.** The clearest case is defect-injection phase: the RCA family looks like an answer (`Code - *`, `Analysis - *`, `Environment - *`) and is not one — `Code - Logic Issue` records where the defect was **found in code**, not the phase in which it was **introduced**. Mapping one to the other would produce a phase-containment metric that reads as measured and would drive real test-strategy decisions. `Phase` is 0% populated, so the honest answer is the sentinel.
