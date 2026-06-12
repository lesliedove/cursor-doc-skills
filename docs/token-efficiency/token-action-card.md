# Token Action Card — Leslie

*One page. Stick it on the monitor. When Cursor flips to usage-based pricing, you're already trained.*

## The one rule

**92.7% of your tokens are cache-reads** — the model re-reading the same thread over and over. Short threads + small contexts + cheap models = the whole strategy.

## Pick the model on purpose

| If the task is... | Use | Don't use |
|---|---|---|
| Read / format / grep / move files | gemini-2.5-flash | Opus anything |
| Cherry-pick, mechanical commits, PR descriptions, RIL/KIL drafting | composer-2.5 | Opus thinking |
| Doc edits (DITA tags, XML tweaks) | composer-2.5 | Opus thinking |
| Multi-file refactor, debug, "figure out why X" | claude-4.6-opus-high (no thinking) | Opus *thinking* |
| Genuinely stuck on a hard reasoning problem | opus-thinking-xhigh | — |

You spent 99.5% of last month on Opus variants. Most of that work didn't need Opus.

## Habits (in order of impact)

1. **Close threads the second a task is done.** `/diary` (write), then close the tab. One command — not `/diary` *and* `/close`. Don't keep threads open "for later."
2. **One task = one thread.** New question = new chat. Cheap to bootstrap, expensive to keep alive.
3. **If a thread crosses ~50K tokens, split it.** Save state, start fresh.
4. **Don't @-mention whole files.** Mention the function. Better yet, let the agent grep.
5. **Never enable Max Mode.** (You're already not — keep it that way.)
6. **Skills > re-explaining.** Every "let me tell you again how X works" is a skill candidate.

## Free stuff (per GHCP docs — Cursor likely the same)

- Inline tab-completion / next-edit suggestions are **not** billed.
- Type a comment, let autocomplete finish the line — costs nothing.

## When Cursor flips to UBP — playbook

- First day: do **not** use Opus until you've checked the budget meter.
- Default to composer-2.5 for the morning routine (standup, recap, ticket fetches).
- Reserve one "Opus session" per day for the actual hard work.
- Watch for the additional-funds portal announcement (Daniel Cohen, GHCP channel).

## Red flags to catch yourself on

- "I'll just keep this thread open while I work on the other thing" → no, close it.
- "Let me @-mention these 8 files for context" → pick 1.
- "I'll use thinking mode just to be safe" → no, use it when you're actually stuck.
- "It's a tiny edit, model choice doesn't matter" → on a 200K-token thread, the model rereads all 200K. It matters.

## If GHCP is any guide

Synopsys flipped GHCP to AI Credits on **June 1**. Users were getting blocked **within 4 hours**. Default $10/user, agent mode would burn it in less than a day. Ashok Nagaraj got 4 days by routing routine work to gpt-5-mini and never using Opus.

Same playbook works here.

---

*Companion to: [token-budgeting-companion.md](token-budgeting-companion.md) (full version with data and sources).*
