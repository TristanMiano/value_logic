# S25: marginal-error acquisition without a product-law premise

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; parent S24.

S24's exact Bayesian planner depends on independence of edge parities. Marginal
calibration does not establish that premise. For example two unbiased equal
edges make the endpoint parity certain although the independent model predicts
zero magnitude. Retain the product model as a useful proposal, and derive an
alternative guarantee that needs only marginal error bounds.

Let E_e be the true edge parity, s_e a forecast sign fixed before the evaluation
task, and P(E_e!=s_e)<=d_e/2 with 0<=d_e<=1 under a declared task source. Edge
errors may be arbitrarily dependent. The root bit is known and edge queries
return checked parities at fixed prices. A fixed purchased set S gives the
forecast sign for a node by using checked labels on S and s elsewhere.
Its mismatch implies at least one unqueried path error, so a union bound gives
expected spin agreement at least `1-sum_(unqueried path)d_e`. If this is
negative, use a fair randomized prediction for that node instead. Thus a
valid expected score lower bound, excluding the common half-score, is

```
L(S) = sum_v r_v * max(0,1-sum_(e in path(v) outside S)d_e) - cost(S).
```

This guarantee is simultaneous over the joint laws satisfying the supplied
marginal bounds. It is not a claim that one joint law attains every node's
bound, or that optimizing L solves the full minimax decision problem. A chosen
fixed set's expected score is bounded without interpreting individual logical
truths as aleatory. Source inference for the marginal bounds remains separate.

Do not reuse unconditional marginals after selecting queries based on their
observed labels: selection can change error rates. This construction commits
the query set first; continuation would need conditional bounds or a fresh
source-level validation of the whole adaptive policy. A timeout is unresolved.

## Compact lower-value profiles

For a subtree with inherited path error budget z>=0, define

```
L_v(z)=r_v*max(0,1-z)
       +sum_(children u) max(L_u(z+d_(v,u)), L_u(z)-c_(v,u)).
```

All profiles vanish for z>=1: there is no positive lower prize and query costs
are nonnegative. They are nonincreasing convex piecewise affine functions.
The edge purchase difference L_u(z)-L_u(z+d) is nonincreasing because convex
slopes are nondecreasing. Hence buying is optimal on an initial interval, and
leaving the edge unresolved on a final interval (with tie choices explicit).

If t is a switch point, child knots k<t survive on the purchased branch and
child knots k>t+d survive on the unresolved branch at k-d. No knot occurs in
both. At most one switch knot is added; adding the local hinge adds at most
one more knot. A coarse induction bounds subtree knots by vertices plus edges,
so exact profiles remain polynomial, with quadratic worst-case total storage.
The bound can likely be sharpened; it is enough for a constructive prototype.

The set lower objective is increasing and supermodular before subtracting
modular costs: positive-part of an increasing affine function has increasing
returns. Ordinary lattice/DP methods again apply. Independence-free marginal
robustness is a change of warrant and conservatism, not a new union-bound rule.

## Comparison and a necessary decision distinction

For d_e=1-b_e, the product-model magnitude is product b_e, whereas the marginal
lower magnitude is max(0,1-sum d_e). The former can be much more optimistic on
long paths. At d=.2 on five unqueried edges, these are .32768 and zero.
Querying an edge can restore a positive robust lower magnitude, and shared
queries benefit several targets. The guarantee may be too conservative to buy
anything; preserve that outcome rather than assume correlation away.

An increase in L is not necessarily an increase over the *actual* score of a
different, unknown-law forecast policy. It certifies absolute score under the
declared ambiguity family and optimizes this particular lower objective.
The common fair-guess baseline has exact half-score under every truth, but
beating only that weak baseline would not by itself satisfy P3-POS01. Relevant
comparisons include conventional robust prediction/optimization with the same
marginal information and all its computation costs.

Next: implement the shifted convex-profile recurrence, test all fixed sets on
small trees, and enumerate arbitrary dependent laws satisfying the marginals
to check the returned score guarantee. Then compare the same source's product
and robust plans without treating their warrants as interchangeable.

Prospective screen: 32 fresh 3–7-node trees, seed 31873. Generate positive
integer weights on every edge-error world, then add no-error weight only as
needed to ensure every marginal error probability is <=1/2. This defines a
varied but finite collection of dependent laws, not all admissible laws.
Use their exact marginal bounds, enumerate every acquisition subset, and
check profile requests at knots, midpoints and 17 grid points. At z=0 check
the score guarantee of every fixed set against the actual dependent law and
record product-model and robust chosen plans separately. Add the explicit
three-edge, exactly-one-error example below. No large workload or comparison
to an unavailable omniscient joint-law controller is proposed as a fair gain.

[Amended result](hinge02.json): 17,792 subset evaluations, 724 profile requests
and 760 actual dependent-law score comparisons agree with the lower guarantee.
The 32 generated laws do not overstate the chosen product plan's actual score;
the explicit negatively dependent example does. With exactly one error among
three edges, all marginals have error 1/3. At edge price 2/5 and a single leaf
prize one, both planners buy nothing. The product profile assigns excess score
1/27, but its fixed positive prediction has actual excess score -1. The robust
planner chooses a fair guess with lower and actual excess score zero. Adding
the common half-score and dividing by total weight gives accuracies 14/27
(product forecast), zero (its actual accuracy), and 1/2 (robust). This diagnoses
the independence premise, not superiority over an informed conventional model.

The first probe used the wrong profile evaluator in its product-comparison
field and failed the example assertion. Its failed source/log/exit, separate
diagnostic, and [explicit same-input repair](hinge_amend.md) are retained.
Neither exact profile algorithm was changed by that repair.

## Learning what the guarantee actually needs

The guarantee uses only source-level upper bounds on each forecast error rate,
not a learned joint distribution or independence test. For a fixed finite edge
library and a frozen forecast policy, an ordinary simultaneous one-sided
confidence event can provide those bounds from checked errors on sampled tasks.
Marginal sampling identities and partial-proof censoring must remain valid;
a failed audit is not a correct prediction. A trivial error upper bound 1/2
is itself a premise and must not be assumed from absent evidence. If the
warranted upper bound exceeds 1/2, set the robust load d_e=2*p_upper, possibly
as large as two, or use an explicitly fair fallback; the recurrence still works
for any nonnegative d. The first implementation checks d<=1 only because its
finite source recipes impose that restriction, not because larger errors are
mathematically impossible.

If priors/forecasts are allowed to change after seeing the calibration labels,
fresh evaluation or a valid simultaneous/adaptive target construction is needed.
Source-level validation of a fixed predictor differs from validating an update
that selected the predictor using those same labels. A stable proposal model
can generate a small bank of policies first; direct policy-value audits may
then be cheaper and less conservative than calibrating every edge. Compare
those routes under the same paid observations before choosing one as a service.

## Simultaneous policy closure from a fixed marginal source

Fix a finite cohort of mathematical edge-label instances, or a declared task
distribution. Let theta_e be the source frequency/probability of positive edge
parity. Suppose one valid simultaneous event gives L_e<=theta_e<=U_e for
every edge in a fixed library. This event need not assume independent edges.
Choose the positive forecast with error upper bound 1-L_e, or the negative
forecast with error upper bound U_e. If neither is better than 1/2, use a fresh
independent fair coin for that edge on each deployment task; its error is
exactly 1/2 by design. Do not treat an unsupported fixed sign as fair.

Each preferred forecast and load d_e=2*min(1-L_e,U_e,1/2) may thus be chosen
after seeing the intervals. The choice of fair or fixed forecast is explicit;
fresh fair coins are independent across edges and the evaluation task. On the
common calibration event, every resulting fixed query set S satisfies the
union-bound score guarantee. Selecting S, stakes or nonnegative prices after
seeing that event's evidence does not require a union bound over all 2^m
sets: the marginal event deterministically implies every plan inequality.
This is simultaneous closure under checked algebra, not free data reuse for
an arbitrary newly trained context-dependent predictor.

The smallest error upper bound can decrease as retained lower/upper endpoints
tighten. The numerical guarantee profiles improve accordingly, but an old
specific forecast sign or coin choice still has its own immutable identity.
When changing signs, use the common theta intervals to re-derive the applicable
error bound; never relabel an old forecast's validation as if it tested the new
forecast. An arbitrary feature-dependent model would need its own target class
or prospective calibration, beyond these constant per-edge choices.

For a fixed finite cohort, all edge error rates are fixed mathematical counts.
Uniform sampling of task identities yields uncertainty about those counts;
it does not make each underlying proposition random. To upper-bound an error
rate using one-sided proof receipts, count checked correct predictions as
positive evidence. Unfinished audits remain unresolved. To construct theta
intervals, separate checked-positive and checked-negative receipt streams can
supply lower bounds for theta and 1-theta, with a simultaneous risk allocation.
Reuse the earlier fixed-source count machinery; do not throw away timeouts.

This yields a prospective integration: acquire a small number of reusable
marginal calibration certificates, compile a robust query-value profile, and
reprice/change stakes or fixed signs under the same event. Its expected benefit
must pay calibration and profile costs, and it can be weaker than directly
auditing a small frozen policy bank. The useful comparison is the strongest
equally informed conventional implementation, which can use this exact same
closure. No material advantage or readiness percentage is yet established.
