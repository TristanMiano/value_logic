# Static review of the paid pruning wrapper and runner

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-controls reviewer, October 10, 2026 UTC. Same-model, nonblind, post-primary-exposure R-P3-B-B DEVELOPMENT. Zero principal or agent research-clock credit. This review read source and saved copies; it did not import or execute a worker, run a policy comparison, or edit an existing source file.

## Disposition and exact sources

The corrected wrapper and runner have **no remaining material integration or accounting blocker within this static review**. The earlier module-loading defect described below was reported before the planned comparison and is addressed in the captured runner. This establishes static consistency with the declared implementation; it does not establish that every later delivery succeeds or that pruning reduces total cost.

The [source binding](source_binding.json) captures 15 files, including the complete worker dependencies, both runners, amendment 5, and the independent pruning review. Its SHA-256 is `48f68f4132ae270e799903d27c073f08892d8d66f2a8bac074573ae4ef21bba9`.

| Inspected item | SHA-256 |
| --- | --- |
| New pruning service adapter | `65d824227e3a06978ed9da155cc930db111499fff4a795c2dde0a6c854b81d34` |
| Corrected pruning runner | `aa1cf405387f6e6117da3e86d220e0c2012ebc541b99d56ce0b90c4600f65e2e` |
| Dependency pruner v1 | `eac1fe24bf0643990d98e229724c7d9642e50d0b7a0fe4fd961b3b04fcb818e5` |
| Unchanged primary service v5 | `b96cae82e0fe3f0f734671d57df81ac3a62350746f73228aef63c2f77bb1745f` |
| Unchanged original runner | `f42bde6b6d1a4422bac3e9e7f38e32a3be38cafad44623ffe1340838fa800cb4` |
| Prospective service amendment 5 | `c7507cbd04e2ce9ff3befc7da09278377aab8388a0a8b092f6fada8ceeb025db` |

## Addressed module and source-closure defect

The first inspected new runner, SHA-256 `330e2566304b7dd4d89285eeca37c4d566839a507fb2ddab70c361d40169d41e`, loaded the new adapter before the original runner. The original runner's loader unconditionally creates its service module. That order could leave the adapter and artifact writer holding distinct service objects: the adapter would execute with its expanded closure while the writer would enroll and capture the old closure. This was a concrete source-binding defect, not a cost outcome. The earlier runner is identified here by the hash observed during that inspection; this snapshot preserves the corrected source, not a reconstructed copy of the earlier one.

The corrected runner loads the original runner first, then loads the adapter through its module-reusing loader. It also asserts that `X.S is R.S` and `X.PRUNE.E is X.S.A`. The original writer therefore reads the same expanded `S.SOURCE_PATHS` that all sessions use. Its source record, per-file enrollment charges, captured program bytes and subsequent stability checks agree. The new runner separately captures its own observer source. No primary source file needs to change.

## Paid production, receipt and storage

`PrunedSession._execute` performs full immutable evidence construction inside `producer_build`, then dependency extraction inside `producer_prune`, then encoding inside `producer_export`. It does not encode and decode an untransmitted full JSON packet merely to prune it. The complete execution of the pruning routine remains inside the inherited event tariff; the local dependency counter is only an additional bounded guard.

The temporary full evidence object is discarded before the declared delivery snapshot. The full warm `RecordingManager` remains in the producer state and is serialized and charged at that snapshot. The overridden `_producer_state` also includes the actual `prune_limit_steps`. Current input and transmitted pruned evidence appear on both applicable sides of the live snapshot. The new receiver is created empty, checks the full zero-base pruned packet under the unchanged rules, and is serialized before disposal. Only after the paid receipt and publication events does the inherited governor expose the current output and discard the fresh receiver.

These are the unchanged declared **live admission/delivery periods**, not physical peak-heap or elapsed byte-time accounting. Temporary construction work is executed and priced, but temporary allocations are not independently promised a physical memory bound. Post-disposal diagnostic sizes remain observer measurements and do not add a duplicate live period. The pruned arm receives no exemption from complete warm-manager retention.

The current frame, complete record, witness, bound and source record pass through the same request codecs and common receipt gate. The pruner receives the evidence object and current inputs, never a successful report from another receiver or a reference-oracle result. A fresh independent receiver supplies the evidence authority. `self.cursor` is explicitly `None`; the wrapper never attempts to use a pruned packet's renumbered counts as an original-manager delta cursor.

## Matching, failures and result interpretation

All six fresh-consumer methods enroll the same expanded source closure, including the pruner and adapter. The two portfolio methods retain the old-domain recipes they use. The ordinary full ADD, pruned ADD and direct-check methods have empty `old_specs`, avoiding a charge for serializing unused old recipes. This is a prospective common comparison convention recorded in amendment 5; it does not rewrite the original primary comparison or assert the minimum cost of an ordinary implementation.

The runner declares all four existing streams, six current requests per stream and six fresh-consumer arms: 144 delivery attempts. It saves each attempt before applying service assertions. It then makes one separately classified, one-step pruning-limit attempt per stream, saves the paid failure, requires `PruneLimit`, and checks full mutable-state eviction and withdrawal of current and previous receipt authority. The four failures are not ordinary cheap successes. The immutable full export precedes the pruning limit, so the governor retains that already paid prefix in the invoice.

The runner's overall `PASS` means the prescribed attempts and assertions completed. Its inherited service assertion permits a properly charged `NO_CURRENT_CERTIFICATE` outcome. Therefore delivery success counts and failure rows must still be reported; `PASS` alone does not say that all 144 deliveries succeeded. Source stability is checked after every saved attempt and at completion. The source-bound primary reference is reused without injecting reference truth into a producer.

The inherited `consumer_thresholds` values are comparisons between observed consumer invoice totals and named thresholds. They are not new executions under those independent caps. An enforced consumer cap must also leave the governor's stated failure reserve available during successful execution. Any practical cap claim should use actual capped attempts or preserve that reserve qualification.

This static review makes no total-cost inference from the author's earlier 18,543-byte transmission reduction over 24 requests. The first packet in every stream had identical full and pruned counts and size, so pruning adds extraction work without reducing that initial transmission. The secondary run must report all producer, receiver, source and storage charges before drawing a finite cost conclusion.

## Independent closure review and additional scope limit

The independent integration reviewer found no material closure or monotone-renumbering defect at the same pruner source. Its captured review SHA-256 is `cdfa325303b7e8177f76823a31aced0c5719bb1c25a981ed9074dc4941e5f56a`; its source-binding SHA-256 is `fd878512dd5cd3733da83ffa9a2e4a59e8577aec220fe529b90791efb02dc914`. That was a separate static inspection, not another execution of the author's 31-event suite.

The qualification added to the handoff is explicit: a pruned packet creates a new node-ID namespace. Its `next_cursor()` must not be fed back into the unchanged full warm manager. A compatible compact resident-state protocol would need additional design and checking. The authorized wrapper correctly confines this exporter to full packets for fresh receivers. The original [implementation and results](../implementation_and_results.md), source snapshot and 31 saved events remain unchanged.
