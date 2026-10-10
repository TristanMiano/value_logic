# Prospective ADD dependency-pruning check

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
**R-P3-B-B DEVELOPMENT; post-primary-exposure exploratory strengthening.**
**Zero principal research-clock credit.** Save this plan before executing or
importing the new pruning implementation. Existing producer, checker, service,
fixtures and primary source snapshots remain unchanged.

## Question and fixed implementation

Can a warm ordinary ADD producer deliver only the current proof's required
dependencies to a fresh receiver? The existing full exporter includes historical
facts no longer needed by the current request. A small final zero root alone is
insufficient: the receiver must still reconstruct the current hard conjunction,
rank sublevel, loss expression and violation goal from checked premises.

Create only `v3/checks/05_add_evidence_prune.py` and new files in this review
directory. The proposed APIs are:

```python
prune_full(evidence, current, witness, bound, expected_record,
           *, work=None, limit_steps=8_000_000) -> E.AddEvidence

export_pruned(manager, current, witness, bound, expected_record,
              *, work=None, limit_steps=8_000_000) -> E.AddEvidence
```

The convenience function pays the ordinary full export before pruning. It does
not invoke a receiver or a truth oracle. `prune_full` accepts only the exact
immutable full evidence type with zero base counts. It binds the caller's frame,
witness and bound to the evidence, scans/indexes the existing facts, seeds every
current hard/soft/difference expression and the exact goal operations, closes
over required expression and recursive Apply premises, retains every referenced
node and its children, and remaps node identifiers in increasing original order.
Relative identifier order is preserved, including canonical commutative keys.

The result preserves the source record, epoch, bits, order, current record,
witness and bound. It is a full v1 packet for a fresh unchanged receiver. This is
dependency pruning under the existing proof rules, not proof minimization or a
new inference rule. The unchanged receiver remains the authority. Missing
required facts, unsupported input mode or exhausted pruning limits fail closed;
no partial proof gains a certificate.

## Source and cost assumptions

The expected source record must already describe the actual production closure,
including the pruner and any common wrapper. Pruning preserves that record; it
does not authenticate a different source or silently rewrite provenance. The
check will freeze the old six-file evidence closure, new pruner, fixed fixture
file and exact harness before execution and verify their hashes afterward.
One fresh process loads that closure using the established shared module names.

The inherited limits remain: 1 through 10 bits, at most 100,000 node facts,
200,000 Apply facts and expression bindings, and 32 MiB output wire. The new
pruning guard is fixed at 8,000,000 dependency steps. Its explicitly counted
table visits, key characters, dependency accesses and output records are a
finite local guard, not a replacement for the complete service tariff. The
later root wrapper must meter full export, validation, indexing, closure,
remapping and serialization. The warm manager is retained and charged in full;
pruning does not shrink it. No production cache or free receiver result is
retained by the new function.

The present check reports exact fact counts and wire bytes, with producer,
pruner, full-receiver and pruned-receiver diagnostic work kept separately. It
does not report a complete scalar bill or infer a total-cost improvement from
smaller output. Receiver execution order is fixed: unpruned full first, pruned
full second, each in a different empty receiver with the same independently
supplied request and source. Neither receiver's report feeds production.

## Fixed inputs and checks

Use the unchanged fixture file SHA
`adfcaf7733b6b401033a7689815c277f746f8fcfe47c1ec7e1733ae8142ca163`:

| Stream | Bits | Current requests |
| --- | ---: | ---: |
| `constant_n3` | 3 | 6 |
| `parity_reassociation_n6` | 6 | 6 |
| `complementary_k3_n5` | 5 | 6 |
| `complementary_k5_n7` | 7 | 6 |

Start one empty warm manager per stream in the fixture's declared order and
process its six current edits in their existing order. Do not bootstrap old
domains or change any input, bound, witness or edit. For all 24 requests, preserve
the full and pruned packets, separate exact receiver reports/work, counts,
serialized warm state bytes and pruning diagnostics. Require both fresh receivers
to certify the exact common mathematical fields. Remapped internal identifiers
and admitted fact counts may differ.

Also perform these fixed focused checks, without tuning after their outcomes:

1. The first parity request in reverse coordinate order, to exercise order-aware
   Apply cofactors and monotone identifier remapping.
2. Idempotent pruning of the last complementary-k5 pruned proof: the second
   result must have identical canonical bytes.
3. Delete the required top-level bad-set Apply fact from the first parity proof.
   The pruner and the unchanged receiver must reject the missing dependency;
   the receiver must retain no admitted facts after rejection.
4. Present a genuine zero-based-prefix delta sliced from the second parity full
   proof. The full-only pruner must reject it rather than treat unknown prior
   state as free evidence.
5. Give the first parity full proof a one-step pruning limit. Preserve the paid
   failure counters and verify that the immutable input is unchanged.
6. Request the false one-bit bound with loss `bit(0)`, no hard/soft rows,
   incumbent `(0,)` and bound zero through `export_pruned`. Preserve the ordinary
   producer's actual violating point `(1,)`; do not manufacture a zero proof.

Retain every first execution, unexpected failure and source revision. Corrections
require a new versioned snapshot/output directory and an explanation. No method
or threshold is selected from these results, and no primary result is rewritten.
An independent source review of closure logic may follow when the integration
reviewer is free. The stopping point is a working bounded exporter, this fixed
check record and a source-bound handoff, not an open-ended pruning search.
