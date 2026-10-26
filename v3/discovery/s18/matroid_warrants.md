# Learning can be easy while exact fault-budget warrants are hard

Codex (GPT-6), s18 DEVELOPMENT. Separate from O18-M/v1. This is a reduction
to established minimum label cut, not a new hardness principle.

The online matroid adapter only needs sound pair-count thresholds and a
mistake-charging argument. It does not identify every utility vector or
compute the exact minimum number of corrupted optimum reports supporting
a countermodel. The latter task can be hard even for partition matroids.

Start with the set-cover/parallel-path label-cut construction in
ordinal_scope.md and a cover budget K no larger than the number of labels.
Replace every labeled edge x->y by

    x -> p_e -> q_e -> y,

where p_e and q_e are private to that edge. The middle comparison p_e>=q_e
retains the original label. Make the two connector comparisons trusted by
including K+1 separate copies of each corresponding pair report. Any utility
vector with at most K false reports must satisfy every connector.

For each label, collect its middle comparisons into ONE reported basis:
use a partition matroid with one two-element block{p_e,q_e} for each edge
carrying that label, all other ground elements loops, and report the basis
consisting of all p_e. This basis is optimal exactly when every p_e>=q_e
in that report. The pairs are disjoint because their endpoints are private.
A report is charged once if any of its comparisons is false.

There exists a compatible utility vector with u_s<u_t and at most K false
reports exactly when K labels can disconnect s from t, hence exactly when
the original set system has a cover of size at most K. In one direction,
threshold a countermodel to binary utilities; its false label reports cut
every path. In the other, remove a covering set of labels, put vertices
reachable from s at0 and the rest at1, and extend over the private edges.
All connectors hold and only the removed labels can be false. The size is
polynomial because K is bounded by the label count.

Therefore deciding whether every utility vector with at most K false
partition-matroid optimum reports satisfies u_s>=u_t is coNP-complete.
Non-entailment has a polynomial binary countermodel certificate, so the
membership claim holds for this explicit restricted input class. A proposed
action's exact optimality warrant inherits this obstruction by using the
rank-one target menu{s,t} and proposing s.

The contrast is useful but limited: single-winner reports admit exact flow
warrants; general partition-basis reports already encode correlated bundles
that make exact warrants hard. The cheap pair-count learner still has its
finite mistake guarantee under the same global round budget. Sufficient
warrants remain available; their incompleteness must not be described as
evidence that an action is actually unsafe. No average-case performance
claim, novelty forecast, or requirement to solve this exact warrant problem
is added to the bounded online contribution event.
