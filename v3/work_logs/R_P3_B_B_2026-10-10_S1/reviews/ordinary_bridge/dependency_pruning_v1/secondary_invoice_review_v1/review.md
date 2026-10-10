# Completed secondary invoices: pruning saves consumer work and adds total cost

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-controls reviewer, October 10, 2026 UTC. Same-model, nonblind, post-primary-exposure R-P3-B-B DEVELOPMENT. Zero principal or agent research-clock credit. This review executed a JSON arithmetic reader only, after the final run summary appeared. It did not import or run a worker, alter a policy, rerun a delivery, or modify an existing artifact.

## Finding and matched scope

Under the declared tariff, dependency pruning **increased the total bill on every one of the 24 matched current deliveries**, while reducing each stream's aggregate transmitted bytes and consumer bill. On the first delivery in each stream, wire size was unchanged and the consumer bill increased by three units. On all 20 later deliveries, both wire size and consumer units decreased. The paid pruning stage exceeded savings elsewhere in all four six-request totals.

This comparison uses `O-ADD-WARM` and `O-ADD-WARM-PRUNED` from the same completed secondary run. Both received the same current cases and source record, had fresh independent consumers, and retained their complete warm producers. All six paired common receipt objects were exactly equal in every stream, including complete current frame record, witness, bound, request ID and source binding. The comparison does not mix primary-v5 costs with the secondary run's larger source closure and revised treatment of unused old inputs.

The complete secondary run reports 144 deliveries, four intended `PruneLimit` failures and 1,177 assertions, with final status `PASS`. The reviewer independently verified the sealed manifest/completed-unit hashes, every captured source hash, all 148 integer invoice sums and budget inequalities, the four separately classified failure rows, and all 24 matched receipt pairs. The [saved results](results.json) retain per-request metrics and differences as well as the aggregates below.

## Exact six-request totals

Every arrow is **full warm ADD to pruned warm ADD**. Wire entries are bytes; total and consumer entries are tariff units.

| Stream | Proof bytes | Total units | Consumer units |
| --- | ---: | ---: | ---: |
| `constant_n3` | 22,041 → 19,832 | 2,647,874 → 2,801,114 | 1,905,926 → 1,677,709 |
| `parity_reassociation_n6` | 56,149 → 53,938 | 7,561,819 → 10,050,503 | 5,035,824 → 4,811,004 |
| `complementary_k3_n5` | 50,558 → 44,823 | 7,164,128 → 8,746,864 | 4,708,852 → 4,081,348 |
| `complementary_k5_n7` | 72,113 → 63,725 | 10,242,633 → 12,805,319 | 6,660,358 → 5,771,346 |
| All 24 deliveries | 200,861 → 182,318 | 27,616,454 → 34,403,800 | 18,310,960 → 16,341,407 |

Thus the fixed comparison removes 18,543 transmitted bytes and 1,969,553 consumer units while adding 6,787,346 total units. The consumer reduction is a real recorded consequence of sending and checking fewer facts. It does not imply a reduction in all work performed to deliver the certificate.

| Stream | Wire bytes removed | Consumer units saved | Total units added |
| --- | ---: | ---: | ---: |
| `constant_n3` | 2,209 | 228,217 | 153,240 |
| `parity_reassociation_n6` | 2,211 | 224,820 | 2,488,684 |
| `complementary_k3_n5` | 5,735 | 627,504 | 1,582,736 |
| `complementary_k5_n7` | 8,388 | 889,012 | 2,562,686 |

Relative to each full warm bill, the total increases are approximately 5.787%, 32.911%, 22.093% and 25.020%, respectively. The corresponding consumer reductions are approximately 11.974%, 4.464%, 13.326% and 13.348%. These percentages describe the recorded six-request sums, not a population estimate or a longer-horizon prediction.

## What pays for the reduction

The adapter first executes the ordinary full immutable export. Its separate `producer_prune` stage performs indexing, dependency extraction, remapping and immutable output construction before encoding the pruned packet. The next table sums that entire priced stage and compares it with the change across all other stages. “Other stages saved” is the full warm total minus the pruned total after removing the pruned stage; it includes all remaining producer, receiver, source, storage and terminal differences.

| Stream | Pruning stage units | Other stages saved | Net total units added |
| --- | ---: | ---: | ---: |
| `constant_n3` | 386,011 | 232,771 | 153,240 |
| `parity_reassociation_n6` | 2,718,060 | 229,376 | 2,488,684 |
| `complementary_k3_n5` | 2,222,294 | 639,558 | 1,582,736 |
| `complementary_k5_n7` | 3,469,396 | 906,710 | 2,562,686 |
| All 24 deliveries | 8,795,761 | 2,008,415 | 6,787,346 |

The complete warm manager remains retained. Per delivery, the pruned arm's post-disposal producer serialization is 35 bytes larger, consistent with its different method name and explicit pruning-limit field; the manager is not compacted. Its producer live snapshot becomes smaller on later deliveries because the transmitted evidence included in that snapshot is smaller. Consumer live snapshots also shrink on later deliveries. These are the declared serialized live-period measurements, not physical heap-peak or elapsed byte-time estimates.

The first requests make the extraction overhead visible without a transmission benefit. Total units added on those requests are 17,358 for the constant stream, 428,512 for parity, 274,781 for the smaller complementary stream and 461,257 for the larger one. Across all requests, even the smallest total increase remains positive: 2,133 units on the constant stream's sixth request. No prefix or per-request total-cost improvement is hidden inside the four aggregate increases.

## Paid failure boundary

The separately declared one-step limit probes occur after request six and are recorded as request seven. Their total invoices are 126,877, 313,539, 332,541 and 463,157 units for constant, parity, complementary k3 and complementary k5, respectively. Each is a `NO_CURRENT_CERTIFICATE` result caused by `PruneLimit`, and each retains a nonzero paid full-export/pruning prefix. They are excluded from the delivery totals above. The source-bound runner also checks eviction and withdrawal of both previous and failed current receipt authority; this arithmetic review did not reconstruct live worker objects.

The consumer savings may matter in a service where producer and consumer resources have different limits. An observed consumer bill below a threshold remains distinct from executing the request with that cap: the inherited governor also reserves failure-output capacity. This review reports the invoices and does not introduce a new capped run, price ratio or deployment claim.

## Source binding and reproduction

The prospective [review plan](plan.md) was saved before reading the completed invoices. The standalone [reader](analyze_invoices.py) imports only standard file, hash, time, argument and JSON facilities. It refuses to read the unit log until `summary.json` exists, checks the recorded closure, and writes a new output path without overwriting a prior result.

| Item | SHA-256 |
| --- | --- |
| Review plan | `8e6ba77f586cdd0a98d7cdddb801ace7cdfef9def1ed13feeeac309f44a0c77e` |
| Arithmetic reader | `f27e941ec4311d0303f805c156b6c05cc72157bc07f1cf03d2021cd0956d24a4` |
| Review results | `5bf78544179fa29d2a9a647a5f6078ff393dff6f3754d4c310e00ce89137a25e` |
| Secondary manifest | `12992eea4dc613466ed101517f5e53d2c04da540cf4d335c2b5238e3a8d565e9` |
| Secondary completed units | `76d3f28bf30edee6e19e5edbdff6a7bb0927032744dd54bf5bd57005c33f90b1` |
| Secondary final summary | `1ed9c87f8b8001b1d11a3c13db8ab09a9d6aea5edb9848e68c88b7ccda23e2c1` |

From the repository root, the original review command was:

```bash
python -B v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/ordinary_bridge/dependency_pruning_v1/secondary_invoice_review_v1/analyze_invoices.py \
  --run v3/work_logs/R_P3_B_B_2026-10-10_S1/development/secondary_pruning_v1 \
  --out v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/ordinary_bridge/dependency_pruning_v1/secondary_invoice_review_v1/results.json
```

For reproduction, choose a new output filename. The output records the review time, so a fresh file's bytes may differ while every source hash and numerical result remains identical. There was one successful execution of this arithmetic reader and no failed analysis or worker rerun in this review.

The result supports a concrete finite tradeoff: this dependency-pruning implementation reduces the fresh consumer's later work at an added producer cost. It does not reduce complete delivery cost on these 24 cases. The primary comparison, independent receiver, original producer and pruning-v1 code remain unchanged; this is an explicitly post-exposure stronger ordinary control.
