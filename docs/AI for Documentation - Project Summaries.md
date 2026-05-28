# AI for Documentation -- Project Summaries

*Leslie Poff, Staff Engineer, ModelCenter and optiSLang Collaborative Services Team*
*Last updated: May 15, 2026*

These are AI-driven documentation projects developed using Cursor IDE with Claude. Each project was built to solve a real pain point in our day-to-day documentation workflow. Most produce reusable Cursor "skills" (instruction files that teach the AI how to do a specific task) and "rules" (persistent guidelines the AI follows when editing files).

Where applicable, the Cursor skill/rule files are included as zip packages in the `skill-packages/` folder so other doc writers can install and adapt them.

---

## Table of Contents

1. [Style Guide Enforcement (DITA/DocBook)](#1-style-guide-enforcement-ditadocbook)
2. [Style Guide Enforcement (API / Developer Portal)](#2-style-guide-enforcement-api--developer-portal)
3. [LLM Documentation Converter](#3-llm-documentation-converter)
4. [AI Doc Accuracy Testing](#4-ai-doc-accuracy-testing)
5. [Automated Doc Ticket Workflow ("ado doc")](#5-automated-doc-ticket-workflow-ado-doc)
6. [Release Deliverables Generator (RIL / KIL / Release Notes)](#6-release-deliverables-generator-ril--kil--release-notes)
7. ["Good Morning, Flo" -- AI-Powered Morning Briefing](#7-good-morning-flo----ai-powered-morning-briefing)
8. [Corporate Install Doc Monitor](#8-corporate-install-doc-monitor)
9. [Internet Help Update Scanner](#9-internet-help-update-scanner)
10. [Other Projects with Corp Doc Potential](#10-other-projects-with-corp-doc-potential)

---

## 1. Style Guide Enforcement (DITA/DocBook)

**Status:** Complete
**Skill package:** `skill-packages/ansys-doc-guidelines.zip`

### Problem

The corporate Ansys documentation style guides (for DITA and DocBook XML) are long PDF documents that doc writers have to look up manually. When using AI to write or edit documentation, the AI has no knowledge of these standards and produces inconsistent output.

### Solution

Converted the official corporate style guides into a Cursor skill that the AI reads and follows whenever it touches DITA or DocBook files. The skill covers:

- Voice, tense, and person conventions
- Terminology substitutions (50+ entries, for example, "click on" becomes "click")
- UI element action verbs (button = click, check box = select/clear, etc.)
- Punctuation rules (serial comma, no contractions, no Latin abbreviations)
- Capitalization rules (title caps for headings, sentence case for body)
- XML formatting rules for both DITA and DocBook
- Entity references for product names (never hardcode -- use `&pn257g;` for optiSLang, etc.)
- Image and alt-text requirements
- Cross-reference and list formatting

### Impact for Corp Doc

Any doc writer using Cursor (or a similar AI tool) can install this skill so that AI-generated or AI-edited content automatically follows corporate standards. This replaces manual style-guide lookups and catches issues before review.

### How to Install

1. Unzip `ansys-doc-guidelines.zip` into your Cursor `~/.cursor/skills/ansys-doc-guidelines/` directory.
2. The AI will automatically reference it when editing `.dita`, `.ditamap`, or `.xml` (DocBook) files.
3. See the included `README.md` for details.

---

## 2. Style Guide Enforcement (API / Developer Portal)

**Status:** Complete
**Skill package:** `skill-packages/api-documentation.zip`

### Problem

API documentation for the Ansys Developer Portal follows a different style guide (Google developer documentation style, sentence case headings, specific `docfx.json` metadata requirements, etc.). AI tools don't know these rules and produce non-compliant output.

### Solution

Converted the API documentation guidelines into a Cursor skill covering:

- Package classification (REST API vs. API prose vs. Library/SDK)
- Required files and directory structure for each package type
- Markdown formatting rules (GitHub Flavored Markdown, UTF-8)
- Metadata requirements for `docfx.json` (title, summary, version, physics)
- API reference quality standards (OpenAPI validation, realistic examples)
- TOC configuration
- Changelog format
- Migration workflow (5-step process to the Developer Portal)
- Compliance checklist

### Impact for Corp Doc

Any team migrating documentation to the Developer Portal can install this skill so their AI assistant produces compliant packages on the first pass, reducing review cycles with the Dev portal team.

### How to Install

1. Unzip `api-documentation.zip` into `~/.cursor/skills/api-documentation/`.
2. See the included `README.md` for details.

---

## 3. LLM Documentation Converter

**Status:** Complete
**Skill package:** `skill-packages/llm-doc-converter.zip`

### Problem

LLMs don't consume documentation the way humans do. A 200-page user guide in DITA or DocBook is too large for any AI to process effectively. Even converting to Markdown doesn't help if the files are too long or lack structured metadata.

### Solution

Built a Python-based converter (with a Cursor skill wrapper) that transforms documentation from DITA, DocBook, HTML, PDF, or Word into flat, LLM-optimized Markdown files. Each topic becomes a self-contained file with:

- **YAML front matter** with product name, version, source book, and original file path
- **TL;DR summary** for quick retrieval
- **Question-oriented titles** ("Installing X" becomes "How do I install X?") to match how users query AI
- **Resolved entity references** (no raw `&pn257g;` in output)
- **Images as alt-text descriptions** since LLMs can't see screenshots
- **Semantic filenames** derived from topic title

The converter also produces an `llms.txt` master index and a `skipped-pages.md` report.

### Results

- **ModelCenter:** 1,334 topics converted (User Guide, Install Guide, MBSE, Plugins, Remote Exec, Release Notes)
- **optiSLang:** 511 topics converted (User's Guide, Install Guide, Tutorials, Interfaces, Release Notes, Calculator Reference)
- The resulting corpus is used as ground truth for the AI accuracy testing project

### Impact for Corp Doc

Any product team can run this converter against their DITA or DocBook source to produce an LLM-optimized version of their documentation. This is directly useful for:

- Feeding product docs to internal AI assistants or chatbots
- Building RAG (Retrieval Augmented Generation) pipelines
- Testing whether AI search engines can answer questions about your product correctly

### How to Install

1. Unzip `llm-doc-converter.zip` into `~/.cursor/skills/llm-doc-converter/`.
2. Install Python dependencies: `pip install lxml pymupdf4llm python-docx`
3. Run: `python scripts/convert.py <source_dir> <output_dir> --product "Your Product" --prefix yp --version "27.1"`

---

## 4. AI Doc Accuracy Testing

**Status:** In progress

### Problem

External AI search engines (ChatGPT, Perplexity, Claude, Gemini, Copilot) consume our public help site (`ansyshelp.ansys.com/public/`) and answer user questions based on it. But we have no visibility into:

- What questions users or bots are asking about our products
- Whether the AI responses are accurate
- Where our documentation has gaps that cause wrong or incomplete AI answers

### Solution (prototype complete)

Building a reusable test harness that:

1. Discovers what questions users and bots are asking about ModelCenter and optiSLang
2. Queries multiple AI engines programmatically with those questions
3. Scores responses for accuracy against our LLM-docs corpus (ground truth)
4. Identifies documentation gaps where bots give wrong or incomplete answers
5. Fixes the source documentation and retests until bots return correct answers

**Progress (May 2026):** Prototype mocked up and tested with the full question set for both ModelCenter and optiSLang. The idea was inspired by the Write the Docs 2026 conference — specifically the "Web Help and Crawlers" talk about building test suites for documentation accuracy through AI answer engines.

### Impact for Corp Doc

This is designed as a **reusable toolkit**. Once proven on MC and oSL, any product team can:

- Point it at their own LLM-docs corpus
- Discover what their users are asking AI about
- Find and fix doc gaps before users hit them
- Track AI answer accuracy over time

This addresses a growing corporate concern: if AI is how users find our documentation, we need to make sure the AI is giving correct answers.

---

## 5. Automated Doc Ticket Workflow ("ado doc")

**Skill package:** `skill-packages/ado-doc-workflow.zip`

### Problem

The typical documentation ticket workflow involves many manual steps:

1. Open the ticket in ADO, read the description and comments
2. Figure out which repo and branch to use
3. Create a working branch with the correct naming convention
4. Make the documentation changes (in DITA or DocBook XML)
5. Commit with the right message format (linking the work item)
6. Create a PR with the correct target branch, auto-complete, and reviewer settings
7. Cherry-pick the PR forward to all applicable release branches
8. Update the ticket state

Each step has specific conventions, and getting any of them wrong means rework.

### Solution

The `ado-doc` Cursor skill automates the entire pipeline. When I say "pick up ticket [ID]," the AI:

1. Fetches the ticket from ADO (via NTLM-authenticated REST API)
2. Reads the description, comments, and attachments to determine what doc work is needed
3. Identifies the correct repo (ModelCenter DITA, optiSLang DocBook, or DevRelDocs API Markdown)
4. Determines the target release branch from the ticket's iteration path
5. Creates a properly named working branch (for example, `LGP/27R1/[ID]-update-ldap`)
6. Applies the documentation changes following the correct XML/Markdown conventions
7. On "ship it" -- commits, merges target, pushes, creates the PR, sets auto-complete, and self-approves (MC only)
8. On "cherry-pick" -- forward-picks to all applicable release branches with PRs for each

### Impact for Corp Doc

The skill demonstrates how to integrate AI into an enterprise documentation workflow end-to-end. The patterns are transferable:

- **ADO integration via REST API:** Any team using TFS/ADO can adapt the API calls
- **Branch naming and PR conventions:** Customizable per team
- **Cherry-pick automation:** Eliminates the most tedious part of multi-release maintenance
- **Style-guide integration:** Automatically applies the style guide skills when editing

The skill is specific to one team's repos, but the architecture is reusable.

---

## 6. Release Deliverables Generator (RIL / KIL / Release Notes)

**Status:** Complete
**Skill package:** included in `skill-packages/ado-doc-workflow.zip`

### Problem

At the end of every release cycle or service pack, doc writers must produce three deliverables:

- **Resolved Issues List (RIL):** Every bug fix in the release, written as a one-line summary with the ticket number.
- **Known Issues List (KIL):** Every unresolved known issue, with workarounds where available.
- **Release Notes:** New features and enhancements, with detailed descriptions and sub-capabilities.

Producing these requires opening a parent tracking ticket in ADO, reading through every child ticket (often 50-100+ items), deciding which qualify for each list, writing a consistent summary for each, converting to DocBook XML or DITA, inserting into the correct files, and archiving the previous release's content. It's tedious, error-prone, and time-consuming.

### Solution

The `ado-release-docs` Cursor skill automates the entire process with a two-phase workflow for each deliverable:

**Phase 1 -- Draft generation:** Given a parent ADO ticket, the AI:

1. Fetches all child and related tickets (via NTLM-authenticated REST API)
2. Filters them by state and resolution reason (for example, RIL includes only items resolved as "Problem corrected," excluding "Not a Bug," "Duplicate," and "Won't Fix")
3. Writes a concise, consistent summary for each qualifying item
4. Produces a Markdown draft file for human review

**Phase 2 -- Insertion:** After the writer reviews and approves the draft, the AI:

1. Converts the approved Markdown to DocBook XML (or DITA for ModelCenter)
2. Archives the previous release's content (moves "current" to "archive" with proper cross-reference stripping)
3. Inserts the new content into the correct XML files (up to three locations per product)
4. Hands off to the standard commit/PR workflow

### What the AI handles for each deliverable

| Deliverable | Filtering logic | Output format |
|---|---|---|
| **RIL** | Resolved/Closed + "Problem corrected" resolution, user-facing fixes only | One-line bullets with ticket numbers |
| **KIL** | Active/New items + "Won't Fix"/"By Design" closures, with workarounds extracted from comments | Bullets with optional workaround sub-sections |
| **Release Notes** | Features/enhancements/significant fixes, grouped by category | Headed sections with detailed descriptions and sub-bullets |

### Impact for Corp Doc

Every product team produces these same three deliverables every release. The patterns are directly transferable:

- **Filtering logic** adapts to any ADO ticket hierarchy -- just point it at your release tracking ticket
- **Summary writing** follows a consistent voice and format across all entries
- **Archive migration** handles the fiddly XML restructuring (stripping images, cross-references, and links from archived content)
- **Multi-file insertion** updates all required locations in one pass

The skill currently targets ModelCenter (DITA) and optiSLang (DocBook), but the architecture works for any product with a similar release ticket structure.

---

## 7. "Good Morning, Flo" -- AI-Powered Morning Briefing

### Problem

At the start of each day, a doc writer needs to:

- Check what they worked on yesterday (dig through git logs, standups)
- Check their calendar for meetings
- Check the Corp-DOC calendar for upcoming deadlines (XML edit dates, FCA, ECC)
- Check if any monitored repos have changed (corporate install docs, API pipelines)
- Check if any doc builds are failing
- Check for reminders they left for themselves

This takes 15-30 minutes of clicking through ADO, Outlook, Jenkins, and git.

### Solution

"Good Morning, Flo" is an AI-powered morning briefing that runs all of these checks in one command. When I say "good morning" to my AI assistant (named Flo), it runs through a structured sequence:

1. **Yesterday's work** -- Summarizes git activity and standup entries
2. **Calendar** -- Shows today's meetings and upcoming Corp-DOC deadlines (via Microsoft Graph API)
3. **Reminders** -- Checks a local reminders file for anything due today
4. **Corporate install doc monitor** -- Checks if the corporate install docs have changed (cadence-based: daily near ECC, weekly otherwise)
5. **Internet help update scanner** -- On XML edit deadline days, scans release branches for doc changes and reports which books need rebuilding
6. **API pipeline health** -- Checks 8 API doc build pipelines for failures
7. **Sprint review folder** -- On the first day of a new sprint, creates the review folder and copies the template
8. **Friday repo monitor** -- Checks if Jason's Friday installer repo has new skills or hooks

The entire briefing completes in under 60 seconds and presents a clean, structured summary.

### Impact for Corp Doc

The components are modular and individually useful:

- **Calendar integration** (Microsoft Graph) is reusable by anyone with an Outlook calendar
- **Corp-DOC deadline awareness** (XML edit dates, ECC, FCA) benefits every doc writer
- **Corporate install doc monitor** could be adapted to monitor any shared doc area
- **Reminder system** is a simple file-based system any individual can use
- **The "briefing" pattern** itself is transferable -- any team could build their own version with their own checks

---

## 8. Corporate Install Doc Monitor

**Skill package:** included in the Flo briefing system

### Problem

The ModelCenter Install Guide references the corporate (unified) installation documentation, which is owned by another team. When they update their docs, we need to update ours to stay consistent. But there's no notification system -- we only find out when a customer reports a mismatch, or when we happen to check.

### Solution

An automated monitor that:

1. Checks `origin/develop` in the documentation repo for changes to `docu_corp/installation/` paths
2. Classifies changes by topic (Unified Installer, Windows/Linux platform requirements, install procedures)
3. Alerts only when something relevant has changed (silent otherwise)
4. Adjusts check frequency based on proximity to ECC (daily within 30 days, weekly within 60, monthly otherwise)
5. Uses the Corp-DOC calendar to detect imminent SP deadlines from Emilee Tkacik

### Impact for Corp Doc

Any product team that depends on shared corporate documentation sections could adapt this pattern to monitor their own dependencies.

---

## 9. Internet Help Update Scanner

### Problem

On XML edit deadline days, doc writers need to figure out which of their books have changes on previously-published release branches so they can request pushes to production from the DBSI team. This means manually running git log commands across multiple branches in multiple repos.

### Solution

An automated scanner that:

1. Reads the Corp-DOC calendar to find XML edit deadline dates
2. Scans the 3 most recent major release branches (plus SPs) in both the documentation and ModelCenter repos
3. Identifies commits in our doc areas between the previous deadline and today
4. Maps changed files to book names (User Guide, Install Guide, Release Notes, etc.)
5. Produces a ready-to-use list for the DBSI ticket
6. Offers to auto-create the DBSI User Story in ADO

### Impact for Corp Doc

Every doc writer has to do this same check on XML edit deadline days. This automation could be adapted per-product by changing the file-to-book mapping table.

---

## 10. Other Projects with Corp Doc Potential

These are additional AI projects from the project log that could benefit the broader documentation community, even though they don't have dedicated skill packages.

### Doc-to-Markdown Conversion (for any purpose)

Used AI to convert optiSLang DocBook documentation to Markdown in minutes -- a task that previously took days. The AI can now handle large files that were too big for earlier models. This is useful for anyone who needs their docs in Markdown format (for wikis, GitHub, internal tools, etc.).

### Writing Documentation from Code

For DigitalThread and MCMBSE, used AI to read the source code repositories and write up documentation that developers hadn't provided. The AI produced accurate, structured content that only needed image updates. This approach works for any product where the code exists but the documentation is thin.

### Word/Markdown to DocBook/DITA Conversion

Converted Word docs, HTML, and Markdown into properly formatted DocBook XML and DITA, matching existing file conventions. Used on multiple optiSLang tickets (tutorials, API docs, feature updates). The AI reads an example file from the repo and produces output in the same style.

### Multi-Branch Cherry-Pick Automation

Automated the process of ensuring that documentation changes on one release branch are forward-merged to all subsequent branches. Completed the 26R1-to-27R1 cherry-pick for both ModelCenter and optiSLang in about an hour -- a task that typically takes a full day or more of manual work.

### Doc Reorganization Analysis

Used AI (GPT-5 via Microsoft 365 Copilot) to analyze user guides for user-friendliness and recommend restructuring. Applied to both ModelCenter (DITA) and optiSLang (DocBook) documentation. The AI recommended new landing pages and topic reordering based on user-task analysis.

---

## Appendix: What is a Cursor Skill?

A **Cursor Skill** is a Markdown file (`SKILL.md`) that teaches the Cursor IDE's AI assistant how to perform a specific task. Think of it as a detailed instruction manual that the AI reads before starting work. Skills can include:

- Step-by-step procedures
- API endpoints and authentication details
- File structure conventions
- Decision trees (if X, do Y)
- Error handling rules

Skills are stored in `~/.cursor/skills/<skill-name>/SKILL.md` and are automatically available to the AI when it recognizes a matching trigger pattern.

A **Cursor Rule** (`.mdc` file) is similar but applies globally or to specific file types. Rules are always-on guidelines rather than triggered workflows.

Both are plain-text files that can be shared, version-controlled, and adapted by other teams.
