param(
    [Parameter(Mandatory=$true)][string]$Event,
    [string]$Mode = '',
    [string]$Lane = '',
    [string]$Note = ''
)
$taskClockPath = Join-Path $PSScriptRoot 'clocks.jsonl'
$taskReading = [ordered]@{
    task = 'F10'; attempt = 'F10-A1'; session = '2026-09-30-S1'
    utc = [DateTime]::UtcNow.ToString('o')
    ticks = [System.Diagnostics.Stopwatch]::GetTimestamp()
    frequency = [System.Diagnostics.Stopwatch]::Frequency
    host = [Environment]::MachineName
    uptime_ms = [Environment]::TickCount64
    event = $Event; mode = $Mode; lane = $Lane; note = $Note
}
$taskLine = $taskReading | ConvertTo-Json -Compress
[System.IO.File]::AppendAllText($taskClockPath, $taskLine + "`n", [System.Text.UTF8Encoding]::new($false))
Write-Output $taskLine
