# Joint error guards: useful correlation, and the cost of checking it

**DEVELOPMENT — Codex (GPT-6), October 13, 2026 UTC.**
Continuation of [cost-region improving maps](improving_maps.md). The
max-sum tree calculation below is ordinary dynamic programming. Its role is
to make the new approximate-reduction guard explicit and paid, not to claim
a new graphical-model algorithm.

## 1. A correlated guard can improve on separate error allowances

For independent action components j and one common cost source w, the error
of forcing each component to its nominated representative is
$`e(w)=\sum_j e_j(w)`$, where each e_j is its nonnegative excess over its
best original choice. The exact uniform guard is
$`\sup_{w\in W}\sum_j e_j(w)`$. Summing the separate uniform guards is
sound but can be strictly larger. A common source event or mode identity must
be retained; replacing it by independent per-component sources loses this
correlation and can make a useful tolerance reduction appear unavailable.

Example: two binary action components have excesses
$`\max(0,t)`$ and $`\max(0,-t)`$, for the same unknown
$`t\in\{-1,1\}`$. The joint map error is exactly one, whereas the sum of
the separate worst errors is two. Both errors are nonnegative, so this is
not cancellation of actual incurred regret. It is incompatible worst cases.

## 2. Exact guard checking contains weighted maximum cut

Let an undirected graph have nonnegative edge weights a_ij and independent
publicly unresolved binary source bits t_i. For each edge create two
independent binary action choices. The first has costs a_ij*t_i and
a_ij*t_j; the second has the same costs in reverse order. All cost features
are nonnegative. The proposed map forces the first choice in both components.

The representative's edge cost is a_ij*(t_i+t_j). The original optimum on
that edge is 2*a_ij*min(t_i,t_j). Hence its exact error is

```math
e_{ij}(t)=a_{ij}|t_i-t_j|,
\qquad
e(t)=\sum_{ij}a_{ij}|t_i-t_j|.
```

Maximizing this over the public independent binary cost source is exactly
weighted maximum cut on the supplied graph. This is an explicit reduction:
the logical action source itself is only a product of two-way choices, and
the map's feasibility is trivial. The difficult duty is its coupled cost
guard. A proposal of an "optimal guard" without its solver, certificate and
bill would hide a substantive computation. The definition above is enough
to establish the reduction, without importing a solver-complexity claim.

On a triangle of unit edges, the two-direction separate allowances total six,
the per-edge joint allowances total three, and the exact global guard is two.
All three numbers have different correlation scopes. None is an observed
realized regret until actual source values are obtained.

## 3. Trees admit compact exact upper certificates

Restrict the source graph to a tree and let each node have a nonempty admitted
finite support Q_i. Here Q_i is {0}, {1} or {0,1}, so paid exact observations
can restrict a node without changing the graph. Root the tree. For every
parent-child edge i,j retain a message

```math
M_{j\to i}(u)=\max_{v\in Q_j}
\left(a_{ij}|u-v|+\sum_{k\text{ child of }j}M_{k\to j}(v)\right),
\quad u\in Q_i.
```

The root's maximum sum of incoming messages is the exact joint guard.
Induction from the leaves proves this: at fixed parent value the descendant
subtrees have disjoint independent source coordinates, so their maximizing
assignments can be combined. The calculation takes
$`O(\sum_{ij}|Q_i||Q_j|)`$ arithmetic after graph/source admission; this
does not imply constant bit cost for large coefficients.

The producer saves every message and an attaining compatible assignment.
A separate checker need only verify that each parent-value message is at
least every corresponding child-value expression, and that the root bound
dominates its supported root values. This proves an upper bound even if the
producer overestimates a maximum. Checking the witness's cut cost equals the
bound establishes exactness. No unobserved source bit is learned by the
witness: it is a compatible worst-case assignment, not the actual hidden
assignment. Charge message production, checking, graph validation and storage.

For a general graph a spanning-tree value is a lower diagnostic, not an
upper guard for the omitted edges. A valid cheap upper adds the sum of the
omitted edges' independent maxima, or obtains a separately checked stronger
relaxation. Cycles cannot silently be ignored.

## 4. Refinement and a prospective finite screen

A truthful audit restricts some Q_i and can only reduce the exact guard.
Changing costs or expanding supports requires a new guard. Recompute and
check the changed messages; there is no free validity transfer merely from
an old root scalar. An incremental implementation could reuse unaffected
subtrees, but that implementation and its exact dependency bindings are
additional work, not assumed savings here.

Before execution: generate 32 small trees (n=2..9 cycling), positive integral
weights 1..4, and nonempty binary node supports using seed 261013. Check each
initial source and every compatible single-node audit refinement against
exhaustive source enumeration. Also test a triangle's correlation gap, and
larger n=32,128,512 cases using an independently checked attaining message
certificate. Include tampered messages/witnesses and a cycle rejection.
These are conditional guard computations, **zero new source audits**. They
establish no cost-learning service advantage or material promotion claim.
