# S24: graded prediction value under imperfect tree forecasts

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
Parents: S20 physical observations, S11 value profiles. The S23 oracle
truncation gains were modest, so further allocation tuning is deprioritized.
This branch changes the observation-value model, not the published S20 claims.

## Model and conditional exact reduction

Take a physical tree rooted at a known bit X_0. Each edge carries a parity spin
E_e in {-1,+1}; a node spin is X_0 times the product along its root path.
The supplied source makes edge spins independent, with preferred sign s_e and
P(E_e=s_e)=(1+b_e)/2, 0<=b_e<=1. A checked edge observation reveals E_e at
nonnegative fixed price c_e. Node decisions are separate bit predictions,
weighted by w_v>=0; put r_v=w_v/2. No alternative node-query methods are
silently added. A known root is a stated premise, not a free general anchor.

Given queried set S, predict each node by multiplying checked edge labels
and preferred signs of its unqueried edges. Conditional expected accuracy is
1/2 + (1/2) product_(e in path(v) outside S) b_e. Thus the optimized expected
score minus invoice equals the constant sum_v w_v/2 plus

```
F(S) = sum_v r_v * product_(e in path(v) outside S) b_e - sum_(e in S)c_e.
```

Even adaptive truth-label policies cannot exceed max_S F(S): revealing an edge
leaves unqueried edges independent with their original laws; terminal accuracy
magnitudes depend only on S. Each leaf of an adaptive policy has the displayed
conditional value, and their probability-weighted mean cannot exceed its
maximum. A maximizing fixed set attains it. This reduction fails for dependent
edge sources, state-changing observations or objectives coupling node choices.

## A decision-value recurrence

Let F_v(x) be the best prize minus descendant-edge invoice in v's subtree when
its current prediction magnitude from ancestors is x in [0,1]. Then

```
F_v(x) = r_v*x + sum_(children u) max(F_u(b_(v,u)*x), F_u(x)-c_(v,u)).
```

Use F_root(1), subtracting F(empty) for acquisition improvement. By induction
F_v is nonnegative, nondecreasing and convex piecewise affine, with slope at
most R_v=sum_(u in subtree(v))r_u. Its affine pieces are concrete descendant
query sets. A maximizing piece supplies an executable fixed acquisition plan.
The number of pieces has not been bounded polynomially; do not infer fast
exact planning from the concise recurrence. The set objective has increasing
returns to query purchase, so a naive one-edge greedy rule can miss profitable
bundles. Ordinary submodular minimization and stochastic network optimization
are relevant comparisons to check before assigning a contribution delta.

## Forecast revision and robustness

For independent edge laws with the same preferred signs and magnitudes in
known intervals [l_e,u_e], the fixed plan's score is monotone in every unqueried
magnitude. Optimizing at the lower endpoint l gives a minimax policy over this
declared product family: that fixed plan has its worst expected score at l,
and no adaptive policy can outperform its optimum under the member l. This is
a source-conditional robust guarantee, not a logical warrant for every world.
Marginal intervals alone do not imply the product-family premise.

For a fixed plan S, two supplied magnitude vectors b,b' satisfy

```
|F_b(S)-F_b'(S)| <= sum_v r_v * sum_(e in path(v) outside S)|b_e-b'_e|.
```

This follows by telescoping products in [0,1]. Unchanged queried edges vanish
from the sensitivity bill. If this bill is bounded by epsilon uniformly over
plans, optimizing the revised forecast incurs at most 2epsilon regret under
the old law. A plan-specific bill can instead certify a proposed revision
against a separate upper bound. The signs are needed for actual predictions:
magnitudes/value profiles alone do not determine which bit to report.

Next: derive a certified finite approximation that prices its representation
error, then check small exact subsets and varied tree shapes. No large harness
or adversarial confirmation is warranted yet.

## Exact compression found before implementing a grid

The apparent exponential envelope is avoidable. For any convex nondecreasing
child function F with nonnegative slopes and b in [0,1],
`d(x)=F(x)-F(b*x)` is nondecreasing: between knots its slope is
F'(x)-b*F'(b*x)>=0. Thus the edge choice switches at most once, from leaving
the edge unresolved to buying it. Let t be the first crossing of d(x)>=c.
Before t use F(b*x); after t use F(x)-c. A child knot k appears on the first
branch only when k<b*t, mapped to k/b, or on the second only when k>t.
Since b*t<=t, a knot cannot appear in both branches; intervening knots vanish.
There is at most one new knot, t. At ties either attaining plan suffices.
Handle b=0, b=1, c=0 and absent crossings explicitly.

Induction over children now gives at most one knot per descendant edge in F_v.
Each subtree profile has at most its edge count plus one affine pieces. Summing
child envelopes only takes the union of their knots; adding r_v*x adds none.
A bottom-up exact-rational implementation can therefore retain polynomial
profiles, with O(n^2) total piece storage in a path if every subtree is kept.
This replaces the proposed approximation step. Arithmetic bit complexity and
implementation cost remain to be checked; an O(n) root profile alone does not
imply O(n) preprocessing.

An independent structural explanation is monotone comparative statics.
The reward A(S)=sum_v r_v product_(path(v) outside S)b_e is increasing and
supermodular. For x<=y, maximizers S at x and T at y satisfy

```
f_x(S intersection T) + f_y(S union T) >= f_x(S) + f_y(T),
where f_x(U)=x*A(U)-cost(U).
```

Optimality forces equality, so the largest optimizer at y contains every
optimizer at x. The largest optimal sets are nested and acquire each edge at
most once. This supplies another reason for at most n profile regions, but
is a standard lattice-comparative-statics pattern, not a novelty claim.
The direct recurrence supplies a concrete construction for this tree family.

Next: read the primary monotone-optimization comparison, implement affine
piece transformations and plan recovery, and check exhaustive small subsets
at all computed breakpoints and interval interiors. New developmental inputs
will be fixed before running. Compare equivalent ordinary dynamic programming
and include profile preparation as well as repeated request costs.

Primary comparison read: Milgrom and Shannon (1994),
[Monotone Comparative Statics](https://lonessmith.com/wp-content/uploads/2023/06/Milgrom-MonotoneComparativeStatics-1994.pdf),
section 2 Theorem 4 and proof, Corollary 2, and section 3 Theorem 5. Their
lattice monotonicity machinery covers the nested-maximizer explanation above;
Theorem 5 attributes the supermodular/increasing-differences result to Topkis.
Our finite choice lattice supplies existence without a compactness issue.
The direct child-profile transform is the implementation to develop here.
The author's Stanford PDF timed out; the linked copy of the original article
was retrieved. No claim to have read Topkis (1978) beyond its publisher abstract.

Prospective small probe: 28 fresh trees of 2–8 vertices, seed 77149, edge
magnitudes in {0,1/4,1/2,3/4,1}, rational nonnegative costs and prizes.
Enumerate all acquisition subsets and compare the profile at every knot,
midpoint and 17-point grid. Reconstruct attaining plans, check the nested
largest sets and nodewise piece bound. For the first 10 cases also enumerate
all edge worlds and adaptive Bellman states to check the decision semantics.
After these checks, measure source/profile/request costs on 256-node path,
star and binary trees for 128 changed root magnitudes. Rebuilding the identical
ordinary DP is a reuse comparison, not the strongest possible specialized
single-query algorithm or a novel-optimizer claim. The laws/prices are supplied.

[First result](biased01.json): 28 fresh trees, 19,432 subset evaluations,
579 profile requests and 5,685 full-belief states agree exactly. Recovered
plans attain each value, are the largest maximizers at the checked points,
and are nested as root magnitude increases. Every node obeys its piece bound.

For 256-node path/star/binary trees, root profiles have 8/63/85 pieces and
all stored subtree profiles have 1,923/318/845 pieces. Preparation costs
13.293/1.033/4.278 ms; 128 value lookups cost 0.130/0.069/0.069 ms.
Recovering all plans costs another 21.292/19.567/23.435 ms, and their direct
feasibility/value checks cost 6.543/6.090/6.951 ms. Rebuilding the identical
complete profile for every request costs 1,861.300/114.453/539.096 ms.
This supports retained-profile capability at supplied-model scope; it is not
a demonstrated advantage over every specialized single-request optimizer,
and it excludes learning/authenticating the source and actual query execution.

## Checked observations and local model revisions

After a checked edge observation, its parity is known. For future planning,
set its magnitude to one and its future acquisition cost to zero; retain the
actual paid invoice separately. Update the preferred sign to the checked
label when producing predictions. Conditioning a product edge source leaves
the unqueried edge laws independent, so this is an exact continuation model
under the original source. A timeout performs none of these substitutions.

A change in one edge's magnitude or future price changes the transformed
profile at its parent and the profiles of that parent's ancestors only.
A changed node prize changes its own profile and ancestors. Other subtree
profiles are reusable at the same versioned source. Recompute the affected
ancestor union once for a batch revision; label changes alone alter prediction
signs but not value magnitudes. This is ordinary dependency-directed DP reuse.
Balanced trees may benefit; a path can require almost the full computation.
The update must still charge validation, source mutation and plan checking.

To certify a returned profile, every child edge transform can be checked on
the union of parent/child branch breakpoints and their intersections: on each
remaining open interval all compared formulas are affine, so endpoint checks
establish equality to the recurrence throughout it. A direct plan check gives
a lower witness; checking the whole recurrence is the optimality certificate.
One returned value and one feasible plan alone do not establish optimality.

The scalar magnitude profile does not encode signs, arbitrary dependence, or
all changes of objective. Its slopes retain aggregate attainable prediction
magnitudes and its intercepts retain paid invoices. Many different sources
and forecasts share those aggregates. Recovering calibrated probabilities
for every proposition from this one profile is therefore unjustified.
