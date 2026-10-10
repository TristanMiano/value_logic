# Independent static review of dependency pruning v1

Contributor: ChatGPT (GPT-6 Astra Pro), integration reviewer, October 10, 2026 UTC. Same-model, nonblind R-P3-B-B DEVELOPMENT; post-primary-exposure variant. Zero principal clock credit. No new pruning execution, policy run or production edit.

## Disposition and source binding

No material dependency-closure or node-remapping defect was found for the declared **full, zero-base input to a fresh independent receiver** service. This is a static reconstruction, not a replacement for independent receipt. The [source binding](source_binding.json) preserves the inspected original snapshot, including:

| Item | SHA-256 |
| --- | --- |
| New pruner, 17,079 bytes | `eac1fe24bf0643990d98e229724c7d9642e50d0b7a0fe4fd961b3b04fcb818e5` |
| Existing producer | `1e40f1bf7a3cb2dc9cfe46beff9a3548392e99e7ff0fa81a6c79c2f53508bbdc` |
| Unchanged independent receiver | `1f396bbb625614c87d48fa5fece438851999a7afeb58d5af6933812b4038c2bf` |
| Prospective pruning plan | `d2d72b5e22146078b515b3785af2c04bb6e4ab34f023ea51317edaf2772f0d9f` |
| Author's 31-event result summary | `ee96092f6f561c155b5ce724dbd63bca192210737cdac59be06a9be42cdb3cd5` |

The [captured pruner](source/v3/checks/05_add_evidence_prune.py) does not import or call an independent receiver. Its authoritative result is still the unchanged receiver's acceptance of the emitted packet. It may reject malformed or unsupported inputs; it does not promise to salvage every corrupted packet with an otherwise usable subgraph.

## Why the retained proof dependencies suffice

`prune_full` fixes the actual Frame, complete expected record, incumbent and bound. It computes the incumbent cutoff with the accepted complete-point semantics. Its current-goal seed sequence matches receiver v1: all current hard expressions and conjunctions; every current soft expression, failure complement, weight product and rank sum; the rank comparison and guard conjunction; the selected difference; and the greater-than-bound bad-set conjunction. It compares the resulting four roots with the existing full evidence. No old guarded conclusion or successful report becomes a new producer premise.

`_Closure.expression` retains the current expression's root and the exact constructor obligations. Literal and bit cases retain their defining terminals/node. Negation and scaling retain the corresponding subtraction/multiplication Apply fact and recursively required child expression. Other constructors retain both child bindings and their Apply fact. It enforces original child-before-parent expression order. Thus removal of an unused historical binding does not remove a required current denotation.

`_Closure.operation` mirrors the receiver's dependency requirements. Exact equal-operand, two-terminal and controlling-value cases need no recursive Apply premises, though the unchanged receiver still checks their arithmetic, derived Boolean types and exact output. All other cases split on the earliest variable of either input in the fixed order and recursively retain both cofactor Apply facts. Each premise must precede its dependent fact. The closure marks every input/output node and every node child; even an input made semantically irrelevant by a controlling value remains available for the receiver's node/type checks.

This is deliberately dependency extraction, not arithmetic acceptance. A structurally present false Apply result might survive extraction, but the independent receiver will still reject it. The correctness statement is that a valid full input retains all premises needed for its current claim, and every emitted claim must pass the same independent checker before becoming authority.

## Why renumbering preserves the wire contract

The node mapping is an injective, increasing map from retained old IDs to consecutive new IDs. Every retained child was marked recursively, and old child-before-parent order is preserved. Variables and the complete variable order do not change. Distinct original node definitions remain distinct under an injective map, and unequal children remain unequal.

Apply and expression rows are filtered in their original sequence, preserving each dependency's postorder. Because the node mapping is increasing, the canonical smaller-ID-first order of commutative Apply operands is preserved. The result IDs, expression roots and four current roots are all translated through the same map. Full mode, three zero base counts and all source/current metadata are retained. The output is then passed through the existing immutable `AddEvidence` constructor; semantic authority still comes from independent receipt.

The current-expression and operation closure concerns unconditional denotations. Therefore no hidden scoped premise is lost merely because historical requests used different hard or rank constraints: current guard construction is reseeded explicitly, and the retained facts themselves do not depend on those old guards.

## Limits that must remain explicit

The pruned packet is a new **full packet for a fresh receiver**. Its renumbered IDs and counts are not the unchanged warm manager's ID namespace. In particular, `next_cursor()` on a pruned packet must not be supplied as the resident delta cursor for that original full manager. A cursor-compatible compact resident-state protocol would require an additional design; it is outside this implementation. This is not a defect in the declared full-only fresh-receiver service.

The original full warm manager is unchanged and remains retained. The convenience exporter first constructs the ordinary full evidence object and then prunes it. A smaller output therefore does not imply lower total work or smaller producer retention. Full export, indexing, dependency traversal, remapping, immutable output construction, serialization and independent checking all remain real work.

The 8,000,000 dependency-step limit is a local traversal guard. It is not the full event/byte bill: for example, sorting comparisons, Python hashing, exact arithmetic, validation and output serialization are not exhaustively represented by that counter alone. The outer service must include this new source file and meter its complete executed work and relevant temporary/storage costs. The source record is preserved rather than authenticated or silently repaired by the pruner; the owner must procure and independently bind the actual closure including the pruner and wrapper.

The plan correctly calls this dependency pruning rather than minimum-proof construction. Required syntax bindings or receiver-rule premises may be retained even when a stronger calculus could avoid them. No inference rule, old worker, receiver or primary result is changed by this new file.

## Existing execution evidence and conclusion

The author result summary reports 31 fixed events passing, including the 24 existing current requests and the declared reverse-order, idempotence, missing-dependency, delta, local-limit and false-bound cases. This reviewer inspected and hash-bound that summary but did not rerun it. The finite audit and primary evidence remain separate from this post-exposure variant.

No source correction is requested from this static review. The stated full-only, trusted-source, unchanged-manager and complete-outer-metering conditions should accompany any later measured use or comparison.
