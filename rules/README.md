# Cursor Rules

**Cursor rules** are `.mdc` files (Markdown with YAML front matter) that give the agent persistent guidance — globally (`alwaysApply: true`) or when specific files or globs match. They live in `%USERPROFILE%\.cursor\rules\` on Windows, or `~/.cursor/rules/` on macOS/Linux. Workspace-scoped rules go in that project's `.cursor/rules/`.

Skills teach the agent *how to run a workflow*; rules teach it *how to behave* on every turn.

Companion analysis for token efficiency: [`docs/token-efficiency/`](../docs/token-efficiency/) — start with the [Token Action Card PDF](../docs/token-efficiency/token-action-card.pdf).

---

## What's in this folder

| Rule | Purpose | Pairs with |
|------|---------|------------|
| [`token-budget.mdc`](token-budget.mdc) | Ambient token discipline — thread-close nudges, model routing, no whole-file reads | [`token-workflow`](../packages/token-workflow), [`token-check`](../packages/token-check) |
| [`edit-discipline.mdc`](edit-discipline.mdc) | Think → minimum → surgical → verify for any authored content | [`ansys-doc-guidelines`](../packages/ansys-doc-guidelines), [`api-documentation`](../packages/api-documentation), [`ado-doc-workflow`](../packages/ado-doc-workflow) |
| [`no-policy-override.mdc`](no-policy-override.mdc) | Never bypass or suggest bypassing PR/branch policies | [`ado-doc-workflow`](../packages/ado-doc-workflow) |
| [`no-ticket-tags.mdc`](no-ticket-tags.mdc) | Omit `System.Tags` on ADO create/edit unless user asks (optional — delete if your team uses tags) | [`ado-doc-workflow`](../packages/ado-doc-workflow) |

All rules ship with `alwaysApply: false` in the front matter. Set `alwaysApply: true` on the ones you want ambient on every chat.

The `ado-doc-workflow` package also bundles a **package-local** `no-credentials-on-cmdline.mdc` under `packages/ado-doc-workflow/rules/` — install that from the zip if you use `Ado-Auth.ps1`; it is not duplicated here because credential-handling setup varies by team.

---

## Installing rules

**Easiest:** drag any `.mdc` file into a Cursor chat and say **"Add this as a global rule."** Cursor copies it to your user rules folder.

**Manual:**

```powershell
Copy-Item "C:\path\to\cursor-doc-skills\rules\*.mdc" `
          "$env:USERPROFILE\.cursor\rules\"
```

Open each file and set `alwaysApply: true` when you want ambient coaching. Leave `false` if you only want the rule when you `@`-mention it or when a skill points at it.

### Suggested bundles

| If you install… | Also install these rules |
|-----------------|--------------------------|
| **Token efficiency** (`token-workflow`, `token-check`) | `token-budget.mdc` (`alwaysApply: true`) |
| **Doc style** (`ansys-doc-guidelines`, `api-documentation`) | `edit-discipline.mdc` |
| **ADO doc workflow** (`ado-doc-workflow`) | `edit-discipline.mdc`, `no-policy-override.mdc`; optionally `no-ticket-tags.mdc` |

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team. Same sharing posture as the rest of [cursor-doc-skills](../README.md).
