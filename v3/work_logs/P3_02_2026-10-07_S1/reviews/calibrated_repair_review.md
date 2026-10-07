# Calibrated target-repair count: internal hostile review

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Status: **accepted conditional characterization and direct reconstruction**, with an explicit distinction between target recovery and recovery of every nuisance parameter. This is an internal same-model review of a proposed P3-02 extension. The arithmetic checks are DEVELOPMENT evidence. This work adds no principal clock credit and makes no claim of a new learning method, scientific contribution, or worldwide priority.

## 1. Exact scope and disposition

Let $`n\ge1`$, $`p\in\Delta_n`$, $`L\in\mathbb Q^{m\times n}`$ be the old fixed known loss rows, and $`C\in\mathbb Q^{k\times n}`$ be the target rows. The task is to recover the whole vector $`Cp`$ exactly for every law in the full normalized simplex. An empty target matrix is allowed and denotes the vacuous target.

Additional queries may use arbitrary fixed known rational loss rows. Every old and new query refers to the **same law** and the **same nuisance parameters**. The four observation contracts, after removing any known offset and known nonzero scale, are:

| Contract | Raw values |
|---|---|
| Known units | $`v=Lp`$ |
| Unknown common offset | $`v=Lp+b\mathbf1_m`$, $`b\in\mathbb R`$ |
| Unknown common positive scale | $`v=sLp`$, $`s>0`$ |
| Unknown common positive affine transformation | $`v=sLp+b\mathbf1_m`$, $`s>0,\ b\in\mathbb R`$ |

The count concerns additional scalar raw queries. It does not charge for linear combinations, exact rational algebra, or decoding; nor does it declare every specified semantic payoff available in an actual application. Queries are fixed before observing the law-dependent values. Negative finite payoffs are allowed. A restricted admissible menu, adaptive acquisition, noise, a restricted source $`P`$, or query-specific nuisance parameters requires a separate contract.

**Disposition:** The proposed count is correct for this scope. It follows from the existing finite normalized-expectation and positive-scale characterizations plus a quotient-dimension argument. The construction is rational and attains the lower bound. No arbitrary nonlinear decoder avoids the bound, because the underlying recovery criteria already quantify over arbitrary decoders.

## 2. Constants must be handled first

If every row of $`C`$ is constant across outcomes, the target is known from normalization. Writing $`c_i=\gamma_i\mathbf1_n^\top`$ gives $`c_i p=\gamma_i`$, so the minimum number of additional queries is **zero**, regardless of $`L`$ or either nuisance.

This includes:

- an empty target matrix;
- any collection of zero, duplicate, or differently scaled constant targets;
- every linear target when $`n=1`$, including the full law $`p=(1)`$.

The remainder assumes at least one target row is nonconstant. In particular, it assumes $`n\ge2`$. Requiring the constant row to be observed in a scale-unknown problem before making this check would overcount a trivial target.

## 3. Effective rows and the proposed formula

When the offset is known, set $`M=L`$.

When the offset is unknown and $`m\ge1`$, choose any old reference row $`L_0`$ and set

```math
M=D_L=
\begin{pmatrix}
L_1-L_0\\
\vdots\\
L_{m-1}-L_0
\end{pmatrix}.
```

When the offset is unknown and $`m=0`$, set $`M`$ to the empty matrix with $`n`$ columns. With $`m=1`$, the same empty effective matrix results, but the existing raw reference is available; these two cases have different additional-query counts.

If scale is known, define

```math
B=\begin{pmatrix}\mathbf1_n^\top\\M\end{pmatrix},
\qquad
R=C,
\qquad
r=\mathrm{rank}\begin{pmatrix}B\\R\end{pmatrix}
  -\mathrm{rank}B.
\tag{1}
```

If scale is unknown, define

```math
B=M,\qquad
R=\begin{pmatrix}\mathbf1_n^\top\\C\end{pmatrix},
\qquad
r=\mathrm{rank}\begin{pmatrix}B\\R\end{pmatrix}
  -\mathrm{rank}B.
\tag{2}
```

Then the exact minimum number of additional raw queries is

```math
\boxed{
r+\mathbf1\{\text{offset unknown and }m=0\}.
}
\tag{3}
```

Equation (3) is applied only after the constants-only exception in Section 2.

The reference choice does not affect the result. All differences from any chosen old reference span the same space of pairwise old-row differences.

## 4. Why these are the required row spaces

For a completed fixed menu $`F`$, the known-unit finite-simplex result gives

```math
Cp\text{ recoverable from }Fp
\quad\Longleftrightarrow\quad
\mathrm{row}C
\subseteq
\mathrm{row}\begin{pmatrix}\mathbf1_n^\top\\F\end{pmatrix}.
\tag{4}
```

The constant row is free information here because $`\mathbf1_n^\top p=1`$.

For unknown scale, the nonconstant-target family version of the scale characterization gives

```math
Cp\text{ recoverable from }sFp
\quad\Longleftrightarrow\quad
\mathrm{row}\begin{pmatrix}\mathbf1_n^\top\\C\end{pmatrix}
\subseteq\mathrm{row}F.
\tag{5}
```

At least one nonconstant row forces the constant-payoff combination to be available, hence forces scale recovery. Once that combination is available, each nonconstant target row must also be in the retained row space; constant target rows are then included automatically.

With an unrestricted unknown offset, differencing retains exactly the law information: if two completed differenced records agree, their reference coordinates can be matched by changing the offset. Thus (4) or (5) applies to the completed difference matrix $`D_F`$. A reference coordinate does not contribute additional law information independently of those differences.

These are global full-simplex criteria. Particular boundary observations may identify more, and a smaller decision service may require less, but neither changes the count for the stipulated linear target vector at every law.

## 5. Lower bound

### 5.1 Known offset, or an old reference already exists

If the offset is known, each new raw loss row adds at most one row-space dimension to $`M=L`$.

If the offset is unknown and an old reference $`L_0`$ exists, a new raw row $`a`$ contributes exactly the new effective difference $`a-L_0`$. It again adds at most one dimension to $`M=D_L`$.

In either case, $`t`$ new raw queries can enlarge the effective base span by at most $`t`$. For target recovery, the completed base must include the whole required row space $`R`$. Therefore its dimension must be at least

```math
\dim\mathrm{row}\begin{pmatrix}B\\R\end{pmatrix}
=\dim\mathrm{row}B+r,
```

so $`t\ge r`$.

This bound does not assume that a decoder is affine or fractional-linear. Those forms are constructive consequences of the stated observation model. The impossibility of a smaller menu comes from (4) or (5), which already rules out any exact decoder when its corresponding inclusion fails.

### 5.2 Unknown offset with no old rows

A nonconstant target cannot be recovered from no observations. If $`t\ge1`$ new raw rows are acquired, choose one as reference. Their effective difference matrix has at most $`t-1`$ rows.

With known scale, the required dimension is

```math
\mathrm{rank}\begin{pmatrix}\mathbf1_n^\top\\C\end{pmatrix}=1+r,
```

while the completed augmented difference matrix has rank at most $`1+(t-1)=t`$. Hence $`t\ge r+1`$.

With unknown scale, the completed difference matrix must contain $`\mathbf1_n^\top`$ and all target rows, whose joint rank is $`r`$. Since its rank is at most $`t-1`$, again $`t\ge r+1`$.

The first raw query supplies a reference, and at most each subsequent query supplies one effective row. Its exact semantic payoff need not be zero for this lower bound.

## 6. Construction achieving the bound

Start from the row span of $`B`$. Iterate through the required rows $`R`$, retaining a row $`q`$ only if appending it increases the span accumulated so far. Let the selected rows be $`q_1,\ldots,q_r`$. Ordinary exact row-space extension gives precisely $`r`$ selected rows and

```math
\mathrm{row}R
\subseteq
\mathrm{row}\begin{pmatrix}B\\q_1\\\vdots\\q_r\end{pmatrix}.
```

All selected rows are rational because the required rows are rational. No irrational basis choice is needed.

Acquire raw loss rows as follows:

| Existing information | Added raw rows |
|---|---|
| Offset known | $`q_1,\ldots,q_r`$ |
| Offset unknown, old reference $`L_0`$ exists | $`L_0+q_1,\ldots,L_0+q_r`$ |
| Offset unknown, no old row | First $`0`$, then $`q_1,\ldots,q_r`$ |

In the second case, the difference between the new record and the reference record is $`q_jp`$ or $`s q_jp`$, exactly as required. In the third case, the zero row provides the reference value $`b`$, after which each difference is again the desired effective observation.

If a selected $`q_j`$ were to generate a raw row identical to an existing row, its effective difference would already be in the old effective row span. It could not have been selected as a rank-increasing row. Duplicate required rows and constants therefore do not cause accidental extra queries.

For known scale, each target has a rational coefficient identity

```math
c_i=\gamma_i\mathbf1_n^\top+\beta_i M_{\mathrm{final}},
```

so its expected value is $`\gamma_i+\beta_i z`$, where $`z`$ is the completed effective observation, divided by a known nonunit scale first if needed.

For unknown positive scale, there are rational coefficient identities

```math
\alpha M_{\mathrm{final}}=\mathbf1_n^\top,\qquad
\beta_i M_{\mathrm{final}}=c_i.
```

The exact admissible effective observation is $`z=sM_{\mathrm{final}}p`$, giving

```math
\alpha z=s>0,\qquad
c_i p=\frac{\beta_i z}{\alpha z}.
\tag{6}
```

These identities form a constructive, exact rational certificate of the retained target and the needed scale calibration. They do not make the division in (6) a native finite piecewise-affine operation on jointly uncertain quantities.

The minimum is thus attained in every case, including empty, zero, or duplicate old rows.

## 7. Target dimension and full-law specializations

With no old queries, let

```math
d_C=\mathrm{rank}\begin{pmatrix}\mathbf1_n^\top\\C\end{pmatrix}-1.
```

If the target family is nonconstant, $`1\le d_C\le n-1`$. The from-scratch counts become:

| Contract | Minimum additional raw queries |
|---|---:|
| Known units | $`d_C`$ |
| Unknown offset | $`d_C+1`$ |
| Unknown positive scale | $`d_C+1`$ |
| Unknown positive affine transformation | $`d_C+2`$ |

This makes the target-specific nature explicit: the required dimension is the number of target directions modulo known constants, not automatically the dimension of the full probability law.

For full-law recovery on $`n\ge2`$, set $`C=I_n`$, so $`d_C=n-1`$. The counts are respectively $`n-1,n,n,n+1`$, agreeing with the earlier calibration table. On the one-outcome simplex, the full law is constant and all four counts are zero.

When an old menu exists, the full-law gap is $`n-\mathrm{rank}[\mathbf1_n^\top;M]`$ with known scale and $`n-\mathrm{rank}M`$ with unknown scale; only the no-old-reference offset case incurs the extra reference query.

## 8. Rational examples and nontrivial edge cases

For three outcomes, write $`e_i`$ for the event-indicator rows, $`\mathbf1=(1,1,1)`$, and $`0=(0,0,0)`$. Counts below use the order known units, unknown offset, unknown positive scale, unknown positive affine transformation.

| Old rows $`L`$ | Target rows $`C`$ | Four counts |
|---|---|---|
| Empty | $`e_1`$ | $`1,2,2,3`$ |
| $`e_1`$ | $`e_1`$ | $`0,1,1,2`$ |
| $`0,0`$ | $`e_1`$ | $`1,1,2,2`$ |
| $`\mathbf1`$ | $`e_1`$ | $`1,1,1,2`$ |
| $`0,\mathbf1`$ | $`e_1`$ | $`1,1,1,1`$ |
| $`e_1,e_2`$ | $`e_1`$ | $`0,1,1,2`$ |
| $`e_1,e_2,e_3`$ | $`e_1`$ | $`0,0,0,1`$ |
| Empty | $`e_1,e_2`$ | $`2,3,3,4`$ |
| Empty | $`e_1,\ 2e_1+\mathbf1,\ 4\mathbf1`$ | $`1,2,2,3`$ |

Several details are exposed by these examples:

- An old zero row contributes no linear rank but is an available offset reference. A second identical zero does not help further.
- An old constant-one row already calibrates an unknown common scale when the offset is known. With unknown offset, that single raw row supplies only a reference.
- Merely repeating an existing raw row yields no new information. If $`L_0=e_1`$, acquiring $`2e_1`$ under known scale and unknown offset gives the new difference $`e_1p`$, whereas another copy of $`e_1`$ would not.
- An old full event-indicator vector under unknown positive scale and offset lacks one calibration direction. One extra zero row suffices: differences give $`sp`$, whose sum gives $`s`$.
- Affine dependence among the target rows is counted correctly. The last family needs only one nonconstant expectation under known units.

### Target recovery need not recover the offset

The count repairs the target service. It must not be described as always recovering every nuisance parameter.

Take old reference $`L_0=e_2`$, target $`C=e_1`$, unknown common positive scale and offset, and add the two raw rows

```math
e_2+\mathbf1=(1,2,1),\qquad e_2+e_1=(1,1,0).
```

The two differences give $`s`$ and $`sp_1`$, so the target and scale are identified. But consider

```math
p=(1/2,1/4,1/4),\quad s=2,\quad b=0,
```

```math
q=(1/2,1/8,3/8),\quad s=2,\quad b'=1/4.
```

Both give the same complete raw observation

```math
(1/2,5/2,3/2).
```

Their offsets differ because the reference expectation $`p_2`$ is not itself retained by the effective target summary. Thus offset recovery would be a stronger requirement. The same issue can occur with known scale and unknown offset. Appending the target-repair queries preserves the old raw information, but does not automatically decode every old absolute expected loss.

## 9. Development checks and certificate review advice

An inline exact-rational Python check compared the proposed formula with a separately expressed binary geometric enumeration:

- Old menus were all multisets of zero through three rows drawn from $`\{-1,0,1\}^2`$: 220 old menus, including empty, zero, negative, and duplicate rows.
- The nonconstant target was $`p_1`$.
- The candidate appended rows were $`0,e_1,e_2`$; all eight subsets were searched for a smallest sufficient extension.
- Sufficiency was tested directly by binary geometry: a nonconstant row for known units; two raw rows with unequal outcome contrasts for unknown offset; two linearly independent raw rows for unknown scale; or three affinely noncollinear raw rows for unknown scale and offset.
- These geometric criteria were evaluated using integer comparisons and determinants. The proposed general count used a separate exact rational Gaussian-elimination rank routine.

All **880 nonconstant contract checks** agreed with the count. In addition, 880 constant-family cases and 880 empty-family cases returned zero, 16 one-outcome cases returned zero, and the nine three-outcome fixtures in Section 8 matched the stated counts.

The observed distributions of minimum additional queries over the 220 binary old menus were:

| Contract | Zero queries | One query | Two queries | Three queries |
|---|---:|---:|---:|---:|
| Known units | 200 | 20 | 0 | 0 |
| Unknown offset | 176 | 43 | 1 | 0 |
| Unknown positive scale | 152 | 64 | 4 | 0 |
| Unknown positive affine transformation | 76 | 116 | 27 | 1 |

The partial-target/unknown-offset collision above also passed exact rational substitution.

This enumeration checks a finite two-outcome fragment and named rational examples. It does not replace the dimension proof or establish arbitrary-dimensional completeness by testing.

For a reusable rational certificate companion, the load-bearing checks are the constants-only branch, the exact base and final ranks, the selected rank-increasing required rows, the raw-to-effective reference relation, and exact coefficient identities for each target and any scale-calibrating row. The no-old-reference query must be counted explicitly. Decimal tolerances should not determine these exact ranks.

A certificate can establish what would follow from declared exact expected-loss observations. It cannot certify that supplied values are expectations rather than realized losses, make an unavailable payoff query physically available, or provide a uniform noise bound as $`s`$ approaches zero. These remain separate scientific and representation assumptions.

## 10. Attribution and conclusion

This is an exact target-specific extension of the finite retention/repair argument across four declared calibration contracts. Its mathematical content is reconstructed from the known-unit row-space criterion, the positive-scale target obstruction, common-offset differencing, and elementary basis extension. It is suitable for a scoped constructive certificate companion.

No counterexample was found to the proposed count under its assumptions. The substantive correction is to keep **target calibration** separate from **complete nuisance recovery**: a nonconstant target under unknown positive scale necessarily reveals the scale, while an unknown offset may remain confounded with an unretained reference expectation.
