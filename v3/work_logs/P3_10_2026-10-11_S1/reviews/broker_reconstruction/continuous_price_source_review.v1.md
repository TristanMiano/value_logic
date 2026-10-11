# Static source review: principal continuous-price observer v1

Contributor: **ChatGPT (GPT-6 Astra Pro)**, agent `/root/freeze_review`.
Signed UTC: **2026-10-11T15:14:02.474597+00:00**. Reviewed source SHA-256: **ac0d00e64621f442ecb382cd4498d6ef5c00c7f88a734f55b9186bcd275d46a1**.

**Verdict: the interval and lower-envelope arithmetic passes this static review. One concrete grid-coverage validation gap should be repaired before claiming a complete frozen-grid cross-check.**

No code was executed and no final input, output, or score was read. The broker observer is unchanged. This is a separate P3-10 review and adds zero principal Research90 minutes.

## Passed mathematical checks

- `region` correctly distinguishes positive, negative and zero slope differences. It reverses the upper-bound inequality for negative slopes, handles impossible constants, retains weak/practical singleton intervals, and represents unbounded upper limits separately.
- The initial domain lower bound is zero and closed. Strict constraints below zero do not incorrectly exclude zero; a strict active bound at zero makes it open. Equal lower/upper bounds are rejected unless both endpoints are included.
- `membership` respects these bounds and flags. The strict alias comparison is impossible because the alias supplies the constant inequality `0 > 0`; a positive practical threshold similarly gives an impossible constant.
- `lower_envelope` considers every nonnegative pairwise intersection, evaluates boundary ties separately, and samples exact rational interiors. Its pruning retains a boundary whenever adjacent minimizing sets change or an extra minimizing line appears only at that point. Removing other cuts leaves a constant minimizing set between retained boundaries. Identical lines remain tied everywhere they minimize.
- `hierarchy` averages scheduled slots within each public population and then averages populations. The intercept is reconstructed from false-positive/false-negative counts under the cell's own normalized stakes; the slope averages each episode's `cold_units / horizon`.
- The calculation uses the complete declared fixed-record paths, excludes mirrors from the distinct-ordinary set, keeps ordinary identities explicit, and does not reinterpret a recorded line as a controller rerun at a new price. Unknown interrupted outer costs remain an explicit restriction on economic interpretation.

## Concrete validation gap

`frozen_cells` is a `defaultdict(list)`. The observer iterates whatever `fixed_record_repricing` rows happen to be present. It does not require equality between the expected cell set and the saved cell set, nor an exact price set/count within each cell. A missing cell therefore gives an empty loop, zero grid comparisons for that cell, and still permits global `status: PASS`. A missing or duplicate price can also escape the coverage check.

The existing arithmetic checks are correct for every row actually visited. To make the stronger complete-grid claim, require:

1. Exactly the expected fixed-record cell keys, without extra or omitted cells.
2. Exactly one row per expected normalized price in each cell.
3. The expected price set equal to the frozen descriptive grid union that cell's original normalized native prices, including the asymmetric-stakes native price where prescribed.

This check must preserve the full required catalogue when a comparison is unavailable; it should not form a favorable subset by omission. The existing `complete_declared_cell` guard is conservative because it also requires other candidate/mirror records to be complete. That can withhold some candidate-specific diagnostics, but cannot create a false positive and is consistent with its stated complete-cell scope.

## Metadata clarification

`candidate_pairwise_crossing_count = len(cuts)` counts distinct retained cut prices before active-envelope pruning, including the domain point zero. Multiple pairs crossing at the same price contribute one cut, and zero may not be a line crossing. A name such as `distinct_cut_prices_including_zero` would describe the current value accurately. This does not affect the envelope or region mathematics.

The reviewed v1 bytes remain in the principal's preserved `observer_source_snapshots/continuous_price_observer.v1.py` snapshot. This note assesses that version only; a revised implementation needs its own bound follow-up observation.
