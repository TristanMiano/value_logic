# Jointly price inspection and direct change

Codex (GPT-6), DEVELOPMENT, October21,2026. A constructive adapter combining
ordinary graph-cut closure, verification and recourse. It lets unreliable
predictions affect the purchase bill while exact receipts and edits determine
correctness. No novelty, runtime superiority or causal adequacy is presumed.

## Interface and fixed certificate plans

An unresolved Boolean vector x is stable throughout one task. A query of i
returns its exact current bit for fee q_i>=0. Overwriting i with b has known
fee w_i^b>=0 and exactly the stated effect. Query/overwrite fees are additive;
the pre-action controller and cut computations must be charged separately.
The goal G consists of implications y_i=>y_j and optional unit requirements
on the final vector y. No other effects, shared fees or model constraints are
silently assumed.

A fixed certificate plan chooses each coordinate as uncommitted, guaranteed0
or guaranteed1. The chosen signs cover every goal clause: an implication is
covered by guaranteed0 at i or guaranteed1 at j. A guaranteed sign b can be
implemented by directly writing b, or by querying and writing b only when
the returned bit differs. Thus every completed plan succeeds on every x.
Changing a prediction affects its cost, not that guarantee.

Let d_i^b be the declared price for guaranteeing b. Encode guaranteed0 as
(z_i,v_i)=(0,0), unknown as(1,0), guaranteed1 as(1,1). The forbidden pair
(0,1) is excluded by v_i=>z_i. Every goal implication adds z_i=>v_j.
A required final0 fixes z_i0; required1 fixes v_i1. The total price is

    sum_i [d_i^0*(1-z_i)+d_i^1*v_i].

All hard constraints are implications and units, so ordinary minimum-weight
closure/minimum cut finds an exact cheapest fixed certificate plan. This is
the same graph primitive as earlier action compilers, now with each sign's
implementation price including an inspection/recourse option. Each sign is
selected at most once. Separate query-then-write and unconditional-write
options are collapsed by their minimum price, retaining the winning mode.

## Expected-price and interval-price interpretations

With known marginal p_i=P(x_i=1), use

    d_i^b = min(w_i^b, q_i + [1-P(x_i=b)]*w_i^b).

Linearity of expectation makes this exact for the fixed-plan class even
under arbitrary dependence between coordinates. It does not prove optimality
over adaptive policies, which may exploit observed correlations or select
which goal clause to cover after seeing answers.

With rectangular marginal bounds l_i<=P(x_i=1)<=u_i, replace P(x_i=1) by l_i
for guaranteed1 and P(x_i=0) by1-u_i for guaranteed0. The resulting plan is
minimax within the same fixed-plan class over *all* joint laws with those
marginal bounds. For any chosen plan, each selected bit has only one required
sign; the respective worst endpoints can occur simultaneously in a product
law. Thus the sum of separate worst fees is attainable, not merely a union
bound. A restricted correlated ambiguity set need not have that property.
Incorrect bounds can spoil the cost forecast but not execution correctness.

## A prediction-based plan with a blind fallback

Given arbitrary bit predictions hat{x}, set d_i^b=w_i^b except when b=hat{x}_i,
where d_i^b=min(w_i^b,q_i). A query-selected sign is bought on the assumption
that its receipt will match; all mismatches can be repaired by writing that
sign. Let Q be its total query fee and W its initially planned overwrite fee.
Let B be the price of the cheapest blind write certificate (the same cut
with d_i^b=w_i^b). Since the blind plan is an allowed option, Q+W<=B.

Make all selected queries before performing any overwrite. Compute R(x),
the total cost to correct the queried mismatches. Then execute whichever is
cheaper: the planned writes plus those corrections, or the blind certificate.
The exact executed fee is

    C(x)=Q+min(W+R(x),B) <= min(Q+W+R(x),2B).

If predictions match on queried bits, C=Q+W, the exact cheapest confirming
certificate price at the predicted world. All worlds remain safe and the
query-plus-edit fee is at most2B, regardless of prediction quality. This
compares to the blind certificate, not an omniscient zero-query optimizer
or a stronger adaptive audit policy. Controller/preparation prices are not
inside the factor2 unless separately bounded. If B=0 the optimized price
is0; zero-price inspections do not invalidate the inequality.

This is a mechanism for making fallible predictions useful without granting
them authority over success. The minimum-cut and bounded-fallback ingredients
are conventional. A primary comparison and a small exact screen are warranted
before assigning the composition a contribution delta.

## Stronger recourse and ordinary adaptive control

After querying, one may instead recompute the cheapest certificate using
every observed sign at zero additional price. Call this completion price
R*(h). It is at most both W+R(x) and B, so Q+R*(h) retains the2B guarantee
and can be strictly better. This extra minimum-cut computation is charged.
For an initial plan selected using arbitrary marginal predictions in[0,1],
the nominal expected-price optimum is at most B and its query fee Q<=B.
Thus the same reoptimization gives safe execution and a2B fee bound even
when all predicted probabilities are wrong. The exact rectangular minimax
claim above concerns fixed signs with individual corrections; reoptimization
improves that plan's fee but is not thereby a solved adaptive minimax problem.

An ordinary exact adaptive oracle is available on small cases. At a partial
receipt h, let R*(h) be its cheapest certified completion and let the next
query of any unobserved i reveal its original bit. Then

    V(h)=min(R*(h), min_i [q_i + E(V(h plus x_i) | h)]).

With no intermediate safety duties or side effects, writes can be postponed
until the end without losing information or raising fees. This recurrence
therefore covers interleaved query/write policies as well. It has up to3^n
receipt states and requires the joint conditional law; zero-probability
branches still receive safe write completions. It never treats a prediction
of probability1 as an unaudited hard fact. This is standard finite belief-
state dynamic programming, not a new solver or an efficient general method.

The first inspect_probe.py execution passed32 small rational panels,445
enumerated certificates,3043 cuts and1440 prediction/world checks. On the24
panels with n<=4, the adaptive oracle strictly improved the reoptimized fixed
plan on12; recourse reoptimization itself strictly improved7 of32 plans.
These are exposed toy cases, not a performance estimate for a workload.

Two explicit limitations matter more than their count:

- Independent bits: two antecedents each equal0 with probability1/2,
  implications from each to a consequent fixed0. Antecedent0 writes cost1,
  consequent1 costs3/2, and each antecedent query costs3/10. Other writes
  and consequent inspection cost10. The best fixed certificate costs3/2;
  querying one antecedent, continuing with the other only after a0 receipt,
  gives the exact adaptive optimum29/20. The initial query's immediate
  expected saving is only1/4, so a strictly myopic buyer also declines it.
- Correlated bits: G=(x0=>x1), equally likely original worlds00 and11,
  each query fee epsilon and each write fee1. The best fixed certificate
  costs1/2+epsilon. Querying one endpoint and, if necessary, the other costs
  3epsilon/2 on that law, with a write fallback on the off-support world10.
  At epsilon1/100 the exact finite gap is34-fold; as epsilon decreases it
  is unbounded. Hard success remains valid on *all* worlds. Thus marginal
  prices do not capture the potential value of adaptive correlation use.

The prospective benefit is a compact, exact fixed-plan optimizer and a
prediction-independent success/fee guarantee, not supremacy over adaptive
ordinary methods. Its closest-prior delta and complete controller cost
remain unassessed. The cheap strong control has already excluded a broad
optimality claim before a large application experiment.
