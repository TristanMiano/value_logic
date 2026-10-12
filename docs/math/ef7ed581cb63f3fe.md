> **Portable math view.** [Preserved source](../../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/REVIEW.md) · [Formatting and provenance](../math_markdown.md).
> Mathematical delimiters and the repository's operator notation are normalized;
> relative links are rebased. The source's evidence bytes remain unchanged.

# Independent review of the post-outcome gate-transfer interpretation

**Signed:** ChatGPT (GPT-6 Astra Pro), `/root/conformance_reconstruction`, 2026-10-11. Principal clock credit: **0**. This is a separate post-outcome P3-10 interpretation review. It does not amend the conformance review or any frozen result.

## Verdict

**The finite-sequence moment decomposition is correct, and all reported moment values and A2 differences reconcile exactly to the saved numeric and frozen scoring results.** The independent checker covers **126/126** broker/mirror parent trajectories, **336/336** prescribed parent slices, **672** base/equal moment records, and **56/56** hierarchical aggregate cells. It also verifies **16/16** population/signature slices and **2,688** block profiles. All actual parents are available, and every aggregate retains its full scheduled denominator. There was one independent review-check attempt, which passed; no producer, paid policy, truth function, private scorer, analyzer, or principal observer was rerun. [Independent check result](../../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/run_01/results.json).

The review identifies **no material numerical defect** in the delivered gate explanation. The principal observer checked its own exact moment identity but did not explicitly assert agreement with each saved numeric/score Brier value. The separate independent checker now supplies that reconciliation: all **10,752** public-row base/equal Brier pairs agree with the numeric reconstruction, all **336** slice Brier pairs agree with sealed score values, and all **56** A2 cells agree with the completed frozen analysis. This is additional validation of saved data, not a replacement run. [Independent checker source](../../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/check_saved_transfer.py).

## Mathematics and aggregation

For a nonempty finite slice with binary labels, the identity is

```math
\overline{(p-y)^2}
=\bar y(1-\bar y)+(\bar p-\bar y)^2
 +\mathrm{Var}_n(p)-2\mathrm{Cov}_n(p,y).
```

Both variance and covariance use denominator **n**, not n−1. It follows by expanding `E[p²] − 2E[py] + E[y]`, using `y²=y`. The independent checker computes raw first/second moments, separately from the principal observer's centered-moment implementation, and confirms exact rational equality for every record.

On the same slice the label-variance terms cancel, so for the frozen equal-advice forecast `r` and recorded base forecast `p`,

```math
\Delta_{A2}=\overline{(r-y)^2}-\overline{(p-y)^2}
=\Delta\text{mean-bias}^2+\Delta\text{forecast variance}
 -2\Delta\text{truth covariance}.
```

Positive A2 favors the recorded base learner. Negative A2 means the equal-advice reference has lower Brier loss. Each component is computed within an original population/seed slice, then averaged over the three fixed seed slots in each population and over the two populations. The checker verifies that hierarchy for every aggregate against the original analysis.

The distinction from pooling is substantive for interpretation. With balanced slice sizes, pooling can preserve the scalar average Brier loss. Its moment components nevertheless include between-path terms and need not equal the average within-path components. In particular, the average squared mean bias is not generally the square of the aggregated mean forecast minus aggregated mean truth. The principal computation correctly uses the former.

This identity is deterministic arithmetic on a recorded sequence. It does not require a sampling model, and it establishes neither calibration nor causal attribution. Forecast variation is useful when sufficiently aligned with truth; its positive variance term cannot be interpreted independently as intrinsically harmful. [Reviewed derivation](../../v3/work_logs/P3_10_2026-10-11_S1/transfer_failure_derivation.md).

## Checked gate-transfer findings

Each gate population has a scheduled 64-position prefix followed by a 64-position transfer suffix, with online state carried across the boundary. Each family/configuration aggregate has **six** parents: two populations × three fixed seed slots. The independent check confirms the pre-transfer weights equal the preceding block's final weights on all 42 gate-family parent records, so no reset is hidden in this interpretation.

For `value_uniform_cold`, the exact primary A2 differences are:

| Prespecified gate slice | Equal-advice minus base Brier | Decimal |
|---|---:|---:|
| Prefix | `183688005805/4947802324992` | +0.037125171 |
| Transfer | `-468694256825/4947802324992` | −0.094727765 |
| Whole | `-71251562755/2473901162496` | −0.028801297 |
| First occurrence | `-19359868751/618475290624` | −0.031302574 |

The adverse transfer effect decomposes exactly as follows:

| Contribution to A2 on transfer | Exact value | Decimal |
|---|---:|---:|
| Equal minus base squared mean bias | `-21823249476995/316659348799488` | −0.068917117 |
| Equal minus base forecast variance | `-133474467861/35184372088832` | −0.003793573 |
| Equal minus base negative-twice covariance | `-17730491/805306368` | −0.022017075 |
| **Total** | **`-468694256825/4947802324992`** | **−0.094727765** |

These terms favor the equal-advice reference on this suffix. The base learner's mean issued suffix forecast is approximately **0.737484**, whereas the true-label fraction in each suffix is **31/64 = 0.484375**. The mean within-path base covariance with truth is approximately **−0.005312**. Its Brier loss is approximately **0.356012**, compared with **301/1152 ≈ 0.261285** for the frozen equal-advice reference. The term called squared mean bias is the average of the six within-path squared biases, not the square formed from those aggregate means. [All exact checked aggregates](../../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/run_01/results.json).

### Advice signatures and state

Both gate suffixes use only the following two six-bit advice signatures. The two populations differ in their finite label counts within a signature:

| Population | Advice signature | Positions | True | False | Unique full keys |
|---|---|---:|---:|---:|---:|
| `p00` | `(0,1,1,1,0,0)` | 22 | 6 | 16 | 22 |
| `p00` | `(0,1,1,1,0,1)` | 42 | 25 | 17 | 42 |
| `p01` | `(0,1,1,1,0,0)` | 18 | 9 | 9 | 18 |
| `p01` | `(0,1,1,1,0,1)` | 46 | 22 | 24 | 46 |

All 64 full keys in each transfer suffix are distinct. This is canonical-key uniqueness within each population; it does not assert logical inequivalence or independent examples. An identical advice signature also does not imply identical CNF content.

For the six `value_uniform_cold` paths, the mean weight carried into transfer on the three advice coordinates that always output 1 on gate queries is **857527/1179648 ≈ 0.727**. About **0.589** is on the no-unit-contradiction advice alone. The suffix forecasts remain high while the observed label fraction is below one half. These are checked features of the realized state and representation, consistent with the exact bias/covariance decomposition. They do not identify which change to the policy would prevent the loss.

Selected-feedback frequencies provide further descriptive context. Across the six uniform paths, the suffix selected true fraction averages **23/48**, close to the suffix's **31/64** population truth fraction. For the ticket selector it is **11/32**. The corresponding prefix averages are **43/96** and **1/3**, while the prefix truth fraction is **1/2**. Both selectors make 16 selections in each 64-position slice. These frequencies cannot isolate acquisition causally: selector changes also alter importance factors, bit consumption, and the inherited update trajectory. The principal derivation correctly avoids a causal selector claim.

### Other effects remain visible

The output includes all configurations and families, retaining favorable, adverse, and small effects. Representative whole-slice A2 values for the two selector configurations are:

| Family | Uniform | Tickets |
|---|---:|---:|
| `mixed` | +0.043141504 | +0.003847293 |
| `cheap_null` | +0.107834628 | +0.014548136 |
| `gate_transfer` | −0.028801297 | −0.000051562 |

On the gate suffix specifically, the ticket effect is **−0.003456914**, considerably smaller in magnitude than the uniform effect. These are finite observed differences; the review does not turn the smaller ticket loss into a causal or general superiority claim. All seven configuration labels, including deliberately duplicated finite/value/cache/mirror paths, remain in the 126-parent record. Such aliases do not provide independent extra experimental evidence.

## Retrospective fitted reference

For a signature stratum containing `n` binary labels with `k` true labels, the retrospective squared-loss-minimizing constant is `k/n`, and its minimum loss sum is

```math
k-k^2/n=n(k/n)(1-k/n).
```

The checker verifies this using the independent raw least-squares expression `k − k²/n` for every saved stratum. The principal output explicitly records `fitted_oracle_is_deployed_comparator=false` for every population/signature slice.

This reference is fitted using the evaluated labels. It is descriptive of that restricted constant-within-signature class on the realized data. It is neither an online lower bound for policies using syntax/history nor a member of the frozen deployed comparator catalogue. It receives no economic comparison, primary win, or prospective policy status. The source and derivation state these limitations correctly.

## Scope and source bindings

The derivation and observer were chosen after observing the adverse frozen gate effect; their status is **post-outcome exploratory interpretation**. Their complete denominators and exact arithmetic strengthen the description of the realized failure without making the choice prospective. No ablation, new seed, state reset, fitted controller, new query, or fresh policy run was conducted for this review. The original failed public prefix and A1 limitations remain in force.

| Reviewed artifact | SHA-256 |
|---|---|
| Principal transfer derivation | `c5a5c19a085603ee1a986d1c3036fb842d4a1dd9bbb6b4a0ba44d80dbb21db32` |
| Principal transfer observer | `ba4193ff74091beca59bae51a0527018521d4d0c509c04eb6ab1d549d4460cc9` |
| Principal transfer result | `a8965c3529347dfb78a342ad83a70f08185459a10a2f9fad50fa6f4cb869895d` |
| Numeric reconstruction result | `8f7e34aef5060b43bccb2447f87238c3b3c864c5a2e375d317472827567da82f` |
| Independent transfer checker | `9d22c4d441cb187f00424e495cf0c54efe53aef581f88a0004d0cdb1d7487fc4` |

The separate review manifest binds this note, the checked source snapshots, and the exclusive independent check result. The existing conformance review manifest remains unchanged.

**Signed:** ChatGPT (GPT-6 Astra Pro), `/root/conformance_reconstruction`. P3-10 post-outcome interpretation review; principal clock credit **0**.
