# F15-ND01: a bounded neural extraction diagnostic

Status: prospective development protocol; written before ND01 discovery or
validation execution. Author: ChatGPT (GPT-6 Astra Pro), 2026-10-05.
User authorization: a fresh, protected **90 engaged research minutes** to
diagnose F15's ordinary-trained neural result. This is a new recurrence after
F15, with its own version and exposure record. It does not reopen or retry F15.

## 1. Question and scope amendment

**Ordinary task training gives the network no particular reason to organize
its features into one clean eight-neuron block for each expected cost.** It
rewards final predictions, while useful intermediate information may be
distributed across neurons, mixed with other inputs, or organized around a
different decomposition of the task. The probe therefore depends on whether
the learned representation is accessible to its restricted extraction method.
This is a plausible explanation to test, not an identified cause or a finding
of technical superposition in these five networks.

The original F14-v1 protocol, 34-file freeze, five F15 networks, original
alignments, final populations, and **0/5 complete identity support** remain
unchanged. F15's complete endpoint combined absolute accuracy, conditional
decisions, matched-control advantage, scale discrimination and replication.
It did not merely ask whether some subset carried useful information. ND01
separates those questions and purchases three pieces of development evidence:

1. **Complete-endpoint calibration:** does the unchanged composite endpoint
   recognize deliberately constructed cost structure under the actual search?
2. **Bounded extraction comparison:** does more search, a different proposal,
   or a criterion more closely aligned with the worst stratum recover cleaner
   interventions from the exact same ordinary-trained networks?
3. **Specified relaxation and exhaustive comparison:** does replacing the
   binary eight-coordinate mask by a fractional mask of total mass eight
   materially improve fidelity while retaining the original network and head?
   Enumerate all binary subsets on the same logit objective to distinguish a
   limitation of coordinate masks from incomplete optimization of that objective.

The recurrence changes discovery/validation seeds, extraction budgets and
methods only in this separate directory. All ND01 outputs are **development
data**, including its independent validation split. This is not an amended
confirmatory F15 result. No F16 review, retention rerun or Gate C/D assessment
is authorized or attempted here. The prior retention application and bounded
C4 synthesis/application contribution retain their original dispositions.

## 2. Fixed inputs and environment

Starting source commit: `9f42a047126618b0364cf334002f846e5839d726`.
The source is the committed F15 record now on GitHub main. Inspect existing
ND01 markers before each stage and never change output directories to evade a
failed attempt. The five source artifacts are the original
`v2/work_logs/F15_v1_run1/preparation_attempt_1/model_{0..4}_prepared.json`.
Their outer file hashes and internal artifact hashes are bound in this
recurrence's manifest. The source F14-v1 manifest SHA256 is
`b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c`.

Use **CPython 3.12.x, NumPy 2.3.5, float64 and PCG64**, with
`OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `MKL_NUM_THREADS=1`
set before Python starts. Verify the unchanged F14 freeze and these runtime
conditions before generating any ND01 population. ND01 requires no PyTorch.
The inherited Windows CRLF, native-crash and path-portability limitations
remain documented in F15; this Linux run neither edits the frozen test nor
supplies a new Windows validation result.

The new `config.json` and `freeze.json` bind the protocol, executable modules,
source dependencies and source artifacts before any discovery execution.
No seed, sample count, method, tolerance or objective is chosen from ND01
validation outcomes. Static review and numerical unit checks of generic
mathematical primitives may precede the freeze, but must not expose a model's
discovery or validation population.

## 3. Complete-endpoint calibration

Use the existing `compiled_cost_network` construction at the same 4–32–1
capacity as the ordinary-trained network. It approximates the signed log-cost
decomposition, with a construction-known eight-coordinate subset per role.
Create five positive-gauge/permutation layouts using seeds **1511601–1511605**
and layout stream 9000. They implement the same constructed function; they
are **five layouts, not five independently learned representations**.

Run the entire original discovery search: four hypotheses, five controls, two
roles and 128 candidates per search. Retain 1,024 fit examples, 128 selection
pairs per stratum and every original selection rule. Initialize the untrained
control directly with the original initializer; perform zero training steps.
Construction-known subsets never enter the candidate search or its ranking.

Evaluate using **1511691–1511695**, 8,192 pairs per stratum, the original
ordinary-task count, strata, incorrect donors, gauge checks and hypotheses.
Apply the unchanged 560-row analysis and complete endpoint literally. Label
its counts as calibration layouts, and keep its development-only support
flag false. Also report construction-known subset accuracy on hash-identical
evaluation arrays, separately from searched/control outcomes. Deterministic
array regeneration for that oracle is recorded and charged, not described as
a second independent population.

A positive oracle with a failed complete searched endpoint would reveal that
the endpoint can fail despite accessible constructed structure. A high-quality
searched alignment can still fail the complete criterion if optimized random
or permuted proposals find comparable subsets. Report the exact blocking
conditions; do not summarize that situation as inability to represent costs.

## 4. Bounded search on unchanged ordinary-trained networks

Use the five original trained parameter arrays without any gradient update.
Discovery seeds are **1510601–1510605** and validation seeds are
**1510691–1510695**. Fit inputs use stream 10; discovery pairs use
100 + 10 times role; validation pairs use 200 + 10 times role; ordinary
validation inputs use stream 300. Fit size is 1,024, selection size is 128
pairs per stratum and validation size is 8,192 pairs per stratum. All methods
for a model use the same pairs. Keep exactly eight selected coordinates.

Compare five proposal families in a fixed order:

| Family | Coordinate proposal weights before the frozen 25% uniform mixture |
|---|---|
| `cost_corr` | Absolute Pearson correlation of hidden activation with the expected cost, as in F15. |
| `uniform` | Uniform, with the same search and validation budget. |
| `permuted_cost_corr` | Correlation with a fixed permuted cost target, as in the original matched control. |
| `log_cost_corr` | Absolute Pearson correlation with the role's signed log-cost. |
| `positive_contribution_cov` | Positive part of covariance between the native output-weighted hidden contribution and signed log-cost, divided by target variance. |

The last two families are separate because absolute Pearson correlation with
`v_j*h_j` cancels nonzero `v_j` magnitude and sign. Calling that operation
output-weighted would not identify a distinct mechanism. Positive covariance
instead considers native contribution size and sign; cancellation between
negative and positive basis functions remains a reason it might perform
poorly. An all-zero proposal falls back to uniform.

For each family and role create a **single 1,024-candidate pool**. Its first
128 candidates define the smaller budget. Evaluate both selection rules on
these same nested pools; do not run extra random pools until a winner appears.
Candidate stream 50 + role and target-permutation stream 61 are fixed.

- `frozen_mse`: original mean probability MSE, then effect MSE, then decoder
  normalized MSE, with the original 1e-12 tie tolerance.
- `robust`: minimize the maximum of the five stratum MAEs divided by .05,
  near-decision disagreement divided by .35 and far-decision disagreement
  divided by .10; then mean probability MSE and equal-target effect RMS.

Keep all candidate subsets, decoder-fit scores and counts, and per-stratum
scores; retain decoder coefficients for every selected alignment. The product
is **20 selected variants per model** (five proposals, two budget prefixes,
two selectors), each with two role subsets. Reuse actual candidate forward
calculations across prefixes/selectors and report actual unique work separately
from the logical cost of running each method independently.

Validation reports every variant, the original frozen subset, no swap, and
whole-layer swap. Report matched proposal comparisons, budget differences and
selector differences using paired means and moments on identical arrays.
This comparison asks whether extraction improves; it does not apply the
original 560-row confidence family to the expanded method family or select a
replacement confirmatory hypothesis after seeing validation.

## 5. Fractional masks and exhaustive binary comparison

Use exactly the same discovery and validation arrays as the bounded-search
comparison. The original hidden activations and affine head are fixed. For
each role fit a mask `m` with `0 <= m_j <= 1` and `sum(m)=8`, acting as

```math
h'=h_b+m\odot(h_d-h_b),\qquad
z'=z_b+\sum_j v_jm_j(h_{dj}-h_{bj}).
```

This family includes every binary size-eight mask. It may act fractionally
on more than eight neurons; equal total mass is not equal coordinate count.
Fit equal-stratum **logit MSE**, including the original base prediction error
in the target, using deterministic projected gradient descent from the uniform
mask. Fix 10,000 maximum iterations, Lipschitz step from the quadratic Hessian,
80 bisection iterations for capped-simplex projection, and first-order
duality-gap stopping tolerance **1e-8**. Save masks, numerical feasibility,
iteration checkpoints, objective and gap. There is no convergence-based
increase of the budget. A run at the cap is an interpretable bounded result.

For a feasible mask and gradient `g`, the linear minimizer puts ones on the
eight smallest entries of `g`. The first-order gap bounds the finite
discovery convex optimum between `f(m)-gap` and `f(m)`; the lower bound also
applies to binary masks on that same logit objective. These are floating-point
numerical bounds, not rigorous interval certificates, population bounds or
probability-MAE impossibility results.

The before-freeze implementation review identified a feasible stronger
comparison: there are exactly **10,518,300** subsets of size eight among 32
coordinates. A single-thread C++ helper enumerates all of them for each role
on the **same discovery logit-MSE quadratic**. Its source, executable, compiler
command and build record are included in this diagnostic freeze. Use float64
without fast-math or floating-point contraction; retain the subset with the
smallest computed quadratic, resolving exact ties by lexicographic order.
Record the enumerated count, objective, subset, native CPU/wall cost and direct
NumPy residual recomputation. This is exhaustive optimization of a finite
floating-point objective; it is not an exact-real or interval-arithmetic proof.
No model data were used to decide to add this comparison. A synthetic-only
feasibility benchmark and generic small-width enumeration checks precede the
freeze. The ten role-specific binary results are saved inside the five soft-mask preparation
units, so the global **15-unit** exposure gate remains unchanged.

Validate four prespecified methods: the fractional mask, its top-eight
rounded mask (stable coordinate-index ties), the exhaustive binary mask, and
the original frozen subset.
Report both logit and probability errors, decisions, equal-target leakage and
mask concentration. The exhaustive comparison separates binary restriction
from search on their common logit objective. Comparisons with the original
probability-MSE selector still involve a changed objective, and finite
discovery optima need not preserve their ordering on validation probability
MAE or near-boundary decisions.
This is neither distributed alignment search nor proof of technical
superposition or unique native utility representation.

## 6. Durability, attempts and exposure

Default run directory: `v2/work_logs/F15_ND01_v1_run1`.
Prepare **all 15 units**—five calibration layouts, five ordinary-network
search records and five ordinary-network soft-mask records—before any
validation population of any arm is generated. Save each complete JSON
artifact exclusively, flush/fsync it, write its SHA256 sidecar, reload it and
run its validator. Validate all 15 again and save the global preparation
manifest before creating the first evaluation exposure marker. Validation
must check source identity as well as new artifact hashes and configurations.

Stages have at most two attempts: the initial attempt and **one unchanged
retry for an unexplained failure**, with a recorded reason. Preserve every
attempt marker, partial file, failure and completed unit. Reuse completed
validated units on a retry. A missing or corrupt artifact is not permission
to overwrite it. An explained deterministic defect requires a named amendment
and disposition of exposed data before any corrected stage; it never
authorizes silently replacing this freeze. Report command exit codes, stdout,
stderr, CPU/wall costs and completion/exposure chronology even on failure.

## 7. Analysis, claims and stopping

Report the unchanged F15 outcome beside these development results. Calibrated
absolute adequacy, advantage over optimized proposals and scale specificity
are distinct conclusions. For ND01 search/masks, report all five model/ten
role rows and each stratum; use paired descriptive differences. Threshold
crossings are point diagnostics unless explicitly part of the unchanged
calibration assessment. No new familywise significance or population
replication claim is made for the expanded analysis.

Use the exact identity

```math
z_{\rm swap}-z_H=e(b)+r_S(d)-r_S(b),
```

where `e=z-z*` and `r_S=sum_{j in S}v_jh_j-ell_role`, to distinguish ordinary
prediction error from failure to isolate a contribution. Existing F15
baseline error, equal-target leakage, strong-control performance and selection
generalization are diagnostic evidence, not proof of a single cause. See
`representation_notes.md` for the derivation and checked primary antecedents.

Preserve the central **D10/L10/E70/O10=100 engaged minutes**, high
D15/L15/E90/O15=135, R/X 60/40 and separate wait forecasts in the session
forecast. Protect **90 D+L+E minutes** without adding overlapping agent time.
The original forecast's optional readout analysis has been made concrete,
before outcomes, as the specified fractional-mask comparison above; a feasible
exhaustive binary comparison was added before freezing to strengthen its
interpretation. These choices do not raise the protected floor. If core
results arrive early, use the remainder for the registered derivation,
mechanistic residual analysis, optimizer audit and primary-source comparison.
Stop optional expansion at the chunk boundary and identify a concrete next
60/90-minute experiment with what additional evidence it could buy.

ND01 is a bounded application and diagnosis using established tools. Better
extraction is not by itself a new general interpretability method; a null
result is not automatically a novel finding. Task completion and scientific
or contribution support have separate dispositions. Keep F16 and Gates C/D
unattempted and reconcile README, TODO, claim records, report and the append-only
time ledger at close. POST-B-1 enters at **701.64299296445** engaged minutes,
with **258.35700703555** remaining to the sixteen-hour checkpoint.
