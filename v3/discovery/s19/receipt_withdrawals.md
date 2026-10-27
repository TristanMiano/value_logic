# Withdrawal-cost profiles for fallible scalar receipts

Codex (GPT-6), October 26, 2026. DEVELOPMENT; derived and finitely checked extension.
The core is ordinary maximum-consensus/weighted-repair reasoning.

Assign a nonnegative declared withdrawal price w_j to old receipt j. For a
subset G of retained receipts, let V_G be its exact attainable future-value
set from anchor_ranges.md. The cost of making a proposed future value q
compatible is

    D(q) = min_(G: q in V_G) sum_(j not in G) w_j.

If q is impossible even after all receipts are withdrawn, D(q)=infinity.
Weights are decision costs or declared trust penalties, not probabilities.
With unit weights D(q) counts the fewest old observations that must be
withdrawn to admit q. A claim that at most s receipts are wrong warrants
only the union of V_G over |G|>=k-s. Choosing a minimum-cost repair does not
establish that the true source lies in that repair when s is unknown.

The local slices now depend on both G and T subset G: apply lower constraints
only for j in G, and upper witness constraints for j in T. There are3^k
(G,T) pairs. Thus at most2*n*3^k local LPs suffice for all subsets G. The
anchored recurrences over all G take O(n*4^k) split work since
sum_(G subset K) 3^|G|=4^k. At most n*3^k labelled intervals result before
merging; a sweep of their endpoints constructs the lower envelope of the
withdrawal costs. Endpoint inclusion must be retained exactly because a
singleton compatible value can have a smaller repair cost than its neighbors.

This profile can explain why a new scalar report conflicts with a retained
model and how many or which weighted observations need revision. It does
not identify the unreliable report or make a repaired source empirically
adequate. Its generic mechanism is familiar repair; any new value would be
the structured resource bound or a demonstrated service consequence. Keep it
as a separate extension rather than adding it to the core range claim.

## Executed profile check

The [frozen source](withdrawal_check.py), [plan](withdrawal_plan.json) and
[result](withdrawal_result.json) check every retained subset for40 exposed
polygon cases, then compare each resulting range with exhaustive attainer
assignments. A closed-endpoint heap sweep is checked at every endpoint and
every open cell midpoint against the exhaustive minimum repair price.
All364 profile atoms have matching prices and recovered source witnesses.
There are80 endpoint price drops relative to an adjacent open cell, so
discarding singleton/endpoint distinctions would lose actual information.

The panel evaluates6,432 local slice entries,70,470 subset split candidates
and16,748 reference assignments. These units differ and are not a speed
comparison. Runtime834,396,600ns includes the separate worked example.
The producer uses exact two-dimensional clipping; generic rational LP
production and full repair-certificate checking are not implemented here.

The full-dimensional noisy example in robust_gap.md adds7 checked atoms
and7 source witnesses. With withdrawal prices1 and2, the old records imply
[21,21.2] union [21.9,22.2], while accepting21.5 requires minimum withdrawal
cost1. This says what the specified revision criterion costs; it does not
establish that the cheaper-to-withdraw record is false. A direct ordinary
weighted consistency optimization obtains the same answer for one quote.
The whole profile is relevant only when many values or budgets are queried.

No internal atom has infinite repair cost in this panel. With all receipts
withdrawn, the compact product source is connected and its continuous
minimum has an interval image; every value inside that unrestricted interval
has some finite repair price. Values outside it remain impossible even after
all withdrawals. This endpoint characterization is mathematical, not an
additional executed test of arbitrary outside inputs.
