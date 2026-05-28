---
name: ado
description: >-
  Query Azure DevOps work items, pipeline status, and PRs on the on-prem TFS
  server. Use when the user needs to check ADO status, view work items, list
  PRs, investigate a failed build, or run the /ado dashboard. For documentation
  workflows (/ado doc), see the ado-doc skill. For sprint reviews (/ado Charlie),
  see the sprint-review skill.
---

# Azure DevOps (On-Prem TFS) Skill

Query work items, pipelines, and pull requests on `ado.internal.synopsys.com` (Synopsys-hosted on-prem TFS, migrated from `tfs.ansys.com` on 2026-05-23) via the REST API with NTLM auth.

## Hard Rule — Never Queue Builds Without Permission

**Do NOT POST to `/_apis/build/builds` (queue a build) without explicit per-definition consent from Leslie.** This is enforced by the global rule at `~/.cursor/rules/no-unsolicited-builds.mdc`. Generic phrases like "test the pipeline", "trigger a build", "make sure CI works" are NOT sufficient — always confirm the specific definition ID + name + branch first.

Read-only diagnostics (fetch definitions, status, logs, timeline, queue health, validation results) are always fine. Anything that produces a build artifact, publishes, deploys, or updates a reference is NOT fine without explicit per-definition consent.

## Credentials

The `.env` file lives at `$env:USERPROFILE\.env` with Ansys network credentials:

```
ADO_Username=SYNOPSYS\<username>
ADO_Password=<password>
```

**Auth method:** NTLM via `Invoke-RestMethod -Credential <PSCredential>`. PATs do NOT work against this server.

### IMPORTANT — Never put the password on a command line

Do NOT use `curl.exe -u "$($env:ADO_Username):$($env:ADO_Password)"` (or `wget`, `Invoke-WebRequest`, or anything that spawns a child process with the credential in argv). PowerShell expands the variable BEFORE `CreateProcess`, so the literal password lands in the child process's command line where Win32 process auditing, WMI `Win32_Process.CommandLine`, Defender for Endpoint, and any EDR can read it. Synopsys security has flagged this exact mistake. The hook `gate-credential-leak.ps1` will block it.

Use the shared helper instead:

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$wi = Invoke-AdoRest -Uri 'https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?api-version=6.0'
```

`Invoke-AdoRest` is a `Invoke-RestMethod` wrapper that:
- Reads `ADO_Username` / `ADO_Password` from `~/.env` and caches a `[PSCredential]` for the session.
- Authenticates via NTLM in-process (no child process spawned).
- Accepts `-Method Get/Post/Patch/Put/Delete`, `-Body <obj-or-json-string>`, `-ContentType`, `-OutFile`, `-Headers`, `-TimeoutSec`.

For complex flows you can also do it manually:

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$cred = Get-AdoCredential
$resp = Invoke-RestMethod -Uri $url -Credential $cred -Method Patch `
          -Body $jsonBody -ContentType 'application/json-patch+json'
```

**Important:** `ADO_Username` already includes the `SYNOPSYS\` domain prefix (formerly `ANSYS\`). Do NOT prepend it again.

## Server Details

- **Base URL:** `https://ado.internal.synopsys.com/tfs`
- **Primary Collection:** `ANSYS_Development`
- **Key Projects:** `Portfolio`, `ModelCenter`, `optiSLang`, `optiSLang_collab`, `DIAMOND`, `ConanDev`
- **API Version:** `api-version=6.0`

## Available Collections

ANSYS_Development, EDI_Collection, ModelCenter, ANSYS_ModelCenter, ANSYS_EBU_Collection, Infrastructure_Collection, and others.

## Scratch Directory

All ticket-related downloads, attachments, helper scripts, extracted images, and ephemeral API JSON files go in `C:\GitRepos\.scratch\`:

- **Per-ticket files** (attachments, marked-up PDFs, source markdown from developers, ADO API cache JSON, extraction scripts, extracted images): `C:\GitRepos\.scratch\<ticket-id>-<short-slug>\`
- **Shared temp files** (PR body JSON, cherry-pick JSON, vote JSON, auto-complete JSON — files not tied to a specific ticket): `C:\GitRepos\.scratch\` (root level)
- **RIL/KIL/RN markdown drafts** stay in `%USERPROFILE%\Downloads\` so they are easy to find and send for review. These are the only ticket-related files that go in Downloads.

Folder naming follows the `<ticket-id>-<short-descriptive-slug>` convention (see `.cursor/rules/scratch-folder-naming.mdc`). When downloading an attachment from a ticket or creating a helper script, always use `C:\GitRepos\.scratch\<ticket-id>-<slug>\` (creating the subdirectory if it does not exist). Never place temp files directly in the repo working tree or in arbitrary locations.

## Commands

### `/ado item <id>` — Show work item details

Fetch a single work item by ID. Parse the URL if the user provides a full TFS URL (extract the ID from the end).

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$wi = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?`$expand=all&api-version=6.0"
```

Present a clean summary table:
- ID, Title, Type, State, Assigned To, Priority
- Area Path, Iteration Path, Target Release
- Created/Changed dates and by whom
- Description (strip HTML tags)
- Acceptance Criteria (strip HTML tags)
- Latest comment if present
- Child work items (from relations where rel = "System.LinkTypes.Hierarchy-Forward")

If the work item is in a different collection (e.g., EDI_Collection), try that collection if ANSYS_Development returns 404.

### `/ado items [query]` — List work items

Query work items assigned to the current user. Optional filter text narrows results by title.

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$wiql = @{
  query = "SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType], [System.AssignedTo] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> 'Closed' AND [System.State] <> 'Removed' ORDER BY [System.ChangedDate] DESC"
}
$ids = (Invoke-AdoRest -Uri 'https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/wiql?api-version=6.0' -Method Post -Body $wiql).workItems.id
```

Then fetch details for each returned ID (batch them, max 200 at a time):

```powershell
$idList = ($ids | Select-Object -First 200) -join ','
$details = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems?ids=$idList&fields=System.Id,System.Title,System.State,System.WorkItemType,System.AssignedTo&api-version=6.0"
```

Present as a markdown table: ID | Type | State | Title

### `/ado children <id>` — List child work items

Fetch the work item, extract child relations (rel = "System.LinkTypes.Hierarchy-Forward"), then batch-fetch those IDs.

Present as a table: ID | Type | State | Assigned To | Title

### `/ado query <WIQL>` — Run a custom WIQL query

Run an arbitrary WIQL query against ANSYS_Development.

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$resp = Invoke-AdoRest -Uri 'https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/wiql?api-version=6.0' `
          -Method Post -Body @{ query = '<WIQL>' }
```

### `/ado prs [project]` — List open pull requests

Default project: `ModelCenter`. User can specify another.

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$prs = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/<project>/_apis/git/pullrequests?searchCriteria.status=active&api-version=6.0"
```

Present as a table: PR ID | Repository | Title | Created By | Created Date

### `/ado pr <id> [project]` — Show PR details

```powershell
$pr = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/<project>/_apis/git/pullrequests/<id>?api-version=6.0"
```

### `/ado builds [project]` — List recent builds

Default project: `ModelCenter`.

```powershell
$builds = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/<project>/_apis/build/builds?`$top=20&api-version=6.0"
```

Present as a table: Build ID | Definition | Status | Result | Start Time | Requested By

### `/ado build <url-or-id>` — Investigate a failed build

Fetch a build's details, timeline, and logs, then triage the failure as a content/authoring issue (our side) or an infrastructure issue (server side).

**Input:** Either a full TFS build URL or a bare build ID.

- URL: `https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_build/results?buildId=12134237&view=results`
- Bare ID: `12134237` (defaults to project `Documentation`)

Parse the URL to extract collection, project, and build ID (see URL Parsing section).

#### Step 1 — Fetch the build summary

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$build = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/<collection>/<project>/_apis/build/builds/<buildId>?api-version=6.0"
```

Extract from the response:
- `result` (succeeded, partiallySucceeded, failed, canceled)
- `status` (completed, inProgress, etc.)
- `definition.name` — the pipeline/definition name
- `sourceBranch` — the branch that was built
- `requestedFor.displayName` — who triggered it
- `startTime`, `finishTime` — compute duration
- `reason` (manual, individualCI, pullRequest, schedule, etc.)

If `result` is not `failed` or `partiallySucceeded`, report that the build did not fail and show the summary only.

#### Step 2 — Fetch the timeline

```powershell
$timeline = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/<collection>/<project>/_apis/build/builds/<buildId>/timeline?api-version=6.0"
```

The response contains a `records` array of `TimelineRecord` objects. Each record has:
- `name` — step/task name
- `type` — "Stage", "Phase", "Job", or "Task"
- `state` — pending, inProgress, completed
- `result` — succeeded, succeededWithIssues, failed, canceled, skipped, abandoned
- `errorCount`, `warningCount`
- `issues[]` — each with `type` ("error" or "warning") and `message`
- `log.id` — ID of the detailed log for this step
- `workerName` — which build agent ran it

**Processing:**

1. Filter to records where `result == "failed"` — these are the failed steps.
2. Collect all `issues` where `type == "error"` from every record (not just failed ones — some errors appear on parent Job/Stage records).
3. Note the `log.id` for each failed Task-level record (type `"Task"`).
4. Note the `workerName` from the Job-level record for context.

#### Step 3 — Fetch logs for failed steps

For each failed Task record that has a `log.id`:

```powershell
$log = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/<collection>/<project>/_apis/build/builds/<buildId>/logs/<logId>?api-version=6.0"
```

If the log is very large, fetch just the tail (last ~200 lines):

```powershell
$tail = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/<collection>/<project>/_apis/build/builds/<buildId>/logs/<logId>?startLine=<totalLines-200>&api-version=6.0"
```

To determine total lines, first fetch the log list to get line counts:

```powershell
$logList = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/<collection>/<project>/_apis/build/builds/<buildId>/logs?api-version=6.0"
```

Each entry has `lineCount`. Use this to compute `startLine` for large logs.

#### Step 4 — Triage the failure

Scan all collected error messages (from `issues[]`) and log content for patterns. Classify into one of three verdicts.

**Content issue (our side)** — match any of these patterns (case-insensitive):

| Category | Patterns |
|----------|----------|
| DITA-OT errors | `DOTX`, `DITA-`, `topicref`, `conref`, `keyref`, `href` in error context |
| Validation | `ERROR` near `.dita`, `.ditamap`, `.xml` file references |
| Broken links/xrefs | `broken link`, `unresolved`, `not found` near `.dita`/`.xml`, `file not found`, `missing` near `reference`, `unable to resolve` |
| Missing images | `image not found`, `missing` near `.png`/`.svg`/`.jpg`/`.gif` |
| Transform errors | `xslt`, `saxon`, `fop error`, `transform` in error context |
| Schema validation | `validation failed`, `schematron` |

**Infrastructure issue (server side)** — match any of these patterns (case-insensitive):

| Category | Patterns |
|----------|----------|
| Agent problems | `agent` near `offline`/`unavailable`, `no agent`, `could not allocate`, `pool` near `queue` |
| Disk/resource | `disk space`, `out of memory`, `no space left`, `insufficient`, `quota` |
| Network | `timeout`, `connection refused`, `network error`, `502`, `503`, `504`, `ECONNRESET`, `ETIMEDOUT` |
| Licensing | `license`, `seat` near `unavailable` |
| Missing tools | `tool` near `not found`, `command not found`, `not recognized as` near `cmdlet` |
| Permissions | `access denied`, `401`, `403`, `permission denied` |
| TFS internal | `internal error`, `TF400`, `TF900`, `VS403` |
| Agent crash | `process` near `exit code`, `worker` near `terminated`, `task` near `failed unexpectedly` |

**Verdict logic:**

1. Scan all error issue messages and log content against both pattern sets.
2. If only content patterns match → **"Content issue (our side)"**
3. If only infra patterns match → **"Infrastructure issue (server side)"**
4. If both match → report both, but lead with whichever has more matches
5. If neither matches → **"Unclear — manual investigation needed"**

#### Step 5 — Present the report

**Build Summary:**

| Field | Value |
|-------|-------|
| Build ID | `<buildId>` |
| Definition | `<definition.name>` |
| Branch | `<sourceBranch>` |
| Requested By | `<requestedFor.displayName>` |
| Reason | `<reason>` |
| Started | `<startTime>` |
| Duration | `<computed>` |
| Result | `<result>` |
| Agent | `<workerName>` |

**Failed Steps:**

| Step | Task | Errors | Warnings |
|------|------|--------|----------|
| `<name>` | `<task.name>` | `<errorCount>` | `<warningCount>` |

**Error Messages:**

List all issues of type `error` from the timeline, one per line. If there are more than 20, show the first 20 and note how many were omitted.

**Log Excerpt:**

For each failed task, show the last ~50 lines of its log in a fenced code block. Label each block with the task name.

**Triage Verdict:**

Display the verdict prominently:

- **Content issue (our side):** Explain which specific error(s) point to a DITA/link/image/transform problem. Suggest what to fix (e.g., "broken conref in `topic_x.dita`", "missing image `screenshot.png`").
- **Infrastructure issue (server side):** Explain which specific error(s) point to an agent/network/resource problem. Suggest next steps (e.g., "re-queue the build", "contact the build infra team").
- **Unclear:** Show evidence from both sides and recommend manual log review.

### Documentation workflows (`/ado doc`)

All `/ado doc` subcommands have been moved to the dedicated **ado-doc** skill at `%USERPROFILE%\.cursor\skills\ado-doc\SKILL.md`. Read that skill for:

- `/ado doc <id>` — full ticket workflow (fetch, branch, apply changes)
- `/ado doc <id> update` — incremental update from new comments
- `/ado doc commitpr` — commit, push, create TFS PR
- `/ado doc commitapi` — commit, push, create GitHub PR (DevRelDocs)
- `/ado doc cherry [pr-id]` — cherry-pick forward
### Release deliverables (RIL, KIL, Release Notes)

RIL, KIL, and Release Notes commands have been moved to the dedicated **ado-release-docs** skill at `%USERPROFILE%\.cursor\skills\ado-release-docs\SKILL.md`. Read that skill for:

- `/ado doc RIL <id>` / `/ado doc RIL` — Resolved Issues List (draft / insert)
- `/ado doc KIL <id>` / `/ado doc KIL` — Known Issues List (draft / insert)
- `/ado doc ReleaseNotes <id>` / `/ado doc ReleaseNotes` — Release Notes (draft / insert)

### Sprint review (`/ado Charlie`)

Sprint review materials generation has been moved to the dedicated **sprint-review** skill at `%USERPROFILE%\.cursor\skills\sprint-review\SKILL.md`. Read that skill for `/ado Charlie <iterations>`.

### `/ado dashboard [id]` — Current work dashboard with standup context

Shows the status of a doc Feature ticket, its children, and grandchildren, focused on **what is actively being worked** and **what could be picked up next**.

**Default root ticket:** `1419305` (27R1 — no argument needed). Pass an optional `<id>` to dashboard a different ticket (e.g., `/ado dashboard 1305252`).

#### Step 1 — Fetch the full hierarchy

Fetch ticket 1419305 with `$expand=all`. Extract child IDs (hierarchy-forward) and related IDs. Batch-fetch children with `$expand=all` to get their own hierarchy-forward relations. Batch-fetch all grandchildren.

For every item extract: `System.Id`, `System.Title`, `System.State`, `System.WorkItemType`, `System.AssignedTo`, `System.IterationPath`.

#### Step 2 — Classify items into sections

Separate all children and grandchildren into two groups:

- **Active work:** State is `Active` (at any level — child or grandchild)
- **Backlog:** State is `New` (at any level)
- **Done:** State is `Closed`, `Resolved`, or `Removed` — collect but show in a collapsed section at the end

A child User Story is "Active" if it or any of its grandchildren are Active. A child is "Backlog" if it and all its grandchildren are New. A child is "Done" if it and all its grandchildren are Closed/Resolved/Removed.

#### Step 3 — Cross-reference standup notes

Read standup files (current month + previous month) from:
```
<your-standup-folder>\
```

For each **Active** item, search Leslie's standup sections for the ticket ID or title keywords (case-insensitive). Also use the alias table (e.g., "screenshot project" → 1419313, "oSP3D API conversion" → 1445200).

**Condense standup mentions:**
- Show at most the **3 most recent distinct mentions** as a brief phrase (not full bullets).
- If the same item appears across many days with the same phrasing (e.g., "worked on screenshot project" x15), condense to a date range: "Mar 9 – Apr 27 (ongoing)".
- For impediments: only show impediments from the **most recent** standup that mentions this item. Skip if none.

For **Backlog** items: skip standup cross-referencing entirely. These haven't been started.

#### Step 4 — Generate the markdown dashboard

Output file: `%USERPROFILE%\Downloads\Dashboards\dashboard_1419305_YYYY-MM-DD.md` (using today's date, e.g., `dashboard_1419305_2026-04-27.md`)

**Structure:**

```markdown
# Doc Work Dashboard — 2027R1

*Generated: <date>*

## Active Work

| # | Story | Task | State | Recent Activity | Impediments |
|---|-------|------|-------|-----------------|-------------|
| [id](url) | Story title | Task title | Active | Latest 3 mentions condensed | Impediment or — |

Group rows by parent User Story. The Story column shows the parent story title on its first row, then blank for subsequent tasks under the same story. If the story itself is the active item (no active grandchildren), show it as a single row.

## Backlog

| # | Story | Task | Iteration |
|---|-------|------|-----------|
| [id](url) | Story title | Task title | IT-5 |

Same grouping by parent story. These are items in `New` state — potential next work.

---

<details><summary>Completed / Removed (<count> items)</summary>

| # | Title | State |
|---|-------|-------|
| [id](url) | Title | Closed |

</details>
```

#### Step 5 — Present summary to user

Show a brief count: X active, Y backlog, Z done. List any open impediments prominently. Show the output file path.

## URL Parsing

### Work item URLs

If the user pastes a full TFS URL like:
`https://ado.internal.synopsys.com/tfs/ANSYS_Development/Portfolio/_workitems/edit/1345958`

Parse it to extract:
- **Collection:** `ANSYS_Development`
- **Project:** `Portfolio`
- **Work Item ID:** `1345958`

Use the extracted collection in the API call (not always ANSYS_Development).

### Build URLs

If the user pastes a build results URL like:
`https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_build/results?buildId=12134237&view=results`

Parse it to extract:
- **Collection:** `ANSYS_Development` (path segment after `/tfs/`)
- **Project:** `Documentation` (path segment before `/_build/`)
- **Build ID:** `12134237` (from the `buildId` query parameter)

Use these values in the build API calls. If the user provides only a bare build ID, default to collection `ANSYS_Development` and project `Documentation`.

## Important: `#` in PR Descriptions

ADO auto-links any `#<number>` pattern in PR titles and descriptions to a work item. Only use `#<number>` when referring to an actual **work item ID**. Never prefix PR numbers with `#` — use the full PR URL or plain number instead. For example:

- **Correct:** `Cherry-pick of PR 678008 (https://ado.internal.synopsys.com/...pullrequest/678008)`
- **Wrong:** `Cherry-pick of PR #678008` — ADO will resolve 678008 to an unrelated work item

This applies to all PR descriptions and titles across `commitpr` and `cherry` commands.

## Output Formatting

- Always present results as clean markdown tables
- Strip HTML from description/acceptance criteria fields
- Show dates in human-readable format (e.g., "Jan 8, 2026")
- For work item details, use a key-value table format (Field | Value)
- Truncate long descriptions at ~500 chars with "..." unless user asks for full detail

## Error Handling

- If 401: credentials may be expired. Ask the user to update their `.env` file
- If 404: try other collections (EDI_Collection, ModelCenter, etc.)
- If connection fails: check VPN — TFS requires Ansys network access
- If `.env` file not found: ask the user to create one (see Credentials section above)
