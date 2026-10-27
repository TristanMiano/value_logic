# A stronger forest property and its first topological obstruction

Codex (GPT-6), October26,2026. DEVELOPMENT derivation. Separate extension;
neither this topology nor its eventual priority assessment is required for
the AR1 full-range event.

## A consistent forest source is contractible

Strengthen the induction in forest_receipts.md. For a rooted configuration
subtree, construct a continuous contraction to a fixed feasible hub. If its
parent predicate can hold anywhere in that subtree, choose the hub to
satisfy it. Require the contraction to preserve that predicate whenever it
holds initially. The predicate is a convex condition on the root block.
The stronger induction also permits an extra convex restriction on that
root. A leaf contracts by a straight segment within its convex domain.

For a nonleaf, keep its root block fixed and contract every child subtree
to its previously chosen hub. A child that initially witnesses a receipt
continues to witness it by the preservation property. If the parent block
witnesses the receipt, it stays fixed during this phase. Thus all receipts
remain valid. At the end, every child capable of witnessing its parent
receipt does so, because its hub was chosen in that predicate.

The root can now move along a straight segment to a fixed hub point in its
convex feasible projection. Receipts with a capable child stay witnessed
by that child; every other receipt is one of the forced root halfspaces.
Choose the root hub in its own parent predicate if that intersection is
nonempty. Convexity then preserves the parent predicate for every starting
point satisfying it. This closes the induction. The hub consists of this
root point and the chosen child hubs, so both phases fix the hub itself.
Rescale the two phases to[0,1/2] and[1/2,1]; their agreement at the boundary
gives a continuous strong contraction. Finite products cover a forest.

This argument needs convex local domains/predicates and independent blocks;
it does not require the affine objective or polyhedral representation.
Those stronger computational hypotheses are still needed for the LP and
rational-certificate claims. Contractibility does not imply convexity.

## Conditioning gives a finite good cover

Use the same omitted-edge set D and the2^t closed branch domains from
forest_receipts.md. Any finite intersection of these branch domains still
has only forest-edge receipt disjunctions, plus the union of their imposed
local halfspaces. A receipt's forest disjunction remains required if any
intersected branch required it; otherwise all branches already supplied a
selected-edge witness. The resulting domain is another forest system.
Consequently every nonempty finite intersection is contractible.

For rational polytopes, all branches are finite unions of polytopes and
admit a common finite triangulation. A suitable finite closed-subcomplex
nerve theorem therefore relates the source to this good cover's nerve;
the topological theorem is imported, not newly proved here. No efficient
nerve-construction claim follows: there can be exponentially many branch
intersections in2^t. The concrete t=1 consequence requires only two sets:
the source is either contractible or has two contractible components.

The imported finite closed semi-algebraic version is Bauer, Kerber, Roll
and Rolle, [Theorem4.10](https://arxiv.org/pdf/2203.03571), with its
triangulation reduction through Lemma4.9 and Theorem4.8. These hypotheses
matter: arbitrary finite closed covers do not justify the inference.

## Two cycles can already support a hole

Take n independent scalars x_i in[0,1], and retain

    min_i x_i=0,       min_i(1-x_i)=0.

The source is precisely S={x:min x=0,max x=1}. Its incidence graph is
K_(n,2), with cycle rank t=n-1. For n=3, S consists of the six edges of a
cube joining vertices that have both a zero and a one: a hexagonal circle.
This is a connected source with a hole at cycle rank2. A continuous scalar
image is still an interval, so interval-valued predictions do not certify
trivial source topology.

More generally subtract the coordinate mean: y=x-mean(x)*1. This is a
homeomorphism from S to{y:sum y=0,max y-min y=1}, with inverse
x=y-min(y)*1. The oscillation max y-min y is a norm on the zero-sum
subspace of dimension n-1. Its unit sphere is homeomorphic to S^(n-2).
Thus cycle rank t can support an S^(t-1) source, including the two points
at t=1. This elementary example is an obstruction and a scope clarification,
not a claim to a new sphere construction or a new general topology bound.

Schnider and Weber's [SoCG2024 paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol293-socg2024/LIPIcs.SoCG.2024.77/LIPIcs.SoCG.2024.77.pdf)
already studies induced cubical solution spaces of Boolean CSPs, including
topological universality. The two minimum receipts above are exactly the
continuous cubical realization of requiring both a true and a false bit.
The sphere example and a generic topology/complexity connection are not
novelty grounds. The possible specific delta remains the convex-block
forest contraction, compact endpoint messages and explicit cycle bound.
