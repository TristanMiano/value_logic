# R1.7 Who determines what is seen again: ratings that cause recurrence

**Author:** Claude (Fable 5.2). **Date:** November 10, 2026. **Cycle:**
[P4-R1-C001](../notebook/P4-R1-C001/record.md), session 5 (cycle unfinished).
**Theses:** C1, C3, C5; handoff from W1 to W6 and W7. **Status:** a small
linear model with elementary proofs and matching simulations, by one model;
not independently reviewed. It is a first model, not a general theory.

**S6 review, Codex (GPT-6), November 10, 2026:** the adaptive-consensus
argument is retained; centering and the neutral stability boundary are made
explicit below. A simultaneous forecast/concept-weight construction with
actual probability forecasts is developed in [R1.9](R1_coupled_reappearance.md).

## The author's framing

Tristan Miano, November 10, 2026, on why J should be the general forecast of
reappearance of [R1.6](R1_reappearance.md): "something has to determine
'success'. That could either be the same agent, another agent, or something
in the environment that requires it."

In R1.6 things reappear because of a persistent state, whatever the
ratings. Here a rating can itself be a cause: what is rated well is repeated,
by the rater or by others, and the environment also keeps or removes things
on its own terms.

## What this shows

- **When only raters determine reappearance, every consensus is borne out.**
  Ratings forecast what will be seen again and also produce it, so
  vindication is guaranteed and carries no information about the world
  (Theorem 15(a)). This is the essay's remark that an embedded agent's
  prediction of its own output is a preference.
- **Raters who adjust their ratings toward being borne out end up tracking
  the environment, however small its share.** The self-fulfilling part of
  vindication rewards all ratings equally, so it cannot choose between
  them; any environmental share breaks the tie. The limit is the
  environment's own ordering of things, reached in a time inversely
  proportional to that share and independent of how strongly ratings cause
  recurrence (Theorem 15(b)). Conventions unrelated to the world are
  therefore long-lived but not stable.
- **When raters are fixed and only their influence changes, conventions can
  lock in.** A consensus around one rater is stable exactly when no rival
  tracks the environment better by more than a margin that grows with the
  strength of rating-caused recurrence and with the rival's dissimilarity.
  Strict inequalities give asymptotic stability; equality needs the boundary
  analysis below. The best available tracker's consensus is stable, with
  neutral ties possible; worse ones
  survive when the environment's share is small (Theorem 15(c)).

Read as a statement about truth as a limit (C3): the factual limit exists
and is reached when judgment can revise itself and the world has any say;
it can be blocked when the only movement is the redistribution of influence
among fixed judges.

## 1. Model

Things $`w`$ have an environmental fitness $`\varphi(w)`$. Subtract its
mean over the fixed reference set; henceforth phi denotes this centered
vector. Adding a constant to growth does not alter the comparisons. Rater $`j`$ has a
rating vector $`r_j`$ over things, centred and of unit norm, and weight
$`w_j`$; $`\bar r=\sum_jw_jr_j`$. The log growth of a thing is

```math
g=\beta\,\bar r+e\,\varphi ,
```

with $`\beta\ge0`$ the strength with which ratings cause recurrence (the
same agent or other agents repeat what is rated well) and $`e\ge0`$ the
strength with which the environment does. A rater is vindicated to the
extent that its ratings forecast growth:
$`s_j=\langle r_j,g\rangle=\beta\langle r_j,\bar r\rangle+e\,h_j`$, with
$`h_j=\langle r_j,\varphi\rangle`$ its alignment with the environment. One
agent rating its own behaviour is the case of a single rater.

## 2. Result

**Theorem 15. Evidence: proved for this model; simulations agree in every
case run.**

- **(a) Raters only.** If $`e=0`$ and raters agree, $`s_j=\beta`$ for every
  common rating vector: all consensuses are equally and fully vindicated.
- **(b) Adaptive ratings.** Let each rater move its rating vector up the
  gradient of its own vindication, staying on the unit sphere, starting from
  a common vector. If $`e>0`$ and the centered phi is nonzero, the ratings converge to
  $`\varphi/\|\varphi\|`$ from every start except its exact opposite, the
  alignment $`a=\langle r,\varphi\rangle/\|\varphi\|`$ obeys
  $`\dot a=e\|\varphi\|(1-a^2)`$, and $`\beta`$ does not enter.
- **(c) Fixed raters.** Let weights follow the replicator dynamic
  $`\dot w_j=w_j(s_j-\sum_kw_ks_k)`$. Consensus on rater $`j`$ is
  asymptotically stable if, for every other rater
  $`k`$
  ```math
  e\,(h_k-h_j)<\beta\,\bigl(1-\langle r_k,r_j\rangle\bigr).
  ```
  If the inequality is reversed strictly for some rival, consensus is
  unstable. At equality with beta>0 and distinct rating vectors it is also
  unstable, by the second-order edge calculation below. Equality with
  beta=0, or between identical rating vectors, can instead give a neutral
  face. The largest-alignment rater is asymptotically stable when beta>0
  and all rivals have distinct vectors, or when beta=0, e>0 and its
  alignment is uniquely largest. Tied maxima at beta=0 are neutrally stable.

*Proof.* (a) $`\langle r,\beta r\rangle=\beta`$ on the unit sphere. (b) The
gradient of $`\langle r,\beta r+e\varphi\rangle`$ with the creditors' mean
held at $`r`$ is $`\beta r+e\varphi`$; its projection on the tangent space
at $`r`$ is $`e(\varphi-\langle r,\varphi\rangle r)`$, because the
projection annihilates $`r`$. This is gradient ascent of
$`\langle r,\varphi\rangle`$ on the sphere, which gives the equation for
$`a`$. (c) At the vertex $`j`$, $`s_j=\beta+eh_j`$ and
$`s_k=\beta\langle r_k,r_j\rangle+eh_k`$. A vertex is asymptotically stable
under the replicator dynamic when it is a strict best reply to itself and
unstable when some other strategy does strictly better against it. To handle
equality, put mass x on rival k and 1-x on j. Let
d=1-<r_k,r_j> and D=e(h_k-h_j)-beta d. The rival's payoff advantage on
this edge is D+2 beta d x. At D=0, beta d>0 implies positive advantage for
every x>0, so the vertex is unstable. If beta d=0, the advantage is zero
on the whole edge, giving a neutral direction rather than attraction.
$`\square`$

## 3. Simulations

[selection_by_rating.py](../notebook/P4-R1-C001/selection_by_rating.py),
seed 20261110.

- **(c).** Six fixed raters with alignments 0.1, 0.3, 0.5, 0.7, 0.0 and
  −0.3 to the environment, 60 things, $`\beta=1`$. Stability of each
  consensus predicted by the inequality and observed by simulation agreed in
  all 30 cases. With $`e/\beta\le1`$ all six consensuses were stable,
  including the one opposed to the environment; at 3 only the two best; at
  10 only the best. From equal weights the best tracker won whenever
  $`e>0`$; at $`e=0`$ the winner (alignment 0.3) was decided by the raters'
  mutual similarity alone.
- **(b).** Eight raters started on a shared convention with zero alignment.
  With $`e=0`$ nothing moved in 4,000 time units. With $`e=0.01,0.1,1`$
  alignment one half was reached at times 57.0, 5.67 and 0.56; with
  $`\beta`$ raised tenfold at $`e=0.1`$ the time was 5.76.

## 4. The three sources

| What determines reappearance | In the model | What vindication certifies |
|---|---|---|
| The same agent | one rater, $`e=0`$ | nothing beyond the agent's own policy |
| Other agents | several raters, $`e=0`$ | membership in the prevailing consensus (compare R1.2's self-confirming states) |
| The environment | $`e>0`$ | alignment with the environment, in the limit under (b), conditionally under (c) |

The earlier results of this cycle that needed an outcome evaluator
(R1.1), or approvals that are honest reports of outcomes (R1.2, R1.4), are
cases where the environment's share is supplied by assumption. R1.4 found
that unconstrained task-specific approval channels conceal positive affine
calibration, including mean and sensitivity; here a related role
appears dynamically: the environment's share is what selects among
otherwise equally self-consistent ratings.

## 5. Limits and named obligations for W6 and W7

- **Linear and static.** Growth is linear in ratings and fitness; the
  population of things is held fixed as a reference instead of evolving
  under its own growth; ratings are compared by inner product, a coarse
  stand-in for the forecasts of R1.6.
- **Fitness is given.** What makes a thing fit, and whether fitness itself
  depends on what agents do or value, is exactly the subject of W7.
  Instrumental convergence (W6) would enter as structure shared by the
  fitness functions of different goals.
- **Conceptualisation and simultaneous adaptation.** Things are taken as
  given kinds here. [R1.9](R1_coupled_reappearance.md) now gives a distinct
  coupled construction with different partitions, calibrated probability
  forecasts and changing influence. It supplies one bridge, not a proof
  that every mixed extension of this unit-sphere model converges.

## 6. Closest established work

Quoted from memory. The replicator dynamic and the stability of strict
equilibria are standard in evolutionary game theory; (c) is a coordination
game with a payoff tilt, and its lock-in is the familiar multiplicity of
conventions. The indirect evolutionary approach to preferences (Dekel, Ely
and Yilankaya, cited in the phase-four initialization review) studies when
selection on material payoffs shapes subjective preferences; (b) is a
minimal instance in which it always does. What is added is the framing by
who determines reappearance and the connection to the vindication results
of this cycle.
