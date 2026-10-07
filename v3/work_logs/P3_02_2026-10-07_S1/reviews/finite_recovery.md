# P3-02 internal review — finite recovery

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **internal same-model independent reconstruction**. The proofs below
reconstruct finite linear algebra, convex geometry and decision theory. They
claim no novelty or independent-model corroboration. This review contributes
no separate time credit to the principal session and attempts no gate.

Read against the P3-01 problem contract, V01–V03 in its desiderata, its
representation boundaries, and the P3-02 session work log. All guarantees below
are conditional on the stated semantic loss matrix, domain and observation
interpretation. Exact expected losses, learned estimates and realized losses
must not be substituted for one another.

## 1. Start with the requested service and its fibers

Let the finite outcome set have size $`n`$, let
```math
\Delta_n=\{p\in\mathbb R^n:p\geq0,\ \mathbf1^\top p=1\},
\qquad L\in\mathbb R^{m\times n},
```
and observe the exact expected-loss vector $`y=Lp`$. The payoffs in $`L`$
are known. Write
```math
A=\begin{pmatrix}\mathbf1^\top\\L\end{pmatrix},\qquad
b(y)=\begin{pmatrix}1\\y\end{pmatrix}.
```
For a declared nonempty admissible set $`P\subseteq\Delta_n`$, define
$`F_P(y)=\{p\in P:Lp=y\}`$.

For any requested exact answer $`g(p)`$, a decoder $`d`$ satisfying
$`d(Lp)=g(p)`$ on $`P`$ exists **if and only if $`g`$ is constant on
every nonempty fiber**. Necessity follows by giving a decoder the same
input twice; sufficiency defines its output to be the fiber's common value.
This is a set-theoretic service characterization. It supplies neither an
efficient decoder nor a permitted encoding.

For a linear target $`g(p)=Cp`$, the equivalent domain-sensitive condition is
```math
(P-P)\cap\ker L\ \subseteq\ \ker C.
```
The left side uses actual differences of admissible laws. Replacing it
unconditionally by $`\mathrm{span}(P-P)\cap\ker L`$ is too strong.

## 2. Exact global recovery on the full real simplex

### Theorem 1: full-law and target-loss recovery

On all of $`\Delta_n`$:

1. $`p`$ is recoverable from $`Lp`$ iff $`\ker A=\{0\}`$, equivalently
   $`\mathrm{rank}A=n`$.
2. A specified vector $`Cp`$ is recoverable iff
   $`\ker A\subseteq\ker C`$, equivalently every row of $`C`$ belongs
   to the row space of $`A`$.
3. In the second case there are a known vector $`\alpha`$ and matrix $`B`$
   with $`C=\alpha\mathbf1^\top+BL`$. Hence
   

```math
   Cp=\alpha+By.
   
```
   Thus the existence of an arbitrary exact decoder for this linear target
   already implies the existence of an affine decoder on the feasible image.

**Proof.** A difference of two laws in one fiber lies in $`\ker A`$.
Conversely, every $`h\in\ker A`$ can be scaled to a difference of two
laws in one fiber: take the strictly positive uniform law $`u`$, and choose
$`\epsilon>0`$ small enough that $`u\pm\epsilon h\geq0`$. Both laws
are normalized and have the same $`L`$-image. Therefore any nonzero
$`h\in\ker A`$ refutes full recovery, and any $`h\in\ker A`$ with
$`Ch\neq0`$ refutes target recovery. The converses are immediate.
Finally, $`(\ker A)^\perp`$ is the row space of $`A`$. This gives the
factorization and decoder. $`\square`$

The statement includes $`n=1`$. The normalization row is essential: $`n-1`$
independent event-indicator expectations can recover an $`n`$-outcome law.
For example $`y_i=p_i`$ for $`i<n`$ gives
$`p_n=1-\sum_{i<n}y_i`$.

If arbitrary known linear loss observables may be chosen, the smallest number
needed for the exact target $`Cp`$ is
```math
\mathrm{rank}\begin{pmatrix}\mathbf1^\top\\C\end{pmatrix}-1.
```
The row-space inclusion proves the lower bound; a basis modulo the constant
row attains it. This counts linear expectation observables on the full real
simplex. It does not rule out arbitrary scalar encodings, restricted families,
or different information and arithmetic access models.

Recovering all expected-loss rows in a class spanning
$`\mathbb R^n`$ entails full-law recovery. A smaller declared class need
not. The retained observation already recovers every affine combination of
its rows and a constant; requiring the whole law for that task is excessive.

## 3. A local fiber can identify more than the global rank implies

Let $`F(y)=F_{\Delta_n}(y)`$ be nonempty, and define its **feasible support**
```math
J(y)=\{j:\text{some }p\in F(y)\text{ has }p_j>0\}.
```
This is the union of supports across the entire fiber. There is a law
$`p^\circ\in F(y)`$ positive in every coordinate of $`J(y)`$: average
one witnessing law for each such coordinate. Therefore
```math
\mathrm{span}(F(y)-F(y))
=\{h:h_{J^c}=0,\ A_Jh_J=0\}.
```
One inclusion follows from the constraints. For the reverse inclusion, any
vector on the right can be scaled in both signs around $`p^\circ`$.

Consequently, **at this particular $`y`$**:

- The full law is identified iff $`\mathrm{rank}A_J=|J|`$.
- The target $`Cp`$ is identified iff
  $`\ker A_J\subseteq\ker C_J`$.

These are local conditions. They do not require a decoder valid at every
possible future observation.

**Boundary singleton.** With $`n=3`$ and $`L=(0,1,2)`$, $`A`$ has
rank two. Observing $`y=0`$ forces $`p=e_1`$, so the law is fully recovered
at that observation. At $`y=1`$, both $`e_2`$ and
$`(e_1+e_3)/2`$ are feasible, so the law is not identified.

**Do not use the support of an arbitrary feasible law.** At $`y=1`$ in
that example, using only the support $`\{2\}`$ of $`e_2`$ falsely suggests
uniqueness. The feasible support is $`\{1,2,3\}`$. An equivalent check
at any particular feasible $`p^0`$ is
```math
F(y)=\{p^0\}
\quad\Longleftrightarrow\quad
\{h\in\ker A:h_j\geq0\text{ whenever }p^0_j=0\}=\{0\}.
```
Nonzero vectors in this cone can be scaled forward from $`p^0`$.

**Convex restricted domains.** If $`P`$ is convex and
$`U=\mathrm{span}(P-P)`$, the global linear-target criterion becomes
```math
U\cap\ker L\subseteq\ker C.
```
Choose a relative-interior point of $`P`$, around which sufficiently small
perturbations in $`U`$ remain in $`P`$, to repeat Theorem 1's proof.
Additional known affine constraints and known support restrictions therefore
can reduce the required measurement dimension.

**Nonconvex exceptions.** For $`P=\{e_1,e_2,e_3\}`$ and $`L=(0,1,2)`$,
all three laws have distinct observed values, despite deficient augmented
rank. A nonlinear restricted family can also permit a nonlinear decoder:
```math
P=\{(t,t^2,1-t-t^2):0\leq t\leq1/2\},\qquad L=(1,0,0).
```
Here $`y=t`$ recovers the law. The square is outside the inherited finite
piecewise-affine term language on this interval; a mathematical decoder does
not silently supply a native kernel operation.

## 4. Partial identification has constructive certificates

For a scalar target $`c^\top p`$ and a feasible observation $`y`$, the
sharp bounds are the linear programs
```math
\underline v(y)=\min_{p\geq0:Ap=b(y)}c^\top p,\qquad
\overline v(y)=\max_{p\geq0:Ap=b(y)}c^\top p.
```
Feasibility and simplex compactness give attained extrema. Ordinary finite
linear-programming duality gives
```math
\underline v(y)=\max_{A^\top\lambda\leq c}\lambda^\top b(y),\qquad
\overline v(y)=\min_{A^\top\mu\geq c}\mu^\top b(y).
```
The inequalities have a direct certificate reading: if
$`A^\top\lambda\leq c`$, then
$`c^\top p\geq\lambda^\top Ap=\lambda^\top b(y)`$ for every feasible
law. A feasible primal law attaining a bound and a matching dual vector
certify its sharpness. Equality of the two endpoints certifies exact
recovery at that observation, even without the global row-space condition.

For learned observations with an externally justified error bound,
```math
F_\epsilon(\widehat y)
=\{p\in\Delta_n:\|Lp-\widehat y\|_\infty\leq\epsilon\}
```
gives analogous linear-programming bounds. The source-membership or coverage
premise is an additional obligation: merely solving the optimization does
not certify that the actual law lies in this set.

**Missing dependence.** On outcomes $`00,01,10,11`$, retain the two
Bernoulli marginals $`a=\mathbb E[X]`$, $`b=\mathbb E[Y]`$. Every compatible
joint law has the form
```math
(p_{00},p_{01},p_{10},p_{11})
=(1-a-b+t,b-t,a-t,t)
```
with the sharp interval
```math
\max(0,a+b-1)\leq t\leq\min(a,b).
```
At $`a=b=1/2`$, the laws
$`(1/2,0,0,1/2)`$ and $`(0,1/2,1/2,0)`$ have identical marginals.
Their disagreement probabilities are zero and one, respectively, so a
choice between predicting equality and predicting inequality can reverse.
Knowledge of independence would reduce the admissible family and fix
$`t=ab`$; that is an extra assumption, and joint variation of $`a,b`$
makes this product non-native in the inherited exact affine fragment.

## 5. Preferences and one decision are distinct weaker services

Suppose rows $`C_a`$ are the expected-loss queries for finitely many
available actions. Lower is better.

### Exact action differences and complete weak preferences

Recovering every difference
$`(C_a-C_b)p`$ suffices to recover the complete weak preference order,
including ties. Theorem 1 applies to the difference rows, but recovering
their magnitudes is stronger than recovering their signs.

For a compact fiber, let
```math
\ell_{ab}=\min_{p\in F(y)}(C_a-C_b)p,\qquad
u_{ab}=\max_{p\in F(y)}(C_a-C_b)p.
```
The sign is constant exactly when
$`\ell_{ab}>0`$, or $`u_{ab}<0`$, or
$`\ell_{ab}=u_{ab}=0`$. A range $`[0,u]`$ with $`u>0`$ does not
preserve the complete weak order: it merges a tie with strict preference.

**Preferences without absolute expected losses.** Let
```math
L=(1,0,0),\quad C_A=(0,1,2),\quad C_B=(1,0,1).
```
Then $`y=p_1`$, while
```math
C_Ap=1-y+p_3,\quad C_Bp=y+p_3,\quad
(C_A-C_B)p=1-2y.
```
The common uncertain component $`p_3`$ prevents recovery of either
absolute expected loss or the full law. Nevertheless, choose $`A`$ for
$`y>1/2`$, $`B`$ for $`y<1/2`$, and either at equality.
The chosen action changes with the retained observation. This is more
informative than a universally dominant-action example.

**Preferences without exact differences.** Let $`L=(1,0,0)`$ and take
an action difference $`d=(0,1,2)`$. Its magnitude $`p_2+2p_3`$ is
underidentified except at special observations, but it is zero exactly
when $`y=1`$ and positive otherwise. Hence complete weak preference is
known globally without recovering its numerical gap.

There is a useful limit to that latter phenomenon. If a row $`d`$ takes
both strictly positive and strictly negative values on the full simplex,
then its sign is identifiable from $`Lp`$ on the full simplex **iff**
$`d`$ is in the row space of $`A`$. To prove necessity, choose a strictly
positive law $`p^0`$ with $`dp^0=0`$, which exists by interpolating
strictly positive laws on opposite sides. Any $`h\in\ker A`$ with
$`dh\neq0`$ produces $`p^0\pm\epsilon h`$ in one fiber with opposite
signs. Thus sign recovery forces $`dh=0`$ for every such $`h`$.
This concerns global recovery and a sign-changing linear comparison;
it is not a necessity claim for arbitrary restricted tasks.

### Some optimal action versus the whole optimal-action set

A summary-based selector that always returns **some** Bayes-optimal action
exists iff
```math
\bigcap_{p\in F(y)}\mathrm{argmin}_a C_ap\neq\varnothing
\quad\text{for every feasible }y.
```
Necessity is immediate; sufficiency chooses an action in each intersection.
For finite actions, a fixed ordering resolves selection among these common
optimal actions.

This condition is weaker than requiring identical optimal-action sets on
the fiber, and weaker than recovering the action prescribed by an externally
fixed tie policy. For example $`C_A=(0,0)`$, $`C_B=(0,1)`$ with no
observation always permits choosing $`A`$, although $`B`$ ties at $`p=e_1`$
and loses at $`p=e_2`$.

A proposed action $`a`$ is common-optimal precisely when
```math
\max_{p\in F(y)}(C_a-C_b)p\leq0\quad\text{for every }b.
```
The deterministic minimax-regret diagnostic is
```math
r^*(y)=\min_a\max_b\max_{p\in F(y)}(C_a-C_b)p.
```
It is nonnegative, and it is zero exactly when a common optimal action
exists. These are constructive ordinary linear-optimization comparisons.
Allowing a randomized action does not rescue exact zero regret when no
common optimal action exists: every supported action would have to have
zero regret at every law. Randomization can improve positive approximate
regret, which is a different service.

## 6. Nuisance scales and changes of units need qualified claims

A binary expected loss $`v=c_0+(c_1-c_0)p`$ determines $`p`$ if the
two known stakes differ. If the stakes or additive charges are unknown,
one should apply the fiber criterion to the enlarged input $`(p,\theta)`$
containing those nuisance parameters. Two admissible such inputs with the
same $`v`$ but different $`p`$ refute identification.

However, **unknown stakes do not universally preclude recovery**. If
all outcome-indicator values $`y_i=s p_i`$ are observed and the same
unknown nonzero scale $`s`$ applies to every coordinate, normalization gives
```math
s=\sum_i y_i,\qquad p_i=\frac{y_i}{\sum_j y_j}.
```
This is an identifiable nuisance-scale example. At $`s=0`$ it fails.
It also uses division by a jointly variable quantity, so it is not
automatically an exact native phase-two decoder.

For a known affine measurement recoding
$`y'=Ty+b`$, the new loss matrix is
$`L'=TL+b\mathbf1^\top`$. It preserves all information exactly when
the map $`y\mapsto Ty+b`$ is injective on $`L(\Delta_n)`$.
An invertible $`T`$ is sufficient, but unnecessary if there are redundant
measurement coordinates. Equivalently on the full simplex, preservation
of the old expected-loss family requires
```math
\mathrm{row}\begin{pmatrix}\mathbf1^\top\\L\end{pmatrix}
=
\mathrm{row}\begin{pmatrix}\mathbf1^\top\\L'\end{pmatrix}.
```
Known common positive rescaling preserves preferences as well. Changing
relative resource prices is instead a new target family; apply the target
row-space or local-fiber criterion again.

For example, two states consume resource vectors $`(1,0)`$ and $`(0,1)`$.
Old prices $`(1,1)`$ give the constant retained cost one. New prices
$`(2,1)`$ produce expected cost $`1+p_1`$, which is not recoverable
from that old scalar. Retaining both resource expectations suffices for
all known linear repricings. This is a scoped sufficient-summary statement,
not a requirement to recover all irrelevant aspects of the law.

## 7. Check results and rejected overgeneralizations

An exact rational development calculation checked the main numerical
witnesses using Python's standard-library fractions and elimination:

- Decision example: augmented measurement rank $`2`$, rank after adding
  both absolute action losses $`3`$, rank after adding their difference
  still $`2`$.
- At $`p=(3/4,1/4,0)`$ and $`q=(3/4,0,1/4)`$, both observations are
  $`3/4`$; costs are respectively $`(1/4,3/4)`$ and $`(1/2,1)`$;
  the action difference is $`-1/2`$ for both.
- Two-marginal example: augmented rank $`3<4`$, identical observations
  for the two supplied laws, and joint-event expectations $`1/2`$ and $`0`$.

These calculations are development checks, not a frozen challenge or new
empirical evidence. An initial attempt to use an unavailable symbolic
library was abandoned; no dependency installation was needed.

The review explicitly rejects these generalizations:

1. Deficient global rank means no particular observation can identify the law.
2. The support of one feasible law is enough for a local rank check.
3. Full-law recovery is necessary for a fixed action choice.
4. Every target-loss row must be recoverable to preserve action preferences.
5. A valid optimal selector requires identical sets of optimal actions.
6. Rank conditions for the full simplex apply unchanged to arbitrary
   nonconvex restricted input families.
7. Unknown stakes always preclude probability recovery.
8. An algebraically available decoder is automatically efficient, robust
   to error, or expressible in the inherited exact kernel.

No theorem here supplies an update rule, logical-uncertainty convergence,
counterfactual dependencies, or an advantage over the ordinary finite
probability/credal and linear-programming comparator. The useful product is
the exact service-specific contract and its constructive failure witnesses.
