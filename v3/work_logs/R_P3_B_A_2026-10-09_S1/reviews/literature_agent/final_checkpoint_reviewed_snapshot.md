# P3-B supplement — paid selective-feedback recurrence

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Selected work: **R-P3-B-A**, attempt **R-P3-B-A-1**.

## Decision and relationship to the earlier gate

**The selected scientific question is answered at a restricted finite scope.**
The recurrence supplies a paid-feedback learning guarantee, a bounded numerical
implementation, observable performance certificates, and a precise economic
obstruction on the declared mathematical family. The accepted alternative was
an informative break-even regime **or** a defensible obstruction; the latter
is the result here. The [session record][session] and [actuals][actuals] record
the separately required Research90 and boundary verification.

This is an additive supplement to the published [P3-B PASS][historical], not
a replacement gate attempt. Its former statement that no all-issued
selective-feedback guarantee had been accepted remains a correct historical
statement. The [new 21-duty overlay][overlay] identifies the narrower gap now
closed and the integration obligations still open. P3-01–07, the original
gate, and the surviving defensive-forecasting addendum retain their evidence.

**P3-N01 is now SUPPORTED as a modest formal adaptation and implementation
synthesis**, under the author's stated contribution criterion. This is an
evaluator judgment about an explicit service and its consequential limits.
It claims neither a new general learning method nor superiority over ordinary
reasoning. The later P3-C author decision remains unattempted. R-P3-N01 remains
a separate, unselected recurrence.

## 1. What the new guarantee actually joins

The [main construction][construction] fixes an exogenous tape of binary
mathematical questions and a finite public expert library. It purchases one
checked answer per block. Forecasts and prospective randomized actions are
issued before their corresponding receipt; only purchased actions are
corrected. The learner updates at the block boundary and never receives
unbought labels. It pays for public advice, selection, checking, state
arithmetic, random bits, setup and output under the declared primitive tariff.

For uniform selection, write $`T=mB`$, $`K=\max(2,B-1)`$, and let $`L_*`$
be the loss of the best fixed expert on the entire exogenous tape. The finite
normalization uses $`M=N2^s`$ positive integer weight mass. With $`h`$ action
bits, the elementary potential bound yields

```math
\mathbb E Z\le
\left(1-\frac1B\right)\left(1+\frac1K\right)L_*
 +(B-1)K\log N
 +\frac{(B-1)mK}{2^s-1}
 +(T-m)2^{-h}.
```

Here $`Z`$ counts terminal errors after correcting bought actions. The fixed
expert comparator receives no such corrections. The exact-log refinement
tightens the first coefficient for binary losses without rerunning a policy.
There is also a separately derived bound for **all immutable issued Brier
losses**, including forecasts whose later actions were corrected. These are
expectation results under the supplied fair-bit model, not pathwise scores or
coverage conclusions from fixed pseudorandom seeds.

The adaptive construction permits unequal positive purchase probabilities and
charges for whole-block public advice before selection. Its loss estimate must
use the actual factor $`1/\pi-1`$ for the remaining-action objective. A concrete
ticket allocation preserves a probability floor and finite arithmetic. The
reviewed trusted `execute()` binds its actual selection; lower-level caller
interfaces require a truthful broker. Selection by disagreement and a fee
proxy is a heuristic, not a proved optimal value-of-computation policy.

This specificity is necessary. Retained counterexamples break the purported
bridge when an answer updates later forecasts in the same block, when the
query tape reacts to the sampled position, when greedy thresholding replaces
the randomized action, or when an adaptive update omits propensity correction.
The [selection-objective note][objective] further separates immediate
correction, future information and interval width. Even with a supplied
truth model equal to the forecast and exact fees, maximizing a benefit/fee
ratio need not minimize the exactly-one-query net-cost objective.

## 2. The economic answer is an obstruction

The development comparison was declared before execution and retains all
20 uniform learner arms, three adaptive arms and eight ordinary-control runs.
The following common example has 3,968 questions and block size eight. Costs
are the declared primitive units, not physical CPU time.

| Procedure | Recorded resource units | Terminal errors |
|---|---:|---:|
| Uniform learner, exact growing state, v1.1 | 2,935,898 | 1,703 |
| Uniform learner, 16-bit mass parameter, v1.1 | 1,039,110 | 1,702 |
| Adaptive ticket learner, 16-bit mass parameter | 1,382,703 | 1,754 |
| Ordinary cold exact table | 171,880 | 0 |

The finite-state change cuts the uniform learner's recorded bill by about
64.6%. Its maximum stored weight shrinks from 1,342 to 18 bits; intermediate
arithmetic has separately recorded, larger widths. Current uniform v1.2 adds
26 setup-registry units to the old invoice by an explicit source transfer.
The old v1.1 run is retained as such. [Complete uniform comparison][uniform];
[adaptive comparison][adaptive]

The source argument goes beyond these seeds. For successful current uniform
runs, the learner's cold bill exceeds the exact table's by at least
$`4908+11T+R_{\rm purchases}`$; the adaptive constant is 8,809. The table is
funded throughout the admitted horizon and has zero terminal errors. Thus the
learner cannot beat that table in terminal-answer cost under a common
nonnegative primitive price and error price. At zero prices the comparison
may be a tie. The analysis explicitly distinguishes sunk/shared registries
from waiving all learner setup while charging the table's full cold setup.

This conclusion is tied to the service. Category-specific resource prices
have mixed signed differences, and independently exported checkable evidence
would require equal delivery obligations for both methods. Neither extension
is silently decided by the common-tariff result. All six matched analytic
Brier-null comparisons are also unfavorable: the issued forecasts score worse
than constant one-half. A reduction relative to the uniform learner alone
would not establish useful mathematical forecasting.

## 3. A learner can assess its own observed episode

The [observable-performance companion][observable] asks a different question
from expert regret: what can the learner certify without access to privately
scored unbought answers? Let $`V`$ be remaining-action error conditional on the
realized selector history, and $`F`$ the all-issued Brier loss. For binary
answers, $`g_t=d_t-q_t(1-q_t)`$, and therefore

```math
F-V=\sum_{\rm purchased}d_t-\sum_{\rm all}q_t(1-q_t).
```

The right side is observable. Centered inverse-probability estimates for
$`V`$ and $`F`$ have **exactly the same unknown residual**. One conditional
exponential event can cover both. Its rate is chosen from the declared
horizon and probability bound before inspecting labels; it is not optimized
after seeing the random sum of squared widths. Adding an action tail yields
a joint fixed-end 95% guarantee for these two targets and terminal errors,
per declared episode under fresh fair bits. A separately allocated two-sided
version can identify poor performance as well as bound losses above.

Public construction and later private-score comparison were sealed in
separate processes. The principal independently reconstructed the estimators,
widths, deterministic envelopes and diagnostic flags directly from all
23 archived public traces and purchased-receipt records. This reused 10,664
paid labels across 49,600 forecast rows; it did not run another policy or
compute unbought truth. The [complete two-sided grid][grid] retains every row:

| Declared diagnostic | Number of rows |
|---|---:|
| Brier lower endpoint exceeds constant-half loss $`T/4`$ | 10 |
| Remaining-action upper endpoint is below the fair-action mean $`(T-m)/2`$ | 0 |
| Remaining-action lower endpoint is above that mean | 0 |
| Empty interval intersections | 0 |

These are development formula flags. They do not validate frequentist
coverage of deterministic seeds or supply simultaneous 95% coverage of all
23 displayed arms. The calculator is offline analysis; a live service must
pay for its wider arithmetic, reads, receipt checks, storage and output.

This is a material Q4 answer even when it reveals poor performance. Exact
knowledge of constant-half Brier and conditional-action loss, for example,
does not distinguish two answer assignments admitted by a source. It does
not undo truth already identified by a singleton source. The Q5 distinction
between information about performance and information about truth stays
explicit.

## 4. Accepted integration obligations

| Interface | Required treatment in P3-08 |
|---|---|
| Checked hard answers and statistical forecasts | Retain hard coordinates and version invalidation; leave old issued forecasts immutable. The new cache-free learner alone does not discharge U04. |
| Within-block hard-answer improvements | Retained-base upper bounds may transfer by pointwise domination with unchanged purchase/update paths and paid extra work. Lower bounds do not transfer. Recomputed changed forecasts need their own predictable sampling proof. |
| Selective feedback | Bind the actual selector probability and checked receipt. Preserve the exogenous tape, frozen-block and action-randomness assumptions or prove a replacement. |
| Failure and budget | Keep actual failed costs and the declared no-successful-answer outcome. An expectation theorem for successful checked purchases is not a guarantee for failed receipts. |
| Current and future usefulness | Same-episode realized cost may add the actual invoice to a terminal certificate pathwise. Future policy cost, changed prices that alter a selector, and arbitrary stopping need their respective models. |
| Ordinary alternatives | Admit the exact table, direct arithmetic, warm cache and ordinary learning methods with the same information, output service and prices. |

The full 21-duty mapping is in the [overlay][overlay]. Q4 improves most. Q1
has a stronger finite learning interface; Q2 retains its earlier finite
answer; Q3 affirmative comparative benefit remains open; Q5 gains the public
performance identity while retaining its source and calibration conditions.
The [contribution assessment][contribution] records object, delta, magnitude,
ordinary antecedents and remaining limits. Source comparisons expressly credit
product weights, label-efficient learning, queried best actions, disagreement
sampling, inverse-probability estimation and exponential concentration.

## 5. Recommendation at this boundary

**Proceed to P3-08 when the author selects it.** The paid-feedback gap no
longer requires a broad recurrence on this same easy family. Integration
should make the accepted contracts and ordinary fallback concrete. A more
discriminating final challenge must admit source-visible mathematical shortcuts
prospectively, rather than removing the successful ordinary control afterward.

Retain **option B, Research90**, before P3-09 if independently delivered
checkable evidence is to be a main contribution endpoint. Equal certificate
construction, export, editing, checking and storage could still resolve a
valuable Q3 comparison. **Option C, Research60**, remains a later opportunity
for counterpossible-policy robustness if that question becomes central.
Neither is selected here. P3-08 remains unstarted, P3-C/D unattempted, and no
final challenge is frozen or exposed.

[historical]: B_1.md
[overlay]: B_1_R_P3_B_A.v1.json
[construction]: ../derivations/07_selective_feedback.md
[observable]: ../derivations/07_observable_performance.md
[session]: ../work_logs/R_P3_B_A_2026-10-09_S1.md
[actuals]: ../work_logs/R_P3_B_A_2026-10-09_S1/actuals.json
[contribution]: ../work_logs/R_P3_B_A_2026-10-09_S1/contribution_assessment.md
[uniform]: ../work_logs/R_P3_B_A_2026-10-09_S1/development/service_comparison/analysis.md
[adaptive]: ../work_logs/R_P3_B_A_2026-10-09_S1/development/allocation_comparison/analysis.md
[grid]: ../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/two_sided_grid.md
[objective]: ../work_logs/R_P3_B_A_2026-10-09_S1/development/selection_objective_boundary.md
