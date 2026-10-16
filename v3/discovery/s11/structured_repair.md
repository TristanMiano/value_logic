# Beyond a chain: a bounded-width repair adapter

Codex (GPT-6), DEVELOPMENT derivation, not an executed extension. This asks
whether the current positive construction is restricted to a linear toy source.
The answer below uses established constraint-satisfaction machinery; it is not
a new general tractability theorem for planning.

## Contract and conditional menus

Let source F and target G be conjunctions of explicitly represented Boolean
constraints on m variables. Supply a tree decomposition of the UNION of their
primal graphs, with B bags, width w, and a nice rooted form. A constraint's
whole scope must fit in one bag. The queryable set has size r. Keep the same
paid original-bit inspections, nonnegative fees, atomic terminal edits and
joint query/edit cap H as [safe_revision.md](safe_revision.md). Truncate H at
r+m. Obtaining/checking the decomposition is additional work.

For every reachable partial query assignment h and every target factor C on
scope U, compute the projection P_U(h) of the globally feasible F_h. Define
the allowed local mask relation

```math
S_U(h)=\{b_U:\ \forall u\in P_U(h),\ u\mathbin\oplus b_U\in C\}.
```

The conjunction of these relations is EXACTLY the uniformly safe mask menu.
The proof distributes the universal quantifier across the target conjunction.
No distribution or independence of factors is needed. Ordinary Boolean
junction-tree messages give globally supported bag assignments; their
projections give P_U(h). Testing all local truth/mask pairs costs at most a
factor 4^(w+1) per bag after factors have been assigned and consolidated there.
Include the input table sizes and factor-assignment work in preparation.
Raw local source relations alone would again be unsound. If F_h is empty,
make the branch abstain rather than deriving useful evidence from vacuity.

## The cap must constrain every realized mask

For a fixed h, a mask DP state records a bag assignment and the number of flips
on variables already forgotten strictly below the bag. Each variable is counted
exactly once, when forgotten. An introduce transition keeps the count; a forget
transition adds the forgotten bit; a join combines two child counts by addition.
Use an empty root and leaf convention. Disallow counts above H-|h| and reject
local masks violating an assigned factor. The resulting transitions have at
most O(B*2^(w+1)*(H+1)^2) size, allowing the quadratic join convolution.

Introduce nonnegative mass on each feasible transition tuple and state.
The outgoing transition mass of a state equals its state mass. For EACH child
slot separately, the sum of parent-transition masses naming a child state
equals that child state's mass. Root state mass sums to terminal-one private
reach. It is essential to preserve child slots: a join sends the same sampled
assignment into both subtrees, not half its probability to each.

These equations describe the exact convex hull of feasible mask realizations.
Every distribution over masks gives such masses. Conversely, sample a root
state, then a transition conditional on each reached state, recursively. The
local consistency relations give one global mask because bags have the running
intersection property; the count transitions enforce its total cap. Induction
down the tree recovers every transition marginal. Zero-mass states can use any
choice since they are not reached. Flip marginals are linear projections of
forget-transition masses, so the existing expected linear terminal cost still
applies. Independent rounding of those flip marginals is not sound.

## A common-world regret separator

Keep the private query-flow variables and aggregate expected cost row for each
full query cell z. For a comparator history h compatible with z, optimize jointly
over one source assignment x and one mask b in its certified menu. A bag now
has up to four possibilities per variable (truth,mask), with the same forgotten-
flip counter. Impose source factors on x, compiled menu factors on b and z's
pins on x. Add each variable's controller-minus-comparator cost at its forget
transition. Subtract the comparator's fixed query fee at the root. A separate
truth-only DP covers comparator abstention. This is the chain separator with
ordinary tree-decomposition joins; it never chooses a fresh source per branch.

There are at most 4^r compatible pairs (z,h). Max-sum epigraphs for these DPs,
the terminal realization polytopes and private query flow therefore give the
following conservative size bound after input preparation:

```math
O\!\left(r3^r+B\,4^{r+w+1}(H+1)^2\right).
```

This counts variables/constraints/transitions up to ordinary sparse local
incidence factors; input factor tables, coefficient formation and rational bit
lengths must also be accounted for. The formula is not an implementation
measurement. It is polynomial for fixed r,w, with H bounded by the number of
distinct possible operations. It is exponential when the source/target union
has large width or the queryable set is large. Cheap separate decompositions
of F and G do not suffice if their union is wide.

## Prior machinery and disposition

[Kolman and Koutecky (2015)](https://kam.mff.cuni.cz/~kolman/papers/CSP-published_EJC.pdf),
Theorem 1.1, Section 2.2 and Lemma 2.1 including the join argument, already
provide compact exact extended formulations for bounded-treewidth CSPs.
That is the relevant prior for global marginal consistency; local edge
marginals alone are insufficient in general. The explicit count and transition
construction above adapts it to a pathwise edit cap and the query-dependent
menu. It does not claim their formulation or the treewidth principle as new.

This extends the plausible verification target from chains to constrained
configuration families with a supplied small-width decomposition. No treewidth
prototype or application benchmark has been run. Before using this as a
load-bearing claim, reconstruct the augmented transition formulation and
coefficient-size bound, and check a branching decomposition with a join against
full masks. Do not spend a new large experimental panel merely to re-establish
standard bounded-width CSP facts. The potentially useful contribution remains
the paid-information/operational-repair adapter and its explicit comparator.
