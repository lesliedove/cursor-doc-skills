---
name: ado-release-docs
description: >-
  Generate and insert Resolved Issues Lists (RIL), Known Issues Lists (KIL),
  and Release Notes for Ansys ModelCenter and optiSLang releases. Used at the
  end of a release cycle or for service packs. Use when the user says "draft
  the RIL", "draft known issues", "draft release notes", "insert the RIL/KIL",
  or runs any /ado doc RIL, /ado doc KIL, or /ado doc ReleaseNotes command.
---

# ADO Release Documentation

Commands for generating and inserting release deliverables: Resolved Issues Lists (RIL), Known Issues Lists (KIL), and Release Notes. These are typically run together at the end of a release cycle or service pack.

**Workflow:** For each deliverable type, there are two commands:
1. `<type> <id>` -- generates a **markdown draft** from a parent ADO ticket for human review
2. `<type>` (no ID) -- inserts the **approved** content into the DocBook XML documentation

After inserting, use `/ado doc commitpr` (from the [ado-doc skill](../ado-doc/SKILL.md)) to commit and create a PR.

## Credentials

Load credentials and use the shared NTLM helper (same as the [ADO skill](../ado/SKILL.md)):

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$wi = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?api-version=6.0"
```

`Invoke-AdoRest` wraps `Invoke-RestMethod -Credential` with `~/.env` pre-loaded. Auth is NTLM in-process; no `curl.exe` is spawned.

### IMPORTANT — Never use `curl.exe -u "$env:..."` for auth'd calls

PowerShell expands credential variables BEFORE `CreateProcess`, so the literal password lands in `curl.exe`'s argv where Win32 process auditing (Event 4688), WMI `Win32_Process.CommandLine`, Defender for Endpoint, and any EDR can read it. Synopsys security has flagged this exact mistake. The hook `gate-credential-leak.ps1` will block it. Use `Invoke-AdoRest` instead.

## PowerShell Execution Guidelines

**CRITICAL:** The Shell tool on Windows wraps commands in a temporary `.ps1` script. PowerShell variables like `$matches`, `$_`, `$since`, and string interpolation with `$()` are unreliable when passed as inline `-Command` strings because the outer shell may strip or mangle them.

**Rule:** For any PowerShell logic that uses `$matches`, `$_`, `ForEach-Object`, `Where-Object`, regex matching, or complex string interpolation:

1. Write the script to a temp `.ps1` file using the Write tool
2. Execute it with `powershell -ExecutionPolicy Bypass -File "<path>"`
3. Delete the temp file afterward

## Branch setup for insert commands

The insert commands (`RIL`, `KIL`, `ReleaseNotes` without an ID) need a branch and eventually a PR. Follow the same branch setup as `/ado doc` Steps 4-6 in the [ado-doc skill](../ado-doc/SKILL.md):
- Determine the release branch
- Pull the branch (with submodule handling for `global/`)
- Create a working branch using the task ID

## Review contacts

- **oSL drafts** (RIL, KIL, Release Notes): Send to David Schneider for review.
- **MC drafts**: Send to Mike Belcher for review.

## Commands

### `/ado doc RIL <id>` -- Generate a Resolved Issues List draft from a parent ticket

Fetch a parent/umbrella work item (e.g., a Service Pack or Release tracking ticket), read all its children, and produce a markdown file listing every resolved (fixed) issue.

**Scope:** This command generates a **markdown draft** for human review. It does NOT touch the XML docs yet -- that happens with `/ado doc RIL` (without an ID).

#### Step 1 -- Fetch the parent work item and its children

Fetch the parent ticket with relations expanded:

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$parent = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/<ID>?`$expand=all&api-version=6.0"
```

Extract IDs from two relation types:
- **Children:** `rel = "System.LinkTypes.Hierarchy-Forward"`
- **Related:** `rel = "System.LinkTypes.Related"`

Parse the URL in each relation's `url` field to get the work item ID. Combine both sets (deduplicate if any overlap).

#### Step 2 -- Batch-fetch all children and related items

Fetch details for all collected IDs (batch in groups of 200):

```powershell
$idList = ($childIds | Select-Object -First 200) -join ','
$details = Invoke-AdoRest -Uri "https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems?ids=$idList&`$expand=all&api-version=6.0"
```

For each child, extract:
- `System.Id`
- `System.Title`
- `System.State`
- `System.WorkItemType`
- `System.Description` (strip HTML tags)
- `Microsoft.VSTS.Common.ResolvedReason` or `System.Reason`
- `System.AreaPath` (to determine if it's optiSLang or ModelCenter)

#### Step 3 -- Filter for resolved/fixed issues

Include an item in the RIL if:
- `System.State` is `Resolved`, `Closed`, or `Done`
- AND `ResolvedReason` is `Problem corrected` or `Already corrected by other work` (exclude `Not a Bug`, `Duplicate`, `Won't Fix`, `By Design`)
- AND the item represents a bug fix or resolved issue (type is `Bug`, `Issue`, `Defect`, or similar -- NOT `Feature`, `User Story`, or `Task` unless the title/description clearly describes a fix)
- AND the fix is **user-facing** -- exclude internal security vulnerability patches, build/packaging fixes, dependency version bumps, and test-only changes unless they directly affect user-visible behavior

**Determining product:** Check `System.AreaPath` for `optiSLang` or `ModelCenter` to group items by product.

#### Step 4 -- Write a short description for each issue

For each qualifying child ticket, write **one bullet point** with:
1. A concise description of **what the issue was** and/or **what was fixed**. Use the title and description from the ticket. Keep it to 1-2 sentences. Write in past tense ("Resolved an issue where...") or present tense describing the fix ("Starting Design Points are now checked properly...").
2. The ticket number in parentheses at the end: `(1262381)`

**Do NOT** follow links to grandchild tickets -- only use the information directly on each child/related ticket. If the ticket has very little detail, write the best summary you can from the title alone.

#### Step 5 -- Generate the markdown file

Create a markdown file at `%USERPROFILE%\Downloads\<product>_RIL_<release>.md` with this naming convention:
- `<product>` = `oSL` for optiSLang, `MC` for ModelCenter
- `<release>` = release version like `2026R1_SP1`, `2027R1`, `2026R2`, etc.
- Example: `oSL_RIL_2026R1_SP1.md`, `MC_RIL_2027R1.md`

Structure:

```markdown
# Resolved Issues -- [Product Name] [Release Version]

- Description of resolved issue one. (1234567)

- Description of resolved issue two. (1234568)

Some issues were resolved in earlier service packs. These are highlighted here for visibility:

- Description of issue resolved in earlier SP. (1234569)
```

**Formatting rules:**
- Each bullet is a `- ` (dash space) at the start of the line
- Ticket number in parentheses at the very end of the bullet, after a space
- One blank line between bullets for readability
- If there are items from earlier SPs (identified by iteration path or tags referencing earlier SPs), group them under the "earlier service packs" subheading
- If an issue is "resolved" because the affected product/feature was replaced entirely (e.g., OWS replaced by SAF), still include it in the RIL and note the replacement in the description
- If there are no resolved issues, write: `See the Ansys 20YY RX Release Notes for descriptions of product enhancements.` (where `20YY` is the release year and `RX` is the release number, e.g., `See the Ansys 2026 R1 Release Notes for descriptions of product enhancements.`)

Present a summary table showing how many children were found, how many qualified as resolved issues, and the output file path.

### `/ado doc RIL` -- Insert approved Resolved Issues List into the documentation

After the user has reviewed and approved the RIL markdown draft (possibly editing it), they will provide the final markdown content. This command converts it to DocBook XML and inserts it into the appropriate file.

**Prerequisites:** The user provides the approved markdown content (either by pasting it or pointing to the edited file).

#### Step 1 -- Determine the target

Ask the user (or infer from context):
- **Product:** optiSLang or ModelCenter
- **Release branch:** which release/SP this is for

#### Step 1b -- Find the work item for branch naming and PR linking

These insert commands do not receive a ticket ID directly. Instead, find the appropriate task ticket by querying ADO:

1. Query for Feature tickets assigned to the current user (`@Me`) that match the target release (by iteration path or title):
   ```powershell
   . "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
   $wiql = @{
     query = "SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.WorkItemType] = 'Feature' AND [System.State] <> 'Closed' AND [System.State] <> 'Removed' ORDER BY [System.ChangedDate] DESC"
   }
   $features = Invoke-AdoRest -Uri 'https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/wiql?api-version=6.0' `
                 -Method Post -Body $wiql
   ```
2. Fetch each Feature's children (hierarchy-forward relations). Look for a **User Story** (or similar) with a title like "Release Tasks".
3. Under that User Story, look for a **Task** whose title references the target product (oSL/optiSLang or MC/ModelCenter) and the type of deliverable (RIL, KIL, Release Notes, or a general "release docs" task).
4. Use that Task's ID for the branch name (`LGP/<release>/<task-id>-ril` or similar) and link it as the work item on the PR.
5. If no matching task is found, present the candidate Feature tickets and their children to the user and ask which to use.

#### Step 2 -- Set up the branch

See "Branch setup for insert commands" above.

#### Step 3 -- Convert markdown to DocBook XML

Convert each markdown bullet to a `<listitem><para>` entry. The full block replaces the content inside the appropriate `<sect1>` in `docu_end/ai_ril/ai_ril.xml`.

**For optiSLang** -- target `<sect1 id="riloptiSLang">`:

Replace the existing content of the sect1 with:

```xml
    <sect1 id="riloptiSLang">
      <title>&pn257g;</title>
      <para>See the &ansysCompany; &ansys_external_version; Release Notes for descriptions of
        product enhancements.</para>
      <itemizedlist>
        <listitem>
          <para>Description of resolved issue one. (1234567)</para>
        </listitem>
        <listitem>
          <para>Description of resolved issue two. (1234568)</para>
        </listitem>
      </itemizedlist>
    </sect1>
```

If the markdown has an "earlier service packs" section, add a `<para>` before that group:

```xml
      <para>Some issues were resolved in earlier service packs. These are highlighted here for
        visibility:</para>
      <itemizedlist>
        <listitem>
          <para>Earlier SP issue description. (1234569)</para>
        </listitem>
      </itemizedlist>
```

**For ModelCenter** -- target `<sect1 id="rilModelCenter">` (or the appropriate MC sect1 in the same file).

#### Step 4 -- Present summary

Show the list of entries added and the file modified. Inform the user they can run `/ado doc commitpr` to commit and create a PR.

### `/ado doc KIL <id>` -- Generate a Known Issues List draft from a parent ticket

Fetch a parent/umbrella work item, read all its children, and produce a markdown file listing every **unresolved known issue**.

**Scope:** Generates a **markdown draft** for human review. Does NOT touch XML docs -- that happens with `/ado doc KIL` (without an ID).

#### Step 1 -- Fetch the parent work item and its children

Same as `/ado doc RIL <id>` Step 1 -- fetch the parent with `$expand=all` and extract both child IDs (hierarchy-forward) and related IDs.

#### Step 2 -- Batch-fetch all children

Same as `/ado doc RIL <id>` Step 2.

#### Step 3 -- Filter for known (unfixed) issues

Include a child in the KIL if:
- `System.State` is `Active`, `New`, `Proposed`, or any state that is NOT `Resolved`/`Closed`/`Done`/`Removed`
- AND the item represents a bug, issue, or known limitation (not a feature request or enhancement)

Also include items that are `Resolved` or `Closed` but with a resolution of `Won't Fix`, `By Design`, `Deferred`, or similar -- these are known issues that were deliberately not fixed.

**Determining product:** Same as RIL -- check `System.AreaPath`.

#### Step 4 -- Write a description for each issue

For each qualifying child ticket, write:
1. A concise description of **the issue** and **how a user would encounter it**. 1-2 sentences. Write from the user's perspective.
2. The ticket number in parentheses: `(1394027)`
3. If a workaround is mentioned in the ticket description, acceptance criteria, or comments, add it on a new line starting with `Workaround:`. If the workaround has multiple steps, use a sub-list.

**Do NOT** follow links to grandchild tickets or related items.

#### Step 5 -- Generate the markdown file

Create a markdown file at `%USERPROFILE%\Downloads\<product>_KIL_<release>.md` with the same naming convention as RIL (e.g., `oSL_KIL_2026R1_SP1.md`).

Structure:

```markdown
# Known Issues -- [Product Name] [Release Version]

- Description of known issue one. (1394027)

  Workaround: Description of the workaround.

- Description of known issue two. (1275716)

  Workaround: Disable "Return licenses after workflow termination".

- Description of known issue three with no workaround. (1364955)
```

**Formatting rules:**
- Each bullet is a `- ` (dash space) at the start of the line
- Ticket number in parentheses after the issue description (before the workaround)
- Workaround on a new line, indented with two spaces to keep it under the bullet, starting with `Workaround:`
- If there are sub-steps in the workaround, use an indented sub-list (four spaces + `- `)
- One blank line between bullets for readability
- If there are no known issues, write: `No known issues, limitations, or documentation inaccuracies.`

Present a summary table showing how many children were found, how many qualified as known issues, and the output file path.

### `/ado doc KIL` -- Insert approved Known Issues List into the documentation

After the user has reviewed and approved the KIL markdown draft, this command converts it to DocBook XML and inserts it into the appropriate file.

**Prerequisites:** The user provides the approved markdown content.

#### Step 1 -- Determine the target

Same as `/ado doc RIL` -- ask/infer product and release branch.

#### Step 1b -- Find the work item for branch naming and PR linking

Same as `/ado doc RIL` Step 1b -- find the appropriate Task ticket under the user's release Feature -> "Release Tasks" User Story hierarchy. Use that Task ID for the branch name and PR work item link.

#### Step 2 -- Set up the branch

See "Branch setup for insert commands" above.

#### Step 3 -- Convert markdown to DocBook XML

Convert each markdown bullet to DocBook entries. The full block replaces the content inside the appropriate `<sect1>` in `docu_end/ai_lmt/ai_lmt.xml`.

**For optiSLang** -- target `<sect1 id="KIL160optiSLang">`:

```xml
    <sect1 id="KIL160optiSLang">
      <title>&pn257g;</title>
      <itemizedlist>
        <listitem>
          <para>Description of known issue one. (1394027)</para>
          <para><emphasis role="bold">Workaround:</emphasis> Description of the workaround.</para>
        </listitem>
        <listitem>
          <para>Description of known issue two. (1275716)</para>
          <para><emphasis role="bold">Workaround:</emphasis> Disable "Return licenses after workflow
            termination".</para>
        </listitem>
      </itemizedlist>
    </sect1>
```

**Workaround formatting in DocBook:**
- Simple workaround: `<para><emphasis role="bold">Workaround:</emphasis> Text here.</para>`
- Multi-step workaround: Use a nested `<itemizedlist>` inside the `<listitem>`, after the workaround `<para>` label
- If no workaround exists for an item, omit the workaround `<para>` entirely

**For ModelCenter** -- target `<sect1 id="KILModelCenter">` in the same file.

#### Step 4 -- Present summary

Show the list of entries added and the file modified. Inform the user they can run `/ado doc commitpr` to commit and create a PR.

### `/ado doc ReleaseNotes <id>` -- Generate a Release Notes draft from a parent ticket

Fetch a parent/umbrella work item, read all its children, and produce a markdown file listing **new features and enhancements** with expanded detail.

**Scope:** Generates a **markdown draft** for human review. Does NOT touch XML docs -- that happens with `/ado doc ReleaseNotes` (without an ID).

Release notes are **more detailed** than RIL/KIL entries. They describe what was added/changed, why it matters, and may include sub-bullets for specific capabilities.

#### Step 1 -- Fetch the parent work item and its children

Same as `/ado doc RIL <id>` Step 1.

#### Step 2 -- Batch-fetch all children

Same as `/ado doc RIL <id>` Step 2.

#### Step 3 -- Filter for features, enhancements, and notable fixes

Include a child in the Release Notes if:
- It represents a new feature, enhancement, or significant improvement (type is `Feature`, `User Story`, `Product Backlog Item`, `Task` with a feature-like title, or `Bug` with a notable user-facing fix)
- It has been `Resolved`, `Closed`, or `Done` (i.e., the work is complete)

**Exclude** purely internal/infrastructure items (build fixes, test updates, etc.) unless they have user-facing impact.

**Determining product:** Check `System.AreaPath` for `optiSLang` or `ModelCenter`.

#### Step 4 -- Write a description for each item

For each qualifying child ticket, write:
1. A **heading line** (the feature/enhancement name) -- use `###` markdown heading
2. A paragraph describing the feature/change in user-facing terms. Be more detailed than RIL -- explain what the feature does and how users benefit. Use the ticket title, description, and acceptance criteria.
3. If the ticket description lists specific sub-features or capabilities, include them as sub-bullets
4. The ticket number in parentheses: `(1177781)`

**Grouping:** If tickets naturally fall into categories (e.g., General, User Interface, Connectors, Algorithms -- as in the PDF example), group them under `## Category` headings.

**Do NOT** follow links to grandchild tickets or related items.

#### Step 5 -- Generate the markdown file

Create a markdown file at `%USERPROFILE%\Downloads\<product>_RN_<release>.md` with the same naming convention as RIL (e.g., `oSL_RN_2027R1.md`).

Structure:

```markdown
# Release Notes -- [Product Name] [Release Version]

## General

### Feature Name One

Description of the feature, what it does, and how users benefit. (1177781)

- Sub-capability one
- Sub-capability two

### Feature Name Two

Description of another feature. (1180361)

## User Interface

### UI Enhancement

Description of UI change. (1177783)

## Connectors

### New Connector Name

Description of the new connector. (1234567)

- Supports X
- Added Y
- Improved Z
```

**Formatting rules:**
- `## Category` headings for major groupings
- `### Feature Name` for each individual feature/enhancement
- Ticket number in parentheses after the description paragraph
- Sub-bullets with `- ` for specific capabilities or sub-features
- One blank line between sections for readability
- If there are no features/enhancements, write: `No new features for this release.`

Present a summary table showing how many children were found, how many qualified as release notes entries, and the output file path.

### `/ado doc ReleaseNotes` -- Insert approved Release Notes into the documentation

After the user has reviewed and approved the Release Notes markdown draft, this command converts it to DocBook XML / DITA and inserts it into the appropriate files. There are **three** places to update per product.

**Prerequisites:** The user provides the approved markdown content.

#### Step 1 -- Determine the target

Ask the user (or infer from context):
- **Product:** optiSLang or ModelCenter
- **Release branch:** which release/SP this is for

#### Step 1b -- Find the work item for branch naming and PR linking

Same as `/ado doc RIL` Step 1b -- find the appropriate Task ticket under the user's release Feature -> "Release Tasks" User Story hierarchy. Use that Task ID for the branch name and PR work item link.

**Target files by product (all three must be updated):**

| # | optiSLang (documentation repo) | ModelCenter (ModelCenter repo) |
|---|---|---|
| 1 | `docu_corp/ai_rn/opti_releasenotes/opti_releasenotes_chp.xml` | `docu_corp/ai_rn/mc_releasenotes/` chapter file |
| 2 | `docu_optislang/opti_new/opti_new_current.xml` | `docu_dita/ModelCenter_RN/new_features.dita` |
| 3 | `docu_optislang/opti_new/opti_new_archive.xml` (migrate old current) | `docu_dita/ModelCenter_RN/archives/<new_file>.dita` + ditamap (migrate old current) |

#### Step 2 -- Set up the branch

See "Branch setup for insert commands" above.

#### Step 3 -- Migrate the existing "current" release notes to archive

Before inserting new content, the **existing** release notes in the "current" slot must be archived.

**For optiSLang:**

1. Read `docu_optislang/opti_new/opti_new_current.xml` -- copy its content (all `<section>` blocks inside the `<chapter>`).
2. Open `docu_optislang/opti_new/opti_new_archive.xml` -- find the `<section id="opti_ug_changelog_vh">` (the main changelog section).
3. Insert a new `<section>` as the **first child** of that section (before the existing archive entries, so newest archive is first). Use the release version as the title (e.g., `<section><title>2026 R1 SP1</title>`).
4. Paste the content from the old current into this new archive section.
5. **Strip images:** Remove all `<informalfigure>`, `<figure>`, `<mediaobject>`, `<imageobject>`, and `<imagedata>` elements and their contents.
6. **Strip cross-references:** Remove `<olink>` elements (replace with just the link text content) and `<link>` elements (replace with just the link text content). Leave the text readable but unlinked.
7. Clear `opti_new_current.xml` back to an empty chapter shell (keep the XML prolog, DOCTYPE, entity declarations, and `<chapter>` wrapper with title -- just remove all `<section>` content).

**For ModelCenter:**

1. Read `docu_dita/ModelCenter_RN/new_features.dita` -- copy its content (all `<section>` blocks inside `<conbody>`).
2. Determine the archive filename from the existing content. Use the convention: `<YYYY>_<RN>_<MM>_<DD>_<YYYY>.dita` where `YYYY` is the release year, `RN` is the release (e.g., `R1`, `r2`), and `MM_DD_YYYY` is the release date. Look at existing archive filenames for the pattern (e.g., `2025_r2_07_16_2025.dita`, `2025_R1_01_14_2025.dita`). If the exact release date is unknown, use the current date or ask the user.
3. Create a new file at `docu_dita/ModelCenter_RN/archives/<filename>.dita` with:
   - Standard ANSYS DITA doctype
   - `<concept id="_<yyyy>_<rn>_release_notes_<month>_<yyyy>">` (follow the existing ID convention)
   - `<title>YYYY RN Release Notes - Month DD, YYYY</title>`
   - `<conbody>` containing the migrated sections
4. **Strip images:** Remove all `<image>`, `<fig>`, `<figure>` elements. (Note: MC release notes rarely contain images, but check.)
5. **Strip links:** Remove `<xref>` elements that use `scope="peer"` or reference other books/topics within the help (replace with just the link text). Keep `scope="external"` xrefs to third-party documentation as-is.
6. Add the new archive file to `BM_ModelCenter_RN.ditamap` -- insert a `<topicref>` as the **first child** under the `<chapter href="ModelCenter_RN/archives.dita">` element (newest archive first).
7. Clear `new_features.dita` back to an empty concept shell (keep the XML prolog, DOCTYPE, `<concept>`, `<title>`, and `<conbody>` -- just remove all `<section>` content).

#### Step 4 -- Insert new release notes into the "current" slot

**For optiSLang -- `opti_new_current.xml`:**

Replace the empty chapter content with new `<section>` blocks converted from the approved markdown:

- `## Category` -> `<section><title>Category</title>`
- `### Feature Name` -> `<bridgehead>Feature Name</bridgehead>`
- Description paragraph -> `<para>Description text. (1177781)</para>`
- Sub-bullets -> `<itemizedlist><listitem><para>Sub-item</para></listitem></itemizedlist>`
- Images referenced in the markdown -> `<informalfigure><mediaobject><imageobject><imagedata fileref="Graphics/<filename>"/></imageobject></mediaobject></informalfigure>`
- Cross-references to other optiSLang guide topics -> `<olink targetptr="<section_id>">Link Text</olink>`

**For ModelCenter -- `new_features.dita`:**

Replace the empty conbody content with new `<section>` blocks converted from the approved markdown:

- `## Category` -> `<section id="<category_id>"><title>Category</title>`
- Feature bullets -> `<ul><li><p>Feature description. (1177781)</p></li></ul>`
- Use `<bridgehead>` for sub-groupings like "Features Updated", "Issues Addressed" where applicable

#### Step 5 -- Insert into the corporate release notes file

**For optiSLang -- `docu_corp/ai_rn/opti_releasenotes/opti_releasenotes_chp.xml`:**

Insert new `<section>` blocks. New sections go **before** existing sections (newest release content first).

```xml
    <section id="opti_relnotes_26r1sp1_general">
        <title>General</title>
        <bridgehead>Feature Name One</bridgehead>
        <para>Description of the feature, what it does, and how users benefit. (1177781)</para>
        <itemizedlist>
            <listitem>
                <para>Sub-capability one</para>
            </listitem>
            <listitem>
                <para>Sub-capability two</para>
            </listitem>
        </itemizedlist>
        <bridgehead>Feature Name Two</bridgehead>
        <para>Description of another feature. (1180361)</para>
    </section>
```

**Section ID convention:** `opti_relnotes_<release>_<category>` where `<release>` is like `26r1sp1`, `27r1`, etc. and `<category>` is lowercase with underscores (e.g., `general`, `user_interface`, `connectors`, `algorithms`).

**For ModelCenter** -- follow the same pattern but with `mc_relnotes_` prefix in section IDs.

**Important:** Do NOT remove or modify existing release notes sections in the corporate file -- only add new ones for the current release.

#### Step 6 -- Present summary

Show all files modified/created across all three targets, and inform the user they can run `/ado doc commitpr` to commit and create a PR.
