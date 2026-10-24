# Precision costs of retaining a response block

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT. This is a consequence
and limitation of the proposed N16 endpoints, separate from the core
contribution event. It gives a uniform precision guarantee, not a runtime
advantage or a new generic approximation principle.

Fix E=e^2>0 and a unit c. Write h=(E+sqrt(E^2+4E))/2, a=1+t,
d=t-E-E/t, and let l(C),u(C) denote the optimized lower and upper formulas
in [the claim](claim.md). Their finite-parameter versions l_T,u_T optimize
over h<=t<=T. All statements below extend the *formulas* continuously to
0<=C<=I. They do not assert the same finite-source realization at singular
boundary blocks.

## Uniform truncation bounds

For a scalar eigenvalue lambda in [0,1], differentiation gives

    d/dt L_t(lambda)
      = lambda*[E*lambda/t^2-(1-lambda)]/[a-d*lambda]^2,

    d/dt U_t(lambda)
      = lambda*[1-b_t*lambda]/[1+d*lambda]^2,
    b_t=1+E*(1+1/t)^2.

Since a-d*lambda>=a-d=1+E+E/t, the positive part of the first
derivative is at most E/[(1+E)*t+E]^2. Since
lambda/(1+d*lambda)<=1/(1+d), the negative part of the second derivative
is at most (b_t-1)/(1+d)^2=E/(t-E)^2. Here t>=h>E, so the
denominators are positive. Integrating these bounds from T to infinity
and averaging over the spectral weights of c proves

    0 <= l(C)-l_T(C) <= E/[(1+E)*((1+E)*T+E)],
    0 <= u_T(C)-u(C) <= E/(T-E).                  (P1)

For example, any parameter beyond T can improve the upper value by no
more than the second expression. This is a bound on optimization of the
retained-information envelope, not on iterations of a full source solve.

## A uniform modulus, and why a linear one fails

The resolvent identity, also for noncommuting C,D, gives

    L_t(C)-L_t(D)
      = a*(aI-dC)^(-1)*(C-D)*(aI-dD)^(-1),
    U_t(C)-U_t(D)
      = a*(I+dC)^(-1)*(C-D)*(I+dD)^(-1).

Thus both scalar finite-t maps are Lipschitz in operator norm with a
constant at most 1+t. Optimization over the same bounded interval retains
the constant 1+T. Since both truncation errors in P1 have a fixed sign,
comparing two optimized values costs only one tail allowance, not two.
For delta=||C-D||op in (0,1], choose T=E+sqrt(E/delta). It satisfies
T>=h, because h-E=E/h and h^2/E=1+h>1. Consequently

    |u(C)-u(D)| <= (1+E)*delta + 2*sqrt(E*delta),
    |l(C)-l(D)| <= (1+E)*delta
                   +[1+(1+E)^(-2)]*sqrt(E*delta).       (P2)

The trivial range bound one can be intersected with these estimates.
Constants are deliberately conservative. The square-root order cannot be
replaced by a uniform linear order across all strictly interior blocks.

For an explicit obstruction take E=1, c=(1,1)/sqrt(2), and first consider
the boundary formulas A_epsilon=diag(epsilon,1), B=diag(0,1). Then u(B)=1/2.
For any t>=h,

    c^T U_t(A_epsilon)c
      >= 1/2 + (1/2)*[t*epsilon/(1+t*epsilon)+1/t].

If t<=1/sqrt(epsilon), the last term is at least sqrt(epsilon)/2.
Otherwise the first term is at least
sqrt(epsilon)/[2*(1+sqrt(epsilon))]. For epsilon<=1 this proves

    u(A_epsilon)-u(B) >= sqrt(epsilon)/4.               (P3)

To stay strictly inside the core domain, replace A_epsilon,B by
diag(epsilon,1-epsilon^4), diag(epsilon^4,1-epsilon^4).
Each replacement changes u by at most 2*epsilon^4+2*epsilon^2 by P2.
For 0<epsilon<=1/64 the resulting gap is at least sqrt(epsilon)/8,
while the matrix distance is epsilon-epsilon^4. Their ratio is unbounded
as epsilon tends to zero. No source-independent linear precision constant
is available over the whole core domain. This does not contradict local
Lipschitz continuity away from singular boundaries.

## A finite rational certificate search with an explicit tolerance

Let gamma in (0,1) be a desired additive error and E>0 rational. Set

    Delta = gamma/[4*(E+2)],
    T0 = E+1+4*E/gamma,
    Tbar = ceil(T0/Delta)*Delta.

Use the rational grid t=j*Delta, retaining only h<=t<=Tbar; the left
condition is checked exactly as t^2>=E*(1+t). Its first member lies within
Delta of h. On t>=h, b_t-1<=1+h<E+2. The derivative bounds above also
give |U_t'|<=E+2 and |L_t'|<=5/4<E+2. Rounding a minimizing/maximizing
parameter upward to this grid therefore costs at most gamma/4. Truncation
at T0 costs less than gamma/4 for either endpoint by P1.

Suppose truthful rational matrices C_minus,C_plus obey the checker's
strict interior/order premises and

    ||C_minus-C||op, ||C_plus-C||op
       <= gamma/[4*(1+Tbar)].                         (P4)

The best grid lower certificate using C_minus is within 3*gamma/4 below
l(C), and the best grid upper certificate using C_plus is within
3*gamma/4 above u(C). A strict decision whose exact sharp endpoint has
margin at least gamma is therefore certified by some finite rational
grid member, assuming the target quadratic form is represented exactly.

This is an existence/construction argument with an intentionally coarse
grid of order gamma^(-2) at fixed E. Conventional scalar convex search
from [parameters.md](parameters.md) is a stronger computational approach.
The existing implementation has dimension, bit and file-size caps, so this
unbounded-arithmetic argument does **not** make that bounded implementation
a complete decision procedure. Nor does it create truthful input brackets.

For fixed nonzero E, P4 asks for matrix error of order gamma^2/E. The
near-boundary example explains why this order can be relevant, while
well-conditioned instances can use much coarser local bounds. Acquisition,
retention and certificate verification must be priced separately. A single
well-chosen value query can still be preferable when the target is known.
