# F14 ordinary-training neural probe: implementation and interpretation

Status: prospective F14 design with **development validation only**. The final
protocol and its frozen configuration govern F15. This note explains the
implementation in [neural.py](neural.py); it does not report a held-out result.
It specializes [the F04 design](F04_neural_probe_design.md), retaining its
ordinary-training requirement and competing high-level cost-scale explanation.

## 1. Ordinary task and what training may access

Inputs are independently uniform `x1,x2 in [-1,1]` and `cFN,cFP in [0.5,2]`.
Let

```
eta(x) = 1/2 + (x1+x2)/8,
Y | x ~ Bernoulli(eta(x)),
J0 = cFN * eta(x),
J1 = cFP * (1-eta(x)).
```

The unconstrained network has four raw input coordinates, 32 ordinary ReLU
hidden units, and one affine scalar logit followed by sigmoid. It has 193
parameters. Inputs, including the two declared costs, enter through the same
dense layer. There are no special cost-computation modules or hidden targets.
The training objective is ordinary weighted binary cross-entropy:

```
L = mean((cFN*Y+cFP*(1-Y)) * (logaddexp(0,z)-Y*z)).
```

The derivative used by the implementation is

```
dL/dz_i = (cFN_i*Y_i+cFP_i*(1-Y_i)) * (sigmoid(z_i)-Y_i) / batch_size.
```

Post-hoc expected costs are calculated by separate functions. A development
test replaces both `action_costs` and `concepts` by functions that raise an
exception, then executes ordinary training successfully. Another checks the
analytic weighted-BCE gradient against finite differences away from ReLU kinks.

Conditional expected loss is `-J0 log(p)-J1 log(1-p)`. Its derivative vanishes
at `p*=J0/(J0+J1)`; its second derivative is positive on `(0,1)`. Consequently,
the independent high-level model predicts action 1 exactly when `J0>=J1`.
This analytical model supplies post-hoc intervention targets; training receives
only newly sampled binary outcomes. Equal performance on the ordinary task
does not imply that a particular internal explanation is correct.

## 2. The affine-output restriction matters

Write `h=ReLU(Wx+b)`, `z=beta+v.h`, and
`phi_S(x)=sum_{i in S} v_i*h_i(x)`. A donor substitution on coordinates `S`
changes the logit by

```
z_intervened = z(base) + phi_S(donor) - phi_S(base).
```

If the unmodified network exactly realizes the optimal logit
`log(J0)-log(J1)`, then exact J0 interchange agreement requires

```
phi_S0(donor)-phi_S0(base) = log(J0(donor))-log(J0(base)).
```

On all pairs of a connected comparison domain, this says
`phi_S0=log(J0)+constant`. For J1 it says
`phi_S1=-log(J1)+constant`. On this experiment's restricted pair support the
equations constrain the sampled comparisons; they do not establish an
unrestricted global representation theorem. A finite ReLU function is
piecewise affine, so exact equality to these nonlinear logarithms throughout
the continuous input domain is not expected. The empirical question is
explicitly approximate.

This yields three separate observations:

- A scalar affine decoder of `J0` or `J1` measures decodability.
- The actual interchanged probability measures the proposed causal relation.
- The subset's weighted logit contribution can be compared with the appropriate
  log-cost plus a development-fitted additive offset as an explanatory diagnostic.

The candidate ranking gives actual intervention probability MSE priority over
both baseline-adjusted effect MSE and decoder NMSE. The latter two break
numerical ties, in that order, within `1e-12`. A good decoder cannot compensate
for a worse primary intervention score. The code reports raw and adjusted
errors separately, so subtracting an inaccurate base prediction cannot make
the primary error disappear.

## 3. Frozen ordinary training and discovery budgets

The full settings are explicit in `neural.defaults()` and are copied into the
F14 frozen configuration. Main settings are:

| Item | Frozen setting |
|---|---|
| Architecture | Four inputs, 32 unconstrained ReLU units, affine scalar logit |
| Arithmetic and RNG | NumPy 2.3.5, float64, explicit PCG64 with SeedSequence |
| Initialization | Hidden weights normal SD `sqrt(2/4)`, hidden biases zero; output weights normal SD `1/sqrt(32)`, output bias zero |
| Training | 3,000 online minibatches of 256 binary outcomes per model |
| Optimizer | Adam: learning rate .003, beta1 .9, beta2 .999, epsilon `1e-8` |
| Independent model replications | Seeds 1500401 through 1500405 |
| Corresponding evaluation streams | Seeds 1500491 through 1500495 |
| Post-hoc decoder fit data | 1,024 independent input rows per model |
| Selection pairs | 128 pairs per role per stratum |
| Candidate capacity | Exactly eight of 32 coordinates per role, proper subsets |
| Candidate search | 128 proposals per role per hypothesis per control |
| Decoder | Scalar affine, standardized hidden features, ridge `1e-6`; unpenalized intercept |
| Final intervention rows | 8,192 per role per stratum per model |
| Final observational task rows | 8,192 independent rows per model |

There are four high-level hypotheses and five search arms, hence 40 role
searches and 5,120 candidate evaluations/decoder fits per model. Every proposed
subset consumes its budget even if it duplicates an earlier proposal. There
is no open-ended search until a favorable candidate appears.

For each target and role, the guided proposal probabilities are a 25% uniform
mixture and 75% normalized absolute single-feature correlation with the
post-hoc target. Its first proposal is the eight most correlated coordinates;
the remaining proposals are weighted samples without replacement within each
subset. Each subset receives its own affine decoder fit and is scored on the
same selection-pair set. A selected index, the complete proposal pool, every
selection score, and the exact fit/evaluation counts are serialized.

The four comparison arms retain the same subset size, decoder family,
candidate count and scoring access:

| Arm | Alteration relative to the guided search |
|---|---|
| `random` | Uniform subsets from all 32 coordinates; same decoder and best-of-budget selection |
| `permuted_concept` | Joint cost-target rows permuted for proposal correlations and decoder fitting; same actual high-level intervention scoring |
| `shuffled_donor` | Independent incorrect donors from the same stratum donor marginal, including during candidate selection |
| `untrained` | Original initialization, same discovery procedure and budgets |

The random arm is a strong ordinary extraction comparator; if it finds an
equally valid abstraction, that may support the abstraction while failing to
support an advantage for the guided extraction method. The permuted-target arm
does not supply an exact permutation p-value: it is a prospectively defined
null search procedure evaluated by the protocol's bounded-error comparisons.

The `shuffled_donor` name follows F04, but the implementation generates fresh
independent incorrect donors. It does not permute a finite reused donor array:
such a permutation would couple rows and invalidate an iid rowwise confidence
calculation. Incorrect donors come from independently generated pairs under
the same stratum conditions, then are paired with the intended base rows.
The extra generation and hidden-forward work is reported.

## 4. Pair population and why all five strata are necessary

Each role/stratum has its own PCG64 stream. Rejection criteria depend on the
declared high-level task alone, never on the learned network's output. Base
and initial donor inputs are independent draws from the ordinary input domain.
For a constrained cost, the donor's corresponding cost input is solved
algebraically from its independently drawn eta; a donor is retained only if
both cost inputs remain in `[.5,2]`.

| Stratum | Prospective rejection conditions and purpose |
|---|---|
| `mixed_near` | Identity-model intervention probability within .04 of .5; at least .05 different from both base and donor optimal probabilities |
| `mixed_far` | Identity-model intervention probability at least .15 from .5; at least .05 different from both base and donor optimal probabilities |
| `preserve_other` | Preserve the other exact action cost; eta changes by at least .08 and the intervened cost by at least .1 |
| `equal_target` | Preserve the exact intervened action cost while changing eta by at least .08 and the other cost by at least .1 |
| `scale_separating` | Every one of the three nonconstant rival predictions differs from the identity prediction by at least .05; identity prediction differs from base by at least .05 and donor by at least .025 |

The preserving-other stratum makes the identity high-level prediction equal
to the donor's optimal output. It cannot by itself distinguish an intermediate
cost representation from a whole-layer transplant. The mixed strata explicitly
remove that degeneracy. In the equal-target stratum, the identity prediction
is the base optimum: nonzero observed swap effects can reveal a representation
of an input factor rather than the declared cost. No-change examples are not
the sole source of a favorable aggregate result.

Stratum labels are conditioned on the identity cost model. A rival's predicted
decision can lie at a different distance from its own boundary. That is a
counterfactual distinction being measured, not grounds to reselect pairs.

Sampling uses batches of 4,096 proposals with a cap of `4,000*n` proposals for
each accepted role/stratum sample of size `n`. Exhausting the cap is an explicit
generator failure; thresholds or sample counts are not relaxed afterward.
The output records proposal counts, accepted counts and input hashes. Existing
F04/C4 examples and every F14 development run remain development evidence.

## 5. Competing high-level scales and exact low-level gauges

The fixed positive family is

```
g_identity(x) = 1,
g_inv_eta(x) = 1/eta(x),
g_inv_one_minus_eta(x) = 1/(1-eta(x)),
g_inv_total_cost(x) = 1/(J0(x)+J1(x)).
```

Every member defines concepts `(g J0,g J1)` with exactly the same pointwise
optimal probability. Its one-role counterfactual generally changes. Each
member receives the same 128 proposals per role/control, decoder capacity,
and selection samples. The three-member alternative family has three times
the aggregate aligned-search budget of the identity alone; this is explicit.
The best rival is selected once by its discovery intervention score before
evaluation. All rival results are retained.

The inverse-total-cost member has concepts `(p*,1-p*)`. It directly challenges
an expected-cost interpretation with a normalized-probability explanation.
Before the final freeze, this member replaced the earlier development family's
`exp((x1+x2)/2)` member on conceptual grounds: the two inverse-eta members
already challenge eta-factor allocation, while inverse total cost challenges
the distinction between absolute expected costs and normalized classification
quantities. The four-hypothesis count and every search/training budget remain
unchanged. The earlier exponential-family development artifacts are preserved
and labeled superseded pilot-family evidence; their trained-network outcomes
were not used to choose the replacement.

Two comparisons answer different questions:

1. **The same selected identity subset, alternative targets.** Compare the
   actual same intervention with the different high-level predictions. This
   asks which declared counterfactual description better explains those chosen
   coordinates.
2. **Separately selected rival subsets.** Each rival may discover a different
   subset. Similar or better fit can mean that another partial decomposition
   is also available. It does not identify a unique absolute internal cost scale.

Only prospectively separating pairs support a scale-discrimination claim.
The code reports their exact count and fraction. The all-rival separation
stratum supplies a direct check of the population's intended discriminating
capacity. The minimum count, inferential treatment and ambiguity disposition
are fixed in the main protocol.

The final all-rival separating population is nonempty with strict interior
margins. For role 0, choose base `(x1,x2,cFN,cFP)=(-.4,-.4,1,1)` and donor
`(.6,.6,1.8,.6)`. The identity, inverse-eta, inverse-one-minus-eta and
inverse-total predictions are respectively `39/59`, `6/11`, `117/152` and
`65/111`. Each rival gap exceeds .05; the identity result also differs from
the base probability `2/5` and donor probability `39/46` by the required
amounts. Negating x and exchanging cFN/cFP gives a role-1 witness. Strict
inequalities at interior points imply a positive-volume accepted neighborhood.
A separate development-only acceptance diagnostic using no trained network
confirmed feasible rejection rates for the replacement family; it did not
choose the family by fitted-network performance.

A separate high-level global multiplier `g=2` leaves every declared
interchange prediction unchanged. Its decoders are multiplied by two without
refitting. This is distinct from the exact low-level gauge control:

```
W'_j = a_j W_pi(j), b'_j = a_j b_pi(j), v'_j = v_pi(j)/a_j, a_j>0.
```

New coordinates are selected by the inverse permutation, and each decoder
coefficient is divided by its matching positive scale. No decoder or subset
is fitted after this transport. The test compares observational probabilities,
single-role intervention probabilities, and decoded values on substituted
hidden states for each of the four aligned high-level hypotheses. Scales are
log-uniform on `[1/8,8]`; the numerical maximum-error
tolerance is `1e-10`. The corresponding algebraic identity is the F04 gauge
result; a finite floating-point check is separately reported.

## 6. Retained metrics and limits of a positive result

The evaluator retains per-role, per-stratum actual probability MAE/MSE/RMSE,
maximum error, decision agreement, original base error, adjusted-effect RMSE,
expected/observed effect magnitude, replaced- and untouched-concept decoder
NRMSE, whole-layer baseline, and no-swap baseline. Independent observational
rows give decoder NRMSE, log-contribution RMSE, task prediction error, weighted
expected BCE and actual expected decision regret. The maximum action-cost gap
on the declared domain is `11/8=1.375`, so normalized decision regret is bounded
by one. This normalization is recorded explicitly for bounded concentration.

Each matched comparison retains `n`, sum, sum of squares, mean improvement,
sample variance and extrema. The main protocol applies its fixed confidence
and multiplicity rule. These are finite-pilot statements conditional on the
trained models and fixed alignments; five selected training seeds do not
establish a distribution-free statement about arbitrary retraining.

The constructed duplicate-neuron witness from F04 W7 is retained. It has an
exact decoder of the duplicated feature while swapping the unused coordinate
has zero logit effect. Its purpose is to reject decodability as sufficient
methodological evidence. It is labeled constructed and is not included as a
successful ordinarily trained network.

The two selected subsets may overlap; the output records the overlap rather
than deleting or silently approving it. A separate two-donor composition
diagnostic executes role0-then-role1 and role1-then-role0. If they overlap,
their logit difference is

```
sum_{i in S0 intersect S1} v_i * (h_i(donor1)-h_i(donor0)).
```

Thus individually predictive swaps need not realize jointly independent
high-level variables. The primary permitted interpretation is a per-role
partial approximate intervention relation on this declared distribution.
The composition results are explicitly secondary and do not upgrade that
claim into a general constructive causal abstraction.

Good task predictions with poor interchange agreement reject this particular
bounded mechanistic hypothesis or its axis-aligned search budget. If the task
itself was not learned, intervention failure is separately classified as
uninterpretable for that intended question. A successful random search does
not imply that the hypothesis is false; a similarly successful competing g
does limit identification. No failure licenses logical supervision, additional
architecture, distributed alignment search, more seeds, or retuned criteria
on the same evaluation data.

## 7. Execution boundary and development record

`prepare_neural(config, seed)` trains and searches. It returns both saved
networks, alignment pools and scores, chosen rival, configuration hash,
selection-data hashes, resource counts and an artifact hash. It generates no
evaluation pairs. The F15 runner must durably save/hash its discovery artifact
before calling `evaluate_neural(prepared, config, evaluation_seed)`. The latter
verifies configuration and discovery hashes before generating examples, and
reports zero alignment refits. The runner owns the split-authorization gate.

`development_smoke()` uses only seeds 1400401 and 1400491, with 128 training
steps, 256 decoder-fit rows, eight candidates, 16 selection pairs/stratum,
32 diagnostic pairs/stratum and 256 task rows. It is an end-to-end development
check at explicitly reduced budgets. Its result contains
`held_out_evaluation_executed=false`. Validation tests use development seed
families only, including a four-step integration run; neither kind of check
is a final evaluation or an estimator of final benchmark performance.

One additional development integration used the complete 3,000-step training
and 128-candidate discovery budgets, then 512 diagnostic pairs per stratum and
8,192 ordinary task rows, exclusively on seeds 1400401/1400491. Its discovery
JSON and file SHA256 were written and reloaded before diagnostic generation.
The [neural-agent development record](../work_logs/F14_2026-10-04_S1/neural_agent/README.md)
preserves configuration, model, selected alignments, proposal pools, results,
resource measurements and the earlier smoke output.

After the prospective rival replacement, the full-budget development
preparation and 512-pair diagnostic were repeated with the normalized family,
under explicit one-thread settings before process startup. Separate
`normalized_*` artifacts preserve this current-family validation. Earlier
exponential-family records remain unchanged and are superseded pilot-family
evidence. This necessary generator/control revalidation did not change any
threshold, training budget or search budget.

The subsequent [full-count development diagnostic](../work_logs/F14_2026-10-04_S1/neural_agent/normalized_fullcount_summary.json)
used the final normalized family, full training/search budgets, **8,192 pairs
per role and stratum**, and 8,192 ordinary task rows on development seeds
1400401/1400491. Its exact configuration and prepared artifact were saved and
hashed before diagnostic generation. The [stable development assessment](../work_logs/F14_2026-10-04_S1/neural_agent/normalized_fullcount_assessment_stable.json)
exercises all 112 per-model confidence rows. Thus the full sample counts have
been validated in development; **all five prospective F15 model/evaluation
seed pairs and their final populations remain unexecuted**. No threshold or
budget was retuned from these results.

A separate [compiled-network search diagnostic](../work_logs/F14_2026-10-04_S1/neural_agent/compiled_search_summary.json)
applied the actual 128-candidate-per-role search without supplying the known
subsets to discovery. Both discovered and supplied-oracle subsets satisfy the
frozen absolute-MAE, conditional-base, derived effect-MAE and decision adequacy
components on this constructed example. This is positive search-sensitivity
evidence with zero ordinary training; it does not assess the full
matched-control/scale-specificity pilot criterion or establish search
completeness, exact coordinate identification, or learned internal structure.

The code records wall time and process CPU time separately. Process CPU may
exceed elapsed time when numerical libraries use multiple threads. Parameter
bytes exclude temporary arrays and optimizer state; they are not presented
as process peak memory. The final runner records environment and thread
metadata. Saved model parameters and alignments are the reproducible
intervention artifacts; same-seed bitwise equality across different NumPy,
BLAS or machine environments is not promised.
