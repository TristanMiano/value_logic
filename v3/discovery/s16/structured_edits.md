# A receipt can retain the part of a value that a structured edit cannot remove

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 23.

Let S=(I+MM^T)^-1 and F(M;v)=v^T S v, ||v||=1. An edit is
N=M+PZ with P^T P=I_r and ||Z||op<=e. Thus only r declared output
directions change. Retain C=W^T S W, where W is orthonormal and spans
P and v. Write P=WJ, v=Wc, E=e^2, a=1+t,
t>=t0=(E+sqrt(E^2+4E))/2, and

    T_W=t I-E*(1+1/t)*J J^T >=0.

Then valid matrix bounds, for all compatible full-dimensional sources, are

    (a*C^-1-T_W)^-1 <= W^T(I+NN^T)^-1 W
                         <= a*(C^-1+T_W)^-1.             (1)

Proof: Young's inequality gives NN^T<=a MM^T+(1+1/t)E PP^T,
and the reverse inequality follows by writing M=N-PZ. The full-space
resolvents are bounded by (a S^-1-T)^-1 and a(S^-1+T)^-1,
where T=tI-E(1+1/t)PP^T is positive and block diagonal across W.
Removing its positive perpendicular block decreases the lower inverse and
increases the upper inverse. A supported Woodbury update then compresses
exactly to (1). Positive definiteness follows from C<=I and T_W<=tI.
These are certificates, not a sharpness claim for structured edits.

## A protected value gives a better lower bound in some directions

Let Q span the orthogonal complement of P, A=Q^T M and u=Q^T v.
Deleting the changed residual rows from the ridge objective proves

    F(N;v) >= f0 := u^T(I+AA^T)^-1 u.

Block inversion of S gives the exact retained expression

    f0 = c^T[C-CJ(J^T C J)^-1 J^T C]c.                 (2)

Thus f0 is known from C even if Q, A and their solves were not retained.
It is independent of e. For example C=diag(.1,.9), P=e_2, v=e_1
gives f0=.1. No edit restricted to the second output row can reduce the
target value below .1. Unrestricted edits do not have this protection.
Use the larger of (2) and the scalar lower bound from (1). Ordinary
Schur complements/shorted operators are the direct mathematical antecedent.

## What extra structure the same receipt identifies

Put K=I+A^T A, x0=K^-1 A^T u, B=P^T M, b=P^T v and
G=P^T S P. Completing the square gives

    F(N;v)=f0+(b-(B+Z)x0)^T
                 [I+(B+Z)K^-1(B+Z)^T]^-1(b-(B+Z)x0).

With Btilde=B K^-1/2 and h=K^1/2 x0, the retained quantities determine

    Btilde Btilde^T = G^-1-I,
    ||h||^2 = ||u||^2-f0,
    Btilde h = b-z,     z=G^-1 P^T S v.

They therefore determine the Gram matrix of the rows of Btilde and h.
But the actual transformed edit is Z K^-1/2; replacing its ellipsoid by
the ball ||Z K^-1/2||<=e is only an outer bound. In particular K=I cannot
be assumed when h is nonzero: then A must be nonzero. This blocks a quick
sharpness claim based on freely choosing a canonical Gram realization.

This pass supplies a useful structured-change certificate, with generic
operator/Schur machinery acknowledged. It does not establish a new robust
optimization method or a measured acquisition/runtime advantage. A dense
W and all receipt acquisition remain charged.
