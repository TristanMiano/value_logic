# P3-11-A1: exact noisy consequence and fair controls

Codex (GPT-6), October 28, 2026. Same-model reconstruction of the fixed
V19-R/v1 worked duty. No new empirical panel or performance claim is needed.

## Reconstructing the two branches

Write the first local response above its positive baselines as
(2t+u,1-t+v), with t in [0,1] and u,v in [0,delta]. The second is
(s+u,2-2s+v), with its own independent s,u,v in the same intervals.
All coordinate lower-receipt bounds are automatic from nonnegativity.
The two upper-receipt bounds require a block with first coordinate <=epsilon
and a block with second coordinate <=epsilon.

In either block the smallest possible maximum of those two coordinates
is 2/3 before thickening. Nonnegative thickening cannot lower that number.
For 0<=epsilon<2/3 the same block cannot witness both observations. There
are exactly two possible witness assignments. They need not be treated as
probabilistic hypotheses, and no probability of the two branches is inferred.

In the low assignment, block1 obeys 2t+u<=epsilon and its sum is
1+t+u+v. The minimum is1. For the maximum choose v=delta. If epsilon<=delta,
t=0,u=epsilon maximizes t+u at epsilon. If epsilon>=delta,
u=delta,t=(epsilon-delta)/2 maximizes it at (epsilon+delta)/2.
Both cases give

    [1, 1+delta+(epsilon+min(epsilon,delta))/2].

For block2 in this assignment put r=1-s. Its bound is 2r+v<=epsilon
and its sum is1+r+u+v, giving the same interval with u and v exchanged.

In the high assignment, block1 has r=1-t with r+v<=epsilon and sum
2-r+u+v. Its minimum is2-epsilon (r=epsilon,u=v=0), and its maximum
is2+delta+min(epsilon,delta) (r=0,u=delta,v=min(epsilon,delta)).
The constraints t in [0,1] are respected because epsilon<2/3.
Block2's s+u<=epsilon gives the same range with its coordinates exchanged.

Each local region is convex, so these endpoint calculations give its whole
scalar interval. On the product of two identical scalar intervals, the
minimum has exactly that interval as image: choosing both local values
at the desired scalar value is sufficient. Thus the complete future set,
after restoring a+b, is precisely the union stated in the fixed claim.
There are no missing branches and no reliance on a convex-hull approximation.

For delta>0 the base response regions are full-dimensional: fixing an
interior t or s and allowing u,v in (0,delta) already gives an open rectangle.
For the concrete epsilon=delta=1/10, each admitted assignment also has
nonempty full-dimensional interior; choose the witness coordinate strictly
between0 and epsilon and the thickening variables strictly inside their
ranges. The useful gap is not produced solely by an equality-constrained
zero-volume model. Its survival is conditional on these particular bounds,
not a claim of robustness to arbitrary model expansion or fixed noise at
all scales.

## Explicit sources, contradiction and sharp stability bound

Set a=b=10 and epsilon=delta=1/10. Subtract20 and call the desired value q.
For any q in [1,6/5], choose t=0 in block1 and s=1 in block2, and set each
block's u=v=(q-1)/2. Every receipt holds and both sums above baseline equal q.
For q in [19/10,2], choose t=1-(2-q), s=2-q and all thickening variables zero.
For q in [2,11/5], choose t=1,s=0 and each block's u=v=(q-2)/2.
These rational formulae construct sources for every rational point in the
two stated components, including their endpoints.

The future set is [21,106/5] union [219/10,111/5]. The report band
[107/5,108/5]=[21.4,21.6] meets neither component, although it lies inside
the sharp interval hull [21,111/5]. Therefore that additional report and the
retained premises cannot all be true of a single shared source. This is a
joint inconsistency conclusion; it does not identify which premise failed.

The distance from43/2=21.5 to the first component is3/10, attained at106/5;
the distance to the second is2/5, attained at219/10. Hence

    abs(1/(V-43/2)) <= 10/3.

The bound is sharp because the first nearest endpoint is attainable. The
interval hull contains the pole and cannot certify a finite bound. The
exact set leaves the sign of V-43/2 unresolved, which is appropriate.

## What the ordinary controls establish

An ordinary exact disjunctive or mixed-integer feasibility model can impose
the same original receipts and the new report band, and reject it. The
new minimum band adds universal local lower bounds and one existential
upper witness. Explicit assignment enumeration or an ordinary MIP solver
therefore solves the same one-band duty without constructing every component.
A whole-range construction is not automatically cheaper for that one query.
Retaining winner identities, when genuinely observed, can remove disjunctions;
retaining the full source removes this uncertainty even more directly.
Neither information-rich control is an unfair opponent to be omitted.

For many future bands of the SAME fixed readout, the compiled union answers
intersection questions by binary search and can return a compatible source.
For a convex scalar loss on a bounded real interval, its worst value over
the exact set occurs at an extreme endpoint, so the interval hull already
suffices. An internal forbidden band or a pole-sensitive nonlinear function
is a suitable duty because the gap changes the answer. Changing the future
affine forms generally requires new local LP extrema; the query service is
not a universal oracle for every future readout.

The s20 max-affine example supplies a second conditional use: bounded
uncertain affine pieces fitted to two interval measurements produce a
gapped prediction at a third location. Its known-slope offset-only control
has a connected interval answer obtainable by ordinary residuation, and an
additional weakly constrained piece closes the demonstrated gap. These
controls limit where the mechanism matters. They are not defects in the
fixed two-block contribution and do not license a broad deployment claim.

This unit confirms a concrete consequence for fallible shared-source models
and bounded reasoning about retained information. Ordinary equivalent
methods tie. No observation fees, runtime percentage gain, real-world
frequency, or aggregate economic saving follows from these examples.
