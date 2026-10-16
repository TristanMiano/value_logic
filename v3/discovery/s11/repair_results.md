# Evidence-enabled repair: first compact solver results

Codex (GPT-6), DEVELOPMENT. [Prospective declaration](safe_lp_plan.md),
[derivation](safe_revision.md), [exact example and target extension](safe_example.md).
rp01 completed all seven declared cases on their first attempts. All ten
small-case solver arms matched full-world LP optima numerically; repaired
controller upper bounds independently matched explicit world/mask enumeration.
The exact 65/64 lower bound from the two-bit argument is also recovered by the
dual certificate. This is same-model constructive screening, not independent
confirmation or a test of a natural application population.

| Case | m/r/H | Full-query regret enclosure | No-query regret enclosure | Certified reduction at least |
| --- | --- | --- | --- | --- |
| 0 | 2/1/2 | [1.015625,1.015625120] | [1.75,1.75] | 41.9642% |
| 1 | 5/2/3 | [1.31666666665,1.316666981] | [4.09374999998,4.093750299] | 67.8371% |
| 2 | 6/2/4 | [1.11785714283,1.117857695] | [3.49999999998,3.5] | 68.0612% |
| 3, changed target | 4/2/3 | [2.8125,2.8125] | [4.75,4.75] | 40.7894% |
| 4, cap zero | 2/1/0 | [1,1] | [1,1] | 0% |
| 5 | 41/3/5 | [19.45507812499,19.455082352] | [23.09999999995,23.100014687] | 15.7788% |
| 6, changed target | 41/3/5 | [18.65937499999,18.659398848] | [33.25,33.25] | 43.8815% |

Decimals are outward display enclosures; exact rational JSON is authoritative.
Reduction uses 1 minus full-query upper divided by no-query lower, not a
comparison of two unverified numerical optima. Each no-query restriction uses
the same full, operationally admissible comparator as the full-query arm.
Case 4 changes the cap for both controller and comparator, so its value must
not be compared to case 0 as an improvement.

Case 5 has 13,400 variables, 14,152 inequalities and 50,414 matrix nonzeros.
The exact upper separator evaluates 54 networks with 10,496 states and 14,098
edges. Case 6 has 3,377 variables, 3,019 inequalities and 13,161 nonzeros;
15 of 27 histories have no usable terminal menu (including unreachable ones).
These are dimensions/operation counts, not full computation invoices.
The largest upper/lower gap is below 0.000023848. The method enumerates histories
and query cells but does not enumerate 2^41 original worlds or all policy trees.

Source hashes: repair_core.py
`3cb1b41b1727deba8ad757e0defcbcfde2e65dc928c816938edebe7d28076efd`;
repair_lp.py
`20b57ef73da8b31af30eddbfef188095f04c46bcb188cdf9ea210a38490bab7f`.
They are executed scientific versions and must retain their bytes.

The useful consequence is an implementable compact controller with a checked
regret interval and constraint-valid randomized repairs. Its operations are
ordinary flow, dynamic programming and minimax optimization. An equivalent
ordinary contingent-repair optimizer ties; no benchmark against an optimized
external planning implementation or priced source acquisition was run.
