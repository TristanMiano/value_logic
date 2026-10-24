# A whole target-response matrix can improve the counterfactual certificate

Codex (GPT-6), October 23, 2026. DEVELOPMENT, same-model derivation.
This extends [projected receipts](projected_receipts.md) beyond reducing all
of C to one lower moment. Robust least squares and quadratic certificates
are prior machinery. No generic optimizer novelty or economic gain is claimed.

Let S=(I+MM^T)^(-1), W^T W=I, C=W^T S W, v=Wc, ||c||=1,
0<C<=I, and ||N-M||op<=e. Write E=e^2 and H=I-C. For any coordinate
vector z, the virtual old primal vector x=M^T S Wz has

    A=||c||^2-2*c^T H z+z^T H z = ||v-Mx||^2+||x||^2,
    q=||x||^2=z^T(C-D)z,  D=W^T S^2 W,
    0<=q<=Q=z^T C H z<=A.                                (1)

The matrix inequalities C^2<=D<=C follow from orthogonal projection
and 0<S<=I. In particular A-Q=||H z-c||^2. Although x is not retained,
its existence gives a feasible primal upper bound for every compatible M:

    F(N;v)<=A+2*e*sqrt(q*(A-q))+E*q.

Choose any eta>0 with eta^2<=E*(1+eta), and put
kappa=E+E/eta-eta>=0. Young's inequality gives the fully checkable bound

    F(N;v)<=(1+eta)*A+kappa*Q.                            (2)

Every term on the right is computed from retained C,c and chosen eta,z.
It is a bound for the original full-dimensional problem, not an assumption
that S leaves span(W) invariant. Any feasible choice suffices; minimizing
the bound is optional paid computation. For E=0 the old value is c^T C c.

## Optimize the virtual primal vector once the witness eta is chosen

Let a=1+eta and B=a*I+kappa*C, which is positive definite. The minimum
of (2) over z is attained at z=a*B^(-1)c, including singular H. Thus

    G_eta(C,c)=a-a^2*c^T H*B^(-1)c
             =c^T [a*(1+E+E/eta)*C*B^(-1)] c.           (3)

The second expression means a rational matrix function, not application
of the sharp scalar envelope separately to eigenvalues. A COMMON eta
must be used for the whole matrix. Independent spectral substitution
was refuted in projected_receipts.md. Taking the minimum of (3) over

    0<eta<=eta_max=(E+sqrt(E^2+4*E))/2

gives a valid bound, with limiting eta=0 supplying the trivial upper1.
For a rational threshold receipt, one rational eta and z in (2) avoid
both scalar optimization and matrix inversion in the checker. Their
acquisition and bit complexity are still paid.

For fixed eta, the scalar matrix function in (3) is increasing and
concave on [0,1], because kappa>=0. Hence c^T g_eta(C)c<=g_eta(c^T Cc).
The extra target information therefore cannot weaken this bound relative
to using the corresponding one-dimensional compression. Strict spectral
spread can improve it. This is a scalar Jensen statement after diagonalizing
C, not a claimed Loewner inequality for the edited resolvent.

## Candidate sharpness argument and its different cases

The upper construction suggests a sharp dimension-unrestricted envelope,
not merely a numerical improvement. The following is still developmental.
Work first with 0<C<I, E>0 and nonzero c. A minimum exists after adding the
eta=0 limit. Write s=c^T Cc and m0=c^T C^2c.

* Interior eta: choose the finite source S=C, M=(C^(-1)-I)^(1/2).
  For the minimizing z in (3), q=Q. Differentiation of the optimized
  quadratic with respect to eta gives A=(1+E/eta^2)*Q, so
  eta=e*sqrt(Q)/sqrt(A-Q). Young's inequality is tight. The gradient in z
  is consequently the gradient of the robust primal objective
  (||v-Mx||+e||x||)^2+||x||^2. The map z to x is invertible under the
  strict spectral assumption. With r=v-Mx, take
  N=M-e*(r/||r||)*(x/||x||)^T. The new residual is
  (1+e||x||/||r||)r. Its least-squares stationarity is exactly that robust
  gradient equation, so x is the new global minimizer and (2) is attained.
  Here Q>0 and A-Q>0; otherwise the positive finite eta stationarity
  could not hold for v nonzero.

* Upper boundary eta_max: kappa=0 and z=c. A one-sided derivative at a
  minimizing upper endpoint gives Q>=s/(1+E/eta_max^2). Define
  q_star=s/(1+E/eta_max^2) and m_star=s-q_star. Thus m0<=m_star<s.
  Choose tau=(m_star-m0)/(s-m0) in[0,1). The positive contraction

      S_tau=[[C, sqrt(tau*C*(I-C))],
             [sqrt(tau*C*(I-C)), I-C]]

  has compression C and target second moment m_star for v=(c,0).
  Its eigenvalues are strictly between0 and1, so finite M exists.
  With w=S_tau*v and x=M^T*w, the rank-one edit
  N=M-e*(w/||w||)*(x/||x||)^T attains the bound: the stationarity condition
  reduces to q_star-m_star=e*sqrt(q_star*m_star), which follows from
  eta_max^2=E*(1+eta_max). The inherited scalar worst case is recovered,
  but its embedding respects the entire compression C.

* Lower boundary eta=0: expansion gives
  G_eta=1+eta*(1-c^T(C^(-1)-I)c/E)+O(eta^2).
  A minimum at0 requires ||M^T v||<=e for M=(C^(-1)-I)^(1/2).
  The edit N=M-v*(M^T v)^T has norm||M^T v|| and N^T v=0, so F(N;v)=1.

Cases with eigenvalue1 can be treated by restriction to its complement
and limits; until those boundary details are checked, the sharpness claim
is scoped to 0<C<I. The certificate (2) itself already covers C<=I.
No independent review or broad sharpness harness has occurred.

This acquisition contract retains k(k+1)/2 old quadratic values, not k
free solve vectors. O(k^2) receipt arithmetic may fit a retention budget
that excludes full old vectors; actual acquisition and later workload must
justify it. Ordinary robust least-squares and matrix-moment implementations
with the same information remain the direct controls.

The small [probe](matrix_probe.py) / [result](matrix_probe.json) passed25
numerical matching constructions:10 interior,8 upper-boundary and7 zero-
boundary cases. Directly inverted edited matrices agree within the stated
developmental tolerance. Separately, exact rational eta=211/5000 certifies
the worked example's upper867127945275459/1611861132384100<.538.
This is stronger than reducing C to the partial moment alone; the earlier
two-moment near-extremizer exceeds.5388 and cannot satisfy this whole C.
The numerical search is not independent confirmation or an exact certificate
of its minimizing eta. The selected rational witness itself is exact.

[The lower companion](matrix_lower.md) develops the dual half of the same
information contract, with a reversed sign restriction on kappa.
