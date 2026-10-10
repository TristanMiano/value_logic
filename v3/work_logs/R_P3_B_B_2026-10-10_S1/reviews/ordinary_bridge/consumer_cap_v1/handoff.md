# Actual consumer-cap runner: unexecuted development handoff

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-controls agent, October 10, 2026 UTC. Same-model, nonblind, post-exposure R-P3-B-B DEVELOPMENT. Zero principal or agent research-clock credit.

The [observer runner](consumer_cap_audit.py) and [prospective contract](consumer_cap_contract_v1.json) are ready for parent inspection and one declared execution. **No worker or harness execution occurred during preparation.** Ownership of these two files is handed back to the parent at the hashes below; any correction should preserve this version first.

| File | SHA-256 |
| --- | --- |
| `consumer_cap_audit.py`, 16,212 bytes, 274 lines | `774ddedcb35eb4cf2c7600b7fdfdc154167cc77a09f00a05d922439f210897fb` |
| `consumer_cap_contract_v1.json` | `1bd2453a909d482e45b97ad9465656b396465e206b1bd54e8b823ac74b8f221c` |
| `preexecution_static_check.json` | `f259f87433164515b9ad6084d9a82faf6cb8567750fc2c5410be0f12ccb9fbb0` |

## Fixed execution

The only command-line option is a new output directory. From the repository root:

```bash
python -B v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/ordinary_bridge/consumer_cap_v1/consumer_cap_audit.py \
  --out v3/work_logs/R_P3_B_B_2026-10-10_S1/development/actual_consumer_cap_v1
```

This command is supplied for the parent and has not been run. The contract fixes consumer capacity at 1,048,576 units and total capacity at 134,217,728 units for each issued request. It uses all four original streams, six edits, six original methods, and both recipient modes: **288 attempts**. It follows the original primary loop order and invokes the exact primary `R.session` constructor, including its old-input recipe handling for every method. Each session proceeds through its next prescribed edit after an ordinary charged failure. The unchanged service controls eviction, source enrollment, rebuilding and receipt withdrawal.

## Source and reference binding

The runner verifies the exact primary manifest, summary, input declaration and completed-unit log, then all nine original source hashes. The new writer requires its worker source record to be byte-identical to the primary record and checks that it still names the original eight worker files. Additional observer source and reference copies enter artifact capture and stability checks, not worker procurement.

The original log contains 29 scalar reference rows and 288 primary deliveries. The runner reuses those 29 rows, checks their full Frame and bound correspondence, and writes `reference_truths.json` with their original log line numbers. It does not invoke `FAMILY.reference_report`, `R.references`, or the scalar oracle. These references are outside the new attempt count.

The final manifest, copied original sources, this runner and contract, all four sealed primary artifacts, the complete input declaration, and extracted reference file are saved before the first `Session` or delivery. The original writer checks all captured source and input files for changes after each saved attempt. The output source tree preserves repository-relative paths for reproduction.

## Recorded outcomes and checks

Every returned unit contains the original output, full invoice, work counters, storage fields and content-addressed packet references. Added observer fields identify the exact supplied Frame/witness/bound; the matching primary log line and consumer bill; whether that original bill fits the named cap; and whether the original bill plus the failure reserve fits. Those predicates are attached after delivery and never enter the worker's inputs or request selection.

State observations record current receipt availability, equality with the paid output, stale receipt availability, scientific-cache emptiness and source enrollment. The completed unit is saved before assertions. If state observation raises, the unit and observation error are saved before stopping. If an exception escapes `deliver`, an entry records the issued input, error and unavailable invoice before the run stops with a harness failure.

Successful outputs are checked against the complete independently fixed common-service record, including the saved incumbent cutoff, supplied witness, exact Frame, bound, unit, request ID and original source record. All invoices must have nonnegative integer categories, exact total and consumer sums, and respect both actual ceilings. Every ordinary failure must withdraw current and past authority, leave scientific caches empty, retain its cause and pay the 113-unit failure terminal. A valid charged failure continues the sequence; a violated harness invariant stops and preserves the unexpected record.

The final count gate requires all 288 prescribed attempts. A `PASS` will mean the sequence and its invariants completed, not that all requested certificates were delivered. Completion counts, failed attempts and all paid prefix costs must be included in interpretation. The two static primary predicates refer to an unconstrained history; funded denial can change later cache state and bills, which is the question this run is designed to resolve.

## Preparation checks and scope

Preparation parsed the runner with Python's AST parser, checked the fixed file-location root calculation, validated the 288-attempt geometry and budgets, and verified the four primary seals plus nine original source hashes. The [static record](preexecution_static_check.json) binds those inputs. The runner was not imported, compiled to bytecode, or executed, and no worker was called.

This is a separate post-exposure funded-state experiment at a threshold already declared in the primary run. Its outcomes belong outside the primary and pruning-secondary populations. It introduces no new fixture, policy, fallback, retry, price selection or final challenge.
