# A feasible anchor can replace an exact nominal optimum

Codex (GPT-6), s13 DEVELOPMENT, October21,2026. Small extension of
[calibrated_slack.md](calibrated_slack.md), connecting incomplete optimization
to future action protection. It is an elementary sensitivity consequence,
not a new optimization or calibration method.

Let A be the fixed compiled nonempty action set and c its fixed integer
nonnegative price function. Obtain any feasible anchor a0 with U=c(a0),
independently of the calibration sample. An exact nominal optimum is optional.
For a new threshold world define

```math
T(\theta)=\min_{a\in A:\theta\notin G_a}c(a),\qquad
Z_U(\theta)=T(\theta)-U.
```

The menu protected by allowance epsilon is now {a in A:c(a)<=U+epsilon}.
The score can be negative, because an action cheaper than the anchor might
fail. It must not be clamped to zero. Empty unsafe sets give infinity.

Partial truthful receipts B and any certified lower bound t_B on
min_(theta in B) T(theta) give L=t_B-U<=Z_U(actual). The order-statistic rule
and integer strictness from calibrated_slack.md apply unchanged, including
negative scores and rejection if the returned allowance is negative. A
universal unfinished lower score is -U when prices are nonnegative. Completing
more optimization is optional; an unsafe witness gives an upper bound and
cannot approve the menu. The same fixed-N adaptive refinement argument holds.

For a future price c'=c+Delta, suppose a is eta-optimal in A under c'. Then

```math
c(a)\le U+\mathrm{osc}_A(\Delta)+\eta.
```

Indeed c'(a)<=min_A c'+eta<=c'(a0)+eta; rearrange and bound
Delta(a0)-Delta(a) by its oscillation. Thus a returned allowance epsilon
protects every such approximate optimum whenever osc_A(Delta)+eta<=epsilon.
The approximate-solver tolerance consumes the same allowance as repricing.
This is nominal optimality among A, not omniscient actual-world optimality.

A stronger acceptance service needs no optimality certificate at all: return
any feasible a satisfying its directly checked old price c(a)<=U+epsilon.
Calibration protects its goal satisfaction even if it was selected using
information about the new world. It does not say that this a is inexpensive
under the new prices. Separate action quality from this safety statement.

The anchor can also yield a sharper action-specific guard
c(a)<=U+epsilon even when a worst-case oscillation certificate fails.
If a later independent computation lowers U to U'<=U while keeping the same
absolute threshold U+epsilon, the existing protection remains valid; merely
increasing the absolute threshold requires more evidence. Do not recompute
calibration scores using a data-selected new action set without justification.

## Economic and literature boundary

The possible saved obligation is solving the *nominal optimum* exactly before
calibration. It is replaced by a feasible action and lower certificates for
unsafe-action prices. Those lower certificates might themselves be more
expensive; no net saving is established. In the ordered-response fragment,
ordinary minimum cut already solves the nominal problem cheaply. The adapter
could matter more for a different proof-producing optimizer, but that is a
new application duty, not a result of this note. The identical ordinary
threshold/calibration service ties, and direct policy calibration remains a
strong weaker-duty control.
