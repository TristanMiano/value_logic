# Positive value observations and a common least action

Codex (GPT-6), s18 DEVELOPMENT. A new information-contract screen, not a
claim of a new optimization principle.

Let a nonempty unknown F be a subset of {0,1}^d. An exact value query returns
v(w)=min_(x in F) w dot x, without a witness. If F is meet-closed, it has the
least point l=AND F. Every nonnegative weight vector has the same minimizer:

    v(w)=w dot l, w>=0.                                    (V1)

Thus d coordinate values determine an executable feasible action and all
future nonnegative-weight optima. These are facts about one deterministic
least action, not probabilities over unresolved propositions. A returned
minimizer from one strictly positive query would already give the same
information. Any claimed gain must justify the value-only access restriction,
and price acquiring the values and verifying the closure warrant.

There is also a useful check without assuming meet closure. Obtain
l_j=v(e_j) and the additional scalar v(1). Every feasible x dominates l.
Then

    l is feasible iff v(1)=sum_j l_j.                      (V2)

The forward implication is immediate. For the converse, a minimizer of
the sum has nonnegative coordinate gaps with total zero, so it equals l.
For binary F the gap is an integer: certified upper/lower intervals proving
v(1)-sum_j l_j<1 can suffice after the individual l_j have been identified
exactly. Intervals that leave those coordinates ambiguous do not authorize
rounding an arbitrary point into F.

With meet closure, subset-weight queries are ordinary subset sums of l.
Sparsity and a restricted measurement alphabet can invite group testing or
compressed recovery. An unbounded-precision lexicographic weighted value can
encode l in one answer; counting that as one unit-cost bit query is unfair.
Neither observation creates a new inference method by changing its name.

For a counterfactual addition of known Horn constraints, the old least action
remains least whenever it satisfies the added constraints: the new feasible
set is a subset of F containing l. It remains optimal for every nonnegative
weight. If a constraint is deleted, source inclusion alone only supplies
l_new<=l; it need not identify any changed coordinate. Ordinary unit
propagation and dependency-aware truth maintenance are the direct controls
when the formula is available. Park the generic counterfactual-reuse claim.

The constructive lesson is to specify whether a scalar service hides a
witness that a normal solver would return cheaply. Equations(V1)--(V2) are
elementary common-minimizer facts; they do not warrant a new family or a
readiness forecast by themselves.
