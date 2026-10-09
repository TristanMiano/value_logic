#requires -Version 5.1
<#
Guarded P3-06 publication wrapper. Uses the user's existing Git identity and
authentication. Never sets credentials, changes execution policy or force-pushes.
The expected ZIP hash must come from the delivery message, outside the ZIP.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Repository,
    [Parameter(Mandatory = $true)][string]$PackageZip,
    [Parameter(Mandatory = $true)][ValidatePattern('^[0-9a-fA-F]{64}$')][string]$ExpectedZipSha256,
    [string]$Python,
    [switch]$CheckOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$packagePath = (Resolve-Path -LiteralPath $PackageZip).Path
$repositoryPath = (Resolve-Path -LiteralPath $Repository).Path
$expectedHash = $ExpectedZipSha256.ToLowerInvariant()
$actualHash = (Get-FileHash -LiteralPath $packagePath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualHash -ne $expectedHash) {
    throw 'ZIP SHA-256 mismatch. The repository has not been changed.'
}
$helperPath = Join-Path $PSScriptRoot 'apply_package.py'
if (-not (Test-Path -LiteralPath $helperPath -PathType Leaf)) {
    throw 'Keep Apply-And-Push.ps1 beside the delivered apply_package.py.'
}
$pythonPrefix = @()
if ($Python) {
    $pythonCommand = $Python
} elseif (Get-Command py -CommandType Application -ErrorAction SilentlyContinue) {
    $pythonCommand = 'py'
    $pythonPrefix = @('-3')
} elseif (Get-Command python3 -CommandType Application -ErrorAction SilentlyContinue) {
    $pythonCommand = 'python3'
} elseif (Get-Command python -CommandType Application -ErrorAction SilentlyContinue) {
    $pythonCommand = 'python'
} else {
    throw 'Python 3.10 or later is required. Install it or supply -Python with its executable path.'
}
$arguments = @($pythonPrefix) + @(
    $helperPath,
    '--repo', $repositoryPath,
    '--package', $packagePath,
    '--zip-sha256', $expectedHash
)
if ($CheckOnly) {
    $arguments += '--check-only'
}
& $pythonCommand @arguments
$helperExitCode = $LASTEXITCODE
if ($helperExitCode -eq 3) {
    throw 'The local application commit is retained, but remote publication is not verified. Resolve the reported condition and rerun this same command; do not append or commit the package again manually.'
}
if ($helperExitCode -ne 0) {
    throw ('The guarded helper stopped with exit code ' + $helperExitCode + '. Read its diagnostic above. No force push was attempted.')
}
