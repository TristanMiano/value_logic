# Partial two-scalar receipts: preserve their joint uncertainty

Codex (GPT-6), DEVELOPMENT, October 22, 2026. Derived from second_receipt.md
and two_scalar_upper.md. This is a prospective exact-information reduction;
no conic implementation or end-to-end service benchmark is claimed.

Let K be a nonempty compact convex set of feasible old pairs(s,m), with
0<s<1 and s^2<=m<s. A common example is the intersection of two truthful
receipt intervals with the moment constraints. Work in a compact subset of
the strict domain for the attainment statements; closure endpoints can be
handled by continuous limits. Define

    L(s,m)=s^2/[s+e^2*m+2*e*sqrt(m*(s-m))],
    U(s,m)=min_(alpha>=0) J(alpha;s,m)

as in the previous notes. The sharp interval permitted by K is

    [min_K L, max_K U].

The lower bound may require limiting matrices for some fixed moments; the
upper bound has finite rank-one witnesses. No joint matrix must realize
both extrema. Exact/outward treatment of K and the distance warrant remains
necessary.

## A tempting corner shortcut is unsound

Fix s=1/10 and e=3/2, while m ranges over its feasible interval. At m=s^2,
the sharp upper bound is13/36, and as m tends to s it tends to1/10.
But at the interior moment m=1/50 the finite extremizer in
finite_extremizers.md attains2/5, greater than both endpoint bounds.
Checking only endpoint moments can therefore certify a false upper bound.
Clipping an infeasible endpoint does not repair this dependence error.

## Lower endpoint is a constant-size conic problem

Write r=m/s and C(r)=1+2*e*sqrt(r*(1-r))+e^2*r. C is positive and concave.
The function1/C is convex, so L(s,m)=s/C(m/s) is its perspective and is
convex. Minimizing L over convex K is a convex problem, not a corner rule.

An explicit epigraph uses variables z,t and d:

    z>=0, z^2<=m*(s-m),
    d=s+e^2*m+2*e*z,
    t>=0, s^2<=t*d,
    (s,m) in K.

Minimize t. The squared-product inequalities are rotated second-order cones.
At an optimum z may be chosen as sqrt(m*(s-m)), giving exactly the displayed
lower endpoint. Box receipts and m>=s^2 also have conic representations.
These are ordinary conic transformations, not a new optimizer.

## Upper endpoint has a convex scalar outer search

For each fixed alpha>=0, put

    A=(1-alpha)^2+2*alpha*(1-alpha)*s+alpha^2*m,
    Q=s-m.

Then J=A+alpha^2*(1+e^2)*Q+2*alpha*e*sqrt(A*Q).
A and Q are affine in(s,m), nonnegative on the feasible moment region, and
the geometric mean is concave. Thus J is concave in(s,m), while it is
convex in alpha by its norm representation.

The common bound

    J(alpha;s,m)>=s+(1-s)*(alpha-1)^2

and J(0)=1 show that a minimizer can always be chosen in[0,2]. The standard
compact convex-concave minimax theorem then gives

    max_(s,m in K) min_(alpha in[0,2]) J
      = min_(alpha in[0,2]) max_(s,m in K) J.               (1)

For a fixed alpha, the inner maximization is a constant-size conic problem:
introduce z>=0 with z^2<=A*Q and maximize the linear expression
A+alpha^2*(1+e^2)*Q+2*alpha*e*z over K. The outer objective is convex as a
maximum of convex functions of alpha. This supplies a bounded scalar search
with checkable inner bounds, rather than a large search over unknown matrices.

An upper certificate needs a certified upper bound on the inner maximum at
one chosen alpha. A merely feasible primal point of that maximization gives
a lower bound and is insufficient. Similarly, a feasible point in the lower
endpoint minimization does not certify its minimum from below. Solver
termination and favorable approximate objectives are not certificates.

## A cheaper conservative alternative

For interval s in[l,u], m in[A0,B0], choose any nonnegative rational alpha.
Bound the affine A above using the signs of its coefficients, and Q above by
u-A0. If these bounds are A_bar,Q_bar, then

    g(N) <= (sqrt(A_bar)+alpha*e*sqrt(Q_bar))^2
             +alpha^2*Q_bar,

clipped to1. A lower certificate follows by separately bounding the numerator
and denominator of L, or by the ratio-interval rule in second_receipt.md.
Outward square-root intervals can make both checks entirely rational. This
loses joint information but can be cheaper than solving the sharp problem.

The proposed practical duty is to retain a few certified scalars after an
expensive solve, then answer later threshold questions under paid edit bounds.
The relevant comparison includes storing primal/dual vectors and direct new
solves; O(1) stored scalars may matter where O(n+r) vectors do not fit. The
same conventional mathematical implementation ties. Usefulness and novelty
require a real retention/acquisition tradeoff, not the phrase "value logic".
