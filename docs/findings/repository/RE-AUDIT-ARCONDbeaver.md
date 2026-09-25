# Developer Repository Re-Audit — ARCONDbeaver.zip Removal Verification

**Subject:** Whether the reported removal of the multiple `ARCONDbeaver.zip` files resolved the
repository-sizing issue
**Repository:** `repo.arconnet.com/root/pam` · branch `35.8.29_Hotfix`
**Jira:** `PAMIT-43050` (original finding) · `PAMIT-42900` (the change under test)
**Baseline audit:** HEAD `12234f037` — see `README.md` (this folder) and `artifacts/repo-issues/evidence/`
**This re-audit:** HEAD `fa04bf6a9`, fast-forwarded from origin (`0 ahead / 0 behind`)
**Reported by:** Soumya (Developer) — multiple `ARCONDbeaver.zip` files removed from the repository
**Verdict:** ⛔ **NOT FIXED — and actively regressing**

⚠️ **This report was first measured at HEAD `1065b4aff` and has been re-measured at `fa04bf6a9` after a
further fast-forward of 11 commits.** The re-measurement did not soften the verdict, it hardened it:
`ARCONDbeaver.zip` **grew from 240 MB to 430 MB** under the same ticket. Figures throughout are at
`fa04bf6a9`; where the intermediate `1065b4aff` value is informative it is shown alongside. §5.3 records
the change.

---

## 1. Verdict

⛔ **NOT FIXED.** The repository did not shrink. It grew by **455 MiB**.

| Question asked | Answer |
|---|---|
| Has the repository size been reduced? | ⛔ **No** — `27.87 GiB` → **`28.31 GiB`** |
| Have the multiple `ARCONDbeaver.zip` files been completely removed? | ⛔ **No** — **1 of 2** copies removed, and only from `HEAD` |
| Has any of the 11.45 GiB attributed to this file been reclaimed? | ⛔ **No** — **0 bytes** |
| Is the surviving copy at least getting smaller? | ⛔ **No** — it **grew 79%**, `240 MB` → **`430 MB`** |
| Is the original sizing issue fully resolved? | ⛔ **No** |
| Did anything genuinely improve? | 🟡 **One duplicate copy left `HEAD`** (−240 MB on a fresh checkout). That saving has since been **more than cancelled** by the 190 MB growth of the surviving copy |

**Why the distinction matters.** The original finding was explicit that this is a *history* problem, not a
checkout problem — `README.md` §1: *"The problem is history, not the checkout. Deleting files today reclaims
nothing, because git keeps every version of every file ever committed."* The change under test deletes a file
in a new commit. That records an absence going forward; it removes nothing from history.

⚠️ **The commit is honest about its own scope; the confirmation relayed onward was broader than the commit.**
`ff853ebc0` states *"Also removed arcondbeaevr from allsupporting dlls"* — singular, one directory. That is
exactly what was measured. This is a reporting gap, not a misstatement by the developer.

---

## 2. The decisive measurement

| Metric | Baseline | Re-audit | Change |
|---|---:|---:|---|
| **Object store total** | **27.8653 GiB** | **28.3096 GiB** | ⛔ **grew +455.0 MiB** |
| — packed (`size-pack`) | 27.8653 GiB | 27.8888 GiB | +24.0 MiB |
| — loose (`size`) | 0 bytes | **430.89 MiB** (87 objects) | ⛔ the new archive, unpacked |
| Bytes, exact | 29,920,098,478 | 30,397,197,312 | **+477,098,834** |
| Packfiles | 2 | 3 (+ `multi-pack-index`) | +1 |
| Objects in pack | 210,471 | 211,036 | +565 |
| `prune-packable` | 0 | 0 | — |
| `garbage` | 0 | 0 | — |
| Space reclaimed | — | **0 bytes** | target was 20.43 GiB |

⚠️ **Quote the total, not `size-pack` alone.** `git count-objects -vH` reports loose and packed separately.
At the time of measurement the newest 430 MB archive was still **loose** (`count: 87`, `size: 430.89 MiB`),
so `size-pack` alone understates the repository by that amount. It will fold into a packfile at the next
`gc` without shrinking.

⛔ **The main packfile is byte-identical in size — `28,765,917,030` bytes at baseline and now.** A history
rewrite would necessarily have replaced it. That single fact settles the question before any per-file
analysis.

`prune-packable: 0` and `garbage: 0` also confirm there is nothing for `git gc` to collect, unchanged from
the baseline.

---

## 3. Before vs after — every metric re-measured

| Metric | Before | After | Change |
|---|---:|---:|---|
| **Object store total** | **27.8653 GiB** | **28.3096 GiB** | ⛔ **grew +455.0 MiB** |
| **`ARCONDbeaver.zip` versions in history** | **50** | **53** | ⛔ **+3 added** |
| **`ARCONDbeaver.zip` size in `HEAD`** | **251,717,722** | **450,989,831** | ⛔ **+79.2% (+190 MiB)** |
| `ARCONDbeaver.zip` copies in `HEAD` | 2 | 1 | ✅ −1 removed |
| `ARCONMacDbeaver.zip` copies in `HEAD` | 3 | 3 | ⛔ unchanged — content replaced |
| `ARCONMacDbeaver.zip` versions in history | — | 3 | ⛔ +2 in the audit window |
| `multitab.zip` versions in history | 48 | 49 | ⛔ +1 |
| `dbeaver.zip` versions in history | 36 | 36 | 🟡 unchanged |
| DBeaver total in `HEAD` | — | 1.523 GiB raw / 0.788 GiB unique | ⛔ largest non-ARCON category |
| Working tree | 7.69 GB | ~7.7 GB | ⛔ net flat — the −240 MB was refilled |
| Total repository | 35.57 GB | ~36.0 GB | ⛔ **larger than before** |
| `HEAD` files over 20 MB | 65 / 4.677 GiB | 64 / **4.622 GiB** | 🟡 −1 file, but only −0.055 GiB |
| Commits, all refs | 35,602 | 35,915 | +313 |
| Remote branches | 3,326 | 3,360 | +34 — all keep history reachable |
| Tags | 307 | 313 | +6 |
| `.gitattributes` tracked | 0 | **0** | ⛔ no mitigation adopted |
| `.git/lfs` present | No | **No** | ⛔ LFS still not adopted |
| `.gitignore` rule barring archives | None | **None** | ⛔ inflow still open |

**Reconciliation.** The `HEAD` large-file line nets out at only `−0.055 GiB` because three effects cancel:
the removed copy (`−251,721,906`), a 1.94 MB reduction on each of the three `ARCONMacDbeaver.zip` copies
(`−5.8 MB`), and the surviving `ARCONDbeaver.zip` growing by `+199,267,925`. **The removal was worth 240 MB;
the growth of the file that stayed cost 190 MB of it back.** Nothing else in `HEAD` moved.

---

## 4. `ARCONDbeaver.zip` — path-level and history-level state

### 4.1 In `HEAD` — one of two paths removed

| Path | Baseline | At `1065b4aff` | At `fa04bf6a9` | Status |
|---|---:|---:|---:|---|
| `PAM/AllSupportingDLLs/ARCONDbeaver.zip` | 251,717,722 | *absent* | *absent* | ✅ **Removed** |
| `PAM/AllSupportingDLLs/ARCOSClients/ARCONDbeaver.zip` | 251,717,722 | 251,721,906 | **450,989,831** | ⛔ **Still present, and now 79% larger** |

The surviving copy is not merely still there. It has been **rewritten twice since the baseline** — first to
blob `b120d44c` (+4,184 bytes), then to a **450,989,831-byte** version by `b4c06f4fc`. That single blob is
larger than any object the original audit found in `HEAD`.

### 4.2 In history — the count went up

| Filename | Baseline versions | Re-audit versions | Change |
|---|---:|---:|---|
| `ARCONDbeaver.zip` | 50 | **53** | ⛔ **+3** |
| `multitab.zip` | 48 | **49** | ⛔ +1 |
| `dbeaver.zip` | 36 | 36 | 🟡 0 |
| `ARCONMacDbeaver.zip` | — | 3 | ⛔ +2 in window |

⛔ **All 53 versions remain fully reachable.** 3,360 remote branches guarantee reachability, so nothing is
unreferenced and nothing is collectable. **The count has moved in the wrong direction at every
measurement:** 50 at baseline, 52 four days after the "removal", 53 the day after that.

---

## 5. What landed alongside the cleanup

⛔ **A new 240 MB version of the same file was committed on the same day, under the same ticket.**

| Commit | Date | Author | Subject | Effect |
|---|---|---|---|---|
| `ff853ebc0` | 2026-08-28 | Chinmay | `PAMIT-42900` — Depricating QA services for MSSQL,ORACLE and MYSQL databases Also removed arcondbeaevr from allsupporting dlls | ✅ removed 1 of 2 `HEAD` copies |
| `d5870681a` | 2026-08-28 | Chinmay | `PAMIT-42900` — Updated dbeaver and db2 changes | ⛔ **added a new 239.9 MB `ARCONDbeaver.zip` blob** |
| `cba4ce506` | 2026-08-26 | Magesh Nadar | ARCONMacDbeaver.zip updated | ⛔ added a 375.2 MB blob |
| `a98b16615` | 2026-08-24 | Magesh Nadar | `CI-22348` — Mac Dbeaver with support for profile whitelisting | ⛔ added a 369.0 MB blob |
| **`b4c06f4fc`** | **2026-09-01** | **Chinmay** | **`PAMIT-42900` — Sybase database support to inhosue dbeaver** | ⛔ **replaced `ARCONDbeaver.zip` with a 430 MB version (+190 MB)** |

### 5.1 Attribution of the two new packfiles

The main pack is unchanged, so all new storage sits in the two packs written since the baseline:

| Packfile | Written | Blobs | Blob bytes | Largest object |
|---|---|---:|---:|---|
| `pack-7c5b15d2…` | 2026-08-28 | 1,737 | 0.857 GiB | 375.2 MB `d2c0dc94` — `ARCONMacDbeaver.zip` |
| `pack-c3b42bb5…` | 2026-09-01 | 61 | 0.235 GiB | **239.9 MB `e32351c4` — `ARCONDbeaver.zip`** |

⛔ **The 1 September pack is 99% one object.** Blob `e32351c4` is a new `ARCONDbeaver.zip` version introduced
by `d5870681a`, and it is stored **whole, with no delta base** — reproducing exactly the non-compressibility
the original audit proved (`README.md` §4.2: 44 of 47 versions stored whole).

### 5.2 `ARCONMacDbeaver.zip` — replaced, never removed

All three copies persist and were updated in the same window:

| Path | Before | After |
|---|---:|---:|
| `PAM/ARCON_ACMO/ARCOSClientManagerOnline_V2/ARCOSClients/ARCONMacDbeaver.zip` | 396,667,262 | 394,725,255 |
| `PAM/AllSupportingDLLs/ARCOSClients/ARCONMacDbeaver.zip` | 396,667,262 | 394,725,255 |
| `PAM/AllSupportingDLLs/ARCONMacDbeaver.zip` | 396,667,262 | 394,725,255 |

All three resolve to the same blob (`07f8430c`), so the pack stores the content once — but the working tree
carries it three times, and the two superseded versions are now permanent history.

### 5.3 The regression measured one day later

⛔ **The trend is the finding.** This report was first measured at `1065b4aff`. A further fast-forward the
next day brought 11 commits, one of which grew the file this audit is about by **79%**:

| Measurement point | `ARCONDbeaver.zip` in `HEAD` | Versions in history | Object store |
|---|---:|---:|---:|
| Baseline `12234f037` | 251,717,722 × **2 paths** | 50 | 27.8653 GiB |
| `1065b4aff` — 4 days after the "removal" | 251,721,906 × 1 path | 52 | 27.8831 GiB |
| `fa04bf6a9` — the next day | **450,989,831 × 1 path** | **53** | **28.3096 GiB** |

`b4c06f4fc` — *"PAMIT-42900 - Sybase database support to inhosue dbeaver"* — is **the same ticket as the
removal**. Nine days after `PAMIT-42900` removed one copy of this archive to reduce repository size, the same
ticket committed a version 190 MB larger than the one it removed.

⚠️ **Net effect of `PAMIT-42900` on repository size: +455 MiB.** The removal saved 240 MB in the checkout;
the two new versions it committed added 240 MB and then 430 MB of permanent history.

---

## 6. Remaining large files in `HEAD`

**64 files over 20 MB, totalling 4.622 GiB.** DBeaver alone accounts for **1.523 GiB** across four paths
(**0.788 GiB** of distinct content) and remains the largest category of non-ARCON code in the repository —
and it is now **the single largest file in `HEAD`**.

| File | Size | Assessment |
|---|---:|---|
| **`ARCONDbeaver.zip`** | **430.1 MB** | ⛔ **The file this audit was about — now the largest object in `HEAD`** |
| `ARCONMacDbeaver.zip` × 3 paths | 376.4 MB ea. | ⛔ Third-party DBeaver; identical blob triplicated |
| `ARCOMPAMUbuntu20_V1.deb` | 222.9 MB | 🟡 Release artifact — belongs in a release page |
| `ARCOMPAMRedHat7.5_V1.rpm` | 172.7 MB | 🟡 Release artifact |
| `ARCOMPAMUbuntu18_V1.2.deb` | 161.3 MB | 🟡 Release artifact |
| `ARCOMPAMUbuntu16.04.03_V4.1.deb` | 155.4 MB | 🟡 Superseded OS, still shipped |
| `ARCONThickClient.msi` | 132.1 MB | 🟡 Release artifact |
| `ARCONAWB.zip` × 2 (64/32) | 124.8 / 116.1 MB | 🟡 Bundled browser runtime |
| `windows_auth.zip` | 116.1 MB | 🟡 Bundled runtime |

The five OS installers alone total **844.4 MB** in `HEAD`.

---

## 7. Duplicate content inside `HEAD`

⛔ **1.40 GB of the checkout is the same bytes committed to multiple paths.** This needs no history rewrite
and shrinks every future clone.

| File | Copies | Redundant bytes |
|---|---:|---:|
| `ARCONMacDbeaver.zip` | 3 | 752.9 MB |
| `avcodec-57.dll` | **15** | 327.4 MB |
| `oraociicus11.dll` | 5 | 136.2 MB |
| `ARCONPyAutomation.exe` | 3 | 58.6 MB |
| `ARCONURLMonitor.exe` | 3 | 58.1 MB |
| `avcodec-58.dll` | 2 | 43.9 MB |
| `dotnetfx.exe` | 2 | 23.8 MB |
| **Total** | | **1,400.9 MB** |

---

## 8. Why the deletion changed nothing

This is the point most worth carrying back to the team, because it will otherwise recur.

| Mechanism | Consequence |
|---|---|
| Git stores every version of every file, permanently | Deleting in a new commit records an absence **going forward** only |
| 3,360 remote branches keep all history reachable | Nothing is unreferenced, so `gc` has nothing to collect (`garbage: 0`) |
| A ZIP is already compressed and cannot be delta-encoded | 44 of 47 versions were already stored **whole**; no redundancy remains for `repack` to exploit |
| Re-audit reproduced this on the newest blob | `e32351c4` — 239.9 MB, stored whole, no delta base |

⛔ **Only a history rewrite reclaims the space:** `git filter-repo` over the offending paths, followed by a
forced re-pack and garbage collection **on the server**, after which every clone must be re-made. That is an
org-wide coordinated operation and the only action that moves the 27.88 GiB figure.

⛔ **`git gc` / `git repack` will reclaim essentially nothing** — show anyone proposing it `garbage: 0`,
`prune-packable: 0`, and the whole-storage measurement above.

---

## 9. Preventive controls — still entirely absent

| Control | State | Consequence |
|---|---|---|
| `.gitattributes` | ⛔ 0 tracked files | No LFS routing, no binary policy |
| Git LFS (`.git/lfs`) | ⛔ Not present | Standard mitigation never adopted |
| `.gitignore` rule for `*.zip` / `*.deb` / `*.rpm` / `*.msi` | ⛔ None | Nothing prevents the next archive |
| Pre-receive size limit | ⛔ Not observed | Nothing prevents the next 240 MB commit |

⚠️ **This is the finding that allowed a 240 MB archive to land on the same day as its own cleanup.** Until a
gate exists, any future rewrite is refilled within weeks.

---

## 10. Recommendations

Ordered by value per unit of risk. **Items 1–3 are worth doing regardless of whether the rewrite is ever
approved.**

| # | Action | Risk | Why |
|---:|---|---|---|
| **1** | **Bar new binary archives at the gate** — pre-receive size limit, or `.gitignore` covering `*.zip` `*.deb` `*.rpm` `*.msi` | ✅ Zero | Without this, everything else is temporary. Directly addresses §5 |
| **2** | **Make `git clone --filter=blob:none` the standard clone**; `--depth 1` for CI | ✅ Zero | 98.1% of history is binary almost nobody needs. Full history retained, contents fetched on demand. Highest value available today, no server change, reversible |
| **3** | **De-duplicate within `HEAD`** — consolidate the 15 `avcodec-57.dll` copies, the 3 `ARCONMacDbeaver.zip` copies, etc. | 🟡 Low | Recovers 1.40 GB from every future clone with no rewrite |
| **4** | **Finish the job on `ARCONDbeaver.zip`** — one copy remains at `PAM/AllSupportingDLLs/ARCOSClients/`; the Mac variant's three copies were never in scope | 🟡 Low | If PAMIT-42900's intent was removal, that path is still outstanding |
| **5** | **Move the OS installers to an artifact store** — 844.4 MB of `.deb` / `.rpm` / `.msi` are release artifacts, not source | 🟡 Low | Also stops each rebuild adding a fresh whole copy |
| **6** | **Then rewrite history** — `git filter-repo` over the three archives | ⛔ Destructive | Reclaims the 20.43 GiB. Rewrites every commit hash, needs server-side `gc`, forces every developer and pipeline to re-clone. Requires the repository owner and a scheduled window — **and is wasted effort until item 1 is in place** |

---

## 11. Reproducing this re-audit

Read-only. No write, rewrite or push was performed against `pam`.

```bash
cd pam

# §0 — confirm you are current FIRST; this report went 11 commits stale in one day
git fetch origin && git rev-list --left-right --count HEAD...origin/35.8.29_Hotfix

# §2 — the decisive measurement. Add `size` (loose) to `size-pack`; do not quote size-pack alone
git count-objects -vH
ls -l .git/objects/pack/

# §4.1 — path-level state in HEAD
git ls-tree -r -l HEAD | grep -iE 'ARCONDbeaver\.zip|ARCONMacDbeaver\.zip'

# §4.2 — distinct blob versions per filename across all refs
git log --all --raw --no-abbrev --format="" -- '*ARCONDbeaver.zip' \
  | awk '{print $4}' | grep -E '^[0-9a-f]{40}$' | grep -v '^0\{40\}$' | sort -u | wc -l

# §5 — the commits under test
git log --all --format='%h %ad %an | %s' --date=short -- '*ARCONDbeaver.zip' | head
git log --all --diff-filter=D --format='%h %ad %an | %s' --date=short \
  -- 'PAM/AllSupportingDLLs/ARCONDbeaver.zip'

# §5.1 — attribute a packfile by object size
git verify-pack -v .git/objects/pack/pack-<id>.idx \
  | awk '$2=="blob"{printf "%12d %s\n", $4, $1}' | sort -rn | head

# §6 — remaining large files in HEAD
git ls-tree -r -l HEAD | awk '$4>20000000 {print $4"\t"$5}' | sort -rn

# §9 — preventive controls
git ls-files | grep -c '.gitattributes'
[ -d .git/lfs ] && echo LFS || echo "no LFS"
```

---

## 12. Method, basis and limits

| Item | Detail |
|---|---|
| **Version-count basis differs between audits** | The baseline's 50 / 48 / 36 came from `git verify-pack -v` attribution across both packfiles. This re-audit's 52 / 49 / 36 counts **distinct blob SHAs reachable from any ref**. Different derivations of the same quantity — the **deltas are corroborated by the named commits in §5**, not inferred from the counts alone |
| **Pack-level subtraction is not clean** | Between the two audits git wrote a `multi-pack-index` and replaced the 2026-08-10 pull pack. The authoritative comparison is `size-pack` from `git count-objects -vH`, which is what §2 quotes |
| **Locally measured** | All figures come from this clone at `fa04bf6a9`, fast-forwarded from origin and verified `0 ahead / 0 behind`. Server-side disk usage may differ from a local clone's |
| **Two measurement points** | First measured at `1065b4aff` (itself a fresh fast-forward of 11 commits), then re-measured at `fa04bf6a9` after a further 11 commits. Both are recorded rather than silently overwritten, because the delta between them **is** the §5.3 finding |
| ⚠️ **The daily refresh can no longer pull `pam`** | `state/daily/last-run.json` for 2026-09-02 records: *"working tree is not clean (1 changed) — refusing to pull"*. The single unclean item is the untracked `AutomationTesting/` leftover from `89218d65a`. **Until it is cleared, `pam` silently stops receiving upstream commits** — which is exactly how this report went 11 commits stale within a day |
| **`ARCONMacDbeaver.zip` history count** | 3 distinct blob contents; it was not in the baseline's top-three attribution because it dedupes to few versions, unlike `ARCONDbeaver.zip`'s 52 |
| **Not re-derived** | The baseline's 73.3% / 20.43 GiB three-archive attribution and the 98.1% binary share were **not** recomputed — `verify-pack` over the 28.77 GB main pack is expensive, and that pack is unchanged, so the baseline attribution still holds |
| **Unrelated observation** | `pam/AutomationTesting/` was deleted upstream in `89218d65a` (1,211 files, including `pom.xml`), which resolves the SCA-scanner concern in the root `CLAUDE.md` §Edit scope. Only **8.8 MB** of untracked `target/` output remains on disk; it is not part of repository size, but it does leave `pam/` with a non-clean `git status` |

**Baseline sources:** `README.md` (this folder) · `findings.csv` rows `F01`, `F09` ·
`artifacts/repo-issues/evidence/E1-git-object-store.txt`, `E3-head-files-over-20MB.txt`,
`E4-history-largest-blob-versions.txt`, `E7-ondisk-pack-attribution.txt`, `E8-pack2-pull-attribution.txt`
