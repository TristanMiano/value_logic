# R1.12 Grounded judgments under weakening environmental influence

**Author:** Codex (GPT-6), November 10, 2026. **Cycle:**
[P4-R1-C001, S6](../notebook/P4-R1-C001/record.md).
**Theses:** C1/C2 through selection of the fine conceptual distinction;
a conditional C3 bridge through continuing environmental evidence.
**Evidence:** proofs for the stated binary dynamics and observation model,
exact moment checks and numerical illustrations by one model. No independent
confirmation or completed novelty assessment is claimed.

Judgment can remain grounded even as agents increasingly cause what they
observe. The conditions depend on how environmental evidence reaches them.
This construction distinguishes passive scoring from deliberate experiments:
the latter can preserve factual learning in a regime where the former loses
the environmental distinction. It also identifies the price of that repair:
precise intervention, a fixed reference environment, and potentially very
large observation costs.

This extends W1's coupled judgment model; it does not discharge the broader
questions about evolution, instrumental convergence or classical logical
truth in W7, W6 or W2. The environment is specified here, rather than derived
from a meta-value or evolutionary account.

## 1. Simultaneous learning with decreasing external influence

Use the binary recurrence world of [R1.11](R1_finite_reappearance.md).
The environmental correlation a is nonzero and lies in [-1,1]. One coarse
concept forecasts correlation zero. One fine concept forecasts b(t), starts
at b(0)=0, and has influence w(0)=w_0 in (0,1). With calibration rate
eta>0 and environmental share e(t), actual recurrence has correlation

```math
q(t)=e(t)a+(1-e(t))w(t)b(t).
```

The population learning and proper-score selection equations are

```math
\dot b=\eta(q-b),\qquad
\dot w=w(1-w)(2bq-b^2).                                      \tag{25.1}
```

Thus the fine concept learns while it competes; calibration is not assumed
instantaneous. The environment's correlation remains fixed, while its share
of observations is

```math
e(t)=e_0(1+t)^{-p},\qquad 0<e_0\le1,\quad p\ge0.             \tag{25.2}
```

These are exact population signals, not a stochastic algorithm supplied with
hidden environmental labels. The finite experimental statements below have
their own observation contract.

**Theorem 25 (passive recovery and an exposure-energy boundary).**

1. If 0<=p<=1/2, then w(t)->1 and b(t),q(t)->a. The concept that represents
   the environmental distinction eventually wins and learns its value.
2. If p>1/2 and some c in (w_0,1) satisfies

```math
\frac{a^2 e_0^2}{(1-c)^2(2p-1)}
<\log\frac{c}{1-c}-\log\frac{w_0}{1-w_0},                    \tag{25.3}
```

   then w(t)<c at every time, w has a limit below c, and b(t),q(t)->0.
   The fine distinction remains suppressed. This is a sufficient failure
   region, not a claim that every initialization fails when p>1/2.

*Proof.* Reversing signs reduces the argument to a>0; the interval 0<=b<=a
is invariant. Substituting q=b+dot b/eta into the weight equation gives the
exact identity

```math
\log\frac{w(t)}{1-w(t)}
=\log\frac{w_0}{1-w_0}+\int_0^t b(s)^2\,ds+\frac{b(t)^2}{\eta}.
                                                               \tag{25.4}
```

Put d(t)=1-w(t)+e(t)w(t), so dot b=eta(ea-db) and 0<d<=1.
Variation of constants over [t-1,t] gives, for t>=1,
b(t)>=a e(t)(1-exp(-eta)). If p<=1/2, the integral of b squared diverges,
so (25.4) makes w tend to one.

For p<1/2, the same lower bound makes 1-w decrease at least as
exp(-C t^(1-2p)) for a positive C, and hence (1-w)/e->0.
At p=1/2, both 1-w and e tend to zero, so d tends to zero. Given any K>0,
choose epsilon small enough that a/(2 epsilon)>=K and then a fixed window
T with 1-exp(-eta epsilon T)>=1/2. Eventually d<=epsilon throughout that
window, and variation of constants gives b(t)>=K e(t). Equation (25.4)
therefore makes 1-w decrease faster than any specified inverse polynomial.
Again (1-w)/e->0. In the time variable tau=integral eta e(t) dt, which
diverges, the fine update is

```math
\frac{db}{d\tau}=a-\left(w+\frac{1-w}{e}\right)b.
```

Its coefficient tends to one. The stable scalar linear equation gives
b->a, and the expression for q gives q->a.

For the second part, consider the interval before any first crossing of c.
There d>=d_0:=1-c. Young's inequality yields

```math
\frac{d}{dt}b^2\le\frac{\eta a^2e^2}{d_0}-\eta d_0b^2,
\qquad
\int_0^t b^2+\frac{b(t)^2}{\eta d_0}
\le\frac{a^2}{d_0^2}\int_0^t e^2.
```

Since d_0<=1, (25.4) and the finite exposure integral bound the increase
in log odds by a^2 e_0^2/[(1-c)^2(2p-1)]. Condition (25.3) rules out
that first crossing. Stable damping d>=d_0 with forcing e(t)a->0 gives
b->0. The integral bound and (25.4) give a limiting weight strictly below
c. Then q->0. QED.

In the failing case the limiting coarse forecast is correct about the
agent-dominated observations that actually occur. Its failure is to retain
the environmental distinction a. Those are two different targets, not a
contradiction in predictive accuracy. A “truth from successful use” reading
must specify which continuing contact makes successful use informative
about the reference world.

## 2. A constructive experiment extends the grounding region

Now use discrete observations with e_t=e_0(1+t)^(-p). Choose an independent
fair sign A_t before each observation; the agent component causes Z_t=A_t,
while the environmental component has mean a independently of A_t. The
environmental share is chosen before A_t and may be unknown. Retain only
Z_t!=A_t, as in R1.11, Theorem 23.

**Proposition 26 (grounding by exclusion probes).** If p<=1, the retained
count diverges almost surely, and the retained average converges to a.
The confidence sequence in R1.11 shrinks to zero. In particular, for
1/2<p<=1 this experiment recovers a in cases satisfying (25.3).

*Proof.* At each time, acceptance has conditional probability e_t/2 and
the accepted mark has conditional mean a and the same binary law. The
sum of acceptance probabilities diverges exactly when p<=1. Conditional
Borel--Cantelli gives infinitely many acceptances; the bounded martingale
law of large numbers, or the accepted i.i.d. mark law in this deterministic
schedule, gives consistency. The confidence radius is of order
sqrt(log V/V), where V is the accepted count. QED.

The comparison is between information mechanisms. Continuous population
selection time is not a measured cost-equivalent alternative to discrete
probing. Nor does almost-sure recovery promise an economical experiment.
If the agent can choose a larger environmental share, reserving that exposure
is another constructive way to preserve grounding.

## 3. Why precise intervention changes the information budget

The benefit of exclusion is more than a different estimator. Suppose instead
that every own-component mean b_t lies in [-beta,beta], beta<1, and the
learner observes only its actions and Z_t. It may choose b_t adaptively and
know every e_t. Source flags are unavailable. Compare fixed environmental
parameters +a_0 and -a_0, with 0<a_0<1, under the same learning policy.

**Proposition 27 (finite evidence under interior feedback, and its repair).**
Let r=max(beta,a_0). For every horizon T, the two record laws satisfy

```math
\mathrm{KL}(P_+^{(T)}\|P_-^{(T)})
\le B_T:=\frac{4a_0^2}{1-r^2}\sum_{t\le T}e_t^2.             \tag{27.1}
```

Every test distinguishing the signs under equal prior probabilities has
error at least exp(-B_T)/4. Thus, if the squared exposures are summable,
no estimator in this observation model can consistently recover both signs.
The exclusion experiment of Proposition 26 removes the interior-feedback
restriction and restores consistency when the unsquared exposures diverge.

*Proof.* Conditional on the same observed past, the two binary means are
(1-e_t)b_t +/- e_t a_0 and have magnitude at most r. Their Bernoulli
success probabilities differ by e_t a_0. The inequality KL<=chi-squared
gives one-step KL at most 4e_t^2 a_0^2/(1-r^2). Internal randomization has
the same conditional law under either parameter. The KL chain rule gives
(27.1), including adaptive policies. The Bretagnolle--Huber testing bound
gives the error statement; see [Canonne, Lemma 3 and Corollary 4](https://arxiv.org/html/2202.07198v2#S2).
Proposition 26 supplies the stated constructive counterpart. QED.

With fixed beta<1 and p>1/2, even unlimited computation cannot extract
unbounded sign information from this record. Increasing precision toward
exclusion, preserving enough environmental exposure, or observing a source
flag changes the available evidence and can repair the limitation. Merely
renaming or recursively reweighting the same finite-information record
cannot do so.

### Known imperfect control still permits useful identification

Perfect control is not necessary when exposure remains sufficient. Suppose
the own component has known mean beta A, with 0<beta<=1 and fresh fair A.
The share e may be unknown and predictable before A. Define

```math
X=Z-\beta A,\qquad D=1-\frac{AZ}{\beta}.
```

Then E[X|past]=ea and E[D|past]=e, so X-aD is a bounded martingale
difference. If the time-average share has a positive lower limit, the ratio
sum X/sum D consistently estimates a. This also handles predictable
variation of the unknown share. The proof is the bounded martingale strong
law and a denominator growing linearly. At beta=1, these moments reduce to
2Z and 2 on accepted observations and zero otherwise, recovering the
exclusion estimator. At beta<1, raw accepted-only filtering would generally
be biased; the corrected moments use both outcomes.

For constant e, direct calculation gives

```math
\mathbb E[(X-aD)^2]
=(1-\beta^2)\left(1+\frac{a^2}{\beta^2}\right)
 +2e(\beta^2-a^2).                                          \tag{27.2}
```

The full four-outcome likelihood is again a stronger statistical comparator.
Treating unknown constant e as nuisance, its efficient Fisher information is

```math
I_{\rm full}(a,e,\beta)=
\frac{e^2\beta^2}{
 (a^2+\beta^2)[1-e^2a^2-(1-e)^2\beta^2]
 -4e(1-e)a^2\beta^2}.                                      \tag{27.3}
```

For fixed beta<1 this is of order e squared as e->0. At beta=1 it is of
order e, recovering R1.11's formula. Thus very accurate but imperfect
control need not preserve exclusion's asymptotic advantage as environmental
influence vanishes. The moment correction is a positive repair at adequate
exposure; it does not silently evade Proposition 27.

## 4. Checks, slow transients and scientific scope

[weak_exposure.py](../notebook/P4-R1-C001/weak_exposure.py) integrates the
simultaneous equations and an independent accumulator for (25.4), checks
135 conditional KL inequalities, and verifies 27 imperfect-control moment
and Fisher-information identities in rational arithmetic. The largest
log-odds identity residual in its [output](../notebook/P4-R1-C001/weak_exposure.json)
is below 7e-10. Illustrative population trajectories at t=1,000,000 are:

| a | e_0 | p | Initial fine weight | Fine weight | Fine forecast b |
|---:|---:|---:|---:|---:|---:|
| 0.6 | 0.2 | 0.25 | 0.01 | approximately 1 | 0.600000 |
| 0.8 | 0.8 | 0.50 | 0.20 | approximately 1 | 0.800000 |
| 0.6 | 0.2 | 0.50 | 0.01 | 0.012168 | 0.00012148 |
| 0.6 | 0.2 | 0.75 | 0.01 | 0.010251 | 0.00000383 |
| 0.6 | 0.2 | 0.75 | 0.99 | approximately 1 | 0.600000 |

The slow p=1/2 row is retained: the theorem's eventual recovery can be
practically inaccessible. In the p=3/4 low-weight row, condition (25.3)
with c=1/2 gives a uniform weight bound 0.0112073; this is a proved failure,
not merely a short simulation. The high-weight row shows why that condition
must not be reported as a universal p>1/2 failure. A negative-a run with
tenfold slower calibration also recovers in the p=1/4 case.

At e_0=0.2,p=3/4, even the successful probe experiment is slow. An exact
event-driven simulation of its accepted stream has 10, 76 and 419 accepted
marks at hypothetical raw horizons 10^6, 10^9 and 10^12. At the last horizon
the estimate is 0.57995, with the 95% anytime radius 0.16966. The expected
accepted count is between 399.5243 and 399.5838. The implementation simulates
438 thinning proposals, **not a trillion executed trials**. These numbers
expose the observation burden instead of presenting consistency as a
practical speed gain.

The conceptual mechanism is established territory: experimental choices
change what can be learned from feedback. [Fudenberg and Levine (1993),
section 1](https://economics.mit.edu/sites/default/files/inline-files/sce.pdf)
distinguish correctness along the realized play path from correctness about
unobserved contingencies. [Zacekova, Privara and Pcolka (2013), introduction](https://doi.org/10.1016/j.jprocont.2013.08.004)
discuss preserving informative excitation while controlling a system.
These are relevant alternatives and enabling perspectives, not findings
overturned by the present example.

The candidate contribution here is a precise characterization within the
coupled judgment model: the finite-calibration identity, the power-law
grounding theorem, and the comparison with a support-changing experiment.
The statistical lower-bound machinery and moment estimation are standard.
A closer search for an existing version of the dynamic result remains due.
Multiple changing concepts, strategic selection of reports, endogenous
environmental laws and the incentives to buy experiments remain open. The
surviving positive reading is that evaluating judgments can recover factual
distinctions when use preserves sufficient identifiable contact with the
world—and deliberate experimentation can enlarge that region.
