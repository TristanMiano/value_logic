# Compile safe atomic edits from local source projections

Codex (GPT-6), DEVELOPMENT. Connects S01/S04/S07/S34: unresolved source worlds,
receipt-conditioned counterfactual edits, and reusable task-specific evidence.
The constraint-projection and graph algorithms are conventional machinery.
The proposed contribution is an exact, costed adapter; priority is not assessed.

## 1. A general bounded-width target compiler

Let F be a satisfiable Boolean source, h a consistent receipt fixing original
bits, and G a CNF target. An atomic mask d toggles the original world x to
x XOR d. It is allowed exactly when every x satisfying F and h gives a
post-edit world satisfying G. The source, target, receipt and toggle semantics
are supplied; they are not learned from this compiler.

For each non-tautological target clause C, let J be its distinct variables
and a its unique falsifying assignment. Compute the local projection
R_J(h)={x_J: x satisfies F and h}. For every v in R_J(h), add the mask clause

```math
\bigvee_{i\in J}\left(d_i\ne v_i\mathbin\oplus a_i\right).
```

The conjunction of these clauses describes **exactly all allowed masks**.
To prove this, the clause C fails after the edit precisely when
x_J XOR d_J=a, equivalently d_J=x_J XOR a. Each realizable v therefore
forbids precisely that mask pattern; no other pattern is forbidden by C.
Intersect over C. A source/receipt contradiction is rejected, rather than
interpreted as permission to edit arbitrarily by vacuous universal validity.

For target width at most k, there are at most |G|*2^k clauses, each width k.
One can obtain its projections with at most |G|*2^k source satisfiability
queries with local assumptions. This avoids enumeration of all source worlds;
it does not make an arbitrary source oracle cheap or solve optimization over
the resulting mask formula. Included local patterns can carry source witnesses;
excluded patterns need checked unsatisfiability evidence.

## 2. A sharper reusable interface when the source is 2-CNF

Suppose F is satisfiable 2-CNF and target width is at most two. Prepare every
target clause's initial projection R_J. After receiving h, compute all literals
forced by F and h. Then

```math
R_J(h)=\{v\in R_J: v\text{ agrees with every forced literal on }J\}.
```

The nontrivial case is J={u,v} and neither variable is forced. Choose an
original F-model x with the desired pair (a,b), an F-and-h model y with u=a,
and an F-and-h model z with v=b. The latter two exist because these variables
are unforced. The coordinatewise majority of x,y,z satisfies every 2-CNF
clause: if a two-literal clause failed in the majority, each literal would
fail in at least two input models, so at least one input would fail both.
The majority satisfies h because y and z do, and has the desired pair because
x,y agree at u and x,z at v. Thus the desired pair remains realizable.
If one endpoint is forced, the other endpoint's unforced status realizes
both its values; if both are forced, consistency supplies their pair.
The singleton case is immediate.

Consequently, no new local satisfiability queries are needed merely because
more original bits have been observed. Initial projections and a literal
propagation graph suffice. In the graph, a clause l OR m gives arcs
not-l=>m and not-m=>l. Start with the source's globally forced literals,
then propagate each queried true literal; contradictory literals reject h.
The initial forced literals and pair projections require paid preparation
(for example reachability computations or prepared 2-SAT calls).

Across a monotonically growing receipt on one fixed world, each newly forced
literal and outgoing implication edge need be processed only once. Keep
incidence lists from variables to target clauses and update their cached
projections only when an endpoint becomes forced. Total propagation and
projection-filter work after preparation is O(n+|F|+|G|), excluding the work
of optimizing an edit, acquiring receipts, and bit-complexity of prices.
Reading submitted receipt literals costs O(N_R) in addition; repeated delivery
of an already known literal cannot be processed for free.
This amortized statement is about one growing receipt, not arbitrary resets,
source changes, target changes or query planning over all possible histories.

Because projections shrink with more receipts, the compiled mask formula
only loses forbidden-pattern clauses. Every old allowed mask remains allowed.
Learning more does not invalidate earlier safe edits under this fixed source
and target. It can expose a harder optimization problem, however.

## 3. Where the fast update fails

For the Horn 3-CNF source u AND v => z, the initial projection onto (u,v)
contains all four patterns. Observe z=0. Neither u nor v is forced, but their
joint pattern 11 is now impossible. Filtering only forced endpoints would miss
this change. Against target u=>v, the receipt enables toggling v: the surviving
00,01,10 become 01,00,11. Before the receipt no mask is universally safe for
that target. Thus width-three source correlations require more than the
2-CNF forced-literal cache. This is a counterexample to extending the fast
update rule, not to the general projection compiler.

## 4. Pure implication sources give an additional optimization simplification

When F=G contains only implications u=>v, first collapse strongly connected
components; original variables in each component are equal and a safe mask
must toggle them together. Work on the resulting strict DAG. Mark nodes as
forced zero, forced one or unknown after receipts.

- An edge between two unknown nodes realizes 00,01,11. Both its mask bits
  must be zero. Hence every unknown node incident to an unknown edge is frozen.
- An unknown node isolated in the unknown-induced graph may toggle freely.
- A known zero with an edge to an unknown successor must stay zero. A known
  one with an unknown predecessor must stay one.
- The remaining known nodes may choose post-edit values satisfying their
  implication edges, with those boundary values fixed.

These conditions are necessary by the local pair patterns and sufficient
edge by edge. They factor the full allowed-mask set. For additive rewards
for accepted toggles, the known region is ordinary maximum-weight closure:
at a known-zero node, its reward is w*y; at a known-one node it is w*(1-y).
The unknown free nodes independently take positive-reward toggles. A minimum
cut solves the closure problem; it does not solve the preceding query policy.
Preparation, graph computation and checking remain real costs.

## 5. Information can expand the menu without making full optimization easy

For general 2-CNF, a compact allowed-mask description is not a polynomial-time
maximum-reward solver. Let F=G consist of clauses not-x_u OR not-x_v for edges
of an arbitrary graph with no isolated vertices. With no receipt the only
safe mask is zero: the all-zero model rules out masks containing an edge,
and if a mask contains vertex u but no neighbor v, the original singleton
model at v becomes invalid after the toggle. Every nonzero mask fails one
of these tests. After observing the all-zero original world, allowed masks
are exactly the graph's independent sets. Maximizing their positive vertex
rewards includes maximum-weight independent set.

The reasoner can always keep the previous safe action and ignore additional
opportunities. This example does not say free information makes decisions
worse; it says exploiting the enlarged menu optimally can become hard.
An anytime optimizer should retain old feasible edits as a baseline.

## 6. Query acquisition still has its own difficulty

For a fixed proposed mask and binary source/target, collect the initially
realizable local patterns that would violate a target clause after that mask.
Each is an obligation to eliminate. On a specified true world x, querying
coordinate i supplies literal (x_i), whose implication closure eliminates
every obligation contradicted by one of its forced endpoint literals.
Since unit propagation takes a union of these closures, a set of queried
coordinates certifies the mask exactly when these coverage sets cover all
obligations. Thus the cheapest **offline certificate on a known world** is
a weighted set-cover instance. This is a comparison benchmark, not knowledge
available to the online reasoner before it buys those values.

Set cover appears even in a simpler certification duty. Use a source with
one implication root_i=>element_j for each membership in a set system. On
the all-one world, certifying that every element is true can be done by
querying true roots whose sets cover the elements; give direct element queries
prohibitively high prices. The cheapest certificate is minimum-cost set cover.
Hence cheap receipt processing does not make query selection easy. Familiar
greedy set-cover guarantees apply to that offline known-outcome problem;
arbitrary source correlations do not automatically give adaptive submodularity.

## 7. Do not manufacture an advantage by withholding overwrite operations

Many configuration interfaces offer set-to-zero and set-to-one operations,
not only toggles. If every coordinate may be overwritten, a satisfying target
assignment can be written without discovering the original world. Queries
then need to justify saved writes or some other real duty. A deployment
comparison must include these operations when the application offers them.

The local compiler extends to **all coordinatewise Boolean operations**.
Represent the chosen unary map at coordinate i by two action bits t_(i,0)
and t_(i,1), giving its output for each original input value. These encode
identity, toggle, constant zero and constant one. For each target clause with
falsifying pattern a and each source projection pattern v, add

```math
\bigvee_{i\in J}\left(t_{i,v_i}\ne a_i\right).
```

The same one-line failure equivalence proves exactness. Restricting the allowed
unary maps at one coordinate is a relation on its two action bits; any subset
of the four maps is expressible by at most four two-literal clauses. Therefore
a binary target still compiles to 2-CNF over 2n action bits. The 2-CNF-source
receipt cache and its amortized update proof continue to apply unchanged.

This gives a polynomial feasibility representation that includes ordinary
overwrites. It does not make arbitrary per-operation cost optimization easy:
those costs are functions of the selected map, and even binary target
optimization can encode independent-set or vertex-cover problems. It also
does not assert physical permission to overwrite a coordinate; the supplied
operation menu is part of the contract. New observations may make two maps
equivalent on the remaining worlds, while their charged execution costs can
still differ.

## Development obligations

Check the compiler and receipt theorem against exhaustive small worlds using
an independently implemented literal-graph path. Inspect closest primary
work on Boolean constraint projections, 2-SAT majority closure, robust
configuration updates and maximum-weight closure. A useful contribution needs
the preparation/update costs and a meaningful operational duty, not merely a
large ratio against explicit world enumeration. Strong ordinary 2-SAT,
constraint-propagation and identical-compiler controls remain mandatory.

The first [development screen](permission_probe.py) completed on the bundled
Python runtime without failure; [results](permission_probe.json) retain its
version and executed source hash. Graph reachability was compared with direct
truth-assignment enumeration on 180 seeded source/target fixtures (126 had
satisfiable sources), all partial receipts for those fixtures, and 32 separate
implication DAGs. The checks covered 6,847 consistent receipts, 5,429 rejected
contradictory receipts, 26,324 local projections, 181,244 mask comparisons and
50,288 additional implication-characterization comparisons. The width-three
counterexample was also executed. These are finite diagnostic checks, not a
proof over all sizes or an independent confirmation. No runtime advantage is
claimed from the small screen's approximately 1.11-second execution.

The separate [all-map screen](map_probe.py), with its [saved output](map_probe.json),
passed 310,208 direct action/world comparisons on 1,592 consistent receipts
from 56 satisfiable sources among 72 seeded fixtures. Restricted per-coordinate
operation menus were included. On 305 growing receipt chains, the incremental
procedure visited each newly forced literal, outgoing implication edge and
installed target-pattern incidence at most once; the asserted bounds held.
These counters exclude preparation and optimization and are not a speedup
against a strong solver. Both executed source files are retained by hash.

## 8. Narrower interpretation after the prior-work screen

There is a direct conventional homomorphism interpretation. Give each coordinate
its own two-element sort. For each target clause scope J, put the compatible
source projection R_J in a source relational structure, and the satisfying
tuples of that target clause in a target structure with the same relation name.
A collection of unary maps t_i is safe exactly when it is a homomorphism from
the source structure to the target structure. The all-map Boolean clauses are
the ordinary constraint expansion of that condition. If source and target are
the same relation, this is the corresponding multi-sorted unary polymorphism.

Thus neither constraint-preserving maps nor uncertainty-safe planning is new.
The remaining candidate is the specific receipt-updated representation, its
source-change certificate discipline, and a useful complete-cost application.
The majority-closure shortcut for binary sources is a specialization of
established bijunctive structure. This is a reason to seek a concrete delta,
not to invent a broad novelty claim from new terminology.

The later [receipt-width note](receipt_width.md) extends the projection update
to arbitrary target scopes and gives its exact semantic boundary: under all
consistent receipts, forced-coordinate pruning is exact on every pair scope
if and only if the source is 2-CNF-definable. It also explains why bounded
input clause width alone does not give the analogous higher-width guarantee.
