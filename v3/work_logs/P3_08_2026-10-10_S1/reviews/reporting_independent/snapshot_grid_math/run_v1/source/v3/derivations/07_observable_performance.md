# Performance certificates from purchased mathematical answers

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Task **R-P3-B-A**, DEVELOPMENT. Companion to the
[paid selective-feedback construction](07_selective_feedback.md).

## 1. The service being certified

The expert-relative theorem bounds an expectation, but a deployed learner
cannot insert privately evaluated loss into its own report. This note asks
what it can certify using its immutable issued forecasts, the labels it paid
for, and the actual purchase probabilities. It provides a separate
concentration statement for that observation contract.

Retain the fixed deterministic query tape, binary answers, frozen block
weights, one checked purchase per block and current-action correction.
Write $`T=mB`$. The actual emitted dyadic forecast on a round is $`q_t`$;
its prospective action is an independent Bernoulli draw with that parameter.
For block $`k`$, its selected position $`J_k`$ has the actual conditional
probability $`\pi_{kt}>0`$. Use the deterministic reciprocal bound $`S=B`$
for uniform selection or $`S=2B`$ for the implemented ticket selector.

Conditional on preceding selections and settled feedback, the current block's
forecasts and answers are mathematically determined before its new selection.
The learner need not have computed every forecast then: the uniform rule may
issue them sequentially. Frozen weights and the exogenous tape make the
conditional argument valid. The adaptive selector additionally pays for the
whole current public block's advice before selecting. Neither service changes
its weights, selector, or bit-consumption schedule in response to sampled
terminal actions.

For the fixed answer $`y_t`$, define

```math
d_t=q_t+(1-2q_t)y_t,\qquad
 g_t=(q_t-y_t)^2.
```

Here $`d_t`$ is the conditional error probability of the prospective action;
$`g_t`$ is the loss of the immutable pre-purchase forecast. The two targets are

```math
V=\sum_k\sum_{t\ne J_k}d_t,\qquad
F=\sum_{t=1}^T g_t.
```

$`V`$ is the error mean conditional on the realized selector history, not the
unconditional mean over new episodes. Both targets can depend on preceding
selections through the learned forecasts. Let $`Z`$ be actual terminal errors.
On successful checked purchases those rounds contribute zero to $`Z`$.

All probability statements below assume fresh independent fair supplied bits.
The development evidence uses specified deterministic pseudorandom seeds; it
checks the formulas and records, and does not validate frequentist coverage.
The statements apply per declared policy and horizon. Reporting 23 diagnostic
arms does not give simultaneous coverage over those 23 arms.

## 2. Basic purchased-label estimators

The quantities

```math
U=\sum_k(\pi_{kJ_k}^{-1}-1)d_{kJ_k},\qquad
A=\sum_k\frac{g_{kJ_k}}{\pi_{kJ_k}}
```

are observable after checked purchased receipts. No unpurchased answer is
needed. For the first target, the block estimation error is

```math
D_k=\sum_t d_{kt}-\frac{d_{kJ_k}}{\pi_{kJ_k}}.
```

Its conditional mean is zero. Its conditional range is a translated set of
values $`-d_{kt}/\pi_{kt}`$, so its width is at most $`S`$, rather than
$`2S`$. The Brier block error has the same argument with $`g`$ in place of
$`d`$. Therefore, separately for either target,

```math
\Pr\!\left[V>U+S\sqrt{\frac{m\log(1/\delta)}2}\right]\le\delta,
\qquad
\Pr\!\left[F>A+S\sqrt{\frac{m\log(1/\delta)}2}\right]\le\delta. \tag{1}
```

These two basic errors need not coincide, so (1) alone does not provide their
joint coverage at the same error allowance.

### Conditional moment reconstruction

For a zero-mean random variable in an interval of width $`c`$, the standard
centered moment bound is $`\mathbb E e^{\lambda X}\le e^{\lambda^2c^2/8}`$.
[Hoeffding 1963](../literature/07_selective_feedback_sources.md#8-observable-performance-bounded-moment-inequality),
§4, equation 4.16, supplies this single-variable fact. Its convex endpoint
bound reduces the log moment to a two-point distribution; the second
log-moment derivative is its tilted Bernoulli variance, at most $`1/4`$.
Integration from zero gives the coefficient $`1/8`$.

Apply this argument conditionally at each block and iterate conditional
expectations. The joint moment is at most $`e^{m\lambda^2S^2/8}`$ even when
successive blocks depend on past purchased answers. Markov's inequality and
$`\lambda=4r/(mS^2)`$ yield $`e^{-2r^2/(mS^2)}`$, proving (1). No
independence of the adaptive block errors has been assumed.

Given the full selector history, the $`T-m`$ unbought action draws are
independent Bernoulli variables with means summing to $`V`$. This follows
from the policy's action-independent state and fixed bit schedule under the
fresh-bit premise. A second bound gives

```math
\Pr\!\left[Z>V+\sqrt{\frac{(T-m)\log(1/\delta_a)}2}\right]
\le\delta_a. \tag{2}
```

A union bound combines (1)'s action-mean statement with (2). If a future
policy lets sampled actions affect selection or state, this conditioning
argument needs its own replacement.

## 3. A public identity links the two unknown performances

For binary answers there is an exact identity

```math
v_t=q_t(1-q_t),\qquad g_t=d_t-v_t,
\qquad F-V=\sum_k d_{kJ_k}-\sum_t v_t. \tag{3}
```

The right side uses only issued forecasts and purchased answers. Thus $`F`$
and $`V`$ have **one shared unknown residual**, conditional on these public
records. An upper confidence statement for either target can transfer to the
other without another error-probability allocation. Sampling the known
$`v_t`$ term is unnecessary.

Center each binary loss by writing

```math
r_t=d_t-\tfrac12=(1-2q_t)(y_t-\tfrac12).
```

Use the two observable estimates

```math
U_c=\frac{T-m}{2}+\sum_k(\pi_{kJ_k}^{-1}-1)r_{kJ_k},
\qquad
A_c=\frac T2-\sum_t v_t+\sum_k\frac{r_{kJ_k}}{\pi_{kJ_k}}. \tag{4}
```

Direct subtraction proves the simultaneous equality

```math
V-U_c=F-A_c
=\sum_k\left(\sum_t r_{kt}-\frac{r_{kJ_k}}{\pi_{kJ_k}}\right). \tag{5}
```

For uniform selection, $`U_c=U`$ exactly. For adaptive selection they may
differ. There is no claim that centering always lowers the realized estimate
or every realized upper bound. It reduces a worst-case range allowance and
removes unnecessary sampling of a public component of Brier loss.

The publicly calculable block quantity

```math
C_k=\max_t\frac{|1-2q_{kt}|}{\pi_{kt}}\le S
```

bounds the width of the centered block error: each
$`r_{kt}/\pi_{kt}`$ lies in $`[-C_k/2,C_k/2]`$. The bound is predictable in
the mathematical filtration because all current forecasts are fixed before
selection. A sequential uniform implementation may finish calculating it at
the block boundary from the forecasts it has then issued. That is sufficient
for reporting the completed block; it creates no free advance computation.

## 4. Use the observed widths without optimizing after seeing them

Let $`Q_j=\sum_{k\le j}C_k^2`$. It is generally random. Substituting its
realized value into the square-root formula optimized for a deterministic
variance allowance is not justified by the preceding proof.

Instead fix $`\lambda>0`$ before inspecting labels. Conditional moments show
that

```math
M_j=\exp\!\left(\lambda\sum_{k\le j}D_k^c
                       -\frac{\lambda^2Q_j}{8}\right)
```

is a nonnegative supermartingale starting at one, where $`D_k^c`$ denotes
the centered error in (5). Consequently, with probability at least
$`1-\delta_s`$,

```math
\sum_{k\le j}D_k^c
\le\frac{\lambda Q_j}{8}+\frac{\log(1/\delta_s)}\lambda
\quad\hbox{for all }j\le m. \tag{6}
```

For completeness, stop at the first violation or at $`m`$. The finite
stopped process still has expectation at most one; on a violation its value
is above $`1/\delta_s`$. Markov's inequality gives (6). This bounded stopping
proof does not require an unbounded optional-stopping limit.

A particularly simple exact reporting rule uses

```math
R=S\left\lceil\sqrt{2m}\right\rceil,\qquad
\lambda=8/R,\qquad \delta_s=1/40,
\qquad \rho_j=Q_j/R+R/2. \tag{7}
```

The first six positive terms of the exponential series at four sum to more
than 40, so $`\log40<4`$. Formula (7) therefore safely dominates (6)'s radius.
Moreover $`Q_m\le mS^2\le R^2/2`$, hence $`\rho_m\le R`$. This improvement
uses one fixed predeclared $`\lambda`$. Selecting a favorable rate after
seeing the path would require a valid mixture or multiple-comparison
correction; it is not part of this result.

At the fixed final horizon also put

```math
r_a=\left\lceil\sqrt{2(T-m)}\right\rceil,
\qquad \delta_a=1/40.
```

The shared event (5)–(7) and action event (2) yield

```math
\Pr\!\left[
 V\le U_c+\rho_m,\quad
 F\le A_c+\rho_m,\quad
 Z\le U_c+\rho_m+r_a
\right]\ge19/20. \tag{8}
```

The mean and Brier statements alone share at least 39/40 coverage. Unlike the
two uncentered bounds, no third error allocation is needed: their deviations
are exactly equal. Only the mean/Brier sampling part is simultaneous over
block prefixes in (6). The joint terminal statement (8) remains fixed-end;
(2) has not supplied an anytime action-error boundary.

## 5. Deterministic clipping and finite arithmetic

Public forecasts also give deterministic upper bounds

```math
V\le\sum_{t\notin\{J_k\}}\max(q_t,1-q_t),\qquad
F\le\sum_t\max(q_t^2,(1-q_t)^2),\qquad Z\le T-m. \tag{9}
```

Each corresponding upper certificate may be clipped by (9). Negative
reported upper values can be replaced by zero; this only enlarges them.
The first cap is for a conditional mean, and cannot be substituted for the
pathwise cap on $`Z`$.

If every forecast equals one-half, $`r_t=0`$ and $`C_k=0`$: independently of
the answers, $`V=(T-m)/2`$ and $`F=T/4`$ exactly. In that case use these exact
identities; the generic fixed-rate boundary need not shrink to zero. Accurate
performance knowledge here conveys no additional information distinguishing
any two admitted binary answer assignments. This is a concrete separation
between knowing a procedure's loss and knowing mathematical truth.

Every forecast is dyadic. For uniform selection the basic action estimator
has denominator $`2^h`$ and the Brier estimator has denominator $`2^{2h}`$.
For ticket selection a common denominator multiplies these by $`B+1`$,
because ticket multiplicity is either 1 or $`B+1`$. Centering does not require
transcendental arithmetic. The squared-width sum has common denominator
$`2^{2h}(B+1)^2`$; the exact radius in (7) uses only integer square root and
rational arithmetic.

These are finite accumulators, but the largest admitted $`h=32`$ Brier and
width accumulations exceed 64 bits. A deployment must account for its wider
arithmetic, public-record reads, receipt checks, storage and output. The
present calculator is **offline analysis**, with an explicit public-only read
boundary, not an uncharged change to any measured learner. The controlled
policy, source registry, seed schedule and deployment invoices remain those
of the saved runs. A later executable integration must version and price
this additional reporting service.

## 6. Evidence and interpretation

The [first design](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate_design.md)
was saved before the basic 23-arm calculation. The
[centering design](../work_logs/R_P3_B_A_2026-10-09_S1/development/centered_certificate_design.md)
was separately saved before its extension. Both use only the 20 retained
uniform and 3 retained adaptive traces; no new policy, service, label or seed
run is needed. Certificate construction and comparison to existing private
evaluator scores are separate stages. Their complete rows and read manifests
are retained in the
[observable-certificate evidence](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/).

The new service supports Q4: a learner can form a rigorously scoped estimate
of its own episode performance from purchased feedback. Equation (3) also
makes a concrete Q5 information statement about two performance targets.
It neither certifies calibration nor turns the action probability into a
coherent mathematical-truth law. A useful performance certificate can reveal
that the method is poor; it cannot create economic superiority over the
error-free exact table. The negative ordinary comparisons remain decisive
for deployment on this family under the stated common unit tariff.

## 7. Two-sided reports can diagnose poor usefulness

An upper certificate can establish an acceptable performance ceiling. A lower
certificate can expose a procedure whose loss exceeds a declared reference.
The same centered construction supplies both, with an explicit larger error
allowance. Keep the fixed rate $`\lambda=8/R`$ and apply the conditional moment
argument to both signs with error $`1/80`$ per tail. Since
$`e^5>1097/12>80`$, define

```math
\rho_{\pm}=Q_m/R+5R/8,\qquad
 r_{a,\pm}=\left\lceil\sqrt{\left\lceil5(T-m)/2\right\rceil}\right\rceil.
 \tag{10}
```

The two sampling tails have total error at most $`1/40`$. The same event
bounds both $`V-U_c`$ and $`F-A_c`$ by absolute value, because they are equal.
The two conditional action tails also have total error at most $`1/40`$.
Thus, per declared episode at the fixed end,

```math
\Pr\!\left[
 |V-U_c|\le\rho_{\pm},\quad
 |F-A_c|\le\rho_{\pm},\quad
 |Z-U_c|\le\rho_{\pm}+r_{a,\pm}
\right]\ge19/20. \tag{11}
```

Here $`\rho_{\pm}\le9R/8`$, not necessarily $`R`$. This is a different
reporting rule from (8), not a free two-sided interpretation of that formula.
The shared sampling part has its fixed-rate prefix property; the complete
terminal statement remains fixed-end. A union over different arms, different
post-selected rates or additional procedures needs a separate allocation.

Intersect each interval with its public deterministic envelope. Besides (9),
use the corresponding minima of the two possible binary losses for $`V`$
and $`F`$, and zero for $`Z`$. If an intersection is empty, retain a confidence
conflict. Do not erase that row or attach ordinary valid better/worse labels
to the empty interval. The coverage statement permits failure paths.

Against the exact constant-half reference, a Brier lower endpoint greater
than $`T/4`$ indicates poorer forecast loss, while an action-mean upper
endpoint below $`(T-m)/2`$ indicates better remaining-action mean. These are
current-episode performance statements under the sampling theorem's premises.
They do not establish generalization to a future tape or a profitable change
of purchase policy. The [two-sided design](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/two_sided_design.md)
and its [additive clarification](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/two_sided_design_clarification.json)
precede the corresponding public-statistics calculation. The original design
and all earlier outputs remain unchanged.

## 8. Integration and value boundaries

### Hard answers and changed forecasts

A later hard-answer mechanism may improve a current action or a forecast for
which the sound answer is available before issuance. If the underlying
purchase and learner-update path remains unchanged, the base process's
upper loss bounds transfer to the improved outputs by pointwise domination,
provided its original statistics remain available and the extra work is paid.

That domination does not transfer lower bounds. Nor does it license inserting
selection-dependent overridden forecasts into the original conditional-moment
proof. If a label bought early in a block changes a later forecast in that
block, the whole forecast vector may no longer be fixed before the selector.
The algebraic identity (5) still holds if **all** targets and statistics are
consistently recomputed, but its zero-mean and predictable-width proof need
not hold. Old base statistics generally do not share (5) with the changed
targets. This is a substantive P3-08 interface obligation, not a retroactive
change to the reviewed cache-free policy.

### Actual cost and a future decision

Let the observed resource vector be $`\mathbf r`$, with declared prices
$`\boldsymbol\lambda`$ and terminal-error price $`c\ge0`$. The event bounding
$`Z`$ immediately also bounds the **same episode's realized all-in cost**:

```math
cZ+\boldsymbol\lambda\cdot\mathbf r
\le c\,\overline Z+\boldsymbol\lambda\cdot\mathbf r. \tag{12}
```

The realized bill can be random and correlated with the selector; adding
that same known bill pathwise requires no independence assumption. It is not
an estimate of the bill on a new episode, and conditional task mean plus a
realized resource bill must not be silently renamed an unconditional expected
policy cost. Repricing this fixed record also does not rerun a price-sensitive
selector. The new reporting calculator's own cost must be included if deployed.

A good current-episode estimate can therefore support accountability or a
specified stopping rule, while a forecast of future usefulness still needs
its own stability/model assumptions. The one-sided prefix sampling bound
licenses exactly its declared statistic, not arbitrary adaptive stopping of
the complete terminal-cost service. P3-07's independently scoped policy-profile
and acquisition results remain separate ways to address a future decision.

The constant-half example in §5 concerns information contributed by the
performance record. Where the received-information source admits two distinct
answer assignments, those assignments have identical constant-half performance.
If sound prior information already leaves a singleton, truth is identified
by that source; this example does not undo the identification.

## 9. Retained numerical evidence and reconstruction

The three public stages retain all 23 earlier episodes. Both the basic and
centered stages validate 49,600 public forecast rows and use 10,664 purchased
labels. They seal before separately invoked private-score comparison. The
two-sided stage reads only sealed public sufficient statistics and makes no
private comparison. All designs, calculator sources, reads, exact fractions,
seals and complete rows are retained in the [evidence directory](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/).

For the reference horizon $`T=3968`$, block size eight and finite-state
parameter 16, the centered one-sided formulas give the following. Numeric
upper endpoints are rounded upward to six decimals; exact rational values
remain in the public result.

| Policy | Basic radius $`R`$ | Centered radius $`\rho`$, rounded upward | Terminal-error upper endpoint | Immutable Brier upper endpoint |
|---|---:|---:|---:|---:|
| Uniform | 256 | 226.787325 | 2,012.253451 | 1,670.306538 |
| Adaptive tickets | 512 | 352.172803 | 2,208.940439 | 1,531.656728 |

The centered uppers improve on the basic uppers throughout this saved grid.
That is descriptive evidence, not a universal ordering of realized bounds:
an adaptive centered estimate can increase enough to offset its smaller
radius. The retained [independent review](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/literature_agent/observable_certificate_review.md)
gives an exact positive-probability counterexample. Some saved conditional
mean endpoints also benefit from the deterministic envelope; their total
improvement must not be attributed solely to a concentration radius.

The [two-sided grid](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/two_sided_grid.md)
has ten Brier lower endpoints above $`T/4`$: both uniform numerical states at
$`T=992`$ with blocks two and four, and at $`T=3968`$ with blocks two, four
and eight. No remaining-action interval gives a strict better/worse judgment
against $`(T-m)/2`$, and no intersection is empty. These flags use the
two-sided rule (10)–(11), not the one-sided table above. They reveal no action
advantage and do not suppress the unfavorable Brier results.

The principal independently reconstructed the [basic estimators](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/principal_basic_audit.json)
and [centered/two-sided statistics](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/principal_centered_audit.json)
directly from archived public traces and purchased receipts, without importing
the calculators or reading private scores. All 23 rows, shared corrections,
predictable widths, clipping envelopes and decision flags passed. The exact
shared correction also agrees with the separately retained private evaluator
difference on every row. This checks implementation and evidence correspondence;
the probabilistic theorem still depends on the declared fair-bit premises.

The [primary-source comparison](../literature/07_selective_feedback_sources.md#9-sampling-inference-and-the-fixed-rate-boundary-are-established-tools)
records the ordinary sampling and exponential-moment antecedents. The added
work is their finite paid-feedback integration and the binary shared-residual
interface, not a claim to a new generic confidence method.

## 10. A sufficient predictable hard-answer interface

The [supplementary composition analysis](../work_logs/R_P3_B_A_2026-10-09_S1/development/frozen_hard_answer_composition.md)
gives a mathematical route for using previously checked answers directly.
Freeze a sound, version-matched answer snapshot at block entry and keep it
fixed through the current selection. Let $`H_{kt}`$ indicate a covered query.
Emit the known correct zero/one forecast there and the base forecast elsewhere;
keep the underlying purchase/update path and random-bit schedule unchanged.
The resulting current vector is predictable, so the sampling proof applies
directly. Newly bought labels can enter this snapshot in a later block, while
still correcting their own current purchased action.

More generally, any predictable public center $`a_{kt}`$ can be subtracted
from conditional action loss if its all-round contribution is restored
exactly. For these hard snapshots, choose $`a_{kt}=(1-H_{kt})/2`$. Known zero
losses then contribute no unknown residual, and the block width becomes

```math
C'_k=\max_t\frac{(1-H_{kt})|1-2q_{kt}|}{\pi_{kt}}\le C_k.
```

The two new estimates still share one residual. This comparison of widths
requires the same base forecasts and actual propensities; it does not order
complete realized endpoints or newly rerun policies. Conditional action tails
may use the number of unbought, not-yet-hard-known positions, because that
count is fixed when conditioning on the complete action-independent selector
and snapshot history. This differs from optimizing a martingale rate using
its random observed width sum.

If all unbought positions are already hard-known, their mean and terminal
losses are exactly zero, while the complete Brier loss is exactly observable
as the sum of the bought positions' issued Brier losses. It need not be zero:
those purchased forecasts may have been unresolved when issued. If every
forecast was already hard-known at issuance, Brier loss is zero as well.

The result supplies a sufficient interface, not an executed cache or reporting
service. Snapshot construction, checking, retention and readout must be paid,
scope changes must invalidate stale answers, and the old base trace is not
relabelled as this new output. Keeping the original quota can also buy an
already known answer; reallocating that purchase would change the policy and
needs its own scope. The combined hard-state implementation remains P3-08.
