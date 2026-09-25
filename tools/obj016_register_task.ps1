<#
.SYNOPSIS
    Register (or remove) the OBJ-016 daily pull-and-refresh scheduled task.

.DESCRIPTION
    Creates a USER-LEVEL Windows scheduled task that runs obj016_daily_refresh.py --execute
    once a day. No administrator rights and no stored password are required: the task runs
    interactively as the current user, so it only fires while that user is logged on.

    StartWhenAvailable is deliberate. This is a workstation, not a server: if the machine is
    off at the scheduled time the task runs at the next opportunity instead of silently
    skipping the day.

    ASCII ONLY, ON PURPOSE. Windows PowerShell 5.1 reads a UTF-8 file with no BOM as ANSI.
    An em-dash then decodes to three cp1252 characters, the last of which is a right double
    quotation mark that PowerShell accepts as a string delimiter - which opens an
    unterminated string and the whole script fails to parse. Keep every character in this
    file 7-bit ASCII.

.PARAMETER At
    Time of day, 24-hour "HH:mm". Default 08:30.

.PARAMETER Remove
    Unregister the task instead of creating it.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\obj016_register_task.ps1
    powershell -ExecutionPolicy Bypass -File tools\obj016_register_task.ps1 -At 21:00
    powershell -ExecutionPolicy Bypass -File tools\obj016_register_task.ps1 -Remove
#>
[CmdletBinding()]
param(
    [string] $At = '08:30',
    [switch] $Remove
)

$ErrorActionPreference = 'Stop'

$TaskName = 'PAM-Dashboard-Daily-Refresh'
# OBJ-025: was Join-Path $PSScriptRoot '..\..' - a two-hop guess that was
# correct only while this script sat at workbench/scripts/. It now lives in
# tools/, one level down, so the root is found by MARKER instead. Mirrors
# tools/paths.py workspace_root().
$Root = $PSScriptRoot
while ($Root -and -not ((Test-Path (Join-Path $Root 'CLAUDE.md')) -and (Test-Path (Join-Path $Root '.claude')))) {
    $Root = Split-Path $Root -Parent
}
if (-not $Root) { throw "cannot locate the workspace root above $PSScriptRoot" }
$Script   = Join-Path $Root 'tools\obj016_daily_refresh.py'

if ($Remove) {
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Output "Removed scheduled task '$TaskName'."
    } else {
        Write-Output "No scheduled task named '$TaskName' - nothing to remove."
    }
    return
}

if (-not (Test-Path $Script)) { throw "Job script not found: $Script" }

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { throw 'python is not on PATH - cannot register the task.' }

# Quote the script path: the workspace path contains a space ("Dev Project").
$action = New-ScheduledTaskAction -Execute $python -Argument "`"$Script`" --execute" -WorkingDirectory $Root

$trigger = New-ScheduledTaskTrigger -Daily -At $At

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 2)

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

$description = @"
OBJ-016. Daily pull and refresh for the PAM API automation workspace.

Fast-forward pulls pam/ (skipped if its tree is dirty), fetches the automation repo and reports
how far AI is behind origin/Dev WITHOUT merging, then re-runs the drift check, the RAG evidence
index and the dashboard datasets.

Does NOT execute the API suite. Does NOT call any PAM endpoint. Does NOT push or merge. Does
NOT apply drift auto-fixes. Log: state\daily\daily.log
"@

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description $description -Force | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
$i = Get-ScheduledTaskInfo -TaskName $TaskName
Write-Output "Registered '$TaskName'"
Write-Output "  state    : $($t.State)"
Write-Output "  runs at  : $At daily (catches up if the machine was off)"
Write-Output "  next run : $($i.NextRunTime)"
Write-Output "  command  : $python `"$Script`" --execute"
Write-Output ''
Write-Output "Run it now : Start-ScheduledTask -TaskName $TaskName"
Write-Output "Remove it  : powershell -ExecutionPolicy Bypass -File tools\obj016_register_task.ps1 -Remove"
