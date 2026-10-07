# P3-03 development evidence

All attempts here are **DEVELOPMENT**. Each has inputs and a manifest saved
before scientific execution, followed by its summary and complete traces.
Earlier manifests bind their historical code/text snapshots; subsequent
development does not rewrite their records.

The largest repetitive trace is stored as deterministic, lossless gzip to keep
repository transfers small. Its logical artifact remains the exact original
JSON bytes hashed by the execution summary. The
[storage record](artifact_storage.json) binds both representations. From the
repository root, materialize and verify it with:

```sh
python v3/checks/03_materialize_evidence.py
```

The utility checks an existing output rather than overwriting it. It does not
rerun an experiment or generate new scientific evidence. Smaller traces remain
plain JSON. Reproduction of an experiment requires a new attempt number and
directory; never overwrite a completed attempt to make current code appear to
have been the originally exercised revision.


## Attempt index and historical execution commands

These commands document the executions already recorded here. Existing attempt
directories deliberately refuse overwrite. They are not instructions to rerun
completed evidence as a routine verification step. Any new scientific attempt
needs an appropriate fresh prospective plan and output directory; some narrow
repair evaluators are deliberately bound to their sole authorized attempt.

| Evidence | Executed command | Saved result |
|---|---|---|
| Original kernel | `python v3/checks/03_bounded_logic_check.py --attempt 1` | [12 suites / 10,840 assertions](attempt_1/summary.json) |
| Original task wrapper | `python v3/checks/03_task_certificate_check.py --attempt 1` | [9 suites / 64 assertions](task_certificate_attempt_1/summary.json) |
| Exact current-record binding | `python v3/checks/03_exact_binding_check.py --attempt 1` | [7 suites / 35 assertions](binding_attempt_1/summary.json) |
| Frontier, initial schema failure | `python v3/checks/03_frontier_check.py --attempt 1` | [Failure retained](frontier_attempt_1/summary.json) |
| Frontier, completed parity then schema failure | `python v3/checks/03_frontier_check.py --attempt 2` | [Failure and 6 completed cases retained](frontier_attempt_2/summary.json) |
| Frontier, remaining cases only | `python v3/checks/03_frontier_check.py --attempt 3 --part ordering_withdrawal` | [8 completed cases](frontier_attempt_3/summary.json) |
| Indexed receipt repair | `python v3/checks/03_receipt_identity_check.py --attempt 1` | [5 suites / 177 assertions](receipt_identity_repair/attempt_1/summary.json) |

The [frontier reconciliation](frontier_reconciliation.json) audits the saved
completed portions without repeating the method. The code at a historical
manifest's hash remains the source of that run: the initial core/wrapper are
in the published partial checkpoint `9712336ec5b29826c2b1eb787a1a499ee3549058`;
the later exact-binding core is also preserved in
[receipt_identity_repair/core_before.py](receipt_identity_repair/core_before.py).
The final repair area saves the current core and its exact delta. Preserved
nested evaluator copies retain their original file bytes and relative-path
assumptions; copying them into an unrelated directory is not a reproduction
of their original environment.
