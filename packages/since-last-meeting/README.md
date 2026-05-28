# "Since Last Meeting" Skill

A Cursor Agent Skill that prepares a one-page "what I've been working on" summary for any recurring meeting. Configure it once with the meeting name and the folders it should watch; from then on it scans your activity since the last cycle and drops a prep doc in your Downloads folder before you walk into the meeting.

Use it for sprint reviews, 1:1s, status meetings, quarterly reviews, project check-ins, "How I AI"-style meetings, or anything else where someone might ask *"so, what have you been up to?"* By default the skill captures everything in the window; you can narrow it to a topic via filter keywords if you want.

---

## What it does

Once configured, the skill:

1. Scans your activity in a configurable window (default: since the last meeting, fallback 14 days):
   - Cursor skills you created or updated
   - Standup-note bullets (your own section, by name)
   - Scratch / working folders that changed
   - Git commits in repos you nominate
   - Cursor agent transcripts (lightweight scan for topic only)
2. Optionally cross-references findings against a personal project list and adds/updates entries.
3. Generates a conversational one-pager at:
   ```
   %USERPROFILE%\Downloads\Meeting-Prep\<meeting-slug>\<meeting-date>-<slug>-prep.md
   ```
   with sections like "What I worked on", "Continued / Updated", "Tickets closed", and "Worth highlighting".

You skim the doc on your way to the meeting and walk in knowing exactly what to say.

---

## Install

### 1. Hand the zip to Cursor

Drag `since-last-meeting.zip` into any Cursor chat (or paste its file path) and say:

> Add this as a global skill.

Cursor unzips it into your global skills folder and the skill is live for every project from then on. (If you'd rather scope it to one project, say *"Add this as a project skill"* — Cursor will install it into that project's `.cursor/skills/` folder instead.)

After Cursor confirms, start a new chat and the skill is available. No restart, no manual paths, no PowerShell.

### 2. Tell Cursor your meeting

In any Cursor chat, say:

> Configure since-last-meeting for me. The meeting is "Sprint Review" and my standup name is "Don".

The agent copies the bundled `config.example.json` to `config.json`, fills in your values, and asks about anything else worth setting (your scratch folder, your repos, your standup-file location). You can also do it yourself — just edit the `config.json` next to the skill's `SKILL.md`. The minimum is:

```json
{
  "meeting_name": "Sprint Review",
  "user_name": "Don"
}
```

`meeting_name` is what appears (case-insensitive) on your calendar for this meeting. `user_name` is the name that appears after `## ` in your team's standup files. If you don't have standup files, leave `user_name` empty and the standup scan will be skipped.

Common other things to set, depending on how you work:

- `git_repos` — repo paths to scan for your commits.
- `scratch_dir` — your working / scratch folder if it isn't `C:\GitRepos\.scratch`.
- `standup_dir` — where your team's standup notes live.

Everything else in `config.example.json` is optional — override only what doesn't match your environment.

### 3. (Optional) First run to seed state

In Cursor, say:

> /since-last-meeting

This will:

- Create the per-meeting state file under `%USERPROFILE%\.config\since-last-meeting\`.
- Create the prep folder under `%USERPROFILE%\Downloads\Meeting-Prep\<slug>\`.
- Scan the configured sources for the last `meeting_cadence_days` (default 14).
- Generate your first prep doc.

Review the doc, tweak the master project list if you've configured one, and you're set.

### 4. (Optional) Wire up auto-trigger from a morning briefing

If you have a morning briefing skill that fetches your calendar, tell it to invoke this skill when the meeting is on the horizon. The pattern is:

> For each meeting configured in `since-last-meeting/config.json`: if it appears on the calendar within `lookahead_days` days, run `/since-last-meeting "<meeting_name>"`.

Skip this if you'd rather run `/since-last-meeting` manually the day before each meeting — it works either way.

---

## Usage

### Normal cycle

- **The day before the meeting** (or the morning of): run `/since-last-meeting`. The prep doc lands in `%USERPROFILE%\Downloads\Meeting-Prep\<slug>\`. Skim it on your way in.

### Useful variations

- **Multiple meetings:** Configure several at once via the `meetings` array in `config.json` (see below). Each gets its own state file and prep folder.
- **Catch up after a long stretch:** `/since-last-meeting` always runs against the recorded last-meeting date in state, or falls back to `meeting_cadence_days`. If you've missed a few cycles, the window auto-grows.
- **Refresh after late work:** Run `/since-last-meeting` again later in the day — it appends an "Added Later" section to the existing prep doc instead of overwriting.
- **Filter to a topic:** Set `filter_keywords` to limit the scan to bullets and folders matching specific keywords. See "Filtering" below.
- **One-shot for a specific meeting:** `/since-last-meeting "Director 1:1"` runs only that meeting (matches a config under that name in the `meetings` array).

---

## What gets detected

| Source | What signals activity | Required config |
|--------|----------------------|------------------|
| **Cursor skills** | Any `SKILL.md` modified since `last_meeting_date`, in `skills_dir` | `skills_dir` (default: `%USERPROFILE%\.cursor\skills\`) |
| **Standup notes** | Bullets in your `## <user_name>` section, optionally filtered by keyword | `standup_dir` + `user_name` |
| **Scratch folders** | Subfolders of `scratch_dir` modified since `last_meeting_date` | `scratch_dir` |
| **Git commits** | Your commits in any nominated repo since `last_meeting_date` | `git_repos` (array of repo paths) |
| **Agent transcripts** | `.jsonl` files in `agent_transcripts_dir` modified since the window — first 2-3 lines only, for topic | `agent_transcripts_dir` |

The skill skips any source whose path isn't configured or doesn't exist, so it's safe to leave sources empty. Configure the ones that match how you actually work and ignore the rest.

---

## Filtering

By default the skill captures **all** activity in the window. That's the right default for status meetings and sprint reviews — your team usually wants the full picture.

If your meeting is narrower (say, a "How I AI" meeting where only AI work matters), set `filter_keywords` in `config.json`:

```json
"filter_keywords": ["AI", "Cursor", "Claude", "agent", "skill", "rule",
                    "automation", "automated", "pipeline", "monitor",
                    "created", "built", "launched", "prototype"]
```

The skill then keeps only standup bullets and scratch folders matching at least one keyword (case-insensitive substring match). Cursor-skill changes are always included regardless of filtering — modifying a skill is itself a strong signal.

---

## Multiple meetings

If you want one install to drive several meetings, use the `meetings` array:

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
      "filter_keywords": ["promotion", "career", "concern", "blocker"]
    },
    {
      "meeting_name": "How I AI",
      "meeting_cadence_days": 14,
      "user_name": "Don",
      "filter_keywords": ["AI", "Cursor", "skill", "automation", "agent"]
    }
  ]
}
```

When you run `/since-last-meeting` with no argument, it runs for whichever meeting is closest on the calendar (or all of them, depending on how you wire the morning briefing). When you run `/since-last-meeting "<name>"`, it runs only for that one. Each meeting has its own state file and prep folder, keyed by a slug derived from the meeting name.

Top-level keys (`scratch_dir`, `git_repos`, etc.) provide defaults; per-meeting keys override them. So you can set sources once at the top and only specialize where it matters.

---

## Customization

Everything in `config.example.json` is overridable:

- **Different cadence** → `meeting_cadence_days`.
- **Different folder layout** → `scratch_dir`, `git_repos`, `standup_dir`, `prep_dir`, `state_dir`, `master_list_path`.
- **Different ticket ID format** → `ticket_pattern` (regex; default matches 6-8 digit IDs).
- **Different git author name** → `git_author` (defaults to `user_name`).
- **Different lookahead** for the calendar trigger → `lookahead_days` (default 3).

See `config.example.json` for the full list with inline explanations.

---

## Troubleshooting

**The prep doc says my standup data was unavailable.**
The skill couldn't find a standup file with a `## <user_name>` section. Check that `user_name` matches the heading exactly (case-sensitive), and that `standup_dir` resolves correctly. If you don't have a team standup file, that's fine — just leave `standup_dir` unset and the prep doc will use other sources.

**The prep doc is empty.**
Either nothing happened in the window, or none of the configured sources captured it. Most often: `git_repos` isn't set or your commits use a different author name. Set `git_author` to match your `git config user.name`.

**The morning briefing isn't running this skill on the right day.**
The auto-trigger depends on the morning briefing routine (a) actually invoking this skill and (b) finding the meeting on your calendar. The skill itself doesn't read the calendar — that's the briefing's job. Check the briefing's wiring, then test by running `/since-last-meeting` manually.

**I want a fresh start.**
Delete the state file at `%USERPROFILE%\.config\since-last-meeting\<slug>.json` and re-run. The skill reinitializes with a `meeting_cadence_days` window.

**My meeting name has special characters / unicode.**
The slug derivation lowercases, replaces non-alphanumerics with `-`, and trims. For example, `"Don's 1:1 with Director"` becomes `dons-1-1-with-director`. The slug is only used for filenames — display always uses your original `meeting_name`.

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team. Generalized from an earlier "How I AI"-specific version so any teammate or any meeting can use the same prep workflow.

Part of the **[`cursor-doc-skills`](https://github.com/lesliedove/cursor-doc-skills)** catalog. Issues, ideas, or improvements — open an issue on the repo or ping Leslie on Teams.
