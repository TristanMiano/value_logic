# Separate development: retaining the old second-moment block

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; exploratory extension.
This is not part of N16-C/v1's readiness event. It generalizes the existing
[two-scalar route](../s14/two_scalar_upper.md), rather than rediscovering it
as new. Closest-prior and implementation assessment remain outstanding.

Retain, in addition to C=W^T S W, the matrix Q=W^T S^2 W, with
S=(I+MM^T)^(-1). Assume 0<C<I and C^2<=Q<C, in matrix order. Set

    T=C-Q>0, H=I-C, B=I-2C+Q=H^2+(Q-C^2)>0.

The normal-equation representation supplies W,R,X with W^T W=I,
W^T R=C, R^T R=Q, X^T X=T, MX=W-R and M^T R=X.
The completion construction shows that every stated C,Q is realizable.
The target is Wc for unit c and the edit norm is at most e>0, E=e^2.

## Sharp lower infimum

For any t>0 put a=1+t, d=t-E-E/t and

    A_t=a C-d Q=a T+(1+E+E/t)Q>0,
    ell(t)=c^T C A_t^(-1) Cc.

The proposed sharp lower endpoint is max_(t>0) ell(t). There is no cap
constraint on t because Q is retained rather than relaxed to C^2.

Validity follows from the first four squares of the lower SDP identity in
dual_certificates.md, taking alpha=A_t^(-1)Cc, w=R alpha and b=X alpha.
Their sum is exactly f-ell(t). Every term is nonnegative for t>0;
the compression term is unnecessary because Q is already known.

Both Q and T are positive definite, so ell tends to zero at t=0 and at
infinity. Its positive maximum occurs at a finite stationary t. At that t,
write m=alpha^T Q alpha and q=alpha^T T alpha. Differentiation gives

    q=E m/t^2.

Here is a direct sequence approaching the bound. Choose W=[I;0] and R
with W^T R=C and R^T R=Q, in n=k+rank(Q-C^2)<=2k outputs. Put

    M0=(W-R)T^(-1/2),
    Z an orthonormal basis for range(R)^perp,
    M_L=[M0, L Z], X_L=[T^(1/2);0], L>0.

Then M_L X_L=W-R and M_L^T R=X_L, so every M_L has exactly the same
retained C,Q. Define r=R alpha, x0=X_L alpha and

    Delta_L=e (r/||r||)(x0/||x0||)^T, N_L=M_L+Delta_L.

The edit has norm e. Direct calculation gives

    N_L^T r=a x0,
    (I+N_L N_L^T)r=a W alpha-d R alpha.

Consequently b=Wc-a W alpha+d R alpha is perpendicular to range(R),
because R^T b=Cc-A_t alpha=0. Also

    I+N_L N_L^T=K+L^2 Z Z^T

for a fixed positive definite K: the edit changes only the first k columns.
In the orthogonal splitting range(R) plus its complement, the Schur formula
shows (K+L^2 Z Z^T)^(-1)b tends to zero. Thus the actual edited residual
converges to r and F(N_L;Wc) converges to c^T C alpha=ell(t).
This proves the lower infimum without a minimax interchange or SDP closure
assumption. If no hidden coordinates are needed, b=0 and equality is finite.

The convergence has an explicit gap. Since v=(I+N_L N_L^T)r+b and
r^T b=0, the excess value is exactly

    F(N_L;v)-ell(t)=b^T(K+L^2 Z Z^T)^(-1)b.

For nonzero b this is positive and at most ||b||^2/L^2: the Schur
complement of K on range(R)^perp is positive definite. This also explains
the approach to the lower endpoint without assuming a numerical limit.

More generally finite attainment at a maximizing t requires b=0. Equality
in the nonnegative square identity forces the new residual and optimizer
to be r and a X alpha, after which their normal equation forces b=0.
Equivalently, d(R-WC)alpha=0, or d^2 alpha^T(Q-C^2)alpha=0.
If this condition holds, the same rank-one edit gives finite attainment;
if it fails at every maximizing t, the infimum is not attained. A known
upper bound on ||M|| changes this information class and can prevent the
approximating sequence. That is a separate, useful limitation.

## Sharp upper endpoint

For alpha in R^k, let

    J(alpha)=(sqrt(1-2 c^T H alpha+alpha^T B alpha)
                  +e sqrt(alpha^T T alpha))^2+alpha^T T alpha.

The proposed sharp upper endpoint is min_alpha J(alpha). The expression
inside the first square root is ||Wc-(W-R)alpha||^2. The objective is a
nonnegative squared sum of norms plus the positive definite quadratic
alpha^T T alpha, hence is strongly convex and has one minimizer.

Validity is ordinary primal reuse: choose the old coefficient X alpha and
bound the new residual by its old norm plus e||X alpha||. For sharpness,
use M0 above with input dimension k. Every input coefficient has the form
T^(1/2)alpha, so this is its complete robust least-squares action problem.

At a nonzero minimizing coefficient x with nonzero old residual r0, set
Delta=-e (r0/||r0||)(x/||x||)^T. The objective is differentiable there;
its zero gradient is exactly the new ridge normal equation for M0+Delta.
Thus the fixed edit attains the robust bound after reoptimization.

If x=0, optimality gives ||M0^T Wc||<=e. The edit
-Wc(M0^T Wc)^T cancels the target and attains one. If x is nonzero but
r0=0, its subgradient condition supplies y with ||y||<=1 and

    e||x|| M0^T y=(1+E)x.

Append one zero output row to M0,W,R and choose an additional component
of y so that ||y||=1. This preserves the displayed equation. Then
Delta=-e y(x/||x||)^T has norm e, the new residual is e||x||y, and
(M0+Delta)^T(e||x||y)=x. Its objective is (1+E)||x||^2=J(alpha).
So the upper endpoint is finitely attained with n<=2k+1,p=k, including
the zero-residual kink. This is the same mechanism as the s14 scalar
rotational example; it does not assume a general minimax identity.

Equivalently, use Young's scalar parameter eta>0, a=1+eta and
b0=1+E+E/eta. With D_eta=a B+b0 T>0,

    upper = inf_(eta>0) [a-a^2 c^T H D_eta^(-1)Hc],

including limiting eta=0 (cancellation) and infinity (a possible residual
kink). Minimizing over alpha and eta commutes because both are infima.
Unlike the N16 formulas, C and Q need not commute. This is a one-parameter
matrix-inverse expression, not a claim of a new robust-LS algorithm.

## Why retain this separate route

The extra block can be formed from old residual-vector inner products when
those vectors were actually computed; their acquisition/storage is paid.
It can improve decisions relative to C alone and distinguishes finite
attainment from merely limiting information ambiguity. Its lower sequence
also shows why adding an actual source-norm warrant could matter.
These are prospective mathematical consequences requiring their own close
comparison and focused checks. They neither increase N16's claimed scope
nor establish a complete-cost improvement or promotion readiness.

## One exact noncommuting screen

[second_check.py](second_check.py) and [second_result.json](second_result.json)
use C=diag(1/4,1/2), Q=[[1/8,1/64],[1/64,81/256]], E=t=1 and target
c=(5/2,1/32) normalized to unit length. Here C and Q do not commute,
C^2<Q<C, and the sharp lower infimum is 640/6401, approximately 0.0999844.
It certifies a strict lower threshold 49/500=0.098. C alone has its sharp
lower cap below 0.098, so cannot supply the same universal lower decision.

The four sequence members L=1,4,16,64 preserve both old blocks exactly and
give edited values approximately 0.1069403161, 0.1011089621, 0.1000625131 and
0.0999892953. The exact gap identity, positivity and 1/L^2 enclosure all
passed. Runtime was 6,728,900 ns. These are finite development checks of the
new sequence, not independent confirmation or evidence of economic advantage.
