# A warrant for a finite observation policy

Codex (GPT-6), DEVELOPMENT, October20,2026. An ordinary guarded weakest-
precondition construction. The fixed-tree projection variant already appears
in s12/task_adequacy.md, under "A narrower fixed-policy variant." This note
substitutes the new action-menu closure at each leaf and records representation,
budget and multi-policy limits. The tree construction itself is inherited,
not a new capability or separately numbered candidate. It repairs a limitation
of the initial-menu warrant, not the general problem of learning adequate
models or sequential causal dynamics.

## Contract and construction

Fix a finite deterministic decision tree whose internal nodes purchase truthful
coordinate observations of a static Boolean world. Its leaves have disjoint,
exhaustive path regions h_l, each a conjunction of unit literals. Repeated or
inconsistent paths may be removed. Before deployment, define a nonempty action
menu A_l at every reachable leaf; each action has goal preimage G_a. For leaves
where the service promises no action, explicitly use an empty accepted region.
Then the largest set on which every action the service may select is correct is

```math
W_T=\bigcup_{l:A_l\ne\varnothing}
   \left(h_l\cap\bigcap_{a\in A_l}G_a\right).
```

Every world takes exactly one path, proving both safety and maximality. A world
outside W_T either reaches a rejecting leaf or makes some retained action fail.
The latter rules out preserving the *entire* menu there, even if a particular
price happens to select a successful action. No probability is needed for this
identity. A probabilistic coverage premise for W_T can be added separately.

For nonempty source F, take A_l=A(F AND h_l) on source-reachable leaves and
reject off-source leaves. Assume these reachable menus are nonempty. Then
F is contained in W_T and the permitted menu at each retained leaf is exactly
A(F AND h_l). Indeed the leaf warrant contains F AND h_l, preserves every
original permission, and cannot add a permission invalid on F AND h_l. This
gives exact conditional-menu preservation along this declared observation tree.
It does not preserve arbitrary later queries, arbitrary goals or new branches.

## Representation and costs

For coordinate toggles and binary goals, each intersection of action preimages
is binary. Use permission_closure.md's second pass after compiling A_l. Thus
W_T is an explicit union of at most L binary sources, where L is the number of
accepted leaves. With F a union of M binary models, a simple uncached bound is
4LgM first-pass satisfiability calls plus4Lg second-pass calls. Charge path
construction, empty-branch checks, source storage, purchased observations and
the controller too. Reusing conditioned projections is a mandatory ordinary
control. A depth-d full tree can have2^d leaves; this is not a succinct guarantee.

The ordered-response analogue uses truthful threshold comparisons, whose paths
are units on threshold bits. Each leaf warrant is an implication system by
ordered_responses.md, and the whole warrant is a union of at most L such systems.
Leaf-specific unary prices can be optimized by ordinary minimum cut. The
warrant covers any selection from the retained menu, so repricing those choices
does not itself require another model-coverage premise.

This can require less model truth than preserving every target projection
after every allowed observation, but may cost far more to represent. The earlier
projection envelope and this policy warrant solve different preservation tasks.
No resource dominance is asserted.

## Budgeted correctness and limits

If each purchased observation has a known fixed price, a leaf's total fee is
known. Retaining only leaves whose fee is at most B gives the largest warrant
for correctness *and* that pathwise observation budget. Correctness alone does
not preserve the old model's expected cost: actual worlds can move to expensive
branches. State-dependent prices, timing leakage, failed observations and
irreversible interventions require their own semantics, not this shortcut.

Intersecting many policy warrants can destroy tractability. A one-query tree
can have warrant (a OR b OR c): when a=1 it accepts every world, and when a=0
it demands b OR c. Both leaves are binary sources. Intersections of such trees
encode arbitrary3CNF. This example allows different fixed goals across the
policy family; no same-goal hardness theorem is asserted. A fixed number k of
explicit L-leaf policies can instead be distributed into at most L^k branches.

This is a useful representation boundary, not an independent planning theorem.
It does not infer causal effects from observational success, and its truth
coverage must still be established by checked premises or paid calibration.
