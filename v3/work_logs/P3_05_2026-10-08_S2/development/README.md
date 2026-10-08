# P3-05 reconstructed development evidence

All bundles below are newly executed DEVELOPMENT, not recovered evidence or
final evaluation. Source snapshots lie directly inside each bundle directory.
Preparation manifests retain their original command paths and observed dates.

| Bundle | Implementation | Result |
|---|---|---|
| [attempt_1](attempt_1/summary.json) | reconstructed-v1 | 1,451 assertions, seven groups; finite oracle and resource fixtures |
| [extension_1](extension_1/summary.json) | reconstructed-v1 | 48 assertions; rank envelope and counterpossible-frame changes |
| [substitution_1](substitution_1/summary.json) | reconstructed-v2 | 159 assertions; nonlinear Boolean maps, withdrawal and type rejection |
| [v2_regression_1](v2_regression_1/summary.json) | reconstructed-v2 | 1,451 assertions, unchanged main driver after explicit implementation extension |
| [v2_extension_1](v2_extension_1/summary.json) | reconstructed-v2 | 48 assertions, unchanged supplement after extension |

The point oracle is separately written by the same contributor, not a blind
independent researcher. Regressions are not additional independent discoveries.
Resource counters are partial and heterogeneous. Warm reuse needs prior cache
admission and can cost more than a simple direct proof; an optimized ordinary
symbolic method is allowed to simplify the parity fixture.

The closing `evidence_index.json` binds these existing files without rewriting
their prospective manifests. `python -X utf8 -B v3/checks/05_verify_evidence.py`
checks their checksums and source/version consistency. It does not rerun the
scientific tests. To re-execute a particular saved version, run its saved driver
with a new `--out` directory outside these historical bundles; all dependencies
used by that driver are in its bundle. Do not overwrite existing output.

Contributor: ChatGPT (GPT-6 Astra Pro), October 8, 2026 UTC.
