# Retained-cut observation cover

**Working DEVELOPMENT derivation; Codex (GPT-6), October 14, 2026.**

This extends the executed direction of [s06 rational cut duals](../s06/cut_dual_derivation.md)
and [s08 induced objectives](../s08/box_regret.md). The dual lower bound itself
is inherited. No new LP duality or stochastic-cover principle is claimed.

## Source contract and fixed certificate

An admitted Boolean source has feasible feature vectors v in {0,1}^n. Checked
source consequences give A v >= k. Retain a nonnegative rational multiplier
lambda, with b=A^T lambda and K=k^T lambda. For any nonnegative objective q,

```math
\min_{v\in V}q\cdot v\ \ge\ L(q)
=K-\sum_i\max(b_i-q_i,0).
```

The bound holds even when b exceeds q. A proposal need not solve an LP, and
reusing it does not require dual feasibility for the new q. All original cuts
and the original source identity remain checked dependencies. We may also use
the always valid lower zero, separately from this one fixed certificate.

A requested repeated deterministic action consists of m complete source models
with counts a_i in {0,...,m}. These are m actual logical copies, not a random
mixture. Costs shared across copies lie in a Cartesian box [l,u]. Applying the
s08 induced objective q_i=a_i u_i+(m-a_i)l_i yields the regret upper

```math
B_\lambda(a;l,u)
=-K+\sum_i\max\{a_i u_i,\ b_i-(m-a_i)l_i\}.
```

Indeed a_i u_i+max(b_i-q_i,0) equals the coordinate maximum above. This also
recovers s06's binary fixed-action formula when m=1. The original regret is
nonnegative for a feasible repeated action. A negative computed B is therefore
evidence of a broken premise or arithmetic, not a usable negative-regret claim.

## Observable additive decrease

Define h_i(l,u)=max(a_i u,b_i-(m-a_i)l). An exact receipt t in [l_i,u_i]
decreases the retained bound by

```math
d_i(t)=h_i(l_i,u_i)-\max\{a_i t,\ b_i-(m-a_i)t\}\ge0.
```

Both terms in the new maximum are bounded by their old counterparts. With a
fixed action and fixed lambda, each coordinate receipt has the same reduction
regardless of the other receipts. The decrease is additive; overlapping query
groups contribute only their newly observed coordinates. For quota
Q=max(B_lambda(initial)-tau,0), the capped sum of observed d_i is a monotone
submodular realization-wise utility. Group queries preserve this by union of
their revealed coordinates. Query independence is not needed for this algebra.

This is a sufficient certificate stopping condition, not necessarily the exact
set of states where some valid action exists. A second certificate, a better
action or a new complete proof may close earlier. The distinction prevents
transferring an exact decision-cover claim from the earlier matroid service.

For m=1,a=1,l=0,u=4,b=2, an audit t=1 decreases this retained bound by 2.
The coefficientwise scalar transport in s08 guaranteed zero for that coordinate.
The extra contraction comes from retaining and reevaluating the checked dual
structure, not from interpreting one scalar lower as a richer proof object.

For an interior count, the best response is near b_i/m, clipped to the interval.
Endpoint responses can be less useful than a middle response. Thus learning only
which costs are low is not a universally sufficient acquisition objective.

## A genuine fallback and bounded planning

The next service should request a tolerance-valid repair, allowing the fixed
supplied action or another checked action. A full-information purchase followed
by an actual complete source solve supplies a fallback. Unlike the earlier
mandatory-anchor construction, its computation invoice is not constant merely
because its physical purchase fee is C. Charge and report those components
separately. A compulsory scalar anchor with a fixed replacement price would make
the no-anchor stopping predicate depend on absolute action cost; it would hide
the retained regret certificate's contribution, so it is the wrong test here.

For any query block of fee c, a conditional lower bound p on the probability of
terminating the certificate duty gives the one-step physical-fee rule c<C p.
The [s08 induction](../s08/budget_cover.md) still bounds expected fee by C, when
the lower probability bound is valid at every reached state. The event can be
the completion of one fixed certificate even if the real checker admits more.
Budget B gives realized physical fee at most B+C. Neither statement bounds
computation or proves optimal expected fee.

With independent finite coordinate laws, convolving the newly exposed d_i and
capping scores at remaining Q computes the block completion probability without
enumerating every source assignment or every complete future policy. Record all
convolution, candidate-block and retained-state costs. Correlated observations
require a valid conditional law or a conservative probability lower bound; using
an independent convolution under arbitrary dependence is not justified.

Overlapping query groups require particular care: even when coordinate costs
are independent, the outcomes of overlapping groups are dependent. The pointwise
cover property survives, but the independent-item greedy approximation theorem
does not transfer on that basis. Conditional convolution over the group's
unobserved coordinates is still correct under independent coordinate laws, so
the elementary baseline-improvement proof remains available. The service must
state which of these two different guarantees it actually uses.

Convolution is only cheap under an explicit bounded-score representation. For
integer scores and quota Q, a capped array has Q+1 entries; rational scores may
require scaling by a large denominator. Record this dependence and reject or
cap unaffordable planning rather than calling it universally polynomial in
the binary input length.

## Constructive boundaries to screen

Sparse positive feature clauses can be acquired by bounded resolution on the
actual input CNF, then yield ordinary packing rows. This is a partial consequence
extractor, not a general structural recognizer or complete source compiler.
Failure to find a cut must yield a weaker bound or fallback, never an invented
cut. Direct input clauses should not be charged as new resolution acquisitions.

A portfolio takes the minimum of several retained bounds. Its stopping predicate
is a union of certificate completions; an arbitrary maximum of their cover
utilities need not be submodular. Keep this separate from the single-certificate
cover theorem. One-certificate probability lower bounds still permit safe
baseline improvement, at the price of potentially missing joint opportunities.

The ordinary disjunctive construction in Deshpande et al., section 4.1 Lemma 1,
supplies a valid alternative: for fixed certificate utilities g_j with positive
quotas Q_j, use product(Q_j)-product(Q_j-g_j). It reaches its goal exactly when
one certificate completes and is pointwise monotone submodular. A two-factor
proof writes the marginal of the product decrease as the first decrease times
the second residual after insertion, plus the second decrease times the first
residual before insertion. Each nonnegative factor decreases as the observation
set grows. Induct for several factors. This imports an established construction;
its multiplied quota and bit lengths must be charged. It does not make the
joint completion probability equal to a product when certificates share costs.

Next checks: exact bound and additive contractions on nonmatroid sources;
source-bound extraction with altered-proof controls; the gap between a scalar
lower and retained dual structure; query-group convolution against enumeration;
then a declared small paid service only if the setup screen is favorable.
