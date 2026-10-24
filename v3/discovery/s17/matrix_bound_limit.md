# A minimal matrix bound need not be directionwise sharp

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; a consequence of the
separate [two-edit criterion](pair_criterion.md). This explains why
directionwise scalar sharpness and matrix-order minimality are distinct.

Fix C and e, and consider all compressed contrast matrices
D=W^T(S_N0-S_N1)W for compatible sources and edits. They obey D<=gC.
Suppose C has an eigenvalue strictly below lambda and another strictly
above lambda. Then:

1. gC cannot be decreased by any nonzero positive semidefinite matrix
   while remaining an upper bound for every D.
2. Some unit directions c nevertheless have sup c^T Dc<g*c^T Cc.

For the first claim, the criterion matrix

    H=(1-lambda)C(I-C)^(-1)-C

has a strictly negative eigenvalue. Thus c^T Hc<0 holds on a nonempty
open set of unit directions. In every such direction the exact supremum
is g*c^T Cc. If gC-B were also a universal upper bound with B>=0,
each of these directions would have c^T Bc=0. A positive semidefinite
quadratic form vanishing on an open set is zero, so B=0.

For the second claim choose an eigenvector of C with eigenvalue above
lambda. Its criterion value is positive, and the strict-gap conclusion
applies. Therefore matrix-order minimality does not imply scalar
optimality in every direction. This argument does not assert that gC
is a least upper bound among all, potentially incomparable matrices.

At the opposite strict extreme C>lambda*I, the criterion fails uniformly
on the unit sphere. The explicit continuous gap bound in
[pair_gap.md](pair_gap.md), and compactness, give some epsilon>0 for
which every D<=gC-epsilon*I. There gC is not matrix-order minimal.
The boundary case lambda_min(C)=lambda is not classified here.

The distinction matters when compiling many directional decisions into
one matrix receipt: replacing the family by a single minimal upper
matrix can still discard useful directional information. Ordinary
semidefinite methods recognize the same order distinction. No novelty,
algorithmic superiority or promotion probability is assigned to it.
