# Repeated invoices on one instance change the information limit

Codex (GPT-6), DEVELOPMENT derivation. The population result in
[invoice_information.md](invoice_information.md) explicitly uses fresh
independent worlds. This note changes the operation interface, rather than
silently importing that theorem into a different experiment.

## Fixed repeated-instance contract

Draw one Boolean world X on n>=2 bits and keep it fixed for k episodes.
Episode j can make at most H_j distinct queries, where 1<=H_j<=n, and reports
only its invoice. A fresh private evaluator has no memory of prior answers.
The public learner may retain past invoices and choose the next episode's
policy from them. Fees are fixed positive query fees as before; answers and
an outcome-dependent terminal charge are not additional outputs. The same
coordinate may be bought again in another episode and is charged again.
There is no private same-world carry of unseen answers between evaluators.

Put d=min(n,sum_j(H_j-1)). The linear span of all complete-transcript event
probabilities, viewed as functions of X, is EXACTLY the degree-at-most-d
Boolean character space V_d.

For the upper bound, fix one transcript and private random seeds. Along that
transcript, each chosen episode policy is fixed by the earlier invoices.
Its invoice-event indicator has degree at most H_j-1 by the single-episode
proof. The transcript indicator is their product on the SAME X; multilinear
reduction cannot increase degree, giving at most sum_j(H_j-1). Average over
independent policy seeds to cover randomization. Public adaptivity introduces
different products for different transcripts, not a larger degree bound.

For the lower bound, take any character chi_S with |S|<=d. Partition S into
sets S_j of sizes at most H_j-1. For every nonempty S_j, query its coordinates
and then buy an unqueried marker precisely when chi_(S_j)=+1. A marker exists
because |S_j|<=n-1. The invoice decodes that character. The product of decoded
characters equals chi_S(X). It is a linear combination of transcript event
indicators, so chi_S lies in the span. Empty groups need no acquisition.
All query and marker fees remain charged; no new physical observation is
claimed in this derivation.

It follows that the full arbitrary population law is identifiable in this
repeated-instance experiment exactly when sum_j(H_j-1)>=n. Below that threshold,
even and odd uniform laws remain indistinguishable because their low-degree
moments agree. At or above it, all Boolean characters are in the span.
This is identification from the FAMILY of permitted experiments, not recovery
from one realized transcript, and it says nothing about the number of fresh
instances needed for accurate population estimates.

## Two useful comparisons

For n=5, episodes of caps three and four can report characters on disjoint
groups of sizes two and three. Their product reveals the fifth-order parity,
which no single episode with at most five distinct queries can reveal through
its predictable invoice alone. The repeated experiment can use seven paid
queries in total, including repeated coordinates serving as markers. There
is no contradiction: the operation menu and total bill changed.

Conversely, if episodes instead use independent fresh X_j, the product of
decoded characters is a product of moments, not the joint moment of X.
The parity ambiguity persists under adaptive fresh-instance episodes, as in
the earlier induction. Confusing these two sampling contracts would create a
false general impossibility or a false free identification claim.

On a checked affine source, apply the earlier dual-coset rank calculation to
V_d; the threshold is d>=rho(C-perp), subject to the already stated degenerate
singleton case. This is a direct corollary, not a new coding theorem. Exact
support premises, misspecification sensitivity and sampling prices remain.

## Disposition

The mechanism is ordinary composition of measurement channels and polynomial
spans. Its role in this program is an explicit delta under a counterfactual
change to available operations: repeated access can recover information that
fresh cost observations cannot. This strengthens the interface specification
for Q2/Q4/Q5; it does not supply a general learner of mathematical truth or a
claim of novelty for polynomial-degree composition. No new test panel is
needed for the displayed finite product proof. Any implementation must preserve
the reset, fixed-world identity and duplicate-query billing assumptions.

## A constructed billing gain from repeated-instance access

Take three independent coordinates in the sense of an unrestricted logical
source (no probabilistic independence is assumed), with fixed fees (1,1,100).
The desired per-instance signal is the parity of coordinates one and two.
A single depth-three episode can query those two coordinates and use coordinate
three as its parity-conditioned marker. Its worst fee is 102.

That worst fee is unavoidable for exact one-episode parity decoding on the
full cube. Both relevant coordinates must be inspected on every world: if one
is not, changing it leaves the invoice unchanged but reverses parity. The
answer to the last query cannot affect an invoice with no later purchase. To
distinguish both values of the second relevant answer after both relevant bits
have been inspected, some compatible branch must therefore buy the remaining
coordinate. There are only three distinct-query purchases, giving a world with
fee 102. Buying the irrelevant coordinate earlier cannot solve this: the last
relevant answer would then have no later purchase through which to signal.
This argument is for exact one-instance decoding, not population estimation
through an arbitrary family of randomized noisy experiments.

Two reset episodes of cap two can do better. In episode one query coordinate
one and conditionally buy coordinate two as a marker; in episode two query
coordinate two and conditionally buy coordinate one. Each invoice reveals its
queried relevant bit, so their product gives the desired parity. The worst
total fee is four, including the repeated purchases. With a fixed per-episode
overhead f, the displayed totals are 102+f and 4+2f; the latter is cheaper
exactly when f<98. Actual setup and checking costs would also belong in a
service comparison. These fees and the interface are constructed assumptions,
not measured application performance.

The useful distinction is permission to revisit the same source, not a
special Value Logic implementation: any ordinary procedure given this same
repeated-instance interface obtains the same gain. Independent fresh worlds
would not reveal this per-instance parity or its arbitrary joint moment.
