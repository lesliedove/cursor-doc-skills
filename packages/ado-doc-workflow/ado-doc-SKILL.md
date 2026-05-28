---
name: ado-doc
description: >-
  Full documentation work item workflow for Ansys ModelCenter, optiSLang, and
  DevRelDocs API repos. Covers fetching tickets, creating branches, applying
  doc changes, committing, PRs, cherry-picks, and generating RIL/KIL/Release
  Notes. Use when the user says "pick up ticket", "work on ticket", "commit and
  PR", "make it so", "cherry-pick", "draft the RIL/KIL/release notes", or runs any
  /ado doc command.
---

# ADO Documentation Workflow

End-to-end commands for documentation work items: fetch a ticket from ADO, set up a branch, apply changes, commit, create PRs, cherry-pick forward, and generate release deliverables (RIL, KIL, Release Notes).

## Credentials

Load credentials from `C:\Users\ldove\.env` and use the shared NTLM helper (same as the [ADO skill](../ado/SKILL.md)):

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$wi = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?api-version=6.0"
```

`Invoke-AdoRest` is a wrapper around `Invoke-RestMethod -Credential $cred` with the `~/.env` credential pre-loaded. Auth method is **NTLM** in-process; no `curl.exe` is spawned.

### IMPORTANT — Never use `curl.exe -u "$env:..."` for auth'd calls

PowerShell expands `$env:ADO_Password` BEFORE `CreateProcess`, so the literal password lands in `curl.exe`'s argv where Windows process auditing, WMI `Win32_Process.CommandLine`, Defender for Endpoint, and any EDR can read it. Synopsys security has flagged this exact mistake. The hook `gate-credential-leak.ps1` will block it. Use `Invoke-AdoRest` (or `Invoke-RestMethod -Credential`) instead.

**Important:** `ADO_Username` in `.env` already includes the `SYNOPSYS\` domain prefix (formerly `ANSYS\`). Do NOT prepend it again. PATs do NOT work against this server.

## Server Details

- **Base URL:** `https://ado.internal.synopsys.com/tfs`
- **Primary Collection:** `ANSYS_Development`
- **API Version:** `api-version=6.0`

## Scratch Directory

All ticket-related downloads, attachments, helper scripts, extracted images, and ephemeral API JSON files go in `C:\GitRepos\.scratch\`:

- **Per-ticket files** (attachments, marked-up PDFs, source markdown from developers, ADO API cache JSON, extraction scripts, extracted images): `C:\GitRepos\.scratch\<ticket-id>-<short-slug>\`
- **Shared temp files** (PR body JSON, cherry-pick JSON, vote JSON, auto-complete JSON -- files not tied to a specific ticket): `C:\GitRepos\.scratch\` (root level)
- **RIL/KIL/RN markdown drafts** stay in `C:\Users\ldove\Downloads\` so they are easy to find and send for review. These are the only ticket-related files that go in Downloads.

Folder naming follows the `<ticket-id>-<short-descriptive-slug>` convention (see `.cursor/rules/scratch-folder-naming.mdc`). When downloading an attachment from a ticket or creating a helper script, always use `C:\GitRepos\.scratch\<ticket-id>-<slug>\` (creating the subdirectory if it does not exist). Never place temp files directly in the repo working tree or in arbitrary locations.

## PowerShell Execution Guidelines

**CRITICAL:** The Shell tool on Windows wraps commands in a temporary `.ps1` script. PowerShell variables like `$matches`, `$_`, `$since`, and string interpolation with `$()` are unreliable when passed as inline `-Command` strings because the outer shell may strip or mangle them.

**Rule:** For any PowerShell logic that uses `$matches`, `$_`, `ForEach-Object`, `Where-Object`, regex matching, or complex string interpolation:

1. Write the script to a temp `.ps1` file using the Write tool (place under `C:\GitRepos\.scratch\<ticket-id>-<slug>\`)
2. Execute it with `powershell -ExecutionPolicy Bypass -File "<path>"`
3. Delete the temp file afterward (or leave it if it'll be reused)

Simple commands (e.g., `git log`, `git checkout`) work fine inline. Auth'd ADO REST calls always use `Invoke-AdoRest` from the shared helper (see Credentials section), never `curl.exe -u`.

## Important: `#` in PR Descriptions

ADO auto-links any `#<number>` pattern in PR titles and descriptions to a work item. Only use `#<number>` when referring to an actual **work item ID**. Never prefix PR numbers with `#` -- use the full PR URL or plain number instead. For example:

- **Correct:** `Cherry-pick of PR 678008 (https://ado.internal.synopsys.com/...pullrequest/678008)`
- **Wrong:** `Cherry-pick of PR #678008` -- ADO will resolve 678008 to an unrelated work item

This applies to all PR descriptions and titles across `commitpr` and `cherry` commands.

## Commands

### `/ado doc <id>` -- Documentation work item workflow

End-to-end command: fetch a doc ticket from ADO, analyse the required documentation changes, set up a working branch in the correct repo, and apply the changes.

**Scope:** This skill applies only to repos under `c:\GitRepos` and their children.

#### Step 1 -- Fetch the work item

Use the same API as `/ado item`:

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$wi = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?`$expand=all&api-version=6.0"
```

Parse the response and present a summary (ID, Title, State, Assigned To, Description stripped of HTML). Also fetch comments:

```powershell
$comments = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>/comments?api-version=3.0-preview"
```

And list attachments (from the `relations` array where `rel = "AttachedFile"`).

#### Step 2 -- Identify documentation work

Scan the description, acceptance criteria, comments, and attachment filenames for:
- Specific pages, topics, sections, or DITA files to update
- New content to add (new topics, sections, screenshots, etc.)
- Text corrections, rewording, or restructuring
- Screenshot additions or replacements
- References to specific guides (User Guide, Install Guide, Release Notes, Plugin docs, MBSE docs, etc.)

Summarize what documentation changes are needed, then proceed immediately to the next steps without waiting for confirmation.

#### Step 3 -- Determine the target repository

Three doc repos live under `c:\GitRepos`:

| Repo | Local path | Remote | Format |
|------|-----------|--------|--------|
| **ModelCenter** | `c:\GitRepos\ModelCenter` | `ANSYS_Development/Documentation/_git/ModelCenter` (TFS) | DITA |
| **documentation** (docu_optiSLang) | `c:\GitRepos\documentation` | `ANSYS_Development/Documentation/_git/documentation.git` (TFS) | DocBook XML |
| **DevRelDocs_API** | `c:\GitRepos\DevRelDocs_API` | `https://github.com/ansys/DevRelDocs.git` (GitHub) | Markdown |

**Important:** The API repository name for the documentation repo is `documentation.git` (with the `.git` suffix). The ModelCenter repo is just `ModelCenter` (no suffix). Always use these exact names in REST API calls to `_apis/git/repositories/<repo_name>/`.

Use clues from the ticket to pick the repo:
- If the ticket's Area Path, title, or description mentions **optiSLang** AND references the **Interfaces and Customizations** guide, the **Python API**, or a Developer Portal URL (`developer.ansys.com`), use `c:\GitRepos\DevRelDocs_API`. See the DevRelDocs_API section below for the special handling this repo requires.
- If the ticket mentions **optiSLang** but refers to the User Guide, Install Guide, Release Notes, or other standard optiSLang docs, use `c:\GitRepos\documentation`.
- Otherwise default to `c:\GitRepos\ModelCenter`.

#### DevRelDocs_API -- special handling

This repo is hosted on GitHub (`ansys/DevRelDocs`), not TFS. It uses a different branching model and a different PR workflow.

**Repo structure for optiSLang API docs:**

Content is organized by release year folder, then by document folder:

```
DevRelDocs_API/
  2026R1/
    oSL_API_interfaces_customization-26-r1/
      docfx.json
      toc.yml
      changelog.md
      opti_api_python_nodes_config_files.md
      ... (other .md files)
      graphics/
  2027R1/
    oSL_API_interfaces_customization-27-r1/
    dpf-cpp-27-r1/
    dpf-framework-27-r1/
```

**Staging branch for 27R1 optiSLang API docs:**

The `oSL_API_interfaces_customization-27-r1` folder is copied from the previous release by Melanie (the DevRelDocs repo owner) at the start of each release cycle. Until she does this, changes accumulate on a **long-lived staging branch** rather than individual per-ticket branches.

- **Staging branch name:** `LGP/27R1/osl-interfaces-customization`
- **Do NOT open a PR** until Melanie has confirmed she has set up the `2027R1/oSL_API_interfaces_customization-27-r1/` folder structure on `main` and the staging branch can be merged.
- All 27R1 optiSLang API doc tickets go onto this **same** staging branch -- do not create a new branch per ticket.

**Workflow for a DevRelDocs_API ticket:**

1. Check whether `2027R1/oSL_API_interfaces_customization-27-r1/` exists on `main`:
   ```powershell
   git -C "C:\GitRepos\DevRelDocs_API" fetch origin
   cmd /c "dir C:\GitRepos\DevRelDocs_API\2027R1"
   ```

2. If the folder **does not exist** on main -- work on the staging branch:
   ```powershell
   git -C "C:\GitRepos\DevRelDocs_API" checkout LGP/27R1/osl-interfaces-customization
   git -C "C:\GitRepos\DevRelDocs_API" pull origin LGP/27R1/osl-interfaces-customization
   ```
   If the staging branch doesn't exist yet locally, create it from main and copy the previous release folder:
   ```powershell
   git -C "C:\GitRepos\DevRelDocs_API" checkout -b "LGP/27R1/osl-interfaces-customization"
   Copy-Item -Recurse "C:\GitRepos\DevRelDocs_API\2026R1\oSL_API_interfaces_customization-26-r1" `
       "C:\GitRepos\DevRelDocs_API\2027R1\oSL_API_interfaces_customization-27-r1"
   ```
   Then update `docfx.json` (change `"version"` and `"title"` from `2026 R1` to `2027 R1`) and add a new `## 2027 R1` section to `changelog.md`.

3. If the folder **does exist** on main -- Melanie has set it up. Treat it like a normal per-ticket branch:
   ```powershell
   git -C "C:\GitRepos\DevRelDocs_API" checkout main
   git -C "C:\GitRepos\DevRelDocs_API" pull origin main
   git -C "C:\GitRepos\DevRelDocs_API" checkout -b "LGP/27R1/<id>-short-description"
   ```

4. Make changes to the appropriate `.md` files in `2027R1/oSL_API_interfaces_customization-27-r1/`.

5. Add a bullet to `changelog.md` under `## 2027 R1` summarizing the change.

6. Commit and push:
   ```powershell
   git -C "C:\GitRepos\DevRelDocs_API" add 2027R1/oSL_API_interfaces_customization-27-r1/
   git -C "C:\GitRepos\DevRelDocs_API" commit -m "<short description> #<id>"
   git -C "C:\GitRepos\DevRelDocs_API" push -u origin HEAD
   ```

7. If on the staging branch: **do not open a PR yet** -- just push and inform the user the change is staged. If on a per-ticket branch (Melanie has set up main): run `/ado doc commitapi` to commit, push, and create a GitHub PR.

**optiSLang API docs: where content lives**

The `documentation` TFS repo (`opti_api_interfaces.xml`) is now a stub -- it contains only a redirect notice to the Developer Portal. Do **not** edit the content inside the commented-out XML there. All live content for the Interfaces and Customizations guide is in `DevRelDocs_API`.

#### Step 4 -- Determine the release branch

Look for a target release / iteration path in the work item fields:
- `Microsoft.VSTS.Scheduling.TargetDate`
- `System.IterationPath`
- `System.Tags`
- Any mention of a version number (e.g., "27.1", "26.2", "25R2") in the description or title

Map the version to a branch name pattern `releases/release-<version>` (e.g., `releases/release-27.1`).

If no release is identified, default to `develop` (currently maps to release **27.1**).

Verify the branch exists on the remote:

```bash
git -C "<repo_path>" ls-remote --heads origin "<branch_name>"
```

If the branch does not exist, list available release branches and ask the user which to use.

**SP branches and `build_internet` (documentation repo only):**

When the release team creates an SP branch (e.g., `releases/release-26.1_SP1`) in the `documentation` repo, they include **all** products but default every book to `build_internet="false"`. This means no product docs build for Cortex unless a doc writer explicitly flips the flag. If you are making doc changes on an SP branch, you **must** also set `build_internet="true"` on every non-deprecated book for the affected product -- otherwise the content won't appear on the help site. The deprecated books (those with `build_long_term_branch="false"`) should stay `build_internet="false"`.

This does not apply to the ModelCenter repo, which is separate and not part of the universal SP branch.

SP doc changes do **not** need to be cherry-picked forward -- the SP is a point-in-time snapshot.

**SP branch freshness check (documentation repo only):**

The release team may branch an SP from the main release branch (`releases/release-26.1`) before notifying doc writers. If doc commits landed on the main release branch *after* the SP was forked, the SP will be missing those changes. This happened with 26R1 SP1 (ticket 1450837) -- the SP was forked on Feb 3, 2026, but 19 optiSLang doc commits landed on 26R1 afterward and were never included.

**Before making any doc changes on an SP branch**, run this check:

```powershell
git -C "<repo_path>" fetch origin
git -C "<repo_path>" log --oneline --first-parent origin/releases/release-<version> --not origin/releases/release-<version>_SP<n> -- docu_optislang/ | Measure-Object -Line
```

If the count is non-zero, there are commits on the main release branch that the SP is missing. Cherry-pick them onto the SP working branch **before** making new changes:

1. List the missing commits with `--first-parent` to get the PR merge commits (not individual branch commits).
2. Verify each commit only touches `docu_optislang/` (or the relevant product directory) using `git diff-tree --no-commit-id --name-only -r <hash>`.
3. Cherry-pick in chronological order (oldest first) with `-m 1` for merge commits.
4. Skip any that result in empty cherry-picks (content already present on SP).

Do **not** do a full `git merge` of the main release branch into the SP -- that brings in every other product's changes and creates a mess. Cherry-pick only the oSL (or relevant product) commits.

#### Step 5 -- Pull the release branch

**Important: `global/` submodule handling when switching branches.**

On `develop`, `global/` is a **git submodule**. On older release branches (e.g., `releases/release-26.1_SP1`), `global/` is a **static folder**. Switching between these requires special handling:

**Switching FROM `develop` TO an older release branch:**

Before checkout, delete the `global/` directory (do NOT commit the deletion -- this is a local working-tree-only operation):

```powershell
git -C "<repo_path>" submodule deinit -f -- global
Remove-Item -Recurse -Force "<repo_path>\global"
Remove-Item -Recurse -Force "<repo_path>\.git\modules\global" -ErrorAction SilentlyContinue
```

Then checkout and pull:

```powershell
git -C "<repo_path>" checkout "<release_branch>"
git -C "<repo_path>" pull origin "<release_branch>"
```

**Switching FROM an older release branch BACK to `develop`:**

No special handling needed -- checking out `develop` will restore `global/` as a submodule automatically. Just run:

```powershell
git -C "<repo_path>" checkout develop
git -C "<repo_path>" submodule update --init --force -- global
```

**General: fix any remaining dirty submodules after checkout.**

Check for dirty state:

```powershell
git -C "<repo_path>" diff --name-only
```

If `tools` or `global` appear as modified (typically `-dirty` due to deleted/untracked files inside the submodule after a branch switch), restore them:

```powershell
git -C "<repo_path>" submodule update --force -- global
git -C "<repo_path>" submodule update --force -- tools
```

This only restores the submodule working tree to its expected commit -- it does **not** delete or commit anything. Only run for submodules that show as dirty.

#### Step 5b -- Activate the work item if it is New

Before creating a branch, check the work item's `System.State` (already fetched in Step 1). If the state is `New`, update it to `Active` -- if we're about to work on it, it should be active in ADO.

```powershell
$patch = @(
  @{ op = 'replace'; path = '/fields/System.State'; value = 'Active' }
)
Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?api-version=6.0" `
  -Method Patch -Body $patch -ContentType 'application/json-patch+json'
```

If the state is already `Active`, `Resolved`, `Closed`, or anything else, skip this step.

#### Step 5c -- Ensure the work item is linked to the doc tracking hierarchy

Check whether this work item is already a child or grandchild of ticket **1419305** (the current-release doc tracking Feature). If it is, skip this step. If it is not, add a **Related** link so the ticket appears in Leslie's doc work dashboard.

**Step 1 — Check the hierarchy.**

Fetch ticket 1419305 with `$expand=all`. Extract all child IDs (relations where `rel = "System.LinkTypes.Hierarchy-Forward"`). Batch-fetch those children with `$expand=all` and extract *their* child IDs the same way. This gives the full set of children and grandchildren.

If the current work item's ID appears anywhere in that set, it is already tracked — skip the rest of this step.

**Step 2 — Add a Related link.**

Choose the link target based on the work item type (already known from Step 1):

| Work item type | Link to |
|---|---|
| User Story | `1419305` |
| Task | `1431240` |

If the type is neither User Story nor Task (e.g., Bug, Feature), default to linking to `1419305`.

```powershell
$patch = @(
  @{
    op    = 'add'
    path  = '/relations/-'
    value = @{
      rel        = 'System.LinkTypes.Related'
      url        = "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<target-id>"
      attributes = @{ comment = 'Linked to doc tracking hierarchy' }
    }
  }
)
try {
  Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?api-version=6.0" `
    -Method Patch -Body $patch -ContentType 'application/json-patch+json'
} catch {
  # 409 Conflict = link already exists; that's fine.
  if ($_.Exception.Response.StatusCode.value__ -ne 409) { throw }
}
```

Where `<target-id>` is `1419305` or `1431240` per the table above.

#### Step 6 -- Create a working branch

Branch name format: `LGP/<release>/<id>-short-description`

Derive `<release>` from the target release branch determined in Step 4:
- Convert the version to the compact release label (e.g., `releases/release-26.1_SP1` -> `26R1_SP1`, `releases/release-27.1` -> `27R1`, `develop` for version 27.1 -> `27R1`)
- Pattern: take the major version, append `R`, then the minor version, then any suffix like `_SP1`

Derive `short-description` from the work item title:
- Lowercase
- Replace spaces with `-` or `_` (prefer `-`)
- Strip special characters
- Truncate to ~50 chars if needed

Example: ticket 1440597 on `releases/release-26.1_SP1` titled "Update LDAP" -> `LGP/26R1_SP1/1440597-update-ldap`
Example: ticket 1400001 on `develop` (27.1) titled "Update Copilot Screenshots" -> `LGP/27R1/1400001-update-copilot-screenshots`

```powershell
git -C "<repo_path>" checkout -b "LGP/<release>/<id>-short-description"
```

#### Step 7 -- Apply the documentation changes

Using the analysis from Step 2, make the changes to the appropriate files in the working branch. The two repos use different authoring formats.

**Key repo structure (ModelCenter) -- DITA:**
- `docu_dita/` -- DITA source files
  - `ModelCenter_UG/` -- User Guide topics (sub-folders: Features, GettingStarted, CommonTasks, Overview, Install, ReleaseNotes, etc.)
  - `ModelCenter_Inst/` -- Installation Guide
  - `ModelCenter_MBSE/` -- MBSE connector docs
  - `ModelCenter_RN/` -- Release Notes
  - `ModelCenter_Rem_Exec/` -- Remote Execution docs
  - `MC_Plugins/` -- Plugin documentation
  - `shared/` -- Shared/reusable DITA content
  - `BM_*.ditamap` -- Book maps (top-level maps for each guide)
- `docu_internet/csv/` -- CSV data for online help
- `global/` -- Global entities and shared resources (DO NOT MODIFY -- shared across repos)

**Key repo structure (documentation) -- DocBook XML:**

The optiSLang docs use ANSYS DocBook XML (not DITA). Key directories:
- `docu_optislang/` -- optiSLang DocBook source files
  - `opti_ug/` -- User's Guide chapters (e.g., `opti_ug_intro.xml`, `opti_ug_user_interface.xml`, `opti_ug_create_open_project.xml`, `opti_ug_systems_nodes_connections.xml`)
  - `opti_tut/` -- Tutorials
  - `opti_api/` -- Interfaces and Customization Guide
  - `opti_inst_lic/` -- Installation and Licensing Guide
  - `opti_new/` -- Release Notes (current + archive)
  - `opti_calc_pages/` -- Calculator/signal reference pages
  - `opti_multi_disc/` -- Methods for Multi-Disciplinary Optimization
  - `opti_pdo/` -- Additional optiSLang publication
- `global/` -- Global entities and shared resources (DO NOT MODIFY)

**Deprecated books (DO NOT add new content to these):**
The following directories contain legacy books whose content has been migrated into `opti_ug` and `opti_inst_lic`. They exist in the repo for older releases but must not receive new content:
- `opti_addin/` -- Excel Add-in (now in `opti_ug`)
- `opti_beta/` -- Beta features (now in `opti_ug`)
- `opti_stats_ug/` -- Statistics on Structures User's Guide (now in `opti_ug`)
- `opti_web_ser_inst/` -- Web Service Installation (now in `opti_inst_lic`)
- `opti_web_ser_ug/` -- Web Service User's Guide (now in `opti_ug`)

DocBook conventions in this repo:
- Books are assembled via `xi:include` in root XML files (e.g., `opti_ug/opti_ug.xml`), not `.ditamap` files.
- Entity references (e.g., `&pn257g;` for the product name) are defined in `.ent` files -- use the existing entities, do not hardcode product names.
- Sections use `<section id="...">`, cross-references use `<xref linkend="..."/>` and `<olink targetptr="..."/>`.
- Follow the existing XML indentation and structure conventions in each file.

**Critical restrictions (both repos):**
- **DO NOT** modify anything under `tools/` (this is a git submodule)
- **DO NOT** modify anything under `global/` (shared across repos; changes here affect all doc projects)
- Only edit files within `docu_dita/` (ModelCenter), `docu_optislang/` (documentation), `docu_internet/`, or other non-global, non-submodule directories
- When creating new topics, follow the existing naming conventions and file structure in the target directory
- For DITA (ModelCenter): add `<topicref>` entries to the relevant `.ditamap` when adding new topics
- For DocBook (documentation): add `<xi:include>` entries to the parent book XML when adding new chapters/sections
- If you need to create helper scripts, scratch files, or intermediate artifacts (e.g., extraction scripts, transformation tools, temp data), place them in `C:\GitRepos\.scratch\<ticket-id>-<slug>\` (see the Scratch Directory section). Never commit helper/scratch files to the working branch.

#### Step 7b -- Resize new images

After placing any new image files, read and follow the **image-resize** skill at `C:\Users\ldove\.cursor\skills\image-resize\SKILL.md` to resize them before committing. Only resize **newly added** images (i.e., files being added in this working branch). Do not resize images that already exist in the repo and are not being replaced.

After making changes, present a summary of all files modified/created.

### `/ado doc <id> update` -- Incremental update from new ticket comments

Update an existing documentation branch with new content from follow-up developer comments. Use this instead of `/ado doc <id>` when the initial documentation pass has already been done and the developer has posted corrections or additions as new comments on the same ticket.

**Scope:** Same repos and restrictions as `/ado doc <id>`.

#### Step 1 -- Fetch the work item and determine the repo

Use the same APIs as `/ado doc` Steps 1 and 3:

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$wi = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?`$expand=all&api-version=6.0"
```

Present a brief summary (ID, Title, State, Assigned To). Determine the target repository using the same logic as `/ado doc` Step 3.

#### Step 2 -- Detect the existing branch

Search for local and remote branches matching the ticket ID:

```powershell
git -C "<repo_path>" branch -a --list "*<id>*"
```

**Branch selection logic:**

1. Collect all matching branches, deduplicating local/remote pairs (e.g., `LGP/27R1/1436797-wdf-export-import` and `remotes/origin/LGP/27R1/1436797-wdf-export-import` count as one).
2. If exactly **one** unique branch matches: use it automatically.
3. If **multiple** branches match: present them to the user and ask which to use.
4. If **no** branches match: abort with a message suggesting the user run `/ado doc <id>` (without `update`) to create the initial branch first.

#### Step 3 -- Switch to the branch and pull the target

Fetch the latest state from the remote, then check out the selected branch:

```powershell
git -C "<repo_path>" fetch origin
git -C "<repo_path>" checkout "<branch_name>"
```

Determine the target release branch using the same logic as `/ado doc` Step 4 (parse the branch name's release label back to the branch name, e.g., `27R1` -> `develop`).

**Check for open PRs on the same ticket** before proceeding:

```powershell
$prs = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/<repo_name>/pullrequests?searchCriteria.status=active&api-version=6.0"
```

Filter the results for PRs whose `sourceRefName` contains the ticket ID. If any are found, warn the user:

> There is an active PR for this ticket: #<prId> (`<branchName>` -> `<targetBranch>`). This PR should be merged before making new changes, otherwise the new commit will be added to the open PR. Proceed anyway?

If no active PRs match, proceed silently.

**Pull the target branch** into the working branch so it absorbs any merged changes and is up to date:

```powershell
git -C "<repo_path>" pull origin <target_release_branch>
```

Apply the same `global/` submodule handling as `/ado doc` Step 5 -- deinit before switching to older release branches, restore submodules after checkout if they show as dirty.

#### Step 4 -- Fetch comments and identify new update content

Fetch all comments on the work item:

```powershell
$comments = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>/comments?api-version=3.0-preview"
```

**Comment parsing logic to find the update:**

1. Sort comments chronologically (oldest first).
2. Find the **most recent** comment by **Leslie Poff** (case-insensitive match on the `createdBy.displayName` field). This is the "marker" comment -- it is where Leslie tagged the developer and shared the pages that had the original/updated content.
3. All comments **after** that marker comment (by any author, but typically the developer) contain the new update content.
4. If there are multiple Leslie Poff comments, always use the **most recent one** as the marker. This handles multiple rounds of updates -- each new Leslie Poff comment resets the "baseline" so only the latest batch of developer responses is treated as new.
5. If there are **no comments after the marker**: report that no new update content was found and ask the user what to do.

**From the post-marker comments, extract:**

- Specific pages, topics, or sections to modify
- Verbatim text corrections or new wording
- New content to add (descriptions, procedures, UI labels, etc.)
- Screenshot additions or replacements
- References to specific files or guide sections

Present a summary of the identified update content before proceeding.

#### Step 5 -- Apply incremental changes

Using the parsed update content from Step 4, modify **only** the files that need updating. Follow the same authoring conventions as `/ado doc` Step 7 (DITA for ModelCenter, DocBook XML for the documentation repo).

**Key difference from a fresh `/ado doc`:** only change what the update requires. Do not re-examine or re-apply the original ticket's full scope. The original content is already in the branch (or merged into the target).

#### Step 6 -- Present summary

Display:

| Field | Value |
|-------|-------|
| Branch | `<branch_name>` |
| Branch state | Pulled latest `<target>` / Already up to date |
| Active PR warning | None / PR #<id> still open |
| Marker comment | Comment by Leslie Poff on `<date>` |
| Update comments | `<count>` comment(s) after marker |
| Files modified | `<list of files>` |

Summarize the changes made, then inform the user they can run `/ado doc commitpr` to commit, push, and create a PR.

### `/ado doc commitpr` -- Commit, push, and create a PR for the current doc branch

Run this after `/ado doc <id>` or `/ado doc <id> update` has applied changes and you are satisfied with them. This command commits the staged changes, pushes the branch, creates a pull request in TFS, and configures it for auto-complete.

**Prerequisites:** You must be on a working branch created by `/ado doc <id>` or `/ado doc <id> update` (format `LGP/<release>/<id>-short-description`), with changes staged or ready to stage.

#### Step 1 -- Identify context from the current branch

Parse the current branch name to extract:
- `<id>` -- the work item ID
- `<release>` -- the release label (e.g., `26R1_SP1`, `27R1`)

Determine the target release branch by reversing the release label:
- `26R1_SP1` -> `releases/release-26.1_SP1`
- `27R1` -> `develop`
- `26R2` -> `releases/release-26.2`
- Pattern: split on `R`, first part is major, second part is minor (strip leading digits after `R` up to `_`), rejoin with `.`, prepend `releases/release-`

Determine the repo by checking which repo's working directory you are in.

Determine the TFS project from the repo:
- `c:\GitRepos\ModelCenter` -> project `Documentation`, repository `ModelCenter`
- `c:\GitRepos\documentation` -> project `Documentation`, repository `documentation.git`

Fetch the work item title from ADO (use `/ado item` API) for the PR title and commit message.

#### Step 2 -- Stage and commit

Stage only the doc files that were changed (never stage `tools/`, `global/`, or anything under `.gitignore`):

```powershell
git -C "<repo_path>" add <list of changed doc files>
git -C "<repo_path>" status
```

Verify that only the intended files are staged. If `tools` or `global` appear in the staged list, unstage them:

```powershell
git -C "<repo_path>" reset HEAD tools
git -C "<repo_path>" reset HEAD global
```

Commit with a message that includes `#<id>` to auto-link the work item:

```powershell
git -C "<repo_path>" commit -m "<short description> #<id>"
```

#### Step 3 -- Merge the target branch before pushing

Fetch and merge the latest target branch into the working branch. This prevents merge conflicts in the PR caused by changes others have pushed to the target since the branch was created.

```powershell
git -C "<repo_path>" fetch origin
git -C "<repo_path>" merge origin/<target_release_branch> --no-edit
```

If the merge produces **conflicts**:

1. Identify conflicting files:
   ```powershell
   git -C "<repo_path>" status
   ```
2. For each conflicting file, keep the working branch version (our changes are authoritative):
   ```powershell
   git -C "<repo_path>" checkout --ours "<conflicting_file>"
   git -C "<repo_path>" add "<conflicting_file>"
   ```
3. Complete the merge:
   ```powershell
   git -C "<repo_path>" commit -m "Merge <target_release_branch> into branch before PR #<id>"
   ```

If the merge is clean (no conflicts), no extra commit is needed -- git will fast-forward or create a merge commit automatically with `--no-edit`.

After merging, check whether `tools` or `global` appear in the staged changes:

```powershell
git -C "<repo_path>" diff --cached --name-only
```

**Submodule pointer rule after merge:**

- If the merge **updated** `global`/`tools` to match the target branch's pointer, that is correct -- **leave them staged**. The merge is aligning the branch with the target, which is exactly what we want. Unstaging them would revert to the branch's old (stale) pointer and cause `global`/`tools` to appear as a diff in the PR.
- If `global`/`tools` were **accidentally modified** by local working-tree changes (e.g., you ran commands inside the submodule directory), then unstage them:
  ```powershell
  git -C "<repo_path>" reset HEAD tools
  git -C "<repo_path>" reset HEAD global
  ```

To tell the difference, compare each submodule's staged pointer to the target branch's pointer:

```powershell
git -C "<repo_path>" ls-tree origin/<target_release_branch> -- global tools
git -C "<repo_path>" diff --cached -- global tools
```

If the staged pointer matches the target branch, it came from the merge and is correct. If it differs from the target, it is a local modification and should be unstaged.

#### Step 4 -- Push the branch

```powershell
git -C "<repo_path>" push -u origin HEAD
```

#### Step 5 -- Create the pull request

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$prBody = @{
  title         = '<id> - <work item title>'
  description   = "Documentation update for work item #<id>.`n`nFiles changed:`n- <list of files>"
  sourceRefName = 'refs/heads/LGP/<release>/<id>-short-description'
  targetRefName = 'refs/heads/<target_release_branch>'
  workItemRefs  = @(@{ id = '<id>' })
}
$pr = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/<repo_name>/pullrequests?api-version=6.0" `
        -Method Post -Body $prBody
```

Save `$pr.pullRequestId` and the user's `id` (`$pr.createdBy.id`) for subsequent API calls.

#### Step 6 -- Set auto-complete with delete source branch

Update the PR to enable auto-complete and set completion options:

```powershell
$ac = @{
  autoCompleteSetBy  = @{ id = $pr.createdBy.id }
  completionOptions  = @{
    deleteSourceBranch = $true
    mergeCommitMessage = '<id> - <work item title>'
    mergeStrategy      = 'squash'
  }
}
Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/<repo_name>/pullrequests/$($pr.pullRequestId)?api-version=6.0" `
  -Method Patch -Body $ac
```

#### Step 7 -- Approve the PR (ModelCenter only)

**Only for the ModelCenter repo** (the current user is a required reviewer on MC PRs):

```powershell
Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/ModelCenter/pullrequests/$($pr.pullRequestId)/reviewers/$($pr.createdBy.id)?api-version=6.0" `
  -Method Put -Body @{ vote = 10 }
```

Vote values: `10` = approved, `5` = approved with suggestions, `0` = no vote, `-5` = waiting for author, `-10` = rejected.

**Do NOT vote on PRs in the `documentation` (optiSLang) repo** -- the user is not a required reviewer there.

#### Step 8 -- Present summary

Display a summary table:

| Field | Value |
|-------|-------|
| Commit | `<commit hash>` |
| Branch | `LGP/<release>/<id>-short-description` -> `<target_release_branch>` |
| PR | `#<pullRequestId>` |
| PR URL | `https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_git/ModelCenter/pullrequest/<pullRequestId>` |
| Auto-complete | Enabled (squash merge, delete source branch) |
| Work Item | `#<id>` linked |
| Approval | Approved / Skipped (depending on repo) |

### `/ado doc commitapi` -- Commit, push, and create a GitHub PR for DevRelDocs_API

Run this after `/ado doc <id>` or `/ado doc <id> update` has applied changes in the `c:\GitRepos\DevRelDocs_API` repo. This command commits, pushes, and creates a pull request on GitHub using the `gh` CLI.

**Prerequisites:** You must be on a working branch in `DevRelDocs_API` with changes staged or ready to stage.

**GitHub CLI location:** `"C:\Program Files\GitHub CLI\gh.exe"`

The CLI is authenticated via Windows Credential Manager (keyring). No token environment variable is needed.

#### Step 1 -- Identify context from the current branch

Parse the current branch name to extract:
- `<id>` -- the work item ID (if present)
- `<release>` -- the release label (e.g., `27R1`)
- Whether this is the oSL staging branch (`LGP/27R1/osl-interfaces-customization`) or a per-ticket branch

Fetch the work item title from ADO (use `/ado item` API) for the PR title and commit message, if a ticket ID is present in the branch name.

#### Step 2 -- Stage and commit

Stage only the changed doc files:

```powershell
git -C "C:\GitRepos\DevRelDocs_API" add <changed files or folder>
git -C "C:\GitRepos\DevRelDocs_API" status
```

Commit with a descriptive message. Include `#<id>` if a ticket ID is available:

```powershell
git -C "C:\GitRepos\DevRelDocs_API" commit -m "<short description> #<id>"
```

#### Step 3 -- Push the branch

```powershell
git -C "C:\GitRepos\DevRelDocs_API" push -u origin HEAD
```

#### Step 4 -- Create the pull request on GitHub

Use the `gh` CLI to create the PR targeting `main`, and add `AnsMelanie` as a reviewer (she is the DevRelDocs repo owner):

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" pr create `
  --repo ansys/DevRelDocs `
  --base main `
  --head "<branch_name>" `
  --title "<id> - <work item title>" `
  --body "<PR body with summary and file list>" `
  --reviewer AnsMelanie
```

**PR body format:**

```
## Summary

- <1-3 bullet points describing changes>

## Test plan

- [ ] Verify the doc set renders correctly on the developer portal
- [ ] Confirm TOC navigation works end-to-end
- [ ] Verify all internal cross-links resolve correctly
```

**Important:** If on the oSL staging branch (`LGP/27R1/osl-interfaces-customization`) and the `2027R1/` folder does not yet exist on `main`, do **not** create a PR -- just push and inform the user the change is staged. Only create a PR when Melanie has confirmed the folder structure is ready on `main`.

#### Step 5 -- Present summary

Display a summary table:

| Field | Value |
|-------|-------|
| Commit | `<commit hash>` |
| Branch | `<branch_name>` -> `main` |
| PR | `#<pr_number>` |
| PR URL | `https://github.com/ansys/DevRelDocs/pull/<pr_number>` |
| Reviewer | AnsMelanie |
| Work Item | `#<id>` (if applicable) |

### `/ado doc cherry [pr-id]` -- Cherry-pick a PR forward to all applicable release branches

Cherry-picks a completed PR forward to all subsequent full release branches and `develop`. Run this after `/ado doc commitpr`, or provide a specific PR number.

- `/ado doc cherry` -- cherry-pick the most recently created PR (from the current `commitpr` context) forward
- `/ado doc cherry <pr-id>` -- cherry-pick a specific PR forward by its PR number

#### Forward-pick rules

Branch ordering is determined dynamically from the remote. Full releases are sorted by version number. `develop` is always last (highest).

**SP branches are never targets** -- skip any branch containing `_SP` when building the forward chain.

- **From an SP branch** (e.g., `releases/release-26.1_SP1`): skip the base release (`releases/release-26.1`) since the SP is forward of it. Pick to all full releases after the base, plus `develop`.
- **From a full release** (e.g., `releases/release-25.2`): pick to all subsequent full releases, plus `develop`.

Example with current branches:
- PR merged to `releases/release-26.1_SP1` -> targets: `develop`
- PR merged to `releases/release-25.2` -> targets: `releases/release-26.1`, `develop`

#### Step 1 -- Resolve the source PR

If no `<pr-id>` given, use the PR from the most recent `/ado doc commitpr` in the current conversation.

Fetch the PR details:

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$src = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/<repo_name>/pullrequests/<pr-id>?api-version=6.0"
```

Extract from the response:
- `targetRefName` -- the branch the PR merged into (e.g., `refs/heads/releases/release-26.1_SP1`)
- `repository.id` -- the repo GUID
- `repository.name` -- the repo name (e.g., `ModelCenter` or `documentation.git`)
- `title` -- the original PR title
- `pullRequestId` -- the source PR number

Also extract the work item ID from the PR title, description, or linked work items.

#### Step 2 -- Build the forward target list

Fetch all remote release branches from the repo:

```powershell
$refs = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/<repo_id>/refs?filter=heads/releases/&api-version=6.0"
```

Build the ordered target list:

1. Parse all branch names, extract version numbers (e.g., `releases/release-26.1` -> `26.1`)
2. **Exclude** any branch containing `_SP` (SP branches are never targets)
3. Sort remaining branches by version number (major, then minor)
4. Determine the source branch type:
   - If the PR's `targetRefName` contains `_SP`: it's an SP branch. The base release is the version before the `_SP` suffix (e.g., `26.1_SP1` -> base is `26.1`)
   - Otherwise: it's a full release branch
5. Filter to only branches **after** the base release in the sorted order
6. Append `develop` as the final target

Present the target list to the user before proceeding.

#### Step 3 -- Cherry-pick to each target

For each target branch, call the cherry-pick API:

```powershell
$cpBody = @{
  generatedRefName = "refs/heads/cherry/<pr-id>-to-<target-label>"
  ontoRefName      = "refs/heads/<target-branch>"
  repository       = @{ id = '<repo-id>' }
  source           = @{ pullRequestId = [int]'<pr-id>' }
}
$cp = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/<repo-id>/cherryPicks?api-version=6.0-preview.1" `
        -Method Post -Body $cpBody
```

Where `<target-label>` is a short label like `26R1` or `develop`.

The API is **async**. Poll for completion:

```powershell
$cpStatus = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/<repo-id>/cherryPicks/$($cp.cherryPickId)?api-version=6.0-preview.1"
```

Check the `status` field: `queued`, `inProgress`, `completed`, or `failed`. Poll every 2-3 seconds until terminal state.

If `failed` and `detailedStatus.conflict` is true, record the conflict and **continue** with remaining targets.

#### Step 4 -- Create a PR for each successful cherry-pick

For each completed cherry-pick, create a PR from the generated branch to the target branch:

```powershell
$cherryPrBody = @{
  title         = 'Cherry-pick: <original PR title> -> <target-branch>'
  description   = "Cherry-pick of PR <pr-id> (<pr-url>) to <target-branch>.`n`nWork item: #<work-item-id>"
  sourceRefName = 'refs/heads/cherry/<pr-id>-to-<target-label>'
  targetRefName = 'refs/heads/<target-branch>'
  workItemRefs  = @(@{ id = '<work-item-id>' })
}
$cherryPr = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/Documentation/_apis/git/repositories/<repo_name>/pullrequests?api-version=6.0" `
              -Method Post -Body $cherryPrBody
```

Then for each created PR, apply the same post-creation steps as `/ado doc commitpr`:
- **Set auto-complete** with delete source branch (same as `commitpr` Step 5)
- **Approve** if ModelCenter repo (same as `commitpr` Step 6)

#### Step 5 -- Present summary

Display a table of all cherry-pick results:

| Target Branch | Cherry-pick | PR | PR URL | Auto-complete | Approval |
|---|---|---|---|---|---|
| `releases/release-26.1` | Completed | #12345 | URL | Enabled | Approved |
| `develop` | Conflict | -- | -- | -- | Manual resolution needed |

If any cherry-picks had conflicts, note which target branches need manual resolution.

### Release deliverables (RIL, KIL, Release Notes)

All release documentation commands have been moved to the dedicated **ado-release-docs** skill at `C:\Users\ldove\.cursor\skills\ado-release-docs\SKILL.md`. Read that skill for:

- `/ado doc RIL <id>` -- generate Resolved Issues List draft
- `/ado doc RIL` -- insert approved RIL into DocBook XML
- `/ado doc KIL <id>` -- generate Known Issues List draft
- `/ado doc KIL` -- insert approved KIL into DocBook XML
- `/ado doc ReleaseNotes <id>` -- generate Release Notes draft
- `/ado doc ReleaseNotes` -- insert approved Release Notes into documentation
