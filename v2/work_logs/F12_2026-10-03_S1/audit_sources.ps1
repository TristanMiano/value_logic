# Read-only provenance audit. Does not modify the preserved experiment manifests.
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$taskRecords=[Collections.Generic.List[object]]::new()
foreach ($taskStudy in @('differential','cost','optional_cost','long_cost')) {
    $taskManifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot "$taskStudy/manifest.json") -Raw | ConvertFrom-Json
    foreach ($taskProperty in $taskManifest.source_sha256.psobject.Properties) {
        $taskPath=$taskProperty.Name
        $taskNormalized=$taskPath.Replace('\','/')
        $taskCurrent=Join-Path $taskRoot $taskPath
        $taskCurrentHash=if(Test-Path -LiteralPath $taskCurrent){(Get-FileHash -LiteralPath $taskCurrent -Algorithm SHA256).Hash}else{$null}
        $taskStatus=if($taskCurrentHash -eq $taskProperty.Value){'CURRENT_MATCH'}else{'CHANGED'}
        $taskSnapshot=$null
        if($taskStudy -eq 'cost' -and $taskNormalized -eq 'v2/verification/sequence_cost.py'){$taskSnapshot='sequence_cost_v1.py'}
        if($taskStudy -eq 'optional_cost' -and $taskNormalized -eq 'v2/verification/optional_cost.py'){$taskSnapshot='optional_cost_v2.py'}
        $taskSnapshotHash=if($null -ne $taskSnapshot){(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $taskSnapshot) -Algorithm SHA256).Hash}else{$null}
        if($taskSnapshotHash -eq $taskProperty.Value){$taskStatus='SNAPSHOT_MATCH'}
        $taskRecords.Add([pscustomobject]@{study=$taskStudy; path=$taskPath; recorded_sha256=$taskProperty.Value;
            current_sha256=$taskCurrentHash; snapshot=$taskSnapshot; snapshot_sha256=$taskSnapshotHash; status=$taskStatus})
    }
}
$taskChanged=@($taskRecords | Where-Object status -eq 'CHANGED')
$taskResult=[ordered]@{
    status='READ_BACK_COMPLETE'; recorded_file_entries=$taskRecords.Count
    current_matches=@($taskRecords | Where-Object status -eq 'CURRENT_MATCH').Count
    snapshot_matches=@($taskRecords | Where-Object status -eq 'SNAPSHOT_MATCH').Count
    changed_entries=$taskChanged
    interpretation='Each manifest hashes Python files present at collection, including utilities it does not execute. Changed entries require inspection; this audit does not equate a file hash with execution or proof correctness. Original sequence implementation and optional CLI snapshots preserve the executed changes.'
    entries=$taskRecords.ToArray()
}
$taskResult | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'source_audit.json') -Encoding utf8NoBOM
[pscustomobject]$taskResult | Select-Object status,recorded_file_entries,current_matches,snapshot_matches,changed_entries | ConvertTo-Json -Depth 6
