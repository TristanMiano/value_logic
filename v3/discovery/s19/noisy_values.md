# Finite-precision optimum receipts and stable value gaps

Codex (GPT-6), October26,2026. DEVELOPMENT. Ordinary polyhedral error bounds
are imported explicitly; the proposed consequence concerns the retained
conditional-value construction, not a new sensitivity theorem.

## Interval receipts preserve the subset mechanism

Suppose old minimum j is known only to lie in [a_j,b_j]. Every generator
satisfies h_j*x_i>=a_j and at least one satisfies h_j*x_i<=b_j. For a subset
T assigned to generator i, replace the old face by the convex slice

    Q_i(T)=B_i intersect {h_j*x>=a_j for all j}
                     intersect {h_j*x<=b_j for j in T}.

Assign one upper witness per receipt. All the earlier endpoint, full-value,
band and pair-contrast constructions apply with these slices: their proofs
need independent convex regions and the finite witness partition, not
literal equality. The same LP counts and subset recurrences follow. Shared
noise correlations or a globally coupled calibration parameter are extra
constraints and cannot simply be dropped. Empty intersections remain an
inconsistency status. Exact receipts are the special case a_j=b_j.

## Local Hausdorff control, with a real branch margin

Fix a consistent exact receipt vector v and expand it uniformly to
[v_j-epsilon,v_j+epsilon]. Write F_epsilon for compatible generator tuples
and V_epsilon for the possible new linear minima. Compactness gives nested
compact sets and V_0 subset V_epsilon. It alone gives convergence as epsilon
shrinks, but no numerical rate.

For each i,T with Q_i^0(T) empty, solve the LP that minimizes epsilon>=0
subject to membership in Q_i^epsilon(T). Its optimum eta_iT is strictly
positive: otherwise compactness of B_i would produce an exact feasible
point. Let eta be the minimum of these positive margins, or infinity if
there are no empty exact slices. There are only n*2^k such slice types.
For 0<=epsilon<eta, every available approximate slice was already feasible
at zero. This restriction prevents silently creating a new witness branch.

For each nonempty exact slice, use a valid Hoffman bound relative to B_i:
any x in its epsilon-relaxation is within H_iT*epsilon of some point in the
exact slice. Use infinity norms for residual and point distance. This is the
classical linear-inequality error bound, or its relative-polyhedron form;
computing a useful upper bound H_iT can be expensive and is not free.
For the new objective h define L=max_(i,T nonempty) ||h||_1*H_iT.
Choose a witness partition for any approximate source and repair each
generator inside its assigned exact slice. Independence combines the repairs
into a source in F_0. Its new minimum differs by at most L*epsilon. Hence

    V_0 subset V_epsilon,
    Hausdorff(V_epsilon,V_0) <= L*epsilon   for epsilon<eta. (N1)

Independent affine edits replace ||h||_1 with the appropriate norm of the
composed linear row at each generator. Pair contrasts use the sum of the
two corresponding Lipschitz bounds. In particular an exact forbidden-value
margin delta at a scalar q remains at least delta-L*epsilon when positive.
No universal well-conditioned constant is claimed; near-degenerate geometry
can make both the useful margin and the error bound unfavorable.

## A gap that survives nonzero precision

Use x=(2t,1-t), y=(s,2-2s), t,s in[0,1], and retain both coordinate minima
in[0,epsilon]. The conditions are

    (t<=epsilon/2 OR s<=epsilon)
    AND (t>=1-epsilon OR s>=1-epsilon/2).

For epsilon<2/3 the same-generator combinations are impossible. The two
remaining rectangles give the exact new minimum of x-coordinate plus
y-coordinate as

    V_epsilon=[1,1+epsilon/2] union [2-epsilon,2].      (N2)

At epsilon=2/3 the intervals touch; for larger epsilon the entire[1,2]
is attainable. The global value range can never exceed[1,2]. Thus a later
division by V-3/2 has a guaranteed denominator margin1/2-epsilon exactly
when epsilon<1/2. Its reciprocal magnitude is bounded by1/(1/2-epsilon).
At epsilon=1/10 this is5/2. Separate endpoint retention stays[1,2] for every
epsilon and cannot certify any positive denominator margin. The ordinary
exact disjunctive calculation ties(N2); this is an information-retention
consequence, not an executed computation or fee saving.

This example avoids an exact-equality-only advantage. It also shows why a
full output gap and safety at one chosen denominator are distinct: the gap
lasts to2/3, but3/2 enters the upper component already at1/2. A decision-
specific band query can stop before constructing the entire interval union.
