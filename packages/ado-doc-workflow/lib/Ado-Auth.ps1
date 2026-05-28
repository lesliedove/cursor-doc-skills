# Ado-Auth.ps1 -- shared NTLM auth helper for on-prem TFS calls.
#
# WHY THIS EXISTS
# ===============
# Do all auth'd HTTP from inside PowerShell using the cmdlets
# Invoke-RestMethod / Invoke-WebRequest with -Credential <PSCredential>.
# A PSCredential object holds the password as a SecureString in PS-process
# memory and never appears in argv of any child process (because there is no
# child process -- IRM is in-process .NET HttpClient, not curl.exe).
#
# Do NOT shell out to curl.exe -u "$($env:ADO_Username):$($env:ADO_Password)".
# PowerShell expands the env vars before calling CreateProcess, so the literal
# password lands in curl's argv where any host-level process monitoring
# (WMI Win32_Process.CommandLine, Defender for Endpoint, Sysmon, EDR)
# captures it. Variable references do not prevent the leak.
#
# USAGE
# =====
# At the top of any script, dot-source this file:
#
#   . "$env:USERPROFILE\.cursor\lib\Ado-Auth.ps1"
#
# Then either:
#
#   $cred = Get-AdoCredential
#   $resp = Invoke-RestMethod -Uri $url -Credential $cred
#
# Or (more concise, recommended):
#
#   $resp = Invoke-AdoRest -Uri $url
#   $resp = Invoke-AdoRest -Uri $url -Method Patch -Body $patchObj `
#             -ContentType 'application/json-patch+json'
#   Invoke-AdoRest -Uri $url -OutFile 'C:\GitRepos\.scratch\foo.json'
#
# DO NOT
# ======
# Never use curl.exe / wget / Invoke-Expression with -u "$env:ADO_Username:..."
# or any other shape where PowerShell expands the credential variable into
# argv of an external process.

$script:AdoAuthCachedCred = $null

function Get-AdoCredential {
  <#
  .SYNOPSIS
  Build a [PSCredential] from $env:USERPROFILE\.env and cache it for the session.

  .PARAMETER EnvFile
  Path to the env file. Defaults to %USERPROFILE%\.env.

  .PARAMETER Refresh
  Force a re-read from the env file (otherwise returns the cached credential).
  #>
  [CmdletBinding()]
  param(
    [string]$EnvFile = (Join-Path $env:USERPROFILE '.env'),
    [switch]$Refresh
  )

  if ($script:AdoAuthCachedCred -and -not $Refresh) {
    return $script:AdoAuthCachedCred
  }
  if (-not (Test-Path $EnvFile)) {
    throw "ADO env file not found: $EnvFile (expected ADO_Username and ADO_Password)"
  }

  $user = $null
  $pw = $null
  foreach ($line in Get-Content $EnvFile -ErrorAction Stop) {
    if ($line -match '^\s*ADO_Username\s*=\s*(.*)\s*$') { $user = $matches[1].Trim().Trim('"').Trim("'") }
    elseif ($line -match '^\s*ADO_Password\s*=\s*(.*)\s*$') { $pw = $matches[1].Trim().Trim('"').Trim("'") }
  }
  if (-not $user) { throw "ADO_Username not found in $EnvFile" }
  if (-not $pw)   { throw "ADO_Password not found in $EnvFile" }

  # Mirror into env so existing skill code that reads $env:ADO_Username
  # for things like NTLM domain prefixes keeps working.
  Set-Item -Path env:ADO_Username -Value $user
  Set-Item -Path env:ADO_Password -Value $pw

  $secPw = ConvertTo-SecureString $pw -AsPlainText -Force
  $cred = New-Object System.Management.Automation.PSCredential($user, $secPw)
  $pw = $null  # drop the local plaintext copy from the function scope
  $script:AdoAuthCachedCred = $cred
  return $cred
}

function Invoke-AdoRest {
  <#
  .SYNOPSIS
  Convenience wrapper around Invoke-RestMethod with the cached ADO credential
  and the on-prem TFS URL conventions baked in. Replaces curl.exe -u ... NTLM.

  .PARAMETER Uri
  Full request URL. Required.

  .PARAMETER Method
  HTTP verb (Get, Post, Patch, Put, Delete). Default: Get.

  .PARAMETER Body
  Request body. Either a string (used as-is) or an object (JSON-encoded).

  .PARAMETER ContentType
  Default 'application/json'. Use 'application/json-patch+json' for ADO PATCH
  document bodies.

  .PARAMETER OutFile
  If set, response body is written to this path (mirrors curl -o).

  .PARAMETER TimeoutSec
  Default 60.

  .PARAMETER Credential
  Override the cached credential (rarely needed).

  .PARAMETER Headers
  Optional additional headers (hashtable).
  #>
  [CmdletBinding()]
  param(
    [Parameter(Mandatory)] [string] $Uri,
    [ValidateSet('Get','Post','Patch','Put','Delete','Head','Options')]
    [string] $Method = 'Get',
    [object] $Body,
    [string] $ContentType = 'application/json',
    [string] $OutFile,
    [int]    $TimeoutSec = 60,
    [System.Management.Automation.PSCredential] $Credential,
    [hashtable] $Headers
  )

  if (-not $Credential) { $Credential = Get-AdoCredential }

  $params = @{
    Uri         = $Uri
    Credential  = $Credential
    Method      = $Method
    TimeoutSec  = $TimeoutSec
    ErrorAction = 'Stop'
  }
  if ($PSBoundParameters.ContainsKey('Body')) {
    if ($Body -is [string]) {
      $params.Body = $Body
    } else {
      $params.Body = ($Body | ConvertTo-Json -Depth 20 -Compress)
    }
    $params.ContentType = $ContentType
  }
  if ($OutFile)  { $params.OutFile  = $OutFile }
  if ($Headers)  { $params.Headers  = $Headers }

  return Invoke-RestMethod @params
}

# Quick sanity check when this file is run directly (e.g., for debugging).
if ($MyInvocation.InvocationName -ne '.') {
  Write-Host "Ado-Auth.ps1 loaded. To use:" -ForegroundColor Cyan
  Write-Host "  . `"$PSCommandPath`""
  Write-Host "  `$cred = Get-AdoCredential"
  Write-Host "  `$resp = Invoke-AdoRest -Uri 'https://ado.internal.synopsys.com/tfs/.../workitems/<id>?api-version=6.0'"
}
