# A sharp local contrast bound with hidden-output uncertainty

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass51.
This is a proposed mathematical adapter, not an independently checked theorem
or a claim of new matrix differentiation. The retained full block matters.

Let S=(I+M M^T)^-1, W^T W=I_k, C=W^T S W, and H=H^T be a task contrast.
For a Frobenius edit ||Delta||_F<=e, set

    P=S W, Q=M^T S W, D=W^T S^2 W.

Then P^T P=D, Q^T Q=C-D and

    d tr(H W^T S W)[Delta] = -2 <P H Q^T, Delta>_F.
    ||P H Q^T||_F^2 = tr(H D H (C-D)).             (1)

Every compatible finite source satisfies C^2<=D<=C. Conversely every D in
this interval can be approximated by a positive contraction S with the
required compression, allowing extra outputs and sufficiently many input
columns. To see the contraction completion, write D-C^2=X X^T. A bottom
block Y can satisfy S=[[C,X],[X^T,Y]] between0 andI exactly when

    X^T C^-1 X <= Y <= I-X^T(I-C)^-1 X,

which is possible because X X^T<=C(I-C). Interior approximation avoids
zero eigenvalues; eigenvalue1 is allowed. Here assume0<C<I, and treat
fixed shape separately. Thus the worst local slope is the explicit compact
optimization2*sqrt(max_D tr(H D H(C-D))). If H is indefinite this objective
is not in general concave in D; a generic convex-optimization claim is unsafe.

## An exact two-action calculation

For k=2,C=c I_2,0<c<1,H=diag(1,-1), the contrast initially vanishes.
Its sharp uniform first-order radius coefficient is

    L(c) = 2*c*sqrt(1-c),             0<c<=1/2,
           2*c*sqrt(2*c*(1-c)),       1/2<=c<1.    (2)

Proof: write D=c T with cI<=T<=I, and T=[[t+a,z],[z,t-a]]. Its eigenvalues
are t+/-r, r=sqrt(a^2+z^2), and r<=min(t-c,1-t). Equation(1) becomes

    tr(H D H(C-D))/c^2 = 2[t(1-t)+r^2-2a^2].

At fixed t this is maximized by a=0 and maximal r. Below t=(1+c)/2 the
result divided by2 is t*(1-2c)+c^2; above it the result is1-t. For c<=1/2
the maximum is at the middle, giving c^2*(1-c). For c>=1/2 it is at t=c,
giving2*c^3*(1-c). Taking twice the square root proves(2).

For c<1/2, the extremal D has eigenvalues c,c^2 and eigenvectors rotated
45 degrees from the two actions. It is approached with just one extra
output and two input columns: take u=(1,1)/sqrt(2),0<tau<1, and

    S_tau = [[c I_2, sqrt(tau*c*(1-c))*u],
             [transpose, 1-tau*c]].

This is positive, at mostI, and rank(I-S_tau)=2. Its D tends to the
required extremizer as tau increases to1. Choose M with M M^T=S_tau^-1-I
and take Delta proportional to-P H Q^T. The source norm diverges in this
limit, so the endpoint is a supremum, not an attained finite-source maximum.
For c>=1/2, D=C^2 is attained by the two-output canonical source directly.

## A finite-edit certificate with a uniform remainder

Form the symmetric dilation A=[[0,M],[M^T,0]] and E=[[0,Delta],[Delta^T,0]].
The output block of Re(I+iA)^-1 is S. With R=(I+iA)^-1 and
R_new=(I+i(A+E))^-1, the exact resolvent identity is

    R_new = R-i R E R-R E R E R_new.

All these resolvents have operator norm at most1. The remainder therefore
has norm at most||E||_op^2=||Delta||_op^2<=e^2. Compression and the nuclear-
operator trace inequality give

    |tr(H W^T(S_new-S)W)| <= e*L(c)+2*e^2          (3)

in the two-action case. The same argument gives e times(1)'s worst slope
plus||H||_* e^2 in general. This uniform remainder also establishes sharpness
of(2) as e decreases to0, despite the approximating source's growing norm.

For c=2/5,e=1/100, equation(3) gives

    contrast radius <= (1/125)*sqrt(3/5)+1/5000
                    < 0.006396774.

Subtracting individually sharp one-target intervals under the same full
block yields radius c*sqrt(e^2*(4+e^2)) >0.008. Therefore(3) reduces that
radius by more than20.04% in this constructed example. It is a guaranteed
width comparison, not a task accuracy, audit-fee or CPU measurement.
The Frobenius budget is shared by the two actions; treating their extremizers
as independently compatible discards this constraint.

If the output dimension is known to be exactly two, D=C^2, and the first
branch in(2) is no longer the sharp slope. Hidden-output uncertainty is
therefore substantive even at first order. All equal-information ordinary
implementations of this calculation give the same certificate.

The small probe passed120 floating derivative/remainder cases and six
sharp-slope limit cases. Its exact rational certificate gives radius upper
79959667/12500000000 and improvement lower20040333/100000000 (>20.04%).
The run took26511700ns on Python3.13.14/NumPy2.2.5; source SHA-256
538d3418cb0def3d1c926c2e95ce9cf5811320796e3896d526f7faee416bb8d5.
Finite probes are developmental checks, not a substitute for the argument.
