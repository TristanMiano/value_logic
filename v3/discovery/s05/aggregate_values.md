# Joint value bounds from shared pair evidence

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; an additional construction within the parity-calibration branch.

## Why retain an aggregate object?

The [single-target closure](calibration_branches.md) is sharp, but different
targets can require different worst-case laws. A value objective usually sums
several errors. It can therefore be useful to retain a certificate for that
whole objective instead of summing individually sharp bounds. This direction
is separate from the acquisition cost of the required pair evidence.

Let `Y_v in {-1,+1}` be common error signs. A graph H of weighted prediction
relations has loss

```text
loss_H(Y) = sum_(ab in H) r_ab * 1[Y_a != Y_b].
```

Suppose the calibration graph G warrants `E 1[Y_a!=Y_b] <= u_ab`.
Any nonnegative coefficients x on G and any pointwise checked inequality

```text
loss_H(Y) <= sum_(ab in G) x_ab * 1[Y_a != Y_b], for every Y,
```

give the expected-loss certificate `E loss_H <= sum x_ab*u_ab`.
The coefficients can be proposed using the calibrated bounds, then checked.
The common validity event covers later choices of H and coefficients that
are fixed independently of the new task's hidden signs. Choosing coefficients
after observing that task's signs is a different conditional problem.

## A cheap sum-of-squares certificate

Write L_H for the graph Laplacian of the weighted loss and L_x for that of
the nonnegative coefficients on G. Because each squared sign difference is
four times its disagreement indicator, it is sufficient that

```text
L_x - L_H is positive semidefinite.
```

A supplied rational factorization of this difference into nonnegative
weighted outer products provides a checkable certificate. This is ordinary
quadratic-form domination applied to the shared error source, not a claim of
new spectral graph machinery. The Laplacian identity and the conventional
use of quadratic-form comparisons were checked in Spielman and Srivastava,
[Graph Sparsification by Effective Resistances, sections 1.1 and 2.1](https://arxiv.org/pdf/0803.0929).
No sparsification algorithm or its runtime guarantee is imported here.
Optimization of such coefficients, including
its setup and checking cost, remains a prospective development direction.
It need not recover the exact binary-cut optimum.

An even simpler exact identity works when G is complete bipartite with equal
parts A and B of size k, and H is the complete graph on those 2k vertices.
For one sign assignment, let a and b count negative signs in the two parts.
If C counts cross-part disagreements and W within-part disagreements, then

```text
C = k*(a+b) - 2*a*b,
W = k*(a+b) - a*a - b*b,
C-W = (a-b)^2 >= 0.
```

Therefore `loss_H=C+W <= 2*C`. If every measured cross-pair has error bound p,

```text
E loss_H <= min(k*k, 2*k*k*p).
```

The first cap is the largest cut of a complete graph on 2k vertices. For
p<=1/2, summing individual shortest-path bounds instead gives
`(3*k*k-2*k)*p`, before any whole-objective cap.

For k=3 and p=1/5, the individual sum is 21/5=4.2 whereas the joint certificate
is 18/5=3.6. The latter is sharp: assign mass 1/20 to each of the nine cuts
containing one vertex from A and one from B, and the remaining 11/20 to the
all-equal assignment. Each observed cross-pair disagrees in four such cuts,
so has error 1/5. Each nonempty cut has eight total disagreements, giving
9*(1/20)*8=18/5. If a root must have positive sign, complement its negative
worlds; all pair disagreements remain unchanged.

## What this changes in the search

There are now two useful operations on the same pair evidence: sharp
single-parity closure, and cheap aggregate certificates that exploit a
shared worst-case law. A direct policy-contrast estimator remains available
and may be tighter or cheaper when only one fixed value comparison matters.
The graph certificate is attractive when many related value queries reuse
the same source and a small algebraic certificate is already available.

The example is a supplied-bound construction, not a measured calibration
gain. General Boolean cut inequalities are richer than positive-semidefinite
domination; the earlier odd `K_(2,3)` example cannot be justified by blindly
reusing the equal-part identity. Adaptive deployment, arbitrary higher-order
targets and a complete low-cost planner are not established here. The next
useful question is whether an actual query menu has this aggregate structure
and whether its certificate saves enough repeated work to repay acquisition.
