# Recorded ADD dependency pruning: implementation and first results

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
**R-P3-B-B DEVELOPMENT; exploratory extension after primary exposure.**
**Zero principal research-clock credit.** Existing workers, primary snapshots,
inputs and results are unchanged. The prospective `plan.md` was preserved before
the first import or execution of the new implementation. No parameter or method
was selected from these results.

## 1. Deliverable and precise scope

The new standalone `v3/checks/05_add_evidence_prune.py` removes historical facts
that the unchanged fresh ADD receiver does not need for the current request. Its
first fixed check passed all 31 recorded events, including 24 comparisons on the
existing six-edit streams, without an unexpected failure or source correction.

The new file has version `rp3bb-add-evidence-prune-v1` and SHA-256
`eac1fe24bf0643990d98e229724c7d9642e50d0b7a0fe4fd961b3b04fcb818e5`
(17,079 bytes). It exposes:

```python
prune_full(evidence, current, witness, bound, expected_record,
           *, work=None, limit_steps=8_000_000) -> E.AddEvidence

export_pruned(manager, current, witness, bound, expected_record,
              *, work=None, limit_steps=8_000_000) -> E.AddEvidence
```

`prune_full` consumes the exact immutable full evidence object with zero base
counts. `export_pruned` first calls the unchanged full object exporter, then
prunes that object. It does not first encode and decode a redundant full JSON
packet; the comparison harness encodes the full packet because that is the
unpruned comparator's actual output. Neither production function imports or
calls the independent receiver, consumes a successful report, or evaluates a
private truth table.

The result is another immutable full v1 evidence object. Encode it with the
unchanged `E.to_wire`, and supply it to a new empty v1 receiver with independently
fixed source record, epoch, bits, order, current frame, witness and bound. The
pruner never returns a resident delta or a receiver receipt. A pruned node ID is
not a continuation of the original manager's node numbering.

## 2. Dependency closure and soundness rationale

The procedure first indexes the supplied full node, Apply and expression tables.
It binds the caller's exact current record, incumbent and rational bound to the
packet, checks incumbent feasibility and derives the current rank cutoff.
It then repeats the receiver's current-goal linkage operations over existing
facts, starting from the zero and one terminals. Seeds include every current
hard formula, every current soft formula and weight, the complete difference
expression, the cutoff and bound tests, and all operations combining those roots
into the current violation goal. It does not start only from the final zero root.

For each required expression binding, its literal/bit definition or complete
child bindings and associated Apply fact are retained. For each required Apply
fact, both operands and the output node are retained. When receiver v1 uses a
same-operand identity, terminal arithmetic or a controlling constant identity,
there are no recursive Apply premises. In every other case, the pruner retains
both cofactor Apply facts for the earliest coordinate in the declared order,
then follows their dependencies. Required Apply and expression predecessors
must precede their dependents in the original tables. Every retained decision
node recursively retains both children.

Emission filters the original Apply and expression sequences in their original
order. Retained node IDs are sorted in increasing original order and mapped
injectively to consecutive IDs. This preserves back references and strict
relative ID order. It therefore also preserves the canonical operand ordering
of every commutative Apply key. Node definitions, expression keys, metadata and
the claim's mathematical values are unchanged; only references are renamed.

Assume the original full packet is accepted by the fixed v1 receiver. Node
induction survives the injective renaming. Every retained Apply check has the
same terminal or identity case, or the same already-checked cofactor premises,
as before. Every retained expression check has its required child definitions
and operation fact. Finally, every lookup in the receiver's reconstruction of
the independently supplied current goal is seeded and retained. The claimed
roots and the zero terminal are consistently renamed. Thus the receiver can
repeat the same checks on the pruned packet and establish the same bound.

This is a dependency-preservation argument for the fixed proof rules, not a
formal verification of Python or a new inference rule. The pruner is not a
validator of the original full packet: malformed dead facts might be discarded,
and malformed retained facts must still be rejected by the receiver. In
particular, the pruner does not independently recompute every terminal Apply
equation. A pruning result has no certificate authority before receipt.

The implementation is called **dependency pruning**, not a minimum proof. It
preserves the existing expression compilation proof and does not search for
alternative derivations, algebraic rewrites, different variable orders or a
smaller semantic certificate.

## 3. Source, budget and retained-state obligations

The source record is preserved exactly. It must already describe the actual
closure including this module and any common wrapper. The new `SOURCE_PATHS`
constant extends the existing six-file evidence closure with this file; the
check adds the unchanged fixture file. A future service wrapper must extend its
actual source enrollment consistently. Pruning does not add its source hash to
an already-issued packet or authenticate a foreign source record.

The inherited caps remain 1 through 10 bits, 100,000 nodes, 200,000 Apply facts
and expression bindings, the existing rational bounds and 32 MiB output wire.
The separate dependency guard is fixed at 8,000,000 steps. It counts explicit
table visits, key characters, dependency accesses and emitted records. A smaller
supplied guard produces a `PruneLimit` with the used, requested and allowed step
counts. It returns no partial output.

These steps are a local termination/resource guard, not units of the common
event/byte tariff. Exact arithmetic, input validation, Python indexing and
hashing, allocation, sorting, output-object validation and serialization still
execute and must all be charged by the enclosing worker meter. The input-table
scan and temporary indexes scale with the supplied full history, even when the
result is much smaller. The convenience path includes the initial full object
export. No full history or parsing work is supplied by a free oracle.

The full warm recording manager is unchanged and remains retained. The check
compares its complete serialized state before and after pruning on every
request. Pruning does not shrink its node table, cache keys, Apply/proof logs or
expression tables. The pruner's indexes and marked sets are temporary; it stores
no scientific state between calls. A later complete comparison must charge the
full warm manager and the smaller fresh receiver state under the same declared
storage convention. The present wire counts do not establish a total-cost gain.

## 4. First fixed results

One empty manager was created for each existing stream and used for all six
current edits in the already declared order. Old-domain bootstrap inputs were
not used by these ADD arms. For every request, the unchanged receiver checked
the unpruned full packet first. A different new receiver then checked the pruned
packet. Receiver work, producer work and pruning work are separate event fields.
No receiver report feeds the producer or pruner.

All 24 pairs certified identical common service fields: complete current record,
bound, supplied-incumbent rank, nonemptiness, entire incumbent-sublevel coverage,
source/epoch context and no selected-identity claim. Admitted fact counts and
internal node IDs may differ.

| Existing stream | Requests | Full wire bytes | Pruned wire bytes | Bytes removed | Maximum pruning steps |
| --- | ---: | ---: | ---: | ---: | ---: |
| Constant, 3 bits | 6 | 20,163 | 17,954 | 2,209 | 1,892 |
| Parity reassociation, 6 bits | 6 | 54,271 | 52,060 | 2,211 | 9,120 |
| Complementary domains, k3/n5 | 6 | 48,680 | 42,945 | 5,735 | 8,002 |
| Complementary domains, k5/n7 | 6 | 70,235 | 61,847 | 8,388 | 12,593 |
| **Total** | **24** | **193,349** | **174,806** | **18,543** | **12,593** |

Each stream's first request has identical full and pruned bytes and counts.
All initial facts are needed by that request under the fixed compilation rules.
Pruning therefore adds work without reducing the first transmission in these
four cases. Historical removal becomes possible on subsequent edits. The
largest observed pruning guard use was 12,593 steps; it does not justify lowering
the prospectively fixed guard or claiming a general worst-case bound of that size.

Counts summed over the six separate full deliveries in each stream are:

| Stream | Nodes full → pruned | Apply facts full → pruned | Expression bindings full → pruned |
| --- | ---: | ---: | ---: |
| Constant, 3 bits | 80 → 55 | 207 → 95 | 33 → 24 |
| Parity, 6 bits | 367 → 348 | 925 → 805 | 182 → 174 |
| Complement k3/n5 | 363 → 268 | 917 → 637 | 153 → 148 |
| Complement k5/n7 | 574 → 419 | 1,334 → 970 | 218 → 208 |

These are sums of retransmitted facts, not distinct manager nodes or heap
objects. In the last k5 request, for example, the full packet contains
139 nodes, 319 Apply facts and 41 expression bindings; the pruned packet contains
80, 179 and 37. Its wire falls from 14,438 to 11,149 bytes while the full warm
manager remains unchanged.

### Focused cases and failures

| Fixed check | Result |
| --- | --- |
| First parity request with reverse coordinate order | Both fresh receivers accepted; the separate convenience export path produced the expected pruned proof. |
| Re-prune last k5 proof | Canonical bytes were identical. |
| Delete required top-level bad-set Apply fact | Pruner rejected `Missing required Apply dependency: ('and', 0, 1)`. |
| Give that damaged proof to unchanged receiver | Receiver rejected the missing Apply fact; admitted counts stayed zero and no current receipt existed. |
| Supply a genuine prefix delta from the second parity request | Pruner rejected the non-full/nonzero-base input. |
| One-step pruning guard | `PruneLimit`, with `1+1194>1`; input evidence remained byte-identical. |
| False one-bit bound through `export_pruned` | Ordinary producer raised `NoBoundProof` and preserved actual violating point `(1,)`. |

There are 31 saved events: 24 standard pairs, one reverse-order pair, one
idempotence check, two missing-dependency rejections, a delta rejection, a guard
failure and a false-bound rejection. There were no unexpected failures and no
post-execution implementation changes. Every full/pruned packet, the malformed
and delta packets, exact input records, separate work vectors, reports and warm
state snapshots is preserved in the run manifest.

## 5. Reproduction and hashes

The first immutable source snapshot is `development/v1/source`; the exact plan
and harness are in `development/v1/research`. From the repository root, choose a
fresh output directory:

```bash
PRUNE_SNAPSHOT=v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/ordinary_bridge/dependency_pruning_v1/development/v1
python -B "$PRUNE_SNAPSHOT/research/check_prune_v1.py" \
  --source-root "$PRUNE_SNAPSHOT/source" \
  --out "$PRUNE_SNAPSHOT/reproduction"
```

The harness refuses an existing output directory, verifies source/research hashes
before and after, and saves an explicit failure record on an unexpected error.
It loads no live worker file outside the copied closure. The example command
reproduces diagnostic proof checks; root owns any subsequent metered control.

| Artifact | SHA-256 |
| --- | --- |
| Prospective plan | `d2d72b5e22146078b515b3785af2c04bb6e4ab34f023ea51317edaf2772f0d9f` |
| Harness | `8a9ee1a80fefa3eec1c0a6e12f949ae009d8d091225af81b045fd9ae50e58312` |
| Source/research manifest | `129564f0cf338491cfb99c39d6eb54505f9d2e0f50f943751eddaee79f716f4c` |
| Exact inputs | `18f16c25ff7945ad9125820939847ec02c0c927a3e608858308864d34c88a2bc` |
| Results | `ee96092f6f561c155b5ce724dbd63bca192210737cdac59be06a9be42cdb3cd5` |
| Events | `883f299030c6a253d2239659c100b42d7bfae8a03e6e1d2a8d54d0fa5ce487b7` |
| Run artifact manifest | `1de7b9aeb89f94504848e16dc3538d568c019202bdc511b0140cccb5b58516bf` |

The unchanged producer is SHA
`1e40f1bf7a3cb2dc9cfe46beff9a3548392e99e7ff0fa81a6c79c2f53508bbdc`;
the unchanged receiver is SHA
`1f396bbb625614c87d48fa5fece438851999a7afeb58d5af6933812b4038c2bf`.
All eight source-file hashes and lengths are in the source manifest. Any later
correction must preserve this first source/run and use a new snapshot.

The extension answers a representation question on exposed DEVELOPMENT inputs.
It supplies a stronger ordinary output path and removes a known source of
unnecessary historical replay. It does not claim an optimized proof, a held-out
result, a tuned consumer threshold, or a measured total-cost improvement.
