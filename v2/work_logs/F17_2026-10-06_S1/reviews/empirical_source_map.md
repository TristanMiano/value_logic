# F17 empirical source map and report-ready material

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated empirical reviewer,
October 6, 2026. Same-model internal review, not external peer review.
Concurrent reviewer time credited to the principal: **zero**.

Assignment: assemble an accurate source map for `paper_v2.md` from existing
F13, F15, F15-ND01 and Gate C evidence. No experiment, training, alignment,
test suite, population generator, or fixed-path audit writer was run. The
only machine operations were source reads and standard-library inspection
of existing JSON. Original scientific files, tests, freezes and ledger were
not edited. Gate C approval is supplied by the author's current instruction;
dated source reports retain their historical gate states.

## 1. Sources and status distinctions

Paths in this table are relative to the repository root. The companion
`empirical_source_map.json` binds the main inspected sources by byte hash
and extracts selected reported aggregates without generating scientific data.

| Paper material | Authoritative source | Exact scope |
|---|---|---|
| Frozen original protocol, populations, thresholds and controls | `v2/experiments/protocol.md`, `config.v1.json`, `freeze.v1.json` | F14-v1 prospective definition, unchanged during F15/F17 |
| Original F15 complete report | `v2/experiments/results.md` | Original confirmatory outcomes, resources, all failures, recovery and claim dispositions |
| Original F15 machine summaries | `v2/experiments/F15_v1_analysis/summary.json`, `retention_by_method.json`, `neural_models.json`, `neural_interval_rows.json` | Summaries of preserved units, not additional samples |
| Original units and preparation/exposure markers | `v2/work_logs/F15_v1_run1/` | Five original model preparations, 160 retention units, five neural evaluations, assessments and stage records |
| Current saved-row recount | `v2/work_logs/C_2026-10-06_S1/saved_results_attempt1/summary.json` and its `reader.py` | Read-only confirmation of counts, useful criteria, preparation chronology and saved control comparisons; no independent new solver execution |
| ND01 report and protocol | `v2/experiments/F15_ND01_results.md`, `neural_diagnostic_v1/protocol.md`, `config.json`, `freeze.json` | Separately frozen development diagnosis on the same five ordinary networks; no F15 retry |
| ND01 aggregate and all variant rows | `v2/experiments/F15_ND01_analysis/core_summary.json`, `calibration_rows.csv`, `mask_rows.csv`, `search_rows.csv` | All registered diagnostic arms retained, including unfavorable selectors and controls |
| ND01 mechanism and semantic limits | `v2/experiments/F15_ND01_analysis/mechanism_derivation.md`, `mechanism_results.json`, `selection_diagnostics.md`, `intervention_algebra.md`, `joint_feasibility.md`, `joint_semantic_error.md` | Explicitly labeled supplementary/post-outcome algebra and saved-data diagnosis |
| Scientific and actual self-assessment derivations | `v2/derivations/06_case_studies.md`, especially §§2.4–2.5, 2.9, 4.1–4.3 | Complete assumptions and native compositional steps; stronger ordinary controls |
| F13 original validation | `v2/verification/F13_results.md` | Forty distinct focused tests passed in separate original runs; combined original attempts failed |
| Current technical regression | `v2/work_logs/C_2026-10-06_S1/reviews/technical/regression_attempt1/result.json` and `stderr.txt` | A later Linux first-attempt 288-test pass, including both F13 modules together; not a whole-repository pass |

Avoid presenting F13's historical unsupported novelty assessment, F15's
historical unattempted Gates C/D, or ND01's historical F16 recommendation as
the current project state. The empirical outcomes remain valid while their
dated workflow pointers are historical. The author has now approved Gate C;
F17 assembles existing research and does not execute Gate D.

## 2. Revision/retention: recommended main table

The experiment uses an exact correlated law on eight Boolean worlds and
the six full orders of three reset procedures. It comprises **16 initial
population seeds × ten revisions = 160 episodes**. Each episode is assessed
by six methods under two source-access regimes: **1,920 method rows and
11,520 scalar queries**. Revisions sharing a seed are dependent. These are
descriptive counts under a stipulated generator, not independent replications
or a generalization estimate to unknown workloads.

Each table row below contains 160 decision rows and 960 scalar queries.
Numeric columns are exact / approximate / refused; decision columns are
certified order / certified fallback / refusal followed by fallback.

| Source access | Method | Numeric counts | Decision counts | Received native comparisons | Useful method rows |
|---|---|---:|---:|---:|---:|
| No reacquisition | fresh | 768 / 0 / 192 | 98 / 30 / 32 | 98 | 68 |
| No reacquisition | cached proof | 768 / 0 / 192 | 98 / 30 / 32 | 98 | 68 |
| No reacquisition | full joint | 768 / 0 / 192 | 98 / 30 / 32 | 98 | 68 |
| No reacquisition | tailored | 416 / 172 / 372 | 85 / 29 / 46 | 88 | 53 |
| No reacquisition | ordinary exact intervals | 416 / 172 / 372 | 85 / 29 / 46 | 88 | 53 |
| No reacquisition | marginal diagnostic | 0 / 0 / 960 | 0 / 16 / 144 | 0 | 0 |
| Adaptive reacquisition | fresh | 960 / 0 / 0 | 126 / 34 / 0 | 126 | 68 |
| Adaptive reacquisition | cached proof | 960 / 0 / 0 | 126 / 34 / 0 | 126 | 68 |
| Adaptive reacquisition | full joint | 960 / 0 / 0 | 126 / 34 / 0 | 126 | 68 |
| Adaptive reacquisition | tailored | 824 / 136 / 0 | 126 / 34 / 0 | 126 | 68 |
| Adaptive reacquisition | ordinary exact intervals | 824 / 136 / 0 | 126 / 34 / 0 | 126 | 68 |
| Adaptive reacquisition | marginal diagnostic | 960 / 0 / 0 | 126 / 34 / 0 | 126 | 68 |

Totals: **8,624 exact, 616 approximate, 2,280 refused** scalar answers;
**1,220 certified orders, 368 certified fallbacks, 332 refusals**;
**1,226 received comparisons and 694 insufficient-current-request results**.
No final case was classified as proof-budget unavailable. The budget-refusal
sentinels remain development evidence. Of the 1,226 receipts, 1,218 concern
certified selected orders and eight are diagnostic. Two certified
epsilon-regret orders lack the separate zero-budget fallback receipt.

The rank-7 full-law methods (`fresh`, `cached_proof`, `full_joint`) carry
the same information. `tailored` and `exact_intervals` carry equivalent
rank-5 old-mean information. Rank-3 marginals are a weaker-information
diagnostic, not an equal-information competitor. All **960** nonredundant
equal-information comparison records agree on the stipulated numerical,
decision, native and acquisition outputs. Strong ordinary fiber optimization
therefore reproduces the service. Useful integration is supported; exclusive
inference power is not.

### Prospective usefulness and actual denominators

A useful row concerns an actual executed nonfallback action after a direct
price or program edit. Its current native proof establishes a margin of at
least `1/20` against fallback, uses at least two distinct nonzero source
premises, and its coherent same-law regret is at most `1/20`. The frozen
criterion required at least four distinct episodes over two seeds, covering
price and program edits, including one uncertain selective no-reacquisition
case with an approximate selected cost.

| Result | Count and denominator |
|---|---:|
| Useful distinct episodes | 68 of 160 total episodes |
| Initial seeds represented by useful episodes | 16 of 16 |
| Small positive price edit | 14 of 16 episodes in that variant |
| Small negative price edit | 14 of 16 |
| Large positive price edit | 9 of 16 |
| Large negative price edit | 16 of 16 |
| Program edit | 15 of 16 |
| Qualifying uncertain, approximate-selected-cost, selective no-reacquisition rows | 30 method rows |
| Distinct episodes represented by those 30 paired-method rows | 15, over eight seeds |
| All useful method rows, including repeated methods/access regimes | 718 of 1,920; not 718 independent successes |

Every admitted numerical answer and certified decision met its registered
tolerance on the actual scoring profile. All **276 realized regrets above
`1/20`** occurred after decision refusal; maximum regret was `7/5`. Those
fallback losses remain part of the complete outcome. Refusal is a distinct
operational result, not credited as useful action.

### Two especially clear saved examples

These are post-exposure illustrations selected by the saved analysis rules,
not new hypotheses or extra confirmatory cases.

1. **Approximate number, useful action, current proof.** Seed 15104,
   `small_price`, tailored/no-reacquisition selects order `(1,2,0)`. Selected
   cost interval is `[13557/6640,34059/16600]`; midpoint is
   `135903/66400`, with actual error `17/66400`. Both coherent and realized
   regret are zero. The received fallback bound is `-7441/16600`, using eight
   source premises and no source query. The ordinary exact-interval method
   returns the same result.
2. **Useful action despite refusal of every precise number.** Seed 15105,
   `program_edit`, tailored/no-reacquisition chooses `(2,1)` with coherent
   regret zero. All six numeric intervals are too wide for the `1/20`
   midpoint-error tolerance. The selected interval is `[370/231,184/77]`,
   but the received fallback bound is `-17/154`. Five tailored
   no-reacquisition program rows have this conjunction. This separates
   information for scalar accuracy from information for choosing well.

### Resource findings worth retaining in the paper

The resource vector includes retained state, context/proof state, source
queries, source work, arithmetic, production and reception. It is not reduced
to a single favorable runtime or payload number.

| Resource finding | Observed value | Interpretation |
|---|---:|---|
| F15 preparation external wall / child CPU | 7.628116 / 7.621769 seconds | Both networks, all five model artifacts and alignments; first attempt |
| F15 evaluation external wall / child CPU | 184.274726 / 184.249148 seconds | Includes retention and neural work; first attempt |
| F15 evaluation peak child RSS | 248,364 KiB | Actual process measure, unlike serialized payload tables |
| Fresh no-reacquisition arithmetic / native-inclusive update | 1.005003 / 72.134739 mean ms per episode | Receipt-required service costs substantially more than arithmetic alone |
| Tailored no-reacquisition arithmetic / native-inclusive update | 5.984763 / 81.452699 mean ms per episode | Uncertainty solving and checking do not show a speed win |
| Tailored / ordinary-interval retained bytes | 125 / 143 median bytes | An 18-byte encoding saving at equal information rank, not total-memory superiority |
| Tailored / fresh total serialized stored upper bytes, no reacquisition | 21,503 / 20,527 median bytes | Larger contexts/proofs can outweigh small payload savings |
| Adaptive repairs across 960 adaptive rows | 412: 60 two-mean and 352 eight-field repairs | The remaining 548 adaptive rows needed no repair |
| Cached proof vs fresh, matched admitted-service no-reacquisition cases | Slower in all 98, mean complete-case difference +81.113254 ms | No cache-speed advantage for this implemented protocol |

Exact mean queries are stipulated source operations: two new means entail
16 world/order paths. Eight returned fields are a wire convention for a
normalized law of information rank seven, not an eight-dimensional lower
bound. All methods initially saw the same eight fields. Adaptive acquisition
is quality-first, triggered by numeric or decision refusal; it was not
optimized for a measurement price. At fee `1/2` per returned scalar field,
all adaptive method families have greater mean source-fee-plus-action costs
than their no-reacquisition counterparts. At fee `1/20`, full information
slightly improves that mean while selective acquisition worsens it.

The `I+hU` and source-fee results for horizons 1, 4, 16 and 64 are algebraic
projections of one recorded update, not repeated-update experiments. Native
subtimers are nested and must not be summed again. Means including refusals
are resource descriptions, not equal-service speed comparisons.

## 3. Original neural result: recommended table and wording

The fixed task has inputs `(x1,x2,cFN,cFP)`, with `x1,x2` in `[-1,1]` and
prices in `[1/2,2]`. The outcome probability is
`eta=1/2+(x1+x2)/8`. A 32-ReLU MLP is trained by ordinary weighted binary
cross-entropy. Its optimal prediction is

```math
p^*=\frac{J_0}{J_0+J_1},\qquad
J_0=c_{FN}\eta,\quad J_1=c_{FP}(1-\eta).
```

Each network has 193 parameters and receives 768,000 binary outcome labels
over 3,000 steps. Across five trained networks this is 3,840,000 binary
labels and **zero expected-cost training labels**. Counterfactual
expected-cost targets are used later for intervention discovery; absence
of those targets from original training must not be misread as absence
from alignment discovery.

Discovery searches 128 candidate eight-coordinate subsets per role,
hypothesis/control and model. Four fixed high-level scales, five arms,
two roles and five models give 25,600 candidate evaluations/decoder fits.
Five complete hashed preparation artifacts precede every final retention
or neural evaluation population. Evaluation contains 409,600 intended pairs,
409,600 independently generated incorrect-donor records, 40,960 ordinary
task examples and 8,192,000 alignment/role/pair evaluations. No alignment
was refitted on final data.

| Frozen endpoint | Observed result | Interpretation |
|---|---:|---|
| Ordinary task readiness | 5/5 models | Registered mean probability-error and decision-regret criteria met |
| Conditional ordinary base accuracy | 50/50 cells supported | No model classified as underlearned under the frozen readiness thresholds |
| Complete identity intervention support | 0/5 models, versus required at least 4/5 | Specified conjunction unsuccessful |
| Identity intervention MAE cells | 2 supported / 48 inconclusive / 0 violated | Wide intervals prevent most accuracy support; none rejects the .05 MAE tolerance |
| Identity near-decision cells | 3 supported / 6 inconclusive / 1 violated | One specific adverse result beyond lack of MAE power |
| Identity far-decision cells | 10/10 supported | Conditional on the prescribed far-margin pairs |
| Identity .01 advantage over matched random search | 0 supported / 9 inconclusive / 1 violated | No demonstrated extraction advantage over this capable ordinary search |
| Identity .01 advantage over permuted-concept search | 1/10 supported | Control still selects with actual intervention targets |
| Identity .01 advantage over incorrect donors / untrained networks | 10/10 each supported | Weaker adverse controls distinguished, without complete support |
| Complete support for each of the three rival scales | 0/5 | No rival was selected as a replacement hypothesis after evaluation |

The four hypotheses retain all original rows. Their complete support is
zero in each case; hypothesis-wise MAE supported/inconclusive/violated counts
are identity `2/48/0`, inverse-eta `0/46/4`, inverse-one-minus-eta
`0/39/11`, and inverse-total-cost (normalized probabilities) `9/41/0`.
These are correlated claims, not independent votes or evidence of a unique
absolute utility scale.

The original simultaneous family contains **560 intervals**, with familywise
alpha `.05`. The Hoeffding radius for an 8,192-row `[0,1]` mean is
`.024726057999695232`; an observed MAE must be at most
`.025273942000304768` to establish a `.05` upper tolerance. A failure to meet
that upper-bound test does not imply a lower-bound violation. Nevertheless,
the actual near-decision violation and failed material-advantage comparison
mean that the result is not solely an interval-width problem.

**Recommended salient interpretation:**

> Ordinary prediction training gives the network no task-specific reason to
> organize each expected cost into one clean eight-neuron block. The loss
> rewards the final prediction while leaving its internal decomposition
> underdetermined. The probe therefore tests accessibility to a particular
> extraction method as well as task competence. Shared or distributed
> features, or another decomposition of the same function, are plausible
> explanations; technical superposition has not been demonstrated here.

The elementary task identity makes this explanation concrete:

```math
\mathrm{logit}(p^*)=
\log c_{FN}-\log c_{FP}+\log\eta-\log(1-\eta).
```

A price-plus-probability-odds computation need not use two separately
swappable blocks for `log J0` and `-log J1`. This is an available alternative
decomposition, not a claim that the five networks were shown to implement it.
Decodability is not causal use; useful individual edits are not a unique or
jointly composable utility representation.

## 4. ND01: helpful diagnostic evidence without a revised F15 success

ND01 is a separately frozen **development** diagnostic. It reused the same
five ordinary networks without any new training steps or labels. It added
a known-structure calibration, wider coordinate search, and a matched
exhaustive-binary/fractional-mask comparison. All 15 diagnostic preparations
were saved and checked before new validation; both stages succeeded on their
first attempts. Its five calibration layouts are rescalings/permutations of
one constructed function, not five independent ordinary training replications.

### Calibration identifies a demanding endpoint

| Constructed-layout criterion | Result |
|---|---:|
| Complete identity endpoint | 0/5 layouts |
| Searched identity adequacy | 5/5 layouts |
| Searched identity MAE upper-bound cells | 50/50 supported |
| Near/far decision upper-bound cells | 20/20 supported |
| Same-subset scale comparisons | 30/30 supported |
| .01 advantage over random / permuted-concept controls | 9/10 / 3/10 roles supported |

Known and recovered cost structure can therefore coexist with zero complete
outcomes. The endpoint additionally demands superiority over controls that
also optimize the true counterfactual target. At the saved paired radius,
even an aligned zero-error method could not beat some controls by the required
confidence margin: every constructed layout has such a blocker. Collapsing
intervals to point means gives only 1/5 complete layouts, so more samples
alone cannot be assumed to resolve the issue. This diagnoses endpoint
selectivity without attributing every ordinary-network failure to it.

### Search and intervention family affect development accuracy

All methods in this table use common new validation pairs. Means weight five
strata equally, then two roles and five fixed models equally. Point adequacy
requires all five role-level MAEs at most `.05`, near disagreement at most
`.35`, and far disagreement at most `.10`. It omits confidence bounds and
the full control/scale conjunction.

| Intervention | Mean MAE | Near disagreement | Far disagreement | Point-adequate roles | Models with both roles point-adequate |
|---|---:|---:|---:|---:|---:|
| Original F15 subsets, on ND01 validation | .039626 | .354932 | .001062 | 3/10 | 0/5 |
| Exhaustive binary size-eight masks | .028251 | .291992 | .000085 | 9/10 | 4/5 |
| Rounded top eight from fractional masks | .029993 | .308508 | .000134 | 9/10 | 4/5 |
| Fractional masks, total mass eight | .025032 | .257288 | 0 | 10/10 | 5/5 |

All ten fractional role means improve over each other method. Exhaustive
search examines all **10,518,300** binary size-eight masks per role, or
105,183,000 total, under the fixed finite binary64 logit-MSE objective.
It does not establish an exact-real, probability-MAE, or population optimum.
Fractional masks share that discovery objective and native head weights;
all ten feasible fractional objectives beat the exhaustive binary minimum.
Seven optimizers meet the declared first-order gap; three reach the fixed
iteration cap, with largest remaining gap `6.577368e-8`. These statuses
remain visible; no extra iteration rescue was performed.

The broader search arm reports all 20 variants. Raising budget from 128 to
1,024 improves aggregate validation MAE for all five proposal families under
the original MSE selector; no role mean worsens in those nested comparisons.
All 100 distinct saved pool prefixes miss the exhaustive optimum under the
matched logit objective. The proposed robust/worst-stratum selector is a
negative result: aggregate validation MAE is worse in all ten family/budget
comparisons. Thus neither a new selector nor more complicated extraction
should be presented as an automatic improvement.

### Remaining semantic question

Single-role improvements leave joint meaning unresolved. Actual fractional
edits have nonzero observed order difference in **all five models**; repeat
application also changes the output further. Secondary compatible-projector
constructions can reproduce the existing fractional individual effects in
four of five models, but their joint high-level accuracy was not validated.
That calculation depends on the declared Euclidean metric and inactive
directions. It is algebraic output equivalence, not learned representation
identification. A saved counterexample shows that even compatible operations
with small individual probability errors need not meet the same joint error
tolerance.

The prospective follow-up **F15-ND02 Research90** can be listed under optional
future neural work: fix a common geometry, train/choose two role interventions
on discovery, then test two-donor joint and repeated interventions with
calibration and matched controls under its own freeze. It remains optional,
deferred and unstarted. The report does not promise rescue of F15's endpoint.

## 5. Report-ready worked examples with ordinary controls

### Scientific replacement from separate premises

In F13's degree-six family, Simpson's rule `S` uses three samples and the
exact-on-family rule `Q` uses four, with its additional node at `1/12`.
Let `E_Q=J+sum Q_j(r_j+e_j)` and
`E_S=J+d+sum S_j(r_j+e_j)`, where `J` is a shared unbounded target error,
`d=u/4-v`, `|d|<=1/64`, `|r_j|<=1/100` and `|e_j|<=1/200`.
The source supplies those separate facts, not a final relative-loss score.
Subtracting errors cancels `J`; signed source scaling/addition and the
maximum-common rule establish a bound on `|E_S|-|E_Q|`. With sample price
`c=1/32` and `sum|S_j-Q_j|=28633/46200`,

```math
L_S-L_Q\leq
\frac1{64}+\frac3{200}\frac{28633}{46200}-\frac1{32}
=-\frac{4873}{770000}<0.
```

This licenses the cheaper three-sample deployment relative to Q under the
admitted source. It does not establish absolute accuracy while J is
unbounded. Withdrawing the joint strip invalidates that replacement
conclusion. Ordinary support-function arithmetic obtains the same bound;
ordinary interpolation supplies Q, and general four-point Gaussian
quadrature is also exact for the declared degree-six polynomial family.
The demonstrated content is compositional, request-specific reasoning under
explicit information and price assumptions, not a novel quadrature advantage.

### Actual bounded self-assessment

The executable source contains short chains `x<=y_i<=b_i`, with each
`b_i` in `{0,1}`, and a long chain `x<=z0<=z1<=z2<=0`.
The current request is `x<=0`. Short version i attempts its own two-row
chain; current reception succeeds exactly when `b_i=0`. The long chain
always resolves this source family. All requests are theorems independently
of short-search success; unresolved means a procedural failure, not falsehood.

Actual calibration executions give prefix moments. Short traces emit five
proof nodes, the complete fallback nine, and unresolved penalty is 20 in
the declared audit-work proxy. For a full three-version cascade,

```math
C=5+5m_1+5m_{12}+20m_{123},\qquad
m_1=\tfrac12,\ m_{12}=\tfrac14,\ 0\leq m_{123}\leq q,
```

so `C-9<=-1/4+20q`. No composite C score is supplied as a premise. The
bound licenses replacement for `q<=1/80`. This changes the selected
procedure on later requests under the declared same-population model.

| Declared failure population | Full cascade expected cost | Cascade unresolved probability | Chosen policy expected cost | Strong ordinary source-visible control |
|---|---:|---:|---:|---:|
| Even parity | 35/4 | 0 | Cascade, 35/4 | 5 expected emitted nodes |
| Odd parity | 55/4 | 1/4 | Complete fallback, 9 | 6 expected emitted nodes |

The ordinary control reads visible `b_i`, chooses a successful short chain
if available, and otherwise uses the long chain. It is stronger on the
emitted-node objective. No total-runtime dominance is inferred without
charging its source inspection and proof construction. The self-assessment
example is finite and staged; it is not a general self-certification scheme
or a hard theorem-proving benchmark.

## 6. Reproducibility without reopening exposed populations

For the report's reader, prefer saved-data verification commands over the
historical prepare/evaluate invocations. Use CPython 3.12.x, NumPy 2.3.5,
Linux and the prescribed thread settings. No PyTorch is required. These
commands preserve the existing reported scientific outcomes and do not
generate new populations or fit models/alignments:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
python -m v2.experiments.freeze verify
python -m v2.experiments.summarize_f15 --check
python -m v2.experiments.neural_diagnostic_v1.runner verify
python v2/experiments/F15_ND01_analysis/summarize.py --check
python v2/experiments/F15_ND01_analysis/selection_diagnostics.py --check
python v2/experiments/F15_ND01_analysis/repeatability.py --check
python v2/experiments/F15_ND01_analysis/joint_feasibility.py --check
python v2/experiments/F15_ND01_analysis/joint_witnesses.py --check
python v2/experiments/F15_ND01_analysis/joint_semantic_error_example.py --check
```

These commands were inspected/documented here, **not rerun by this reviewer**.
Their original observed verification results are linked in the F15 and ND01
reports. The F15 summary verifier assumes the existing output directory;
its `--check` branch compares saved bytes and does not replace files.
The diagnostic runner's `verify` branch validates freeze, preparations,
exposure binding and completed unit hashes. Do not use `prepare`/`evaluate`
against completed attempt directories. Do not run one-off fixed-path audit
writers over preserved evidence.

Original F14 manifest: **34 files**, SHA256
`b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c`.
ND01 manifest: **47 files plus five source preparations**, SHA256
`9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c`.

F15 has a documented storage exception: its original retention aggregate is
zero bytes while its original sidecar names the nonempty digest. The 160
individual original units are intact. A separately preserved 15,833,616-byte
canonical recovery exactly matches the original digest
`0b0d9f79a7e74ddecef52bf5d20654eb433a5472d66cc3df63f84ae27dd04691`.
The original aggregate is not silently repaired: original F15 sidecars are
180/181, with this explicit exception; ND01 sidecars are 103/103. Both
scientific stages of each study succeeded on their first attempt.

Current verification must distinguish scope and date. F15's unchanged
Linux focused suite passed 78 tests. Gate C later passed 288 selected tests
on its first Linux attempt, including both F13 modules together. F13's
historical combined crashes and the separate Windows frozen path-portability
defect remain recorded. Neither this source review nor those focused passes
establishes a current whole-repository or Windows pass, and native crashes
were not diagnosed as hardware failure.

## 7. Principal drafting recommendations

Lead the empirical section with the retention question and its distinct
scalar/action/receipt outcomes. Put equal-information ordinary agreement
beside the main results, and state resource disadvantages where readers
first see the corresponding method. Then report neural task readiness and
zero complete support together, followed immediately by the eight-neuron
accessibility explanation. Summarize ND01 as diagnosis of the method and
endpoint, with its point-criterion table plainly labeled development.

Do not place original F15 and ND01 point-adequacy counts in one undifferentiated
success column. Do not write that all neural hypotheses were falsified,
that no representations exist, that superposition was demonstrated, that
fractional masks solve joint interpretation, or that a null outcome is
automatically novel. The supported contribution rests on the separately
assessed C4/F16 synthesis and specialized mathematical application.

The two worked examples should show at least one line of genuine premise
composition and their ordinary comparators. These examples are explanatory
mathematics and executable finite cases, not physical or general reasoning
benchmarks. Detailed derivation links remain necessary alongside polished
paper statements.

### Inspection limitations and minor read failures

One attempted path, `v2/experiments/F15_v1_analysis/summarize.py`, did not
exist; the actual reporter is `v2/experiments/summarize_f15.py`, subsequently
read directly. Some broad search/JSON output was clipped by the tool;
targeted section and aggregate reads supplied the material used above.
These are read-only inspection issues, not scientific failures or retries.

Draft review is pending receipt of the principal's paper draft. This source
map does not itself certify a final report or advance Gate D.
