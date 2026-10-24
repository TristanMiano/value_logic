# Exhaustive scalar branches and the small-edit comparison

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; a clarification of the
core proof and its strongest information control, not a new contribution
event. Write E=e^2, h=(E+sqrt(E^2+4E))/2, H=I-C,
s=c^T Cc, m=c^T C^2c and q=s-m. All of s,m,q are positive.

## Uniqueness and branch classification

The perspective representations in [parameters.md](parameters.md) do more
than rule out spurious local optima. The upper objective before minimizing
over z is strictly convex in (z,r) on its finite domain. If two points have
different z, the term z^T C H z is strictly convex. If they have the same
nonzero z and different r, the term E z^T C H z/r is strictly convex.
If z=0 at both, the term ||c||^2/(1-r) is strictly convex. The closed
perspective at r=0 forces z=0 and preserves this argument. Consequently
the partially minimized upper function is strictly convex: evaluate at the
convex combination of its two unique minimizers and use the strict inequality.

For the lower objective before maximizing over w, -||w||^2 is strictly
concave whenever the two w differ. If they coincide and are nonzero,
the negative perspective terms are strict when r differs. A lower maximizer
at an interior r has w nonzero because c is nonzero and its positive
definite quadratic has a nonzero linear term. The endpoint r=0 has w=0.
These observations give strict concavity of the partially maximized lower
function, including comparisons with r=0. Its positive maximum is unique.

Thus the endpoint derivative conditions in [proof.md](proof.md) are also
sufficient. There are exactly the following alternatives (equality belongs
to the indicated endpoint):

* Lower cap: m <= s(1+h)/(2+h). The value is s/(1+h).
* Lower interior: m > s(1+h)/(2+h). There is one interior stationary
  point in the concave r parameter, and the canonical k-dimensional source
  attains the endpoint.
* Upper cap: m <= s/(2+h). The value is (1+h)s.
* Upper cancellation: c^T(C^(-1)-I)c <= E. The value is 1.
* Otherwise the upper optimizer is a unique interior point.

The two upper endpoint conditions cannot overlap. The cap condition and
m>=s^2 imply s<=1/(2+h), while inverse Jensen gives
c^T(C^(-1)-I)c >= 1/s-1 >= 1+h > E=h^2/(1+h).
These are analytic classification checks, not a new numerical search rule.
The proof of endpoint attainment does not depend on uniqueness, so failure
of this supplementary argument would not silently invalidate that proof.

## Why strong old-solution controls are close for small edits

For fixed C,c, rescale t=e u. The lower denominator is

    I + e[u H+C/u] + e^2 C,

and the upper denominator is I+e(u-1/u)C-e^2 C. Uniformly on compact
positive u intervals, the two scalar families expand to

    lower = s-e[q u+m/u]+O(e^2),
    upper = s+e[q u+m/u]+O(e^2),

with u>=h/e tending to the constraint u>=1. Minimizing q u+m/u gives

    A(C,c) = s                     if m<=s/2,
             2 sqrt(m(s-m))         if m>=s/2.

The optimizing scales stay bounded and bounded away from zero as e tends
to zero. To see the upper bound on the scale, a cap choice has O(e) loss
from s, whereas, for t tending to zero with t/e tending to infinity,
the leading positive loss is q t; for t bounded away from zero the loss
from s is bounded away from zero. The same argument applies to both
families, using q>0. The lower constraint supplies the lower bound.
It follows that the exact endpoints have first-order changes -e A and
+e A, respectively. This is a local asymptotic statement with C,c fixed,
not a bound uniform as eigenvalues approach 0 or 1.

For a completely specified old solution/residual pair, the derivative of
F(M;v) in an edit Delta is -2 w^T Delta x, where w=(I+MM^T)^(-1)v
and x=M^T w. Its largest absolute norm-budgeted first-order change is
2e||w||||x||. In the canonical source these squared norms are m and s-m.
Thus, in the m>=s/2 regime, retaining C does not improve that leading
sensitivity over the full old vectors. Its sharper finite-edit interval can
still improve a decision, as the exact examples do. In the m<s/2 regime,
C allows hidden second moments above m, so it is not globally more
informative than retaining those complete vectors.

This explains the scale of the approximately 1.80% width improvement in
[width_control.md](width_control.md); it does not predict an empirical
distribution of improvements. The larger-budget
[cancellation example](cancellation_decision.md) demonstrates another regime.
No ordinary same-information method is surpassed by this asymptotic analysis.
