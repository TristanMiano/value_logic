# S23: learning cutoff values from censored runs

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.
Parent branches: S12/S16/S22. This initially preserves the derivation begun
before the interrupted source comparison; its writing earns no duplicate time.

Fix a task, program, seed stream and execution state. Let T be the first
attempt producing a checked receipt. With receipt value V and attempt price c,
the cap-n payoff is `g_n=V 1[T<=n]-c min(T,n)`. Its increments are
`D_i=1[T>=i] * (V 1[T=i]-c)`. Different programs or state/cache trajectories do not
automatically share this same-prefix counterfactual.

Before unseen execution choose an independent random cap C, conditional on
visible context X and prior tasks, with q_i=P(C>=i|X)>0. A forecast b_i(X)
fixed before C yields the nested-censoring estimator

```
Z_n = sum_(i<=n) b_i + sum_(i<=n) 1[C>=i] (D_i-b_i)/q_i.
```

Conditional on the complete trajectory, E_C Z_n=g_n. This does not require a
correct runtime-hazard model. Forecast error affects efficiency, not this
identity. If success is observed before C, subsequent increments are known
zero without executing them; the displayed estimator remains computable.

Set R_i=D_i-b_i, q_0=1 and lambda_i=1/q_i-1/q_(i-1)>=0. For i<=j the nested
indicator covariance is 1/q_i-1. Telescoping the covariance matrix gives

```
Var_C(Z_n | trajectory) = sum_(i<=n) lambda_i (sum_(k=i..n) R_k)^2.
```

Tail residuals, not isolated increment errors, determine truncation variance.
With A_i=E[(sum_(k=i..n)R_k)^2|X] and w_i=c P(T>=i|X), expected execution
cost is sum_i w_i q_i. Set z_i=1+sum_(j<=i)lambda_j. Minimizing cost under an
added-censoring-variance budget B becomes the convex program

```
min sum_i w_i/z_i  subject to lambda>=0, sum_i A_i lambda_i<=B.
```

Forecast/setup costs are additional. A probability floor can bound z_i. KKT
for a positive lambda_l equates sum_(i>=l) w_i/z_i^2 to nu A_l. Rewriting in
q-coordinates gives differences A_i-A_(i+1) which need not be nonnegative;
an uncoupled Neyman-allocation shortcut is not justified.

Partial deterministic receipts are also useful: early success T<=C determines
every g_n. With no success by C, g_n=-cn for n<=C; for n>C it lies in
[-cn, max(-cn,V-c(C+1))]. Interval decision regret avoids hazard inversion.

Primary comparison: Rhee and Glynn (2015),
[Unbiased Estimation with Square Root Convergence for SDE Models](https://web.stanford.edu/~glynn/papers/2015/RheeG15.pdf),
section 2 coupled-sum construction, Theorem 1 statement and expected work
equation (8), were read during an entirely excluded interrupted interval.
Random truncation and its unbiasedness are imported principles; no novelty
claim for those principles or for ordinary convex allocation is made.
Subsequently read section 3 equation (16), Proposition 1 and its proof, and the
following discussion of collapsing negative-coefficient levels. The source
already treats monotone truncation probabilities, work-variance optimization
and negative coefficient repairs. The finite lambda-coordinate formulation
above is a convenient specialization, not an established novelty. McLeish (2011) was opened
but its body was not retrieved/read; do not treat that as a completed comparison.

Next: derive simple finite-path checks including poor forecasts and matched
execution costs, then connect bounded estimators to an ordinary simultaneous
policy-bank confidence event. Learning from a declared task distribution will
not warrant success probabilities for every individual mathematical instance.

## Tail calibration and decision contrasts

For fixed X and q, let m_i=E[D_i|X]. The oracle forecast b=m minimizes every
tail residual second moment simultaneously. Specifically, A_i(b) equals the
conditional variance of sum_(k=i..n)D_k plus (sum_(k=i..n)(m_k-b_k))^2.
Thus excess censoring variance from a fallible forecast is exactly the sum of
these squared tail biases weighted by lambda_i. Accuracy on individual
increments is not the relevant weighted loss. An oracle forecast's production
cost is not free; learned forecasts must be fitted before the current cap draw
and unseen trajectory. Poor forecasts remain unbiased and can be much worse.

For a proposed cap a versus cap b, use the increment coefficients
d_i=1[i<=a]-1[i<=b]. The same estimator and variance identity apply to d_i D_i,
with correspondingly transformed forecasts. Shared prefixes cancel exactly.
No separate recovery of both absolute values is required. In the bounded cap
menu this is ordinary paired estimation; its prospective usefulness is a paid
controller that spends on relevant continuation, not a new probability rule.

Across independently drawn tasks from a declared source, q and b may adapt to
past logs and current visible X. Conditional design unbiasedness still holds,
so the centered estimates form martingale differences about the source's
policy value (or its context-conditional target). A positive probability floor
and bounded stakes/costs give bounded increments for ordinary simultaneous
confidence methods. This does not make a per-task lower hazard guarantee:
statistical source validity and instance-specific logical receipts stay distinct.

Prospective cheap screen: 24 generated finite runtime laws on T=1..H+1,
H=6, seed 61357; T=H+1 represents no success within the horizon. Independently
enumerate all cap outcomes for three forecast choices (zero, oracle increments,
and sign-reversed oracle). Check unbiasedness, conditional/total variance,
tail calibration and every cap contrast with exact rational arithmetic. Include
nonmonotone tail second moments and compare matched-expected-work endpoint-only
audits. Report all efficiency losses as well as gains. This is an algebraic
developmental screen, not confidence calibration or real solver evidence.

[Amended finite result](censor02.json): 25,873 conditional unbiasedness/variance
checks, 3,528 cap contrasts and 72 tail-calibration checks agree exactly.
Forty-two adjacent tail-second-moment pairs increase, so monotonicity is not
automatic. Arbitrary nested caps have lower variance than matched-work
endpoint-only audits in only 7 of 72 comparisons; they lose 65. By forecast:
zero wins 1/24, oracle wins 0/24, reversed wins 6/24. Do not mistake structural
unbiasedness for economic usefulness. The first output was malformed because
of a deterministic JSON replacer bug; [amendment](censor_amend.md) preserves
its source/output and records the same-input repaired run.

## A cheap allocation diagnostic before further implementation

For one target and a fixed forecast, minimize cost plus nu times added
censoring variance. In lambda coordinates its derivative at coordinate l is
`nu*A_l - sum_(i>=l) w_i/z_i^2`. At an endpoint-only design q_i=r, lambda_1
is the only positive coordinate. An interior optimum for that coordinate has
nu*A_1=r^2*W_1, where W_l=sum_(i>=l)w_i. Convexity then proves this design
globally optimal whenever A_l/W_l>=A_1/W_1 for every positive W_l (zero-work
tails are handled separately). This is a sufficient/necessary KKT diagnostic
at that interior endpoint design, not a universal property of receipt times.
The arbitrary-cap losses above motivate checking this before building a
complicated optimizer. An endpoint-only design may simply be the best design.

If A_l=0 and W_l>0, randomization can suppress that tail without added variance
for the stated target/forecast, in the limiting design q->0. Exact zero must
be warranted, not inferred from a small pilot. Finite probability floors keep
unseen discrepancies observable. For several cap contrasts, each gets its own
linear variance budget in lambda, preserving convexity and making the
decision menu explicit. This is ordinary optimal experimental design over
coupled truncation indicators; a large menu and model estimation can erase
its kernel benefit.

The [post-exposure diagnostic](censor_diag01.json) finds the endpoint-only
design satisfies the exact KKT inequalities in 8/24 zero-forecast, 10/24 oracle
and 6/24 reversed-forecast cases. The remaining 48 cases have an improving
cut direction; this does not contradict losing arbitrary nested designs.

## Two-level constructive repair

Suppose `A_l/W_l < A_1/W_1`, and define Wp=W_1-W_l and Wt=W_l. With two
survival probabilities x before l and y thereafter, expected work is Wp*x+Wt*y
and added variance is `(A_1-A_l)/x + A_l/y - A_1`. Both coefficients are
positive in a strict improving case with Wp,Wt>0. Under work budget K, ordinary
two-stratum square-root allocation gives

```
s = sqrt((A_1-A_l)*Wp) + sqrt(A_l*Wt)
x = K * sqrt((A_1-A_l)/Wp) / s
y = K * sqrt(A_l/Wt) / s.
```

The diagnostic implies x>y. If x>1, set x=1 and y=(K-Wp)/Wt; otherwise the
displayed probabilities apply. Endpoints and zero coefficients are separate
limits. This uses a distribution on caps {0,l-1,H}, with early stopping on
receipt. It is a targeted repair of the arbitrary-design loss, not a new
allocation principle. Search l over a short decision horizon and include the
unchanged endpoint design as a fallback. A paid pilot must estimate these
moments; the supplied-law advantage cannot be claimed as net practical gain.

Prospective development on the already exposed 24 laws: propose each valid
two-level design with floating-point square roots, round x downward to a
2^-16 grid, and choose the largest grid y allowed by the exact rational work
budget and y<=x. Reject zero y. Evaluate work and variance exactly, retaining
the original endpoint design if no proposal improves it. Save every selected
design and its expected-work/variance comparison. This is constructive
post-exposure repair, not fresh confirmation.

[Repair result](censor_repair01.json): 154 feasible grid proposals yield exact
selected-policy mean/variance matches on all 72 comparisons. The fallback
never worsens the endpoint variance at its work budget. It improves 16/24
zero, 14/24 oracle and 18/24 reversed cases. Mean total-variance ratios are
0.9821, 0.9938 and 0.9375, respectively; best ratios are 0.9148, 0.9478 and
0.8256. The oracle's mean improvement is only about 0.6%, before model/setup
cost. These modest supplied-law gains do not justify a large optimizer or a
positive readiness claim. Retain the estimator and allocation diagnostic as
components; prioritize a workload where retained evidence changes a real
solver/controller decision.
