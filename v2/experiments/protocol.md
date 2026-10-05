# F14-v1: prospective revision/retention challenge and ordinary-training neural probe

**Execution contract for F15.** Contributor: **ChatGPT (GPT-6 Astra Pro)**,
with attributed retention, neural and design-audit sub-agent contributions.
Developed October 4–5, 2026, from C4 revision
`6ce41d7caaba8b66cf813fc5949a92f95d42766c`.

This protocol, [configuration](config.v1.json), implementation, normative
design notes and focused tests are bound by [the freeze manifest](freeze.v1.json).
The manifest is created after development validation. Its successful
verification is a precondition to F15 execution. F14's completion and measured
research floor are recorded in [TODO](../../TODO_v2.md) and
[the work record](../work_logs/F14_2026-10-04_S1.md); a protocol document alone
does not satisfy either requirement. **No final evaluation is part of F14.**

## 1. Questions, claims and limits fixed before evaluation

The project studies useful reasoning with fallible, revisable models. This
experiment freezes two small questions, with different evidence types:

| Part | Question | What a favorable result can support |
|---|---|---|
| Revision/retention | For a declared consumer, what survives a change in prices, programs or source authority, and what must be refused or acquired? | A bounded application integrating exact ordinary information analysis, native current-request reception, useful decisions and complete declared accounting |
| Neural probe | After ordinary weighted outcome training, do selected hidden coordinates approximately implement expected-cost interventions, with evidence beyond decoding and competing descriptions? | A per-role partial approximate intervention relation on the stipulated pair populations, conditional on the five frozen trained models |

The contribution selected by C4 remains **modest methodological synthesis/formal
adaptation with small technical application extensions, supported relative to
the named inspected antecedents**. See
[C4's assessment](../contribution_review.md),
[the contribution plan, section 12](../contribution_plan.md),
[C4's derivation](../derivations/09_c4_price_revision.md) and
[its comparison scope](../literature/06_c4_contribution_comparison.md).
F14 makes that assessment testable at a bounded application level. It does
not independently establish worldwide priority, a general foundation,
exclusive capability, speed superiority, deployment calibration or learned
internal structure. The unavailable technical section noted in C4 remains
unresolved at that broader scope; F16 may reopen R-N01-01.

The ordinary controls are expected to be strong. Exact ordinary optimization
over the same information cannot be beaten in sharpness by a sound native
reconstruction. Equality or superior ordinary performance must be reported.
It displaces exclusive or performance claims; it does not automatically
displace the synthesis claim. A useful application result requires more than
passing implementation tests or reproducing an already-known mathematical
separation. Section 8 fixes the contribution-facing interpretation and further
work when the difference remains unsupported.

**Scope reductions are intentional:** three reset procedures; exact supplied
finite probability laws; one ordinary MLP architecture; proper coordinate
subsets; four fixed high-level hypotheses. There is no new sampling-estimator
experiment, stateful learned evaluator, unrestricted representation search,
hyperparameter sweep or deployment study.

## 2. Development, discovery and evaluation separation

| Use | Retention seeds | Neural seeds / data |
|---|---|---|
| Permanent development | 14101, 14102; all explicit sentinels and earlier F01–C4 examples | Training/discovery 1400401; diagnostics 1400491; all F04 examples and constructed calibration fixtures |
| F15 training and alignment discovery | None | 1500401, 1500402, 1500403, 1500404, 1500405 |
| F15 final evaluation | 15101 through 15116 inclusive | Corresponding streams 1500491, 1500492, 1500493, 1500494, 1500495 |

Every already examined example remains development evidence. New seeds do not
make an old example newly held out, and development results cannot be pooled
into final denominators. The generator itself is known and fixed; evaluation
tests new draws from that stipulated generator, not generalization to unknown
tasks. Retention's ten variants share the initial law within a population
seed. They are **160 episodes from 16 population draws**, not 160 independent
population replications.

F15 has two separate commands. `prepare` trains all five models and selects
all alignments using their own discovery data. It saves and hashes the complete
networks, untrained initializations, candidate pools, all scores, decoders and
selected indices. **All five complete discovery artifacts must be durable
before any final retention case or neural evaluation pair is generated.**
`evaluate` preflights all artifacts and writes an exclusive exposure marker
binding their preparation manifest before generating cases. It never trains,
selects another alignment, adds candidates, chooses a seed or changes a cutoff.

The seed list is a sampling plan, not additional information available to a
restricted retention method. Its admitted hypothesis class is the complete
probability-law fiber stated below. A method may not enumerate seeds or the
generator's integer-weight support to recover discarded information. Source
revision labels contain no generator seed. Hidden scoring inputs remain
outside restricted solvers. The paired neural streams and generation counts
are specified in [neural.py](neural.py); changing call shape or stream identity
requires a new freeze, even if a top-level seed stays the same.

The fourth neural scale was changed during F14 development from the
illustrative exponential scale to normalized task probabilities. This was a
design challenge about a stronger ordinary explanation, before final data,
without selecting on trained-model performance. Earlier exponential-family
outputs are preserved and marked superseded development. The final family
below is the only F15 family. Other development repairs, including conditional
base calibration and accounting guards, are recorded in the work log.

## 3. Revision/retention population and information contracts

### 3.1 Source and consumers

A world is a three-bit failure mask in lexicographic order, with bit 1 meaning
that the corresponding fixed reset procedure fails. A full order tries each
procedure until the first success; if all tried procedures fail, it pays the
terminal penalty. Source outcomes are fixed within a world. The independent
path interpreter in `v2/verification/case_reference.py` supplies exact cost
vectors. The connection to actual bounded native-attempt statuses is exercised
by a permanent development test. Final population evaluation is the finite
reset-law model, not a new live-workload calibration.

For each seed, `random.Random("F14-retention-v1:<seed>")` draws eight independent
integer weights uniformly from 1 through 17 and normalizes them as rational
probabilities. Initial prices are `(1,1,1)`, terminal penalty is `4`, and the
shared deterministic fallback costs `5/2`. Every sampled law has full support.
The six full permutations are the initial consumer family. The source-drift
variant uses the next eight integer draws for the new law.

| Frozen variant | Revision |
|---|---|
| `unchanged` | No price, program or authority change |
| `small_price` | Procedure 2 price increases by `1/40` |
| `small_negative_price` | Procedure 2 price decreases by `1/40` |
| `large_price` | Procedure 2 price increases by `1` |
| `large_negative_price` | Procedure 2 price decreases by `1/2` |
| `proportional` | All prices and terminal penalty multiply by `2` |
| `program_edit` | Replace full orders by the six ordered pairs, stopping after two attempts |
| `known_marginals` | Keep old prices/orders; supply all three exact current marginal failure probabilities |
| `withdrawal` | Old facts lose current authority; scoring law stays unchanged |
| `source_drift` | Old facts lose current authority; scoring law changes |

All methods receive the same initial source and current public query metadata.
The known marginal inputs are charged equally. Withdrawal invalidates old
facts for **every** method, including complete retention: an old true theorem
need not be an admissible current premise.

### 3.2 Six methods, with complete source accounting

| Method | Durable information | Strong ordinary computation |
|---|---|---|
| `fresh` | Eight world-probability fields, affine information rank 7 | Direct weighted-world means and point-law regret; no unnecessary LP |
| `cached_proof` | Same full law, old proof and its complete old source context | Check old reception; direct full-law computation and replacement proof when required |
| `full_joint` | Seven nonempty joint failure moments | Exact Boolean moment inversion followed by direct computation |
| `tailored` | Minimal old-price summary: one base and four residuals, rank 5 | Reconstruct the old mean profile and optimize its compatible-law fiber |
| `exact_intervals` | All six old means, rank 5 | Generic exact optimization over the same information fiber as the tailored summary |
| `marginal_diagnostic` | Three marginal probabilities, rank 3 | Exact optimization over the larger fiber; a deliberately weaker-information diagnostic |

All six methods participate in both access panels. Payloads have different
information contents by design. Equal-information comparisons are
`fresh`/`cached_proof`/`full_joint` and `tailored`/`exact_intervals`, at the same
source-authority state and acquisition access. The hidden full-law scoring
oracle is labeled a different-information reference where appropriate.

Information ranks concern these declared linear measurements of the source
law. Byte comparisons concern their explicit wire encodings and complete
storage accounting. Neither is a lower bound for arbitrary nonlinear packing,
compression, source-program descriptions or seed reconstruction. The five-value
summary is minimal for the stated linear consumer family under C4's assumptions;
it is not declared to be the shortest possible bit representation of a sampled
finite-generator law.

The exact fiber is `P={p>=0: A p=b, sum(p)=1}` after the actually retained and
currently admitted measurements. Generic rational elimination and basic
feasible-point enumeration use at most `C(8,4)=70` candidate bases. Strong
full-information methods use the known point directly. Bounds are checked
against exact dual certificates; no floating tolerance enters the retention
calculation. A canonical feasible point computed from retained constraints
provides the native consistency witness. The scoring law is not silently
used for that witness.

### 3.3 Numerical answers, decisions and native reception

For each requested order, return its exact interval `[l,u]` over the fiber:

| Numerical disposition | Frozen rule |
|---|---|
| Exact | `l=u`; return that value |
| Meaningful approximation | `0<u-l<=2 tau`; return the midpoint |
| Refusal | `u-l>2 tau`; no admitted point answer |

Here **`tau=1/20`** in declared cost units. The midpoint minimizes worst-case
absolute error for this scalar consumer. Midpoints from different intervals
are not claimed to form one coherent probability law.

For each order and the fallback, compute the **same-law** robust regret

\[
\rho(a)=\max_{b}\max_{p\in P}\{C_a(p)-C_b(p)\}.
\]

Choose the minimum regret, then the smallest upper absolute cost, then the
fixed order index. Admit the choice only if **`rho<=epsilon=1/20`**. A selected
fallback is `certified_fallback`; an admitted procedure is `certified_order`.
If the minimum regret exceeds epsilon, report `refusal_to_fallback` and
actually pay the fallback's cost. Refusal earns no useful-choice credit, and
its realized regret is reported even when large. Regret cannot be computed
by subtracting unrelated interval endpoints.

The tolerance is five percent of one old attempt charge and two percent of
fallback cost. These are declared task preferences, not fitted cutoffs. A
`1/40` price edit supplies a prospectively motivated approximation regime:
knowing the complete old mean profile can preserve a useful decision while
exact recovery fails. Larger changes, program edits and authority loss test
the other regimes. No positive fraction is promised in advance.

For the selected admitted order, request a native proof that its expected
cost minus fallback is at most zero. If the decision is fallback or refusal,
the first order's comparison remains a diagnostic only. Probability sources
have unit `P`; the declared positive `P→U` conversion of factor one makes the
normalization to the chosen loss unit explicit. Existing row, scale, addition,
conversion, rewrite and all-cases rules reconstruct the ordinary dual bound.
The producer budget is **128 proof steps**. An unavailable proof or a valid
weaker bound is never relabeled a received zero-budget request.

Each row distinguishes:

- Truth of that comparison under the stipulated full current law.
- Robust validity over the actual retained/current information fiber.
- Proof availability under the frozen producer budget.
- Reception for the exact current pair, source revision, units and budget.
- Numerical admission and useful all-alternative decision quality.

The native fallback comparison is not itself a proof of epsilon regret against
every order. That stronger certificate comes from the ordinary fiber argument.
Permanent development sentinels exercise stale-source rejection, changed-pair
rejection, valid-but-budget-unavailable production and the F08 full-source /
target-unit-reduct separation. They are not final cases or new kernel results.

### 3.4 Matched acquisition panels

**No reacquisition:** a method receives only its payload, current public query
and newly declared source facts. Discarded information is unavailable.

**Adaptive reacquisition:** every method has the same exact source-oracle
capability, whose archive storage is charged even when unused. First compute
the retained-data answers and decision. Acquire only when at least one of the
six numerical queries is refused or the decision is refused. The preliminary
work is charged. This is a fixed quality-first rule, not an optimal policy for
every acquisition price.

For a stable one-price edit, the complete old-mean profiles may acquire the
two current means for `(0,2,1)` and `(0,1,2)`. C4's constructive repair restores
the full law; the generic old-plus-new equation system independently checks
the same result. Other necessary repairs obtain the full eight-field current
law. Two-mean repair is not used after old facts lose authority. No claim of
two-measurement minimality is made when additional lower-order facts are
already known; the known-marginal variant here keeps old prices.

An exact mean query is a stipulated source operation, not a finite-sample
estimator. Returning two means actually evaluates sixteen world/order paths
at the source. Record query calls, returned scalar fields, transferred bytes,
source work and archive bytes separately. A full-law response has eight
fields by wire convention; seven independent coordinates would encode the
normalized law. Report both dimensions rather than claiming an eight-scalar
information lower bound.

Sensitivity prices are **0, `1/20`, `1/2` per exact scalar measurement**.
The initial eight source fields and any three new known marginals are common
charges; method-specific repair adds two or eight fields when requested.
Decision loss plus these explicit acquisition prices is reported. CPU time
and storage bytes have no invented conversion to those loss units.

### 3.5 Resource vector and finite accounting

F15 runs exactly **16 seeds × 10 variants × 6 methods × 2 panels = 1,920
method rows**, each with six numeric query dispositions, for 11,520 queries.
`run_generated_case` measures common synthetic source/query production and
serialization. Each method separately charges retention production, old
source/proof preparation and checks, current archive production, acquisition,
update/solve work, decision computation, current context construction and
the complete native protocol. Internal native substage timers are diagnostic
subtotals and are not added twice. Scoring and report writing are separately
identified harness work.

Report durable payload, cached source and proof, current source and proof,
public schema, query metadata and external archive bytes. Serialized active
upper bounds can include duplicate encodings; they are not process RSS.
Report basis counts, vertices and rational matrix dimensions for transient
solver work. Initial full-source exposure also counts, even for a small final
cache. Common production/input costs are charged equally rather than omitted.

Both arithmetic-only and native-inclusive timings are retained. A fast direct
numeric control need not pay an optional receipt wrapper when discussing
numeric computation alone. Receipt-required comparisons include the wrapper
for every method. Timing here is observed local wall time; process-level wall
and CPU totals also appear in the runner. No distributional speed inference
is made from a single measured event.

For horizons **1,4,16,64**, report `I+h U` using measured initial cost `I` and
one-update cost `U`. Report the strict eventual crossing against fresh solving
and each stated horizon. This is an **algebraic projection**, not a repeated
update experiment: future cached replacements, changing revisions and runtime
noise are not modeled. A cheaper setup can win briefly while its slower
updates lose later. Claims must identify both the quality and access contract;
faster refusal is not a successful computation of the same answer.

## 4. Ordinary-training neural probe

### 4.1 Task, labels and frozen compute

Independent raw inputs are `x1,x2~Uniform[-1,1]` and
`cFN,cFP~Uniform[.5,2]`. Let

\[
\eta(x)=\tfrac12+(x_1+x_2)/8,\quad Y\mid x\sim\mathrm{Bernoulli}(\eta),
\qquad J_0=c_{FN}\eta,\quad J_1=c_{FP}(1-\eta).
\]

Train a dense four-input, 32-ReLU, one-affine-logit sigmoid network by ordinary
weighted binary cross-entropy with weight `cFN Y+cFP(1-Y)`. **Only sampled
binary outcomes enter as training labels.** Costs are task inputs and loss
weights, not internal targets. No modular architecture, auxiliary expected-cost
loss, activation label or interchange-training objective supplies the proposed
hidden structure. Its analytical optimum is `p*=J0/(J0+J1)`; action 1 is chosen
when predicted probability is at least one half.

| Parameter | Frozen value |
|---|---|
| Parameters / arithmetic | 193 parameters; float64 |
| Initialization | Hidden normal SD `sqrt(2/4)`, output normal SD `1/sqrt(32)`, zero biases |
| Training | 3,000 online steps × 256 outcomes = 768,000 labels/model |
| Optimizer | Adam, learning rate .003, beta1 .9, beta2 .999, epsilon `1e-8` |
| Decoder fit rows | 1,024/model, independent of selection/evaluation streams |
| Discovery pairs | 128/role/stratum |
| Hidden subset capacity | Exactly eight of 32 coordinates per role |
| Candidate budget | 128 per role/hypothesis/control; duplicates consume budget |
| Decoder | Scalar affine; standardized features; ridge `1e-6`, unpenalized intercept |
| Final pair count | 8,192/role/stratum/model |
| Final ordinary task count | 8,192/model |
| Proposal batch / cap | 4,096; at most `4,000*n` proposals per stratum sample |
| Random generator | Explicit NumPy PCG64 with SeedSequence, fixed stream identifiers |

There are four hypotheses × five arms × two roles: **5,120 candidate
evaluations/decoder fits per model**, 25,600 across five models. Training uses
3,840,000 binary outcomes in total. The main final intervention population has
409,600 intended pairs across all models/roles/strata; independent incorrect
donor streams add the same number of generated pair records. All 20
hypothesis/arm combinations are evaluated, producing 8,192,000 role-pair
evaluations, in addition to gauges, calibration and diagnostic computations.
Saved resource fields give actual proposal and forward-work counts.

### 4.2 What is intervened on

Swap one selected hidden subset from a donor into a base example, leaving all
other activations at the base values. Role 0 predicts replacement of `J0`;
role 1 predicts replacement of `J1`. The high-level probability is respectively
`J0(d)/(J0(d)+J1(b))` or `J0(b)/(J0(b)+J1(d))`.

For an affine output, the swapped subset contributes
`phi_S(d)-phi_S(b)` to the logit. Exact expected-cost interchange with an exact
base network would require `phi_S0=log J0+constant` and
`phi_S1=-log J1+constant` on a connected comparison domain. Finite ReLU pieces
cannot represent these smooth logarithms exactly throughout the open domain;
the empirical criterion is approximate. Raw expected-cost decoding is
auxiliary and cannot establish the causal claim. See
[the derivation and adverse cases](F14_design_notes.md) and
[the neural design](neural_design.md).

Select candidates by actual intervention probability MSE; baseline-adjusted
effect MSE and decoder NMSE break ties, in that order, within `1e-12`. The
guided pool starts with the eight largest absolute feature/target correlations,
then samples subsets from a 25% uniform / 75% correlation mixture. Every arm
uses the same capacity, candidate count, selection samples and actual
high-level scoring access.

| Arm | Matched change |
|---|---|
| `aligned` | Guided proposals for the declared concept |
| `random` | Uniform proper subsets; best-of-128 search and the same decoder |
| `permuted_concept` | Permute target rows for proposal/decoder fitting; retain actual intervention scoring |
| `shuffled_donor` | Independent incorrect donor from the same stratum donor marginal, in discovery and evaluation |
| `untrained` | Original random initialization with otherwise identical search |

The permuted arm is a control procedure, not an exact permutation p-value.
Incorrect donors are generated independently per record; no finite-array
permutation is used to pretend dependent rows are independent. Whole-layer
transplant and no-swap behavior are also reported as diagnostics. Two role
subsets may overlap. Secondary two-donor composition/order tests expose that
limitation; primary success does **not** establish a joint constructive
abstraction or arbitrary simultaneous interventions.

### 4.3 Fixed pair strata and high-level rivals

Base and initial donor inputs are independent draws. Rejection depends only
on the stipulated high-level task, never the trained model. Each role and
stratum has its own stream. In the two equality strata, solve the donor cost
input to preserve the indicated exact expected cost and reject if it leaves
`[.5,2]`.

| Stratum | Frozen condition on the identity high-level model |
|---|---|
| `mixed_near` | `abs(pH-.5)<=.04`; both `abs(pH-p*(b))` and `abs(pH-p*(d))>=.05` |
| `mixed_far` | `abs(pH-.5)>=.15`; the same two gaps at least .05 |
| `preserve_other` | Preserve the untouched action cost; change eta by at least .08 and target cost by at least .1 |
| `equal_target` | Preserve the targeted action cost; change eta by at least .08 and other cost by at least .1 |
| `scale_separating` | Every nonconstant rival differs from identity `pH` by at least .05; identity differs from base by .05 and donor by .025 |

The preserve-other stratum alone could be explained by copying the donor's
whole output. The mixed strata remove that simple equality. The equal-target
stratum tests whether swapping an input factor changes output despite an
unchanged proposed cost. Its no-effect rows cannot hide mixed-stratum failures
because each stratum has its own criterion. Rival decision margins are not
used to reselect identity-conditioned pairs.

The four fixed, network-independent positive scale functions are:

| Identifier | `g` | Concepts |
|---|---|---|
| `identity` | `1` | `(J0,J1)` |
| `inv_eta` | `1/eta` | Reassign the shared eta factor; first concept is `cFN` |
| `inv_one_minus_eta` | `1/(1-eta)` | Reassign the other outcome factor; second concept is `cFP` |
| `inv_total_cost` | `1/(J0+J1)` | Normalized task probabilities `(p*,1-p*)` |

Every scale preserves the ordinary optimum but generally changes one-role
interventions. Each receives the full matched search. The three rivals have
three times the aggregate aligned search budget of identity; that is disclosed,
not hidden as one comparator. The best rival is chosen on discovery scores
before evaluation, and all rival results remain reported.

Primary scale contrasts compare **the same identity-selected intervention**
against each competing prediction on all `scale_separating` rows. Separately
searched rival subsets are additional results. Different scales can have
different approximation difficulty within eight coordinates; a failed rival
search does not establish a unique absolute cost representation. The bounded
family does not cover arbitrary positive or network-dependent scales.

### 4.4 Transport and method calibration

For every aligned high-level hypothesis, draw one fixed evaluation-stream
permutation and independent log-uniform positive neuron scales in `[1/8,8]`.
Transport incoming weights/biases, outgoing inverse scales, subset indices and
decoder coefficients. **No refitting is allowed.** Maximum discrepancies in
ordinary probability, intervened probability and decoder value must each be
at most **`1e-10`**. A global high-level factor-two scale is also transported
and must preserve predictions/decoder scaling within that tolerance.

These controls cover the specified transformations, not every functional
equivalence on the input domain. Always-active affine units can admit additional
mixing that changes coordinate substitutions while preserving ordinary output.
The bounded-domain example and primary-source scope checks are in
[the source note](../literature/07_f14_protocol_sources.md#6-gauge-controls-are-not-an-exhaustive-equivalence-class).
No generic parameter-identification or arbitrary-reparameterization invariant
claim is made, and a negative coordinate search remains limited to its budget.

The permanent unused-duplicate witness requires exact decoding of an unused
unit while its intervention has zero causal output effect. A separately
constructed 32-unit ReLU calibration approximates the four log terms by
secants and gives a conservative uniform probability error below .01; its
known eight-coordinate role subsets exercise all pair strata and transported
gauges. Wrong-role and whole-layer interventions are challenged. This network
is explicitly compiled, receives no ordinary-learning credit, and supplies
neither the ordinary model's labels nor its architecture modules.

A separate two-unit cancelling-pair development example has exact cost
interchange effects while removing both units leaves ordinary output unchanged.
It is not the F14 training task and is not evidence of such a mechanism in
trained models. It fixes an interpretation boundary: even a positive partial
intervention relation does not establish ordinary-circuit necessity. The
source debate and the example are documented in
[the focused source check](../literature/07_f14_protocol_sources.md).

## 5. Statistical thresholds, falsifiers and negative interpretation

The neural inference population is conditional on each already trained and
selected model/alignment and the stipulated pair generator. Different metrics
may share rows. Intended and incorrect donor records are independent across
rows; strata are separately generated. No claim of iid repeated training
seeds or deployment calibration is made.

For a bounded sample mean with range width `w`, use the two-sided Hoeffding
interval with radius

\[
r=w\sqrt{\log(2K/\alpha)/(2n)},\qquad K=560,\quad\alpha=.05,
\]

clipped to the declared range. The union bound covers all rows in the following
fixed family. No data-dependent reduction of `K` is allowed. Search candidates
chosen only on independent discovery data are not additional evaluation
claims. Fixed strata are pooled only with equal sizes and equal weights;
Hoeffding applies to independent bounded terms even when their stratum
distributions differ. No quadratic Cartesian-pair sample inflation is used.

| Interval rows | Per model | All five models |
|---|---:|---:|
| Ordinary task probability MAE and normalized decision regret | 2 | 10 |
| Conditional base MAE: two roles × five strata | 10 | 50 |
| Intervention MAE: four hypotheses × two roles × five strata | 40 | 200 |
| Near/far decision disagreement: four × two × two | 16 | 80 |
| Paired advantage over four matched controls, pooled over five strata: four × two × four | 32 | 160 |
| Three same-subset scale contrasts × two roles, each frequency and error advantage | 12 | 60 |
| **Total** | **112** | **560** |

Probability absolute errors and disagreement indicators lie in `[0,1]`.
The exact task action-regret maximum is `11/8`; divide regret by it before
using a `[0,1]` interval. Paired absolute-error improvements lie in `[-1,1]`.
At `n=8192`, radii are approximately `.0247261` and `.0494521` respectively;
at the pooled `n=40960`, `.0110578` and `.0221157`. These conservative margins
make the actual sample means required for support stricter than the tolerances.
Inconclusive intervals are a possible intended outcome, not grounds to extend
the sample or choose a new threshold.

| Requirement | Frozen interpretation |
|---|---|
| Ordinary task learning | Upper MAE bound `<=.05`; upper normalized-regret bound times `11/8 <=.05` |
| Conditional base learning | Upper base MAE `<=.05` separately for each role/stratum |
| Interchange accuracy | Upper intervention MAE `<=.05` for every stratum of both roles |
| Far / near decisions | Upper disagreement bound `<=.10` / `<=.35`, respectively |
| Matched-control specificity | Lower paired MAE improvement `>=.01` over **each** of random, permuted-concept, incorrect-donor and untrained search, per role/hypothesis, on the equal-stratum mixture |
| Same-subset scale specificity | Lower identity MAE advantage `>=.01` against each rival, for both roles on the separating stratum |
| Separating coverage | All 8,192 planned rows must satisfy every rival gap; reported conditional-frequency lower bound `>=.90` |
| Numerical validity | All four transported gauges, global scale and unused-duplicate checks valid; zero alignment refits |
| Fixed-replicate pilot support | Full identity criteria on at least four of the five prespecified models, with numerical validity for every model |

The .05 probability tolerance is a declared five-percentage-point resolution;
the .01 superiority margin requires a material difference rather than a
strictly positive microscopic advantage. Decision thresholds separately treat
near-boundary and far-boundary changes. They are design preferences, not
empirical calibrations. No decoder threshold substitutes for intervention
agreement. Diagnostic decoder drift, contribution residuals and RMSE do not
receive unlisted confirmatory claims.

Conditional base and actual-intervention bounds also imply

\[
\mathbb E\left| (p_I-p_B)-(p_H-p_*)\right|
\le \mathbb E|p_I-p_H|+\mathbb E|p_B-p_*|\le .10.
\]

This is a derived **mean absolute adjusted-effect** bound, not an RMSE or
per-example guarantee, and requires no extra confidence-family row. It applies
to every scale because the unmodified high-level probability is invariant.
The separating frequency is conditional on a generator designed to separate;
it does not estimate the prevalence of separating examples in ordinary inputs.

The executable analysis retains all five models and all controls. Its outcomes
are distinct:

- **Numerical/protocol failure:** transport, counts, hashes, budgets or source
  contracts fail. Repair the implementation or protocol; no scientific support
  is assigned to the failed run.
- **Task underlearning:** the ordinary task criterion fails. This is a failure
  at the frozen training budget, not evidence that expected costs are absent
  from every possible learned representation.
- **Interchange inadequate:** the fixed selected subsets miss one or more
  thresholds. A lower confidence bound above the MAE tolerance specifically
  falsifies that selected subset's tolerance claim on that stratum. Merely
  failing an upper-bound support test can be inconclusive.
- **Adequate but not discriminated:** identity interchange is adequate but
  strong ordinary controls or scale explanations are not separated. Do not
  claim a distinctive extraction method or a selected absolute-cost description.
- **Competing scale supported:** a separately searched rival satisfies its
  bounded criteria while identity does not. Report its exact scope and search
  limits, without assuming unique internal semantics.
- **Scoped identity support:** the full criteria above hold. This supports
  only the stated per-role partial relation for these fixed models and pair
  generators; it establishes neither a joint abstraction nor worldwide novelty.

A negative coordinate-subset search does not exclude distributed rotations,
larger subsets, a different architecture, another task, more training or all
possible causal abstractions. Such changes would be new work, not rescue
search within this frozen test.

## 6. Retention correctness and useful-application criteria

All 160 episodes and 1,920 method rows must be reported in their frozen order.
Missing, duplicated or substituted cases/controls make the run incomplete.
Every rational interval must contain the actual stipulated source value;
every admitted midpoint must meet tau; every certified decision must meet
epsilon. Native reception cannot contradict the full source value or its
retained-fiber bound. These are exact zero-false-admission requirements.
`analysis.py` also checks order/index bindings, coherent regret, source-truth
flags and the distinction between fallback certification and refusal.

A **useful native derivation** must satisfy all of the following:

1. It concerns a direct price or program edit, not unchanged/proportional reuse.
2. It certifies the actual selected and executed nonfallback order for the
   current request/source.
3. Its upper bound on cost minus fallback is at most `-1/20`.
4. Its native proof uses at least two distinct nonzero source-row premises.
5. The independently computed coherent regret certificate is at most `1/20`.

The bounded application criterion requires useful derivations in at least
**four distinct `(seed,variant)` episodes across at least two population seeds**,
including a price revision and a program edit. At least one must use
`tailored` or `exact_intervals` **without reacquisition and with more than one
feasible law vertex, with an approximate rather than exact selected-order
cost**. An unknown law can still have a known scalar mean; the extra condition
excludes merely shifting an already-known selected mean by a constant. It
also prevents the whole demonstration from reducing to full-law retention.
The criterion establishes a meaningful
bounded integration/use case, not a new mathematical theorem, independent
novelty verdict or unique capability. Source-row composition and its semantic
significance remain available for F16 reconstruction.

Report exact/approximate/refused counts, certified orders/fallbacks/refusals,
true-full-law but unsupported-retained-fiber comparisons, current receipts,
stale-cache rejections, budget refusals, actual regret, repair usage and all
paired resource differences. Identify rows where an approximate number
coexists with a certified order and rows where refusal still loses decision
value. Development counts validate these report paths but are not acceptance
frequencies for F15. Retention summaries are descriptive for the sampled
finite population; no unregistered confidence claim is made about workloads.

The report includes complete numerical, decision, native and acquisition
quality vectors beside resource differences. Literal equality of two refusals
is not admitted service. Separate flags require all numerical queries admitted,
a certified decision, and reception of a selected-order proof. Equal-information
control groups must agree on exact intervals, deterministic ordinary decisions,
semantic native targets and the frozen acquisition policy. Proof size, timing,
cache behavior and budget-limited receipt status remain separately reported;
equal information alone does not guarantee equal native production cost.

## 7. Runtime, commands, failures and reproduction

The primary frozen runtime is **CPython 3.12.x and NumPy 2.3.5**, CPU only.
Set `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1` before the Python
process starts. `requirements-f14.txt` is separate from earlier phase-one
requirements; no PyTorch installation or change to those requirements is
needed. Record interpreter, OS/platform, NumPy version, thread environment,
wall/CPU time, source/config/manifest hashes and data/artifact digests. NumPy
does not promise bitwise equality across different builds/hosts. Such drift is
reported and checked with the numerical contract, not silently treated as
identical arithmetic or hardware failure.

The manifest binds raw bytes. Scoped Git attributes preserve the frozen files
and development artifacts across Windows line-ending settings. If an existing
Windows working tree already contains converted CRLF versions of unchanged
dependencies, use a clean fresh checkout/worktree of the F14 commit before
verification. An attribute change need not rewrite existing working files.
Do not replace manifest hashes merely to admit a mismatching checkout.
Transport correction is distinct from an unexplained Python/native failure;
neither a hash mismatch nor Linux success diagnoses the earlier host.

From the repository root, F14 development validation is:

```bash
python -m pip install -r v2/experiments/requirements-f14.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -m unittest discover -s verification -p 'test_v2_f14*.py' -v
python -m v2.experiments.runner develop --task F14 --out <new-development-directory>
python -m v2.experiments.freeze verify
```

The **F15 commands below are instructions for the next task, not operations
performed in F14**:

```bash
python -m v2.experiments.freeze verify
python -m v2.experiments.runner prepare --task F15 --out v2/work_logs/F15_v1_run1
python -m v2.experiments.runner evaluate --task F15 --out v2/work_logs/F15_v1_run1
```

In PowerShell, use the Python 3.12 launcher and set the environment first:

```powershell
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
py -3.12 -m pip install -r v2/experiments/requirements-f14.txt
py -3.12 -m v2.experiments.freeze verify
# In F15 only:
py -3.12 -m v2.experiments.runner prepare --task F15 --out v2/work_logs/F15_v1_run1
py -3.12 -m v2.experiments.runner evaluate --task F15 --out v2/work_logs/F15_v1_run1
```

Use one primary output directory for this version. Do not delete, overwrite or
silently restart it to get favorable results. Complete units have independent
SHA256 sidecars; stage manifests bind them. Complete-stage markers prohibit
another run. Every model and control is checked before exposure, including
training steps, outcome labels, absence of cost labels, subset/search budgets,
network/decoder shapes, finite values and internal hashes.

Preserve stdout/stderr and native exit status externally when launching a
process. Caught failures produce a traceback and observed attempt wall/CPU
record. A hard process exit may leave only its start marker and completed
units; missing end times are **unobserved**, not zero and not inferred from
later idle time. Classify deterministic bugs, missing dependencies, numerical
failures and unexplained process failures separately. Existing Windows-host
symptoms do not diagnose hardware and are not an additional F14 investigation.

After an **unexplained** failure, allow at most one unchanged retry for that
stage, with a concrete record of the reason:

```bash
python -m v2.experiments.runner evaluate --task F15 --out v2/work_logs/F15_v1_run1 \
  --retry-unexplained --failure-note "<observed failure and reason it is unexplained>"
```

The analogous `prepare` command is permitted only before evaluation exposure.
Retry uses an exclusive second-attempt directory, verifies the original
freeze/preparation digest, reuses completed checked units, preserves partial
files and reruns only unfinished units. It cannot add training, change seeds
or hide the first attempt's costs. There is no third attempt. A deterministic
scientific or implementation flaw requires a named repair and versioned
protocol disposition, not the unexplained-failure switch. Directory markers
are an auditable workflow control, not proof that nobody ran an unrecorded copy.

If a frozen dependency or criterion changes, the current version's primary
analysis stops. Preserve exposed data as development for any new version,
state the exact amendment and choose fresh evaluation streams before another
primary run. Never replace an existing manifest in place to erase this event.
Development fixes before the first final freeze are recorded in F14's work log.

## 8. F15 report, contribution decision and later work

F15 produces `v2/experiments/results.md` and machine-readable outputs. The report
must identify its commit, freeze hash, exact command/environment, every attempt
and exposed/completed/missing unit, all model and method outcomes, interval
criteria, source access, acquisition charges and resource limits. It reports
the prescribed failures and null comparisons as well as attractive examples.
It may not claim independent review from F14's collaborating implementation
audits. F16 remains the fresh adversarial reconstruction task.

| Outcome | Required contribution disposition |
|---|---|
| Correct admissions and useful bounded application, ordinary controls match or win | Report integration/synthesis evidence and its exact limits; no speed or exclusivity claim |
| Correct implementation but no useful-application criterion | Implementation validation only; identify which consumer, source or decision obligation is missing |
| Neural adequate but controls/scales tie | Possible partial relation, unresolved interpretation/extraction specificity; no unique cost claim |
| Neural unsupported or underlearned | Complete the bounded negative report; do not claim causal expected-cost representation |
| False admission, stale authority, hidden source access, incoherent regret or omitted source costs | Block the affected application claim; assign the exact mathematical/implementation repair |
| Closest-work reconstruction displaces the claimed meaningful difference | Reopen R-N01-01 and name a 60/90-minute comparison or constructive-work chunk with an explicit evidence target |

Neither a positive neural result nor superiority to ordinary arithmetic is
required for the current modest synthesis claim. Conversely, a null result
does not automatically become a novel negative finding. Its significance,
exact difference and antecedents must be supported. F15 may complete with
negative results while Gate C remains blocked. Gate C separately requires
technical readiness, meaningful scoped contribution support and F16's resolved
objections; F14/F15 execution alone cannot manufacture that pass.

The next implementation task after completed F14 is **F15, unstarted until
explicitly undertaken**. F16, F17 and Gates C/D remain unattempted. Gates A/B
retain their stated scoped readiness passes. The cumulative POST-B-1 clock
continues from C4's 534.976816 engaged minutes, including its earlier
54.976816-minute eight-hour overshoot; the next checkpoint is sixteen hours.
F14 time and floor accounting are in its work/time ledgers, separate from
experimental compute and overlapping sub-agent work.

## 9. Primary-source and internal grounding

The frozen experiment is an adaptation and application of established tools.
The precise design arguments and inspection limits are in
[F14's design audit](F14_design_audit.md),
[the retention note](retention_design.md),
[the neural note](neural_design.md) and
[the root derivations](F14_design_notes.md).
The additional [source inspection and cancellation analysis](../literature/07_f14_protocol_sources.md)
records exact inspected versions and limits of stronger mechanistic claims.

- Geiger, Lu, Icard and Potts (2021),
  [Causal Abstractions of Neural Networks](https://proceedings.neurips.cc/paper/2021/file/4f5c422f4d49a5a807eda27434231040-Paper.pdf),
  sections 2–3: causal abstraction and interchange methods are antecedents;
  this protocol claims only its restricted approximate relation.
- Hewitt and Liang (2019),
  [Designing and Interpreting Probes with Control Tasks](https://aclanthology.org/D19-1275.pdf),
  sections 2–3: probe/control comparisons motivate matched capacity; this
  protocol adapts that concern to intervention-scored subset search.
- Geiger et al. (2022),
  [Inducing Causal Structure for Interpretable Neural Networks](https://proceedings.mlr.press/v162/geiger22a.html):
  interchange intervention training is a relevant contrast; it is not used
  in the ordinary model here.
- Geiger et al. (2024),
  [Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations](https://proceedings.mlr.press/v236/geiger24a/geiger24a.pdf),
  sections 3.3–3.4: broader distributed alignment methods limit the meaning
  of a negative coordinate-subset result.
- Hoeffding (1963), *Probability Inequalities for Sums of Bounded Random
  Variables*, JASA 58(301):13–30,
  [original-paper scan](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf),
  printed page 16, Theorem 2: the independent bounded-variable inequality,
  combined here with a finite union bound. The concentration tool is established.
- NumPy,
  [2.3 random-number compatibility policy](https://numpy.org/doc/2.3/reference/random/compatibility.html):
  explicit bit generator, call shape and runtime provenance are necessary;
  broad cross-host bitwise reproduction is not promised.

No local derivation, successful test or absence from this focused source set
is evidence of worldwide firstness.
