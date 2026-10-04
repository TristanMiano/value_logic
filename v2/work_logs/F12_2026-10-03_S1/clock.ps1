param(
  [ValidateSet('start','stop','check','wait_start','wait_end')][string]$Event,
  [ValidateSet('D','L','E','O')][string]$Mode,
  [ValidateSet('R','X','')][string]$Lane = '',
  [string]$Note = ''
)
$taskReading = [ordered]@{
  task='F12'; attempt='R-N01-01-C2'; session='2026-10-03-S1'
  utc=[DateTime]::UtcNow.ToString('o'); ticks=[Diagnostics.Stopwatch]::GetTimestamp()
  frequency=[Diagnostics.Stopwatch]::Frequency; host=[Environment]::MachineName
  uptime_ms=[Environment]::TickCount64; event=$Event; mode=$Mode; lane=$Lane; note=$Note
}
$taskJson = $taskReading | ConvertTo-Json -Compress
[IO.File]::AppendAllText((Join-Path $PSScriptRoot 'clocks.jsonl'),$taskJson+"`n",[Text.UTF8Encoding]::new($false))
$taskJson
