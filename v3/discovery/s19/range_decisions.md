# When a complete scalar range changes a decision

Codex (GPT-6), October26,2026. DEVELOPMENT; a relevance screen, not a new
decision theorem. Keep this limitation beside the AR1 contribution claim.

Let S be a nonempty compact set of possible scalar values, with endpoints
l and u. For every action a whose loss L(a,v) is convex in v,

    max_(v in S) L(a,v) = max(L(a,l), L(a,u)).

Indeed v is a convex combination of l,u, so convexity bounds its loss by
the larger endpoint loss; both endpoints belong to S. Therefore replacing
S by its interval hull leaves every action's worst loss, and hence the
minimax action, unchanged. This includes absolute and squared prediction
loss, not just monotone loss. An expensive complete range has no added
decision value for this specified duty. This statement does not apply to
source-coupled regret between several counterfactual optima: their
differences need their common source, as edit_decisions.md demonstrates.

Gaps do have a concrete role when a new report must be checked against a
fallible fixed-source model, or a downstream computation has a forbidden
denominator band. The positive-cost example in robust_gap.md has
S=[21,21.2] union [21.9,22.2]. A report interval[21.4,21.6] is incompatible
with the old source/receipt premises. The same S has distance0.3 from21.5,
so every compatible source satisfies |1/(V-21.5)|<=10/3. The interval hull
cannot supply any finite reciprocal bound. This is conditional numerical
stability, not a claim that an uncertain denominator has a known sign.

An ordinary exact disjunctive calculation gives the identical conclusion.
For one prescribed forbidden band, direct feasibility can be cheaper than
constructing all gaps. Retaining the complete range is principally a
reusable answer object for many subsequent bands or nonconvex scalar-loss
queries under the same future objective and source version. It does not
automatically amortize across different future objectives. Those require
new local objective extrema even if some feasible slices can be reused.

## A finite query family may be the better contract

For a piecewise-linear loss with finitely many breakpoints, partition the
scalar axis into its linear pieces. On each closed piece intersected with
S, the maximum is achieved at an extreme attainable value in that piece.
Thus two constrained endpoint queries per piece suffice; empty pieces are
ignored. There is no need to materialize every component of S. The source
constraint for a target band[a,b] is V>=a and V<=b: add f_i>=a locally,
then select one witness i with f_i<=b. This is another ordinary finite
disjunction, or an extra receipt in AR1. Its cost must be compared with
full-range construction for the actual number and kind of later queries.

These observations narrow the useful claim. They do not erase the exact
range algorithm, its output bound, or its model-criticism consequence;
they prevent treating more retained geometry as universally better use
of a bounded reasoner's resources.
