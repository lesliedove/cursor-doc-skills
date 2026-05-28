# Ansys API Documentation Guidelines — Cursor Skill

This skill gives your Cursor AI agent the full Ansys API documentation guidelines so it can help you create, review, and migrate documentation for the Dev portal.

## What's included

| File | Purpose |
|------|---------|
| `SKILL.md` | Core rules — package classification, style, metadata, compliance, PR process |
| `api-guidelines-reference.md` | Deep-dive reference — writing guidelines for REST/gRPC/Library/SDK, detailed metadata, full compliance checklist |
| `migration-reference.md` | Migration workflows — the 5-step process, package requirements, and format conversion instructions (DITA, DocBook, Doxygen, Sphinx, Jupyter, C#, proto, Word/PDF) |

## Install

### Step 1: Copy the skill folder

Copy the entire `api-documentation` folder (the one containing this README) to your Cursor skills directory:

**Windows:**

```
C:\Users\<your-username>\.cursor\skills\api-documentation\
```

**macOS / Linux:**

```
~/.cursor/skills/api-documentation/
```

You can do this from the command line:

**Windows (PowerShell):**

```powershell
Copy-Item -Path ".\api-documentation" -Destination "$env:USERPROFILE\.cursor\skills\api-documentation" -Recurse
```

**macOS / Linux:**

```bash
cp -r ./api-documentation ~/.cursor/skills/api-documentation
```

### Step 2: Verify

1. Open Cursor (or restart it if it was already open).
2. Start a new Agent chat.
3. The skill should appear in the agent's available skills list as **api-documentation**.

You can test it by asking the agent something like:

> "What files are required for a REST API documentation package on the Dev portal?"

The agent should reference the skill and answer using the Ansys-specific guidelines.

## Updating

To update the skill, replace the files in your `~/.cursor/skills/api-documentation/` folder with the latest versions. No other configuration is needed.

## Uninstall

Delete the `api-documentation` folder from `~/.cursor/skills/`.

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team.

Part of the **[`cursor-doc-skills`](https://github.com/lesliedove/cursor-doc-skills)** catalog. Issues, suggestions, or migration-workflow updates — open an issue on the repo or ping Leslie on Teams.
