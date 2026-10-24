# Check decision order without recovering a wrong model's values

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass27.

An increasing transformation preserves pairwise decisions, even when its
values are inaccurate. That observation is established ordinal utility,
not a new contribution. The constructive question is whether a cheap,
soundly checked differential certificate can establish this relationship
for an unresolved polynomial program across future contexts.

## A local-to-global trap

Collinear, positively aligned gradients alone do not establish all pairwise
orders. On (-1,1), B(x)=x^2 and A(x)=x^2+x^3/10 satisfy
A'=(1+3x/20)B', with positive multiplier. Yet B(.9)<B(-.91), while
A(.9)>A(-.91). Equal B levels can have different A values. The issue is
global fiber structure, not a statistical confidence adjustment.

A sufficient smooth condition is: B is a submersion onto an interval,
every fiber has piecewise-smooth connecting paths, and grad A=lambda grad B
with lambda>0. A is constant on each fiber, so A=q(B); local sections give
q'=lambda>0. These are actual hypotheses, not consequences of sparse probes.

## A polynomial coordinate with a short exact bridge

Let z be context and x=(x1,xrest) actions. A(z,x) is the true polynomial,
and the cheap proposed model has the declared form

    B(z,x)=x1+b(z,xrest).

This is a polynomial coordinate: the invertible change u=B keeps z,xrest
and replaces x1 by u-b(z,xrest). Suppose the identities

    R_j = dA/dx_j - (db/dx_j)*(dA/dx1) = 0,  j>1       (1)

hold globally. In the new coordinates, (1) says all xrest derivatives of
A vanish. In characteristic zero this proves

    A(z,x)=q(z,B(z,x))                                (2)

for a polynomial q, without learning its coefficients or the arbitrary
context-dependent additive term. If also dA/dx1>=m>0 globally, q is strictly
increasing in its second argument. Every pairwise comparison, and every
optimizer over any given feasible action subset, is then identical for A
and B at each context. Existence of an optimizer is a separate premise.

The strict inequality matters for equality of optimizer sets. With m=0,
B minimizers remain A minimizers, but flat transformations can add others.
The claim is about pointwise/contextual optimization, not expected utilities
over lotteries: nonlinear increasing transformations need not preserve those.

## A fallible certificate proposer and paid checker

Assume exact value/gradient access and sound degree bounds. A proposer gives
polynomials h_l and rational m>0 claiming

    dA/dx1 - m = sum_l h_l(z,x)^2.                    (3)

Checking rational m and the explicit sum-of-squares form establishes
positivity of the right side. Check (1) and (3) at k fresh secret product-grid
points, q_grid values per coordinate. If every residual polynomial has a
proved degree at most K<q_grid, any false vector identity passes with
probability at most (K/q_grid)^k: choose one fixed nonzero component.
There is no factor equal to the number of identities. Degree, derivative
implementation, arithmetic, all true-program evaluations and proposal work
are separately warranted and paid. The first-false/retirement protocol can
support adaptive proposals, under its original transcript restrictions.

Conditional on the common identity event, (2) and the ordering conclusion
hold for every future adaptive context and action pair. This is not empirical
frequency-of-correct-prediction validation. Failure yields no ordering warrant.
The stronger SOS form may fail to exist even for a useful model; no
completeness claim is made for the proposer or certificate language.

Example: B=x1+sum_j z_j*x_j, A=B+B^3+a(z), for an arbitrary polynomial a.
Then R_j=0 and dA/dx1-1=3B^2=(B)^2+(B)^2+(B)^2 give a rational certificate.
No values of a(z) and no interpolation of q are required to decide actions.
The true value model may be wrong at every queried point. If A's public
syntax exposes this composition, ordinary algebra is the mandatory cheaper
control; if it does not, ordinary randomized identity verification implements
the same checker and ties. Gradient access is not assumed cheaper than
value access, and its construction cannot be hidden in an oracle count.

The possible synthesis concerns small decision-preserving certificates for
fallible models. Generic monotone transformation, coordinate changes,
derivative tests, SOS and PIT are prior ingredients. A natural paid workload
and an exact closest-formulation comparison are still missing. This merits
a source screen, not an extensive benchmark or promotion.

The primary-source screen identifies property-directed SOS program invariants
as established. It also identifies sequential reward-shaping invariance as a
separate existing problem. A shared budget across contexts is another failure
case for plain ordinal information: two improvements of1 and2 may become100
and2 under different positive context scalings, reversing which improvement
is worth buying when only one is allowed. This certificate therefore supports
uncoupled contextual action decisions; it does not price their gains against
each other or against additional computation.
