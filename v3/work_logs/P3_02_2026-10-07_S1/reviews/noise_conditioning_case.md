# P3-02 — exact noisy recovery in a three-outcome case

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
**/root/scoring_sources**. Same-model internal, nonblind derivation check.
This note owns no clock, ledger, status, gate or principal-file decision.
Concurrent reviewer effort is not additional principal research credit.
The calculations are development material, not a frozen challenge.

## 1. Result and exact service

The proposed formula is correct. Let
```math
L_\delta=
\begin{bmatrix}
0&1&1\\
0&1&1+\delta
\end{bmatrix},\qquad \delta>0,
```
and observe $`y=L_\delta p+e`$, with $`p\in\Delta_3`$ and
$`\|e\|_\infty\leq\epsilon`$, where $`\epsilon\geq0`$. The target is the
single scalar $`p_3`$. If a decoder may choose any scalar estimate as a
function of the observation, its global minimax absolute-error radius is
```math
\boxed{
R_\delta(\epsilon)
=\frac12\min\left\{
1,\frac{4\epsilon}{\delta},
\frac{1+2\epsilon}{1+\delta}
\right\}.}
\tag{N1}
```
The same optimum is available if the scalar estimate must lie in $`[0,1]`$.
This is a bounded deterministic-error result. No stochastic independence,
noise distribution, learned-error certificate or statistical confidence
level is assumed.

The proof below derives a matching upper bound and explicit compatible laws
with a common observation. No external theorem or source survey is required
for the calculation. The claim concerns this scalar target and this declared
noise set, rather than an unrestricted vector-reconstruction radius.

## 2. Pair modulus and law-difference feasibility

For a feasible observation $`y`$, define
```math
F_y=\{p\in\Delta_3:\|L_\delta p-y\|_\infty\leq\epsilon\}.
```
It is nonempty, compact and convex. Its $`p_3`$-projection is a closed
interval. The interval midpoint attains error equal to half its width, and
no other scalar output can have smaller maximum error on that interval.

Two laws $`p,q`$ admit a common noisy observation exactly when
```math
\|L_\delta(p-q)\|_\infty\leq2\epsilon.
\tag{N2}
```
Necessity is the triangle inequality. For sufficiency, the common midpoint
observation $`y=(L_\delta p+L_\delta q)/2`$ lies within $`\epsilon`$ of both.
It follows that the global radius is half the largest target difference
between pairs satisfying (N2).

Swap the pair if necessary so that $`r=p_3-q_3\geq0`$. Put
```math
h=p-q=(-t,t-r,r),\qquad L_\delta h=(t,t+\delta r).
```
A zero-sum vector $`h`$ is the difference of two probability vectors if and
only if $`\|h\|_1\leq2`$. Necessity follows from their unit masses. For
sufficiency, write $`h=h_+-h_-`$; the two positive masses are equal and
at most one, so the same nonnegative residual mass can be added to both.

For the present parameterization,
```math
\frac{\|h\|_1}{2}
=
\begin{cases}
r-t,&t\leq0,\\
r,&0\leq t\leq r,\\
t,&t\geq r.
\end{cases}
```
Thus probability-difference feasibility is exactly
```math
0\leq r\leq1,\qquad r-1\leq t\leq1.
\tag{N3}
```
This includes the positivity/normalization restriction that a bound using
only the inverse observation map can miss.

Write $`a=2\epsilon`$. Because $`r\geq0`$ and $`\delta>0`$, the two
noise constraints reduce to one interval:
```math
|t|\leq a,\quad |t+\delta r|\leq a
\quad\Longleftrightarrow\quad
-a\leq t\leq a-\delta r.
\tag{N4}
```
Combining (N3) and (N4), a given $`r\in[0,1]`$ is attainable exactly when
```math
\max(-a,r-1)\leq\min(1,a-\delta r).
```
The only further nonautomatic inequalities are
```math
\delta r\leq2a,\qquad
(1+\delta)r\leq1+a.
\tag{N5}
```
The maximal target difference is therefore
```math
r_*=\min\left\{1,\frac{2a}{\delta},
\frac{1+a}{1+\delta}\right\},
```
which proves the upper bound in (N1).

## 3. A matching rational construction

For this $`r_*`$, choose
```math
t_*=\min(0,a-\delta r_*),\qquad
q=(0,1,0),\qquad
p=(-t_*,\,1-r_*+t_*,\,r_*).
\tag{N6}
```
If $`\delta r_*\leq a`$, then $`t_*=0`$, and $`p`$ is a mixture of the
second and third outcomes. Otherwise $`t_*=a-\delta r_*<0`$;
the second inequality in (N5) ensures
$`1-r_*+t_*\geq0`$. In either case $`p,q\in\Delta_3`$, and their target
values are $`r_*`$ and zero.

Take the common observation
```math
y=\frac{L_\delta p+L_\delta q}{2}
=\left(1+\frac{t_*}{2},
1+\frac{t_*+\delta r_*}{2}\right).
\tag{N7}
```
The noise vector for $`q`$ is
$`(t_*/2,(t_*+\delta r_*)/2)`$, and that for $`p`$ is its negative.
Each coordinate is bounded in absolute value by $`\epsilon`$, by (N4).
Thus any scalar estimate at this observation errs by at least $`r_*/2`$
on one of the two laws. This matches the upper bound and proves (N1).

When $`\delta,\epsilon`$ are rational, the minimum, all coordinates of
these laws, and the common observation are rational. No limiting or
approximately feasible pair is required on the closed simplex.

The construction has three transparent regimes:

| Range of $`a=2\epsilon`$ | $`r_*`$ | Matching $`p`$, with $`q=(0,1,0)`$ |
|---|---|---|
| $`0\leq a\leq\delta/(\delta+2)`$ | $`2a/\delta`$ | $`(a,\ 1-a-2a/\delta,\ 2a/\delta)`$ |
| $`\delta/(\delta+2)\leq a\leq\delta`$ | $`(1+a)/(1+\delta)`$ | $`((\delta-a)/(1+\delta),\ 0,\ (1+a)/(1+\delta))`$ |
| $`a\geq\delta`$ | $`1`$ | $`(0,0,1)`$ |

At regime endpoints the adjacent formulas agree. In the first regime both
noise coordinates saturate with opposite signs. In the middle regime the
second coordinate saturates, but pushing the first further would require
a negative second-outcome probability. In the last regime two simplex
vertices already realize the maximum possible target separation.

## 4. Precisely when the simple inversion bound is loose

Subtracting the two observed coordinates gives
```math
y_2-y_1=\delta p_3+(e_2-e_1).
```
Inversion and the error box give error at most $`2\epsilon/\delta`$;
the constant estimate $`1/2`$ also gives error at most $`1/2`$.
Hence
```math
R_\delta(\epsilon)\leq
\min\{1/2,2\epsilon/\delta\}.
```
The extra probability-feasibility cap in (N1) can make this inequality
strict. The exact piecewise radius is
```math
R_\delta(\epsilon)=
\begin{cases}
2\epsilon/\delta,
&0\leq\epsilon\leq\dfrac{\delta}{2(\delta+2)},\\[6pt]
\dfrac{1+2\epsilon}{2(1+\delta)},
&\dfrac{\delta}{2(\delta+2)}
\leq\epsilon\leq\dfrac{\delta}{2},\\[6pt]
1/2,&\epsilon\geq\dfrac{\delta}{2}.
\end{cases}
\tag{N8}
```
For every $`\delta>0`$, the simple minimum bound is strictly loose exactly
when
```math
\frac{\delta}{2(\delta+2)}<\epsilon<\frac{\delta}{2}.
```
The two equality endpoints are not loose.

For $`\delta=1`$, three rational examples check the regimes:

| $`\epsilon`$ | Matching $`p`$ | Common $`y`$, with $`q=(0,1,0)`$ | Exact $`R`$ | Simple bound |
|---:|---|---|---:|---:|
| $`1/10`$ | $`(1/5,2/5,2/5)`$ | $`(9/10,11/10)`$ | $`1/5`$ | $`1/5`$ |
| $`1/4`$ | $`(1/4,0,3/4)`$ | $`(7/8,5/4)`$ | $`3/8`$ | $`1/2`$ |
| $`1/2`$ | $`(0,0,1)`$ | $`(1,3/2)`$ | $`1/2`$ | $`1/2`$ |

In the middle example, the first law has exact observation
$`(3/4,3/2)`$ and the second has $`(1,1)`$. Their common observation
requires noise $`(1/8,-1/4)`$ for $`p`$ and
$`(-1/8,1/4)`$ for $`q`$. The $`3/4`$ target separation establishes
the $`3/8`$ lower bound; the third cap proves no larger separation is
possible.

## 5. Optional pointwise decoder and interval check

There is also a closed-form interval for each feasible observation. Write
$`u=p_2+p_3`$ and $`r=p_3`$, so $`0\leq r\leq u\leq1`$.
At fixed $`r`$, compatible $`u`$ must lie in
```math
[r,1]\cap[y_1-\epsilon,y_1+\epsilon]
\cap[y_2-\epsilon-\delta r,y_2+\epsilon-\delta r].
```
Requiring every lower endpoint to be below every upper endpoint gives,
for feasible $`y`$ and $`\delta>0`$,
```math
r_{\min}(y)=
\max\left\{
0,\frac{y_2-1-\epsilon}{\delta},
\frac{y_2-y_1-2\epsilon}{\delta}
\right\},
\tag{N9}
```
```math
r_{\max}(y)=
\min\left\{
1,\ y_1+\epsilon,\
\frac{y_2+\epsilon}{1+\delta},\
\frac{y_2-y_1+2\epsilon}{\delta}
\right\}.
\tag{N10}
```
The scalar midpoint $`(r_{\min}+r_{\max})/2`$ is minimax for that
observation. Its maximum error over feasible observations equals (N1).
Equations (N9)–(N10) are stated on feasible observations; checking the
nonemptiness of the original compatible set is still necessary when an
arbitrary input $`y`$ is supplied.

For the matching observation in (N7), the interval is exactly
$`[0,r_*]`$: (N6) supplies both endpoints, and the already proved global
separation bound excludes any larger upper endpoint.

## 6. Edge cases and interpretation

- If $`\delta>0`$ and $`\epsilon=0`$, the observations identify
  $`p_3=(y_2-y_1)/\delta`$ exactly, so $`R_\delta(0)=0`$.
- If $`\delta=0`$, both rows are $`(0,1,1)`$. The laws
  $`(0,1,0)`$ and $`(0,0,1)`$ have identical exact observations,
  so the global radius is $`1/2`$ for every $`\epsilon\geq0`$, including
  zero. Formula (N1) uses division by $`\delta`$ and must not be
  evaluated at this point.
- For fixed positive $`\epsilon`$, the radius reaches $`1/2`$ as soon
  as $`0<\delta\leq2\epsilon`$. Exact full rank by itself consequently
  supplies no uniform robustness as the rows approach one another.
- The extremizing construction uses boundary laws. On the strictly positive
  simplex it still gives the same supremum radius by perturbing both laws
  toward a common interior law; the maximum need not be attained there.
  For $`\delta=0`$, strictly positive pairs likewise approach target
  separation one.

The informative feature of the calculation is the middle regime:
normalization and nonnegativity constrain how observation errors can hide a
change in $`p_3`$. This gives an exact improvement over the unstructured
inversion bound for the declared scalar service. It does not establish a
general superiority claim, an independent empirical finding, or a new
learning guarantee.
