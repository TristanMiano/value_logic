param(
    [Parameter(Mandatory=$true)][string]$Event,
    [string]$Mode = '',
    [string]$Lane = '',
    [string]$Note = ''
)
$taskClockPath = Join-Path $PSScriptRoot 'clocks.jsonl'
$taskReading = [ordered]@{
    task = 'N01'; attempt = 'R-N01-01-C3'; session = '2026-10-02-R1'
    utc = [DateTime]::UtcNow.ToString('o')
    ticks = [System.Diagnostics.Stopwatch]::GetTimestamp()
    frequency = [System.Diagnostics.Stopwatch]::Frequency
    host = [Environment]::MachineName
    uptime_ms = [Environment]::TickCount64
    event = $Event; mode = $Mode; lane = $Lane; note = $Note
}
$taskLine = $taskReading | ConvertTo-Json -Compress
[IO.File]::AppendAllText($taskClockPath, $taskLine + "`n", [Text.UTF8Encoding]::new($false))
Write-Output $taskLine
