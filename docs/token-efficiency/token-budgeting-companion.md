# Token-Budget Companion — Preparing for Cursor's Switch

**Source:** "How I AI" 2026-06-05 with Jason, plus the Synopsys GitHub Copilot Usergroup channel and your own Cursor team-usage CSV.

> **Why this matters now:** Cursor is expected to follow GitHub Copilot's billing change to usage-based (token-based) pricing. We don't have a date, but Synopsys-side GHCP made the cutover on **June 1, 2026** — and people in that channel were getting blocked **within 4 hours of the cutover**. We want to be ready before the same thing lands in Cursor.

---

## 1. The two pricing models, in plain English

### Request-based pricing (what we have now)

You're billed per **interaction**, regardless of how big or small it is.

- A "request" = one round-trip you ask the model to do. Cursor's "Premium Request" was the unit.
- Your plan gives you a fixed number of premium requests per month (e.g., 500). After that you're either blocked, throttled, or charged per overage request.
- **A 30-line file edit and a 30-page refactor cost the same.** That's why it felt unlimited.
- Strategy under this model: *don't worry about how much context you load — just don't make a million separate requests.*

### Usage-based / token-based pricing (where Copilot just landed; Cursor next)

You're billed per **token** the model reads and writes. Tokens ≈ word fragments.

- Every token in the conversation **counts every turn the model thinks**. If you have a 100K-token conversation and ask one tiny question, you're paying for the model to re-read all 100K tokens to answer.
- Four token "buckets" exist on the bill (you'll recognize them from the Cursor CSV):
  - **Input (without cache write)** — fresh context the model is reading for the first time.
  - **Input (with cache write)** — context the model is reading *and* saving so the next turn can read it cheaper.
  - **Cache read** — re-reading already-saved context. Roughly **10% of input price** at Anthropic, but volume usually swamps this.
  - **Output** — what the model writes back. This is the most expensive per-token bucket.
- A 30-line edit on a thread that already has 200K tokens of context is **way more expensive** than the same edit on a fresh thread.
- Strategy under this model: *short threads, small contexts, cheaper models for routine work, big models reserved for actual reasoning.*

### So why is this scary?

- **Default behavior is the trap.** The way most of us use Cursor today (long-running threads, Opus-high-thinking by default, lots of @-mentioned files) is the most expensive way to use a token-priced product.
- The folks in the Copilot channel went from "unlimited" to "blocked at 25% of the day" because their habits were tuned to the old model. Quote from Chad Kasell on the channel: *"If trying to use in Agent Mode, you are likely to peel through all AI Credits in less than 1 day."*

---

## 2. What your own usage looks like right now

From `team-usage-events-10336957-2026-06-05.csv` (the file labeled "(1)" was a duplicate — same hash). Window: **2026-05-01 → 2026-05-21** (3 weeks, 15 active days).

| Metric | Value | Notes |
|---|---|---|
| Total tokens | **1,178,720,551** | ~1.18 B |
| Total events | 1,355 | |
| Included | 662,712,636 tokens (682 events) | the "free" tier portion |
| On-Demand | 509,987,600 tokens (669 events) | already overflowing |
| Errored / no charge | 6,020,315 tokens (4 events) | |
| Max Mode | **Never used** (good — Max Mode is a token bomb) | |

### Where the tokens actually went

| Bucket | Tokens | Share |
|---|---|---|
| **Cache Read** | 1,092,859,347 | **92.7%** |
| Input (with cache write) | 55,540,335 | 4.7% |
| Input (no cache) | 22,434,206 | 1.9% |
| Output | 7,886,663 | 0.67% |

**The single most important number on this page:** 92.7% of every token spent was the model re-reading the same conversation context. That's the lever. If we could halve average thread length, we could roughly halve the bill — output and fresh input are basically rounding errors.

### Where the tokens went, by model

| Model | Events | Total Tokens |
|---|---:|---:|
| claude-4.6-opus-high | 767 | **795,064,363** |
| claude-opus-4-7-thinking-xhigh | 130 | 265,178,643 |
| claude-4.6-opus-high-thinking | 123 | 111,812,718 |
| composer-2-fast | 4 | 6,149,352 |
| gemini-2.5-flash | 331 | 515,475 |

99.5% of your tokens are on Opus variants. Gemini Flash had 331 events for ~0.5M tokens — i.e., **640× cheaper per event** than Opus on average. There is real room to shift work down.

### Daily peaks

Worst day in the window: **2026-05-12 — 162M tokens in one day** (135 events, ~1.2M tokens/event average). That day alone is roughly the entire monthly budget at Synopsys's current GHCP $10/user cap.

---

## 3. Strategies, ranked by impact for *your* workflow

I've ordered these by *expected savings × ease for you to actually do it*. The top four are where the real money is.

### Tier 1 — Highest impact, lowest cost to adopt

#### 1. Close threads aggressively. Stop letting them grow.

This is the single biggest win because of the 92.7% cache-read figure.

- Use `/diary` the second a task is done, then close the tab — one command, not `/diary` *and* `/close`. Don't leave the thread open for "the next thing."
- Each new task = new thread. Cheaper to re-bootstrap with a skill than to keep paying cache-read on 500K stale tokens.
- When a thread crosses ~50K tokens, ask whether it should be split. If yes, save state via `/diary`, start fresh.
- Already-running long threads: when you don't need full history, ask the agent to **compact** before continuing.

**How to do it:** habit change + Friday's `/close` already does this for you. Just *use it more*.

#### 2. Match the model to the task

You ran 99% of work on Opus. Most of what we do daily does not need Opus.

| Task type | Suggested model | Why |
|---|---|---|
| File reading, formatting, grep, simple edits | `gemini-2.5-flash` or `composer-2.5` | 100–600× cheaper per turn |
| Cherry-picks, mechanical commits, PR descriptions | `composer-2.5` | Cursor's own cheap model, decent at structured ops |
| Doc edits (DITA tag adjustments, XML tweaks) | `composer-2.5` or non-thinking Sonnet | No reasoning needed |
| Drafting release notes, RIL, KIL from raw data | non-thinking Opus or Sonnet | Reasoning helps but not deep |
| Multi-file refactors, debugging, ambiguous "figure out why X" | `claude-4.6-opus-high` (no thinking) | Save thinking for actual reasoning loops |
| **Only-when-stuck** investigation | `claude-opus-4-7-thinking-xhigh` | Reserve for the 5% of tasks where it matters |

Ashok Nagaraj on the Copilot channel reported their `$10/user` allocation lasted **4 full days** by routing to gpt-5-mini for PR filing, gpt-5.3-codex for code edits, and Sonnet for "rubber-duck" thinking, never touching Opus 4.6 or GPT-5.5. Same idea applies to Cursor.

**How to do it:** when you start a new chat, pick the model deliberately. Switch mid-thread if the task simplifies.

#### 3. Don't use thinking variants by default

In your CSV, `claude-opus-4-7-thinking-xhigh` was 130 events for 265M tokens — average **2M tokens per turn**. Thinking models stuff a lot of internal reasoning into the cache. Use them only when the question genuinely needs reasoning ("why is this build failing", "design a strategy for X"). Don't use them for "rename this variable."

#### 4. Use skills, not re-explanations

Skills are loaded on-demand and avoid re-pasting the same instructions every thread. Every skill you write once saves you tokens forever.

- This is exactly Jason's strategy: *"introducing skills to reduce token usage."*
- Concretely: every time you find yourself re-explaining something to the agent in chat, that's a candidate for a skill.

### Tier 2 — Real wins, slightly more setup

#### 5. Limit @-context

Each `@file.md` you mention loads the whole file into context — *and that file then gets cache-read on every turn for the rest of the thread*. A 2,000-line file mentioned once costs you ~6K tokens × every turn. Practical rules:

- Mention the smallest unit you can: a function, not the file.
- Don't @-mention "for context" — only when the agent needs to read it.
- Drop big @-context out of the thread once the relevant edit is done (start a new thread).

#### 6. Adopt CLI output trimming (when it lands in Cursor)

The Copilot channel surfaced two of these:

- **rtk** (Rust Token Killer) — a CLI proxy that strips noise from command output before it reaches the LLM. Author claims 60-90% savings on common dev commands. Implemented via hooks; works in Copilot CLI today, not yet in VS Code Preview. ([rtk-ai/rtk](https://github.com/rtk-ai/rtk))
- **VS Code's built-in** `chat.tools.compressOutput.enabled` setting does similar at the editor level.
- Cursor doesn't have an equivalent toggle yet, but Friday's hook system could host an `rtk`-style preprocessor when this matters.

**Why it helps:** terminal commands routinely drop 5–50K tokens of noise into the cache (build logs, `npm install` output, `git status` for huge repos). That noise then cache-reads forever.

#### 7. Sub-agents on cheaper models

Cursor's `Task` tool already supports launching subagents with their own model. Pattern:

- Orchestrator: Opus high (you, planning).
- Subagent for "read 50 files and summarize": composer-2.5 or gemini-flash.
- Subagent for "draft a PR description": composer-2.5.

Pablo Munoz on the channel: *"orchestrating sonnet/gpt5.4 that delegates to gpt5-mini for summarizing reading tasks or delegates to gpt codex models for editing."*

### Tier 3 — Big wins but real engineering effort

#### 8. Knowledge-graph style memory (Graphify / navigational memory)

Karan Bhagat shared **Graphify** ([safishamsi/graphify](https://github.com/safishamsi/graphify)): pre-compute a graph over your codebase + diagrams + docs, then the agent navigates the graph instead of re-reading whole files. Claims up to 70× token reduction on large codebases. Caveat: in Dave Wadkins's benchmark on the channel, Graphify didn't actually win — Serena MCP did better, but Serena got blocked at Synopsys.

Pablo Munoz also pushed an internal alternative: build "navigational memory" via subject-predicate-object triples in a markdown file. Start simple, scale to a SPARQL/Neo4j backend later. Realistic for our doc workflow — the doc repos already have a clear hierarchy that maps cleanly to triples.

This is a real project, not a habit change. Probably worth tracking but not urgent unless Cursor moves to UBP fast.

#### 9. Local models for non-product work

Jason's experiment: **Gemma 12B + Friday Light + clog code as harness** for local agentic tasks without cloud cost.

Channel context (Dave Wadkins): approved local models like Gemma4 are **not** approved for code that ships into product (legal/IP risk on copyright matching). They *are* fine for:

- Plan mode
- Code review
- Debug / profiling
- Reports / research / analysis
- Email drafts

For your work, that's most of it. The blocker is GPU horsepower on your laptop, but it's a real path forward.

#### 10. Synopsys SCS Gateway (for the future)

Gilles Huron mentioned the SNPS Cognitive Service (SCS) Gateway already routes OpenCode requests to open-weight models (Kimi K2.5 is operational), with token-caching and prompt-compression on the roadmap. Not a knob you can turn today, but worth knowing about: there may be an internal "cheap model" route eventually that doesn't burn Cursor credits at all.

### Tier 4 — Things that look like savings but aren't (or are uncertain)

- **Auto-tab completion / Copilot inline suggestions:** per the GHCP docs (Olivier Andrieu cited this on the channel), code completions and next-edit suggestions are **not** billed in AI credits — they remain unlimited on paid plans. So tab-completion isn't the threat. We just don't know yet whether Cursor will treat its inline completions the same way.
- **"Just use Composer for everything":** Composer 2.5 is great for mechanical work, but at Opus quality it'd cost you more rework time than the model savings. Match the model to the task; don't over-rotate.
- **Compaction will save us:** It helps, but it doesn't help enough on its own. The 92.7% cache-read share is mostly *not* from over-long single threads — it's from the fundamental shape of multi-turn agent use. Compaction is a tool, not a strategy.

---

## 4. Concrete plan for you, this week

Without any platform change, just by changing how *you* work:

| When | Action | Expected impact |
|---|---|---|
| Right now | When starting routine work (formatting, file moves, grep, ticket fetches), pick **composer-2.5** or **gemini-2.5-flash** explicitly | 30–60% cost reduction on those tasks |
| Right now | Stop using `claude-opus-4-7-thinking-xhigh` as a default. Reserve for actual reasoning. | 20%+ on monthly bill |
| Right now | `/diary` when a task is done, then close the tab. Don't keep threads open "just in case." | Cuts cache-read meaningfully |
| This week | Audit one or two recurring multi-step tasks (e.g., commit-and-PR flow) for sub-agent opportunities | Sets up for when UBP lands |
| This week | When the corp-install monitor or the standup picks up a routine task, ask Flo to use a cheap model for the read pass | Targeted savings |
| Watching | The "additional funds request portal" mentioned by Daniel Cohen on the channel — when it ships, it's the official route to adjust budget caps | — |
| Watching | Cursor's UBP timing — Jason has no firm date, but expect it. | — |

---

## 5. Open questions to bring back to Jason

These came up while writing this and don't have clean answers yet:

- Will Cursor's "Included" tier under UBP be tokens, requests, or a hybrid? GHCP went straight to AI Credits; Cursor could split.
- Does Cursor's Task tool sub-agent feature charge to the orchestrator or the sub-agent's quota?
- Is there a cache-aware "summarize and discard" affordance in Cursor that we should be using before threads grow?
- When Composer 3 ships (custom XAI-trained Cursor model), what's the token-cost story? Jason said it should "help manage token constraints" — by how much?

---

## Sources

- How I AI meeting 2026-06-05 (Jason Kaiser host)
- Synopsys GitHub Copilot Usergroup Teams channel — General channel, posts from 2026-05-20 to 2026-06-05 (Chad Kasell, Dave Wadkins, Eric Stephan, Karan Bhagat, Pablo Munoz, Ashok Nagaraj, Daniel Cohen, Mehul Mittal, Xiaoli Fu, Tom McCallum, et al.)
- `team-usage-events-10336957-2026-06-05.csv` (the (1) duplicate is byte-identical)
- [GHCP usage-based billing docs](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enter)
- [rtk-ai/rtk](https://github.com/rtk-ai/rtk)
- [safishamsi/graphify](https://github.com/safishamsi/graphify)
- [AI Tools Board Approved List](https://jiradocs.internal.synopsys.com/spaces/GenAICOE/pages/1091121723/AI+Tools+Board+Approved+List)
