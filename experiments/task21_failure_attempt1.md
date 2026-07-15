# Task 21 infrastructure-failure record: attempt 1

Date: 2026-07-15  
Disposition: **unread infrastructure failure; not an empirical result**

## Invocation and failure

Task 21 released the frozen entry point exactly as registered:

```text
python -m experiments.run_experiment --task21-final RUN-VALUE-LOGIC-FINAL-V1
```

The process used the frozen Task 20 runtime (CPython 3.13.3, NumPy 2.2.5,
CPU PyTorch 2.8.0) and remained responsive and CPU-active. After approximately
35 minutes it exited with code 1 through a fatal interpreter error rather than
a Python exception:

```text
Fatal Python error: _PyEval_EvalFrameDefault: Executing a cache.
Python runtime state: initialized

Current Python frame:
  experiments/protocol.py:1095 in _audit_nested
```

The calling stack placed the failure in final-confirmation evaluation while a
tolerance-transfer probe payload was being passed through the scorer-input
firewall. This is an impossible CPython bytecode-evaluator state, not a failed
assertion in the value-logic implementation and not a numerical endpoint.
The exact upstream trigger has not been established.

## Embargo and partial-artifact audit

No `raw_results_v1.json` was written. Before any prediction, label, loss,
calibration value, or endpoint metric was read, the filesystem was audited only
for artifact existence, filename/count, byte size, and whole-file hashes:

- `fit_complete_v1.json` existed; SHA-256
  `ad48b716945edb146ed3692a26a2ffe93f32e13afe78e3d560d75a6fee57f3be`;
- `model_states_v1.npz` existed; SHA-256
  `38a939225b373694c194015b3b18c4e4be1a2a67c30fa8f065408b476894a9e7`;
- 191 of 400 trace shards existed, totaling approximately 0.535 GiB;
- the counts by fit seed were 50 for 101, 50 for 211, 50 for 307, and 41
  for 401.

These are incomplete execution products and must not be treated as a result,
used for model or threshold selection, or combined with a later confirmation.

## Registered recovery scope

Section 12 of the preregistration and `protocol_v1.json` permit the same seed
and configuration to be rerun after an unread infrastructure failure, with the
failure logged. They forbid rerunning because of numerical or unfavorable
outcomes. This attempt meets the infrastructure exception because the
interpreter terminated before a raw result existed and no metrics were read.

The recovery must therefore preserve the frozen source hashes, dependency
versions, seeds, manifests, model-selection rule, fitting/calibration paths,
endpoints, and analysis plan. A maintenance-patch change to the CPython host,
if used to avoid the interpreter defect, is an execution-environment deviation
and must be reported with the final results. Partial artifacts from this attempt
must be removed before the guarded entry point is invoked again; their hashes
and this record preserve the audit trail.
