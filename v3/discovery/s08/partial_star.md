# Act before a vertex cover is fully observed

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The shared-cost frontier does not require purchasing every neighbor first.
Consider the same original exactly-one star, with two components per edge,
positive integral edge weights w_i, and every cost in [0,H]. Let k_i count
components choosing leaf i. An unobserved leaf has interval [0,H]; an observed
leaf y has the singleton interval [y,y]. Denote those endpoints l_i,u_i.

If the center remains unknown, a fixed action has the exact bounds

```math
R_0=\sum_i k_i w_i u_i,\qquad
R_H=\sum_i(2-k_i)w_i(H-l_i),\qquad R=\max(R_0,R_H),
\qquad U=\sum_i w_i\{k_i u_i+(2-k_i)H\}.
```

Regret is a convex piecewise-affine function of the joint cost vector, since
it is fixed action cost minus the minimum of all feasible affine action costs.
Its maximum over the box occurs at a vertex. At center 0, each leaf's regret
is k_i w_i y_i and is maximal at u_i. At center H, it is
(2-k_i)w_i(H-y_i) and is maximal at l_i. The shared center's two maxima are
taken **after** summing its incident terms. Nonnegative action coefficients
make U exact at every coordinate's upper endpoint. A group of unresolved
edges is therefore still tractable without pretending their extrema vary
independently.

Unlike the fully observed-neighbor case, U is not a constant plus R_H:
the difference depends on k when l_i<u_i. Retaining only one of the previous
two coordinates can lose an action needed against replacement. The correct
ordinary DP retains the smallest U and a witness at every exact (R_0,R_H),
with three transitions k=0,1,2 per edge. For a requested tolerance tau, prune
any state whose either endpoint regret exceeds tau: every later contribution
is nonnegative. The surviving final state with least U solves the uniform
repair duty. The state space is pseudopolynomial; an explicit cap may return
UNRESOLVED, never an unwarranted infeasibility conclusion.

If the center is observed at z, each unknown leaf can vary independently.
The per-edge quantities are

```math
r_i(k)=\max_{y\in\{l_i,u_i\}}
w_i\{k y+(2-k)z-2\min(y,z)\},\qquad
u_i(k)=w_i\{k u_i+(2-k)z\}.
```

Convolve exact sum r_i with minimum sum u_i, pruning sums above tau. Resolved
leaf intervals are treated by the same formula. This also supplies a complete
action when all costs are acquired. Mandatory/common unknown anchor A cancels
from repair-only regret, but contributes max A to U and min A to the lower
bound on the optimum. Combined repair regret is max(R,U+max A-price);
replacement regret is max(0,price-min A-min OPT_star).

**ps01 screen before paid use:** degrees 1..4, unit weights and one seeded
weight vector per degree (seed 8141650), H=4. Each node is unobserved or
observed at 0,2,4. Check every partial state, all 3^degree actions, and targets
at each attainable regret plus adjacent integer values. Compare the DP's
least upper cost with exhaustive actions. Independently evaluate fixed-action
regret and upper cost on every box corner; use all interior values on selected
small states. State-cap exhaustion is tested and must not be called infeasible.
This is a finite development screen with zero physical audits. Source/action
checks and physical acquisition costs belong to any later service declaration.
