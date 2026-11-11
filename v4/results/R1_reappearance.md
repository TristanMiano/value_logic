# R1.6 Judgment as a forecast of reappearance: finer concepts capture more, up to the world's own distinctions

**Author:** Claude (Fable 5.2). **Date:** November 10, 2026. **Cycle:**
[P4-R1-C001](../notebook/P4-R1-C001/record.md), session 4 (cycle unfinished).
**Theses:** C1, C2. **Status:** proof and checks by one model; not
independently reviewed. The partition involved is classical (section 6).

**S6 review, Codex (GPT-6), November 10, 2026:** Theorem 13 was
reconstructed and checked using a separate rational-probability implementation.
The comparison with R1.1 is corrected in section 3: a common proper-scoring
framework does not make the two objectives identical.
[R1.8](R1_quantitative_recovery.md) supplies an explicit diagnostic bound.

## The author's statement this formalises

Tristan Miano, November 10, 2026:

> Intuitively, I expect J to be something like a prediction that a certain
> task will be done again (or rather, that a positive rating means it will be
> seen again, negative that it will not). Tasks themselves can be broken down
> into task types and task sub-types and so on. In order to do J "well", one
> must be able to recognize those sub-types well enough to make ever more
> granular predictions. Those who are more capable predictors at judgement
> would therefore have very refined conceptualizations of their observable
> world.

Earlier results in this cycle read J more narrowly, as a forecast of a
performer's later *result*. Here J forecasts that *what was seen* will be
seen again, which is the author's reading. Proper forecasting accommodates
both questions, with their different targets and side information explicit.

## What this shows

- **"It will be seen again" needs a concept of "it".** A judgment about one
  thing is a forecast about a kind, and the kind is fixed by the judge's
  conceptualisation. So task delineation is not an extra step before
  judging; it is what gives a judgment its content.
- **Finer concepts never capture less, and capture strictly more until they
  resolve every two things that recur differently** (Theorem 13). Two things
  "recur differently" when seeing one or the other changes what should be
  expected next. Past that point further splitting captures nothing. The
  judges who predict best therefore all share one conceptualisation, up to
  idle distinctions, and it is fixed by the world.
- **Types, sub-types and so on form a ladder of gains.** Each split of a
  kind is worth drawing exactly when its two sides, as currently grouped,
  recur differently, and the gains add up to the total available. In the
  worked hierarchy: 0.179 nats for the first split into two types, 0.0105
  for sub-types, 0.0002 for sub-sub-types, and exactly zero for a fourth
  level that the world does not have.
- **More capable judges have more refined concepts, in two senses.** A judge
  who captures nearly all the available information cannot be merging any
  two kinds whose merging would lose more than its shortfall. And a judge
  who must learn from limited experience does best with coarse concepts at
  first and finer ones as experience grows: in the same hierarchy the best
  level was the first up to 8 sightings, the second from 16 to 128, and the
  third from 256, never the idle fourth.

## 1. Setting

There is a persistent state $`\theta\sim P`$: who is acting, or what regime
holds. Given $`\theta`$, the things seen $`W_1,W_2,\dots`$ are independent
with law $`L(\cdot\mid\theta)`$ on a finite set; a thing can be a task, a
task with how it turned out, or any observable event. A
**conceptualisation** $`c`$ groups things into kinds. A judgment on
$`W_1`$ at granularity $`c`$ is a forecast of the kind of $`W_2`$ from the
kind of $`W_1`$, and its worth is

```math
I(c)=I\bigl(c(W_1);c(W_2)\bigr),
```

the information that the kind of thing seen once carries about the kind
seen next. Two things are **equally diagnostic** when their likelihoods are
proportional as functions of the state,
$`L(w\mid\theta)/L(w)=L(w'\mid\theta)/L(w')`$ almost surely. Write $`c^*`$
for the conceptualisation that merges exactly the equally diagnostic things.

Only observations with positive marginal probability are included. I(c) is
the best log-score gain over the unconditional baseline for the c-label,
not its unadjusted probability of reappearing. In an i.i.d. world with
unequal event frequencies and no varying state, c* has one cell and I=0.
The individual frequencies still matter for forecasting: a one-cell model
can retain them in an explicit within-cell decoder. The theorem recovers
state-diagnostic distinctions, not every difference in marginal frequency.

## 2. Result

**Theorem 13. Evidence: proved; checked on 200 random worlds over all 203
conceptualisations of six things.**

- **(a)** If $`c'`$ refines $`c`$ then $`I(c')\ge I(c)`$.
- **(b)** $`I(c)\le I(c^*)=I(W_1;W_2)`$ for every $`c`$, with equality
  exactly when $`c`$ refines $`c^*`$.
- **(c)** If $`c'`$ splits one kind $`\kappa`$ of $`c`$ in two, then
  $`I(c')>I(c)`$ exactly when the two parts have non-proportional
  aggregate likelihoods
  $`g_{\kappa_i}(\theta)=\sum_{w\in\kappa_i}L(w\mid\theta)`$.

*Proof.* (a) is data processing. For $`I(c^*)=I(W_1;W_2)`$: the posterior
of $`\theta`$ given $`W_1`$ depends on $`W_1`$ only through its class, so
the law of $`W_2`$ given $`W_1`$ does too, and by symmetry the same holds
with the roles exchanged. For strictness, let $`c'`$ refine $`c`$ with
$`I(c')=I(c)`$. Then
$`I(c_1;c_0)\le I(c'_1;c_0)\le I(c'_1;c'_0)`$ are equalities, so
$`c'_0`$ is independent of $`c'_1`$ given $`c_0`$. Restricted to a kind
$`\kappa`$ of $`c`$ with parts $`\kappa_a`$, the chance that the next thing
is in $`\kappa_b`$ after one in $`\kappa_a`$ is proportional to
$`\Gamma_{ab}=\mathbb E[g_{\kappa_a}g_{\kappa_b}]`$ and must not depend on
$`a`$. A symmetric Gram matrix with proportional rows has rank one, so the
$`g_{\kappa_a}`$ are proportional. This is (c), and applied to the common
refinement of $`c`$ and $`c^*`$ it gives (b): the parts of a kind that
mixes two classes of $`c^*`$ are not proportional. $`\square`$

**Corollary 14 (capable judges are refined).** For two classes $`A,B`$ of
$`c^*`$ let $`\lambda(A,B)>0`$ be the loss $`I(c^*)-I(c)`$ for the $`c`$
that merges only $`A`$ and $`B`$. A conceptualisation that merges all of
$`A`$ with all of $`B`$ has $`I(c)\le I(c^*)-\lambda(A,B)`$. So a judge
within $`\eta`$ of the available information keeps apart every pair with
$`\lambda>\eta`$: the better the judge, the finer the distinctions it must
be drawing. *Proof.* Such a $`c`$ is refined by the common refinement of
itself and the merged $`c^*`$, whose worth is that of the merged $`c^*`$.
$`\square`$

**The ladder.** Along any chain from "one kind" to $`c^*`$ the gains of the
successive splits are non-negative and sum to $`I(W_1;W_2)`$. A hierarchy of
types and sub-types is such a chain with every gain positive. The order of
splits is not unique, and a gain depends on what has already been split.

## 3. One forecasting framework, with distinct questions

Let a thing be a task instance together with its result, $`W=(x,y)`$, in the
model of R1.1. Its likelihood is
$`q(x\mid\theta)\,f(y\mid\theta,z(x))`$, where $`q`$ may depend on the
state if performers choose their tasks.

- Under R1.1's independent assignment, twin tasks give equally diagnostic
  things (x,y) and (x',y), for every positive-mass result y. With
  skill-dependent assignment, their normalized joint likelihoods need not
  agree; assignment itself can convey persistent state.
- Theorem 13 applies directly to whole observations even under
  skill-dependent task choice: c* is the partition of individual
  (task,result) observations by proportional likelihoods. A task partition
  c induces the restricted representation (c(x),y). It is sufficient for
  this whole-observation game exactly when that induced representation
  refines c*. This is a statement about each retained result y, not an
  identification of a task partition with a partition of task/result pairs.
- It does not settle R1.1's open question about *outcome-only* prediction
  with unflagged assignment. Even under independent assignment,
  ```math
  I((c(X_1),Y_1);(c(X_2),Y_2))
  =H(Y_2\mid c(X_2))+V_1(c).
  ```
  The baseline depends on c. With no varying skill and task success
  probabilities 0.2 and 0.8, preserving task identity improves V_1 by
  0.1927447570 nats while all these pairwise mutual informations are zero.
  [R1.8, section 3](R1_quantitative_recovery.md#3-what-the-two-games-share-and-what-they-do-not)
  records the comparison.

Thus both readings make a conceptualisation answerable to future experience.
The precise predictive question determines which distinctions are useful.
T = J² reads here: scoring reappearance forecasts selects the kinds that
retain the predictive information relevant to that declared question.

## 4. Judges who learn from limited experience

A judge who does not know the state's frequencies estimates them at its own
granularity from $`n`$ sightings and is scored on the next thing seen.
Coarse kinds are estimated quickly and wrongly lumped; fine kinds are right
and slow. In the hierarchy of section 5 (40,000 simulated histories per
entry; expected log score, higher is better):

| Sightings | 2 types | 4 sub-types | 8 sub-sub-types | 16 (idle split) | Best |
|---|---|---|---|---|---|
| 1 | −2.598 | −2.740 | −2.959 | −3.139 | 2 types |
| 8 | −2.485 | −2.506 | −2.710 | −3.119 | 2 types |
| 16 | −2.472 | −2.455 | −2.574 | −2.870 | 4 sub-types |
| 128 | −2.449 | −2.383 | −2.393 | −2.444 | 4 sub-types |
| 256 | −2.447 | −2.377 | −2.375 | −2.398 | 8 sub-sub-types |
| 512 | −2.446 | −2.374 | −2.367 | −2.376 | 8 sub-sub-types |

Refinement follows experience, and the level that splits things the world
treats alike is never best. This is a simulation of one estimator in one
world, not a theorem; R1.2, Theorem 6 proves eventual selection of the twin
partition for a different bounded judge, not a universally nested path of
finite-history optima.

## 5. Checks

[reappearance.py](../notebook/P4-R1-C001/reappearance.py), seed 20261110.

- **Theorem 13.** 200 random worlds with six things and four states, half
  with a forced equally diagnostic pair: in every world the maximisers of
  $`I`$ among all 203 conceptualisations were exactly the refinements of
  $`c^*`$, and $`I`$ was monotone under refinement. Smallest loss of a
  non-refinement: $`2.5\times10^{-6}`$ nats against a tolerance of
  $`10^{-10}`$.
- **Ladder.** Sixteen things indexed by four bits and eight states indexed
  by three; bit $`l`$ of the thing interacts with bit $`l`$ of the state
  with strengths 1.0, 0.4, 0.15, and the fourth bit of the thing with
  nothing. $`I`$ at the five levels: 0, 0.1792, 0.1897, 0.1899, 0.1899;
  $`c^*`$ has eight kinds.

## 6. Closest established work

Quoted from memory. $`c^*`$ is the minimal sufficient partition of
classical statistics: observations are grouped when their likelihood ratios
agree. Theorem 13(b) is the corresponding statement that a statistic loses
no information exactly when it is sufficient, specialised to forecasting the
next observation and with the strictness argument made explicit; it is the
one-step, exchangeable counterpart of Shalizi and Crutchfield's refinement
lemma for causal states. That the best resolution of a learned model grows
with the amount of data is the content of minimum-description-length and
histogram-resolution results. What is added is small: the identification of
this structure with the author's J and T and the explicit one-step Gram
argument. The S6 review read [Shalizi and Crutchfield's refinement lemma
and proof](https://arxiv.org/abs/cond-mat/9907176v2). Section 3 now states
the relation to Theorem 1 without identifying their optimization problems.

## 7. Limits and named obligations

- **No feedback from rating to recurrence.** Things are seen again here
  because of the state, not because they were rated well. If a positive
  rating is also a cause of repetition, the process is a selection dynamic.
  That is not modelled here; [R1.9](R1_coupled_reappearance.md) provides a
  bounded simultaneous forecast/representation dynamic as a bridge to W7.
- **Conditionally independent sightings.** No learning by the performer and
  no order effects within a history.
- **A rating is coarser than a forecast.** A yes or no carries at most the
  information of the forecast it summarises. The theorem is about forecasts.
- **Explicit bound added:** [R1.8, Theorem 17](R1_quantitative_recovery.md)
  bounds the information loss using kind frequencies and normalized
  likelihood separation, with an asymptotically sharp binary example.
- **Capability as experience** is shown by simulation only.
