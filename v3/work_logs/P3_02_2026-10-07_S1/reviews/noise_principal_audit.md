# P3-02 — noise, coherent recovery and native-interface audit

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
**/root/scoring_sources**. Same-model internal, nonblind conceptual review.
No checker code was run for this audit. It owns no principal edit, status,
gate, clock or time-ledger decision; concurrent reviewer effort is not
additional principal research credit. All constructions remain development.

## 1. Snapshot and explicit scope

The principal's current **sections 12–13** were audited from this snapshot:

| File | SHA-256 |
|---|---|
| v3/derivations/02_probability_information.md | 817bafd86e5f8e06797b24b967f0c6640b1b81783ae712e1ebf8c7f8467fea24 |
| v3/foundations/01_representation_boundaries.md | 2b8cc22c9f4f33cfd254936ffa91f63a7102736ee1df1cc073ba6b552f02a6d8 |
| v3/literature/02_probability_sources.md | bb0a6779471c248d6aeab1d54f59f712e71c6df1c89d5dd13a06db188f764afa |
| v3/work_logs/P3_02_2026-10-07_S1/reviews/noise_conditioning_case.md | 9e8097a7207c9a94d84c4f63fdfac255d3b92136fbb7e6f6aa6fe85d885627c4 |

The native assumptions were compared with the inherited representation
boundary and the selected core/rule/native-reconstruction passages it
references. This audit checks mathematical interpretation and displayed
calculations. It does not certify the execution counts, replay every receipt,
or independently establish the fourteen development LP regimes.

**Finding:** the scalar modulus, exact conditioning formula, coordinate
center formulas, numerical calibration example and native examples are
correct under their declared interfaces. Two small assumptions should be
made explicit:

1. In PI-13, require the error set $`E`$ to be **nonempty** as well as
   compact, so the global feasible source and displayed maximum exist.
2. Describe the compatible-center problem as convex when **the actual
   fiber $`F_z`$ is convex**. Convexity of $`P`$ alone does not suffice
   if $`E`$ is nonconvex. For a finite union of native polyhedral cases,
   enumerate cases or use an explicitly disjunctive procedure; it is not
   automatically one LP.

Two further service boundaries are established in §§5–6: randomization
cannot bypass a common-optimum obstruction to zero regret, but can reduce
positive minimax regret; and one scalar optimal risk can identify a binary
law, whereas a continuous scalar cannot identify the full simplex when
$`n\geq3`$. Both results include direct proofs.

## 2. PI-13 and the exact conditioning case

### 2.1 The pair modulus

With nonempty compact $`P,E`$, known finite linear maps $`L,c`$, and the
Cartesian source $`P\times E`$, each feasible fiber
```math
F_z=\{p\in P:z-Lp\in E\}
```
is nonempty compact. Two laws share an observation if and only if
```math
L(p-q)\in E-E.
```
Indeed, equality of observations says
$`Lp+e_p=Lq+e_q`$, or $`L(p-q)=e_q-e_p`$; the converse uses the
witnesses in the difference set.

The midpoint of the extreme scalar targets on each fiber has maximum
error half their separation, even if the intermediate scalar values do
not themselves come from compatible laws. Every pair sharing that
observation imposes the matching lower bound. The pair-feasible set is
compact because $`E-E`$ is compact; it is nonempty because it includes
$`p=q`$. Thus the principal's maximum, rather than merely a supremum,
is justified.

No convexity, symmetry of $`E`$, or stochastic noise distribution is
required for this free scalar result. The principal now correctly
describes $`P\times E`$ as a deterministic Cartesian premise, rather
than statistical independence. A law-dependent observation mechanism
requires its actual pair relation.

### 2.2 The $`L_\delta`$ radius is exact

For
```math
L_\delta=
\begin{bmatrix}0&1&1\\0&1&1+\delta\end{bmatrix},
\qquad \delta>0,\quad |e_j|\leq\epsilon,
```
let $`a=2\epsilon`$, orient the pair so
$`r=p_3-q_3\geq0`$, and write
```math
h=p-q=(-t,t-r,r).
```
The probability-difference condition is
```math
0\leq r\leq1,\qquad r-1\leq t\leq1,
```
while overlap of the two observation boxes requires
```math
-a\leq t\leq a-\delta r.
```
The intersection is nonempty exactly when
```math
r\leq1,\qquad \delta r\leq2a,\qquad
(1+\delta)r\leq1+a.
```
Consequently
```math
R_\delta(\epsilon)=\frac12
\min\left\{1,\frac{4\epsilon}{\delta},
\frac{1+2\epsilon}{1+\delta}\right\}.
```

The principal's matching construction is valid:
```math
t=\min(0,2\epsilon-\delta r),\quad
q=e_2,\quad p=(-t,1-r+t,r),
\quad z=(L_\delta p+L_\delta q)/2.
```
It gives probability vectors, admissible errors and target separation
equal to the upper bound. The pointwise interval formulas (34) agree
with the independent projection calculation in noise_conditioning_case.md.

The displayed principal example also checks. At
$`\delta=2,\epsilon=2/5`$, the maximum target separation is $`3/5`$.
Take $`p=(2/5,0,3/5)`$, $`q=e_2`$, and
$`z=(4/5,7/5)`$. The two exact observation vectors are
$`(3/5,9/5)`$ and $`(1,1)`$; both are within the declared box around
$`z`$. The radius is $`3/10`$, below the simple inversion bound $`2/5`$.

The $`\delta=0`$ and zero-noise cases are correctly stated separately.
The fixed-$`\delta`$ inverse bound alone does not establish a statistical
penalty for protocols retaining paired or shared-error information.

## 3. Coherent and free centers

### 3.1 The maximum-coordinate formulas are correct

On any nonempty compact fiber $`F`$, let
```math
a_j=\min_{p\in F}C_jp,\qquad b_j=\max_{p\in F}C_jp.
```
For an arbitrary vector answer $`v`$,
```math
\sup_{p\in F}\|v-Cp\|_\infty
=\max_j\{v_j-a_j,\ b_j-v_j\}.
```
This follows by exchanging the finite coordinate maximum with the
supremum and considering each coordinate's extreme values. Hence
```math
r_{\rm free}=\max_j(b_j-a_j)/2.
```
The complete set of free minimax centers is the box
```math
\prod_j[b_j-r_{\rm free},\,a_j+r_{\rm free}].
```

If the answer must be $`Cq`$ for one compatible law $`q\in F`$, the
principal's formula
```math
r_{\rm coh}=\min_{q\in F}\max_j\{C_jq-a_j,\ b_j-C_jq\}
```
and its intersection criterion for equality with $`r_{\rm free}`$ follow
immediately. Compactness ensures attainment. The general factor-two bound
also follows here: any compatible answer is at most the target-set diameter
from any other compatible target, and that diameter in this norm equals
$`2r_{\rm free}`$.

For $`F=\Delta_3,C=I`$, the unrestricted radius is $`1/2`$. A compatible
law of radius $`r`$ must satisfy $`q_i\geq1-r`$ for every $`i`$;
normalization implies $`r\geq2/3`$, attained at the uniform law. This
correctly shows a coherence penalty despite a convex fiber.

For a scalar target and convex fiber, averaging laws attaining the two
extremes gives a compatible scalar midpoint. The multidimensional gap
does not contradict that scalar fact. The principal correctly limits its
half-width vector formula to the unweighted maximum-coordinate norm.

### 3.2 Convexity must refer to the actual fiber

The objective in the compatible-center minimization is convex and
piecewise affine in $`q`$, but the feasible set also matters.
Both $`P`$ and $`E`$ convex imply $`F_z`$ convex. Convex $`P`$ by itself
does not.

For example, on $`\Delta_2`$, retain $`Lp=p_1`$, let
$`E=\{-1/2,1/2\}`$, and observe $`z=1/2`$. Then
```math
F_z=\{(1,0),(0,1)\}.
```
For the scalar target $`p_1`$, the free radius is $`1/2`$, but every
compatible answer has radius one. The source $`P`$ is convex; the
nonconvex error set created a nonconvex fiber.

Suggested algorithm sentence:

> If the actual fiber is a nonempty compact polytope, the compatible-center
> problem is an LP after computing the coordinate extrema. On a compact
> convex fiber it is a convex optimization problem. A finite union of
> polyhedral cases can be handled case by case, with the stated coverage
> and computational costs.

For such a finite union, first obtain coordinate extrema over the whole
union. Then minimize the resulting center objective on each compatible
case and choose the best case optimum. Convexifying a source just to use
one LP may change which answers count as compatible.

### 3.3 Calibration and source reuse

The shared-bias example is correct: normalization identifies the common
bias, while replacing it by separate error intervals loses that relation.
The noisy-scale interval $`[6/11,10/13]`$, its two affine certificates,
midpoint $`94/143`$, radius $`16/143`$, and the normalized-observation
worst error $`4/33`$ all check algebraically. The separately known-scale
interval $`[7/12,3/4]`$ uses an additional premise and is appropriately
distinguished.

The source-reuse conclusion is also sound. A selected compatible estimate
does not justify discarding other compatible laws. Likewise, a simultaneous
coverage premise can control the unconditional event of a false selected
conclusion without guaranteeing the same error rate after conditioning on
acceptance. These are limits of the declared information, not statistical
guarantees supplied by the deterministic calculations.

## 4. Native interpretation in section 13

### 4.1 Directed-unit binary example

The stipulated equations give $`y=1+4p`$ with $`2\leq y\leq3`$, hence
the semantic bounds $`1/4\leq p\leq1/2`$. With only a declared
$`P\to U`$ map, the corresponding native conclusions initially remain
in loss unit $`U`$.

The target-$`P`$ reduct retains only $`0\leq p\leq1`$; its assignment
$`p=3/4,y=5/2`$ refutes $`p\leq1/2`$ while satisfying that reduct.
It is deliberately not a model of the full loss-unit source. This is the
correct distinction for the inherited reduct obstruction. An explicit
reciprocal conversion or an external semantic adapter supplies a different
authorized interpretation route. No reverse conversion follows from the
positive numerical factor alone.

### 4.2 Finite matrix example

The normalization and two retained means have determinant four and the
unique law $`(1/4,1/2,1/4)`$. The identity
```math
p_1=(3/2)s-(1/2)\ell_1-(1/2)\ell_2
```
is correct. The three appropriately oriented source inequalities, with
nonnegative weights $`3/2,1/2,1/2`$, certify the upper bound $`p_1\leq1/4`$.
Opposite equality orientations certify the lower bound. This explains how
signed rowspace coefficients are implemented without an invalid
negative-multiplier inference.

The interpretation requires the legitimate unit transport and source
validation already stated. A numerical row identity alone does not grant
the checker access to otherwise unavailable premises.

### 4.3 Ratios, open domains and finite affine syntax

Under a justified $`v_i=sp_i`$ interpretation and positive
$`S=\sum_i v_i`$, the fixed-threshold equivalence
```math
p_i\geq t\quad\Longleftrightarrow\quad tS-v_i\leq0
```
is correct. Its right side is an affine loss-unit query for rational fixed
$`t`$; the returned probability interpretation still uses the external
calibration semantics.

The distinction between global $`s>0`$ and a native closed positive-margin
case is correct. A finite union of closed polyhedra cannot project to the
entire open positive half-line; projections of these finite polyhedra remain
polyhedral and closed. An actual positive rational bound or concretely
checked positive observation supplies the local domain needed for the
ratio adapter. This does not make variable division a native term.

The independently bounded-payoff projection is an exact special-purpose
elimination. It gives affine constraints after the proof in section 11;
it does not license a graph of arbitrary uncertain products. The principal
keeps fixed known coefficients, variable optimization, rational literals
and general exact-real constants distinct.

The code-execution paragraph reports separate development evidence. This
conceptual audit neither reran those checks nor audited the stated
acceptance/rejection counts.

## 5. Randomized decisions: exact and approximate service

Let $`\mathcal A`$ be a finite nonempty original action menu, with finite
loss rows $`c_a`$, and let $`F`$ be a nonempty compatible law set. At law
$`p`$, put
```math
m(p)=\min_{b\in\mathcal A}c_bp,\qquad
r_a(p)=c_ap-m(p)\geq0.
```
A randomized action distribution $`\lambda\in\Delta_{\mathcal A}`$ has
worst-compatible **expected** regret
```math
\mathcal R_F(\lambda)
=\sup_{p\in F}\sum_a\lambda_a r_a(p).
\tag{R1}
```
The expectation is over the action draw. The law is chosen without access
to that private draw; $`\lambda`$ depends only on the retained observation.
The underlying law is not changed by the action report.

### 5.1 Zero regret has exactly the common-optimum requirement

For any such distribution,
```math
\mathcal R_F(\lambda)=0
\quad\Longleftrightarrow\quad
\mathrm{supp}\lambda
\subseteq
\bigcap_{p\in F}\mathrm{argmin}_{a\in\mathcal A}c_ap.
\tag{R2}
```
If the supremum is zero, then at each $`p`$ a sum of nonnegative terms
$`\lambda_ar_a(p)`$ is zero. Every action with positive weight must
therefore have zero regret at every compatible law. Conversely, a mixture
supported on common optima has zero regret everywhere.

The support is nonempty, so there exists a zero-regret randomized answer
if and only if there exists a common optimal original action. Consequently,
allowing these randomized answers does not relax the exact common-optimum
criterion on a fiber, or its fixed-linear information consequence in PI-9.
This concerns the zero expected-regret service under (R1); it is not a
universal restriction on every randomized acquisition or decision criterion.

### 5.2 Positive minimax regret can strictly improve

With no information on $`\Delta_2`$, take
```math
c_A=(0,1),\qquad c_B=(1,0),
```
and choose $`A`$ with probability $`\lambda`$.
The two pure laws give regrets $`1-\lambda`$ and $`\lambda`$.
At any intermediate law, regret is a convex piecewise-affine function of
the law, so neither exceeds the larger endpoint value. Thus
```math
\mathcal R_{\Delta_2}(\lambda)=\max(\lambda,1-\lambda).
```
Every deterministic choice has worst regret one. The half-half mixture
has worst expected regret $`1/2`$, the minimum. There is no common pure
optimum, so the improvement remains strictly above zero, as (R2) requires.

If an adversary observes the realized action and then chooses its law,
the relevant order becomes
$`\sum_a\lambda_a\sup_{p\in F}r_a(p)`$; this example then gives one.
The order of information and expectation is therefore part of the service.
Randomization access and its costs also need a declared operational model.

For a finite polytope with vertices $`p^k`$, this randomized regret problem
has an ordinary LP:
```math
\min_{\lambda,t}t,\quad
\lambda\geq0,\quad\mathbf1^\top\lambda=1,\quad
\sum_a\lambda_a(c_a-c_b)p^k\leq t
\quad\text{for every }b,k.
```
This follows from
mixed regret $`=\max_b(\sum_a\lambda_ac_a-c_b)p`$ and maximizing the
resulting linear pieces at vertices. A fixed rational mixture gives an
affine expected-loss row; solving for a mixture and granting its
operational meaning remain separate from a native inference rule.

## 6. One scalar optimal risk: a scoped positive and obstruction

### 6.1 Binary shifted Brier is identifying

Let $`p=\Pr(Y=1)`$ and use reports $`q\in[0,1]`$ with
```math
\ell(q,Y)=(q-Y)^2+2Y.
```
Its exact expected risk is
```math
R_p(q)=(q-p)^2+3p-p^2.
```
The unique optimum is $`q=p`$. The scalar Bayes risk
```math
H(p)=3p-p^2
```
is strictly increasing on $`[0,1]`$, since its derivative is $`3-2p>0`$.
An exact optimal-risk observation $`h\in[0,2]`$ therefore identifies
```math
p=\frac{3-\sqrt{9-4h}}2.
\tag{R3}
```
This is a known outcome-dependent shift common to all reports. It changes
the information in the absolute risk while leaving every report preference
and the truthful optimum unchanged.

The interpretation requires the exact risk, known semantic score and
certified optimum. An arbitrary achieved or realized score does not
automatically have the form $`H(p)`$. Computing or finding the optimum is
not free access to it.

The numeric inverse in (R3) uses a nonlinear square root. For a fixed
rational threshold $`t\in[0,1]`$, monotonicity instead gives
```math
p\geq t\quad\Longleftrightarrow\quad h\geq3t-t^2.
```
That is an affine query in $`h`$ after an explicit semantic monotonicity/
optimal-risk adapter; it does not place the uncertain quadratic graph in
the native language.

### 6.2 Continuous scalar summaries cannot identify the full higher simplex

Here is an elementary proof with an explicit continuity premise. Suppose
$`n\geq3`$ and $`H:\Delta_n^\circ\to\mathbb R`$ is continuous. Choose an
interior point $`u`$ and two independent tangent directions $`v,w`$.
For sufficiently small $`\rho>0`$, every point
```math
p_\theta=u+\rho(\cos\theta\,v+\sin\theta\,w)
```
lies in the interior. The points $`p_\theta`$ and $`p_{\theta+\pi}`$
are distinct because $`v,w`$ are independent. Define
```math
g(\theta)=H(p_\theta)-H(p_{\theta+\pi}).
```
This is continuous on $`[0,\pi]`$, and $`g(\pi)=-g(0)`$.
If $`g(0)=0`$, there is already a collision; otherwise the intermediate
value theorem gives a zero between the two endpoints. Thus two distinct
interior laws have the same scalar value.

This proves nonidentification for this full-law service. It does not
exclude scalar representations of a restricted one-dimensional law family,
a scalar target property, a decision label, or a discontinuous encoding.

Under PI-7's finite-score truthful-optimum assumptions, the Bayes risk is
in fact continuous on the interior. It is finite there and is concave,
being the infimum of the affine risks $`p\mapsto p^\top\ell(q)`$.
A short local justification avoids an additional unproved regularity import:
choose a small closed cube in relative coordinates entirely inside the
simplex interior. Concavity bounds $`H`$ below by the minimum of its
finitely many corner values, while one fixed finite score row bounds it
above by an affine function. On a smaller concentric cube, extend any
line through two points a fixed additional distance inside the larger
cube and apply concavity in both directions. The two finite bounds give
a constant times the distance as a bound on the value difference.
Hence $`H`$ is locally Lipschitz and continuous.

Therefore a scalar Bayes risk in that finite-score class cannot identify
every law for $`n\geq3`$, although the binary construction above can.
The obstruction uses only a two-dimensional interior slice and the
intermediate value theorem; it is not an unqualified theorem that one
real number cannot encode multiple real parameters.

## 7. Integration disposition

PI-13 and the native interpretation are conceptually sound with the two
explicit-premise refinements in §1. The randomized and optimal-risk cases
are useful additional service boundaries, with direct constructive and
negative proofs. They are ordinary finite decision/scoring comparisons,
not a contribution-gate determination, an empirical learning result or an
extension of the inherited grammar.

No conclusion in this review applies automatically to revisions made after
the recorded snapshot hashes.
