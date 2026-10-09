# Focused controller implementation review, v2

Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation agent, 2026-10-09 UTC. Development review only. Agent time is unmeasured and receives zero principal Research90 credit.

## Review conclusion

The intended v1 repairs are present and pass the focused checks on the admitted, correctly scoped profile path. The saved v2 run has internally consistent paired outcomes, profile sums, interval coverage, selection accounting, and own-audit sums. This review found no numerical error in those saved results.

One selector control-flow defect remains when assessment exhausts its budget after price validation but before catalogue and scope validation. The return path can use the first name of an unvalidated generic profile as the fallback action. The narrow reproduction below returns `guess0` with a claimed conditional lower gain of zero. A source revision is recommended before relying on the public exhaustion/fallback interface. This defect does not affect the default 20,000-unit assessments saved in `run_v2`.

An additional malformed-input observation concerns use of `abs()` on an arbitrarily large negative integer before rejecting it. That is outside the documented bounded-input domain and does not affect the valid v2 data. It is listed separately from the selector defect.

## Frozen sources and evidence

| Source | SHA-256 |
|---|---|
| `07_computation_adapter.py`, v1.1 | `06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615` |
| `07_paid_reasoning.py`, v2 | `5c402c2ea4d142df3181b6e0344a76fd1fee2c85d78283a76ee1f9b691522a44` |
| `07_paid_reasoning_development.py`, v2 | `4cfd2ff6cab0619ee2ff89f20c731e68b4297a8b2e6c152df94b85a2308e4cc7` |

The current files and the copies under `development/run_v2/sources` matched the run manifest at review start. Exact copies are retained under `development/controller_review_agent/source_snapshot_v2`. `review_manifest_v2.json` records these source hashes and hashes of all 14 top-level run evidence files.

The retained review programs are `implementation_probes_v2.py` and `profile_binding_probes_v2.py`; their outputs are `implementation_probe_results_v2.json` and `profile_binding_probe_results_v2.json`. Both load the preserved v2 sources, reuse the saved evidence, and create new result files without overwriting prior outputs. The full development driver and old suites were not rerun. A second independent agent reviewed profile identity, builder/freeze, scope binding, and procurement; its conclusions agree with the retained focused probes.

## Remaining selector defect

`select()` reserves 256 final-readout units and one output unit. Its optional meter then pays 64 preflight units. Once prices are validated, it attempts to pay the 976-unit catalogue/range/scope comparison. If that payment fails, the `BudgetExhausted` handler resets `selected` to zero. The final return subsequently chooses `profile.names[selected]`, even though no check has yet established that position zero is the current public fallback.

The focused witness starts with the saved immutable profile and swaps its first two policy names. This remains a structurally valid generic `Profile`, but it is not the current modular catalogue and should never be used to select a named modular policy. No unbounded value, mutation after construction, or private state modification is needed.

| Assessment cap | Observed result |
|---:|---|
| 320 | Fixed `fallback`, no profile identity or priced certificate |
| 321 | `guess0`, kind `assessment_budget_exhausted`, conditional lower gain `0`, supplied profile identity returned |
| 1,296 | Same incorrect `guess0` result; 321 units spent |
| 1,297 | Correctly rejects the mismatched catalogue |
| 20,000 | Correctly rejects the mismatched catalogue |

The consequences are greater than a display mismatch if callers execute the returned policy. At the saved high price vector and public population, the exact expected saving of `guess0` relative to fallback is `-855/31` per query. A conditional lower value of zero is not valid for that returned action. The positive-certificate booleans happen to remain false, but the action and numerical lower field are still inconsistent.

The exhaustion path should return the fixed public fallback independently of unvalidated profile contents. A separate admission flag can prevent profile-bound identity, scope, and statistical fields from being returned before the catalogue/scope comparison succeeds. Validated prices can still support explicitly unprofiled accounting if desired. The important property is that an incomplete admission cannot alter the fallback or bind a certificate to unchecked metadata.

## Complete-policy resource boundaries

The v2 disjoint meter partitions resolve the former output/category-limit and pending-job problems. The isolated review checked 120 cases: two bounded queries, four policy types, and 15 response budgets including zero, one, the cleanup-reservation threshold, several partial-computation points, and the full 1,024-unit cap. One query uses maximum-length ASCII query and source labels and exponent 191.

Every checked case obeyed total, per-category, and partition limits. No adapter retained an active job at return. At budget zero, no action or initial report was issued. At budget one, terminal output could be issued without an unfunded initial half report. The public half report is only present when its forecast charge succeeds.

Timeout and denied-computation paths explicitly call the public cancellation API using the separately reserved cleanup budget. The maximum-label cap-6 example returned fallback after 270 counted units and recorded one cancelled-job release. The full policy on that query returned the correct checked answer after 445 units and recorded one completed-job release. Acquisition and terminal output are funded before the returned answer/action is exposed. The adapter source remains v1.1; no arithmetic implementation or prior evidence was changed for this review.

The uniform accounting statement remains an abstract operation-model statement. The default response leaves 958 units for optional work, 65 for cleanup, and one for terminal output. The previously reviewed bounded cold-completion calculation fits the optional partition, with the extra initial forecast unit. This is not a measurement of Python runtime, operating-system work, or heap allocation.

## Profile construction, identity, and admitted arithmetic

The frozen profile now requires exact capped ASCII policy and feature identities before uniqueness hashing. Mutable feature aliases, non-ASCII text, and a 65-character feature label all reject. The profile digest is computed during paid construction and cached. Replacing the process-local hash function with a failing sentinel did not affect subsequent identity reads.

The generator/driver source hash now changes the profile law scope. Changing only that hash changes `actual_scope()`, and the saved profile matches the independently reconstructed scope. With enough budget to perform admission, the modular selector rejects a supplied range matrix that differs from the exact current `paired_ranges()` matrix.

The builder pays its bounded metadata-admission bundle before allocating its working matrix. It funds the row bundle before inspecting any data cell. Both a valid row and a row with an invalid final cell at budget zero now raise `BudgetExhausted` without inspecting that final cell. A funded invalid row consumes the declared 421-unit bundle and leaves both the row count and sums unchanged.

Freezing pays 16,384 profile units and 8,192 retention units before creating the immutable object. Its returned setup vector includes those new charges plus the complete external resource vector. The retained probe verifies this directly. Reading the cached identity does not add an unrecorded reconstruction or hash step to selection.

The valid setup-to-recover domain is now explicitly limited to nonnegative fractions with at most 256-bit components. The former accepted 2,048-bit setup counterexample rejects. A focused admitted fraction at the 256-bit boundary completes with the paid 256-unit final bundle; the largest rational component returned in that case has 291 bits, below the 2,048-bit primitive cap. Source inspection confirms that final online-cost, horizon, subtraction, and certificate arithmetic passes through `exact()` before return. This single boundary probe is not an exhaustive arithmetic proof; the bounded domain and guarded operations supply the relevant implementation argument.

For malformed inputs outside that domain, `abs(q.numerator).bit_length()` can copy an arbitrarily large negative numerator before rejecting it. The range validators similarly use `abs(x) > 1_000_000`. Direct `numerator.bit_length()` and ordered endpoint comparisons avoid those copies. No claim about hostile arbitrary-size input admission should be inferred from the valid-input operation cap until that boundary is clarified or changed.

## Saved paired data, intervals, and selection accounting

The review reconstructed the saved evidence without executing the full experiment again:

- All 1,024 acquired profile rows match the public population row with the same index, including mathematical input, checked label, action, status, initial report, feature vector, and paired vector.
- The sampled indices exactly reproduce the declared profile seed 307083. The four saved prefix sums at 128, 256, 512, and 1,024 match the raw rows, and every paired coordinate lies within its analytic range.
- All 248 exhaustive population rows reconstruct the saved feature means and paired means exactly. Profile and population IDs do not change the counted query behavior in this cold-episode interface.
- The four integer radii satisfy both `2*n*r*r >= k` and the simultaneous tail-budget inequality for 22 nonconstant cells, four declared prefixes, and delta `1/20`. All four use `k=12`. The resulting intervals contain the exact population means for this saved realization.
- All 72 saved selections conserve their declared meter totals. Their reported assessment cost is exactly the price vector dotted with the recorded resource categories. Their all-in lower gain equals conditional lower gain minus actual assessment cost minus stated setup recovery. Each saved lower field is below the corresponding exact population gain.

The ordinary same-interface comparator is literally the same selector supplied the same frozen profile, prices, horizon, and setup cost. Its recorded equality therefore establishes representation/equal-access consistency, not a separate superiority experiment. The public population structure and public shortcuts remain available to ordinary methods. The exact enumeration and private reference answers do not enter sampled-profile selection.

The gross-value screen is also paid. Its stated lower assessment cost uses a mandatory 160-unit radius bundle, so it is a conservative screen for this fixed complete-assessment catalogue. It is not a claim that every conceivable ordinary controller needs that cost or that acquiring a profile is always economically useful.

## Procurement and own-audit accounting

The saved profile's setup vector is exactly the sum of all executed policy-resource vectors plus its profile-building meter. It includes the 8,192-unit builder admission, all four freeze/hash bundles totaling 65,536 profile units, all four retained-profile bundles totaling 32,768 storage units, source registry read/hash work of 17,624 units, public population construction of 992 units, and population retention of 496 units.

The resulting profile procurement totals 1,695,543 abstract units. The standalone exhaustive population diagnostic totals 360,126 units, including 248 separately identified private reference-call counts. Removing those diagnostic calls leaves the deployable checked-outcome enumeration at 359,878 units. These raw totals only have an economic meaning after a declared category price vector is applied. The exhaustive path now pays the same source-registry/population startup routine as sampled acquisition and pays a final retention bundle. It does not inherit those resources free from the preceding sampled run.

The own-audit scope is distinct: a fixed acquired profile is already present, selection is repeated under fixed prices, and every mathematical query starts with a fresh adapter/cache. This is a warm-profile, cold-query episode. Acquisition of the original deployment profile remains separate setup. The audit neither updates the selected controller nor feeds its outcomes back into the profile used for that audit.

All 256 saved audit rows reproduce seed 307081, have exact baseline-minus-controller pairing, remain within their analytic ranges, and sum to the frozen audit profile. Their reported three-way observed costs reconstruct exactly from the raw features. Because the frozen selected policy is `full_fallback`, controller and charged-exact query outcomes/costs coincide; the controller's additional assessment and storage charges explain its extra deployment cost.

The audit closure digest reconstructs from the recorded closure contents and binds the three frozen source hashes, profile identity, prices, reset rule, batch size, and audit seed. Its saved timestamp precedes the first audit-row generation by program order. Source changes require a new bound profile/audit scope and fresh independent evidence rather than relabeling this audit as an evaluation of the new version.

Self-audit procurement now includes the preliminary selection, registry startup, closure hashing/retention, builder work, query/evidence costs, and final profile freezing. Its setup vector matches the saved procurement vector. The separate final audit check consumes 1,094 units and must be added when presenting procurement plus final checking as one total. The positive `9844159/40960` lower gain per batch concerns the fixed deployment comparison with fallback; it excludes audit procurement and does not show an advantage over the charged-exact comparator.

## Disposition

The v2 source/evidence review is complete and preserved. The source freeze for this review may end. A narrowly versioned fix to the incomplete-admission fallback branch, followed by focused boundary verification, is warranted. The v2 data remain readable development evidence for their exact frozen sources. No root controller/driver, old P3-01–06 evidence, clocks, ledger, plans, gates, or publication files were changed by this review.
