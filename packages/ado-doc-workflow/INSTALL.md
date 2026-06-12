# ado-doc-workflow — Installation

This bundle contains four Cursor skills/rules for Azure DevOps documentation work:

| File | Install location | Purpose |
|------|------------------|---------|
| `ado-query-SKILL.md` | `%USERPROFILE%\.cursor\skills\ado\SKILL.md` | Read-only ADO queries (`/ado item`, `/ado items`, `/ado prs`, `/ado build`, `/ado dashboard`, etc.) |
| `ado-doc-SKILL.md` | `%USERPROFILE%\.cursor\skills\ado-doc\SKILL.md` | End-to-end doc ticket workflow (`/ado doc <id>`, `/ado doc commitpr`, `/ado doc cherry`, etc.) |
| `ado-release-docs-SKILL.md` | `%USERPROFILE%\.cursor\skills\ado-release-docs\SKILL.md` | RIL / KIL / Release Notes generators |
| `flo.mdc` | `%USERPROFILE%\.cursor\rules\flo.mdc` | Optional. Orchestrator persona that routes natural-language requests to the skills above. |

The simplest way to install: drag any of the `.md` / `.mdc` files (or the unzipped folder) into a Cursor chat and say **"Add this as a global skill / rule"**. Cursor will put each file in the right place. The renames above are how the published filenames map to the standard Cursor skill folder names.

---

## REQUIRED: install the credential helper

The skills authenticate to ADO using a small PowerShell helper bundled at `lib\Ado-Auth.ps1`. It wraps `Invoke-RestMethod -Credential <PSCredential>`, which keeps the password in PS-process memory and never lets it appear on a command line. **Don't substitute `curl.exe -u "$env:..."` — even with a variable reference, PowerShell expands the value before `CreateProcess`, so the literal password lands in `curl`'s argv where process auditing and EDR can read it.** Use the helper.

1. Copy `lib\Ado-Auth.ps1` from this bundle to `%USERPROFILE%\.cursor\lib\Ado-Auth.ps1`
   (create the `lib` folder if it doesn't exist).

2. Create `%USERPROFILE%\.env` (or whatever path you prefer; the helper
   accepts `-EnvFile <path>`) with:

   ```
   ADO_Username=ANSYS\<your-username>
   ADO_Password=<your-password>
   ```

   The username must already include the `ANSYS\` domain prefix for
   NTLM. Lock the file down (`icacls %USERPROFILE%\.env /inheritance:r /grant:r "%USERNAME%:F"`).

3. (Strongly recommended) Copy `rules\no-credentials-on-cmdline.mdc` from
   this bundle to `%USERPROFILE%\.cursor\rules\no-credentials-on-cmdline.mdc`.
   This rule keeps agents from regressing to the `curl.exe -u` pattern.

   Optional shared rules from the repo [`rules/`](../../rules/) folder:
   `edit-discipline.mdc`, `no-policy-override.mdc`, and (if your team
   does not use ADO tags) `no-ticket-tags.mdc`. See
   [`rules/README.md`](../../rules/README.md).

Quick smoke test (PowerShell):

```powershell
. "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
$wi = Invoke-AdoRest -Uri 'https://ado.internal.synopsys.com/tfs/ANSYS_Development/_apis/wit/workitems/1?api-version=6.0'
$wi.id
```

If you see a ticket ID, you're set. If you see a 401, double-check the
`ANSYS\` prefix on `ADO_Username` and that the password in `.env`
matches your current AD password.

---

## Questions / bugs

Ping **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team. Or open an issue on the repo.
