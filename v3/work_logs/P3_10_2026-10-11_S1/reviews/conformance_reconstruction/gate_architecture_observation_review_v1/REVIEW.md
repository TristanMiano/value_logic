# Gate architecture observation: independent exact reconciliation

**Signed:** ChatGPT (GPT-6 Astra Pro), `/root/conformance_reconstruction`, 2026-10-11. **P3-10 post-outcome interpretation; zero principal clock credit.**

## Finding

**PASS.** Independent exact arithmetic reproduces every reported group, block, parent, population and configuration field in the principal gate-architecture result. All **42** scheduled suffix scores reconcile exactly to their sealed base/issued Brier sums and means. The common hindsight terms are

```math
I=\frac{197}{1536}=0.128255208333\ldots,\qquad
M=\frac{11}{512}=0.021484375,\qquad
I+M=\frac{115}{768}=0.149739583333\ldots.
```

These are means using the complete 64-position suffix denominator and the frozen seed-then-population hierarchy. They are the fitted optimum for the declared relaxed, block-specific, monotone two-signature forecast class. The prior mathematical review's GA-01 is now closed by both the source clarification and independent checks that all suffix keys are new relative to the prefix and earlier suffix positions.

The independent completed result is [run_02/results.json](sandbox:/workspace/scratch/095cdac579b7/value_logic/v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/run_02/results.json), SHA-256 **`5a2c23429ed21036335aa6fe44e451679dcadc43c12665ddd6f3b7f00f3a1ce8`**. The reconstruction code is [check_saved_gate_v2.py](sandbox:/workspace/scratch/095cdac579b7/value_logic/v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/check_saved_gate_v2.py).

## Complete scope and binding

| Reconciled object | Complete denominator |
|---|---:|
| Gate numerical parents | 42: 7 configurations × 2 populations × 3 prescribed seeds |
| Suffix positions per parent | 64, all closed |
| Forecast/truth pairs checked | 2,688 |
| Per-parent block instances | 672 |
| Present-or-absent group instances | 1,344 |
| Sealed suffix-score records | 42 |
| Hierarchical configuration aggregates | 7 |
| Distinct public populations | 2 |
| Distinct population/block pairs | 32 |
| Distinct suffix label positions | 128 |

All records remain included. Duplicate policy/seed paths do not turn the 128 label positions or 32 population blocks into independent new populations. The checker records 37,410 individual assertions; those are implementation checks, not additional scientific samples.

The checker imports only Python's standard library. It does not import or execute the principal observer, its lineage reader, a frozen method, a generator, a truth function, a scorer or an analyzer. It reads the pinned previously reconstructed numeric truth transcript and independently recomputes the new statistics. Thus it is independent of the new decomposition implementation; it is not a second truth-oracle reconstruction.

The result binds 182 read files by SHA-256. The two original input tapes are read through their pinned input-reference rows and seals. Every public full semantic key and query ID is checked against its original tape position. The 42 public results retain their original prospective unchanged-public-record identity in the pinned composite index. Each amended score is checked through the evaluation completion index and seal, with its exact public/input result links and scheduled unit identity. The original failed lineage and unknown failed prefix cost remain unchanged.

## Exact population structure

| Population | Positions | Blocks | Present groups | Mixed groups | Pure present groups | Absent groups | Order-violating blocks | I | M | I+M |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| p00 | 64 | 16 | 31 | 12 | 19 | 1 | 2 | 11/96 | 5/256 | 103/768 |
| p01 | 64 | 16 | 29 | 14 | 15 | 3 | 6 | 109/768 | 3/128 | 127/768 |
| Complete structural census | 128 | 32 | 60 | 26 | 34 | 4 | 8 | — | — | — |

Both populations contain 31 true suffix labels. Pure groups and all four absent groups are retained. The fitted-group frequencies are descriptive properties of the saved tapes, not estimated conditional probabilities asserted for another population.

The two sources of irreducible error within this class are distinct. For example, population p00 block 27 has group counts `(2 positions, 2 true)` and `(2 positions, 0 true)`. Both groups are pure, so I = 0, but their empirical means reverse the required order. The pooled minimum gives M = 1 for that four-position block. Thus monotonicity can impose a positive penalty even when neither group has mixed labels.

## Actual loss and excess over the relaxed optimum

Every row below retains all six population/seed parents. Equal values are preserved rather than selected away.

| Configuration | Actual Brier mean | Excess E |
|---|---:|---:|
| finite_tickets_cold | 0.264741636337 | 0.115002053004 |
| finite_uniform_cold | 0.356012487407 | 0.206272904074 |
| ordinary_kernel_mirror | 0.356012487407 | 0.206272904074 |
| value_tickets_cached_hashed | 0.264741636337 | 0.115002053004 |
| value_tickets_cold | 0.264741636337 | 0.115002053004 |
| value_uniform_cached_hashed | 0.356012487407 | 0.206272904074 |
| value_uniform_cold | 0.356012487407 | 0.206272904074 |

Uniform-family actual loss is exactly **195719934769/549755813888**, with excess **340199184787/1649267441664**. Ticket-family actual loss is **27289360079/103079215104**, with excess **3951440453/34359738368**. In every case actual loss equals I+M+E exactly, without rounding tolerance.

## The projection cross term is material

The checker reconstructs each residual using the binary raw-sum identity `k − k²/n`. When order is violated, it computes the fitted loss as the single pooled raw-sum minimum, then obtains M by subtraction. This differs from the principal's centered-group formula and direct closed-form penalty. It additionally checks the exact projection identity from the mathematical review:

```math
E=n_0(p_0-q)^2+n_1(p_1-q)^2
 +\frac{2n_0n_1}{n_0+n_1}(\mu_0-\mu_1)(p_1-p_0)
```

in the pooling case. Here q is the pooled empirical mean. All 168 method/seed copies of the eight distinct order-violating blocks have a positive cross term. The hierarchy gives:

| Forecast family | Squared-distance part | Cross term | Their sum E |
|---|---:|---:|---:|
| Uniform | 0.201340838269 | 0.004932065805 | 0.206272904074 |
| Tickets | 0.104206181587 | 0.010795871417 | 0.115002053004 |

The exact cross terms are **248239/50331648** and **271687/25165824**, respectively. Replacing E by only squared distance to the fitted pair would therefore misstate these saved outcomes. This confirms the derivation's existing warning; it is not a new policy comparison.

## Preserved reviewer failure and narrow correction

The independent checker had **one reviewer-only failed attempt**, preserved with its source, start record and full traceback in [run_01/failure.json](sandbox:/workspace/scratch/095cdac579b7/value_logic/v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/run_01/failure.json). It incorrectly compared `forecast_readouts` to the numeric horizon. The sealed field is a diagnostic dictionary, as the frozen broker scoring source specifies. The first parent's 64 rows, 16 blocks, full-key bindings, decomposition and Brier totals had matched before that unrelated schema assertion stopped the run.

V1 and its failure were left unchanged. V2 removes only that erroneous comparison and uses the new exclusive `run_02` path. The 64-position horizon/closed-round checks, complete arithmetic and exact sealed Brier comparisons remain. [revision_v2.json](sandbox:/workspace/scratch/095cdac579b7/value_logic/v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/revision_v2.json) preserves the exact two-line change and both source hashes. V2 ran once and passed at **2026-10-11 16:15:18.378870 UTC**. No principal or official artifact was changed or rerun.

## Interpretation limits

This result confirms a retrospective lower bound for a specified relaxation of the observed forecast architecture. Group constancy, nonnegative positive-mass weights, common dyadic projection, ordering, key newness, absence of prior hard overrides and equality of base/issued forecasts are checked on all included records. The relaxed fitted class has access to the labels and may choose arbitrary real forecasts independently in each block.

Its fitted optimum is not a deployed ordinary comparator, an online-achievable guarantee, or a lower bound for arbitrary reasoning on the public CNFs. E does not identify a causal effect of the selector, the update rule, quantization or delayed information, nor estimate safely avoidable online error. These Brier statements concern pre-purchase base/issued forecasts; they do not impose the same bound on terminal actions after purchased labels can change an action. No fixed mathematical truth is treated as an iid random event.

All new calculations are post-outcome unbilled observer work. No endpoint, accepted duty status, economic gate, author gate or P3-11 judgment is changed. Principal agent credit remains zero.

## SHA-256 roots

| Item | SHA-256 |
|---|---|
| Principal decomposition result | `553c91374ac015cd65f83325301e79f341d2198efe24adc0e318951bd1543fc1` |
| Principal observer source | `5224c7a3993863e55d01d1d9845660566c3637a852da6415e9932251d07db9b6` |
| Clarified derivation | `4824a27987bf36369d01d08d11bbeefbe387bc48a59df28f699a6d0c762d9bc2` |
| Independent numeric truth transcript | `8f7e34aef5060b43bccb2447f87238c3b3c864c5a2e375d317472827567da82f` |
| Independent checker v1 | `a598fae63f67e31283ff91414e41da59204ec59f07bee812af3529b3d859bdaf` |
| Preserved v1 reviewer failure | `637945e913823af17cac3df61e03101cf4c6e7d46edbeb92cd0c08708c558dcd` |
| Independent checker v2 | `63438b39e021ee3c21dd51e0f0d3fa6cf7d0ba05c04f82a8c06da604ecbdd0ca` |
| Independent v2 result | `5a2c23429ed21036335aa6fe44e451679dcadc43c12665ddd6f3b7f00f3a1ce8` |

`manifest.json` binds this review and every preserved artifact in this review directory, including both attempts and the reviewed principal source snapshots.
