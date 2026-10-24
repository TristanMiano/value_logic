# A sharp relative objective bound for reusing a ridge solution

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass31.
Same-model derivation. The proof uses classical compression/Kantorovich
inequalities; novelty of this particular deployment formulation is unassessed.

Let J_M(x)=||y-M^T x||^2+||x||^2, with optimum x_M and value r_M.
For N=M+D and ||D||op<=e, write E=e^2 and c=1+E/2. Then

    J_N(x_M) / r_N <= c^2 = (1+E/2)^2.             (1)

For y=0 both objectives are zero, and the un-divided inequality applies.
This requires no retained r_M or response matrix, only an exact old solution
and an edit warrant. It prices the relative objective cost of continued use,
not the change in the optimum's value or a posterior predictive risk ratio.

## Proof by a shear and inverse compression

Let V be the graph of M in R^(m+n), with orthonormal basis Q, and put

    L = [[I,0],[D,I]],       H=L^T L.

The old optimal residual vector v=(y-M^T x_M,x_M) is in V. The new residual
of the same x_M is L^(-T)v. The new minimum is its orthogonal projection
onto L V, since both vectors satisfy (I,N^T)w=y. Write v=Qz. Therefore

    J_N(x_M)=z^T B z,       r_N=z^T A^(-1)z,
    A=Q^T H Q,             B=Q^T H^(-1) Q.

Direct block multiplication gives

    H+H^(-1)=diag(2I+D^T D, 2I+D D^T) <= (2+E)I.

Consequently B<=2c I-A<=c^2 A^(-1); the second inequality is equivalent
to (A-cI)^2>=0. This proves (1), without a small-edit assumption.

The constant is attained: take M=I_2, D=e*[[0,-1],[1,0]] and nonzero y.
Then x_M=y/2, r_N=||y||^2/(2+E), and J_N(x_M)=(2+E)||y||^2/4.
Thus the relative excess E+E^2/4 cannot be uniformly decreased.

For e=.1, (1) is1.010025: at most1.0025% excess objective. This is a
conditional analytic guarantee, not measured computation saved. The edit
radius is in the whitened/regularized coordinates of this objective.

## An approximate old solution

Suppose a checked old relative gap is J_M(x)<= (1+delta)r_M. Define

    d=e*sqrt(1+E/4),       c=1+E/2,       c^2-d^2=1.

Then the following bound holds:

    J_N(x)/r_N <= [c*sqrt(1+delta)+d*sqrt(delta)]^2.   (2)

Let v=(y-M^T x,x), z=P_V v, q=v-z. Then ||z||^2=r_M and
||q||^2<=delta*r_M. The new minimum is P_(LV)L^(-T)v, so projection
onto the single vector Lz gives

    r_N >= ||z||^4/(z^T H z).

The spectrum of H lies in [c-d,c+d], and H^(-1)<=2cI-H. For unit u,w,
let rho=u^T w and H=cI+dK, ||K||<=1. Put a=u^T K u and b=w^T K w.
Then

    (u^T H u)(w^T H^(-1)w)
       <= (c+da)(c-db)
       = [c+d(a-b)/2]^2-d^2[(a+b)/2]^2
       <= [c+d*sqrt(1-rho^2)]^2.

The final step uses the two eigenvalues +/-sqrt(1-rho^2) of uu^T-ww^T,
so (a-b)/2<=sqrt(1-rho^2); the terms being squared are nonnegative.
Apply u=z/||z|| and w=v/||v||, with rho=||z||/||v||. This proves (2).
The e=0 case follows directly, without defining K. No sharpness claim for
the full approximate-solve interface is needed here.

A residual bound supplies the old relative gap without an exact optimum:
g_M=(I+MM^T)x-My and J_M(x)-r_M=g_M^T S_M g_M<=beta^2.
If J_M(x)>beta^2, delta=beta^2/[J_M(x)-beta^2] is conservative.
All objective/residual evaluations and lower-bound warrants are paid.

## Development screen and comparison duty

reuse_ratio_probe.py tested1200 seeded finite cases across five matrix shapes,
three edit radii and a broad range of source scales. No counterexample to
(1) was found; largest normalized excess was0.9999691441621441. The JSON
records source hash/runtime/versions and witnesses; stdout/stderr are retained.
The proof above, not this screen, supports the unrestricted mathematical claim.

The ratio is a natural stopping/reuse service: a reasoner can trade a checked
old solve gap and an edit radius against an explicit allowed loss. It makes
the computation-price interface more concrete. It does not by itself show
that acquiring the edit warrant is cheaper than solving again, nor that this
Kantorovich consequence is absent from the existing perturbation literature.
An ordinary implementation with these premises gives the identical bound.

## Exact finite sanity check

reuse_exact_probe.py checks1800 rational2-by-2 transport identities, mean
bounds and exact-solve reuse inequalities, including600 zero-data cases.
It also checks3600 approximate-solve inequalities by squaring only after
isolating a nonnegative radical term, plus three exact noncommuting equality
witnesses. All pass. The model-mixture counterexample has variance451/2>1.
The run takes443,545,100ns under Python3.12.14; JSON records the source hash.
This is a small same-model development check, not independent confirmation
or evidence of an end-to-end computational advantage.
