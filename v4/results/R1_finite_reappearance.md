# R1.11 Finite evidence for judgment under self-influenced recurrence

**Author:** Codex (GPT-6), November 10, 2026. **Cycle:**
[P4-R1-C001, S6](../notebook/P4-R1-C001/record.md).
**Theses:** C1/C2 through observed selection of useful distinctions; a
conditional grounding mechanism relevant to C3. **Evidence:** mathematical
construction, exact identities and reproducible finite simulations by one
model. This is a useful synthesis of established statistical and decision
tools, not a new concentration inequality or a confirmed new algorithm.

The population construction in [R1.9](R1_coupled_reappearance.md) explains
when evaluating judgments selects adequate concepts. Here a bounded
controller can collect evidence, retain it through changes in its own
behavior, and choose whether a distinction is useful before its parameter
is fully resolved. An explicit experiment can reveal environmental
recurrence even when the source of each observation is not labeled.

## 1. The same binary world, with finite observations

Let current and next observations be X,Y in {-1,+1}. The environmental
kernel has correlation a in [-1,1]: P(Y=y|X=x)=(1+a xy)/2. A constant
concept represents a=0; a two-kind concept represents every a. Put Z=XY.
Before each observation the controller chooses a mean b_t for its own
contribution. The actual conditional law is

```math
\mathbb E[Z_t\mid\mathcal F_{t-1}]
=e_t a+(1-e_t)b_t.                                            \tag{23.1}
```

The environmental share e_t and controller b_t may depend on the past.
The environmental a is fixed for the results in sections 2--5. This is a
binary Markov construction, or an experiment with fresh contexts and the
same conditional law. Equation (23.1) must not be inferred from an arbitrary
persistent-latent-performer history: there the posterior can change the
conditional environmental mean. The learner is not given a.

Two targets are distinguished. Predicting actual next sightings targets
e_t a+(1-e_t)b_t. Grounding a judgment in what the environment would produce
targets a. The latter is a declared reference experiment, not a relabeling
of the former. At grounded consensus b_t=a they coincide. The decision
payoffs below evaluate this reference environment.

## 2. Two observation modes, one retained evidence record

**Known-feedback mode.** Observe Z and know the chosen e>0 and b. Add

```math
\Delta U=e[Z-(1-e)b],\qquad \Delta V=e^2.                       \tag{23.2}
```

**Exclusion-probe mode.** Choose a fresh uniform sign A independently of
the past. The agent component produces Z=A exactly; the environment still
produces a sign of mean a, independently of A. The share e may be unknown,
but is chosen before A and does not depend on it. Accept only Z!=A. An
accepted observation adds (Z,1) to (U,V); a rejection adds (0,0).

**Theorem 23 (retained evidence across feedback changes).** Either mode,
or a predictable mixture of them, permits one common record (U_t,V_t).
For any preselected alpha in (0,1) and rho>0, with probability at least
1-alpha, simultaneously at every time with V_t>0,

```math
\left|\frac{U_t}{V_t}-a\right|
\le\frac{u_\alpha(V_t)}{V_t},\qquad
u_\alpha(v)=\sqrt{(v+\rho)\log\frac{v+\rho}{\rho\alpha^2}}.      \tag{23.3}
```

Intersect the interval with [-1,1]. Known changes in feedback do not require
discarding the earlier record. This retains evidence under the specified
mechanism changes, not under every counterfactual change to the environment.

*Proof.* In known-feedback mode, Delta U-a Delta V is conditionally
centered with range length 2e, so its exponential moment is bounded by
exp(lambda^2 Delta V/2). In probe mode,

```math
P(Z=z,\mathrm{accept}\mid\mathcal F_{t-1})
=\frac{e_t}{2}\,\frac{1+az}{2}.                              \tag{23.4}
```

Conditional accepted marks therefore have mean a. Rejections multiply the
exponential process by one; accepted marks have the same unit-variance
exponential bound. Thus exp{lambda(U-aV)-lambda^2 V/2} is a nonnegative
supermartingale in either mode. Mixing lambda with N(0,1/rho) gives
sqrt(rho/(V+rho)) exp{(U-aV)^2/[2(V+rho)]}. The maximal inequality and
inversion give (23.3). QED.

This is the standard two-sided normal-mixture construction of
[Howard et al., equation 14 and Proposition 5](https://arxiv.org/abs/1810.08240v9),
applied to these two compatible evidence channels. Its tuning parameter
rho is not a Bayesian prior on a. The resulting confidence sequence remains
valid under optional stopping and data-dependent choices of the next mode.

For K categorical outcomes, choose a uniform proposed symbol A, make the
agent component produce A, and retain Y only when Y!=A. Its accepted law
is exactly the environmental p because
P(Y=y,accept|past)=e_t(1-1/K)p_y. For fixed e, m accepted marks require
m/[e(1-1/K)] raw probes in expectation. With predictable shares, continuing
exposure supplies continuing evidence; the accepted count diverges almost
surely if the sum of conditional acceptance probabilities diverges.

The intervention has a cost. In the binary case it discards half the
environmental observations on average. A genuine source flag would retain
all of them. The filter generates a useful identifiable event; it does not
infer an unobserved source for every outcome.

## 3. How much information does the experiment supply?

Neutral feedback b=0 with known fixed e gives a binary observation of mean
ea, whose Fisher information for a is e^2/(1-e^2a^2). Accepted exclusion
marks supply e/[2(1-a^2)] per raw probe. This changes the small-e order
from e^2 to e because the intervention reduces overlap with the agent's
own outcomes. It is a difference between experiments, not a superiority
claim about a newly named estimator.

A stronger comparator uses the full likelihood of all four (A,Z) events
under a constant unknown e. Direct differentiation of probabilities
e(1+a)/4, e(1-a)/4, (2-e+ea)/4, (2-e-ea)/4 gives efficient information
for a, with e treated as a nuisance parameter,

```math
I_{\rm full}(a,e)=\frac{e}{(1-a^2)(2-e+ea^2)}.
```

The accepted-marks information is a fraction 1-e(1-a^2)/2 of this value.
At a=0.6,e=0.1 it retains 96.8%; at e=0.9 it retains 71.2%.
The full stationary likelihood is more informative. The accepted stream
additionally permits an unknown, predictably varying share without fitting
that nuisance path. These are different assumptions and tradeoffs.

For a transparent cost comparison, alpha=0.05,rho=1 gives radius at most
0.1 once V reaches 1,319. The counts below use the same boundary; probe and
flag counts are expectations for reaching that many accepted marks.

| Environmental share | Neutral known-feedback trials | Exclusion probes, expected | Observed source flag, expected |
|---:|---:|---:|---:|
| 0.5 | 5,276 | 5,276 | 2,638 |
| 0.2 | 32,975 | 13,190 | 6,595 |
| 0.1 | 131,900 | 26,380 | 13,190 |
| 0.05 | 527,600 | 52,760 | 26,380 |

These are declared information-radius costs, not measured end-to-end
algorithm speedups. Computation, feasibility and any lasting effects of
intervention must also be counted for an application.

## 4. Acting and stopping before a is resolved

Using a fine forecast b gives reference-environment quadratic-score gain
2ab-b^2 over the coarse forecast. It also costs kappa>=0 per future use.
The oracle chooses between coarse gain zero and fine gain a^2-kappa.
Given a confidence interval [l,u], a fixed fine b has worst possible regret

```math
R_f(b)=\max\{b^2-2bl+\max(\kappa,l^2),
                 b^2-2bu+\max(\kappa,u^2)\},
\qquad
R_0=\max\{0,l^2-\kappa,u^2-\kappa\}.                         \tag{24.1}
```

For l<u, minimize R_f using

```math
b_* = \mathrm{clip}_{[l,u]}
 \frac{\max(\kappa,u^2)-\max(\kappa,l^2)}{2(u-l)}.              \tag{24.2}
```

For l=u take b_*=l. Choose whichever of R_f(b_*) and R_0 is smaller.

**Proposition 24 (decision and sufficient stopping certificate).** On the
confidence event, this decision has per-use regret at most the selected R.
For H future uses under the same reference environment, pure additional
information can improve expected payoff by at most HR. A proposed query
whose cost is at least HR cannot repay its cost through those uses alone.

*Proof.* For fixed a, fine regret is b^2-2ab+max(kappa,a^2), a convex
function of a. Its maximum on the interval occurs at an endpoint. The two
endpoint quadratics intersect at (24.2); clipping to [l,u] gives their
minimax point. The coarse expression follows directly. Perfect information
cannot improve on the oracle, proving the H-use cap. QED.

The converse is not asserted: a query cheaper than HR can still be wasteful.
A small remaining uncertainty can also be enough to choose the coarse model
when max(l^2,u^2)<kappa, or to use a fine model when its gain comfortably
exceeds its cost. Neither requires learning a exactly.

### Two reproducible decision comparisons

The first experiment retains known-feedback evidence through a substantial
policy change, then seeks a tight certificate with probes. Its true a=0.6
is available only to the simulator. Fine cost is 0.04 and H=100.

| Evidence stage | Naive accumulated mean | Corrected interval | Chosen fine b | Regret bound per use |
|---|---:|---:|---:|---:|
| 5,000 observations, e=0.2,b=0.9 | 0.8292 | [0.30776,0.78424] | 0.54600 | 0.05676 |
| Another 5,000, e=0.1,b=-0.8 | 0.0828 | [0.33454,0.76466] | 0.54960 | 0.04625 |
| 15,419 accepted marks from 153,000 probes added | — | [0.56399,0.62720] | 0.59560 | 0.000999 |

The environmental parameter stayed fixed while raw observations changed
radically. The retained record (U,V) remained meaningful. At the last row,
the H-use information cap is 0.099891, below the next block's cost 0.1.
That proves a sufficient stopping decision. But the probes cost 15.3,
and acting immediately after the second row would have produced about
31.746 units of reference gain, versus 16.698 after probing costs.
The certificate-seeking policy is worse by about 15.048 units on this path.
The tighter certificate is real; it does not justify over-querying.

A second calculation repairs the query-selection question under an explicit
subjective model. Let p=(1+a)/2 have prior Beta(1,1), keep H=100 and
kappa=0.04, and charge 0.01 per raw probe with e>=0.2. Each accepted mark
then costs at most 0.1 in expectation. After n accepted marks and k positive
ones, the posterior mean of a is (2k-n)/(n+2), and the Bayes action's
expected gain is max(0,((2k-n)/(n+2))^2-kappa). The prior predictive k is
uniform on 0,...,n, so the batch's expected net benefit is exactly

```math
\frac{H}{n+1}\sum_{k=0}^{n}
 \max\left\{0,\left(\frac{2k-n}{n+2}\right)^2-\kappa\right\}
-0.1n.                                                       \tag{24.3}
```

Exact rational evaluation selects n=24, with prior expected net gain
24.93254 and expected probe cost at most 2.4. The search through n=299 is
complete: the prior perfect-information gain is H(112/375), so larger
query costs cannot be repaid. This is ordinary Bayesian value of
information applied to the declared experiment. It supports a useful action
before full parameter resolution, while making the prior assumption and
the limited one-batch comparison visible. It is not a prior-free optimum
over all adaptive query strategies.

The saved seed 20261111 happens to produce 24 positive marks in 24
acceptances, a probability 0.8^24 in the fixed a=0.6 evaluation world. Its
posterior mean 0.92308 overestimates a; the action still yields 18.95213
units after the realized 261-probe cost. That unusual path is retained,
not substituted for the exact prior-average calculation above.

## 5. Fallible mechanisms, with explicit repairs

**Known mean-error bounds.** If (23.1) has an additive conditional mean
error of at most epsilon_t, accumulate B=sum e_t epsilon_t in corrected
mode. The interval radius becomes (u_alpha(V)+B)/V. A wrong feedback
record must not be treated as exact merely because there are many samples.

**Imperfect probe control.** If the agent component disagrees with its
chosen A with probability at most epsilon, the accepted contamination
fraction is at most

```math
\xi=\frac{(1-e)\epsilon}{e/2+(1-e)\epsilon}.                  \tag{25.1}
```

A known lower e gives a uniform upper bound on xi; widening each accepted
mark's possible mean bias by 2xi restores the corresponding confidence
guarantee. Without exposure/control information, a small self-generated
error can dominate a rare environmental signal. Improving control,
auditing its error, or using a known-feedback correction are distinct
constructive responses.

**Action-dependent source choice.** If the environment's share depends on
the fresh proposed A, (23.4) need not hold. For example, a=0, exposure 3/4
when A=-1 and 1/4 when A=+1 gives accepted mean 1/2. Precommitting the
source-selection rule before the fresh action repairs the condition;
known action-dependent probabilities can instead support reweighting.

**Changing environmental targets.** Known behavior changes preserve the
record because a is unchanged. A genuine change in a needs a new segment,
a declared drift allowance, or a valid model comparison. Retaining all old
evidence as if it described the current environment is not justified by
Theorem 23. The positive target is reusable evidence with compatibility
conditions, not universal reuse.

## 6. A narrow strategic scoring repair and its scope

With known e>0 and actual chosen agent mean b, a report r can be evaluated
by

```math
S_{\rm ref}(r;Z,e,b)=2r\frac{Z-(1-e)b}{e}-r^2.                \tag{25.2}
```

Its expectation is 2ra-r^2, uniquely maximized at r=a, even if b is chosen
as a function of r. This is a direct unbiased-score correction. It cancels
the specified self-influence; it does not elicit the uncorrected actual
recurrence mean. The mechanism and exposure must be observed accurately,
and F must remain invariant to the report. A fixed number of accepted probe
marks likewise permits ordinary proper scoring for the environmental mean
when source selection obeys the probe assumptions. Query costs and any
report-dependent delays require separate incentive accounting.

This provides one concrete response to R1.9's strategic-forecast obligation.
It does not show that a population will spontaneously adopt the correction,
or that the reference environment is the right target for every agent.
Those are questions about shared aims and environmental selection for W6/W7.

## 7. Evidence and relationship to established methods

[finite_reappearance.py](../notebook/P4-R1-C001/finite_reappearance.py) and
its [output](../notebook/P4-R1-C001/finite_reappearance.json) reproduce 45
rational correction/probe identities, 48 misfire cases, 16 full-likelihood
information checks, 330 minimax decision grids, both decision calculations,
and the retained adverse comparison. The finite simulation implements this
binary controller; it does not implement the simultaneous population ODE
or a general finite-data version of Theorem 18.

- [Natarajan et al. (2013), Lemma 1](https://proceedings.neurips.cc/paper/2013/hash/3871bd64012152bfb53fdf04b401193f-Abstract.html)
  supplies unbiased correction for known class-conditional label noise.
  Equation (23.2) is that same inverse-channel idea: the equivalent flip
  rates are (1-e)(1-b)/2 and (1-e)(1+b)/2. Renaming it as value logic
  does not make it a competing new implementation.
- [Scott (2015), Proposition 1 and section 3](https://proceedings.mlr.press/v38/scott15.html)
  characterizes mixture-proportion estimation using irreducibility and
  related separation assumptions. Our probe deliberately controls a
  contaminating component and rotates an excluded event, a stronger
  experimental capability than passive samples from one fixed mixture.
  Its elementary rejection identity does not establish a new general
  decontamination theorem.
- [Boeken, Zoeter and Mooij (2025), sections 4--5 and Appendix D](https://arxiv.org/abs/2510.21335v1)
  develops proper evaluation with declared performative structure and
  corrections. Equation (25.2) is a concrete scalar reference-score
  construction in that established direction, with its own observed
  mixture-mechanism assumptions.
- Normal-mixture inference, minimax regret, and Bayesian value of
  information are standard tools. The contribution level here is their
  explicit compatible use in a judgment-and-reappearance world: how to
  obtain evidence, what to retain, when a concept is worth using, and which
  costs prevent further resolution from being worthwhile.

The strongest supported reading is therefore conditional and operational:
finite judgments can select useful structure while their own causes and
the value of further inquiry are being tracked. Extending this construction
to richer concepts, unknown control errors and evolving environments is
the next constructive problem, paired with tests identifying which changes
invalidate the retained evidence or the chosen reference target.
