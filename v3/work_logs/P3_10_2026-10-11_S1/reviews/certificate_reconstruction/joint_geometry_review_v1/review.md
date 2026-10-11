# Independent review of the joint report geometry observer

Signed: **ChatGPT (GPT-6 Astra Pro), `/root/certificate_reconstruction`**  
UTC: 2026-10-11T16:04:01.480713+00:00  
Disposition: **PASS: zero numerical mismatches; source-review findings G1 and G2 closed. One misleading diagnostic-count field name is documented below.**

## Bound artifacts and independent method

This review binds principal observer source `bf5b7fe496c30d8f85587fb790c908de2920551e0a1f714aca5e39a9da5242c3`, public geometry `b799dfefc43182d85032650e0364df3fdf48ce5eb497b9250dbe3043b5871d14`, and validation `d2fc5a797ad99e9e2da117e977d88b49090de58f8f3da9f7f6b5f2009f12ebf4`. The derivation and implementation addendum are preserved with SHA-256 `207b74d3554f0bb297bf8d25aecf673c5264b98a1bb97d34e90df798c6e3e93d` and `5e0f146f99776a302e354a395ba3a132c2153d22d8ad5412ae315144652c5ac3`. Source/data snapshots and bindings are in `initial_snapshot_manifest.json`.

The independent `independent_check_v1.py` imports only the Python standard library. It reconstructs public constants and grouped coefficients directly from the sealed input/public JSON, checks full scope, scheduled row identities, provider/version, and the exact chronological selected invoice roster, and substitutes each parent's end-of-episode paid labels. Its reads of official records match the previously independent A1 lineage inventory, with original and amended bindings preserved.

The geometric construction is different from the principal's angle-sorted edge walk: it repeatedly takes the convex hull of the current hull and its translate by one generator, using lexicographic monotone chains and exact rational orientation tests. It separately compares the area with the sum of absolute pairwise generator determinants, reconstructs every retained vertex from its saved binary mask, and checks support sums in every saved diagnostic direction. Corner membership is checked by asking whether adjoining the corner enlarges the independently reconstructed hull, in addition to checking compatibility of per-key endpoint requirements.

The independent public reconstruction was saved before parsing the existing numeric and validation payloads. The subsequent containment phase reuses the numeric truth JSON already verified by this reviewer's earlier independent forecast reconstruction; **no new truth evaluator was written or executed**. All 126 frozen F/Z scores are checked again by reading their saved JSON and verifying its public-result binding. This is an unblinded post-outcome review. It reruns no paid worker, reporter, generator, scorer, or frozen analysis and contributes zero principal research-clock credit. Its one execution completed in 22.348 seconds, with no observer failure.

## Complete reconstruction

The independent result is **PASS with zero mismatches**:

- **126/126** scheduled parents and successful paid reports, containing **10,752** positions and **2,688** selected checked receipts.
- **6,463** unresolved-key instances across the 126 parent-specific regions. These are not 6,463 globally distinct claims.
- **10,272** retained polygon vertices, each matched exactly and accompanied by a valid binary witness over its ordered unresolved-key list. The principal's 10,398 witness checks also include the closing vertex later removed from each of 126 saved polygons.
- All **378** F/V/Z sharp marginal intervals, **504** rectangle-corner conclusions, and **21** family/configuration summaries agree exactly.
- Each summary has all **six** scheduled parent reports: three seeds in each of two populations, with the declared equal-population hierarchy. No available-parent-only averaging is used.
- All **126/126** existing target triples satisfy the public F−V identity, and all recorded (F,Z) pairs are in the independent hull and in its binary relaxed image. Saved F and Z agree with the original frozen scores.

All 126 realized regions are two-dimensional; there are no points or segments in this cohort. A parent has 22–89 unresolved full keys, 19–69 nonparallel generator directions, and 38–138 vertices. The addendum and source handle zero vectors, one-point hulls, collinear segments, closing-vertex removal and zero-area denominators correctly. Those degenerate branches receive mathematical/source review; this cohort does not empirically exercise them.

**All four corners are incompatible in every report: 504/504 excluded corners.** Each coordinate's marginal extreme is nevertheless attained somewhere in the binary-key relaxation. The exclusion concerns jointly attaining two separate coordinate extrema and is not a failure of either marginal bound.

## Area summaries and dependence

The table shows the hierarchical mean of each parent's convex-hull area divided by its own marginal rectangle area. Values are rounded here; exact rational values and every original summary are retained in `summary.json` and the independent public reconstruction.

| Family | Uniform selector | Ticket selector |
|---|---:|---:|
| cheap_null | 0.49961050 | 0.62765309 |
| mixed | 0.60536163 | 0.68958104 |
| gate_transfer | 0.53067979 | 0.65192187 |

These are means of individual area ratios, not ratios of summed areas. The smallest individual ratio is exactly **6600924/20211907 ≈ 0.326585908**; the largest is **5962075/8049981 ≈ 0.740632183**. The first occurs on cheap-null population 01, uniform seed 3091002; the second on mixed population 01, uniform seed 3091002, in their corresponding coupled configurations.

For each fixed population, seed and selector, the unknown-key list and vectors are identical across the four uniform configurations or three ticket configurations. Their known-label origins can translate the region, but the polygon area and rectangle-area ratio agree exactly. Consequently the 126 records comprise **36 coupled geometry classes**, and the 21 summaries have only six distinct family/selector area means. Neither count is a number of independent statistical replications. A retained-area fraction is geometric size in the (F,Z) coordinates; it is not a probability, fraction of logically realizable CNF worlds, calibration measure, or task-loss improvement.

## Original F/V reports: width equality is structural here

All **126/126** original paid reports satisfy, exactly,

`live_center_F − live_center_V = C`,

and both the lower and upper deterministic-envelope endpoints and delivered interval endpoints satisfy the same translation. Their delivered widths and conflict flags consequently agree. This checks the original paid report, in addition to the new key-based geometry. The earlier source-review caution remains valid for arbitrary separate interval constructions; this particular reporter supplies stronger structure.

A source derivation explains the equality. Let r be the snapshot reference forecast: the base forecast except where an earlier-block checked receipt makes the snapshot exact. At a selected position, subtracting the V importance-weighted accumulator from the F accumulator cancels the selector-propensity factor. The remaining half-baseline and selected term equal `d(r,y)=r+(1−2r)y`. Subtracting all forecast-variance terms then gives

`reference_center_F − reference_center_V = sum_selected (r−y)² − sum_unselected r(1−r) = C_ref`.

The recorded reference corrections transform this into

`live_center_F − live_center_V = C_ref − reference_correction_F + reference_correction_V = C`.

The original deterministic bounds also translate term by term: selected positions contribute the same observable Brier term to the F−V difference, prior-hard unselected positions contribute zero, and every other position obeys `Brier = binary_error_functional − q(1−q)` at both binary-label endpoints. The reporter then clips both live-center intervals with the **same sampling radius** against these translated bounds. Maximum and minimum commute with a fixed translation, which proves translation of both delivered endpoints. Its exact-all-remaining-known branch preserves the identity as well.

Reference centers need their own qualifier. Their difference equals the live C on **120/126** records. On the other **six**, the difference is exactly `C + reference_correction_F − reference_correction_V`. These six are cheap-null population 01, uniform seeds 3091002 and 3091003, in value-uniform-cold, value-uniform-cached-hashed and ordinary-kernel-mirror. Their correction differences are respectively `−164904831/1073741824` and `−596537799/4294967296`. This is the intended snapshot-versus-live distinction, not a failed identity or numerical defect.

This arithmetic proof requires the admitted binary transcript and its sound, consistently bound labels. It does not need the MT path to establish independent fair bits. Any statistical interpretation of V or of the confidence intervals still retains the frozen theorem's original assumptions.

## Closed source findings and retained label issue

G1 is closed: the implementation flips into `dy > 0 or (dy == 0 and dx > 0)`, shifts the origin correctly, and merges only codirected parallel vectors. G2 is closed: one point has one vertex, one direction gives a two-endpoint segment, multiple directions give dimension two, and zero rectangle area is reported with a null area ratio. The exact output reconstructs after these source-level corrections.

**Minor field-label issue retained:** `nonaxis_support_checks` counts *all* diagnostic direction vectors, including axes. The exact saved total is **13,170 = 1,256 axis + 11,914 non-axis** vectors. These are vector queries, including positive scalar multiples, not 13,170 distinct geometric rays or independent trials. Calling them “diagnostic directions” in the interpretation is accurate. The values themselves are correct, so no source/output edit or rerun is needed.

## Interpretation boundary

The geometry is exact for a relaxation in which each unresolved full key has an independent binary label while the recorded forecasts and actions are fixed. Its support extrema and binary vertex witnesses are sharp for that abstraction; cross-key logical CNF constraints may remove assignments, and fractional convex-hull points need not be actual truth vectors. The public construction does not purchase those additional constraints.

The source and addendum adequately preserve the confidence and economic boundaries. Intersecting a valid joint confidence region with a deterministic outer region does not cost additional confidence, but it retains the original fair-bit and all-path premises and does not produce a new joint level from unrelated marginal levels. The MT finite cohort supplies no empirical coverage claim. This post-outcome observer is not the original paid reporting algorithm, does not replace A5, and has no demonstrated deployed fee or feedback-policy advantage. The unknown-prefix global economic gate remains false.

## Audit files

The independent result SHA-256 is `c0adfc9c8ae49f8e4ae4d256f8d3949df3c1d5a2876475cd51e35c21f7a4c6d8`; its saved public reconstruction SHA-256 is `02558d4f92476201ea5b63ab2a7108d049bd224c1f1c9b2e3eeaf05febe31b33`. The independent source SHA-256 is `f3b53a5d069539a245359cc30fb66d58745dcfdac17505b7877e6039d9db5fb8`. `independent_observation_v1/source_hashes.json`, its signature, `summary.json`, and `source_review_closure.json` retain the complete review trail without modifying earlier artifacts.
