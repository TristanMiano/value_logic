# Where coupled computation-cost information actually helps

Codex (GPT-6), October 11, 2026. DEVELOPMENT, constructive screen of S06.
Continues the [stopping-pair construction](../s01/comparison.md).

## 1. Completed execution removes one side of the uncertainty

Let the selected procedure A finish, with checked receipts R and known complete
cost a. Every completion of R follows the same deterministic A trace, so
C_A(x)=a throughout that source. Consequently

    range_R(C_A-C_B) = [a-max_R C_B, a-min_R C_B].

The joint comparison is then no stronger than *exact conditional single-policy
cost bounds*. This is an elementary but consequential obstruction to using the
quadratic pair kernel for every post-execution learning update. The previous
cheap replay interval was a weak comparison, not the best ordinary control.
This conclusion needs deterministic replay and complete accounting of A's bill;
unobserved stochastic overhead is outside the exact constant premise.

For static k-of-n policies with outcome-independent nonnegative prices, exact
single-policy bounds cost O(n) unit work. At a possible final coordinate t,
choose output e and K=k (e=1) or K=n-k+1 (e=0). A stop is feasible iff t can be e
and the preceding prefix has f known e bits and u unknown bits with

    f <= K-1 <= f+u.

Forcing t=e then gives K winning bits, so the opposite certificate cannot occur.
Scan the two outputs and running prefix counts; take minimum/maximum feasible
prefix bills. Nonnegative prices also make these bills monotone in stop index.

After A has supplied a certificate, its output e is already fixed across R.
The lower endpoint for B is obtained by setting every unknown bit to e; the
upper by setting every unknown bit to 1-e. At least K fixed e bits prevent the
opposite outcome in either completion. B stops respectively at its earliest or
latest possible Kth e. Two ordinary replays therefore attain both endpoints.
Outcome-local prices break monotonicity of total cost under this replacement,
so that extension still needs order-statistic optimization, not this shortcut.

The useful new direction would need pre-execution information, comparisons
among two unfinished policies, a cheaper compressed library update, or a
different shared-computation structure. Do not claim the pair kernel itself
improves completed-policy feedback over this O(n) method.

## 2. An elementary complete dominance characterization

Assume the source is all bit vectors, all coordinate acquisition prices are
strictly positive (possibly outcome-local), setup fees are equal and per-query
control charges are common and nonnegative. Let m=min(k,n-k+1). Every execution
queries at least m bits. Two fixed orders have identical costs on every vector
iff their first m coordinates have the same set and all subsequent coordinates
appear in the same order. Otherwise neither order pointwise dominates the other.

Proof of sufficiency: the first m bits must all be purchased, regardless of
their internal order, and thereafter the same checked set and suffix are used.
For necessity/incomparability, take the first j>=m where the prefix sets differ.
If j=m, choose the outcome e whose certificate needs m bits, and set precisely
the m bits in B's first m positions to e, all others to 1-e. B stops at m;
A must purchase every one of these winning bits and at least one extra, so
A costs strictly more. Exchanging A and B gives the reverse witness.

If j>m, both prefixes at j-1 have the same set S, while B's jth bit b and
A's jth bit a differ. Choose m-1 arbitrary members of S to be e and also set
b=e; set all other bits to 1-e. B stops exactly at j. A must first buy all of
S, then its different a, and continue until b; its purchased set strictly
contains B's. Exactly m e bits exist globally, so neither execution can obtain
the opposite certificate. Strictly positive prices make A more expensive.
Swap A/B for the other witness. This also proves the necessity statement.

For unit prices there is a shorter no-strict-dominance argument: all fixed
orders have equal expected cost under a full-support exchangeable input law;
pointwise inequality would force pointwise equality. The prefix construction
is stronger because it handles unequal, outcome-local positive prices and
explicitly constructs the two counterexamples in O(n) work.

After removing common receipts for a **live** remaining-cost comparison, the
same result applies to the residual all-completions threshold problem. Thus
the pair kernel cannot find live robust dominance between genuinely different
orders merely from such receipts. Setup differences, zero-cost computations,
checked correlations, or another objective can change this premise.

This narrows S06 substantially: exact pair bounds may still quantify maximum
regret or compare differently priced guidance, but universal elimination of
unequal orders is unavailable in this base model. A fair ordinary control can
answer the dominance question in O(n), without the quadratic kernel. The proof
is developmental and does not assert literature priority.

## 3. Constructive repair

Use a statistical *selection* criterion or a regret tolerance while retaining
sound output checking. Alternatively introduce justified logical correlations
between subcomputations, which the all-completions kernel deliberately ignores.
A source constraint is useful only if discovering/checking it costs less than
the computations it saves. The next direction is comparative feedback on such
a compressed logical source, with fully charged preprocessing.

## 4. Cheap developmental check

`python v3/discovery/s02/feedback.py v3/discovery/s02/feedback01.json` checked
5,039 order/threshold cases with n<=6: 43 equivalent-order cases were checked
on all truth vectors, and 9,992 strict endpoint witnesses were checked using
positive outcome-local prices. It also matched the two-replay feedback bounds
to 3,400 compatible completions in 270 fixtures with n<=9. The
[source-bound record](feedback01.json) preserves counts and examples. This is
a small principal-generated development probe, not independent confirmation.
