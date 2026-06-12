# Token Workflow Skill — Shared Edition

Plan multi-phase ticket work into **short Cursor threads** with durable handoffs on disk (`workflow.md` + `worklog.md` in your scratch folder). Proven pattern for parser/code fixes and non-trivial doc work where one mega-thread would burn cache-read tokens.

Part of the **[cursor-doc-skills](https://github.com/lesliedove/cursor-doc-skills)** catalog.

---

## What it does

| Phase | Where it runs | Output |
|-------|---------------|--------|
| **Planning** | One chat (any model) | `workflow.md` with per-thread bootstrap prompts + token traps |
| **Execution** | One chat **per phase** (`composer-2.5` default) | Phase done-when met; `worklog.md` updated |
| **Between phases** | `/diary`, close tab | Handoff on disk — next thread reads scratch only |

Default phase pattern for code bugs: **TDD → fix → ship** (3 threads).

---

## Install

Drag the unzipped folder (or `token-workflow.zip` from `dist/`) into a Cursor chat and say **"Add this as a global skill."**

You should end up with:

```
%USERPROFILE%\.cursor\skills\token-workflow\
  SKILL.md
  README.md
  workflow-template.md
  example-workflow.md
```

### Optional: ambient token nudges

Install [`rules/token-budget.mdc`](../../rules/token-budget.mdc) from the repo root (`%USERPROFILE%\.cursor\rules\`, `alwaysApply: true`). It reminds the agent to suggest `/diary` + close tab at task wrap, avoid whole-file reads, and route routine work to cheaper models. See [`rules/README.md`](../../rules/README.md).

### Scratch folder convention

The skill assumes ticket scratch lives at `C:\GitRepos\.scratch\<ticket-id>-<slug>\` with a required `worklog.md`. If your team uses a different path, update the paths in `SKILL.md` or add a workspace rule that defines your scratch location.

---

## Usage

```
/token-workflow 12345
```

The planning chat will fetch the ticket, map the repo, write `workflow.md` + `worklog.md`, and print the Thread 1 bootstrap prompt.

**Then close the planning tab.** Open a fresh `composer-2.5` thread and paste that prompt.

Between every phase: `/diary`, close tab, new thread, next bootstrap from `workflow.md`.

See [example-workflow.md](example-workflow.md) for a filled reference.

---

## Works well with

| Skill / doc | Role |
|-------------|------|
| **ado-doc** | Doc edits, commit/PR, cherry-picks during execution threads |
| **diary** | Ticket-scoped `worklog.md` vs global `diary.md` |
| **token-check** | Weekly measurement that your thread-splitting habits are working |
| **docs/token-efficiency/** | Action Card + companion analysis in this repo |

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team. Shared edition strips personal paths and tracker-specific examples.
