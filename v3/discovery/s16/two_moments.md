# Two retained moments: a sharp lower bound and a sharp upper problem

Codex (GPT-6), October 23, 2026. DEVELOPMENT; same-model derivation.
**Lineage correction:** inspection during s16 found that
[s14's lower theorem](../s14/second_receipt.md) and
[sharp upper theorem](../s14/two_scalar_upper.md) already establish this
two-moment envelope. The present derivation is a same-model reconstruction,
with an alternative angle parameterization and lower witness, not a new
sharp-envelope result. No independent reconstruction or novelty verdict has
occurred. The useful new work here is the application to cross-target
receipt acquisition and its explicit threshold checker.

Let S=(I+MM^T)^(-1), ||v||=1, s=v^T S v and m=v^T S^2 v. Assume
0<s<1 and s^2<=m<s. Set q=s-m>0. Retain s,m and a sound edit bound
||N-M||op<=e. Matrix dimensions and all other information are unrestricted.
The degenerate s=m=1 case is addressed below.

## Sharp lower envelope

The old response w=S v and old primal z=M^T w satisfy

    <v,w>=s, ||w||^2=m, ||z||^2=q, Mz=v-w.

The old dual direction and the edit bound give

    F(N;v)>=L2(s,m,e):=s^2/[m+(sqrt(q)+e*sqrt(m))^2].   (1)

This lower bound is sharp as an infimum at every admissible s,m. To see
this, choose v=(1,0), w=(s,sqrt(m-s^2)), d=v-w, and a unit vector u
orthogonal to w. For every T>0 define the two-column matrix

    M_T=[d/sqrt(q), T*u],
    N_T=M_T+[e*w/sqrt(m), 0].

Because <d,w>=q and <u,w>=0, (I+M_T M_T^T)w=v exactly. Thus the source
receipts s,m are exact for every T; ||N_T-M_T||op=e. In the orthonormal
basis (w/sqrt(m),u), the second diagonal of I+N_T N_T^T tends to infinity,
while its first diagonal is 1+(sqrt(q/m)+e)^2 and its off-diagonal is fixed.
The inverse therefore converges to the rank-one matrix supported on w,
giving F(N_T;v)->(1). This is a limit witness, not a finite-attainment claim.

## Sharp upper envelope as one scalar maximization

Write a=1-s, b=sqrt(m-s^2), r=e*sqrt(q). Restrict the new primal solve
to multiples t*z. With h=(N-M)z, ||h||<=r, the restricted exact minimum is

    min_t ||v-t(d+h)||^2+t^2*q
      =1-<v,d+h>^2/(||d+h||^2+q).                      (2)

For a fixed component of h along v, the worst perpendicular component
increases the norm of d's perpendicular component. If r<a, an optimum has
negative parallel component and positive aligned perpendicular component,
both on the boundary of the ball. Therefore the universal upper envelope is

    U2(s,m,e)=max_{0<=theta<=pi/2}
      [q+(b+r*sin(theta))^2] /
      [(a-r*cos(theta))^2+q+(b+r*sin(theta))^2].         (3)

If r>=a, U2=1: cancel the parallel component. When e=0, (3) equals s.
The quarter-circle reduction follows by reflecting any positive parallel
edit to its negative counterpart, aligning the perpendicular edit with the
old perpendicular vector, and exhausting unused radius in those favorable
directions. The denominator's positive q prevents singular ratios.

Equation (3) is SHARP, not just the result of restricting a particular
source solve. Choose the one-column source M=d/sqrt(q), with v,w,d as above.
It has exactly the required old response w. For any maximizing h in (2),
set N=(d+h)/sqrt(q). The edit norm is at most e, and its full primal space
is exactly the line used in (2). This attains the universal upper value in
two target dimensions and one action dimension. The one-dimensional compact
optimization can be enclosed outward; an ordinary optimizer's floating
maximum is not by itself an upper certificate.

At s=m=1, the sharp bounds are 1/(1+e^2) and1, attained by M=0 with N=e*v
and N=0 respectively. For 0<s<1, m=s is not attained by a finite M, because
S is positive definite and S-S^2 is zero only in its eigenvalue-one space.
Boundary limits must not be described as finite receipts.

## A cheap usable bound without solving the sharp upper problem

For any fixed t>=0, triangle inequality in the restricted primal gives

    F(N;v)<=B_t(s,m,e)
      :=[sqrt(1-2*(1-s)*t+(1-2*s+m)*t^2)
           +e*t*sqrt(s-m)]^2 + t^2*(s-m).              (4)

The old fixed-primal bound is t=1. Allowing a different scale costs only a
scalar calculation. We do not need to assert any interchange of min and
max in order to use (4). For a lower moment receipt m>=l, maximize (4) over
the permitted interval before choosing t, or give a separate monotonicity
certificate. Substitution of l without that justification is not sound.

For s=1/2, l=41/100, e=1/10, take t=31/32. Put q=s-m in [0,9/100] and
C_t=1-t+t^2/2. Expanding (4) yields

    B_t=C_t + 2*t*e*sqrt(q*(C_t-t^2*q)) + t^2*e^2*q.

Here q<=9/100<C_t/(2*t^2), so both additional terms increase with q.
The worst case is m=l. At that endpoint,

    B_t=1025/2048 + 93*sqrt(42601)/512000
                     + 8649/10240000 < 539/1000,       (5)

using sqrt(42601)<206401/1000. Thus the three old scalar target values in
[projected receipts](projected_receipts.md) certify F(N;v)<.539, improving
that note's initial fixed-primal certificate (<.5395, enough for .54).
The one-old-value contract still permits100/181>.552. This is a stronger
counterfactual decision from the same paid cross-target information, without
requiring the exact m or an additional operator solve.

The improvement is in a certified value threshold, not measured audit fees
or CPU. An ordinary implementation with the same receipts ties. The lower
formula (1), the sharp upper envelope and matching extremizers were already
established in s14. Alternative formulas do not raise their novelty or
readiness by being rederived. The closest-prior comparison remains open
at that inherited scope.

The [exact probe](moments_probe.py) passed108 lower-witness evaluations
across27 families and108 upper-witness evaluations, with9 source receipt
pairs. It also checked the strict threshold using the rational upper
275877743/512000000<.539. A finite feasible edit has value66181/122825,
above.5388, illustrating that this example is close to the bound. The
[output](moments_probe.json) binds the source and records5,372,100ns of
execution. These finite checks supplement the derivation; they do not
establish general sharpness independently or measure economic superiority.
