<#
.SYNOPSIS
    Register (or remove) the OBJ-017 weekly API execution scheduled task.

.DESCRIPTION
    Creates a USER-LEVEL Windows scheduled task that runs obj017_weekly_execution.py --execute
    every Sunday. No administrator rights and no stored password: the task runs interactively as
    the current user, so it only fires while that user is logged on.

    ExecutionTimeLimit is 14 hours, not a typo. The execution itself is capped at 6 hours by
    --budget-seconds, and a single automatic resume can add another 6, so the worst legitimate
    case is ~12 hours plus reporting. MultipleInstances IgnoreNew means a run that is still going
    when the next Sunday arrives is never doubled up.

    ASCII ONLY, ON PURPOSE. Windows PowerShell 5.1 reads a UTF-8 file with no BOM as ANSI. An
    em-dash then decodes to three cp1252 characters ending in a right double quotation mark, which
    PowerShell accepts as a string delimiter - opening an unterminated string and failing the whole
    file at parse time. Keep every character here 7-bit ASCII.

.PARAMETER At
    Time of day, 24-hour "HH:mm". Default 10:00.

.PARAMETER Remove
    Unregister the task instead of creating it.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\obj017_register_weekly_task.ps1
    powershell -ExecutionPolicy Bypass -File tools\obj017_register_weekly_task.ps1 -At 22:00
    powershell -ExecutionPolicy Bypass -File tools\obj017_register_weekly_task.ps1 -Remove
#>
[CmdletBinding()]
param(
    [string] $At = '10:00',
    [switch] $Remove
)

$ErrorActionPreference = 'Stop'

$TaskName = 'PAM-Weekly-API-Execution'
# OBJ-025: was Join-Path $PSScriptRoot '..\..' - a two-hop guess that was
# correct only while this script sat at workbench/scripts/. It now lives in
# tools/, one level down, so the root is found by MARKER instead. Mirrors
# tools/paths.py workspace_root().
$Root = $PSScriptRoot
while ($Root -and -not ((Test-Path (Join-Path $Root 'CLAUDE.md')) -and (Test-Path (Join-Path $Root '.claude')))) {
    $Root = Split-Path $Root -Parent
}
if (-not $Root) { throw "cannot locate the workspace root above $PSScriptRoot" }
$Script   = Join-Path $Root 'tools\obj017_weekly_execution.py'

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

$action = New-ScheduledTaskAction -Execute $python -Argument "`"$Script`" --execute" -WorkingDirectory $Root

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At $At

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 14)

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

$description = @"
OBJ-017. Weekly full API execution for the PAM automation workspace.

Probes the environment WITHOUT a credential first, so a token is never spent against a host that
cannot answer. Aborts immediately if a previous token attempt latched. Then: generate flows ->
chain_runner --execute (full suite, 6-hour budget, GET/POST/PUT/PATCH) -> one resume if any flow
aborted -> validation gate -> run workbook against the previous run -> regenerate the dashboard.

NEVER passes --allow-teardown, --allow-preexisting-teardown or --include-unsafe. NEVER retries the
token. NEVER runs Maven or a TestNG suite. Log: state\weekly\weekly.log
"@

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description $description -Force | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
$i = Get-ScheduledTaskInfo -TaskName $TaskName
Write-Output "Registered '$TaskName'"
Write-Output "  state    : $($t.State)"
Write-Output "  runs at  : Sundays $At (catches up if the machine was off)"
Write-Output "  next run : $($i.NextRunTime)"
Write-Output "  command  : $python `"$Script`" --execute"
Write-Output ''
Write-Output "Dry run first : python tools\obj017_weekly_execution.py"
Write-Output "Run it now    : Start-ScheduledTask -TaskName $TaskName"
Write-Output "Remove it     : powershell -ExecutionPolicy Bypass -File tools\obj017_register_weekly_task.ps1 -Remove"
