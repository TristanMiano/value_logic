# Amended analysis: independent development readback

Contributor: ChatGPT, GPT-6 Astra Pro. Date: 2026-10-11.

This same-model, nonblind P3-09 review gives zero principal research-clock credit. It reads preserved DEVELOPMENT scores and paid records, runs only the captured analyzer's pure observer helpers, and uses explicitly synthetic score dictionaries. It calls no adapter, policy, provider, receiver, reporter, private-truth function or final generator. No final population, final case, final outcome or machine configuration is read. Existing scientific evidence and canonical source are not edited.

## Result

**No remaining numerical blocker was found in the amended analysis scope tested here.** The source version is [p309_analyze.py](source/v3/experiments/p309_analyze.py), SHA-256 `197527ab8e3a29a26ed327a179ec668a510b5c10fd6de0752b5f318b2aa4f229`. A final readback confirmed that the live analyzer still matched that hash.

The review performs **2,726 independent observer checks**: 1,354 using all 30 preserved broker records, 20 using disjoint synthetic dictionaries, and 1,352 using the 13 preserved standardized certificate histories. These are arithmetic, identity, invoice and denominator checks; their count is not an inferential sample size. [Broker reconstruction](replay_results_v2.json), [synthetic checks](synthetic_results.json), [certificate reconstruction](certificate_results.json)

The [initial review](../initial_review.md), original counterexamples and their source snapshot remain intact. The current changes resolve the concrete cross-stakes subtraction defect and complete the A1/A3/A4/A5 fields and slice aggregates identified there. The source-only evidence for semantic-failure handling and local import closure remains as described in that initial review; this readback does not repeat a complete kernel or runtime audit.

## Source and data binding

The [amended source manifest](source_manifest.json) has SHA-256 `09b4c0d4a8086d15e17f3a04da8c7f6b630a8c765533c139d7001706eeb066d9`. It captures the analyzer, its lifecycle dependency, the three adapters, the paid reporter and the protocol prose. The broker source is `6dbe26a870416ae54a206d258472ab710a2d78d9705cfde68ebd56cf491b9787`; the certificate source is `14db182d5ace8f8670cd298c3dad456e54e72a3e1ecdbfe36d5238fca6f1126c`.

| Preserved DEVELOPMENT input | Bound SHA-256 | Used as |
| --- | --- | --- |
| `reviews/broker_design/development_v1/run/results.json` | `7a2d6d7eba3699008f6d31a05eeb07fa0a02518bf11601f0ae630382022585e7` | All 30 original public records and private scores; 28 normal toy executions plus two deliberately altered denial configurations. |
| `reviews/broker_design/a5_observer_v1/run/results.json` | `6ac07c9920c79e68b6357d7f9366932134c259c8509bdb780f3f50ce5c022c78` | Matching A5 observer comparisons attached to copies of the old scores; every used endpoint and fee is reconstructed from its original paid report. |
| `reviews/structural_design/development_smoke_v1/results.json` | `819dce1ed0e4f44f43a062ae683c1a4f56e2263bc567b951e839692e3eaf5c0c` | Thirteen standardized histories, each with four paid attempts and its original score. |

The original broker executions retain their **65,114-unit source invoice**. The newly enlarged adapter would have a prospective 66,076-unit source invoice on a new execution; that amount is not substituted into old measurements. The certificate records likewise retain their v1 measured invoices rather than being relabeled as v1.1 executions. The three additional direct reserve probes in the certificate artifact have no standardized history score and are not invented as capped catalogue rows. [Bound replay scripts and outputs](../amended_replay_v2.py), [certificate reader](../amended_certificates.py)

### Preserved reader failure

The first broker reader assumed the A5 supplement duplicated each real paid report. It actually stores `optional_report:null` for real records, using their ID to reference the hash-bound original; only synthetic examples embed that object. The reader stopped at that assertion before evaluating the analyzer. Its [failure result](replay_results.json), original reader and the [explicit reader amendment](reader_amendment.json) are preserved. The revised reader binds ID and horizon, then independently checks every endpoint and fee against the original report. This was a reviewer join error, not an analyzer defect or lost scientific record. No worker was repeated to resolve it.

## 1. Broker actions, couplings and economics

All 11 declared toy pair links are present: four base/live, two cold/reuse, one ordinary mirror and four stakes references. For each pair, the independent reader computes current and reference action losses from their false-positive/false-negative counts using **one current stake vector and one normalizer**. It then adds the cost difference using one common normalized price. These values equal the amended paired fields. [Broker results](replay_results_v2.json)

The original cross-stakes counterexample is also tested through the complete `broker_analysis` helper. Identical actions with one false positive in two positions still have self-stakes means `1/2` and `1/6`, but their common-stakes action difference is now zero, their common priced difference is zero, and the whole-pair practical-action flag is false. There is no apparent gain merely from changing the loss definition. [Synthetic results](synthetic_results.json)

The A1 predicates distinguish their contracts. Base/live requires the shadow base path to agree and checks loss domination; cold/reuse requires the complete declared mathematical paths to agree while permitting provider and bill changes; the ordinary mirror requires its mathematical and invoice identity. The preserved real toy has no coupling violation. A copied synthetic mirror score with a one-unit invoice difference correctly fails `ordinary_identity_pass` and enters the combined A1 violations list, although its path hashes remain unchanged. [Captured analyzer](source/v3/experiments/p309_analyze.py), [injected observer-only result](replay_results_v2.json)

A4 now records the exact cold-cost ratio and gates its inclusive 0.95 criterion on a complete pair, equal delivered/action paths and equal scored outcomes. The independent reader reconstructs the ratios, equality predicates and practical flags from the original bills and score fields. Paired configuration means retain the full scheduled pairing denominator. Changed outcomes continue to use action/priced effects; an identical-kernel ordinary interpretation is still present and supplies no superiority requirement.

## 2. First occurrences, transfer slices and missing outcomes

Each configuration now has explicit first-key and scheduled-segment summaries, including per-episode expected/closed counts, hierarchy-weighted means, fixed-expert readouts and the practical learning threshold. The 30-record saved toy has only its `whole` segment, so it cannot by itself test a transfer suffix or unequal population weighting. That limitation is explicit in the output.

The disjoint dictionary probe supplies one slot in one public population and two slots in a second. Its target-suffix base-loss mean is correctly `1/2`; an execution-weighted mean would differ. First-key denominators of 2, 3 and 3 retain all eight scheduled positions while their mean loss is correctly `7/12`, rather than the pooled-position value `5/8`. These are hand-written score dictionaries, not generated scientific cases or transfer results. [Synthetic reader](../amended_synthetic.py), [results](synthetic_results.json)

Making one parent episode incomplete while leaving a selected suffix complete makes the primary suffix mean unavailable and its practical flag false. It does not drop that parent to produce a favorable mean. The expected episode and position counts remain present. This matches the amended protocol's explicit restriction on using a complete slice from an incomplete or invalid parent.

The original missing-seal, incomplete-cost and unequal-delivery-ID counterexamples remain preserved in the initial probe. This readback does not replace them with a successful-only table.

## 3. Optional public reporting

The revised score's `paid_report_comparison` compares every reported V/F/Z interval to the **same paid report's deterministic observable envelope**. Widths and signed endpoint gains divide by the scheduled horizon. The independent reader reconstructs those values from the original endpoints, checks their separate actual fee, and verifies the inclusive 0.01 predicate.

The 30 original broker records contain seven successful reports, two failed reports and 21 not-requested dispositions. The seven reports produce 21 quantity comparisons; all have zero width reduction against their observable envelopes. Their fees remain counted. These numbers concern only the already exposed development toy. They imply neither a final reporting outcome nor empirical confidence coverage. [Broker reconstruction](replay_results_v2.json), [A5 source](source/v3/experiments/p309_broker.py)

The synthetic two-population case checks the aggregate threshold exactly: gains `1/50` in the first population and zero in both slots of the second give a hierarchy-weighted gain `1/100`, which passes inclusively. Replacing the second population's gains with `-1/25` gives an adverse mean `-1/100`, which stays negative and does not pass. An incomplete parent or conflicting report makes the requested mean unavailable, retains its ID and paid fee, and prevents a practical reporting claim. A successful-report-only denominator is never substituted. [Synthetic results](synthetic_results.json)

The final source-only [protocol readback](protocol_scope_readback.md), SHA-256 `c8a403defe251c8253e46e369f279b7ece1271d09a170df2b2bb820072930952`, resolves the remaining wording ambiguity. The observer independently reconstructs **endpoint/envelope arithmetic from the saved paid report**. The inherited paid reporter reconstructs the snapshot/grid quantities from the owned transcript; this task does not add a second independently implemented verifier for all its formulas. A5 now states that division explicitly. The [membership readback](protocol_scope_readback.json) also confirms that the freeze names the inherited live-reporting, snapshot-reporting, budget-selection and selected-receipt-reuse derivations. All fair-bit, sound-receipt and all-path funding assumptions remain mathematical premises; the seeded development trajectories do not establish them.

## 4. Certificate coverage and resource vectors

The independent certificate reader reconstructs every original per-stage invoice and sums its raw categories. Producer plus consumer equals total. Output, source and storage coordinates match their declared overlapping diagnostic definitions. It checks the exact correctly delivered request IDs against the saved paid terminal statuses, then reconstructs all 144 directed comparison records across stream/family and fresh/resident scopes. [Certificate reader](../amended_certificates.py), [results](certificate_results.json)

The 13 toy histories each correctly decline the deliberately false second bound and deliver the other three requests. Equal counts are not substituted for ID inclusion, and this three-request service is not mislabeled as delivery of all four planned requests. These histories are in the original full-budget condition only. They supply no new capped-history or unseen-family result.

The amended analyzer separately reports `componentwise_named_diagnostic_dominance` and `componentwise_primitive_tariff_dominance`, retaining the aggregate coordinate convention. In the explicit 90-native-call versus 100-opcode synthetic comparison, the first stage/diagnostic vector is ordered, but primitive tariff dominance is false. The prior interpretation error is therefore prevented: a consumer aggregate improvement is not automatically a gain at every primitive price. All original all-attempt bills remain in the comparison.

## Final scope of this acceptance

The amended code is accepted for the inspected finite-panel arithmetic and failure-denominator obligations. This is not final evaluation, evidence of generalization, a new theorem verification, a physical runtime validation, an endorsement of five empirical wins, or an automatic phase/status closure. Parent-owned outer attempt-audit propagation and runtime preparation remain separate reviews. The source-only approval also does not grant permission to change the analyzer after exposure or to rerun an unfavorable scientific unit.

No further analyzer edit is requested on the basis of these checks. The original defects, the reviewer join error, all original measured invoices, and the scope limitations remain durable alongside the passing readback.
