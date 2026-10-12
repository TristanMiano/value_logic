# A value frontier that asks only for the missing proof work

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT derivation. Read with [the coverage-method bridge](frontier_sources.md),
[retained numeric cuts](value_cuts.md), [partition transport](proof_partitions.md),
and [the actual changed-clause prototype](partition_transport_findings.md).
The local-cube acquisition controller below is prospective; its new-call
bound is not a runtime experiment.

## Two useful frontiers share one paid source

One frontier consists of feasible actions and checked lower constraints on
their possible costs. For fixed soft meanings, let F be all feasible violation
vectors, S the retained feasible vectors, and O an outer relaxation certified
by past proofs. Then `conv(S) subset conv(F) subset O`. A new weight vector w
queries an upper action cost U from S and a lower optimum bound L from O.
It does not require reconstructing the whole feasible set. Previous weighted
value bounds can enter O as their original coefficient inequalities; a learned
or numerical dual proposal can be checked before it supplies a new lower bound.

The second frontier is a covering partition of assignment space. Its cells
retain the conditional source region in which more proof work might help.
After a meaning change, the old numeric constraints may be invalid, while
the same partition can be reinterpreted by checking the current clauses.
The inner action archive is rechecked at the same time. These two frontiers
provide a concrete connection between useful unresolved mathematics, value
queries, and counterfactual revision.

The current all-coordinate binary witness bank already has a precise
compression limit: every distinct subset-minimal mask is uniquely optimal for
some strictly positive weight vector. Generic convex pruning cannot remove
another such mask while preserving all-weight coverage of that bank. A useful
next domain can instead have a small number of meaningful grouped costs or a
declared restricted preference region. This changes the requested value family
explicitly; it does not hide an unfavorable weight query. AOLS-style coverage
acquisition and CMOVE-style factorized coverage are strong existing comparisons,
with their actual scalar calls, vector evaluations and induced-width costs.

## Local acquisition under a fixed current request

Suppose checked cells cover the current hard-feasible assignments. Each cell c
has a valid lower cost ell_c, and a retained feasible action has upper cost U.
Fix nonnegative integer weights, replacement price p and tolerance tau for
this request. Let `A=min(U,p)` and `t=A-tau`. A cell can obstruct the requested
action certificate only when it is currently feasible and `ell_c<t`.

Choose one such cell and make the complete conditional query

```text
Does some current hard-feasible assignment in c have cost <= A-tau-1?
```

A checked feasible witness improves the delivered action cost by at least
tau+1. A checked negative result proves cost at least t throughout this cell,
so this cell no longer obstructs the current requested tolerance. The negative
result is conditional on the cube: it cannot be promoted to a whole-source
refutation unless all other cells are covered too.

Return the repair attaining U when U<p, otherwise replacement. When every cell
is discharged, global L>=A-tau and the delivered action has regret at most tau.
An unresolved capped call supplies neither improvement nor a negative result;
its spent work remains in the invoice. Its best available action and remaining
regret bound are still returnable.

## Why this can be a finite, selectively useful continuation

Let N be the number of initially blocking cells and
`a0=min(U0,p)-min(L0,p)` the initial action gap. Keep the current weights, price
and tolerance fixed during this argument. As improved witnesses lower U, the
required threshold t can only decrease. A cell already discharged at an earlier
threshold therefore remains discharged. Cells that were initially above t
never become blocking. There can be at most N complete negative cell answers.

Every complete positive answer lowers the action cost by at least tau+1, and
the valid initial lower bound prevents it from decreasing without limit. Thus
there can be at most `floor(a0/(tau+1))` such positive answers. A simple bound is

```text
complete conditional calls <= N + floor(a0/(tau+1)).
```

This is a branch-and-bound progress argument at a requested action precision.
It does not bound the work of an individual complete query, the number of
unresolved caps, the size of a retained partition, or the compilation bill.
A single whole-source budget query may be cheaper than many conditional calls.
The value of the partition is the opportunity to reuse already discharged
regions and direct new work to the remaining ones. A strong conventional
controller should receive the same partition and conditional-call interface.

The actual provider adapter must preserve the root cube, variable map and
proof dependencies. A checker for a whole-source proof under added assumptions
can validate a conditional answer, but those assumptions must survive in the
receipt. An arbitrary solver log does not automatically provide a checked
covering partition. After weights or meanings change, run the appropriate
transport rule before reusing any discharged-cell claim.

## Where learning can now enter usefully

Cell choice need not affect certificate validity. A heuristic or learned model
can propose which blocking cell is likely to yield an improved witness cheaply,
which can be discharged cheaply, or which new preference query could supply
evidence useful to many later requests. Checked receipts determine whether the
proposal accomplished either purpose. Useful context includes the current cube,
forced violations, active hard conflicts, retained proof structure and actual
past costs; the optimum value alone does not determine proof-production cost.

Log the actual context, choice, cap, spent work, feasible-action improvement,
new conditional bound and changed cache state. An interrupted attempt is
censored feedback, not an observed refutation. These data are sequential and
selected by the controller; raw averages do not by themselves establish
population calibration or an off-policy value guarantee. Such statistical
claims need a separately justified sampling or exploration contract.

The economic target also needs to remain explicit. Action improvement, a
requested regret certificate, and future reuse are different potential
benefits. A negative proof can tighten the certificate without changing the
current action. Its usefulness should be measured against the actual output
duty and future requests, with computation charged, rather than equating every
interval reduction with realized action gain. The next constructive task is to
build the common callable service and develop acquisition choices within it;
the present examples do not justify freezing one minor choice for confirmation.
