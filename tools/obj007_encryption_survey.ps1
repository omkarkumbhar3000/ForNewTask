# obj007_encryption_survey.ps1 — classify text columns as plaintext or ciphertext
#
# PURPOSE
#   Answers the decisive OBJ-007 question: how widespread is column-level encryption in
#   ARCOSDB_U16SP2_WEBSM_QA? If the columns that identify a business record are encrypted,
#   DB validation cannot match a created object by name and the whole validation design changes.
#
# METHOD — this is INFERENCE, not a schema fact. SQL Server column-level encryption here is
#   application-side (the app encrypts before INSERT), so the catalog reports plain varchar/
#   nvarchar and gives no hint. Classification is therefore by VALUE SHAPE:
#     * ciphertext  — base64 charset only, length a multiple of 4, decodes to a whole number of
#                     16-byte AES blocks, and the decoded bytes are high-entropy / non-textual
#     * plaintext   — anything that reads as text, a number, a date, a GUID, or an email
#     * ambiguous   — short base64-looking tokens that could be either
#   Every verdict below is reported with the sampled value so a human can overrule it.
#
# SAFETY: SELECT only, TOP-capped, read-only. Inherits the deny-by-default guard in
#         obj007_db_probe.ps1 (dot-sourced).

. "$PSScriptRoot\obj007_db_probe.ps1"

function Get-ValueClass {
    <#  Classify a single sampled value by shape. Returns a label + why. #>
    param([object]$Value)

    if ($null -eq $Value)            { return @{ class = 'null';      why = 'NULL' } }
    $s = [string]$Value
    if ($s.Trim().Length -eq 0)      { return @{ class = 'empty';     why = 'empty string' } }

    # Obvious plaintext shapes, checked before the base64 test because short words like
    # "Test" are valid base64 by charset and would otherwise be misfiled.
    if ($s -match '^[0-9]+$')                        { return @{ class='plaintext'; why='all digits' } }
    if ($s -match '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-') { return @{ class='plaintext'; why='GUID' } }
    if ($s -match '^\S+@\S+\.\S+$')                  { return @{ class='plaintext'; why='email' } }
    if ($s -match '^\d{4}-\d{2}-\d{2}') { return @{ class='plaintext'; why='ISO date' } }
    if ($s -match '^\d{1,2}[/-]\d{1,2}[/-]\d{4}')    { return @{ class='plaintext'; why='date' } }
    if ($s -match '\s')                              { return @{ class='plaintext'; why='contains whitespace' } }
    if ($s -match '^(true|false|yes|no|Y|N)$')       { return @{ class='plaintext'; why='boolean-ish' } }

    $isB64Charset = $s -match '^[A-Za-z0-9+/]+={0,2}$'
    $lenOk        = ($s.Length % 4) -eq 0

    if ($isB64Charset -and $lenOk -and $s.Length -ge 16) {
        try {
            $bytes = [Convert]::FromBase64String($s)
            if (($bytes.Length % 16) -eq 0 -and $bytes.Length -ge 16) {
                # Entropy check: AES output is ~uniform. Count printable-ASCII fraction.
                $printable = 0
                foreach ($b in $bytes) { if ($b -ge 32 -and $b -le 126) { $printable++ } }
                $frac = $printable / $bytes.Length
                if ($frac -lt 0.75) {
                    return @{ class = 'ciphertext'
                              why   = "base64 -> $($bytes.Length)B = $($bytes.Length/16) AES block(s), printable frac $([math]::Round($frac,2))" }
                }
                return @{ class = 'ambiguous'
                          why   = "base64 -> $($bytes.Length)B but decodes to mostly-printable (frac $([math]::Round($frac,2)))" }
            }
            return @{ class='ambiguous'; why="base64 -> $($bytes.Length)B, not an AES block multiple" }
        } catch {
            return @{ class='plaintext'; why='base64-like charset but not decodable' }
        }
    }

    # Base64 charset but too short to be an AES block, or odd length.
    if ($isB64Charset -and $s.Length -lt 16) { return @{ class='plaintext'; why='short token, below one AES block' } }
    return @{ class='plaintext'; why='non-base64 characters present' }
}

function Invoke-ColumnSurvey {
    <#  Sample the text columns of one table and classify each. #>
    param(
        [Parameter(Mandatory=$true)][string]$Table,
        [int]$SampleRows = 4,
        [switch]$Mask
    )

    $cols = Invoke-Probe -Quiet -TimeoutSec 60 -Sql @"
SELECT c.name AS col, ty.name AS dtype
FROM sys.columns c JOIN sys.types ty ON ty.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('$Table')
  AND ty.name IN ('varchar','nvarchar','char','nchar','text','ntext')
ORDER BY c.column_id
"@
    if (-not $cols) { Write-Host "  (no text columns / table not found: $Table)"; return @() }

    $out = @()
    foreach ($c in $cols) {
        $cn = $c.col
        $vals = Invoke-Probe -Quiet -TimeoutSec 60 -Sql @"
SELECT TOP $SampleRows LEFT(CONVERT(varchar(max), [$cn]), 120) AS v
FROM [$Table] WHERE [$cn] IS NOT NULL AND LEN([$cn]) > 0
"@
        if (-not $vals -or $vals.Count -eq 0) {
            $out += [pscustomobject]@{ table=$Table; column=$cn; dtype=$c.dtype
                                       verdict='no-data'; why='all NULL/empty in sample'; sample='' }
            continue
        }
        $classes = @(); $whys = @()
        foreach ($v in $vals) { $r = Get-ValueClass $v.v; $classes += $r.class; $whys += $r.why }

        $cipher = ($classes | Where-Object { $_ -eq 'ciphertext' }).Count
        $plain  = ($classes | Where-Object { $_ -eq 'plaintext'  }).Count
        $amb    = ($classes | Where-Object { $_ -eq 'ambiguous'  }).Count
        if     ($cipher -gt 0 -and $plain -eq 0) { $verdict = 'ENCRYPTED' }
        elseif ($cipher -gt 0)                   { $verdict = 'MIXED' }
        elseif ($amb -gt 0 -and $plain -eq 0)    { $verdict = 'AMBIGUOUS' }
        else                                     { $verdict = 'PLAINTEXT' }

        $sample = [string]$vals[0].v
        if ($Mask -and $verdict -eq 'PLAINTEXT' -and $sample.Length -gt 6) {
            $sample = $sample.Substring(0, 3) + '***'      # avoid dumping live credentials
        }
        if ($sample.Length -gt 46) { $sample = $sample.Substring(0, 46) + '..' }

        $out += [pscustomobject]@{ table=$Table; column=$cn; dtype=$c.dtype
                                   verdict=$verdict; why=($whys | Select-Object -First 1); sample=$sample }
    }
    return $out
}
