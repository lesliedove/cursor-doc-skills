# Token Efficiency — Reference Docs

*Leslie Poff, Staff Engineer — prepared after the June 2026 "How I AI" session with Jason Kaiser*

Synopsys flipped GitHub Copilot to usage-based (token) pricing on **June 1, 2026**; Cursor is expected to follow. These docs turn usage data and GHCP channel experience into habits you can adopt before the billing model changes.

## Start here

| Doc | What it is | Read when… |
|-----|------------|------------|
| [**Token Action Card**](token-action-card.md) · [PDF](token-action-card.pdf) | One printable page — model picks, six habits, red flags | You want something to pin on the monitor |
| [**Token Budgeting Companion**](token-budgeting-companion.md) | Full analysis with Leslie's CSV data, ranked strategies, sources | You want to understand *why* the habits matter |
| [**Work Summary**](token-efficiency-work-summary.md) | How the habit stack fits together (skills, rules, worklog split, measurement) | You're presenting at How I AI or onboarding a teammate |
| [**Sample weekly check**](token-check-2026-06-11.md) | Example output from `/token-check` after one week of new habits | You want to see what "good progress" looks like |

## The headline number

**92.7% of tokens in the baseline window were cache-reads** — the model re-reading the same thread, not reasoning or output. Short threads, small contexts, and cheaper models for routine work attack that directly.

## Related Cursor skills (not in this folder)

These live in personal `~/.cursor/skills/` installs today; they implement the patterns described in the work summary:

- **`token-workflow`** — plan multi-phase ticket work into short threads (`/token-workflow <ticket-id>`)
- **`token-check`** — weekly health check against a frozen May 2026 baseline (`/token-check`)

If those get packaged for this repo later, they'll land under [`packages/`](../packages/).

## Origin

Written June 2026 from Leslie's Cursor team-usage CSV, the Synopsys GHCP Usergroup channel, and the biweekly Corporate Doc "How I AI" meeting. Internal Synopsys use — same sharing posture as the rest of [cursor-doc-skills](../../README.md).
