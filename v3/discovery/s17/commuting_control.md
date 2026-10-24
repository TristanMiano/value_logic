# Why scalar spectral mixtures do not solve the block problem

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; a rejected reduction of
[N16-C/v1](claim.md). This clarifies the candidate's mathematical content;
the unrestricted ordinary [Gram SDP](gram_sdp.md) still ties its endpoints.
No superiority over conventional noncommuting methods is asserted.

An attractive shortcut is to diagonalize the old source and average sharp
scalar perturbation bounds, allowing an arbitrary hidden spectral measure
consistent with C. This loses general edited matrices. In fact, at a strict
interior upper optimizer and a target c that is not an eigenvector of C,
even the closed matrix-valued scalar-mixture relaxation has a strictly
smaller upper endpoint than N16-C.

## The scalar-mixture comparison

For 0<lambda<=1 define

    f_e(lambda)=1/[1+max(sqrt(1/lambda-1)-e,0)^2],
    f_e(0)=0.

This is continuous on [0,1]. If S_M and S_N commute and ||N-M||op<=e,
their common eigenbasis satisfies S_N<=f_e(S_M). Indeed, in each common
eigendirection z, reverse triangle inequality gives
| ||M^T z||-||N^T z|| |<=e. In terms of the corresponding old and new
inverse-Gram eigenvalues, this is exactly the displayed scalar upper bound.
No shared right singular basis is needed for this necessity argument.

A larger, closed comparison class takes any finite positive semidefinite
matrix weights A_j with

    sum A_j=I, sum lambda_j A_j=C, 0<=lambda_j<=1,

and maximizes sum f_e(lambda_j)c^T A_j c. Allowing zero eigenvalues gives
this class more closure points than finite old matrices possess. It is
equivalent to a positive operator-valued spectral measure with its first
moment fixed. The maximum is attained: split weights into rank-one terms;
their total scalar mass is tr(I)=k, and the normalization, first moment
and objective lie in the convex hull of a compact set parametrized by
lambda in [0,1] and a unit vector. Finite-dimensional convex-hull
compactness also supplies a finite representation of an optimum.

Realize the weights by an isometry W into a direct sum and let S have
scalar blocks lambda_j I. Then W^T S W=C and the objective is
v^T f_e(S)v for v=Wc. This is ordinary finite dilation machinery.

## Equality obstruction at a strict interior upper parameter

Suppose the N16 optimum has finite t>h, so d=t-E-E/t>0, a=1+t.
The scalar Young bound gives

    f_e(lambda)<=U_t(lambda)=a lambda/(1+d lambda).

Its equality set on [0,1] is exactly

    {0,lambda_t}, lambda_t=1/[1+E(1+1/t)^2].           (C1)

For a positive scalar old singular value sigma>e, Young equality requires
sigma-e=e/t, which gives C1. When sigma<=e, the scalar endpoint is one
and U_t is strictly greater than one for finite t. The limit at zero
supplies the other equality point.

For every dilated mixture,

    v^T f_e(S)v <= v^T U_t(S)v <= c^T U_t(C)c.         (C2)

If the mixture reached the last expression, the first equality would force
v to have spectral support only at {0,lambda_t}. For the second equality,
use inverse compression with A=I+dS. Its variational proof shows equality
on c holds precisely when

    A^(-1)Wc=W(I+dC)^(-1)c.

Write z=(I+dC)^(-1)c. Equivalently S Wz=W Cz. The first equality also
implies Wz=A^(-1)v has spectral support in {0,lambda_t}, so
S^2 Wz=lambda_t S Wz. Since S Wz=W Cz,

    W^T S^2 Wz=C^2 z=lambda_t C z.

C is invertible; hence Cz=lambda_t z, and c=(I+dC)z is an eigenvector
of C. This contradicts the stipulated target. Thus no optimal mixture
can achieve C2, and compactness gives a strictly positive gap.

N16's direct proof nevertheless constructs a finite source/edit attaining
c^T U_t(C)c. Its edited response therefore cannot commute with the old
response in this case. An example in the present record is
C=diag(1/10,9/10), c=(1,1)/sqrt(2), e=1/10: the branch conditions exclude
both the upper cap and cancellation, and c is not an eigenvector.
The statement here is qualitative strictness, not a measured percentage.

## Consequence for the assessment

Scalar optimal recovery of an unknown spectral distribution is an
insufficient reduction, even after allowing matrix-valued weights and
arbitrary hidden coordinates. The noncommuting source/edit compatibility
is real mathematical content. This explains one reason the exact block
solution is not obtained merely by averaging scalar endpoints.

It does not settle moderate novelty. Matrix S-lemma and operator-interpolation
methods already allow noncommuting matrices and provide the exact ordinary
comparison. The potential increment remains their particular explicit
one-parameter solution and finite equality construction. This obstruction
narrows a proposed shortcut; it is not evidence that no existing theorem
can supply the result by another route.
