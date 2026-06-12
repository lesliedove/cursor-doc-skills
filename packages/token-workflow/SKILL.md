---
name: token-workflow
description: >-
  Plan and run multi-thread, token-efficient ticket workflows. Writes
  workflow.md + worklog.md in scratch, splits work into one phase per chat
  (TDD → fix → ship), and pairs with /diary between threads. Use when the
  user says "/token-workflow", "plan token workflow", "split threads for
  ticket", "token-efficient workflow", or before multi-phase code/parser work
  on composer-2.5 instead of one long Opus thread.
---

# Token Workflow

Split multi-phase ticket work into **short threads** with durable handoffs in scratch. The goal: avoid paying cache-read tax on a growing mega-thread (see `token-budget.mdc` and the `token-check` skill).

**Proven pattern:** DocBook/XML parser fix — plan → failing test → fix → ship across three `composer-2.5` threads. See [example-workflow.md](example-workflow.md).

## When to use

| Use token-workflow | Skip — use ado-doc or a single thread |
|---|---|
| Multi-phase work with natural stop points | One-shot typo or single-file doc edit |
| Code fix needing TDD + implementation + PR | Active debugging (keep one thread until root cause found) |
| Known token traps (huge XML, full corpus rebuild) | Standard DITA/doc pick-up with no special traps |
| Mechanical work on `composer-2.5` | Multi-branch doc cherry-picks where context already loaded |

**Relationship to ado-doc:** `ado-doc` owns the doc edit/commit/PR mechanics. `token-workflow` owns **how many chats** and **what persists between them**. For doc tickets, run `/token-workflow` first when phases or traps warrant splitting; execution threads still follow `ado-doc` for edits and shipping.

## Commands

| You say | Action |
|---|---|
| `/token-workflow 12345` | Plan mode — fetch ticket, write scratch artifacts, print Thread 1 bootstrap |
| `/token-workflow` (no ID) | Plan mode — ask for ticket ID if not obvious from context |
| `run thread N for 12345` | Execution mode — read scratch `workflow.md`, do only phase N, stop at done-when |
| `extend workflow for 12345` | Add phases (e.g. post-merge skill sync) to existing `workflow.md` |

## Planning phase (keep it thin)

Run in **one planning chat** on whatever model the user chose. Do not start Thread 1 in the same chat.

1. **Fetch ticket** — `ado` skill (or your tracker), read title, AC, comments. Note linked investigation scratch (`<scratch_dir>\<other-ticket>-*\investigation.md`).
2. **Map repo** — correct git root (ticket title can mislead; verify before writing paths).
3. **Pick phase pattern** — default for code bugs: **TDD → fix → ship** (3 threads). See [Phase patterns](#phase-patterns).
4. **List token traps** — files not to load whole, builds not to run in-thread, models per phase.
5. **Ensure scratch folder** — `<scratch_dir>\<ticket-id>-<slug>\` per your team's scratch convention. Create `worklog.md` if missing.
6. **Write `workflow.md`** — from [workflow-template.md](workflow-template.md). Include copy-paste bootstrap prompts for every thread.
7. **Seed `worklog.md`** — Status, open items, link to `workflow.md`.
8. **Tell the user:** "Planning done. `/diary`, then close this tab. Open a **new** `composer-2.5` thread and paste the Thread 1 prompt from `workflow.md`."

Default scratch path: `C:\GitRepos\.scratch\` (override in your team's scratch-folder rule if different).

Planning output should fit in scratch — **not** in chat history that execution threads must re-read.

## Execution rules (every thread)

1. **New chat per phase.** Never continue the planning thread for Thread 1.
2. **Bootstrap:** read only `workflow.md` (+ `worklog.md` if resuming mid-ticket). Point at investigation notes; do not re-derive them.
3. **Do not read global `diary.md` backlog** during ticket threads — use ticket-scoped `worklog.md` only (see `diary` skill hybrid model).
4. **Stop at done-when** for that phase. Do not bleed into the next phase.
5. **`/diary`** before the next thread — updates `worklog.md` and optionally rolls up to workspace `diary.md`; then close the tab.
6. **Model:** `composer-2.5` (or `gemini-2.5-flash`) for mechanical phases. Opus/thinking only when genuinely stuck on architecture or ambiguous root cause — and only in that one thread.

## Phase patterns

### A. Code bug (default) — 3 threads

| Thread | Objective | Done when |
|---|---|---|
| 1 — TDD | Branch, failing test/fixture, minimal repro | Test fails for the right reason |
| 2 — Fix | Minimal code change, tests green | All targeted tests pass; no scope creep |
| 3 — Ship | Commit, push, PR, link tracker | PR open; user said "ship it" |

Optional **Thread 4+** (thin, no new workflow doc): post-merge housekeeping, tracker close comment — one prompt each, or folded into a final "we're done" chat.

### B. Doc edit (DITA/DocBook) — 2–3 threads

| Thread | Objective | Done when |
|---|---|---|
| 1 — Edit | Branch, apply AC on first target branch | Diff ready; preview/build if cheap |
| 2 — Ship | Commit, PR, link ticket (ado-doc commitpr) | PR open |
| 3 — Forward | Cherry-pick to release branches (ado-doc cherry) | Only if multi-branch; **separate thread per branch** if diffs are large |

Use when the edit is non-trivial or the book is huge — not for a one-paragraph typo.

### C. Investigation → fix — 2 threads minimum

| Thread | Objective | Done when |
|---|---|---|
| 1 — Investigate | Repro, root cause, write `investigation.md` in scratch | Cause documented; fix approach chosen |
| 2+ | Run pattern A or B from investigation | Per chosen pattern |

If investigation is already done in another scratch folder, **link it in `workflow.md`** — do not re-investigate.

## Model selection

| Phase | Default model | Escalate to Opus/thinking when |
|---|---|---|
| Planning | User's choice | Repo mapping ambiguous, multiple valid architectures |
| TDD / fixture | `composer-2.5` | — |
| Fix / edit | `composer-2.5` | Recursion or parser logic genuinely stuck after one retry |
| Ship | `composer-2.5` | — |
| Investigation | User's choice | — |

Call out model choice in `workflow.md` header.

## Artifacts

| File | Purpose |
|---|---|
| `<scratch_dir>\<ticket-id>-<slug>\workflow.md` | Phases, done-when, bootstrap prompts, token traps |
| `<scratch_dir>\<ticket-id>-<slug>\worklog.md` | Ticket-scoped status; session notes between threads |
| `investigation.md` | Optional; link when prior work exists |

Resolve folder: glob `<scratch_dir>\<ticket-id>-*\`.

## Token traps table (always include in workflow.md)

| Don't | Do instead |
|---|---|
| Load multi-thousand-line source XML/docs whole | Grep line ranges; small test fixture |
| Full corpus / book rebuild in-thread | Targeted pytest or one-topic preview |
| Re-explain prior investigation in chat | `investigation.md` path in bootstrap prompt |
| `@`-mention entire parser/book files | Grep function names; read slices |
| One mega-thread for all phases | One phase per thread, `/diary` between |
| Opus for mechanical fix/commit | `composer-2.5` |
| Auto-read global `diary.md` at thread start | `worklog.md` only |

Add ticket-specific traps (e.g. "do not queue CI build without explicit consent") as rows.

## After the last thread

1. Roll up in `worklog.md` → Status `Shipped` (or `PR open`).
2. `/diary` rolls session to workspace `diary.md` if configured.
3. Optional: spot-checks listed in `workflow.md` — **post-merge, new thread or manual**, not blocking.

## Related

- [workflow-template.md](workflow-template.md) — blank `workflow.md` skeleton
- [example-workflow.md](example-workflow.md) — filled reference from a real parser fix
- `diary` skill — hybrid worklog vs global diary
- `close` skill — optional session end between threads
- `ado-doc` skill — doc edits, commitpr, cherry
- `token-check` skill — weekly habit verification
- `docs/token-efficiency/` in [cursor-doc-skills](https://github.com/lesliedove/cursor-doc-skills) — companion docs and Action Card
