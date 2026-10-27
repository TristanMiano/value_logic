# Sparse receipt incidence: convex local messages and cycle conditioning

Codex (GPT-6), October26,2026. DEVELOPMENT. New structural derivation;
ordinary tree message passing and cycle conditioning are mandatory controls.
This extension is separate from the core AR1 event.

## Contract

There are n independent compact rational source polytopes B_i and k receipts

    a_j <= min_(i in I_j) g_ji(x_i) <= b_j,

with nonempty listed I_j and affine g_ji. The future value is
V=min_i f_i(x_i), with affine f_i. First absorb every universal lower
inequality g_ji>=a_j into the local polytope Q_i. A receipt now asks that
at least one of its incident predicates P_ji: g_ji<=b_j hold. All variables
must have feasible source points even when they witness no receipt.

Use the bipartite incidence graph on configurations and receipts. An absent
edge means a configuration is not an alternative for that receipt; a known
constant above the upper bound can represent it in the dense formalism.

## Forest consistency and projections

Root a tree at a configuration. A configuration-to-parent-receipt message
has two flags: its subtree is feasible without requiring its parent
predicate (F0), and feasible while requiring that predicate (F1).
For a child receipt, all child F0 flags must hold. If some child F1 holds,
the receipt imposes no restriction on the parent configuration; otherwise
it forces the parent's own predicate. These statements are exact because
different child subtrees have independent variables.

The configuration's feasible projection is therefore Q_i intersected with
the forced child halfspaces. Two LP feasibility calls compute F0 and F1.
A two-pass tree traversal computes all directed messages. At any node,
intersect Q_i with the halfspaces forced by all neighboring messages to get
its exact global projection P_i. If any required subtree is infeasible,
the component is infeasible. A root test handles this before optimization.

There are O(n+k) local LP calls on a forest, with constraint-input assembly
and rational solver costs charged separately. A naive implementation can
copy O(sum_i degree(i)^2) constraint rows across directed messages. This is
not a linear-time bit-complexity claim. Saved feasible LP points extend to
a global witness by selecting one available child witness whenever a
parent predicate is false.

## The compatible source is path connected

Prove the stronger inductive statement with any additional convex
restriction on the root configuration. The leaf case is convex. At a
fixed root point, each child subtree's unrestricted source and its
parent-predicate-restricted source are path connected by induction.

For a receipt whose parent predicate is false, the allowed tuple of child
subtrees is a union of products, one for each child able to witness it.
Each product is path connected. They have a common point: choose a
predicate-satisfying subtree point for every capable child and any feasible
point for the rest. Therefore their union is path connected. If the parent
predicate is true, the fiber is just the unrestricted product.

For every child receipt with a capable child, fix one such child and fixed
subtree witnesses. Receipts without a capable child already constrain the
root by a halfspace. The fixed descendant choices work for every root
point in its convex projection. Any source can first move, with its root
fixed, through the connected fiber to these choices. The root can then
move along a line segment with descendants fixed. Finally move through
the destination fiber. This supplies a piecewise path, not merely a claim
that a connected projection has connected preimage.

Disconnected incidence components form an independent product, preserving
path connectedness. Consequently the entire attainable scalar value set
is one closed interval whenever the source is nonempty. This does not
assert convexity of the source: min(x,y)=0 on the unit square gives an
L-shaped source even on a one-receipt tree.

## Exact future upper value with two scalar messages

For a rooted configuration subtree, let A_i be the largest attainable
minimum of all its future f-values; let B_i be the same maximum when its
parent predicate must hold. Use minus infinity for infeasibility. These
maxima are attained by compactness. A floor z is feasible in the respective
subtree exactly when z<=A_i or z<=B_i.

For child receipt j define

    C_j = min_(child h) A_h,     m_j = max_(child h) B_h.

Empty minima/maxima are plus/minus infinity. Its child subtrees can all
meet floor z precisely when z<=C_j. Subject to that, the receipt holds
if either z<=m_j or the parent configuration satisfies P_ji.

To compute A_i, maximize z over x_i in Q_i, f_i(x_i)>=z,
z<=C=min_j C_j, and the constraints

    z<=m_j OR P_ji(x_i).

For B_i also impose the parent predicate. This small disjunctive problem
has a threshold sweep using only local LPs. Impose all rows with m_j=-infinity.
Let U=min(C,max f_i over the current polytope). If the polytope is empty,
return minus infinity. Sort the finite thresholds increasingly. At threshold
t, if U<=t, stop with U. Otherwise save a current optimizer, impose all
rows having threshold t, and recompute U. If the new U<t (including an
empty polytope), return t with the saved point; at exactly t those new
rows were optional. Otherwise continue. Return U after the last group.

Between consecutive thresholds the required rows are constant. Crossing
a threshold is possible only if the preceding LP reaches it. If imposing
the next group drops the upper bound below it, that threshold was feasible
before the group and no larger value survives. This proves the sweep.
Each A_i or B_i uses at most one plus its child-receipt count LPs. Thus a
rooted tree needs O(n+k) local LPs plus threshold sorting. Cap infeasibility
from a child is detected first. All comparisons and boundary cases use
exact numbers; no binary-search precision parameter is hidden.

For a maximizing local point, a false parent-side receipt predicate is
completed by some child with B_h>=z; other children use A_h witnesses.
This reconstructs a full source at the reported optimum. Different
incidence components combine by taking their upper values' minimum.

The lower endpoint is min_i min_(x_i in P_i) f_i(x_i), using the two-pass
global projections and n additional LPs. For an intermediate requested
q, add f_i>=q locally, recompute forest projections, and find a node whose
minimum f_i equals q. Extend its minimizing point through the saved
messages. The interval theorem ensures such a node for q between the
endpoints. This uses O(n+k) LP calls; it need not search an inductively
constructed topological path.

## t incidence edges beyond a forest

Choose a spanning forest and let D be its t omitted edges, where
t=E-(n+k)+c and c counts incidence components. Branch over all subsets
S of D. Impose P_ji for each selected edge (j,i) in S. A receipt touched
by S is already witnessed, so remove its remaining disjunction. Every
other receipt keeps only its spanning-forest edges. Keep every universal
lower bound throughout. If an unwitnessed receipt has no remaining edge,
that branch is infeasible.

Each branch is a forest system with extra local halfspaces, hence has an
interval value image computable as above. Every branch source satisfies
the original receipts. Conversely, choose one actual witness per receipt
in an original source and select exactly those chosen edges lying in D.
That branch contains the source. No assertion that unselected edges are
false is needed. Therefore the full range is a union of at most2^t
intervals, using O(2^t*(n+k)) local LP calls plus graph, constraint-copying,
sorting and exact-arithmetic costs. This is ordinary cycle conditioning
with a specialized tractable leaf problem.

The component bound is tight even for a connected graph and this minimum
readout. Let a central block have x in[0,1]^t and t leaf blocks y_j in[0,1].
For each j retain min(x_j,y_j)=0 and min(1-x_j,1-y_j)=0. These force
(x_j,y_j) to be (0,1) or (1,0), independently. The incidence graph has
4t edges,3t+1 vertices, one component, and hence cycle rank t. Set the
central future readout to sum_j 2^j*x_j (j=0,...,t-1), and each leaf
readout to2^t. The resulting minimum takes exactly2^t isolated values.

This is an explicit structural algorithm/output result, not evidence of
practical solver superiority. Natural sparse histories, comparison with
existing compact-constraint tree algorithms, and implementation checks
remain to be assessed. Do not treat this new extension as a required
condition for the earlier independent-block AR1 contribution event.

## Development screen and comparison status

The precommitted forest_solver.py/forest_probe.py run passed74 rational
cases against the general AR1 range composition. There were63 forests,
six inconsistent cases,105 cycle branches, and249 checked endpoint or
interior source witnesses. The two explicit tight examples supplied the
only disconnected outputs; tested cycle ranks were0,1,2. The run took
1,430,277,000ns, with1,868 local vertex-LP calls including interior-witness
reconstruction and870 reference local slices. These counts cover different
duties and do not establish a solver speedup. Both routes share a rational
vertex helper; all evidence is same-model DEVELOPMENT.

Dechter's tree/cutset algorithms and Jefferson--Moore--Nightingale--Petrie's
OR propagation are direct conventional antecedents. The retained possible
delta is the compact continuous-polytope messages, full scalar-image
statement and explicit cycle-rank output bound, not the general idea of
tree inference. The disjunctive-temporal literature has different binary
difference predicates and numeric/domain hypotheses. Its general bounded
treewidth results must not be transferred automatically to this contract.
Closest-result comparison is incomplete; readiness is unassessed.
