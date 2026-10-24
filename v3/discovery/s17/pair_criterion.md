# When a retained block attains the ordinary two-edit diameter

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; a separate extension,
with novelty unassessed. This resolves the previously screened condition B3
in [pair_block.md](pair_block.md); it does not change N16-C/v1's event.

Fix e>0 and let g=g(e), lambda=1/(1+a^2) be the sharp universal coefficient
and unique scalar contact point in [pair_radius.md](pair_radius.md).
Let 0<C<I and ||c||=1, and put

    s=c^T Cc, m=c^T C^2c, b0=c^T C(I-C)^(-1)c.

The supremum of the two-edit contrast over the same compatibility class
as N16 equals g*s **if and only if**

    (1-lambda)*b0 <= s.                              (K1)

If K1 fails, that supremum is strictly smaller than g*s, although this
argument does not compute its exact value. Finite attainment of g*s occurs
if and only if Cc=lambda*c. Otherwise K1 gives a supremum approached by
finite sources with at most k+1 output and input dimensions.

## Necessary condition, without assuming bounded source dimensions

The universal proof bounds each contrast by v^T S R(S)v, v=Wc, where
R has its unique maximum g at lambda and 0<S<=I. Put
j(z)=z*(g-R(z)); its only zeros on [0,1] are0 and lambda.
If a sequence of contrasts tends to g*s, then

    v^T j(S)v -> 0.

For f(z)=z*(z-lambda), continuity and compactness imply
v^T f(S)^2v ->0. Indeed, in small neighborhoods of the two zeros f^2
is arbitrarily small; on their complement j has a positive minimum,
so the remaining integral is bounded by a constant times v^T j(S)v.
This argument uses scalar spectral measures of probability mass1 and
works even when dimensions vary with the sequence.

Set Q=W^T S^2 W. Always C^2<=Q<=C. A subsequence of these bounded
k-by-k matrices converges, and the preceding norm estimate gives

    Qc=lambda*Cc.

Thus Z=Q-C^2 lies in [0,T], where T=C-C^2>0, and
Zc=b=(lambda*C-C^2)c. Write K=T^(-1/2)ZT^(-1/2), so 0<=K<=I.
The inequality K^2<=K gives

    b^T T^(-1)b <= c^T b=lambda*s-m.                 (K2)

Diagonalizing C only to simplify this scalar expression, the difference
between the two sides of K2 is

    (1-lambda)*[(1-lambda)*b0-s].

Since lambda<1, K2 is exactly K1. Consequently failure of K1 excludes
even an approaching sequence, proving the asserted strict inequality.

## A one-output completion proves sufficiency

Assume K1 and define A=lambda*s-m. K2 implies A>=0. If A=0, then
b=0, so invertibility of C gives Cc=lambda*c. The canonical square
source M=(C^(-1)-I)^(1/2), with opposite edits of magnitude e on this
target eigenspace, attains g*s finitely.

Suppose A>0. Define the vector B=b/sqrt(A) and scalar

    D=lambda-(b^T Cc)/A,
    S0=[[C,B],[B^T,D]],  W=[I;0].

Direct multiplication shows S0^2 Wc=lambda*S0 Wc. Schur complements give

    D-B^T C^(-1)B=0,
    1-D-B^T(I-C)^(-1)B
       =(1-lambda)*[s-(1-lambda)*b0]/A >=0.           (K3)

Hence 0<=S0<=I and its compression is exactly C. The spectral measure
of Wc under S0 is supported at0 and lambda. S0 itself is singular,
which is why it is only a limiting resolvent.

For 0<delta<1 set

    S_delta=(1-delta)S0+delta*diag(C,1/2).

Then 0<S_delta<I with the same compression C. Let

    M_delta=(S_delta^(-1)-I)^(1/2),
    N0_delta=M_delta-eI, N1_delta=M_delta+eI.

Both edits have norm e. Their resolvent difference is the continuous
matrix function d_e(S_delta), where for 0<z<=1

    d_e(z)=1/[1+(sqrt(1/z-1)-e)^2]
            -1/[1+(sqrt(1/z-1)+e)^2],
    d_e(0)=0.

Functional calculus is continuous on the fixed compact spectral interval.
Since d_e(lambda)=g*lambda and the target measure of S0 is supported
at0 and lambda, these finite contrasts converge to g*s. This supplies
sufficiency with n=p=k+1, including equality in K1.

For any finite source S>0, equality in the universal bound forces
S Wc=lambda*Wc and therefore Cc=lambda*c. This proves the finite
attainment characterization, not merely nonattainment for the displayed
sequence.

## Interpretation and cheap instances

The criterion can be written lambda>=1-s/b0. Jensen's inequality gives
b0>=s/(1-s), so K1 implies s<=lambda; equality forces Cc=s*c.
The earlier sufficient condition C<=lambda*I implies K1, but is not
necessary. At e=1, lambda is between0.28 and0.29:

- C=diag(1/10,3/10), c=(1,1)/sqrt(2): s=1/5, b0=17/63,
  so the required cutoff is22/85<0.28. Equality of the supremum follows
  even though the block's larger eigenvalue exceeds lambda.
- C=diag(1/10,2/5), the same c: s=1/4, b0=7/18, and the cutoff
  is5/14>0.29. The retained block forces a strict improvement over g/4.

This identifies when the additional block information can improve the
universal old-value-only diameter. The ordinary common-source Gram SDP
already computes the exact answer in either case. The potential delta is
an explicit equality criterion and small limiting completion, not a new
advantage over that SDP or a demonstrated computational saving.

The [screen](criterion_result.json), using the preserved
[corrected adapter](criterion_check_v2.py), verifies three exact Schur
identities and the exact signs of both criterion examples. Four finite
floating witnesses approach the first example's supremum; at delta=1e-8
the observed gap is about1.44e-9 and the source norm is about21349.
The ordinary SDP agrees there to1.24e-10 and shows an approximate
0.00833045 strict gap for C=diag(0.1,0.4). The floating gap is not a
rigorous numerical certificate. The initial adapter failed on a wrong
JSON field before the mathematical checks; [failure](criterion_failed.json)
and [v1](criterion_check.py) are preserved. The repaired run used
71,707,600ns after setup on Python3.12.14.
