# P3-06 mathematical-query development

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.

Version 2 corrects resource instrumentation while retaining version 1's exact input-generation identifier.
Version 1 source bytes and output remain preserved under `mathematical_queries_v1/source_snapshot`.
The old `max_state_fraction_bits` was the maximum over final accumulators, not a temporal peak.
Version 2 separately reports final accumulator size, final complete state size, and a peak measured after
every issue and reveal. Pending predictions are included; retained immutable reports were measured when
issued. Per-boundary observations are saved. This measures Fraction numerator/denominator bit sizes,
not RAM use or temporary arithmetic intermediates. No new population or parameter choice is introduced.

This is a bounded development run. It neither freezes a final challenge nor selects paid computation.
Subagent research time is unmeasured and contributes zero principal Research90 credit.

## Declared contract

Queries ask whether `(a**n mod m) == r`, with `0 <= a <= 8191`, `0 <= n <= 192`,
`2 <= m <= 97`, and `0 <= r < m`. Inputs and issue-time weights/loss tables are saved.
The full generator intentionally selects roughly balanced true/false queries using exact arithmetic.
Its selection rule and computation are public and charged in generation counters; these are synthetic cases,
not a claim about a natural mathematical-query distribution or an unpredictable outcome process.

The null family excludes the partial shortcut's applicable bases and is null only relative to the declared
small heuristic library. Its public generator is itself exploitable by an ordinary predictor that knows
the case and index. No hidden-source advantage, distributional difficulty, or useful-expert guarantee is claimed.

Every fresh unknown claim is reported before repeated-multiplication production and an independent binary
square-and-multiply check. Python `pow` supplies an additional ordinary cross-check. Checked receipts are
withheld from the learners until end-of-tick scheduled admission. Pending tail answers are saved for
reproduction but never admitted, used in expert history, or included in reported scores. This is local
deterministic checking, without a formal-proof or receipt-authentication claim.

A same-scope admitted residue entails every target equality for those exact exponentiation inputs.
The cached duplicate at issue 33 has a fresh ID but receives its known exact probability and exact action
costs. No learner state is created for that request. Historical forecasts retain their original hashes;
admission adds a separately versioned exact interpretation. A wrong-scope receipt is rejected without
changing the evidence cache. No malformed external evidence is being certified by this small check.

## Methods and accounting

Four expert reports are available to each learned method: constant one half, a Laplace-smoothed admitted
residue frequency by modulus, an exact partial shortcut for bases congruent to 0, 1, or minus 1 (and
exponent zero), and a deliberately fallible parity heuristic. The scope cache wraps all these reports
equally on already known claims. No expert receives a withheld answer. The exact modular-power baseline
may compute every new query immediately; its answer is not passed to other methods before admission.

Each scalar configuration is compared with an ordinary K29 adapter using the same features and identical
core. Their equality is intentional and checked report by report; it is not independent validation.
The decision configuration adds the two continuous exposure-difference features, with dyadic positive
smoothing. Mixed losses are expected losses of this declared action mixture; hard-action losses are
recorded separately and do not inherit that guarantee. Costs and weights vary according to public schedules.

The score-only baseline implements the binary specialization of [Vovk and Zhdanov's Brier AA](https://www.jmlr.org/papers/volume10/vovk09a/vovk09a.pdf),
JMLR 2009, Section 2 Algorithm 1/Theorem 1 and Section 5. The source's vector Brier loss equals twice
our scalar squared loss. For a declared maximum stake, the fixed exponent-update rate is twice its
reciprocal; the current weighted generalized losses use the corresponding scaled rate. Binary substitution
uses `(1 + g0 - g1)/2`. Binary64 log/exp and clipping are logged. The ideal real-arithmetic constant
regret is a source/reference comparison, not a certified guarantee for these floating outputs.

Primitive modular multiplication/reduction counts are separate for production, checking, generation and
the ordinary exact solver. The checker and solver independently run the binary algorithm. Python `pow`
calls are counted but their internal multiplication counts are unknown. Core score evaluations, bisections,
fraction bit lengths, copy counts and observed call wall times are recorded; these are not hard time or
memory caps. Shared expert work is actually performed once and assigned to each learned method for a
standalone comparison. Hashing, serialization, interpreter overhead and total memory are not fully metered.

## Results

All scores below use admitted queries only, including known-cache requests. Regret compares a fixed expert
or fixed action index over the same issue-time weights. Negative action regret is legitimate. Exact values,
the five calibration bin residuals and their masses, reported root allowances, and startup/later splits
are in each case JSON. Rounded numbers here do not replace those exact records.

| Case / method | Admitted / pending | Weight | Brier / weight | Regret to best expert | Mixed regret | Hard regret |
|---|---:|---:|---:|---:|---:|---:|
| recurring_shortcuts / scalar_without_decision | 128 / 0 | 128.000000 | 0.011165 | 1.429070 | -137.695312 | -138.000000 |
| recurring_shortcuts / scalar_with_decision | 128 / 0 | 128.000000 | 0.110599 | 14.156653 | -97.398460 | -95.000000 |
| recurring_shortcuts / ordinary_brier_aa_binary64 | 128 / 0 | 128.000000 | 0.004223 | 0.540557 | -143.366277 | -143.000000 |
| recurring_shortcuts / ordinary_fast_exact | 128 / 0 | 128.000000 | 0.000000 | 0.000000 | -144.000000 | -144.000000 |
| balanced_nonshortcut_null / scalar_without_decision | 128 / 0 | 128.000000 | 0.265712 | 2.261084 | -31.395996 | -32.000000 |
| balanced_nonshortcut_null / scalar_with_decision | 128 / 0 | 128.000000 | 0.308615 | 7.752704 | 4.112284 | -2.000000 |
| balanced_nonshortcut_null / ordinary_brier_aa_binary64 | 128 / 0 | 128.000000 | 0.250303 | 0.288798 | -40.330942 | -42.000000 |
| balanced_nonshortcut_null / ordinary_fast_exact | 128 / 0 | 128.000000 | 0.000000 | -31.750000 | -135.000000 | -135.000000 |
| delayed_pending_tail / scalar_without_decision | 120 / 8 | 450.000000 | 0.233969 | 30.536139 | -116.435303 | -119.000000 |
| delayed_pending_tail / scalar_with_decision | 120 / 8 | 450.000000 | 0.282883 | 52.547201 | 75.970792 | 70.000000 |
| delayed_pending_tail / ordinary_brier_aa_binary64 | 120 / 8 | 450.000000 | 0.192746 | 11.985746 | -139.952534 | -141.000000 |
| delayed_pending_tail / ordinary_fast_exact | 120 / 8 | 450.000000 | 0.000000 | -74.750000 | -467.000000 | -467.000000 |
| varying_stakes_actions / scalar_without_decision | 128 / 0 | 480.000000 | 0.266031 | 7.944847 | -144.913330 | -144.000000 |
| varying_stakes_actions / scalar_with_decision | 128 / 0 | 480.000000 | 0.318507 | 33.133415 | -17.692409 | -39.000000 |
| varying_stakes_actions / ordinary_brier_aa_binary64 | 128 / 0 | 480.000000 | 0.251391 | 0.917445 | -177.734128 | -178.000000 |
| varying_stakes_actions / ordinary_fast_exact | 128 / 0 | 480.000000 | 0.000000 | -119.750000 | -508.000000 | -508.000000 |

The matched ordinary K29 rows are omitted from this display because every issued report and all
metrics equal their scalar counterpart exactly. The JSON retains all six method records.

## Interpretation and limits

The exact solver incurs zero Brier loss on every admitted case and remains available throughout.
This small arithmetic domain therefore supplies no evidence that fallible forecasting is preferable
to ordinary exact computation at these budgets. The question tested is whether the forecast adapter
preserves scope, chronology, expert comparisons, action accounting and residual certificates when
fresh deterministic answers arrive on a delay schedule. The current comparisons do not establish
a practical win, broad mathematical learning, or a contribution-gate result.

Finite success of the scalar inequalities is checked against the exact audit; it does not establish
asymptotic convergence on these short cases. Calibration ratios require their own positive bin
mass, and pending forecasts are excluded rather than assigned fabricated outcomes. Larger decision
feature norms and more simultaneous copies can enlarge a correct but loose bound.

Issue-index startup and later summaries are descriptive, not selected test endpoints. No final
evaluation population, final controls, paid computation policy, or freeze is created here.
