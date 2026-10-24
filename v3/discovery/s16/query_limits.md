# Scalar-query limits depend on the promised output

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass62.
Exact noiseless oracle q_C(z)=z^T C z, with unknown0<C<I in R^(k by k).
The following are deterministic worst-case transcript arguments, not lower
bounds on noisy statistical learning or all forms of matrix access.

## Exact answers to every later target require the whole symmetric dimension

Let m=k*(k+1)/2. Along any adaptive transcript with fewer than m scalar
queries z_j, there is a nonzero symmetric H orthogonal to every z_j*z_j^T.
For an interior source C, both C+epsilon*H and C-epsilon*H remain strictly
between0 and I when epsilon is sufficiently small. They produce the same
query answers and hence the same adaptive path. Some later c has c^T Hc
nonzero, so the two sources have different old target values c^T Cc.
Already the zero-edit duty cannot be answered exactly for every later c.
Conversely the diagonal and pairwise-sum queries recover C using m values.
This is elementary linear optimal recovery; no generic novelty claimed.

## Even one exact inverse target can require more than one old value

Fix c=e_1 and d>0, and ask for the exact nonlinear target
R(C)=c^T(I+d*C)^(-1)c for every allowed C. At the isotropic source
C_0=lambda*I,0<lambda<1, any deterministic exact algorithm must use at
least2*k-1 scalar queries along its transcript.

Let V span the measured rank-one matrices. Every H in V-perp preserves
the transcript for C_0+epsilon*H. With s=1+d*lambda, the local expansion is

    R(C_0+epsilon*H)
      =1/s-(d*epsilon/s^2)*c^T Hc
            +(d^2*epsilon^2/s^3)*||Hc||^2+O(epsilon^3).

Exact determination throughout the transcript fiber therefore requires
Hc=0 for every H in V-perp. Equivalently V contains the k-dimensional
space A of symmetric matrices supported in row/column1. Write each query
z_j=(a_j,b_j), b_j in R^(k-1). To span all off-diagonal entries of A,
the b_j must span R^(k-1). Hence the lower-right projections b_j*b_j^T
span a space of dimension at least k-1: choose k-1 independent b_j;
their rank-one matrices are linearly independent by applying a left inverse
to a putative linear relation. Projection of V onto the lower-right block
thus has rank at least k-1, and its kernel contains A of dimension k.
Consequently dim V>=2*k-1, so at least that many queries are necessary.

This source-local bound is attained: query q(e_1) and q(e_1+e_i),
q(e_1-e_i) for i=2,...,k. On the C_0 transcript these certify C*e_1=
lambda*e_1 for every compatible C, and therefore R(C)=1/(1+d*lambda).
An exact algorithm for arbitrary C can take further queries on other
transcripts. No global2*k-1 upper bound has been proved.

The same lower bound applies to exact c^T U_t(C)c when d>0, since that
quantity is (a/d)*(1-R(C)). It does NOT apply to returning a valid upper
certificate which happens to be tight at C_0. Indeed the one-query bound
a*q(c)/(1+d*q(c)) is valid by scalar Jensen and is tight at C_0, though
it need not equal the exact block value at other compatible matrices.

Thus the two proposed-value witnesses in query_witness.md are not an exact
nonlinear-oracle reconstruction for every source. They return valid bounds,
whose tightness depends on the proposal. This distinction is central to a
bounded reasoner's contract: a useful decision certificate can require much
less information than exact recovery or certified optimality of that bound.
Query vector storage, arithmetic, adaptivity and exact-real access remain
priced assumptions; a full response-vector oracle changes the result.
