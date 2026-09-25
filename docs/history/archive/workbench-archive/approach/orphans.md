# Orphaned Test Classes — Phase 0.5

**Definition:** a test class that exists in `src/test/java/com/arcon/tests/` but is not referenced by any suite XML. TestNG never executes it, so it contributes zero coverage while still carrying maintenance cost.

| Measurement | At audit | After Phase 0 |
|---|---:|---:|
| Test classes on disk | 883 | 883 |
| Classes reachable from a suite | 146 | 665 |
| **Orphaned** | **737** | **218** |

519 classes were recovered in Phase 0 — 292 by repairing broken suite references, 227 by creating the three missing negative-API suites.

---

## 1. Recovered in Phase 0

### 1.1 Via reference repair

341 suite entries pointed at packages that no longer exist. Correcting them made 292 previously unreachable classes executable again.

| Dead package in XML | Real package on disk | Refs |
|---|---|---:|
| `com.arcon.tests.API_With_Excel.All_API_Positive` | `com.arcon.tests.API.All_API_Positive` | 126 |
| `com.arcon.tests.API_With_Excel.Negative_API.UnauthorizedAccess` | `com.arcon.tests.API.Negative_API.UnauthorizedAccess` | 68 |
| `com.arcon.tests.API_With_Excel.Negative_API.MethodNotAllowed` | `com.arcon.tests.API.Negative_API.MethodNotAllowed` | 68 |
| `com.arcon.tests.API_With_Excel.Positive` | `com.arcon.tests.API.All_API_Positive` | 40 |
| `com.arcon.tests.API_With_Excel.Negative_API.KotakSNOWApi` | `com.arcon.tests.API.Negative_API.KotakSNOWApi` | 1 |
| `com.arcon.tests.API_With_Excel.AllAPIPositive` | `com.arcon.tests.other.AllAPIPositive` | 2 |
| `com.arcon.tests.CRUD.AdminConsole.*` | `com.arcon.tests.UI.CRUD.AdministrativeConsole.*` | 10 |
| `com.arcon.tests.E2E.*` | `com.arcon.tests.UI.EndToEnd.*` / `com.arcon.tests.UI.CRUD.*` | 47 |
| `com.arcon.tests.UI.EndToEnd.AccessControl.*` | `com.arcon.tests.UI.CRUD.AccessControl.*` | 4 |
| `com.arcon.tests.UI.CRUD.PAMLogs.{Create,Delete,Modify}.ApiLogsTest` | `com.arcon.tests.UI.CRUD.PAMLogs.All.ApiLogsTest` | 3 |

`E2E.*` could not be rewritten with a single prefix rule — several classes referenced as `E2E.ACMO.manager.*` and `E2E.ACMO.myAccess.*` actually live under `UI.CRUD.ACMO.*`. Each was resolved individually by class name against the real tree.

### 1.2 Via new suites

Three negative-API failure modes had test classes but **no suite XML at all**, so 227 negative tests had never run. Suites created in `API_Suites/Negative/`:

| New suite | Classes |
|---|---:|
| `InvalidDataType.xml` | 76 |
| `InvalidValue.xml` | 76 |
| `MissingParameter.xml` | 75 |

Generated in the same shape as the existing `MethodNotAllowed.xml` / `UnauthorizedAccess.xml`: `TestListener`, `parallel="classes"`, `thread-count="2"`, `configfailurepolicy="skip"`.

> These 227 tests have never executed in CI. Expect first-run failures that reflect genuine untested behaviour, not regressions introduced by this work. Triage them in Phase 1 before treating any as a defect.

---

## 2. Remaining orphans — 218

Grouped by package. **Decision column is empty on purpose** — these need an owner call, and guessing would either delete real coverage or register tests that were deliberately parked.

### 2.1 PAMLogs sub-packages — 127 classes

The largest cluster. `UI/CRUD/PAMLogs/` holds 143 classes; only 16 are in `CRUD_Suites/PAMLogs.xml` and `PAMLogs_New.xml`.

| Package | Classes | Decision |
|---|---:|---|
| `UI.CRUD.PAMLogs.All_New` | 84 | |
| `UI.CRUD.PAMLogs.Modified` | 24 | |
| `UI.CRUD.PAMLogs.Select` | 8 | |
| `UI.CRUD.PAMLogs.All` | 4 | |
| `UI.CRUD.PAMLogs.Started` | 2 | |
| `UI.CRUD.PAMLogs.Assigned` | 1 | |
| `UI.CRUD.PAMLogs.Created` | 1 | |
| `UI.CRUD.PAMLogs.Download` | 1 | |
| `UI.CRUD.PAMLogs.Export` | 1 | |

**Open question:** the naming (`All` vs `All_New`, `Modified`) suggests `All_New` supersedes `All`. If so, `All` is dead code for Phase 6 and `All_New` should be registered. If both are live, both need suites.

### 2.2 `other.*` — 39 classes

| Package | Classes | Decision |
|---|---:|---|
| `other.validateBlankColumnData` | 12 | |
| `other.AdminuiRightClick` | 12 | |
| `other.AdminuiPredefinedValuesInForm` | 12 | |
| `other` (root) | 3 | |

`other` is not a PAM module. Phase 4 increment 13 proposes folding these into their owning modules (Setting / AdminUI) or deleting them.

### 2.3 UI modules — 43 classes

| Package | Classes | Decision |
|---|---:|---|
| `UI.CRUD.SessionMonitoring` | 8 | |
| `UI.EndToEnd.AdministrativeConsole.Reports` | 6 | |
| `UI.EndToEnd.raiseRequestServiceAccess.delegation` | 5 | |
| `UI.CRUD.setting_Other` | 4 | |
| `UI.EndToEnd.raiseRequestServiceAccess.adHoc` | 3 | |
| `UI.EndToEnd.AdministrativeConsole.PAMLogs` | 3 | |
| `UI.Negative.Servicepassword` | 2 | |
| `UI.Negative.ServiceAccess.OneTimeServiceAccess` | 2 | |
| `UI.EndToEnd.AdministrativeConsole` | 2 | |
| `UI.Negative.ServiceAccess.TimeBasedServiceAccess` | 1 | |
| `UI.Negative.ServiceAccess.PermanentServiceAccess` | 1 | |
| `UI.EndToEnd.Setting` | 1 | |
| `UI.CRUD.DigitalVault` | 1 | |
| `UI.CRUD.autoOnboarding` | 1 | |
| `UI.CRUD.ACMO_Reports` | 1 | |
| `UI.CRUD.ACMO` | 1 | |

`UI.CRUD.SessionMonitoring` is notable — all 8 classes are orphaned despite `CRUD_Suites/SessionMonitoring.xml` existing. That suite needs inspection.

### 2.4 API — 9 classes

| Package | Classes | Decision |
|---|---:|---|
| `API.All_API_Positive` | 3 | |
| `API.Negative_API.SNOWApi` | 2 | |
| `API.Negative_API.KotakSNOWApi` | 2 | |
| `API_UI` | 2 | |
| `API.Token` | 1 | |
| `API.Negative_API.MethodNotAllowed` | 1 | |

`SNOWApi` / `KotakSNOWApi` are customer-specific (ServiceNow integration) and may be intentionally excluded from the standard regression run — confirm before registering.

---

## 3. References disabled during repair

Two suite entries named classes that exist nowhere in the repo. Rather than delete the intent, both were replaced with a `PAMIT-TODO` comment recording the situation.

| File | Missing class | Note |
|---|---|---|
| `CRUD_Suites/AccessControl.xml` | `UI.EndToEnd.AccessControl.login_page` | No such class. The other four AccessControl classes resolved to `UI.CRUD.AccessControl.*`; this one has no counterpart. Restore the class or delete the entry. |
| `E2E_Suites/PAMLogs_E2E.xml` | `UI.EndToEnd.PAMLogs.UserCRUDTest` | Three same-named classes exist elsewhere — `UI.CRUD.setting.UserCRUDTest`, `other.AdminuiPredefinedValuesInForm.UserCRUDTest`, `other.validateBlankColumnData.UserCRUDTest`. Path context does not disambiguate; needs an owner decision. |

Find them with:

```bash
grep -rn "PAMIT-TODO" --include=*.xml "Automation gitlab repo/pam_automation_bootstrap"
```

---

## 4. Recommended next actions

| Priority | Action | Owner |
|---|---|---|
| 1 | Decide `PAMLogs.All` vs `All_New` — supersession or coexistence | Module owner |
| 2 | Inspect `CRUD_Suites/SessionMonitoring.xml` — suite exists but all 8 classes orphaned | Framework |
| 3 | Resolve the two `PAMIT-TODO` entries | Module owner |
| 4 | Confirm whether `SNOWApi` / `KotakSNOWApi` are deliberately excluded | QA lead |
| 5 | Fold or delete `other.*` (Phase 4 increment 13) | Framework |
| 6 | Triage the first run of the 227 newly reachable negative-API tests | QA |
