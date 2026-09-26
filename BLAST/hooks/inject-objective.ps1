# inject-objective.ps1 - UserPromptSubmit hook: put BLAST/Objective.md into context on every prompt.
#
# Wired in .claude/settings.json. This is the ONE live path for the objective (no @-import in
# CLAUDE.md, which would go stale after session start while this stays current).
#
# - Finds the workspace root by marker (CLAUDE.md + .claude/), never by counting parents.
# - Never fails silently: a missing, unreadable or oversized objective still produces a visible
#   warning in context, because a hook that prints nothing looks exactly like a healthy one.
#
# Verify by running it and checking that it prints one JSON object:
#   powershell.exe -NoProfile -ExecutionPolicy Bypass -File BLAST\hooks\inject-objective.ps1

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

$MaxChars = 10000   # above this, hook output may reach context only as a truncated preview

function Find-Root([string]$start) {
    $dir = Get-Item -LiteralPath $start
    while ($null -ne $dir) {
        $hasFile = Test-Path -LiteralPath (Join-Path $dir.FullName 'CLAUDE.md') -PathType Leaf
        $hasDir = Test-Path -LiteralPath (Join-Path $dir.FullName '.claude') -PathType Container
        if ($hasFile -and $hasDir) { return $dir.FullName }
        $dir = $dir.Parent
    }
    return $null
}

$rule = @'
[BLAST objective-first rule - auto-injected by BLAST/hooks/inject-objective.ps1]
For every substantive CLI instruction (build, analyse, fix, run, produce): FIRST archive the outgoing
objective to docs/history, THEN write the instruction into BLAST/Objective.md, read it back, ask genuine
ambiguities as multiple-choice questions, fold the answers in, and only then do the work, using the
updated file as the governing context. A correction amends the current instruction. Questions,
conversational replies and process/config changes do not rewrite the file.
Current contents of BLAST/Objective.md follow.
'@

try {
    $root = Find-Root $PSScriptRoot
    if (-not $root) {
        $body = "WARNING: workspace root not found above $PSScriptRoot (no directory holds both CLAUDE.md and .claude/). The objective was NOT loaded."
    }
    else {
        $objective = Join-Path $root 'BLAST\Objective.md'
        if (-not (Test-Path -LiteralPath $objective -PathType Leaf)) {
            $body = "WARNING: $objective does not exist. The objective was NOT loaded; read or recreate it before working."
        }
        else {
            $text = [System.IO.File]::ReadAllText($objective, [System.Text.Encoding]::UTF8)
            $body = "$rule`n`n$text"
            if ($body.Length -gt $MaxChars) {
                $body = "WARNING: BLAST/Objective.md is $($text.Length) characters; keep it under about $MaxChars or only a preview may reach context. Move history to docs/history.`n`n$body"
            }
        }
    }
}
catch {
    $body = "WARNING: inject-objective.ps1 failed: $($_.Exception.Message). The objective was NOT loaded; read BLAST/Objective.md directly."
}

$envelope = @{ hookSpecificOutput = @{ hookEventName = 'UserPromptSubmit'; additionalContext = $body } }
[Console]::Out.Write(($envelope | ConvertTo-Json -Compress -Depth 5))
exit 0
