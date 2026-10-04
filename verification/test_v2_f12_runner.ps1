param([Parameter(Mandatory=$true)][string]$EvidenceDirectory)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../v2/verification/report_validation.ps1')
$taskExpected=@{status='PASS'; family='grid'; queries=3}
$taskFixtures=@(
    @('{"status":"PASS","family":"grid","queries":3}', $true),
    @('{"status":"PASS","family":"grid","queries":3,', $false),
    @('null', $false),
    @('[]', $false),
    @('"PASS"', $false),
    @('{"status":"PASS","family":"grid","queries":"3"}', $false),
    @('{"status":"PASS","family":"grid","queries":true}', $false),
    @('{"status":"PASS","family":"grid","queries":3.0}', $false),
    @('{"status":"PASS","family":"grid"}', $false),
    @('{"status":"pass","family":"grid","queries":3}', $false),
    @('{"status":"PASS","family":"rational","queries":3}', $false)
)
$taskFile=[IO.Path]::GetTempFileName()
try {
    foreach($taskFixture in $taskFixtures) {
        [IO.File]::WriteAllText($taskFile,$taskFixture[0])
        $taskResult=Test-F12Report -Path $taskFile -Expected $taskExpected
        if($taskResult.valid -ne $taskFixture[1]){throw "Unexpected fixture classification: $($taskFixture[0])"}
        if(-not $taskResult.valid -and [string]::IsNullOrEmpty($taskResult.error)){throw 'Rejection lost its reason.'}
    }
} finally {
    Remove-Item -LiteralPath $taskFile
}
$taskMissing=Test-F12Report -Path $taskFile -Expected $taskExpected
if($taskMissing.valid -or [string]::IsNullOrEmpty($taskMissing.error)){throw 'Missing report must be a recorded failure.'}
$taskCount=0
foreach($taskStudy in @('differential','cost','optional_cost','long_cost')) {
    $taskDirectory=Join-Path $EvidenceDirectory $taskStudy
    $taskManifest=Get-Content -LiteralPath (Join-Path $taskDirectory 'manifest.json') -Raw | ConvertFrom-Json
    foreach($taskUnit in $taskManifest.units) {
        $taskAttempt=$taskUnit.attempts | Where-Object {$_.valid_report -and $_.exit_code -eq 0 -and -not $_.timed_out} | Select-Object -Last 1
        if($null -eq $taskAttempt){throw 'This validation expects completed evidence.'}
        if($taskStudy -eq 'differential') {
            $taskExpected=@{status='PASS'; family=$taskUnit.family; start=$taskUnit.start; stop=$taskUnit.stop; queries=3*($taskUnit.stop-$taskUnit.start)}
        } else {
            $taskCycles=if($null -eq $taskManifest.cycles){1}else{$taskManifest.cycles}
            $taskExpected=@{schema='F12-sequence-cost-v1'; status='PASS'; sequence=$taskUnit.sequence; strategy=$taskUnit.strategy; cycles=$taskCycles; queries=18*$taskCycles}
        }
        $taskResult=Test-F12Report -Path (Join-Path $taskDirectory $taskAttempt.report) -Expected $taskExpected
        if(-not $taskResult.valid){throw "Rejected saved report $($taskAttempt.report): $($taskResult.error)"}
        $taskCount++
    }
}
[ordered]@{status='PASS'; synthetic_cases=$taskFixtures.Count+1; saved_reports=$taskCount} | ConvertTo-Json
