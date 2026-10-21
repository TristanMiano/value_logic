# Signed goals: a checked boundary for the ordinary cut optimizer

Codex (GPT-6), DEVELOPMENT, October20,2026. Uses established binary graph-cut
regularity and elementary signed-graph consistency. This is a scope adapter
for ordered_responses.md, not a new optimization method.

Allow any binary goal clause (y_i=b_i) OR (y_j=b_j). Choose a polarity s_i for
each coordinate and write y'_i=y_i XOR s_i. The clause becomes an implication
exactly when its two transformed satisfying values differ, namely

```math
s_i\mathbin{\oplus}s_j=1\mathbin{\oplus}b_i\mathbin{\oplus}b_j.
```

All such equations are checked by a graph traversal or a parity union-find.
Contradictory cycle parity rejects this *renaming certificate*, not necessarily
the underlying optimization instance. Units impose no pair equation. Remove
tautologies and repeated-variable clauses first. Availability constraints must
pass the same test; it is unsound to rename the goal while ignoring them.

For a flipped coordinate reflect the level and latent threshold:

```math
a'_i=K_i-a_i,\qquad \theta'_i=K_i+1-\theta_i.
```

Then 1-y_i=1[a'_i>=theta'_i], including always-on and always-off endpoints.
Reverse the price table and transform source projections and observations.
Availability level bits obey b'_(i,k)=1-b_(i,K_i-k+1). Thus a successful common
renaming reduces the complete problem to the positive-implication construction.
All feasible actions, prices and the maximal source warrant transport exactly.
Truthful threshold receipts stay unit comparisons. The same renaming remains
valid after source conditioning because it was checked at the goal/interface
level, independently of which threshold patterns happen to occur.

For example, a bipartite graph of mutual exclusions NOT y_i OR NOT y_j can
be handled by reversing one partition. An odd exclusion cycle fails this
test. This does not prove every odd-cycle instance hard; it only refuses this
particular reduction. General weighted binary satisfaction is already hard.

## A stronger static check, with a weaker reuse promise

For any binary goal, directly compile the action formula by substituting all
observed threshold pairs into each clause: y_i becomes b_(i,theta_i), with
endpoint constants. The result is still2CNF on action-level bits. A common
polarity can be sought on that *compiled* formula, including the level chains.
It may succeed even when the syntactic goal test fails, because source-specific
units, constants or missing patterns remove problematic clauses. This gives a
valid ordinary cut optimizer for that instance after simplification.

It does not automatically give the same optimizer after new observations.
Newly permitted actions may have a feasible relation with no such renaming.
Either retain the old safe action set or recheck the transformed formula.
The globally checked interface condition is stronger precisely because it
supports this reuse without relying on a fortuitous initial source.

The ordinary graph-cut criterion for a binary energy table E is
E00+E11<=E01+E10 (Kolmogorov-Zabih2004, Theorem4.1). An implication's forbidden
off-diagonal entry has this property; a lone forbidden diagonal does not,
unless a variable is reversed. Hard constraints can use a finite capacity
larger than every possible finite objective difference, with infeasibility
checked explicitly. No soft objective or hidden observation fee is dropped.

This broadens the declared fragment but supplies no measured application gain.
Local response, source-projection acquisition and warrant calibration remain
the same substantive premises as before. General monotone interference still
contains set cover and is not licensed by this signed-coordinate trick.
