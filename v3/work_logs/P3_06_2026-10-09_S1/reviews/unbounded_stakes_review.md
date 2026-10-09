# P3-06 independent review: unbounded native stakes

Contributor: **ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer**.
October 9, 2026 UTC. Subagent effort is unmeasured; principal research-time
credit is zero. This is a P3-06 refinement review, not a paid-reasoning policy.

**Disposition:** the proposed normalization and geometric obstruction are
valid. The geometric constant can be strengthened. Polynomial growth must
be accompanied by the stated dispersion condition; a polynomial upper bound
alone does not suffice. The following statements concern one sequential
forecaster unless delayed aggregation is explicitly invoked.

## 1. Contract and exact normalization

Before its binary answer, round $`t`$ announces two finite rational affine
action losses $`c_t(i,y)=b_{t,i}+d_{t,i}y`$. Fix the cost unit, including the
reference unit used by the floor one, and put

```math
D_t=|d_{t,1}-d_{t,0}|,
\qquad M_t=2^{\lceil\log_2\max(1,D_t)\rceil},
\qquad S_T=\sum_{t\le T}M_t.
```

The power can be found by exact rational/integer comparisons; a floating
logarithm is unnecessary. We have $`M_t\ge1`$, $`D_t\le M_t`$ and
$`M_t<2\max(1,D_t)`$.

Supply the scalar core with weight $`w_t=M_t`$, normalized table
$`c'_t=c_t/M_t`$, and positive smoothing width $`\eta_t`$. Let $`s_t(p)`$ be
its action-one mixture probability. In native units the same rule is

```math
s_t(p)=\mathrm{clip}_{[0,1]}
\left(\frac12-\frac{c_t(1,p)-c_t(0,p)}{2M_t\eta_t}\right).
```

The core's weighted normalized mixture and comparator losses equal the
original native losses exactly:

```math
M_t\bigl((1-s_t)c'_t(0,y_t)+s_tc'_t(1,y_t)\bigr)
=(1-s_t)c_t(0,y_t)+s_tc_t(1,y_t),
\qquad M_tc'_t(i,y_t)=c_t(i,y_t).
```

Writing $`\bar d_t=d_{t,0}+s_t(d_{t,1}-d_{t,0})`$, the core's action
coordinate also becomes exactly the native-cost coordinate

```math
M_t\gamma(\bar d'_t-d'_{t,i})=\gamma(\bar d_t-d_{t,i}).
```

Thus the existing smooth-action identity is retained with a native fixed-action
regret comparator. The action chosen at every round is scored as a mixture;
the previously stated conditions for converting that score into expected
sampled-action performance still apply.

## 2. Common potential and normalized refinement

The normalized slope **range** is at most one. The individual normalized
slopes or table entries need not be bounded, because they may share a large
common component. The action features use slope differences, so this causes
no problem for the following norm estimate:

```math
\|\Phi_t(p)\|^2\le
M_t^2(N\alpha^2+\beta^2+\gamma^2),
\qquad
B_T\le\frac{N\alpha^2+\beta^2+\gamma^2}{4}\sum_tM_t^2+\sum_tA_t.
```

For the native signed regret to either fixed action index,

```math
G_{T,i}=\sum_t\bigl((1-s_t)c_t(0,y_t)+s_tc_t(1,y_t)-c_t(i,y_t)\bigr),
```

the proved common-vector consequences are

```math
G_{T,i}\le\frac18\sum_tM_t\eta_t+\frac{\sqrt{B_T}}{\gamma},
```

```math
\sum_tM_t\bigl((p_t-y_t)^2-(q_{t,j}-y_t)^2\bigr)
\le\frac{2\sqrt{B_T}}{\alpha},
\qquad
\left|\sum_tM_tb_k(p_t)(y_t-p_t)\right|\le\frac{\sqrt{B_T}}{\beta}.
```

Consequently, if

```math
\sum_tM_t^2=o(S_T^2),\qquad \sum_tA_t=o(S_T^2),\qquad \eta_t\longrightarrow0,
```

the upper bounds divided by $`S_T`$ vanish. Here $`S_T\ge T\to\infty`$,
and the weighted smoothing condition follows from $`\eta_t\to0`$: split the
sum into a finite prefix and a tail whose width is arbitrarily small.

In the certified root mode with fixed absolute tolerance $`\delta>0`$,
$`\sum_tA_t\le2\delta T`$, so $`\sum_tA_t/S_T^2\le2\delta/T`$. That
allowance condition is then automatic. It remains an explicit condition when
root work is capped and the actual residual can exceed the requested tolerance.

This is stake-normalized native action regret and weighted predictive
refinement. It does not claim vanishing native regret per unweighted round,
vanishing outcome-oracle action regret, conditional accuracy in rarely
occupied bins, or calibration of every absolute native cost stream.

For a delayed pool, replace $`\sqrt{B_T}`$ by the relevant aggregate
$`H_T=\sum_k\sqrt{B_T^{(k)}}`$. A rate then requires $`H_T/S_T\to0`$ and
the existing settled-prefix/coverage conditions. The single-copy dispersion
assumption does not remove the copy-growth obstruction.

## 3. Polynomial stakes and a polynomial-envelope failure

The conditions admit dense unbounded schedules such as
$`M_t=\Theta(t^a)`$ for any fixed $`a>0`$. Then
$`S_T=\Theta(T^{a+1})`$ and $`\sum_tM_t^2=\Theta(T^{2a+1})`$, so the
normalized potential term is $`O(T^{-1/2})`$ under fixed root tolerance.
With the dyadic width $`\eta_t=\Theta(1/t)`$, normalized smoothing slack is
$`O(T^{-1})`$. For bounded comparable stakes, its rate is
$`O(\log T/T)`$. These are upper rates for the displayed certificates.

Merely requiring $`D_t\le t^2`$ is insufficient. Set $`D_t=t^2`$ when
$`t=2^{2^k}`$, and zero otherwise. Then $`M_t=t^2`$ on those occasions and
one elsewhere. At a new spike time $`t_k`$, the previous spike contributes
only $`t_{k-1}^2=t_k`$, and total earlier stake is $`O(t_k)`$. The new stake
$`t_k^2`$ dominates, and $`\sum_{t\le t_k}M_t^2/S_{t_k}^2\to1`$.
The correct general hypothesis is dispersion, not a polynomial envelope.

## 4. Geometric lower bound, with a sharper constant

In the generic binary prediction protocol, take two constant experts zero and
one, announced weights $`w_t=r^t`$, and reports in $`[0,1]`$. Choose
$`y_t=1`$ if $`p_t<1/2`$, and zero otherwise. Every report has squared loss
at least one quarter. Write $`W_T=\sum_{t\le T}w_t`$ and
$`P_T=W_T-w_T`$. Then

```math
L_T\ge W_T/4,
\qquad
\min(L_{T,0},L_{T,1})\le P_T,
\qquad
\frac{P_T}{W_T}<\frac1r.
```

The second inequality chooses the constant expert matching the last outcome;
it loses nothing on that round and at most all preceding stake. Therefore

```math
\frac{L_T-\min_iL_{T,i}}{W_T}
\ge\frac14-\frac{P_T}{W_T}
>\frac{r-4}{4r}.
```

This gives a positive uniform lower bound already for $`r>4`$. The proposed
weaker constant $`(r-5)/(4r)`$ for $`r>5`$ is valid; it follows by using only
the learner's final-round lower bound instead of its all-round lower bound.
The obstruction is a generic binary-tape result. It is not an asserted trace
of the modular arithmetic query family or an experimental finding about that
family's difficulty.

## 5. Common offsets, arithmetic size and attribution

Adding any known common outcome-dependent cost $`h_t(y)`$ to both actions
preserves $`D_t`$, $`M_t`$, action-cost differences and all action features.
Holding the other announced inputs fixed, it preserves the forecasting
trajectory and action regret. It changes absolute realized and forecast costs.
No absolute loss-calibration theorem follows from that cancellation.

Dividing by a power of two introduces no new odd denominator factor. It does
not remove odd factors already present, bound huge common offsets or pay for
their input and arithmetic. A restricted finite-bit corollary remains possible:
if original input magnitudes grow at most polynomially, original rational
denominators divide a fixed integer, widths are dyadic and roots use fixed
certified tolerance, then the scale exponents, root depths and numeric-state
bit lengths remain $`O(\log(t+1))`$ by the earlier denominator argument.
For example, $`M_t=O(t^a)`$ gives $`R_{t-1}=O(t^{a+1/2})`$ and score
Lipschitz bound $`O(t^{2a+3/2})`$. Arbitrary unbounded input bit sizes are
outside that corollary, and nonnumeric metadata/complete external computation
remain outside its numeric-kernel account.

The proof is an algebraic normalization and application of the reconstructed
continuous-feature potential and smooth-action theorem in the
[independent proof review](independent_proof_review.md), particularly §§2,8,13.
It should inherit that defensive-forecasting source attribution. No separate
priority claim or new universal unbounded-value calculus is established here.
The geometric and sparse-spike obstructions are elementary derivations above;
no external impossibility theorem is silently imported.

## 6. Independent evidence

The [exact probe](unbounded_stakes_review.py) and its
[immutable result](unbounded_stakes_review_result.json) report **PASS**, with
34,937 assertions. They cover all 64 six-label paths for native normalization
with changing cost offsets and nonunit feature scales; exact native scoring;
forecast/offset invariance; denominator factors; both geometric lower bounds
on a finite report grid; and dense/sparse stake examples. Counts are finite
evidence, not proofs of the asymptotic statements.

Reviewed module: `p306-scalar-v2.1`, SHA-256
`b66af7ec64b7e690aaa15c0901b2ccb220f93f97962052607481ddd7ae240e07`;
unchanged throughout the run. Observed script execution: 871,426,566 ns,
recorded as runtime evidence and not principal research credit.

**Signed:** ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer.
No P3-07 work or gate was started.
