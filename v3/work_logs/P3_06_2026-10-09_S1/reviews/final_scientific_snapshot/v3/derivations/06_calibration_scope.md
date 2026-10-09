# P3-06 — Calibration scope and the stronger ordinary comparison

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
Mathematical companions to [CF-1–CF-3](06_cost_forecast_refinement.md), with
explicit distinctions between implemented features, proposed extensions and
already available ordinary methods. No novelty or contribution-gate pass is
claimed.

## 1. What fixed tents do and do not say

The implemented scalar learner controls the residuals of a finite announced
set of continuous tents. Let $`E_j=\sum_t w_tb_j(p_t)(y_t-p_t)`$. Its
calibration block gives the joint inequality

```math
\sum_{j=0}^{m}E_j^2\le B_T/\beta^2.
```

For any fixed coefficient vector $`v`$, it follows that
$`|\sum_jv_jE_j|\le\|v\|_2\sqrt{B_T}/\beta`$. This is stronger than
summing separate coordinate bounds, but the test must belong to that finite
span. A small total-weight-normalized residual also leaves open large
conditional error on a sufficiently rare bin. Indicators of arbitrary
discontinuous sets do not become covered merely by taking more observations
with a fixed grid.

### CF-13: a fixed loss table can use the same calibration block

Fix a finite collection of binary affine loss rows throughout the episode.
At each grid center $`j/m`$, choose an optimal action with an announced tie
rule, and write its slope as $`d_j`$. The lower envelope of affine losses is
concave, so $`d_j`$ is nonincreasing. At
$`p=(j+r)/m`$, mix the adjacent center actions with probabilities $`1-r,r`$.
If the table's slope range is $`D`$, its forecast-cost excess over the best
action at $`p`$ satisfies

```math
0\le\mathrm{gap}(p)
\le\frac{r(1-r)(d_j-d_{j+1})}{m}\le\frac{D}{4m}.
```

To see the first upper bound, every other affine row is at least the selected
left cost at the left center and the selected right cost at the right center.
Linearity lower-bounds its interior value by the chord between those two
optimal endpoint costs. Subtracting that chord from the mixture cost gives
the displayed expression. The constant is attained by a crossing at a grid
endpoint with the tied endpoint action chosen appropriately: on the first
cell use $`c_A(y)=Dy`$ and $`c_B(y)=D/m`$, choosing A at zero and B at
$`1/m`$. At $`p=1/(2m)`$ the excess is $`D/(4m)`$. A unique crossing
can approach that value as it approaches the endpoint. For a two-action table, a crossing at the cell
midpoint instead has maximum excess $`D/(16m)`$ and zero excess exactly
at the crossing.

For a fixed comparator action $`a`$ with slope $`d_a`$, the exact regret
identity is

```math
G_{T,a}=\sum_t w_t\mathrm{gap}_a(p_t)
             +\sum_j(d_j-d_a)E_j,
```

where $`\mathrm{gap}_a`$ is the mixture's forecast-cost difference
from that comparator and can be negative. Therefore

```math
G_{T,a}\le\frac{DW_T}{4m}
 +\frac{\sqrt{\sum_j(d_j-d_a)^2}\sqrt{B_T}}{\beta}
\le\frac{DW_T}{4m}+\frac{D\sqrt{(m+1)B_T}}{\beta}.
```

This supports any fixed finite table, including more than two actions, without
adding action features. It is a separately derived readout; the production
action experiment uses CF-6's crossing-centered smoothing instead. Fixed
resolution gives a possible nonvanishing upper allowance after normalization,
not a proof of persistent realized error.

If tables vary with time, their slopes belong inside the time sum and the
fixed $`E_j`$ generally do not suffice. The
[independent comparison](../work_logs/P3_06_2026-10-09_S1/reviews/tent_action_comparison.md)
preserves an exact two-round example with zero tent residuals and positive
fixed-action regret under changing tables. CF-6's predictable action features
address that separate contract; they do not promise an empirical advantage.

## 2. CF-14: a finite-tent extension for every fixed continuous test

This extension is proved but not installed in the production learner, whose
configuration caps the grid at 64 bins. Assume unit weights, immediate full
feedback, a fixed finite expert library, fixed positive feature scales and
certified absolute root tolerance $`\delta`$. If the action block is used,
assume slope ranges at most $`D`$. Put

```math
C=(N\alpha^2+\beta^2+\gamma^2D^2)/4+2\delta.
```

Omit the action term when absent. The tent squared norm is at most one, so
every local prefix has $`B_n\le Cn`$ independently of the number of bins.
For a function with $`\|f\|_\infty\le1`$ and Lipschitz constant at most
$`L`$, linear interpolation $`f_m=\sum_jf(j/m)b_j`$ obeys
$`\|f-f_m\|_\infty\le L/(2m)`$. Hence

```math
\left|\sum_{t\le n}f(p_t)(y_t-p_t)\right|
\le\frac{\sqrt{m+1}\sqrt{Cn}}{\beta}+\frac{Ln}{2m}.
```

Restart the learner in epochs of lengths $`H_k=2^k`$ and use
$`m_k=\lceil H_k^{1/3}\rceil`$ throughout epoch $`k`$. Summing the
geometric series, including an unfinished current epoch, gives

```math
\sup_{\|f\|_\infty\le1,\;\mathrm{Lip}(f)\le L}
\left|\sum_{t\le T}f(p_t)(y_t-p_t)\right|
\le\frac{\sqrt{3C}/\beta+L/2}{1-2^{-2/3}}(T+1)^{2/3}.
```

The same restarts give expert regret at most
$`2\sqrt C\sqrt{T+1}/[\alpha(1-2^{-1/2})]`$. With the global dyadic
smoothing schedule $`\eta_t=c2^{-\lceil\log_2(t+1)\rceil}`$, mixed
regret to each fixed action is at most

```math
\frac{\sqrt C\sqrt{T+1}}{\gamma(1-2^{-1/2})}
 +\frac c{16}\lceil\log_2(T+1)\rceil.
```

The global time index matters: restarting the smoothing schedule in every
epoch incurs an additional logarithmic factor in that slack estimate.
Uniform approximation by piecewise-linear functions then gives vanishing
normalized residual for each fixed continuous function. It does not give
uniform convergence over all continuous tests with unbounded complexity, or
over arbitrary discontinuous selectors.

Under CF-11's fixed-denominator input contract, the active numerical state
and separate epoch summaries use $`O(T^{1/3}\log(T+1))`$ bits. Literal
retention of every full feature record uses
$`O(T^{4/3}\log(T+1))`$ bits. The summary must keep terms separately when
flattening them could introduce different odd denominators. These are
mathematical storage bounds for that representation, not measurements of
Python heap size. The complete prefix and bit arguments are in the
[independent epoch review](../work_logs/P3_06_2026-10-09_S1/reviews/growing_tent_epochs_review.md).

## 3. CF-15: the established Fermi–Sobolev method is stronger on this class

[Vovk's Working Paper 13](https://www.probabilityandfinance.com/articles/13.pdf),
§3, equations (7)–(10), already supplies the Fermi–Sobolev norm and kernel

```math
\|f\|_{\mathrm{FS}}^2=\left(\int_0^1 f\right)^2+\int_0^1(f')^2,
\qquad k(q,p)=\frac43+\frac{q^2+p^2}{2}-\max(q,p).
```

Its K29-star theorem gives simultaneous residual control for this function
space. A function in the above fixed Lipschitz ball has norm at most
$`\sqrt{1+L^2}`$. Because
$`p(1-p)k(p,p)\le13/48`$, the bare exact unweighted kernel construction
satisfies

```math
\sup_{\|f\|_\infty\le1,\;\mathrm{Lip}(f)\le L}
\left|\sum_{t\le T}f(p_t)(y_t-p_t)\right|
\le\sqrt{13(1+L^2)T/48}.
```

Thus the new epoch derivation is not the best available calibration exponent
for this class. The stronger square-root bound is an ordinary antecedent,
not a result first obtained by Value Logic. It changes the interpretation of
the proposed extension even though the extension remains correct.

The same direct-sum argument can add expert and smooth-action features.
With announced weights, its potential budget has the coarse upper bound

```math
B_T\le\frac{N\alpha^2+(4/3)\beta^2+\gamma^2D^2}{4}
                    \sum_t w_t^2+\sum_t A_t,
```

and the Lipschitz-ball residual is at most
$`\sqrt{1+L^2}\sqrt{B_T}/\beta`$. Approximate roots, large weights and
delayed copies retain their own actual allowances or transfer terms. This
does not attach the kernel bound to the already issued finite-tent reports,
and it does not import CF-12's different exponential expert guarantee.

### Finite computation and the limit of the comparison

For historical reports $`q_s`$ and signed coefficients
$`a_s=w_s(y_s-q_s)`$, retain $`A=\sum a_s`$,
$`Q_1=\sum a_sq_s`$, $`Q_2=\sum a_sq_s^2`$, and the two ordered prefix
sums up to the candidate $`p`$. Then

```math
\sum_s a_sk(q_s,p)
=\left(\frac43+\frac{p^2}{2}\right)A+\frac{Q_2}{2}
  -pA_{\le p}-(Q_1-Q_{1,\le p}).
```

This identity handles duplicate reports, endpoints and signed cancellation.
Although $`\|k_p-k_q\|_{\mathrm{FS}}^2=|p-q|`$ makes the feature map
only one-half Hölder in Hilbert norm, the finite-history scalar score is
Lipschitz. Its kernel contribution has the valid bound

```math
\mathrm{Lip}(S_{\mathrm{FS}})
\le w\beta^2\sum_s|a_s|+(11/6)w^2\beta^2.
```

An augmented balanced tree could support one kernel query or one admitted
update in $`O(\log n)`$ rational operations and comparisons, using
$`O(n)`$ stored rational records. This conditional data-structure analysis
is not an implementation, a cost bound for a complete forecast or a bit/CPU
cap. The [independent algebra probe](../work_logs/P3_06_2026-10-09_S1/reviews/fs_kernel_comparison_review.md)
passes 2,692 checks of the kernel, prefix identity, positive-definite feature
representation and exact derivative extrema. It deliberately uses list
scans and makes no runtime comparison.

The two calibration representations have different strengths. A particular
fine tent has an FS norm growing with its grid resolution, while the explicit
finite block controls its named coordinates directly. The FS result covers
an entire fixed Lipschitz ball but may retain a growing history support. Its
stronger exponent therefore does not establish domination of every named-bin
finite certificate or every resource budget.

## 4. A separate BRIA coverage obligation remains

The [BRIA sparse-coverage witness](../work_logs/P3_06_2026-10-09_S1/reviews/bria_sparse_coverage_witness.md)
shows that vanishing average squared-loss regret, continuous-test residuals,
fixed-action regret and reward overestimation do not imply BRIA's additional
test-history requirement. Its hypothesis outpromises on a sparse infinite
set. Every permitted matching-action test has zero empirical record, so none
can tend to negative infinity along the outpromise times.

BRIA's test set is restricted by action matching; it need not be a subset
of the outpromise set. The distinction is essential to the witness. It is
a nonimplication between stated criteria, not a generated trajectory of the
production forecaster. CF-12's stronger constant regret against its supplied
perfect expert excludes this particular logarithmic-loss tape, so the
witness is not claimed to refute that capital theorem. No implementation here
establishes the full BRIA hypothesis-class coverage condition or full logical
induction.

The later [CF-16 companion](06_bria_boundary.md) closes that specific
comparison gap with a different summable-error tape. Its Brier regret and
all actual-path centered capital components are uniformly bounded, its
decisions are optimal, and its always-kept promise still outpromises its
slightly conservative reward estimate forever. This stronger nonimplication
does not claim either implemented forecaster emits that tape or supplies its
outcome-uniform numerical allowances.
