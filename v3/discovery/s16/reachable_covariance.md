# Full response information gives a joint reachable covariance set

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass45.
Procrustes distance, Bures geometry and semidefinite programming are prior
machinery. The purpose here is to state their exact information/shape scope.

Suppose the full old response C=(I+MM^T)^(-1) is retained, M is n-by-m,
and the edit obeys ||N-M||F<=e. Write A=C^(-1)-I and B=X^(-1)-I for a
proposed edited response0<X<=I. Then X is reachable if and only if

    rank(B)<=m,
    d_B(A,B)^2 := tr(A)+tr(B)-2 tr((A^(1/2) B A^(1/2))^(1/2)) <= e^2. (1)

The old feasibility premise already gives rank(A)<=m. To derive(1), fix a
factor of B with at most m columns and optimize its right orthogonal
orientation against the given M. Expanding the squared Frobenius distance
leaves maximization of the cross trace. A singular-value decomposition
gives its nuclear-norm maximum, the square-root trace in(1). The available
m columns suffice whenever both factor ranks are at most m. This is the
ordinary orthogonal Procrustes/Bures identity, specialized to the response.

An alternative exact condition, which also exposes the operator-norm case,
is existence of K with

    Z=[[A,K],[K^T,B]] >=0,  rank(Z)<=m.                (2)

The factors of Z can be right-rotated so their first block is exactly M.
The edited factor N then obeys

    ||N-M||F^2=tr(A+B-K-K^T),
    ||N-M||op^2=lambda_max(A+B-K-K^T).

Thus replace the scalar trace constraint by A+B-K-K^T<=e^2 I for an
operator-norm edit. This is exact WITH the rank condition. No claim is made
that dropping rank is harmless for the operator-norm version.

## An exact convex problem for one useful joint duty

When m>=n and H>=0, minimizing the weighted sum of edited variances
tr(H X) under the Frobenius budget is the semidefinite program

    minimize tr(H T)
    subject to B>=0, [[A,K],[K^T,B]]>=0,
               tr(A+B-K-K^T)<=e^2,
               [[I+B,I],[I,T]]>=0.                 (3)

The last constraint is T>=(I+B)^(-1); its relaxation is tight at the
minimum because H>=0. Optimizing K gives(1), and m>=n removes the rank(B)
restriction. The PSD H hypothesis matters: (3) is not a valid relaxation
for an arbitrary signed action contrast or for maximizing variance.
The matrices in(3) have output dimension n; this is not a small compressed
receipt unless the full retained output block itself is small.

Dropping shape can create an unattainable apparent gain. For M=0, n=2,
m=1, e=1 and H=I, any actual update has rank at most1 and the minimum
trace response is3/2. The rank-free SDP selects B=I/2 and gives4/3.
Two input columns make4/3 attainable. The difference is an information
and feasibility distinction, not a numerical-solver defect.

This result gives a strong conventional joint-control problem for the
earlier response-envelope work. It does not claim new Bures geometry or a
new SDP technique. Useful novelty, if any, must reside in a narrower
retention/verification contract or consequence not already in that work.
