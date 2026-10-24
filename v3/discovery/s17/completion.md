# Completion comparison and an old-response parametrization

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT. These are our
reconstructions for comparison, not independent confirmation or new claims
about classical completion theory. See [literature.md](literature.md).

## What the classical linear constraint already permits

A contraction B satisfying BS=T can be represented by the positive block
matrix

    [[I, S, B^T],
     [S^T, S^T S, T^T],
     [B, T, I]].

Schur complement of the first I leaves a zero diagonal block, forcing
T=BS, and the other diagonal block is I-BB^T. Prescribing a block row
and column of B makes this a one-missing-block positive completion problem.
Compatible positive Gram representations on the overlapping principal
submatrices can be glued along their common span. This reconstructs the
mechanism behind the inspected strong-Parrott result without relying on
corrupted OCR signs. Thus adding linear interpolation equations is already
within the classical method. N16 needs to identify its remaining nonlinear
constraints, rather than treating interpolation as a distinguishing feature.

## Exact parametrization of the old responses alone

Fix W^T W=I and 0<C<I. Let R denote all old residual vectors,
X all old coefficient vectors. Their normal equations are

    R+MX=W,    M^T R=X.                              (1)

The stored information is W^T R=C. Write Q=R^T R. Equations (1) imply

    X^T X=C-Q,    C^2<=Q<C.                         (2)

The lower inequality is projection onto span(W). For strictness on the
right, if Xz=0 then Rz=Wz by (1), whence Cz=z; since C<I, z=0.

Conversely, choose any Q satisfying (2), any R with W^T R=C and
R^T R=Q, and any X with X^T X=C-Q. Such R exists whenever the available
hidden output dimension is at least rank(Q-C^2); in coordinates W=[I;0],
take R=[C;H] with H^T H=Q-C^2. X has full column rank and can be chosen
in input dimension at least k. Put A=W-R. Then

    R^T A=C-Q=X^T X.                               (3)

There is an M with MX=A and M^T R=X. An explicit construction is

    M0=A(X^T X)^(-1)X^T,
    D=X-M0^T R,
    M=M0+R(R^T R)^(-1)D^T.

Indeed D^T X=X^T X-R^T A=0, so MX=A, and M^T R=X.
In fact for this particular compatible pair D=0 already, because
M0^T R=X(X^T X)^(-1)A^T R=X. The displayed correction also illustrates
the general two-sided interpolation compatibility condition. Therefore
(I+MM^T)R=W and W^T(I+MM^T)^(-1)W=C exactly.

The entire old-response moment class is consequently just the matrix
interval C^2<=Q<C, with the indicated dimension condition. This is a
direct finite-dimensional construction. It makes the moment freedom in
the cap witnesses explicit and connects it to ordinary interpolation.
It does not establish a novel general completion theorem.

## Why the edited problem is still coupled

Let v=Wc, r and x be the edited residual and coefficient, and
N=M+Delta. Besides (1), the new equations demand

    Mx=v-r-Delta x,    M^T r=x-Delta^T r,
    ||Delta||op<=e.

Two-sided interpolation forces, among other conditions,

    R^T(v-r-Delta x)=X^T x,
    r^T(W-R)=x^T X-r^T Delta X,
    r^T v=||r||^2+||x||^2.

The unknown response vectors multiply the unknown edit. These equations
do not constitute a single fixed-data linear interpolation problem.
Fixing their Gram data may permit a completion-based elimination, but
that elimination and its scalar optimization still have to be shown.
The endpoint witnesses in [proof.md](proof.md) supply one direct route.
This observation limits a claimed immediate reduction; it is not proof
that no such reduction exists or that the resulting corollary is novel.
