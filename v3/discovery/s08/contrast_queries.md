# Audit a policy-fee contrast directly

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The learning target need not be either counterfactual action. After an exact
action is already delivered, a policy's last query can still be missing
while its total from-scratch invoice is determined: the last value affects
the action, but no longer affects how many observations that policy buys.
Executing the complete alternative policy can therefore overpay when the
only remaining duty is to learn its invoice or its contrast with another.

Let f be a checked integer contrast function under the current receipts.
Its edge-valued representation is an offset plus a canonical residual node.
The offset is already known and does not affect the cost of learning the
remaining value. With positive fixed coordinate audit fees, define

```math
G(0)=0,\qquad
G(v)=\min_{i\in\mathrm{supp}(v)}
\left[c_i+\max\{G(v_{i=0}),G(v_{i=1})\}\right].
```

Here each cofactor is renormalized, and its additive offset is discarded
only for **planning future observations**, not for evaluating f. The chosen
coordinate is removed from each cofactor's support. Thus recursion strictly
decreases support size. Cached states can be keyed by residual function node,
rather than by the entire receipt pattern. Induction proves that G is the
minimum worst-case remaining physical audit fee among deterministic exact
function-evaluation policies. Randomized decision trees have a different
minimax objective; no optimality claim for them is made here.

A certificate supplies every admitted cofactor edge, each residual G value,
and its selected query. Independently check source-function identities,
absence of the queried variable from cofactors, and all Bellman equalities.
For a mere upper quote, only the selected-query inequalities are needed;
the proposed first implementation checks the full finite minimization.
Counterfactual fees remain from-scratch fees even when pilot observations
reuse paid receipts. The physical pilot bill charges only newly bought
coordinates. Its source and receipt identities stay the same as the action.

This is ordinary exact decision-tree optimization on a smaller checked
target. Neither decision-tree Bellman recursion nor EVBDD cofactoring is new.
The useful integration is the explicit, paid link from original action
receipts to the cost of learning **only** a policy contrast.

First screen: the n=6 and n=10 cs01 fee vectors, the two distinct invoice
representatives established by checked syntax pruning, and both logging
policies. Prepare the global contrast, then for every complete indicator
world compare direct contrast evaluation, full alternative-policy replay
with receipt reuse, and auditing every still-unknown coordinate. Check
contrast values and actual additional fees, including all zero-query cases.
Cap at 100,000 distinct planning states and 250,000 EVBDD nodes per fee
vector; save interrupted and capped attempts. No physical audits in this
conditional screen. Later paid learning requires its own frozen design.
