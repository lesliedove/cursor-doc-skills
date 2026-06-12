# Cursor Rules

**Cursor rules** are `.mdc` files (Markdown with YAML front matter) that give the agent persistent guidance — globally (`alwaysApply: true`) or when specific files or globs match. They live in `%USERPROFILE%\.cursor\rules\` on Windows, or `~/.cursor/rules/` on macOS/Linux. Workspace-scoped rules go in that project's `.cursor/rules/`.

Skills teach the agent *how to run a workflow*; rules teach it *how to behave* on every turn. The token-efficiency habit stack uses both: [`token-workflow`](../packages/token-workflow) and [`token-check`](../packages/token-check) skills plus the always-on rule below.

Companion analysis docs: [`docs/token-efficiency/`](../docs/token-efficiency/) — start with the [Token Action Card PDF](../docs/token-efficiency/token-action-card.pdf).

---

## What's in this folder

| Rule | Purpose | Install |
|------|---------|---------|
| [`token-budget.mdc`](token-budget.mdc) | Ambient token discipline — thread-close nudges, model routing, no whole-file reads, sub-agent defaults | Copy to `%USERPROFILE%\.cursor\rules\token-budget.mdc` and set `alwaysApply: true` |

---

## Installing a rule

**Easiest:** drag `token-budget.mdc` into a Cursor chat and say **"Add this as a global rule."** Cursor copies it to your user rules folder.

**Manual:**

```powershell
Copy-Item "C:\path\to\cursor-doc-skills\rules\token-budget.mdc" `
          "$env:USERPROFILE\.cursor\rules\token-budget.mdc"
notepad "$env:USERPROFILE\.cursor\rules\token-budget.mdc"
```

Open the file and set `alwaysApply: true` in the YAML front matter when you want ambient coaching on every chat. Leave it `false` if you only want the rule when you `@`-mention it or when another skill points at it.

---

## Works well with

| Artifact | Role |
|----------|------|
| [`docs/token-efficiency/`](../docs/token-efficiency/) | Action Card + companion — the *why* behind the habits |
| [`token-workflow`](../packages/token-workflow) | Split multi-phase tickets into short threads |
| [`token-check`](../packages/token-check) | Weekly measurement that habits are working |

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team. Same sharing posture as the rest of [cursor-doc-skills](../README.md).
