# Calibration forced by the action duty

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
Constructive response to the cost of [the full Markov likelihood service](ms01/results.json).
Bernoulli calibration, confidence-set stopping and finite policy comparisons
are ordinary methods. The proposed connection is that the **logical action
duty forces an informative adjacent observation** on a predictable event,
making a cheap parameter sample available from purchases already required
for the repair.

## A valid transition sample inside every suitable request

Assume the stationary symmetric homogeneous Markov source from
[the model declaration](correlated_models.md), with one fixed rho and fresh
rows. The first queried vertex I is selected using prior rows and public
metadata, before any current-row value is observed. Its indicator is middle
with probability one-half, regardless of I and rho.

If that first indicator is middle, every still-unqueried neighbor is mandatory
for a zero-regret action certificate. Query one adjacent vertex J next, chosen
using only the known first index/value and prior information. Under this
source,

```math
\Pr(X_J=\mathrm{middle}\mid X_I=\mathrm{middle},I,J,\text{prior history})
=\rho.
```

The stationary symmetric chain is reversible, so either adjacent direction
has the same conditional repeat probability. There is no other current-row
observation to bias this local conditional law. Root selection may adapt
across requests; the statement remains valid. Every row whose first query
is middle therefore contributes one Bernoulli(rho) sample, and these samples
are valid at their adaptively selected arrival times. Rows whose first query
is extreme contribute no transition sample. They remain paid requests and
cannot be erased from the cost denominator.

The existing stack policy already executes an adjacent forced query next
after a middle first root: its left neighbor if present, otherwise its right
neighbor. Both receipts are needed by that path's zero-regret duty. Statistical
reuse adds computation and retention but **zero additional physical audits**.
This does not claim that arbitrary adjacent pairs selected later in a row
are unbiased. Additional observed context can change their conditional law.

If n=1 there is no edge or forced neighbor, so this mechanism supplies no
sample. Nonstationary, nonsymmetric, nonhomogeneous or outside-menu sources
require a new derivation. A graph with cycles does not inherit the chain/tree
transition identity merely because its edges look similar.

## Stop learning when the decision is already identified

For a fixed prepared bank of policies pi and model menu k, obtain **exact**
expected physical-fee values V(pi,k), not only upper bounds. Selected-policy
Bellman equalities can be checked in O(n^2) using independent transition
matrix arithmetic; no optimization over alternative roots is needed to prove
the value of the selected policy. Mark its optimal-model support as

```math
A_\pi=\{k:V(\pi,k)=\min_{\pi'}V(\pi',k)\}.
```

If a warranted confidence set C is contained in some A_pi, that policy is
optimal within the prepared bank for every remaining model. Further model
identification cannot improve that same bank's expected physical fee. Freeze
C and pi and stop statistical updates, while continuing to buy and check
every receipt needed for each action. This relies on the fixed source/model
menu, fees, bank and task duty. A source/fee/bank change invalidates the
stopping certificate. It is not permission to stop monitoring a changing
external system under an unchanged label.

Stopping before identifying rho exactly is permitted and meaningful. The
confidence set's all-time coverage makes the data-selected stopping rule
valid; the true fixed model remains in the frozen set on the same event.
If no common minimizing policy exists yet, continue the cheap transition
calibration and use a policy minimizing its largest value over C. Include
every update and failed-to-resolve sample in the invoice.

## Prospective development ablation

Preserve ms01 in full. Reuse its exposed nine environments, seeds and rows
as DEVELOPMENT to isolate this changed learning mechanism. First independently
check the policy-bank values with equality, compile A_pi masks, and compare
the first-middle/next-neighbor sample law against full small-source enumeration.
Then run the new learner and the identical ordinary controller. Use exact
rational time-uniform Hoeffding intervals for a single Bernoulli parameter
with alpha=1/20, intersecting the fixed rho menu. Stop on a common optimal
policy cell and retain its source/cost/bank binding. Include one estimator
that continues to exact menu identification as a diagnostic of unnecessary
learning, not a weak sole baseline.

Report actual physical fees, sample counts, stopping rows, retained model
sets, overhead and bank preparation. Compare with the full-likelihood learner
and static robust menu policy. A reduced learning bill or model count alone
does not establish a complete-cost win or independent confirmation. All
original-source actions still require exact receipt-based checks.

Before the first run, add a second estimator: a finite-menu Bernoulli
mixture-likelihood confidence sequence, with weights initially one and one
update by r or 10-r per forced-pair repeat/nonrepeat sample. Retain model k
when 100 times its weight is at least the sum of all five weights. The same
mixture likelihood-ratio argument as the full observation learner supplies
all-time coverage at alpha=1/20. Exact integer arithmetic and gcd reduction
avoid numerical likelihood underflow. Compare both this estimator and the
single-parameter Hoeffding estimator, each with a common-cell stopping arm,
an identical ordinary arm, and a continue-to-singleton diagnostic. All six
arms pay their own setup and execution costs. The per-arm confidence claim
does not become a joint 95 percent claim over every experimental arm.
