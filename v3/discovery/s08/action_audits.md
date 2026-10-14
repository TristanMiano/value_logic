# Action-adaptive audits: residual cut uncertainty

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
This derives a different use of the cost source in [joint guards](joint_guard.md).
Ordinary weighted graph coverage and dynamic programming are intended strong
controls. The prospective claim is a connection between an exact robust
decision duty and a paid observation plan, not a new graph optimization method.

## Source and duty

Let G be a finite undirected graph with nonnegative edge weights a. Each
vertex i has an unknown bit t_i; the admitted source contains every bit vector.
An exact audit of vertex i costs c_i>0 and truthfully reveals its bit. Each
edge ij contributes two independent binary action components. In each,
choosing endpoint i costs a_ij*t_i and choosing j costs a_ij*t_j. The hard
source forces exactly one choice in each component, with no cross-component
constraints. This product structure must be read and checked from the original
source; it is not inferred from a few feasible assignments.

An output is a fixed feasible action after some audited set Q and its observed
values. Its regret is against the best feasible action at the same actual bit
vector. The certificate must bound regret uniformly over all remaining
compatible bits. Initially no probability law is stipulated. A worst-case
witness is not an acquired actual bit vector.

## Exact robust value after an arbitrary audited set

For an edge with an audited endpoint i, choose i twice if t_i=0. If t_i=1
and j is not audited, choose j twice: its cost is no greater than i's. If both
are audited, choose an endpoint of minimum value. Every such edge is optimal
for every compatible completion, so its regret is zero.

For an edge whose endpoints are both unaudited, choose each endpoint once.
Its regret is a_ij*abs(t_i-t_j). These choices establish the upper bound

```math
R^*(Q)\leq \mathrm{MaxCut}(G[V\setminus Q]).
```

For the reverse inequality, fix any feasible output, including a randomized
one evaluated by its expected cost. On an unaudited edge let k in [0,2] be
the expected number of selections of its first endpoint. For complementary
remaining bit vectors t and 1-t, the two regrets on this edge sum to
2*a_ij*abs(t_i-t_j), irrespective of k. Choose t attaining the maximum cut
of the remaining induced graph. The average of the output's regret under
these two compatible completions is at least that maximum cut; audited-edge
regrets are nonnegative and can only increase the average. One completion
therefore has at least this regret. Consequently

```math
R^*(Q)=\mathrm{MaxCut}(G[V\setminus Q]).
```

The result holds for **every** observed outcome on Q. In particular, logical
proof search cannot lower this residual minimax duty below the value above:
the obstruction is genuine missing cost information, after granting the full
logical source. Extra constraints on compatible bits would change the result.

## Optimal audit planning on a forest

If G is a forest, every remaining induced graph is bipartite, and its maximum
cut equals its total edge weight. Thus Q is sufficient for tolerance tau iff
the total weight of edges with neither endpoint in Q is at most tau. The
cheapest sufficient fixed plan is weighted partial vertex cover on the forest.
For tau=0 this is weighted vertex cover.

Outcomes cannot improve the worst-case acquisition cost: every leaf of any
adaptive policy must contain a sufficient Q, whose cost is at least the
minimum sufficient fixed-set cost. Purchasing that minimizing fixed set
attains the bound on every outcome. This argument requires deterministic
worst-case cost and a pathwise uniform regret certificate; it is not a claim
about expected-cost policies under a learned prior or probabilistic stopping.

For integer edge weights and tau, root each tree. Define F_i(x,r) as the
minimum audit cost inside i's subtree, with i selected iff x, and exactly r
uncovered internal edge weight. Initialize F_i(x,0)=c_i*x. Merge child j by
adding F_j(y,s) and replacing r by r+s+a_ij*(1-x)*(1-y). Discard r>tau.
The root minimum over x and r<=tau gives an attaining set. Nonnegative edge
weights justify discarding those states. This is ordinary tree knapsack,
pseudopolynomial in tau; it is not a polynomial bit-complexity claim.

Every covered edge then receives the observed-value rule above, and every
uncovered edge the balanced action. A small checker can verify the source,
audit receipts, selected set, action choices and the residual edge-weight sum.
That suffices for the regret guarantee even without trusting planner
optimality. A separate exhaustive subset check on small instances can test
the planner's finite optimality. Charge planner, checking, action construction,
all actual audits, retained receipts, exports and ordinary controls.

## Prospective implementation screen

Build the original exactly-one CNF for each edge component and check its
factorization and ordered cost map. Admit no extra clauses. Compare a tree
knapsack planner, an independently specified ordinary graph planner, a
weight-per-audit-cost greedy cover and full bit identification. Enumerate
small tree/source outcomes, freeze all designs before acquisition, and retain
prefix receipts before each possible interruption. Also include a cycle with
an explicitly checked maximum-cut bound, and reject the forest shortcut on it.
Use small n<=7 for exhaustive source and audit-set comparisons, then n=32/128
only with a directly checked sufficient set. Cost conclusions must include
the planner's work; a reduced audit count alone is not a complete benefit.

This extension remains DEVELOPMENT and does not redefine F01.
