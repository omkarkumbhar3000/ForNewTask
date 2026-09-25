# DevProjects Control Center — the decision frontend for `engage`

**`OBJ-027`** · React + Vite · light theme only · **Audience:** the workspace owner

```
engage discovers and analyses  →  this UI presents decisions
→  the owner approves          →  engage executes safely
```

`engage` keeps the intelligence. This app does not re-derive anything and does not decide
anything — it renders what `engage` measured, collects choices, and hands approved actions
back for execution.

---

## 1. Running it

```powershell
python tools\control_center.py --open      # serve + open the tokenised URL in the browser
python tools\control_center.py --read-only # serve, but refuse /api/execute entirely
python tools\control_center.py --selftest  # 19 guard checks, opens no socket
```

The server prints a URL carrying a **one-off token**. Open that URL — the page refuses to
work without it, and says so rather than failing blankly.

Rebuild the UI after changing anything under `src/`:

```powershell
cd tools\control-center
npm install
npm run build          # emits dist/, which control_center.py serves
npm run dev            # or vite on :5175 for iteration
```

---

## 2. ⛔ Security posture

**The frontend is a decision interface, never a security boundary.** Assume every request
is forged; nothing in the server trusts the browser.

| Guard | How |
|---|---|
| **No command ever crosses the wire** | The browser sends an action *type* plus a target. Both are looked up in `ACTIONS` in `control_center.py`. There is no code path from request data to a shell string |
| **Server-side whitelist** | Three action types exist: `repo.pull_ff_only`, `data.refresh`, `decision.note`. Anything else is refused **by name**, so a forged request produces an audit line rather than a silent no-op |
| **Absent on purpose, and staying absent** | push · merge · rebase · reset · checkout · clean · stash · conflict resolution · credential edits · deletion · anything issuing product HTTP |
| **Existing policy is reused, never widened** | Every git action goes through `engage_core.run_git` (its own allow-list) and `engage_core.policy_for` (per-repository rights, `D28`). If the CLI would refuse it, so does this |
| **Plans are re-derived at execute time** | The server recomputes whether a pull is safe instead of trusting what the page was showing. A tree that went dirty after render cannot be pulled over |
| **Loopback only** | Bound to `127.0.0.1`, not configurable. Verified with `netstat` |
| **Per-process token** | Random, required on every request, in memory only — never written to disk, so it cannot outlive the server that issued it |
| **Zero product HTTP** | The server has no HTTP client at all. It cannot reach `/arcontoken` or the API suite even by mistake |

⚠️ **Safe-by-default rather than deny-by-default**, extending `D31`'s reasoning from
`engage` to its frontend. Starting the server executes nothing. Every action it can perform
is non-destructive by construction. The `--execute` convention that guards the rest of
`tools/` guards scripts that can issue HTTP to a shared environment; this one cannot.

---

## 3. The views

| View | State | Data source |
|---|---|---|
| **Overview** | ✅ Substantive | `summary`, `attention`, `drift`, `scheduled_tasks` |
| **Applications** | ✅ Substantive | `repositories[]` — state, policy, commits, local changes, and the pull action *only* where `engage` decided a fast-forward is safe |
| **Pending tasks** | ✅ Substantive | `open_objectives`, `resume_points`, `todos`, filterable by type and priority |
| **Approvals** | ✅ Substantive | Everything flagged `needs_confirmation`, plus the rest of the attention list |
| **Recommendations** | 🟡 Partial | `recommended[]` is shown verbatim, plus the decision vocabulary and the live action whitelist. ⚠️ `engage` does not tag its recommendations individually as fact-vs-suggestion, so they are labelled as a group. Inferring the split here would be fabrication |
| **History** | 🟡 Partial | ⚠️ `engage` **overwrites** its context every run by design, so there is no archive of past analyses to show. What accumulates is this app's two append-only journals, starting from first use |
| **Execution results** | ✅ Substantive | The last `engage` steps plus the outcome of the batch you submitted, with **refusals shown separately from failures** — a refused action did not go wrong, it was never allowed |

---

## 4. Decision memory — what each verb commits you to

Every verb has defined behaviour, because otherwise *ignore* quietly becomes *never show me
this defect again*.

| Verb | Behaviour |
|---|---|
| `accept` / `approve` | Execute now. `approve` is used where the item needed explicit confirmation |
| `reject` | Do not execute. Recorded, offered again next run |
| `ignore_once` | Skip **this run only**. Reappears next time, unchanged |
| `consider_next` | Do not execute now; resurface next run, marked *carried over* |
| `not_interested` | Suppress **until the underlying condition changes** |
| `defer` · `review` | Carried forward with a note / flagged for manual inspection |
| `always_ask` | Require approval every run. The default |
| `always_approve` | ⛔ Granted **only** to an action type declared both reversible and safe. Refused otherwise — a potentially destructive operation must never become silently automatic |

**How `not_interested` expires.** Each item carries a **fingerprint** of its material state.
A suppression only matches while the fingerprint matches, so the moment the facts move the
item reappears — flagged *reappeared* rather than surfacing as if it were new. This is the
same mechanism the drift loop uses for waivers, where a waiver is keyed to the evidence hash
it was granted against. **Nothing important can be permanently buried by one dismissal.**

---

## 5. Design

Joins the existing dashboard system rather than starting a second one. `styles.css`,
`router.js`, `Card`, `DataTable` and `States` are shared with `tools/dashboard/`; every
Control Center style is built on that file's `:root` tokens with **no new colour literals**.
Light theme only, as declared there.

Status colour is never the only signal: every severity chip carries its word, and every
execution result carries a glyph and a reason — red/green alone collapses under deuteranopia.

⚠️ `format.js` is deliberately **not** shared. See its header: the two dashboards are fed
opposite data contracts (0–100 versus 0–1 fractions), so a shared `pct()` would silently
rescale one app by 100×.

---

## 6. Extending it

| To add… | Change |
|---|---|
| A new executable action | One entry in `ACTIONS` in `control_center.py`, with its `(handler, reversible, safe, auto-approvable)` flags. `audit_action_table()` refuses to start the server if the flags are inconsistent |
| A new item source | One function in `src/utils/items.js` returning items with a `key` and a `fingerprint` |
| A new view | One file in `src/pages/`, one row in `NAV` in `Shell.jsx` |

⛔ **Do not widen the whitelist to make the UI more capable.** If an action is not safe
enough for `engage`, it is not safe enough here — this server is downstream of that
decision, not a way around it.

**After changing either side, run both self-tests:**

```powershell
python tools\control_center.py --selftest   # 19 checks
python tools\engage_selftest.py             # 57 checks
```
