# Token Check — week ending 2026-06-11

*Example report shape — anonymized from a real weekly check after adopting Action Card habits.*

## Headline

- Total tokens this week: **141 M** (baseline weekly avg: 393 M) — **64% below baseline**
- **Cache-read volume: 127 M** this week (baseline: ~364 M/week) — **65% below baseline**
- **Cache-read per event: 297 K** (baseline: ~807 K) — **63% below baseline**
- Opus-variant share: **51%** (baseline: 99.5%) — inflated by one pre-change day (Jun 4); **26% since Jun 5**

Token-action habits are working. Total volume and cache-read *volume* are down sharply. Three days in the window were zero-Opus. The lightest day hit 7.4 M cache-read, 137 K/event.

## Wins

- **Cache-read per event: 297 K** vs baseline 807 K — threads are ~3× shorter on average
- **Cache-read per active day: 25 M** vs baseline 73 M — **65% down**
- **Lightest day:** 7.4 M cache-read, 137 K/event (best in the window)
- **Post habit-change:** cache-read per event **223 K**; several all-Composer days
- **Weekly total 141 M** vs 393 M baseline — largest single win
- **Max Mode: 0** | **On-Demand: 0** in the rolling week

## Watch items

- **One pre-change day still in the 7-day window** — drops off next Friday; expect headline numbers to improve further.
- **Transition day** — higher volume than other post-change days; normal when habits are new.

## Cache-read (volume focus)

| Metric | This week | Baseline | Change |
|--------|----------:|---------:|-------:|
| Cache-read tokens (week) | 127 M | ~364 M | **−65%** |
| Cache-read per event | 297 K | ~807 K | **−63%** |
| Cache-read per active day | 25 M | ~73 M | **−65%** |
| Lightest day | 7.4 M cache-read | — | 137 K/event |

*Cache-read share: ~90% (baseline 92.7%). Normal for Agent threads — track volume, not this ratio.*

## Flags

- Thinking-variant events: **64** in rolling week (**37** post-change — rare/intentional)
- Max Mode events: **0** (target: always 0)

## Recommendation for next week

1. **Keep the Composer-default pattern** — Opus only for real reasoning.
2. **Re-export CSV on your check day** — stale pre-change days roll off the window.
3. **Split threads at ~50K** if a task is still going — `/diary` mid-task beats a 30-turn marathon.
