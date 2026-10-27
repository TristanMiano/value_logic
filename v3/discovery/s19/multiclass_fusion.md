# A late multiclass extension of the overlapping-marginal screen

Codex (GPT-6), October26,2026. DEVELOPMENT derivation; compare immediately,
before implementing. Binary tractability was parked against Eban et al.

Let there be K labels and a supplied junction tree of observed feature
cliques. For label theta, the known weighted clique masses M_theta,C have
total mass p_theta and agree on separators. Sum_theta p_theta=1. Nature
may choose any full class-conditional distributions with these marginals;
conditional independence is NOT imposed on Nature. Prediction may randomize.

For every nonempty label subset A and clique C introduce a nonnegative
table R_A,C. Require separator consistency separately for each A, and

    sum_(A containing theta) R_A,C = M_theta,C.

Write r_A for the common total mass of R_A,C. The proposed exact LP is

    minimize sum_A r_A.                              (MF1)

Its value is the smallest compatible Bayes correct-classification
probability; one minus it is worst Bayes error and, by finite minimax,
the robust randomized classification error. It uses2^K-1 tables per
clique, so fixed K and bounded supplied clique width give polynomial
table size. No polynomial-in-K or automatic narrow-tree construction
claim is made, and a compact executable prediction policy is separate.

For any full class masses M_theta(y), sort their distinct positive levels
at each y. The layer-cake decomposition gives nonnegative R_A(y) such
that M_theta(y)=sum_(A containing theta)R_A(y) and
sum_A R_A(y)=max_theta M_theta(y). Their clique marginals are feasible
for(MF1), with objective equal to Bayes correct probability.

Conversely, extend every feasible R_A,C separately to a full submeasure
R_A by the junction-tree extension. Set M_theta=sum_(A containing theta)R_A.
These class masses have the required marginals and satisfy pointwise
max_theta M_theta<=sum_A R_A. Thus their Bayes correct probability is at
most the LP objective. The two directions prove equality at the optima.
Zero-mass components use the zero measure. Binary K=2 recovers the
common-submeasure construction in overlap_fusion.md.

## Arbitrary finite loss menus: same polyhedral mechanism

For loss vectors L_a in R^K, the unnormalized Bayes risk is
b(m)=min_a L_a dot m for m>=0. Its finitely many decision cones are
polyhedral. Enumerate the extreme rays of each nonzero cone, normalizing
each ray v to sum_theta v_theta=1. For every ray introduce a consistent
family of clique submeasures R_v,C, impose
sum_v v_theta*R_v,C=M_theta,C, and maximize sum_v b(v)*r_v.

Every density vector decomposes within a minimizing-action cone into its
extreme rays, where b is linear. This gives a feasible table objective
equal to its Bayes risk. Conversely, independent extensions of the ray
submeasures produce compatible class masses; concavity and homogeneity
give b(sum_v v R_v)>=sum_v b(v)R_v pointwise. Hence the LP is exact.
Ray enumeration and its output can be expensive. This is a finite
polyhedral reformulation, not a general efficient arbitrary-menu theorem.

## Immediate comparison and disposition

Mazuelas, Romero and Grunwald, *Minimax Risk Classifiers with 0-1 Loss*,
[JMLR24(208),2023](https://jmlr.org/papers/volume24/22-0339/22-0339.pdf),
Theorem2 and AppendixB give the exact moment-constrained minimax problem.
Their feature map can consist of indicators of each clique configuration
and label; set confidence widths to zero. This is precisely the present
marginal uncertainty set, without imposing an empirical full-feature
marginal. Finite nonempty support satisfies their regularity condition R1.

Our specialization of their formula is immediate. Write the clique scores
as s_C(y_C,theta). For a fixed nonempty label subset A, their dual constraint
is

    max_y sum_C sum_(theta in A) s_C(y_C,theta) <= 1 + |A|*nu.

The left side is ordinary additive junction-tree maximization. Enumerating
the2^K-1 subsets and using tree messages gives polynomial separation in
the supplied table size for fixed K. The standard message inequalities
also give a finite extended LP. Thus (MF1)'s polynomial fixed-K/width
tractability is already available from that result and tree inference.
The layer-cake proof is a useful primal reconstruction, not evidence of
a distinct contribution. Their rule also supplies the prediction policy
that the new primal-only construction left open.

**PARK** the standalone multiclass novelty claim before implementation.
Retain this derivation as a comparison/control. The arbitrary-loss ray
variant remains a polyhedral reformulation, not an assessed novelty claim;
the paper explicitly points to earlier general-loss minimax work. No new
numerical readiness, experiments, or improvement metric is warranted.
