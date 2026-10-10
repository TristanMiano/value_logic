# Observer recipe for funded completion and delivered-request inclusion

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-controls reviewer, October 10, 2026 UTC. Same-model, nonblind, post-exposure R-P3-B-B DEVELOPMENT. Zero principal or agent clock credit. This recipe was written from the fixed sources without reading the running unit log. It changes neither runner nor contract and calls for no worker execution or additional request.

## What to compare

Use the completed actual-cap run only after its summary reports `PASS`. Verify its manifest, unit-log and captured-source hashes; require the 288 distinct prescribed keys `(stream, recipient, method, request_index)` and the original input/source binding. Match every primary observer field back to the corresponding sealed primary row. The 29 old/current scalar truths remain existing evidence, not new trials.

The principal comparison has eight groups: each of four streams under each recipient mode. Within each group, compare the six fixed methods at every prefix from one through six. A delivered-request set records which independently specified requests actually received their required certificate. This is different from the within-certificate mathematical coverage of the full incumbent sublevel, and it does not assert that past receipts remain current after later requests.

For method $`m`$ and prefix $`k`$, define:

```math
I_m(k)=\{i\leq k:\mathrm{status}_{m,i}=\mathrm{DELIVERED}\},
\qquad C_m(k)=\sum_{i=1}^{k}c_{m,i},
\qquad U_m(k)=\sum_{i=1}^{k}u_{m,i}.
```

Here $`c`$ and $`u`$ are total and consumer invoice units for **every issued attempt**, including failures. Report exact request identities, delivered count, failure count, total bill, consumer bill, and the failure-only portions of those bills. Keep complete, partial and zero-completion paths explicit.

For a pair of methods in the same group and prefix, one provides at least the other's delivered service at no greater total cost precisely when its delivered-request set includes the other's and its total bill is no larger. Require at least one strict inequality for a strict comparison. Sets with different missing requests can be incomparable even when their cardinalities agree. The consumer bill is a separately reported resource axis; a stronger three-axis comparison may additionally require it to be no larger, but must be labeled separately from the requested inclusion-plus-total-cost comparison.

A six-request endpoint comparison must not be presented as a comparison at every earlier prefix. If claiming that one complete path covers another throughout the sequence at no higher accumulated cost, check inclusion and cost at **all six prefixes**. Exact ties remain ties. A cheap zero-completion path provides no delivered certificate; it is a failed-service record, not a cheap successful method or a certificate-service winner. Likewise, do not rank partial paths by dividing only successful invoice costs by their successful count. Failed prefixes are real procurement costs.

If combining streams, use the explicit finite package of all four streams with request identities `(stream, index)` and the recorded sums. That package is not an inferred task distribution, and no unrecorded mixture weights are needed. The eight individual group tables should remain available.

## Compare static affordability with actual funded status

For each exact matched primary row, retain both predicates already declared and recorded by the observer:

```math
P_{m,i}=[u^{\mathrm{primary}}_{m,i}\leq T],
\qquad
Q_{m,i}=[u^{\mathrm{primary}}_{m,i}+R\leq T],
\qquad
A_{m,i}=[i\in I_m(6)],
```

where $`T=1048576`$ and $`R=1024`$. For each predicate and each group, report all four combinations with actual status: predicted affordable/delivered, predicted affordable/failed, predicted unaffordable/delivered, predicted unaffordable/failed. Preserve the exact discrepant request identities and amounts, not only aggregate accuracy. Repeat the counts by prefix and distinguish rows before any prior failure from rows following one or more failures in the same session.

The difference between the two primary predicates isolates a declared reserve band in the **same primary bill**. It does not, by itself, establish that reserve capacity caused a particular funded failure. The funded and primary paths may enter that request with different caches and proof histories. A resource error records its stage but does not include a distinct exhausted-cap identifier or requested-charge amount in the saved error. Do not infer a unique denial cause where that information is absent.

In the unchanged meter, every successful consumer charge must leave the protected reserve available. With identical starting state and an identical executed charge path, the reserve-adjusted test is the relevant replay condition. The unconstrained primary history need not supply that starting state after the funded run has denied a request. The new predicate values are observer diagnostics, not signals that selected actions or requests.

## Source enrollment and scientific caches are separate state

Service v5 initializes `source_enrolled=False`. `_enroll` sets it to true only after the complete enrollment routine returns. `_evict` clears the ADD manager, cursor, independent receiver, producer and receiver portfolio caches, old packets, old input records, and current payload. It does **not** clear `source_enrolled`, the caller's `old_specs`, source record, stream identity, bit/order configuration or advancing request index.

Consequently, a failure during incomplete enrollment can cause enrollment to be attempted again on the next prescribed request. Once enrollment has completed, a later failure retains that installed-source fact while withdrawing scientific cache authority. The next request can therefore have a paid installation and empty scientific caches. The boolean observation after each attempt, its predecessor, and `common_source` invoice stages distinguish these cases. A failed request's source fees and partial computation remain in the cumulative bill even when the next request rebuilds.

This produces two possible directions of discrepancy. Losing resident domain or ADD receipt state can require a later full bootstrap or full proof where the primary path used a cheap update. A primary-affordable request may then fail. Conversely, the fresh-recipient `O-ADD-WARM` arm exports its entire accumulated manager. Eviction removes that historical accumulation; a later newly built full proof can be smaller than the corresponding primary full proof, potentially permitting delivery that a primary static bill rejected. Cache eviction is therefore not uniformly a cost increase. Both discrepancy directions must be retained.

For each session, report the indices of failures, successful requests after a failure, the observed enrollment sequence, and failure-stage/cause counts. Interpret those as the outcomes of this fixed failure policy. No unexecuted fallback, partial-cache salvage or cache-retention strategy is credited. The source-bound run can demonstrate state and cost changes, but does not identify every counterfactual intermediate state without additional execution.

## Minimum evidence tables

The concise result should contain:

1. Eight group tables with one row per method: delivered request IDs, counts, all-attempt total/consumer cost, and failure-only cost. Include prefix records in the machine-readable artifact.
2. Pairwise request-inclusion and total-cost comparisons at each prefix; exact ties and incomparable delivered sets remain explicit. Keep zero-completion records outside claims of successful service.
3. Both static-predicate discrepancy tables with exact request IDs, primary bill, actual outcome, actual bill, prior-failure status and enrollment state.
4. Paid failures and subsequent recoveries, with failure causes/stages and the source-enrollment distinction above.

No broad leader claim follows from a smaller invoice when the delivered-request set is smaller or different. Actual cap compliance and the changed funded history are the result under study. The original primary and pruning-secondary populations remain separate.

## Source binding

| Inspected source | SHA-256 |
| --- | --- |
| Service v5 | `b96cae82e0fe3f0f734671d57df81ac3a62350746f73228aef63c2f77bb1745f` |
| Immutable actual-cap observer | `774ddedcb35eb4cf2c7600b7fdfdc154167cc77a09f00a05d922439f210897fb` |
| Immutable prospective contract | `1bd2453a909d482e45b97ad9465656b396465e206b1bd54e8b823ac74b8f221c` |

This document is an additive interpretation recipe. It does not change the worker, fixture, primary runner, actual-cap observer, contract, prescribed outcomes or budgets. No running log was inspected while deriving it, and no polling or wait loop was used.
