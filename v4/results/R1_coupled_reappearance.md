# R1.9 Coupled judgment and conceptual kinds under self-influenced recurrence

**Author:** Codex (GPT-6), November 10, 2026. **Cycle:**
[P4-R1-C001, S6](../notebook/P4-R1-C001/record.md).
**Theses:** C1, C2; a bounded construction relevant to C3/C5 and the W7 handoff.
**Evidence:** a population-level proof, independently implemented ODE checks,
and a bounded comparison with established work. Written and checked by the
same model; not independently confirmed. This is a construction for the
specified learning and selection dynamics.

## The proposed contribution

Judges here do three things together: forecast what will be seen again, help
cause those sightings, and gain or lose influence according to predictive
success. They use different conceptual partitions. Under a positive share of
environmental recurrence and continued learning by alternatives, the candidate
construction drives the forecasts toward the environmental recurrence law and
selects precisely the partitions capable of representing it. A coarsest
predictively sufficient partition can then be read from that law.

This couples the kinds in [R1.6](R1_reappearance.md) to the feedback in
[R1.7](R1_who_determines_reappearance.md). The scoring rule is quadratic and
strictly proper, and all judges forecast the same underlying events. Their
conceptualisations determine what information they retain; they do not receive
different scientific questions merely by renaming an event.

## 1. Common events, concepts and forecasts

Let the observable alphabet W be finite, with known reference frequencies
$`\mu_x>0`$, summing to one. Equip matrices with

```math
\langle A,B\rangle_\mu=\sum_{x,y}\mu_x\mu_y A_{xy}B_{xy},
\qquad \|A\|_\mu^2=\langle A,A\rangle_\mu.
```

An admissible recurrence density R is symmetric, nonnegative, and satisfies
$`\sum_y\mu_yR_{xy}=1`$ for every x. It forecasts the next event by
$`P_R(Y=y\mid X=x)=\mu_yR_{xy}`$. Thus all such recurrence laws have marginal
mu and are reversible. This is a substantive model restriction.

The environment has one admissible density F. In the conditional-i.i.d. model
of R1.6 it is

```math
F_{xy}=\mathbb E[\ell_x(\theta)\ell_y(\theta)],
\qquad \ell_x(\theta)=L(x\mid\theta)/\mu_x.
```

The dynamics below also make sense for admissible F without that Gram form.

There is a finite catalogue C of conceptual partitions, including the finest
partition f. For a partition c let $`\Pi_c`$ be conditional expectation under
the reference product law mu x mu given $`(c(x),c(y))`$. Explicitly, if x and y
are in cells A and B,

```math
(\Pi_c R)_{xy}
=\frac{\sum_{u\in A,v\in B}\mu_u\mu_vR_{uv}}{\mu(A)\mu(B)}.
```

This is an orthogonal projection in the displayed inner product. It preserves
admissibility. A c-judge's density $`R_c`$ satisfies $`\Pi_cR_c=R_c`$.
Its predicted mass of kind B is $`\mu(B)R_c(A,B)`$; within B its decoder uses
$`\mu_y/\mu(B)`$. That decoder and reference frequencies are part of its
information representation, not missing distinctions supplied for free later.

## 2. Ratings cause recurrence and compete for influence

Let $`w_c\ge0`$ sum to one and define

```math
\bar R=\sum_cw_cR_c,
\qquad Q=eF+(1-e)\bar R,\qquad 0<e\le1.
```

With probability e, the environment determines the next sighting using F.
Otherwise the community's weighted forecasts help produce it, using bar R.
Both mechanisms condition on the same current observation. Ratings therefore
change the distribution on which their predictive success is measured.

Use the proper quadratic score on recurrence densities,

```math
S(R;x,y)=2R_{xy}-\sum_v\mu_vR_{xv}^2,
\qquad s_c=\mathbb E_{\mu_x\mu_yQ_{xy}}S(R_c;X,Y)
=2\langle R_c,Q\rangle_\mu-\|R_c\|_\mu^2.
```

For a fixed Q, the best c-forecast is $`\Pi_cQ`$. Consider the simultaneous
population equations

```math
\dot R_c=\eta_c(w,R)(\Pi_cQ-R_c),
\qquad
\dot w_c=w_c\left(s_c-\sum_dw_ds_d\right).
```

The first equation calibrates forecasts from the distribution of later
observations. The second reinforces the kinds used by successful forecasters.
The rates are locally Lipschitz and satisfy fixed bounds
$`0<\eta_{\min}\le\eta_c\le\eta_{\max}<\infty`$. Every model continues
calibrating even when its current influence is small or zero. The finest
model starts with positive weight. Other starting weights may be zero.

This condition allows a fixed total learning budget. If one unit of a
c-model's update costs kappa_c > 0, allocate a budget B > 0 with a reserve
0 < b <= B among m models:

```math
\eta_c=\frac{b/m+(B-b)w_c}{\kappa_c},
\qquad \sum_c\kappa_c\eta_c=B.                                  \tag{18.1}
```

The reserve buys continued learning by alternatives. The cost units here
are declared rates of population learning; finite-sample computation costs
have not been measured. Finding a tractable catalogue remains a separate
obligation.

These are population equations using exact expected signals. They specify a
mathematical composition, not a proved finite-sample learner. The environment
law F is used in the analysis; calibration can in principle estimate Pi_c Q
from observations without being told F. That estimation needs its own analysis.
Calibration responds to the current distribution while holding it fixed for
the update. It is an assumed learning rule, not a claim that a strategic
forecaster maximizing its total influence on outcomes would choose that rule.

## 3. The convergence argument

**Theorem 18 (coupled recovery with persistent learning).** Under the stated assumptions,
let $`\delta_c=\|F-\Pi_cF\|_\mu^2`$. Then Q and bar R converge to F, every
forecast R_c converges to Pi_c F, and total weight on partitions with
delta_c > 0 tends to zero. Every initially present partition with delta_c=0
retains positive limiting weight; all weights converge. The environment may
have any positive share e, but the time to recover can become large as e
shrinks.

*Proof.* The admissible matrices and weight simplex form a compact invariant
set. Positivity of an initially positive weight is preserved at every finite
time. Consider

```math
\mathcal P
=2e\langle F,\bar R\rangle_\mu+(1-e)\|\bar R\|_\mu^2
 -\sum_cw_c\|R_c\|_\mu^2
=e\|F\|_\mu^2-e\|F-\bar R\|_\mu^2
 -\sum_cw_c\|R_c-\bar R\|_\mu^2.
```

Differentiating with respect to weights gives s_c; differentiating within a
judge's projected space gives $`2w_c(\Pi_cQ-R_c)`$. Consequently,

```math
\dot{\mathcal P}
=\mathrm{Var}_w(s_c)+2\sum_cw_c\eta_c\|\Pi_cQ-R_c\|_\mu^2\ge0. \tag{18.2}
```

The derivative is uniformly continuous on the compact invariant set and has
finite integral, so it tends to zero. Cauchy--Schwarz applied to
$`\dot{\bar R}=\sum_c\dot w_cR_c+\sum_cw_c\dot R_c`$ now gives
$`\dot Q\to0`$. For every c, even one of zero weight,
$`h_c=R_c-\Pi_cQ`$ obeys
$`\dot h_c=-\eta_ch_c-\Pi_c\dot Q`$. The positive lower rate bound and
variation of constants imply that h_c tends to zero.

For fixed weights the calibration equations have a unique solution: the map
$`R_c\mapsto\Pi_c[eF+(1-e)\sum_dw_dR_d]`$ contracts the maximum entry norm
by 1-e. The distance to this solution is at most
$`\max_c\|h_c\|_\infty/e`$, uniformly over weights.

At an exactly calibrated profile put
$`d=F-\bar R`$ and
$`V=\sum_cw_c\|R_c-\bar R\|_\mu^2`$. Since R_c=Pi_c Q and R_f=Q,

```math
E:=e\|F\|_\mu^2-\mathcal P=e\|d\|_\mu^2+V,
\qquad
s_f-\sum_cw_cs_c=e^2\|d\|_\mu^2+V\ge eE.
```

If the decreasing potential gap E had a positive limiting value, uniform
closeness to calibration would eventually give
$`d(\log w_f)/dt\ge eE_\infty/2>0`$. This contradicts w_f <= 1.
Thus E tends to zero, so bar R and Q tend to F. The stable calibration
equations then give R_c -> Pi_c F for every c.

The projection identity and variance decomposition give

```math
E\ge e\sum_cw_c\|F-R_c\|_\mu^2\ge e\sum_cw_c\delta_c.
```

Thus nonsufficient partitions lose all mass. Their limiting score deficit is
delta_c, so each initially present nonsufficient weight eventually decreases
at least exponentially at rate delta_c/2. Set E_c=R_c-Pi_c F. The calibration
equations and the maximum-norm contraction imply

```math
\frac{d^+}{dt}\max_c\|E_c\|_\infty
\le-\eta_{\min}e\max_c\|E_c\|_\infty
 +C\sum_{c:\delta_c>0}w_c
```

for a fixed finite C. Hence forecast errors and score errors decrease
exponentially after a finite transient (with a possible polynomial factor
when rates coincide). Score differences between sufficient partitions are
integrable. Their log weight ratios therefore converge to finite numbers.
Together with the vanishing nonsufficient mass, this proves the final weight
claims. QED.

## 4. Why the surviving kinds are factual in this model

In the R1.6 Gram setting, Pi_c F=F exactly when c refines its diagnostic
partition c*. One direction follows because equal normalized likelihoods
give equal rows and columns. Conversely, identical rows for x and x' imply
that ell_x-ell_x' is orthogonal to every ell_y. It belongs to their span,
so its squared norm is zero. Thus the coarsest partition read from the
limiting forecast is precisely c*.

This is a typed, dynamic reading of T = J²: predictive evaluation changes
which conceptualisations have influence, and the limiting judgment reveals
the coarsest sufficient conceptualisation. The result selects sufficient
refinements; removing their idle labels is the explicit row-equivalence
operation. It does not claim that every population converges to one syntactic
vocabulary or that a finer label set is always better at finite resources.

## 5. The reserve matters: a matched failure and repair

Let W have two equiprobable symbols, s=(1,-1), and F=1+a ss^T with a=1/2.
There are two concepts: the constant partition, whose only admissible density
is 1, and the finest partition, with density 1+b ss^T and weight w. With
e=1/2, the coupled equations reduce to

```math
q=ea+(1-e)wb,\qquad
\dot b=\eta(w)(q-b),\qquad
\dot w=w(1-w)(2bq-b^2).                                        \tag{18.3}
```

**Failure when only influence funds learning.** Take eta(w)=w, w(0)=1/100
and b(0)=-1/2. While -1/2 <= b <= -1/4 and w <= 1/100,

```math
2bq-b^2=\tfrac12b+(w-1)b^2\le-299/1600.
```

Consequently w decreases at least as fast as
exp(-kappa t), where kappa=(99/100)(299/1600)=0.18500625.
On this region 0 <= dot b <= (3/4)w. Its total possible increase is at most
(3/4)(1/100)/kappa < 0.04055, too small to leave the region through b=-1/4.
This closes the bootstrap: w tends to zero and the useful fine model never
corrects its initially wrong sign. Positive environmental exposure alone
does not rescue a model whose learning vanishes with its influence.

**Repair with the same learning budget.** Give the two models rates
eta_f=nu+(1-2nu)w and eta_coarse=nu+(1-2nu)(1-w), with 0<nu<1/2.
Their rates still sum to one. Theorem 18 now gives w -> 1 and b -> a.
The reserve reallocates some effort to alternatives; it does not add total
learning effort in this comparison.

**Weak exposure can be slow.** At the coarse boundary w=0 the rare fine
model calibrates to b=ea. Its local invasion rate is e^2 a^2. Thus the
qualitative guarantee for every e>0 is compatible with a long transient as
environmental exposure shrinks. No uniform recovery time independent of e
or of predictive separation is claimed.

## 6. Other limits with constructive follow-ups

- **Environmental share.** With e=0, an arbitrary consensus recurrence
  density can sustain itself. Positive e supplies a route to grounding under
  the other assumptions; it is not by itself a universal guarantee.
- **Strategic forecasts.** A strictly proper score evaluates predictions
  correctly for a fixed outcome distribution. A forecaster that optimizes
  how its report changes that distribution faces a different problem.
  The present construction specifies calibration; incentives to adopt it
  need a mechanism or behavioral argument. Reference-policy evaluation or
  correction for known self-caused recurrence offers a constructive route.
- **Available concepts.** The finest partition is present with positive
  starting weight. A catalogue without a needed distinction may remain
  insufficient. Mutation or exploration that introduces the distinction is
  an important extension, not supplied by this theorem.
- **Population expectation.** Finite-data calibration, noisy competition,
  limited computation and endogenous reference frequencies remain open.
  The potential provides a starting point for robustness bounds and tests.
- **External kernel.** F is fixed while ratings change the sightings. A
  changing environment can create new useful distinctions; the conditions
  for tracking them belong to the next development of this construction.

## 7. Evidence and closest work

[coupled_reappearance.py](../notebook/P4-R1-C001/coupled_reappearance.py)
integrates these population equations using SciPy. Log weights and symmetric
joint-mass coordinates preserve the weight simplex, forecast symmetry and
reference marginals. It does not import the earlier Fable dynamics. The
[saved checks](../notebook/P4-R1-C001/coupled_reappearance.json) include:

| Check | Result |
|---|---|
| Potential derivative, 16 profiles and rate choices | Largest scaled finite-difference error 3.8e-11 |
| Two kinds, four symbols; e=1 or 0.2, unit rates or reserved budget | Nonsufficient mass below 2e-7 by time 1200 |
| Same four-symbol test with an alternating, non-Gram reversible kernel | Recovery by time 1200 |
| Unequal marginal frequencies and a weak distinction | Nonsufficient mass 0.09536 and maximum mean-forecast error 0.008919 at time 12000 |
| Continuation of that weak-distinction test | Nonsufficient mass 1.42e-12 or less by total time 60000 |
| Rare model, learning proportional to influence | Weight tends numerically to zero; b remains near -0.48472 |
| Same initial state and total budget, reserve nu=0.05 | Weight tends to one; b tends to 0.5 |

The weak-distinction trial initially failed an overly strong finite-horizon
expectation. Both checkpoints are retained. Numerical agreement with a limit
is not a finite-time theorem. Sampled potential decreases were at floating
roundoff scale, and the zero-exposure and missing-concept cases retained
incorrect forecasts as predicted.

The closest established comparisons clarify what is and is not added:

- [Perdomo et al. (2020), Performative Prediction](https://proceedings.mlr.press/v119/perdomo20a.html),
  especially Theorem 3.5, supplies contractive retraining conditions and
  distinguishes deployment optimality from stability. Here the linear
  environmental mixture is contractive at fixed weights; the extra argument
  handles changing concept weights and rules out persistent insufficient
  representations. The common reversible marginal and finite catalogue
  remain substantial restrictions.
- [Oesterheld et al. (2023)](https://proceedings.mlr.press/v216/oesterheld23a.html),
  Proposition 1 and section 8 with Appendix D, separates performative score
  maximization from calibration and analyzes stable updates. Its no-regret
  comparison includes the current true conditional forecast as a dynamic
  comparator. It should not be identified with ordinary regret to a fixed
  finite list of initially specified models. Theorem 18 adds the stated
  competing representation and learning-allocation construction; it does
  not solve strategic honesty.
- [Mertikopoulos and Sandholm, Riemannian Game Dynamics](https://arxiv.org/abs/1603.09173),
  Proposition 6.4, gives potential ascent and convergence to rest points for
  a broad class of game dynamics. The identity (18.2) uses this familiar
  geometry. Potential ascent alone does not establish environmental recovery:
  the continued calibration and positive finest-model weight argument
  exclude insufficient boundary limits here.
- [Boeken, Zoeter and Mooij (2025)](https://arxiv.org/abs/2510.21335v1),
  sections 2--5 and Appendix D, treats conditional forecasts, performative
  divergence and inverse-probability corrections. It supplies relevant
  mechanisms for the strategic and reference-policy extension, with
  different assumptions from the dynamics proved here.

The candidate contribution is the explicit coupled construction, its
representation-recovery conclusion and the fixed-budget failure/repair.
Proper scoring, projection, replicator dynamics and potential arguments are
established ingredients. The comparison supports developing this synthesis;
it is not an exhaustive theorem-level novelty clearance.
