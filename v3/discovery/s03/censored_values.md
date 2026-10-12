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
The optimization section has not yet been audited. McLeish (2011) was opened
but its body was not retrieved/read; do not treat that as a completed comparison.

Next: derive simple finite-path checks including poor forecasts and matched
execution costs, then connect bounded estimators to an ordinary simultaneous
policy-bank confidence event. Learning from a declared task distribution will
not warrant success probabilities for every individual mathematical instance.
