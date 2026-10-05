# Fixed-model search comparison: F15-ND01

Authored by ChatGPT (GPT-6 Astra Pro). This is a development diagnostic. It
does not revise the frozen F15 result or train any new network.

## The representational assumption under test

Ordinary task training constrains the output function, but it supplies no
particular reason for a cost-specific internal computation to occupy one
eight-neuron coordinate subset. The ordinary optimum admits the logit

\[
\log J_0-\log J_1
=\log c_{\mathrm{FN}}-\log c_{\mathrm{FP}}
 +\log\eta-\log(1-\eta).
\]

A network can approximate this through shared, mixed, or distributed features.
Consequently, a failure of coordinate-subset replacement can reflect a mismatch
between the representation learned and the intervention family searched. It
does not on its own show that the relevant information is absent, and a good
decoder does not establish that the network uses it in the proposed causal way.
This diagnostic tests whether better search within the same eight-coordinate
family helps before attributing failure to that family itself. The separate
soft-mask diagnostic relaxes the coordinate restriction.

## Five proposal families

All families propose eight distinct indices out of the same 32 hidden units.
All use the same fit inputs, discovery pairs, actual interchange scoring, and
disjoint shared validation pairs. A duplicate proposal consumes its budget.

| Family | Proposal score | Sampling rule |
|---|---|---|
| `cost_corr` | Absolute Pearson correlation of hidden activation with the target expected cost | Original F15 candidate-pool rule, including the stable top-eight first candidate |
| `uniform` | None | Uniform random eight-element subsets |
| `permuted_cost_corr` | Absolute Pearson correlation with a once-permuted expected-cost target | Original F15 permuted-target proposals; actual identity interchange targets still score the candidates |
| `log_cost_corr` | Absolute Pearson correlation with the signed log cost | Same correlation proposal rule, changing only the target scale |
| `positive_contribution_cov` | Positive part of covariance between the native output contribution `v_j * h_j` and signed log cost, divided by log-target variance | Normalize the nonnegative scores across units, mix 25% uniform probability, and use stable top-eight scores first; use uniform sampling if all scores vanish |

The signed log target is `log(J0)` for role 0 and `-log(J1)` for role 1.
Absolute Pearson correlation of `v_j * h_j` with this target would be identical
to absolute correlation of `h_j` with `log(J)` whenever `v_j` is nonzero:
both the coefficient's magnitude and its sign cancel in the normalization and
absolute value. We therefore separate a log-target-only arm from an actual
sign- and magnitude-sensitive output-contribution arm. Contributions with
negative covariance may still be useful jointly; the covariance heuristic is
an explicit candidate for evaluation, not a promised improvement.

## Nested budgets and two selectors

Each family/role generates one 1,024-candidate pool. The smaller budget uses its
first 128 candidates. Both selectors reuse the same candidates and scores.
All 1,024 candidates receive the frozen scalar-cost decoder fit; those fits
retain the original MSE selector's final tie-breaker. The permuted family also
uses its permuted target for this decoder fit, as in the frozen implementation.

The `frozen_mse` selector uses the unchanged implementation's lexicographic
ranking: mean interchange probability MSE, adjusted effect MSE, then decoder
NMSE. The `robust` selector ranks the maximum of five stratum MAE/.05 values,
near-boundary disagreement/.35, and far-boundary disagreement/.10; its next
tie-breakers are mean probability MSE and unchanged-target output effect RMS.
Both use the original `1e-12` tie band and stable first-candidate choice on a
complete tie. No validation result or advantage over another search selects a
candidate.

## Split and accounting

Discovery seeds are 1510601–1510605. Validation seeds are 1510691–1510695.
Fit inputs use stream 10, proposals stream `50 + role`, target permutation
stream 61, discovery pairs `100 + 10 * role`, validation pairs
`200 + 10 * role`, and ordinary validation examples stream 300. These are new
development populations using the unchanged generators. Same-seed proposal
streams across families implement a coupled comparison; differing weights still
produce different pools. Every family's 128-budget arm is an exact prefix of
its own 1,024-budget arm.

The public `prepare_one`/`evaluate_one` separation is supplemented by a pure
`validate_prepared` check. The runner owns the stronger cross-model requirement:
save, hash, reload, and validate all prepared artifacts before generating the
first validation population. Evaluation performs no search and no decoder fit.

For each model the actual search performs 10,240 candidate scores and decoder
fits. Treating two budgets and two selectors as independent searches would
instead charge 23,040 logical candidate scores and fits. Both counts are saved;
reused scores do not count as new evidence. Evaluation also reuses predictions
for identical selected role/subset combinations, with actual and logical
intervention row counts reported separately.

Validation saves per-stratum errors, decisions, unchanged-target leakage,
ordinary/no-swap/whole-layer baselines, observational decoder and log-contribution
errors, and paired error-improvement sufficient statistics. Budget comparisons,
selector comparisons, and family comparisons remain descriptive. The pointwise
error/decision threshold indicator excludes the rest of the full F15 endpoint
and has no confirmatory confidence interpretation.
