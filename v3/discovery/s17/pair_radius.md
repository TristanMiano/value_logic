# Exact common-source relative diameter for any edit radius

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; separate analytic
extension of [the unit-radius ordinary comparison](pair_exact.md).
Novelty is unassessed. This result uses established Young inequalities;
it is neither a new optimizer nor an N16-C/v1 promotion prerequisite.

For e>0 put E=e^2. Let q be the unique positive root of

    P_E(q)=q^3+(1+2E)q^2-(1+8E+3E^2)q-(1+E)^2,       (A1)

and a=sqrt(q). Define

    g(e)=4ae(1+a^2)/[(1+(a-e)^2)(1+(a+e)^2)].          (A2)

For every finite real M and every N_0,N_1 of its shape with
||N_i-M||op<=e,

    -g(e) S_M <= S_N0-S_N1 <= g(e) S_M,
    S_A=(I+AA^T)^(-1).                               (A3)

The coefficient is the smallest possible, already attained by scalar
M=[a], N_0=[a-e], N_1=[a+e]. For every target v it bounds the absolute
contrast by g(e)F(M;v), including nonunit targets. At e=0 the limit is zero
and both edits coincide with M. This statement includes sources with zero
singular values and arbitrary rectangular shapes.

## Root location and feasible parameters

The signs of the cubic coefficients are +,+,-,-, so Descartes' rule gives
one positive root, counting multiplicity. Alternatively its derivative
has one positive zero, with P decreasing from a negative value up to that
point and increasing thereafter to infinity. Direct substitution gives

    P_E(1)=-8E-4E^2<0,
    P_E(E)=-8E^2-3E-1<0.

Let b=(e+sqrt(E+4))/2, so b^2-eb=1. With z=b^2>1, E=(z-1)^2/z and

    P_E(z)=(z-1)(z+1)^2/z^2>0.

Consequently max(1,e)<a<b. In particular

    k=1+ae-a^2>0,  l=a^2+ae-1>k>0.

Choose lower parameter u=e/a>0 and upper parameter t=e/(a-e)>0.
The known-source Young bounds have

    d_u=u-E-E/u=-e l/a,
    d_t=t-E-E/t=e k/(a-e)>0.

All denominators are positive on the whole spectrum 0<S_M<=I. These
choices therefore give universal operator inequalities, without knowing
the singular vectors or the old solution of a particular source.

## Common spectral upper bound

Subtract the lower bound for N_1 from the upper bound for N_0. Their
difference is S_M R(S_M), with

    R(lambda)=a/[a-e+e k lambda]-a/[a+e+e l lambda].    (A4)

The sign of its derivative is the sign of

    sqrt(l)(a-e)-sqrt(k)(a+e)
       +e[k sqrt(l)-l sqrt(k)]lambda.

This affine expression decreases strictly. At lambda_star=1/(1+a^2),
the two denominators in A4 become
a[1+(a-e)^2]/(1+a^2) and a[1+(a+e)^2]/(1+a^2). The identity

    l[1+(a-e)^2]^2-k[1+(a+e)^2]^2 = 2 P_E(a^2)       (A5)

shows that the derivative vanishes there. Hence R increases to lambda_star
and decreases afterwards, and its global maximum on [0,1] is A2.
Functional calculus proves the upper half of A3; swap the edits for the
lower half. The scalar witness realizes A2 exactly, proving sharpness.

The proof uses no assumption that the edited matrices commute. The only
functions evaluated in a common spectral basis are the two valid bounding
functions of the same unedited S_M. This is why independent endpoint
subtraction using only a scalar old value loses information.

## Meaning and scope

This gives an exact comparison coefficient for the whole radius family,
using one cubic root and a scalar extremizer. It is a more useful analytic
output than an incremental SDP decimal improvement, but a short derivation
from classical inequalities may be judged routine. Do not infer novelty
from the failure of earlier weaker controls to match it.

For regularization rho>0, the value
min_x {||v-Mx||^2+rho||x||^2} equals F(M/sqrt(rho);v).
Thus a physical edit bound epsilon becomes e=epsilon/sqrt(rho) in A3.
This is ordinary rescaling, not an extra theorem or measured computation gain.

## Focused exact algebra check

[pair_radius_check.py](pair_radius_check.py) and
[pair_radius_result.json](pair_radius_result.json) verify A5, the scalar
derivative, and all three root-location identities symbolically. Rational
bisection encloses q,a and g(e) at e=1/10,1/2,1,2,10; every coefficient
interval has width below 1e-25. The values are approximately
0.200004901843, 1.010339800682, 2.159643663133, 5.495604651012 and
101.735881403862. These are exact interval checks with decimal displays,
not floating universal proof.

For e=1 the script also constructs rational u,t from a rational a and
proves the spectral difference is at most
**2159643663133/1000000000000** times S_M. Clearing its two positive
denominators gives a quadratic with positive leading coefficient and
strictly negative exact discriminant. This ordinary certificate is stronger
than the previous rational SDP coefficient and requires no optimizer trust.
The record includes the exact coefficients and discriminant. Runtime was
113,189,000 ns on Python3.13.14 with SymPy; it is verification cost, not
a comparative speedup or an independently replicated result.
