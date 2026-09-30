param([switch]$AppendLedger)
$ErrorActionPreference = 'Stop'
$f08Root = Split-Path -Parent $PSScriptRoot
$f08Project = Split-Path -Parent (Split-Path -Parent $f08Root)
$f08Records = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'clocks.jsonl') | ForEach-Object { $_ | ConvertFrom-Json -DateKind String }
$f08Segments = [Collections.Generic.List[object]]::new()
$f08Open = $null
foreach ($f08Record in $f08Records) {
    if ($f08Record.event -eq 'start') {
        if ($null -ne $f08Open) { throw 'Overlapping clock starts.' }
        $f08Open = $f08Record
    }
    if ($f08Record.event -ne 'end') { continue }
    if ($null -eq $f08Open -or $f08Open.mode -ne $f08Record.mode -or $f08Open.lane -ne $f08Record.lane) { throw 'Unmatched clock end.' }
    if ($f08Open.host -ne $f08Record.host -or $f08Open.frequency -ne $f08Record.frequency) { throw 'Incomparable monotonic clocks.' }
    $f08Elapsed = [decimal]($f08Record.ticks-$f08Open.ticks)/[decimal]$f08Open.frequency
    $f08Wait = [decimal]0; $f08Unknown = [decimal]0
    $f08Status = 'closed; engaged research after exclusions'
    switch -Wildcard ($f08Open.utc) {
        '2026-09-30T03:49:03*' { $f08Unknown += [decimal](5791759261049-5790546503702)/10000000 }
        '2026-09-30T04:16:54*' { $f08Unknown += [decimal](5810109352942-5807730405737)/10000000 }
        '2026-09-30T04:54:11*' { $f08Unknown += 30 } # conservative D small-tool reserve
        '2026-09-30T03:34:32*' { $f08Wait += [decimal]8.85763 }
        '2026-09-30T03:54:27*' { $f08Wait += [decimal]9.4130246 }
        '2026-09-30T03:55:56*' { $f08Wait += [decimal]3.9334667 }
        '2026-09-30T04:26:41*' { $f08Wait += [decimal](0.2204879+0.2195276+2.3240497+1.8917914+1.7288612+10.000319) }
        '2026-09-30T04:36:59*' { $f08Wait += [decimal]10.0125593 }
        '2026-09-30T04:45:38*' { $f08Wait += [decimal](0.2531209+14.5793782+14.6892685+10.0022577) }
        '2026-09-30T04:59:48*' { $f08Wait += [decimal](9.1602171+6.3435716+0.3099281) }
    }
    if ($f08Open.mode -eq 'E') { $f08Unknown += 2 } # additional small-tool reserve per segment
    if ($f08Open.mode -in @('O','L')) {
        $f08Wait=0; $f08Unknown=$f08Elapsed
        $f08Status='closed; occupancy only; engaged/wait/recovery split unmeasured'
    }
    $f08Engaged=$f08Elapsed-$f08Wait-$f08Unknown
    if ($f08Engaged -lt 0) { throw 'Exclusions exceed occupancy.' }
    $f08Segments.Add([pscustomobject][ordered]@{
        task_id='F08'; attempt_id='F08-A1'; session_id='2026-09-30-S1'
        mode=$f08Open.mode; lane=$f08Open.lane; start_utc=$f08Open.utc; end_utc=$f08Record.utc
        elapsed_seconds=$f08Elapsed; engaged_seconds=$f08Engaged; tool_wait_seconds=$f08Wait
        idle_seconds=0; unmeasured_seconds=$f08Unknown; forecast_seconds=''
        artifact='v2/work_logs/F08_2026-09-30_S1.md'; status=$f08Status
    })
    $f08Open=$null
}
$f08Totals=[ordered]@{}
foreach ($f08Mode in @('D','L','E','O')) {
    $f08Selected=@($f08Segments | Where-Object mode -eq $f08Mode)
    $f08Totals[$f08Mode]=[ordered]@{
        engaged_minutes=($f08Selected | Measure-Object engaged_seconds -Sum).Sum/60
        occupancy_minutes=($f08Selected | Measure-Object elapsed_seconds -Sum).Sum/60
        blocked_wait_minutes=($f08Selected | Measure-Object tool_wait_seconds -Sum).Sum/60
        unmeasured_minutes=($f08Selected | Measure-Object unmeasured_seconds -Sum).Sum/60
    }
}
$f08Lanes=[ordered]@{}
foreach ($f08Lane in @('R','X')) {
    $f08Lanes[$f08Lane]=(@($f08Segments | Where-Object { $_.mode -in @('D','L','E') -and $_.lane -eq $f08Lane }) | Measure-Object engaged_seconds -Sum).Sum/60
}
$f08Summary=[ordered]@{
    source='UTC plus same-boot monotonic QPC pairs in clocks.jsonl'
    totals=$f08Totals; research_lane_minutes=$f08Lanes
    protected_D90_satisfied=($f08Totals.D.engaged_minutes -ge 90)
    open_segment=$f08Open
    accounting='D exclusions: mixed code interval; compaction/recovery gap; extra 30-second reserve. E: recorded command waits plus two seconds per segment. L/O: occupancy only, no invented engaged split. Background compute overlaps are not charged as blocked waits. Orientation and gaps outside paired segments are uncredited.'
}
$f08Segments | Export-Csv -LiteralPath (Join-Path $PSScriptRoot 'segments.csv') -NoTypeInformation -Encoding utf8NoBOM
$f08Summary | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'actuals.json') -Encoding utf8NoBOM
if ($AppendLedger) {
    if ($null -ne $f08Open) { throw 'Close all segments before appending the master ledger.' }
    $f08Ledger=Join-Path $f08Project 'v2/time_ledger.csv'
    $f08Original=[IO.File]::ReadAllBytes($f08Ledger)
    $f08OriginalText=[Text.Encoding]::UTF8.GetString($f08Original)
    if ($f08OriginalText -match '(?m)^"?F08,|(?m)^"F08",') { throw 'F08 ledger rows already exist; refusing duplicate append.' }
    $f08Hash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($f08Original)).ToLowerInvariant()
    $f08Csv=@($f08Segments | ConvertTo-Csv -NoTypeInformation)
    $f08Suffix=($f08Csv[1..($f08Csv.Count-1)] -join "`n")+"`n"
    if (-not $f08OriginalText.EndsWith("`n")) { $f08Suffix="`n"+$f08Suffix }
    [IO.File]::AppendAllText($f08Ledger,$f08Suffix,[Text.UTF8Encoding]::new($false))
    $f08After=[IO.File]::ReadAllBytes($f08Ledger)
    $f08Prefix=[byte[]]::new($f08Original.Length)
    [Array]::Copy($f08After,$f08Prefix,$f08Original.Length)
    $f08AfterHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($f08Prefix)).ToLowerInvariant()
    if ($f08AfterHash -ne $f08Hash) { throw 'Historical ledger prefix changed.' }
    [ordered]@{historical_bytes=$f08Original.Length; historical_sha256=$f08Hash; prefix_preserved=$true; rows_appended=$f08Segments.Count} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'ledger_append.json') -Encoding utf8NoBOM
}
$f08Summary | ConvertTo-Json -Depth 8
