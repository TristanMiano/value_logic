# Direct reconstruction of the N16-C/v1 endpoints

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; same-model reconstruction.
This argument reconstructs the [specified claim](claim.md), using direct
normal equations to check attainment. It is not independent confirmation.
The [literature log](literature.md) credits the classical ingredients.

## 1. Ridge value and compression inequality

For any real N and v, strict convexity of
J_N(x)=||v-Nx||^2+||x||^2 gives the unique minimizer
x_N=N^T(I+NN^T)^(-1)v. Completing the square, or substituting its normal
equation N^T(v-Nx_N)=x_N, gives F(N;v)=v^T(I+NN^T)^(-1)v.
The dual identity is

    F(N;v) = max_w [2 v^T w - w^T(I+NN^T)w].             (1)

For a positive definite A and an isometry W, apply this quadratic
variational identity to (Wc)^T A^(-1)(Wc) and restrict the optimizing
vector to Wz. This proves, for all c,

    W^T A^(-1) W >= (W^T A W)^(-1).                    (2)

Thus the needed inverse-compression statement follows directly; no
scalar convexity is promoted to operator convexity without justification.

## 2. Validity for every compatible source and edit

Put S=(I+MM^T)^(-1), S_N=(I+NN^T)^(-1), Delta=N-M,
E=e^2, a=1+t, d=t-E-E/t. For t>=t0, d>=0. Vector Young's
inequality and ||Delta||op<=e give

    NN^T <= a MM^T + (1+1/t) E I,
    MM^T <= a NN^T + (1+1/t) E I.

Adding identities, rearranging and reversing positive definite order on
inversion yield

    L_t(S) <= S_N <= U_t(S),
    L_t(X)=X(aI-dX)^(-1), U_t(X)=aX(I+dX)^(-1).          (3)

The denominators are positive for 0<=X<=I because
a-d=1+E+E/t>0. For d>0 write

    L_t(X)=(a/d)(aI-dX)^(-1)-I/d,
    U_t(X)=(a/d)[I-(I+dX)^(-1)].                        (4)

Applying (2) proves

    L_t(C) <= W^T L_t(S)W <= W^T S_N W
             <= W^T U_t(S)W <= U_t(C).                 (5)

For d=0 the same statement follows by linearity. This establishes every
pointwise scalar bound and allows different t choices for a declared c.
It does not establish a Loewner infimum of separately optimized matrices.

Both rational maps in (4) are operator increasing on this domain. Hence
truthful brackets 0<C_minus<=C<=C_plus<I give

    c^T L_t(C_minus)c <= F(N;Wc) <= c^T U_t(C_plus)c.    (6)

Intersect scalar endpoints with [0,1]; do not clip matrix eigenvalues.
The checker needs (6), not the attainment argument that follows.

## 3. A finite dilation that adjusts one second moment

Let H=I-C, s=c^T Cc, m0=c^T C^2c, with ||c||=1 and 0<C<I.
Then 0<m0<s. Given any m_star in [m0,s), put

    tau=(m_star-m0)/(s-m0),
    S_tau = [[C, sqrt(tau C H)],
             [sqrt(tau C H), H]],
    W = [I;0], v=Wc.                                  (7)

Diagonalize C orthogonally. For each eigenvalue lambda in (0,1), the
corresponding two by two block has trace 1 and determinant
(1-tau)lambda(1-lambda)>0. Both its eigenvalues therefore lie in (0,1).
Thus 0<S_tau<I, its compression is C, and

    v^T S_tau^2 v = m0+tau(s-m0)=m_star.

The finite square source M=(S_tau^(-1)-I)^(1/2) realizes it with
n=p=2k. This construction is an elementary contraction dilation, an
established ingredient rather than a separate novelty claim.

## 4. Lower endpoint: existence and interior attainment

Use eta=t>=t0, a=1+eta, kappa=E+E/eta-eta<=0, B=aI+kappa C.
The lower scalar function is l(eta)=c^T C B^(-1)c. It is positive,
continuous, and tends to zero as eta tends to infinity because I-C>0.
Its maximum is attained at a finite eta>=t0.

At an interior maximizer choose S=C, M=(C^(-1)-I)^(1/2), W=I, v=c,
and define

    z=B^(-1)c, w=Cz, x=M^T w,
    m=||w||^2=z^T C^2z, q=||x||^2=z^T C H z.

Both m,q are strictly positive. Differentiating the scalar function gives

    l'(eta) = -q+(E/eta^2)m = 0,
    e sqrt(m/q) = eta.                                (8)

Take N=M+e(w/||w||)(x/||x||)^T. This edit has operator norm e.
Directly, N^T w=(1+eta)x=a x and

    (I+NN^T)w
      = w+a[(I-C)z+e sqrt(q/m) C z]
      = a z+[1-a+aE/eta] C z
      = (aI+kappa C)z=c.                              (9)

Consequently w=S_N c and F(N;c)=c^T w=l(eta). There is no minimax
interchange in this attainment check.

## 5. Lower left endpoint

Let h=t0, so E=h^2/(1+h). At eta=h, B=(1+h)I and l(h)=s/(1+h).
A maximum at the left endpoint has right derivative <=0. Substituting
z=c/(1+h) into (8)'s derivative formula implies

    m0 <= m_star=s(1+h)/(2+h),
    q_star=s-m_star=s/(2+h).

Use (7) for this m_star. With w0=S_tau v and x0=M^T w0 we have
||w0||^2=m_star and ||x0||^2=q_star. Choose
N=M+e(w0/||w0||)(x0/||x0||)^T. Now

    e sqrt(m_star/q_star)=h,
    e sqrt(q_star/m_star)=h/(1+h).

Using Mx0=v-w0 gives (I+NN^T)w0=(1+h)v. Thus
F(N;v)=v^T w0/(1+h)=s/(1+h), attaining the lower endpoint.
Derivative equality and tau=0 are allowed; tau is always strictly below 1.

## 6. Upper endpoint: compact parameter and interior attainment

Reparameterize t=E(1+eta)/eta. This maps 0<eta<=h onto t>=h.
Put a=1+eta, kappa=E+E/eta-eta>=0, B=aI+kappa C, b=a+kappa.
Elementary substitution in (3) gives

    g(eta)=c^T U_t(C)c
          =a-a^2 c^T H B^(-1)c
          =a b c^T C B^(-1)c.                         (10)

Set g(0)=1. Since C>0 this is the continuous limit at zero, so a
minimum exists on the compact interval [0,h]. For a positive interior
minimizer take the canonical S=C, M=(C^(-1)-I)^(1/2), W=I and

    z=a B^(-1)c, w=Cz, x=M^T w, r=c-Mx=c-Hz,
    q=||x||^2=z^T C H z,
    A=||r||^2+q.

The optimized quadratic representation is

    g(eta)=min_z [a(1-2c^T Hz+z^T Hz)+kappa z^T C H z].

Its unique minimizer is the displayed z since H>0 and B>0 commute.
Differentiate at that minimizer (or differentiate (10) and substitute z):

    0=g'(eta)=A-(1+E/eta^2)q,
    ||r||^2=E q/eta^2.                                (11)

Here q>0 and r=(b/a)w, so r is nonzero. Set
N=M-e(r/||r||)(x/||x||)^T. Then r_new=c-Nx=a r=b w.
Equation (11) gives e sqrt(m/q)=E a/(eta b), where m=||w||^2.
The normal equation is now checked explicitly:

    N^T r_new = b[1-e sqrt(m/q)]x
              = [b-Ea/eta]x=x.                       (12)

The final equality uses b=1+E+E/eta. Hence x is the unique minimizer
for N, and J_N(x)=(||r||+e||x||)^2+q=g(eta), by (11).
This proves finite attainment with n=p=k.

## 7. Upper positive endpoint

If the minimum is at eta=h, then kappa=0, z=c, A=s, q=s-m0.
The left derivative is <=0, giving

    m0 <= m_star=s/(2+h),
    q_star=s-m_star=s(1+h)/(2+h).

Use (7) for this second moment, with w=S_tau v and x=M^T w.
The old residual is w. Choose N=M-e(w/||w||)(x/||x||)^T. The new
residual is (1+h)w because e sqrt(q_star/m_star)=h. Moreover

    N^T[(1+h)w]
      =(1+h)[1-e sqrt(m_star/q_star)]x=x,

as e sqrt(m_star/q_star)=h/(1+h). Thus x is its new optimizer and

    F(N;v)=(1+h)^2 m_star+q_star=(1+h)s=g(h).

Again equality in the derivative condition causes no exception.

## 8. Upper zero endpoint

Expansion of (10) at zero gives

    g(eta)=1+eta[1-c^T(C^(-1)-I)c/E]+O(eta^2).

A minimum at zero requires r0=c^T(C^(-1)-I)c<=E. For the canonical
M=(C^(-1)-I)^(1/2), take N=M-c(M^T c)^T. Since ||c||=1,
||N-M||op=sqrt(r0)<=e and N^T c=0. The new minimizer is x=0,
so F(N;c)=1=g(0). No infinite matrix or singular old source is required.

## 9. What this reconstruction establishes and leaves open

Equations (5) and the finite constructions in sections 4–8 jointly support
the claimed exact scalar endpoints for all 0<C<I, e>0 and unit c. Each
endpoint has a source with n=p in {k,2k}; different endpoints can require
different sources. The argument neither fixes an original full M nor
restricts the ambient dimensions in advance. All t optimization is scalar,
and proof validity is distinct from computational construction of a certified
minimizer. E=0 simply returns c^T Cc, outside the positive-edit theorem.

This removes the need for the developmental gradient/minimax shorthand in
the s16 attainment notes. It does not establish novelty, empirical usefulness,
the soundness of a particular parser, or any optional extension. Subsequent
focused checks must challenge algebraic identities and the implementation
contract without treating numerical matches as proof of these universal claims.

## Focused development checks

An additional elementary consequence is that every value between the two
endpoints is attainable, not only the endpoints. Express both constructed
witnesses in dimension2k with W=[I;0]; pad a k-dimensional canonical
witness using an unused identity source block and zero edit. Both old
resolvents S0,S1 are then strictly between0 and I with the same compression C.
For0<=theta<=1, set S_theta=(1-theta)S0+theta*S1,
M_theta=(S_theta^(-1)-I)^(1/2), and interpolate the two displayed edits
linearly. Their norm remains at most e. The resulting edited value is
continuous in theta and has the two sharp endpoint values at its ends.
The intermediate value theorem fills the interval. This is a finite
realization argument, not a probabilistic mixture of different sources.
It strengthens the information interpretation without adding a new
promotion prerequisite or claiming novelty for the path argument.

[endpoint_check.py](endpoint_check.py) and its [exact record](endpoint_result.json)
cover eight branch examples: both interior endpoints, derivative equality at
each cap, upper cancellation with both slack and tight budget, and two
non-eigenvector k=2 cap cases requiring hidden coordinates. The latter use
rational 4-by-4 S and calculate the edited Gram matrix exactly, avoiding
floating square roots of M=(S^(-1)-I)^(1/2). Both its new normal equation and
the inverse quadratic value agree exactly. The source and edit realization
still rest on the proof above. Runtime was 4,718,300 ns on Python 3.12.14.
These finite branch checks passed; they are not independent confirmation.
