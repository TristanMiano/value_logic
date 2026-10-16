# The geometry of a counterfactual feedback request

Codex (GPT-6), DEVELOPMENT extension of S06's receipt replay. This compares
different allowed changes to the same computation order; it is one mechanism
with different interfaces, not a new family per distance measure.

## Certificate predecessor region

Let R be already purchased true receipts and C be any subset with Stop(C)=true.
For a declared family P of complete query orders define U_P(C) as the union
of all identities that occur no later than the last member of C in some order
in P. Acquiring U_P(C) minus R suffices to replay every candidate's exact bill:
monotonicity guarantees that each has stopped by that last certificate member.

Computing this union is itself a planning task. It need not be easy merely
because C is short. Nor is this acquisition list always necessary for a fixed
predicate: known logical relations can make some values irrelevant. For the
first-positive predicate with a single known positive i and all other observed
values zero, however, every unobserved j that can precede i is necessary in
the all-zero unobserved completion. Changing only that j to one gives an
indistinguishable observed trace with a different candidate bill, when fees
are strictly positive. This is a matching information lower bound for that
interface, not a claim that every predicate needs the entire union.

## Cheap certificate choice under position windows

Suppose every candidate places identity j in [earliest_j,latest_j]. Let
U=max_{i in C}latest_i. Any queried identity before the last certificate
member has earliest_j<U. Thus acquire every missing j with earliest_j<U;
members of C are already known. Infeasible position assignments can make this
bound loose, but never require buying a later value.

There is a cheap way to choose the strongest bound available from R: find the
smallest deadline u for which
Stop(R restricted to identities with latest_i<=u) holds. The predicate is
monotone, so a sorted sweep or binary search over deadlines suffices. This
minimizes max latest_i over all known certificate subsets without enumerating
those subsets. Include the predicate-checking cost. The fee/count bound is
monotone in u, so this also minimizes the particular window-based upper bound.

For bandwidth d, earliest_j=max(1,j-d), latest_j=min(n,j+d). The result yields
the earlier prefix cutoff M_C+2d-1 (with end truncation). Choosing a smaller
certificate maximum M_C can avoid extra purchases caused by already observed
high-index values that were irrelevant to stopping. Worst-case 3d-1 remains
attainable for an executing family member.

## A different distance gives a different exact budget

Let P be permutations with at most k inversions relative to the reference
(Kendall distance), k>=1. Putting identity j before identity i<j requires at
least j-i inversions: for each intermediate identity, either it precedes i
or follows j or creates another needed inversion, in addition to (j,i).
Equivalently, inserting j before i realizes this minimum j-i.

If the reference stops at L, an unknown j>L can occur before completion of
its certificate prefix only if it precedes some i<=L. Thus j<=L+k, and at
most k additional values suffice. This is sharp for a unique positive at L:
each of the next k identities can be moved just before L within the inversion
budget, and changing that value changes its candidate bill.

If an arbitrary pi in P executes first and stops with L receipts, let M be
their largest reference identity. Since moving M to position <=L costs at
least M-L inversions, M<=L+k. Every candidate stops by the last of these
receipts, and no item above M+k can precede any of them. Buying missing
identities through M+k therefore costs at most 2k additional observations.
This is sharp: move the unique positive at i=L+k forward k places. The k
omitted predecessors and next k successors can each precede i in an allowed
candidate. The usual indistinguishable-completion argument requires all 2k.

The same bounds follow for total absolute displacement at most 2k: reversing
the relative order of i<j requires total absolute displacement at least
2(j-i), and moving j directly before i attains that amount. These statements
concern observation counts; weighted acquisition fees and planning remain
separate. The finite-family automaton for the inversion budget has not yet
been implemented here.

## Cheap rejection: precedence width alone is insufficient

Consider two unrelated chains, each with n/2 items, and allow all their
interleavings. The precedence poset has width two. Execute the whole first
chain and stop at its last item, the unique positive. Every item in the second
chain can precede that positive in another allowed interleaving. Thus exact
all-family feedback can require n/2 extra values even at width two. A narrow
precedence frontier does not by itself imply a small acquisition budget.

For a general poset and a singleton positive i, an unobserved j can precede i
iff the poset does not require i before j. Incomparable chains therefore keep
a large feedback obligation. Bounded displacement, fixed small blocks and
bounded inversions supply additional locality that mere precedence width lacks.

This gives an early selection rule: measure the certificate predecessor region
before committing to a learning benchmark. A large expert family can have
cheap feedback, while a small-width representation can still have expensive
feedback. Neither policy count nor representation width alone answers the
information-acquisition question.

[df01](df01/attempts.jsonl) screens the two distance contracts on n=5,6,7
and k=1,2,3. All first attempts passed: 80,064 exact replay comparisons and
92 pairwise minimum-distance checks. Explicit larger examples attain 2k
extra receipts for both metrics. The input worlds are binary first-positive
examples; the general predicate argument is a separate derivation.

[Blanc, Koch, Lange and Tan (2022)](https://proceedings.mlr.press/v162/blanc22a/blanc22a.pdf),
Theorems 1.2--1.5 and section 2, give an important related query-complexity
comparison. They find nearest input changes for a monotone black-box function
using function-evaluation queries and implicit decision trees. Here the unknown
object is one fixed receipt vector and the output is costs of alternative
query orders. Their theorem is not imported across these different oracle
contracts; it is a relevant strong method if a later repair problem admits
their monotonicity and function-query interface.
