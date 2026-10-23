# Recycle a certified error space after model changes

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 33.

Suppose a common event E, already acquired with failure probability at most
delta_0, warrants A(x)-B(x) in a known d-dimensional column space U for every
allowed x. U need not be orthonormal here. Retain d independent coordinate
rows J, so U_J is invertible. The [exact skeleton](error_skeleton.md) then
repairs every output from d exact anchor outputs.

## Sound edit and inexpensive recompression

A model change B'=B+Delta with a proved all-input image bound
image(Delta) subset T inherits the error-space bound U'=span(U,T).
This implication holds on the SAME E, even for adaptively chosen edits whose
proofs are sound. Repeating such implications does not spend fresh delta.
It may grow the correction dimension, so it does not guarantee cheaper work.
For Delta in U the old anchors remain valid without any new random test.

Let U' have d' independent columns and J' be d' independent rows. On E,

    F'(x)=A(x)-B'(x)=U' C(x),
    C(x)=(U'_J')^(-1) [A_J'(x)-B'_J'(x)].                    (1)

If the edited model error is now known to be a polynomial of degree <=D,
freeze the edit and its basis before fresh product-grid samples. Apply the
range certificate from [pass 20](anytime_range.md) to C, in d' coordinates.
Each probe requires only d' exact anchor outputs, plus the model evaluation
and coefficient transform. If its certified coefficient range is V, then
U'V is the new all-input error space. A second anchor selection can reduce
later exact checking from d' to rank(V) coordinates.

The fresh certificate can be conditioned on the entire earlier history:
the degree bound and fresh sample law remain valid for the now-fixed C.
If it has false-completion probability <=delta_1, the inherited claim has
failure probability <=delta_0+delta_1. No independence between the two
certificates is needed. An unbounded sequence of statistical recompressions
needs a summable or otherwise valid common error budget. Algebraic transport
alone and new statistical compression are different operations.

## Resource example and strongest immediate control

Take n=128, d'=12, actual residual rank 4, degree <=4, and product grid
size 257. The pass-20 fully resolved certificate at delta_1=.001 and
theta=1/2 stops within seven probes for this rank. Acquiring those seven
coefficient vectors uses at most 7*12=84 exact coordinate outputs, rather
than 7*128=896 for direct full-output range acquisition: 90.625% fewer in
THIS acquisition component. The already available 12-anchor repair is the
appropriate immediate deployment control. Compression to four anchors saves
eight exact coordinate evaluations per future case. Ignoring other costs,
84/8=10.5 future cases amortize the acquisition.

Neither percentage nor amortization includes model calls, basis arithmetic,
selection, exact bit complexity, proofs, storage or shared batch evaluations.
If the true solver computes all coordinates together, coordinate count may
be the wrong currency. Direct symbolic compression or ordinary incremental
CUR/range methods can be stronger controls. An identical ordinary algorithm
ties. The potential contribution is a reusable evidence contract spanning
model edits, conditional fresh certification and bounded correction cost;
generic low-rank reconstruction itself is not new.

## Failure screens

* An arbitrary edited program need not preserve the degree bound or the old
  error space. A model-version name is not an image proof.
* Inputs selected because their residuals looked small are not fresh uniform
  grid probes. Ordinary deployment cases cannot be silently relabelled.
* Approximate membership cannot substitute for the exact all-input premise
  in (1); see [conditioning](approx_skeleton.md).
* Reusing the original random sample after choosing B' from that sample does
  not obtain the stated conditional certificate. Freshness or an appropriate
  simultaneous theorem must be paid for.
