$ErrorActionPreference = 'Stop'
$taskPython = 'C:\Users\trist\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$taskDirectory = 'v3/discovery/s11/rf01'
foreach ($caseIndex in 1..8) {
    foreach ($attemptIndex in 0..2) {
        $caseName = 'c{0:d2}a{1:d1}' -f $caseIndex, $attemptIndex
        $caseOutput = "$taskDirectory/$caseName.json"
        $caseLog = "$taskDirectory/$caseName.log"
        if ((Test-Path -LiteralPath $caseOutput) -or (Test-Path -LiteralPath $caseLog)) { throw 'Preserve existing attempt.' }
        $taskTimer = [System.Diagnostics.Stopwatch]::StartNew()
        & $taskPython -X utf8 v3/discovery/s11/robust_flip.py --case $caseIndex --out $caseOutput *> $caseLog
        $caseExit = $LASTEXITCODE
        $taskTimer.Stop()
        $record = [ordered]@{ case = $caseIndex; attempt = $attemptIndex; exit_code = $caseExit; elapsed_milliseconds = $taskTimer.ElapsedMilliseconds; output = $caseOutput; log = $caseLog }
        $line = $record | ConvertTo-Json -Compress
        Add-Content -LiteralPath "$taskDirectory/attempts.jsonl" -Value $line -Encoding utf8
        Write-Output $line
        if ($caseExit -eq 0) { break }
    }
}
