# What the exposed repair bank establishes

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT, same-model.
One execution of [the frozen probe](retention_check.py), under its
[prospective contract](retention_probe.md), produced [this result](retention_result.json).
Source SHA256:ca2858a1f08399f33057609c2ec123ab99ede3acc4b2ac887d0eb39ebce5c046.
Python3.12.14; measured execution7,750,000,000ns. No new solver calls and no
exact-optimum diagnostic. All old proof and witness checks were repeated:
4,374 shared-admission units plus3,601 proof/profile units.

The bank has16 public incumbents,13 optional feasible witnesses and18 optional
negative proofs. Its31 optional receipts concern16 separate sources; their
small blocks have only68 local subsets altogether. Exact source-wise dynamic
programming takes709 combination transitions for every retention budget.
It is an ordinary exact algorithm and is also our strongest selection control.

| On the same80 exposed contexts | Tree-leaf profiles | Transported scalar cuts |
|---|---:|---:|
| Baseline closures, public incumbent/zero lower/replacement only |4|4|
| Full31-receipt-bank closures |55|51|
| Fewest receipts matching those full-bank closures |27|27|
| Full-bank bound-evaluation tariff on all contexts |10,655|5,905|
| Selected27-receipt bound-evaluation tariff |9,060|5,005|
| Sum of optional compact JSON payload bytes, full / selected |1,150 /999|1,253 /1,062|
| Pairs closing a context that neither member closes alone |11|11|

The tree bank can therefore discard four optional receipts without losing any
of its55 closures on this panel, reducing this particular warm evaluation
tariff by1,595 units (about14.97%). This is not a total counted-computation
reduction: table construction itself costs10,655 units, bank selection is
additional, and neither future frequencies nor amortization are established.
Source admission, dispatch overhead, raw proof retention and runtime memory
are not those compact payload bytes. The full bank was already small.

At budget10, exact tree selection closes31 contexts, singleton closure greedy
30, continuous-gap greedy24 and pair-at-a-time greedy31. At budget14 the
counts are39,37,28,39. These examples confirm that maximizing bound reduction
and maximizing decisions settled can differ on real archived proof objects.
They do not establish superiority over existing exact selection. Pair greedy
also loses to the exact control at budgets13 and15. At budget27 every method
reaches the full tree bank's55 closures.

The deliberately extensive greedy comparison costs far more than the small
exact dynamic program: the tree arm evaluated100,052 global candidate banks,
1,600,970 local banks and3,491,315 retained-value comparisons; the scalar arm
evaluated86,583 global banks,1,385,466 local banks and3,298,915 comparisons.
These include overlapping internal counts, so summing them as if disjoint
tariff categories would double count. They are a transparent implementation
bill, not a new provider invoice or a reason to prefer brute-force controls.

The frozen initial bank is different from s05's adaptive stream. That stream
acquired new receipts and closed61 versus57 requests from its changing cache;
our55 versus51 cannot replace those old metrics. No source fee saving is
measured here. A trusted compiled bank remains grounded in the repeated raw
source/proof checks; hashes alone do not prove its claims.

## Constructive disposition

Retain the complementary-certificate abstraction and its simple conditional
coverage result. The archive supplies a natural instance of complementarity,
not just an XOR toy. Small independent source blocks admit exact budget
allocation, and ordinary exact allocation ties. An economic contribution would
need a credible memory/query regime and comparison with ordinary cache
compression or solver retention. Do not spend this recurrence tuning these
eighty old contexts or treating the14.97% warm-evaluation figure as an overall
gain. The next broader question is how retained existential information can
support new actions when its witnesses are unavailable or change validity.
