param([Parameter(Mandatory=$true)][string]$OutputDirectory,
      [ValidateSet('original','optional')][string]$Experiment='original',
      [ValidateRange(1,3)][int]$Repetitions=3,
      [ValidateRange(1,4)][int]$Cycles=1,
      [ValidateRange(1,3)][int]$MaxAttempts=3)
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$taskOutput=[IO.Path]::GetFullPath($OutputDirectory,(Get-Location).Path)
New-Item -ItemType Directory -Path $taskOutput -Force | Out-Null
$taskManifest=Join-Path $taskOutput 'manifest.json'
if (Test-Path -LiteralPath $taskManifest) { throw 'Choose a fresh output directory to preserve all prior attempts.' }
$taskPython=(Get-Command python).Source
$taskStrategies=@('fresh','catalogue','reuse','reuse-fallback')
$taskModule='v2.verification.sequence_cost'
if ($Experiment -eq 'optional') {
    $taskStrategies=@('fresh','catalogue','anchored-reuse','selected-fresh')
    $taskModule='v2.verification.optional_cost'
}
$taskSequences=@('fixed-directions','withdrawals','stable-revisions')
$taskHashes=[ordered]@{}
Get-ChildItem $PSScriptRoot,(Join-Path $taskRoot 'v2/checks') -File -Filter '*.py' | Sort-Object FullName | ForEach-Object {
    $taskHashes[[IO.Path]::GetRelativePath($taskRoot,$_.FullName)]=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
}
$taskUnits=[Collections.Generic.List[object]]::new()
for ($taskRepeat=0; $taskRepeat -lt $Repetitions; $taskRepeat++) {
    foreach ($taskSequence in $taskSequences) {
        for ($taskOrder=0; $taskOrder -lt $taskStrategies.Count; $taskOrder++) {
            $taskStrategy=$taskStrategies[($taskOrder+$taskRepeat)%$taskStrategies.Count]
            $taskUnit=[ordered]@{sequence=$taskSequence; strategy=$taskStrategy; repetition=$taskRepeat+1; order=$taskOrder; status='INCOMPLETE'; attempts=@()}
            for ($taskAttempt=1; $taskAttempt -le $MaxAttempts; $taskAttempt++) {
                $taskStem='{0}_{1}_rep{2}_attempt{3}' -f $taskSequence,$taskStrategy,($taskRepeat+1),$taskAttempt
                $taskReport=Join-Path $taskOutput ($taskStem+'.json')
                $taskInfo=[Diagnostics.ProcessStartInfo]::new()
                $taskInfo.FileName=$taskPython; $taskInfo.WorkingDirectory=$taskRoot
                $taskInfo.UseShellExecute=$false; $taskInfo.CreateNoWindow=$true
                $taskInfo.RedirectStandardOutput=$true; $taskInfo.RedirectStandardError=$true
                $taskArguments=@('-X','faulthandler','-m',$taskModule,'--strategy',$taskStrategy,'--sequence',$taskSequence,'--cycles',"$Cycles",'--json',$taskReport)
                foreach ($taskArgument in $taskArguments) { $taskInfo.ArgumentList.Add($taskArgument) }
                $taskStarted=[DateTime]::UtcNow
                $taskWatch=[Diagnostics.Stopwatch]::StartNew()
                $taskProcess=[Diagnostics.Process]::Start($taskInfo)
                $taskStdout=$taskProcess.StandardOutput.ReadToEndAsync(); $taskStderr=$taskProcess.StandardError.ReadToEndAsync()
                $taskTimedOut=-not $taskProcess.WaitForExit(120000)
                if ($taskTimedOut) { $taskProcess.Kill($true); $taskProcess.WaitForExit() }
                $taskWatch.Stop()
                [IO.File]::WriteAllText((Join-Path $taskOutput ($taskStem+'.stdout.txt')),$taskStdout.GetAwaiter().GetResult(),[Text.UTF8Encoding]::new($false))
                [IO.File]::WriteAllText((Join-Path $taskOutput ($taskStem+'.stderr.txt')),$taskStderr.GetAwaiter().GetResult(),[Text.UTF8Encoding]::new($false))
                $taskValid=$false
                if ($taskProcess.ExitCode -eq 0 -and -not $taskTimedOut -and (Test-Path -LiteralPath $taskReport)) {
                    $taskResult=Get-Content -LiteralPath $taskReport -Raw | ConvertFrom-Json
                    $taskValid=($taskResult.schema -eq 'F12-sequence-cost-v1' -and $taskResult.status -eq 'PASS' -and $taskResult.sequence -eq $taskSequence -and $taskResult.strategy -eq $taskStrategy -and $taskResult.cycles -eq $Cycles -and $taskResult.queries -eq 18*$Cycles)
                }
                $taskUnit.attempts += [ordered]@{number=$taskAttempt; command=@($taskPython)+$taskArguments; start_utc=$taskStarted.ToString('o'); end_utc=[DateTime]::UtcNow.ToString('o'); process_elapsed_seconds=$taskWatch.Elapsed.TotalSeconds; exit_code=$taskProcess.ExitCode; timed_out=$taskTimedOut; valid_report=$taskValid; report=[IO.Path]::GetFileName($taskReport)}
                Write-Output "$taskStem exit=$($taskProcess.ExitCode) valid_report=$taskValid"
                if ($taskValid) { $taskUnit.status='PASS'; break }
            }
            $taskUnits.Add($taskUnit)
            [ordered]@{schema='F12-cost-manifest-v1'; experiment=$Experiment; cycles=$Cycles; repetitions=$Repetitions; max_attempts=$MaxAttempts; source_sha256=$taskHashes; units=$taskUnits.ToArray(); complete=$false} |
                ConvertTo-Json -Depth 15 | Set-Content -LiteralPath $taskManifest -Encoding utf8NoBOM
        }
    }
}
$taskAll=(@($taskUnits | Where-Object { $_.status -ne 'PASS' }).Count -eq 0)
[ordered]@{schema='F12-cost-manifest-v1'; experiment=$Experiment; cycles=$Cycles; repetitions=$Repetitions; max_attempts=$MaxAttempts; source_sha256=$taskHashes; units=$taskUnits.ToArray(); complete=$taskAll} |
    ConvertTo-Json -Depth 15 | Set-Content -LiteralPath $taskManifest -Encoding utf8NoBOM
if (-not $taskAll) { exit 1 }
