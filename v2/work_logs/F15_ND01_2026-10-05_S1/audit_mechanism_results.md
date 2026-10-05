# F15-ND01 independent saved mechanism-output audit

Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
Concurrent work adds zero separate root-clock minutes. This is not F16.

**Verdict: PASS; 5,250 checks; 0 failures.**

The audit binds the saved mechanism JSON and executed source to the current
diagnostic freeze, all fifteen preparations and evaluations, original five
model artifacts, and core table hashes. No input/activation populations were
regenerated, no model forwards or fits were performed, and no iterative or
exhaustive optimizer was run.

## Independently recomputed checks

- All 200 candidate-coverage rows were rescored from saved Gram matrices,
  linear terms and constants using compensated scalar summation over the
  saved candidate subsets. The selected indices, best pool values, nonnegative
  coverage/selection gaps and their additive decomposition agree.
- All 150 intervention-error cells agree with the independently saved core
  MAE/logit-MSE cells and CSV table. Error-component sums, cross-moment bounds,
  unchanged-target diagnostics and energy-participation arithmetic agree.
- All 160 neurons' affine minima/maxima were independently evaluated at the
  sixteen exact rational box corners; classifications and rank/nullity bounds
  agree. All five models have globally inactive coordinates.
- All ten rank-one constructions satisfy the saved coefficient/root,
  symmetry, idempotence, sphere and native-head identities. The null directions
  are exact inactive-coordinate directions, with no learned projector fit.
- All fifteen composition records have the correct native commutator
  coefficients, mask overlaps, secondary-panel labels, probability/logit
  consistency and small reported identity errors.

## Findings that affect interpretation

All **100 distinct family/budget/role/model pool prefixes** miss
the exhaustive binary optimum for the same finite discovery logit objective;
none attains it within 1e-10. The smallest coverage gap is
**0.001780578**. For the original-style
cost-correlation, 128-candidate, frozen-MSE selection, the mean selection-
objective gap is **0.000000000**
and the mean candidate-coverage gap is
**0.025980112**.
Thus that comparison's missed logit optimum is a candidate-coverage limitation,
not an alternative winner already present in the same pool. This concerns the
discovery logit objective, not an optimized probability-MAE endpoint.

Fractional masks show nonzero secondary order drift in
**5/5 models**; their order-
probability RMS values are [0.01124108059102392, 0.03685184371259687, 0.011428942408088064, 0.016096617703330252, 0.02001078567366533].
Single-role improvement therefore does not establish a coherent joint two-cost
decomposition.

The source networks have **[2, 2, 3, 3, 3] globally
inactive units**. Their null directions permit the constructed rank-one
projectors to reproduce the fractional output effect, with maximum reported
validation discrepancy **2.748e-16**.
This is an algebraic output-equivalence construction using functionally
inactive dimensions, not evidence that training learned semantic subspaces,
nor a DAS result or jointly orthogonal role decomposition.

## Audit limits

The composition panels are not stored as raw arrays. This audit verifies their
saved coefficients, identities' reported errors and consistency bounds; it
does **not** independently recompute panel-specific joint RMS/MAE values.
The exact-box proof treats the saved binary64 parameters as exact real
coefficients, separately from the reported floating execution residuals.

One initial read-only source lookup used a nonexistent diagnostic-directory
path; it was corrected to the analysis directory before computation. No input,
model, scientific artifact or frozen file was changed by the audit.

The first audit attempt failed two audit-only assertions because it expected
the literal status `complete`; the frozen runner correctly stores
`preparation_complete` and `evaluation_complete`. Both manifests contained all
fifteen units, and all numerical/hash/source checks passed. Its original source,
JSON, SHA sidecar and Markdown are preserved in
[audit_mechanism_results_attempt1](audit_mechanism_results_attempt1/README.md).
The present second audit corrects only that schema assertion and rechecks the
saved records. No scientific artifact was changed and no population was drawn.

Machine-readable details: [audit_mechanism_results.json](audit_mechanism_results.json).
