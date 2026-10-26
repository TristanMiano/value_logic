# Scope of fallible ordinal receipts

Codex (GPT-6), s18 DEVELOPMENT; same-model derivations, not confirmation.

## Improving feedback is sufficient, but must be specified

For the pair-only strongest-path update, optimal responses can be weakened.
On all but C rounds, require the returned item i to be no worse than the
proposed j, and to be strictly better whenever j is truly suboptimal in
the available set. It need not be globally optimal. Then each false directed
comparison still occurs at most C times and every uncorrupted mistake still
increments a strict true pair. The same binom(d,2)(C+1)+C bound follows.
If strict improvement is required only when regret exceeds epsilon, the
same proof bounds the number of rounds whose regret exceeds epsilon.

This variant records ONLY i versus j. It cannot infer that i dominates
every available alternative. Nonworse self-feedback on a suboptimal j
violates the progress assumption and must count among the exceptional
rounds. The assumption is substantive, not inferred from receiving a reply.
The broader coactive-learning literature is a necessary comparator.

## Shared report faults: a tractability boundary

The exact cut construction in ordinal_cuts.md uses a report asserting one
winner is at least as good as every item in a set. Its unit-capacity report
node charges that entire star once. Arbitrary conjunctions of comparisons
in one report need not have this polynomial reduction.

For a general bundle of directed weak comparisons, thresholding a real
countermodel u_a<u_b to binary utilities again cannot create a newly false
report. Thus the minimum number of false bundles equals the minimum number
of labels crossing an a-to-b cut, with one label per report. It also equals
the minimum number of whole labels whose deletion destroys every a-to-b
path: a cut supplies such a deletion; a deletion supplies the reachable
side of a cut using only deleted labels. This is minimum label cut.

A direct set-cover reduction shows the obstruction. For each universe
element e, create an internally disjoint a-to-b path. Put one edge on this
path for each set containing e, labeled by that set. Each label forms one
report containing all edges with that label. Deleting labels disconnects
all paths exactly when their sets cover every element. If an element is
in no set, the set-cover instance is immediately infeasible and can be
handled before the reduction. The construction has polynomial size.
Hence exact arbitrary-bundle fault counting is NP-hard, even though each
report contains only ordinary weak comparisons and the underlying paths
are otherwise disjoint. This is a reduction to an established problem,
not a claim to have introduced minimum label cut.

The positive contract is therefore useful: a single reported winner has
an exact polynomial warrant with a shared fault charge; unrestricted
correlated batches cannot silently inherit that computational promise.
Pairwise expansion with a separate fault charge per edge changes the
source model. Treating the entire report as one fault preserves the
intended meaning but may change the algorithmic difficulty.

## The action family is part of the retained-information contract

Component order suffices for linear optimization over matroid bases; the
matroid extension supplies its explicit mistake argument. It need not
suffice after a change to a nonmatroid action family. Consider the only
allowed compound actions{a,d} and{b,c}. Utilities(4,3,2,0) and(10,3,2,0)
have exactly the same strict component order a>b>c>d, but their preferred
actions are respectively{b,c} and{a,d}. Even a completely correct retained
component order cannot decide this edited problem. The missing information
is about sums, not about a finer tie-break or more accurate order learning.

This rules out an unrestricted extension of the coordinate-order adapter.
Treating all compound actions as separate alternatives is an ordinary
fallback, but can enlarge the named universe exponentially. A counterfactual
change in the constraint family therefore changes both what information
must be retained and the relevant computation bound.
