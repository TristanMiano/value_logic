# Gate transfer: a restricted forecast-class decomposition

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.
Status: **post-outcome exploratory interpretation**, before computing the new
blockwise quantities. The final gate Brier failure and two advice signatures
are already known. This is not a prospective endpoint or a new paid experiment.
Initial research budget: eight engaged minutes, extend only for a concrete
remaining mathematical or data-binding issue. No actual learned path changes.

## 1. A restricted class, not a bound on all admitted reasoning

The frozen gate suffix has two binary advice signatures,
`s0=(0,1,1,1,0,0)` and `s1=(0,1,1,1,0,1)`. The actual six-expert weights are
fixed within each four-position block, nonnegative, and have fixed total mass.
Consequently the two pre-purchase base forecasts in a block are constant
within each signature and satisfy `0 <= p0 <= p1 <= 1`. The final downward
dyadic projection preserves this order. The suffix has unique full keys, so
there is no prior matching hard receipt that could change this base signature
structure. All these properties must be checked against the saved public trace.

Consider the larger, relaxed class that may choose arbitrary real forecasts
`(p0,p1)` separately in every block, subject only to that weak order. This
relaxes the deployed positive integer weights, the update dynamics and the
dyadic output constraint. It also gives the fitting procedure retrospective
access to all labels. Its optimum is therefore a **hindsight lower bound for
this restricted architecture**, not an attainable online forecast, not a
minimum over all logical reasoners, and not a new ordinary comparator.

The complete CNF remains public and an exact solver can distinguish claims
with the same advice. Thus a feature collision proves only that the displayed
advice map is insufficient for a perfect signature-only forecast on that
block. It does not say the mathematical claim lacks a definite truth or that
additional paid computation could not resolve it.

## 2. Exact within-signature variance

For each present block/signature group g, let n_g be its number of positions,
t_g its true labels, and mu_g=t_g/n_g. For any common group forecast p_g,

\[
\sum_{i\in g}(p_g-y_i)^2
=n_g\mu_g(1-\mu_g)+n_g(p_g-\mu_g)^2.
\]

The first term is the exact residual from opposite labels sharing that block
and advice signature. It is zero if the group is pure. Minimizing independently
over all group forecasts gives the sum of those residuals. This lower bound
is already retrospective and cannot be read as an observed conditional law.

## 3. The additional monotonicity constraint

If both signatures occur and `mu0 <= mu1`, their separate fitted means obey
the architecture's weak order. If `mu0 > mu1`, the constrained optimum pools
the means at `mu=(n0*mu0+n1*mu1)/(n0+n1)`. The additional minimum loss is

\[
M=\frac{n_0n_1}{n_0+n_1}(\mu_0-\mu_1)^2.
\]

To see this, the unconstrained strictly convex quadratic has its minimum at
the two empirical means. When they violate the order, the constrained optimum
lies on `p0=p1`; differentiating the one-dimensional quadratic gives the pooled
mean. Expanding around that mean gives M. If a signature is absent, its unused
forecast can satisfy the order without affecting loss, so M=0.

Write I for the summed within-group residual. For every recorded block the
decomposition is exactly

\[
\text{actual Brier sum}=I+M+E,
\qquad E=\text{actual Brier sum}-(I+M)\ge0.
\]

E is excess relative to the relaxed, label-informed, block-specific monotone
fit. It bundles any lack of future information, the actual update rule, weight
constraints and projection. It is **not** a causal effect of selection or an
estimate of avoidable online error. In particular, projection onto the order
cone can have a nonzero cross term, so E must not be replaced without proof by
only the squared distance from the pooled fit.

## 4. Saved-data audit and interpretation

The observer will reconstruct group counts from the two public gate tapes and
the independently checked saved truth transcript, then check all corresponding
42 numerical mixture/live/mirror suffix records. It will retain the 64-position
denominator, all 16 suffix blocks per population, both signatures and every
pure/mixed/absent group. It will verify actual forecast equality within group,
monotonicity, no prior hard receipt, and exact identity with each sealed suffix
Brier score. Seed means and then population means remain the frozen hierarchy.

The oracle terms I and M depend only on the frozen tape's block/signature labels,
so duplicate policy paths cannot increase the number of structural examples.
All 42 records remain visible, with the two population/32-block structure
reported separately. No new generator, truth evaluator, paid service, policy
ablation, empirical coverage estimate, author gate or P3-11 work is performed.
