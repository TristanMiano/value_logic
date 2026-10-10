# Independent receiver and checked-admission reconstruction

Contributor: ChatGPT (GPT-6 Astra Pro), integration reviewer, October 10, 2026 UTC. Same-model, nonblind R-P3-B-B DEVELOPMENT review. Static source inspection only; zero overlapping principal research-time credit.

## Disposition and exact scope

I find no material soundness defect in the reviewed independent receiver or its checked ADD-to-portfolio admission boundary. This is a source reconstruction under the stated trusted in-process owner assumption. It does not certify the producer's whole implementation, the parent's forthcoming event/byte tariff, arbitrary external Python mutation, or funded completion.

The [source binding](source_binding.json) and captured files preserve the inspected versions:

| Source | Scope | SHA-256 |
| --- | --- | --- |
| `05_add_evidence_check.py` | Full independent receiver, 33,036 bytes | `1f396bbb625614c87d48fa5fece438851999a7afeb58d5af6933812b4038c2bf` |
| `05_add_evidence.py` | Canonical receiver loader and `admit_checked_add` adapter only | `1e40f1bf7a3cb2dc9cfe46beff9a3548392e99e7ff0fa81a6c79c2f53508bbdc` |
| Receiver author's results | Existing 42-group execution; not rerun by this reviewer | `bd942a12faa59fd0d1571e4b65dc76003f3967aa944c53b7f5e28b1b3c3ef1f0` |

The captured [checker](source/v3/checks/05_add_evidence_check.py) imports the accepted finite Frame grammar, not the ordinary ADD Manager or the new producer. The [wire contract](source/v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/ordinary_bridge/wire_contract_v1.md) agrees with the implementation on the reviewed interfaces.

## The load-bearing induction

**Node denotation.** `_View.admit_nodes` assigns every terminal its reduced exact rational value, with positive denominator and bounded components. Every decision references already present children, has distinct child IDs and places its variable strictly before both children in the owner's complete order. Full unique-key checks reject duplicate terminal or decision nodes across both pending and resident chunks. Consequently the checked node graph is a reduced ordered finite ADD. Its Boolean flags are derived from terminal values and both child flags, never supplied as authoritative packet claims.

**Unconditional Apply facts.** `_View.admit_applies` admits a key only once, requires supported operation and exact integer IDs, canonicalizes the declared commutative cases, and checks Boolean inputs for Boolean conjunction/disjunction. `_operation_result` justifies an output by an exact identity, exact terminal arithmetic/comparison, a controlling value, or two previously checked cofactor Apply facts. The latter splits at the earliest variable of either input and requires the exact unique result node, or the common child result. Postorder lookup admits neither missing nor future Apply premises. Induction therefore gives the complete pointwise identity for each admitted operation on every assignment in the fixed Boolean cube.

This inference never takes the current hard formula, an incumbent cutoff, or a previously accepted conditional bound as an extra premise. A current assumption cannot become a resident unconditional rewrite. Equal-operand and controlling-value rules remain sound because the Boolean-only rules also require the derived Boolean types. The noncommutative `sub`, `le` and `gt` cases preserve operand order.

**Expression denotation.** `_expression` independently parses bounded canonical expression strings using the inherited rational and type restrictions. `_View.admit_expressions` checks literals and variables against canonical node definitions, and every constructor against already checked child expression roots and the required Apply fact. The inherited `_key` spelling is independently reconstructed by `_syntax_key`. A packet cannot bind an arbitrary expression to a convenient zero root merely by declaring it equal. Expression facts, like Apply facts, are unconditional in the fixed coordinate interpretation.

**Current request.** `Receiver.receive` compares the complete expected source record, owner epoch, bit count, order, and exact resident base counts before admitting candidate facts. The independently supplied actual `Frame` is validated, its complete `record()` must equal both the independent expected record and the packet record, and the packet must retain the independently fixed witness and requested bound. Boolean-as-integer indices and witnesses are excluded. The source record's equality binds the claimed source context; it is not a substitute for the owner's actual source procurement and version selection.

The receiver then evaluates the complete incumbent with the accepted scalar-at-a-point grammar to establish feasibility and its one-tier cutoff. At a complete Boolean point, the inherited interval interpreter is exact by induction on the grammar; using it here does not assume the producer's ADD correctness. From the unconditional checked expression and Apply ledgers, the receiver constructs the current hard conjunction, weighted soft-failure rank, rank-at-most-cutoff guard, requested difference and greater-than-bound bad set anew. It compares all four declared roots with those derived roots and requires the bad-set root to be the canonical zero terminal.

Thus, for current hard feasibility $`H(x)`$, current rank $`r(x)`$, incumbent cutoff $`c`$, difference $`D(x)`$ and independently requested bound $`b`$, the checked conclusion is

```math
\forall x:\quad H(x)\wedge r(x)\le c\ \Longrightarrow\ D(x)\le b.
```

The feasible incumbent belongs to this guard and establishes `NONEMPTY`. Finite-domain minimizers all have rank at most a feasible incumbent's rank, so the report's entire-incumbent-sublevel coverage includes all current minimizers. The conclusion does not claim selected-identity recovery. Removing a hard constraint or changing rank rows requires the newly reconstructed guard; an old conditional conclusion alone cannot certify the edited request.

## Resident ownership and output boundary

Only the final `_state = next_state` publishes newly verified facts; parsing, local validation, current-root checks and report construction occur first. `fork()` shares prior tables but stages all later admissions in new pending lists/dictionaries and a new chunk. The public receive path never writes to prior chunk dictionaries. An unsuccessful call leaves admitted denotation chunks unchanged while its attempt counter changes intentionally to invalidate retrieval of the previous current receipt.

The stored receipt is canonical JSON, so mutating the returned report dictionary does not rewrite committed receipt authority. `current_receipt` also checks the active attempt and caller request ID. Explicit successful request IDs cannot be reused in an epoch. The parent's owned delivery must use these explicit IDs, verify on a fork, charge final storage/output, and publish that fork only when its whole transaction succeeds.

Two scope qualifications matter. First, `_Chunk` is a frozen dataclass containing private ordinary dictionaries. Those dictionaries are persistent by API discipline, not immutable against arbitrary Python access. `Receiver` fields and private state likewise belong to a trusted owner. This matches the stated contract; it is not isolation from hostile code in the same interpreter. Second, explicit `reset` and direct `receive` are owner operations. A trace interruption after the checker commit may occur before the return value is delivered, as the module documentation states. The outer owner's staged publication protocol is therefore required for a paid all-or-nothing service. This static review does not turn standalone raw work counters into such a protocol.

Exact resident counts are not a cryptographic state digest. This does not create a semantic shortcut: any new fact is checked against the actual resident denotations, and the current theorem is independently reconstructed. The owner must still keep the intended receiver instance, source context and epoch aligned with the producer's episode; counts alone are not an authorization token.

## Checked admission into the unchanged portfolio kernel

The inspected `admit_checked_add` accepts the exact canonical independent Receiver class and exact unchanged PortfolioCache class, verifies a fresh handle, binds the source and complete current record, validates the complete incumbent and bound, and enforces the inherited 128-bit cutoff interface. It calls the independent checker on a receiver fork with the owner's explicit request ID, then compares the returned report with the newly committed receipt and checks the exact bound, cutoff, `NONEMPTY`, coverage, version and request fields.

Only after that verification does it create a new portfolio cache, copy the already admitted old domains, and append the new domain under the fresh handle. It returns staged receiver/cache objects while leaving the originals unchanged. This is an explicit new verified admission rule, rather than acceptance of a caller's status dictionary. Subsequent domain choices, replacements, tree production and verification use the unchanged portfolio kernel.

The admission soundness argument is direct: the checked ADD receipt establishes the same full hard/rank domain and bound stored in the new domain certificate. The old kernel may therefore use that theorem as an admitted premise. The original tree-bootstrap path remains a distinct comparator whose construction, export, checking and storage must be charged. The new adapter does not justify omitting those costs for the ADD path; it only supplies a sound alternative route to the same receiving premise.

## Accounting and evidence limits

`storage()` serializes the full declared retained representation: node and unique tables, derived Boolean flags, Apply and expression bindings, source/order context, request IDs and receipt state. The stated measure is serialized bytes, not native heap memory. Exact source reading, diagram construction, intermediate Apply work, wire export/parse, record comparisons, checked admission, persistent storage and final delivery remain chargeable in the parent's common service.

The receiver author's [outcomes](source/v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/focused_v1/outcomes.md) report 42 fixed groups passing, including 29 expected rejections, source-bound full/delta cases, expression/Apply corruption, stale source/epoch/current data, constraint withdrawal and finite receipt limits. Those are the author's executions. This reviewer performed zero new probes and zero policy runs. The present support is the independent source induction above and precise interface inspection; it does not claim exhaustive malformed-input testing or final evaluation.

No source edit is requested on this reviewed boundary. The parent should retain the already declared source-authentication, trusted-owner, finite arithmetic-cap and paid outer-transaction scopes in the experiment report.
