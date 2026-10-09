# Independent reconstruction of the bounded-state weight normalization

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Separate same-model, nonblind mathematical review for R-P3-B-A. The root
supplied the proposed normalization rule; this note independently reconstructs
its guarantee. No principal time credit and no root-source edits.

**Verdict: the proposed normalization is valid with the stated additional
loss allowance.** It replaces the original linear-in-horizon integer bit
growth by a chosen finite state precision. Its nonzero approximation allowance
is consequential and cannot be omitted, even when one expert is perfect.

## 1. Integer map and retained probability mass

Fix $`N\geq2`$, an integer precision $`s\geq1`$, and

```math
M=N2^s,\qquad \delta=N/M=2^{-s},\qquad K\geq2,\qquad\eta=1/K.
```

Maintain positive integer weights with $`\sum_iw_i=M`$. Initialize all
weights to $`2^s`$, giving the uniform prior. Given the selected binary
expert-loss vector $`\ell\in\{0,1\}^N`$, calculate

```math
v_i=w_i(K-\ell_i),\qquad
V=\sum_iv_i,\qquad
r_i=v_i/V.
```

Thus $`r`$ is exactly the unrounded normalized product-weights posterior.
Define

```math
u_i=1+\left\lfloor\frac{(M-N)v_i}{V}\right\rfloor,
\qquad R=M-\sum_iu_i,
\qquad w'_i=u_i+1\{i<R\},
```

where indices are zero-based and the last term allocates the remainder to
the first $`R`$ fixed indices. No sorting of fractional remainders is needed.

Because $`\sum_i(M-N)r_i=M-N`$ is an integer,

```math
R=\sum_i\left((M-N)r_i-\lfloor(M-N)r_i\rfloor\right)
```

is an integer satisfying $`0\leq R<N`$. Therefore the final weights are
positive and sum exactly to $`M`$. Moreover,

```math
\frac{w'_i}{M}
 \geq\frac{1+\lfloor(M-N)r_i\rfloor}{M}
 \geq(1-\delta)r_i. \tag{R}
```

The first inequality is unaffected by which fixed indices receive the
remainder. This is the precise one-sided condition needed for the proof;
nearest-probability rounding is unnecessary. It also implies that the new
distribution is a mixture of $`r`$ with total redistributed mass at most
$`\delta`$.

The main formula requires $`s\geq1`$: at $`s=0`$ the multiplicative
retention lower bound is zero and its logarithmic penalty is infinite.
For $`N=1`$, no learning normalization is needed and the single distribution
is exact; treating that trivial case separately avoids an artificial penalty.

## 2. The additional potential term

At block $`k`$, let $`p_{k,i}=w_{k,i}/M`$ and
$`z_k=\langle p_k,X_k\rangle`$, where $`X_k`$ is the selected loss vector.
The unrounded posterior satisfies

```math
r_{k,i}=\frac{p_{k,i}(1-\eta X_{k,i})}{1-\eta z_k}.
```

Applying (R), taking logarithms and summing gives, for every fixed expert,

```math
\log p_{m+1,i}-\log p_{1,i}
 \geq m\log(1-\delta)
    +\sum_k\log(1-\eta X_{k,i})
    -\sum_k\log(1-\eta z_k).
```

Since $`p_{1,i}=1/N`$ and $`p_{m+1,i}\leq1`$,

```math
\sum_k\log(1-\eta z_k)
 \geq-\log N+m\log(1-\delta)
       +\sum_k\log(1-\eta X_{k,i}).
```

The same elementary bounds used in the original proof,
$`\log(1-\eta z)\leq-\eta z`$ and
$`\log(1-\eta x)\geq-\eta x-\eta^2x^2`$ for $`\eta\leq1/2`$,
therefore yield

```math
\sum_k z_k
 \leq \sum_kX_{k,i}+\eta\sum_kX_{k,i}^2
       +\frac{\log N}{\eta}
       +\frac{m}{\eta}\log\frac1{1-\delta}. \tag{P-R}
```

The derivation is pathwise in the selected losses. It does not assume that
rounding errors have zero mean, so the deterministic index rule introduces
no missing centering premise.

For a fixed loss tape and the same block chronology as the original review,
multiply the expectation of (P-R) by $`b-1`$. With
$`K=\max(2,b-1)`$, the paid-action cancellation still applies. The all-in
result becomes

```math
\mathbb E[J_T]
 \leq L_*+(b-1)K\log N
       +(b-1)mK\log\frac1{1-2^{-s}}
       +mf+\mathbb E[O_T]+S+\rho_T. \tag{J-R}
```

An entirely rational safe bound for the normalization term is

```math
(b-1)mK\log\frac1{1-2^{-s}}
 \leq\frac{(b-1)mK}{2^s-1}. \tag{E-R}
```

Indeed, $`-\log(1-\delta)=\int_0^\delta(1-x)^{-1}dx
\leq\delta/(1-\delta)`$. This term prices approximation error in task
loss; the actual operations that normalize weights still belong in $`O_T`$.

For the unchanged ideal forecast, the separate all-issued Brier bound is

```math
\mathbb E\sum_t(p_t-y_t)^2
 \leq(1+1/K)L_*+bK\log N
       +bmK\log\frac1{1-2^{-s}}.
```

If the retained forecast is a rounded action probability, its appropriate
forecast rounding allowance also remains. Neither forecast inequality
inherits the paid-action cancellation.

## 3. Finite arithmetic and exact action probabilities

The persistent weights satisfy $`1\leq w_i\leq M`$ and therefore need
at most

```math
s+\lceil\log_2N\rceil+1
```

bits each. The unnormalized products and their sum obey

```math
v_i\leq KM,\qquad (K-1)M\leq V\leq KM.
```

Every normalization numerator is bounded by

```math
(M-N)v_i\leq M^2K.
```

A safe bit bound for these numerators is thus
$`2(s+\lceil\log_2N\rceil)+\lceil\log_2K\rceil+1`$.
The action-sampling shift has the separate bound
$`s+\lceil\log_2N\rceil+h+1`$. Give the bit-tape sampler its own fixed
transient bound, as explained in the initial implementation review.

For binary experts, the exact ideal probability is
$`p_t=\sum_iw_i a_{t,i}/M`$. If $`N=2^r`$, then $`M=2^{s+r}`$.
When $`h\geq s+r`$, every such probability has an exact $`h`$-bit
representation: the floor in the action sampler loses nothing. In that
case $`\rho_T=0`$, and a retained dyadic forecast is also the ideal
forecast. For the current four-expert service, the condition is simply
$`h\geq s+2`$.

If the action grid is coarser, retain the usual safe
$`(T-m)2^{-h}`$ action allowance and $`2T2^{-h}`$ issued-Brier allowance.
For non-power-of-two $`N`$, exact dyadic representation is not automatic.

Fixed precision gives a per-round approximation floor. A bounded prospective
horizon can instead choose $`s`$ so that $`2^s-1`$ is of order $`mK`$;
then the cumulative normalization allowance stays bounded while persistent
weight bit length grows only logarithmically with the horizon. This is a
planning consequence of (E-R), not a measured speed or resource advantage.

## 4. A necessary-penalty witness

Take $`N=2`$, $`s=1`$, $`M=4`$, $`K=2`$, block size two, and two
constant experts 0 and 1. Every true answer is zero. The normalization map
has

```math
(2,2)\longmapsto(3,1)\longmapsto(3,1)\longmapsto\cdots.
```

The perfect expert has full-tape loss zero. With one unbought action per
block, the expected task loss over ten blocks is

```math
\frac12+9\cdot\frac14=\frac{11}{4}.
```

This exceeds the original unrounded allowance $`2\log2<2`$. The error
keeps growing linearly because the other expert retains positive weight.
Thus silently carrying the original constant-regret theorem into the
fixed-state implementation is incorrect. The added term in (J-R) prevents
that mistake.

## 5. Independent finite evidence

[The exact probe](bounded_normalization_probe.py) enumerates **2,240**
positive-weight-state, binary-loss and learning-factor cases. It covers
$`N=2,3,4`$, precisions one or two, and $`K=2,3`$. It checks mass
preservation, positivity, $`0\leq R<N`$, componentwise retained mass and
the $`M^2K`$ numerator bound. The saved
[output](bounded_normalization_probe.stdout.json) passed, including the
ten-block necessary-penalty witness. No seeds or private query-evaluation
population are involved.

This establishes only the enumerated finite checks in addition to the
general proof above. It is not a review of the subsequently edited root
implementation. The final code needs to implement this exact normalization
and charge its actual arithmetic before the new guarantee is accepted.
