# Tight receipt sets and continuous model revisions

Codex (GPT-6), October26,2026. DEVELOPMENT; new structural screen.
This uses the matroid-local feasibility regime of matroid_receipts.md.
The initial conjecture below is resolved by an existing topological
reconfiguration theorem, through the reduction recorded at the end.

Suppose each generator's feasible assigned-receipt sets form a matroid M_i
on K. For base-polytope coordinate-zero receipts, these are the restrictions
of the dual matroids. A compatible assignment partitions K into independent
sets T_i. Its one-receipt-move graph describes source connectivity by
fiber_components.md. Let r_i be the matroid ranks.

The standard matroid-partition feasibility inequalities are

    |S| <= sum_i r_i(S), for every S subset K.

Call S tight when equality holds. In any compatible assignment,
|T_i intersect S|<=r_i(S), and summing gives equality. Thus every bin has
exactly r_i(S) assigned elements of S. Moving an element of S to another
bin would exceed that receiving bin's rank on S. No element in any tight
set can change its bin along a one-receipt-move path.

The union S_star of all tight sets is tight: the rank sum is submodular,
cardinality is modular, and feasibility makes the difference nonnegative.
Closure of its zero sets under union follows. Hence the assignment on
S_star is an invariant of every connected component.

Fix this assignment. The sets T_i intersect S_star are bases of M_i
restricted to S_star. After fixing those bases, the remaining independent
sets are exactly those of M_i/S_star. For every nonempty residual set U,

    sum_i r_(M_i/S_star)(U) > |U|,

because equality would make S_star union U tight. This reduces the
sufficiency question to strict matroid-partition slack.

**Screening conjecture:** when these inequalities are strict for every
nonempty U, the single-element reassignment graph is connected. Equivalently,
in the original instance two feasible assignments are connected exactly when
they agree on S_star. Standard matroid-union augmenting paths are a plausible
route, but their simultaneous exchanges must be turned into valid sequential
moves; that step is not assumed for free.

A small exact probe will enumerate binary linear matroids and uniform
matroids, compare complete reassignment components with this invariant, and
preserve any counterexample. If false, the necessary invariant remains
valid but must not be advertised as a connectivity algorithm. If true, a
primary comparison against matroid partition reconfiguration is still needed.

## Screen result and disposition

The frozen matroid_component_probe.py completed1,328 cases:968 exhaustive
unordered collections of up to three binary three-element rank tables and
360 seeded larger binary/uniform cases. There were1,027 feasible cases,
126,887 feasible assignment states,545 strict-slack cases and1,299 components.
No counterexample was found. These finite checks are developmental evidence,
not the reason the general assertion now follows.

Wdowinski's [Hall theorem for reconfigurations](https://arxiv.org/pdf/2511.04863),
Theorem2.2 and Proposition2.8, supply the strict-slack step. On labelled
copies (j,i), take the direct-sum matroid of the residual matroids M_i/S_star.
Color all copies of receipt j with color j; omit loop copies. The rank of
the union of color classes U is exactly the sum of the residual ranks on U.
It exceeds |U|. A matroid independence complex has topological connectivity
parameter at least its rank, so the cited theorem connects its colorful
independent transversals. Its adjacency requires the union of two successive
transversals to be independent. This holds here precisely for a valid move:
the receiving bin can accept the receipt, and the other bins retain their
previous independent sets. Thus its graph is the required assignment graph.
When the residual ground set is empty there is just the fixed assignment.

Combining that imported sufficiency with the tight-set argument above gives
the proposed component characterization. Source components, and hence any
continuous scalar readout, are connected when no nonempty tight set exists.
For fixed k one may enumerate all rank sums to compute S_star; this note
does not claim the best oracle complexity or implement a shortest path.

**PARK as a standalone novelty candidate.** The result is a useful corollary
for receipt models, but the difficult connectivity step is already supplied
by the literature. The source's full topological proof was not independently
reconstructed. Hanaka et al.'s ISAAC2024 basis-sequence theorem was also read;
its fixed-size disjoint bases and exchanges have different move semantics,
so it is not silently substituted for the theorem actually used here.
