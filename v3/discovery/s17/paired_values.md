# A shared old source constrains two counterfactual values

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT. This is a separate
exploratory extension, not part of the N16-C/v1 contribution event or its
readiness estimate. It addresses comparison of two changes to one source.

Let N_i=M+Delta_i, ||Delta_i||<=e_i, v_i=Wc_i and
f_i=min_x ||v_i-N_i x||^2+||x||^2, for i=0,1. The old retained block is
C=W^T(I+MM^T)^(-1)W. Subtracting N16's sharp upper endpoint for f_0 and
sharp lower endpoint for f_1 is valid. It need not be sharp: the two endpoint
witnesses may require different M. Keeping the common source is meaningful
counterfactual information, not a different convention for probability.

## Exact conventional formulation and the new screen

Extend [the ordinary Gram formulation](gram_sdp.md) to output vectors
[W,R,r_0,u_0,r_1,u_1] and input vectors [X,x_0,z_0,x_1,z_1]. Impose the old
constraints and each edit's two-sided norm/interpolation constraints. In
addition require the four common-source cross identities

    r_i^T(v_j-r_j-u_j)=(x_i-z_i)^T x_j,  i,j in {0,1}.

They are the remaining entries of D^T B=F^T A for
A=[X,x_0,x_1], B=[W-R,v_0-r_0-u_0,v_1-r_1-u_1],
D=[R,r_0,r_1], F=[X,x_0-z_0,x_1-z_1]. Maximizing f_0-f_1 is again a
linear objective over two PSD Gram matrices. The established operator
interpolation theorem is the ordinary comparator; this is not a new SDP method.

The closed relaxation has the same supremum as the genuine source class.
For its nondegenerate points use the earlier simultaneous interpolation
construction for M, then complete Delta_0 and Delta_1 separately. For density,
take M=diag((C^(-1)-I)^(1/2),1,1), W=[I;0;0], and let Delta_i have only
epsilon*c_i in its own new input column, for 0<epsilon<min(e_0,e_1).
The two new residuals and optimizers have nonzero, distinct spare coordinates.
Thus [R,r_0,r_1] and [X,x_0,x_1] both have full column rank. A positive
convex mixture with these Gram matrices gives the required nondegeneracy;
letting its weight tend to zero proves the assertion. This assumes e_i>0
and unit c_i. No finite-attainment conclusion is made for the supremum.

[paired_probe.py](paired_probe.py) / [result](paired_result.json) screened
eight small cases. All met the prospective numerical feasibility/comparison
tolerances. For C=1/10, c_0=c_1=1 and e_0=e_1=1, separate subtraction is
sqrt(5)/10, approximately 0.22360680, whereas the paired SDP gives about
0.21596437. Interior and orthogonal-target controls agree with separate
subtraction to numerical tolerance. Solver values are not certificates.

## Exact enclosure for one shared-source decision

[paired_cert.py](paired_cert.py) / [result](paired_cert_result.json) converts
the first numerical dual into a rational certificate. It rebuilds every
constraint coefficient and the objective exactly. If y are its equality
multipliers and mu>=0 its inequality multipliers, the reconstructed matrices
S_G,S_H satisfy the identity

    B-(f_0-f_1) = <S_G,G>+<S_H,H>-sum(mu_j*g_j)

on the equality constraints, where g_j<=0 and
B=215964367/1000000000. Exact rational Schur pivots verify
S_G+10^(-6)I>0 and S_H+10^(-6)I>0. The conservative bounds
tr(G)<=51/10 and tr(H)<=41/10 follow from f_i=||r_i||^2+||x_i||^2<=1,
the two norm budgets and the old Gram identity. Therefore every genuine
compatible shared-source pair satisfies

    f_0-f_1 <= 215973567/1000000000 = 0.215973567 < 0.216.

The floating solver merely proposed the multipliers. Exact matrix positivity,
nonnegative norm multipliers, the displayed linear identity and trace bounds
prove this universal claim. They do not rely on numerical strong duality.
The certificate script's runtime was 1,002,800 ns, not a speedup measurement.

A genuine finite witness almost reaches it. Set a=63/40, L=1000,
lambda=1/(1+a^2), nu=1/(1+L^2), p=(1/10-nu)/(lambda-nu),
M=diag(a,L), W=(sqrt(p),sqrt(1-p))^T. Edits diag(-1,0) and diag(1,0)
have norm one and preserve the same old source. Its exact value difference is

    p*[1/(1+(a-1)^2)-1/(1+(a+1)^2)] > 0.2159,

approximately 0.2159629064. Thus the true supremum is enclosed tightly,
without asserting an exact analytic optimizer or attainment. The new .216
threshold is a development illustration selected after the numerical screen.

## A stronger ordinary control before reporting an improvement

Even separate scalar transfer bounds can exploit shared geometry. For the
same target, ||N_0-N_1||<=e_0+e_1. The earlier universal scalar ratio bound
gives f_0<=a(e_0+e_1)*f_1, where
a(e)=1+(e^2+sqrt(e^4+4e^2))/2. With upper and lower bounds U,L from the
old block, this implies

    f_0-f_1 <= U-max(L,U/a(e_0+e_1)).

To see this, for each f_0<=U the difference is at most
f_0-max(L,f_0/a), an increasing function of f_0. In the scalar example,
this improves the separate width to

    (3+sqrt(5))*(sqrt(2)-1)/10.

The paired SDP must be compared with this tighter three-source scalar
control too, not only with 0.22360680. Its further improvement is smaller.
Both controls are conventional deductions, and their costs depend on the
chosen arithmetic interface. No new audit-fee, runtime or acquisition gain
has been measured. The useful lesson is that sharp marginal intervals do
not automatically describe a jointly attainable counterfactual contrast.

An analytic formula for general C, targets and budgets remains unassessed.
The candidate is retained as a specific follow-on question; the exact SDP
and one small decision already settle this limited information comparison.
