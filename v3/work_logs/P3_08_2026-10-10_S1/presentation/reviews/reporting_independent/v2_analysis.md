> **Portable display copy — notation only.**
>
> Original: [v3/work_logs/P3_08_2026-10-10_S1/reviews/reporting_independent/v2_analysis.md](../../../reviews/reporting_independent/v2_analysis.md)  
> Original SHA-256: `7099e4db09a2ccc31f4e5623eeb56bb020ee339184c61b41555ae44ddc3e9819`.
>
> Generated with the unchanged math guard's `transform(protect=True)`,
> plus relocation of relative links to their original destinations.
> The original scientific document remains unchanged. This is a source-notation
> check, with no live-render or new mathematical validation claim.

# Independent public-only audit of reporter v2

Disposition: **PASS for the sealed public replay and declared finite contract.** The independent implementation compared 180 reports, four constructions on each of 45 public broker episodes. All 192 checks passed. No private score archive was read. This is same-model, nonblind DEVELOPMENT review with zero principal time credit. These repeated analyses of already sealed traces are retrospective; they do not establish prospective empirical coverage.

## Exact source and evidence

The audited reporter is `p308-live-performance-v2`, 24,013 bytes, SHA-256 `990f3b417d4ab366a9be7baccb137d4335d90d284354c61d3d8f15dbfeafe0e1`. The source and imported dependency closure are copied under `v2_run_v1/source`; before and after manifests are identical. The public input archive has SHA-256 `2ba7748ea44b71c15c13044ba77148a5076e4776e5b9f99c54dcd4c1482dc566`; the 180-report public replay archive has SHA-256 `bc7bb4970de4abaebdf37dfab01b3fa15b8ec4eae519847916f2d0a62fe39f18`.

`audit_reporting_v2.py` reconstructs expectations from public issued forecasts, selectors, checked receipts, and independently sealed configuration flags. It does not import the reporter's calculator to construct expected values. It uses exact rational arithmetic and explicit block-entry copies of known answers, a different representation from the production reporter's receipt-block test. The earlier independent audit helper is used for source/cost inspection, not to generate v2 mathematical expectations. Complete comparisons, focused probes, width comparisons, and bounds are in `v2_run_v1`; `summary.json` supplies the reproduction command.

## Four constructions and chronological hard masks

The Cartesian product is reference basis `base` or `snapshot`, and radius rule `fixed` or `grid`. For each construction the audit independently reconstructs the selected index and actual propensity from the executed uniform or ticket selector; a snapshot reference must not substitute the propensity of a hypothetical selector that would have preferred different queries.

For the snapshot basis, $`H_0`$ means the exact key had a checked answer at block entry. $`H_1`$ means it had one before the particular issuance. The independent reconstruction verifies $`H_0\leq H_1`$, removes block-entry known positions from the reference residual and range, and translates only newly known within-block positions by their exact public loss deltas. Raw live corrections and reference-relative corrections are separately compared. Thus a receipt obtained later cannot retroactively turn an earlier forecast into a hard answer. Base-basis reference centers agree with the earlier construction, while snapshot centers are independently calculated from the frozen mask.

Hard mode is taken from the sealed broker configuration in the independent expectation. The production legacy inference is therefore actually tested rather than copied. Explicit Boolean mode, the per-row hard flags, prior checked receipts and final retained/active counts must agree. A hard-off trace can contain purchased checked receipts without treating them as hard reuse. The exact-all-known exception is validated using what was public at each issuance and what was subsequently checked for selected positions.

## Grid arithmetic and finite bounds

The audit enumerates the predeclared geometric rate set, including the original fixed rate and deduplicating it when it is already a power-of-two multiple of the propensity denominator. It independently computes $`J`$, $`c=\lceil\log_2(80J)\rceil`$, and every rational candidate radius $`Q/R+cR/8`$. If several rates tie, any true minimizer is accepted. It checks the selected rate, minimum radius, resulting interval clipping and the fixed-end action tail. The mathematical justification and prospective-choice restriction are reviewed in `snapshot_grid_math/review.md`; this implementation audit does not replace that argument.

Across all admitted finite grid shapes, the earlier exhaustive bound reconstruction gives $`J\leq9`$, $`c\leq10`$, and an exact maximum of 215 bits for the relevant radius cross-product precheck. A simpler symbolic bound is 229 bits, below the reporter's 256-bit cap. The largest value actually encountered in this replay was 97 bits. The coarse source-derived primitive-cost bound is 138,434,527,232, below the report budget of $`2^{48}`$; the inspected per-row operation count is 58, within its conservative 100-operation allowance. Actual report bills ranged from 53,184 to 836,632. These are claims in the declared integer-operation tariff, not physical CPU/heap measurements or inclusion of historical source development.

## Focused new boundaries and adverse comparisons

Focused probes accept consistent explicit true/false hard modes and reject a contradictory hard mode, a non-Boolean explicit mode, incorrect zero and inflated final store counts, and a mutation with block-entry knowledge but a false later hard flag. Unknown reference/radius names are rejected. A public ticket example exercises deduplication when the original fixed rate is already in the geometric grid. The prior v1 audit remains the evidence for unchanged receipt, source-tag, propensity, late-budget and key-scope boundaries; this replay does not multiply those unchanged tests.

Snapshotting strictly reduces $`Q`$ on 15 of the 45 episodes. Its combination with the grid is not uniformly narrower: snapshot/grid has smaller radius than base/fixed on 16 episodes and larger radius on 29, with no ties. Relative to snapshot/fixed, the grid radius is smaller on 15 episodes and larger on 30. The union correction can outweigh rate selection. These adverse comparisons are retained in `v2_run_v1/public_width_comparisons.json`; none is filtered out as an unsuccessful reporting case.

The accepted claim is exact public formula agreement and contract validation for the sealed finite replay. Choice of basis/radius must precede episode outcomes for a prospective coverage claim, and every sampling path must fund the declared service obligations. Neither a successful retrospective replay nor successful-path conditioning supplies those missing premises.
