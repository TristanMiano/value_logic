# F15 descriptive saved-model diagnostics

Contributor: **delegated ChatGPT (GPT-6 Astra Pro), F15 analysis audit**.

These are parameter calculations and descriptive functions of already saved statistics. No input population, network prediction, training, decoder fit, alignment selection, additional confidence interval or F16 reconstruction was performed. The frozen primary conclusions are unchanged.

The complete [machine record](model_diagnostics.json) includes exact rational neuron bounds, every search row, candidate coverage and input/script SHA256 hashes. The [script](model_diagnostics.py) uses only the Python standard library and preserves existing outputs by exclusive creation.

## 1. Discovery-selected versus saved final MSE

The selection score averages 640 discovery pairs per role; the saved final MSE below averages five equal strata of 8,192 pairs, totaling 40,960. Both concern the same discovery-selected subset. The following means average the ten fixed model/role rows descriptively; they are not new population estimates or confidence tests.

| Hypothesis | Arm | Mean discovery MSE | Mean final MSE | Final > discovery, /10 |
|---|---|---:|---:|---:|
| identity | aligned | 0.0025667 | 0.0025276 | 4 |
| identity | random | 0.0035938 | 0.0035196 | 4 |
| identity | permuted_concept | 0.0042753 | 0.0042445 | 5 |
| identity | shuffled_donor | 0.0182962 | 0.0183031 | 5 |
| identity | untrained | 0.0423001 | 0.0430679 | 7 |
| inv_eta | aligned | 0.0040142 | 0.0040232 | 5 |
| inv_eta | random | 0.0055446 | 0.0055280 | 5 |
| inv_eta | permuted_concept | 0.0057562 | 0.0057222 | 4 |
| inv_eta | shuffled_donor | 0.0226780 | 0.0228863 | 5 |
| inv_eta | untrained | 0.0408031 | 0.0417126 | 7 |
| inv_one_minus_eta | aligned | 0.0054774 | 0.0054663 | 5 |
| inv_one_minus_eta | random | 0.0077310 | 0.0076560 | 4 |
| inv_one_minus_eta | permuted_concept | 0.0072225 | 0.0072069 | 5 |
| inv_one_minus_eta | shuffled_donor | 0.0230476 | 0.0228771 | 4 |
| inv_one_minus_eta | untrained | 0.0447743 | 0.0452933 | 8 |
| inv_total_cost | aligned | 0.0014809 | 0.0015321 | 7 |
| inv_total_cost | random | 0.0016874 | 0.0017251 | 7 |
| inv_total_cost | permuted_concept | 0.0017747 | 0.0017373 | 4 |
| inv_total_cost | shuffled_donor | 0.0113794 | 0.0115496 | 6 |
| inv_total_cost | untrained | 0.0411059 | 0.0422602 | 7 |

Across all 200 hypothesis/arm/model/role rows, final MSE exceeds selected discovery MSE in 108 cases; identity-aligned does so in 4 of ten. The signs and sizes describe the saved run. They do not isolate discovery selection bias from finite-sample composition, identify the cause of unsupported intervention criteria, or justify additional fitting.

## 2. Actual candidate-pool coverage

The declared coordinate-subset space has **10,518,300** elements. A unique 128-candidate pool covers **0.001217%** of that space. Saved pools contain 127–128 unique subsets; 2 duplicate draws appear across the 25,600 charged candidate evaluations. Duplicate draws still consumed their frozen budget.

The union across all four hypotheses and five arms contains 1646–1662 distinct subsets per fixed model/role, from 2,560 charged proposals. Random pools are identical across hypotheses for the same model/role. Aligned and incorrect-donor pools are also identical within each hypothesis/model/role; their scoring donors differ. Shared pools support matched comparisons and should not be mistaken for independent exploration.

These fractions measure saved coordinate coverage only. They do not estimate the chance of a valid representation, establish search insufficiency as the cause of the result, or show that a larger search would succeed. Many different subsets could be redundant or equally poor.

## 3. Exact preactivation ranges from stored parameters

The frozen [input generator and MLP convention](../../experiments/neural.py) use raw inputs `(x1,x2,cFN,cFP)` on `[-1,1]² × [1/2,2]²`, a `4 × 32` input-weight array, and `h_j=max(sum_i x_i*w_ij+b_j,0)`. The [design](../../experiments/neural_design.md) explains the affine-output restriction. For each neuron, summing each coefficient's two endpoint products gives the exact affine minimum/maximum on this box. The calculation treats every stored binary64 coefficient as an exact rational number; displayed float endpoints round outward. It makes no claim about every implementation's final-bit BLAS rounding.

`Always zero` means the upper preactivation bound is nonpositive; `strictly active` means its lower bound is positive; `sign switching` means the interval spans zero. These are parameter properties over the full box, not empirical activation frequencies.

| Model seed | Network | Always zero | Strictly active | Sign switching | Boundary nonnegative |
|---|---|---:|---:|---:|---:|
| 1500401 | untrained | 2 | 1 | 29 | 0 |
| 1500401 | trained | 2 | 0 | 30 | 0 |
| 1500402 | untrained | 1 | 3 | 28 | 0 |
| 1500402 | trained | 2 | 1 | 29 | 0 |
| 1500403 | untrained | 1 | 0 | 31 | 0 |
| 1500403 | trained | 3 | 0 | 29 | 0 |
| 1500404 | untrained | 3 | 2 | 27 | 0 |
| 1500404 | trained | 3 | 1 | 28 | 0 |
| 1500405 | untrained | 2 | 2 | 28 | 0 |
| 1500405 | trained | 3 | 1 | 28 | 0 |

### Identity-aligned selected coordinates

| Evaluation seed | Role | Selected always-zero units | Selected strictly-active units | Selected sign-switching units |
|---|---:|---:|---:|---:|
| 1500491 | 0 | 0 | 0 | 8 |
| 1500491 | 1 | 1 | 0 | 7 |
| 1500492 | 0 | 0 | 1 | 7 |
| 1500492 | 1 | 0 | 0 | 8 |
| 1500493 | 0 | 1 | 0 | 7 |
| 1500493 | 1 | 0 | 0 | 8 |
| 1500494 | 0 | 0 | 1 | 7 |
| 1500494 | 1 | 0 | 0 | 8 |
| 1500495 | 0 | 0 | 1 | 7 |
| 1500495 | 1 | 0 | 0 | 8 |

Each role retains exactly eight coordinate slots, but a slot need not contribute a varying hidden feature throughout the declared domain. Always-zero units are constant in this stored mathematical network; strictly-active units contribute affine functions. Neither fact identifies cost semantics, establishes which units ordinary task behavior needs, or explains a final-error difference by itself. Every hypothesis/control's selected-unit classes and output weights are retained in JSON.

## 4. Selected-role overlaps

| Model seed | Identity overlap units | Overlap activation classes | Saved maximum composition-order probability difference |
|---|---|---|---:|
| 1500401 | none | {} | 0.000000000 |
| 1500402 | 30 | {"sign_switching": 1} | 0.087538567 |
| 1500403 | 13 | {"sign_switching": 1} | 0.071200176 |
| 1500404 | 8 | {"sign_switching": 1} | 0.000412094 |
| 1500405 | 1, 20 | {"sign_switching": 2} | 0.125664544 |

Overlap count alone is not an effect-size measure: activation ranges and output coefficients also matter. The composition figures here are copied from the frozen secondary diagnostic, with no new intervention. They retain the distinction between separate role relations and joint independently composable variables.

## Interpretation and accounting

These diagnostics make the saved models and finite search easier to inspect. They do not attribute the unsupported full neural criterion to optimization, capacity, inactive neurons, search coverage or discovery selection. Those explanations remain possible follow-up questions requiring a separately authorized experiment. The primary report's ordinary-learning, support-versus-falsification, control and scale dispositions remain unchanged.

This work is overlapping delegated F15 analysis, with zero additional principal engaged minutes claimed. Output files were created exclusively; exact input hashes and measured script compute time are in the JSON record.
