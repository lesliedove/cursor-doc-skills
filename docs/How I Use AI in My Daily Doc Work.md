# How I Use AI in My Daily Doc Work

*Leslie Poff, Staff Engineer*<br>
*ModelCenter and optiSlang, Collaborative Services Team*<br>
*May 2026*

---

## The short version

I use **Cursor IDE with Claude** as my primary working environment. Over the last year I've layered on a system of Cursor skills and rules. Together they turn the AI from a generic chat partner into a workflow operator that knows our repos, our style guides, our ticket system, and our release calendar.

I primarily use AI to eliminate the parts of doc work that aren't writing -- the clicking, looking up, branching, cherry-picking, building, and report-generating -- so the time I spend on actual writing is higher quality and more focused. Also, rather than having *less* work as one would assume, I have ended up with *more* work as each AI project spawns another and another. 

---

## A day in the life

Here is what an average day looks like. Almost every step is something I used to do manually and now don't.

### Morning -- "Good morning, Flo"

I open Cursor and type **"good morning, Flo"**. My assistant (I named it Flo, after the Progressive insurance lady -- relentlessly cheerful, weirdly into the boring stuff) runs through a structured briefing in under a minute:

- Yesterday's git activity and standup notes, condensed
- Today's standup file generated from yesterday's commitments
- Today's calendar (pulled from Outlook via Microsoft Graph)
- Upcoming Corp-DOC deadlines (XML edit dates, ECC, FCA)
- Local reminders due today
- Whether the corporate install docs have changed (relevant to the MC and oSL Install Guides)
- Whether any of the doc build pipelines are failing
- The current state of my doc tickets (a small dashboard)
- A web dashboard auto-opened in my browser for visual reference

I start Flo and then go make my coffee. When I come back, I read the daily report and get started.

### Picking up a ticket -- "ticket 12345"

When a doc ticket is assigned to me, I tell Flo to **"get ticket 12345."** It does the entire setup:

1. Fetches the ticket from ADO (REST API, NTLM auth)
2. Reads the description, comments, and attachments to figure out what's actually being asked
3. Identifies the correct repo (ModelCenter DITA, optiSLang DocBook, or DevRelDocs API Markdown)
4. Determines the right release branch from the iteration path and/or comments
5. Creates a properly named working branch in git (for example, `LGP/27R1/12345-update-ldap`)
6. Adds the changes specified in the ticket

Then we work on edits together. The AI applies the corporate style guide automatically because I've taught it our rules (more on that below).

When I'm satisfied, I say **Make it so**. It commits to the right location (Doc repos or GitHub for API), with the right message format (linking the work item in ADO), adds AnsMelanie as a reviewer for API docs, merges the target, pushes the changes, opens the PR with auto-complete set, and self-approves where appropriate. If the change needs to forward-merge into later releases, I ask it to cherry-pick, and it does that across every applicable branch.


### Writing and editing -- the style guide is invisible

When I edit a `.dita`, `.ditamap`, `.xml` (DocBook), or API Markdown file, Cursor automatically applies the right rule set. I converted both corporate style guides (the DITA/DocBook one and the Developer Portal API one) into Cursor skills, so the AI:

- Uses our terminology substitutions ("click on" -> "click", "fly-out menu" -> "shortcut menu", and 50+ more)
- Applies our voice and tense conventions
- Uses entity references for product names (`&pn257g;` instead of hardcoding "optiSLang")
- Follows our heading capitalization rules per output format
- Catches forbidden phrases (no contractions, no Latin abbreviations, no "please")
- Formats XML tags consistently per file type

I never have to remind it. It just follows the rules.

Both style-guide skills are packaged as zip files (`ansys-doc-guidelines.zip` for DITA/DocBook and `api-documentation.zip` for the Developer Portal) and are available to any doc writer who wants to install them. 

### Release deliverables -- RIL, KIL, Release Notes

At the end of every release cycle or service pack, every doc writer has the same tasks: produce a Resolved Issues List, a Known Issues List, and Release Notes. Each one can require walking through 50-100+ child tickets in ADO, deciding which qualify, writing a consistent summary, and converting it all to DocBook XML or DITA.

Now I just say **"draft the RIL for ticket 1234567."** The AI:

1. Pulls every child ticket from the parent
2. Filters by state and resolution reason (RIL only includes "Problem corrected" items, excluding "Not a Bug" / "Duplicate" / "Won't Fix")
3. Writes a consistent one-line summary for each qualifying item
4. Hands me a Markdown draft for review

I edit the Markdown like a normal document and send it off for review. When I'm happy, I say **"insert the RIL"** and it converts to the right XML format and inserts into the right file. Same workflow for the KIL (with workaround extraction from comments) and Release Notes (grouped by category, with sub-bullets). One of the best parts for me is that the AI knows or finds the appropriate repo folders, while I always forget where they are (or where I wrote them down last time).

### Monitoring -- things that should bug me, when they should bug me

A lot of "doc work" is actually "noticing things." I now have automated monitors that bug me only when bugging is warranted:

- **Corporate Install Doc Monitor** -- watches the shared corp install docs repo for changes that would affect the MC and oSL Install Guides. Cadence-based: checks daily near ECC, weekly otherwise. Silent unless something changed.
- **Internet Help Update Scanner** -- checks the Corporate-DOC calendar for "Internet Help Updates". Then on XML edit deadline days, it scans the last three release branches for doc changes and tells me which books need to be pushed so I can include them in the DBSI ticket.
- **API Pipeline Health Check** -- watches 8 API doc build pipelines and alerts me only when something fails.
- **Friday Repo Monitor** -- watches Jason's `Friday` bot repo for new skills or hooks I might want to adapt (more on Friday in the next section).

Every one of these used to be mental work to "remember to check the calendar" or "find out from Jason". Now they fire when they need to, and stay quiet otherwise.

### End of day -- "Goodnight, Flo"

When I'm wrapping up, I say **"Goodnight, Flo"** and Flo writes a diary entry to the workspace's `diary.md` summarizing what happened today, what's still open, and any context tomorrow's me will need. The next morning's briefing reads from that diary so I land back in context fast. On Fridays, it also checks my calendar for Monday; if I have our team's "How I AI" meeting, then my agent creates my prep doc (scans my work since the last AI meeting and summarizes my AI work) so Monday's biweekly is ready.

---

## How the whole thing is built

### Where Flo comes from

My assistant is named **Flo**, but the underlying bot pattern isn't mine -- it's adapted from **Friday**, Jason Kaiser's personal bot repo. Jason built Friday as a general-purpose Cursor assistant; I took the concept, kept the parts that made sense for documentation work, and rebuilt the rest around my own workflow. So when you see references to Jason's `Friday` repo (for example, the Friday Repo Monitor in the previous section), that's where the architecture originated.

What's mine: the doc-team-specific skills (style guides, ADO ticket flow, RIL/KIL/Release Notes generation, install-doc monitoring, internet-help scanner, sprint-review and Charlie-backlog reports), the morning briefing tailored to my actual data sources, and the customizations to the underlying rules so the assistant behaves like a documentation-focused operator rather than a general coding assistant.

### The pieces

The architecture is simple enough that anyone reading this could replicate it:

| Component | What it is | Where it lives |
|-----------|------------|----------------|
| **Skills** | Markdown files (`SKILL.md`) that teach the AI how to do a specific task | `~/.cursor/skills/<skill-name>/` |
| **Rules** | Markdown files (`.mdc`) that apply guidelines globally or to specific file types | `~/.cursor/rules/` or per-workspace `.cursor/rules/` |
| **Commands** | Project-specific instruction files invoked by `/command` | `.cursor/commands/` in the workspace |
| **Diary files** | Per-workspace `diary.md` files where the AI logs session state | Root of each workspace |
| **State** | Small JSON files that track what's been done | `~/.config/<skill-name>/state.json` |

A skill is just a text file. You can write one in an afternoon. You can share one by zipping the folder. You can adapt someone else's by editing the file.

### How diary files work

The diary file is the simplest of these but ends up being one of the most useful. Each workspace has a `diary.md` at its root that the AI reads at session start and writes to at session end. A typical diary entry records:

- What I was working on (ticket numbers, branches, repos)
- What got done and what's still open
- Any decisions made or context that would be hard to reconstruct tomorrow (for example, "decided to wait on Adam's review before cherry-picking 27R1")
- Open questions for the next session

The diary turns AI sessions from amnesiac one-offs into a continuous thread of work. When I open Cursor the next morning, the assistant already knows where I left off -- no re-explaining, no re-orienting. For a job like documentation where context-switching across tickets, repos, and release branches is constant, this single feature recovers more time per week than anything else on this list.

### Shareable skill packages

Several of these skills are already packaged as zip files in the `skill-packages/` folder so other doc writers can install and adapt them:

- `ansys-doc-guidelines.zip` -- the DITA/DocBook style enforcement skill
- `api-documentation.zip` -- the Developer Portal API style enforcement skill
- `ado-doc-workflow.zip` -- the end-to-end ADO doc ticket workflow (includes RIL/KIL/Release Notes generation)
- `llm-doc-converter.zip` -- the doc-to-LLM-Markdown converter

The companion document, `AI for Documentation - Project Summaries.md`, has install instructions and a per-project breakdown for each one.

---

*Cursor IDE: <https://cursor.com> -- the AI-first IDE that hosts the skills/rules system.*
*Claude: <https://anthropic.com/claude> -- the model that does most of the heavy lifting in my Cursor setup.*
