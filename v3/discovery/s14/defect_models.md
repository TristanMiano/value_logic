# Fallible implication models with a paid defect budget

Codex (GPT-6), DEVELOPMENT, October22,2026. S02/S04/S28 lineage. This is a
new scope of the existing cut/source adapter, not a new max-flow algorithm.
Compare [optimal repaired sources](../s12/optimal_repair_source.md), which
retain only minimum-defect worlds, and [calibrated slack](../s13/calibrated_slack.md).

## Keep a sublevel source rather than assert the whole model

Let a directed graph carry nonnegative rational weights w_uv on predicted
implications x_u=>x_v. Define the actual defect score

    V_w(x)=sum_(u,v) w_uv [x_u=1 and x_v=0].

Weights here measure an explicitly chosen defect budget. They are not
automatically probabilities or action prices. The source is F_B={x:V_w(x)<=B},
with B>=0, so it is nonempty (all-zero and all-one worlds belong). For a
target s=>t, s!=t, let lambda_w(s,t) be its directed minimum cut capacity.
Then

    min_(x_s=1,x_t=0) V_w(x)=lambda_w(s,t),
    F_B entails (x_s=>x_t) iff lambda_w(s,t)>B.

The proof is the standard assignment/cut correspondence. A feasible flow
of value greater than B already certifies acceptance before the maximum flow
is known. A cut of capacity at most B gives a concrete counterworld. Neither
solver status nor an unverified weight vector is a receipt by itself.
For a conjunction of target implications, take the minimum of their cut
values. Several individually false model clauses may coexist with every
target remaining guaranteed.

Example: two paths s->a->t and s->b->t, all weights1. The target has cut
value2 and holds on every world with at most one failed model edge. The
world (s,a,b,t)=(0,1,0,0) violates one model edge while satisfying the target.
A distribution supported only on such nonzero-defect worlds can make the
complete model false on every case while preserving the target. This is a
conditional useful-model construction; learning its budget remains separate.

The old action compiler can use these binary projections. For atomic setters
and implication goals, compute the relevant constrained minimum defect for
each prospective failure pattern; then solve the same compiled action problem.
Hard partial observations become forced sides of a cut. An inconsistent
receipt/source combination is not permission to assert an arbitrary action.
One must check nonemptiness under the receipts before using a universal claim.

## A precise limitation of marginal reliability alone

Suppose the only probabilistic premises are

    P(x_u=1,x_v=0)<=p_uv,

with no independence or joint error budget. Let D be the shortest directed
s-to-t path length with edge lengths p_uv (D=infinity if no path). Then the
sharp upper bound over all joint laws is

    P(x_s=1,x_t=0) <= min(1,D).

Upper bound: on any path a target failure requires at least one failed edge;
apply the union bound and choose the cheapest path. For attainability, take
shortest-path distances d(v), truncate at D when D is finite and positive,
and use a random threshold theta uniform on[0,D]. Set x_v=1 iff d(v)<=theta.
Then s=1,t=0 almost surely, and an edge fails on a threshold interval of
length at most p_uv. If D<=1, use this cut distribution with probability D
and the all-zero world otherwise. Its edge failure probabilities are at
most p_uv and its target failure probability is D. If D>1, use the cut
distribution always; each edge failure probability is at most p_uv/D<=p_uv.
If D=0 the bound0 follows from a zero-length path. If no path exists, the
reachable-vertex cut has no outgoing edge and gives target failure1 with
every modeled edge satisfied. All claims include zero-probability endpoints.

Equivalently, optimizing a weighted-score Markov bound over nonnegative w
does not improve on this shortest path when only these marginals are known:
the ratio (sum_e w_e p_e)/lambda_w(s,t), where lambda>0, has infimum D
for a finite path. Normalize lambda>=1. Max-flow/min-cut gives a unit flow
bounded by w, whose p-cost is at least the shortest-path cost; putting unit
weight on a shortest path attains it. Cap probability bounds at1.

Thus redundant paths alone do not amplify reliability without a stronger
joint premise. A hard or statistically calibrated tail bound for V_w is
meaningfully additional evidence. The argument is ordinary union bounds,
shortest paths and flow duality; it is retained to prevent an overclaimed
ensemble gain, not presented as a new probability principle.

## Acquisition and revision screen

A fixed score's upper quantile can be calibrated by ordinary one-sided
tolerance limits on independently sampled worlds. Upper bounds on calibration
scores are conservative for this upper-tail duty. This direction differs
from the lower scores used for the earlier unsafe-gap allowance. An action
whose cut margin exceeds the calibrated budget inherits the common score
event, including after selecting among many such actions. The event's
statistical scope and all label/computation costs still apply.

There is an immediate obstruction to cheap partial score receipts:
maximizing V_w over a partially observed box is NP-hard in general. Put
equal-weight arcs in both directions on every edge of an undirected graph;
V_w is then the cut size. Consequently tractable minimum-defect queries do
not imply tractable exact upper scores for calibration. The sum of unresolved
edge weights is a valid coarse upper bound, and bounded-width graphs admit
ordinary dynamic programming, but neither is an unpriced precision oracle.

For just one implication, direct calibration buys at most its two endpoint
bits per case. Full model-score evaluation may buy every vertex, so a model
learning harness is not justified by this example alone. A many-target reuse
duty, a cheaply supplied structural budget, or a stronger partial score
certificate is needed before pursuing measured acquisition savings.

For graph-weight revisions, a retained feasible flow remains a lower receipt
if its capacities still fit. Deleted/reduced capacities can be handled by
discarding affected path flow, with lost value explicitly charged. This is
ordinary flow sensitivity; full recomputation and existing sensitivity
oracles are mandatory comparisons. No new dynamic-graph performance claim.

Disposition: retain the exact defect-source interface and the sharp marginal
obstruction; defer an implementation workload until its evidence economics
survive the direct-target comparator. This keeps a concrete broader-model
lead without making another narrow harness the research program.
