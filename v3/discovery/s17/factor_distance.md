# A conventional covariance-factor representation of the edit constraint

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; prior-work comparison.
This is not a new metric or an additional contribution claim.

For PSD n-by-n matrices A,B define

    beta(A,B)^2 = min_K lambda_max(A+B-K-K^T)
                 subject to [[A,K],[K^T,B]] >= 0.

This is the centered Gaussian operator-norm specialization of the covariance
program in Peyre's Proposition 3.6 / Appendix D, recorded in
[literature.md](literature.md). Its finite factor interpretation follows
directly from a Gram factorization, without importing the transport theory.

If M M^T=A and N N^T=B, then K=M N^T is feasible and

    A+B-K-K^T=(M-N)(M-N)^T.

Conversely factor any feasible block as [M;N][M;N]^T. At most 2n columns
are needed, and the same identity holds. The feasible K set is compact:
every scalar entry is bounded by the corresponding two-by-two PSD minor.
Thus beta is the minimum operator-norm distance over pairs of common-width
factors, when that width may be chosen. A prescribed small number of columns
would impose an extra rank restriction and is not automatically equivalent.

Consequently the dimension-unrestricted N16 problem can also be written
using PSD A,B, the condition beta(A,B)<=e, the retained equality
W^T(I+A)^(-1)W=C, and objective c^T W^T(I+B)^(-1)Wc.
This is an exact alternative representation of the source/edit class.
It is not yet the claimed analytic solution: the inverse-compression
constraint and the fixed-target inverse objective still have to be optimized.

The prior commuting-covariance formula cannot simply diagonalize this whole
problem. The extremizing edit in the direct proof is generally rank one
along target-dependent directions, and A and B need not commute. Nor does
commutation with C follow from retaining C. The operator-interpolation Gram
SDP remains the more direct exact conventional formulation for comparing the
claimed one-parameter solution. This extra representation adds context to
the novelty risk, not evidence of an algorithmic or economic advantage.
