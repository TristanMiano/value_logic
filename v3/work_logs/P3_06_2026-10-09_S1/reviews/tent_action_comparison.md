# P3-06: tent action readout and direct action features

Contributor: **ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer**.
October 9, 2026 UTC. Mathematical comparison only; no production method or
gate was added. Research effort is unmeasured and receives no principal-clock
credit. This strengthens the valid but loose constant in §7 of the earlier
[independent review](independent_proof_review.md).

## 1. Sharp finite-grid forecast-loss slack

Fix one finite affine binary action table $`c_a(y)=b_a+d_ay`$ for all rounds.
At every grid center $`x_j=j/m`$, select an optimal action $`a_j`$ under the
announced tie rule, and write $`d_j=d_{a_j}`$. At forecast $`p`$, score the
action mixture with probabilities $`b_j(p)`$, the existing triangular tents.
These are action-mixture weights; no randomized forecast is introduced.

Center optimality implies $`d_j\ge d_{j+1}`$: the selected left action is
no worse at the left center and the selected right action is no worse at the
right center, so subtracting the two comparisons gives the slope ordering.

Let $`p=x_j+r/m`$, $`0\le r\le1`$. Only the two adjacent tents are nonzero.
For any comparator action $`a`$, optimality at the endpoints gives

```math
c_{a_j}(p)-c_a(p)\le(d_j-d_a)\frac r m,
\qquad
c_{a_{j+1}}(p)-c_a(p)\le-(d_{j+1}-d_a)\frac{1-r}{m}.
```

Multiply by the two mixture probabilities and add. The comparator slope
cancels, producing the sharper local inequality

```math
\bar c(p,p)-c_a(p)
\le\frac{r(1-r)}m(d_j-d_{j+1}).
```

Thus with $`D=\max_a d_a-\min_a d_a`$,

```math
0\le\bar c(p,p)-\min_a c_a(p)
\le\frac{r(1-r)}m(d_j-d_{j+1})
\le\frac{\max_j(d_j-d_{j+1})}{4m}
\le\frac D{4m}.
```

The former $`D/(2m)`$ bound loses a factor of two by separately taking
absolute values before the comparator slopes cancel.

The new uniform constant is sharp. Pick a cell with right endpoint $`u`$,
and two nonnegative binary cost rows corresponding to
$`c_A(y)=Dy`$ and $`c_B(y)=Du`$. Choose $`B`$ at their tie $`p=u`$.
The left-center action is $`A`$, the right-center action is $`B`$, and at
the midpoint the mixture exceeds the optimal forecast cost by exactly
$`D/(4m)`$. Moving the crossing slightly inside the cell makes both center
optima unique and approaches the same constant.

## 2. The complete fixed-table action bound

Let $`E_j=\sum_t w_tb_j(p_t)(y_t-p_t)`$ and let the original scalar potential
satisfy $`\sum_jE_j^2\le B_T/\beta^2`$. For each fixed action $`a`$, define
$`\nu_{a,j}=d_j-d_a`$. The exact identity is

```math
G_{T,a}
=\sum_t w_t\bigl(\bar c(p_t,p_t)-c_a(p_t)\bigr)
 +\sum_j\nu_{a,j}E_j.
```

For each issued $`p_t`$, select its cell $`j_t`$ and fractional position
$`r_t`$. A useful computable slack is

```math
\Gamma_T=\sum_t\frac{w_tr_t(1-r_t)}m
             (d_{j_t}-d_{j_t+1}).
```

Then all fixed action indices simultaneously satisfy

```math
G_{T,a}\le\Gamma_T+
\frac{\|\nu_a\|_2\sqrt{B_T}}{\beta}
\le\frac{DW_T}{4m}+\frac{D\sqrt{(m+1)B_T}}{\beta},
\qquad W_T=\sum_t w_t.
```

One can retain the exact first sum or exact dot product when available;
the norm bound is an upper certificate. Since the inequality holds for every
fixed action, the comparator may be designated retrospectively as the best
fixed member of the announced action set. The outcome-optimal action changing
on every round is a different comparator.

The table may contain more than two actions. This readout uses the already
present tent features, so its mathematical guarantee does not require adding
action coordinates to the old forecasting state.

## 3. What changes with direct smooth-action features

| Question | Fixed-table tent readout | Direct two-action feature extension |
|---|---|---|
| Local forecast-loss slack | At most the occupied cell's slope drop times $`r(1-r)/m`$; worst case $`D/(4m)`$ | At most $`\eta_t/8`$, sharply |
| Residual term for comparator $`a`$ | $`\|\nu_a\|_2\sqrt{B_T}/\beta`$ | $`\sqrt{B_T^{\mathrm{ext}}}/\gamma`$ |
| Additional forecasting coordinates | None beyond the existing tents | Two |
| Number of actions | Any fixed finite table | Two in the implemented extension |
| Changing announced tables | Needs extra structure or features for their varying coefficients | Explicitly supported with stable action indices |
| Existing forecasts | Readout can use the existing scalar forecasts under the fixed-table contract | Adding features generally changes subsequent scalar forecasts |
| Main resource parameter | More centers increase dimension and feature Lipschitz constants | Smaller width increases action-feature Lipschitz constants |

For two actions whose crossing lies in a grid cell of width $`h=1/m`$,
write its fractional location as $`u\in[0,1]`$ and its slope difference as
$`g`$. The grid mixture ramps linearly across that whole cell. Its exact
maximum local excess is

```math
\frac{gh}{4}\max(u^2,(1-u)^2).
```

Indeed, on one side of the crossing its excess is $`ghr(u-r)`$ and on the
other it is $`gh(1-r)(r-u)`$. The two maxima give the formula. At a midpoint
crossing it is $`gh/16`$; near a grid endpoint it approaches $`gh/4`$.
The direct ramp centers on the actual crossing. With $`\eta=gh/2`$, it has
the same transition width and uniform slack $`gh/16`$. At a midpoint crossing
the two action rules coincide pointwise. This does not make their forecasters
or potential certificates identical.

For unit weights and fixed certified root tolerance, the coarse tent bound
has normalized order $`O(1/m+\sqrt{m/T})`$ at fixed table/feature scales.
Choosing $`m=\Theta(T^{1/3})`$ prospectively for a horizon-specific learner
balances this particular bound at $`O(T^{-1/3})`$. It is not an impossibility
rate for other grid methods, and changing $`m`$ in a running forecaster does
not inherit the old state. The prototype's finite bin-count cap also does
not implement an unrestricted growing-grid construction.

The direct feature bound instead allows normalized $`O(T^{-1/2})`$ plus
smoothing slack at bounded stakes/slopes, with fixed action dimension.
Its root effort and changed potential are still real costs. These are
comparisons between the proved bounds, not an empirical speed or performance
advantage over the strongest ordinary online decision method.

## 4. Why a changing table breaks the fixed coefficient combination

If the announced table and center-optimal actions change with $`t`$, the
exact correction becomes

```math
\sum_{t,j}w_tb_j(p_t)
  (d_{t,a_{t,j}}-d_{t,a})(y_t-p_t).
```

The coefficients now vary inside the sum over rounds. The old residual
$`E_j`$ stores no such weighting, so there need not be any fixed vector
$`\nu_a`$ whose dot product with those residuals equals this correction.
Even changing only intercepts can change which action is optimal at a center
and hence which slope appears. Common offsets preserve the differences;
arbitrary changes do not.

Here is an exact two-round witness with unit weights and $`m=2`$:

| Round | Issued $`p`$ | Outcome | Action 0 row | Action 1 row |
|---|---:|---:|---|---|
| 1 | $`1/2`$ | 0 | $`(3/2,3/2)`$ | $`(5/2,0)`$ |
| 2 | $`1/2`$ | 1 | $`(3/2,3/2)`$ | $`(0,5/2)`$ |

At the middle center, action 1 is uniquely optimal under both announced
forecast-cost tables: its forecast cost is $`5/4`$, versus $`3/2`$.
The tent readout therefore chooses action 1 on both rounds. It loses five,
while fixed action 0 loses three; action regret is two.

Every tent residual is zero: only the middle tent is occupied and the
signed errors are $`-1/2,+1/2`$. But its changing slope coefficient is
$`-5/2,+5/2`$, making the true residual correction $`5/2`$. The two forecast
gaps sum to $`-1/2`$, so the exact regret is $`-1/2+5/2=2`$.
No fixed linear combination of the zero old residuals recovers that term.
Repeating the pair gives linear fixed-action regret with exactly zero
continuous-bin residuals. This is a counterexample to the implication from
those statistics, not an asserted production-forecaster trace.

Direct action features work because their predictable varying slope
coefficient is included in the feature *before* choosing the forecast.
A fixed menu of additional coefficient-weighted tests could also be analyzed
by the same potential proof. Those features cannot be silently added to the
old scalar state after labels are known.

## 5. Narrow manuscript wording review

I inspected the newly integrated CF-7, CF-10 and CF-11 in
`v3/derivations/06_cost_forecast_refinement.md`. Their mathematical claims and
production-scope distinctions are supported. I requested these wording
clarifications before closure:

- CF-7 profile identities/dimension are fixed prospectively, and their
  per-round weights are known before choosing the report. CF-10 rows likewise
  arrive before report selection; merely preceding the answer is insufficient.
- The $`O(T^{-1/2})`$ CF-10 certificate rate needs fixed certified tolerance
  or another adequate quantitative allowance bound. The weaker little-oh
  allowance condition alone permits slower convergence.
- CF-11's fixed-denominator inputs are the expert values, stakes and action
  rows, with fixed positive rational scales. The separately specified varying
  dyadic smoothing width is excluded from that fixed-denominator condition.

CF-7's signed-coefficient/nonnegative-resulting-weight distinction and
uniform norm factor are correct. If normalized calibration services are
intended in its retention statement, per-profile total weights and bin
occupancies should also be retained; loss totals and signed residuals alone
support only their corresponding unnormalized menu scores.

No proof probes were repeated for this review. The proofs and rational witness
above are the evidence. **Signed:** ChatGPT (GPT-6 Astra Pro).
