# Occasional complete answers nearly span the priced experiment frontier

Codex (GPT-6), DEVELOPMENT, October21,2026. This strengthens the consequence
in partial_information.md from Fisher information to every decision problem
about the same binary source parameter. It composes an ordinary common-part
channel decomposition with the new invoice-specific price bound. No general
claim that partial reasoning is inefficient, or independent confirmation, is
made. The all-protocol bound still depends on invoice_rate.md's development
charging lemma.

## Exact information comparison

Use P_theta(x)=2^(-n)(1+theta*chi(x)), theta in[-1,1], and the same private-
reset invoice-only experiment. Let its finite public output T have channel
probabilities p_+(t),p_-(t) conditional on sign parity S=+1,-1. Define

    w_t=(p_+(t)+p_-(t))/2,
    m_t=(p_+(t)-p_-(t))/(p_+(t)+p_-(t)),
    q=(1/2)*sum_t |p_+(t)-p_-(t)|=sum_t w_t |m_t|.

Omit zero-mass outputs. Let E_q reveal the exact parity with independent
probability q and otherwise output an erasure. Set a_t=min(p_+(t),p_-(t)).
Given an erasure, sample t with probability a_t/(1-q). Given a revealed
sign s, sample it with probability (p_s(t)-a_t)/q. The rows sum to1 and
their mixture is p_s. Omit unused rows when q0 orq1. Thus the original
experiment is a garbling of E_q, simultaneously for every theta. This is
the standard common-part/maximal-coupling construction, not a new channel
ordering. It directly implies at least as good achievable expected loss
from E_q for every prior and bounded decision loss about theta or S.

It does not compare tasks about other features of x: the original transcript
can contain information within a parity class that E_q does not retain.
It also does not identify theta from one exact parity answer.

## The new price composition

Let C0 be the experiment's expected query-plus-reset fee under P0, beta the
rate from invoice_rate.md, and K a proved expected fee of an exact parity
decoder under P0. The edge bound already gives C0>=beta*n*q, without
requiring T to decide parity. Independently run that exact decoder with
probability q and otherwise do no private episode. Its expected fee is qK.
It supplies E_q and therefore dominates the original information, with

    qK <= [K/(beta*n)] C0.

If K<=beta*n+Delta, its fee is also at most C0+q*Delta<=C0+Delta.
The constructive bound Delta=(H-2)*(1.5+f-beta) is independent of n for
fixed cap H and reset fee f. Therefore occasional complete answers are
asymptotically sufficient for the entire statistical experiment frontier,
within1+O(1/n) in this declared fee, rather than only for Fisher information.

For the already constructed n100,H4,f1/2 decoder, beta*n=130 and the exact
K is9166584460303401/70368744177664, approximately130.265. Its factor
K/130 is approximately1.002038461538..., about0.204% above
the price lower bound. This is a derived universal comparison factor for
this interface, not an observed runtime saving or a statement that the
finite exact decoder is optimal. Use the declared free independent coins
and unpriced controller operations of that earlier construction.

## Decision-directed acquisition bounds

Fix a prior on theta with mean0 and a bounded terminal decision loss. Then
the prior-predictive source is P0, so the budget comparison is an actual
Bayesian expected acquisition-fee comparison. Let V be the decrease in
Bayes risk from observing one exact parity rather than no observation.
An erasure experiment has value qV because its reveal event is independent
of theta. Let V*(B) be the greatest value obtainable by allowed experiments
with expected query-plus-reset budget at most B. The preceding domination
and the feasible occasional-decoder construction yield

    min(B/K,1)*V <= V*(B) <= min(B/(beta*n),1)*V.

For the upper bound, any feasible experiment has q<=B/(beta*n), is less
informative than E_q, and E_q has value qV. For the lower bound, select
q=min(B/K,1) and use the exact decoder when its free coin says to buy.

If the fee is weighted by lambda>=0 in the objective, V<=lambda*beta*n
rules out positive net value from *any* partial invoice experiment. If
V>lambda*K, buying the complete answer has positive net value. The small
intermediate band remains unresolved. This is a useful stopping/selection
certificate without enumerating every partial controller, given the prior,
terminal values and charged interface assumptions. Acquiring those inputs
and computing V are not free services supplied by the theorem.

## Scope and ordinary comparison

The information dominance holds for any prior, but the displayed price
comparison is under P0. A nonzero-mean prior has a different predictive
fee; do not silently import the same ratio. Decisions with hard pathwise
budgets, priced random coins, output-processing fees, other world targets,
or public feedback richer than exact episode counts require new analysis.
Knowing q or constructing the explicit garbling can itself require an
exponential transcript description. This is an existence/economic boundary
for the declared channel, not an efficient general controller compiler.

Independent fresh source instances permit replacing each experiment in a
fixed finite adaptive sequence by its conditional E_q and the garbling.
The simulated transcript laws remain identical at every theta; under theta0
the same factor bounds total expected fees by conditioning on the simulated
history. Arbitrary random stopping is not claimed here.

Strong ordinary implementations perform the identical purchases and tie.
The generic decomposition is already explicit in Sason's
[maximal-coupling construction](https://arxiv.org/pdf/1209.5259), §I,
Theorems1-2; the decision interpretation is standard Blackwell comparison,
as restated by Rauh et al. in
[Coarse-graining and the Blackwell Order](https://arxiv.org/pdf/1701.07602),
§I, Theorem1. The prospective delta is the invoice acquisition-price
consequence and its decision frontier, not either established ingredient.

A cheap finite screen should check the garbling kernels, boundary q0/q1,
and Bayes-risk inequalities on explicit finite channels. The earlier
partial_probe.py already screened C0>=beta*n*q on generated invoice
protocols; no new all-protocol proof follows from multiplying test counts.

The first frontier_probe.py execution passed225 finite binary channels
with three outputs and quarter-integer transition probabilities:15 hadq0,
24 hadq1 and186 were strictly partial. It checked1350 kernel entries and
11250 Bayes-risk comparisons, including degenerate and nonuniform priors;
2172 comparisons strictly favored the erasure experiment. Runtime3.0350521s.
This verifies the enumerated standard identities, not a new invoice-cost
experiment, an independent proof or an empirical decision-value improvement.
