# Token Efficiency — Reference Docs

*Leslie Poff, Staff Engineer — prepared after the June 2026 "How I AI" session with Jason Kaiser*

Synopsys flipped GitHub Copilot to usage-based (token) pricing on **June 1, 2026**; Cursor is expected to follow. These docs turn usage data and GHCP channel experience into habits you can adopt before the billing model changes.

## Start here

| Doc | What it is | Read when… |
|-----|------------|------------|
| [**Token Budgeting Companion**](token-budgeting-companion.md) | Full analysis with Leslie's CSV data, ranked strategies, sources | You want to understand *why* the habits matter |
| [**Work Summary**](token-efficiency-work-summary.md) | How the habit stack fits together (skills, rules, worklog split, measurement) | You're presenting at How I AI or onboarding a teammate |

## The headline number

**92.7% of tokens in the baseline window were cache-reads** — the model re-reading the same thread, not reasoning or output. Short threads, small contexts, and cheaper models for routine work attack that directly.

## Cursor skills (installable packages)

These implement the patterns described in the work summary. Source and zips live under [`packages/`](../packages/):

| Package | What it does | Install |
|---------|--------------|---------|
| [**`token-workflow`**](../packages/token-workflow) | Plan multi-phase ticket work into short threads with scratch handoffs (`/token-workflow <ticket-id>`) | Drag `dist/token-workflow.zip` into Cursor → "Add as global skill" |
| [**`token-check`**](../packages/token-check) | Weekly health check against your frozen baseline (`/token-check`) | Same |

Each package has a `README.md` with config steps. **`token-check`** needs a one-time `config.json` (copy from `config.example.json`) with **your** baseline numbers — the example values are illustrative, not universal.

## Cursor rules (always-on guidance)

| Rule | What it does | Install |
|------|--------------|---------|
| [**`token-budget.mdc`**](../rules/token-budget.mdc) | Ambient coaching — thread-close reminders, model routing, no speculative `@`-mentions | Copy to `%USERPROFILE%\.cursor\rules\` and set `alwaysApply: true` (see [rules/README.md](../rules/README.md)) |

This is **Part 2** of the habit stack in the [Work Summary](token-efficiency-work-summary.md). The rule turns the companion habits into ambient coaching without re-explaining the 92.7% cache-read number every session.

## Origin

Written June 2026 from Leslie's Cursor team-usage CSV, the Synopsys GHCP Usergroup channel, and the biweekly Corporate Doc "How I AI" meeting. Internal Synopsys use — same sharing posture as the rest of [cursor-doc-skills](../../README.md).
