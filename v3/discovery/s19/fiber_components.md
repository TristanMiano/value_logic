# Connectivity of a short minimum-receipt history

Codex (GPT-6), October26,2026. DEVELOPMENT; exploratory structural question.
This is distinct from the already derived scalar-minimum anchor formula.

## Why the source itself might admit a useful bound

For a fixed assignment of k receipts to n independent generators, the
compatible source is a product of convex slices. Each such product is
connected. The complete source is their union; two products intersect when
every generator can simultaneously satisfy its two assigned receipt sets.
Thus a graph of feasible assignments with intersection edges describes
the source components. Keeping all n^k assignments is a valid generic
method but does not exploit a short observation history well.

Any continuous scalar readout has an interval image on each connected
component. Therefore a component bound would apply beyond a future minimum,
including sums of counterfactual minima. It would not by itself optimize
that readout or make mixed-action regret tractable.

An initial conjecture for screening is that the number of components is
bounded by a function of k alone, possibly k!, independent of n and local
dimension. This is NOT an established claim. There is a matching-looking
example: n=k; each generator has x_i=1-p_i with p_i in the k-simplex; every
coordinate minimum is0. A generator can witness a zero only at a simplex
vertex and can witness just one coordinate. All k receipts force a
permutation of the k vertices. The source has k! isolated points. A generic
linear scalar readout can assign different values to all of them.

The earlier two-hypersimplex example gives exponentially many components
with just two generators. AR1's much smaller bound for one future minimum
uses the particular readout and must not be confused with source compression.

## A finite screening abstraction

For each generator choose a finite menu of receipt subsets. A local menu
entry says which receipts are witnessed at that vertex. Realize this menu
as simplex vertices, with g_j=0 on vertices that include j and1 otherwise.
At a convex mixture the zero set is the intersection of the selected
vertices' zero sets. Global feasibility means the union of current local
zero sets covers all k receipts.

Two feasible menu assignments differing at one generator can be connected
by its line segment: receipts not covered by the other generators belong
to both endpoint zero sets and hence remain zero along that segment.
Conversely, the product-simplex feasible set is the union of faces
described by these choices, so its component count is the component count
of this feasible one-coordinate-change graph. Empty local zero sets are
allowed. Redundant dominated menu entries cannot create an extra component:
they can move to their superset without losing coverage.

The cheap probe will enumerate small menus and sample larger ones, looking
for counterexamples to an observation-only component bound. Passing is
only exploratory evidence; no readiness estimate follows from it.

## Development screen and subsequent proof

The frozen [probe](fiber_component_probe.py), [plan](fiber_component_plan.json)
and [result](fiber_component_result.json) examined23,866 menu instances,
230,153 Cartesian states and83,942 feasible states. It found no violation.
The maximum for k=3,n=2 was3; permutation fixtures attained k! through k=6.
Runtime355,165,800ns. These checks motivated the argument below; they are
neither its proof nor independent confirmation. The result is exposed.

**Proposed component theorem.** Let B_i be nonempty compact convex sets and
let Q_i(T) be the local convex slices defined in anchor_ranges.md. If their
global compatible source is nonempty, it has at most k! connected components.
The bound is attained by the simplex construction above. The same statement
holds for interval observations, not just exact receipts. Empty sources have
zero components; k=0 gives the connected product and the convention0!=1.

For a feasible assignment alpha of receipts to generators, let T_i(alpha)
be its assigned sets and let C_alpha be the product of Q_i(T_i(alpha)).
These finitely many nonempty compact convex cells cover the source.
Their intersection graph has the same components as their union. If two
cells intersect, each Q_i(T_i(alpha) union T_i(beta)) is nonempty. Move
receipts one at a time from their alpha bins to their beta bins. At every
step each bin's set is a subset of that union and is feasible. Adjacent
assignment cells intersect. Thus we can equivalently use the graph whose
edges move one receipt between bins when the enlarged receiving bin is
feasible. This also proves that all source components are path connected.

Fix the generator order1,...,n. Within any assignment component, repeatedly
move a receipt to a lower-index bin whenever that move is feasible. The
integer potential sum_j alpha(j) strictly decreases, so this terminates at
an assignment tau admitting no such move. Order the k receipts by their
tau-bin index, breaking ties arbitrarily. Run ordinary first-fit assignment
in that receipt order: put each receipt in the lowest-index bin whose
current set remains feasible after adding it.

Inductively this reconstructs tau. When a receipt belonging to bin c is
processed, every lower-index bin already has its whole final set. None can
accept this receipt, by the terminal property of tau. Its own bin c can
accept it because its current set plus this receipt is a subset of the
feasible final set. Therefore first fit chooses exactly c.

There are only k! receipt orders. Each order produces at most one completed
assignment, and every component contains at least one such assignment.
Hence the number of components is at most k!. The proof uses only hereditary
bin feasibility and convexity of assignment cells. It does not claim first
fit succeeds on every order or that its different outputs are disconnected.

## Consequences and limits

Any continuous scalar function on the compatible source has an image that
is a union of at most k! closed intervals. This is a topological statement;
it does not compute their endpoints. For a future affine minimum, combine
it with AR1 to obtain at most min(k!, n*2^k) components in the returned set.
For general sums, ratios on a nonzero denominator, or mixed-decision
readouts, the endpoint optimization may remain difficult. The joint-value
hardness example is not contradicted.

Enumerating first-fit orders and retaining one feasible source witness for
each completed assignment gives at most k! representatives and hits every
source component. A naive implementation uses at most n*k*k! local
feasibility tests; precomputed2^k tables per generator make these lookups.
This is a diversity guarantee, not an epsilon-cover, probability model or
worst-loss certificate. One point cannot represent all decisions in a
component. The strongest relevant ordinary comparison is first-fit
coloring/partition reconfiguration; novelty still requires a primary screen.

## A closer ordinary antecedent and a shorter path

The accessible primary text of *Recoloring graphs via tree decompositions*
(European Journal of Combinatorics69,2018), Lemma6, already shows that a
proper coloring can move to the greedy coloring for its color-class order
while recoloring each vertex at most once. Thus the elementary greedy
normalization idea is established. Our adaptation uses different hereditary
feasibility families for the bins and then relates assignments to convex
source cells. Do not present the generic normalization as newly discovered.

The same one-pass proof works here. Process receipts in their original bin
order. Before processing an item originally in bin c, all lower original
bins have been processed and no item from them moved upward. Lower receiving
bins therefore contain only processed items. Bin c still contains a subset
of its original feasible set. The lowest feasible current bin is at most c;
its choice agrees with first fit on the processed prefix. Move the receipt
there. The move is feasible, and repeating processes each receipt once.
This constructs a path to a greedy representative in at most k moves,
strengthening the earlier decreasing-potential termination argument.

Geometrically, a receipt move can be realized by changing only the receiving
generator within its old convex slice to a point that also witnesses the
new receipt; the old witness remains valid during that segment. After at
most k such segments, move inside the final product cell to a chosen
representative. This supplies a path of at most k+1 straight segments,
conditional on the local feasible points. It is not an efficient method
for deciding whether two arbitrary greedy representatives are connected.

## An exploratory finite reduction for component connectivity

There is also an observation-parameter reduction of the assignment graph.
Give generator i its hereditary feasibility type

    F_i = {T subset K : Q_i(T) is nonempty}.

At most2^(2^k) types exist. Keep at most k+1 labelled bins of each type;
temporarily leave every removed bin's assigned set empty. This operation
preserves the number of assignment components. Its proof is combinatorial,
not a license to discard these generators' future objective responses.

Every feasible assignment uses at most k nonempty bins. For a removed bin
with assigned set T, there is an empty retained bin of the same type; move
the receipts of T to it one at a time. Heredity makes every move feasible.
This reaches the retained subgraph. For a path in the original graph, track
each occupied original bin by a distinct retained bin of its type. A move
to a previously empty bin uses a spare retained bin, which exists because
there are k+1 slots but at most k nonempty bins in total. A move to an
occupied bin uses its current representative. Thus the path can be
simulated after relabelling occupied bins within each capped type.

Such relabellings do not change connectivity: use an empty retained bin
as temporary storage and move a whole feasible receipt block through it,
one receipt at a time. This implements permutations of occupied bins of
the same type. Types with at most k bins were never capped and can keep
their original identities throughout. Hence the simulated endpoints are
connected to the desired retained endpoints, proving the converse as well.

With N <= (k+1)*2^(2^k) retained bins, explicit assignment-graph search is
finite-parameter tractable in k: at most N^k assignments and k*N candidate
moves per assignment, after at most n*2^k local feasibility calls. This
coarse double-exponential dependence is not a practical recommendation.
The reduction preserves connectivity only. Replacing removed source vectors
by representatives can change numerical extrema, action costs and all
probabilities. Those would require a different warranted compression.
This refinement is derived, unimplemented, and has not had its own close
literature screen; it is separate from the core AR1 contribution event.
