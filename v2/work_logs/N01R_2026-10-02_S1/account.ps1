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
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T02:16:57.964').ticks; end=(Find-Reading '2026-10-03T02:20:10.828').ticks; reason='Unclocked derivation in literature segment; no retrospective mode credit' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T02:23:05.409').ticks; end=(Find-Reading '2026-10-03T02:24:51.236').ticks; reason='Mixed mathematical design and administration in literature segment; excluded' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T02:32:29.477').ticks; end=(Find-Reading '2026-10-03T02:32:59.205').ticks; reason='Unclocked timing administration; excluded' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T02:44:16.747').ticks; end=(Find-Reading '2026-10-03T02:50:03.822').ticks; reason='Context compaction and recovery; excluded' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T03:07:42.357').ticks; end=(Find-Reading '2026-10-03T03:08:47.538').ticks; reason='Unclocked mathematical extension in literature segment; excluded' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T03:27:24.251').ticks; end=(Find-Reading '2026-10-03T03:29:04.931').ticks; reason='Unclocked mathematical planning during literature; excluded' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T03:36:01.596').ticks; end=(Find-Reading '2026-10-03T03:41:29.881').ticks; reason='Context compaction and recovery; excluded' },
    [pscustomobject]@{ start=((Find-Reading '2026-10-03T03:46:46.110').ticks-60*$taskFrequency); end=(Find-Reading '2026-10-03T03:46:46.110').ticks; reason='Conservative sixty-second exclusion for mathematical planning during literature' },
    [pscustomobject]@{ start=((Find-Reading '2026-10-03T03:49:18.183').ticks-45*$taskFrequency); end=(Find-Reading '2026-10-03T03:49:18.183').ticks; reason='Conservative forty-five-second exclusion for mathematical planning during literature' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T04:06:19.516').ticks; end=(Find-Reading '2026-10-03T04:13:20.767').ticks; reason='Conservative exclusion of pre-compaction segment and recovery through first resumed checkpoint' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T04:47:23.000').ticks; end=(Find-Reading '2026-10-03T04:52:02.010').ticks; reason='Context compaction and recovery during verification; excluded' },
    [pscustomobject]@{ start=(Find-Reading '2026-10-03T04:55:10.244').ticks; end=(Find-Reading '2026-10-03T04:56:10.636').ticks; reason='Closure drafting before O segment; no retrospective mode credit' }
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
                task_id='N01'; attempt_id='R-N01-01-C3'; session_id='2026-10-02-R1'
                mode=$reading.mode; lane=$reading.lane; start_utc=$taskActive.utc; end_utc=$reading.utc
                elapsed_seconds=([double]$reading.ticks-[double]$taskActive.ticks)/$taskFrequency
                engaged_seconds=0.0; tool_wait_seconds=0.0; idle_seconds=0.0; unmeasured_seconds=0.0
                forecast_seconds=''; artifact='v2/work_logs/N01R_2026-10-02_S1.md'
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
foreach ($row in $taskRows) {
    foreach ($wait in $taskWaits) { $row.tool_wait_seconds += Overlap-Seconds $row.start_ticks $row.end_ticks $wait.start $wait.end }
    foreach ($excluded in $taskExclusions) { $row.unmeasured_seconds += Overlap-Seconds $row.start_ticks $row.end_ticks $excluded.start $excluded.end }
    $row.engaged_seconds = $row.elapsed_seconds-$row.tool_wait_seconds-$row.unmeasured_seconds
    if ($row.engaged_seconds -lt 0) { throw 'Exclusions overlap or exceed a segment.' }
}
# Conservative non-credit reserve for short unbracketed reads, patch calls and
# clock overhead across the session. This is unknown occupancy, not idle time.
foreach ($reserveMode in @('D','L','E','O')) {
    $taskReserve = switch ($reserveMode) { 'D' {120.0} 'L' {150.0} default {30.0} }
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
$taskForecast = @{D=5400; L=1800; E=900; O=900}
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
    task='N01'; engaged_minutes=$taskTotals; research_lane_minutes=$taskLanes
    tool_wait_minutes=[Math]::Round([double]($taskRows | Measure-Object tool_wait_seconds -Sum).Sum/60,6)
    unmeasured_within_segments_minutes=[Math]::Round($taskWithinUnknownSeconds/60,6)
    unsegmented_gap_minutes=if ($null -ne $taskGapSeconds) {[Math]::Round($taskGapSeconds/60,6)} else {$null}
    total_unmeasured_minutes=if ($null -ne $taskGapSeconds) {[Math]::Round(($taskWithinUnknownSeconds+$taskGapSeconds)/60,6)} else {$null}
    closed_segment_wall_minutes=[Math]::Round($taskClosedWallSeconds/60,6)
    observed_clock_span_minutes=[Math]::Round($taskClockSpanSeconds/60,6)
    protected_minimum='D+L120'; short_D_overhead_reserve_seconds=120; short_L_overhead_reserve_seconds=150; short_E_overhead_reserve_seconds=30; short_O_overhead_reserve_seconds=30
    open_segment_mode=if ($null -ne $taskActive) {$taskActive.mode} else {$null}
    initial_orientation='unmeasured; no retrospective credit'; literature='new targeted primary-source comparison; no credit from prior N01 or F10'; final_delivery='post-final-accounting documentation and commit handling unmeasured'
    exclusions=$taskExclusions; closed_rows=$taskRows.Count
}
$taskActuals | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'actuals.json') -Encoding utf8NoBOM
if ($AppendLedger) {
    if ($null -ne $taskActive -or $null -ne $taskWaitActive) { throw 'Close all segments and waits before appending.' }
    $taskLedger = Join-Path $taskRoot 'v2/time_ledger.csv'
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'ledger_append.json')) { throw 'This session has already appended its ledger.' }
    if (@(Import-Csv -LiteralPath $taskLedger | Where-Object { $_.attempt_id -eq 'R-N01-01-C3' -and $_.session_id -eq '2026-10-02-R1' }).Count) { throw 'Existing recurrence session rows require explicit reconciliation.' }
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
