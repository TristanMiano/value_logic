$ErrorActionPreference = 'Stop'
$taskPython = 'C:\Users\trist\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$taskDirectory = 'v3/discovery/s11/qf01'
if (Test-Path -LiteralPath $taskDirectory) { throw 'Preserve existing run; inspect before retrying.' }
New-Item -ItemType Directory -Path $taskDirectory | Out-Null
foreach ($caseIndex in 1..11) {
    $caseName = 'c{0:d2}' -f $caseIndex
    $caseOutput = "$taskDirectory/$caseName.json"
    $caseLog = "$taskDirectory/$caseName.log"
    $taskTimer = [System.Diagnostics.Stopwatch]::StartNew()
    & $taskPython -X utf8 v3/discovery/s11/query_flip.py --case $caseIndex --out $caseOutput *> $caseLog
    $caseExit = $LASTEXITCODE
    $taskTimer.Stop()
    $record = [ordered]@{ case = $caseIndex; exit_code = $caseExit; elapsed_milliseconds = $taskTimer.ElapsedMilliseconds; output = $caseOutput; log = $caseLog }
    $line = $record | ConvertTo-Json -Compress
    Add-Content -LiteralPath "$taskDirectory/attempts.jsonl" -Value $line -Encoding utf8
    Write-Output $line
}
