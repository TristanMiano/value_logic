# Common uncertainty shapes, exact cores and a small-subset obstruction

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT, same-model.
This is a constructive continuation of [the value-only convex core](convex_core.md).
The general core is already the guaranteed/interior/invariant hull studied in
computational geometry. A new name would not be a contribution.

## A direct exact reduction

Suppose each contact/uncertainty region is B_i=a_i+C, with the same nonempty
compact convex C, and each unknown point x_i can independently be anywhere in
B_i. Let P=conv{a_i}. Then

    intersection_(x_i in B_i) conv{x_i} = P minus_Pontryagin (-C), (T1)

where P minus_Pontryagin D means{y:y+D subset P}. This is set erosion,
not the set of pairwise vector differences.

For any h, the smallest possible support of a selected hull is

    min_(x_i) max_i h.x_i = max_i h.a_i + min_(c in C) h.c
                         = h_P(h)-h_C(-h).

Consequently y belongs to all selected hulls iff
h.y+h_C(-h)<=h_P(h) for every h, precisely y-C subset P. If
P={y:H_j.y<=b_j}, this is the finite system

    H_j.y <= b_j-h_C(-H_j) for every original facet j.            (T2)

This is ordinary support arithmetic/Pontryagin difference. It avoids
enumerating independent uncertain point configurations after the central
polytope has been constructed. Hull construction and support evaluation are
still real work. It is not a new general robust optimization algorithm.

## Four rational squares

Take d=2, centers E=(1,0),N=(0,1),W=(-1,0),S=(0,-1), and
C=[-2/5,2/5]^2. These are four disjoint, full-dimensional compact convex
squares. P is the unit l1 ball. Its four facet normals have both components
equal to+/-1, so h_C(-H_j)=4/5. Equation(T2) gives the exact common core

    K = {y:|y_1|+|y_2|<=1/5}.                                  (T3)

Now omit S. For the triple E,N,W, every common point must obey

    -y_2 <= -2/5,
     y_1+y_2 <= 1/5,
    -y_1+y_2 <= 1/5.

The first inequality comes from the downward support direction; the others
from the two upward diagonals. Add the first inequality twice and each of
the others once:0<=-2/5, a contradiction. Thus this triple's guaranteed hull
is empty. Rotation proves the same for all four triples. Every smaller
subset also has empty guaranteed hull by monotonicity.

The whole set has a nonempty two-dimensional core, while the convex hull of
the union of all three-region cores is empty. All four receipts are jointly
useful; no fixed three-receipt core can replace them.

## Relation to one inspected prior claim

Lee and Abbas, [arXiv:2403.09009v1](https://arxiv.org/pdf/2403.09009v1),
Definition4.2, define this same intersection. Their Theorem4.5 asserts its
equality to the convex hull of the union of invariant hulls of all(d+1)-region
subsets. At d=2, (T3) and the empty-triple calculation contradict that stated
identity under disjoint convex square regions. The theorem's proof uses
Lemma4.3; here the core vertex(1/5,0) lies in the interior of the convex hull
of the E and W squares, contrary to that lemma's stated assertion.

This is a local counterexample to the inspected version, not a verdict on
every consensus result or another published version. Verify version context
and the finite arithmetic before relying on the objection. Do not contact
authors or represent this as independently confirmed.

Ordinary Caratheodory is not contradicted. For every actual configuration,
a point in its hull has a representation using at most d+1 actual points.
The selected subset can depend on the hidden configuration. A fixed small
subset whose hull contains the point under every configuration is a different
quantifier order. Combining small guaranteed cores does not generally repair
that exchange.

## Bounded exact check, specified before execution

For a polytope uncertainty region, checking every combination of its vertices
suffices for the entire guaranteed hull: in each support direction, every
individual minimum occurs at a vertex. Thus the four squares require256
corner configurations, and each triple requires64. Enumerate these512 total
configurations with rational arithmetic; compute each actual convex hull and
intersect the hulls. Check that the four-region intersection has exactly the
four vertices of(T3), and that each triple intersection is empty. Separately
check the three-inequality rational contradiction and the individual region
nonintersection/full-dimensional premises. Record source hash and execution
once; preserve a failure before versioning any repair. This is a finite
same-model check, not a proof audit of the cited paper or a general algorithm
benchmark. No sampled hidden configurations or floating-point tolerances.

The [executed rational check](core_check.py) passed all512 configurations:
[result](core_result.json). Python3.12.14,62,000,000ns measured runtime,
source SHA2563cc0f6241fc2f8ff3c8711eaea9afe85d74eeb7603ad958d1d2c9af68a82a92d.
The alternate six-page author-hosted PDF states the same disputed identity as
Theorem4.4. Its proof reference points to the arXiv preprint. This does not
establish the absence of an erratum or other versions.

The older sound comparator is particularly strong: Davari–Edalat–Lieutier2019
describe the established rectangular-region construction using2^d same-corner
hulls. Thus only four carefully selected hulls, not our exhaustive256, suffice
for the complete four-square core. Their pre-inner support expression also
supplies(T1) immediately when combined with ordinary Pontryagin difference.
The exhaustive check is developmental arithmetic evidence; it is not an
efficient new algorithm. See the [source scopes](literature.md).
