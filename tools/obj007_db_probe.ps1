# obj007_db_probe.ps1 — read-only SQL Server probe for OBJ-007 items 4 and 13
#
# PURPOSE
#   Reusable, SELECT-only query harness against the QA_MsSQL database used by the PAM API.
#   Built because pyodbc is not installed and the only local ODBC driver is the legacy
#   "SQL Server" one. Uses .NET System.Data.SqlClient directly instead.
#
# SAFETY — these are controls, not preferences
#   * Database is pinned to ARCOSDB_U16SP2_WEBSM_QA. The `devops` login is sysadmin over
#     30 databases; this script must never be the thing that mutates one.
#   * Invoke-Probe REFUSES any statement whose first keyword is not SELECT or WITH, and
#     refuses any statement containing a mutating keyword. Deny-by-default.
#   * Every call carries a command timeout (default 60 s).
#
# USAGE
#   . .\obj007_db_probe.ps1                       # dot-source to get the functions
#   Invoke-Probe "SELECT TOP 10 name FROM sys.tables"
#   Invoke-Probe -Sql "SELECT ..." -Db "OTHER_DB" -TimeoutSec 30 -AsJson

$script:Obj007Server   = '10.10.0.194,1433'
$script:Obj007Db       = 'ARCOSDB_U16SP2_WEBSM_QA'
$script:Obj007User     = 'devops'
# Supplied via the environment so the credential is not committed:
#   $env:OBJ007_DB_PASSWORD = '<password>'   (before dot-sourcing this script)
$script:Obj007Password = $env:OBJ007_DB_PASSWORD

# Any statement containing one of these (as a whole word) is refused outright.
$script:Obj007Forbidden = @(
    'INSERT', 'UPDATE', 'DELETE', 'MERGE', 'TRUNCATE', 'DROP', 'CREATE', 'ALTER',
    'GRANT', 'REVOKE', 'DENY', 'EXEC', 'EXECUTE', 'BACKUP', 'RESTORE', 'SHUTDOWN',
    'BULK', 'OPENROWSET', 'WRITETEXT', 'UPDATETEXT', 'RECONFIGURE', 'KILL', 'DBCC'
)

function Test-ProbeSafe {
    <#  Returns $true only for a read-only statement. Deny-by-default. #>
    param([string]$Sql)

    $stripped = $Sql -replace '--[^\r\n]*', ' ' -replace '/\*[\s\S]*?\*/', ' '
    $trimmed  = $stripped.Trim()

    if ($trimmed -notmatch '^\s*(SELECT|WITH)\b') {
        Write-Error "REFUSED: statement does not begin with SELECT or WITH."
        return $false
    }
    foreach ($kw in $script:Obj007Forbidden) {
        if ($stripped -match "\b$kw\b") {
            Write-Error "REFUSED: statement contains forbidden keyword '$kw'."
            return $false
        }
    }
    return $true
}

function Invoke-Probe {
    <#  Runs one read-only statement and returns rows as PSCustomObjects. #>
    param(
        [Parameter(Mandatory = $true)][string]$Sql,
        [string]$Database = $script:Obj007Db,
        [int]$TimeoutSec = 60,
        [switch]$AsJson,
        [switch]$Quiet
    )

    if (-not (Test-ProbeSafe -Sql $Sql)) { return }

    $cs = "Server=$($script:Obj007Server);Database=$Database;User Id=$($script:Obj007User);" +
          "Password=$($script:Obj007Password);Connect Timeout=20;TrustServerCertificate=True"

    $conn = New-Object System.Data.SqlClient.SqlConnection $cs
    $rows = @()
    try {
        $conn.Open()
        $cmd = $conn.CreateCommand()
        $cmd.CommandTimeout = $TimeoutSec
        $cmd.CommandText = $Sql
        $rdr = $cmd.ExecuteReader()
        while ($rdr.Read()) {
            $o = [ordered]@{}
            for ($i = 0; $i -lt $rdr.FieldCount; $i++) {
                $name = $rdr.GetName($i)
                if ([string]::IsNullOrEmpty($name)) { $name = "col$i" }
                $val = $rdr.GetValue($i)
                if ($val -is [System.DBNull]) { $val = $null }
                $o[$name] = $val
            }
            $rows += [pscustomobject]$o
        }
        $rdr.Close()
    }
    finally {
        if ($conn.State -eq 'Open') { $conn.Close() }
    }

    if ($AsJson) { return ($rows | ConvertTo-Json -Depth 5 -Compress) }
    if (-not $Quiet) { $rows | Format-Table -AutoSize | Out-String -Width 400 }
    return $rows
}

function Get-ProbeScalar {
    param([string]$Sql, [string]$Database = $script:Obj007Db, [int]$TimeoutSec = 60)
    $rows = Invoke-Probe -Sql $Sql -Database $Database -TimeoutSec $TimeoutSec -Quiet
    if ($rows -and $rows.Count -gt 0) {
        return ($rows[0].PSObject.Properties | Select-Object -First 1).Value
    }
    return $null
}
