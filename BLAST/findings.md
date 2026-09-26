# Findings — Research, Discoveries, Constraints

> Append-only research log. Everything learned about APIs, data shapes, rate limits and edge cases lands
> here before it hardens into `LLM.md` or an `architecture/` SOP. Project-specific findings from the
> retired PAM runs (F1–F20) are in git at `2a3298d:BLAST/findings.md`.

---

## Verified environment

Measured on the D: machine during `OBJ-031`. Re-measure on any other machine.

- **Node.js v24.16.0**, npm 11.13.0: native `fetch`, native `--env-file`, ESM auto-detected. No `dotenv`,
  no `axios`, no build step required.
- **Python:** only `python3.11` (3.11.9, uv-managed, no packages) works. `python`, `python3` and `py` are
  Microsoft Store stubs or absent. The toolkit's packages go in a venv (`tools/requirements.txt`).
- **Windows PowerShell 5.1** is the primary shell; Git Bash is available. Git 2.55, Git LFS 3.7.1.
- Platform: Windows 11.

## Platform gotcha — Windows + Node + fetch ⚠️

_Found the hard way during the framework trial. Applies to any HTTP tooling built with Node._

Calling `process.exit()` after an awaited `fetch` aborts the process with a libuv assertion —
`!(handle->flags & UV_HANDLE_CLOSING)`, `src\win\async.c:94` — and exit code **127**, even when the HTTP
request fully succeeded. Undici's keep-alive socket is still closing when the runtime is torn down.

**Rule:** set `process.exitCode` and let the event loop drain. Never call `process.exit()` in a script that
has made an HTTP request.

## Platform gotcha — console encoding ⚠️

A Python child process with no console picks the Windows ANSI codepage and crashes on the first non-ASCII
character it prints. Every script reconfigures stdout/stderr to UTF-8, and a Bash run sets `PYTHONUTF8=1`.
In a Windows `set`, quote the assignment (`set "PYTHONUTF8=1"`): `set PYTHONUTF8=1 && …` captures the
trailing space and Python rejects the value `"1 "`.

## Platform gotcha — hook commands ⚠️

Claude Code runs hook commands through a POSIX shell, which expands `$variables` before PowerShell sees
them. Inline `-Command` payloads therefore break; a hook invokes a `-File` wrapper script instead
(`hooks/inject-objective.ps1`). Every hook failure mode is silent by construction (`Test-Path`,
`2>/dev/null`, `|| true`), so a hook is verified by running its command and parsing the JSON it prints.

## GROQ API — verified in the framework trial

- OpenAI-compatible: `POST https://api.groq.com/openai/v1/chat/completions`, `Authorization: Bearer <key>`,
  body `{ model, messages, response_format, temperature }`.
- JSON mode (`response_format: {type:"json_object"}`) reliably returns parseable JSON.
- `openai/gpt-oss-120b` on the free tier responded in ~2s for a ~400-char prompt. The free tier can return
  HTTP 429 under load — surface it rather than swallowing it.
- `node --env-file=.env` strips surrounding quotes automatically. The flag must be on every run command.

## Patterns that proved out

- **Deterministic boundary works.** The model returns JSON only; code renders the document. Zero formatting
  drift across runs, and the renderer is independently testable.
- **Defensive normalization is worth it.** Filtering non-string array members and defaulting missing keys
  turned schema drift into degraded output instead of a crash.
- **Reconciliation is not validation.** Re-running a generator reproduces its own rule, so a rule that is
  correctly implemented and wrongly named reconciles perfectly. Only an independent re-derivation from the
  source data catches it, and a validator is trusted only after it has been seen to fail.
- **A whole-file write can destroy authored text.** `write_text` truncates before it encodes, so an
  encoding error leaves the file empty. Markdown is edited in place with targeted edits.
