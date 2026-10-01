$ErrorActionPreference = 'Stop'
$gateRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$gateSources = @(
  'v2/foundations/03_provisional_core.md',
  'v2/foundations/03b_observation_and_revision_audit.md',
  'v2/derivations/02_inference_rules.md',
  'v2/derivations/02b_source_transport_and_withdrawal.md',
  'v2/derivations/02c_derived_cases_and_completion.md',
  'v2/derivations/03_soundness.md',
  'v2/derivations/03d_producer_contract_audit.md',
  'v2/derivations/03f_soundness_acceptance.md',
  'v2/derivations/04_characterization.md',
  'v2/derivations/04a_characterization_reconstruction.md',
  'v2/derivations/04b_uniform_revision_characterization.md',
  'v2/derivations/04g_characterization_acceptance.md',
  'v2/derivations/05_fragments_and_comparisons.md',
  'v2/derivations/05g_comparison_reconstruction.md',
  'v2/literature/02_core_audit.md',
  'v2/literature/02a_research_calibration.md',
  'v2/research_protocol.md',
  'v2/checkpoints/A_1.md',
  'v2/checkpoints/A_1_timing_review.json'
)
$gateSources += Get-ChildItem (Join-Path $gateRoot 'v2/checks') -Filter 'f0*.py' |
    Where-Object Name -match '^f0[5-9]_' |
    ForEach-Object { 'v2/checks/' + $_.Name }
function Hash-Paths($paths) {
  foreach ($path in ($paths | Sort-Object -Unique)) {
    $absolute = Join-Path $gateRoot $path
    [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $absolute).Length; sha256=(Get-FileHash -LiteralPath $absolute -Algorithm SHA256).Hash.ToLowerInvariant()}
  }
}
$gateEvidence = @(
  'v2/checkpoints/B_1_reconstruction.md','v2/checkpoints/B_1_results.json',
  'v2/checkpoints/B_1_timing_review.json','v2/checkpoints/audit_b1_timing.py',
  'v2/checks/gate_b_review.py','verification/test_v2_gate_b.py'
)
$gateEvidence += Get-ChildItem $PSScriptRoot -File | Where-Object Name -ne 'manifest.ps1' |
    ForEach-Object { 'v2/work_logs/B_1_2026-09-30_S1/' + $_.Name }
$gateManifest = [ordered]@{
  source_baseline='d50905e89be0741feb9a1993fefb5db3424f957d'
  reviewer='Codex (GPT-6); fresh same-agent non-blinded reconstruction'
  hash_convention='SHA256 of observed worktree bytes; baseline files unchanged by Gate B. Timing audit separately hashes exact historical Git ledger bytes.'
  scope='Required mathematical dependency reconstruction; auxiliary code is versioned as supporting context, not a claim of fresh line-by-line review of every optional theorem or function.'
  sources=@(Hash-Paths $gateSources)
  evidence=@(Hash-Paths $gateEvidence)
}
$gateManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $gateRoot 'v2/checkpoints/B_1_inputs.json') -Encoding utf8NoBOM
Write-Output "Hashed $($gateSources.Count) source files and $($gateEvidence.Count) evidence files."
