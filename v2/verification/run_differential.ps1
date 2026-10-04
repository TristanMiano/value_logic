param([Parameter(Mandatory=$true)][string]$OutputDirectory,
      [ValidateSet('grid','rational','boundary','offgrid','all')][string]$Family='all',
      [ValidateRange(1,100)][int]$ShardSize=100,
      [ValidateRange(1,3)][int]$MaxAttempts=3)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'report_validation.ps1')
$taskRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$taskOutput = [IO.Path]::GetFullPath($OutputDirectory,(Get-Location).Path)
New-Item -ItemType Directory -Path $taskOutput -Force | Out-Null
$taskPython = (Get-Command python).Source
$taskCounts = [ordered]@{grid=900; rational=257; boundary=9; offgrid=4}
$taskManifest = Join-Path $taskOutput 'manifest.json'
if (Test-Path -LiteralPath $taskManifest) { throw 'Choose a fresh output directory; prior attempts must be retained.' }
$taskFiles = @('model.py','native.py','producer.py','reference.py','ordinary.py','receipts.py','workloads.py','differential.py')
$taskHashes = [ordered]@{}
foreach ($taskName in $taskFiles) {
    $taskHashes["v2/verification/$taskName"] = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $taskName) -Algorithm SHA256).Hash
}
Get-ChildItem (Join-Path $taskRoot 'v2/checks') -File -Filter '*.py' | Sort-Object Name | ForEach-Object {
    $taskHashes["v2/checks/$($_.Name)"] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
}
$taskUnits = [Collections.Generic.List[object]]::new()
foreach ($taskFamily in $taskCounts.Keys) {
    if ($Family -ne 'all' -and $Family -ne $taskFamily) { continue }
    for ($taskStart=0; $taskStart -lt $taskCounts[$taskFamily]; $taskStart+=$ShardSize) {
        $taskStop = [Math]::Min($taskStart+$ShardSize,$taskCounts[$taskFamily])
        $taskUnit = [ordered]@{family=$taskFamily; start=$taskStart; stop=$taskStop; status='INCOMPLETE'; attempts=@()}
        for ($taskAttempt=1; $taskAttempt -le $MaxAttempts; $taskAttempt++) {
            $taskStem = '{0}_{1:D4}_{2:D4}_attempt{3}' -f $taskFamily,$taskStart,$taskStop,$taskAttempt
            $taskReport = Join-Path $taskOutput ($taskStem+'.json')
            $taskInfo = [Diagnostics.ProcessStartInfo]::new()
            $taskInfo.FileName=$taskPython; $taskInfo.WorkingDirectory=$taskRoot
            $taskInfo.UseShellExecute=$false; $taskInfo.CreateNoWindow=$true
            $taskInfo.RedirectStandardOutput=$true; $taskInfo.RedirectStandardError=$true
            $taskArguments=@('-X','faulthandler','-m','v2.verification.differential','--family',$taskFamily,'--start',"$taskStart",'--stop',"$taskStop",'--json',$taskReport)
            foreach ($taskArgument in $taskArguments) { $taskInfo.ArgumentList.Add($taskArgument) }
            $taskStarted=[DateTime]::UtcNow
            $taskWatch=[Diagnostics.Stopwatch]::StartNew()
            $taskProcess=[Diagnostics.Process]::Start($taskInfo)
            $taskStdout=$taskProcess.StandardOutput.ReadToEndAsync()
            $taskStderr=$taskProcess.StandardError.ReadToEndAsync()
            $taskTimedOut = -not $taskProcess.WaitForExit(120000)
            if ($taskTimedOut) { $taskProcess.Kill($true); $taskProcess.WaitForExit() }
            $taskWatch.Stop()
            [IO.File]::WriteAllText((Join-Path $taskOutput ($taskStem+'.stdout.txt')),$taskStdout.GetAwaiter().GetResult(),[Text.UTF8Encoding]::new($false))
            [IO.File]::WriteAllText((Join-Path $taskOutput ($taskStem+'.stderr.txt')),$taskStderr.GetAwaiter().GetResult(),[Text.UTF8Encoding]::new($false))
            $taskValid=$false
            $taskReportError=$null
            if ($taskProcess.ExitCode -eq 0 -and -not $taskTimedOut -and (Test-Path -LiteralPath $taskReport)) {
                $taskValidation=Test-F12Report -Path $taskReport -Expected @{status='PASS'; family=$taskFamily; start=$taskStart; stop=$taskStop; queries=3*($taskStop-$taskStart)}
                $taskValid=$taskValidation.valid
                $taskReportError=$taskValidation.error
            }
            $taskUnit.attempts += [ordered]@{number=$taskAttempt; command=@($taskPython)+$taskArguments; start_utc=$taskStarted.ToString('o'); end_utc=[DateTime]::UtcNow.ToString('o'); process_elapsed_seconds=$taskWatch.Elapsed.TotalSeconds; exit_code=$taskProcess.ExitCode; timed_out=$taskTimedOut; valid_report=$taskValid; report_error=$taskReportError; report=[IO.Path]::GetFileName($taskReport)}
            Write-Output "$taskStem exit=$($taskProcess.ExitCode) valid_report=$taskValid"
            if ($taskValid) { $taskUnit.status='PASS'; break }
        }
        $taskUnits.Add($taskUnit)
        [ordered]@{schema='F12-differential-manifest-v1'; family=$Family; shard_size=$ShardSize; max_attempts=$MaxAttempts; source_sha256=$taskHashes; units=$taskUnits.ToArray(); complete=$false} |
            ConvertTo-Json -Depth 15 | Set-Content -LiteralPath $taskManifest -Encoding utf8NoBOM
    }
}
$taskPassed=@($taskUnits | Where-Object { $_.status -eq 'PASS' })
$taskAll=($taskPassed.Count -eq $taskUnits.Count)
[ordered]@{schema='F12-differential-manifest-v1'; family=$Family; shard_size=$ShardSize; max_attempts=$MaxAttempts; source_sha256=$taskHashes; units=$taskUnits.ToArray(); complete=$taskAll; passed_sources=($taskPassed | ForEach-Object {$_.stop-$_.start} | Measure-Object -Sum).Sum} |
    ConvertTo-Json -Depth 15 | Set-Content -LiteralPath $taskManifest -Encoding utf8NoBOM
if (-not $taskAll) { exit 1 }
