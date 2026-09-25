<#
.SYNOPSIS
    Register (or remove) the daily client-raised PAMIT ticket analysis task (OBJ-028).

.DESCRIPTION
    Creates a USER-LEVEL Windows scheduled task that runs pamit_client_analysis.py once a
    day at 09:00. No administrator rights and no stored password are required: the task
    runs interactively as the current user, so it fires only while that user is logged on.

    StartWhenAvailable is deliberate. This is a workstation, not a server: if the machine
    is off at 09:00 the run happens at the next opportunity instead of silently skipping
    the day and leaving a hole in the dated summary series.

    The job is READ-ONLY against Jira. It issues GET requests plus POST to the two Jira
    search endpoints and nothing else - the guard in jira_query.py refuses any other
    method or path. It never touches a PAMIT ticket, field, comment or workflow, and it
    issues ZERO requests to the PAM product API.

    ASCII ONLY, ON PURPOSE. Windows PowerShell 5.1 reads a UTF-8 file with no BOM as ANSI.
    An em-dash then decodes to three cp1252 characters, the last of which is a right
    double quotation mark that PowerShell accepts as a string delimiter - which opens an
    unterminated string and the whole script fails to parse. Keep every character in this
    file 7-bit ASCII.

.PARAMETER At
    Time of day, 24-hour "HH:mm". Default 09:00.

.PARAMETER Remove
    Unregister the task instead of creating it.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\jira\register_client_analysis_task.ps1
    powershell -ExecutionPolicy Bypass -File tools\jira\register_client_analysis_task.ps1 -At 07:30
    powershell -ExecutionPolicy Bypass -File tools\jira\register_client_analysis_task.ps1 -Remove
#>
[CmdletBinding()]
param(
    [string] $At = '09:00',
    [switch] $Remove
)

$ErrorActionPreference = 'Stop'

$TaskName = 'PAM-Client-Ticket-Analysis'

# Root by MARKER, never by counting parents. Mirrors tools/paths.py workspace_root():
# this script sits two levels down (tools\jira\), and a fixed-depth guess is exactly
# what broke seven scripts during the v0.3 restructure.
$Root = $PSScriptRoot
while ($Root -and -not ((Test-Path (Join-Path $Root 'CLAUDE.md')) -and (Test-Path (Join-Path $Root '.claude')))) {
    $Root = Split-Path $Root -Parent
}
if (-not $Root) { throw "cannot locate the workspace root above $PSScriptRoot" }
$Script = Join-Path $Root 'tools\jira\pamit_client_analysis.py'

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
if (-not (Test-Path (Join-Path $Root 'tools\jira\.env'))) {
    throw "tools\jira\.env is missing - the task would fail every morning on auth."
}

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { throw 'python is not on PATH - cannot register the task.' }

# PYTHONUTF8=1 is not optional. A scheduled child Python gets NO console, so it picks
# the ANSI codepage and dies printing the report's non-ASCII characters. The same trap
# was already measured on the daily refresh job.
#
# The assignment MUST be quoted as set "VAR=value". Written the obvious way,
#     set PYTHONUTF8=1 && python ...
# cmd assigns everything up to the ampersand INCLUDING the space, so the value becomes
# "1 " and Python refuses to start:
#     Fatal Python error: preconfig_init_utf8_mode: invalid PYTHONUTF8 environment
#     variable value
# That was measured here, not guessed: the first registration of this task exited 1 in
# under a second every time and wrote nothing, with no error anywhere the job's own log
# could show it. Quoting the assignment ends the value at the closing quote.
$argument = "/c set `"PYTHONUTF8=1`" && `"$python`" `"$Script`""
$action = New-ScheduledTaskAction -Execute "$env:SystemRoot\System32\cmd.exe" `
    -Argument $argument -WorkingDirectory $Root

$trigger = New-ScheduledTaskTrigger -Daily -At $At

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive -RunLevel Limited

$description = @"
OBJ-028. Daily client-raised PAMIT ticket analysis, 09:00.

Reads Jira PAMIT READ-ONLY and produces five views: the whole 35.8.29 build line with Jira
release dates reported as context, the in-flight focus builds (HF12 / HF13 current / HF14 /
HF15), what clients reported in the last 30 days at any fix version, Query C (open client
defects carrying no fix version), and the testing weak-spot axis.

Writes a dated summary to docs\analysis\summary\summary_YYYY-MM-DD.md which is never
overwritten across days, refreshes docs\analysis\D1-client-ticket-patterns.md, and stores
data under artifacts\client-tickets\.

Does NOT modify any Jira ticket, field, comment or workflow. Does NOT call the PAM product
API. Does NOT push, merge or touch git. Log: state\client-analysis\analysis.log
"@

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal -Description $description -Force | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
$i = Get-ScheduledTaskInfo -TaskName $TaskName
Write-Output "Registered '$TaskName'"
Write-Output "  state    : $($t.State)"
Write-Output "  runs at  : $At daily (catches up if the machine was off)"
Write-Output "  next run : $($i.NextRunTime)"
Write-Output "  command  : cmd.exe $argument"
Write-Output ''
Write-Output "Run it now : Start-ScheduledTask -TaskName $TaskName"
Write-Output "Remove it  : powershell -ExecutionPolicy Bypass -File tools\jira\register_client_analysis_task.ps1 -Remove"
