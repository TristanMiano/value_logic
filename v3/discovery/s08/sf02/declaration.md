# Shared unknown cost changes the witness frontier

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The previous star has one known center and independent unknown leaves, so
per-edge worst regrets add. Reverse the acquired set: one unknown center z
in {0,1,2} and several neighbors all observed at cost 1. Edge i has weight
w_i and two exactly-one components. Let k_i components choose the known
neighbor and K=sum w_i k_i, W=sum w_i. The exact joint quantities are

```math
R=\max(K,2W-K),\qquad U=4W-K.
```

Individual edge extrema cannot be maximized separately because they share z.
For weights 3 and 5, counts (0,2) give K=10, R=10, U=22. Balanced counts
(1,1) give R=8,U=24. At tolerance 10, an edgewise treatment would forbid
the first action: its separate regret bounds add to 16. Restricting each
count to 1 or 2 also misses it, since the smallest positive bias is 3.
The useful bias is signed, 5-3=2, and is justified by the shared source cost.

For tolerance tau>=W, minimize U by maximizing an attainable K<=tau. This
is bounded subset sum with **two copies of each weight**. The balanced K=W
is always feasible, and the remaining inequality K>=2W-tau follows from
tau>=W and K>=W. It is not enough to solve the earlier one-copy positive-bias
problem; that was valid only for independently varying unknown leaves.

More generally, let a queried vertex cover leave an independent set of
unknown vertices. Group every edge by its unknown endpoint. If the observed
neighbor costs c_i all lie in a common unknown interval [L,U], the two extreme
regrets of a group's count vector are

```math
R_L=\sum_i k_iw_i(c_i-L),\qquad
R_U=\sum_i(2-k_i)w_i(U-c_i).
```

Its joint regret is max(R_L,R_U), and its absolute upper cost is
2 sum_i w_i c_i + R_U. Different unknown groups vary independently in the
compatible set, so group regrets add exactly. Thus a local two-coordinate
frontier and an ordinary multiple-choice budget convolution can minimize
the absolute upper cost under a global regret tolerance. Resolved edges and
mandatory/common costs are added separately with their correct source
dependence. A probability model is unnecessary for these uniform claims.

This is ordinary aggregation of shared variables and multiobjective dynamic
programming, not a claim that signed cancellation or Pareto frontiers are
new. The research question is the cost of acquiring/checking this geometry
and using it to shrink the actual observation duty against an equal-interface
ordinary controller.

sf01 finite screen: degree 1..8, one unit vector and two seeded integral
weight vectors in 1..7 per degree (seed 8141630); all 3^degree count actions
and every integer tolerance 0..2W. Compare the two-copy planner with exact
count enumeration and the restricted one-copy-bias planner; record every
strict improvement and the weights (3,5), tau=10 boundary. Also test 20
seeded groups of degree 1..5 with integer interval endpoints L<U in 0..8,
known centers inside that interval and positive weights. Check both endpoint
regret identities against every integral unknown value. These are mathematical
checks, with no new physical acquisition. Freeze source and declaration first.
