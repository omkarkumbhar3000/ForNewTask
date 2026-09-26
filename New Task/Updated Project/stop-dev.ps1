# Stops the CleverCubs application on port 8080. Add -Database to stop the MySQL container as well (its data is kept).
#
#   powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\stop-dev.ps1" [-Database]
param([switch]$Database)

$busy = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($busy) {
    Stop-Process -Id $busy.OwningProcess -Force
    Write-Host "Stopped CleverCubs (process $($busy.OwningProcess))."
} else {
    Write-Host 'CleverCubs is not running.'
}
if ($Database) {
    Push-Location $PSScriptRoot
    try { docker compose stop | Out-Host } finally { Pop-Location }
}
