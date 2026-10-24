# What sharpness contributes to the decision contract

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; consequences of the
pinned theorem, not separately claimed novelties.

The successful threshold example needs the valid upper inequality, not
the full sharpness proof. Young and inverse-compression inequalities already
supply that inequality. The extra role of sharpness is to characterize when
the available information is insufficient: a more sophisticated sound method
using only the same C,c,e cannot certify below a threshold at or below the
attained upper endpoint, nor above a threshold at or above the attained lower
endpoint. The endpoint witnesses establish this obstruction directly.

This distinction matters to the contribution assessment. A positive
threshold example alone cannot establish the value or novelty of the sharp
theorem. A useful synthesis would combine inexpensive sufficient certificates
with a precise account of which unresolved decisions require additional
information. It still needs a close comparison with ordinary optimal recovery.

## Truthful matrix-order brackets

Suppose the information class is exactly

    0<C_minus <= C <= C_plus<I,

with the same dimension-unrestricted source contract. The optimized lower
endpoint for C_minus and upper endpoint for C_plus are sharp for this larger
class. Validity follows from operator monotonicity; attainability follows
because C_minus and C_plus themselves are allowed sources. Different
endpoints can again use different sources. This is an immediate consequence
of the core theorem, not a new uncertain-input theorem.

If those brackets were obtained by relaxing a box of scalar query intervals,
their whole matrix-order class may contain matrices that fail the original
query intervals. The resulting bounds remain sound, but need not be sharp
for the stronger original observations. In particular, the 32-fold tolerance
example is a sufficient precision result for the specified adapter, not an
optimal query-precision claim.

## Rational witness completeness has a bounded qualification

For rational C_minus,C_plus,E>0,V=cc^T and threshold, continuity and density
of rational parameters ensure a finite rational witness for every strict
threshold lying outside the corresponding optimized interval. A parameter
at the irrational cap can be approached from above. Upper endpoint one
can be handled by the checker's scalar cap when the threshold exceeds one.
Witnesses for the other side of the reported interval can be chosen
independently; universal validity ensures their consistency.

This is a statement about unbounded exact rational enumeration, not about
the existing checker's fixed 4096-bit input cap. A tiny positive margin may
require more bits than that cap allows. The actual bounded checker is sound
on accepted inputs and may abstain even when the mathematical information
would determine a strict decision. The contribution claim does not promise
decision completeness, an optimizer, or a uniform runtime bound.

The preceding statement also fixes the target weight to the core rank-one
case. The checker's broader PSD trace-one weights give sound bounds, but
sharpness for a weighted mean is a separate problem and is not inferred
from scalar sharpness one target at a time.

## A decision that does not presume a free future optimizer

A concrete use is approval of an entire counterfactual edit family before
its particular member has been selected: retain the old block, receive a
norm-budget warrant, and require that every permitted edited model's best
ridge objective stay below the declared threshold. The preferred example
approves this family from the rounded block. The full-rank same-vector
counterexample shows why the weaker retained information cannot support
the same universal approval.

This is an ex ante robustness decision. A future optimizer has not been
computed or supplied by the certificate. If a real workflow must solve the
edited problem anyway and gets its value for free, avoiding a separate
value query gives no such fee saving. The break-even identity in decision.md
applies only when those are actually distinct paid operations. The bounded
contribution can still be a useful explicit guarantee without a measured
production speedup, under the author's moderate-contribution standard.
# Finite attainment determines strict boundary decisions

The final path argument in [proof.md](proof.md) fills the entire N16
interval with finite realizations. In particular, if a threshold equals
either sharp endpoint, the corresponding universal strict inequality fails
because an equality witness exists. For this core claim, saying the sharp
upper endpoint is below a threshold is therefore equivalent to saying
every compatible value is strictly below it.

This equivalence must not be transferred to the separate
[paired nonattainment regime](pair_block.md). There every finite contrast
is strictly below g*s, while its supremum equals g*s. A qualitative
strict statement can then hold without a positive uniform margin. A
finite source-norm warrant restores a quantitative margin as described
in [pair_norm.md](pair_norm.md). The distinction concerns quantifiers,
not numerical rounding or a solver's tolerance.
