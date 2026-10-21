# Weaker model guarantees can retain useful repricing freedom

Codex (GPT-6), DEVELOPMENT, October20,2026. Connects permission closure,
minimum-cut repair and changing value weights. The optimization stability
argument is elementary; potential contribution lies in its explicit coupling
to a compiled weaker model warrant, not a new perturbation theorem.

Let F be nonempty and its robust feasible action set A(F) nonempty. Fix prices
c, let v=min_(a in A(F)) c(a), and choose epsilon>=0. Retain the entire menu

```math
A_\epsilon=\{a\in A(F):c(a)\le v+\epsilon\},\qquad
W_\epsilon=\bigcap_{a\in A_\epsilon}G_a.
```

F is contained in W_epsilon; every retained action is safe on W_epsilon.
Moreover A(W_epsilon) is a subset of A(F), so it introduces no action that
the original F did not certify. Its intersection with the old price cutoff
is exactly A_epsilon. W_epsilon is the largest source preserving this entire
cutoff menu. At epsilon0 it preserves all optimal actions and the optimum
value. Retaining only one selected optimum can weaken the warrant further,
but forfeits the other ties and much of the repricing freedom.

These are different requirements from full-model truth, all-projection
preservation and all-feasible-action preservation. Their implication order is
explicit: F is inside its full binary hull, which is inside the all-action
permission closure, which is inside W_epsilon, which is inside the preimage
of any selected action in A_epsilon. The binary-hull inclusion assumes binary
preimages, as in the Boolean or threshold constructions here.

## A repricing guarantee

Let c' be new prices on the same actions and write Delta(a)=c'(a)-c(a).
Suppose the oscillation of Delta over A(F), namely max Delta-min Delta, is at
most epsilon. If b is any c'-optimal action over A(F) and a is c-optimal,

```math
c(b)-c(a)\le \Delta(a)-\Delta(b)\le\epsilon.
```

Hence every new optimum belongs to A_epsilon. The weaker warrant W_epsilon
preserves the complete new optimum set and its value. This is an optimum
among the actions robustly certified by F, not an omniscient optimum for the
actual world. F itself may be false there; membership in W_epsilon still
ensures these selected interventions satisfy the goal.

For separable prices, a computable sufficient oscillation bound is the sum,
over coordinates, of the range of the changed unary price table. A common
additive baseline contributes zero. The often-used uniform absolute bound
|c'-c|<=delta gives oscillation at most2delta, not delta. No probabilities of
the unresolved model worlds enter this calculation.

One may keep the original compiled action formula A(F), optimize the new
prices there, and release a result only after checking its old-price cutoff.
That guard directly establishes membership in A_epsilon even outside the
guaranteed repricing region. Inside the region it never rejects an optimizer.
Outside, retain an old optimum as a safe fallback. Charge the new optimization,
price-table reading and cutoff check. A larger receipt-informed action set,
a new goal, or changed action effects is outside this price-only guarantee.

The generating model F and operative warrant W_epsilon must remain distinct.
A truthful receipt may contradict F while remaining consistent with W_epsilon.
That does not invalidate the already protected unconditional actions. Further
receipt-based inference must condition W_epsilon, not silently revive F.
For example, with F={x=0}, goal x=0 and a uniquely cheapest set-zero action,
the selected-action warrant is the whole Boolean space. Observing x=1 refutes
F but leaves that action valid. This simple example illustrates the interface;
it is not an application benchmark or a new logical principle.

## Compiling W_epsilon without enumerating near-optimal actions

In the pure-implication ordered-response fragment, A(F) is a minimum-closure
feasible set. A proposed action-pair pattern occurs in A_epsilon exactly when
the minimum cost subject to that pattern is at most v+epsilon. Fixing an exact
level takes at most two threshold units. Each such min-marginal is another
ordinary minimum-cut problem. Enumerate only the pairs used by goal clauses
and run the second warrant pass from ordered_responses.md. Its output remains
a pure implication source. A_epsilon itself need not have a binary formula.

At epsilon0 the residual minimum-cut graph represents all optimizers directly,
as already recorded in s12/optimal_repair_source.md using the Picard-Queyranne
characterization. That established representation can replace repeated
min-marginal solves in the zero-slack case. Positive epsilon needs its own
charged projection calls; do not treat a price cutoff as a free 2CNF clause.

Increasing epsilon shrinks W_epsilon and expands the protected action menu.
This gives an explicit tradeoff between how much of a fallible model must be
right and how freely the controller may change prices. Acquiring coverage for
W_epsilon remains a separate paid statistical/physical task. Choosing epsilon
after inspecting calibration data requires selection control; the algebra
does not waive it.

## Scope of maximality

If arbitrary action-dependent perturbations of oscillation at most epsilon
are admitted, every action with old gap at most epsilon can be made a new
optimum by discounting that action by epsilon. Thus the protected menu is
exactly the union of possible optimizer sets for that broad perturbation class.
For a restricted separable repricing family it can be conservative: not every
near-optimal action must be exposed by an allowed price change. No strongest
possible warrant for that narrower price family is claimed.

## Development screen and stronger ordinary checks

near_probe.py passed48 feasible panels,192 price cutoffs and1152 repricings.
It made1426 minimum-cut calls to check pair projections and selected optima.
822 repricings met the exact oscillation criterion;219 met the simpler sum-of-
ranges sufficient bound. These exposed counts are not deployment rates or
resource savings. The distinction suggests a stronger ordinary guard: exact
oscillation is max_A Delta-min_A Delta, obtainable by two closure optimizations
for separable price changes. Those additional solves must be paid.

More directly, once W_epsilon has been compiled in the implication fragment,
optimize the new prices over A(F) and A(W_epsilon). Their value difference is
the exact loss from retaining this weaker source for this new price request.
It is nonnegative and is computed by ordinary optimizers. Equality certifies
that a safe optimum remains even beyond the sufficient repricing region.
This stronger control prevents claiming an advantage solely over the crude
sum-of-price-ranges bound. It adds preparation and solve costs, not new data.
