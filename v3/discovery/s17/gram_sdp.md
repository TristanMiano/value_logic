# An exact conventional semidefinite comparison

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; our reduction using
classical finite-dimensional operator completion. This is a stronger
comparison for [N16-C/v1](claim.md), not an independent confirmation or a
claim that a cited paper states this particular program verbatim.

## Two Gram matrices and linear constraints

Keep k,C,c,E from the core claim. Introduce output-space vectors

    W=[w_1,...,w_k], R=[R_1,...,R_k], r,u

and input-space vectors

    X=[X_1,...,X_k], x,z.

Only their two Gram matrices are optimization variables: G for [W,R,r,u]
of size 2k+2 and H for [X,x,z] of size k+2. Every inner product below is
therefore a linear function of G or H. Set v=Wc symbolically. Impose

    G>=0, H>=0,
    W^T W=I, W^T R=C,
    R^T R+X^T X=C,                                  (G1)
    R^T(v-r-u)=X^T x,                               (G2)
    r^T(W-R)=(x-z)^T X,                             (G3)
    v^T r=||r||^2+||x||^2,                          (G4)
    r^T u=x^T z,                                    (G5)
    ||u||^2<=E||x||^2,
    ||z||^2<=E||r||^2.                              (G6)

Minimize or maximize the linear objective v^T r. This is a finite SDP,
whose size depends only on the retained dimension k. No unknown matrix
entry, matrix inverse, rank constraint or bilinear optimization variable
appears in the program. The product Wc uses the fixed coefficients c.

Every genuine compatible source/edit gives feasible Gram data: take

    R=(I+MM^T)^(-1)W, X=M^T R,
    r=(I+NN^T)^(-1)v, x=N^T r,
    u=(N-M)x, z=(N-M)^T r.

The normal equations give (G1)-(G5); the norm budget gives (G6).
Thus the SDP initially gives outer endpoints. The converse below proves
that its optimized values are exact as infimum and supremum.

## Bounded two-sided interpolation

For fixed vectors x,z in an input space and r,u in an output space, there
exists Delta with norm at most e satisfying

    Delta x=u, Delta^T r=z

if and only if (G5)-(G6) hold. Zero vectors cause no exception: the norm
inequalities force the matching prescribed image to vanish. In nonzero
cases use orthonormal bases beginning with x/||x|| and r/||r||. The first
column and first row of Delta/e are prescribed, their shared entry agrees
by (G5), and each has norm at most one by (G6). The contraction-completion
theorem fills the remaining block.

For completeness, its sufficiency can be reconstructed directly. For a
partial contraction [[A,B],[D,?]], the row and column inequalities factor
B=(I-AA^T)^(1/2)P and D=Q(I-A^T A)^(1/2) with contractions P,Q.
The completion -Q A^T P gives the product

    diag(I,Q)
    [[A,(I-AA^T)^(1/2)],[(I-A^T A)^(1/2),-A^T]]
    diag(I,P).

The middle Julia matrix is orthogonal; the outer factors are contractions.
The factorization of B,D follows by pseudoinversion of the defect square
roots and their row/column inequalities. This is standard machinery credited
to the completion sources, not a new interpolation lemma.

## Recovering a source on the nondegenerate part

Factor feasible Gram matrices into vectors. Suppose [X,x] and [R,r] each
have linearly independent columns. Put

    A=[X,x], B=[W-R,v-r-u],
    D=[R,r], F=[X,x-z].

Equations (G1)-(G5) say exactly D^T B=F^T A. There exists a finite M with
MA=B and M^T D=F: start with M0=B(A^T A)^(-1)A^T and set

    M=M0+D(D^T D)^(-1)(F-M0^T D)^T.

The compatibility equality makes the correction vanish on A, while its
transpose supplies the required action on D. Separately obtain Delta from
the bounded interpolation above and set N=M+Delta. The resulting equations
are

    MX=W-R, M^T R=X,
    Nx=v-r, N^T r=x.

They establish both old and new ridge normal equations, the exact retained
C, and the desired edited objective v^T r. No minimax interchange is used.

## Removing the nondegeneracy restriction by a feasible mixture

A genuine source with both required column independences always exists.
Take n=p=k+1, W=[I;0], A0=(C^(-1)-I)^(1/2), and

    M=diag(A0,1), Delta=[[0,epsilon*c],[0,0]],
    0<epsilon<e.

The old R=[C;0] and X=[A0 C;0] have rank k. For the new residual,

    r_top=(C^(-1)+(epsilon^2/2)cc^T)^(-1)c,
    r_bottom=-(epsilon/2)c^T r_top,
    x_bottom=(epsilon/2)c^T r_top.

The scalar c^T r_top is positive, so the last coordinates show that [R,r]
and [X,x] have rank k+1. This gives feasible Gram matrices G0,H0 with
positive-definite corresponding principal submatrices.

For any feasible G,H, their convex mixture with a positive weight theta
of G0,H0 still satisfies every SDP constraint and has those principal
submatrices positive definite. It therefore comes from an actual source
by the preceding construction. As theta decreases to zero, its objective
converges to the original feasible objective. Dimensions at most 2k+2
outputs and k+2 inputs suffice for this approximation.

The feasible set is bounded and closed. From (G4), Cauchy-Schwarz and
||v||=1, its objective f satisfies 0<=f=||r||^2+||x||^2<=sqrt(f), hence
f<=1. Equation (G1) bounds R and X; (G6) bounds u and z. PSD Gram
matrices then bound every cross entry. The SDP thus attains both its
endpoints, and the mixture argument proves that they equal the original
source class's infimum and supremum. The direct N16 proof additionally
shows finite attainment with its smaller stated witness dimensions.

## Implication for contribution assessment

Ordinary semidefinite optimization and operator completion can express the
same information problem exactly. The strongest comparison is therefore
not merely a full-source solver or a scalar-only heuristic. N16's possible
delta is an explicit one-parameter solution of this information-constrained
SDP, together with finite extremizers and a small rational decision interface.
That may be a useful moderately novel synthesis; the derivation alone does
not establish novelty. A prior general result might already specialize to
the same collapse. The next literature comparison should include Gram-based
performance estimation and exact operator-interpolation formulations.

Numerical SDP solutions, if used as a screen, are only approximate controls;
they do not replace the exact theorem or rational checker.

The later [explicit dual certificates](dual_certificates.md) prove both
scalar bounds directly for every feasible point of the closed SDP. Together
with the genuine source/edit extremizers, they establish its exact values
without needing the mixture argument or numerical strong duality. The
mixture argument remains a valid characterization of the whole feasible
objective range; it is no longer the only route to the endpoint comparison.

## Direct specialization of the closest operator-interpolation result

The subsequent primary-source search found an especially close match:
[Bousselmi, Hendrickx and Glineur](https://arxiv.org/pdf/2302.08781),
Theorems 3.1 and 3.6. The inspection scope is in [literature.md](literature.md).
Their bounded interpolation theorem supplies (G5)-(G6) directly on taking
its four vector lists to be x,u,r,z and its norm bound to be e.

For the unbounded old source, use the four lists A,B,D,F defined above.
Their Theorem 3.6 specializes to D^T B=F^T A and existence of a scalar
ell>0 such that

    [[A^T A,B^T B],[B^T B,ell I]] >= 0,
    [[D^T D,F^T F],[F^T F,ell I]] >= 0.               (G7)

All their blocks are linear functions of G,H, and ell is an additional
variable. These LMIs retain the otherwise omitted kernel compatibility.
Thus adding (G7) gives a direct finite SDP representation with actual
source reconstruction at every feasible point, rather than only the
closed relaxation's approximation argument. Its feasible set need not be
bounded in ell, and projecting away ell need not give a closed set.
The preceding mixture argument proves that dropping (G7) nevertheless
preserves both optimized values for this particular interior-C problem.

This import substantially narrows any contribution claim: a generic exact
SDP and finite-dimensional operator interpolation are already available by
a straightforward specialization. What is not supplied by the inspected
theorems is the analytic collapse to N16's one-parameter rational families
or the stated small finite extremizers. Whether that additional solution
is a useful, moderately novel corollary/synthesis remains the assessment
question. A keyword difference does not establish that judgment.

## Focused numerical screen

[gram_probe.py](gram_probe.py) and [gram_result.json](gram_result.json)
compare the closed two-Gram program with scalar optimization on six cases:
scalar cap, interior and cancellation branches, the preferred block decision,
and dense two- and three-dimensional retained matrices. All twelve endpoint
solves reported `optimal`, with no warnings. The largest discrepancy was
5.072e-9 and the largest reported constraint violation 1.130e-9, within the
prospective 1e-6 and 5e-7 screening tolerances. The script recorded 94,448,400
ns for its six-case loop. Imports/setup were additional work, and no timing
comparison or exact certificate is inferred from these solver outputs.

CVXPY 1.9.3 with Clarabel 0.11.1 ran in an ignored task-local environment;
the result records Python, NumPy and SciPy versions. Installation did not
change the repository's dependency requirements. This one screen checks a
new mathematical comparator, not the already reviewed rational checker.
