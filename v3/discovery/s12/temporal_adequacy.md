# Task-scoped reliance for a schedule model with false intermediate claims

Codex (GPT-6), October 19, 2026. DEVELOPMENT synthesis; no new application
measurement or priority claim. This joins the task-adequacy and temporal
constructions rather than adding another candidate family.

## Exact projected source and surviving observations

Let F be the bounded nonempty integer difference-constraint source in
[temporal_receipts.md](temporal_receipts.md), with reference x_0=0 and its paid
closed distance matrix D. Fix observable origins Q and target origin scopes J,
including reference zero wherever a unary bound is used. Define H by requiring
that x_(Q union J) lie in P_(Q union J)(F) for every declared J. Original
coordinates not used by any of these scopes keep their declared ambient domains.

Eliminating a variable from difference constraints adds all composed paths
through it. Consequently P_S(F) is exactly the constraints
x_j-x_i<=D_ij for i,j in S, together with the same reference convention.
There is an integer extension whenever those inequalities hold: elimination
of integral difference bounds preserves integrality of the extension interval.
Equivalently, append the fixed selected coordinates as reference bounds and
use feasible integral shortest-path potentials. Thus H has an explicit
representation using only the selected entries of the original closure.
An arbitrary syntactic subgraph is insufficient; its omitted paths may induce
essential selected-endpoint constraints.

For every interval receipt history h on Q and every declared target scope J,

    P_J(H intersect h) = P_J(F intersect h).

The witness proof in [task_adequacy.md](task_adequacy.md) does not rely on Boolean
coordinates or singleton receipts: a witness agrees with actual x on all Q,
so it satisfies every interval restriction that x satisfies. Adaptive histories
are included pathwise. Empty-source compatibility is also preserved, provided
there is at least one declared target scope. Maximality holds for an interface
that permits exact observations of all Q; restricting to a coarser interval
vocabulary can allow an even larger envelope and needs its own characterization.

Every specified copy/offset edit with target scopes pulled back to the declared
original scopes therefore retains the temporal service's exact guarantees on H.
Keeping H as an adequacy event does not require materializing H at execution:
the controller may continue using D and its unary bounds. A supplied event
Pr(x not in H)<=epsilon gives one unconditional error bound for the entire
adaptive same-world stream. Conditional error on an accepted subset is a
different quantity, and replacing the underlying world requires new accounting.

## A concrete nonvacuous duty

Let all coordinates be integers in [0,10], and let the model be

    F: 0 <= q <= z_1 <= ... <= z_k <= a <= 10.

Only q may be observed and only a is a target origin. Its task envelope is
H: 0<=q<=a<=10; the intermediate z coordinates are unrestricted within their
ambient domains. Actual q=6, a=8, and every z_i=2 violates F but belongs to H.
Observing q>=6 enables the edit y=a-6 with target 0<=y<=4. It is valid for
every H-world with that receipt and gives actual y=2. Before the receipt,
the same edit cannot be certified because H permits a=0.

This demonstrates unresolved target information, useful counterfactual change
and reliance on a globally false model in one small duty. It does not justify
the endpoint ordering as a physical fact, or turn a schedule transformation
into causal control. A cheaper direct model q<=a gives the identical service.
The full chain contributes a derivation or explanation of the endpoint relation;
its extra claims need not all be true in the deployed world.

Enlarging Q to include z_1 can remove the actual world from the envelope.
The actual observations q>=6,z_1=2 then contradict F. The controller must
report the conflict, even though the earlier endpoint-only duty was sound.
More permitted observation can strengthen the required adequacy event; it is
not automatically a free improvement in a fixed-model certification service.

## What a fee claim would have to pay

Suppose a trustworthy endpoint warrant is already available and observing q
costs c_q while observing a directly costs c_a. On a stated workload in which
the chosen q receipt enables the requested edit, let P be source/closure
preparation and V the remaining controller work converted to the same units.
Over T such instances, the endpoint method costs P+T(c_q+V); direct target
observation costs T*c_a plus its own specified action/controller costs.
Ignoring common costs, a gain requires c_a>c_q+V and
T>P/(c_a-c_q-V). This is an algebraic break-even condition, not evidence that
such prices or workload frequency hold. Failed enabling receipts, fallback,
source changes and obtaining the endpoint warrant must also be included.

If calibration uses fully labelled endpoints, its label purchase need involve
two origins instead of k+2, but its statistical and selection assumptions are
unchanged. It cannot be advertised as a measured audit-fee saving. In this
particular constructed world the full model is false, so comparing equal
zero-error full-model and endpoint-model calibrations would be incoherent.
The appropriate ordinary comparator is direct endpoint modeling/calibration,
which ties the same projected service and may avoid unnecessary preparation.

## Contribution disposition

The useful object is a declared observation/operation contract, a maximal
adequacy event and exact reuse with charged preparation. Projection, temporal
closure and ordinary task-specific modeling are established ingredients.
This example makes a possible service concrete without establishing novelty
or economical deployment. It favors a small motivated duty over a larger
synthetic chain benchmark; a benchmark built solely to make intermediate
labels expensive would not resolve the closest-prior question.
