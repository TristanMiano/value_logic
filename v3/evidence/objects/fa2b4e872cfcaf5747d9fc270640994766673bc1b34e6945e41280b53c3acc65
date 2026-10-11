# Independent review of forecast mechanism decomposition

Signed: ChatGPT (GPT-6 Astra Pro), `/root/certificate_reconstruction`  
UTC: 2026-10-11T15:49:11.575377+00:00  
Disposition: **PASS for the source mathematics and complete numerical reconstruction. Two exposition clarifications are requested below; neither requires changing the calculation or rerunning it.**

## Reviewed artifacts and independence

This review binds the principal's mechanism observer source SHA `0ce6254d8d210241296356dc220a244c315cf5a0acbaa0a9225f4ba9e52e1a6f`, its result SHA `cda4fd8e624e6a3efc6b2e93eed7664082853c30a4682bcab5b56697688fc428`, and the original derivation SHA `20f3369b402fe471953f210bf409f6d2ef51a721166d2f61f01c8bf1e274b55b`. Exact source/result snapshots are retained in `source_and_data/`, with `initial_snapshot_manifest.json`. The initial mechanism source and the before-execution denominator revision record are also preserved. The result's source, derivation and numeric-input hashes all match those snapshots.

A separate `independent_check_v1.py` imported only the standard library. It did not import the principal observer, lineage reader, frozen generator, paid worker, private scorer or analyzer. It read exact public and score JSON already bound by the earlier independent certificate lineage hash inventory, verified result seals/identities, and reconstructed the decomposition directly from raw recorded weights, advice, forecasts, selected labels and terminal actions. It independently evaluated 413 distinct full CNF keys by filtering sets of Boolean assignments, providing a separate truth implementation from the principal numeric observer's bit-parallel masks. No paid path or official output was rerun or modified. Concurrent review contributes zero principal clock credit.

Evidence: [independent results](independent_observation_v1/results.json), [consumed source/data hashes](independent_observation_v1/source_hashes.json), [signed output hashes](independent_observation_v1/signature.json).

## Denominators and exact agreement

The independent check is PASS with **zero mismatches**:

- All **126/126** scheduled broker/mirror parents are complete, valid and audited; zero are unavailable.
- All **10,752** positions and **2,688** four-position block profiles were reconstructed.
- All parent named slices and first-occurrence memberships/denominators match both the mechanism result and raw frozen scores.
- All **56** family/configuration/slice cells match. Each contains the exact six distinct parent episodes: three scheduled seeds in each of two populations. There are no dropped, duplicated or relabeled parents.
- Every field of each hierarchical mean agrees exactly as a rational number; every A2 value and 0.01 practical-threshold decision agrees with the frozen analysis. Whole-slice A2 also agrees with the frozen primary configuration summary.
- Configuration IDs uniquely fix the relevant stakes in this roster, so the supplemental family/configuration grouping does not accidentally combine different objectives.

The 56 cells comprise overlapping slices and coupled configurations/mirrors; they are not 56 independent statistical comparisons. The result contains 26 cells meeting the A2 practical cutoff, 21 adverse A2 cells, and 41 cells with base Brier below constant half. Those are bookkeeping counts over these overlapping views, not new inferential claims or performance rankings beyond the declared finite cohort.

The source retains scheduled configuration/slice cells even if every parent is unavailable and labels partial-parent means as descriptive. In the realized artifact all parents and slices are complete, so no partial-parent computation supplies a positive result. The hierarchy is exactly mean-within-population over its three seed paths, then the equal mean across the two populations. First-occurrence counts are not pooled to give larger populations more weight.

## Algebra and signed interpretation

For binary truth y, exact equal advice mixture r, the weighted mixture w formed from recorded weights, base forecast p and issued forecast q, all checked identities hold:

1. A2 = (r−y)² − (p−y)².
2. A2 = [(r−y)² − (w−y)²] + [(w−y)² − (p−y)²].
3. The second term is exactly (w−p)(w+p−2y).
4. With d(p,y)=p+(1−2p)y and v(p)=p(1−p), A2 = [d(r,y)−d(p,y)] − [v(r)−v(p)].

The variance-difference sign in the source and output is correct: it is baseline r's v minus base p's v, and is **subtracted** from the binary-error-functional improvement. v is a Bernoulli-parameter variance term, not the empirical temporal variance of the forecasts.

An observed aggregate example is the uniform gate-transfer whole slice: A2 is approximately −0.028801297, the binary-error-functional improvement is +0.021409869, and the variance difference is +0.050211166. The subtraction gives the adverse Brier result exactly. Fourteen of the 56 aggregate cells exhibit opposite A2/binary-functional signs, all in the gate-transfer whole or first-occurrence slices across the coupled configurations. The same pattern appears in different representations of the same underlying paths and should not be counted as independent evidence.

**Clarification R2 — distinguish pointwise signs from averaged signs.** At an individual binary-truth position, the two changes cannot have opposite signs. If y=0, A2=(r−p)(r+p) and the binary-functional change is r−p. If y=1, A2=(p−r)(2−r−p) and the binary-functional change is p−r. The multiplying factor is nonnegative in either case. Opposite signs arise only after averaging heterogeneous positions. The original derivation already mentions mixtures of positions, but an explicit sentence stating this pointwise restriction would prevent a plausible misreading of the preceding paragraph. The independent check finds zero pointwise sign reversals, as the algebra requires.

The d term is not the realized terminal loss difference. The derivation correctly states that interpreting it as conditional expected Bernoulli action error requires a matching independent fair draw. Reconstruction of one prescribed MT bit string does not establish that probability assumption. The statement is exact finite path arithmetic, with no empirical fair-bit or calibration claim.

## Quantization boundary and limitation

All recorded weight vectors contain six strictly positive integers and have mass 6×65,536. For W equal to the integer sum of weights on positive advice, w=W/(6D), p=floor(W/6)/D and D=65,536. Thus the final projection error is exactly a remainder in {0,1,…,5}/(6D). Every point satisfies 0≤w−p≤5/(6D) and absolute Brier projection contribution ≤5/196,608 ≈0.000025431315.

The observed pointwise contribution ranges from approximately -0.000019675968 to 0.000023784588; hierarchical contributions range from approximately -0.000002114960 to 0.000003191939. All are inside the theoretical bound. Its sign is nonnegative for y=0 and nonpositive for y=1. It is therefore not justified to call this arithmetic effect neutral noise. Every first block has exactly zero reweighting term, leaving only the final projection contribution before hardening.

The uniform nonnegative hierarchical weights preserve the bound. Every observed practical A2 cell consequently has reweighting contribution at least 0.01−5/196,608 ≈0.009974568685. The source's inequality and conditional full-denominator interpretation are correct.

**Clarification R1 — identify the already rounded weights inside w.** w is unrounded only with respect to the final forecast projection. It is computed using the actual integer weights after the implementation's fixed-mass update rounding and residual allocation. The 5/196,608 result bounds w→p only. It does not bound accumulated weight-update quantization, compare with a hypothetical real-valued weight trajectory, or prove that the observed improvement would persist under a different update implementation. The phrase “recorded learned weights” points toward this qualification, but the explicit limitation should appear beside the quantization claim.

The learning/acquisition interpretation is otherwise suitably restricted: uniform and ticket configurations differ in both selection behavior and update factors/bit scheduling. Their contrast does not isolate acquisition quality alone. A2 compares base forecasts with the original equal advice mixture and does not establish advantage over constant half, individual experts, a different deployed ordinary policy or the identical ordinary kernel.

## Hard-receipt and terminal chronology

For every position the independent checker reconstructed the previously acquired exact full-key receipts before considering its current selected label. It verified q=p without prior matching evidence and q=y with prior matching evidence. Therefore

    base Brier − issued Brier = prior_receipt × base Brier ≥ 0.

All **526** prior-hard-receipt positions change their forecasts. All **8,946** first-key positions have no prior same-key receipt and zero hard-forecast or hard-terminal correction. First occurrence remains a full canonical key condition; it is not a claim that different keys are logically unrelated.

At all **2,542** selected positions without a prior receipt, the issued forecast remains exactly p even though the selected checked label subsequently supplies the terminal truth. This verifies the claim that a newly bought label cannot retroactively fix the historical forecast. At selected positions both base and live terminal actions use that label; any hardening benefit to the forecast is separate from the selected position's already corrected terminal outcome.

At unselected positions, the recorded base/live terminal difference satisfies

    base error − live error = 1{prior receipt, base error, unselected} ≥ 0.

There are **98** terminal-error corrections over the fixed 10,752-position roster. The checker uses actual recorded base/terminal actions, not the binary-error functional as a substitute. This is an unweighted binary-error count; any separate priced or asymmetric-stakes interpretation must use its frozen normalization and pricing fields rather than substituting this count.

## Final scope and requested closure

No source or data defect was found in the mechanism calculation. It agrees with the original frozen A2 reference and cannot alter the primary result. Its quantization and hardening terms correctly separate final arithmetic projection, base-weight behavior, prior evidence and current terminal purchase effects. It neither supplies a free deployed controller nor changes the global economic gate.

R1 and R2 are exposition-only qualifications. A separately hashed addendum can close them without modifying the original result or rerunning any observer. The original result's derivation hash must continue to refer to the preserved original derivation bytes. Fair-bit, first-key, full-parent-denominator, no-retroactive-forecast and no-new-economic-claim qualifications are already adequate.
