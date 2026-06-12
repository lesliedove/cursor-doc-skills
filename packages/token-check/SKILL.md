---
name: token-check
description: >-
  Weekly token-usage health check. Compares the latest Cursor team-usage CSV
  to a frozen baseline and flags wins/regressions. Use when the user says
  "/token-check", "how am I doing on tokens", "token progress", drops a
  team-usage CSV for review, or on their configured weekly check day.
---

# Token Check

Weekly progress check on token discipline. Designed to take ~2 minutes of the user's time and very few tokens to run.

**Also applies ad-hoc** when the user drops a `team-usage-events-*.csv` path in chat — same reporting rules, same tone.

## Setup (first run only)

Copy `config.example.json` to `config.json` next to this `SKILL.md` and edit:

- **`baseline`** — your frozen comparison numbers from a first usage analysis (see README).
- **`downloads_dir`**, **`report_dir`**, **`history_dir`** — override only if your layout differs.
- **`reference_docs_dir`** — where the companion doc lives on your machine.

See [README.md](README.md) for the full walkthrough.

## When to run

- On your configured check day (`check_day_of_week` in config), or when a workspace reminder prompts you.
- Anytime the user asks "how am I doing on tokens", "token progress", or runs `/token-check`.
- Anytime the user shares a fresh team-usage CSV for evaluation.

## What the user does first

The CSV isn't fetched automatically — Cursor admin doesn't expose a stable API for team-usage events:

1. Tell the user: "Download the latest team-usage CSV from `https://cursor.com/dashboard` → Team → Usage → Export, and drop it in your Downloads folder."
2. Wait for confirmation. Then proceed.

Look for the most recent file matching `team-usage-events-*-*.csv` in `downloads_dir` from config (default `%USERPROFILE%\Downloads\`). If the user names a specific file, use that one.

## Baseline (from config.json)

Read `baseline` from `config.json`. **Do not update the baseline without asking the user** — drift in the baseline hides drift in habits.

Default example values (replace with yours on first setup):

| Metric | Example baseline | Direction we want |
|---|---|---|
| Window | 2026-05-01 → 2026-05-21 | — |
| Total tokens / week (avg) | ~393 M | down |
| Avg tokens / event | ~870 K | down |
| **Cache-read / week** | **~364 M** | **down (primary thread-length lever)** |
| **Cache-read / event** | **~807 K** | **down** |
| **Cache-read / active day** | **~73 M** | **down** |
| Cache-read share | 92.7% | *(informational only — see below)* |
| Opus-variant share | 99.5% | down |
| Composer + Gemini share | <0.5% | up |
| Thinking-variant events | 130 (in baseline window) | down (rare/intentional) |
| Max Mode | 0 events | stay at 0 |

### How to talk about cache-read (required reading before reporting)

**Do not lead with cache-read % or frame ~90% as failure.** Any normal multi-turn Agent thread is 85–95% cache-read by turn 5+. That ratio barely moves when habits improve.

What *does* move — and what hits the bill — is **cache-read volume**:

- **Total cache-read tokens** in the week (and vs baseline weekly)
- **Cache-read per event** — proxy for average thread length
- **Cache-read per active day**
- **Trend on the lightest recent day** — best signal that `/diary` + close is working

Mention cache-read **share** only in a footnote: *"Share still ~90% — expected for Agent mode; volume is what we track."*

Never write "still using nearly 90% on cache-read" as a regression unless **volume** also went up.

## What to compute

For the current CSV's *most recent 7 days*:

1. Total tokens in the week.
2. **Cache-read tokens (absolute)** — total, per event, per active day.
3. **Cache-read vs baseline** — % change on volume metrics (not share).
4. Tokens by `Kind` (Included vs On-Demand vs Errored).
5. Tokens by `Model`, with % share.
6. Average tokens per event.
7. Top 3 days by token volume — and **lightest day** (cache-read volume on that day).
8. Count of events on thinking-variant models.
9. Any Max Mode events (should always be zero).
10. Cache-read share — compute but **do not headline** (footnote only).

If the CSV spans a clear pre/post boundary (e.g. after you adopted the habit stack), also compute a **post-change slice** with the same volume metrics.

## How to compute

Load paths from `config.json`. PowerShell snippet (agent runs this; values from config):

```powershell
$config = Get-Content (Join-Path $PSScriptRoot 'config.json') -Raw | ConvertFrom-Json
$dl = $config.downloads_dir -replace '%USERPROFILE%', $env:USERPROFILE
$csv = Get-ChildItem (Join-Path $dl 'team-usage-events-*.csv') | Sort-Object LastWriteTime -Desc | Select-Object -First 1
$data = Import-Csv $csv.FullName | ForEach-Object { $_ | Add-Member -NotePropertyName _Date -NotePropertyValue ([datetime]$_.Date) -PassThru }
$end = ($data | Sort-Object _Date -Desc | Select-Object -First 1)._Date
$start = $end.AddDays(-7)
$week = $data | Where-Object { $_._Date -ge $start -and $_._Date -le $end }

function Sum-Long($rows, $col) { ($rows | ForEach-Object { [long]$_.$col } | Measure-Object -Sum).Sum }

$totalTokens = Sum-Long $week 'Total Tokens'
$cacheRead   = Sum-Long $week 'Cache Read'
$events      = $week.Count
$activeDays  = ($week | Group-Object { $_._Date.ToString('yyyy-MM-dd') }).Count

$cachePerEvent = if ($events) { [math]::Round($cacheRead / $events) } else { 0 }
$cachePerDay   = if ($activeDays) { [math]::Round($cacheRead / $activeDays) } else { 0 }
$cacheShare    = if ($totalTokens) { [math]::Round(100.0 * $cacheRead / $totalTokens, 1) } else { 0 }

$bl = $config.baseline
$baselineWeeklyCache = $bl.cache_read_weekly
$baselineCachePerEvent = $bl.cache_read_per_event
$baselineCachePerDay = $bl.cache_read_per_active_day

$byModel = $week | Group-Object Model | ForEach-Object {
  [pscustomobject]@{
    Model = $_.Name
    Events = $_.Count
    Tokens = Sum-Long $_.Group 'Total Tokens'
  }
} | Sort-Object Tokens -Descending

$byDay = $week | Group-Object { $_._Date.ToString('yyyy-MM-dd') } | ForEach-Object {
  $dayTokens = Sum-Long $_.Group 'Total Tokens'
  $dayCache  = Sum-Long $_.Group 'Cache Read'
  [pscustomobject]@{
    Day = $_.Name
    Events = $_.Count
    Tokens = $dayTokens
    CacheRead = $dayCache
    CachePerEvent = if ($_.Count) { [math]::Round($dayCache / $_.Count) } else { 0 }
  }
} | Sort-Object Day

$thinkingEvents = ($week | Where-Object { $_.Model -match 'thinking' }).Count
$maxMode        = ($week | Where-Object { $_.'Max Mode' -eq 'Yes' }).Count
```

Then format the report (see "Output" below).

## Output

Save the report to `<report_dir>/token-check-<YYYY-MM-DD>.md` (expand `%USERPROFILE%` in config) and print it to chat. Structure:

```markdown
# Token Check — week ending <YYYY-MM-DD>

## Headline

- Total tokens this week: **X** (baseline weekly avg: …)
- **Cache-read volume: Y** this week (baseline: …/week)
- **Cache-read per event: Z** (baseline: …)
- Opus-variant share: **W%** (baseline: …%)

[1-2 sentence verdict — better, worse, mixed. Lead with total volume and cache-read *volume*, not share.]

## Wins
- [volume improvements, model mix, thinking events down, etc.]

## Watch items
- [only things that actually got worse — volume up, Opus creep, etc.]
- [do NOT list "cache-read still ~90%" here]

## Cache-read (volume focus)
| Metric | This week | Baseline | Change |
|--------|----------:|---------:|-------:|

*Cache-read share: ~N% (baseline …%). Normal for Agent threads — track volume, not this ratio.*

## Model mix this week
| Model | Events | Tokens | % of week |

## Daily volumes
| Day | Events | Total tokens | Cache-read | Cache/event | Notes |

## Flags
- Thinking-variant events: N (target: rare and intentional)
- Max Mode events: 0/N (target: always 0)

## Recommendation for next week

[1-3 specific actions based on what the data shows]
```

Then **append a snapshot** to `<history_dir>/<YYYY-MM-DD>.json` (create the folder if needed).

If at least 4 weekly snapshots exist, also produce a trend section for the last 4 weeks — **volume columns first**, share last.

See [samples/token-check-example.md](samples/token-check-example.md) for a real report shape.

## Tone

Discipline check, not a scolding. Wins first. Watch items framed as "try next week," not "you screwed up."

**Cache-read reporting:** celebrate falling *volume*. Never imply failure because share stayed ~90%. Reference the companion doc in `reference_docs_dir` when suggesting habit changes.

## Hard rule

**This skill itself should be cheap to run.** Don't read the whole CSV into chat — analyze in PowerShell, summarize. Don't load the companion doc unless asked. Don't recompute the baseline; it's frozen in config.

## Related

- [`rules/token-budget.mdc`](../../rules/token-budget.mdc) — optional always-on rule this skill measures against
- [config.example.json](config.example.json) — paths and baseline
- `token-workflow` skill — multi-thread ticket planner
- `docs/token-efficiency/` in cursor-doc-skills — companion docs and work summary
