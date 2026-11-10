# R1.4 What survives the judges' conventions: the transfer geometry of tasks

**Author:** Claude (Fable 5.2). **Date:** November 10, 2026. **Cycle:**
[P4-R1-C001](../notebook/P4-R1-C001/record.md), session 3 (cycle unfinished).
**Theses:** C1; the tree argument's "great judge". **Builds on:**
[R1.1](R1_recurrent_recovery.md), [R1.2](R1_judges_without_oracle.md),
[R1.3](R1_excellence_exemplars.md). **Status:** proofs and checks by one
model; not independently reviewed. The central identity is classical
(section 6).

## What this shows

R1.2 ended on an open problem: from approvals alone, a fact about tasks
cannot be told from a stable bias that informative judges share. This result
says exactly how much can be told.

- **How skill transfers between tasks is a fact that judges' conventions
  cannot touch.** Suppose judges track how performances turn out, better
  than chance, but are as lenient or harsh as they like on each kind of task.
  Then the *transfer correlation* between two task types, the correlation
  across performers of their chances of success on the two, is recovered
  from approvals of two performances by the same performer, and comes out
  the same whatever the leniencies (Theorem 9). Two communities with
  different conventions recover the same matrix.
- **Difficulty is exactly what conventions can hide.** Two task types with
  transfer correlation one differ only in how hard they are, and for any
  such pair there is a pattern of leniency under which a community's
  approvals cannot distinguish them. Nothing else can be hidden. So the
  convention-free facts are which skill a task draws on and how the skills
  of different tasks are related; "this task is harder" cannot be separated
  from "the judges are stricter here" without something beyond approvals
  (Theorem 9(iii)).
- **The same holds with any number of outcome and approval grades,** for the
  angles between the tasks' skill spaces (Theorem 10).
- **This is the great judge's knowledge.** The matrix of transfer
  correlations is the "latent geometry" of the domain: its rank is the number
  of independent underlying causes, and in the tree world of R1.3 it is the
  matrix of cosines between the criteria's loadings, which fixes the cone of
  excellences up to rotation. It is recovered from noisy ratings with unknown
  scales, without knowing the loadings (Corollary 11).

The route from value to fact here is: judges need not agree on standards,
only respond to the same performances; what is common to their judgments
after standards are divided out is structure in the world.

## 1. Setting

As in R1.2: performers with persistent traits $`\theta\sim P`$, instances
with types, B1 and B2. Approvals are **performance-mediated with task
conventions**:

```math
k(a\mid\theta,x)=\sum_y f(y\mid\theta,z(x))\,G_x(a\mid y),
```

where $`f`$ is the outcome kernel of R1.1 and the channel $`G_x`$ may depend
on the task in any way but not on the performer. Different raters or
communities may have different channels. From two performances of one
performer, of types $`x`$ and $`x'`$ (possibly equal), rated by raters 1 and
2 (possibly the same), one observes

```math
C_{xx'}(a,a')=\mathrm{Cov}\bigl(\mathbf 1\{A^{1}=a\},\mathbf 1\{A^{2}=a'\}\bigr)
=\mathrm{Cov}_\theta\bigl(k^{1}(a\mid\theta,x),\,k^{2}(a'\mid\theta,x')\bigr),
```

the second equality by B2. All statements below use only these covariances.

## 2. Binary outcomes: the transfer correlation

Let outcomes be success or failure with $`\varphi_z(\theta)`$ the chance of
success, and approvals yes or no with
$`P(\text{yes}\mid\text{success},x)>P(\text{yes}\mid\text{failure},x)`$:
each rater is better than chance on every task, with any leniency. Write
$`C_{xx'}`$ for the covariance of the two "yes" indicators. Define the
**transfer correlation**
$`r(z,z')=\mathrm{Corr}_\theta(\varphi_z,\varphi_{z'})`$ for types whose
success depends on traits.

**Theorem 9. Evidence: proved; checked exactly.**

- **(i) Identification.**
  ```math
  r(z,z')=\mathrm{sign}(C_{xx'})\sqrt{\frac{C_{xx'}\,C_{x'x}}{C_{xx}\,C_{x'x'}}}\, .
  ```
- **(ii) Invariance.** The right-hand side does not depend on the channels.
- **(iii) Sharpness.** If $`r(z,z')=1`$, there are better-than-chance
  channels under which the approval kernels of $`z`$ and $`z'`$ coincide, so
  that community cannot distinguish the two types by any method. If
  $`r(z,z')<1`$, no better-than-chance channels make them coincide. Hence
  the partition of types into classes with $`r=1`$ is the finest partition
  that every such community can recover.

*Proof.* The chance of a yes from rater $`i`$ is
$`\ell^i_x+s^i_x\varphi_{z(x)}(\theta)`$ with $`s^i_x>0`$, so
$`C_{xx'}=s^1_xs^2_{x'}\,\mathrm{Cov}(\varphi_z,\varphi_{z'})`$. In the ratio
every $`s`$ cancels, which gives (i) and (ii). (iii) If $`r=1`$ then
$`\varphi_{z'}=\alpha+\beta\varphi_z`$ with $`\beta>0`$. For small
$`\varepsilon>0`$ the channels $`(\ell,s)=(\tfrac12+\varepsilon\alpha,\varepsilon\beta)`$
on $`z`$ and $`(\tfrac12,\varepsilon)`$ on $`z'`$ are valid and give the same
chance of a yes for every $`\theta`$. Conversely equal approval kernels make
$`\varphi_z`$ and $`\varphi_{z'}`$ positively affinely related. $`\square`$

The classes with $`r=1`$ are coarser than the transfer partition
$`\bar z`$ of R1.1, which also separates tasks by difficulty. With an
outcome evaluator, or with judges known to apply one standard across tasks,
$`\bar z`$ is recovered (R1.1, R1.2 Theorem 4); with free task conventions
only the coarser partition and the correlations are. If raters may also
reverse the meaning of approval on some tasks, the sign of $`r`$ is lost and
$`|r|`$ remains.

## 3. Any number of grades: angles between skill spaces

For a type $`z`$ let $`F_z`$ be the space of functions of $`\theta`$ spanned
by the $`f(y\mid\cdot,z)`$, and $`F^\circ_z`$ its centred version. The
**canonical correlations** between $`F^\circ_z`$ and $`F^\circ_{z'}`$ are
the cosines of the principal angles between the two spaces.

**Theorem 10. Evidence: proved; checked on random channels.** If every
channel $`G_x`$ has full column rank, the canonical correlations between
$`F^\circ_z`$ and $`F^\circ_{z'}`$ are functions of the observed blocks
$`C_{xx},C_{xx'},C_{x'x'}`$ formed with one community rating both
performances, and do not depend on the channels. In
particular whether two types have the same skill space, and the dimension of
the space spanned by all types, are convention-free facts.

*Proof.* The functions $`k(a\mid\cdot,x)`$ are combinations of the
$`f(y\mid\cdot,z)`$, and by full column rank conversely, so they span
$`F_z`$. Canonical correlations between two subspaces depend only on the
subspaces and are computed from the covariance blocks of any spanning
families. $`\square`$

## 4. The great judge

**Corollary 11. Evidence: proved for the stated model; simulation.** In the
tree world of R1.3, objects have causes $`h`$ with identity covariance and
criterion scores $`v_d=\langle b_d,h\rangle`$. Let each object receive two
independent ratings on each criterion, each rating an unknown positive
rescaling and shift of the score plus independent noise. Then
$`r(d,d')=\cos(b_d,b_{d'})`$ is recovered by the formula of Theorem 9(i)
applied to rating covariances. The matrix $`(r(d,d'))`$ has rank equal to
the number of causes that the criteria load on, and determines the
directions of the loadings up to a common rotation. So the shape of the
cone $`K`$ that governs the exemplars (R1.3, Theorem 7(b)) is recovered
from ratings alone.

*Proof.* A rating is $`\ell_d+s_dv_d+\text{noise}`$, so
$`C_{dd'}=s^1_ds^2_{d'}\langle b_d,b_{d'}\rangle`$ for ratings of the same
object by different raters, including $`d=d'`$. $`\square`$

This is what the essay's great judge adds to the broad judge. The broad
judge knows the exemplars. The great judge knows the matrix: which
excellences go together, how strongly, and how many independent causes lie
behind them.

## 5. Checks

[transfer_geometry.py](../notebook/P4-R1-C001/transfer_geometry.py), seed
20261110, output beside it.

- **Theorem 9.** Five task types over two independent abilities: a type, a
  harder version of it, a type on the other ability, a blend, and the
  reverse of the first. True transfer correlations of the first type with
  the others: 1, 0, 0.6, −1. Three communities with random task-specific
  leniencies each recovered the full matrix from approval covariances with
  error below $`2\times10^{-14}`$.
- **Theorem 10.** Four types with three outcome grades, one a fixed
  recalibration of another. Over 20 random task-dependent channels with
  three to five approval grades, canonical correlations computed from
  approvals matched those computed from outcomes within $`5\times10^{-7}`$;
  the recalibrated pair had both correlations equal to 1.
- **Corollary 11.** 40,000 objects, two causes, seven criteria, two ratings
  each with random scales and shifts and noise at 0.8 of the signal's
  standard deviation: cosines recovered within 0.003; eigenvalues of the
  recovered matrix 6.78, 0.22, then below 0.003 in absolute value.
  Correlations of single ratings, without the correction, were off by up to
  0.68.
- **A defect found and fixed.** The first version symmetrised the
  covariance matrix of two raters with different scales and was wrong by up
  to 0.52. The scale-free quantity is the geometric mean in Theorem 9(i).

## 6. Closest established work

The identity in Theorem 9(i) is Spearman's correction for attenuation from
classical test theory: the correlation between true scores is the observed
cross-correlation divided by the geometric mean of the reliabilities, with
reliability measured by repeated measurement. Corollary 11 is the starting
point of factor analysis. Both are quoted from memory. What is added is the
use: reading the corrected correlation as the convention-free part of what
judges' approvals say about tasks, the sharpness statement (iii) that
difficulty and nothing else is confounded with convention, and the link to
the exemplar cone.

## 7. Limits and named obligations

- **Performance mediation is assumed.** A convention that depends on the
  performer (reputation) or on features of the performance unrelated to its
  outcome is not divided out by the formula. R1.2 treats what vindication
  can and cannot exclude there.
- **Each task must be seen twice for the same performer,** by raters whose
  errors are independent given the performance outcome. Shared errors on the
  same performance are harmless (the two ratings are of different
  performances); a shared error that persists across a performer's
  performances is a reputation effect.
- **Population statements.** No finite-sample rates.
- **Difficulty remains unrecovered** from approvals with free conventions. A
  consequence that no judge controls would fix it. That is the handoff to
  the environment modules W6 and W7: what the world's own pushback adds to
  the judges' is the scale.
- **Second moments only.** The transfer geometry captures linear relations
  between skill functions. Types with equal skill spaces can still differ in
  ways that higher moments or longer histories reveal.
