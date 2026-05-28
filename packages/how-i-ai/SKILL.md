---
name: how-i-ai
description: >-
  Prepare for the biweekly "How I AI" meeting. Discovers AI work done since
  the last meeting (from skills, scratch folders, standups, and agent
  transcripts), updates your personal AI project list, and drops a prep doc
  in Downloads. Runs automatically on Fridays when "How I AI" appears on
  Monday's calendar, or manually via /how-i-ai.
---

# How I AI — Meeting Prep Skill (Shared Edition)

Automatically prepares materials for the biweekly "How I AI" meeting. Detects the meeting on Friday (via a Monday calendar peek), scans for new AI work, updates your personal project list, and creates a lightweight prep doc to glance at on Monday morning.

This is the shared edition. Read the bundled `README.md` once to set up your config, then use the skill the same way every meeting cycle.

## Setup (first run only)

Before the first run, the skill needs your name and Graph API credentials. See `README.md` (bundled with this skill) for the full setup walkthrough.

The minimum required configuration is a `config.json` file alongside this `SKILL.md` containing at least your standup name:

```json
{
  "user_name": "Don"
}
```

Everything else has sensible defaults and can be overridden in `config.json` as needed.

## Paths (resolved at runtime)

The skill resolves these paths every run. All `%USERPROFILE%` references expand to the current user's home directory, so the same paths work for any user without editing.

| Item | Default path | Override key in `config.json` |
|------|--------------|-------------------------------|
| **Skills directory** | `%USERPROFILE%\.cursor\skills\` | `skills_dir` |
| **Agent transcripts** | `%USERPROFILE%\.cursor\projects\<your-workspace-folder>\agent-transcripts\` — must be set per user | `agent_transcripts_dir` |
| **Standup files** | `%USERPROFILE%\Documents\Standups\<year>\` — must be set per user | `standup_dir` |
| **Scratch folder** | `C:\GitRepos\.scratch\` | `scratch_dir` |
| **AI projects folder** | `%USERPROFILE%\Documents\AI Projects\` | `ai_projects_dir` |
| **Master project list** | `<ai_projects_dir>\List of AI projects.md` | `master_list_path` |
| **Prep doc output** | `%USERPROFILE%\Downloads\How-I-AI\` | `prep_dir` |
| **State file** | `%USERPROFILE%\.config\how-i-ai\state.json` | `state_dir` |
| **Graph token env file** | `%USERPROFILE%\.env` | `env_file` |

The agent transcripts folder uses the standard Cursor naming convention. Cursor encodes the absolute path of your workspace into the folder name under `%USERPROFILE%\.cursor\projects\`. Open that folder, find the entry that matches your workspace, and set `agent_transcripts_dir` in `config.json` accordingly.

## State File

The state file lives at `<state_dir>\state.json` (defaults to `%USERPROFILE%\.config\how-i-ai\state.json`):

```json
{
  "user_name": "Don",
  "last_checked": "YYYY-MM-DD",
  "last_meeting_date": "YYYY-MM-DD",
  "last_prep_generated": "YYYY-MM-DD",
  "skill_mtimes": {
    "ado-doc": "YYYY-MM-DDTHH:MM:SS"
  },
  "known_project_headings": [
    "<headings from your master project list>"
  ]
}
```

The state file is created automatically on first run.

## When to Run

### Automatic trigger (Friday morning)

If you have a morning briefing routine that fetches Monday's calendar on Fridays (the "Monday peek"), invoke this skill after the calendar data is available:

1. Check whether **any** Monday event subject contains `"How I AI"` (case-insensitive). The match string is configurable via `meeting_name` in `config.json`.
2. If found: run the full workflow (Steps 1-6).
3. If not found: stop silently. Do not show any output.

If you don't have a morning briefing skill, set up a calendar reminder for every other Friday and run `/how-i-ai` manually.

### Manual trigger

`/how-i-ai` — always run the full workflow regardless of day or calendar. Useful for ad-hoc prep or catch-up after a long stretch without a meeting.

### End-of-day refresh trigger (optional)

If you keep an agent window open all day and call a "close" / "goodbye" workflow at the end, that workflow can re-invoke this skill in **refresh mode** to catch late-Friday work that landed after the morning prep. See "Refresh Mode" below.

## Step 0 — Load configuration

Before running any other step, load the configuration:

```powershell
$skillDir = Split-Path -Parent $PSCommandPath  # directory containing SKILL.md
$configPath = Join-Path $skillDir "config.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
} else {
    Write-Host "No config.json found. See README.md for setup instructions." -ForegroundColor Yellow
    # Prompt for user_name and write minimal config
    $userName = Read-Host "What name appears in the standup file under '## <name>' for your section?"
    $config = @{ user_name = $userName }
    New-Item -ItemType Directory -Path $skillDir -Force | Out-Null
    $config | ConvertTo-Json | Set-Content $configPath
}
```

Resolve all paths from the table above, substituting `%USERPROFILE%` with `$env:USERPROFILE` and `<user>` with `$env:USERNAME`.

If `user_name` is missing from the config, the standup scan in Step 2b cannot run — warn and continue with the other data sources.

## Step 1 — Determine the Date Window

The "since" date is the window of work to scan.

1. Read `state.json`. If `last_meeting_date` exists, use it as the start of the window.
2. If no state file or no `last_meeting_date`: default to 14 days ago.
3. The end of the window is today.

```powershell
$stateDir = "$env:USERPROFILE\.config\how-i-ai"
if (!(Test-Path $stateDir)) { New-Item -ItemType Directory -Path $stateDir -Force | Out-Null }
$stateFile = "$stateDir\state.json"
if (Test-Path $stateFile) {
    $state = Get-Content $stateFile | ConvertFrom-Json
    $sinceDate = [datetime]::Parse($state.last_meeting_date)
} else {
    $sinceDate = (Get-Date).AddDays(-14)
}
```

## Step 2 — Discover New AI Work

Collect evidence of new or changed AI work from multiple sources.

### 2a — New or modified skills

Scan the skills directory for `SKILL.md` files whose last-write time is after `$sinceDate`:

```powershell
$skillsDir = "$env:USERPROFILE\.cursor\skills"
Get-ChildItem -Path $skillsDir -Filter "SKILL.md" -Recurse |
    Where-Object { $_.LastWriteTime -gt $sinceDate } |
    ForEach-Object { "$($_.Directory.Name)|$($_.LastWriteTime.ToString('yyyy-MM-dd'))" }
```

Compare against `state.json`'s `skill_mtimes`. Classify each as:
- **New skill** — not in the previous state
- **Updated skill** — in the previous state but mtime changed

### 2b — Standup notes (only if `user_name` is configured)

Read the standup files for the current month (and previous month if the window spans months). Extract **only the user's sections** (from `## <user_name>` down to the next `## ` heading or `---` separator).

Scan the user's "Accomplished" bullets for AI-related keywords:
- Tool mentions: `Cursor`, `Claude`, `Copilot`, `AI`, `GPT`, `agent`, `LLM`
- Skill/rule mentions: `skill`, `rule`, `SKILL.md`, `.mdc`
- Automation mentions: `automated`, `automation`, `pipeline`, `monitor`, `script`
- New-capability signals: `created`, `built`, `added`, `new`, `launched`, `prototype`, `drafted`, `feasibility`

Collect matching bullets with their dates. Group multiple mentions of the same project across days into a single entry.

### 2c — Scratch folder activity

The scratch folder (default `C:\GitRepos\.scratch\`) is where AI-driven work lives. Any folder modified since `$sinceDate` is candidate AI work.

```powershell
$scratchDir = "C:\GitRepos\.scratch"
if (Test-Path $scratchDir) {
    Get-ChildItem $scratchDir -Directory |
        Where-Object { $_.LastWriteTime -gt $sinceDate } |
        Sort-Object LastWriteTime -Descending |
        ForEach-Object { "$($_.LastWriteTime.ToString('yyyy-MM-dd HH:mm'))  $($_.Name)" }
}
```

For each folder:
1. Folder names typically follow `<ticketID>-<description>` — extract the ticket ID if present.
2. Look at the files inside to gauge scope. Signals:
   - Multiple numbered markdown files (e.g. `01-architecture.md` through `15-glossary.md`) = substantial doc work
   - `report.md`, `summary.md`, `analysis.md` = analytical / review work
   - Python scripts (`.py`) = tooling or automation built
   - `*-spec.md`, `*-plan.md` = design / planning work
3. For substantial folders, read the README / summary to understand what was done.

**This is a high-signal source.** Don't skip it — everything in scratch was AI-driven.

### 2d — Agent transcripts (lightweight scan)

List `.jsonl` files in the agent transcripts directory modified since `$sinceDate`. Read just the first 2-3 lines of each (which typically contain the user's initial prompt) to identify chats about new AI work vs. routine tasks.

Flag any that look like new project work (creating skills, building automations, prototyping tools, etc.) vs. routine `/standup`, `/recap`, or doc ticket work.

This is a **lightweight** scan — don't read full transcripts. Just capture the topic.

### 2e — Compare against the master project list

Read the master project list (default `%USERPROFILE%\Documents\AI Projects\List of AI projects.md`). If the file doesn't exist yet, that's fine — every discovered item is a new project candidate. Create the file on first run with a header:

```markdown
# My AI Projects

A running list of the AI-driven work I've shipped or am building.

---

```

Extract all `## ` headings (project names). Compare discovered work from 2a-2d against these:
- If a discovered item matches an existing heading: check if status seems outdated based on new evidence. Mark as **updated** if so.
- If a discovered item doesn't match any heading: mark as **new project candidate**.

## Step 3 — Update the Master Project List

Edit the master list (path from Step 2e).

### New projects

For each new project candidate, add a new `## ` section before the `---` separator (or at the end if no separator exists). Follow this format:

```markdown
## <Project Name>

**Status:** <In progress | Complete>

**Problem:** <One paragraph — what pain point does this solve?>

**Solution:** <One or more paragraphs — what was built and how it works.>
```

Use the evidence from standup notes, skill contents, and transcripts to write the Problem and Solution.

### Updated projects

For existing projects with new activity:
- Update the **Status** if it changed
- Append new details to the **Solution** if the project gained significant capabilities
- Do NOT rewrite the whole entry — append or refine

### Confirmation

Before changing the master list, show the user what will be added/updated:

```
--- How I AI Prep ---

New projects to add:
  - <Project Name>: <one-line summary>

Updated projects:
  - <Project Name>: <what changed>

Proceed with updates? [y/n]
```

If running non-interactively as part of an automated morning briefing with no objection, proceed.

## Step 4 — Generate the Prep Doc

Create a prep document in the prep directory (default `%USERPROFILE%\Downloads\How-I-AI\`).

### Folder structure

```
%USERPROFILE%\Downloads\How-I-AI\
  2026-05-19-how-i-ai-prep.md    (date = the Monday meeting date)
  2026-05-05-how-i-ai-prep.md    (previous meetings accumulate here)
```

### Prep doc format

```markdown
# How I AI — Prep Notes for <Monday date>

*Generated <today's date and time> by Flo*
*Window: <sinceDate> to <today>*

## New Since Last Meeting

### <Project or Capability Name>

<2-4 sentences: what it is, why it matters, what's interesting about it.
Written in first person since the user will present this conversationally.>

### <Next item>

...

## Updated / Continued Work

- **<Project Name>:** <one-line summary of what progressed>
- **<Project Name>:** <one-line summary>

## Demo-Worthy?

<If any item seems particularly demo-able or visual, call it out here
with a suggestion for what to show. Otherwise: "Nothing jumps out as a
live demo this time — the bullets above should be enough.">
```

The prep doc is a cheat sheet for a 5-minute presentation, not a formal report. It should be concise and conversational.

### Create the folder if needed

```powershell
$prepDir = "$env:USERPROFILE\Downloads\How-I-AI"
if (!(Test-Path $prepDir)) { New-Item -ItemType Directory -Path $prepDir -Force | Out-Null }
```

## Step 5 — Update State and Report

### Update state.json

```json
{
  "user_name": "<from config>",
  "last_checked": "<today>",
  "last_meeting_date": "<the Monday date of the upcoming How I AI meeting>",
  "last_prep_generated": "<today>",
  "skill_mtimes": { "<current mtimes for all skills>" },
  "known_project_headings": [ "<all ## headings from the updated master list>" ]
}
```

### Display summary

```
--- How I AI (Monday) ---

Prep doc: <prepDir>\<Monday>-how-i-ai-prep.md

New since last meeting:
  - <Project/capability>: <one-liner>
  - <Project/capability>: <one-liner>

Updated:
  - <Project>: <one-liner>

Master list updated.
```

If there's genuinely nothing new:

```
--- How I AI (Monday) ---

No new AI work detected since <last_meeting_date>.
Nothing to prep — you're caught up!
```

## Refresh Mode (end-of-day, Friday only)

When invoked from a close / goodbye workflow on a Friday, run this abbreviated workflow instead of the full Steps 1-5.

### Refresh Step 1 — Locate the existing prep doc

The upcoming Monday is `today + 3` days when today is Friday. The prep doc is at:

```
<prepDir>\<Monday yyyy-MM-dd>-how-i-ai-prep.md
```

If the prep doc does NOT exist, abort silently. (Morning prep didn't run today — nothing to refresh against. The Monday morning briefing will catch up.)

### Refresh Step 2 — Determine the refresh window

Read the prep doc's `*Generated <timestamp> by Flo*` line. Parse the timestamp. The refresh window is from that timestamp to **now**.

If the prep doc has already been refreshed today (i.e. it already contains a `## Added During the Day` section dated today), use the most recent refresh timestamp. This makes the close workflow idempotent.

### Refresh Step 3 — Re-scan, narrower window

Repeat Step 2 of the full workflow (sub-steps 2a-2d) but with `sinceDate` set to the refresh window start instead of the meeting window start. The scratch folder is the highest-signal source for late-day work.

### Refresh Step 4 — Append (do not overwrite)

If nothing new was found, abort silently. Otherwise, append at the bottom of the prep doc:

```markdown

---

## Added During the Day

*Appended <timestamp> by Flo via close workflow*
*Refresh window: <window start> to <window end>*

### <Project or Capability Name>

<2-4 sentences, same conversational tone.>

### <Next item>

...
```

Also add a line under the doc's `*Generated ...*` header noting the update.

### Refresh Step 5 — Update state and report briefly

Update `state.json` with `last_refresh` and `last_refresh_items_added`. Leave the meeting metadata untouched (refresh is a delta, not a re-prep).

```
--- How I AI refresh ---

Found <N> new item(s) since this morning's prep:
  - <Project>: <one-liner>

Appended to: <prepDir>\<Monday>-how-i-ai-prep.md
```

## Error Handling

- **Calendar data unavailable (token expired):** If running automatically and Monday events couldn't be fetched, skip silently. If running manually via `/how-i-ai`, warn that the meeting date couldn't be confirmed but proceed using the assumed biweekly cadence.
- **Standup files missing or unreadable:** Skip that data source, note it in the prep doc ("standup data unavailable").
- **Agent transcripts inaccessible:** Skip silently — supplementary data.
- **Master list missing:** Create it with the header shown in Step 2e. Still generate the prep doc.
- **State file missing:** Initialize with current state. On first run, use 14-day default window.

Never let a single failure block the whole workflow. Always generate the prep doc with whatever data is available.

## Optional Integrations

### Morning briefing hook

If you have a personal morning briefing skill, add a Friday-only section that delegates to this skill after the calendar step:

```
If today is Friday and Monday's calendar contains "How I AI":
  Run the how-i-ai skill (full workflow).
  Show the summary section in the briefing output.
Else:
  Skip silently.
```

### Close / goodbye hook

If you have a close-session skill, add a Friday-only step that invokes this skill in refresh mode:

```
If today is Friday and a prep doc exists for the upcoming Monday:
  Run the how-i-ai skill in refresh mode.
  The refresh appends any late-Friday AI work to the existing prep doc.
```

Both integrations are optional. The skill works fine without them — just run `/how-i-ai` manually on Friday mornings.
