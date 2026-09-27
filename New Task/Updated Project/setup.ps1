# CleverCubs one-step setup for Windows (README.md section 5). It checks what the project needs, installs
# what can safely be installed, prepares the local configuration without printing any secret, installs the
# project's dependencies, starts the application and opens it in Chrome. Safe to run again: nothing that
# already exists is overwritten.
#
#   powershell -ExecutionPolicy Bypass -File "New Task\Updated Project\setup.ps1"                 everything
#   ... -CheckOnly                     report only: install nothing, write nothing, start nothing
#   ... -NoInstall                     never install software; list what is missing instead
#   ... -NoStart                       prepare everything, but do not start the application
#   ... -NoBrowser                     start, but do not open Chrome
#   ... -AdminEmail you@example.com    also create a local Super Admin (its temporary password goes into .env only)
#   ... -CloneTo C:\work\CleverCubs    run this file on its own: clone the repository into that folder first
param(
    [switch]$CheckOnly,
    [switch]$NoInstall,
    [switch]$NoStart,
    [switch]$NoBrowser,
    [string]$AdminEmail = '',
    [string]$CloneTo = ''
)

# Not 'Stop': Windows PowerShell 5.1 turns every stderr line of a native tool (docker compose and git print
# their progress there) into an error record when output is captured, and 'Stop' would end the script on the
# first one. Native tools are judged by their exit codes; the few cmdlets that must not fail use -ErrorAction Stop.
$ErrorActionPreference = 'Continue'
$RepoUrl = 'https://github.com/omkarkumbhar3000/ForNewTask.git'
$ProjectInRepo = 'New Task\Updated Project'
$AppUrl = 'http://127.0.0.1:8080'
$MinJava = 25
$MinNode = 20
$install = -not ($CheckOnly -or $NoInstall)
$results = New-Object System.Collections.Generic.List[object]
$manual = New-Object System.Collections.Generic.List[string]

function Say($text) { Write-Host "==> $text" -ForegroundColor Green }
function Note($text) { Write-Host "    $text" }
function Warn($text) { Write-Host "!!  $text" -ForegroundColor Yellow }
function Stop-Setup($text) { Write-Host "STOP: $text" -ForegroundColor Red; exit 1 }
function Record($item, $status, $detail) { $results.Add([pscustomobject]@{ Item = $item; Status = $status; Detail = $detail }) }

function Update-SessionPath {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}

function Install-WithWinget($id, $name) {
    if (-not $install) { return $false }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        $manual.Add("Install $name by hand (winget is not available on this PC).")
        return $false
    }
    Say "Installing $name with winget ($id)"
    winget install --id $id --exact --silent --accept-package-agreements --accept-source-agreements | Out-Host
    Update-SessionPath
    return ($LASTEXITCODE -eq 0)
}

# A JDK is usable when its "release" file says version 25 or newer. JAVA_HOME is tried first, then the usual
# install folders (Oracle, Eclipse Temurin, Microsoft, Azul), newest first.
function Find-Jdk {
    $candidates = @()
    if ($env:JAVA_HOME) { $candidates += $env:JAVA_HOME }
    foreach ($base in @("$env:ProgramFiles\Java", "$env:ProgramFiles\Eclipse Adoptium", "$env:ProgramFiles\Microsoft", "$env:ProgramFiles\Zulu")) {
        if (Test-Path $base) { $candidates += (Get-ChildItem $base -Directory | Sort-Object Name -Descending | ForEach-Object FullName) }
    }
    foreach ($jdkHome in $candidates) {
        $release = Join-Path $jdkHome 'release'
        if ((Test-Path (Join-Path $jdkHome 'bin\java.exe')) -and (Test-Path $release)) {
            $line = Select-String -Path $release -Pattern '^JAVA_VERSION="(\d+)' | Select-Object -First 1
            if ($line -and [int]$line.Matches[0].Groups[1].Value -ge $MinJava) {
                return [pscustomobject]@{ Home = $jdkHome; Major = [int]$line.Matches[0].Groups[1].Value }
            }
        }
    }
    return $null
}

function Find-Chrome {
    $paths = @()
    foreach ($key in @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe', 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe')) {
        $item = Get-ItemProperty $key -ErrorAction SilentlyContinue
        if ($item) { $paths += $item.'(default)' }
    }
    $paths += "$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
    return $paths | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
}

function Test-DockerEngine {
    docker info *> $null
    return ($LASTEXITCODE -eq 0)
}

# Letters and digits only, from the operating system's cryptographic generator.
function New-Secret([int]$length = 32) {
    $chars = [char[]]'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    $bytes = New-Object byte[] $length
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    $rng.Dispose()
    return -join ($bytes | ForEach-Object { $chars[$_ % $chars.Length] })
}

if ($env:OS -ne 'Windows_NT') { Stop-Setup 'This script is for Windows. README.md section 5 lists the manual steps for other systems.' }
Say ('CleverCubs setup' + $(if ($CheckOnly) { ' (check only: nothing is installed, written or started)' } else { '' }))

# --- 1. Git and Git LFS (the course media is stored with Git LFS) ---------------------------------------------
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { [void](Install-WithWinget 'Git.Git' 'Git') }
if (Get-Command git -ErrorAction SilentlyContinue) {
    Record 'Git' 'OK' ((git --version) -replace 'git version ', '')
    git lfs version *> $null
    if ($LASTEXITCODE -ne 0) { [void](Install-WithWinget 'GitHub.GitLFS' 'Git LFS'); git lfs version *> $null }
    if ($LASTEXITCODE -eq 0) { Record 'Git LFS' 'OK' (((git lfs version) -split ' ')[0]) }
    else { Record 'Git LFS' 'MISSING' 'needed for the course media'; $manual.Add('Install Git LFS: winget install --id GitHub.GitLFS -e') }
} else {
    Record 'Git' 'MISSING' 'install Git'
    $manual.Add('Install Git: winget install --id Git.Git -e')
}

# --- 2. The project: next to this script, or cloned -----------------------------------------------------------
$root = $PSScriptRoot
if (-not (Test-Path (Join-Path $root 'app\pom.xml'))) {
    if (-not $CloneTo) { Stop-Setup "This script is not inside the CleverCubs project. Run it with -CloneTo <folder> to clone $RepoUrl first." }
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Stop-Setup 'Git is needed to clone the repository.' }
    if (Test-Path (Join-Path $CloneTo $ProjectInRepo)) {
        Note "Already cloned: $CloneTo"
    } elseif ($CheckOnly) {
        Stop-Setup "Check only: the repository is not cloned yet ($CloneTo)."
    } else {
        Say "Cloning $RepoUrl into $CloneTo"
        # core.longpaths: in a deep folder a repository path can pass Windows' 260-character limit.
        git -c core.longpaths=true clone $RepoUrl $CloneTo | Out-Host
        if ($LASTEXITCODE -eq 0) { git -C $CloneTo config core.longpaths true }
        if ($LASTEXITCODE -ne 0) { Stop-Setup 'git clone failed; see the output above.' }
    }
    $root = Join-Path $CloneTo $ProjectInRepo
}
$root = (Resolve-Path $root -ErrorAction Stop).Path
Record 'Project folder' 'OK' $root

# A first setup downloads about 3 GB (Docker images, the Maven cache, the JDK); later runs need little.
$drive = (Get-Item $root).PSDrive
$firstSetup = -not (Test-Path (Join-Path $root '.env'))
if (($firstSetup -and $drive.Free -lt 6GB) -or $drive.Free -lt 1GB) {
    Warn ("Only {0:N1} GB free on {1}:. A first setup needs about 6 GB (README.md section 4)." -f ($drive.Free / 1GB), $drive.Name)
}

# --- 3. Course media (Git LFS files must be real files, not pointers) ---------------------------------------
$sample = Join-Path $root 'media\alphabets\apple.png'
if (-not (Test-Path $sample)) {
    Record 'Course media' 'MISSING' 'media folder not found'
    $manual.Add('The media folder is missing: re-clone the repository with Git LFS installed.')
} elseif ((Get-Item $sample).Length -lt 1024 -and (Get-Content $sample -TotalCount 1) -like 'version https://git-lfs*') {
    if ($CheckOnly) {
        Record 'Course media' 'TO DO' 'LFS pointers only; setup will run git lfs pull'
    } else {
        Say 'Downloading the course media (git lfs pull, about 420 MB)'
        Push-Location $root
        try { git lfs install --local | Out-Null; git lfs pull | Out-Host } finally { Pop-Location }
        Record 'Course media' 'OK' 'downloaded with git lfs pull'
    }
} else {
    Record 'Course media' 'OK' 'present'
}

# --- 4. Java 25 or newer ----------------------------------------------------------------------------------------
$jdk = Find-Jdk
if (-not $jdk -and (Install-WithWinget 'EclipseAdoptium.Temurin.25.JDK' 'Eclipse Temurin JDK 25')) { $jdk = Find-Jdk }
if ($jdk) {
    $env:JAVA_HOME = $jdk.Home
    Record 'Java (JDK)' 'OK' "$($jdk.Major) at $($jdk.Home)"
} else {
    Record 'Java (JDK)' 'MISSING' "JDK $MinJava or newer"
    $manual.Add("Install a JDK $MinJava or newer: winget install --id EclipseAdoptium.Temurin.25.JDK -e")
}

# --- 5. Docker Desktop (runs MySQL for development and the test databases) ------------------------------------
if (Get-Command docker -ErrorAction SilentlyContinue) {
    $engine = Test-DockerEngine
    if (-not $engine -and -not $CheckOnly) {
        $exe = @("$env:ProgramFiles\Docker\Docker\Docker Desktop.exe", "$env:LOCALAPPDATA\Programs\DockerDesktop\Docker Desktop.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
        if ($exe) {
            Say 'Starting Docker Desktop (this can take a minute)'
            Start-Process $exe
            for ($i = 0; $i -lt 60 -and -not $engine; $i++) { Start-Sleep -Seconds 3; $engine = Test-DockerEngine }
        }
    }
    if ($engine) { Record 'Docker Desktop' 'OK' ("engine " + (docker version --format '{{.Server.Version}}' 2>$null)) }
    else { Record 'Docker Desktop' 'NOT RUNNING' 'start Docker Desktop'; $manual.Add('Start Docker Desktop and wait until it says the engine is running, then run this script again.') }
} else {
    Record 'Docker Desktop' 'MISSING' 'needs administrator rights and a restart'
    $manual.Add('Install Docker Desktop (administrator rights, WSL 2, then a restart): winget install --id Docker.DockerDesktop -e')
}

# --- 6. Chrome (opens the application; the browser tests use it too) -----------------------------------------
$chrome = Find-Chrome
if (-not $chrome -and (Install-WithWinget 'Google.Chrome' 'Google Chrome')) { $chrome = Find-Chrome }
if ($chrome) { Record 'Google Chrome' 'OK' $((Get-Item $chrome).VersionInfo.ProductVersion) }
else { Record 'Google Chrome' 'MISSING' 'the default browser is used instead'; $manual.Add('Install Google Chrome: winget install --id Google.Chrome -e') }

# --- 7. Node.js (only for the browser tests in e2e\) ------------------------------------------------------------
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node -and (Install-WithWinget 'OpenJS.NodeJS.LTS' 'Node.js LTS')) { $node = Get-Command node -ErrorAction SilentlyContinue }
if ($node -and [int]((node -v) -replace '^v(\d+).*', '$1') -ge $MinNode) {
    Record 'Node.js' 'OK' "$(node -v) (browser tests only)"
    $modules = Join-Path $root 'e2e\node_modules'
    if (Test-Path $modules) {
        Record 'Browser-test packages' 'OK' 'e2e\node_modules present'
    } elseif ($CheckOnly) {
        Record 'Browser-test packages' 'TO DO' 'setup will run npm ci in e2e\'
    } else {
        Say 'Installing the browser-test packages (npm ci in e2e\; the installed Chrome is used, no browser download)'
        npm ci --prefix (Join-Path $root 'e2e') | Out-Host
        Record 'Browser-test packages' $(if ($LASTEXITCODE -eq 0) { 'OK' } else { 'FAILED' }) 'npm ci'
    }
} else {
    Record 'Node.js' 'OPTIONAL' "Node $MinNode+ is needed only for the browser tests"
}

# --- 8. Local configuration (.env): created from .env.example; only EMPTY values are filled --------------------
$envFile = Join-Path $root '.env'
$example = Join-Path $root '.env.example'
if ($CheckOnly) {
    Record 'Local configuration' $(if (Test-Path $envFile) { 'OK' } else { 'TO DO' }) $(if (Test-Path $envFile) { '.env present' } else { 'setup will create .env' })
} else {
    if (-not (Test-Path $envFile)) { Copy-Item $example $envFile -ErrorAction Stop; Note 'Created .env from .env.example (it is gitignored).' }
    $lines = [System.IO.File]::ReadAllLines($envFile)
    $fill = [ordered]@{ CC_DB_ROOT_PASSWORD = 32; CC_DB_MIGRATOR_PASSWORD = 32; CC_DB_APP_PASSWORD = 32 }
    $filled = @()
    for ($i = 0; $i -lt $lines.Length; $i++) {
        foreach ($key in @($fill.Keys)) {
            if ($lines[$i] -match "^$key=\s*$") { $lines[$i] = "$key=$(New-Secret $fill[$key])"; $filled += $key }
        }
        if ($AdminEmail -and $lines[$i] -match '^CC_ADMIN_EMAIL=\s*$') { $lines[$i] = "CC_ADMIN_EMAIL=$AdminEmail"; $filled += 'CC_ADMIN_EMAIL' }
        if ($AdminEmail -and $lines[$i] -match '^CC_ADMIN_INITIAL_PASSWORD=\s*$') { $lines[$i] = "CC_ADMIN_INITIAL_PASSWORD=$(New-Secret 20)"; $filled += 'CC_ADMIN_INITIAL_PASSWORD' }
    }
    if ($filled.Count -gt 0) {
        # UTF-8 without a byte-order mark: docker compose and Spring both read this file.
        [System.IO.File]::WriteAllLines($envFile, $lines, (New-Object System.Text.UTF8Encoding $false))
        Record 'Local configuration' 'OK' ("filled in .env (values not shown): " + ($filled -join ', '))
        $volume = docker volume ls --quiet --filter name=clevercubs_clevercubs-mysql 2>$null
        if ($volume -and ($filled -match '^CC_DB_')) {
            Warn 'A MySQL data volume already exists and new database passwords were just generated. If the application cannot connect, reset the local database (this deletes local data): docker compose down -v'
        }
    } else {
        Record 'Local configuration' 'OK' '.env already complete; nothing changed'
    }
    if ($filled -contains 'CC_ADMIN_INITIAL_PASSWORD') {
        $manual.Add("Local Super Admin: sign in as $AdminEmail with the temporary password in .env (CC_ADMIN_INITIAL_PASSWORD), then choose your own.")
    }
}

# --- 9. Start the application and open it in Chrome ------------------------------------------------------------
$running = $false
try { $running = (Invoke-WebRequest -UseBasicParsing "$AppUrl/api/v1/public/health" -TimeoutSec 3).StatusCode -eq 200 } catch { }
$ready = ($results | Where-Object { $_.Status -in @('MISSING', 'NOT RUNNING', 'FAILED') -and $_.Item -notin @('Google Chrome', 'Browser-test packages') }).Count -eq 0
if ($CheckOnly -or $NoStart) {
    Record 'Application' $(if ($running) { 'RUNNING' } else { 'NOT STARTED' }) $(if ($CheckOnly) { 'check only' } else { '-NoStart' })
} elseif ($running) {
    Record 'Application' 'RUNNING' "already running at $AppUrl"
    if (-not $NoBrowser) { if ($chrome) { Start-Process $chrome "--new-window $AppUrl" } else { Start-Process $AppUrl } }
} elseif (-not $ready) {
    Record 'Application' 'NOT STARTED' 'fix the missing items above first'
} else {
    $startArgs = @{}
    if ($NoBrowser) { $startArgs.NoBrowser = $true }
    & (Join-Path $root 'start-dev.ps1') @startArgs
    try { $running = (Invoke-WebRequest -UseBasicParsing "$AppUrl/api/v1/public/health" -TimeoutSec 5).StatusCode -eq 200 } catch { $running = $false }
    Record 'Application' $(if ($running) { 'RUNNING' } else { 'FAILED' }) "$AppUrl (log: .tmp\app.log)"
    if (-not $running) { $manual.Add('The application did not start: read .tmp\app.log in the project folder (README.md section 11).') }
}

# --- 10. Summary ------------------------------------------------------------------------------------------------
Write-Host ''
Say 'Summary'
$results | Format-Table -AutoSize | Out-String -Width 200 | Write-Host
if ($manual.Count -gt 0) {
    Warn 'Still to do by hand:'
    $manual | ForEach-Object { Note "- $_" }
    exit 2
}
Say "Done. Production: https://clevercubs.vercel.app  |  Local: $AppUrl  |  Guide: README.md at the repository root"
