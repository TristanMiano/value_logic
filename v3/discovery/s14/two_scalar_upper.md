# Sharp two-scalar upper transport: one convex scalar problem

Codex (GPT-6), DEVELOPMENT, October 22, 2026. Continues second_receipt.md.
This is a proposed general theorem with a reconstructable proof; no
independent confirmation or novelty verdict has occurred.

Retain s=g(M), m=||(I+MM^T)^(-1)v||^2, ||v||=1, and ||N-M||op<=e.
For 0<s<1 and s^2<=m<s, write q=sqrt(s-m), b2=1-2*s+m. Define

    J(alpha) = (sqrt(1-2*alpha*(1-s)+alpha^2*b2)
                +alpha*e*q)^2 + alpha^2*q^2, alpha>=0.

Then the dimension-unrestricted sharp upper envelope is

    U_e(s,m)=min_(alpha>=0) J(alpha).                       (1)

The minimum exists and is unique when q>0. The objective is strongly convex:
it is the square of the nonnegative convex function
||v-alpha*M*z||+alpha*e*||z||, plus alpha^2*q^2. The theorem is an
explicit one-variable convex characterization, not yet a closed radical
formula or a measured fast implementation. Cases e=0 or s=1 are immediate.

## Universal upper bound

Let w=(I+MM^T)^(-1)v and z=M^T*w. Then M*z=v-w, ||z||=q,
v^T*M*z=1-s and ||M*z||^2=b2. The primal identity gives, for any alpha>=0,

    g(N)<=||v-alpha*N*z||^2+alpha^2*||z||^2
          <= (||v-alpha*M*z||+alpha*e*q)^2+alpha^2*q^2.

The right side is exactly J(alpha). No new matrix entry is used in the
application once the two old scalar receipts and distance warrant are known.

## Attainment by a rank-one old matrix

Choose unit v and a vector w with v^T*w=s, ||w||^2=m; dimension two suffices.
Let the old matrix have one column M0=(v-w)/q. Then M0^T*w=q and
w+M0*(M0^T*w)=v. Thus its old response and squared-resolvent moment are
exactly the required s,m. Its whole primal variable is a scalar z, so
alpha*q ranges over all nonnegative candidate solutions.

Let alpha_star minimize J. First suppose alpha_star>0 and the unperturbed
residual r0=v-alpha_star*q*M0 is nonzero. Choose the column perturbation

    H=-e*r0/||r0||.

At z_star=alpha_star*q this realizes the worst residual norm
||v-(M0+H)*z_star||=||r0||+e*z_star. Differentiating the smooth robust
objective at its minimizer gives zero derivative for the fixed-H quadratic
||v-(M0+H)*z||^2+z^2 at z_star. That quadratic is strictly convex, so z_star
is its global minimizer. Hence this N0=M0+H attains (1).

If alpha_star=0, its right derivative gives e>=M0^T*v=(1-s)/q.
Choose H=-(M0^T*v)*v, whose norm is at most e. Then N0^T*v=0 and g(N0)=1,
the value J(0). If r0=0, v and M0 are parallel, forcing m=s^2. The explicit
zero-residual construction in the next section covers that case, after adding
one zero row if needed. Thus no unproved minimax exchange is required.

## An explicit rotational regime when the old moment is minimal

If m=s^2, put x=sqrt((1-s)/s). The old response vector is s*v; this does
NOT force every future perturbed matrix to remain scalar. For x>0,

    U_e(s,s^2)=1,                                e>=x;
               1/[1+(x-e)^2],                  e<x, e*(x-e)<=1;
               (1+e^2)/x^2,                    e<x, e*(x-e)>=1.

The formulas agree on the boundaries. To derive them, the scalar convex
objective is (|1-x*z|+e*|z|)^2+z^2. A minimizer has z>=0. On z<=1/x its
stationary point is (x-e)/[1+(x-e)^2]; it lies in that range exactly when
e*(x-e)<=1. Otherwise the optimum is the kink z=1/x. For z>=1/x the
objective is increasing from the kink. The e>=x case chooses z=0.

In the kink regime, take M0=x*v, choose a unit vector u with

    v^T*u=(e+1/e)/x,

and set N0=x*v-e*u. The regime condition makes this inner product at most
one, so dimension two supplies u. Direct substitution in
g(N0)=1-(v^T*N0)^2/(1+||N0||^2) gives (1+e^2)/x^2. The remaining branch
uses N0=(x-e)*v, and the cap uses N0=0 when affordable.

For s=1/10, m=1/100, e=1, x=3. A scalar change alone reaches response1/5,
but a permitted rotation reaches2/9. One explicit pair is

    v=(1,0), M0=(3,0),
    N0=(7/3,-sqrt(5)/3), ||N0-M0||=1.

Both old scalar receipts are exact. This rules out claiming that m=s^2
makes a scalar-only upper calculation sharp. When x<=2 the rotational
regime is empty; for x>2 it occupies a nonempty intermediate range of e.

## Contribution and application limits

The sharp lower endpoint in second_receipt.md and (1) jointly characterize
what two scalar receipts can guarantee under a norm-bounded edit. The
endpoints may use different extremizers; this is an interval contract,
not a claim that one matrix attains both endpoints simultaneously.

For interval receipts one can optimize over the compatible(s,m) region or
use conservative enclosures. Do not evaluate (1) at the interval midpoint.
The partial-moment acquisition and all outward arithmetic remain paid.
Robust least-squares objectives of the form ||residual||+e*||solution|| are
established, including El Ghaoui and Lebret. The possible specialized delta
is the exact reduction from two old scalars, its sharpness, and a useful
bounded-reasoning service; the closest-prior comparison is still open.

The small executed two_scalar_upper_probe.py passes 12 exact rational
rotational equality cases and 40 floating-point general attainment checks.
Maximum numerical discrepancy is 3.34e-16. The latter checks supplement the
proof; they are not exact interval certificates for the scalar minimizer.
