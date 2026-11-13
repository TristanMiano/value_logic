# R6.5 Judging forecasts by their uses can recover common facts

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** a composition of established online learning with R6.1's
decision geometry; a separate, implemented learner using outcomes revealed
only by purchased trades. These are finite, explicitly typed mechanisms.

Different final goals can teach agents to rely on the same factual judgment.
The mechanism has two parts: the goals make a factual error costly, and the
agent uses actual consequences to revise its trust in the judge that made
the error. Sufficient overlap makes a shared component converge; it does not
make the agents' remaining purposes identical.

## 1. From successful subgoals to time-average adoption

Consider a finite bank of K judging or control procedures. Each produces an
action for the current task. The outer learner chooses which procedure to
use, observes its achieved payoff, and updates its weights. A different
procedure's payoff is not revealed. Payoffs include whatever action costs
the model prices, and lie in a known interval of width W.

Current payoff vectors must be chosen independently of the learner's current
random choice, conditional on the past. For a causal comparison between
whole policies, use repeated reset tasks or exogenous opportunities: the
external-regret comparison below does not reconstruct the different future
world that a different past action might have caused.

**Lemma 1 (shared-subgoal adoption).** Suppose a procedure c has conditional
expected payoff at least delta>0 above every alternative on every round,
and the learner has expected regret at most B_T to always choosing c. Then

```math
\mathbb E\sum_{t\le T}\mathbf 1\{I_t\ne c\}
\le \frac{B_T}{\delta}.                                  \tag{J.1}
```

*Proof.* Conditional on the past and the chosen alternative, the expected
payoff difference is at least delta whenever I_t differs from c. Sum and
use the regret bound. QED.

Sublinear regret therefore gives time-average adoption. This can hold for
agents with different clamped final goals, each evaluating its procedures
by its own goal, or through changes of goal that preserve the net advantage.
Different initial positive weights affect the learning transient. The lemma
does not require identical initial subgoals or identical final utilities.

If two procedures tie, this argument gives no pressure to choose the same
one; both can remain useful. If a private alternative is better for one
agent, that agent has reason to retain it. A common capability can also be
valuable without being the best use of a scarce resource. The constructive
condition is a positive margin against the *available alternatives*, with
costs included, rather than the name of a supposedly universal subgoal.

## 2. A concrete bounded evaluator

For normalized rewards G in [0,1], ordinary Exp3 uses weights w_j initially
proportional to positive priors pi_j, mixes their normalized distribution with
uniform exploration of mass gamma, and updates only the chosen weight:

```math
P_t(j)=(1-\gamma)\frac{w_{j,t}}{\sum_k w_{k,t}}+rac\gamma K,
\quad
\widehat G_{j,t}=\frac{G_{j,t}\mathbf 1\{I_t=j\}}{P_t(j)},
\quad
w_{j,t+1}=w_{j,t}\exp\left(\frac\gamma K\widehat G_{j,t}\right).
                                                               \tag{J.2}
```

For a fixed comparator j and 0<gamma<1, the standard potential argument gives

```math
B_T\le W\left[\frac{K\log(1/\pi_j)}\gamma
                    +(e-1)\gamma T\right].                    \tag{J.3}
```

The algorithm and bound are established work, not a new Value Logic learner.
See [Auer et al. (2002), section 3](https://homepages.math.uic.edu/~lreyzin/papers/auer02.pdf).
For completeness, the proof's operative steps are these. With eta=gamma/K,
eta*Ghat<=1, so exp(x)<=1+x+(e-2)x^2 bounds each weight increment. Upper-bound
the log total weight by the resulting first and second moments; lower-bound
it by the comparator's log weight. Conditional importance weighting gives
E Ghat_j=E G_j and E sum_j P_j*Ghat_j^2<=K. Combining the bounds and the
exploration term proves (J.3). Uniform priors and a horizon-tuned gamma give
order sqrt(T*K*log K) regret. This proof compares a fixed procedure under
nonanticipating feedback; it is not a guarantee of optimal strategic interaction.

## 3. When better practical judgment implies a more accurate fact

Use the finite outcome and context model from [R6.1](R6_goal_judgment.md).
The conditional law p(X) is fixed. Each candidate judge supplies a forecast
r_j(X); it is selected before the current goal is revealed. Current contexts
and outcomes are fresh draws, and the goal family is independent of them
conditional on past information. The family may change with time.

Assume the current goal contracts satisfy R6.1's curvature bound with matrix
A_t, and that d^T A_t d>=lambda*||d||_2^2 for every zero-sum contrast d,
with a common lambda>0. Payoffs have width W. Suppose the candidate bank
contains p itself, although the learner does not know which candidate it is.

**Theorem 2 (goal-mediated factual recovery).** If the normalized-payoff
learner has expected regret R_T against that candidate, then

```math
\frac1T\sum_{t\le T}\mathbb E\|r_{I_t}(X_t)-p(X_t)\|_2^2
\le\frac{2W R_T}{\lambda T}.                              \tag{J.4}
```

*Proof.* Conditional on the past and chosen judge, R6.1 lower-bounds the
expected actual payoff loss by lambda/2 times forecast squared error.
Sum these inequalities and use actual-payoff regret W*R_T. QED.

If a fixed candidate has total actual-payoff approximation loss A_T relative
to p, replace the numerator by 2*(W*R_T+A_T). The vocabulary assumption is
therefore visible as a model-approximation obligation. Costly representation
or computation can make a coarse judge optimal; the zero-error conclusion
requires that the comparator and the payoff comparison satisfy the stated
cost contract. [R6.2](R6_observed_shared.md) characterizes one such cost boundary.

For two agents whose goals both cover a feature v, full-law separation is
unnecessary. Suppose each agent's regret bounds its squared error in v's
conditional expectation. The inequality

```math
\bigl[\langle v,r_i-r_j\rangle\bigr]^2
\le2\bigl[\langle v,r_i-p\rangle\bigr]^2
  +2\bigl[\langle v,r_j-p\rangle\bigr]^2                  \tag{J.5}
```

then forces time-average agreement on that feature when both errors vanish.
The forecasts are evaluated on the same fresh context distribution. Their
private, uncovered features may remain different. Agreement is warranted
here because both are disciplined by the same world law through separating
uses, rather than because agreement defines the law.

This gives a positive answer for clamped final goals with plastic subgoals:
their shared need for an accurate capability can drive convergence even
while the final goals remain fixed and different. Coverage can also survive
goal drift. If it becomes too weak, the quantitative bound weakens with it;
restoring informative opportunities or using a more targeted learner is a
specific repair.

## 4. A learner that extracts facts from actual payoff

For a binary outcome with a uniform price t, a purchased trade pays Y-t.
Its realized payoff reveals Y as payoff+t. A declined trade pays zero and
reveals no Y. This observation model supports a much more efficient learner
than treating each forecast as an unrelated arm.

There are finitely many raw contexts x, each recurring with positive
probability, and a fixed unknown p_x=P(Y=1|x). Maintain outcome counts only
for purchased trades in that context. Start with pseudocount strength two,
and clip the estimated forecast to [eta,1-eta], where the true probabilities
lie in that interval. The estimate determines the next trade decision.

**Proposition 3 (observed-payoff calibration).** Suppose prices and outcomes
are conditionally independent given the current context, and informative
goal opportunities occur with deterministic probabilities alpha_t satisfying
sum_t alpha_t=infinity. Then this learner's forecasts converge to p_x almost
surely for every context.

*Proof.* Each round has conditional probability at least
alpha_t*P(X=x)*eta of revealing an outcome in context x. The probability of
no further such observations after any fixed time is bounded by a product
of one minus these lower bounds, which is zero. Thus every context supplies
infinitely many observations. Inclusion is decided by the price, context and
past before the fresh outcome is revealed. The retained outcomes in that
context therefore form an iid Bernoulli(p_x) sequence. The strong law,
vanishing pseudocount weight and clipping to an interval containing p_x give
the conclusion. QED.

A finite confidence statement does not need to condition on a fixed sample
count. For m context/learner streams and their first n>=1 observed outcomes,
a union bound over all streams and all n gives simultaneous sample-mean error
at most

```math
\sqrt{\frac{\log(\pi^2mn^2/(3\delta))}{2n}}.             \tag{J.6}
```

The pseudocount estimate adds at most 2/(n+2). This remains valid at the
adaptively reached counts. Clipping cannot increase error when p_x lies in
the clipping interval. It is a bound on a declared fixed world, not on
outcomes the agent can manipulate to vindicate its forecast.

The known interior range can be relaxed by decreasing eta_t to zero while
keeping sum_t alpha_t*eta_t infinite. The same observation argument then
recovers boundary probabilities too, while clipping bias vanishes. Such a
schedule explicitly pays for continued exploration; its finite cost and rate
must be assessed rather than assumed free. If total opportunity exposure is
finite, recovery from arbitrary initial guesses need not occur. Recurring
informative uses supply the constructive condition.

## 5. Payoff-only experiment and the stronger comparison

The [pre-execution contract](../notebook/P4-R6-C001/explore.md#c2-practical-feedback-clamped-goals-and-j-squared)
fixed 16 repetitions and four initial judge priors. In half the repetitions
the two equally likely contexts have true probabilities (0.2,0.8); in the
other half they have (0.8,0.2). Neither learner receives the true sign. The
three candidate judges predict the positive relation, 0.5 everywhere, or the
negative relation. Exp3's gamma is tuned once to the final horizon. The
structured learner starts with the mean forecast implied by the same prior.

Both receive the same potential contexts, prices and outcomes, but each
observes an outcome only when its own action purchases the trade. The
structured update decodes that outcome from the payoff; Exp3 uses only its
selected judge's scalar return. These are genuinely different uses of the
same access, both established methods.

| Hazard opportunities | Learner | Mean cumulative population decision regret | Mean final forecast squared error | Mean earned payoff per opportunity |
| ---: | --- | ---: | ---: | ---: |
| 32,768 | Exp3 over judges | 1,234.026563 | 0.032138 | 0.132551 |
| 32,768 | Outcomes decoded from payoff | 3.448135 | 0.000024 | 0.170087 |
| 131,072 | Exp3 over judges | 1,807.213359 | 0.003197 | 0.156262 |
| 131,072 | Outcomes decoded from payoff | 4.155076 | 0.000009 | 0.169991 |

All means cover the same 64 specified runs. The oracle's expected payoff is
0.17; a finite realized mean can exceed that expectation by sampling noise.
Population regret integrates the price law using the hidden true probability
only for evaluation. It is actual decision value forgone, not a monetary
audit fee or a measured CPU cost. Both methods purchase outcomes on about
half the opportunities. Exp3 chooses the correct judge in about 96.89% of
the final 4,096 opportunities, averaged over runs, but its earlier mistakes
remain charged in cumulative regret.

The [program](../notebook/P4-R6-C001/payoff_learning.py) and
[per-run output](../notebook/P4-R6-C001/payoff_learning.json) preserve this
adverse comparison for the generic evaluator. The positive construction is
stronger when it exploits the known payoff structure. No claim is made that
these methods outperform established statistics, or that the generic judge
bank is the best available learner.

## 6. The precise connection to judging judgment

The **task** is a goal-conditioned choice in an uncertain context. The
**first-order judge** is the forecast-based action ranking. Its **performance**
is the achieved return in the world. The **second-order judge** assesses and
updates reliance on that first-order judge using those returns. In R6.1/R6.2,
this also selects which context distinctions deserve retention. That last
operation is the task-delineation connection to T=J^2.

Instrumental convergence and J-squared meet at this mechanism: several
different outer purposes can vindicate the same improved judge or intermediate
capability. Their shared external constraints can therefore change what they
value internally. A fixed-point or successful-use theorem needs the declared
feedback, exposure, representation and cost conditions; the phrase “judging
judgment” does not supply them by itself.

The payoff-only learner is implemented. The finite-bank curvature theorem is
a mathematical composition. [R6.16](R6_learned_concepts.md) implements learned
representation selection using purchased payoff observations, with explicit
training and deployment prices. Shared funding and endogenous goal revision
remain separate: their observation and cost contracts still need integration.
The cycle advances C1/C2 and a restricted C3 mechanism while keeping that
larger obligation explicit.
