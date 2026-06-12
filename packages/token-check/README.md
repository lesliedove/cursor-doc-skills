# Token Check Skill — Shared Edition

Weekly health check on Cursor token discipline. Compare your latest team-usage CSV against a **frozen baseline** and get a short report: wins first, volume-focused cache-read metrics, model-mix drift, and concrete recommendations for next week.

Part of the **[cursor-doc-skills](https://github.com/lesliedove/cursor-doc-skills)** catalog. Companion analysis docs live in [`docs/token-efficiency/`](../../docs/token-efficiency/).

---

## What it does

1. You export `team-usage-events-*.csv` from the Cursor admin dashboard (Team → Usage → Export).
2. Run `/token-check` (or drop the CSV path in chat).
3. The agent analyzes the **last 7 days** in PowerShell — the CSV never gets dumped into chat.
4. A markdown report lands in your configured `report_dir` (default `%USERPROFILE%\Downloads\How-I-AI\`).
5. A JSON snapshot appends to `history_dir` for trend charts after 4+ weeks.

**Key metric:** cache-read **volume** (tokens/week, per event, per active day) — not cache-read **share**, which stays ~90% in normal Agent threads regardless of habits.

---

## Install

### 1. Skill

Drag the unzipped folder (or `token-check.zip` from `dist/`) into a Cursor chat and say **"Add this as a global skill."**

```
%USERPROFILE%\.cursor\skills\token-check\
  SKILL.md
  README.md
  config.example.json
  samples\token-check-example.md
```

### 2. Config

```powershell
Copy-Item "$env:USERPROFILE\.cursor\skills\token-check\config.example.json" `
          "$env:USERPROFILE\.cursor\skills\token-check\config.json"
notepad "$env:USERPROFILE\.cursor\skills\token-check\config.json"
```

**Required:** replace the `baseline` block with numbers from **your** first usage analysis. The example values are Leslie's May 2026 window — useful as a reference shape, not as your comparison point.

**Optional:** copy the reference docs from this repo into `reference_docs_dir`:

```powershell
$dest = "$env:USERPROFILE\Downloads\How-I-AI"
New-Item -ItemType Directory -Path $dest -Force | Out-Null
Copy-Item "C:\path\to\cursor-doc-skills\docs\token-efficiency\token-budgeting-companion.md" $dest
```

### 3. Optional: always-on rule

Install [`rules/token-budget.mdc`](../../rules/token-budget.mdc) from the repo root — copy to `%USERPROFILE%\.cursor\rules\token-budget.mdc` (or drag into Cursor → "Add as global rule"). Set `alwaysApply: true` in the YAML front matter for ambient nudges on every chat. See [`rules/README.md`](../../rules/README.md).

---

## Usage

**Weekly (recommended):** Friday morning — export CSV, then `/token-check`.

**Ad-hoc:** Drop a CSV path: "run token check on `C:\Users\me\Downloads\team-usage-events-….csv`"

**Reminder:** Add a one-line entry to your workspace `.cursor/reminders.md` if you want Flo (or your morning routine) to prompt you on `check_day_of_week`.

---

## Sample output

See [samples/token-check-example.md](samples/token-check-example.md) — a real week showing 65% below baseline on cache-read volume after adopting the habit stack.

---

## Works well with

| Artifact | Role |
|----------|------|
| **token-workflow** | Split multi-phase tickets so weekly volume actually drops |
| **[`rules/token-budget.mdc`](../../rules/token-budget.mdc)** | Ambient coaching the check measures against |
| **docs/token-efficiency/** | Companion + work summary — the *why* behind the habits |

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team. Shared edition uses `config.json` instead of hardcoded paths and baseline.
