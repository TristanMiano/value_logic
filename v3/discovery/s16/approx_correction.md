# Task-specific approximate correction needs a validated error tube

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 24.

Suppose F=A-B lies in V plus a Euclidean ball of radius epsilon, uniformly
on a declared input domain. V=image(U), U^T U=I. A paid coordinate/general
measurement returns y=HF+n, ||n||<=delta. A task asks for t^T F.
For any w satisfying U^T H^T w=U^T t,

    |t^T F-w^T y| <= epsilon*||t-H^T w||+delta*||w||.     (1)

This follows by canceling the unrestricted V component. Selecting w is a
small convex program, but any checked feasible w supplies a certificate.
The infimum R of the right side is the optimal uniform worst-case radius
for this symmetric information contract (under the usual finite-dimensional
duality, or its limiting zero-radius version). The dual maximizes t^T f
subject to ||P_(Vperp) f||<=epsilon and ||Hf||<=delta. The two inputs
f,-f with noise -Hf,+Hf have common observation zero, proving the lower
bound R for every decoder. Thus the bound is not a claim that nonlinear
recovery could not be better on a particular nonzero observation fiber.
If no feasible w exists and epsilon,delta are finite, an unconstrained V
direction in ker(H) with nonzero target makes uniform error unbounded.

For coordinatewise noise |n_j|<=delta_j replace delta||w|| by
sum_j delta_j|w_j|. If t is orthogonal to V, no query is required for
the bound epsilon||t||. Recovering every coordinate may need many more
anchors. A directly available exact target query is a mandatory comparator;
the coordinate menu must be a real restriction, not an artificial handicap.
DEIM, optimal recovery and PBDW supply the underlying reconstruction ideas.

## Acquire a uniform tube by checking a proposed polynomial identity

Assume each coordinate of F(x) is a polynomial of total degree <=D on
[-1,1]^p, and paid exact evaluations are available. A fallible proposer
chooses a rational orthogonal projector P onto V and supplies rational
polynomials h_(j,k), defining SOS polynomials sigma_j=sum_k h_(j,k)^2.
It proposes the identity

    epsilon^2-||(I-P)F(x)||^2
        = sigma_0(x)+sum_(j=1)^p (1-x_j^2)*sigma_j(x).    (2)

Every polynomial and the degree warrant are frozen before private fresh
validation points. Let K bound the total degree of the difference between
both sides. Evaluate (2) at k independent uniform points in S^p, where
S is a rational grid of q>K distinct elements. A false identity passes
with probability <=(K/q)^k. A true identity proves the tube on the entire
cube by nonnegativity. Hence with that same failure probability, acceptance
warrants (1) for every future input, including adaptively chosen ones.

This is a one-sided randomized mathematical check, not certainty and not
an empirical population calibration statement. An actual projector check
P^T=P=P^2 and coefficient/degree checks are paid. Rational P need not be
represented by a rational orthonormal U; the constraint in (1) can instead
be written P(H^T w-t)=0. Encoding, bit growth, SOS construction and all k
full-vector truth evaluations are charged. The grid need not lie inside
the cube for polynomial identity testing, but the oracle must admit it.

An honest proposer might fail to find (2) even if the desired bound is
true. This particular SOS form is a sufficient certificate, not a complete
bounded-degree decision procedure. A stronger theorem about existence or
degree is not assumed. Reusing the same private points for adaptively
chosen proposals invalidates the simple bound; fresh tests with a summable
failure budget, or a separate adaptive-validation argument, are needed.

## Transport and contribution screen

If an explicit model edit gives F'=L F+G and a checked decomposition of
G into a new known span plus residual of norm <=epsilon_G, use a span
containing L V and the known G component. Its residual is <=||L||epsilon
+epsilon_G on the inherited common event. No fresh union bound is needed
for this deterministic consequence. New unrelated fitted models require
new evidence.

The potential advance over s15's exact range is tolerance for a uniformly
small nonzero residual, coupled to task-specific paid measurements. SOS,
polynomial identity testing, approximate interpolation and robust recovery
are established ingredients. Whether this explicit paid lifetime interface
is a useful moderately novel synthesis remains unassessed; source comparison
and a plausible certificate-producing workload come before a large harness.
