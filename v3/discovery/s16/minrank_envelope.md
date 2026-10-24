# A lower envelope when the source uses the minimum number of input columns

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; pass 26.
Prospective same-model derivation, not independent confirmation.

Retain 0<C<=I on a k-dimensional orthonormal target space, ||c||=1,
and require M to have exactly r=rank(I-C)>0 columns. In a retained
orthogonal basis write C=I_(k-r) direct-sum C0, 0<C0<I, c=(c1,c0).
Let E=e^2>0, s=c^T Cc, m0=c^T C^2c, and

    cap=(E+sqrt(E^2+4E))/2,
    ustar=1/(2+cap),   bstar=1/(1+cap).

The candidate sharp lower endpoint over all compatible sources, arbitrary
additional output dimensions, and edits of operator norm <=e is:

* if s-m0>=ustar*s, it is bstar*s;
* otherwise it is the exact edited minimum for the canonical source
  M0=(0; (C0^-1-I)^1/2) and target (c1,c0).

The second value has the scalar representation below. This includes the
extra-column obstruction, while the earlier dimension-unrestricted bound
allows at least one more input column when needed.

## Reduce every compatible minimum-column source

Put X=M(I+M^T M)^-1/2. Since I-C=(W^T X)(W^T X)^T has rank r,
a right orthogonal change makes W^T X=(0; (I-C0)^1/2). Write the other
rows of X as Z. Then

    B=I-X^T X=C0-Z^T Z,        0<B<=C0,
    M=X B^-1/2.

Conversely every such B is realized by factoring C0-B in additional
output directions. For an input x=B^1/2 y, put

    z=(I-C0)^1/2 c0,
    A(y)=1-2*z^T y+||y||^2,
    a=||x||^2=y^T B y,      Q(y)=y^T C0 y.

The old squared residual is A-a. At fixed x, an operator-norm edit can
reduce its norm by at most e||x||, and a rank-one edit attains that
reduction (or cancels the residual). Thus the joint minimum over M, edits
and x reduces exactly to

    min_y min_(0<a<=Q(y))
        f(A,a),   f(A,a)=a+max(sqrt(A-a)-e*sqrt(a),0)^2.  (1)

At y=0 include a=0. Every positive a<=Q is attainable, for example by
B=(a/Q)C0. The closure a=0 adds f=A and cannot improve the attained
edited minimum, which is strictly below the unedited s for e>0,r>0.

For fixed A, f is minimized at a=ustar*A, with value bstar*A;
before that point it decreases with a. Also A>=s, with unique minimizer
y=z. If Q(z)>=ustar*s, the first case follows. Otherwise a global minimum
must have a=Q: an interior minimum in a has f=bstar*A, whose stationary
point y=z is infeasible. At the joining boundary the derivative in a is
zero, so the same conclusion applies. Coercivity f>=bstar*A prevents
escape to infinity. Taking B=C0 realizes a=Q for every y, proving the
canonical-source reduction. Finally Q(z)=s-m0.

## A scalar formula for the canonical edited minimum

This part holds for any fixed full-column-rank M and unit v. Let
B=M^T M>0, g=M^T v, bmin=lambda_min(B). For 0<t<=1 define

    rho(t)=1/(1-t)-E/t,
    A_t=(1-t)B+(1+E-E/t)I.

Let tmin be the unique root rho(tmin)=-bmin. For t>tmin and t<1,

    tmin=2E/[bmin+1+E+sqrt((bmin+1+E)^2-4*bmin*E)].

Then

    h(t)=(1-t)-(1-t)^2*g^T A_t^-1 g.                   (2)

At tmin use the pseudoinverse when g is orthogonal to the least-eigenvalue
space, and value minus infinity otherwise; h(1)=0. Then

    min_(||Delta||<=e) F(M+Delta;v) = max_[tmin,1] h(t). (3)

Proof: for R=||v-Mx||^2 and a=||x||^2,

    a+max(sqrt(R)-e*sqrt(a),0)^2
      =sup_(0<t<=1) [(1-t)R+(1+E-E/t)*a].

The quadratic in x has Hessian 2A_t>=0 on the stated interval, so its
minimum h(t) is a lower bound. At an interior maximizer, its minimizing
x satisfies -R+E*a/t^2=0 by differentiation, making this same t attain
the supremum. The bound is attained by the corresponding rank-one edit.

At the left endpoint, let x0 be the minimum-norm quadratic minimizer.
The finite right derivative at an endpoint maximum is nonpositive.
Adding z in the least-eigenvalue space changes that derivative by
(E/tmin^2-bmin)||z||^2, a strictly positive coefficient. Choose its norm
to make the derivative zero. It still minimizes the quadratic and now
attains the supremum in t, supplying the hard-case witness. The other
endpoint has value0 and cannot maximize because a finite edited inverse
is positive and h is positive for t sufficiently close to1.

This proof explicitly handles a singular endpoint rather than relying on
a numerical optimizer. Scalar trust-region/hard-case and regularized
total-least-squares methods are required direct literature comparisons.
The potential local delta is the minimum-column information contract and
its sharp source reduction, not scalar search in general.

For C=diag(1,1/2), c=e1, e=1, the canonical B=1 and g=0 give
tmin=(3-sqrt(5))/2 and (3)=(sqrt(5)-1)/2, agreeing with the direct
geometry in rank_boundaries.md. With zero input columns (r=0,m=0),
there is no edit at all and F=1; that degenerate case is outside this formula.

## Developmental screen and shape metadata

The corrected [small probe](minrank_probe.py) checks36 compatible-source
cases (9 cap,27 canonical), including9 scalar hard cases, one additional
hard case with nonzero g, and two local primal optimization comparisons.
Its [r1 evidence](minrank_probe_r1.json) passed in12,659,100ns. The original
reporting-variable bug and artifacts are preserved in failures.md. Neither
finite checks nor a local optimizer establish the global theorem.

Together with rank_boundaries.md, the proposed dimension classification is:

* m<rank(I-C): no compatible source;
* m=rank(I-C)>0: this lower endpoint; the earlier upper envelope still has
  matching sources;
* m>=rank(I-C)+1: both earlier unrestricted endpoints have matching sources;
* rank(I-C)=m=0: F=1; rank(I-C)=0 and m>=1: lower1/(1+E), upper1.

Here m counts allowed input columns. It does not impose full column rank
when m exceeds rank(I-C); zero columns are permitted. Extra output dimensions
are available in the matching-source class. Fixed output dimension is a
different problem. Appending a zero input column changes the allowed edit
domain, even though it leaves the original response matrix unchanged.

For C=diag(1,1/2), c=e1, e=1, retaining m=1 reduces the exact admissible
value width from1/2 to(3-sqrt(5))/2, a factor3-sqrt(5), or about23.6068%
less width than the m-unrestricted contract. This is dimension metadata,
not an additional matrix-value query. Its storage/checking cost remains
part of the interface; no wall-clock or stream saving has been measured.
An ordinary reasoner with the same shape metadata and envelope ties.
