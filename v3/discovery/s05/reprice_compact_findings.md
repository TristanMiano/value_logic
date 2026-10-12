# Exact profile compression with an explicit setup bill

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. [Implementation](reprice_compact.py),
[results and complete named-operation invoices](reprice_compact_results.json).
Inputs are the preserved [repricing profiles](maxsat_reprice_results.json)
and their [original proof/witness evidence](maxsat_repair_results.json).
No new solver call or optimum diagnostic was made.

## Constructive result and its price

The compact representation preserves the original transported lower profile
and best retained-witness upper profile **exactly**, for every nonnegative
weight vector on the same soft clauses. On the five already exposed weight
edits, per-edit tree-profile service cost falls from **2,283 to 752 units**
(67.1%). The additional compilation bill is **5,943 units**, so the method
costs more on the first three edits and first repays its setup on the fourth.
After five edits its full bill is **17,678**, versus **19,390** for raw trees.
This is an 8.8% reduction under this declared operation tariff.

Storage does **not** improve after adding the shared sum DAG. Logical
persistent payload grows from 455 to 487 words, with another 56 DAG workspace
cells. Fewer retained receipts therefore do not imply a smaller full service.
The stronger scalar control remains cheaper and keeps its weaker certificates.

These are alternative service bills from the same admitted receipt archive.
The exploration does not refund the earlier run or erase its common historical
solver-acquisition bill of 77,646 units. No claim about production solver
runtime, currency, unseen weight edits, or a new optimization principle follows.

## Why the representation is exact

For a violation mask a, its repriced cost is `a dot w`. If a is a subset of b,
then `a dot w <= b dot w` for every w>=0. Thus, within a row's witness set,
discarding supersets preserves the minimum objective U(w). Within one negative
tree's soft-leaf family, discarding supersets preserves its minimum lower
profile L_T(w). Equal masks retain their earliest representative. When some
weights are zero, an optimal retained assignment can differ from the original
tie choice, but its objective value and hard feasibility remain valid. No tie
changed in this particular five-edit comparison.

There is also a sufficient relation between whole tree families A and B:

```text
For every b in B, some a in A satisfies a subset-of b.
Then min_(a in A) a dot w <= min_(b in B) b dot w for all w>=0.
```

Tree A can consequently be removed from the outer maximum defining L(w).
Mutual domination uses the earliest original tree as the tie representative.
Strict dominance is transitive; a removed tree may point to another removed
tree, with the chain ending at a retained stronger tree. The saved reduction
certificates record the actual decisions. Rows without a negative tree retain
lower bound zero. A public feasible witness ensures every row keeps a usable
upper bound. The implementation rejects negative weights and changed source
identities; these reductions do not justify changing clauses or their meanings.

The compiler then inserts all retained witness/leaf masks into one DAG, sharing
arithmetic across rows as well as across receipt types. The recurrence was fixed
before execution:

```text
sum[0] = 0
low    = mask & -mask
parent = mask ^ low
sum[mask] = sum[parent] + weight[index(low)]
```

Parents are emitted before children by a deterministic depth-first traversal.
Each distinct nonzero mask sum is evaluated once per edit. No choice of bit,
mask order, reduction strategy, or tariff was tuned after observing its bill.
Arithmetic sharing does not transfer feasibility between rows: each row still
selects only its own checked witnesses and uses only its own checked trees.

## Counts, bills, and fair controls

| Quantity | Original raw tree service | Compact tree service |
|---|---:|---:|
| Feasible witness receipts | 29 | 23 |
| Negative tree profiles | 18 | 14 |
| Soft-leaf mask occurrences | 147 | 77 |
| Shared nonzero sum nodes | 0 | 55 |
| Witness/tree payload before DAG | 455 | 321 |
| Persistent payload including DAG | 455 | 487 |
| Additional DAG workspace cells | 0 | 56 |

Storage counts use the original n+2-word witness convention, one word per tree
header/mask, and three words per DAG instruction. They exclude unchanged clause
and proof archives, common row metadata, Python container overhead, and execution
stack. They are not byte counts or complete process memory measurements.

The new scalar control receives the same witness reduction, a witness-only DAG
(32 nonzero nodes), and shared once-per-vector delta/ratio arithmetic. It retains
the original additive-plus-ratio lower bound exactly. It pays for its own DAG
and only its required witness compilation. This prevents a tree-method benefit
from being manufactured by withholding cheap witness reuse from the control.

| Service | Full one-time setup | Per edit | Total after five edits |
|---|---:|---:|---:|
| Original raw tree | 7,975 | 2,283 | 19,390 |
| Compact tree | 13,918 | 752 | 17,678 |
| Original additive + ratio scalar | 4,374 | 1,163 | 10,189 |
| Compact additive + ratio scalar | 5,233 | 535 | 7,908 |

The full compact-tree setup consists of 4,374 shared original admission/witness
units, 3,601 original proof-check/leaf-compilation units, 404 witness-reduction
units, 4,577 leaf/tree-reduction units, and 962 DAG-compilation/storage units.
The original profile writes remain charged even though transient raw profiles
can later be released. Leaf subset scans alone cost 4,154 units: setup is a real
bottleneck, rather than a nominal constant hidden by the presentation.

Each compact-tree edit charges 8 weight-admission units, 386 DAG evaluation
units, 46 witness-selection units, 168 tree-selection units, and 144 price-report
units. Seven units are charged for each DAG node evaluation: three instruction
word reads, two operand reads, addition, and result write. All invoice categories
are in the result file. Hashing, JSON transport, Python bookkeeping, and research
report serialization remain infrastructure outside the service tariff, as in
the original experiment. No CPU-instruction interpretation is intended.

For k future edits from an existing raw profile, conversion costs `5943+752*k`
against `2283*k` without conversion. The crossover is k>=4 under this tariff.
Compact scalar compilation repays itself at the second edit. The compact tree
still costs 217 more units per edit than the compact scalar service, and 8,685
more setup units. Tighter certificates have a price even after compression.

## Preserved precision, zero gains, and checks

All five exposed recipes are retained: identity, uniform doubling, first-half
doubling, last-half zeroing, and right rotation. Identity and uniform doubling
still have no tree-precision advantage over the ratio control. The reductions
do not create a new certificate or improve its numeric value. They preserve the
prior constructive gains, including the three new exact optimum certificates
under last-half zeroing, while lowering recurring service cost.

The single executed run rechecked the original proof/witness archive, reproduced
both original setup invoices, and matched all **80 row-edit** lower and upper
profiles to the saved repricing results. The compact scalar lower values also
match all 80 saved scalar values. No exact-optimum field was used. All source and
prior-result hashes remained unchanged. These finite comparisons check the
implementation on the exposed workload; the subset and recurrence arguments
give the stated all-nonnegative-weight validity. This remains a small development
probe with an explicit time/storage tradeoff, not a readiness claim.
