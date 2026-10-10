# Independent receiver focused checks v1

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Same-model independent implementation and source reconstruction. DEVELOPMENT;
zero principal-clock credit. These are functional checks of the new finite
certificate bridge, separate from the parent's resource comparison.

## Result and exact source scope

All **42 fixed probe groups passed**, including 29 expected receiver rejections.
The complete producer/receiver closure was copied before execution, executed
from that copy, and found byte-identical afterward. The seven-file snapshot
includes the six runtime sources and the independent check runner. Runtime:
CPython 3.12.14, Clang 22.1.3. No malformed proof was accepted in this declared
set, and no source correction or retry was needed for this run.

| Artifact | SHA-256 |
|---|---|
| Independent checker, 33,036 bytes | `1f396bbb625614c87d48fa5fece438851999a7afeb58d5af6933812b4038c2bf` |
| Producer and admission adapter, 34,908 bytes | `1e40f1bf7a3cb2dc9cfe46beff9a3548392e99e7ff0fa81a6c79c2f53508bbdc` |
| Complete results | `bd942a12faa59fd0d1571e4b65dc76003f3967aa944c53b7f5e28b1b3c3ef1f0` |

See [source manifest](source_manifest.json), [complete results](run/results.json),
[executed check runner](source/v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/check_receiver_v1.py),
and the [independent design/soundness reconstruction](../receiver_design_v1.md).
Separately, all eleven historical sources read for the reconstruction remain
identical to selected base commit `33c6d6795aac894bd3cf8575e44f1d6f38f6ae56`;
see [accepted source preservation](../accepted_sources.json).

## Positive coverage

A constant bound is admitted in full mode. An edited hard constraint is
admitted on a fork using only its delta facts. The original owner remains
unchanged, and a fresh receiver accepts a subsequent full export containing
all retained facts. Its denotation counts match the resident receiver even
though its receipt history is different. A returned mutable report dictionary
cannot alter the receiver's stored immutable receipt. Retrieval under a
different request id returns no current receipt.

The fixed arithmetic example includes every supported expression constructor,
rational input weights and nested Boolean/numeric expressions. It is checked
under natural and reversed variable orders. This validates these concrete
cases; it is not an exhaustive validation of every admitted expression.

Forward- and reverse-associated three-bit parity produce a checked zero
difference in the DAG receiver. The same ordinary producer also exports a
legacy tree, and the unchanged portfolio verifier independently accepts it
with eight direct leaves and seven splits. Thus the old receiver's exact
format expansion is actually exercised, rather than inferred from the size
of an unchecked ordinary root.

The parity packet contains 19 retained nodes, 44 checked Apply facts and 13
expression bindings. Its full wire is 3,394 bytes and its declared receiver
retention proxy is 4,713 bytes in this source snapshot. These include proof
construction facts, not just the final reduced root. They are **not** a claim
that the full packet is smaller than every legacy proof in this tiny case,
nor a resource advantage after setup, production, transfer and checking.

A rank-zero tied family retains both states with its preferred first bit.
The bound one is accepted for loss equal to the second bit. Trying bound zero
exposes the tied violating optimum `(0, 1)` through the ordinary producer.
A constraint-withdrawal case accepts its initial conditional bound and a
freshly rechecked weaker current bound. An old guarded packet relabelled with
the withdrawn frame is rejected.

## Rejection and ownership coverage

The fixed negative set includes unknown or duplicate JSON keys, invalid UTF-8,
excessive nesting, floating-point input, Boolean node identifiers, unreduced or
nonpositive-denominator rationals, an oversized terminal component, forward
node references, duplicate nodes, a wrong Apply equation, unavailable earlier
Apply premises, missing child expression binding, wrong expression denotation,
and a forged current guard root. It also includes source, epoch, variable-order,
resident-base, incumbent, bound and exact-current-record mismatches.

A constant-zero bad assertion cannot bypass an infeasible incumbent or an
empty current hard domain. Full mode refuses a nonempty resident receiver.
Old wire refuses a newly owned epoch/order context. Exactly 256 successful
public-API admissions are allowed in the receipt-cap probe; the 257th request
is rejected before adding any new denotation chunk.

For every rejected request the runner compares admitted chunks, counts,
receipt count and previously admitted request ids with their earlier state.
They remain unchanged. Attempt metadata may change so that retrieval of an
old current receipt cannot be confused with the rejected attempt. This is
intentional ownership behavior, not silent deletion of valid unconditional
facts. The parent additionally stages delivery on a receiver fork and publishes
only after funded serialization and terminal output.

The source-bound adapter from a checked ADD receipt into the old portfolio
domain is statically inspected here; its direct execution belongs to the
producer owner's separate smoke evidence. The new adapter invokes the exact
receiver on a fork, checks its newly committed receipt, and stages a fresh
domain after source/current/witness/cutoff/bound/coverage checks. It accepts
no arbitrary report dictionary as an admission warrant. The inherited
128-bit cutoff restriction on this domain adapter is narrower than general
intermediate ADD arithmetic and must remain declared.

## Reproduction and limits

From a checkout containing this snapshot, use a new output directory:

```bash
python v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/focused_v1/source/v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/check_receiver_v1.py --source-root v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/focused_v1/source --out /tmp/rp3bb-receiver-new-run
```

The relative `v3/checks` layout in the source snapshot is intentional: sibling
imports and complete source-record paths resolve inside that saved root. A
flat copy of the files is not the recorded reproduction layout. Every valid
or mutated wire actually delivered in this run is saved in `run/wires`, with
hashes in results. Successful reports are saved separately in `run/reports`.

These checks do not execute the parent's event/byte tariff or establish a
funded completion bound. They do not test arbitrary hostile Python objects,
physical process isolation, cryptographic authentication, actual heap limits,
all possible malformed JSON documents, all grammar inputs, or final-evaluation
performance. Their load-bearing semantic conclusion is supported by the
independent induction over nodes, Apply claims and expression bindings;
the finite probes target concrete implementation and interface risks.
