# Semantic verification

This directory began as a compact, standard-library Python reference for the finite witness in [`formalism/05a_integration.md`](../formalism/05a_integration.md). It now also tests the Task 20 neural implementation, which requires the frozen NumPy/PyTorch runtime recorded in [`experiments/implementation_v1.json`](../experiments/implementation_v1.json). It remains verification infrastructure rather than a proof-assistant formalization.

**F16 complete at adversarial-review scope; D60 and Research90 satisfied.**
F01–F15, N01, C3 and C4 retain their completed task scopes; F15 and ND01 retain
their recorded protected floors. The [F16 adversarial review](../v2/derivations/07_adversarial_review.md)
and [work record](../v2/work_logs/F16_2026-10-05_S1.md) distinguish the new
mathematical/implementation checks from the preserved frozen experiments.
F16-R01 corrects C4-A1's three-procedure midpoint-coherence warning;
[F16-C1](../v2/derivations/10_f16_coherent_recovery.md) supplies a compatible
common-minimax decoder on the full exact equal-price summary fiber for
separately applied single-price edits.
C4-S remains a modest supported synthesis/application relative to checked work;
worldwide priority is unestablished. A/B retain their scoped passes; C/D are
unattempted. After F16 closure the next task is a separate Gate C assessment;
F17 and optional deferred F15-ND02 remain unstarted. See
[the current TODO](../TODO_v2.md) and [phase-two verification](../v2/verification/README.md).

The following F14 validation is historical development evidence.
F14's [protocol](../v2/experiments/protocol.md) uses CPython 3.12 and its separate
[NumPy 2.3.5 requirement](../v2/experiments/requirements-f14.txt); it does not
replace the phase-one neural runtime. Its 78 focused tests passed:

```text
python -m unittest discover -s verification -p 'test_v2_f14*.py' -v
python -m v2.experiments.freeze verify
```

Set `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS` and `MKL_NUM_THREADS` to `1` before
F14/F15 work, as specified in the protocol. The broader F14 repository attempt
had 1,638 successful cases and two legacy neural module-import errors because
PyTorch was unavailable. This is not a full-repository pass; those module bodies
did not execute. [F14 work and preserved logs](../v2/work_logs/F14_2026-10-04_S1.md).
The recorded Windows follow-up had six older dependency files with CRLF
byte differences, three focused-suite native access violations, and the separate
deterministic path-portability defect in
`test_dependency_closure_includes_parent_initializers_and_relative_imports`
(backslash paths compared with forward-slash strings). The crashes do not
identify a hardware cause. Use an unchanged clean Linux checkout for the frozen
runtime; no registered hash or frozen test was changed to accommodate Windows.
F15's completed Linux execution is in [results](../v2/experiments/results.md),
and the separately frozen [ND01 diagnostic](../v2/experiments/F15_ND01_results.md)
used the saved networks without retraining. F16's read-only integrity review
verified both freezes and preserved the original damaged F15 aggregate with its
already documented separate exact recovery. See the
[integrity record](../v2/work_logs/F16_2026-10-05_S1/reviews/integrity_review.md).
The validation records below retain their historical scopes.

Gate B's new wrapper runs **19 hostile tests**, all passing locally. Run
`python -X faulthandler -m unittest verification.test_v2_gate_b -v`.
The [finite report](../v2/checkpoints/B_1_results.json) has 13 cap values,
221 direct rational points and three received composite examples. During
Gate B, three full-suite and three aggregate F05–F09/Gate-B runs failed
natively; no current broad-suite pass is claimed. The [decision](../v2/checkpoints/B_1.md)
and [work record](../v2/work_logs/B_1_2026-09-30_S1.md) preserve scope and logs.

F10 changes research documentation and timing records, not the semantic code.
Its three `python -m verification` attempts all exited with native error
`0xC0000005`; attempt 2 also printed an `ERROR` for a phase-one native-kernel
test that printed `ok` in attempts 1 and 3. The crash prevented its traceback
summary, so the cause is unresolved and no full-suite pass is claimed. See the
[F10 record](../v2/work_logs/F10_2026-09-30_S1.md) for logs and validation.
The
three `test_v2_f09_*.py` wrappers run **46 focused comparison tests**, which
passed locally. Eight native certificates also passed the unchanged receiver
and serialization round trip. Full-suite and combined F08/F09 attempts ended
in native Python failures after bounded retries, so they are not reported as
passes. See the [F09 record](../v2/work_logs/F09_2026-09-30_S1.md) and
[phase-two README](../v2/README.md) for exact commands and scope. These tests do
not implement or verify the optional general affine certificate compiler.

The implementation separates request well-formedness (`WF`) from meaningful three-valued atom assessment (`K_3 = {refuted, open, supported}`). Finite meet plus `WF` derives the four public outcomes. Indexed diagnostics are a disjoint sum retaining exactly the applicable witness, obstacle, or counterwitness plus safety flags and provenance; there is intentionally no closed reason-code enumeration. Missing evidence is an open diagnostic, while an omitted diagnostic record makes a purported well-formed fixture invalid.

From the repository root, run:

```powershell
python -m verification
```

The command exercises the three-stage integrated witness, the finite Task 14 separation/cardinality countermodels, the Task 14A transport/routing bounds, the Task 14B typed-footprint and audit-repair witnesses, the Task 14C proof-carrying-plan and stratified-assessment witnesses, the Task 15 encoding-contract regressions, the Task 16 hybrid-ReLU wrapper regressions, the Task 17 representation-theorem boundary witnesses, the Task 18 loss/calibration contract, the Task 19A generator/protocol, the Task 20 neural-symbolic implementation, the Task 22B policy/value reconstruction boundaries, the Task 32 GitHub-math compatibility guard, and all local Markdown links. The Task 22B suite checks the exact encoder-image round trip, oracle `2 rho` action-gap bound, tight tie/flip cases, conservative `4 rho` non-abstention boundary, scalar-value harness propagation, stochastic/modal separation, support and history countermodels, IID disagreement, and trajectory coupling. The Task 20 suite checks the closed learner/oracle boundary, matched capacity and paired initialization, independent-world calibration, exact boundary/zero semantics, missing/invalid/polarity overrides, every required ablation, `WF + K_3`, masks and fallback, transfer construction, prediction-before-evaluation hashing, system-grade/certificate separation, and the final-entry guard. Its pilot-role neural smoke path is run separately with `python -m experiments.run_experiment --smoke`; it is not an empirical endpoint. The formal/interface suites remain finite regression witnesses rather than proof-assistant formalizations or accepted empirical certificates; their proofs and contracts are in the cited formalism/ML files and [`experiments/02_implementation.md`](../experiments/02_implementation.md).
