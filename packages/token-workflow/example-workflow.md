# Example workflow (reference)

Filled workflow from a production run: nested DocBook `<section>` elements under bridgehead parents were dropped from LLM corpus output.

## Summary

- **Problem:** Parser dropped nested sections in a specific XML pattern.
- **Pattern:** TDD → fix → ship (3 threads + thin post-merge threads for skill sync and tracker close).
- **Key trap:** Source fixture XML was ~32K lines — grep or small test fixture only.

## Phase split

| Thread | Focus | Outcome |
|---|---|---|
| Plan | Workflow planning | `workflow.md` written |
| 1 — TDD | Failing pytest on feature branch | Test fails for the right reason |
| 2 — Fix | Minimal code change | All targeted tests green |
| 3 — Ship | Commit, push, PR | PR open, ticket linked |
| Post | Housekeeping | Separate one-off chats |

## What made planning "earn its keep"

1. **Repo mapping** — ticket title suggested one repo; fix lived in another.
2. **Model** — `composer-2.5` for all three execution threads.
3. **Token traps** — documented before any thread could load the huge XML or rebuild the corpus.
4. **Bootstrap prompts** — Threads 2–3 needed zero re-explanation from the planning chat.

## Thread 1 bootstrap (abbreviated)

```
Pick up ticket <id> in C:\GitRepos\<correct-repo>.
Read <scratch_dir>\<ticket-id>-<slug>\workflow.md and
<scratch_dir>\<prior-ticket>-investigate\investigation.md.
Branch feat/<ticket-id>-<slug> from main.
Write a failing pytest fixture for the bridgehead + nested <section> pattern.
Do not read the full 32K-line source XML.
Stop after the test fails — don't fix yet.
```

## Reuse next time

Same repo + same TDD→fix→ship pattern: copy `workflow-template.md`, swap ticket/repo/paths, update traps — **skip a long planning chat**.
