# R1.1 Recurrent judgment recovers the transfer structure of tasks

**Author:** Claude (Fable 5.2). **Date:** November 9, 2026. **Cycle:**
[P4-R1-C001](../notebook/P4-R1-C001/record.md), session 1 (cycle unfinished).
**Theses:** C1, C2. **Status:** stated results with proofs and exact numerical
checks, written and checked by the same model in one session. Not
independently reviewed. Evidence levels are marked per result.

**S6 review, Codex (GPT-6), November 10, 2026:** Theorems 1--3 were
reconstructed and Theorems 1--2 checked with a separate implementation.
[R1.8](R1_quantitative_recovery.md) extends Theorem 2's bound to all n>=1.
The earlier records and attribution are preserved; see the
[review](../notebook/P4-R1-C001/review_s6.md).

## What this shows

Score a judge by how well its judgments of a performer predict that
performer's later results. Then:

- **The task delineations that earn the best score are exactly the ones that
  separate every two task types on which skill transfers differently**
  (Theorem 1). One reappearance of the performer is enough.
- **Without reappearance, the same scoring recovers only differences in average
  difficulty.** What judging the judge adds to judging the performance is
  therefore exactly the facts about transfer: task types that are equally
  hard but draw on different skills (Theorem 1(d), Proposition 4).
- **Good judging is robustly informative:** a judge whose score is within
  $`\eta`$ of the best cannot confuse two task types that are both common
  and sufficiently different, with an explicit bound (Theorem 2).
- **The optimal judge and the true delineation determine each other.** Every
  judge implicitly delineates tasks by what it treats as interchangeable. All
  optimal judges implicitly use the same, factual, delineation, and that
  delineation is the only one that is optimal and reproduces itself through
  its own judge (Theorem 3). This is a typed reading of T = J².

The conditions are an evaluator with access to later outcomes, tasks met
independently of skill (or an identifiable share of them, Proposition 5), and
scoring of the best forecast a delineation supports. The society of judges
who evaluate one another without such an evaluator is not treated here.

## 1. The judgment core

**Objects.** A performer has a latent skill $`\theta`$ with law $`P`$ on a
measurable space. A task instance $`x`$ has a type $`z(x)`$ in a finite set
$`Z`$. An outcome $`Y`$ lies in a finite set $`\mathcal Y`$ and is the
value-relevant result of one performance (for example approved or not).

**Assumptions.**

- **A1 (tasks met independently of skill).** Instances are drawn i.i.d. from
  a law $`q`$ with $`q(z)>0`$ for every type, independently of skills.
- **A2 (conditional independence).** Given skills and instances, outcomes of
  distinct performances are independent, and a performance of instance $`x`$
  by skill $`\theta`$ has outcome law $`f(\cdot\mid\theta,z(x))`$.

**Two factual partitions of the types.**

- Types $`z,z'`$ are **twins** when
  $`f(\cdot\mid\theta,z)=f(\cdot\mid\theta,z')`$ for $`P`$-almost every
  $`\theta`$. Write $`\bar z`$ for the map to twin classes, the **transfer
  partition**, and $`f_A(\cdot\mid\theta)`$ for the outcome law of class $`A`$.
- Types are **marginal twins** when their outcome laws agree for a performer
  met once: $`\int f(\cdot\mid\theta,z)\,dP=\int f(\cdot\mid\theta,z')\,dP`$.
  Write $`\pi_0`$ for this coarser **difficulty partition**.

**Delineations and judges.** A delineation is a map $`c`$ from instances to a
finite set of cells. In an episode a performer has $`n`$ past performances
and one target performance whose outcome $`Y_0`$ comes later. A judge with
delineation $`c`$ sees the history $`H^c_n=((c(x_s),Y_s))_{s\le n}`$ and the
target cell $`c_0=c(x_0)`$, and issues a forecast $`a\in\Delta(\mathcal Y)`$
of $`Y_0`$. This forecast is the judgment: "yes" is the expectation that
success reappears.

**The second-order score.** A judge is scored by $`\mathbb E\log a(Y_0)`$.
The value of a delineation is the best score it supports,

```math
V_n(c)=\sup_a\mathbb E\log a(Y_0)=-H(Y_0\mid H^c_n,c_0),
```

attained by the Bayes forecast $`M^c_n=P(Y_0\in\cdot\mid H^c_n,c_0)`$. Any
strictly proper score gives the same maximizers; log score is used for its
information identities. Partitions are compared up to sets of instances of
probability zero.

## 2. Recovery

**Theorem 1 (recurrent recovery). Evidence: proved; checked exactly.**
Assume A1 and A2.

- **(a)** If $`c'`$ refines $`c`$, then $`V_n(c')\ge V_n(c)`$.
- **(b)** $`V_n(c)\le V_n(\bar z)`$ for every $`c`$ and $`n`$, with equality
  whenever $`c`$ refines $`\bar z`$.
- **(c)** For every $`n\ge 1`$: if $`c`$ does not refine $`\bar z`$, then
  $`V_n(c)<V_n(\bar z)`$. Hence for $`n\ge1`$ the optimal delineations are
  exactly the refinements of the transfer partition, and $`\bar z`$ is the
  coarsest of them.
- **(d)** For $`n=0`$ the optimal delineations are exactly the refinements of
  the difficulty partition $`\pi_0`$.

So the distinctions recovered at the first reappearance, and not before, are
exactly the pairs of types with equal average difficulty and different
dependence on skill. If skill does not vary, $`\bar z=\pi_0`$ and
reappearance adds nothing.

*Proof.* (a) A judge with $`c'`$ can discard information.

(b) Let $`d=(c,\bar z)`$ be the common refinement. By A1 and A2, conditional
on the twin classes of the $`n+1`$ instances, the pair
$`(\theta,(Y_s)_{s\le n})`$ is independent of the instances themselves,
because outcome laws depend on an instance only through its class and
instances are independent of skill. Hence
$`P(Y_0\in\cdot\mid H^d_n,d_0)=P(Y_0\in\cdot\mid H^{\bar z}_n,\bar z_0)`$ and
$`V_n(d)=V_n(\bar z)`$. By (a), $`V_n(c)\le V_n(d)`$, and if $`c`$ refines
$`\bar z`$ then $`d=c`$.

(c) Suppose a cell $`\kappa`$ of $`c`$ meets two distinct classes $`A\ne B`$
with positive probability and $`V_n(c)=V_n(\bar z)=V_n(d)`$. Since
$`M^c_n=\mathbb E[M^d_n\mid H^c_n,c_0]`$,

```math
V_n(d)-V_n(c)=\mathbb E\,\mathrm{KL}\left(M^d_n\,\|\,M^c_n\right)=0,
```

so $`M^d_n=M^c_n`$ almost surely. Fix values $`\rho`$, of positive
probability, for the $`d`$-labels and outcomes of history positions
$`2,\dots,n`$, and let $`P_\rho`$ be the posterior law of $`\theta`$ given
$`\rho`$. For $`a,b\in\{A,B\}`$ and $`y',y\in\mathcal Y`$ put

```math
N_{ab}(y',y)=\int f_a(y'\mid\theta)\,f_b(y\mid\theta)\,dP_\rho,\qquad
D_a(y')=\int f_a(y'\mid\theta)\,dP_\rho.
```

On the event that position 1 has label $`(\kappa,a)`$ and outcome $`y'`$ and
the target has label $`(\kappa,b)`$, A1 and A2 give
$`M^d_n(y)=N_{ab}(y',y)/D_a(y')`$ when $`D_a(y')>0`$. On all four such events
the $`c`$-information is identical, so $`M^c_n(y)`$ takes one value
$`m(y)`$. Therefore $`N_{ab}(y',y)=m(y)D_a(y')`$ for all $`a,b`$ (trivially
when $`D_a(y')=0`$), which gives $`N_{AA}=N_{AB}`$ and $`N_{BA}=N_{BB}`$, and

```math
\int\bigl(f_A(y'\mid\theta)-f_B(y'\mid\theta)\bigr)
     \bigl(f_A(y\mid\theta)-f_B(y\mid\theta)\bigr)\,dP_\rho
 =N_{AA}-N_{AB}-N_{BA}+N_{BB}=0 .
```

Taking $`y'=y`$ shows $`f_A(y\mid\cdot)=f_B(y\mid\cdot)`$ $`P_\rho`$-almost
everywhere, for every $`y`$. Since $`P`$ is the mixture of the $`P_\rho`$,
the classes $`A`$ and $`B`$ are twins, a contradiction.

(d) $`V_0(c)=-H(Y_0\mid c_0)\le -H(Y_0\mid x_0)`$, with equality exactly
when the outcome law of a once-met performer is constant on almost every
cell, by strict concavity of entropy. $`\square`$

**Remark (why one reappearance suffices).** The proof uses only that a past
performance and the target can both fall in the confused cell. The quantity
that vanishes is the second moment of the difference in skill profiles, so
any skill-dependent difference between two types is visible to a judge who
has seen the performer once before.

**Theorem 2 (near-optimal judges separate distinct, common types).
Evidence: proved; checked on 1,200 cases.** Assume A1 and A2 and $`n=1`$.
Let a cell of $`c`$ contain instances of classes $`A\ne B`$ with
probabilities $`\alpha,\beta>0`$. Then

```math
V_1(\bar z)-V_1(c)\;\ge\;\frac12\left(\frac{\alpha\beta}{\alpha+\beta}\right)^{2}
\sum_{y\in\mathcal Y}\Bigl(\mathbb E\bigl[(f_A(y\mid\theta)-f_B(y\mid\theta))^{2}\bigr]\Bigr)^{2}.
```

Consequently a judge whose score is within $`\eta`$ of optimal cannot use a
delineation that merges two classes for which the right-hand side exceeds
$`\eta`$.

*Proof.* With $`n=1`$ there is no $`\rho`$ and $`P_\rho=P`$. By Pinsker's
inequality and $`\|\cdot\|_1\ge\|\cdot\|_2`$,
$`V_1(d)-V_1(c)\ge\frac12\sum_y\mathbb E(M^d_1(y)-M^c_1(y))^2`$, and the
expectation is the expected conditional variance of $`M^d_1(y)`$ given the
$`c`$-information. Keep only the $`c`$-information "history $`(\kappa,y)`$,
target $`\kappa`$" and, within it, the two pairs of hidden labellings
$`\{AA,AB\}`$ and $`\{BB,BA\}`$. A variable taking values $`v_1,v_2`$ on
events of probability $`w_1,w_2`$ contributes at least
$`\frac{w_1w_2}{w_1+w_2}(v_1-v_2)^2`$ to the expected conditional variance.
The pair $`\{AA,AB\}`$ has $`w=\alpha D_A(y)\alpha`$ and
$`\alpha D_A(y)\beta`$, and similarly for $`\{BB,BA\}`$. With
$`u=M_{AA}-M_{AB}`$ and $`v=M_{BB}-M_{BA}`$ evaluated at $`(y,y)`$,

```math
V_1(d)-V_1(c)\ge\frac12\cdot\frac{\alpha\beta}{\alpha+\beta}
\sum_y\bigl(\alpha D_A(y)u^2+\beta D_B(y)v^2\bigr),
\qquad D_A(y)u+D_B(y)v=\mathbb E\bigl[(f_A(y)-f_B(y))^2\bigr],
```

the identity being the display in the proof of Theorem 1(c). By
Cauchy--Schwarz,
$`(D_Au+D_Bv)^2\le(\alpha D_Au^2+\beta D_Bv^2)(D_A/\alpha+D_B/\beta)`$ and
$`D_A/\alpha+D_B/\beta\le(\alpha+\beta)/(\alpha\beta)`$. $`\square`$

The deficit of a merge is not always increasing in $`n`$ (22 of 1,200
random cases over $`n=1,2,3`$), so the bound is stated for the
single-reappearance game in the original session. **S6 extension:**
[R1.8, Theorem 16](R1_quantitative_recovery.md) proves this same lower
bound for every n>=1, by conditioning on the remaining fine history and
averaging posterior second moments. This does not require monotonicity of
the actual deficit.

## 3. The judge and the delineation determine each other

Fix $`n\ge1`$. Two maps connect delineations and judges.

- **From a delineation to a judge.** $`a_c`$ is the Bayes forecast
  $`M^c_n`$: the best judge that delineates tasks by $`c`$.
- **From a judge to a delineation.** A judge using cells treats two cells as
  **interchangeable** when replacing one by the other at any single place in
  its input (a history label or the target label) never changes its
  forecast, on inputs of positive probability. $`T(a)`$ is the delineation
  obtained by merging interchangeable cells: what the judge treats as the
  same task.

**Theorem 3 (typed T = J² at the optimum). Evidence: proved.** Assume A1,
A2 and $`n\ge1`$.

- **(i)** $`T(a_c)`$ merges two cells exactly when their cell kernels
  $`\tilde f_\kappa(\cdot\mid\theta)=\sum_z P(z\mid\kappa)f(\cdot\mid\theta,z)`$
  agree for almost every skill.
- **(ii)** If $`c`$ is optimal for the second-order score, then
  $`T(a_c)=\bar z`$. Every optimal judge implicitly delineates tasks by the
  transfer partition, whatever finer labels it was given.
- **(iii)** $`\bar z`$ is the unique delineation that is both optimal and a
  fixed point, $`T(a_c)=c`$.

*Proof.* (i) If the kernels agree, the likelihood of every input is unchanged
by the replacement, so the forecast is. Conversely, invariance under
replacing the target label gives $`N_{\kappa\kappa}=N_{\kappa\kappa'}`$ and
$`N_{\kappa'\kappa}=N_{\kappa'\kappa'}`$ for the cell kernels and every
$`\rho`$, and the argument of Theorem 1(c) applies. (ii) By Theorem 1(c) an
optimal $`c`$ refines $`\bar z`$, so each cell kernel is the kernel of its
class, and by (i) cells are merged exactly when they lie in one class. (iii)
An optimal fixed point refines $`\bar z`$ and has no two cells in one class.
$`\square`$

**Reading.** Optimality says no predictive difference is missed. The fixed
point says no distinction is drawn without a predictive difference. Together
they single out the facts. Task delineation, T, is what the second-order
evaluation of judgment, J², selects, and it can be read off the selected
judge. The equality holds at the optimum and on the quotient by twins, not
as an identity of functions.

## 4. Limits, with repairs

**Proposition 4 (no reappearance, no transfer facts, by any method).
Evidence: proved.** If every performer is observed on a single instance, the
law of all observed data depends on $`f`$ only through the once-met outcome
laws. Two worlds with the same once-met laws and different transfer
partitions are then observationally identical, so no procedure, recursive or
not, recovers more than $`\pi_0`$. *Proof.* The data are i.i.d. pairs with
law $`q(x)\int f(y\mid\theta,z(x))\,dP`$. $`\square`$

*Example.* Two types, two equally likely skills, success probability 0.9 on
the type matching the skill and 0.1 on the other. Every once-met success
rate is one half, as in a world of pure coin flips. With reappearance the
true delineation scores $`-0.471,-0.408,\dots\to-0.325`$ nats at
$`n=1,2,\dots`$, while a Bayes-optimal judge who cannot tell the two types
apart stays at $`-\log 2`$ for every $`n`$: its judgments look random
although it uses everything it distinguishes.

**Proposition 5 (skill-dependent choice of tasks). Evidence: (a) exact
examples; (b) proved.**

- **(a)** Without A1 recovery can fail in both directions. If each skill
  attempts only the type it is good at, merging the two types costs nothing.
  If twins are chosen at skill-dependent rates and some other type depends on
  skill, splitting the twins strictly helps (0.042 nats in the example).
- **(b) Repair by identifiable assignment.** Suppose each performance is,
  independently with probability $`\varepsilon>0`$, *assigned*: its instance
  is drawn from $`q`$ independently of skill, and the judge sees which
  performances were assigned. Then for $`n\ge1`$, if $`c`$ does not refine
  $`\bar z`$, $`V_n(c)<V_n(c,\bar z)`$. Every optimal delineation still
  separates all non-twins. *Proof.* Run the argument of Theorem 1(c) on the
  event that position 1 and the target are assigned. $`\square`$

Under (b) optimal delineations may be strictly finer than $`\bar z`$: they
can also record who chooses what, which is a fact about the population. In
the specialist example an unflagged assignment share of 1% already makes the
merge costly (0.0086 nats at $`n=2`$). The general unflagged-assignment
question was open in the original session. **S6, Codex (GPT-6):**
[R1.10, Theorem 19](R1_selected_tasks.md) proves recovery for n>=3, and
Proposition 20 gives a strictly positive example showing that two past
performances can be insufficient. One history suffices for almost every
positive assignment kernel in a finite-state model, while Theorem 21
identifies the limiting optima. In the original 200 random worlds with full-support skill-dependent
choice, the optimal delineations at $`n=1`$ were exactly the refinements of
the partition by proportional joint kernels
$`q(z\mid\theta)f(\cdot\mid\theta,z)`$; this is not a theorem, and it fails
in degenerate cases (twins chosen differently when no outcome depends on
skill).

**Other limits of this result.**

- **Twins are invisible under independent assignment.** Under A1, raw
  labels that differ only within a twin class are not recovered by any
  outcome-based evaluation (phase one, F.4). Under skill-dependent choice,
  assignment labels can carry additional finite-history information, as
  Proposition 5 and R1.10 explain.
- **Best forecast, known model.** $`V_n(c)`$ scores the best judge using
  $`c`$. A poor judge with the right delineation can score below a good judge
  with a coarser one, and judges who must learn the outcome laws from finite
  data are not treated. Under exact Bayes forecasting, needless splits cost
  nothing, so optimality alone gives refinements of $`\bar z`$ and the fixed
  point (or a cost of distinctions) is what selects $`\bar z`$ itself.
  *Added in session 2:* for bounded judges needless splits do cost score,
  and $`\bar z`$ is the unique optimum given enough history
  ([R1.2, Theorem 6](R1_judges_without_oracle.md#5-bounded-judges-select-the-transfer-partition-itself)).
- **An outcome oracle.** The evaluator sees later outcomes. Judges credited
  only by later judgments are treated in [R1.2](R1_judges_without_oracle.md).

## 5. The physics-task instance

Performers are four model builds that include or neglect a drag correction
and a special-relativistic correction. Tasks fall in three regimes: slow
vacuum, slow with drag, fast vacuum. A build is adequate in a regime when
every correction it neglects is below the tolerance there, with illustrative
log-sizes ($`-1.2`$ for drag in the drag regime, $`-2`$ for the relativistic
term in the fast regime, negligible elsewhere), and the judged outcome is
adequacy flipped with probability 0.05.

| log₁₀ tolerance | Recovered without reappearance | Recovered with reappearance |
|---|---|---|
| $`-1`$ (loose) | one task | one task |
| $`-1.5`$ | {slow vacuum, fast vacuum}, {drag} | the same |
| $`-3`$ (strict) | {slow vacuum}, {drag, fast vacuum} | three tasks |

Two things are visible. **What counts as one task depends on the standard of
judgment:** at a loose tolerance the Newtonian and relativistic regimes are
the same task, and at a strict one they are not. **At the strict tolerance
the drag regime and the fast regime are equally hard on average and are
separated only by reappearance,** because the builds that handle one are not
the builds that handle the other.

## 6. Checks

Exact enumeration, no sampling, in
[exact_scores.py](../notebook/P4-R1-C001/exact_scores.py),
[selection_probe.py](../notebook/P4-R1-C001/selection_probe.py) and
[stability_check.py](../notebook/P4-R1-C001/stability_check.py), with saved
outputs beside them. For every set partition of the types:

- Theorem 1(a)-(d) held in three designed worlds, the three physics
  tolerances and 300 random worlds with two or three outcomes, a forced twin
  pair and, where feasible, a forced equal-difficulty pair, for $`n\le2`$
  (up to $`n\le5`$ in designed worlds). Zero violations. The smallest
  deficit of a non-refinement at $`n=1`$ was $`3.2\times10^{-7}`$ nats,
  against a comparison tolerance of $`10^{-10}`$.
- Theorem 2's bound held in all 1,200 merged pairs from 400 random worlds,
  including nearly-twin types; the actual deficit was at least 14 times the
  bound.

These checks support the statements on small finite worlds. They are not a
substitute for review of the proofs.

## 7. Closest established work and the difference

Sources were consulted at the level of abstracts and stated theorems; no
proof was reconstructed from them and no novelty clearance is claimed.

- **Causal states and the refinement lemma.**
  [Shalizi and Crutchfield](https://arxiv.org/abs/cond-mat/9907176) show that
  any partition of a process's pasts that predicts as well as the causal
  states refines them almost everywhere, and that the causal states are the
  minimal sufficient statistic for prediction. Theorem 1(b)-(c) is the same
  kind of statement for a different object: a partition of *task instances*
  applied slot by slot to a performer's history and target, whose
  predictive role exists only through the performer's reappearance.
- **Twin-free graphons.**
  [Borgs, Chayes and Lovász](https://arxiv.org/abs/0803.1244) call two
  points twins when their kernel sections agree almost everywhere and show
  that every graphon reduces to a twin-free one, unique up to isomorphism.
  The transfer partition is the twin reduction of the performer-by-task
  outcome kernel on the task side.
- **Latent block models.**
  [Keribin, Brault, Celeux and Govaert](https://doi.org/10.1007/s11222-014-9472-2)
  study estimation and selection for categorical latent block models,
  extending earlier binary models. Under suitable identification assumptions,
  co-clustering a performer-by-task table can target the same column classes.
- **Information elicitation.**
  [Kong and Schoenebeck](https://arxiv.org/abs/1605.01021) pay agents an
  information-monotone measure of dependence between their reports, and in
  [later work](https://arxiv.org/abs/1802.08887) show that under
  independence conditional on the ground truth the Bayes posterior
  predictors maximize the mutual-information gain. This is the natural tool
  for judges evaluated only against each other.

What this result adds, at the level actually supported: the identification
of the reappearance threshold (difficulty at $`n=0`$, transfer at every
$`n\ge1`$) with an elementary second-moment proof; the explicit stability
bound; the typed judge/delineation correspondence with its unique optimal
fixed point; and the reading of these as C1 and C2. An equally informed
co-clustering method can recover the same population partition. This common
target is informative, but it does not make a likelihood-based co-clustering
algorithm identical to the conditional prediction objective V_n. Their
finite-data assumptions, costs and procedures require separate comparison.

## 8. Gap to the theses

- **C1** asks for recovery that first-order judgment cannot achieve. Shown:
  with an outcome oracle, exactly the transfer facts are added by
  reappearance. Not shown: recovery when judges are evaluated only by other
  judges; finite-data rates; learned forecasters.
- **C2** asks that the task partition and the judge weighting determine each
  other. Shown: the partition and the optimal judge do, at a unique fixed
  point. Not shown: a weighting over many fallible judges, and the dynamics
  that reach or miss the grounded fixed point.
- This result alone does not treat excellence exemplars, learned judge
  weights, or C5. Subsequent cycle results address those restricted topics
  in [R1.2](R1_judges_without_oracle.md), [R1.3](R1_excellence_exemplars.md),
  [R1.5](R1_weight_dynamics.md) and [R1.9](R1_coupled_reappearance.md).
  Broad self-trust and the full incremental-information question remain open.
