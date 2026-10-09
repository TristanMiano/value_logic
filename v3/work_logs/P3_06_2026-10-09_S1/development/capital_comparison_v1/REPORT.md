# Ordinary capital-sum development comparison

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.

This separately versioned ordinary benchmark instantiates the nonnegative forecast-continuous
supermartingale method in [Vovk (2007), §§2–3](https://arxiv.org/pdf/0708.1503).
Expert, signed tent and centered smooth-action components share one scalar report.
The exponential and logarithmic calculations use outward exact rational enclosures.
The source module records a capital allowance, which is different from the K29 squared-potential allowance.

The declared comparison reuses the first 32 issue ticks of each existing development tape.
It fixes the horizon, stake/slope envelopes, equal prior budgets, rational rate rule and numerical caps
before this run. Every method is scored only on the labels admitted by the same tick-32 cutoff.
Pending answers, including ones admitted later in the original full run, remain unscored here.
This later development comparison is not a final prospective evaluation or a priority claim.

| Case / method | Settled / pending | Brier per weight | Brier regret | Mixed-action regret |
|---|---:|---:|---:|---:|
| recurring_shortcuts / ordinary_capital_sum | 32 / 0 | 0.026581 | 0.850586 | -27.375000 |
| recurring_shortcuts / scalar_without_decision | 32 / 0 | 0.044651 | 1.428819 | -21.695312 |
| recurring_shortcuts / scalar_with_decision | 32 / 0 | 0.286194 | 9.158199 | 1.953236 |
| recurring_shortcuts / ordinary_brier_aa_binary64 | 32 / 0 | 0.016892 | 0.540557 | -27.366277 |
| recurring_shortcuts / ordinary_fast_exact | 32 / 0 | 0.000000 | 0.000000 | -28.000000 |
| balanced_nonshortcut_null / ordinary_capital_sum | 32 / 0 | 0.257374 | 0.235971 | 1.897217 |
| balanced_nonshortcut_null / scalar_without_decision | 32 / 0 | 0.292465 | 1.358890 | 9.158691 |
| balanced_nonshortcut_null / scalar_with_decision | 32 / 0 | 0.284791 | 1.113313 | 9.241352 |
| balanced_nonshortcut_null / ordinary_brier_aa_binary64 | 32 / 0 | 0.258996 | 0.287863 | 1.031378 |
| balanced_nonshortcut_null / ordinary_fast_exact | 32 / 0 | 0.000000 | -8.000000 | -28.000000 |
| delayed_pending_tail / ordinary_capital_sum | 29 / 3 | 0.224023 | 7.918472 | -29.125000 |
| delayed_pending_tail / scalar_without_decision | 29 / 3 | 0.277980 | 13.799868 | 11.478516 |
| delayed_pending_tail / scalar_with_decision | 29 / 3 | 0.290804 | 15.197652 | 46.699710 |
| delayed_pending_tail / ordinary_brier_aa_binary64 | 29 / 3 | 0.221570 | 7.651165 | -37.952534 |
| delayed_pending_tail / ordinary_fast_exact | 29 / 3 | 0.000000 | -16.500000 | -102.000000 |
| varying_stakes_actions / ordinary_capital_sum | 32 / 0 | 0.258997 | 1.079641 | -3.875000 |
| varying_stakes_actions / scalar_without_decision | 32 / 0 | 0.259732 | 1.167845 | 0.086670 |
| varying_stakes_actions / scalar_with_decision | 32 / 0 | 0.293796 | 5.255547 | -13.533586 |
| varying_stakes_actions / ordinary_brier_aa_binary64 | 32 / 0 | 0.259969 | 1.196281 | -15.734128 |
| varying_stakes_actions / ordinary_fast_exact | 32 / 0 | 0.000000 | -30.000000 | -121.000000 |

The matched ordinary K29 copies remain identical to their scalar counterparts and are omitted here.
Exact solver work and the binary64 AA remain available ordinary comparisons. No external authentication,
hard resource bound, unbounded-stake constant regret or guarantee for sampled hard actions is claimed.
The capital construction has its own finite-horizon calibration/action constants. More copies add their
individual constant expert-regret bounds; no free delayed-feedback theorem is assumed.
Complete exact certificates, per-copy states, intervals, prior masses and rate choices are in the JSON files.
