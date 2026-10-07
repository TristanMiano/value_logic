# Frontier capacity and syntactic ordering: static review

**Status:** mathematical and read-only algorithm review; no executable cases run for this review. Any later probe is separate DEVELOPMENT evidence. This concurrent same-model review receives **zero additional time credit**.

**Inspected implementation:** [03_bounded_logic.py](../../../checks/03_bounded_logic.py), especially `Kernel._source_step`, `Kernel.run`, `tri`, `interval`, initialization and the report's `source_exactly_filtered` field. The inspected mathematical kernel is `finite-cover-v1`; the report interface is `finite-cover-report-v2`. The claims below describe the current committed-transition semantics, not a proposed replacement algorithm.

## 1. Setting and operational assumptions

There are $`k`$ active Boolean coordinates. A cell is an ordinary cube in $`\{0,1,*\}^k`$, and the initial frontier contains the all-star cube. `_source_step` pops the first queued cell, tests accepted constraints in their stored order, and then:

1. Deletes a cell if a constraint has Strong-Kleene value false throughout it.
2. Records a feasible singleton if the cell is fully fixed and no constraint rejected it.
3. Requeues a non-singleton unchanged if the committed cell count is already at `cell_cap`.
4. Otherwise replaces it with both children obtained by splitting its first free coordinate, appending those children to the FIFO queue.

The examples fix the query catalogue, accepted constraints and loss throughout refinement. There are no incoming literal receipts, source withdrawals, or other requeues. One may use opaque queries and `mode="source"`. Finite calls to `run` continue to respect their transaction allowances; a stalled frontier does not mean a single call blocks indefinitely. Termination claims require enough subsequent source service. They do not assume that a single fixed finite allowance suffices for every instance.

The cell cap bounds the frontier at observable committed boundaries. The current replacement constructs two children and updates the dictionary before deleting their parent. Starting with $`N`$ committed cells, this can temporarily leave $`N+2`$ dictionary entries and then commit $`N+1`$ cells. A committed capacity result is therefore not a total allocation, peak byte, or CPU bound.

## 2. Parity: minimum exact representation

Let $`k\geq2`$, and let the accepted conditional source constraint $`H`$ be odd parity. Write

```math
S=\{x\in\{0,1\}^k:\text{the number of 1 entries in }x\text{ is odd}\},
\qquad C=2^{k-1}.
```

Every cube with a free coordinate contains both an odd-parity and an even-parity assignment: hold the other coordinates fixed and flip that coordinate. Consequently, no non-singleton cube is contained in $`S`$. An exact union of ordinary cubes representing $`S`$ must therefore use at least $`C`$ singleton cells; those $`C`$ satisfying singleton cells suffice. Overlapping cubes do not avoid this obstruction, because union cannot remove the unwanted even assignments from a non-singleton cube.

This is a lower bound for **exact representation as a union of ordinary cubes**. It is not a universal space or computation lower bound. A symbolic parity formula represents the same finite source much more compactly, and an ordinary solver may reason directly with that formula.

## 3. Why the current algorithm stalls at cap $`C`$

A proper partial assignment extends to both parities. Soundness of Strong-Kleene evaluation prevents the parity formula from being definitely false on any such cube. In fact it cannot be definitely true there either. On singleton assignments, the supported Boolean interpreter agrees with the ordinary Boolean truth table.

Before the final depth, therefore, there are no pruning operations. FIFO order and the first-free-coordinate rule build complete breadth levels. After $`C-1`$ splits, the frontier consists of exactly $`C`$ cells, each fixing the first $`k-1`$ coordinates and leaving the last coordinate free.

At cap $`C`$, all these cells are non-singletons, none can be pruned, and every attempted split is rejected by the capacity guard. Each attempted source transaction rotates one cell to the back of the queue without changing the frontier. Continued service repeats this configuration indefinitely.

The source remains nonempty and the cover remains sound. The kernel has not found a witness through singleton processing and has not obtained an exactly filtered source. This is a refinement obstruction, not a conflict certificate. In particular, capacity sufficient to store the final exact representation need not suffice for the implementation's intermediate committed states.

## 4. Why cap $`C+1`$ suffices, and what FIFO revisits cost

After the same $`C-1`$ initial splits, there are $`C`$ one-free-coordinate parent cells. At cap $`C+1`$, the first such parent can be split into two singleton children, bringing the committed frontier to $`C+1`$ cells.

Suppose $`r`$ one-free-coordinate parents remain after this split. They precede the two new children in the FIFO queue. Each encounters the full frontier once and moves to the queue's tail. The two children are then processed consecutively, before those requeued parents. Exactly one child is rejected by parity; the other is a feasible singleton. After both child transactions the frontier has $`C`$ cells again, and the queue consists of the remaining $`r`$ parents.

This is an induction invariant. Every remaining parent can in turn be split; its false child eventually releases the required slot. After all $`C`$ final parents have been processed, the frontier contains the $`C`$ satisfying singleton assignments and the agenda is empty. Thus committed cap $`C+1`$ suffices for termination in this fixed-source scenario with continuing service. No fair retry assumption beyond the actual FIFO requeue mechanism is needed here.

The exact source-transaction counts in this scenario are:

| Operation | Count |
| --- | ---: |
| Successful splits before the one-free-coordinate level | $`C-1`$ |
| Successful final-coordinate splits | $`C`$ |
| False-singleton prune transactions | $`C`$ |
| True-singleton feasibility transactions | $`C`$ |
| Capacity-stop transactions | $`\sum_{r=0}^{C-1}r=C(C-1)/2`$ |

Therefore the total number of source transactions through empty agenda is

```math
(2C-1)+2C+\frac{C(C-1)}2
=4C-1+\frac{C(C-1)}2.
```

The $`2C-1=2^k-1`$ successful splits and $`4C-1=2^{k+1}-1`$ distinct tree-node visits are familiar full binary-tree counts. **The distinct-node count does not bound all source transactions when capacity stops revisit queued cells.** The extra term above is a concrete correction for this particular FIFO parity run. It does not count dispatcher checks, input admission, reporting, hashing, or scheduled evidence work as free. Those have their separately recorded accounting.

The exact count assumes the initial all-star frontier, a single fixed parity source, the existing FIFO child insertion order, and no external agenda changes. It should not be reused as an exact count for arbitrary constraint systems or resumed states. With committed cap at least $`2^k`$, a general finite Boolean instance never needs a capacity stop during ordinary complete splitting, giving the usual distinct-node bound as a sufficient source-work bound for that more generous capacity regime.

## 5. A lookahead operation could finish parity at cap $`C`$

Consider an alternative transition that constructs and tests both children before atomically replacing the parent with all children that are not definitely false.

At earlier parity levels, both children survive and the frontier grows toward $`C`$. At the final one-free-coordinate level, exactly one singleton child survives. Replacing each parent with that child preserves a committed count of $`C`$ and eventually yields the exact source at that capacity.

This is a constructive alternative for the named example. It requires charged child evaluations, safe temporary storage and an appropriate atomic commit. It is **not** the current `_source_step`, which commits both children before a later transaction checks either. It also does not prove that a minimum final representation capacity suffices for every possible source under lookahead.

## 6. Syntactic coordinate order can dominate interval refinement cost

Now take no source constraints and no acquired evidence. Let the last coordinate be $`x=x_{k-1}`$ in the kernel's zero-based indexing, and use the permitted loss expression

```math
f(x)=\min(x,1-x).
```

The subtraction is representable by `add` with a known negative rational `scale`. The structural interval interpreter returns $`[0,1]`$ whenever $`x`$ is free: it separately encloses $`x`$ and $`1-x`$, then applies the interval extension of `min`. Once $`x`$ is fixed to either Boolean value, the returned interval is $`[0,0]`$. Thus the actual loss is always zero, but the unsplit structural enclosure need not recognize the shared dependence.

For a union of cells, a single cell with free $`x`$ keeps the global upper bound at one. With the current first-free-coordinate rule, every earlier coordinate must be fixed on a branch before $`x`$ can be split. There is no pruning in this example. Consequently, reaching global upper bound zero requires all

```math
2^k-1
```

splits of the complete binary tree and retains all $`2^k`$ singleton cells. Committed cap at least $`2^k`$ is necessary for this run to reach upper bound zero. A smaller cap can leave the bound permanently at one even though the exact loss is zero everywhere.

Under FIFO and sufficient capacity, all internal-node splits occur before singleton processing. A report immediately after the last split already has bounds $`[0,0]`$; `source_exactly_filtered` remains false until the agenda's singleton checks are completed. The numerical loss duty and the implementation's complete-filtering flag therefore have different stopping times.

An alternative relevant-coordinate-first rule splits $`x`$ at the root. Its two children each have exact loss interval $`[0,0]`$, even though the other $`k-1`$ coordinates remain free. One split and committed cap two suffice for that loss-bound duty. For $`k=1`$, both orders require one split; the separation is substantive for $`k\geq2`$.

The present kernel has no selectable coordinate heuristic: it uses `cube.index(None)`. Reordering the query list and consistently transporting expression indices can put the relevant coordinate first without changing the represented loss problem. It does change the executed priority rule relative to the semantic queries. An exact mathematical recoding therefore does not by itself establish identical bounded traces or acquisition/refinement costs; a cost-preserving comparison must also transport the scheduling contract.

An ordinary Boolean simplifier can prove $`f=0`$ without any splitting. This example diagnoses a particular interval expression and scheduler, and does not establish a general lower bound on solving the task.

## 7. Executable admission and remaining boundaries

The parity argument is mathematical for arbitrary finite $`k`$. Executable examples must satisfy the actual fixed caps, including at most 12 atoms, 4,096 committed cells, 256 expression nodes and depth 48. There is no primitive XOR in the Boolean syntax: the supplied source must use supported `and`, `or` and `not` expressions.

For an explicit admitted scale, use a balanced recursive XOR expansion

```math
X(A,B)
=(A\land\neg B)\lor(\neg A\land B)
```

This uses $`s(1)=1`$ and $`s(2m)=4s(m)+5`$ expression nodes when the two subexpressions have equal sizes. Hence a balanced eight-coordinate parity expression uses $`s(8)=169`$ nodes, fits the expression-depth cap, and has $`C=128`$ with the corresponding committed caps 128 and 129. This establishes an available encoding, not a minimal-formula theorem or a claim that every larger encoding is admitted. No instance was executed for this review.

The source constraint is explicitly conditional caller input. The kernel's Boolean cells describe the active finite assessment fragment; the parity example does not turn that fragment into complete arithmetic models or supply an oracle for mathematical truth. All conclusions rely on the fixed source and specified representation, transaction and scheduling rules.

**Review conclusion:** the proposed cap-$`C`$ obstruction, cap-$`C+1`$ constructive completion, and last-coordinate ordering separation are correct with the stated scope. The material correction is to distinguish successful splits and distinct tree nodes from all charged source transactions, because the current retry queue can incur $`C(C-1)/2`$ extra capacity-stop transactions in the parity example.
