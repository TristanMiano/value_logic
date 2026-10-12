# S13Q: a decision problem where the closure value is exact

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.

The earlier closure bound was generally only an upper bound on information
value. Here a different action representation makes the same computation exact.
It is a specialization to a structured decision model, not a new max-flow
algorithm or a law of unrestricted logical uncertainty.

## Separable decisions, shared information

There are m independent fair unknown bits X_i. A query reveals one named bit;
queries are pure observations and repeated purchases are unnecessary. There
are k outputs Z_e equal to the parity of nonempty mask R_e. The terminal action
is a vector a in {0,1}^k, with utility sum_e w_e 1[a_e=Z_e], where w_e>=0 and
sum w_e<=1. The action is represented by k independent output choices, not by
enumerating its 2^k possibilities. Query prices are q_i>=0.

At a leaf of any adaptive query tree, let B be the revealed bit set. Conditional
on the actual history, all unqueried bits remain independent and fair. A parity
is known exactly when its mask is contained in B, and is otherwise marginally
fair. Correlations between unknown outputs are irrelevant to the additive
utility because the action has independent coordinates. Thus the best expected
terminal utility is exactly

    c* + f(B),   c* = (1/2)sum_e w_e,
    f(B) = sum_{e:R_e subset B} w_e/2.

For any adaptive policy the expected net gain over c* is
E[f(B)-q(B)] <= max_B[f(B)-q(B)] = Gamma. A fixed maximizing batch B attains
Gamma, by choosing the revealed parity for completed outputs and any fixed
guess for the others. Therefore Gamma is the **exact optimal value across all
finite adaptive query policies**, computed by ordinary maximum closure. The
proof needs no enumeration of actions, worlds or observation histories.

The inference is unchanged if each bit has a random nonnegative completion
cost C_i, provided primitive pairs (X_i,C_i) are mutually independent, bits are
marginally fair, the full query reports its bit and cost only at completion,
and no other signal reveals unqueried states. Whether i is ever queried is
measurable without (X_i,C_i), so E[1[i queried] C_i]=Pr(i queried) E C_i.
Replacing q_i by E C_i gives the same expected-cost theorem. Cost may correlate
with its own bit. Cross-primitive runtime dependence, partial time signals,
mutable caches and hard realized-budget constraints need different analyses.

## Scalar prices and expected budgets

At tariff multiplier lambda>=0, the exact value is the profile Gamma(lambda)
already compiled in [price_profiles.md](price_profiles.md), with rewards w_e/2.
Thus this family supplies a nonconstant *decision-value* service, rather than
only an upper-bound service. Affine slopes identify the base cost of an optimal
batch. The graph, decision utility and source law must be bound together.

For an expected base-cost budget b, allow an independent lottery over batches.
Every adaptive policy induces a distribution over B and has the same expected
reward/cost pair as that batch lottery. Conversely every lottery is feasible.
The best gross gain is the finite linear program

    max sum_B p_B f(B),  sum_B p_B q(B)<=b,
    p_B>=0, sum_B p_B=1.

Its dual is min_{lambda>=0}[Gamma(lambda)+lambda b]. Profile breakpoints give
the upper concave hull of attainable cost/reward pairs. At an exposed segment,
mix its two neighboring batches to meet the expected budget; their mixture
attains the dual bound. At most two batches are needed. These probabilities
are chosen action randomization, not inferred epistemic weights over worlds.
This is ordinary finite LP duality applied to the exact decision reduction.

A hard per-run budget is different. One parity of two bits, total output weight
one and unit bit costs has zero attainable gain at hard budget one. An expected
budget-one lottery buys both bits with probability 1/2 and gains 1/4. Therefore
the concave profile does not solve the hard-budget problem. With two-bit masks,
the latter includes selecting at most b vertices to maximize the weight of
induced edges; no polynomial claim is made for that combinatorial problem.

## Boundaries and next constructive check

The earlier binary action on a weighted sum of parities couples the output
choices and generally has cancellation; the additive action-vector reduction
does not apply to it. General Boolean targets can reveal partial information
before all their prerequisites are known, so the leaf gain is no longer this
completion reward. Correlated input priors likewise break the marginal-fairness
step. Queries that choose among alternative bundles of prerequisites introduce
a different selection problem. These are structural assumptions, not cosmetic
notation choices.

Maximum closure is the established primitive described in Hochbaum's already
read selection-problem review; no new optimization principle is claimed. The
new developmental consequence is an exact end-to-end reduction for this
compressed decision family, including a certificate and expected-budget service.
Next compare small full Bellman trees to closure and reconstruct budget lotteries;
then measure source construction, flow and witness checks on a larger supplied
portfolio. An equally informed ordinary Bayesian planner can use the identical
reduction. External program relevance and the cost of warranting independence
remain open before any material-positive readiness forecast.

## Developmental checks and correlated-source extension

[portfolio01.json](portfolio01.json) retains 28 fresh small cases. The ordinary
maximum-closure optimum matches full-belief Bellman planning on 5,562 states;
the same values match when each cost is half its mean for bit 0 and 3/2 of its
mean for bit 1. All 140 expected-budget lotteries match enumeration of feasible
one/two-batch extreme points. The hard/expected-budget separation gives 0 versus
1/4 as derived. A supplied 256-bit / 768-output portfolio takes 2.492 ms to
generate and normalize, 8.143 ms to solve, and 2.020 ms to check, selecting 31
bits. Its net utility is 1631543/3175424. The 2^768 action count is implicit;
the comparison makes no claim to have run an exponential planner on that case.

The source need not consist of independent *named facts*. Let named facts x
satisfy a consistent supplied affine binary system A x=b, and let the prior be
uniform on its solutions. Gaussian elimination gives x=x0+N z with free
coordinates z independent and fair. If the available primitive queries reveal
these selected free coordinates (with declared prices), each target parity
c_e x is a constant phase c_e x0 plus the free-coordinate parity c_e N z.
The phase changes the correct output action, but not the gain from revealing
its support. Constant outputs have known value one and belong in the baseline.
The remaining supports/rewards compile into the same closure service. Charge
elimination and its relation check; do not assume arbitrary correlated priors
or arbitrary query sets reduce to coordinate queries at the same cost.

For a fixed matrix A and target rows c_e, a consistent change only to b leaves
the nullspace N and all target supports unchanged. Under the corresponding
uniform affine source and value-independent prices, the **whole acquisition
value profile and its optimal batches are invariant**. Update only the target
phases and output actions. Thus a checked right-hand-side assumption revision
can retain all paid optimization work. This is an algebraic counterfactual
semantics, not an inferred causal intervention. An inconsistent b is rejected
as an empty deployment source; it is not a warrant for every action.

If available queries are arbitrary overlapping linear measurements, their
span rather than a coordinate subset determines which targets are known.
The no-adaptive-benefit argument still applies under the uniform affine law
and fixed prices, but the subset reward may have substitutes as well as
complements. Two alternative ways to learn a target invalidate the simple
completion-hypergraph reduction. An arbitrary query library therefore needs
a separate optimizer; the closure claim is restricted to the stated basis.
This boundary is useful for assessing whether a compiler has silently granted
free access to a convenient latent variable.

The [affine prototype](affine01.json) checks 32 small systems, 532 complete
right-hand-side choices and 984 satisfying worlds against the compiled relation.
It rejects noninvertible row operations, inconsistent revisions and omitted
access to a required free fact. On a supplied 128-fact / 80-relation system
with 64 free coordinates and 256 outputs, source construction, elimination,
flow/check and 48 consistent phase updates total 5.464 ms; generating the same
source plus 48 cold reconstructions costs 191.603 ms. All 48 deliberately
inconsistent revisions are rejected. Its optimal net utility is 129/256 at the
**restricted free-coordinate query interface**, not over every original fact
that might physically be measurable. The prepared ordinary service is identical.

That restriction matters even in two facts. Under x_1=x_2, fixed elimination
may choose x_2 as the free coordinate. If observing x_1 costs 1/100 and x_2
costs 2/5, a one-output prediction gains 49/100 by querying x_1, versus 1/10
in the chosen x_2-only interface. A compiler's access check does not prove that
its selected interface includes every useful physical query. A new exact
rank-value family in [rank_values.md](rank_values.md) handles arbitrary linear
queries for a different, explicitly stated terminal objective.
