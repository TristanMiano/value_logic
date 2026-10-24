# A simpler operator proof, simultaneous targets and rounded receipts

Codex (GPT-6), October 23, 2026. DEVELOPMENT. This reorganizes the new
matrix bounds using ordinary operator Young/Jensen inequalities. It is
not an independent reconstruction. The simpler proof narrows the possible
novelty to the exact retained-information contract and its sharpness result.

Let S=(I+MM^T)^(-1), S_new=(I+NN^T)^(-1), ||N-M||op<=e, E=e^2>0.
For any t>=t0=(E+sqrt(E^2+4E))/2 put

    a=1+t, d=t-E-E/t>=0,
    L_t(X)=X*(a*I-d*X)^(-1),
    U_t(X)=a*X*(I+d*X)^(-1).                           (1)

All denominators are positive on0<=X<=I, since a-d=1+E+E/t>0.

## Full response inequalities

Writing N=M+Delta, the elementary squared-norm inequality gives

    NN^T <= (1+t)*MM^T+(1+1/t)*E*I.

This is a Loewner inequality: test it on every vector. After adding I
and reversing order on inversion, it gives S_new>=L_t(S).
Apply the same argument to M=N-Delta and rearrange to get

    I+NN^T >= (1/(1+t))*(S^(-1)+d*I).

The right side is positive, so inversion gives S_new<=U_t(S).

## A compression is enough for a family of later targets

For W^T W=I and retained C=W^T S W, the inverse-compression inequality
W^T A^(-1)W >= (W^T A W)^(-1) implies

    L_t(C) <= W^T L_t(S)W <= W^T S_new W
             <= W^T U_t(S)W <= U_t(C).                (2)

For d>0, use L_t(X)=(a/d)*(a*I-d*X)^(-1)-I/d and
U_t(X)=(a/d)*(I-(I+d*X)^(-1)); d=0 follows directly.
These are ordinary operator convexity/concavity special cases, explicitly
credited to the comparison in literature.md. No general scalar-to-operator
inference is made.

The SAME t in each matrix bound works for every later c simultaneously.
For each requested v=Wc one may also optimize t after seeing c, because
(2) already holds for all t,c on the same deterministic receipt event.
Taking independently optimized eigenvalue bounds does not preserve (2).
An infimum in Loewner order is not supplied by pointwise scalar minimization.

The upper formula is exactly the earlier parameterization: in
matrix_receipt.md set t=E*(1+eta)/eta, mapping eta in(0,t0] onto
t in[t0,infinity). The lower formula already uses t=eta. Thus the two
earlier sharpness constructions match these simpler bounds in0<C<I.
Their different compatible extremizers and boundary qualifications remain.

## Truthful matrix error bars

Suppose an acquired receipt proves C_minus<=C<=C_plus. The same rational
maps are operator increasing on their valid denominator domains; this
also follows directly from the inverse forms above. Consequently

    L_t(C_minus) <= W^T S_new W <= U_t(C_plus).          (3)

For example, a warranted operator error||C_hat-C||<=epsilon gives
C_minus=C_hat-epsilon*I and C_plus=C_hat+epsilon*I. It is sufficient
to check the displayed denominator domains; the lower answer may be
negative and then uninformative. For a particular c, intersect its scalar
interval with[0,||c||^2]. Do not silently treat printed C_hat as exact.

Do NOT clip eigenvalues of C_minus up to0 or C_plus down to1 and claim
that the new matrices still bracket C. Although the clipping functions
are monotone on scalars, they are not generally operator monotone. Unless
commutation or a separate warrant is available, such clipping can reverse
the necessary matrix comparison. Retaining a feasible matrix uncertainty
set and optimizing over it is another, more costly option.

A concrete lower-clipping counterexample is
C=[[3/20,1/4],[1/4,3/4]] and C_minus=diag(-1/10,1/2).
Both C and I-C are positive definite (determinants1/20 and3/20), and
C-C_minus is the positive semidefinite all-ones matrix divided by4.
But C-diag(0,1/2) has determinant-1/40, so clipping the lower matrix
destroys its order warrant. This also arises from C_hat=diag(3/20,3/4)
with an exact operator error bound1/4. Replacing C by I-C gives the
corresponding upper-clipping obstruction.

The resolvent identity gives simple error penalties when the endpoints
have the stated order. If ||C-C_minus||<=epsilon and both are<=I, then

    ||L_t(C)-L_t(C_minus)||<=a*epsilon/(a-d)^2.

If0<=C<=C_plus and||C_plus-C||<=epsilon, then

    ||U_t(C_plus)-U_t(C)||<=a*epsilon.

These are conservative norm bounds. They establish continuity of a fixed
certificate, not optimal precision allocation or a measured numerical price.

## Retention costs must include the target basis

Retaining C uses k(k+1)/2 scalars, but an arbitrary dense W itself costs
nk scalars. A small-retention service therefore needs W already available,
procedurally specified, or externally supplied as part of later requests.
Selected coordinate targets give a simple implicit W, costing their indices.
If W must be stored densely just for this service, retaining S*W can be a
competitive ordinary control and the claimed storage motivation may vanish.
Acquisition of C, its error warrant, t/z witnesses and the edit norm bound
must all be charged. The construction does not turn source access into a
free resource merely by calling the result a receipt.
