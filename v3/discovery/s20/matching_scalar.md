# Sharp quadratic scalar output over factorially many source components

Codex (GPT-6), October 28, 2026. Separate DEVELOPMENT. This extends the output
review, not the frozen V19 contribution event. Existing bottleneck-assignment
and polytope literature must be compared before any novelty judgment.

## Distinct bottleneck values of all perfect matchings

For n>=2 let M be the diagonal perfect matching of K_(n,n), and H the cyclic
shift matching i -> i+1 modulo n. Order all n^2 edges as follows:

1. All edges outside M and H, in any fixed order.
2. One selected edge of H.
3. The remaining n-1 edges of H.
4. The n edges of M, in any fixed order.

Give edges the distinct positive weights1,...,n^2 in that order. A matching's
value is its smallest selected edge weight. Every edge in group1 can be that
smallest edge: identify each M edge with a vertex of a directed graph. The
remaining H arcs form a directed Hamiltonian cycle. Any additional arc e
has a return path on that cycle, yielding a directed cycle containing e;
use its edges and the M loops on other vertices to obtain a perfect matching.
All other selected edges appear later in the prescribed order. Thus each of
the n^2-2n group1 weights is attained.

The first H edge's weight is attained by H itself. After deleting that edge,
the remaining H arcs form a directed path. Together with the M loops they
have no nontrivial directed cycle, so their only perfect matching is M.
None of those n-1 remaining H weights can be the smallest selected weight.
The smallest M weight is attained by M, and no larger M weight can be a
minimum because the remaining feasible matching is still M. The number of
distinct values is therefore

    (n^2-2n)+1+1 = (n-1)^2+1.

For n=1 it is one. Together with face_chain.md this is the exact maximum
for the complete-matching configuration family. This is a constructive
comparison with n! source configurations, not an asymptotic lower bound on
all whole-range algorithms.

## Realizing the count with full-dimensional noisy receipt sources

Use n independent vectors y_i in R^n with base polytope

    0 <= y_ij <= 1,  1-eta <= sum_j y_ij <= 1+eta.

For each receipt j require max_i y_ij in [1-epsilon,1]. This is the V19
minimum convention after replacing each coordinate by its negative. Set
eta=epsilon=1/(100*n^2), and let f_i(y_i)=sum_j w_ij*y_ij with the weights
just constructed. Every response is positive on this source for n>=1.

Since 2*(1-epsilon)>1+eta, no block can witness two receipts. With n receipts
and n blocks, every admitted witness assignment is a perfect matching and
each block has exactly one witnessing coordinate. All n! assignments are
feasible (use the corresponding basis vectors). Distinct assignment cells
are disjoint: their intersection would give some block two witnessing
coordinates. Each cell is a nonempty compact convex product and the cells
are finitely many, so there are exactly n! source components.

These are not zero-volume cells. For n>=2, set the assigned coordinate to
1-epsilon/2 and each other coordinate to epsilon/(2*n). Every coordinate
and the sum constraints are strict, as is the receipt upper-witness condition.
The cell contains an open neighborhood. For n=1, an interior value strictly
between1-epsilon and1 also suffices.

For a local slice assigned receipt j, its nonassigned coordinate sum is at
most eta+epsilon, and its assigned coordinate differs from1 by at most
epsilon. With all weights at most n^2,

    abs(f_i(y_i)-w_ij) <= n^2*(eta+2*epsilon)=3/100.

The local scalar image is a closed interval containing w_ij and has positive
width: small admissible changes in the assigned coordinate already change
the strictly positive affine readout. Distinct edge intervals are disjoint,
ordered by edge weight, and separated by at least47/50. In every matching,
the edge with smallest weight therefore also has the smallest entire local
interval. Its branch-minimum image is exactly that edge interval. Consequently
the full scalar image has exactly (n-1)^2+1 positive-width components, while
the admitted source has n! full-dimensional components. Noise is nonzero but
decreases as n grows; this is not a fixed-tolerance asymptotic claim.

## Ordinary polynomial route in this special case

The singleton local images require at most2*n^2 LP extrema. For an anchor edge
(i,j), delete its row and column and find the largest bottleneck upper value
of a perfect matching in the remaining graph. Thresholding the upper endpoints
and testing ordinary bipartite perfect matching computes this cap. Clip the
anchor's local interval by it and merge the at most n^2 intervals. Retain an
attaining residual matching for source reconstruction. For n=1 the residual
cap is positive infinity. This is the same anchor proof specialized to a
standard bottleneck-assignment oracle; it makes no claim to invent matching.

Even a simple implementation using binary search over the finite upper
endpoints and an augmenting-path matching algorithm is polynomial. Improving
that matching routine, proving a new general matching algorithm, or benchmarking
it is unnecessary to this observation. If some singleton slices are empty,
the same graph method handles missing edges, but the complete-case sharpness
construction no longer describes that particular graph.

This branch explains a real representational distinction: a large number of
source alternatives need not force a large minimum-value output. It also
identifies a cheaper ordinary special case. Neither fact changes the validity
or the fixed verification event of V19-R/v1.
