param([switch]$AppendLedger)
$ErrorActionPreference = 'Stop'
$taskCulture = [Globalization.CultureInfo]::InvariantCulture
$taskRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$taskEvents = @(Get-Content -LiteralPath (Join-Path $PSScriptRoot 'clocks.jsonl') | ForEach-Object { $_ | ConvertFrom-Json -DateKind String })
if (($taskEvents.host | Select-Object -Unique).Count -ne 1 -or ($taskEvents.frequency | Select-Object -Unique).Count -ne 1) { throw 'Mixed clock runtime.' }
$taskFrequency = [double]$taskEvents[0].frequency
function Find-Reading([string]$prefix) {
    $found = @($taskEvents | Where-Object { $_.utc.StartsWith($prefix) })
    if ($found.Count -ne 1) { throw "Ambiguous clock prefix: $prefix" }
    return $found[0]
}
function Overlap-Seconds($a,$b,$c,$d) {
    return [Math]::Max(0.0,([Math]::Min([double]$b,[double]$d)-[Math]::Max([double]$a,[double]$c))/$taskFrequency)
}
$taskExclusions = @(
    [pscustomobject]@{ start=(Find-Reading '2026-10-04T15:09:08.914').ticks; end=(Find-Reading '2026-10-04T15:12:58.576').ticks; reason='Conservative context compaction/recovery exclusion through resumed clock check' }
    [pscustomobject]@{ start=(Find-Reading '2026-10-04T16:03:09.574').ticks; end=(Find-Reading '2026-10-04T16:11:31.231').ticks; reason='Conservatively exclude entire O interval since last observed clock through second context recovery; research floors unaffected' }
)
$taskRows = [Collections.Generic.List[object]]::new()
$taskWaits = [Collections.Generic.List[object]]::new()
$taskActive = $null; $taskWaitActive = $null; $taskPrevious = -1
foreach ($reading in $taskEvents) {
    if ([double]$reading.ticks -lt $taskPrevious) { throw 'Clock moved backwards.' }
    $taskPrevious = [double]$reading.ticks
    switch ($reading.event) {
        'start' {
            if ($null -ne $taskActive) { throw 'Overlapping engaged segments.' }
            $taskActive = $reading
        }
        'stop' {
            if ($null -eq $taskActive -or $taskActive.mode -ne $reading.mode -or $taskActive.lane -ne $reading.lane) { throw 'Unmatched segment stop.' }
            $taskRows.Add([pscustomobject]@{
                task_id='F13'; attempt_id='R-N01-01-F13-A'; session_id='2026-10-04-S1'
                mode=$reading.mode; lane=$reading.lane; start_utc=$taskActive.utc; end_utc=$reading.utc
                elapsed_seconds=([double]$reading.ticks-[double]$taskActive.ticks)/$taskFrequency
                engaged_seconds=0.0; tool_wait_seconds=0.0; idle_seconds=0.0; unmeasured_seconds=0.0
                forecast_seconds=''; artifact='v2/work_logs/F13_2026-10-04_S1.md'
                status='closed; measured after explicit exclusions'; start_ticks=$taskActive.ticks; end_ticks=$reading.ticks
            })
            $taskActive = $null
        }
        'wait_start' {
            if ($null -ne $taskWaitActive) { throw 'Overlapping tool waits.' }
            $taskWaitActive = $reading
        }
        'wait_end' {
            if ($null -eq $taskWaitActive) { throw 'Unmatched tool end.' }
            $taskWaits.Add([pscustomobject]@{start=$taskWaitActive.ticks; end=$reading.ticks})
            $taskWaitActive = $null
        }
    }
}
# Preserve raw clocks while correcting a batched mode-change call whose code
# argument was drafted before it executed. The two endpoints were observed;
# this interval counts as E/X, never toward the protected D floor.
$taskCorrectionStart = Find-Reading '2026-10-04T15:53:40.414'
$taskCorrectionEnd = Find-Reading '2026-10-04T15:55:16.136'
$taskCorrectionApplied = $false
for ($i=0; $i -lt $taskRows.Count; $i++) {
    $row = $taskRows[$i]
    if ($row.mode -eq 'D' -and $row.start_ticks -lt $taskCorrectionStart.ticks -and $row.end_ticks -eq $taskCorrectionEnd.ticks) {
        $taskCodeRow = $row.PSObject.Copy()
        $taskCodeRow.mode = 'E'; $taskCodeRow.lane = 'X'
        $taskCodeRow.start_utc = $taskCorrectionStart.utc; $taskCodeRow.start_ticks = $taskCorrectionStart.ticks
        $taskCodeRow.elapsed_seconds = ([double]$taskCodeRow.end_ticks-[double]$taskCodeRow.start_ticks)/$taskFrequency
        $taskCodeRow.status += '; corrected observed code-drafting interval from D to E/X'
        $row.end_utc = $taskCorrectionStart.utc; $row.end_ticks = $taskCorrectionStart.ticks
        $row.elapsed_seconds = ([double]$row.end_ticks-[double]$row.start_ticks)/$taskFrequency
        $row.status += '; shortened by recorded code-drafting classification correction'
        $taskRows.Insert($i+1,$taskCodeRow)
        $taskCorrectionApplied = $true
        break
    }
}
if (-not $taskCorrectionApplied) { throw 'Expected observed mode correction could not be applied.' }
foreach ($row in $taskRows) {
    foreach ($wait in $taskWaits) { $row.tool_wait_seconds += Overlap-Seconds $row.start_ticks $row.end_ticks $wait.start $wait.end }
    foreach ($excluded in $taskExclusions) { $row.unmeasured_seconds += Overlap-Seconds $row.start_ticks $row.end_ticks $excluded.start $excluded.end }
    $row.engaged_seconds = $row.elapsed_seconds-$row.tool_wait_seconds-$row.unmeasured_seconds
    if ($row.engaged_seconds -lt 0) { throw 'Exclusions overlap or exceed a segment.' }
}
# Conservative non-credit reserve for short unbracketed reads, patch calls and
# clock overhead across the session. This is unknown occupancy, not idle time.
foreach ($reserveMode in @('D','L','E','O')) {
    $taskReserve = switch ($reserveMode) { 'D' {60.0} 'L' {30.0} 'E' {120.0} 'O' {30.0} default {0.0} }
    for ($i=$taskRows.Count-1; $i -ge 0 -and $taskReserve -gt 0; $i--) {
        if ($taskRows[$i].mode -eq $reserveMode) {
            $deduction = [Math]::Min($taskReserve,$taskRows[$i].engaged_seconds)
            $taskRows[$i].engaged_seconds -= $deduction
            $taskRows[$i].unmeasured_seconds += $deduction
            $taskRows[$i].status += "; includes conservative $reserveMode overhead reserve"
            $taskReserve -= $deduction
        }
    }
}
$taskForecast = @{D=3600; L=600; E=1200; O=600}
foreach ($mode in @('D','L','E','O')) {
    $first = $taskRows | Where-Object mode -eq $mode | Select-Object -First 1
    if ($null -ne $first) { $first.forecast_seconds = $taskForecast[$mode] }
}
$taskTotals = [ordered]@{}
foreach ($mode in @('D','L','E','O')) {
    $sum = ($taskRows | Where-Object mode -eq $mode | Measure-Object engaged_seconds -Sum).Sum
    $taskTotals[$mode] = [Math]::Round([double]$sum/60,6)
}
$taskLanes = [ordered]@{}
foreach ($lane in @('R','X')) {
    $sum = ($taskRows | Where-Object { $_.lane -eq $lane -and $_.mode -ne 'O' } | Measure-Object engaged_seconds -Sum).Sum
    $taskLanes[$lane] = [Math]::Round([double]$sum/60,6)
}
$taskFields = @('task_id','attempt_id','session_id','mode','lane','start_utc','end_utc','elapsed_seconds','engaged_seconds','tool_wait_seconds','idle_seconds','unmeasured_seconds','forecast_seconds','artifact','status')
$taskClosedWallSeconds = [double]($taskRows | Measure-Object elapsed_seconds -Sum).Sum
$taskClockSpanSeconds = ([double]$taskEvents[-1].ticks-[double]$taskEvents[0].ticks)/$taskFrequency
$taskGapSeconds = if ($null -eq $taskActive) { [Math]::Max(0.0,$taskClockSpanSeconds-$taskClosedWallSeconds) } else { $null }
$taskWithinUnknownSeconds = [double]($taskRows | Measure-Object unmeasured_seconds -Sum).Sum
$taskCsvRows = foreach ($row in $taskRows) {
    $copy = [ordered]@{}
    foreach ($field in $taskFields) {
        $copy[$field] = if ($field -match '^(elapsed|engaged|tool_wait|idle|unmeasured)_seconds$') { ([double]$row.$field).ToString('F7',$taskCulture) } else { $row.$field }
    }
    [pscustomobject]$copy
}
$taskCsvRows | Export-Csv -LiteralPath (Join-Path $PSScriptRoot 'segments.csv') -NoTypeInformation -Encoding utf8NoBOM
$taskActuals = [ordered]@{
    task='F13'; engaged_minutes=$taskTotals; research_lane_minutes=$taskLanes
    tool_wait_minutes=[Math]::Round([double]($taskRows | Measure-Object tool_wait_seconds -Sum).Sum/60,6)
    unmeasured_within_segments_minutes=[Math]::Round($taskWithinUnknownSeconds/60,6)
    unsegmented_gap_minutes=if ($null -ne $taskGapSeconds) {[Math]::Round($taskGapSeconds/60,6)} else {$null}
    total_unmeasured_minutes=if ($null -ne $taskGapSeconds) {[Math]::Round(($taskWithinUnknownSeconds+$taskGapSeconds)/60,6)} else {$null}
    closed_segment_wall_minutes=[Math]::Round($taskClosedWallSeconds/60,6)
    observed_clock_span_minutes=[Math]::Round($taskClockSpanSeconds/60,6)
    protected_minimum='D60 within D+L+E90'; short_D_overhead_reserve_seconds=60; short_L_overhead_reserve_seconds=30; short_E_overhead_reserve_seconds=120; short_O_overhead_reserve_seconds=30
    open_segment_mode=if ($null -ne $taskActive) {$taskActive.mode} else {$null}
    initial_orientation='unmeasured; no retrospective credit'; literature='focused primary-source comparisons; access and locators in literature/05_f13_case_comparison.md'; final_delivery='post-final-accounting documentation and commit handling unmeasured'
    exclusions=$taskExclusions; closed_rows=$taskRows.Count
    mode_correction=[ordered]@{start=$taskCorrectionStart.utc; end=$taskCorrectionEnd.utc; from='D/R'; to='E/X'; reason='Code drafted before a batched mode-change call executed; raw readings preserved'}
}
$taskEngagedTotal = [Math]::Round([double]($taskTotals.Values | Measure-Object -Sum).Sum,6)
$taskPackageTotal = [Math]::Round(367.344527+$taskEngagedTotal,6)
$taskActuals.total_engaged_minutes = $taskEngagedTotal
$taskActuals.total_research_minutes = [Math]::Round($taskTotals.D+$taskTotals.L+$taskTotals.E,6)
$taskActuals.protected_floor_met = ($taskTotals.D -ge 60 -and $taskActuals.total_research_minutes -ge 90)
$taskActuals.package_before_minutes = 367.344527
$taskActuals.package_after_minutes = $taskPackageTotal
$taskActuals.four_hour_overshoot_minutes = [Math]::Round($taskPackageTotal-240,6)
$taskActuals.remaining_to_eight_hours_minutes = [Math]::Round(480-$taskPackageTotal,6)
$taskActuals.forecast_error_vs_central_100_minutes = [Math]::Round($taskEngagedTotal-100,6)
$taskActuals.c4_central_package_close_minutes = [Math]::Round($taskPackageTotal+70,6)
$taskActuals.c4_high_package_close_minutes = [Math]::Round($taskPackageTotal+105,6)
$taskActuals | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'actuals.json') -Encoding utf8NoBOM
if ($AppendLedger) {
    if ($taskTotals.D -lt 60 -or ($taskTotals.D+$taskTotals.L+$taskTotals.E) -lt 90) { throw 'F13 protected D60/research90 is not met.' }
    if ($null -ne $taskActive -or $null -ne $taskWaitActive) { throw 'Close all segments and waits before appending.' }
    $taskLedger = Join-Path $taskRoot 'v2/time_ledger.csv'
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'ledger_append.json')) { throw 'This session has already appended its ledger.' }
    if (@(Import-Csv -LiteralPath $taskLedger | Where-Object { $_.attempt_id -eq 'R-N01-01-F13-A' -and $_.session_id -eq '2026-10-04-S1' }).Count) { throw 'Existing recurrence session rows require explicit reconciliation.' }
    $taskBefore = [IO.File]::ReadAllBytes($taskLedger)
    $taskBeforeHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($taskBefore))
    $taskLines = @($taskCsvRows | ConvertTo-Csv -NoTypeInformation)
    [IO.File]::AppendAllText($taskLedger,($taskLines[1..($taskLines.Count-1)] -join "`n")+"`n",[Text.UTF8Encoding]::new($false))
    $taskAfter = [IO.File]::ReadAllBytes($taskLedger)
    $taskPrefix = [byte[]]::new($taskBefore.Length)
    [Array]::Copy($taskAfter,$taskPrefix,$taskBefore.Length)
    if ([Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($taskPrefix)) -ne $taskBeforeHash) { throw 'Historical ledger prefix changed.' }
    [ordered]@{before_bytes=$taskBefore.Length; before_sha256=$taskBeforeHash; after_bytes=$taskAfter.Length; appended_rows=$taskRows.Count; historical_prefix_preserved=$true} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'ledger_append.json') -Encoding utf8NoBOM
}
$taskActuals | ConvertTo-Json -Depth 6
