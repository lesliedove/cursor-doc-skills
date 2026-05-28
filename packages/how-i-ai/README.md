# How I AI Skill — Shared Edition

A Cursor Agent Skill that prepares biweekly "How I AI" meeting notes for you automatically. It scans your AI work since the last meeting (skills, scratch folders, standups, agent transcripts), updates your personal AI project list, and drops a one-page prep doc in your Downloads folder.

This is the shared version — same skill Leslie uses, with personal references stripped out and a single config knob for your name.

---

## What it does

Twice a month (assuming a biweekly "How I AI" meeting), the skill:

1. Scans the last ~14 days for AI-driven work — new or updated Cursor skills, scratch folder activity, your standup bullets, and recent agent transcripts.
2. Cross-references findings against your personal AI projects list and adds/updates entries.
3. Generates a conversational one-pager in `%USERPROFILE%\Downloads\How-I-AI\<Monday-date>-how-i-ai-prep.md` summarizing what's new, what's continued, and what's demo-worthy.

You glance at the doc Monday morning before the meeting and know exactly what to say.

---

## Install

### 1. Unzip into your Cursor skills folder

```powershell
$dest = "$env:USERPROFILE\.cursor\skills\how-i-ai"
Expand-Archive -Path "how-i-ai.zip" -DestinationPath $dest -Force
```

You should end up with:

```
%USERPROFILE%\.cursor\skills\how-i-ai\
  SKILL.md
  README.md
  config.example.json
```

### 2. Create your config file

Copy `config.example.json` to `config.json` and edit one line:

```powershell
Copy-Item "$env:USERPROFILE\.cursor\skills\how-i-ai\config.example.json" `
          "$env:USERPROFILE\.cursor\skills\how-i-ai\config.json"
notepad   "$env:USERPROFILE\.cursor\skills\how-i-ai\config.json"
```

Change this line to your standup name:

```json
"user_name": "Don"
```

That's the only required edit. Everything else has sensible defaults. If you ever move your scratch folder or skills directory, override those keys in `config.json` too.

### 3. (Optional) Set up the calendar auto-trigger

The skill can run automatically every Friday morning if it sees "How I AI" on Monday's calendar. This requires Microsoft Graph API credentials so it can read your Outlook calendar.

Skip this step if you'd rather just run `/how-i-ai` manually on Friday mornings — the skill works fine without it.

If you do want the auto-trigger:

a. **Get a Graph API token.** Ask Leslie for her Graph token setup walkthrough (`graph-token-gen` in her scratch folder), or follow Microsoft's docs to register an app with `Calendars.Read` permission for your account.

b. **Save credentials to `%USERPROFILE%\.env`**:

```
GRAPH_CLIENT_ID=<your-app-id>
GRAPH_TENANT_ID=<synopsys-tenant-id>
GRAPH_CLIENT_SECRET=<your-secret>
```

c. **Hook it into your morning routine.** If you don't have a morning briefing skill, the simplest pattern is to add a Cursor rule that runs on Friday morning. Open Cursor settings and add to your User Rules:

```
On Fridays, when I start a chat with "good morning" or similar,
check Monday's Outlook calendar via Microsoft Graph. If any event
contains "How I AI", run the how-i-ai skill in full mode.
```

d. **Test it.** On Friday morning, type "good morning" and confirm the skill runs.

### 4. First run

Run the skill manually once to seed the state file:

```
/how-i-ai
```

The skill will:
- Create `%USERPROFILE%\.config\how-i-ai\state.json` with your name and starting timestamps.
- Create `%USERPROFILE%\Documents\AI Projects\List of AI projects.md` with a header (if you don't already have one).
- Scan the last 14 days for AI work.
- Generate your first prep doc in `%USERPROFILE%\Downloads\How-I-AI\`.

Review the prep doc and tweak the master project list as needed. After this, every cycle is automatic (or one `/how-i-ai` away).

---

## Usage

### Normal cycle

- **Friday morning:** Run `/how-i-ai` (or let the auto-trigger fire if you set it up). Prep doc lands in Downloads.
- **Monday morning:** Open `%USERPROFILE%\Downloads\How-I-AI\<this-Monday>-how-i-ai-prep.md`. Skim it. Walk into the meeting.

### Useful variations

- **Catch up after a stretch of meetings missed:** Run `/how-i-ai` any day. It uses the last meeting date from state, or falls back to 14 days.
- **Refresh after late-Friday work:** If you do significant AI work Friday afternoon, run `/how-i-ai` again before logging off. It'll append a "Added During the Day" section to the existing prep doc.
- **Manual project list edits:** The master list at `%USERPROFILE%\Documents\AI Projects\List of AI projects.md` is yours to edit freely. The skill respects your edits — it only appends new sections or updates Status lines.

---

## What gets detected

| Source | What signals AI work |
|--------|----------------------|
| **Cursor skills** | Any `SKILL.md` file modified since the last meeting, in `%USERPROFILE%\.cursor\skills\` |
| **Standup notes** | Bullets in your standup section mentioning AI tools, skills, automation, or "created / built / drafted / prototype" |
| **Scratch folders** | Any folder under `C:\GitRepos\.scratch\` modified since the last meeting (everything in scratch is AI-driven by definition) |
| **Agent transcripts** | Cursor chat `.jsonl` files modified since the last meeting — used as a tiebreaker / supplement |

The scratch folder is the highest-signal source. If you've been doing AI work and not putting it in `.scratch`, the skill will likely miss it. Move plans, prototypes, and exploration into `.scratch` to make them visible to this skill (and to the standup automation).

---

## Customization

Everything Leslie's version does is here, controlled by `config.json`:

- **Different meeting name?** Change `meeting_name`.
- **Different cadence?** Change `meeting_cadence_days`.
- **Different folder layout?** Override any of `scratch_dir`, `ai_projects_dir`, `prep_dir`, `standup_dir`, `agent_transcripts_dir`.

See `config.example.json` for the full list with inline explanations.

---

## Troubleshooting

**The prep doc says my standup data was unavailable.**
The skill couldn't find a standup file with a `## <YourName>` section for the current window. Check that `user_name` in `config.json` matches the exact heading in the standup file (case-sensitive). Check that the standup directory path resolves correctly.

**The prep doc is empty (no new work found).**
Either no AI work landed in the last cycle, or none of it left traces in the four signal sources. Move work into `.scratch\` going forward and the next run will catch it.

**The calendar trigger doesn't fire on Friday.**
The auto-trigger depends on (a) your morning briefing routine actually invoking the skill on Fridays, and (b) a working Graph token. Test the token by running a quick calendar query manually. If unsure, just run `/how-i-ai` manually — that path doesn't depend on the calendar.

**I want to roll back state.**
Delete `%USERPROFILE%\.config\how-i-ai\state.json` and re-run. The skill will reinitialize with a 14-day window.

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team. This shared edition extracts the personal/Flo-specific bits so any teammate can drop it in and go.

Part of the **[`cursor-doc-skills`](https://github.com/lesliedove/cursor-doc-skills)** catalog. Issues or improvements — open an issue on the repo or ping Leslie on Teams.
