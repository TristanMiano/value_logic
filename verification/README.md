# Semantic verification

This directory began as a compact, standard-library Python reference for the finite witness in [`formalism/05a_integration.md`](../formalism/05a_integration.md). It now also tests the Task 20 neural implementation, which requires the frozen NumPy/PyTorch runtime recorded in [`experiments/implementation_v1.json`](../experiments/implementation_v1.json). It remains verification infrastructure rather than a proof-assistant formalization.

The implementation separates request well-formedness (`WF`) from meaningful three-valued atom assessment (`K_3 = {refuted, open, supported}`). Finite meet plus `WF` derives the four public outcomes. Indexed diagnostics are a disjoint sum retaining exactly the applicable witness, obstacle, or counterwitness plus safety flags and provenance; there is intentionally no closed reason-code enumeration. Missing evidence is an open diagnostic, while an omitted diagnostic record makes a purported well-formed fixture invalid.

From the repository root, run:

```powershell
python -m verification
```

The command exercises the three-stage integrated witness, the finite Task 14 separation/cardinality countermodels, the Task 14A transport/routing bounds, the Task 14B typed-footprint and audit-repair witnesses, the Task 14C proof-carrying-plan and stratified-assessment witnesses, the Task 15 encoding-contract regressions, the Task 16 hybrid-ReLU wrapper regressions, the Task 17 representation-theorem boundary witnesses, the Task 18 loss/calibration contract, the Task 19A generator/protocol, the Task 20 neural-symbolic implementation, and all local Markdown links. The Task 20 suite checks the closed learner/oracle boundary, matched capacity and paired initialization, independent-world calibration, exact boundary/zero semantics, missing/invalid/polarity overrides, every required ablation, `WF + K_3`, masks and fallback, transfer construction, prediction-before-evaluation hashing, system-grade/certificate separation, and the final-entry guard. Its pilot-role neural smoke path is run separately with `python -m experiments.run_experiment --smoke`; it is not an empirical endpoint. The formal/interface suites remain finite regression witnesses rather than proof-assistant formalizations or accepted empirical certificates; their proofs and contracts are in the cited formalism/ML files and [`experiments/02_implementation.md`](../experiments/02_implementation.md).
