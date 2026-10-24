# Scalar optimization is conventional convex optimization

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; an assessment of the
algorithmic content of [the core proof](proof.md), not a separate novelty claim.

Write H=I-C, E=e^2>0, h=(E+sqrt(E^2+4E))/2, and ||c||=1.
The sharpness proof does not require a unique optimizing scalar. Nevertheless,
there are useful convex parameterizations for finding its rational witnesses.

## Upper endpoint

For eta in (0,h], set r=eta/(1+eta), so 0<r<=h/(1+h). The optimized
upper expression in proof equation (10) is

    G(r)=min_z { ||Hz-c||^2/(1-r)
                + E z^T C H z/r + z^T C H z }.        (P1)

Indeed, A-Q=||Hz-c||^2 and Q=z^T C H z in the earlier representation;
a=1/(1-r), while a+kappa=1+E/r. Each quadratic-over-positive-linear
term is a convex perspective. Their sum is jointly convex in (z,r),
so partial minimization over z makes G convex. At r=0 the closed
perspective forces z=0 because C H>0, and G(0)=1. Thus the scalar
minimization is convex on a compact interval, including this endpoint.

For clarity, the standard perspective inequality itself follows by
weighted Cauchy–Schwarz:

    ||theta u+(1-theta)v||^2/[theta s+(1-theta)t]
      <= theta ||u||^2/s+(1-theta)||v||^2/t

for s,t>0 and theta in [0,1]. Applying a fixed square root of C H
gives the same statement for its positive quadratic form.

## Lower endpoint

Put r=1/(1+eta), with 0<r<=1/(1+h), and K=C^(-1)-I>0. The lower
function becomes

    L(r)=c^T [I+K/r+E I/(1-r)]^(-1)c
        =max_w { 2c^T w-||w||^2
                  -w^T K w/r-E||w||^2/(1-r) }.       (P2)

The objective is jointly concave in (w,r), by the same perspective fact.
Partial maximization makes L concave. At r=0, its closed extension has
w=0 and L(0)=0. This agrees with the strict-domain eta=infinity limit.
Thus maximizing L is another ordinary scalar convex optimization problem.

## Implication for the claim

These reformulations support stable one-dimensional search and identify
which endpoint derivative needs checking. They do not create a new generic
optimization method. The rational checker only needs feasible rational t
values, so approximate scalar optimization can propose them without becoming
part of its soundness assumptions. A strict threshold margin can be certified
without certifying the exact optimizer. Any claimed time advantage still
needs the true acquisition, retention, arithmetic and warrant costs.

The common scalar parameter is crucial. Replacing P1 or P2 by a separate
optimizer for each eigenvalue exchanges an optimization and a sum and can
give an invalid bound. The convexity here concerns the whole target function.
