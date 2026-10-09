# P3-06 exploratory comparison: exponential defensive capital

Contributor: **ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer**.
October 9, 2026 UTC. This is a mathematical ordinary-method comparison, not a
production replacement or claim of exact-rational implementation. Subagent
effort is unmeasured and receives zero principal-clock credit. No P3-07 work
or gate was started.

**Disposition:** the proposed finite capital sum is valid and materially
strengthens the ordinary benchmark. Under an announced bounded horizon/stake
envelope it simultaneously gives constant finite-expert squared-loss regret,
finite continuous-test calibration, and smooth fixed-action regret. Numerical
capital allowances, prospective tuning and the distinction between centered
action residual and actual action regret are essential.

## 1. Input and parameter contract

Fix a finite horizon $`H`$, $`N`$ supplied experts, $`m+1`$ continuous tents,
and two announced affine action rows per round. All current expert values,
weights, action rows and positive smoothing widths are available before the
issued scalar $`p_t`$ is chosen. One sequential copy uses only previously
admitted outcomes. Assume a known positive upper weight bound $`w_{\max}`$
through that horizon, with $`0\le w_t\le w_{\max}`$, binary outcomes and
expert reports in $`[0,1]`$. A positive slope-range envelope $`D_{\max}`$ is useful
for an explicit action rate; the exact finite certificate can instead retain
the actual sums of squared coefficients.

Use $`\kappa`$ for the expert capital parameter, reserving $`\eta_t`$ for the
already defined smooth-action width. Fix $`0<\kappa\le2/w_{\max}`$. Each
calibration or action capital parameter is positive and fixed prospectively
within its component. Finite positive priors also remain fixed and sum to one.
The horizon, envelopes and priors may determine these parameters before play.

## 2. The centered exponential inequality

For fixed $`p\in[0,1]`$ and real $`h`$,

```math
(1-p)e^{-hp}+pe^{h(1-p)}\le e^{h^2/8}.
```

A self-contained verification defines the logarithm of the left side as
$`f(h)=\log(1-p+pe^h)-ph`$. It satisfies $`f(0)=f'(0)=0`$ and
$`f''(h)=q_h(1-q_h)\le1/4`$, with
$`q_h=pe^h/(1-p+pe^h)`$. Twice integrating gives the result; the endpoint
cases $`p=0,1`$ are immediate.

Consequently, for every predictable continuous real coefficient $`a_t(p)`$,
the one-round multiplier

```math
\exp\left(\lambda a_t(p)(y-p)-\frac{\lambda^2a_t(p)^2}{8}\right)
```

has expectation at most one under the two weights $`1-p,p`$. This is a
condition checked at a candidate report. It is not an assumption that the
actual mathematical answer is sampled from that distribution.

## 3. Three component families

### 3.1 Expert regret

Let $`R^B_{T,i}=\sum_t w_t((p_t-y_t)^2-(q_{t,i}-y_t)^2)`$. Writing
$`x=q-p`$, its increment is

```math
w\bigl((p-y)^2-(q-y)^2\bigr)=2wx(y-p)-wx^2.
```

Applying the centered inequality with $`h=2\kappa wx`$ bounds the expectation
of its exponential multiplier by

```math
\exp\left((\kappa^2w^2/2-\kappa w)x^2\right)\le1,
```

because $`\kappa w\le2`$. Therefore
$`\exp(\kappa R^B_{T,i})`$ is a forecast-continuous supermartingale.
The weight bound is needed for this fixed parameter; arbitrary larger future
weights cannot silently retain it.

### 3.2 Calibration

Put

```math
E_{T,j}=\sum_t w_tb_j(p_t)(y_t-p_t),
\qquad V^C_{T,j}=\sum_t[w_tb_j(p_t)]^2.
```

The two components

```math
\exp\left(\mathord\pm\lambda_j E_{T,j}
                 -\lambda_j^2V^C_{T,j}/8\right)
```

are supermartingales by taking $`a_t(p)=w_tb_j(p)`$ and both parameter signs.
These test the same issued scalar, with the same finite continuous selection
scope as the polynomial construction.

### 3.3 Smooth action residuals

Let $`s_t(p)`$ be the rational clipped smooth action rule and
$`\bar d_t(p)=d_{t,0}+s_t(p)(d_{t,1}-d_{t,0})`$. Define the **centered**
action residual and its squared-coefficient sum by

```math
Z_{T,i}=\sum_t w_t(\bar d_t(p_t)-d_{t,i})(y_t-p_t),
\qquad
V^A_{T,i}=\sum_t[w_t(\bar d_t(p_t)-d_{t,i})]^2.
```

Then
$`\exp(\rho_iZ_{T,i}-\rho_i^2V^A_{T,i}/8)`$ is another continuous
supermartingale. The coefficient can have either sign; the centered
inequality uses its squared range length.

The actual signed mixed-action regret $`G_{T,i}`$ is a different quantity:

```math
G_{T,i}\le Q_T+Z_{T,i},\qquad Q_T=\frac18\sum_t w_t\eta_t.
```

An exponential of actual action regret without subtracting its forecast
slack need not be a supermartingale. One may use the centered expression
above, or the smaller component based on $`G_{T,i}-Q_T`$.

The scored loss is the mixture of the two announced action losses. If an
actual action is sampled from that mixture, its sampled-path fluctuation is
a separate question, and the mathematical label and admitted inclusion must
not be changed by that sample. The capital argument itself makes no claim
that a realized sampled loss equals its mixture loss.

## 4. One scalar controls the finite sum

Let $`K_t`$ be the prior-weighted sum of the preceding $`N+2(m+1)+2`$
nonnegative components. It starts at one. For the current history and a
candidate $`p`$, each component satisfies the preceding one-step inequality,
so their sum satisfies

```math
(1-p)K_t(p,0)+pK_t(p,1)\le K_{t-1}.
```

Both outcome functions are continuous in $`p`$. Define
$`D_t(p)=K_t(p,1)-K_t(p,0)`$. Choose zero if $`D_t(0)\le0`$, and otherwise
choose one if $`D_t(1)\ge0`$. The endpoint with greater weight in the
displayed average then dominates the other outcome value, so both are at
most $`K_{t-1}`$.

If neither endpoint condition holds, continuity gives an interior root.
At that root the two outcome capitals are equal; their average inequality
again bounds both by $`K_{t-1}`$. Induction gives $`K_T\le1`$ along every
actual binary path. No true-outcome probability model is required.

This is a different forecasting rule from the polynomial K29-star score.
The resulting guarantees cannot be attached to forecasts generated by the
old rule merely by calculating these capital values afterward.

## 5. Finite certificates and horizon tuning

Each component is at most the total capital. If its prior is $`\pi`$, taking
logarithms gives

```math
R^B_{T,i}\le\frac{\log(1/\pi_i^B)}{\kappa},
```

```math
E_{T,j}\le\frac{\log(1/\pi_j^+)}{\lambda_j}
                    +\frac{\lambda_jV^C_{T,j}}8,
\qquad
-E_{T,j}\le\frac{\log(1/\pi_j^-)}{\lambda_j}
                    +\frac{\lambda_jV^C_{T,j}}8,
```

```math
G_{T,i}\le Q_T+\frac{\log(1/\pi_i^A)}{\rho_i}
                      +\frac{\rho_iV^A_{T,i}}8.
```

These identities bound each fixed component simultaneously. For a known
positive envelope $`U\ge V_H`$, setting
$`\lambda=\sqrt{8\log(1/\pi)/U}`$ gives the endpoint bound
$`\sqrt{U\log(1/\pi)/2}`$. This parameter is chosen from a prospective
envelope. Minimizing the displayed expression afterward using the observed
$`V_H`$ does not give a guarantee for the forecast sequence generated with
a different parameter. A declared collection of parameter components would
be a different legitimate approach.

For example, allocate one third of the prior to each component family,
uniformly inside the family, and use $`\kappa=2/w_{\max}`$,
$`U_C=Hw_{\max}^2`$, $`U_A=Hw_{\max}^2D_{\max}^2`$. At the declared horizon,

```math
R^B_{H,i}\le\frac{w_{\max}}2\log(3N),
\qquad
|E_{H,j}|\le w_{\max}
\sqrt{\frac H2\log(6(m+1))},
```

```math
G_{H,i}\le Q_H+w_{\max}D_{\max}
\sqrt{\frac H2\log6}.
```

Zero coefficient envelopes yield zero residuals and can be handled directly.
For fixed finite families and bounded stakes/slopes these are constant expert
regret, $`O(\sqrt H)`$ calibration residuals and $`O(\sqrt H)+Q_H`$ action
regret. The horizon-tuned calibration/action bounds are not automatically
anytime $`O(\sqrt T)`$ bounds beyond the declared horizon. They also do not
remove rare-bin normalization or missing-label coverage requirements.

## 6. Numerical capital allowances

The exact-root construction is a real-valued mathematical benchmark. A
computable implementation could instead certify
$`K_t\le K_{t-1}+\epsilon_t`$, with known nonnegative capital allowances.
Then

```math
K_T\le C_T:=1+\sum_{t\le T}\epsilon_t,
```

and every certificate above replaces $`\log(1/\pi)`$ by
$`\log(C_T/\pi)`$. A bounded cumulative allowance preserves a constant
expert bound. Fixed absolute per-round allowance generally changes it to
$`O(\log T)`$, and also changes the calibration/action constants or tuning.
One finite-horizon option is a prospectively allocated total error budget.

An approximate difference root is enough because the average inequality
implies

```math
\max_yK_t(p,y)\le K_{t-1}
 +\max\{(1-p)D_t(p),-pD_t(p)\}
\le K_{t-1}+|D_t(p)|.
```

Thus a certified $`|D_t(p)|\le\epsilon_t`$ yields the required capital
allowance. Numerical evaluation uncertainty must also be included in that
certificate. The stored polynomial K29 potential allowance is not this new
capital allowance; its formula cannot be reused unchanged.

Rational inputs do not make the exponential capital values or exact root
rational. Certified exponential enclosures, a sound root/sign procedure,
precision/work bounds and retained parameter/error records would be needed.
Continuity proves existence, not a fixed-cost exact comparison primitive.
The original $`06_defensive_forecasting.py`$ module implements the rational
polynomial potential. This abstract review does not inspect the subsequently
developed $`06_capital_forecasting.py`$ implementation; its executable
enclosures, API and computational allowance need their own independent
audit. No new code or proof probe was run for this comparison.

For delayed feedback, separate-copy reasoning would add the corresponding
per-copy bounds and costs; the new constant expert certificate does not
magically become independent of the number of copies. No paid acquisition
policy or unseen-population conclusion is supplied here.

## 7. Source inheritance and project consequence

I inspected [Vovk, *Defensive forecasting for optimal prediction with expert
advice*, arXiv:0708.1503v1](https://arxiv.org/pdf/0708.1503): §2 equation (2)
and Lemma 1 state the forecast-continuous supermartingale mechanism; §3
Lemma 2 proves the quadratic exponential for parameter at most two; its
Theorem 1 combines expert components for constant quadratic-loss regret.
Our bounded-weight expert argument applies that one-step calculation with
parameter $`\kappa w_t`$. The tent and centered smooth-action components and
their finite prior allocation are the explicit instantiations reconstructed
above. The binary difference-root proof is a direct specialization of the
same mechanism.

This is a strong ordinary benchmark and an adaptation of an established
method. It improves the currently established worst-case expert certificate
for the rational polynomial prototype. That comparison does not prove the
old prototype could never admit a stronger analysis, establish practical
dominance of exponentials under equal computation, or support a priority
claim. The old method retains a concrete exact-rational implementation and
checked finite resource statements. Mathematical approval of the exponential
alternative does not approve its separately developed implementation or
computational allowance account.

**Signed:** ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer.
