# ado-doc-workflow — Installation & Security Notes

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

> **This bundle was refreshed on 2026-05-28** in response to a Synopsys
> security finding. The previous version of these skills used
> `curl.exe --ntlm -u "$($env:ADO_Username):$($env:ADO_Password)" <url>`
> for all ADO API calls. That pattern leaks the literal password into
> the `curl.exe` process command line, where it is captured by Windows
> process auditing (Event ID 4688), Sysmon, Defender for Endpoint, and
> any process that can read `Win32_Process.CommandLine` via WMI.
>
> PowerShell expands `$env:VAR` **before** calling `CreateProcess`, so
> referencing the password through a variable does **not** prevent the
> leak — the literal value still lands in argv. This had been silently
> happening on every ADO call.
>
> The fix: do all auth'd HTTP from inside PowerShell using
> `Invoke-RestMethod -Credential <PSCredential>`. The credential is held
> as a `SecureString` in PS-process memory and never appears in any
> child-process argv (because there is no child process — `IRM` is
> in-process .NET HttpClient).

The new SKILL files in this bundle reference a shared helper at
`%USERPROFILE%\.cursor\lib\Ado-Auth.ps1`. **You must install it for the
skills to work.**

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

3. (Strongly recommended) Copy `rules\no-credentials-on-cmdline.mdc` to
   `%USERPROFILE%\.cursor\rules\no-credentials-on-cmdline.mdc`. This
   rule documents the leak and forbids agents from regressing to the
   old pattern.

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

## What changed between bundle versions

- All `curl.exe --ntlm -u "..."` examples in the three SKILL files were
  replaced with `Invoke-AdoRest` calls (which use `Invoke-RestMethod
  -Credential` under the hood).
- All `curl ... -X PATCH -d '...'` examples were replaced with
  `Invoke-AdoRest -Method Patch -Body @{ ... }` (PowerShell hashtable
  bodies, JSON-encoded by the helper).
- The credentials section in each SKILL no longer shows a literal
  `-u 'ANSYS\<user>:<pass>'` template; it just dot-sources the helper.
- New file: `lib/Ado-Auth.ps1` — the shared credential helper.
- New file: `rules/no-credentials-on-cmdline.mdc` — the protective rule.
- `flo.mdc` — minor refresh; no security change.

If you customized your local copy of any SKILL file from a previous
bundle, merge the relevant new credential-handling sections in rather
than blowing your edits away.

---

## Optional: matching hook

The host where this bundle was authored also runs a
`gate-credential-leak.ps1` Cursor hook that blocks `curl.exe -u`,
`wget --user`, basic-auth URLs, and literal env-file values from ever
hitting any shell command. That hook is not bundled here because it's
tied to a specific `.env` path, but the rule file describes its
behavior and you can lift its logic from `%USERPROFILE%\.cursor\hooks\`
on the authoring host if you want the same belt-and-suspenders setup.

---

## Questions

Ping Leslie Poff (Team Charlie, Collaborative Services) on Teams.
