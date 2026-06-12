# Token Check — week ending 2026-06-11

*CSV: `team-usage-events-10336957-2026-06-11 (1).csv`*

## Headline

- Total tokens this week: **141 M** (baseline weekly avg: 393 M) — **64% below baseline**
- **Cache-read volume: 127 M** this week (baseline: ~364 M/week) — **65% below baseline**
- **Cache-read per event: 297 K** (baseline: ~807 K) — **63% below baseline**
- Opus-variant share: **51%** (baseline: 99.5%) — inflated by one pre-change day (Jun 4); **26% since Jun 5**

Token-action habits are working. Total volume and cache-read *volume* are down sharply. Jun 8, 9, and 11 were zero-Opus days. Jun 11 is the lightest day in the window (7.4 M cache-read, 137 K/event).

## Wins

- **Cache-read per event: 297 K** vs baseline 807 K — threads are ~3× shorter on average
- **Cache-read per active day: 25 M** vs baseline 73 M — **65% down**
- **Jun 11 lightest day:** 7.4 M cache-read, 137 K/event (best in the window)
- **Post Jun 5:** cache-read per event **223 K**; Jun 8–11 all Composer, zero Opus
- **Weekly total 141 M** vs 393 M baseline — largest single win
- **Max Mode: 0** | **On-Demand: 0** in the rolling week

## Watch items

- **Jun 4 still in the 7-day window** — one pre-change Opus day (43 M cache-read alone). Drops off next Friday; expect headline numbers to improve further.
- **Jun 5 transition day** — 31 M cache-read at 198 K/event; clearly the outlier among post-change days now.

## Cache-read (volume focus)

| Metric | This week | Baseline | Change |
|--------|----------:|---------:|-------:|
| Cache-read tokens (week) | 127 M | ~364 M | **−65%** |
| Cache-read per event | 297 K | ~807 K | **−63%** |
| Cache-read per active day | 25 M | ~73 M | **−65%** |
| Lightest day | Jun 11 — 7.4 M | — | 137 K/event |

*Cache-read share: ~90% (baseline 92.7%). Normal for Agent threads — track volume, not this ratio.*

## Model mix this week

| Model | Events | Tokens | % of week |
|-------|-------:|-------:|----------:|
| claude-opus-4-7-thinking-xhigh | 64 | 72.3 M | 51.3% |
| composer-2.5 | 152 | 68.4 M | 48.5% |
| gemini-2.5-flash | 212 | 0.3 M | 0.2% |

*Since Jun 5: Composer 73.5%, Opus 26.2%, Gemini 0.3%*

## Daily volumes

| Day | Events | Total tokens | Cache-read | Cache/event | Notes |
|-----|-------:|-------------:|-----------:|------------:|-------|
| 2026-06-04 | 52 | 48.0 M | 43.3 M | 833 K | Pre-change; all Opus — rolls off Friday |
| 2026-06-05 | 156 | 34.5 M | 30.9 M | 198 K | Token action card — transition day |
| 2026-06-08 | 96 | 29.6 M | 26.4 M | 275 K | 100% Composer |
| 2026-06-09 | 70 | 20.6 M | 19.0 M | 271 K | 100% Composer |
| 2026-06-11 | 54 | 8.4 M | 7.4 M | **137 K** | Lightest day — habit win |

## Flags

- Thinking-variant events: **64** in rolling week (**37** since Jun 5 — rare/intentional post-change)
- Max Mode events: **0** (target: always 0)

## Recommendation for next week

1. **Keep the Jun 8–11 pattern** — Composer default; Opus only for real reasoning.
2. **Re-export CSV Friday** — Jun 4 drops off the window; rolling totals should look even better.
3. **Split threads at ~50K** if a task is still going — `/diary` mid-task beats a 30-turn marathon.
