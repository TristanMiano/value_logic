# P3-06 finite bound usefulness and resource correction

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.

## What this analysis establishes

The saved certificates are mathematically valid on the enumerated records, but
their finite usefulness depends on the comparator and denominator. Every
reported Brier bound beats the coarse total-unknown-weight bound. Three of the
four decision-feature Brier bounds fail to improve an elementary bound obtained
from the actual issued expert forecasts. The decision-feature calibration bound
adds no improvement over elementary bin bounds in the delayed and varying-stake
cases. The mixed-action certificates do improve their elementary action bounds
in all four cases. None of those comparisons establishes predictive superiority.

This analysis reads [v1 records](../mathematical_queries_v1/REPORT.md); it does
not run or tune a learner. It reconstructs scores and per-copy potential terms
with exact rational arithmetic. The public synthetic generator, small declared
expert library, and availability of cheap ordinary exact computation retain
their original limitations. Results for matched ordinary K29 adapters coincide
and are not duplicated in the tables.

## Comparisons and interpretation

Let $`I`$ denote admitted unknown-at-issue records, and include cache-at-issue
records in the full score set. For each cached record this analysis checks
$`p_t=y_t`$ and exact expert reports. Their Brier loss and calibration residual
are zero. Let $`W_u=\sum_{t\in I}w_t`$ and let $`H`$ be the sum of square roots
of the settled per-copy potential bounds. The rational upper enclosure actually
reported is used in all numerical comparisons below. The
[existing derivation](../../../../derivations/06_cost_forecast_refinement.md)
supplies the potential and regret identities; this note does not change it.

The coarse Brier regret bound is $`W_u`$. A sharper elementary comparator-specific
bound uses the issued forecasts alone:

```math
T_i^{\mathrm{B}}=\sum_t w_t\max_{y\in Y_t}
       \bigl((p_t-y)^2-(q_{t,i}-y)^2\bigr),\qquad
L-L_i\le T_i^{\mathrm{B}}.
```

Here $`Y_t=\{y_t\}`$ for a checked answer already known at issue and
$`Y_t=\{0,1\}`$ otherwise. Consequently $`\max_i T_i^{\mathrm{B}}`$ bounds regret
to the best fixed expert. The smaller bound for the particular observed best
expert is also reported, with that expert named retrospectively. This does not
identify the best expert in advance. Neither maximization claims that all
roundwise worst outcomes are jointly realizable by this mathematical generator.
Each inequality holds on the realized adaptive tape.

The recorded generic Brier certificate is $`2H`$. Retaining the already established
distance term gives $`2H-D_i`$, where
$`D_i=\sum_t w_t(q_{t,i}-p_t)^2`$. This is a sharper reading of the same saved
identity, without a new run. It is useful to distinguish the universal
fixed-comparator statement from a bound for the expert that happened to win.

For actions, write $`\bar c_t(y)=(1-s_t)c_{t,0}(y)+s_tc_{t,1}(y)`$. The
elementary envelope is

```math
T_i^{\mathrm{A}}=\sum_t w_t\max_{y\in Y_t}
                  (\bar c_t(y)-c_{t,i}(y)).
```

Then $`\max_iT_i^{\mathrm{A}}`$ bounds regret to the best fixed action. This
is at least as strong as using the sum of maximum row differences. The
decision-feature certificate is $`H+\sum_{t\in I}w_t\eta_t/8`$. Retaining actual
forecast gaps $`G_i=\sum_t w_t(\bar C_t(p_t)-C_{t,i}(p_t))`$ sharpens it to
$`H+\max_iG_i`$. The known-cache records have zero residual and nonpositive
forecast gaps. No action certificate is inferred for the mode without decision
features, and no mixed-action certificate is assigned to hard rounded actions.

For tent $`h_j`$, let $`M_j=\sum_t w_th_j(p_t)`$ include all scored records.
The elementary calibration bound is

```math
|E_j|\le T_j^{\mathrm{C}}
 =\max\left\{\sum_{t\in I}w_th_j(p_t)p_t,
             \sum_{t\in I}w_th_j(p_t)(1-p_t)\right\}\le M_j.
```

Exact cache reports are essential for their omitted numerator contribution.
The certificate $`|E_j|\le H`$ only improves this elementary bound when
$`H<T_j^{\mathrm{C}}`$. Conditional calibration divides by $`M_j`$, not by total
weight. Empty bins have zero residual and no conditional ratio. A populated
bin consisting only of known exact answers already has elementary bound zero.
The inequalities were independently checked by the same-model proof reviewer;
the arithmetic in this artifact is implementation-author analysis.

## Settled copies and root allowances

| Case / mode | Created / settled / positive-bound copies | Unknown weight | H | Actual allowance | Allowance / sum B |
|---|---:|---:|---:|---:|---:|
| recurring_shortcuts / scalar_without_decision | 1 / 1 / 1 | 127.000 | 1.814 | 0.005104 | 0.155103% |
| recurring_shortcuts / scalar_with_decision | 1 / 1 / 1 | 127.000 | 15.530 | 0.006523 | 0.002704% |
| balanced_nonshortcut_null / scalar_without_decision | 1 / 1 / 1 | 127.000 | 5.459 | 0.012723 | 0.042701% |
| balanced_nonshortcut_null / scalar_with_decision | 1 / 1 / 1 | 127.000 | 20.810 | 0.012356 | 0.002853% |
| delayed_pending_tail / scalar_without_decision | 8 / 4 / 4 | 449.000 | 47.860 | 0.012844 | 0.002219% |
| delayed_pending_tail / scalar_with_decision | 8 / 4 / 4 | 449.000 | 194.710 | 0.011781 | 0.000122% |
| varying_stakes_actions / scalar_without_decision | 1 / 1 / 1 | 479.000 | 24.657 | 0.014909 | 0.002452% |
| varying_stakes_actions / scalar_with_decision | 1 / 1 / 1 | 479.000 | 107.546 | 0.010745 | 0.000093% |

The delayed run creates eight copies. Four contain admitted feedback and four
contain only pending forecasts at this boundary. Only the first four contribute
positive settled potential. Their individual variance, allowance, bounds and
square-root enclosures are in `analysis.json`. All eight pending queries remain
excluded from scores and settled potential; their issue-time allowances are
retained separately. The allowance fractions show that feature variance, rather
than insufficient root accuracy, dominates these finite bound sizes. These
figures do not license setting a nonzero actual allowance to zero.

## Brier nonvacuity

| Case / mode | Actual best-expert regret | Reported 2H | Coarse W_u | Elementary, all fixed experts | Elementary, observed best | 2H−D, observed best |
|---|---:|---:|---:|---:|---:|---:|
| recurring_shortcuts / scalar_without_decision | 1.429 | 3.628 | 127.000 | 89.322 | 1.429 | 2.199 |
| recurring_shortcuts / scalar_with_decision | 14.157 | 31.060 | 127.000 | 63.332 | 14.157 | 16.903 |
| balanced_nonshortcut_null / scalar_without_decision | 2.261 | 10.917 | 127.000 | 36.501 | 10.736 | 9.876 |
| balanced_nonshortcut_null / scalar_with_decision | 7.753 | 41.620 | 127.000 | 38.720 | 23.463 | 37.230 |
| delayed_pending_tail / scalar_without_decision | 30.536 | 95.720 | 449.000 | 112.371 | 70.873 | 62.982 |
| delayed_pending_tail / scalar_with_decision | 52.547 | 389.420 | 449.000 | 120.138 | 108.580 | 331.586 |
| varying_stakes_actions / scalar_without_decision | 7.945 | 49.314 | 479.000 | 106.403 | 42.966 | 44.554 |
| varying_stakes_actions / scalar_with_decision | 33.133 | 215.092 | 479.000 | 156.693 | 106.057 | 192.627 |

The plain scalar's generic bound improves the uniform elementary envelope in
all four cases; the decision scalar does so only in the shortcut case. Against
the envelope for the actual winning expert, none of the unsharpened `2H`
bounds improves it. Retaining the distance term gives such an improvement for
the plain scalar on the null and delayed cases. The elementary bound against
an endpoint-valued exact shortcut equals the actual squared loss on the
shortcut family, so the potential certificate cannot sharpen that particular
comparison. This is not evidence that the potential inequality is incorrect.

## Mixed actions and hard decisions

| Case | Actual mixed regret | H + smoothing slack | Elementary action envelope | H + observed forecast gap | Actual hard regret |
|---|---:|---:|---:|---:|---:|
| recurring_shortcuts | -97.398 | 15.966 | 134.251 | -78.314 | -95.000 |
| balanced_nonshortcut_null | 4.112 | 21.246 | 165.985 | 19.683 | -2.000 |
| delayed_pending_tail | 75.971 | 196.108 | 649.752 | 161.064 | 70.000 |
| varying_stakes_actions | -17.692 | 108.970 | 659.990 | 44.564 | -39.000 |

Every displayed mixed-action certificate improves the corresponding elementary
action envelope. In the shortcut case the retained-gap bound is negative: this
particular certificate establishes an advantage over both fixed action indices
on the admitted tape. It compares fixed indices across changing loss tables,
not an outcome-aware optimal action or the competing adaptive methods. The
plain scalar, AA and ordinary exact baseline still have better observed action
performance in these runs. Positive delayed mixed regret and negative shortcut
regret are both compatible with the one-sided theorem. Hard-action observations
remain separate; their proximity to mixed losses does not transfer a guarantee.

## Calibration denominators

| Case / mode | H / total weight | Actual max residual / total weight | Populated bins | H improves mass bound | H improves elementary forecast-range bound |
|---|---:|---:|---:|---:|---:|
| recurring_shortcuts / scalar_without_decision | 0.014172 | 0.003824 | 5 | 5 | 4 |
| recurring_shortcuts / scalar_with_decision | 0.121329 | 0.022535 | 5 | 4 | 2 |
| balanced_nonshortcut_null / scalar_without_decision | 0.042645 | 0.027480 | 5 | 3 | 3 |
| balanced_nonshortcut_null / scalar_with_decision | 0.162579 | 0.082955 | 5 | 3 | 2 |
| delayed_pending_tail / scalar_without_decision | 0.106356 | 0.018040 | 5 | 3 | 3 |
| delayed_pending_tail / scalar_with_decision | 0.432689 | 0.053743 | 5 | 0 | 0 |
| varying_stakes_actions / scalar_without_decision | 0.051369 | 0.030502 | 4 | 3 | 2 |
| varying_stakes_actions / scalar_with_decision | 0.224054 | 0.107173 | 5 | 2 | 0 |

Total-weight normalization alone can make a correct bound look useful even
when it says nothing new about any conditional bin. In particular, the delayed
and varying-stake decision-feature bounds do not improve a single elementary
bin bound. Other cases improve some bins and not others. `analysis.json` gives
every exact mass, residual, elementary bound, potential bound, and conditional
ratio, including zero-mass/known-only cases. The valid combined bound is the
minimum of the elementary and potential bounds; it never needs to be weakened
to the larger one for presentation.

## Resource-metric correction and receipt repair

Version 1's `max_state_fraction_bits` measured final accumulators, not a peak.
Its script and core are byte-preserved under
`../mathematical_queries_v1/source_snapshot/v3/checks/`. Version 2 retains the
v1 generation identifier and measures state after every issue/reveal boundary,
including pending predictions. Former pending reports cover the fractions
retained in immutable history. It distinguishes final accumulators, final state,
and the temporal maximum; it does not measure peak RAM or transient arithmetic.

| Case / mode | V1 final accumulator | V2 final state | V2/V3 peak | Boundary observations |
|---|---:|---:|---:|---:|
| recurring_shortcuts / scalar_without_decision | 177 | 177 | 179 | 256 |
| recurring_shortcuts / scalar_with_decision | 233 | 233 | 233 | 256 |
| balanced_nonshortcut_null / scalar_without_decision | 204 | 204 | 210 | 256 |
| balanced_nonshortcut_null / scalar_with_decision | 249 | 249 | 253 | 256 |
| delayed_pending_tail / scalar_without_decision | 213 | 213 | 213 | 248 |
| delayed_pending_tail / scalar_with_decision | 244 | 244 | 244 | 248 |
| varying_stakes_actions / scalar_without_decision | 219 | 219 | 226 | 256 |
| varying_stakes_actions / scalar_with_decision | 274 | 274 | 274 | 256 |

Four peaks exceed the old final-accumulator counter. Inputs, complete issue
records, metrics and core audits match exactly between v1 and v2. The v2 source
and output were then preserved before a separately reviewed receipt repair.
Python dataclass equality had admitted Boolean/numeric aliases, and receipt
counter dictionaries were mutable. Version 3 uses strict scalar types,
immutable counter tuples and a registration-time canonical digest. Its malformed
receipt probes check evidence and all core states remain unchanged. Saved v1/v2
ordinary integer receipts were valid; this defect invalidated the broader
receipt-interface claim, not their recorded forecast scores. V3 retains the
same input population and exactly matches projected numerical reports, metrics,
core audits and measured fraction peaks. Receipt encodings/digests change as
intended, so complete v3 receipt byte equality is not claimed.

All completed run files and archived source hashes were checked before analysis.
No failed development execution was produced in these revisions. One source
patch initially failed context verification before applying and was retried;
it did not run a partially patched method. The independent review's defect
witness remains separate evidence. No source or result from v1/v2 was overwritten.

## Boundary conclusion

Nonvacuity means improvement over an explicitly named bound on the same
records. It does not establish favorable finite predictive performance,
asymptotic convergence, originality, or a reason to prefer fallible forecasting
to the cheap exact solver in this domain. The useful result is a checked
restricted forecast/decision/evidence integration with explicit finite limits.
This analysis introduces no parameter sweep, final controls, paid-computation
policy, contribution gate, P3-07 work or principal Research90 credit.
