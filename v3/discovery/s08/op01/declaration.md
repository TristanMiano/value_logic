# Observation policy for an action-dependent stopping duty

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The partial-star action frontier makes the stopping predicate exact. It does
not make greedy acquisition optimal. For a finite, explicitly admitted cost
alphabet, the ordinary minimax decision-tree recurrence is

```math
V(s)=0\quad\text{if a uniform action is already warranted},
\qquad
V(s)=\min_{i\text{ unobserved}}\left(c_i+\max_{v\in S_i}V(s\cup\{i=v\})\right)
\quad\text{otherwise}.
```

The terminal repair action must meet both its repair-only regret tolerance
and its upper cost against replacement. A terminal replacement must have a
sufficient lower bound on the original optimum. Source supports, query fees,
price and tolerance are part of the policy's identity. Every branch is over
the declared support; a continuous source cannot silently use this finite
branching certificate. The endpoint action bound itself remains valid over
the enclosing continuous box.

A supplied policy is safe if all reachable terminal actions and all response
branches are checked. Its worst fee follows by backward maximization. Calling
it minimax **optimal** additionally requires ruling out every action at each
nonterminal state and comparing every available query. The small experiment
will independently enumerate actions and reconstruct that lower-bound premise.
All planning and admission work is charged once per actual service duty.
Amortization across requests is shown explicitly, not assumed free.

## Greedy theorem boundary

Even the exact regret reduction need not be pointwise submodular after
replacement is included. Take one edge with two exactly-one components,
weight 1, costs independently in {0,1,2}, replacement price 1, and realized
costs (1,1). Before any observation, replacement has worst regret 1 and no
repair does better. After observing either cost alone at 1, the other can
still be 0, so replacement still has worst regret 1; each repair's worst
combined regret is at least 1. After observing both, the true optimum is 2
and replacement's regret is 0. Thus the reduction in the optimal combined
regret is 0 for either singleton and 1 for the pair. The second observation
has greater marginal benefit than the first. This falsifies submodularity
of this **particular natural gap utility**, not the existence of every possible
alternative cover utility or every approximation algorithm.

## op01 finite and paid declaration

Use four new original exactly-one stars: weights (1,1), (5,2), (1,2,3), and
(2,3,5,1), H=5. Each node has alphabet {0,2,3,5}; an independent mandatory
anchor has alphabet {0,A}, A=10H sum(weights). Acquire and independently
check the same original resolution step used by fs01 to establish that
mandatory feature. Per case, use six deduplicated duties from prices A,
A+H sum(weights), A+2H sum(weights), crossed with tolerances floor(HW/2)
and HW. Query fees are new seeded integers 1..7 with anchor fee 9 (8141660).
For each duty build and check an exact minimax policy and a fixed cheapest
query policy with the same full action frontier. A narrow median/balanced
action menu is a development comparator, not the strongest ordinary baseline.
The exact policy is shared with an ordinary mirror.

Run 64 fresh requests per case/duty/arm, seeds 8141670..8141673, with independent
uniform cost coordinates and a fair anchor bit. Arms: minimax policy,
ordinary minimax mirror, cheapest full-frontier policy, and cheapest narrow
menu. Freeze declarations, implementation and seeds before physical calls.
Record every actual cost receipt and final source action. Reconstruct each
output from its original clauses, features and every compatible finite world.
Report setup and repeated costs separately. All evidence is DEVELOPMENT,
with zero complete SAT provider calls; four local resolution steps are paid.
Failures preserve their physical prefixes and unknown costs, never free retries.
