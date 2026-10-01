# Semantic verification

This directory began as a compact, standard-library Python reference for the finite witness in [`formalism/05a_integration.md`](../formalism/05a_integration.md). It now also tests the Task 20 neural implementation, which requires the frozen NumPy/PyTorch runtime recorded in [`experiments/implementation_v1.json`](../experiments/implementation_v1.json). It remains verification infrastructure rather than a proof-assistant formalization.

Phase two is complete through F10 at task scope; Gate B passed at mathematical-readiness scope; N01 is selected, unstarted; F11 remains unstarted.

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
