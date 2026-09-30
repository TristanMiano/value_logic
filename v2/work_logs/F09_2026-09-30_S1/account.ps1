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
    @('2026-09-30T15:35:26.055','2026-09-30T15:36:24.918','Status-patch drafting mixed into D1'),
    @('2026-09-30T15:39:42.184','2026-09-30T15:40:19.833','Executable planning mixed into D2'),
    @('2026-09-30T15:46:11.509','2026-09-30T15:48:28.224','Optional theory planning mixed into E1'),
    @('2026-09-30T16:42:12.728','2026-09-30T16:46:47.733','Context compaction and recovery; no engaged-time credit')
) | ForEach-Object { [pscustomobject]@{ start=(Find-Reading $_[0]).ticks; end=(Find-Reading $_[1]).ticks; reason=$_[2] } }
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
                task_id='F09'; attempt_id='F09-A1'; session_id='2026-09-30-S1'
                mode=$reading.mode; lane=$reading.lane; start_utc=$taskActive.utc; end_utc=$reading.utc
                elapsed_seconds=([double]$reading.ticks-[double]$taskActive.ticks)/$taskFrequency
                engaged_seconds=0.0; tool_wait_seconds=0.0; idle_seconds=0.0; unmeasured_seconds=0.0
                forecast_seconds=''; artifact='v2/work_logs/F09_2026-09-30_S1.md'
                status='closed; measured after explicit exclusions'; start_ticks=$taskActive.ticks; end_ticks=$reading.ticks
            })
            $taskActive = $null
        }
        'tool_start' {
            if ($null -ne $taskWaitActive) { throw 'Overlapping tool waits.' }
            $taskWaitActive = $reading
        }
        'tool_end' {
            if ($null -eq $taskWaitActive) { throw 'Unmatched tool end.' }
            $taskWaits.Add([pscustomobject]@{start=$taskWaitActive.ticks; end=$reading.ticks})
            $taskWaitActive = $null
        }
    }
}
foreach ($row in $taskRows) {
    foreach ($wait in $taskWaits) { $row.tool_wait_seconds += Overlap-Seconds $row.start_ticks $row.end_ticks $wait.start $wait.end }
    foreach ($excluded in $taskExclusions) { $row.unmeasured_seconds += Overlap-Seconds $row.start_ticks $row.end_ticks $excluded.start $excluded.end }
    $row.engaged_seconds = $row.elapsed_seconds-$row.tool_wait_seconds-$row.unmeasured_seconds
    if ($row.engaged_seconds -lt 0) { throw 'Exclusions overlap or exceed a segment.' }
}
# Conservative non-credit reserve for short unbracketed reads, patch calls and
# clock overhead across the session. This is unknown occupancy, not idle time.
$taskReserve = 90.0
for ($i=$taskRows.Count-1; $i -ge 0 -and $taskReserve -gt 0; $i--) {
    if ($taskRows[$i].mode -eq 'D') {
        $deduction = [Math]::Min($taskReserve,$taskRows[$i].engaged_seconds)
        $taskRows[$i].engaged_seconds -= $deduction
        $taskRows[$i].unmeasured_seconds += $deduction
        $taskRows[$i].status += '; includes conservative D overhead reserve'
        $taskReserve -= $deduction
    }
}
$taskForecast = @{D=4200; L=0; E=1500; O=720}
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
    $sum = ($taskRows | Where-Object lane -eq $lane | Measure-Object engaged_seconds -Sum).Sum
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
    task='F09'; engaged_minutes=$taskTotals; research_lane_minutes=$taskLanes
    tool_wait_minutes=[Math]::Round([double]($taskRows | Measure-Object tool_wait_seconds -Sum).Sum/60,6)
    unmeasured_within_segments_minutes=[Math]::Round($taskWithinUnknownSeconds/60,6)
    unsegmented_gap_minutes=if ($null -ne $taskGapSeconds) {[Math]::Round($taskGapSeconds/60,6)} else {$null}
    total_unmeasured_minutes=if ($null -ne $taskGapSeconds) {[Math]::Round(($taskWithinUnknownSeconds+$taskGapSeconds)/60,6)} else {$null}
    closed_segment_wall_minutes=[Math]::Round($taskClosedWallSeconds/60,6)
    observed_clock_span_minutes=[Math]::Round($taskClockSpanSeconds/60,6)
    protected_D60_met=($taskTotals.D -ge 60); short_D_overhead_reserve_seconds=90
    open_segment_mode=if ($null -ne $taskActive) {$taskActive.mode} else {$null}
    initial_orientation='unmeasured; no retrospective credit'; literature='not used'
    exclusions=$taskExclusions; closed_rows=$taskRows.Count
}
$taskActuals | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'actuals.json') -Encoding utf8NoBOM
if ($AppendLedger) {
    if ($null -ne $taskActive -or $null -ne $taskWaitActive) { throw 'Close all segments and waits before appending.' }
    if (-not $taskActuals.protected_D60_met) { throw 'D60 is not met.' }
    $taskLedger = Join-Path $taskRoot 'v2/time_ledger.csv'
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'ledger_append.json')) { throw 'This session has already appended its ledger.' }
    if (@(Import-Csv -LiteralPath $taskLedger | Where-Object task_id -eq 'F09').Count) { throw 'Existing F09 ledger rows require explicit reconciliation.' }
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
