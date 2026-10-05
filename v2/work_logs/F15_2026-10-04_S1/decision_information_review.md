# F15 review of the saved rectangular-regret diagnostic

Reviewer: **delegated ChatGPT (GPT-6 Astra Pro), F15 saved-data review**.
Disposition: **formula and all requested counts verified; no correction needed**.
Credited E minutes: **0**. This review adds no population, registered control,
confirmatory interval, F16 work, or novelty claim.

## Formula

For the Cartesian box of recorded action-cost intervals,

\[
\sup_{c\in\prod_i[l_i,u_i]}\left(c_a-\min_b c_b\right)
=\max_b\sup_c(c_a-c_b)
=\max\left(0,\max_{b\ne a}(u_a-l_b)\right).
\]

The self comparison is identically zero, even for a wide interval. Treating
it as `upper[a] - lower[a]` would be incorrect. The seventh action is the
exact fallback interval `[5/2, 5/2]`. The attainable same-law cost profiles
are contained in this box, so the recorded coherent regret cannot exceed
the rectangular regret for the **same selected recommendation**.

The reviewer used an independent calculation: enumerate the deterministic
corners of each saved interval box, compute `cost[a] - min(costs)` at each
corner, then maximize by action. This is algebra on saved endpoints, not
new experimental sampling. It checked **all 1,920 rows and 13,440 per-action
regrets**, covering 321 distinct interval boxes. All values agree with the
proposed formula and saved analysis. The selected/executed distinction was
also checked: **74 refused rows** have different recommendation and execution
indices, and the diagnostic uses the recommendation's coherent regret.

## Counts

| Saved descriptive outcome | Independently verified |
|---|---:|
| Certified decisions with no rectangle-certifiable action | 22 rows / 11 episodes |
| Such rows in each selective no-reacquisition method | 11 tailored; 11 exact intervals |
| Useful native rows with no rectangle-certifiable action | 16 rows / 8 episodes |
| Certified decisions with some numeric refusals | 80 |
| Certified decisions with all six numeric queries refused | 32 |
| Certified orders whose selected cost is numerically refused | 24 |

The first qualifying program illustration is **seed 15105**, `program_edit`,
tailored/no-reacquisition, selected index 5, order `(2,1)`. Its coherent regret
is **0**, while its best rectangular regret is **155/231**, well above 1/20.
Its original native receipt and useful-derivation disposition are unchanged.

These are method-row counts, with equivalent selective methods sharing the
same episodes. They describe the loss from relaxing joint feasibility to a
rectangle. They do not establish an advantage over an ordinary solver that
keeps the same-law fiber, or impossibility for every algorithm that also uses
additional program/source relations. The analysis already preserves this
descriptive scope.

The reproducible independent checker and machine record are
[`decision_information_review.py`](decision_information_review.py) and
[`decision_information_review.json`](decision_information_review.json). They
record source hashes and leave the original data, analysis, and report intact.
