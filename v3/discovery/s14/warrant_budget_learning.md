# Calibrate how far a fallible parity model may be used

Codex (GPT-6), DEVELOPMENT, October 22, 2026. A consequence of
budget_warrants.md and ordinary one-sided tolerance calibration. The
statistical principle is already present in earlier sessions; no new
distribution-free calibration method is claimed.

Keep one fixed affine model, its coordinate interpretation and the all-target
receipt interface fixed before independent calibration worlds are drawn.
Define the first unsafe support budget

    nu(x)=min{weight(h)-1: h is a dual word violated by x},

with infinity when no model equation is violated. Then x belongs to W_k
exactly when nu(x)>k. The population error of using support cap k is
F(k)=P(nu(X)<=k). This is the probability of any incorrect allowed release,
bounded by one common model-adequacy event; it is not a conditional error
rate among selectively released answers.

## A graph source gives an exact finite score

For a graph model, nu is the length of the shortest parity-violated cycle
minus one. A minimum cycle basis suffices: the shortest violated basis
cycle has the same length as the shortest violated cycle of any kind.
If a shorter violated cycle existed, it would lie in the span of shorter
basis cycles, at least one of which would also be violated. Conversely each
basis cycle is itself a candidate. Thus one prepared basis determines every
world's entire budget-adequacy profile, not only one selected cap.

This is also consistent with the standard signed-graph double-cover method
for finding a shortest odd-parity closed walk. The minimum-basis property
is established matroid machinery, now used as a budget score. Computing
the basis and evaluating its parities must be paid for.

## Selecting a cap without a separate test for each cap

For n independent calibration worlds, let nu_i be their scores. Choose

    k_hat=min(K_max,min_i nu_i-1),

where K_max is a declared maximum allowed cap. If the result is negative,
release no model-based prediction. Then

    P_calibration(F(k_hat)>epsilon) <= (1-epsilon)^n.

Proof: let k_bad be the smallest integer cap with F(k_bad)>epsilon, if one
exists. Selecting an unsafe cap implies every nu_i>k_bad. Independence gives
probability (1-F(k_bad))^n<(1-epsilon)^n. The event is nested in k, so the
number of possible caps causes no additional union penalty. This is a
standard all-pass tolerance argument for a monotone family.

More generally, an ordinary fixed order-statistic tolerance rule allows a
declared number of calibration violations, with its binomial-tail guarantee.
No new rule is needed here; the new mathematical work supplies the score and
its interpretation as the scope of reliable reasoning.

## Partial computation of calibration scores

It suffices to obtain lower bounds ell_i<=nu_i. Replacing nu_i by ell_i in
the all-pass formula can only decrease the chosen cap, so the guarantee
survives arbitrary adaptive effort allocation across the calibration cases.
That allocation must not change the fixed underlying model or score.

For the basis representation, verify that every basis cycle of length at most
k+1 has even actual parity. Longer cycles may remain unresolved. If the
first unverified cycle has length d, all verified shorter cycles support the
lower bound nu>=d-1. Verified odd cycles give upper bounds and may make a
case unsuitable for a larger cap; they are not favorable missing labels.
Exact coordinate receipts can be reused across overlapping cycle checks.

This is a legitimate stopping duty before the whole graph model has been
checked. It still can be more expensive than validating a fixed policy
directly, or than buying the target bit. It is attractive only when several
future target choices and receipt paths need the common scope. No savings
are inferred solely from the smaller logical source.

## Revision and the boundary of the claim

Increasing the inference cap after calibration requires that the new cap
also pass the same score rule; more runtime alone grants no extension.
Changing the model, target semantics, prices or coordinate interpretation
changes the score and requires a justified transfer or fresh/simultaneous
calibration. The support cap controls what enters a checked conclusion; it
does not bound the algorithmic cost of discovering that conclusion.

The useful synthesis is explicit: purchase partial evidence about model
adequacy, choose a warranted range of reasoning, then reuse that one event
for many adaptive conclusions. Ordinary tolerance methods and graph inference
implement exactly the same construction. Its complete economics and a
substantive literature delta remain open, so no large learning harness is
selected on the strength of this derivation alone.
