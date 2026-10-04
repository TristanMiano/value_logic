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
    [pscustomobject]@{ start=(Find-Reading '2026-10-04T17:37:23.814').ticks; end=(Find-Reading '2026-10-04T17:41:00.637').ticks; reason='Exclude complete context compaction/recovery interval since last observed reading' }
    [pscustomobject]@{ start=(Find-Reading '2026-10-04T18:16:57.136').ticks; end=(Find-Reading '2026-10-04T18:20:12.773').ticks; reason='Exclude second complete context compaction/recovery interval since last observed reading' }
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
                task_id='C4'; attempt_id='R-N01-01-C4-A'; session_id='2026-10-04-S1'
                mode=$reading.mode; lane=$reading.lane; start_utc=$taskActive.utc; end_utc=$reading.utc
                elapsed_seconds=([double]$reading.ticks-[double]$taskActive.ticks)/$taskFrequency
                engaged_seconds=0.0; tool_wait_seconds=0.0; idle_seconds=0.0; unmeasured_seconds=0.0
                forecast_seconds=''; artifact='v2/work_logs/C4_2026-10-04_S1.md'
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
# Preserve raw events; these conservative interval corrections use observed endpoints.
$taskCorrections = @(
    @{start='2026-10-04T18:10:38.058'; end='2026-10-04T18:13:41.531'; mode='O'; lane=''; reason='Conservatively exclude whole interval containing the accounting-script draft before its mode transition; substantive notes in that interval are also uncredited research'}
    @{start='2026-10-04T17:47:11.872'; end='2026-10-04T17:51:31.098'; mode='E'; lane='X'; reason='Includes code drafted before a batched mode-change call executed; classify whole observed interval as computational development'}
    @{start='2026-10-04T17:58:01.690'; end='2026-10-04T17:59:32.342'; mode='D'; lane='X'; reason='General equal-price moment geometry derivation during contribution comparison'}
    @{start='2026-10-04T18:01:55.570'; end='2026-10-04T18:03:53.332'; mode='D'; lane='X'; reason='General radius, canonical contrast and coherence derivation after computational exploration'}
)
foreach ($correction in $taskCorrections) {
    $from = Find-Reading $correction.start
    $to = Find-Reading $correction.end
    $matched = $false
    for ($i=0; $i -lt $taskRows.Count; $i++) {
        $row = $taskRows[$i]
        if ($row.start_ticks -le $from.ticks -and $row.end_ticks -ge $to.ticks) {
            $parts = [Collections.Generic.List[object]]::new()
            if ($row.start_ticks -lt $from.ticks) {
                $before = $row.PSObject.Copy()
                $before.end_ticks=$from.ticks; $before.end_utc=$from.utc
                $parts.Add($before)
            }
            $changed = $row.PSObject.Copy()
            $changed.start_ticks=$from.ticks; $changed.start_utc=$from.utc
            $changed.end_ticks=$to.ticks; $changed.end_utc=$to.utc
            $changed.mode=$correction.mode; $changed.lane=$correction.lane
            $changed.status += '; corrected mode: '+$correction.reason
            $parts.Add($changed)
            if ($row.end_ticks -gt $to.ticks) {
                $after = $row.PSObject.Copy()
                $after.start_ticks=$to.ticks; $after.start_utc=$to.utc
                $parts.Add($after)
            }
            $taskRows.RemoveAt($i)
            foreach ($part in $parts) {
                $part.elapsed_seconds=([double]$part.end_ticks-[double]$part.start_ticks)/$taskFrequency
                $taskRows.Insert($i,$part); $i++
            }
            $matched=$true
            break
        }
    }
    if (-not $matched) { throw 'Expected observed mode correction could not be applied.' }
}foreach ($row in $taskRows) {
    foreach ($wait in $taskWaits) { $row.tool_wait_seconds += Overlap-Seconds $row.start_ticks $row.end_ticks $wait.start $wait.end }
    foreach ($excluded in $taskExclusions) { $row.unmeasured_seconds += Overlap-Seconds $row.start_ticks $row.end_ticks $excluded.start $excluded.end }
    $row.engaged_seconds = $row.elapsed_seconds-$row.tool_wait_seconds-$row.unmeasured_seconds
    if ($row.engaged_seconds -lt 0) { throw 'Exclusions overlap or exceed a segment.' }
}
# Conservative non-credit reserve for short unbracketed reads, patch calls and
# clock overhead across the session. This is unknown occupancy, not idle time.
foreach ($reserveMode in @('D','L','E','O')) {
    $taskReserve = switch ($reserveMode) { 'D' {60.0} 'L' {60.0} 'E' {90.0} 'O' {30.0} default {0.0} }
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
$taskForecast = @{D=1800; L=1500; E=300; O=600}
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
    task='C4'; engaged_minutes=$taskTotals; research_lane_minutes=$taskLanes
    tool_wait_minutes=[Math]::Round([double]($taskRows | Measure-Object tool_wait_seconds -Sum).Sum/60,6)
    unmeasured_within_segments_minutes=[Math]::Round($taskWithinUnknownSeconds/60,6)
    unsegmented_gap_minutes=if ($null -ne $taskGapSeconds) {[Math]::Round($taskGapSeconds/60,6)} else {$null}
    total_unmeasured_minutes=if ($null -ne $taskGapSeconds) {[Math]::Round(($taskWithinUnknownSeconds+$taskGapSeconds)/60,6)} else {$null}
    closed_segment_wall_minutes=[Math]::Round($taskClosedWallSeconds/60,6)
    observed_clock_span_minutes=[Math]::Round($taskClockSpanSeconds/60,6)
    protected_minimum='D+L+E60'; short_D_overhead_reserve_seconds=60; short_L_overhead_reserve_seconds=60; short_E_overhead_reserve_seconds=90; short_O_overhead_reserve_seconds=30
    open_segment_mode=if ($null -ne $taskActive) {$taskActive.mode} else {$null}
    initial_orientation='unmeasured; no retrospective credit'; literature='focused primary-source comparisons; access and locators in literature/06_c4_contribution_comparison.md'; final_delivery='post-final-accounting documentation and commit handling unmeasured'
    exclusions=$taskExclusions; closed_rows=$taskRows.Count
    mode_corrections=$taskCorrections
}
$taskEngagedTotal = [Math]::Round([double]($taskTotals.Values | Measure-Object -Sum).Sum,6)
$taskPackageTotal = [Math]::Round(461.480742+$taskEngagedTotal,6)
$taskActuals.total_engaged_minutes = $taskEngagedTotal
$taskActuals.total_research_minutes = [Math]::Round($taskTotals.D+$taskTotals.L+$taskTotals.E,6)
$taskActuals.protected_floor_met = ($taskActuals.total_research_minutes -ge 60)
$taskActuals.package_before_minutes = 461.480742
$taskActuals.package_after_minutes = $taskPackageTotal
$taskActuals.eight_hour_overshoot_minutes = [Math]::Round($taskPackageTotal-480,6)
$taskActuals.remaining_to_sixteen_hours_minutes = [Math]::Round(960-$taskPackageTotal,6)
$taskActuals.forecast_error_vs_central_70_minutes = [Math]::Round($taskEngagedTotal-70,6)
$taskActuals.f14_central_package_close_minutes = [Math]::Round($taskPackageTotal+105,6)
$taskActuals.f14_high_package_close_minutes = [Math]::Round($taskPackageTotal+155,6)
$taskActuals | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'actuals.json') -Encoding utf8NoBOM
if ($AppendLedger) {
    if (($taskTotals.D+$taskTotals.L+$taskTotals.E) -lt 60) { throw 'C4 protected research60 is not met.' }
    if ($null -ne $taskActive -or $null -ne $taskWaitActive) { throw 'Close all segments and waits before appending.' }
    $taskLedger = Join-Path $taskRoot 'v2/time_ledger.csv'
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'ledger_append.json')) { throw 'This session has already appended its ledger.' }
    if (@(Import-Csv -LiteralPath $taskLedger | Where-Object { $_.attempt_id -eq 'R-N01-01-C4-A' -and $_.session_id -eq '2026-10-04-S1' }).Count) { throw 'Existing recurrence session rows require explicit reconciliation.' }
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
