# S13P: certificates for an exact price profile

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.

## Object and elementary construction

Fix finitely many nonempty prerequisite sets R_e, rewards r_e>=0 and strictly
positive base prices q_i. Let f(B)=sum_{e:R_e subset B}r_e, q(B)=sum_{i in B}q_i,
and Gamma(lambda)=max_B[f(B)-lambda q(B)] for lambda>=0. This is the closure
upper bound from [adaptive_bounds.md](adaptive_bounds.md), not in general the
actual value of information. Nonempty supports exclude a constant reward at
infinite price; such a constant could instead be separated explicitly.

The function f is supermodular: each completion indicator has increasing
marginal returns. For optimal sets A at lambda and B at mu>lambda, compare A
with A union B, and B with A intersection B. Optimality and supermodularity give

    mu q(B\A) <= f(B)-f(A intersect B)
                 <= f(A union B)-f(A) <= lambda q(B\A).

Positive q implies B subset A. Thus optimal sets at distinct prices are nested.
At ties multiple sets may be optimal, but all nondegenerate affine pieces can
be represented by at most m+1 nested sets. Gamma is convex, nonincreasing and
piecewise affine. It is zero after sum r/min q, since every nonempty purchase
costs at least min q. At zero, the all-bits set is optimal.

An ordinary exact flow oracle suffices to discover the profile. Between two
prices with optimal lines a_L-lambda c_L and a_R-lambda c_R, find their rational
intersection x. Query the oracle at x. If its value equals the two lines, those
lines describe the entire interval: every competing affine line is below the
appropriate line at both ends of each subinterval. If the oracle is strictly
above, its new optimal line splits the interval and recursion continues. If
both endpoint lines coincide, convexity and the feasible line show equality
throughout. Strict new pieces shrink the purchase set, so only O(m) oracle calls
are needed. This simple implementation pays separate cold flow calls; it is
not the strongest parametric max-flow algorithm.

## Small checker, continuum of prices

For each output interval [l,u], retain one cut and feasible allocations at its
two endpoints. Check every row, price capacity and prerequisite membership,
and equality between each endpoint flow value and this cut capacity. Capacities
are affine in lambda, so interpolating the endpoint flows gives a feasible flow
at every interior price. The fixed cut also has affine capacity. Flow/cut
equality therefore holds on the whole interval. The consumer need not trust
the recursive discovery algorithm or solve another flow.

The checked source captures immutable affine coefficients and endpoints.
Future queries check source version, exact nonnegative scalar price and interval
membership, then evaluate one line. A binary search costs O(log m) comparisons,
plus rational arithmetic. Graph semantic authentication is a separate obligation;
an arbitrary version string does not establish real-world identity.

Consequences include exact inverse queries: the first price at which Gamma<=d
is obtained by solving the relevant affine inequality. For d=0 the threshold
is max_{B nonempty} f(B)/q(B), an ordinary maximum-density closure ratio. It is
a sufficient all-adaptive no-purchase tariff under the acquisition hypotheses,
not necessarily the smallest tariff at which actual information is unprofitable.
The slopes encode the base price of the active optimizing set; they are
sensitivity information in the value function, not a probability distribution.

## Prototype and paid scope

[price_flow.py](price_flow.py) is a separate version exposing the old flow
control's bit-side cut. [price_profile.py](price_profile.py) builds profiles and
checks endpoint interpolation. [price01.json](price01.json) retains the fresh
seed, exact input graphs, certificates, queries, interpreter and source hashes.
All 2,158 small exhaustive queries on 32 graphs match. These are cheap
development checks, not independent theorem reconstruction.

| Supplied graph, 64 bits / 192 terms | Pieces | Cold oracle calls for setup | Build | Check | Setup + 128 lookups | 128 cold solves + checks |
|---|---:|---:|---:|---:|---:|---:|
| Overlapping supports | 20 | 39 | 74.315 ms | 10.168 ms | 85.027 ms | 272.912 ms |
| Eight support blocks | 30 | 59 | 102.889 ms | 14.731 ms | 118.175 ms | 255.037 ms |

One cold run per graph; no noise estimate, held-out transfer or external semantic
cost. Bad version, negative price and floating rather than exact price are
rejected. The service wins at this supplied repeated-query scope, while losing
for sufficiently few queries. It has no advantage over an identical ordinary
parametric service; optimized parametric flow and incremental flow remain
stronger unimplemented controls. The certificate/consumer split is the useful
integration being developed, not a claim to invent parametric optimization.

## Primary comparison scope

Gallo, Grigoriadis and Tarjan, *A Fast Parametric Maximum Flow Algorithm and
Applications*, SIAM J. Comput. 18(1), 1989, pp. 30-55,
[publisher abstract](https://epubs.siam.org/doi/10.1137/0218003), identifies
parametric flow with only constant-factor overhead in its stated algorithmic
setting. Only that abstract was read here. The linked Princeton 1987 report
returned HTTP 403; its search extract is not a read of the full theorem.
No complexity claim from that algorithm is imported into this implementation.
Our elementary nesting and certificate argument above is reconstructed locally.
