# S13: acquisition bundles from sparse value terms

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; hypotheses revisable.
Parents: S11M sparse policy values and S12 partial policy-bank receipts.

## Termwise lower receipts and a paid batch

Fix a versioned utility polynomial y(x)=a0+sum_e a_e*chi_e(x), x in {-1,1}^m,
known to lie in [0,1]. Primitive computations reveal coordinates at known
nonnegative prices q_i. The semantics must warrant their outputs; the pricing
and forecasting model do not establish truth. For revealed set A, a simple
lower receipt is

    z(A,x)=a0 + sum_{e subset A} a_e*chi_e(x)
                 - sum_{e not subset A} |a_e|.

It is monotone in A and never exceeds y. Clip at zero for the statistical
source if necessary. Unlike canonical polynomial simplification after partial
substitution, this intentionally retains separate terms. It can therefore miss
early cancellation benefits. Its restricted structure makes batch planning
tractable, and is a comparison/design choice rather than an optimal bound.

At a current transcript, fix a nonadaptive additional batch B before its
outputs. Let R_e be the still-unrevealed coordinates of a pending term, and
m_e be a supplied conditional forecast for its full signed parity. Completing
the term improves the un-clipped lower receipt by |a_e|+a_e*chi_e, with forecast
reward r_e=|a_e|+a_e*m_e>=0. For a coherent conditional model this is its exact
expected termwise improvement. Under independent uniform unresolved bits,
m_e=0 for every pending term. Arbitrary bounded forecasts remain advice only.

For a fixed posterior Q and a context occurring n_i times among t actual iid
draws, multiply each policy's term reward by Q_theta*n_i/t. The resulting sum
is exactly its predicted improvement in the un-clipped PAC-Bayes lower bound:
the KL penalty is unchanged. This is a **certificate-improvement objective**,
not automatically expected decision utility or a calibrated value of computation.
If the original certificate is negative, clipping can change its incremental
economics. Reoptimizing Q later cannot invalidate the source, but is not part
of this fixed-Q planning identity.

The acquisition problem is

    max_B sum_{e: R_e subset B} r_e - sum_{i in B} q_i.

A single parity term with at least two unknown bits has zero one-bit marginal
reward at the empty batch; every positive bit price defeats myopic purchase.
Nevertheless buying all its bits has positive objective if r_e exceeds their
total price. Shared bits can make several individually unprofitable terms
jointly profitable. Singleton-greedy is therefore only a diagnostic baseline.

## Ordinary maximum-closure solution and certificate

Create a positive-weight node for each reward r_e and a negative-weight node
for each cost -q_i. Add arcs e->i for all i in R_e. A closed set selecting a
reward must buy every prerequisite. Source->reward capacity r_e, bit->sink
capacity q_i, and prerequisite capacity M>sum_e r_e yield a min-cut encoding.
The empty acquisition gives cut sum r, so an optimum never cuts an M arc.
For any finite feasible cut, cut capacity equals sum r minus its net objective.
With nonnegative rewards, all completed reward nodes may be included. Thus a
minimum cut gives an exact optimal **nonadaptive priced batch for this surrogate**.

A candidate flow with capacities, conservation, and value equal to a candidate
cut supplies an exact rational optimality witness. This checker can be small
and independent of the numerical or combinatorial flow-search implementation.
It does not certify forecasts, prices, primitive semantics or actual usefulness.
No hard resource cap, adaptive observation tree, alternative OR proof route,
or arbitrary uncertainty over prices is silently covered by the reduction.

Primary comparison: Hochbaum (2004), *Selection, Provisioning, Shared Fixed
Costs, Maximum Closure, and Implications on Algorithmic Methods Today*,
pp. 709-713, sections 1 and 2.1, explicitly gives arbitrary prerequisite sets,
shared item costs and the bipartite min-cut reduction. Those pages were read
in the [author-hosted paper](https://hochbaum.ieor.berkeley.edu/html/pub/MS-50-anniversary-selection.pdf).
The optimization principle is imported unchanged. The proposed adaptation is
the mapping from partial compiled value terms, cached sample multiplicities
and posterior weights into those rewards. Picard's 1976 publisher abstract was
also accessible; the earlier author report's PDF timed out and was not read.

## Forecast sensitivity and limits

For two reward vectors r and rhat, let epsilon=sum_e |r_e-rhat_e|. Every batch's
objectives differ by at most epsilon. Therefore an exact rhat-optimal batch has
at most 2*epsilon regret under r (prices fixed). If each individual error is
bounded separately, only terms completed by either competing batch are needed
in that bound. This does not supply the errors: validating conditional model
forecasts remains an acquisition/evidence duty.

Mixtures of fallible forecasters can supply their weighted m_e; the same
ordinary closure optimization applies. A model mixture is not evidence for
itself. Robust max-min batch choice, adaptive replanning after observations,
and economic comparison with a full conventional metareasoning controller
remain open. The claimed expected values require coherent conditional forecasts;
sound lower receipts do not require that forecast to be correct.

## First cheap development screen

[acquire_flow.py](acquire_flow.py) implements ordinary augmenting-path max flow
with rational capacities and a separate capacity/conservation/cut checker.
[acquire01.json](acquire01.json) contains 100 small cases matching exhaustive
batch search, 226 receipt-refinement checks, and 156 exact conditional batch
expectation checks. Both the parity and shared-prerequisite fixtures cause
singleton greedy to buy nothing, while closure net objectives are 1/4 and 1/8.
An 80-primitive, 240-term supplied graph took 106.765 ms for solve plus check.
These are surrogate objectives and supplied prices; primitive computation
economics have not been measured. The conventional closure control is identical.

## Rejecting a tempting stronger interpretation

Take two terminal actions with the identical utility (1+chi)/2, where chi is
an unknown fair parity. Both lower receipts start at zero; learning chi raises
their expected certificate by 1/2. But the best terminal action's expected
utility remains 1/2, with or without learning. Every positive acquisition price
makes the actual decision worse. Hence positive certificate-improvement value
does **not** license a paid decision. This is a substantive objective defect,
not a failure of the lower-bound or max-flow algebra. Retain S13 as an evidence
scheduling primitive and repair decision planning using action contrasts in
[contrast_acquisition.md](contrast_acquisition.md).
