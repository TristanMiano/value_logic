param([Parameter(Mandatory=$true)][string]$Script, [Parameter(Mandatory=$true)][string]$OutDir, [int]$First=0, [int]$Last=0, [string]$Python='python')
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }
foreach ($caseIndex in $First..$Last) {
    foreach ($attemptIndex in 0..2) {
        $caseName = 'c{0:d2}a{1:d1}' -f $caseIndex, $attemptIndex
        $caseOutput = "$OutDir/$caseName.json"
        $caseLog = "$OutDir/$caseName.log"
        if ((Test-Path -LiteralPath $caseOutput) -or (Test-Path -LiteralPath $caseLog)) { throw 'Preserve existing attempt.' }
        $taskTimer = [System.Diagnostics.Stopwatch]::StartNew()
        & $Python -X utf8 $Script --case $caseIndex --out $caseOutput *> $caseLog
        $caseExit = $LASTEXITCODE
        $taskTimer.Stop()
        $record = [ordered]@{ case = $caseIndex; attempt = $attemptIndex; exit_code = $caseExit; elapsed_milliseconds = $taskTimer.ElapsedMilliseconds; output = $caseOutput; log = $caseLog }
        $line = $record | ConvertTo-Json -Compress
        Add-Content -LiteralPath "$OutDir/attempts.jsonl" -Value $line -Encoding utf8
        Write-Output $line
        if ($caseExit -eq 0) { break }
    }
}
