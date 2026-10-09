# Portable formatting view

This is a display copy of [the original source-bound analysis](analysis.md).
Only math delimiters/macros are normalized below; the original evidence file
remains unchanged at SHA-256 `867bb706a0fe8ff7f6739381ca0451166bfe2c3c64d367da3e0350b49c5017f6`.

---

# Observable episode certificates from purchased labels

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. R-P3-B-A,
**DEVELOPMENT; zero added principal-clock credit.**

Both prospectively specified offline diagnostics completed on all **20
existing uniform arms and three existing adaptive arms**. Purchased labels
and immutable public forecasts suffice to calculate explicit upper
certificates for episode performance. The centered extension also exposes
an exact relation between immutable Brier loss and unbought conditional
action loss, so one sampling event can support both targets. These are
source-bound mathematical and analysis results. No policy, service, random
seed, private label computation or deployed invoice was changed.

The [baseline design](../observable_certificate_design.md) and
[centered design](../centered_certificate_design.md) were saved before their
respective calculations. Complete exact rows are in the
[baseline public result](public_stage_001/result.json) and
[centered public result](centered_public_stage_001/result.json). The
[full grid](full_grid.md) provides a readable numerical comparison; exact
fractions remain authoritative.

## Public-only computation and later private comparison

Each first-stage process opened only allowlisted public transcript,
selected-receipt and allocation members. The uniform container also holds
private material: its whole-file SHA256 was computed over opaque ZIP bytes,
but private members were never decompressed or deserialized. The reader did
not run a whole-container `testzip()` that would open those private members.
Instead, reading each permitted public member verified that member's CRC
and its saved payload hash. Metadata manifests provide provenance without
opening the private results whose digests they name.

Both first stages checked **49,600 public rows and 10,664 selected labels**.
They rejected any purchased-label field on an unpurchased row, checked
receipt identity/status and exactly one receipt per block, and always used
the probability emitted before the selected answer was bought. A terminal
action corrected by a receipt never replaced that earlier forecast in a
loss estimator. Adaptive selected propensities were reconstructed from the
published favorite and ticket multiplicity. Current-block width calculations
used the complete public probability vector for every position.

Each public-only result was saved and hashed with its reader audit and
compressed selected-observation terms before a separate comparison program
was invoked. The baseline public stage closed at **22:36:35 UTC** and its
private comparison began at **22:37:31 UTC**. The centered public stage
closed at **22:41:26 UTC** before its own separate comparison. Those second
stages read already saved private score summaries; they did not calculate
any new labels. Each first-stage seal records zero preceding private-score
reads.

The audit is an explicit code/reader and schema boundary, not a claim of
general operating-system information-flow isolation. Source, archive,
member and output hashes, commands, timestamps and reader events are retained
in each stage. The [final identity/integrity audit](shared_identity_audit.json)
checks both seals, both public reader logs and the compressed analysis
outputs. It also checks the common-deviation identity against the later
private scores.

## Baseline certificate

Let `d_t=q_t` when `y_t=0` and `d_t=1-q_t` when `y_t=1`, using the actual
issued dyadic probability. Let `g_t=(q_t-y_t)^2`. If position `J` is purchased
with propensity `pi_J`, the observable selected contributions are

```math
U_k=(\pi_J^{-1}-1)d_J,
\qquad A_k=g_J/\pi_J.
```

The first estimator targets the realized-selector conditional action mean
`V=sum_unbought d_t`; the second targets immutable all-issued Brier
`F=sum_all g_t`. Their martingale sampling deviations separately have
conditional range width at most `S`, where `S=B` for uniform sampling and
`S=2B` for the adaptive ticket rule. This is a statement about the frozen
block and fair selector contract, not an assumption of IID labels.

For `m=T/B`, the exact conservative sampling radius is
`R=S*ceil_sqrt(2m)`. The terminal action radius is
`ceil_sqrt(2(T-m))`. They use `log(40)<4` to avoid floating-point logarithm
or square-root uncertainty. The calculator retains the integer radicands,
ceiling-root witnesses and exact Fraction estimators. The resulting upper
bounds are `U+R` for `V`, `A+R` for `F`, and `U+R+action_radius` for sampled
terminal loss, clipped at `T-m` or `T` as appropriate.

Under the fresh fair-randomness theorem premises, the mean and Brier upper
statements **separately** have at least `39/40` coverage. Adding the action
tail gives at least `19/20` for terminal errors. This baseline calculation
does not claim joint terminal-plus-Brier `19/20` coverage, nor simultaneous
coverage for 23 episodes. All 23 computed upper bounds are below their
trivial range caps. Every displayed inequality happens to hold against the
saved private scores, but no seeded inequality was a pass/fail requirement
or a coverage experiment.

## Centering exposes one shared unknown residual

For binary labels, set `v_t=q_t(1-q_t)` and `r_t=d_t-1/2`. Then `g_t=d_t-v_t`,
which gives the exact episode identity

```math
F-V=\sum_{t\,\mathrm{selected}}d_t-\sum_{t=1}^{T}v_t.
```

The right side is already known after the purchased receipts arrive.
Centering the two observable estimates therefore gives

```math
U_c=\frac{T-m}{2}+\sum_k(\pi_J^{-1}-1)r_J,
\qquad
A_c=\frac{T}{2}-\sum_t v_t+\sum_k r_J/\pi_J.
```

Now `F-A_c=V-U_c`: the two performance targets have the same unknown
sampling residual. The public calculator verifies
`A_c-U_c=sum_selected d-sum_all v` using only public forecasts and selected
labels. The separate later audit verified this correction equals the
private `F-V` in every one of the 23 saved episodes. It also verified
`U_c=U` in all 20 uniform episodes; adaptive centering may change `U`.

For each frozen block define the public predictable bound
`C_k=max_t |1-2q_t|/pi_t` and `Q=sum_k C_k^2`. The reported radius is

```math
R=S\lceil\sqrt{2m}\rceil,\qquad
\lambda=8/R,\qquad
R_c=Q/R+R/2.
```

The choice of `lambda` is determined solely by the declared `m,S`. It is
not optimized after seeing `Q`, labels or private scores. This matters:
the realized random `Q` cannot simply be substituted into a retrospectively
optimized fixed-variance Hoeffding expression. The specified fixed-lambda
exponential argument permits this predictable quadratic term. The
calculator checks exactly that `Q<=m*S^2` and `R_c<=R`.

The centered estimates can be signed; the code preserves signed numerator
accumulators. It reports raw upper bounds and clips them at zero and the
valid public deterministic caps:

```math
V\le\sum_{t\,\mathrm{unbought}}\max(q_t,1-q_t),
\qquad
F\le\sum_t\max(q_t^2,(1-q_t)^2).
```

Realized terminal errors retain the `T-m` cap. They do not use the smaller
conditional-mean cap. At `q=1/2` everywhere, the public caps themselves give
the exact `V=(T-m)/2` and `F=T/4`; no label sampling is needed to know those
losses. Certificate precision describes knowledge of performance, and does
not by itself make the forecast perform well.

Under the centered theorem contract, one sampling event supports both `V`
and `F`; one additional action tail yields joint at least `19/20` coverage
for terminal errors and immutable Brier at a fixed endpoint, for one arm.
The action step is fixed-end. This report does not claim an anytime joint
terminal certificate or simultaneous coverage for all 23 arms.

## Numerical effect on the existing episodes

Every centered reported upper bound is smaller than its baseline counterpart
in this saved grid. Conditional/terminal reductions range from approximately
2.5714 to 273.6050; Brier reductions range from 1.8067 to 231.0285. These are
descriptive comparisons of already specified formulas on the same saved
public observations, not evidence that a forecast or policy became more
accurate. The source controllers, purchases and decisions are unchanged.

Selected examples follow. Displayed upper values are rounded **upward** to
six decimal places; the JSON records retain exact fractions.

| Existing episode | Baseline terminal upper | Centered terminal upper | Baseline Brier upper | Centered Brier upper |
|---|---:|---:|---:|---:|
| Uniform 3,968 / 8, state16 | 2,041.466126 | 2,012.253451 | 1,699.711845 | 1,670.306538 |
| Adaptive 992 / 4, state16 | 620.687897 | 541.751162 | 485.349656 | 410.805818 |
| Adaptive 992 / 8, state16 | 759.784986 | 660.390408 | 556.673143 | 444.624649 |
| Adaptive 3,968 / 8, state16 | 2,482.545414 | 2,208.940439 | 1,762.685237 | 1,531.656728 |

For the uniform 3,968/8 normalized episode, the centered sampling radius is
226.787325 instead of 256. For adaptive 3,968/8, it is 352.172803 instead of
512. The centered 992/4 and 992/8 adaptive conditional-mean bounds are
clipped at their public deterministic caps; the latter's Brier bound is
also clipped there. In these three cases the final cap should not be
credited to purchased-label concentration. Across the grid, 21 conditional
and 22 Brier bounds remain strictly below their respective public caps.

All 23 centered inequalities happen to hold against saved private scores.
The audit requires the exact shared-residual identity and source/output
integrity, not this probabilistic inequality. Fixed MT seeds are formula
illustrations and do not validate frequentist coverage.

## Resource and preservation scope

Current raw baseline accumulators reach at most 31 bits for `U` and 46 for
`A`; centered signed-magnitude accumulators reach 30 and 47 bits, with 54
bits for the raw `Q` numerator. These are the observed accumulator widths,
not bounds on every temporary integer used by Python's Fraction arithmetic.
The larger admitted action precision can require more than one 64-bit word.
An online deployment would need to price signed updates, width computation,
division, retained records and certification explicitly. This offline
calculation adds no free capability to the old metered deployment.

The public calculation runtimes were about 1.423 seconds for baseline and
1.610 seconds for centered, excluding their final output packaging. Runtime
is external analysis metadata and is not converted into abstract resource
units or principal research-clock credit. No experimental budget, actual
purchase bill, learner invoice or earlier score was modified.

Three small deterministic output ZIPs preserve the baseline selected terms,
centered selected terms and centered public block ranges, totaling **897,936
bytes**. Their manifests record raw member length, count and SHA256. The
final read-only audit checked archive/member hashes and CRCs, seals, both
reader logs, all uniform centering identities and all 23 public/private
shared residuals. No loose raw JSONL duplicates were written. The original
uniform and adaptive evidence archives remain untouched.

## Exact bindings

- Baseline public result SHA256:
  `d41e0f2f4ee07f9d33ad69947cd0e14438d66b6db3d027846f5087d871dd3ff9`.
- Centered public result SHA256:
  `ccc3fe8098155b380b76200d0a3c446438c186e63927baeff739e49d350b3e30`.
- Baseline private comparison SHA256:
  `95fc8835f51f61ac3daf729a2c52e4c194f0265d6d1198e729edceeabdafe019`.
- Centered private comparison SHA256:
  `0eb0c627e8c5cdacefb3aeb8091486d1eb28c08c7ce34ab0e03a3d3df1e52dc3`.
- Shared-identity/output audit SHA256:
  `76da2b2537865b8ff474b9a7e7154e4f120a6e58f7e9bfde52b559c466fd92e5`.

Each public result and protocol contains complete source, source-design,
archive and opened-member bindings. No scientific rerun, new seed, tuning
choice, P3-08 activation or plan/ledger edit was performed by this agent.

## Final separately planned two-sided diagnostic

After the foregoing stages were complete, root saved
[two_sided_design.md](two_sided_design.md) before this final calculation.
The additional question is whether the paid evidence can also identify an
episode whose forecast is worse than the immutable no-information Brier
null. Earlier private scores were already exposed when this design was
written; this is additional DEVELOPMENT analysis, not a new confirmatory
experiment.

The final [public-only result](two_sided_public_stage_001/result.json)
consumes only the sealed centered sufficient statistics, their public seal,
the prospective design and its own source. Its
[reader audit](two_sided_public_stage_001/reader_audit.json) records **zero
private inputs and zero raw-archive reads**. No policy, service, RNG or
label computation occurred. All 23 rows were retained. The
[full interval grid](two_sided_grid.md) renders them with outward-rounded
endpoints; exact fractions remain in the result.

The same fixed `lambda=8/R` is used for both sampling signs, with error
`1/80` per tail. Since `log80<5`, the conservative two-sided sampling radius is

```math
\rho=Q/R+5R/8\le9R/8.
```

The bound here is `9R/8`, rather than the preceding one-sided `R` bound.
The two-sided action radius is the exact integer
`ceil_sqrt(ceil(5(T-m)/2))`. The `V` and `F` intervals intersect their
pointwise public envelopes, with lower endpoints
`V_lo=(T-m)-V_hi` and `F_lo=T-2*sum(v)-F_hi`. Terminal errors intersect only
`[0,T-m]`. Any empty intersection would remain explicit and suppress all
ordinary better/worse certificate labels for that row. **No empty
intersection occurred** in these 23 calculations.

Under the per-episode fresh fair-bit theorem premises, the shared two-sided
sampling event and the two action tails give a joint fixed-end interval
statement for `V`, `F` and terminal errors with probability at least
`19/20`. This does not provide a simultaneous23-arm guarantee, an anytime
terminal guarantee or empirically validated confidence for deterministic
MT seeds. No lambda, radius or decision threshold was optimized using the
computed endpoints.

The prescribed endpoint rule produces the following flags:

| Decision test | Number of retained rows flagged |
|---|---:|
| Brier lower bound strictly above `T/4` | **10** |
| Conditional-action upper bound strictly below `(T-m)/2` | **0** |
| Conditional-action lower bound strictly above `(T-m)/2` | **0** |
| Empty-intersection/conflict rows | **0** |

The ten Brier flags are the exact and state16 uniform arms at horizon992
with blocks2 and4, and at horizon3,968 with blocks2,4 and8. All remaining
rows are retained without that flag, including all three adaptive arms.
Thus, under the stated formula's fair-bit premises, purchased evidence can
support a bad-forecast diagnosis in some existing episodes. This final
diagnostic does not certify conditional-action superiority or infer a
changed future purchase policy. Its displayed count is not a family-wide
95% conclusion.

All statements refer to the unchanged base forecast/update paths. If an
answer override improves outputs pointwise, a base upper bound may transfer
while the base statistics are retained. These lower-bound diagnoses do not
automatically transfer. The algebraic shared identity still holds when all
forecasts, statistics and targets are consistently recomputed, but changes
using current purchased answers can break the required block predictability
and zero-mean sampling argument. No override was applied in this diagnostic.

The final result SHA256 is
`0308b41dfee9b9f2efdbbbb37ea557cccd607bf130a554cc052304a0ff60a9cf`;
its public reader audit SHA256 is
`3fd810899abe9b9ec8d5164c63fc3222041836c4d87ec6ee94de90ca52e9e8d5`.
It sealed at22:48:41 UTC with zero private input reads. All prior stages,
designs and results remain unchanged. This is the final authorized
diagnostic from this agent; no further analysis or run was selected.
