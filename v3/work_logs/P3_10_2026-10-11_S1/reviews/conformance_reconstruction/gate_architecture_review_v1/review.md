# Gate architecture decomposition: independent mathematical review

**Signed:** ChatGPT (GPT-6 Astra Pro), `/root/conformance_reconstruction`, 2026-10-11. **Source-only; zero principal clock credit.**

**Disposition: the decomposition and its projection inequality are correct under the declared hypotheses.** I found one narrow premise-wording issue concerning prior receipts. No saved-data calculation, production run, truth evaluation or empirical experiment was performed in this review.

The reviewed source is preserved as [derivation.reviewed.md](sandbox:/workspace/scratch/095cdac579b7/value_logic/v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_review_v1/derivation.reviewed.md), SHA-256 **`d1429792630f6ce44b097f818d6fec625ba52cd16fd1d47adcaf6cfba959bcc9`**. Its numerical checks are prospective tasks within this already post-outcome interpretation; this mathematical review does not assert that those checks have run.

## 1. Exact decomposition and constrained minimum

Fix a block. For each present signature group g, assume binary labels, n_g > 0, empirical mean mu_g, and a common forecast p_g. Expanding the squares and using the definition of the empirical mean gives

```math
\sum_{i\in g}(p_g-y_i)^2
=\underbrace{n_g\mu_g(1-\mu_g)}_{I_g}
 +n_g(p_g-\mu_g)^2.
```

This is a deterministic finite identity. It requires no iid, exogeneity, calibration or population-law assumption. Binary labels are needed for the displayed form of I_g; for general real labels it would instead be the within-group sum of squared deviations. A group of one label is pure and has I_g = 0. An absent group contributes zero and has no defined empirical mean.

When both groups are present, put N = n_0+n_1, w = n_0 n_1/N, delta = mu_0-mu_1, and let mu_bar be their weighted pooled mean. For forecasts satisfying 0 <= p_0 <= p_1 <= 1, write d = p_1-p_0 >= 0 and p_bar for their weighted mean. The part of the loss above I = I_0+I_1 is exactly

```math
J(p_0,p_1)
=N(\bar p-\bar\mu)^2+w(d+\delta)^2.
```

If delta <= 0, the two empirical means are feasible and attain J = 0. If delta > 0, the minimum is attained at d = 0 and p_bar = mu_bar: both forecasts equal the pooled mean, which lies in [0,1]. Consequently

```math
M=w(\max\{\delta,0\})^2,\qquad
\min_{0\le p_0\le p_1\le1}\text{Brier sum}=I+M.
```

This verifies the claimed pooling penalty, including the probability-box constraint. If a signature is absent, its unused forecast can be chosen above or below the observed group's empirical mean as required, so M = 0 and the observed group still attains its mean. The equality case delta = 0 also has M = 0. These branches should be applied before any division by an absent group's count.

For any actual feasible ordered pair, E = actual Brier sum − (I+M) is therefore nonnegative. The formula concerns sums within a block; episode means require summing the block terms and dividing by the complete episode-slice denominator.

## 2. The projection cross term really can be nonzero

In the pooling case delta > 0, let q = mu_bar. A second expansion gives the useful exact identity

```math
E=n_0(p_0-q)^2+n_1(p_1-q)^2
  +2w\delta(p_1-p_0).
```

The last term is nonnegative because the actual pair is ordered. It vanishes if the actual pair is pooled, but is generally positive. Thus the derivation is correct to reject replacing E by only the squared distance to the fitted pair. In the nonpooling case, the fitted pair is the two empirical means and E is simply the weighted sum of their squared forecast deviations.

For a direct two-position check, take n_0 = n_1 = 1, mu_0 = 1, mu_1 = 0 and actual forecasts (0,1). The actual sum is 2, I = 0, M = 1/2 and E = 3/2. Squared distance to the pooled pair (1/2,1/2) is only 1/2; the remaining 1 is exactly the cross term. This is hand arithmetic illustrating the identity, not an additional experiment.

A further deterministic consistency bound is 0 <= I <= I+M <= N/4. The last inequality holds because a constant forecast equal to the whole block's empirical mean is always feasible and has sum N mu_bar(1−mu_bar) <= N/4. It applies to the hindsight optimum; it does not upper-bound the actual learner's loss.

## 3. Hypotheses and interpretation

| Premise | Role and review boundary |
|---|---|
| Binary labels and complete group membership | Needed for I_g = n_g mu_g(1−mu_g) and the exact full-denominator identity. Binding the saved truth transcript to the public positions remains a data-audit obligation. |
| One actual forecast per block/signature group | Required for the group decomposition with a common p_g. A method that reacts to an additional feature or changes forecasts within a group belongs to another class. Direct trace checks of within-group equality are sufficient. |
| Actual pair in 0 <= p_0 <= p_1 <= 1 | Needed for the relaxed optimum to lower-bound actual loss. Nonnegative weights with **positive total mass**, fixed within the block, and a common monotone output quantizer provide the stated sufficient mechanism. The proposed direct forecast-order checks remain necessary to establish the actual trace's membership. |
| No intervening hard-receipt modification of that base forecast | This is a structural path premise, not a consequence of the projection theorem. See the wording issue below. The planned direct no-prior-receipt check supplies the required evidence if successful. |
| Arbitrary real block-specific fitted forecasts with hindsight labels | Makes the fitted class a relaxation of the deployed positive-integer, update-constrained and dyadic class. The minimum is a lower bound on that restricted architecture's recorded loss, not a funded online strategy or a new ordinary comparator. |
| All blocks, groups and hierarchy retained | Compute I and M separately for each actual population/block, including pure and absent groups, then aggregate. Refitting after pooling blocks or populations changes the class. The proposed 64-position denominators, 16 blocks per population, two populations and all 42 records are planned audit coverage, not numerical facts newly verified here. |

The source's interpretation is appropriately narrow. I measures mixed labels sharing the stipulated block/signature representation. M is the additional hindsight cost of the monotonicity restriction on that same class. E is the remaining actual excess over its relaxed optimum; it cannot identify the causal contribution of selection, updates, quantization or information delay. No part supplies a bound on all logical reasoners: another method can inspect the full public CNF or compute additional features. The fitted empirical means are not thereby population probabilities or earlier beliefs.

I and M depend on the population's fixed block/signature labels, so replaying multiple methods or seeds does not create new structural label examples. Method-dependent E can still vary. The draft correctly keeps the 42 policy records visible while separately reporting the two-population/32-block structure and the frozen seed-then-population hierarchy.

## 4. Narrow wording issue: suffix uniqueness versus prefix receipts

**GA-01.** In §1, the implication “The suffix has unique full keys, so there is no prior matching hard receipt” needs an explicit scope. Keys unique **within the suffix** could still match keys purchased in the prefix. Either say that every suffix key is new relative to the **entire prior episode history**, if that is what the saved audit establishes, or rely directly on the planned current-receipt check. The latter is already listed in §4 and is sufficient for the intended argument.

Suggested wording: “The audit must establish that each suffix full key is new relative to the earlier episode history, or directly establish the absence of a prior matching current hard receipt; consequently no such receipt changes the base signature structure.”

This issue concerns the justification of trace membership, not the algebra of I+M+E. A negative exact E in later computation should be treated as a failed feasibility/binding premise or calculation, rather than clamped away.

## 5. Preservation

Only this owned review directory was written. The principal derivation, draft results, official artifacts, accepted statuses and gates were left unchanged. `manifest.json` binds the source snapshot, start record and this signed review. No data observer or private payload was executed or read, and no conclusion about the yet-uncomputed I, M or E values is asserted.
