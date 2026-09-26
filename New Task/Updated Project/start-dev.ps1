# Starts CleverCubs for local development: checks the setup, starts MySQL in Docker, builds the application,
# starts it on http://127.0.0.1:8080 and opens the browser. Run from any folder:
#
#   powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\start-dev.ps1"
#   ... -SkipBuild     reuse the last build
#   ... -Restart       stop an instance already running on port 8080 first
#   ... -NoBrowser     do not open the browser
param([switch]$SkipBuild, [switch]$Restart, [switch]$NoBrowser)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$app = Join-Path $root 'app'
$url = 'http://127.0.0.1:8080'

function Step($text) { Write-Host "==> $text" -ForegroundColor Green }
function Fail($text) { Write-Host "STOP: $text" -ForegroundColor Red; exit 1 }

# 1. Java: use JAVA_HOME if it is valid, otherwise the newest JDK under Program Files\Java.
if (-not $env:JAVA_HOME -or -not (Test-Path (Join-Path $env:JAVA_HOME 'bin\java.exe'))) {
    $jdk = Get-ChildItem 'C:\Program Files\Java' -Directory -Filter 'jdk-*' -ErrorAction SilentlyContinue |
        Where-Object { Test-Path (Join-Path $_.FullName 'bin\java.exe') } |
        Sort-Object Name -Descending | Select-Object -First 1
    if (-not $jdk) { Fail 'No JDK found. Install JDK 25 or newer.' }
    $env:JAVA_HOME = $jdk.FullName
}
$java = Join-Path $env:JAVA_HOME 'bin\java.exe'
Step "Java: $env:JAVA_HOME"

# 2. Configuration: .env holds the database passwords and the first Super Admin; it is never committed.
$envFile = Join-Path $root '.env'
if (-not (Test-Path $envFile)) {
    Copy-Item (Join-Path $root '.env.example') $envFile
    Fail "Created .env from .env.example. Fill in every value in $envFile, then run this script again."
}

# 3. Media: the course pictures, sounds and videos live in Updated Project\media (made once by tools\extract_content.py).
if (-not (Test-Path (Join-Path $root 'media\alphabets'))) {
    Fail 'The media folder is missing. Run: python3.11 "New Task\Updated Project\tools\extract_content.py"'
}

# 4. Database.
Step 'Starting MySQL (Docker)'
docker info *> $null
if ($LASTEXITCODE -ne 0) { Fail 'Docker is not running. Start Docker Desktop and try again.' }
Push-Location $root
try { docker compose up -d | Out-Host } finally { Pop-Location }
for ($i = 0; $i -lt 60; $i++) {
    $health = docker inspect --format '{{.State.Health.Status}}' clevercubs-mysql 2>$null
    if ($health -eq 'healthy') { break }
    Start-Sleep -Seconds 2
}
if ($health -ne 'healthy') { Fail 'MySQL did not become healthy. Check: docker logs clevercubs-mysql' }

# 5. Port 8080.
$busy = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($busy) {
    if ($Restart) {
        Step "Stopping the instance on port 8080 (process $($busy.OwningProcess))"
        Stop-Process -Id $busy.OwningProcess -Force
        Start-Sleep -Seconds 2
    } else {
        Fail "Port 8080 is already in use (process $($busy.OwningProcess)). Open $url, or run with -Restart."
    }
}

# 6. Build.
$jar = Join-Path $app 'target\clevercubs-1.0.0-SNAPSHOT.jar'
if (-not $SkipBuild -or -not (Test-Path $jar)) {
    Step 'Building (tests are run separately with: app\mvnw.cmd -f app\pom.xml verify)'
    & (Join-Path $app 'mvnw.cmd') -q -f (Join-Path $app 'pom.xml') -DskipTests package
    if ($LASTEXITCODE -ne 0) { Fail 'The build failed. See the output above.' }
}

# 7. Start, detached, with the log in .tmp\app.log.
$logs = Join-Path $root '.tmp'
New-Item -ItemType Directory -Force $logs | Out-Null
Step 'Starting CleverCubs'
$proc = Start-Process -FilePath $java -ArgumentList '-jar', 'target\clevercubs-1.0.0-SNAPSHOT.jar', '--spring.profiles.active=dev' `
    -WorkingDirectory $app -RedirectStandardOutput (Join-Path $logs 'app.log') -RedirectStandardError (Join-Path $logs 'app-err.log') `
    -WindowStyle Hidden -PassThru
$ok = $false
for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 2
    if ($proc.HasExited) { break }
    try { if ((Invoke-WebRequest -UseBasicParsing "$url/api/v1/public/health" -TimeoutSec 3).StatusCode -eq 200) { $ok = $true; break } } catch { }
}
if (-not $ok) { Fail "CleverCubs did not start. See $logs\app.log" }
Step "CleverCubs is running at $url (process $($proc.Id)). Stop it with stop-dev.ps1."

if (-not $NoBrowser) {
    $chrome = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe") |
        Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($chrome) { Start-Process $chrome $url } else { Start-Process $url }
}
