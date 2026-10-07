# P3-02 internal review — unknown scales, offsets and probability information

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **proved conditional characterizations; internal same-model hostile
checking and reconstruction**. This note checks the principal's conjecture,
states its necessary qualifications and gives rational witnesses. It claims
no new scientific contribution, adds no principal-session clock credit, and
changes no primary artifact, task status or gate.

## 1. Scope and service

Let $`n\geq2`$, let
```math
\Delta_n=\{p\in\mathbb R^n:p\geq0,\ \mathbf1_n^\top p=1\},
```
and let $`L\in\mathbb R^{m\times n}`$ be a fixed, known finite loss
matrix. The target is the exact scalar expectation $`cp`$, for a fixed
known row $`c\in\mathbb R^{1\times n}`$. A nonconstant target means
$`c\notin\mathrm{span}\{\mathbf1_n^\top\}`$.

The observation is
```math
v=sLp,\qquad s>0,
```
where the common scale $`s`$ is unknown and may take any positive value.
Global recovery requires one decoder with output $`cp`$ for every
admissible pair $`(p,s)`$. These are exact observations with their stated
semantics, not learned estimates or realized losses.

Every constant target $`c=\gamma\mathbf1_n^\top`$ is trivially
recoverable, with output $`\gamma`$, for every $`L`$. It must therefore
be excluded from the proposed nonconstant-target necessity claim.

## 2. Unknown positive scale: the conjecture is correct

### Theorem 1

For every nonconstant $`c`$, $`cp`$ is globally recoverable from $`sLp`$
on $`\Delta_n\times(0,\infty)`$ if and only if
```math
\boxed{\mathbf1_n^\top\in\mathrm{row}L
\quad\text{and}\quad c\in\mathrm{row}L.}
```

**Sufficiency.** Choose known rows $`\alpha,\beta`$ with
$`\alpha L=\mathbf1_n^\top`$ and $`\beta L=c`$. Then
```math
\alpha v=s>0,\qquad \beta v=s\,cp,\qquad
cp=\frac{\beta v}{\alpha v}.
```
The constant-payoff combination calibrates the scale.

**Necessity of the constant-payoff combination.** If
$`\mathbf1_n^\top\notin\mathrm{row}L`$, there is
$`h\in\ker L`$ with $`H=\mathbf1_n^\top h\ne0`$.
Because $`c`$ is nonconstant, choose $`p\in\mathrm{ri}\Delta_n`$
such that
```math
ch-Hcp\ne0.
```
Such a choice must exist: otherwise $`cp=ch/H`$ at every interior
law, and hence, by continuity at the vertices, all entries of $`c`$
would be equal.

For sufficiently small nonzero $`t`$, all coordinates of $`p+th`$
and the denominator $`1+tH`$ are positive. Define
```math
p_t=\frac{p+th}{1+tH},\qquad s_t=s(1+tH)>0.
```
The law $`p_t`$ is normalized, and
```math
s_tLp_t=sL(p+th)=sLp.
```
However,
```math
cp_t-cp=\frac{t(ch-Hcp)}{1+tH}\ne0.
```
Thus the same observation has two admissible target values.

**Necessity of the target row.** Now suppose
$`\mathbf1_n^\top\in\mathrm{row}L`$, but
$`c\notin\mathrm{row}L`$. There is $`h\in\ker L`$ with
$`ch\ne0`$, and every such $`h`$ has
$`\mathbf1_n^\top h=0`$. Small perturbations $`p\pm th`$ of an
interior law remain normalized and have the same $`Lp`$, but different
values of $`cp`$. Using the same positive scale gives the obstruction.
$`\square`$

An equivalent way to see the problem is to put $`x=sp`$. The admissible
homogeneous vector satisfies $`x\geq0`$, $`x\ne0`$, and the observation
becomes the linear map $`v=Lx`$. The target is the ratio
```math
\frac{cx}{\mathbf1_n^\top x}.
```
The proof shows that a nonconstant ratio of this particular form can be
identified on the entire nonnegative cone only when both its numerator
and denominator rows are retained.

### Consequences and constructive positive cases

- Full-law recovery holds iff $`\mathrm{rank}L=n`$.
  A left inverse recovers $`x=sp`$, after which
  $`s=\mathbf1_n^\top x`$ and $`p=x/s`$.
- If even one nonconstant linear target is globally identified, the common
  scale is also identified. If the constant row is absent, the only
  globally recoverable linear targets are constants.
- A target family $`Cp`$ consisting entirely of constant rows is trivial.
  Otherwise, global recovery requires the constant row and every row of
  $`C`$ to belong to $`\mathrm{row}L`$.
- With $`L=I_n`$, the values $`v_i=sp_i`$ give
  $`s=\sum_i v_i`$ and $`p_i=v_i/\sum_jv_j`$.
- A supplied constant-payoff row is another calibration: if
  $`L`$ contains $`\mathbf1_n^\top`$ and $`c`$, their observed values
  are $`s`$ and $`scp`$, whose ratio recovers the target.

Thus one extra independent linear observation can matter: full-law recovery
needs augmented rank $`n`$ with a known scale, but rank $`n`$ of $`L`$
itself when the scale is unknown.

## 3. Unknown common offset as well

Suppose
```math
v=sLp+b\mathbf1_m,\qquad s>0,\quad b\in\mathbb R,
```
with the same unrestricted offset in every observation coordinate. Choose
a reference row $`L_0`$, and define
```math
D=\begin{pmatrix}L_1-L_0\\ \vdots\\ L_{m-1}-L_0\end{pmatrix},
\qquad
z=\begin{pmatrix}v_1-v_0\\ \vdots\\v_{m-1}-v_0\end{pmatrix}=sDp.
```
For $`m=1`$, $`D`$ and $`z`$ are empty.

These differences retain exactly the information available about $`p`$
after allowing an unrestricted offset. In particular, if
$`sDp=tDq`$, then observations for $`(p,s,b)`$ and $`(q,t,b')`$
agree after choosing
```math
b'=b+sL_0p-tL_0q.
```
Hence the omitted reference coordinate cannot resolve a collision of
the differenced observation.

### Corollary 2

For a nonconstant linear target:
```math
\boxed{
cp\text{ recoverable from }sLp+b\mathbf1_m
\iff
\mathbf1_n^\top,c\in\mathrm{row}D.
}
```
If $`\alpha D=\mathbf1_n^\top`$ and $`\beta D=c`$, then
```math
s=\alpha z,\qquad cp=\frac{\beta z}{\alpha z}.
```
Full-law recovery holds iff $`\mathrm{rank}D=n`$. It therefore
requires at least $`n+1`$ raw scalar observations in this fixed-matrix
model. With full-law recovery, the scale and then the offset are recovered
as well.

A constructive full-law example uses the zero-payoff row followed by
the $`n`$ event-indicator rows. The zero row gives $`v_0=b`$, and
```math
v_i-v_0=sp_i,\qquad
s=\sum_{i=1}^n(v_i-v_0),\qquad
p_i=\frac{v_i-v_0}{s}.
```
For a single target, rows $`0,\mathbf1_n^\top,c`$ give
```math
cp=\frac{v_c-v_0}{v_{\mathbf1}-v_0}.
```

### Known scale, unknown offset

If the nonzero scale $`s`$ is known, the exact condition instead is
```math
\boxed{
c\in\mathrm{row}
\begin{pmatrix}\mathbf1_n^\top\\D\end{pmatrix}.
}
```
Indeed, $`c=\gamma\mathbf1_n^\top+\beta D`$ yields
$`cp=\gamma+\beta z/s`$. The ordinary normalized-simplex kernel
obstruction proves necessity.

For example, $`L=I_n`$ and known $`s`$ give
```math
b=\frac{\sum_i v_i-s}{n},\qquad
p_i=\frac{v_i-b}{s}.
```
With both $`s,b`$ unknown, that same $`n`$-entry matrix is insufficient
for any nonconstant linear target: its difference rows sum to zero and
cannot span $`\mathbf1_n^\top`$.

## 4. Optional general additive nuisance: use a complete quotient

For known $`B\in\mathbb R^{m\times r}`$ and unrestricted
$`\theta\in\mathbb R^r`$, consider
```math
v=sLp+B\theta.
```
Choose a matrix $`N`$ whose rows span the complete left nullspace of $`B`$.
Equivalently,
```math
NB=0,\qquad \ker N=\mathrm{im}B.
```
Then $`Nv=sNLp`$, and equality of these quotient observations is
equivalent to the original signal difference being removable by a nuisance
shift. Consequently:

- With unknown $`s>0`$, a nonconstant target is globally recoverable iff
  $`\mathbf1_n^\top,c\in\mathrm{row}(NL)`$.
- With known nonzero $`s`$, it is recoverable iff
  $`c\in\mathrm{row}([\mathbf1_n^\top;NL])`$.
- Full-law recovery with unknown scale requires and is implied by
  $`\mathrm{rank}(NL)=n`$.

The completeness condition matters. Merely choosing any $`N`$ with
$`NB=0`$ gives a potentially lossy reduction, whose criterion is
sufficient but need not be necessary. For example, take a common offset
on three observations and loss rows
```math
(0,0),\quad(1,0),\quad(0,1).
```
Both differences from the first row form $`I_2`$ and identify the law
under unknown positive scale. Keeping only the first difference also
annihilates the offset, but discards the information required to calibrate
that scale.

Restrictions or dependencies on nuisance parameters need their own fiber
analysis. The equivalences above use the stated unrestricted additive
nuisance range and a common positive scale.

## 5. Normalizing nonnegative loss observations

Let $`L\geq0`$ entrywise, and define the column-sum row
```math
u^\top=\mathbf1_m^\top L.
```
Then
```math
w(p)=\frac{Lp}{\mathbf1_m^\top Lp}
=\frac{Lp}{u^\top p}
```
is defined at every $`p\in\Delta_n`$ **iff every column sum $`u_j`$
is strictly positive**. Necessity is tested at the vertices; sufficiency
follows from $`u^\top p\geq\min_j u_j>0`$.

Under this condition, equality of two normalized observations is precisely
positive proportionality of the two unnormalized observations:
```math
w(p)=w(q)
\iff
Lp=\frac{u^\top p}{u^\top q}Lq.
```
These are exactly the unknown-positive-scale fibers. Theorem 1 therefore
applies unchanged to recovery from $`w`$: a nonconstant linear target
requires $`\mathbf1_n^\top,c\in\mathrm{row}L`$, and full-law
recovery requires $`\mathrm{rank}L=n`$.

Although $`w`$ is a normalized vector on measurement coordinates, it is
generally not the original outcome law. Its ordinary probability
decomposition is informative. Set
```math
U=\mathrm{diag}(u_1,\ldots,u_n),\quad
M=LU^{-1},\quad
r=\frac{Up}{u^\top p}.
```
The columns of $`M`$ sum to one, $`r\in\Delta_n`$, and
```math
w=Mr,\qquad
p=\frac{U^{-1}r}{\mathbf1_n^\top U^{-1}r}.
```
Thus normalization first reweights the state probabilities by known
column totals and then applies an ordinary stochastic matrix. The
reweighting is bijective when all $`u_j>0`$; rank remains the
full-law obstruction. This is a reconstruction of the probability
comparison, not a new probability semantics.

If a nonnegative matrix has a zero column sum, normalization is undefined
at that state's pure law. One may restrict the domain or add an explicit
zero-signal symbol, but must state the change.

For signed matrices, normalizing by the coordinate sum need not even
preserve positive-ray information. With $`L=(-1,1)`$, the scalar
observation $`v=s(1-2p_1)`$ retains its sign. Dividing by its own value
gives $`w=1`$ whenever nonzero and loses that sign. A fixed-sign nonzero
denominator is needed for the normalization equivalence; nonnegativity
and positive column sums provide it in the stated case.

## 6. Decisions can survive when every nonconstant linear target fails

### Positive scale alone: a nonnegative, everywhere-normalizable example

Take action losses
```math
L=\begin{pmatrix}0&1&2\\1&0&1\end{pmatrix}
=\begin{pmatrix}c_A\\c_B\end{pmatrix}.
```
The constant row is not in its row space. A combination giving one in
the first two coordinates would require coefficient one on each row,
but would give three in the third coordinate.

By Theorem 1, **no nonconstant linear target $`cp`$ is globally
recoverable from $`sLp`$**. Nevertheless, choosing the smaller observed
entry is exactly Bayes-optimal:
```math
\mathrm{argmin}(v_A,v_B)
=\mathrm{argmin}(c_Ap,c_Bp).
```
This is a nonconstant decision rule, since
```math
(c_A-c_B)p=1-2p_1.
```
Choose $`A`$ when $`p_1>1/2`$, $`B`$ when $`p_1<1/2`$, and either
at equality. The observation preserves this threshold and its tie
without recovering the numerical value of $`p_1`$ globally.

A strictly interior rational collision is
```math
p=(3/5,1/5,1/5),\quad s=1,
```
```math
q=(11/18,1/9,5/18),\quad t=9/10,
```
for which
```math
sLp=tLq=(3/5,4/5).
```
In particular, $`p_1\ne q_1`$, while action $`A`$ is optimal at both.
The kernel witness is $`h=(-1,-2,1)`$, with
$`\mathbf1^\top h=-2`$.

The column sums are $`(1,1,3)`$, all positive. The normalized
observation is the same at both laws:
```math
w=(3/7,4/7).
```
The example therefore applies to normalized nonnegative loss vectors
without any excluded zero-denominator law.

Adding an unrestricted common offset does not affect the preserved
action ranking either. It cannot restore the lost linear targets.

### Unknown scale and offset: event indicators retain their ordering

Take $`L=I_3`$, with $`v=sp+b\mathbf1_3`$. Difference rows have
coordinate sum zero, so Corollary 2 rules out every nonconstant linear
target. Nonetheless, all coordinate rankings of $`p`$, including ties,
are exactly retained by the common positive affine transformation.

For example,
```math
p=(1/2,1/3,1/6),\quad s=1,\ b=0
```
and
```math
q=(5/9,1/3,1/9),\quad t=3/4,\ b'=1/12
```
give the same vector $`v=(1/2,1/3,1/6)`$, with all probabilities
strictly positive. The full order and the minimizing action for these
indicator losses are preserved, while the laws differ.

These examples distinguish information sufficient for an ordinal
decision from recovery of a specified linear expectation. They do not
contradict the known-scale sign-crossing result, whose information
map is the fixed linear observation $`Lp`$ without nuisance scaling.

## 7. Assumptions and limits that affect the conclusion

1. **Global versus local.** The impossibility concerns one decoder valid
   everywhere. Particular observations can identify more. For example,
   with nonnegative loss columns $`(1,0),(0,1),(1,1)`$, observing a
   positive multiple of $`(1,0)`$ forces the first pure law, despite
   failure of global identification.
2. **A strictly positive scale.** If $`s=0`$ is admitted, the observation
   at that scale is independent of $`p`$, destroying every global
   nonconstant target regardless of matrix rank. Unknown negative scales
   would also invalidate the direct preference-preservation argument.
3. **Known payoff matrix and common nuisances.** Different unknown scales
   on different entries, unknown payoff rows, or constrained nuisance
   relationships are different observation contracts.
4. **Exact identification is not a stability guarantee.** Even a full-rank
   matrix can have arbitrarily small raw observations as $`s\to0`$.
   Fixed absolute measurement error can then be amplified by the scale
   normalization. No uniform noise guarantee is asserted here.
5. **Information recovery is not native representability.** The decoder
   generally divides jointly variable quantities. Replacing $`sp`$ by
   a homogeneous coordinate makes the observation linear, but does not
   make its normalization an existing phase-two affine operation.
   Known rational coefficients or known scale supplied per request have
   a different native-language status.
6. **Expectation typing remains necessary.** Applying these formulas to
   realized score vectors can recover a realized one-hot outcome, rather
   than the subjective law whose expectations were intended. Matrix
   compatibility alone supplies no evidence about that interpretation.

The separate [scoring-span review](scoring_span_review.md) provides
conditions under which finitely many exact expected-score differences can
have full rank. The nuisance characterization here concerns what those
declared linear observations retain once their matrix is fixed.

## 8. Exact development checks

A standard-library rational calculation verified both numerical collisions,
the scale example's kernel witness and its normalized vector. It also
checked that every probability in both supplied pairs is strictly positive.
The results were:

- Scale example: identical $`v=(3/5,4/5)`$ and normalized
  $`w=(3/7,4/7)`$; $`Lh=0`$ and $`\mathbf1^\top h=-2`$.
- Scale-plus-offset example: identical
  $`v=(1/2,1/3,1/6)`$.

These are development checks only. The proofs give the general conditions;
the examples do not establish a learning result or a contribution claim.
