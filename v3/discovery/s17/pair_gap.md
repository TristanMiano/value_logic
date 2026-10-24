# A quantitative block-information improvement over the universal diameter

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT, separate from N16-C/v1.
The comparison is with the sharp ordinary bound using only the old target
value. The stronger ordinary Gram SDP uses the block and still ties.

Use the notation of [the equality criterion](pair_criterion.md), with
k0=1+ae-a^2>0, l0=a^2+ae-1>0. The double contact in the scalar proof gives

    g-R(z)=g e^2 k0 l0 (z-lambda)^2
            /[(a-e+e k0 z)(a+e+e l0 z)].

Thus, for0<=z<=1,

    z[g-R(z)] >= K z(z-lambda)^2 >= K z^2(z-lambda)^2,
    K=g e^2 k0 l0/[(a-e+e k0)(a+e+e l0)]>0.         (Q1)

Let eta=(1-lambda)*b0-s>0 and T=C-C^2. With
b=(lambda*C-C^2)c define

    F(b)=b^T T^(-1)b-c^T b=(1-lambda)*eta,
    d=2T^(-1)b-c=[(2lambda-1)I-C](I-C)^(-1)c.

Every compatible Q=W^T S^2W supplies y=(Q-C^2)c with F(y)<=0.
Convexity of the quadratic F, or direct expansion at b, gives

    F(b)<=-d^T(y-b)<=||d||*||y-b||.

Here d cannot be zero when F(b)>0, since the global minimum of F is
nonpositive (F(0)=0). Moreover y-b=W^T(S^2-lambda*S)Wc, so Q1 yields
the explicit uniform inequality

    contrast <= g*s-K*F(b)^2/||d||^2 < g*s.          (Q2)

This establishes a positive numerical margin without relying on an
approximate SDP. It is generally conservative, not the exact block
diameter. A simpler scalar-moment consequence is

    contrast <= g*s-K*(max(0,m-lambda*s))^2/s,        (Q3)

by Cauchy--Schwarz with weight z and c^T Qc>=m. Q2 can improve the
bound even when Q3 is zero.

## The first two spectral moments do not decide equality

At e=1 compare these two retained blocks and targets:

    A: C=diag(1/10,3/10), c=(1,1)/sqrt(2),
    B: C=diag(14/75,19/20), c=(15,2)/sqrt(229).

Both have s=1/5 and m=1/20. But b0 is17/63 for A and34/61 for B.
The criterion holds for A and fails for B. The first block therefore has
supremum g/5, whereas the second has a strictly smaller supremum, with
an explicit positive gap supplied by Q2. These are moments of the
compressed block C, not a claim that all retained old solution vectors
or the full old second response block coincide.

This is a useful limitation on a proposed scalar simplification: old value
and this one additional moment cannot recover the block's diameter
eligibility. The complete matrix or another sufficient nonlinear statistic
can. It is not evidence that no small statistic can help, since the criterion
itself uses just s and b0 for the specified equality question.

The [rational instantiation](gap_result.json) certifies K>3/20 and
0.28714<lambda<0.28715 from the existing rational cubic enclosure.
For block B, Q2 improves the universal bound by at least
0.0002153742220; Q3 supplies zero there. For diag(0.1,0.4) with equal
target weights, Q2 gives at least0.0000505326061, while Q3 is stronger.
These conservative absolute margins have exact rational values in the
record. [gap_check.py](gap_check.py) took368,900ns after setup, using
Python3.12.14. They measure bound improvement with extra block information,
not audit fees, computation or an advantage over the same-information SDP.
