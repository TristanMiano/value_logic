# R1.13 Coupled judgment from observed outcomes

**Author:** Codex (GPT-6), November 10--11, 2026. **Cycle:**
[P4-R1-C001, S6](../notebook/P4-R1-C001/record.md).
**Theses:** C1/C2, with a conditional C3 connection. **Evidence:** an
almost-sure convergence proof, finite-observation bounds and an implemented
stochastic learner, all by one model. This realizes the binary fixed-exposure
case of R1.9; it is not a realization of its full catalogue theorem.

A judge can learn a useful distinction and gain influence from the same
stream of observed outcomes, even when its forecasts help cause that stream.
In this construction the learner receives neither the environmental parameter
nor its share of observations. The familiar operations are calibration and
exponential weighting. Their coupling selects the adequate concept under
the stated conditions; weak exposure can make selection far slower than
using the fine representation from the start.

## 1. Observation contract and updates

There are two equiprobable observable symbols. Write Z_t in {-1,+1} for
the product of the current and next symbol. The coarse concept predicts
mean zero. The fine concept predicts b_t in [-1,1], and has weight w_t in
(0,1). The actual observation obeys

```math
\mathbb E[Z_t\mid\mathcal F_{t-1}]
=q_t=ea+(1-e)w_tb_t,\qquad 0<e\le1,\quad -1\le a\le1.       \tag{28.1}
```

The environmental mean a and share e are fixed but unknown to the learner.
The formula can be implemented as the binary Markov mixture in R1.9; it
does not require independent contexts. The filtration contains the past,
and b_t,w_t are chosen before Z_t is observed.

Let eta>0. Choose deterministic steps gamma_t>0 satisfying

```math
\eta\gamma_t\le1,\qquad
\sum_t\gamma_t=\infty,\qquad\sum_t\gamma_t^2<\infty.
```

Write L_t=log(w_t/(1-w_t)). After observing Z_t, update

```math
b_{t+1}=b_t+\eta\gamma_t(Z_t-b_t),\qquad
L_{t+1}=L_t+\gamma_t(2b_tZ_t-b_t^2).                         \tag{28.2}
```

The second increment is the fine forecast's realized quadratic-score
advantage over the coarse forecast. It uses the forecast made **before**
the observation. The observation then trains the next forecast; it does not
retroactively improve the score. Calibration receives effort independently
of the model's current weight. Each step has constant arithmetic and memory
cost in this two-concept model.

## 2. Grounding without an expected-score oracle

**Theorem 28 (observed coupled recovery).** For any b_0 in [-1,1] and
0<w_0<1, the updates satisfy:

- If a!=0, then almost surely w_t->1 and b_t,q_t->a.
- If a=0, then almost surely b_t,q_t->0 and w_t converges to a value strictly
  between zero and one. Equivalent concepts may coexist.

*Proof.* The forecast update is a convex combination, so b stays in [-1,1].
Expanding its square gives the exact pathwise identity, with t=0,...,N-1,

```math
L_N=L_0+\sum_{t<N}\gamma_tb_t^2
 +\frac{b_N^2-b_0^2}{\eta}
 -\eta\sum_{t<N}\gamma_t^2(Z_t-b_t)^2.                        \tag{28.3}
```

The last sum converges because its summands are bounded by 4 eta gamma_t^2.
In particular, L_N is bounded below uniformly on every path: early mistakes
cannot send an initially present fine model to negative infinite log odds.

Put d_t=1-(1-e)w_t in [e,1], xi_t=Z_t-q_t, and G_N=sum_{t<N}gamma_t.
The martingale sum sum gamma_t xi_t converges almost surely by bounded
increments and square-summable steps. If sum gamma_t b_t^2 were finite,
weighted Cauchy--Schwarz would give

```math
\frac{\left|\sum_{t<N}\gamma_td_tb_t\right|}{G_N}
\le\sqrt{\frac{\sum_{t<N}\gamma_tb_t^2}{G_N}}\longrightarrow0.
```

Telescoping the forecast update and dividing by eta G_N would then give
0=ea. For a!=0 this is impossible. Thus the energy term in (28.3)
diverges, L_N->infinity, and w_N->1.

To finish, let x_t=b_t-a and r_t=-(1-e)(1-w_t)b_t->0. Then
x_{t+1}=(1-eta e gamma_t)x_t+eta gamma_t r_t+eta gamma_t xi_t.
Let M_t=eta sum_{s<t}gamma_s xi_s, with almost-sure limit M_infinity.
The corrected error y_t=x_t+M_infinity-M_t satisfies

```math
y_{t+1}=(1-\eta e\gamma_t)y_t
 +\eta\gamma_t\,[r_t+e(M_\infty-M_t)].
```

The forcing tends to zero, the averaging coefficients are nonnegative, and
their accumulated gain is infinite. The initial-state coefficient tends
to zero, while the weighted forcing tends to zero, proving b_t->a.

For a=0, conditional squared-error drift is at most
-2 eta e gamma_t b_t^2+4 eta^2 gamma_t^2. Adding the remaining deterministic
tail 4 eta^2 sum_{s>=t}gamma_s^2 to b_t^2 gives a nonnegative
supermartingale. It converges, and the summed drift gives
sum gamma_t b_t^2<infinity almost surely. Since sum gamma_t is infinite,
the limit of b_t^2 is zero. Equation (28.3) now gives a finite limiting
L, hence a strictly interior limiting weight. QED.

The positive result is about the specified updating rule. Proper scoring
does not by itself incentivize a strategic agent to follow calibration
when it can manipulate future observations. Nor does coexistence at a=0
select the shortest vocabulary: that needs an explicit complexity cost or
a separate merge operation.

## 3. An explicit finite-observation guarantee

The same identity supplies a conservative rate, rather than relying only
on asymptotic consistency. Let H>=sum gamma_t^2 be known and fix alpha>0.
Define

```math
C_\alpha=\frac2\eta+\sqrt{2H\log(2/\alpha)},\qquad
B(G)=L_0-\frac{b_0^2}{\eta}-4\eta H
       +\frac{(e|a|G-C_\alpha)_+^2}{G},\quad G>0.             \tag{28.4}
```

**Corollary 28A (selection and forecast bounds).** With probability at
least 1-alpha, simultaneously for every N>=1,

```math
L_N\ge B(G_N),\qquad w_N\ge\frac{1}{1+\exp[-B(G_N)]}.        \tag{28.5}
```

For preselected K<N, set delta_K=1/(1+exp(B(G_K))),
Delta G=sum_{K<=t<N}gamma_t, and gamma_max=max_{K<=t<N}gamma_t.
For any beta>0, with probability at least 1-alpha-beta,

```math
|b_N-a|\le
2\exp(-\eta e\Delta G)
+\frac{1-e}{e}\delta_K
+\sqrt{\frac{2\eta\gamma_{\max}}e\log(2/\beta)}.              \tag{28.6}
```

Intersect this bound with the trivial upper bound two when it is vacuous.
The model parameters in the guarantee need not be known to execute the
learner. They are required to turn it into a prospective numerical budget.

*Proof.* A two-sided exponential-martingale bound gives, uniformly in N,
|sum_{t<N}gamma_t xi_t|<=sqrt(2H log(2/alpha)) on the first event.
Telescoping the b update and using |b_N-b_0|<=2 gives

```math
e|a|G_N\le C_\alpha+
          \sqrt{G_N\sum_{t<N}\gamma_tb_t^2}.
```

Insert its energy lower bound in (28.3) to obtain (28.5).
B(G) is nondecreasing: the positive-part term is zero before
G=C_alpha/(e|a|), and thereafter has nonnegative derivative. Thus
1-w_t<=delta_K for all t>=K on that event.

Expand the error recursion over [K,N). The initial coefficient is at most
exp(-eta e Delta G); the residual coarse-influence term is at most
(1-e)delta_K/e. The noise coefficients are deterministic,
eta gamma_s times the subsequent product of (1-eta e gamma_t).
Their sum is at most 1/e, and each is at most eta gamma_max, so their
squared sum is at most eta gamma_max/e. The bounded martingale inequality
gives the last term with failure probability beta. A union bound proves
(28.6). QED.

For gamma_t=(t+25)^(-0.6), eta=1, b_0=-0.5, w_0=0.01 and a=0.6,
[stochastic_bounds.py](../notebook/P4-R1-C001/stochastic_bounds.py) uses
integral bounds on the step sums. Its
[output](../notebook/P4-R1-C001/stochastic_bounds.json) gives sufficient
budgets for weight at least 0.99 from the midpoint onward and final
forecast error at most 0.1, with joint probability at least 0.95:

| Environmental share | Conservative sufficient observations |
|---:|---:|
| 0.5 | 509,644 |
| 0.2 | 17,977,084 |
| 0.05 | 17,320,022,212 |

These are sufficient bounds, not necessary sample counts or executed
experiments. Their looseness and strong exposure dependence are explicit
limitations of this proof and this slow step schedule.

## 4. Implemented comparison

[stochastic_judgment.py](../notebook/P4-R1-C001/stochastic_judgment.py)
separates the simulator from a learner whose update accepts only Z and the
step. It runs twelve independent paths for each of five parameter settings,
one million observations each. An ordinary single fine predictor uses the
same calibration rule and starts with full influence. Each method therefore
receives the same number of observations from its own induced process;
common random numbers couple the comparisons. This is an informative
alternative, not an identical information stream.

The [output](../notebook/P4-R1-C001/stochastic_judgment.json) retains all
checkpoints and individual final values. At one million observations:

| Environment a, share e | Mean fine weight | Coupled learner's fine-forecast MSE | Single fine predictor's MSE |
|---|---:|---:|---:|
| 0.6, 0.2 | approximately 1 | 0.00019211 | 0.00019211 |
| 0.6, 0.5 | approximately 1 | 0.00009791 | 0.00009791 |
| 0.6, 0.05 | 0.005113 | 0.32410844 | 0.00198564 |
| -0.6, 0.2 | approximately 1 | 0.00048419 | 0.00048419 |
| 0, 0.2 | 0.003191 | 0.00012524 | 0.00059064 |

MSE is the average over twelve realized paths, not an exact population risk.
The positive cases start with the wrong forecast sign. The negative-a case
starts positive. The fine weight starts at 0.01 throughout. The exact
pathwise identity's largest numerical residual is below 3e-11.

The weak-exposure case preserves an important adverse result: asymptotic
selection is far too slow at this horizon. At e=0.2 and 100,000 observations,
the mean fine weight was only 0.13053 and its MSE 0.21531, compared with
0.00202 for the single fine predictor. Once the coupled system gives all
influence to the fine model, its update becomes the same as the comparator;
under the common random numbers their late numerical paths coincide. That
explains the ties without turning them into an independent performance gain.

## 5. A tested intervention can select a useful concept earlier

The slow weak-exposure run suggests a constructive change in the experiment.
Suppose the controller can carry out the exact exclusion probes of R1.11:
it randomly proposes a sign, its own component reproduces that sign, and the
source share is chosen before the proposal. Accepted marks estimate the
environmental a even when that share is unknown. This is additional control
authority; it was not available to the passive learner in (28.2).

**Corollary 28B (certified adoption and subsequent grounding).** Fix a fine
concept cost kappa in [0,1), and use R1.11's confidence sequence I=[l,u]
with failure probability alpha. While probing, choose the first applicable
decision:

- Adopt the fine concept when dist(0,I)^2>kappa, initialized with
  b*=proj_I(0), the point of I closest to zero.
- Choose the coarse concept when max(l^2,u^2)<kappa.
- Otherwise continue the stated experiment, or retain an unresolved decision
  if the authorized query budget ends.

On the simultaneous confidence event, fine adoption has strictly positive
reference-environment score gain 2ab*-(b*)^2-kappa over coarse. Freezing that
forecast preserves this guarantee while a stays fixed. A coarse decision is
oracle-optimal among the two concept classes at this cost. Assume that on
any path of indefinite probing its cumulative exposure diverges. If
a^2!=kappa, the decision occurs in finite time almost surely.

After fine adoption, an alternative is to give that concept full influence
and continue calibration with deterministic steps gamma_t<=1,
sum gamma_t=infinity and sum gamma_t^2<infinity. If subsequent predictable
environmental shares have a positive lower bound, then b_t and the actual
conditional mean converge almost surely to a. This convergence statement
does not turn every intermediate calibrated forecast into a certified one.

*Proof.* When I is positive, a>=l=b*>0, hence
2ab*-(b*)^2>=l^2>kappa. The negative case is symmetric. If the whole
interval has squared magnitude below kappa, even the best fine forecast
has lower net value than coarse. Infinite cumulative probe exposure produces
infinitely many accepted marks; their mean converges to a and the confidence
radius tends to zero. Strict separation from the decision boundary then
forces a finite decision, whether or not an earlier confidence failure
occurred. Correctness of that decision has the stated confidence guarantee.

For calibration after adoption, let x_t=b_t-a. Under full influence,
the conditional drift of x_t^2 is at most
-2e_min gamma_t x_t^2+4gamma_t^2. The nonnegative supermartingale obtained
by adding the remaining 4 sum gamma_t^2 tail converges, and its drift gives
sum gamma_t x_t^2<infinity. Thus x_t^2 tends to zero, and so does the
actual-mean error. The argument applies conditionally after the random
adoption time, with the step schedule restarted there. QED.

This is a mathematical composition of R1.11's experiment and the single-fine
case of stochastic calibration, with an explicit selection step. The
companion [probe_adoption.py](../notebook/P4-R1-C001/probe_adoption.py)
implements that composition, including cases
where the coarse concept is worth keeping. It does not implement an
evolutionary incentive to perform the experiment. Probe feasibility, changes
caused by forced actions, query fees and foregone deployment utility must be
priced in an application; trial counts alone do not establish a net gain.

Its [saved output](../notebook/P4-R1-C001/probe_adoption.json) uses twelve
paths per setting, 100,000 raw observations per method and path, kappa=0.04
and 95% confidence per path. The methods induce different streams, coupled
by common random numbers. At a=0.6,e=0.05 all twelve paths adopt fine,
with median decision trial 3,499 (range 288--7,379). Final forecast MSE is
0.008891, versus 0.323874 for passive coupled selection and 0.008680 for
always using the fine predictor. The intervention repairs the selection
delay; it does not outperform the already adequate fine comparator here.
At a=0,e=0.05 every path selects coarse, with median decision trial 16,422.

At a=0.1,e=0.05, ten paths certify coarse and two remain unresolved at the
budget. At the exact boundary a=0.2, all twelve exhaust 100,000 probes
without a strict decision; coarse already has oracle value there. This is
a material cost failure of certificate-only querying. R1.11 Proposition 24
provides a sufficient information-cost cap, and its Bayesian calculation
shows a positive query-selection route under a prior. Neither turns this
unpriced experiment into an economically optimal controller. Coverage in
the table is per path, not a simultaneous 95% claim across all 72 paths.

An ordinary experiment-design and confidence-bound controller implementing
these steps is the same method. Its value here is the mechanism: a judgment
can earn influence by predicting what survives a controlled check against
its own causal effect, and can then become calibrated to that grounded
recurrence. It also supports an adequate coarse judgment when the remaining
distinction is too small to repay its declared use cost.

## 6. Established machinery and the remaining contribution

[Mendler-Dunner et al. (2020), Theorem 3.2](https://proceedings.neurips.cc/paper_files/paper/2020/file/33e75ff09dd601bbe69f351039152189-Paper.pdf)
already prove stochastic performative retraining rates under strong convexity,
smoothness and sufficiently weak distribution sensitivity. A single fine
predictor here is an elementary example of that contraction. Their general
rate result is stronger than the single-model consistency part of this note.
The additional object here is the competing coarse/fine influence, with an
exact identity that prevents loss of the adequate representation and links
its selection to environmental recovery.

Stochastic approximation and its relationship to ODEs are classical; see
[Benaim (1999), sections 4.1--4.2](https://numdam.org/item/SPS_1999__33__1_0/).
The proof above supplies the specific boundary-selection argument directly.
Calling the implementation exponential weighting plus online calibration
describes the same algorithm. The scientific content is the specified
grounding guarantee and its integration with concept selection, not a claim
that conventional learning cannot express it.

The next extensions are multi-concept finite-data recovery, endogenous
creation of missing distinctions, and strategic adoption of the calibration
or intervention rule. Corollary 28B supplies a bounded faster-selection route
and a coarse-adequacy decision; a useful application still needs its full
intervention economics.
The decreasing-exposure theorem in R1.12 is a separate population result;
its thresholds have not been transferred to this stochastic step schedule.
