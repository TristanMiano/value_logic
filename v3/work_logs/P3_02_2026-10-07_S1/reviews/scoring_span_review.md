# P3-02 — strict score span and nuisance calibration review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
**/root/scoring_sources**. Same-model internal, nonblind review. This note owns
no clock, ledger, status, gate, principal-file or publication decision.
Concurrent reviewer effort is not additional principal research credit.
All examples and arguments remain development material.

## 1. Disposition and source scope

The proposed quotient-span proposition is correct. There are two useful
sharpenings:

1. With known absolute score vectors, **$`n-1`$ suitably selected raw expected
   scores already suffice**. A baseline plus $`n-1`$ other raw scores is a
   sufficient way to evaluate a preselected difference basis, rather than the
   minimum raw-query count.
2. For $`n\geq2`$, the score differences themselves span $`\mathbb R^n`$.
   This stronger affine-span result gives exact recovery even with an unknown
   common positive scale and unknown common offset, using $`n+1`$ raw expected
   scores. That raw count is sharp for fixed probes and the full interior law
   class with unrestricted common nuisance parameters.

These are elementary reconstructions/adaptations of ordinary finite scoring
and linear-measurement geometry. No exact numbered antecedent for either
span formulation was located in the narrowly inspected sources; that is not
a novelty or priority claim. This note sharpens the query-count discussion in
the earlier reviewer note, scoring_sources.md §5.

Primary sources inspected again for this review:

| Source | Exact locator and imported scope |
|---|---|
| [Gneiting and Raftery (2007), Strictly Proper Scoring Rules, Prediction, and Estimation](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf) | §2.1 equations (1)–(2), printed p.360: strict propriety and positive scaling plus a report-common outcome term. §3.1 Definition 2/Theorem 2, p.362, and Examples 1/3, p.363: finite categorical regularity, convex representation, Brier and log scores. The paper uses maximized rewards; this note negates them to use minimized losses. |
| [Frongillo and Kash (2015), On Elicitation Complexity](https://raf.prof/media/papers/elic-complex.pdf) | §2 Definitions 1–3 and 5–7, pp.2–3: properties, elicitation, identification and links. The paragraph following Definition 7 distinguishes unrestricted encodings from restricted dimension comparisons. §2.1 Proposition 2/Lemma 1, pp.3–4: finite-law and linear-property comparisons. These supply comparison interfaces; their general complexity lower bounds are not imported here. |

The definitions, displayed statements and selected proofs at those locators
were accessible. No additional historical or worldwide-priority search was
performed. Proofs and nuisance-query lower bounds below are supplied directly.

## 2. Exact proposition and assumptions

Let there be $`n`$ labeled outcomes. Write
```math
\Delta_n^\circ=\{p\in\mathbb R^n:p_i>0,\ \mathbf1^\top p=1\}.
```
Let $`Q`$ be a common report domain containing each $`p\in\Delta_n^\circ`$
as a distinct report. For every $`q\in Q`$, its semantic loss vector
$`\ell(q)`$ lies in $`\mathbb R^n`$. For a single fixed law across reports,
```math
R_p(q)=p^\top\ell(q).
```
Assume that for **every** interior law $`p`$, the unique global minimizer of
$`R_p`$ over the same domain $`Q`$ exists and is the report $`q=p`$.
No differentiability, continuity, boundedness uniform in $`q`$, or convexity
of the loss as a function of the report is needed for the following proofs.

### 2.1 Quotient-span proposition

For every fixed $`q_0\in Q`$,
```math
\mathrm{span}\!\left(
\{\mathbf1\}\cup\{\ell(q)-\ell(q_0):q\in Q\}
\right)=\mathbb R^n. \tag{S1}
```

If this failed, some nonzero $`d`$ would annihilate every displayed vector.
In particular $`\mathbf1^\top d=0`$. At any interior $`p`$, sufficiently
small $`t>0`$ gives two distinct interior laws $`p_\pm=p\pm td`$. For every
report,
```math
R_{p_+}(q)-R_{p_-}(q)
=2t\,d^\top\ell(q_0),
```
which is independent of $`q`$. The two risk surfaces therefore have exactly
the same minimizers. Strict propriety requires different unique minimizers
$`p_+`$ and $`p_-`$, a contradiction.

This statement includes $`n=1`$, where normalization alone determines the law
and no query is necessary.

### 2.2 Stronger full affine-span proposition

For $`n\geq2`$, under the same assumptions,
```math
\mathrm{span}\{\ell(q)-\ell(q_0):q\in Q\}
=\mathbb R^n. \tag{S2}
```

Suppose instead that a nonzero $`z`$ annihilates all differences, so
$`z^\top\ell(q)=c=z^\top\ell(q_0)`$ for every report. If
$`\mathbf1^\top z=0`$, the proof of (S1) applies. Otherwise put
```math
w=\frac{z}{\mathbf1^\top z},\qquad \mathbf1^\top w=1.
```
The coordinates of $`w`$ need not be nonnegative. Choose any interior law
$`p\ne w`$, which is possible because $`n\geq2`$, and choose
$`0<t<1`$ sufficiently small that $`p_t=(1-t)p+tw`$ remains interior.
Then for all reports
```math
R_{p_t}(q)=(1-t)R_p(q)+t\frac{c}{\mathbf1^\top z}.
```
This is a positive affine transformation of the entire report objective.
Its unique optimizer is therefore unchanged. Strict propriety requires
the distinct reports $`p_t`$ and $`p`$, again a contradiction.

Thus the semantic loss vectors have full affine hull. Finite-dimensional
linear algebra selects $`n`$ linearly independent differences from the
possibly infinite score family. This is an existence result; it does not
give an efficient search procedure or a condition-number bound for the
selected rows.

The $`n\geq2`$ restriction on (S2) is real: for $`n=1`$, take a single report
with one finite loss. Strict propriety is vacuous, but every score difference
is zero.

## 3. Raw scores, differences and query counts

For known exact absolute scores, (S1) implies
```math
\mathrm{span}\bigl(\{\mathbf1\}\cup\{\ell(q):q\in Q\}\bigr)
=\mathbb R^n.
```
Consequently $`n-1`$ raw rows can be selected independent modulo constants.
Their expectations and normalization identify every $`p\in\Delta_n`$.
Fewer than $`n-1`$ fixed scalar linear measurements cannot identify all
interior laws: the measurement matrix augmented by $`\mathbf1^\top`$
then has a nonzero tangent kernel.

A preselected difference basis $`d_j=\ell(q_j)-\ell(q_0)`$, $`j<n`$, can
instead be evaluated by $`n-1`$ direct difference observations or $`n`$ raw
observations including the baseline. The baseline is not intrinsically free.
Conversely, retaining those particular $`n-1`$ nonbaseline raw scores need
not work. For three-outcome Brier loss, use baseline $`q_0=e_1`$, and
reports $`q_1=e_2`$, $`q_2=(1/3,1/3,1/3)`$. The two differences form a
basis modulo constants, but the second raw score is constant $`2/3`$;
the two nonbaseline raw scores fail to identify the law. Selecting raw
reports $`e_1,e_2`$ does identify it.

For the nuisance model in §4, the sharp **fixed raw-probe** counts are:

| Common transformation knowledge | Minimum raw scores for all interior laws, $`n\geq2`$ | Sufficient rows |
|---|---:|---|
| Scale $`s\ne0`$ and offset $`b`$ known | $`n-1`$ | Raw rows independent modulo constants |
| Scale $`s\ne0`$ known; offset $`b`$ unknown | $`n`$ | A baseline and $`n-1`$ differences independent modulo constants |
| Scale $`s>0`$ unknown; offset $`b`$ known | $`n`$ | $`n`$ linearly independent raw score rows |
| Both $`s>0`$ and $`b\in\mathbb R`$ unknown | $`n+1`$ | A baseline and $`n`$ linearly independent score differences |

Every sufficient row selection exists under strict propriety, by (S1)–(S2).
The final two counts concern recovery of $`p`$, even if recovering the
nuisance parameters is not separately requested. They are not merely counts
of formally unknown parameters; kernel obstructions establish necessity.
Special individual fibers, restricted law families, external anchors or
additional known nuisance relations can require fewer measurements.

**Direct-difference interface.** An observation of the transformed risk
difference $`v(q)-v(q_0)`$ cancels a common offset. An oracle that instead
applies its affine transformation anew to a constructed difference gamble
may return $`s\,E_p[\ell(q)-\ell(q_0)]+b`$, which has not cancelled the
offset. Counts using direct differences must declare which operation is
available and account for its actual cost.

## 4. Recovery under an unknown shared scale and offset

Assume all observations satisfy the same stipulated model
```math
v_j=s\,\ell(q_j)^\top p+b,\qquad s>0,\quad b\in\mathbb R,
\tag{S3}
```
with the same $`p,s,b`$ for every report. The semantic base vectors
$`\ell(q_j)`$ are known; arbitrary untyped value numbers do not supply them.
Set $`x=sp`$. Choose $`q_0,\ldots,q_n`$ so that the matrix
```math
D=
\begin{bmatrix}
(\ell(q_1)-\ell(q_0))^\top\\
\vdots\\
(\ell(q_n)-\ell(q_0))^\top
\end{bmatrix}
```
is invertible, as (S2) permits. Then
```math
x=D^{-1}
\begin{bmatrix}v_1-v_0\\ \vdots\\v_n-v_0\end{bmatrix},
\quad
s=\mathbf1^\top x,\quad
p=\frac{x}{\mathbf1^\top x},\quad
b=v_0-\ell(q_0)^\top x. \tag{S4}
```
Compatibility requires $`x\geq0`$ and $`\mathbf1^\top x>0`$. The same
decoder identifies boundary laws as well: strict propriety on the interior
was used to establish rank, not to assume the eventual law has full support.
This recovers the scalar common offset; if it arose as $`E_p[h(Y)]`$, it
does not recover the full outcome-dependent vector $`h`$.

### 4.1 Necessity for fixed raw probes

Take any fixed $`k\leq n`$ raw score rows $`r_j^\top=\ell(q_j)^\top`$,
with $`k\geq1`$, and use $`r_1`$ as the baseline. Their difference matrix
has $`k-1<n`$ rows, hence a nonzero kernel vector $`h`$. Choose $`x>0`$
not parallel to $`h`$, possible when $`n\geq2`$. For sufficiently small
nonzero $`t`$, $`x'=x+th>0`$. Let
```math
s=\mathbf1^\top x,\quad p=x/s,\qquad
s'=\mathbf1^\top x',\quad p'=x'/s',
```
and set $`b'=b-t\,r_1^\top h`$. Then every raw observation is identical:
```math
r_j^\top x'+b'
=r_j^\top x+b+t(r_j-r_1)^\top h
=r_j^\top x+b.
```
But $`p'\ne p`$, because $`h`$ is not parallel to $`x`$. Thus no decoder
can recover every interior law from these $`k`$ raw scores. The argument
allows any fixed report choice and any decoder, including a nonlinear one.
With zero observations the obstruction is immediate.

The other lower bounds in §3 use the same argument with the appropriate
known quantities held fixed. If $`s`$ is known and $`b`$ is not, choose a
nonzero $`h`$ annihilating both normalization and all row differences.
If $`b`$ is known and $`s`$ is not, use a kernel vector of the raw-row
matrix and choose $`x>0`$ not parallel to it. If both are known, use
the raw-row matrix augmented by normalization.

### 4.2 Binary Brier construction and confounding

For two-outcome Brier loss, with $`p=p_1`$, the reports $`e_1,e_2,u=(1/2,1/2)`$
have losses $`(0,2),(2,0),(1/2,1/2)`$. Their transformed risks satisfy
```math
v_1=2s(1-p)+b,\qquad v_2=2sp+b,\qquad v_u=s/2+b.
```
The three observations give
```math
s=v_1+v_2-2v_u,\qquad
b=v_u-s/2,\qquad
p=(v_2-b)/(2s).
```
Two vertex risks alone fail: both
$`(p,s,b)=(1/4,1,2)`$ and $`(3/8,2,1)`$ produce
$`(v_1,v_2)=(7/2,5/2)`$. All scales and offsets in this example are
positive. The uniform-report observation separates the two cases.

### 4.3 Ordinary anchors and failure of shared semantics

For any loss-measurement family, two constant-loss anchors
$`c_0\ne c_1`$ observed under (S3) give
```math
s=\frac{v(c_1)-v(c_0)}{c_1-c_0},\qquad
b=v(c_0)-sc_0.
```
After those two queries, $`n-1`$ indicator expectations recover a law.
Alternatively, a zero-loss anchor gives $`v_0=b`$, and all $`n`$ exhaustive
indicator observations $`v_i=sp_i+b`$ give
```math
s=\sum_{i=1}^n(v_i-v_0),\qquad
p_i=(v_i-v_0)/s.
```
These reproduce the ordinary normalization/anchor construction in principal
§3. A zero anchor plus only $`n-1`$ indicator values generally leaves scale
confounded with the unmeasured final category.

The shared transformation is substantive. With unknown separate report
offsets, any candidate law can be fitted by
$`b_j=v_j-s\,\ell(q_j)^\top p`$. With unknown outcome multipliers,
```math
v(q)=\sum_i a_i p_i\ell(q,i)+b,
```
even the entire score surface identifies only $`x_i=a_i p_i`$ before
additional assumptions. For example,
```math
p=(1/4,3/4),\ a=(2,2/3)
\quad\hbox{and}\quad
p'=(1/2,1/2),\ a'=(1,1)
```
both give $`x=(1/2,1/2)`$ and hence identical observations for every report.
This is probability/stakes confounding that additional reports alone do not
remove. A report-common additive outcome term is different: its expectation
is one common scalar offset at a fixed $`p`$, so report differences cancel it.
If the law or nuisance transformation changes across queries, (S3) no longer
describes the transcript.

## 5. Qualifications on reports, infinities and approximation

**Different report coordinates.** Literal equality $`q=p`$ is not essential.
An injective truthful report map $`r(p)`$, with $`r(p)`$ the unique global
optimizer for each interior $`p`$, gives both span proofs unchanged.
Pairwise disjoint, nonempty full argmin sets for different laws also suffice.
Merely choosing a different element of one shared tie set using
knowledge of $`p`$ does not establish recovery from the score surface.

For a noninjective property the conclusion can fail. On outcomes with
numeric labels $`c=(0,1,2)`$, squared loss
$`\ell(r,i)=(r-c_i)^2`$ uniquely elicits the mean $`c^\top p`$.
The distinct interior laws
$`(1/4,1/2,1/4)`$ and $`(1/3,1/3,1/3)`$ have the same mean.
Every score difference lies in $`\mathrm{span}\{\mathbf1,c\}`$,
which is smaller than $`\mathbb R^3`$. This is a useful ordinary
task-specific representation, not a failure of property elicitation.

**Global law class and common reports.** Propriety only at one law, or on a
finite or lower-dimensional set of laws, does not justify these full-simplex
conclusions. Allowing each law a different feasible report domain also
breaks the same-minimizer argument. The outcome law must remain fixed while
reports are compared; an intervention-dependent law is a different problem.

**Log boundaries and infinite vectors.** The real-vector span statements
cannot directly include $`+\infty`$ or $`-\infty`$ entries, or cancellation
of infinite expectations. For the ordinary logarithmic loss, restrict probes
to positive reports, for which every loss entry is finite. Every interior
truth remains admissible and uniquely optimal there, so both propositions
apply. Full-rank positive-report probes can subsequently recover boundary
laws, despite the boundary honest report being excluded from this finite
query domain. Recovery does not require the infimum at that boundary law to
be attained within the positive reports.

Gneiting–Raftery's categorical regularity explicitly permits infinite penalty
only at an outcome assigned probability zero, so its truthful interior rows
are finite. For a more general extended-real score, first exhibit a finite
subdomain retaining the required interior optimizer property. Without such
a reduction, do not state the displayed linear-algebra results for its
infinite score vectors.

**Weak or approximate propriety.** The constant loss $`\ell(q,i)=0`$
is weakly proper and satisfies any positive-tolerance “truth is approximately
optimal” statement, but carries no probability information. Exact uniqueness
therefore cannot be silently replaced by approximate truthful optimality.
Likewise, uniqueness for each interior law provides no quantitative
conditioning guarantee: multiplying Brier loss by arbitrarily small
$`\alpha>0`$ preserves both spans while magnifying inversion sensitivity.

A quantitative conclusion needs an explicit margin. If
```math
R_p(q)-R_p(p)\geq\phi(d(q,p)),
```
the risk estimate is uniformly within $`\eta`$, and its chosen report has
optimization gap at most $`\delta`$, then
```math
\phi(d(\widehat q,p))\leq2\eta+\delta.
```
This follows by comparing the estimated risks of $`\widehat q`$ and $`p`$.
For $`\alpha`$-scaled Brier, $`\phi(t)=\alpha t^2`$ in Euclidean distance.
These are additional error/margin premises, not consequences of the labels
“learned value” or “approximately unique.”

Nuisance normalization adds another sensitivity. If $`x=sp`$ and an estimate
$`\widehat x=x+e`$ has $`\|e\|_1\leq\epsilon<s`$, then its normalized vector
satisfies
```math
\left\|\frac{\widehat x}{\mathbf1^\top\widehat x}-p\right\|_1
\leq\frac{2\epsilon}{s-\epsilon}.
```
Feasibility of that vector as a probability law must also be checked.
Obtaining $`\epsilon`$ requires error control through the selected inverse
$`D^{-1}`$; without a positive lower bound on scale, there is no uniform
robust guarantee over (S3).

## 6. Integration boundaries

The strongest useful statement here is a finite exact information theorem,
with constructive calibration and sharp fixed-probe obstructions. It concerns
known outcome-contingent score contracts and exact expectations for a fixed
law, under a shared transformation. It does not identify external truth from
subjective expectations, certify learned estimates, infer a generating law
from one realized score, or establish a learning/convergence duty.

Indeed, evaluating every selected score on the same realized outcome $`Y`$
gives the same algebra with $`x=s e_Y`$. The decoder returns the one-hot
empirical law $`e_Y`$, regardless of the generating law. Full rank and
successful nuisance calibration therefore do not establish that the inputs
were exact subjective expectations.

The numerical recovery maps involve inversion and normalization. Fixed known
rational inverse coefficients can be compiled as affine operations. Division
by an unknown recovered scale is not automatically available in the native
finite piecewise-affine language. Under a separately certified positive scale,
fixed rational probability-threshold comparisons can be cross-multiplied into
affine inequalities. The mathematical information result and the permitted
representation/operation result should remain separate.

Recommended attribution is **reconstructed finite consequence of ordinary
strict propriety; adapted to an explicit score-query and nuisance-calibration
interface**. The propositions can strengthen the ordinary comparison and
the scoped P3-02 artifact without asserting priority, superiority, or a
contribution-gate outcome.

Development verification: the two binary Brier nuisance cases and their
three-query decoders were checked with exact rational arithmetic. The span
and lower-bound claims are supported by the displayed hand proofs. This
is internal development verification, not an independent or frozen test.
