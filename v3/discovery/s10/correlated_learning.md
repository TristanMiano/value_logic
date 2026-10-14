# Learning a conservative common score law under within-request dependence

Codex (GPT-6), DEVELOPMENT, 2026-10-14. Proposed extension, not an executed
service. The current rl01 learner does NOT implement this sampling rule.

The first-observation-per-coordinate rule prevents duplicate billing bias but
does not prevent selection bias under dependence. For example, X=Y is a shared
Bernoulli(1/2) outcome. Query X always and query Y only when X=0. Every observed
Y is0, even though its marginal is balanced. Unique observations do not fix it.

A sufficient replacement rule chooses at most one representative per score type
from the **first physical purchase of a request**, before seeing any outcome of
that request. If that purchase is an optional singleton, only its type obtains
a sample. If it is an immediate full fallback, choose one representative of each
available type by a fixed index rule before receiving the bundle. Do not add
later adaptively selected observations to these calibration histograms. The
purchase and representatives may depend on past requests. Assume requests are
independent and stationary, and all coordinates of a given type share a marginal
law. Within-request dependence is unrestricted.

Each type's sampled sequence then has its stationary marginal law at predictable
sampling times. The earlier anytime one-sided confidence calculation applies
to these samples, counting at most one per type per request. Dependence between
different type histograms does not invalidate the union bound. It can reduce
how quickly useful information is obtained. Unseen required types have lower
tails zero and can force immediate fallback; this is conservative, not evidence
of learning failure. Selecting those types deliberately would need a priced
exploration rule.

For a fixed candidate order, each prefix can take the minimum only over types
actually present in that prefix. This can avoid an unused poorly sampled type
forcing its bound to zero. Each survival term then has its own valid common
lower law; summing the corresponding upper bounds remains conservative by
linearity. Choosing an order from past data is allowed, but changing the order
in response to current outcomes requires a new conditional analysis. Price the
search over orders explicitly.

Let L_{type,r} be valid lower bounds for Pr(score>=r), r=1,2. For all types
used by a candidate fixed prefix, choose L_r=min_type L_{type,r}. These define
one common three-score distribution G. Every actual marginal stochastically
dominates G. For each coordinate there exists a conditional randomization
producing Y_i<=X_i with marginal G; applying these kernels to the actual joint
vector preserves the coordinatewise inequality while allowing arbitrary
dependence among the Y_i. Consequently

```math
\Pr\!\left[\sum X_i<Q\right]
\le \sup_{Y_i\sim G}\Pr\!\left[\sum Y_i<Q\right].
```

The sharp three-score formula supplies the right side without assuming that
the actual marginals are equal or independent. At each valid past history the
prefix invoice using these bounds is conservative. Include immediate fallback;
its predicted physical fee is at most C. The history-conditional and
(1+delta)TC expectation interpretations in learning_interpretation.md still
apply, with fresh independence across requests and the new sampling rule.
The pathwise reserve remains separate and can protect against stationary-law
violations. No rate to the best policy is established.

This is an ordinary robust-probability and confidence-bound composition. The
next measurement should test whether its slower but unbiased samples and cheap
formula repay planning cost, against exact-threshold and empirical ordinary
controls. Do not promote it from this derivation alone.
