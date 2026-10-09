# P3-06 independent review: growing tents with epoch restarts

Contributor: **ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer**.
October 9, 2026 UTC. This is a mathematical extension and source comparison.
No executable code or numerical proof probe was created or run, no production
method was changed, and no gate or P3-07 work was started. Subagent effort is
unmeasured and receives zero principal-clock credit.

**Disposition:** the proposed construction is sound under full immediate
feedback and unit weights. It gives a uniform bound for each fixed bounded
Lipschitz class, convergence for every fixed continuous scalar-report test,
and simultaneous expert and smooth fixed-action regret bounds. Its resource
statement requires the restricted rational input contract below. Its rate is
not an optimality claim: the already cited Fermi–Sobolev kernel gives a stronger
ordinary Lipschitz calibration certificate.

## 1. Contract and dimension-independent potential budget

All outcomes are binary, and each answer is admitted before the next issue.
Fix a finite expert library with stable indices and reports in $`[0,1]`$,
positive scales $`\alpha,\beta`$, and a fixed positive root residual tolerance
$`\delta`$. Use unit weights. Each epoch starts a fresh copy of the CF-1
learner, with a grid size fixed throughout that epoch. All current expert
values and optional loss rows are available before its scalar report is
chosen. Root search is certified to the tolerance; a fixed unsuccessful
iteration cap would not supply the allowance bound used here.

Optionally include the two CF-6 action features at fixed scale $`\gamma>0`$,
with the announced slope ranges bounded by a constant $`D`$. The two action
labels retain their identities across epochs. Define

```math
C=\frac{N\alpha^2+\beta^2+\gamma^2D^2}{4}+2\delta.
```

Omit the action term when that block is absent. Since the tents satisfy
$`\sum_jb_j(p)^2\le1`$, the potential budget for every local prefix of
$`n`$ rounds is

```math
B_{e,n}\le Cn,
\qquad
\sum_{j=0}^{m_e}E_{e,n,j}^2\le\frac{B_{e,n}}{\beta^2},
\qquad
E_{e,n,j}=\sum_{t\in(e,n)}b_{j,m_e}(p_t)(y_t-p_t).
```

The constant $`C`$ is independent of the number of tents. The calibration
feature norm uses their squared sum, not their number. These are pathwise
inequalities for every admissible binary sequence, without a stochastic
model for its labels.

## 2. Sharp interpolation error and a local prefix certificate

Let $`\mathcal F_L`$ consist of all real functions on $`[0,1]`$ with
$`\|f\|_\infty\le1`$ and Lipschitz constant at most $`L`$. Define

```math
f_m(p)=\sum_{j=0}^{m}f(j/m)b_{j,m}(p).
```

For $`p=(j+r)/m`$, where $`0\le r\le1`$, only the two adjacent tents
contribute. Hence

```math
|f(p)-f_m(p)|
\le (1-r)L\frac r m+rL\frac{1-r}{m}
=\frac{2Lr(1-r)}m
\le\frac{L}{2m}.
```

The mesh constant $`1/2`$ can be attained by a Lipschitz V-shaped function
on one cell when its amplitude fits the unit bound. There is no need to use
the looser error $`L/m`$ from the earlier source-comparison draft.

The coefficient vector $`(f(0),f(1/m),\ldots,f(1))`$ has norm at most
$`\sqrt{m+1}`$. Also $`|y_t-p_t|\le1`$. Applying Cauchy–Schwarz to the
calibration residual vector therefore gives, simultaneously for the whole
class,

```math
\sup_{f\in\mathcal F_L}
\left|\sum_{t\in(e,n)}f(p_t)(y_t-p_t)\right|
\le\frac{\sqrt{m_e+1}\sqrt{B_{e,n}}}{\beta}
     +\frac{Ln}{2m_e}
\le\frac{\sqrt{m_e+1}\sqrt{Cn}}{\beta}
     +\frac{Ln}{2m_e}.
```

The inequality holds for every prefix of the epoch. It does not assume that
the epoch has completed, and it does not replace the actual number $`n`$ of
observations by its planned horizon inside the premise.

## 3. Doubling epochs, including their unfinished prefixes

Use planned epoch lengths and fixed epoch resolutions

```math
H_k=2^k,\qquad m_k=\lceil H_k^{1/3}\rceil,\qquad k=0,1,\ldots.
```

Suppose epochs $`0,\ldots,K-1`$ are complete and the current epoch has
received $`n`$ outcomes, with $`0\le n\le H_K`$. Then

```math
T=(H_K-1)+n,\qquad H_K\le T+1.
```

For a nonempty current prefix the stronger $`H_K\le T`$ holds. At the
instant a new epoch starts, $`n=0`$ and its residual contribution is zero.
Thus a large newly planned horizon does not create an unobserved error term.

Write $`n_k=H_k`$ for completed epochs and $`n_K=n`$. Applying the local
inequality to the same function in every epoch and then the triangle
inequality gives the exact summed certificate

```math
\sup_{f\in\mathcal F_L}
\left|\sum_{t=1}^{T}f(p_t)(y_t-p_t)\right|
\le \frac{\sqrt C}{\beta}
       \sum_{k=0}^{K}\sqrt{(m_k+1)n_k}
     +\frac L2\sum_{k=0}^{K}\frac{n_k}{m_k}.
```

Since $`m_k+1\le3H_k^{1/3}`$, $`m_k\ge H_k^{1/3}`$ and
$`n_k\le H_k`$, each epoch contributes at most
$`(\sqrt{3C}/\beta+L/2)H_k^{2/3}`$. Summing the geometric series yields

```math
\sup_{f\in\mathcal F_L}
\left|\sum_{t=1}^{T}f(p_t)(y_t-p_t)\right|
\le
\frac{\sqrt{3C}/\beta+L/2}{1-2^{-2/3}}(T+1)^{2/3}.
```

For $`T\ge1`$ the epoch containing the latest observed round can always be
chosen nonempty, in which case $`T^{2/3}`$ replaces $`(T+1)^{2/3}`$ in
this convenient upper bound. The displayed $`T+1`$ version also covers the
empty-epoch convention without ambiguity. Neither version fails at a restart.

Thus the normalized residual is uniformly
$`O((1+L)T^{-1/3})`$ for every fixed $`L<\infty`$. The algorithm's
schedule does not need to know $`L`$.

## 4. Quantifiers and continuous tests

The finite inequality holds for every horizon and every function in a
declared Lipschitz ball. It therefore also controls a function selected
retrospectively from that same fixed ball. It does not assert uniform
convergence over functions with unrestricted and increasing Lipschitz
constants.

For any fixed continuous $`f`$ on $`[0,1]`$, piecewise-linear interpolation
approximates it uniformly by a Lipschitz function $`g`$. After scaling for a
finite sup norm, the preceding result applies to $`g`$. For every
$`\varepsilon>0`$ choose such a fixed $`g`$ with
$`\|f-g\|_\infty\le\varepsilon`$. Then

```math
\limsup_{T\to\infty}\frac1T
\left|\sum_{t=1}^{T}f(p_t)(y_t-p_t)\right|
\le\varepsilon.
```

Letting $`\varepsilon`$ decrease to zero proves convergence for each fixed
continuous test. No common quantitative rate for the entire unit ball of
continuous functions follows from this argument. Discontinuous indicators
cannot be uniformly approximated in this way; the preserved CF-5 threshold
counterexample remains relevant. Tests here depend on the scalar report,
not on an unannounced context, semantic query class, or hindsight label.
Conditional frequency statements still require sufficient selected mass.

## 5. Expert and smooth-action guarantees survive the restarts

For each fixed supplied expert index $`i`$, sum CF-2 across the epochs:

```math
L_T-L_{T,i}
\le\frac2\alpha\sum_{k=0}^{K}\sqrt{B_{k,n_k}}
\le\frac{2\sqrt C}{\alpha(1-2^{-1/2})}\sqrt{T+1}.
```

This is an upper bound on signed regret to the same global fixed comparator.
It uses no resetting of the comparator's loss. As in the calibration bound,
one may use $`T`$ for a nonempty-current-epoch convention.

If the optional two-action block is present, use the global issuance index
in the dyadic smoothing schedule, with fixed $`c>0`$:

```math
\eta_t=c\,2^{-\lceil\log_2(t+1)\rceil}.
```

Then, for each fixed action index,

```math
G_{T,i}
\le\frac{\sqrt C}{\gamma(1-2^{-1/2})}\sqrt{T+1}
     +Q_T,
\qquad
Q_T=\frac18\sum_{t=1}^{T}\eta_t
\le\frac c{16}\lceil\log_2(T+1)\rceil.
```

Each complete dyadic smoothing block has sum $`c/2`$, which proves the last
inequality. Resetting the smoothing index inside every epoch would instead
make this simple summed slack bound $`O((\log T)^2)`$; the asserted
$`O(\log T)`$ term uses the global schedule. The scored loss is the announced
action mixture. Sampled actions require a separate fluctuation analysis and
must not alter the mathematical label or admitted inclusion.

## 6. Restricted numerical resources

The statistical inequalities above need no rationality hypothesis. For the
following numerical size bounds, additionally fix the expert count, positive
rational scales and $`c,\delta`$, a uniform input-magnitude bound and one
common denominator for expert values and action-row entries. Use dyadic
bisection and certified root mode. Query strings, proofs, external expert
computations and duplicated exported histories remain separately charged.

Although $`m_k`$ changes between epochs, the actual feature formula is
$`b_{j,m}(p)=\max(0,1-|mp-j|)`$. Its integer $`m,j`$ coefficients have
$`O(\log(T+1))`$ bits. At a dyadic candidate with exponent $`a`$, its
value has denominator dividing $`2^a`$; a spurious odd factor from writing
a center as $`j/m`$ is absent from the simplified feature value. Integer mesh
growth therefore does not introduce fresh odd denominators into the core.

The Euclidean Lipschitz constant of the tent vector is at most
$`\sqrt2\,m`$: almost everywhere exactly two of its derivatives can be
nonzero, with slopes $`m,-m`$. The complete feature norm remains bounded,
while the complete Lipschitz constant is
$`O(m_k+1+\eta_t^{-1})=O(t+1)`$ at global issue $`t`$. Previous certified
root success gives $`\|R\|=O(\sqrt t)`$, so the next score has a
$`O((t+1)^{3/2})`$ Lipschitz bound. A computable polynomial upper bound
suffices to certify $`O(\log(t+1))`$ bisections, without assuming the desired
bit bound in advance.

The nested dyadic-denominator argument of CF-11 now applies coordinate by
coordinate. Each core numeric coordinate, potential term and global dyadic
smoothing sum has $`O(\log(T+1))`$ bits. The active vector dimension is
$`O(T^{1/3})`$. Consequently:

- Active learner numeric state occupies $`O(T^{1/3}\log(T+1))`$ bits.
- Retaining one residual vector and constant-size certificate summary per
  completed epoch has the same total order, since $`\sum_{k\le K}m_k`$
  is $`O(T^{1/3})`$.
- Retaining every numeric issue and settlement record once, with its full
  epoch feature vector, occupies at most $`O(T^{4/3}\log(T+1))`$ bits.

These are size bounds, not constant-time arithmetic or an end-to-end CPU
budget. They do not charge evaluation of an arbitrary subsequently supplied
real test function as free. Nor do they assert that every derived closed-form
certificate has an $`O(\log T)`$ reduced denominator: flattening a sum of
$`n_k/m_k`$ terms can combine different mesh denominators. Keeping those
per-epoch terms costs only $`O((\log(T+1))^2)`$ bits, within the stated
summary size bound, and the analytic geometric bound needs no such flattening.

The current production module fixes its bins and caps them at 64. This
unbounded-grid epoch rule is a theorem extension, not a claim about the
existing four-bin run or a tested growing-grid implementation. The argument
also assumes immediate complete feedback. A delayed extension must explicitly
sum all per-copy/per-epoch terms and handle unresolved observations; the
present rate cannot be transferred merely by naming the delayed wrapper.

## 7. Direct primary antecedents and a stronger ordinary rate

I rechecked [Vovk, *Non-asymptotic calibration and resolution*](https://www.probabilityandfinance.com/articles/13.pdf),
§5 Corollary 1 and its proof: a universal RKHS gives vanishing normalized
residuals for every continuous test on a compact context/report space. I also
checked [Foster and Hart, *Smooth calibration, leaky forecasts, finite recall,
and Nash dynamics*](https://math.huji.ac.il/~hart/papers/calib-eq.pdf), §4
Theorem 10 and Appendix A Lemmas 17–18, which give fixed-Lipschitz-class
guarantees and a finite uniform approximation construction. Neither is being
credited with this exact epoch schedule; neither supports a priority claim
for it. A finite forecast grid in the latter paper is not the same as a
finite tent-feature grid with continuous scalar reports.

There is also a directly stronger rate in Vovk's existing source. Its §3
Fermi–Sobolev norm and kernel satisfy

```math
\|f\|_{\mathrm{FS}}^2
=\left(\int_0^1f(u)\,du\right)^2+\int_0^1f'(u)^2\,du
\le1+L^2,
\qquad
\sup_p K_{\mathrm{FS}}(p,p)=\frac43
```

for our unit-bounded Lipschitz class. The derivative is interpreted almost
everywhere. Theorem 2 therefore supplies an ordinary
$`O(\sqrt{1+L^2}\sqrt T)`$ residual certificate. A direct sum with the
fixed expert and smooth-action blocks retains that order, by the same CF-1
argument with a bounded Hilbert-space feature norm. This is a source-based
mathematical comparison, without a new implementation or resource claim.
The finite-tent rate proved here must not be described as universally best.

**Signed:** ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer.
