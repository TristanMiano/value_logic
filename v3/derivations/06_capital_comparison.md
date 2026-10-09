# P3-06 — A stronger ordinary forecasting benchmark

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
This is a new P3-06 development branch. It preserves the original polynomial
forecaster and does not confer a contribution-gate result.

## 1. Why this comparison changes the interpretation

The surviving K29-star construction gives square-root finite-expert regret
together with continuous calibration and smooth action guarantees. That
expert rate is a property of its chosen potential, not an established price
that every simultaneous construction must pay. A finite sum of nonnegative
exponential forecasting capitals gives a stronger ordinary comparison.

The governing source is [Vovk, *Defensive forecasting for optimal prediction
with expert advice*, §§2–3, Lemmas 1–2 and Theorem 1](https://arxiv.org/pdf/0708.1503).
The expert exponential and defense of a continuous supermartingale are direct
inheritance. The particular tent and centered action components below are
explicit instantiations of that same mechanism. No new priority is asserted.
The [independent mathematical review](../work_logs/P3_06_2026-10-09_S1/reviews/exponential_capital_comparison.md)
reconstructs the complete proof and its quantifiers.

Fix a finite horizon $`H`$, a positive stake cap $`w_{\max}`$, a positive
action-slope-range cap $`D_{\max}`$, a finite supplied expert library and
the current tent family. Before choosing $`p_t`$, receive all current
expert values, the weight $`0\le w_t\le w_{\max}`$, the two affine action
rows and their positive smoothing width. The labels remain checked binary
answers; the actual answer need not have any stochastic law.

## 2. CF-12: one scalar defends three capital families

For any candidate $`p`$ and real $`h`$,

```math
(1-p)e^{-hp}+pe^{h(1-p)}\le e^{h^2/8}.
```

One proof differentiates $`\log(1-p+pe^h)-ph`$ twice: its second derivative
is at most $`1/4`$, and its value and first derivative vanish at zero.
Integrating twice proves the inequality. Consequently, for any predictable
continuous coefficient $`a_t(p)`$,

```math
\exp\left(\lambda a_t(p)(y-p)-\frac{\lambda^2a_t(p)^2}{8}\right)
```

has weighted average at most one under the two candidate weights $`1-p,p`$.
This is an algebraic test used to choose a forecast, not an assumption about
how mathematical truth is generated.

Use $`R^B_{T,i}=L_T-L_{T,i}`$ for squared-loss regret, $`E_{T,j}`$ for a
tent residual, and $`Z_{T,i}`$ for the **centered** action residual. Define

```math
V^C_{T,j}=\sum_t[w_tb_j(p_t)]^2,\qquad
Z_{T,i}=\sum_t w_t(\bar d_t(p_t)-d_{t,i})(y_t-p_t),
\qquad V^A_{T,i}=\sum_t[w_t(\bar d_t(p_t)-d_{t,i})]^2.
```

The capital components are

```math
\exp(\kappa R^B_{T,i}),\qquad
\exp(\mathord\pm\lambda_jE_{T,j}-\lambda_j^2V^C_{T,j}/8),\qquad
\exp(\rho_iZ_{T,i}-\rho_i^2V^A_{T,i}/8).
```

Here $`0<\kappa\le2/w_{\max}`$, and every $`\lambda_j,\rho_i`$ is
positive and fixed prospectively. For the expert term, the squared-loss
increment equals

```math
w\bigl((p-y)^2-(q-y)^2\bigr)
=2w(q-p)(y-p)-w(q-p)^2.
```

The exponential inequality bounds its conditional multiplier by
$`\exp((\kappa^2w^2/2-\kappa w)(q-p)^2)\le1`$. The other two
families use the centered inequality directly. The action exponent must
use $`Z`$: the actual mixed-action regret has a possible positive forecast
gap and satisfies only

```math
G_{T,i}\le Q_T+Z_{T,i},\qquad Q_T=\frac18\sum_t w_t\eta_t.
```

Take positive prior weights summing to one across all components, and let
$`K_t`$ be their weighted sum. Then $`K_0=1`$ and, for every candidate,

```math
(1-p)K_t(p,0)+pK_t(p,1)\le K_{t-1}.
```

Both outcome functions are continuous. If their difference
$`D_t(p)=K_t(p,1)-K_t(p,0)`$ is nonpositive at zero, choose zero; if it
is nonnegative at one, choose one. Otherwise an interior root makes the
two outcome values equal. In each case both next capitals are at most the
old capital. A forecast that directly satisfies both inequalities is equally
valid and need not be an exact difference root.

Each nonnegative component is bounded by the total capital. More generally,
if numerical work certifies $`K_T\le C_T`$, its prior $`\pi`$ gives

```math
R^B_{T,i}\le\frac{\log(C_T/\pi_i^B)}{\kappa},\qquad
|E_{T,j}|\le\frac{\log(C_T/\pi_j^C)}{\lambda_j}
                  +\frac{\lambda_jV^C_{T,j}}8,
```

```math
G_{T,i}\le Q_T+\frac{\log(C_T/\pi_i^A)}{\rho_i}
                      +\frac{\rho_iV^A_{T,i}}8.
```

The displayed two-sided calibration form uses equal positive/negative priors.
The variances here are squared one-step coefficient ranges; they are different
from the polynomial potential's $`p(1-p)\|\Phi\|^2`$ term.

Assigning one third of the prior to each family, uniformly within that family,
and using $`\kappa=2/w_{\max}`$ gives ideal expert regret
$`(w_{\max}/2)\log(3N)`$. Prospective horizon tuning of the other parameters
gives calibration $`w_{\max}\sqrt{H\log(6(m+1))/2}`$ and action regret
$`Q_H+w_{\max}D_{\max}\sqrt{H\log6/2}`$. These are simultaneous
ordinary bounds with constant expert regret at fixed caps and family size.

The executable benchmark uses a transparent rational approximation to that
rate scaling, not the optimal real-valued tuning:

```math
\lambda=\frac4{w_{\max}\lceil\sqrt H\rceil},\qquad
\rho=\frac4{w_{\max}D_{\max}\lceil\sqrt H\rceil}.
```

Its recorded finite certificates use these actual rates and observed squared
coefficient sums. No rate is optimized after inspecting those sums. The
ideal optimally tuned constants are not attached to this rational-rate run.

## 3. Certified numerical implementation

The [separate module](../checks/06_capital_forecasting.py), version
`p306-capital-enclosure-v1.1`, stores exact rational log-capital states.
It never needs to store an exact transcendental capital or an exact irrational
root. Positive Taylor sums, explicit remainders and outward rounding enclose
each exponential with rationals.

To enclose $`e^x`$, halve $`|x|`$ until the reduced argument $`z`$ lies
in $`[0,1]`$. If the Taylor sum includes terms through degree $`n`$, its
positive remainder is at most $`2/(n+1)!`$: subsequent term ratios are at
most $`1/(n+2)`$. Round the lower endpoint down and upper endpoint up to a
dyadic grid. Repeated outward-rounded squaring preserves enclosure. For
negative $`x`$, reciprocate the positive interval with reversed endpoints
and outward rounding. The exact zero argument returns the exact unit interval.

For logarithms of rational $`x\ge1`$, reduce to $`[1,2]`$ by powers of two.
With $`z=(x-1)/(x+1)`$, use the positive series

```math
\log x=2\sum_{k\ge0}\frac{z^{2k+1}}{2k+1}.
```

After $`n`$ terms its remainder is at most
$`2z^{2n+1}/((2n+1)(1-z^2))`$. The code allocates the error across the
reduced logarithm and the required multiples of $`\log2`$. This yields
an exact rational upper bound for the reported regret certificates.

At issue time let $`[L,U]`$ enclose the actual old capital and let
$`[L_y,U_y]`$ enclose the two possible next capitals. The recorded allowance is

```math
A_t^{\mathrm{cap}}=\max(0,U_0-L,U_1-L).
```

For either outcome, $`K'_y\le U_y\le L+A_t^{\mathrm{cap}}\le
K+A_t^{\mathrm{cap}}`$. Thus
$`C_T=1+\sum_tA_t^{\mathrm{cap}}`$ is a checked inductive upper bound,
including a forecast returned after numerical search exhaustion. This is
**not** the preserved polynomial core's allowance.

The numerical request divides a declared total budget $`1/65536`$ across
the horizon. If every issue meets its request, the sum is bounded by that
budget; otherwise the actual allowance is used. A bounded total allowance
preserves constant expert regret. Fixed positive allowance every round would
instead introduce a growing $`\log C_T`$ term. The module has explicit
root/precision caps and does not promise that every configuration meets its
requested tolerance. A certified return and a met numerical request are
separate statuses.

The [independent implementation review](../work_logs/P3_06_2026-10-09_S1/reviews/capital_enclosure_review.md)
verified the interval arguments, reconstructed the component histories and
tested both binary continuations. It preserved two different failures to
meet a request: insufficient enclosure precision despite true capital decrease,
and a zero-bisection return with genuine capital growth. Both had valid actual
allowances and `allowance_met=False`. It also preserved a cache-validation
alias defect in v1 and verified the v1.1 public-validation repair. An enclosing
rational result is not a constant-cost or hard-memory guarantee.

## 4. What the bounded comparison observed

The [comparison driver](../checks/06_capital_development.py) reused the first
32 issue ticks of each existing mathematical development case. Horizon, caps,
priors, rate rule and numerical budgets were fixed in the source before this
run. All methods were scored only on the same labels admitted by that cutoff.
The delayed case has 29 scored answers and three pending answers; labels
admitted later in the original longer run were excluded.

| Case | Capital Brier / weight | Plain polynomial | Decision polynomial | Brier AA | Exact arithmetic |
|---|---:|---:|---:|---:|---:|
| Recurring shortcuts | 0.026581 | 0.044651 | 0.286194 | 0.016892 | 0 |
| Nonshortcut null | 0.257374 | 0.292465 | 0.284791 | 0.258996 | 0 |
| Delayed cutoff | 0.224023 | 0.277980 | 0.290804 | 0.221570 | 0 |
| Varying stakes | 0.258997 | 0.259732 | 0.293796 | 0.259969 | 0 |

The capital method improves both polynomial variants' Brier loss in these
four checked prefixes. It does not dominate AA, and no learned method
matches exact arithmetic on correctness. These are later development
comparisons, not a final test, a natural query distribution or a practical
advantage claim.

All 128 issued capital forecasts met their numerical requests; their actual
capital allowances were zero. The unit-stake one-copy expert bound is
approximately 1.242454. It is approximately 9.939627 at stake cap eight,
and 39.758507 for the four-copy delayed cutoff. The latter is the sum of
four bounds, not a free single-copy guarantee. Full exact bounds and outcomes
are in the [saved report and manifest](../work_logs/P3_06_2026-10-09_S1/development/capital_comparison_v1/REPORT.md).

The finite calibration/action bounds can still be loose: at the delayed
cutoff the individual calibration upper bounds exceed total scored weight.
A stronger expert guarantee does not make every other finite certificate
useful. The four case issue-call totals ranged from about 0.47 to 1.13 seconds,
with 6,528–11,936 exponential enclosure calls per case. Those are observed
implementation costs. The earlier 128-query resource totals are not presented
as matched 32-query timings. Shared expert work and the mathematical answer
producer/checker retain the original harness's separate charges.

## 5. Boundaries retained

The [constant-bound BRIA witness](06_bria_boundary.md) shows that even
summable prediction errors and bounded actual-path expert/calibration/action
capital monitors do not imply BRIA's exact coverage condition. It does not
claim a generated trajectory of this forecaster or a bound on its issued
outcome-uniform allowances. The [unit-transport result](06_price_replay.md)
separately shows how the rate envelopes and cost/smoothing settings must
transform to preserve this implementation's scalar under a change of units.

The construction changes the forecasting algorithm. Its bounds do not certify
the old polynomial reports. Fixed calibration rates do not automatically give
an anytime vanishing rate past the announced horizon; restarts or additional
parameter components require their own accounting. Arbitrarily larger future
stakes violate the fixed expert-rate premise. Delayed copies sum their own
certificates on settled prefixes. Mixture loss, sampled action loss and an
outcome oracle remain distinct comparators.

This result improves the ordinary comparison that P3-06 must survive. It does
not establish full Logical Induction, BRIA coverage, a universal value carrier,
joint logical coherence, or a policy for buying computations. P3-N01 remains
**NOT YET SUPPORTED**; P3-07 and later gates remain separate tasks.
