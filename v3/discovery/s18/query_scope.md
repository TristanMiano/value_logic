# A smaller requested answer can make query competitiveness harder

Codex (GPT-6), DEVELOPMENT, s18. Early rejection of a proposed geometric
acquisition shortcut; the lower bounds are ordinary search reductions.

Suppose each of n>=2 scalar points is initially known only to lie in(-1,1).
A unit-cost query returns its exact value. The requested answer is whether0
lies in their convex hull, not the entire hull or the identities of all its
boundary points. Correctness is required for every compatible input.

Consider inputs with one point equal to0 and every other point equal to1/2.
The omniscient certificate optimum is1: query the zero point. Any deterministic
algorithm has an all-positive query path; placing the unique zero at its last
queried index forces n queries. Before that query, the all-positive completion
still makes the correct answer false. The competitive ratio is therefore at
least n, even in dimension one. Querying all points matches this upper bound.
Randomization against a uniformly located zero forces expected(n+1)/2 queries
by averaging over positions in the all-positive path; this is already linear
against the same one-query certificate optimum.

This is not merely a zero-boundary degeneracy. Restrict all exact inputs to
{-1/2,+1/2}, and promise one negative point and n-1 positive points only for
the lower-bound distribution, not as information supplied to the algorithm.
Every such positive instance has a two-query certificate. The all-positive
completion still has to be distinguished, so deterministic worst cost is n.
Under a uniformly located single negative, a zero-error randomized algorithm
uses expected at least(n+1)/2+1/n queries: it must find the negative, and if
it finds it first it still needs a positive. The resulting ratios are n/2
and(n+1)/4+1/(2n). The actual hull has a1/2 interior margin in every one of
these positive instances. A margin alone does not eliminate hidden-index search.

The bounds concern information queries only. Arithmetic, storage and detecting
already settled cases have not been billed. They also do not contradict
constant-competitive full-hull identification algorithms: their output duty
and omniscient comparator are different. One cannot transfer a guarantee by
silently replacing that comparator with the much smaller certificate for one
requested decision.

## Consequences for this program

A fallible model that accurately proposes a zero or a useful opposite-sign
witness can greatly improve a particular run. That is ordinary advice-guided
search, and its benefit must be measured against the strongest search policy
with the same information. A deterministic universal constant-competitive
claim for this interface is already ruled out. No new harness is warranted
for that rejected claim.

An aggregate value query is a different interface. A truthful bound on the
minimum and maximum can certify membership without disclosing either extremal
point. That recovers the value-only receipt mechanism, but it does not make the
aggregate query free. Its acquisition cost and any already returned witness
must be included before comparing it with point queries.

Likewise, selecting verified uncertainty regions by ordinary circle coverage
can give a compact certificate for a fixed action. It does not determine which
unverified or refining query will be useful. Predetermined nested regions,
exact-point revelation and stochastic proof success are distinct contracts.
