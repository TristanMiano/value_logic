# F16 source-uncertainty boundary: independent hand audit

**Contributor:** ChatGPT (GPT-6 Astra Pro), delegated separate mathematical check.  
**Date:** 2026-10-05 UTC. **Principal clock credit:** zero.

**Scope and method.** I read `source_uncertainty_boundary.md` §§1–5, derived the source and minimax calculations by hand, reported a missing closedness qualification, then read the corrected §1 and newly added §6. I subsequently read derivation `10_f16_coherent_recovery.md` §10 to check its final source-restriction corollary against the triangle laws already checked in `additional_source_coherence_gap.md`; the upper/lower theorem was not reopened. This is a separate reconstruction by the named contributor, not a blinded external or human review. No scripts, experiments, numerical searches, external browsing, or saved checks were run. Only this audit file was written; the principal made the correction to the principal note.

**Disposition:** the interval-source example, all six revised means, piecewise compatible radius, rational example, two-point-source boundary, and final source-restriction corollary are correct. The original §1 claim needed a closedness qualification; the current wording supplies it. I find no remaining defect within the stated unit-old-price and decoded-law contracts.

## 1. Exact old-profile statement and the repaired qualification

With unit old attempt prices, an order `(i,j,k)` has mean

```math
C_{ijk}=1+m_i+m_{ij}+M m_{123}.
```

Subtract the equations for two laws with the same entire old profile. Comparing orders `(i,j,k)` and `(j,i,k)` shows that every singleton shift is a common value $`u`$. Each pair shift is consequently a common value $`v`$, and, when $`M>0`$, the terminal shift is $`-(u+v)/M`$. All Boolean moments determine the law, so the entire fiber has an affine parametrization by these two coordinates. The offsets of a possibly nonexchangeable reference law remain fixed; exchangeability is unnecessary here.

A nonempty **closed** convex restriction of the probability-simplex fiber has compact convex image $`K\subseteq\mathbb R^2`$. Its coordinate bounding-box center is in $`K`$: after normalizing nondegenerate coordinate ranges to $`[-1,1]`$, exclusion of the origin would give a strict separating inequality $`ax+by\ge\gamma>0`$. Coordinate reflections permit $`a,b\ge0`$. A point attaining $`x=-1`$ forces $`b>a`$, while a point attaining $`y=-1`$ forces $`a>b`$, a contradiction. Degenerate intervals reduce to a segment or point. Thus one permitted law attains every singleton and pair midpoint, including their fixed affine offsets.

**Objection SU-01, repaired.** The first draft said any nonempty convex restriction remained compact. Convexity alone does not imply this. The bounded convex set

```math
K=\{(x,y):x,y\ge0,\ x+y<1\}
```

has coordinate infima/suprema 0 and 1, but excludes its bounding-box midpoint $`(1/2,1/2)`$. A sufficiently small translated/scaled copy also fits inside the two-coordinate fiber of a strictly positive k3 law, so this is a substantive qualification for unrestricted convex restrictions. Earliest affected dependency: the compactness assertion in §1, before applying the planar lemma. Repair: require a nonempty closed convex restriction, or directly assume the resulting intersection is compact. The principal adopted the former wording. Finite closed-polyhedral sources already satisfy it; the interval example below was closed from the outset.

The displayed terminal-shift formula uses the unit old-price normalization. With a common old price $`c`$, it becomes $`-c(u+v)/M`$; the geometric conclusion is unchanged.

## 2. Exact source equivalence and all six revised means

On the stipulated exactly-one-failure support, the only probabilities are $`p_1,p_2,p_3`$, and an old order beginning with $`i`$ has mean $`1+p_i`$. With $`a=(1-\delta)/3`$, normalization and $`p_j,p_k\ge a`$ imply

```math
p_i\le1-2a=a+\delta.
```

Thus the six old-mean intervals, restricted to the declared support face, are exactly the three lower bounds $`p_i\ge a`$ and normalization. Conversely, these inequalities imply every displayed interval. Since $`\delta>0`$, setting $`z_i=(p_i-a)/\delta`$ gives exactly the full probability simplex, with no missing source points. The assumptions $`0<\delta\le1`$ ensure $`a\ge0`$.

Write $`\beta=1+\epsilon>0`$. Directly following the first attempt, and a second attempt only when the first fails, gives:

| Order | Revised mean |
|---|---|
| `(1,2,3)` | $`1+p_1`$ |
| `(1,3,2)` | $`1+\beta p_1`$ |
| `(2,1,3)` | $`1+p_2`$ |
| `(2,3,1)` | $`1+\beta p_2`$ |
| `(3,1,2)` | $`\beta+p_3`$ |
| `(3,2,1)` | $`\beta+p_3`$ |

There is no third attempt or terminal penalty on this support, so the argument indeed permits every $`M\ge0`$.

After subtracting the known offsets, these queries are $`\delta`$ times the coordinate directions with coefficients $`1,\beta,1,\beta,1,1`$. Taking the maximum query error gives weights $`(\alpha,\alpha,1)`$, where $`\alpha=\max(1,\beta)`$. Every coordinate endpoint is attained by a simplex vertex. Consequently, for a permitted decoded center $`z`$, its exact normalized worst error is

```math
R(z)=\max_i w_i\max(z_i,1-z_i),\qquad w=(\alpha,\alpha,1).
```

Taking the supremum over the source and maximum over the finite query list commutes. This establishes equality, without treating the three unknown probabilities as independent. Unrestricted coordinate midpoints attain radius $`\delta\alpha/2`$, and a largest-width query forces that lower bound.

## 3. Compatible radius, including both parameter regimes

Any feasible radius $`r=R(z)`$ satisfies $`r\ge\alpha/2`$. It also implies

```math
z_1,z_2\ge1-r/\alpha,\qquad z_3\ge1-r.
```

Summing and using $`\sum z_i=1`$ yields

```math
r\ge\frac{2\alpha}{\alpha+2}.
```

These lower-bound inequalities remain valid even when a right-hand side is negative, so the note's additional discussion of $`r\le1`$ is harmless but unnecessary.

For $`1\le\alpha\le2`$, the center

```math
z=\left(\frac\alpha{\alpha+2},\frac\alpha{\alpha+2},
\frac{2-\alpha}{\alpha+2}\right)
```

is in the simplex, all its coordinates are at most $`1/2`$, and all three weighted one-minus-coordinate errors equal $`2\alpha/(\alpha+2)`$. This attains both necessary bounds. For $`\alpha\ge2`$, $`z=(1/2,1/2,0)`$ has errors $`(\alpha/2,\alpha/2,1)`$, attaining radius $`\alpha/2`$. Therefore

```math
r_{\mathrm{compatible}}=
\delta\max\left\{\frac\alpha2,\frac{2\alpha}{\alpha+2}\right\}.
```

This is precisely the piecewise formula in §4. Both branches agree at $`\alpha=2`$. Its ratio to the free radius is $`4/(\alpha+2)`$ on $`[1,2]`$ and one thereafter. The statements for $`-1<\epsilon\le0`$, $`0<\epsilon<1`$, and $`\epsilon\ge1`$ follow exactly. At $`\epsilon=0`$, uncertain old means themselves are still being predicted; a positive coherence penalty there is consistent with the task's uncertain-source contract.

## 4. Rational example

For $`\delta=1/100`$, $`\epsilon=1/10`$, one has $`a=33/100`$, $`\alpha=11/10`$, and

```math
z=(11,11,9)/31,\qquad p=(1034,1034,1032)/3100.
```

The probability numerators sum to 3100. The lower bound is $`33/100=1023/3100`$, leaving nonnegative slacks $`(11,11,9)/3100`$. The old intervals are exactly $`[133/100,134/100]`$. The revised intervals are this same interval for orders `(1,2,3)` and `(2,1,3)`, $`[1363/1000,1374/1000]`$ for `(1,3,2)` and `(2,3,1)`, and $`[143/100,144/100]`$ for the orders beginning with 3.

At the compatible center, the normalized weighted errors are all $`22/31`$. Hence

```math
r_{\mathrm{free}}=\frac{11}{2000},\qquad
r_{\mathrm{compatible}}=\frac{22}{3100}=\frac{11}{1550},\qquad
\frac{r_{\mathrm{compatible}}}{r_{\mathrm{free}}}=\frac{40}{31}.
```

Every numerical assertion in §5 is exact.

## 5. Added §6: the nonconvex two-point source

For $`q_A=e_2`$, the exchangeable moment triple is $`(m_1,m_2,m_3)=(2/3,1/3,0)`$. For $`q_B=(5/6)e_0+(1/6)e_3`$, it is $`(1/6,1/6,1/6)`$. With $`M=4`$, both have every old mean equal to

```math
1+m_1+m_2+4m_3=2.
```

A single edited price contributes $`\epsilon`$, $`\epsilon m_1`$, or $`\epsilon m_2`$, according to whether the edited procedure is first, second, or third. The corresponding differences between the two laws are zero, $`\epsilon/2`$, and $`\epsilon/6`$. Thus the two revised-answer vectors have exact maximum-coordinate distance $`d=|\epsilon|/2`$.

Their unrestricted midpoint has radius $`d/2=|\epsilon|/4`$, and the triangle inequality supplies the matching lower bound. A decoded law in the declared two-point source must choose an endpoint and has worst error $`d=|\epsilon|/2`$. For nonzero admissible $`\epsilon`$, the factor-two ceiling is attained. The mixture realizes the unrestricted midpoint but is excluded by the source contract. The note correctly avoids extending this deterministic single-law conclusion to randomized expected-error criteria or to native convex-polytope sources.

## 6. Scope disposition

The interval-source result depends on the exactly-one-failure support face as well as the narrow old-mean intervals. It establishes an existence boundary for uncertain sources, and does not establish a penalty for the unrestricted noisy-summary fiber. The note expressly retains this distinction. The source is planar, but its query directions include all three simplex coordinates; the third is affine in the negative sum of the other two, so the exact-profile common-two-shift argument does not apply. For fixed $`\epsilon`$, both absolute radii vanish linearly with $`\delta`$; the strict relative gap is therefore compatible with the exact-data result.

## 7. Final corollary: compatible radius need not decrease under source restriction

This is the new paragraph in derivation 10 §10, not an additional claim about the unrestricted noisy-summary fiber. Keep its k4, M1, delta=1/200 example. The already checked triangle source P has normalized proper-moment image

```math
T=\mathrm{conv}\{(1,1,0),(1,0,1),(0,1,1)\}.
```

The law $`q_{\mathrm{free}}=(75,96,56,96,77)/400`$ has the same exact old profile and normalized proper coordinates $`c=(1/2,1/2,1/2)`$. For $`Q=\mathrm{conv}(P\cup\{q_{\mathrm{free}}\})`$, its query image is exactly $`\mathrm{conv}(T\cup\{c\})`$. Adding c neither increases nor decreases any coordinate range: all remain [0,1]. Hence the unrestricted radius for each source is delta/2=1/400. The law q_free is a permitted center for Q and attains this lower bound, proving its compatible radius is also 1/400. For P, the previously reconstructed sum-of-coordinates lower bound and centroid attain 2delta/3=1/300.

Thus P is a proper subset of Q and the compatible radius increases upon restricting Q to P, while unrestricted uncertainty stays unchanged for this query family. Both source sets remain compact, convex, rational and within the same exact old-summary fiber. The reason is precise: the minimization domain for the decoded center shrinks along with the set of possible true laws. A nonzero fixed single-price edit multiplies both radii by |epsilon| and preserves the strict inequality. This corollary is correct.

**Signed:** ChatGPT (GPT-6 Astra Pro), delegated independent hand audit. No principal time credited; no experiment, gate, or frozen-source changes.
