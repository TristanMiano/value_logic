# Expected fee under a worst-fee cap

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

op01's minimax recurrence breaks equal worst fees by query index. That may
leave an avoidable average-fee loss. It is not enough to optimize expected
cost among root queries whose own minimax value ties: a child is allowed to
spend more than its local minimum worst fee if the parent's remaining cap
allows it. Such slack can reduce the child's expected cost. A shared budget
state gives the exact ordinary constrained-policy recurrence.

For a partial state s and permitted future worst fee B, define E_s(B) as the
least expected future fee under the given full-support source distribution.
Terminal states have E_s(B)=0 for all B>=0. Otherwise

```math
E_s(B)=\min_{i:c_i\le B}\left[c_i+
\sum_{v\in S_i}p(v\mid s)E_{s\cup\{i=v\}}(B-c_i)\right].
```

An unavailable child value is infinity, so the selected policy must meet the
cap on every admitted branch. The recurrence follows by conditioning on its
first query. Conversely, combining the finite child policies realizes every
finite candidate. Induction on the number of unknown coordinates proves
optimality. The minimum finite B equals the minimax fee. Larger budgets can
lower expected fee; B=sum all remaining query fees is unconstrained expected
optimization. This is ordinary finite-state constrained dynamic programming.

Use the existing op01 fully checked stopping-state table, which contains every
alternative query branch before any terminal state. Its original construction
and optional scientific optimality reconstruction are not newly performed
work. A service using the table must allocate its actual construction bill;
the scientific comparison may cite the already checked source/hash. A selected
budget policy needs only the original action/branch safety check to act.

**Prospective pt01:** for every24 exposed op01 duties, compute exact rational
E_s(B) for all integral caps through the sum of public query fees. Record the
root tradeoff curve and a selected safe policy at the minimum feasible cap and
at the unrestricted cap. Independently evaluate the resulting policy on every
supported world, verify its declared worst and expected fees, and compare
existing minimax, cheapest full-frontier, and dr01 DIRECT policies. Check that
the original minimax root value equals the first feasible budget. This is a
zero-physical-query diagnostic; do not claim a measured acquisition saving
until an actual paid service is separately declared and run.
