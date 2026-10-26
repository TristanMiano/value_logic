# Relative-error demonstrations with an unknown objective

Codex (GPT-6), DEVELOPMENT, s18. Early branch suggested by Lindner et al.2024
Appendix C. That source treats optimal demonstrations and unknown linear
rewards. This note reconstructs a bounded approximate variant; novelty is
unassessed. All guarantees are conditional on the performance premise below,
not on a fallible predictor's unsupported claim to have optimized well.

## Contract and exact compatibility test

Known points x_0,...,x_m are feasible for an unknown convex set F. Focus on
one point x_i, accompanied by a truthful statement: for some unknown linear
reward r, its regret over F is at most tau times its demonstrated advantage,

    sup_(x in F) r.(x-x_i) <= tau*Delta(r),
    Delta(r)=max_j r.(x_i-x_j)>0, tau>=0.                      (D1)

This ratio is invariant under positive reward rescaling and additive reward
constants. It is a substantive approximate-performance premise. Merely being
feasible does not imply it. Put q_j=x_i-x_j, L=span{q_j}, d=dim L>0. Work in
L, quotienting out reward directions orthogonal to all demonstrated contrasts.
Normalization Delta=1 leaves the finite union of compact polytopes

    H = union_j H_j,
    H_j={r in L: -tau<=r.q_k<=1 for every k, r.q_j=1}.          (D2)

Assume H is nonempty; otherwise the original demonstrations already refute
(D1). Compactness follows because the q_k span L and all their projections
are bounded. Let a proposed additional feasible point be y.

If y-x_i lies outside L, it is compatible with(D1): an unconstrained reward
component in L-perp can make r.(y-x_i) arbitrarily negative. If y-x_i is in L,
it is compatible exactly when

    min_(r in H) r.(y-x_i) <= tau.                            (D3)

Necessity follows from(D1). For sufficiency choose a minimizing r and set
F=conv{x_0,...,x_m,y}; its linear reward maximum occurs at one of these
points, each satisfying the normalized regret bound. Thus the maximal region
that this one demonstration certifies as infeasible is

    U_i={x_i+v: v in L, min_(r in H) r.v>tau}.                 (D4)

This is an intersection of strict halfspaces, hence relatively open and
convex in L. It is exactly computable from the vertices of the H_j, or by
one ordinary linear program per nonempty H_j for each proposed action.
No generic inverse-optimization or LP algorithm novelty is claimed.
For several independently unknown objectives with the same type of premise,
a new point is compatible iff it passes every demonstration's test. Their
guaranteed-unsafe regions combine by union. The common minimal compatible
F is still the hull of all original points plus y.

## A dimension-dependent threshold for nontrivial exclusion

If H is nonempty and tau<1/d, then U_i is nonempty. To prove this, suppose
0 belongs to conv(H). Caratheodory gives a positive convex combination of
k<=d+1 vectors r_l in H with sum_l lambda_l*r_l=0. For each l choose an
active contrast q_(j_l) with r_l.q_(j_l)=1. Every other r_h satisfies
r_h.q_(j_l)>=-tau. Therefore

    0 >= lambda_l - tau*(1-lambda_l),
    lambda_l <= tau/(1+tau).

Some lambda_l>=1/k>=1/(d+1), implying tau>=1/d, a contradiction. Hence0 is
outside the compact convex set conv(H). Strict separation supplies a v with
min_H r.v>0, and scaling v makes this minimum exceed tau. This proves the
claim. The conclusion concerns an unrestricted counterfactual action space;
if the actual available actions are bounded, the resulting ray may leave it.

The threshold is sharp as a uniform guarantee. In R^d let x_i=0 and choose
d+1 known feasible contrasts q_1,...,q_(d+1) forming a simplex around0 with
sum q_j=0. For each l there is a reward r_l with

    r_l.q_l=1, r_l.q_j=-1/d for j!=l.

The r_l also sum to0. At tau=1/d they belong to H, so min_H r.v<=0 for every
v and U_i is empty. For any larger tau the same obstruction remains. For
smaller tau this particular data set makes H empty, since after one contrast
reaches1 the remaining d must sum to-1. This distinguishes inconsistency of
the premise from a consistent premise that excludes no new points.

## Rational examples and elementary certificates

In two dimensions take q_1=(1,0), q_2=(0,1), q_3=(-1,-1). At tau=1/2 the
normalized reward set consists exactly of (1,-1/2),(-1/2,1),(-1/2,-1/2).
Their average is0; the exact unsafe region is empty. These are rational
sharpness witnesses, not a floating geometric picture.

An explicit sufficient exclusion certificate avoids solving every LP. If

    y-x_i=sum_j alpha_j*q_j, alpha_j>=0,

then, writing alpha_min=min_j alpha_j, every r in H has

    r.(y-x_i) >= (1+tau)*alpha_min - tau*sum_j alpha_j.         (D5)

Indeed at least one contrast is1, and all the others are at least-tau.
Thus a right side greater than tau proves y infeasible. Include only genuine
nonzero catalogue contrasts and remember that any of them may be the active
one; dropping possible active contrasts without another warrant is unsound.
At tau=0 this recovers the positive-coefficient unsafe-cone argument of the
exact-demonstration source. The LP test is generally stronger than(D5).

For a one-dimensional numerical example, known feasible points include-1,
4/5 and1, with demonstrated point x_i=4/5. The positive reward orientation
has normalized advantage9/5 and observed shortfall1/5, ratio1/9. If
1/9<=tau<9, only this orientation is compatible. Then the exact unsafe set
is y>4/5+(9/5)*tau. At tau=1/5 it excludes y>29/25. This uses approximate
optimality of an interior observed point, not exact optimality of a vertex.

## Early screen and remaining duties

Compare against approximate inverse optimization, revealed-preference
polyhedra and the full approximate-demonstration results of CoCoRL before
considering a contribution event. The potentially useful increment is the
scale-free compatibility test plus the sharp1/d threshold, not the basic
separating-hyperplane method. No source fee, data-learning guarantee, safe
action construction or independent proof confirmation is established here.

## Stronger ordinary control: Minkowski asymmetry gives the threshold

The early source screen found a direct classical explanation. Let
Q=conv{q_j}, and let c be a Minkowski center of Q with asymmetry s, so

    Q-c subset -s*(Q-c),  1<=s<=d.

For r in H, the support inequality gives

    1-r.c <= s*(h_Q(-r)+r.c) <= s*(tau+r.c),
    r.c >= (1-s*tau)/(s+1).                                  (D6)

Thus if tau<1/s, the explicit point y=x_i+t*c is guaranteed infeasible for

    t > tau*(s+1)/(1-s*tau).                                 (D7)

The earlier1/d statement follows immediately from the established s<=d bound.
It must not be advertised as a new geometric threshold. For an original
demonstration hull P with Minkowski center z, c=x_i-z; the excluded ray points
away from that center. If available actions are restricted, intersect the
ray with that action set before asserting a useful decision consequence.
The exact polyhedral test(D3) can still be tighter than this sufficient ray.

Full optimal computation of the center is unnecessary for soundness. Any
checked reflection containment Q-c subset -kappa*(Q-c) yields the same
formulas with kappa in place of s. For a finite vertex list, a model can propose
c,kappa and a convex representation of each reflected/rescaled vertex in Q.
Nonnegative weights summing to1 and the stated vector equalities give a finite
ordinary certificate. A poor proposal weakens the ray or fails verification;
it never licenses an unwarranted inference about the unknown reward.

This is a promising bounded *application* of existing convex geometry to a
relative-performance information contract. A useful, moderately novel claim
would have to distinguish that synthesis from established approximate inverse
optimization. The basic ratio normalization, robust feasibility test, center
LP and dimension bound are all ordinary tools and receive full credit here.

## Prospective bounded check

Before execution: enumerate exact rational vertices of the planar normalized
reward faces for three cases: the sharp triangle at tau=1/2 and just below;
a translated triangle with an interior demonstration and tau=1/4; and a
centrally symmetric diamond at tau=1 and just below. Verify the exact empty/
nonempty distinctions, the proposed safe-to-reject ray, and affine covariance
under one nonsingular rational coordinate change. Check the one-dimensional
threshold29/25 separately. Use ordinary vertex enumeration as the control,
not sampling or a claimed novel solver. This is a finite arithmetic probe,
not independent proof confirmation, a general grid or measured query savings.

[The rational probe](demo_check.py) passed once; [result](demo_result.json).
It tested116 line pairs with31 feasible intersections (including duplicates),
and the interior-demo example has worst normalized proposed-action advantage
13/28>1/4. The sharp triangle and symmetric examples, inconsistent smaller
error levels, one-dimensional boundary and affine covariance all agree.
Python3.12.14;1,493,300ns execution; source SHA256
f5de72165006461d75b7879bc880d7af4c548eed7b0b638d076bfbab5b30f8e9.
The same-model exact calculation supports the small examples only.
