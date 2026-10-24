# A finite joint receipt for a whole structured-edit family

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass44.
This is an explicit Woodbury/Gaussian-conditioning adapter, not a new
matrix-inversion identity. It is a strong control for norm-only envelopes
when the actual edit directions are known and affordable to retain.

Let M be n-by-m, P be n-by-r and Q be m-by-s, with Q^T Q=I.
Consider every N_A=M+P A Q^T, A in R^(r by s). P need not be orthogonal.
Let S=(I+MM^T)^(-1), targets W be n-by-k, and fix observed y in R^m.
Under the common standard Gaussian prior and unit observation noise,
mu=S M y and r0=y^T(I+M^TM)^(-1)y. Define

    U=[P,MQ],   G=U^T S U,   B=U^T S W,   C=W^T S W,
    g=U^T mu,  h=W^T mu,    q=Q^T y,
    K_A=[[AA^T,A],[A^T,0]],
    D_A=(I+K_A G)^(-1) K_A.

I+K_A G is invertible and D_A is symmetric. Indeed,
I+N_A N_A^T=I+MM^T+U K_A U^T is positive definite, and the inverse-free
Woodbury identity applies even when K_A is singular. The receipt has
O((k+r+s)^2) scalar entries, plus the source, direction and interpretation
identities; forming MQ and the solves for S is charged setup work.

For a=Aq, let G_P denote G's first r columns, g_P its first r entries,
B_P its first r rows, and t=g+G_P a. Then the entire family satisfies

    C_A = C - B^T D_A B,
    h_A = h + B_P^T a - B^T D_A t,
    r_A = r0 - 2 a^T g_P - a^T G_PP a + t^T D_A t.       (1)

C_A is the target posterior covariance and h_A the target posterior mean.
For the second and third lines, expand Ny=My+Pa before applying Woodbury.
The determinant lemma also gives

    det(I+N_A^T N_A)/det(I+M^TM) = det(I+K_A G)>0,
    p_A(y)/p_0(y) = det(I+K_A G)^(-1/2)
                      * exp(-(r_A-r0)/2).                (2)

Thus the SAME finite receipt supports exact model-conditional predictions
and relative likelihoods across a continuous edit family. A separately
declared prior over A can be updated using(2); integration or optimization
over that prior remains paid computation. The receipt does not discover
the prior, make the Gaussian model true, or calibrate a real-world model.
Covariance values alone generally do not determine these likelihoods.

## A symmetric representation and singular G

For numerical implementation, blindly inverting the nonsymmetric I+KG is
unnecessary. Factor G=L L^T with L having independent columns, dimension
d=rank(G). Set H_A=I_d+L^T K_A L. It is positive definite. Because
the columns of B and g lie in range(L), set b=L^dagger B and z=L^dagger g.
Then, in particular,

    C_A = C - b^T b + b^T H_A^(-1) b,
    det(I+K_A G)=det(H_A).                            (3)

To prove this, write S^(1/2)U=Z L^T with Z^T Z=I_d. The edited inverse
inside the S congruence is I-ZZ^T+Z H_A^(-1) Z^T. This also establishes
positive definiteness and the range assertions without assuming G invertible.
Equivalent small symmetric solves produce the other entries in(1).
Finite precision still needs a rounding/error certificate; formal exactness
does not make a floating Cholesky computation an outward bound.

## Exact small example and a boundary on what old values reveal

Take M=diag(3,1), P=e1, Q=e2, W=e1 and y=(1,1). The receipt is

    G=diag(1/10,1/2), B=(1/10,0)^T, C=1/10,
    g=(3/10,1/2)^T, h=3/10, q=1, r0=3/5.

For scalar edit A=a,

    C_a=2/(20+a^2),  h_a=(6+a)/(20+a^2),
    r_a=(a^2-6a+12)/(20+a^2),  determinant ratio=1+a^2/20.

The edits +a and -a have identical target covariance but different means
and data likelihoods. Their likelihood ratio is exp(6a/(20+a^2)). At a=1,
C=2/21,h=1/3,r=1/3. These are mathematical examples, not measured speedups.

## What is gained, what is not

After paid setup, every edited response requires algebra in at most r+s
dimensions, independent of n and m except for outputting requested objects.
This is useful only when many edits share P,Q, W and y or their retained
subspaces. Changing a direction, target or observation can require new
source access. If W is the whole output space, storing C is not small.
An ordinary Woodbury implementation supplied the same receipt ties exactly.
Compared with norm-only receipts this is a richer information contract,
not a free improvement under identical information. Generic exact-update
novelty is rejected; a useful formal synthesis would need a narrower stated
delta and a real acquisition/use case.

The exact rational [development probe](edit_kernel_probe.py) matched all
four quantities in(1)–(2) in96 cases, including rectangular edits, zero
updates and singular G. It passed on Python3.12.14 in39,233,800ns; source
hash and scope are in [the result](edit_kernel_probe.json). This is a finite
screen, not independent confirmation or a performance benchmark.
