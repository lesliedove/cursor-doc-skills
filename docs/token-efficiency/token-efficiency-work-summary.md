# Token Efficiency Work — Full Summary (2026-06-05)

**Author:** Flo (with Leslie)  
**Context:** Post–How I AI meeting with Jason Kaiser; GHCP at Synopsys flipped to usage-based pricing June 1, 2026 (users blocked within hours). Cursor is expected to follow.  
**Companion docs in this folder:** [token-budgeting-companion.md](token-budgeting-companion.md)

---

## Executive summary

Today we turned Jason's UBP warning and Leslie's own usage data into a **layered safety net**: analysis docs you can read, a one-page habit card you can pin, an always-on agent rule, weekly measurement, daily reminders, thread/workflow patterns proven on a real ticket, and a hybrid diary model so ticket threads stop loading your entire backlog every turn.

The headline from Leslie's May 1–21 Cursor team-usage CSV:

| Finding | Implication |
|---|---|
| **92.7% of 1.18B tokens were cache-reads** | The model re-reading the same thread — not reasoning, not output — is where the money goes |
| **99.5% of tokens on Opus variants** | Most daily work doesn't need Opus; model choice is a huge lever |
| **Thinking models: ~2M tokens/event** | Reserve for genuine stuck-on-a-hard-problem moments |
| **Gemini Flash: 331 events, ~0.5M tokens total** | ~640× cheaper per event than Opus on average |

**The strategy in one sentence:** short threads, small contexts, cheap models for routine work, durable handoffs on disk so you don't pay cache-read tax to keep context in chat.

---

## Part 1 — Starting docs (analysis & habits)

### Token Budgeting Companion (`Token-budgeting-companion-2026-06-05.md`)

Full write-up (~220 lines) synthesizing:

- Request-based vs token-based pricing, in plain English
- Leslie's CSV breakdown (buckets, models, daily peaks — worst day 2026-05-12: 162M tokens)
- Strategies ranked by impact × ease for this workflow
- A concrete "this week" action table
- Open questions for Jason (Included tier shape, sub-agent billing, compaction affordances, Composer 3 cost story)
- Sources: How I AI meeting, Synopsys GHCP Usergroup channel (50+ messages via Graph), GHCP billing docs, community tools (rtk, Graphify)

**Why it helps:** When UBP lands, you won't be reading blog posts under pressure — the analysis is already done, grounded in *your* numbers, with Synopsys-specific context (GHCP channel war stories, Ashok Nagaraj's 4-day/$10 playbook).

### Token Action Card (`Token-action-card-2026-06-05.md`)

One printable page:

- Model-selection table (flash/composer for routine → Opus no-thinking for hard → thinking only when stuck)
- Six habits in impact order (close threads, one task = one thread, 50K split, no whole-file @-mentions, no Max Mode, skills > re-explaining)
- "Free stuff" callout (inline tab-completion unbilled per GHCP docs)
- UBP-day playbook and red-flag self-checks

**Why it helps:** The companion is for understanding; the Action Card is for *doing*. Daily reminders point at it. `/standup` section 13 launches a PDF version in Edge when present (`Token-action-card.pdf` — export from the markdown if you want the auto-launch).

### Meeting notes (`Meeting notes 2026-06-05.md`)

Reformatted from raw dump to structured markdown (decisions, open questions, topic sections, follow-up table).

**Key meeting threads relevant to today's work:**

- Jason: skills reduce token usage; shift routine work to Composer 2.5; token efficiency will matter when subsidy ends
- Jason: `/close` writes diary + indexed summary; compaction improvements + hooks retain skill context after compaction
- Jason: Friday offloads full transcript before compaction so context isn't lost

---

## Part 2 — Always-on rule (`rules/token-budget.mdc`)

New **always-applied** rule so every Flo session nudges token discipline without Leslie re-explaining it. **Repo copy:** [`rules/token-budget.mdc`](../../rules/token-budget.mdc) — install to `%USERPROFILE%\.cursor\rules\` and set `alwaysApply: true`.

| Behavior | Why |
|---|---|
| Suggest `/close` or `/diary` when a task wraps — with explicit "cache-read tax" phrasing | Makes the cost visible at the moment of habit failure |
| Grep/read slices instead of whole files (>500 lines) | Whole files enter cache and re-read every turn |
| Don't propose thinking models for routine work | Thinking variants are 2M tokens/event in the baseline data |
| Call out model mismatch **once** (Opus/thinking + mechanical task → suggest composer/gemini) | Nudge without nagging |
| Sub-agents on `composer-2.5` for read/summarize/format | Orchestrator can stay on Opus; delegates stay cheap |
| Suggest split at ~50K tokens **once per thread** | Long threads compound cache-read |
| Don't @-mention files speculatively | Defensive context loading is expensive |

**Exceptions baked in:** active debugging stays one thread; multi-branch doc cherry-picks stay one thread; never auto-switch models; never refuse Opus when Leslie chose it.

**Why it helps:** Habits decay. The rule turns the Action Card into ambient coaching — Flo says the quiet part out loud once per task wrap instead of Leslie having to remember the 92.7% number.

---

## Part 3 — Weekly measurement (`/token-check` skill)

**Package:** [`packages/token-check`](../../packages/token-check) (shared edition with `config.json`)  
**History dir:** `%USERPROFILE%\.cursor\bot\token-history\` (JSON snapshots per week)

What it does:

1. Leslie downloads latest `team-usage-events-*.csv` from Cursor admin → Downloads
2. Flo runs a PowerShell analysis on the **last 7 days** (doesn't dump CSV into chat)
3. Compares to **frozen baseline** (May 1–21 — do not update without explicit OK)
4. Saves report to `Downloads/How-I-AI/token-check-<date>.md` + JSON snapshot
5. After 4+ snapshots, shows trend section

Metrics tracked: total tokens/week, cache-read %, Opus share, composer+gemini share, thinking events, Max Mode (target: 0).

**Why it helps:** You can't improve what you don't measure. Weekly check is designed to cost ~few tokens itself — analyze in shell, summarize. Wins first, regressions framed as "try this next week."

---

## Part 4 — Daily reminders (June 8–30)

**Location:** Team Charlie `.cursor/reminders.md` — 17 weekday one-time entries.

Progression:

- **Week 1 (Jun 8–12):** deliberate model for `/standup`, close standup thread when done, notice 50K drift, try composer-2.5 once, first `/token-check` Friday
- **Weeks 2–3:** re-read card if drifted, `/close` even when premature, resist whole-file @-mentions
- **Jun 30:** decision point — extend daily nudges or downgrade to Friday-only

**Why it helps:** The Action Card is useless if it's in Downloads and forgotten. Reminders rotate the specific habit of the day so the card doesn't become wallpaper.

---

## Part 5 — Hybrid worklog convention (diary split)

**Problem:** Ticket-focused threads were loading `diary.md` Current Next Steps — dozens of unrelated open items — on every pickup. That's pure cache-read waste.

**Solution — two layers:**

| Layer | Location | When |
|---|---|---|
| **worklog.md** | `C:\GitRepos\.scratch\<ticket-id>-<slug>\` | Ticket threads read/write this only |
| **diary.md** | Team Charlie workspace root | Standup, context switches, `/close` rollup |

### Files updated

| Artifact | Change |
|---|---|
| `C:\GitRepos\.cursor\rules\scratch-folder-naming.mdc` | `worklog.md` required on folder create; template; backfill if missing |
| `~/.cursor/skills/ado-doc/SKILL.md` | Step 1b: ensure scratch folder + worklog before edits |
| `~/.cursor/skills/diary/SKILL.md` | Hybrid read/write table; don't auto-read global diary in ticket threads |
| `~/.cursor/skills/close/SKILL.md` | Roll up worklog → diary on close |
| `~/.cursor/rules/file-output-location.mdc` | Scratch path + worklog note |

**Backfill:** `1462314-nested-sections/worklog.md` created. Remaining scratch folders still need batch backfill (deferred to a fresh `composer-2.5` thread).

**Why it helps:** Ticket thread bootstrap loads ~50 lines of relevant state instead of 1,800+ lines of global backlog. `/close` still gives you the rollup for standup and "where was I."

---

## Part 6 — `token-workflow` skill (multi-phase tickets)

**Package:** [`packages/token-workflow`](../../packages/token-workflow)  
**Invoke:** `/token-workflow <ticket-id>` or "plan token workflow for 12345"

Artifacts per ticket:

- `workflow.md` — phases, done-when criteria, copy-paste bootstrap prompts, token traps table
- `worklog.md` — ticket-scoped status between threads
- `workflow-template.md` — blank skeleton for next ticket
- `example-1462314.md` — filled reference from today's production run

### Phase patterns

| Pattern | Threads | Use when |
|---|---|---|
| **A — Code bug** | TDD → fix → ship (3) | Parser bugs, testable repros |
| **B — Doc edit** | Edit → ship → forward (2–3) | Non-trivial or huge books |
| **C — Investigation** | Investigate → then A or B | Root cause unknown |

### Execution rules

1. **New chat per phase** — never continue the planning thread for Thread 1
2. Bootstrap from scratch files only — not chat history
3. **Don't read diary.md** during ticket threads
4. Stop at done-when; `/close` between phases
5. Default execution model: **`composer-2.5`** (or gemini-flash)

**Why it helps:** Codifies what worked on 1462314 so the next multi-phase ticket doesn't rediscover thread-splitting in an expensive Opus mega-thread. Planning earns its keep once; repeats copy the template.

---

## Part 7 — Proof of concept: ticket 1462314 (full day arc)

Real ticket, real ship, token-efficient pattern end-to-end.

| Thread | Session | Model | Outcome |
|---|---|---|---|
| Plan | `1462314-token-workflow-plan` | (planning) | `workflow.md` written; repo mapped to `llm-doc-converter` not `documentation.git` |
| 1 — TDD | `1462314-nested-sections-tdd` | composer-2.5 | Failing pytest + fixture; no 32K-line XML load |
| 2 — Fix | `1462314-nested-sections-fix` | composer-2.5 | `_emit_section_topics()`; 5 pytest green |
| 3 — Ship | `1462314-nested-sections-ship` | composer-2.5 | PR [#2](https://github.com/lesliedove/llm-doc-converter/pull/2) |
| Post | skill sync, ADO close | thin threads | Skill updated; ticket closed |

**Token traps documented before execution:**

- Don't load `opti_ug_avail_modules.xml` whole (~32K lines)
- Don't rebuild full corpus in-thread
- Link prior investigation (`1462049-osl-investigate/investigation.md`) instead of re-deriving

**Why it helps:** This isn't theoretical — it's the reference implementation that became `example-1462314.md` and informed the `token-workflow` skill.

---

## Part 8 — Screenshot project extension

Screenshot automation is a known token sink (long manifests, VM sessions, image review in chat).

| Deliverable | Location |
|---|---|
| Project-specific workflow doc | `GitRepos/MCoSL_screenshot_project/screenshot_project_T_repo/docs/TOKEN-BUDGET-WORKFLOW.md` |
| `/screenshot-session` skill | `screenshot_project_T_repo/.cursor/skills/screenshot-session/SKILL.md` |

Key patterns: **one thread = one failure cluster**, composer-2.5 default, probe before re-run, gallery not chat for images, offline triage via `_ai_precheck.py`, **Token note:** on scope confirms so Leslie sees *why* one cluster per thread matters.

**Why it helps:** General token rules don't cover repo-specific traps (manifest re-runs, VM menu help). This extends the system where the burn rate is highest.

---

## Part 9 — Standup integration

**`/standup` command** (`Team Charlie/.cursor/commands/create-stand-up-notes.md`):

- **Section 13:** After web dashboard opens, launch Token Action Card PDF in Edge
- **standup.mdc rule:** Lists Token Action Card as a required final section (don't skip)

**Standup thread discipline** (from token-budget-setup session):

- Run `/standup` on Opus **without thinking**
- **`/close` immediately** when morning routine finishes — everything important is on disk
- New thread per midday task
- Fresh "goodnight" thread for end-of-day accomplishments roll-up

**Why it helps:** Standup alone can be a 12-section, high-context thread. Closing it prevents paying cache-read on calendar + reminders + dashboard for the rest of the day.

---

## Part 10 — Hooks (what changed, what didn't)

**No new token-specific hooks were added today.** The existing hook stack still supports the compaction/memory story Jason described:

| Hook | Role | Token relevance |
|---|---|---|
| `pre-compact.ps1` | Saves redacted transcript snapshot before context compaction | Compaction without total context loss — lets you split threads without losing work |
| `load-memory.ps1` | Injects canonical memory files once per session | Avoids re-loading memory every prompt; pairs with diary/worklog on disk |
| `gate-credential-leak.ps1` | Blocks secrets on argv | Indirect — failed redaction → bigger retry threads |

Jason's Friday pattern (offload transcript → compact → retain skill context via hooks) is the **infrastructure** this work assumes. Today's focus was **habits + handoff files + measurement**, not new hook code.

**Watching (not built today):** community tools like **rtk** (CLI output trimming via hooks) and VS Code's `chat.tools.compressOutput.enabled` — noted in companion doc as Tier 2 when Cursor exposes equivalent.

---

## How the pieces fit together

```
┌─────────────────────────────────────────────────────────────────┐
│  UNDERSTAND          Token Budgeting Companion + Meeting notes   │
├─────────────────────────────────────────────────────────────────┤
│  DO DAILY            Token Action Card + reminders + standup    │
│                      close + model choice                      │
├─────────────────────────────────────────────────────────────────┤
│  AMBIENT NUDGE       token-budget.mdc (always-applied rule)      │
├─────────────────────────────────────────────────────────────────┤
│  TICKET WORK         token-workflow → workflow.md + worklog.md   │
│                      ado-doc Step 1b → scratch handoffs          │
│                      /close → diary.md rollup                    │
├─────────────────────────────────────────────────────────────────┤
│  MEASURE             /token-check weekly → How-I-AI reports      │
│                      + ~/.cursor/bot/token-history/            │
├─────────────────────────────────────────────────────────────────┤
│  REPO-SPECIFIC       screenshot TOKEN-BUDGET-WORKFLOW + skill  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Expected impact (honest)

| Lever | Expected savings | Confidence |
|---|---|---|
| Close threads at task done | High — attacks 92.7% cache-read directly | High if habit sticks |
| composer-2.5 / gemini for routine | High on those tasks | High — baseline shows 99.5% Opus |
| Hybrid worklog (no diary load) | Medium per ticket pickup | High — smaller bootstrap context |
| token-workflow (phase split) | High on multi-phase code/parser work | Proven on 1462314 |
| token-budget rule nudges | Medium — prevents drift | Depends on follow-through |
| /token-check | Zero direct savings — enables correction | N/A (measurement) |

**What won't save you alone:** compaction without thread discipline; switching models on a 200K-token thread; thinking mode "to be safe."

---

## Still open (as of end of day)

| Item | Notes |
|---|---|
| Backfill `worklog.md` in remaining `C:\GitRepos\.scratch\` ticket folders | Batch job; use `composer-2.5` |
| First `/token-check` | Fri 2026-06-12 — need fresh CSV from Cursor admin |
| Token Action Card PDF | Local copy in `Downloads/How-I-AI/` (not shipped in this repo) |
| Jun 30 reminder decision | Extend daily nudges or Friday-only |
| Optional 1462314 corpus spot-check | `opti_ug_avail_modules.xml` on next LLM rebuild |

---

## File index (everything touched 2026-06-05)

### This folder (`docs/token-efficiency/`)

| File | Purpose |
|---|---|
| `token-budgeting-companion.md` | Full analysis |
| `token-efficiency-work-summary.md` | **This document** |

### cursor-doc-skills repo (`rules/` + `packages/`)

| Path | Purpose |
|---|---|
| `rules/token-budget.mdc` | Always-applied discipline (install to `~/.cursor/rules/`) |
| `packages/token-check/` | Weekly health check + `config.example.json` |
| `packages/token-workflow/` | Multi-thread ticket planner + template + example |

### Global Cursor config (after install)

| Path | Purpose |
|---|---|
| `~/.cursor/rules/token-budget.mdc` | Always-applied discipline (copy from repo `rules/`) |
| `~/.cursor/skills/token-check/` | Weekly health check skill |
| `~/.cursor/skills/token-workflow/` | Multi-thread ticket planner |
| `~/.cursor/bot/token-history/` | Weekly JSON snapshots (created at runtime) |
| `~/.cursor/skills/diary/SKILL.md` | Hybrid worklog model |
| `~/.cursor/skills/close/SKILL.md` | Worklog rollup |
| `~/.cursor/skills/ado-doc/SKILL.md` | Step 1b worklog |
| `~/.cursor/rules/file-output-location.mdc` | Scratch + worklog paths |
| `~/.cursor/rules/flo.mdc` | token-workflow routing |
| `~/.cursor/skills/flo/SKILL.md` | Skill inventory |

### GitRepos

| Path | Purpose |
|---|---|
| `C:\GitRepos\.cursor\rules\scratch-folder-naming.mdc` | worklog.md convention |
| `C:\GitRepos\.scratch\1462314-nested-sections\workflow.md` | 1462314 phase plan |
| `C:\GitRepos\.scratch\1462314-nested-sections\worklog.md` | 1462314 ticket diary |
| `MCoSL_screenshot_project/.../TOKEN-BUDGET-WORKFLOW.md` | Screenshot token guide |
| `MCoSL_screenshot_project/.../screenshot-session/SKILL.md` | Screenshot session skill |

### Team Charlie workspace

| Path | Purpose |
|---|---|
| `.cursor/reminders.md` | 17 token Action Card reminders (Jun 8–30) |
| `.cursor/commands/create-stand-up-notes.md` | Section 13: Action Card PDF launch |
| `.cursor/rules/standup.mdc` | Token Action Card in required sections |
| `diary.md` | Session rollups for all of the above |

---

*Generated 2026-06-05 by Flo. For the next How I AI: the story is "we didn't just analyze the problem — we built the habit stack, proved it on a shipped ticket, and wired measurement for June."*
