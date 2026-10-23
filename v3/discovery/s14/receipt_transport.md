# Response receipts under changed intervention directions

Codex (GPT-6), DEVELOPMENT, October22,2026. This is a derived numerical
certificate adapter, not a claim of novelty in matrix perturbation theory.
The previous [SPD fallback](../s13/spd_fallback.md) covers omitted PSD updates;
the present duty changes the existing edit factor, including signed changes.

## Input and paid warrant

Let A be fixed SPD, b fixed and nonzero, y0=b^T A^(-1)b, and

    y_U(t)=b^T(A+t U U^T)^(-1)b / y0, t>=0.

An old response receipt describes U. A new edit U'=U+Delta may reuse it only
with an independently justified bound ||A^(-1/2)Delta||op<=epsilon.
Computing or validating that bound is paid. A sufficient, sometimes crude,
input is A>=alpha I and ||Delta||F<=d, giving epsilon=d/sqrt(alpha).
Insertion/removal of columns can use zero padding in a common column space.
Scalar response receipts alone do not establish this structural premise.

Put v=A^(-1/2)b/sqrt(y0), M=sqrt(t)A^(-1/2)U and
g(M)=v^T(I+MM^T)^(-1)v, with ||v||=1. For R=(I+MM^T)^(-1),
w=Rv, z=M^T w, s=g(M), a=||w|| and q=||z||,

    s=a^2+q^2,   s<=a,   a^2<=s,
    Dg(M)[H]=-2 w^T H z.

The first identity follows from (I+MM^T)w=v; the inequalities follow from
Cauchy-Schwarz and 0<R<=I. Consequently

    |Dg(M)[H]| <= 2 a sqrt(a-a^2) ||H||op
                <= (3 sqrt(3)/8) ||H||op.

The maximum occurs at a=3/4. Integrating along the straight segment gives

    |y_U'(t)-y_U(t)| <= min(1, (3 sqrt(3)/8) sqrt(t) epsilon).

The global Lipschitz constant is sharp: the scalar case M=1/sqrt(3), v=1
attains it infinitesimally. No assertion of a sharp finite-distance modulus
is made. Applying the argument to every unit v also gives the corresponding
operator-norm bound for the two inverse matrices.

## A receipt-dependent transport metric

The same derivative can use the old value rather than its global maximum.
Set x=a^2 in [s^2,s]. Maximizing 2 sqrt(x(s-x)) gives

    G(s)=s                         for 0<s<=1/2,
         2 s^(3/2) sqrt(1-s)       for 1/2<=s<1.

Define the increasing transform, with Phi(1/2)=0,

    Phi(s)=log(2s)                         for 0<s<=1/2,
           1-sqrt((1-s)/s)                for 1/2<=s<=1.

Then Phi'=1/G below1, so |D(Phi composed with g)[H]|<=||H||op.
For a formal endpoint argument, first truncate Phi above at Phi(1-delta),
integrate the resulting locally Lipschitz composition along the segment,
and let delta decrease to zero. Positive definiteness keeps g bounded away
from zero on this compact segment. Thus

    |Phi(g(M+H))-Phi(g(M))| <= ||H||op.

Use Phi(0)=-infinity and the monotone inverse

    F(r)=exp(r)/2                 for r<=0,
         1/[1+(1-r)^2]           for 0<=r<=1,
         1                       for r>=1.

A truthful interval [L,U] in[0,1] transports to

    [ F(Phi(L)-sqrt(t)epsilon),
      F(Phi(U)+sqrt(t)epsilon) ],

with the lower endpoint0 when L=0. This is a sufficient nonlinear band,
not a demonstrated minimax band. At an exact old response1 it gives the
sharp lower endpoint1/(1+t epsilon^2), attained by a scalar edit from zero.
The simpler bound |log g(M+H)-log g(M)|<=||H||op also follows directly from
2aq<=a^2+q^2=s, and gives the ordinary multiplicative transport comparator.

## Uniform decision service and other changes

The [four-receipt band](rational_receipts.md) has width at most0.0461 on
[1,16], conditional on its stated receipts. With epsilon=0.001 the global
transport rule gives width, and hence upper-envelope decision regret, at
most 0.0461+3 sqrt(3)*0.001 <0.051297. This is a derived guarantee under
a new premise, not an observed compute saving. The nonlinear rule can give
a narrower instance-specific band. Receipt acquisition, norm warrant,
interpolation, transport and decision optimization must all be charged.
For sequential edits, compare to the stored receipt's origin or accumulate
validated distances; a new version label does not reset the error budget.

Two elementary established comparators extend the scope without new claims:

* If (1-eta)A<=A'<=(1+eta)A, eta<1, then in unnormalized responses
  y_A(t/(1+eta))/(1+eta) <= y_A'(t)
  <= y_A(t/(1-eta))/(1-eta). This follows by inverse Loewner order and
  requires old receipts at the rescaled parameters, possibly outside their
  original interval.
* For a changed right-hand side b'=b+d and fixed A+tUU^T, a validated
  ||A^(-1/2)d||<=e transports an unnormalized [L,U] to
  [(max(0,sqrt(L)-e))^2,(sqrt(U)+e)^2] by the norm triangle inequality.

These facts turn model-version changes into explicit quantitative duties.
An ordinary validated numerical method can implement the same adapter.
Whether the combined contract is a useful moderately novel contribution
depends on closest-prior review and complete acquisition/computation costs.
