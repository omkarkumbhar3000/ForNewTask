# Developer Repository Size — Findings and Evidence

**Repository:** `pam/` — ARCON PAM product source · `https://repo.arconnet.com/root/pam.git`
**Measured at:** branch `35.8.29_Hotfix`, commit `12234f037`, working tree clean
**Reported concern:** the folder is ~28 GB, which seems disproportionate
**Verdict:** ⛔ **Confirmed, and understated.** The folder is **35.57 GB**. The 28 GB observed is almost
exactly `.git` (27.88 GB). **Three third-party ZIP files are 72.7% of it. All product source is 0.8%.**
**Audience:** the product repository owner, and a developer who can act. ARCON PAM is not our repository —
everything here is a recommendation to raise, not an action we have taken.

> ⛔ **Nothing in this investigation modified `pam/`.** Every command was read-only — no `gc`, `prune`,
> `repack`, `filter-repo`, or any branch/file operation. `git status` is still clean at `12234f037`.

---

## 1. Summary

The repository is **35.57 GB across 28,827 files**, and it splits in a way that changes the diagnosis:

| Component | Size | Files | Share |
|---|---:|---:|---:|
| **`.git/` — commit history** | **27.88 GB** | **107** | **78.4%** |
| Working tree (checked-out files) | 7.69 GB | 28,720 | 21.6% |
| **Total** | **35.57 GB** | **28,827** | 100% |

**The problem is history, not the checkout.** Deleting files today reclaims nothing, because git keeps
every version of every file ever committed.

**Root cause, in one sentence: large third-party binary archives were committed to git and re-committed
dozens of times, and because a ZIP is already compressed, git cannot delta it and stored a full fresh
copy every time.**

Measured directly from both packfiles — **not estimated** — three filenames account for **20.43 GiB of the
27.86 GiB total (73.3%)**:

| File | Versions in history | **On-disk pack bytes** | Share of history | What it actually is |
|---|---:|---:|---:|---|
| `ARCONDbeaver.zip` | 50 | **11.45 GiB** | **41.1%** | DBeaver — an open-source DB client |
| `multitab.zip` | 48 | **4.59 GiB** | 16.5% | MultiTab client installer |
| `dbeaver.zip` | 36 | **4.39 GiB** | 15.8% | DBeaver again, second copy |

**A single file — `ARCONDbeaver.zip` — is 41% of this repository.** It is not ARCON code.

**Binary artifacts are 98.1% of the repository's history.** All C# source across 30,888 versions is
**0.204 GiB — 0.8%**.

**It is still growing.** A routine 106-commit update pulled on 2026-08-10 added **1.1 GB** while changing
only 142 files — about **10 MB per commit**.

**For scale:** the QA automation repository, same organisation and era, is **131 MB**. This repository is
**271× larger**.

---

## 2. Where the 35.57 GB sits

### 2.1 The packfile — authoritative on-disk attribution

From `git verify-pack -v`, which reports each object's *actual compressed size in the packfile*.
**Both packs are attributed:** the main pack is 26.790 GiB and the 2026-08-10 pull pack is 1.074 GiB,
totalling **27.864 GiB** — which reconciles with the 27.88 GB measured on the filesystem.

The table below is the main pack. **The second pack is almost a single file:** of its 1.074 GiB,
**0.954 GiB (88.8%) is three new versions of `ARCONDbeaver.zip`** — see §4.5.

| Extension | **On-disk** | Share | Versions | Category |
|---|---:|---:|---:|---|
| **`.zip`** | **21.579 GiB** | **80.6%** | 262 | ⛔ Third-party archives |
| `.msi` | 1.850 GiB | 6.9% | 112 | ⛔ Windows installers |
| `.exe` | 1.230 GiB | 4.6% | 490 | ⛔ Compiled binaries |
| `.deb` | 0.437 GiB | 1.6% | 3 | ⛔ Linux installers |
| `.dll` | 0.413 GiB | 1.5% | 1,690 | ⛔ Compiled libraries |
| `.nupkg` | 0.273 GiB | 1.0% | 170 | ⛔ NuGet packages |
| `.pkg` | 0.211 GiB | 0.8% | 1 | ⛔ macOS installer |
| **`.cs`** | **0.204 GiB** | **0.8%** | **30,888** | ✅ Product source |
| `.rpm` | 0.169 GiB | 0.6% | 1 | ⛔ Linux installer |
| `.jar` / `.asar` | 0.115 GiB | 0.4% | 43 | ⛔ Packaged binaries |

**Binary artifacts: 26.28 GiB = 98.1% of the pack. Source: 0.8%.**

⚠️ **Note how well source compresses.** `.cs` is 12.38 GiB of *logical* content across 30,888 versions
but only **0.204 GiB on disk** — a 60× saving, because text deltas beautifully. `.zip` gets almost no
benefit, which is the entire problem. **Do not target source files; they are already nearly free.**

### 2.2 The current checkout — 7.363 GiB across 19,091 files

| Extension | Bytes | Share | Files |
|---|---:|---:|---:|
| `.zip` | 2.189 GiB | 29.7% | 40 |
| `.dll` | 1.938 GiB | 26.3% | 1,089 |
| `.exe` | 1.366 GiB | 18.6% | 188 |
| `.deb` | 0.527 GiB | 7.2% | 3 |
| `.pkg` / `.rpm` | 0.380 GiB | 5.2% | 2 |
| `.msi` | 0.140 GiB | 1.9% | 13 |
| `.db` | 0.111 GiB | 1.5% | 5 |
| **`.cs` — product source** | **0.103 GiB** | **1.4%** | **6,866** |
| `.mp4` | 0.043 GiB | 0.6% | 11 |

---

## 2.3 Jira status

| Ticket | Group | Covers | Status |
|---|---|---|---|
| [**PAMIT-43050**](https://arcon-tech-solution.atlassian.net/browse/PAMIT-43050) | **B1 — Binary artifacts committed to version control** | F01, F02, F03, F07, F13 | ✅ Raised · `Bug` · `Sev-1` / `High` · component `SCM` |
| — | B2 — No controls prevent binary intake | F04, F08, F10, F12, F15 | ⬜ Drafted, held |
| — | B3 — Checkout carries redundant binaries | F05, F06, F11 | ⬜ Drafted, held |
| — | B4 — Adopt partial clone; plan history remediation | F09, R01, R03 | ⬜ Drafted, held |

Built by `tools/jira/create_b01.py`. Attached: `findings.csv`, `README.md` (this file) and a zip of
`evidence/`. **B2–B4 are deliberately not raised** — the owner approved B1 only.

**Daily status review:** `python tools\jira\track_tickets.py` reports the live status and assignee of
every tracked group and flags the ones that are ours — see [`tools/jira/TRACKING.md`](../tools/jira/TRACKING.md).
It flags a ticket in **`QA Testing`** (any assignee) or in **`Awaiting Response` assigned to
Omkar Kumbhar**. Read-only: `GET` requests only, it never modifies an issue.

---

## 3. Findings

Ranked by contribution. **L** = layer: `history` needs a rewrite to fix; `tree` can be fixed going
forward; `process` is why it keeps happening.

| # | Ticket | L | Sev | Finding | Measured | Remediation | Risk |
|---|---|---|---|---|---:|---|---|
| **1** | [PAMIT-43050](https://arcon-tech-solution.atlassian.net/browse/PAMIT-43050) | history | 🔴 Critical | **Three third-party ZIP archives are 73.3% of the repository.** `ARCONDbeaver.zip` (50 versions, **11.45 GiB — 41.1% on its own**), `multitab.zip` (48), `dbeaver.zip` (36). **Measured proof they cannot compress: 44 of 47 versions are stored whole with no delta base.** Two of the three are **DBeaver, an open-source tool that was never ARCON code** | **20.43 GiB on disk** | Purge with `git filter-repo`; distribute via artifact store or release page | ⛔ Destructive rewrite |
| **2** | [PAMIT-43050](https://arcon-tech-solution.atlassian.net/browse/PAMIT-43050) | history | 🔴 Critical | **All `.zip` content is 80.6% of the packfile** from only 262 versions — the pattern is broader than those three files | **21.58 GiB on disk** | As above, plus a pre-receive hook rejecting archives | ⛔ Destructive rewrite |
| **3** | [PAMIT-43050](https://arcon-tech-solution.atlassian.net/browse/PAMIT-43050) | history | 🔴 Critical | **Installer packages are committed as source**: `.msi` 1.85 GiB, `.exe` 1.23 GiB, `.deb`/`.rpm`/`.pkg` 0.82 GiB. Includes `ARCON PAM.msi` (7 versions, 0.79 GiB) and `dotnetfx.exe`, a **Microsoft redistributable** | **3.90 GiB on disk** | Publish to a release/artifact store; purge from history | ⛔ Destructive rewrite |
| **4** | ⬜ Need to create a ticket | tree | 🔴 Critical | **`.gitignore:363` declares `/PAM` — the entire product tree — yet 17,872 files under `PAM/` are tracked.** `.gitignore` never applies to already-tracked files, so the rule is inert *and actively misleading*. It would also silently block genuinely new `PAM/` files from being staged | 17,872 tracked files under an "ignored" path | Remove the false `/PAM` rule; add real artifact rules; `git rm --cached` the artifacts | Medium |
| **5** | ⬜ Need to create a ticket | tree | 🟠 High | **3.69 GiB of the checkout is duplicate filenames at different paths**, of which 1.51 GiB is byte-identical. ⚠️ Git stores identical blobs **once**, so this is a per-checkout cost, not history bloat — but it multiplies history as soon as copies drift and are updated separately | **3.69 GiB per checkout** | Consolidate to one location; reference rather than copy | Medium |
| **6** | ⬜ Need to create a ticket | both | 🟠 High | **`msedgedriver.exe` is committed at 45 paths with 45 *distinct* SHAs** — 45 genuinely different versions, 593 MB in the checkout alone. `chromedriver.exe` has 14. Browser drivers are version-pinned downloads, never source | 738 MB in HEAD + history churn | Fetch at test time via WebDriverManager or a CI cache | Low |
| **7** | [PAMIT-43050](https://arcon-tech-solution.atlassian.net/browse/PAMIT-43050) | history | 🟠 High | **`PAM/AllSupportingDLLs/` is 18.02 GiB of logical history from only 734 versions** — ~25 MB per version. A vendored third-party dependency tree under version control | 18.02 GiB logical | Migrate to NuGet or an internal feed | High |
| **8** | ⬜ Need to create a ticket | process | 🟠 High | **3,326 remote branches and 307 tags.** Every ref keeps its blobs reachable, so nothing is ever unreachable — which is why `git gc` reports zero garbage and the pack never shrinks | 3,326 refs | Prune merged and abandoned release branches | Medium |
| **9** | ⬜ Need to create a ticket | process | 🟠 High | **Still growing, and one file dominates the growth.** A 106-commit pull on 2026-08-10 changing 142 files created a 1.074 GiB pack, of which **0.954 GiB (88.8%) was three new versions of `ARCONDbeaver.zip`** — none of them in `HEAD`. All C# source in that pull was 0.7% | 1.074 GiB / 106 commits | Fix #4 and #6 first — they are the inflow | Low |
| **9b** | ⬜ Need to create a ticket | process | 🟠 High | **No Git LFS and no `.gitattributes` anywhere in the repository.** The standard mitigation for large binaries was never adopted, and nothing constrains binary intake | 0 `.gitattributes` files; no `.git/lfs` | Adopt LFS *(see §5.4)* or a size-gate hook *(§5.3)* | Low |
| **10** | ⬜ Need to create a ticket | tree | 🟡 Medium | **A duplicate misnamed `gitignore`** (no leading dot, 6,654 B) sits beside the real `.gitignore` (6,669 B). Git ignores a dotless file entirely; the two differ by 14 lines, so rules a developer believes are active are not | 14 differing lines | Delete `gitignore` after reconciling its 14 lines | Low |
| **11** | ⬜ Need to create a ticket | tree | 🟡 Medium | **Media and database binaries in source control**: 11 `.mp4` (43 MB), 5 `.db` (111 MB incl. three ~23 MB SQLite files), 2 `.bak` (25 MB) | 179 MB | Move to shared storage; generate DBs at test time | Low |
| **12** | ⬜ Need to create a ticket | tree | 🟡 Medium | **Two junk top-level directories are tracked**: `%LOCALAPPDATA%/` — a literal unexpanded environment variable used as a folder name by a script that failed to expand it — and `108.0.5359.125/` (a Chrome version), whose `chromedriver.exe` is a **1-byte placeholder**. Both confirmed tracked, 2 files each. Evidence that scripted commits reach shared branches unreviewed | 2 dirs, 4 files | Delete; fix the script that created it | Low |
| **13** | [PAMIT-43050](https://arcon-tech-solution.atlassian.net/browse/PAMIT-43050) | history | 🟡 Medium | **Generated tooling output was committed on some branch** — `graphify-out/` (1,099 versions, 0.09 GiB) and a 60 MB `syftSbomTable.json`. ⚠️ Neither is in `HEAD`; both are reachable from other refs, so they still occupy history | 0.15 GiB | Add to `.gitignore`; purge in the same rewrite | Low |
| **14** | — *(context, not a defect)* | — | ℹ️ Context | **The QA automation repository is 131 MB total** — same organisation, same era. This repository is **271×** larger | 271× ratio | — | — |

---

## 4. Evidence

Raw captures are in [`evidence/`](evidence/). Every figure below is reproducible read-only.

### 4.1 The size split

```powershell
$p = "E:\Omkar\Automation\Dev Project\pam"
Get-ChildItem "$p\.git" -Recurse -Force -File | Measure-Object Length -Sum   # 27.88 GB, 107 files
Get-ChildItem $p        -Recurse -Force -File | Measure-Object Length -Sum   # 35.57 GB, 28,827 files
```

```
$ git count-objects -vH
in-pack: 210471 · packs: 2 · size-pack: 27.87 GiB · loose: 0 · garbage: 0
```

`loose: 0`, `garbage: 0`, `prune-packable: 0` — **the repository is already optimally packed.**
This single line disproves "just run `git gc`". → [`evidence/E1-git-object-store.txt`](evidence/E1-git-object-store.txt)

### 4.2 Findings 1–3 — authoritative pack attribution

```bash
git verify-pack -v .git/objects/pack/pack-e43e14d9…idx
# fields: <sha> <type> <size> <size-in-packfile> <offset>
# aggregate column 4 by extension, joining sha -> path via:
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)'
```

**On-disk pack bytes by filename — top 8:**

| File | Versions | On-disk |
|---|---:|---:|
| `ARCONDbeaver.zip` | 47 | 10.500 GiB |
| `multitab.zip` | 48 | 4.589 GiB |
| `dbeaver.zip` | 36 | 4.388 GiB |
| `ARCON_Mac.zip` | 2 | 1.071 GiB |
| `ARCON PAM.msi` | 7 | 0.786 GiB |
| `ARCONThickClient.msi` | 8 | 0.695 GiB |
| `ARCON RDPS Installer.exe` | 14 | 0.533 GiB |
| `ARCONMacDbeaver.zip` | 1 | 0.368 GiB |

→ [`evidence/E7-ondisk-pack-attribution.txt`](evidence/E7-ondisk-pack-attribution.txt) ·
[`evidence/E4-history-largest-blob-versions.txt`](evidence/E4-history-largest-blob-versions.txt)

**Why re-committing a ZIP costs so much — and this is measured, not theory.** Git delta-compresses
similar objects, but a ZIP is already DEFLATE-compressed, so two builds differing slightly produce almost
entirely different byte streams. `verify-pack` reports whether each object was stored as a delta or whole.
For `ARCONDbeaver.zip`:

```
versions in the main pack : 47
stored WHOLE (no delta base) : 44      <- 93.6%
stored as a delta            :  3
```

**44 of 47 versions are stored in full.** `ARCONDbeaver.zip` averages **229 MB of permanent storage per
commit of that one file.** This is also why compression settings and `gc` cannot help: there is no
redundancy left for git to exploit.

### 4.3 Finding 4 — the inert `/PAM` ignore rule

```
$ sed -n '358,364p' .gitignore
# Fody - auto-generated XML schema
FodyWeavers.xsd
/PAM                       <- line 363

$ git ls-files PAM/ | wc -l
17872
```

Appended after a stock Visual Studio `.gitignore` template. It has no effect on the 17,872 already-tracked
files, and misleads anyone reading it. → [`evidence/E6-gitignore.txt`](evidence/E6-gitignore.txt)

### 4.4 Findings 5–6 — duplication in the checkout

| Total | Copies | Distinct SHAs | File |
|---:|---:|---:|---|
| 1,134.9 MB | 3 | **1** | `ARCONMacDbeaver.zip` *(identical — git stores once)* |
| 593.3 MB | 45 | **45** | `msedgedriver.exe` *(45 different versions)* |
| 480.1 MB | 2 | 1 | `ARCONDbeaver.zip` |
| 377.1 MB | 16 | 2 | `avcodec-57.dll` |
| 201.7 MB | 6 | 2 | `oraociicus11.dll` |

The `distinct SHAs` column is the one that matters: identical copies are cheap in `.git` and expensive in
every checkout; **distinct versions are expensive in both.**
→ [`evidence/E2-head-tree-composition.txt`](evidence/E2-head-tree-composition.txt)

### 4.5 Findings 8–9 — why it cannot shrink, and keeps growing

```
$ git rev-list --all --count                                     35602
$ git for-each-ref --format='%(refname)' refs/remotes | wc -l      3326
$ git tag | wc -l                                                   307
$ git log --all --reverse --format='%ad' --date=short | head -1  2021-07-01
```

Five years, 35,602 commits, **3,326 remote branches**. Ongoing inflow, measured on 2026-08-10:

```
$ git pull --ff-only origin 35.8.29_Hotfix
Updating e278fd399..12234f037   Fast-forward
 142 files changed, 6940 insertions(+), 5224 deletions(-)
$ ls -lh .git/objects/pack/pack-e625f4b0*.pack     ->  1.1G
```

**106 commits · 142 files · 1.074 GiB.** Attributing that pack object-by-object shows what was actually
transferred:

| Content | On-disk | Share of the pull |
|---|---:|---:|
| **`ARCONDbeaver.zip` — 3 new versions** | **0.954 GiB** | **88.8%** |
| `SSHLogsConsumerBotInstaller.msi` | 0.034 GiB | 3.1% |
| `graph.json` *(tooling output)* | 0.032 GiB | 3.0% |
| **All C# source in the pull** | **0.008 GiB** | **0.7%** |

**One file was 88.8% of a routine update.** None of those three ZIP versions is in `HEAD` — they arrived
on branches this developer will never check out, and they are now permanent.

---

## 5. Remediation — ordered, with honest risk

⛔ **We have executed none of these.** `pam/` is not our repository.

### 5.1 What will NOT work

**`git gc` / `git repack` will reclaim essentially nothing.** `loose: 0`, `garbage: 0`,
`prune-packable: 0`, and 3,326 refs keep everything reachable — nothing is unreachable to collect.
More fundamentally, §4.2 shows **44 of 47 versions of the largest file are already stored whole because
they cannot be delta-compressed**; there is no redundancy left for a repack to find. Show anyone
proposing "just run gc" both of those measurements.

**There is also no Git LFS and no `.gitattributes` anywhere** — `git ls-files | grep -c '.gitattributes'`
returns **0**, and `.git/lfs` does not exist. The standard mitigation for large binaries was never
adopted, and nothing in the repository constrains binary intake.

### 5.2 Immediate, zero-risk, entirely under a developer's own control

No server change, no permission needed, fully reversible:

```bash
# Blobless clone — full history, file contents fetched on demand
git clone --filter=blob:none https://repo.arconnet.com/root/pam.git

# Shallow clone — for CI, which almost never needs history
git clone --depth 1 --branch 35.8.29_Hotfix https://repo.arconnet.com/root/pam.git

# Sparse checkout — only the sub-tree you work on
git sparse-checkout set PAM/ARCONPAMAPI
```

⭐ **Make `--filter=blob:none` the default clone command for every developer and every CI job.** Since
98.1% of history is binary blobs almost nobody needs, this avoids nearly all of the 27.88 GB transfer
while keeping full history. **Highest value, zero risk, available today.**

### 5.3 Stop the inflow — low risk, needs the repo owner

| Step | Effect |
|---|---|
| Remove the false `/PAM` line; add real rules for `*.zip *.msi *.exe *.dll *.deb *.rpm *.nupkg bin/ obj/ packages/` | Stops new artifacts entering |
| `git rm --cached` the drivers, installers and archives; fetch at build time | Removes them from *future* commits — **history keeps its copies** |
| Delete the misnamed `gitignore`, reconciling its 14 differing lines | Removes a false source of truth |
| **Server-side pre-receive hook rejecting any file over ~10 MB** | The only durable fix — prevents recurrence |

### 5.4 Reclaim the 27.88 GB — high risk, org-wide coordination

Both options **rewrite every commit SHA**:

| Option | Effect | Cost |
|---|---|---|
| **`git filter-repo`** purging archives + installers | Removes `.zip`/`.msi`/`.exe`/`.deb`/`.rpm`/`.pkg` from all history. **Measured target: 26.79 GiB → ~1.3 GiB** (removing 21.58+1.85+1.23+0.44+0.21+0.17 GiB) — a **~95% reduction** | Every SHA changes; every clone re-made, every open MR rebased, tags re-signed, pinned CI SHAs updated |
| **Git LFS migration** (`git lfs migrate import --include="*.zip,*.msi,*.exe"`) | Binaries become LFS pointers; history keeps its shape | Same rewrite cost, plus LFS server storage/quota and every developer installing LFS |

Unlike the earlier estimate, the ~1.3 GiB figure is **arithmetic on measured on-disk pack bytes**, not on
logical sizes — though only a rehearsal on a clone can confirm it exactly.

**Recommendation:** adopt §5.2 today; propose §5.3 to the product team this week; treat §5.4 as a planned
maintenance event with a scheduled freeze — never opportunistically.

---

## 6. Limits of this analysis

- **§2.1, §4.2 and §4.5 figures are true on-disk packfile bytes** from `git verify-pack -v`. **Both packs
  are now attributed** (26.790 + 1.074 = 27.864 GiB), reconciling with the 27.88 GB filesystem figure.
- Figures labelled *logical* (finding 7, `AllSupportingDLLs` 18.02 GiB) are uncompressed content sizes and
  will be **smaller on disk**. They are used only where on-disk attribution was not computed per-directory.
- The ~1.3 GiB post-purge target assumes those extensions are purged from **all** refs and that no other
  large object class emerges; it is arithmetic, not a trial run.
- Per-branch unique content was not measured — 3,326 refs makes that expensive.
- ⚠️ **A correction made during this work:** an earlier pass parsed `git ls-tree -l` with whitespace
  splitting. Git separates the path with a **tab**, and many paths here contain spaces, so filenames like
  `ARCON PAM.msi` were truncated to `ARCON` — fabricating a phantom "251 copies of ARCON" finding and
  skewing the extension table. All tables here are re-derived with tab-aware parsing. The regeneration
  scripts in this folder use the corrected method.

## 7. Reproducing this

Read-only, from `pam/`:

```bash
git count-objects -vH
git ls-tree -r -l HEAD > headtree.txt
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' > objsizes.txt
git verify-pack -v .git/objects/pack/pack-<sha>.idx > verifypack.txt
```

Then, from this folder:

```bash
python regenerate-pack-attribution.py    # §2.1, §4.2 — authoritative on-disk figures
python regenerate-head-analysis.py       # §2.2, §4.4 — checkout composition and duplication
python regenerate-history-analysis.py    # logical-size history tables
```
