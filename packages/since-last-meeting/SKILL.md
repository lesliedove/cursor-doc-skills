---
name: since-last-meeting
description: >-
  Prepare a "what I've been working on" summary for any recurring meeting.
  Scans your activity since the last meeting (commits, standups, scratch
  folders, Cursor skills, agent transcripts) and drops a one-page prep doc
  in Downloads. Configurable for any meeting name and cadence — use it for
  sprint reviews, 1:1s, team meetings, "How I AI", quarterly check-ins, or
  anything else that recurs. Runs on demand via /since-last-meeting, or
  automatically from a morning briefing routine.
---

# Since Last Meeting — Generic Meeting Prep Skill

A configurable prep skill that summarizes "what have I been doing" for any recurring meeting. Point it at the meeting name on your calendar, tell it which folders to watch, and it generates a one-pager you can skim before walking in.

By default the skill captures **all** activity in the window — the right behavior for sprint reviews, status meetings, and similar "what have you been doing" check-ins. For narrower meetings (an "AI-only" demo round, a security review, etc.) you can supply `filter_keywords` to keep only matching items.

## Setup (first run only)

The skill needs a `config.json` next to this `SKILL.md`. The bundled `config.example.json` is the template — copy it and edit at minimum two values:

```json
{
  "meeting_name": "Sprint Review",
  "user_name": "<YourName>"
}
```

Everything else has sensible defaults; override only what doesn't match your environment. See `README.md` for the full setup walkthrough.

## Paths (resolved at runtime)

All `%USERPROFILE%` references expand to the current user's home, so the same config works for every teammate without editing.

| Item | Default path | Override key in `config.json` |
|------|--------------|-------------------------------|
| **Skills directory** | `%USERPROFILE%\.cursor\skills\` | `skills_dir` |
| **Agent transcripts** | `%USERPROFILE%\.cursor\projects\<workspace>\agent-transcripts\` | `agent_transcripts_dir` |
| **Standup files** | (none — set `standup_dir` if you have one) | `standup_dir` |
| **Scratch folder** | `C:\GitRepos\.scratch\` | `scratch_dir` |
| **Git repos to scan** | (none — set `git_repos` if you want git activity) | `git_repos` |
| **Master project list** (optional) | (none — set `master_list_path` if you keep one) | `master_list_path` |
| **Prep doc output** | `%USERPROFILE%\Downloads\Meeting-Prep\<meeting-slug>\` | `prep_dir` |
| **State file** | `%USERPROFILE%\.config\since-last-meeting\<meeting-slug>.json` | `state_dir` |
| **Graph token env file** | `%USERPROFILE%\.env` | `env_file` |

The `<meeting-slug>` is derived from `meeting_name` — lowercased, spaces replaced with hyphens, non-alphanumerics stripped. So `"Sprint Review"` becomes `sprint-review`. This lets the skill be installed once and used for multiple meetings (each gets its own state file and output folder).

## State File

State lives at `<state_dir>\<meeting-slug>.json`:

```json
{
  "meeting_name": "Sprint Review",
  "user_name": "Don",
  "last_checked": "YYYY-MM-DD",
  "last_meeting_date": "YYYY-MM-DD",
  "last_prep_generated": "YYYY-MM-DD",
  "skill_mtimes": {
    "<skill-name>": "YYYY-MM-DDTHH:MM:SS"
  },
  "known_project_headings": [
    "<headings from master_list_path, if configured>"
  ]
}
```

Created automatically on first run.

## When to Run

### Manual trigger

`/since-last-meeting` — always run the full workflow. Use this whenever you want a snapshot, regardless of cadence or calendar.

You can also pass an optional meeting argument if you have multiple configured meetings:

`/since-last-meeting "Director 1:1"` — uses the config keyed under that meeting name (see "Multiple meetings" below).

### Automatic trigger (calendar-aware morning briefing)

If you have a morning briefing routine that fetches your calendar, invoke this skill when the configured meeting appears within the next N days:

1. Look ahead `lookahead_days` (default 3) on the calendar.
2. If any event subject contains `meeting_name` (case-insensitive), run the full workflow.
3. If not, stay silent.

The morning briefing wires up the calendar peek; this skill just runs when called.

### Refresh trigger (optional)

If your prep doc was generated in the morning and significant work landed before the meeting, you can re-invoke the skill in **refresh mode** to append late-day work to the existing prep doc without overwriting the morning's content. See "Refresh Mode" below.

## Step 0 — Load configuration

```powershell
$skillDir = Split-Path -Parent $PSCommandPath
$configPath = Join-Path $skillDir "config.json"
if (-not (Test-Path $configPath)) {
    Write-Host "No config.json found. See README.md for setup instructions." -ForegroundColor Yellow
    exit 1
}
$config = Get-Content $configPath | ConvertFrom-Json
```

Required keys: `meeting_name` (always), `user_name` (only required if `standup_dir` is set). Resolve all paths from the table above, substituting `%USERPROFILE%` with `$env:USERPROFILE` and `<workspace>` with whatever the user configured in `agent_transcripts_dir`.

Compute the meeting slug:

```powershell
$slug = ($config.meeting_name.ToLower() -replace '[^a-z0-9]+','-').Trim('-')
```

If the user runs `/since-last-meeting "<other meeting name>"` and the config contains a `meetings` array (multi-meeting mode), pick the matching entry. Otherwise use the top-level config.

## Step 1 — Determine the date window

The "since" date is the start of the activity window:

1. Read `state.json` for this meeting slug. If `last_meeting_date` exists, use it.
2. If no state file: default to `meeting_cadence_days` ago (default 14).
3. The end of the window is **now**.

```powershell
$stateDir = "$env:USERPROFILE\.config\since-last-meeting"
if (-not (Test-Path $stateDir)) { New-Item -ItemType Directory -Path $stateDir -Force | Out-Null }
$stateFile = Join-Path $stateDir "$slug.json"
if (Test-Path $stateFile) {
    $state = Get-Content $stateFile | ConvertFrom-Json
    $sinceDate = [datetime]::Parse($state.last_meeting_date)
} else {
    $sinceDate = (Get-Date).AddDays(-1 * ($config.meeting_cadence_days ?? 14))
}
```

## Step 2 — Discover activity

Collect evidence from each configured source. **Skip any source whose path isn't configured or doesn't exist.** Don't fail — just note in the output what was unavailable.

### 2a — Cursor skills modified

Scan `$skillsDir` for `SKILL.md` files modified after `$sinceDate`:

```powershell
Get-ChildItem -Path $skillsDir -Filter "SKILL.md" -Recurse |
    Where-Object { $_.LastWriteTime -gt $sinceDate } |
    ForEach-Object {
        [pscustomobject]@{
            Skill   = $_.Directory.Name
            Mtime   = $_.LastWriteTime
            IsNew   = -not ($state.skill_mtimes.PSObject.Properties.Name -contains $_.Directory.Name)
        }
    }
```

Classify as **new skill** (not in previous state) or **updated skill** (in state, mtime changed).

### 2b — Standup notes (if `standup_dir` and `user_name` configured)

Read standup files for the current month (and previous month if window spans). Extract the user's section: from `## <user_name>` down to the next `## ` heading or `---` separator.

For each accomplishment bullet:
- Capture the date and bullet text.
- If `filter_keywords` is configured, only keep bullets matching at least one keyword.
- If `filter_keywords` is empty/missing, keep all bullets (this is the generic mode — capture everything).

Group multiple mentions of the same project across days into a single entry where possible.

### 2c — Scratch folder activity (if `scratch_dir` configured)

```powershell
if ($config.scratch_dir -and (Test-Path $config.scratch_dir)) {
    Get-ChildItem $config.scratch_dir -Directory |
        Where-Object { $_.LastWriteTime -gt $sinceDate } |
        Sort-Object LastWriteTime -Descending
}
```

For each modified folder:
1. Folder names often follow `<ticketID>-<description>` — extract the ticket ID if present.
2. Look at file types to gauge scope:
   - Multiple numbered Markdown files → substantial doc work
   - `report.md`, `summary.md`, `analysis.md` → analytical / review work
   - Python scripts → tooling or automation
   - `*-spec.md`, `*-plan.md` → design / planning work
3. For substantial folders, read the README/summary to describe what was done.

If `filter_keywords` is set, only include folders whose names or summaries match. Otherwise include all.

### 2d — Git activity (if `git_repos` configured)

For each repo in `git_repos`:

```powershell
foreach ($repo in $config.git_repos) {
    if (-not (Test-Path "$repo\.git")) { continue }
    Push-Location $repo
    try {
        git log --since="$($sinceDate.ToString('yyyy-MM-dd'))" --author="$($config.git_author ?? $config.user_name)" `
                --pretty=format:"%h|%ad|%s" --date=short
    } finally { Pop-Location }
}
```

Group commits by repo and by ticket ID (extracted from commit message via the configured `ticket_pattern`, default `\b\d{6,8}\b` for 6-8 digit ticket IDs). PRs merged in the window are particularly interesting.

### 2e — Agent transcripts (lightweight scan, if configured)

List `.jsonl` files in `agent_transcripts_dir` modified after `$sinceDate`. Read just the first 2-3 lines (the user's initial prompt) to identify the topic. Don't read full transcripts — this is a tiebreaker.

Flag any transcripts that look like new project work (creating skills, building automations, exploratory prototyping) versus routine `/standup`, `/recap`, or doc-ticket sessions.

### 2f — Compare against the master project list (if `master_list_path` configured)

If a master project list is configured, read it. Extract all `## ` headings (project names). Compare against discovered work:

- Match → check whether the project's status seems outdated; mark as **updated** if so.
- No match → mark as **new project candidate**.

If no master list is configured, every discovered item is just a "thing that happened" — no new/updated bookkeeping.

## Step 3 — Update the master project list (optional)

This step runs **only if `master_list_path` is configured**. Skip otherwise.

### New projects

For each new project candidate, append a `## ` section before the trailing `---` (or at the end). Format:

```markdown
## <Project Name>

**Status:** <In progress | Complete>

**Problem:** <One paragraph — what pain point does this solve?>

**Solution:** <One or more paragraphs — what was built and how it works.>
```

Use evidence from standup notes, skill contents, and transcripts to write Problem and Solution.

### Updated projects

For existing projects with new activity:
- Update **Status** if it changed.
- Append new details to **Solution** if the project gained capabilities.
- Don't rewrite the whole entry — append or refine.

### Confirmation

Before changing the master list, show the user what will change:

```
--- Since-Last-Meeting: <Meeting Name> ---

New projects to add:
  - <Project Name>: <one-line summary>

Updated projects:
  - <Project Name>: <what changed>

Proceed with updates? [y/n]
```

In a non-interactive morning-briefing context with no objection, proceed automatically.

## Step 4 — Generate the prep doc

Write the prep doc into `<prep_dir>\<meeting-date>-<slug>-prep.md`. The meeting date is the date of the upcoming meeting if known (from calendar lookahead), or today's date if unknown.

### Folder structure

```
%USERPROFILE%\Downloads\Meeting-Prep\<meeting-slug>\
  2026-05-19-sprint-review-prep.md
  2026-05-12-sprint-review-prep.md
```

### Prep doc format

```markdown
# <Meeting Name> — Prep Notes for <meeting date>

*Generated <today's date and time>*
*Window: <sinceDate> to <today>*

## What I Worked On

### <Project / Capability / Ticket>

<2-4 sentences in first person, conversational. What it is, why it
mattered, what's interesting. The user will read this 30 seconds
before walking into the meeting.>

### <Next item>

...

## Continued / Updated

- **<Project Name>:** <one-line summary of what progressed>
- **<Project Name>:** <one-line summary>

## Tickets Closed / Merged

- **<Ticket ID>:** <short title — repo / PR if relevant>
- **<Ticket ID>:** <short title>

## Worth Highlighting

<If anything is particularly demo-able, blocking, or worth flagging
to the room, call it out here. Otherwise: "Nothing jumps out as a
must-mention this round.">
```

The "Tickets Closed / Merged" and "Worth Highlighting" sections are optional — omit them if there's nothing to put there. The prep doc is a cheat sheet, not a report.

### Create the folder if needed

```powershell
$prepDir = "$env:USERPROFILE\Downloads\Meeting-Prep\$slug"
if (-not (Test-Path $prepDir)) { New-Item -ItemType Directory -Path $prepDir -Force | Out-Null }
```

## Step 5 — Update state and report

### Update state.json

```json
{
  "meeting_name": "<from config>",
  "user_name": "<from config>",
  "last_checked": "<today>",
  "last_meeting_date": "<the date of the upcoming meeting>",
  "last_prep_generated": "<today>",
  "skill_mtimes": { "<current mtimes for all skills>" },
  "known_project_headings": [ "<all ## headings from the updated master list, if applicable>" ]
}
```

### Display summary

```
--- <Meeting Name> Prep ---

Prep doc: <prepDir>\<date>-<slug>-prep.md

What I worked on:
  - <Project/capability>: <one-liner>
  - <Project/capability>: <one-liner>

Updated:
  - <Project>: <one-liner>

Master list updated.   (if applicable)
```

If genuinely nothing happened in the window:

```
--- <Meeting Name> Prep ---

No activity detected since <last_meeting_date>. Either it was a quiet
cycle or none of the configured sources captured what you did. Add
or check sources in config.json if this seems wrong.
```

## Refresh Mode (append late-day activity)

When invoked from a "close session" workflow or a follow-up call later in the day, run an abbreviated refresh instead of the full workflow.

### Refresh Step 1 — Locate the existing prep doc

The prep doc is at `<prep_dir>\<meeting-date>-<slug>-prep.md`. If it doesn't exist, abort silently — there's nothing to refresh against.

### Refresh Step 2 — Determine the refresh window

Read the prep doc's `*Generated <timestamp>*` line. Parse the timestamp. The refresh window is from that timestamp to **now**.

If a `## Added Later` section already exists with a recent timestamp, use that timestamp instead so the refresh is idempotent.

### Refresh Step 3 — Re-scan, narrower window

Repeat Step 2 (sub-steps 2a–2e) with `sinceDate` set to the refresh window start.

### Refresh Step 4 — Append (do not overwrite)

If nothing new was found, abort silently. Otherwise append to the prep doc:

```markdown

---

## Added Later

*Appended <timestamp>*
*Refresh window: <start> to <end>*

### <Project / Capability>

<2-4 sentences in the same conversational tone.>
```

Add a line under the doc's `*Generated …*` header noting the update.

### Refresh Step 5 — Update state and report briefly

Update `state.json` with `last_refresh` and `last_refresh_items_added`. Leave meeting metadata untouched (refresh is a delta, not a new prep).

```
--- <Meeting Name> refresh ---

Found <N> new item(s) since the morning prep:
  - <Project>: <one-liner>

Appended to: <prep doc path>
```

## Multiple meetings (advanced)

If you want to track several meetings with one install, use the `meetings` array in `config.json`:

```json
{
  "meetings": [
    {
      "meeting_name": "Sprint Review",
      "meeting_cadence_days": 14,
      "user_name": "Don",
      "filter_keywords": []
    },
    {
      "meeting_name": "Director 1:1",
      "meeting_cadence_days": 7,
      "user_name": "Don",
      "filter_keywords": ["promotion", "career", "concern"]
    }
  ]
}
```

When invoked without arguments, run for **all** configured meetings whose calendar lookahead matches. When invoked with `/since-last-meeting "<name>"`, run only for that one. Each meeting gets its own state file and prep folder, keyed by slug.

## Filter keywords (optional)

If `filter_keywords` is non-empty, the standup-bullet and scratch-folder scans (Steps 2b and 2c) only include items matching at least one keyword (case-insensitive substring match).

For example, an AI-only review meeting could set:

```json
"filter_keywords": ["AI", "Cursor", "Claude", "agent", "skill", "rule",
                    "automation", "automated", "pipeline", "monitor",
                    "created", "built", "launched", "prototype"]
```

If `filter_keywords` is empty or missing, capture everything. That's the right default for sprint reviews, status meetings, and similar "what have you been doing" meetings.

## Error Handling

- **A configured source doesn't exist** (skills dir missing, scratch dir missing, etc.): warn once at the top of the prep doc, skip the source, continue.
- **Standup files unreadable or `user_name` not configured**: skip Step 2b, note "standup data unavailable" in the prep doc.
- **Agent transcripts inaccessible**: skip Step 2e silently — supplementary data only.
- **Master list missing but `master_list_path` configured**: create it with a minimal header (`# My Projects\n\n---\n`), then continue.
- **State file missing**: initialize with current state. First run uses `meeting_cadence_days` as the window.
- **Calendar data unavailable**: if running automatically, skip silently. If running manually via `/since-last-meeting`, warn that the meeting date couldn't be confirmed but proceed using the cadence.

Never let one failure block the workflow. Always generate the prep doc with whatever data is available.

## Optional Integrations

### Morning briefing hook

Add a section to your morning briefing routine that delegates to this skill when the meeting is on the horizon:

```
For each configured meeting in since-last-meeting/config.json:
  If the meeting appears on the calendar within `lookahead_days`:
    Run /since-last-meeting "<meeting_name>" (full workflow).
    Show the summary in the briefing output.
  Else:
    Skip silently.
```

### Close-session hook

If you have an end-of-day "close" or "diary" workflow, invoke this skill in refresh mode for any meeting whose prep doc was generated today:

```
For each prep doc generated today:
  Run /since-last-meeting refresh "<meeting_name>".
  The refresh appends late-day activity to the existing prep doc.
```

Both integrations are optional. The skill works fine standalone — just run `/since-last-meeting` whenever you want a snapshot.
