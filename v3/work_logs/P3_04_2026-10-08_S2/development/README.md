# P3-04 replacement development evidence

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
All material is **DEVELOPMENT**, designed with the manuscript examples visible.
These are new S2 executions, not recovered S1 batches or held-out evaluation.

| Record | Current result |
|---|---|
| [First implementation run](attempt_1/summary.json) | PASS, eight suites, 28,064 assertions. Includes 512 small selector requests, 2,928 stopping prefixes, independent point/set comparison, Horn/arithmetic policies, structural adapters, encoding, ranked selection and gate witnesses. |
| [Composition supplement](composition_1/summary.json) | PASS, 288 paired-support requests and 39,457 assertions. Checks explicit arithmetic-normality-to-XOR translation, Boolean CNF gates, each penalty tier and all optimal assignments. |

Each directory contains a prospective manifest, complete dependency snapshots
and actual results. The first has per-suite progress records. No post-failure
rerun or undeclared source change occurred in these two runs. Successful finite
coverage does not establish general code correctness, native-checker integration,
learning performance or philosophical uniqueness. The current code matches
both runs' implementation hash; their drivers are different named scopes.

From the repository root, a repeat uses new output paths, never these saved ones:

```powershell
$out = Join-Path $env:TEMP ("p304-check-" + [guid]::NewGuid().ToString())
py -3 -B v3/checks/04_counterfactual_repair_check.py --output "$out-core"
py -3 -B v3/checks/04_cnf_composition_check.py --output "$out-composition"
```

Both programs require Python 3.10+ and the standard library only. The complete
research source/evidence bundle permits fresh reruns without the lost original
code or outputs. A repeat execution is not automatically extra research credit.
