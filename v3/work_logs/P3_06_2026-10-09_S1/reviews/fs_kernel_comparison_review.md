# Independent Fermi–Sobolev kernel comparison

Contributor: **ChatGPT (GPT-6 Astra Pro), independent implementation reviewer**.
October 9, 2026 UTC. Bounded development algebra and source comparison;
zero principal Research90 credit. No forecaster, ordered tree or parameter
sweep was implemented.

**Disposition:** all requested kernel, prefix-sum and score-continuity
identities are correct. The ordinary Fermi–Sobolev construction gives a
stronger asymptotic calibration rate on each fixed Lipschitz ball than the
proposed finite-tent epoch bound. Its resource comparison remains conditional
on an implementation and on the rational arithmetic model being charged.

## 1. Source and comparison scope

Independently reopened: Vladimir Vovk,
[Non-asymptotic calibration and resolution](https://www.probabilityandfinance.com/articles/13.pdf),
Working Paper 13, revised July 1, 2006. Section 3, equations (7)–(10), gives the
Fermi–Sobolev norm and kernel; Section 4, Theorem 2, gives simultaneous RKHS
residual control. The correction term examined below belongs to the paper's
**K29-star** score. The uncorrected K29 rule is related but has a different
variance bound and constants.

The resulting comparison concerns the one-dimensional report coordinate and
a fixed Lipschitz constant. It does not attach a new certificate to forecasts
already produced by the finite-tent code, or import the separate exponential
benchmark's logarithmic finite-expert guarantee.

## 2. Exact kernel and finite-prefix identity

The source kernel expands to

```math
k(q,p)=1+(q-1/2)(p-1/2)
       +\frac{|q-p|^2-|q-p|+1/6}{2}
       =\frac43+\frac{q^2+p^2}{2}-\max(q,p).
```

Here $`q_s`$ denotes an earlier issued scalar, not an expert value. For signed
residual coefficients $`a_s=w_s(y_s-q_s)`$, define

```math
A=\sum_s a_s,\qquad Q_1=\sum_s a_sq_s,\qquad
Q_2=\sum_s a_sq_s^2,
```

```math
A_{\le p}=\sum_{q_s\le p}a_s,\qquad
Q_{1,\le p}=\sum_{q_s\le p}a_sq_s.
```

Splitting the maximum at $`q_s\le p`$ gives the exact identity

```math
\sum_s a_s k(q_s,p)
=\left(\frac43+\frac{p^2}{2}\right)A+\frac{Q_2}{2}
 -pA_{\le p}-(Q_1-Q_{1,\le p}).
```

Repeated locations and endpoint ties cause no problem: at equality the two
possible assignments contribute the same $`a_sp`$. The coefficients must
retain their signs. In particular, $`A=0`$ does not make the kernel sum zero;
the remaining moments and prefix terms still matter.

## 3. Geometry and the scalar score bound

The diagonal and the distance between evaluation sections are

```math
k(p,p)=\frac43-p(1-p)\in[13/12,4/3],
```

```math
\|k_p-k_q\|_{\mathrm{FS}}^2
=k(p,p)+k(q,q)-2k(p,q)=|p-q|.
```

An independent feature representation also verifies positive definiteness.
Put $`h_p(t)=t-\mathbf1\{t>p\}`$. Then
$`k(q,p)=1+\int_0^1 h_q(t)h_p(t)\,dt`$. Evaluation is represented by the
pair $`(1,h_p)`$ because integration by parts gives
$`f(p)=\int_0^1f+\int_0^1 h_pf'`$.

The evaluation-section map is therefore one-half Hölder in Hilbert norm;
it is not Lipschitz in that norm. Nevertheless, each scalar kernel section
is one-Lipschitz as a function of the candidate report. Away from its knot,

```math
\frac{\partial}{\partial p}k(q,p)=p-\mathbf1\{q\le p\},
\qquad \left|\frac{\partial}{\partial p}k(q,p)\right|\le1.
```

For current weight $`w\ge0`$ and scale $`\beta`$, the corresponding score
contribution is

```math
S_{\mathrm{FS}}(p)
=w\beta^2\sum_s a_sk(q_s,p)
 +(1/2-p)w^2\beta^2 k(p,p).
```

Writing $`g(p)=(1/2-p)k(p,p)`$ gives

```math
g'(p)=-\frac{11}{6}+3p-3p^2,
\qquad \sup_{p\in[0,1]}|g'(p)|=\frac{11}{6}.
```

The score is continuous across the finitely many knots. Combining its
piecewise derivative bounds proves the requested global bound

```math
\mathrm{Lip}(S_{\mathrm{FS}})
\le w\beta^2\sum_s|a_s|+\frac{11}{6}w^2\beta^2.
```

The coefficient $`11/6`$ is attained by the correction derivative at an
endpoint. No erroneous Lipschitz assumption about the Hilbert-valued feature
map is needed.

## 4. Uniform Lipschitz-ball calibration

A Lipschitz function on the interval is absolutely continuous, with derivative
bounded almost everywhere by its Lipschitz constant. Thus

```math
\|f\|_\infty\le1,\quad\mathrm{Lip}(f)\le L
\quad\Longrightarrow\quad
\|f\|_{\mathrm{FS}}^2
=\left(\int_0^1 f\right)^2+\int_0^1(f')^2
\le1+L^2.
```

Combining this observation with the source's simultaneous RKHS bound gives,
for the exact unweighted K29-star forecasts from this kernel,

```math
\sup_{\|f\|_\infty\le1,\,\mathrm{Lip}(f)\le L}
\left|\sum_{t=1}^T(y_t-p_t)f(p_t)\right|
\le\sqrt{1+L^2}
\sqrt{\sum_{t=1}^T p_t(1-p_t)k(p_t,p_t)}.
```

The diagonal bound alone yields $`\sqrt{(1+L^2)T/3}`$. A direct refinement
uses $`p(1-p)k(p,p)\le13/48`$, giving
$`\sqrt{13(1+L^2)T/48}`$: write $`z=p(1-p)\le1/4`$ and observe that
$`z(4/3-z)`$ is increasing on $`[0,1/4]`$.
Both bounds have order $`\sqrt T`$ for fixed $`L`$.
Announced bounded weights can be represented by the weighted feature map;
the corresponding variance sum then contains $`w_t^2`$. Approximate roots,
other feature blocks and delayed copies require their actual additional
terms or transfer arguments.

This strengthens the calibration exponent relative to the finite-tent epoch
$`T^{2/3}`$ upper bound on the same fixed-Lipschitz test class. It does not
cover arbitrary discontinuous indicator tests or a Lipschitz constant allowed
to grow without being charged in the bound.

## 5. Conditional resources and bounded probe

The identity needs two ordered prefix sums, $`A_{\le p}`$ and
$`Q_{1,\le p}`$, plus global $`A,Q_1,Q_2`$. A balanced tree keyed by the
rational forecast and augmented with subtree sums could support one kernel
query or one admitted update with $`O(\log n)`$ rational comparisons and
arithmetic operations, where $`n`$ bounds the number of stored locations.
It would use $`O(n)`$ stored rational records in the worst case. The absolute
coefficient sum for the score bound can be maintained separately.

This is conditional data-structure analysis. No tree is implemented here.
Forecast selection may require many kernel queries, and exact comparisons,
numerators, denominators and root precision still carry costs. This note
proves no hard bound on bit sizes, memory in bytes or CPU use, and reports no
runtime advantage.

The [standalone rational probe](../development/independent_fs_kernel_v1/probe_fs_kernel.py)
and its [result](../development/independent_fs_kernel_v1/probe_fs_kernel_result.json)
pass **2,692 checks**: 256 kernel pairs, 208 prefix evaluations across 13
history prefixes, and all 93 endpoint/interior extrema needed to bound the
piecewise score derivative on those fixed fixtures. It also checks signed
Gram norms through the integral feature representation and finite increments
crossing the knots. Queries are deliberately evaluated by list scans, so the
probe verifies algebra without claiming an ordered implementation.

The prior repository, principal clock, phase status and gate decisions are
unchanged by this review.
