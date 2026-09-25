# Layer 1 — Architecture (SOPs)

Technical Standard Operating Procedures, written in Markdown. One file per capability.

Each SOP defines:
- **Goal** — what this capability achieves
- **Inputs** — parameters and their shapes
- **Logic** — the deterministic step sequence
- **Edge cases / learnings** — accumulated failure knowledge
- **Output shape** — cross-reference to the schema in `LLM.md` §3

> **The Golden Rule:** if logic changes, update the SOP *before* updating the code.
>
> **Self-annealing:** when a tool in `tools/` fails, the fix is not complete until the
> matching SOP here records the learning, so the error cannot repeat.

_Empty — SOPs are authored during Phase 3 (Architect)._
