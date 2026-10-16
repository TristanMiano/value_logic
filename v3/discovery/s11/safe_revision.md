# Queries that enable constraint-preserving revisions

Codex (GPT-6), DEVELOPMENT. A new S01/S04/S11 connection, beyond using queried
values only to predict output cost. The original answer vector satisfies a
declared chain of Boolean relations. A revised output must also satisfy that
chain. This is a chosen finite repair semantics, not an inferred causal model
or a claim that changing a mathematical statement changes arithmetic.

## Information can change the admissible revision menu

Let F be the nonempty set of original sign vectors satisfying the checked
binary relations R_i(x_i,x_{i+1}). At a paid query history h, let F_h be the
compatible original vectors. A flip mask b is permitted at h if
x xor b belongs to F for EVERY x in F_h. Repeated queries reveal original
values, not revised values; charge query and flip fees and a pathwise cap H.
Terminal zero requires no revision. Terminal one outputs the revised vector
and incurs its linear weighted cost. This explicitly chosen repair semantics
defines the candidate's domain. The previous prototype allowed unconstrained
output flips; results under that earlier menu do not transfer automatically.

Constraints apply to the released terminal vector. A revision is an atomic
batch charged per changed bit; the derivation does not require every
intermediate single-bit edit to satisfy the relations. Requiring such a path
would define a different reachability problem. Queries always inspect the
unchanged original source, so moving edits to the terminal batch preserves
all information and can remove redundant flips at nonnegative fee.

The requirement is operationally checkable from the received logical source.
Define the exact adjacent projection

```math
P_i(h)=\{(x_i,x_{i+1}):x\in F_h\}.
```

The permitted flip-pair relation is

```math
S_i(h)=\{(b_i,b_{i+1}):
 \forall(u,v)\in P_i(h),\
 ((-1)^{b_i}u,(-1)^{b_{i+1}}v)\in R_i\}.
```

A mask is uniformly valid exactly when every adjacent pair belongs to S_i(h).
Proof: validity of the revised vector is the conjunction of the local
relations; universal quantification distributes over that finite conjunction.
Use the projection of the GLOBALLY compatible source, not merely R_i with
nearby query literals: distant evidence can rule out a pair. A forward/backward
feasibility pass on the chain computes all P_i(h) in O(m) Boolean work for a
fixed history. Empty histories are unreachable under the source; validity
there is vacuous and cannot supply evidence about a reachable world.

Example in 0/1 notation: F={(0,0),(0,1),(1,1)} encodes x_0 implies x_1.
Before any query, only the identity bitwise flip mask preserves F for all
originals. After observing x_0=0, flipping x_1 alone is valid for both remaining
worlds, even though x_1 remains unknown. After observing x_0=1, the source is
the singleton (1,1), so flipping x_0 alone is valid, whereas flipping x_1 alone
is invalid. Thus a query can buy a certificate enabling an otherwise forbidden
revision. No probability estimate is required for that change of menu.

One exact consequence: keep that implication source, use weights (1,1) on
signs, zero flip fees, one queryable bit x_0 at fee 1/4, and H=2. The
point-source comparator costs are -2, -7/4 and 0 at (0,0),(0,1),(1,1).
Without querying, the controller cannot revise and its minimum worst-case
regret is 7/4. A controller that queries x_0, stops with zero on x_0=1,
and on x_0=0 uses terminal one while flipping x_1 with probability 7/16 has
worst-case regret 9/8. At the first two worlds the regrets both equal 9/8;
at the last it is 1/4. Thus evidence-enabled, paid revision already gives a
strict finite capability improvement over the optimized no-query class.
This is a worked construction, not yet a claim that 9/8 is the full optimum
or a complete-cost advantage over an ordinary planner with the same access.

## Convex realization of permitted terminal revisions

At h, permitted masks are paths through the binary chain S_i(h) with a count
of used flips <=H-|h|. A layered network state is (position,last flip,count).
Unit flow through this network is the convex hull of permitted masks; each
flip marginal is the sum of the corresponding local flip edges. Scaling the
flow by the private probability of terminal one gives an exact randomized
terminal menu, with every realized mask obeying both the logical condition
and the pathwise cap. This replaces the earlier uniform-matroid marginal
constraint, which would be unsound for a constrained revision menu.

The outer private-reach query flow remains source-independent. Histories
retain queried values, and the terminal network at each history depends only
on that history and the checked source. The merged-history realization proof
therefore still applies. A sampled revision must be realized by network-path
sampling, not by independently flipping marginal probabilities.

## A comparator detail that changes the earlier reduction

Every competing procedure must obey the SAME history-dependent validity rule
for every compatible original source, including branches not reached by one
particular source law. A point-mass source at x does not let the comparator
bypass this rule by silently using unpurchased facts as certificates.
Consequently, queries are NOT necessarily dominated for that comparator:
they can certify an admissible repair. The earlier query-free B(x) formula
does not apply to this semantics.

The worst-law regret is nevertheless attained at a point mass, since it is
convex in the law over F. For known x, a comparator can choose a compatible
query history h, pay the sum of its distinct query fees, and then choose the
best permitted mask in S(h) under the remaining cap. Any order of those
queries reaches h on x; all other observed branches can stop with terminal
zero, yielding a globally valid policy. This proves

```math
B(x)=\min\left\{0,\min_{h\preceq x,\ |h|\le H}
 \left[\sum_{j\in\mathrm{dom}(h)}q_j+
 \min_{b\in S(h),\ |b|\le H-|h|}
 \left(\sum_i w_i(-1)^{b_i}x_i+\sum_i f_i b_i\right)\right]\right\}.
```

For fixed controller rows C_pi(z),s_zi, a regret separator maximizes jointly
over x, a comparator history h compatible with the full query cell z, and a
permitted comparator mask. The chain dynamic program now carries
(last truth,last flip,flip count), checks R_i for original truth and S_i(h)
for the revision mask, and uses local score
w_i*(s_zi-1+2*b_i)*x_i-f_i*b_i. Subtract the comparator query fees and add
the controller's fee. Terminal-zero comparison is separate. All choices
refer to ONE original x; no source is reselected after an observation.

Enumerating compatible (z,h) pairs gives at most 4^r pairs (each query
coordinate has four possibilities: either sign observed, or either sign
unobserved). A loose separator bound is O(4^r*m*H), plus constructing the
at-most 3^r conditional revision menus. Epigraphs of these max-sum recurrences
and the terminal realization networks yield a compact LP for fixed r and H.
The controller network itself has O(3^r*m*H) size. Sparse coefficient maps
must be retained explicitly; arithmetic bit lengths and source compilation
are separate costs. This is a derived adapter, not yet an executed solver.

## Why this is worth a cheap screen

The useful difference from the preceding free-output revision model is that
paid evidence changes what can be certified as an admissible counterfactual.
The logical source is not treated as a free predictive law. The construction
uses ordinary constraint propagation, robust universal feasibility, network
flow and minimax epigraphs; it must be compared with equally informed ordinary
constrained-repair planning. Generic tractability or general counterfactual
semantics are not new claims.

First screen only the menu compilation and point-source comparator: enumerate
small chains and histories, compare every permitted mask with universal
world checking, and compare the comparator formula with unrestricted query
trees. Include the implication example above. Advance to a larger optimizer
only if this screen exposes a useful distinction worth retaining.
