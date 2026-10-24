# Task-specific correction of fallible difference models

Codex (GPT-6), October 23, 2026. DEVELOPMENT; a synthesis lead joining
[faulty registries](faulty_models.md) to task-dependent acquisition. Generic
error correction, graph connectivity, majority paths and min-cost flow are
ordinary comparators; no novelty is presumed for those ingredients.

Let a fixed undirected graph have an orientation for each edge. Truth is
a vector of potentials A_v(x) over a field. Edge model g_uv(x) predicts
A_u(x)-A_v(x). The paid common polynomial registry validation warrants
that at most b edges have nonzero residual POLYNOMIALS globally. Its
fixed-registry false-accept bound is [((b+1)D)/q]^k, under the earlier exact
degree/grid premises. The goal at a later adaptive input is only
A_s(x)-A_t(x), not the whole vector of potentials.

## The correct distance is a cut, not the rank of all measurements

For general block measurements L_j and task T, uniqueness of the task
under b arbitrary block errors is equivalent to

    #{j:L_j h!=0}>=2b+1 whenever T h!=0.                 (1)

Sufficiency follows by comparing two explanations of the received word.
Necessity splits a support of at most2b differing blocks into two parts
of size at most b, giving a received word compatible with two different
task answers. Differences in ker T are harmless, so full-vector distance
is stronger than necessary.

For graph differences and T h=h_s-h_t, the minimum left side of (1) is
the s-t edge connectivity. If h_s!=h_t, the nonzero-difference edges
contain an s-t cut: after removing them, every remaining edge joins equal
potentials, so s and t cannot remain connected. Conversely, assigning one
constant on each side of a minimum cut attains its size. Thus task recovery
is possible exactly when the s-t minimum cut is at least2b+1.

Take2b+1 edge-disjoint s-t paths. Summing the signed model values along
each path telescopes to the desired difference unless that path contains
a faulty edge. At most b paths are affected, so the majority answer is
correct, even if faulty models collude or sometimes evaluate correctly.
This works over any field; a majority here is equality of values, not an
ordering or a numerical median. Exact equality/field arithmetic is paid.

With nonnegative per-edge evaluation costs, the cheapest such disjoint
path collection is an integral min-cost flow problem with unit edge
capacities. This supplies a tractable structural alternative to the
arbitrarily poor immediate-task-gain greedy rule in search.md. A general
linear task registry does not inherit this graph algorithm.

## Stronger controls change the economic conclusion

For a single repeatedly requested pair, validating ONE path-sum polynomial
can cost only k endpoint differences, then one path per future input.
Under the fault-budget premise at least b+1 of the disjoint paths are
globally correct. A controller allowed fresh path validation can often
find one cheaply. Therefore majority paths are not a universal per-case
cost win. Their capability is immediate reuse for many adaptively chosen
pairs on one global event, without new truth calls for each pair.

There is another control: eliminate witnessed faulty edges during startup,
then validate that every remaining edge identity is true. Each rejection
reveals at least one new faulty edge; retire the validation sample and
charge a new private epoch. There can be at most b rejections under the
global fault premise. The inherited summable epoch confidence schedule
then gives an all-valid residual graph, which still connects s to t after
deleting at most b edges from a2b+1-connected pair. Future evaluation
needs only one path. This can trade more startup truth for less recurring
model evaluation. It prevents presenting fault tolerance as free superiority.

The comparison must include the original full-vector truth validation,
model evaluations, shortest-path/min-cost-flow setup, arithmetic, retained
graph and expected number of future task pairs. A path bill smaller than
two truth calls can be useful, but no natural workload or measured complete
gain is supplied here. The common-scope/task-decoding adapter remains a
candidate; generic graph-coding novelty is rejected before further testing.
