# Which parts of a fallible model matter to the requested outputs?

Codex (GPT-6), DEVELOPMENT, October 22, 2026. A refinement of
budget_warrants.md; derivation only until the inexpensive screen below.

Let C=x0+V be a nonempty affine Boolean model, T the allowed target
coordinates, c_i>=0 the receipt prices, and B a per-conclusion receipt
budget. A legal release observes S disjoint from its target j in T,
c(S)<=B, requires that C conditioned on x_S is nonempty, and releases
the unique model-implied value of x_j. Model inconsistency causes no release.

A circuit of V-perp is a nonzero dual word with inclusion-minimal support.
Define D_(B,T) as the span of all circuits h for which some j in T meets

    h_j=1 and sum_(i in supp(h) except j) c_i <= B.

Then the exact largest world source protecting EVERY such legal release is

    W_(B,T)=x0 + D_(B,T)-perp.

## Why circuits, rather than all target-containing equations

Necessity: for a circuit h and target j, the projection of C onto
S=supp(h) minus j is the entire Boolean cube. Otherwise a nonzero dual
word supported inside S would contradict circuit minimality. Consequently
every actual x_S is a consistent model observation. If x violates h,
the resulting model prediction at j is a legitimate but wrong release.

Sufficiency: any legal fiber implication has a dual word h supported in
S union {j} with h_j=1. Among dual words with target j supported inside h,
choose c with minimal support. It is a circuit: a smaller nonzero dual
word either contains j, contradicting selection, or can be subtracted from
c to obtain a smaller word containing j. The circuit is affordable. If x
satisfies every eligible circuit then c*(x-x0)=0. The word h+c is supported
in S, so the nonempty model fiber implies (h+c)*(x-x0)=0. Hence h also
holds at x, and the released value is right.

This proves exactness even for restricted targets, nonuniform prices,
arbitrary adaptive target/receipt choices and arbitrarily many releases,
provided each conclusion obeys the same fixed interface. It does not
bound the computational effort to discover or check a certificate.

The source stays affine. Non-target model failures are not automatically
disqualifying. This is more precise than spanning every affordable dual
word that happens to contain a target.

Example: coordinates (a,b,c), model b=0 and a=c, allowed target T={a},
all receipt prices one and B=2. The dual words are b, a+c and a+b+c.
Only a+c is an eligible circuit, so exact task adequacy is a=c, with b
unrestricted. Spanning all target-containing dual words would also force
b=0, an unnecessary demand. If b=1, observations including b have empty
model fibers; observations of c alone still give the correct a.

The explicit consistency requirement matters. An implementation that
releases arbitrary algebraic consequences even after contradictory
observations has a different, stricter protection source. Its checker
cannot silently use this theorem.

## Graph interpretation and an algorithmic caution

For a vertex-XOR graph model, dual circuits are simple cycles. The exact
target-price of a cycle is

    price_T(C)=sum_(e in C)c_e - max_(e in C intersect T)c_e,

with infinity if it contains no allowed target. Short-price simple cycles
generate the warrant. For T=all edges this recovers the earlier theorem.

For restricted T, a shortest parity walk is not automatically a permitted
simple cycle. A walk through a target edge can acquire odd parity by a
detour around an unrelated non-target odd cycle. Decomposing that walk
may leave the only odd cycle outside T. Therefore the easy doubled-graph
walk oracle must not be imported as a minimum eligible-cycle oracle.
An efficient restricted-target compiler remains a separate question.

## Rooted bases supply that compiler with established machinery

The source search found a stronger route than repairing the walk oracle.
Eppstein, McCarthy and Parrish, *Rooted Cycle Bases* (arXiv1504.04931v1,
Theorems 1 and 2; journal version 2017) give a polynomial minimum-weight
cycle basis in which every cycle contains a specified root edge, on the
root's biconnected block with positive edge weights. Use that algorithm as
an imported component, not a new cycle-basis result.

For each allowed target e that lies on a cycle, compute a minimum rooted
basis B_e of its block using the additive receipt prices. Let K be the
union of these bases. It has at most |T| times the graph's cycle rank
members. Give each member its actual price_T, then greedily extract an
independent basis in increasing price_T order. Call the result B_T.

Claim: for EVERY B, members of B_T with price_T<=B span exactly the eligible
cycles of price_T<=B. To prove the candidate-set property, take an eligible
cycle C and choose e in C intersect T of maximum price. In the rooted
cycle matroid, the threshold property of B_e expresses C as a sum of
rooted basis cycles D with additive cost c(D)<=c(C). Each such D contains
e, so price_T(D)<=c(D)-c_e<=c(C)-c_e=price_T(C). Thus K's price-B portion
spans every eligible cycle. Ordinary greedy independence extraction then
preserves all these threshold spans simultaneously.

This constructs a single compact hierarchy for all budgets, even with
multiple restricted targets and unequal prices. No expensive shortest
simple parity-path solver is needed in this reduction. The new step here
is the union-of-rooted-bases price comparison; the basis solvers and greedy
linear matroid step are conventional.

The imported polynomial algorithm explicitly assumes positive prices.
For rational nonnegative prices, a deterministic secondary perturbation
can first make prices positive while preserving all strict original
cycle comparisons: clear denominators to integer weights and add the same
epsilon with 0<epsilon<1/(m+1) to each edge. Every simple cycle has at most
m edges, so an original weight gap of at least one cannot reverse. The
resulting minimum rooted basis is still minimum for original total weight
by the matroid threshold property. Evaluate final receipt budgets with
the ORIGINAL prices, not the perturbed ones. This is an exact rational
reduction; bit complexity and tie handling belong to implementation costs.

At unrestricted budget, only biconnected blocks containing a target edge
need be trusted. Each such block's whole cycle space is generated by
cycles through that target; cycles in other blocks are irrelevant to this
release interface. A bridge target permits no parity prediction at all.

The possible contribution is an exact resource-and-target scope for
relying on a false affine model. Code circuits, projection duality and
ordinary conditional inference are established ingredients; no new
general logic, statistical method or economic saving is asserted.

The exact target_warrant_probe.py screen passed 600 small affine panels
(14,880 world checks), including zero prices and restricted target sets.
Spanning all eligible target-containing words was unnecessarily restrictive
on 67 of those panels. The explicit three-coordinate example admits four
worlds under the exact warrant versus two under that stronger requirement.
For 24 tiny graphs and three target sets each, union-of-rooted-bases
compression matched all 1,269 tested price thresholds. Its rooted bases
were obtained by exhaustive cycle enumeration and greedy elimination;
the screen does not implement the imported polynomial algorithm.
An additional 288 all-target odd-walk oracle cost checks passed. Runtime
198,080,200 ns is the screen's runtime, not an application speedup.
