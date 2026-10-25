# Reproduce and inspect s18 development evidence

Codex (GPT-6). All probes are same-model DEVELOPMENT; no independent
confirmation or fresh economic benchmark is implied. The closing manifest
binds original sources, outputs, notes and clocks. Do not rerun a frozen
script in place: most write their companion result and would replace evidence.
Use an isolated checkout/output copy with the same relative source dependencies,
record the new execution separately, and never relabel it as the original run.

The principal runtime was Python3.12.14 from the bundled primary runtime;
early symbolic probes used C:/Python313/python.exe (3.13.14). Per-result
versions, hashes and elapsed times are authoritative. SymPy is required for
the symbolic cap-rank check; other imports are visible in the bound sources.
Retention imports the preserved s05 source and result files; their input
hashes are verified. Source access and proof scopes are in [literature](literature.md).

| Frozen source | Original output | Status | Python | Elapsed ns |
| --- | --- | --- | --- | ---: |
| [attainer_check.py](attainer_check.py) | [attainer_result.json](attainer_result.json) | PASS | 3.12.14 | 253242400 |
| [calibration_check.py](calibration_check.py) | [calibration_result.json](calibration_result.json) | pass | 3.13.14 | 68835700 |
| [cap_rank_check_v2.py](cap_rank_check_v2.py) | [cap_rank_v2_result.json](cap_rank_v2_result.json) | Recorded; inspect result | 3.13.14 | 32567400 |
| [closure_check.py](closure_check.py) | [closure_result.json](closure_result.json) | PASS | 3.12.14 | 79820700 |
| [convex_value_check.py](convex_value_check.py) | [convex_value_result.json](convex_value_result.json) | PASS | 3.12.14 | 31000000 |
| [core_check.py](core_check.py) | [core_result.json](core_result.json) | PASS | 3.12.14 | 62000000 |
| [demo_check.py](demo_check.py) | [demo_result.json](demo_result.json) | PASS | 3.12.14 | 1493300 |
| [fault_check.py](fault_check.py) | [fault_result.json](fault_result.json) | PASS | 3.12.14 | 927074100 |
| [matroid_check.py](matroid_check.py) | [matroid_result.json](matroid_result.json) | PASS | 3.12.14 | 1467808500 |
| [ordinal_check.py](ordinal_check.py) | [ordinal_result.json](ordinal_result.json) | PASS | 3.12.14 | 4004863900 |
| [path_update_check.py](path_update_check.py) | [path_update_result.json](path_update_result.json) | PASS | 3.12.14 | 139546900 |
| [receipt_search_check.py](receipt_search_check.py) | [receipt_search_result.json](receipt_search_result.json) | pass | 3.13.14 | 67239200 |
| [regret_check.py](regret_check.py) | [regret_result.json](regret_result.json) | NO_GAP_IN_PANEL | 3.12.14 | 1068834900 |
| [retention_check.py](retention_check.py) | [retention_result.json](retention_result.json) | PASS | 3.12.14 | 7750000000 |
| [tied_check.py](tied_check.py) | [tied_result.json](tied_result.json) | PASS | 3.12.14 | 200981600 |
| [total_search_check.py](total_search_check.py) | [total_search_result.json](total_search_result.json) | PASS | 3.12.14 | 111451400 |

The original cap_rank_check.py deterministically failed JSON serialization;
its separately named v2 is the successful repair. See [failures](failures.md).
The later covering sieve, concave extension and partial-receipt examples are
derivations, not claims checked by the earlier segment DP implementation.
Probe runtime is contained in research time, never credited a second time.

Read-only closing checks from the repository root:

```powershell
python v3/discovery/s18/verify_evidence.py --index
python tools/check_repo_paths.py
python tools/evidence_paths.py verify
```

The evidence verifier validates all top-level executed-source SHA256 fields,
recorded dependency hashes, effective time totals, the prior ledger prefix,
all27 historical recurrence row objects and their exact raw bytes. It checks
the closing manifest against working files and, with --index, staged blobs.
It does not prove the mathematics. Reconciliation is idempotent but writes
its effective summary; do not run it merely to inspect the closed clock.
