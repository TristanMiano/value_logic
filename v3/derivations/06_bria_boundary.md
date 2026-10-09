# P3-06 — Constant forecast bounds still do not imply BRIA coverage

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
**CF-16:** an exact comparison of criteria, with a bounded development probe.
This strengthens the earlier sparse witness without claiming a trajectory of
either implemented forecaster or a new BRIA theorem.

## 1. Why the stronger witness is needed

The [earlier sparse witness](../work_logs/P3_06_2026-10-09_S1/reviews/bria_sparse_coverage_witness.md)
separates BRIA coverage from vanishing average forecast and action metrics.
Its cumulative Brier loss against a perfect supplied expert grows
logarithmically, so CF-12's constant-regret conclusion rules out that particular
tape. This leaves a narrower question: would constant regret and bounded
calibration/exposure capitals suffice to establish coverage?

They do not. The construction below has summable forecast errors, zero
decision regret and uniformly bounded capital components, but a correct
hypothesis outpromises its reward estimate forever.

The comparison uses [Oesterheld, Demski and Conitzer, *A Theory of Bounded
Inductive Rationality*](https://arxiv.org/pdf/2307.05068), Definitions 2–7.
Their §4.5 already observes that a hypothesis which always keeps its promise
can be rejected only finitely often by an agent covering it. The witness
instantiates that observation and checks compatibility with the stronger
forecast bounds. It is not an original discovery of the coverage requirement.

## 2. An efficiently representable forecast tape

For $`t\ge1`$, define

```math
k_t=\lceil\log_2(t+1)\rceil,\qquad
\epsilon_t=2^{-2k_t-3},\qquad p_t=1-\epsilon_t,\qquad y_t=1.
```

Here $`k_t`$ is computed by integer bit length, not an approximate logarithm.
Block $`k`$ contains $`2^{k-1}`$ rounds, so geometric summation gives

```math
\sum_{t\ge1}\epsilon_t=\frac1{16},\qquad
\sum_{t\ge1}\epsilon_t^2=\frac1{896}.
```

Every scalar is a dyadic rational with $`O(\log(t+1))`$ bits. The cumulative
error sums also have nested dyadic denominators of that order. This is a
representation statement for this explicit tape, not CF-11 applied to a
new production algorithm.

Let the expert library contain the constant expert one. The learner's
cumulative squared loss and its regret to that perfect expert are at most
$`1/896`$. Its regret to any other expert is no larger, because that expert's
squared loss is nonnegative. For every test with $`|f|\le1`$,

```math
\left|\sum_{t\le T}f(p_t)(y_t-p_t)\right|
\le\sum_{t\le T}\epsilon_t\le\frac1{16}.
```

This bound even allows an arbitrary bounded sequence of test coefficients;
no continuity or fixed-test assumption is needed for this special summable
error tape. It is not a universal forecasting guarantee.

## 3. Perfect decisions, slightly conservative reward estimates

Use two known affine cost rows

```math
c_0(y)=\frac{1-y}{2},\qquad c_1(y)=1-y,
```

and rewards $`r_i(y)=1-c_i(y)`$, all in $`[0,1]`$. Action zero minimizes
forecast cost for every $`p\in[0,1]`$, with a declared zero tie choice at
one. The constant choice of action zero is continuous as a decision exposure;
there is no hard-threshold discontinuity. Its estimated reward is

```math
e_t=r_0(p_t)=1-\epsilon_t/2<1.
```

Both actions actually yield reward one on this tape. The chosen action has
zero cumulative regret to each fixed action and to the realized outcome
oracle. Its cumulative reward overestimation is negative,
$`\sum_t(e_t-1)=-\sum_t\epsilon_t/2`$, so it satisfies BRIA's no-
overestimation condition. Its pointwise reward-estimation error tends to zero
and its total absolute error is bounded.

Now choose the single hypothesis that always recommends action zero and
promises reward one. It is a constant-time hypothesis. It strictly
outpromises $`e_t`$ on every round, so its rejection set is all positive
integers. Every subset of rounds is an admissible action-matching test set;
in particular, the full history is available for testing. But every test
increment is exactly

```math
r_t-h_t^e=1-1=0.
```

Every empirical record is therefore zero, and no such record tends to
negative infinity along the infinite rejection set. Coverage fails. The gap
is not inadequate realized reward, untested alternatives or sparse sampling.
It is the criterion's requirement that an always-kept promise cannot strictly
outpromise the estimate forever, even by a summable amount.

## 4. The exponential capitals remain bounded on this tape

This witness also survives the stronger metric comparison in CF-12. For any
real coefficient $`a_t`$ and real rate $`\lambda`$, completing the square
gives the pointwise inequality

```math
\lambda a_t\epsilon_t-\frac{(\lambda a_t)^2}{8}
=2\epsilon_t^2-\frac{(\lambda a_t-4\epsilon_t)^2}{8}
\le2\epsilon_t^2.
```

Summation bounds every centered calibration or action exponent by
$`2\sum_t\epsilon_t^2\le1/448`$. This applies to both calibration signs
and to any finite predictable coefficient sequence. For expert capitals with
unit weights and $`0<\kappa\le2`$, the Brier-regret exponent obeys the same
bound. Hence every component and every fixed positive-prior sum whose priors
sum to one satisfy

```math
K_T\le e^{1/448}<\frac{448}{447}.
```

The strict rational upper bound follows by comparing the exponential series
with the geometric series for $`1/(1-x)`$, at $`x=1/448`$. These are
bounded actual-path monitors. With the constant optimal action zero, the
two action exposure coefficients are zero and $`1/2`$, and its forecast slack
is zero. The general inequality also covers the original smoothed mixture's
coefficients; both actions have equal realized cost on this tape.

The distinction is essential: this calculation does **not** show
$`K_T\le1`$, certify both counterfactual next outcomes at every issue, or
bound the sum of CF-12's issued numerical allowances. It does not show either
production selection algorithm emits these forecasts. It proves that the
listed constant-regret, calibration, action and bounded-capital conclusions
alone do not imply BRIA coverage. A claim about the actual algorithm's full
coverage would need a separate proof or a separately verified trajectory.

### A report-transport consequence

The constant scalar tape $`p_t^*=1`$, with the same action and estimate one,
does cover this singleton hypothesis class and does not overestimate. The
new tape differs from it by total scalar displacement only $`1/16`$, with
per-round displacement of order $`t^{-2}`$. Thus even summable, vanishing
output error can destroy this exact coverage condition while leaving the
chosen actions and their realized rewards unchanged. CF-9's quantitative
Brier and continuous-test transport is therefore not a BRIA-coverage
transport theorem. A finite-precision BRIA claim needs its own analysis of
strict outpromise and numerical error.

## 5. Evidence and interpretation

The small [rational probe](../work_logs/P3_06_2026-10-09_S1/development/bria_constant_bound_v1/probe.py)
checks the dyadic blocks, prefix sums, regret/reward identities and completed-
square inequalities on the fixed 127-round fixture (20,588 checks, PASS).
The infinite result rests on
the displayed proof and [independent reconstruction](../work_logs/P3_06_2026-10-09_S1/reviews/final_scientific_integration_review.md),
not on enumeration. Its numerical result is recorded separately; no final
challenge or new forecaster is created.

BRIA and the forecast criteria ask different questions. This witness has
optimal realized decisions, so failure of its stronger coverage condition is
not evidence of a practical decision loss in this environment. Conversely,
excellent realized scores do not license claiming the full source criterion.
The Value Logic contribution obligation remains NOT YET SUPPORTED.
