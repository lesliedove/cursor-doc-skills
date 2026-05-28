# cursor-doc-skills

A catalog of [Cursor](https://cursor.com) skills built by **Leslie Poff** (Team Charlie, Collaborative Services, Synopsys) for AI-driven documentation work on Ansys ModelCenter, optiSLang, and Developer-Portal API docs.

Each subfolder in [`packages/`](packages) is a standalone Cursor skill you can drop into your own Cursor install. Pre-built zips for each package live in [`dist/`](dist) for one-click install.

For the full background on each project — problems solved, results, screenshots — see [`docs/AI for Documentation - Project Summaries.md`](docs/AI%20for%20Documentation%20-%20Project%20Summaries.md). The README is just a launcher.

---

## What's a Cursor skill?

A **Cursor skill** is a folder containing a `SKILL.md` file (plus any supporting scripts or config) that teaches the Cursor agent how to do a specific task. When the agent recognizes a matching trigger — a slash command, a phrase, or a file type — it reads the `SKILL.md` and follows the instructions inside.

Skills live in `%USERPROFILE%\.cursor\skills\<skill-name>\` on Windows, or `~/.cursor/skills/<skill-name>/` on macOS/Linux. They're plain Markdown — easy to read, easy to adapt, easy to share.

> **New to Cursor skills?** Start with `ansys-doc-guidelines` or `api-documentation`. They're style-guide skills that activate automatically when you edit DITA, DocBook, or Markdown API docs — no commands to memorize, just install and start writing.

---

## What's in this repo

| Package | What it does | Best for |
|---------|--------------|----------|
| [`ansys-doc-guidelines`](packages/ansys-doc-guidelines) | Ansys corporate style guide for DITA and DocBook XML. The agent automatically follows voice, terminology, punctuation, capitalization, and tagging rules when editing `.dita`, `.ditamap`, or DocBook `.xml` files. | Anyone editing Ansys product docs |
| [`api-documentation`](packages/api-documentation) | API/Developer Portal style guide. Covers Markdown formatting, `docfx.json` metadata, package structure, OpenAPI quality, and the migration workflow to the Dev Portal. | Anyone migrating or maintaining API docs |
| [`ado-doc-workflow`](packages/ado-doc-workflow) | End-to-end Azure DevOps documentation ticket workflow — fetch ticket, create branch, apply doc changes, commit, PR, cherry-pick to release branches, update state. Includes the RIL/KIL/Release Notes generator and a credential-handling helper. | Any team doing TFS/ADO doc tickets |
| [`help-bot-doc-testing`](packages/help-bot-doc-testing) | Test harness that queries multiple AI engines (ChatGPT, Perplexity, Claude, Gemini, Copilot) with product questions, scores their answers against a ground-truth corpus, and surfaces documentation gaps. | Teams who want to know whether AI search engines answer correctly about their product |
| [`since-last-meeting`](packages/since-last-meeting) | Generic "what did I work on since the last meeting" prep skill. Configurable for any recurring meeting (sprint reviews, 1:1s, status meetings). Drops a one-pager in your Downloads folder before every cycle. | Anyone with a recurring meeting that needs a "what I've been up to" summary |
| [`how-i-ai`](packages/how-i-ai) | Biweekly "How I AI" meeting prep skill — discovers new AI work since the last meeting, updates a master project list, and drops a prep doc in Downloads. Fires automatically on Fridays when "How I AI" is on Monday's calendar. | AI demo / show-and-tell meeting prep |
| **llm-doc-converter** | Python-based converter that turns DITA, DocBook, HTML, PDF, or Word documentation into LLM-optimized Markdown with YAML front matter, TL;DR summaries, and question-oriented titles. Lives in its own repo: [`lesliedove/llm-doc-converter`](https://github.com/lesliedove/llm-doc-converter). | Building RAG corpora, feeding docs to AI assistants, AI accuracy testing |

---

## Installing any package

Cursor handles the install for you. Pick whichever way is easiest:

1. **Browse the package folder on GitHub**, copy whichever files you want, and drop them into Cursor — Cursor will offer to install them as a skill.
2. **Download the zip from [`dist/`](dist)** (or grab it from a [release](../../releases)), drag it into a Cursor chat, and say *"Add this as a global skill."* Cursor unzips it into your global skills folder and the skill is live for every project from then on.
3. **Or paste the zip's path** (`C:\path\to\<package>.zip`) into a chat and say the same thing.
4. **Or unzip the folder yourself anywhere convenient,** drag the folder into a Cursor chat, and say *"Add this as a global skill."*

If you want it scoped to one project instead of globally, say *"Add this as a project skill"* — Cursor will install it into that project's `.cursor/skills/` folder instead of your user-level one.

After Cursor confirms, start a new chat and the skill is available. No restart, no PowerShell, no manual paths.

### One-time configuration

A few skills need a small config file or credential before first use:

- **`since-last-meeting`** and **`how-i-ai`** — set your meeting name and standup name. Just say *"Configure since-last-meeting for me"* (or `how-i-ai`) in Cursor and the agent will walk you through it.
- **`ado-doc-workflow`** — requires `%USERPROFILE%\.env` with `ADO_Username` and `ADO_Password`, plus the bundled `lib\Ado-Auth.ps1` helper at `%USERPROFILE%\.cursor\lib\`. See [`packages/ado-doc-workflow/INSTALL.md`](packages/ado-doc-workflow/INSTALL.md) for details.
- **`help-bot-doc-testing`** — needs API keys for the engines you want to test (see its `README.md`).
- **`ansys-doc-guidelines`**, **`api-documentation`** — no config required; activate on file-type match.

Each package folder has its own `README.md` (or `INSTALL.md`) describing what it does, any optional config, and what triggers it. Cursor reads that automatically when you ask it to install — but you can always read it yourself first if you want.

---

## How these skills get used in practice

Most skills are **trigger-based**: you don't run them explicitly, the agent picks them up when it sees relevant files or phrases. For example:

- Open a `.dita` file and ask the agent to fix an inconsistency → `ansys-doc-guidelines` fires automatically.
- Say "pick up ticket 12345" → `ado-doc-workflow` fetches the ticket, creates a branch, etc.
- Say "draft the RIL for ticket 99999" → the release-deliverables sub-skill drafts the Resolved Issues List.

A few are **slash-command** or **scheduled**:

- `/since-last-meeting` generates the prep doc; can also fire automatically from a morning briefing routine when the meeting is on the calendar.
- `/how-i-ai` does the same for the biweekly "How I AI" meeting.

Each package's `README.md` and `SKILL.md` list the exact triggers.

---

## Adapting a skill for your team

These skills are **starting points**, not finished products. The patterns transfer well, but the specifics (repo paths, branch naming, ADO project names, style conventions) are Team Charlie-shaped. Open the `SKILL.md` and look for:

- **Hardcoded paths** — replace with your repos.
- **Hardcoded ADO project / area / iteration paths** — replace with yours.
- **Hardcoded reviewer / branch naming patterns** — replace with your team's conventions.
- **Style-guide content** (`ansys-doc-guidelines`, `api-documentation`) — these are corporate-wide, so they should mostly drop in unchanged. The terminology table and entity reference list are the most likely things to need product-specific additions.

Cursor skills are just Markdown. If a section doesn't apply, delete it. If something is missing, add it. The agent reads exactly what you write — there's no compilation step, no build, no plugin system to learn.

---

## Regenerating the zips

The source of truth is each folder under [`packages/`](packages). The zips in [`dist/`](dist) are convenience artifacts. To rebuild them after editing a package:

```powershell
.\scripts\make-packages.ps1
```

The script walks every subfolder in `packages\`, zips each one into a `dist\<name>.zip`, and reports sizes. Re-run it before committing if you've edited package contents.

---

## Contributing

Pull requests welcome. Two main flavors of change:

- **Add a new package** — drop a `packages\<your-skill>\` folder with a `SKILL.md` and a `README.md`, run `make-packages.ps1`, and PR.
- **Update an existing package** — edit files in `packages\<name>\`, regenerate the zip, and PR.

Open an issue if you find a bug, an outdated reference, or something that doesn't generalize beyond Team Charlie's setup.

---

## Questions

Ping **Leslie Poff** (`ldove@synopsys.com`) on Teams or email.

---

## License & sharing

Internal Synopsys / Ansys tools. Repo is private to keep internal-infrastructure references (TFS URLs, NTLM domain, internal SharePoint paths) inside the firewall. The *patterns and approaches* are fine to talk about externally (conferences, blog posts, etc.); the corporate-specific configs and style content are not. Don't redistribute outside Synopsys without checking first.
