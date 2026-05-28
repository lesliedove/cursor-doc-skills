# Ansys Documentation Guidelines — Cursor Skill

A Cursor AI skill that gives your agent comprehensive knowledge of Ansys corporate documentation standards for DITA and DocBook content.

## What's included

| File | Purpose |
|------|---------|
| `SKILL.md` | Entry point — concise, LLM-optimized rules for writing style, terminology, XML formatting, and document structure |
| `writing-style-reference.md` | Deep reference — complete terminology table, detailed punctuation rules, indexing guidelines, equation/unit formatting |
| `xml-structure-reference.md` | Deep reference — DocBook and DITA element reference, tagging rules, document structure, tag comparison table |

## Install

### Option A: Personal install (all your Cursor workspaces)

**Windows (PowerShell):**

```powershell
Copy-Item -Path ".\ansys-doc-guidelines" -Destination "$env:USERPROFILE\.cursor\skills\ansys-doc-guidelines" -Recurse
```

**macOS / Linux:**

```bash
cp -r ./ansys-doc-guidelines ~/.cursor/skills/ansys-doc-guidelines
```

### Option B: Repository-level install (shared with your team)

Copy the `ansys-doc-guidelines` folder into your documentation repo:

```
your-repo/.cursor/skills/ansys-doc-guidelines/
```

Everyone who clones the repo gets the skill automatically.

## Verify installation

1. Open a Cursor chat (Ctrl+L or Cmd+L).
2. The skill should appear in the agent's available skills list as **ansys-doc-guidelines**.
3. Ask the agent: "What are the Ansys rules for writing a cross-reference?" — it should reference the guidelines.

## When the agent uses this skill

The agent activates this skill when working on:

- DITA topics (`.dita`, `.ditamap`)
- DocBook XML files (`.xml`)
- Any Ansys product documentation
- Writing style, terminology, or formatting questions
- Document structure or XML tagging tasks

## Update

Re-run the install command. The copy overwrites the existing files.

## Uninstall

**Windows:**

```powershell
Remove-Item -Path "$env:USERPROFILE\.cursor\skills\ansys-doc-guidelines" -Recurse -Force
```

**macOS / Linux:**

```bash
rm -rf ~/.cursor/skills/ansys-doc-guidelines
```

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team.

Part of the **[`cursor-doc-skills`](https://github.com/lesliedove/cursor-doc-skills)** catalog. Issues, suggestions, or terminology updates — open an issue on the repo or ping Leslie on Teams.
