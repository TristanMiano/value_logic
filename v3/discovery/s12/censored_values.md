# Unfinished verification can produce a score, not a free truth label

Codex (GPT-6), s12 DEVELOPMENT. Early screen of a Q1/Q3/Q4 connection.
This is a specialization of established inverse-probability weighting and
randomized debiasing, not a new generic learner.

## Terminal-only correction

Fix one deterministic mathematical instance with exact Boolean answer y and
a verifier that returns it after T finite work steps. A fallible predictor
supplies p before execution. Independently draw a cutoff C with survival
q_t=Pr(C>=t)>0. Execute only min(T,C) steps and return

```math
Z=p+\frac{\mathbf 1\{T\le C\}}{q_T}(y-p).
```

The correction is computed only on completion, when T and y are observed.
Conditional on the fixed instance, E[Z]=y and
Var(Z)=(y-p)^2(1/q_T-1). Expected purchased work is sum_(t<=T)q_t.
Thus a long-running instance whose prediction happens to be correct need not
contribute additional variance, but this is not known from its timeout.

For a fixed residual |y-p|>=r>0, bounded expected work uniformly over arbitrary
T requires summable q_t and hence q_T->0. Its variance is then unbounded.
Conversely a uniform finite variance bound requires q_T bounded below and
therefore expected work growing with T. There is no distribution-free uniform
cost/variance bargain for arbitrary unresolved computations in this interface.

## Progressive fallible predictions

For a finite trace, allow predictions p_0,...,p_T=y after successive paid
prefixes. Before paying step t, continue with probability r_t>0 chosen from
the already observed prefix. For a fixed full computational trace let
Q_t=product_(s<=t)r_s and Q_0=1. The roulette coins affect continuation only;
condition on any other algorithm randomness. With I_t indicating survival,

```math
Z=p_0+\sum_{t=1}^T I_t(p_t-p_{t-1})/Q_t,\qquad E[Z]=y.
```

The exact conditional variance is

```math
\mathrm{Var}(Z)
=\sum_{t=1}^T (y-p_{t-1})^2(1/Q_t-1/Q_{t-1}).
```

To derive it, for s<=t use E[I_s I_t]=Q_t, so the normalized indicators have
covariance 1/Q_s-1. Expanding the variance and telescoping the squared
remaining residuals gives the displayed expression. Prefix-dependent
continuation probabilities are fixed along the conditioned full trace. This
does not permit a decision to continue based on the unseen next answer.

A good intermediate model can reduce the variance paid for later truncation.
Bad predictions do not create bias on a finite terminating trace, but may make
the estimator costly or unstable. Across instances, unconditional variance
also includes variation in y. Acquisition and evaluation of the predictors
are additional work. Infinite traces need convergence and integrability
conditions; finite-trace algebra cannot be extended to arbitrary nonhalting
mathematical questions without them.

## Why the returned number is not a per-instance probability forecast

The estimator can lie outside [0,1]. This is necessary in general: if a random
variable Z lies in [0,1] and is unbiased for a fixed y in {0,1}, then Z=y almost
surely. An unresolved shared computation prefix cannot return the correct
endpoint almost surely in two still-compatible instances with opposite y.
Clipping the roulette score to [0,1] generally introduces bias. It may support
population-value estimation under a valid sampling/variance contract; it is
not a checked truth value for the individual unfinished instance.

## Literature and disposition

Rhee and Glynn's [2015 paper](https://web.stanford.edu/~glynn/papers/2015/RheeG15.pdf),
Section 2/Theorem 1 and Section 3/Proposition 1/Theorem 3, already develops
unbiased random truncation, variance expressions and work/variance allocation,
and credits McLeish's earlier debiasing construction. Its infinite-level
conditions are not automatically satisfied by a fallible mathematical model.

Learning from timeout intervals is also established: Bengs and Hullermeier's
[resource-censored bandits](https://link.springer.com/article/10.1007/s10994-022-06271-z),
Sections 2.3–2.4 and 3.2, jointly choose an arm and a resource limit and reuse
censored feedback across smaller limits. A generic cutoff learner or survival
model would repeat this direction.

**Disposition:** park the generic mechanism without a new experiment. Retain
the explicit distinction between a useful unbiased value score, a valid
probability forecast and a proof. A later application would need actual
prefix predictors, justified tails or finite horizons, complete bills and
comparison with ordinary debiasing/control-variate methods.
