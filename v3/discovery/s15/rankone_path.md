# A declared rank-one edit path has a small exact response profile

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 31.
This is a Woodbury/rational-interpolation adapter, not a new matrix identity.

For a real matrix M and unit vector v, let

    f(t)=min_x (||v-(M+t*u*z^T)x||_2^2+||x||_2^2).

The counterfactual explicitly changes M along the SAME paid rank-one
direction for all real t. Let Q=I+M*M^T, w=M*z, gamma=z^T*z and retain

    s=v^T*Q^-1*v,
    a=u^T*Q^-1*u, b=u^T*Q^-1*w, c=w^T*Q^-1*w,
    d=u^T*Q^-1*v, e=w^T*Q^-1*v.

The resolvent identity gives, for every real t,

    D(t)=1+2*b*t+(b*b+a*(gamma-c))*t*t,
    R(t)=2*d*e*t+((gamma-c)*d*d+2*b*d*e-a*e*e)*t*t,
    f(t)=s-R(t)/D(t).                                      (1)

Indeed Q_t=Q+[u,w]*[[gamma*t*t,t],[t,0]]*[u,w]^T; apply the
two-dimensional Woodbury formula and simplify. When u,z are nonzero,
a>0 and gamma-c=z^T*(I+M^T*M)^-1*z>0, so
D(t)=(1+b*t)^2+a*(gamma-c)*t*t>0. Zero u or z gives the constant path.
Formula (1) extends continuously to t=0 without inverting the singular
two-dimensional update at that point.

## Information and acquisition

Once s is known, two applications of Q^-1, to u and w, plus one M*z
product and the listed inner products acquire the remaining profile. All
future path values use a quadratic numerator and denominator. This says
which information is sufficient; inverse solves, vector storage, dot
products and arithmetic precision are charged. Ordinary Woodbury updates
are exactly the strong comparator and achieve the same reduction.

Alternatively, five exact values at distinct t determine the complete
degree-(2,2) rational function. The cross product of two candidate
numerators/denominators has degree at most four, so five distinct roots
force equality wherever the denominators are nonzero. With f(0)=s already
known, four more exact path values give linear equations for the four
remaining normalized rational coefficients. A degenerate linear system
may represent a lower-degree function; it does not invalidate uniqueness
of the rational function. Removable poles must be cancelled or avoided
with a valid positive-denominator representation.

No analogous guarantee follows from five approximate samples without an
additional conditioning/interval analysis. Nor do five values identify
the response to unrelated edit directions. Unknown matrices consistent
with old values may still have different optimizers and other responses.
The profile certifies optimal values after reoptimization, not a common
precommitted optimizer at all t.

Screen outcome: retain a useful implementation route for explicit low-rank
counterfactual services, but reject generic novelty of the curve compression.
This differs from the norm-only scalar envelopes because it purchases
direction-specific information. Neither information contract dominates
the other for free.
## Exact finite screen and the approximate-data obstruction

The [rational probe](path_probe.py) passes315 direct/profile equalities on
45 matrices of dimensions1–3, plus225 checks of the rational function
reconstructed from five values. Nine interpolation systems have rank2 rather
than4; the function remains determined even though its coefficient description
is not unique. The other36 have rank4. No sampled test denominator was zero;
removable poles must still be handled in a general implementation. Runtime
34,602,200 ns, Python3.12.14, and source hash are in [result](path_probe.json).

Exact interpolation cannot be transferred to approximate receipts without
conditioning information. Given any five distinct sampled t_i and an
unsampled t_0, the scalar family

    M(t)=K(t-t_0),     f(t)=1/[1+K^2(t-t_0)^2]

has f(t_i) tending to zero at all five samples as K grows, while f(t_0)=1.
Any fixed positive observation tolerance can therefore hide a unit-height
peak. These are valid rank-one paths. They do not contradict exact rational
identification; the small nonzero values encode the peak with increasing
ill-conditioning. A warranted direction norm changes the problem.

For a general differentiable real matrix path A(t), fixed unit v, and
f(t)=v^T(I+A A^T)^(-1)v, let y=(I+A A^T)^(-1)v,
alpha=||y|| and beta=||A^T y||. Then

    f=alpha^2+beta^2<=alpha,
    |f'|=2|y^T A' A^T y|<=2||A'|| alpha beta
         <=(3 sqrt(3)/8)||A'||.                            (2)

For the last step, beta^2<=alpha-alpha^2; maximizing
2 alpha sqrt(alpha-alpha^2) over alpha in[0,1] gives alpha=3/4.
The constant is sharp already for scalar A=1/sqrt(3) and unit derivative.
Thus a paid bound ||A'||<=K gives a global Lipschitz constant3 sqrt(3)K/8.
Also2 alpha beta<=f yields |(log f)'|<=||A'||. Integrating this latter bound
is valid, although the anchored finite-edit envelope is generally sharper.

Sound sample intervals plus (2) can certify a whole parameter interval by
intersecting their Lipschitz cones. Better still, apply the earlier sharp
one-receipt envelope using the warranted distance between each sample's
operator and the proposed operator, then intersect the resulting bounds.
This supplies a safe approximate-receipt route without pretending that a
floating rational fit is a certificate. Sampling, interval optimization and
direction-bound acquisition remain paid. Lipschitz global optimization and
matrix perturbation are conventional comparators; this adapter has no
generic novelty claim.
