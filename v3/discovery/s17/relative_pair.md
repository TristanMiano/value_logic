# A universal relative bound for two edits of one source

**Later disposition:** [pair_exact.md](pair_exact.md) and
[pair_radius.md](pair_radius.md) give a stronger exact ordinary analytic
comparison, with a scalar extremizer for every radius. The coefficient
advantage below is superseded, not the validity of this preserved certificate.

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; separate exploratory
candidate N17-P/v0. This is not part of N16-C/v1's event or readiness.
The proof uses conventional Gram interpolation and rational SDP dual
certificates. Its novelty has not been assessed against the closest prior
resolvent-diameter results.

For any finite real M, any v, and N_i=M+Delta_i with ||Delta_i||op<=1,
write F(A;v)=v^T(I+AA^T)^(-1)v. The exact certificate below proves

    |F(N_0;v)-F(N_1;v)|
      <= (4319301263/2000000000)*F(M;v)
       < (54/25)*F(M;v)  when v != 0.                 (R1)

The first coefficient is **2.1596506315**. A finite scalar example gives
ratio **2.1596431434**, so the optimal universal coefficient lies in this
interval of width less than 0.0000075. No exact optimizer or exact radical
formula is asserted. For v=0 both sides of the non-strict inequality are zero.

Since R1 holds for every v, it also gives both Loewner inequalities

    -g*(I+MM^T)^(-1)
      <= (I+N_0 N_0^T)^(-1)-(I+N_1 N_1^T)^(-1)
      <= g*(I+MM^T)^(-1),   g=4319301263/2000000000.

There is no unit-target assumption or retained block in this statement.
The regularization coefficient and edit radii are both one. Rescaling
those quantities into a different relative budget requires a separate
statement; this certificate does not cover arbitrary radii by substitution.

## Exact certificate independent of target normalization

Let w=(I+MM^T)^(-1)v, b=M^T w, and s=v^T w=||w||^2+||b||^2.
For i=0,1 put r_i=(I+N_i N_i^T)^(-1)v, x_i=N_i^T r_i,
u_i=Delta_i x_i, z_i=Delta_i^T r_i, and f_i=v^T r_i.
Use the Gram matrices of output vectors [v,w,r_0,u_0,r_1,u_1] and input
vectors [b,x_0,z_0,x_1,z_1]. The exact constraints are those of
[paired_values.md](paired_values.md), with old value s and an unrestricted
||v||^2. They follow from the actual normal equations and norm budgets.

The [certificate script](relative_pair.py) rebuilds each linear constraint
and the objective exactly. It uses the earlier numerical dual only to
propose rational coefficients y_0,...,y_16. Three exact projections,

    y_1=-y_3-y_8,
    y_4=1-y_13-y_14,
    y_9=-1-y_15-y_16,

and y_0=0 make the entire v row/column of the output slack identically
zero. Thus no bound on ||v|| is used. The resulting unshifted constant is
B=107982531/50000000 times s. In the script's documented constraint order,
the slack identity is

    B*s-(f_0-f_1)=<S_G,G_without_v>+<S_H,H>-sum(mu_j*g_j),

where every g_j<=0 is a norm constraint and each mu_j>=0. The rational
5-by-5 matrices S_G,S_H and all multipliers are in
[relative_pair_result.json](relative_pair_result.json). Exact Schur pivots
prove S_G+delta I>0 and S_H+delta I>0 for delta=10^(-9).
The script also records all seven predetermined shift screens, not just
the first passing choice. All passed; no failed numerical run was hidden.

The trace correction is bounded independently of the target norm:

    tr(G_without_v)+tr(H)
      <= s+2*(f_0+f_1)
      <= [1+4*a(1)]*s < (23/2)*s,
    a(1)=(3+sqrt(5))/2 <21/8.

The second inequality uses the ordinary graph-shear transfer bound
f_i<=a(1)*s from [geometry.md](geometry.md), valid for arbitrary v.
Therefore f_0-f_1 <= [B+(23/2)*10^(-9)]*s, exactly the coefficient in
R1. Interchanging the two edits proves the absolute-value statement.
This proof needs neither numerical strong duality nor a claim that every
abstract Gram point is realized by a source.

The rational verification ran in 1,362,600 ns on Python 3.12.14. This is
certificate verification time for this construction, not a comparison to
another algorithm. The script and numerical-proposal dependency are hashed.

## Finite lower witness and strong comparison

Take scalar M=[a], N_0=[a-1], N_1=[a+1], v=1, a=63/40. Both edits
have norm one and

    [F(N_0;1)-F(N_1;1)]/F(M;1)
       =4*a*(1+a^2)/(a^4+4)=2.1596431434... .

This exact rational witness provides the lower end of the stated enclosure.
It does not rely on a limiting hidden source or extrapolation from a grid.

Subtracting separate sharp multiplicative bounds gives sqrt(5)*s,
approximately 2.236068*s. A stronger ordinary comparison also uses
||N_0-N_1||<=2 and f_0<=a(2)*f_1. It gives

    |f_0-f_1| <= (3+sqrt(5))*(sqrt(2)-1)*s,

approximately **2.16885037*s**. R1 improves this stronger coefficient by
about **0.4242%**, not by the larger percentage against separate bounds.
The convenient rounded 2.16 coefficient improves it by about 0.4081%.
These percentages concern a worst-case relative contrast bound; they are
not audit fees, arithmetic work or measured wall-time savings.

A subsequent [primal/dual reuse comparison](pair_control.md) strengthens
the ordinary coefficient again to 2.1668350851. Against that control the
improvement is about **0.33156%**. Use this smaller comparison when reporting
the present candidate; the 0.4242% figure above is a preserved weaker scope.

For s=1/10, R1 supplies an upper contrast below 0.215966, and the scalar
witness mechanism is consistent with the earlier near-attainment example.
The old exact certificate for that special s remains preserved. The new
statement's contribution is its universal relative scope and explicit
near-optimal enclosure, not another decimal improvement on that one case.

The obvious next cheap screen is a close comparison with existing relative
resolvent perturbation and diameter inequalities. An analytic optimal
coefficient, other radii or a full block contrast formula are optional
extensions, not prerequisites to the validity of R1. Ordinary interpolation
and SDP certificates already explain the method. Keep this as a separate
candidate until its possible mathematical delta has been assessed.
