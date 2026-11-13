# R6.1 Practical goals can generate a common factual standard

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** mathematical construction, exact finite checks and primary-source
comparisons; see the [assessment](../notebook/P4-R6-C001/assessment.md).

Different purposes can reward the same accurate judgment. In the construction
below, agents evaluate forecasts by the returns of practical choices. A broad
enough set of those choices makes inaccurate factual forecasts costly. Agents
can therefore share a standard of good judgment without sharing a final goal.
The result also identifies the precise distinctions each goal family requires,
the distinctions every agent requires, and the extra information available by
pooling complementary agents.

This advances the C1/C2 mechanism and prepares C3's successful-use question.
It is a decision-theoretic construction, not a general truth theory. Its
proper-score geometry is established mathematics; the contribution sought is
the explicit connection between instrumental uses, judgment and shared kinds.

## 1. The judgment experiment

Let Y take values in a finite outcome set of size m>=2, and let X be an observed
context with finite positive-probability support. Write p(x)=P(Y|X=x).
A representation c(X) restricts what the agent retains about its context.
A forecast r is a probability vector; its decision consequences will be judged.

A goal g is drawn independently of (X,Y) and announced before acting. It
specifies a finite action set and bounded payoff vectors u_g(a) in outcome
space. The action a_g(r) maximizes the forecast expected payoff; fix a
measurable tie rule. Define the attainable value and the expected payoff
vector selected by the forecast as

```math
\Phi(p)=\mathbb E_g\max_a\langle p,u_g(a)\rangle,
\qquad h(r)=\mathbb E_g u_g(a_g(r)).                         \tag{G.1}
```

The forecast's expected achieved payoff in world p is dot(p,h(r)). Thus
the evaluation comes from the consequences of a practical judgment. Nothing
in this definition yet ensures that every factual error changes an action.

**Lemma 1 (decision-generated judgment).** Phi is convex, h(r) is a
subgradient at r, and the payoff regret is

```math
\Phi(p)-\langle p,h(r)\rangle
 =\Phi(p)-\Phi(r)-\langle h(r),p-r\rangle\ge0.              \tag{G.2}
```

*Proof.* A maximum of linear functions is convex. The selected action gives
Phi(p) >= dot(p,h(r)), while Phi(r)=dot(r,h(r)). Subtracting the latter
identity gives both the subgradient inequality and (G.2). Expectations are
well defined by the bounded-payoff assumption. QED.

For a representation c, the calibrated posterior is pbar(c)=E[p(X)|c(X)].
Its optimal value loss is

```math
\Delta(c)=\mathbb E\bigl[\Phi(p(X))-\Phi(\bar p(c(X)))\bigr]. \tag{G.3}
```

The linear term in (G.2) has conditional expectation zero. Equation (G.3)
compares optimal decisions under different retained information. Equation
(G.2) additionally measures errors made by a possibly inaccurate forecast.
Neither equation alone pays for acquiring information or computing an action.

## 2. A concrete goal-coverage condition

Goal j offers a choice between payoff zero and the contract v_j(Y)-t.
The vector v_j describes an outcome the agent cares about; t is its opportunity
cost or price in the same units. Draw j with probability alpha_j>0. Conditional
on j, draw t with density w_j on [a_j,b_j], an interval containing every entry
of v_j, with b_j>a_j. Prices and the chosen goal are independent of (X,Y).
The agent buys precisely when dot(r,v_j)>t; ties have zero probability.

Suppose w_j(t)>=rho_j>0 almost everywhere on the interval. Define

```math
A=\sum_j\alpha_j\rho_j v_jv_j^T,
\qquad z_j(p)=\langle p,v_j\rangle.                         \tag{G.4}
```

**Theorem 2 (practical coverage makes judgment informative).** The expected
payoff regret of any forecast r under the true outcome law p obeys

```math
\Phi(p)-\langle p,h(r)\rangle
 \ge\frac12(p-r)^TA(p-r).                                 \tag{G.5}
```

If prices are uniform, take rho_j=1/(b_j-a_j); then (G.5) is an equality.
For any context representation,

```math
\Delta(c)\ge\frac12\mathbb E
 \bigl[(p(X)-\bar p(c(X)))^TA(p(X)-\bar p(c(X)))\bigr].       \tag{G.6}
```

Loss is zero exactly when every z_j(p(X)) is measurable from c(X).
If the payoff contrasts separate the probability simplex, define

```math
\lambda=\min_{d:\,\mathbf1^Td=0,\ \|d\|_2=1}d^TAd>0.
```

Then regret at most epsilon forces squared forecast error at most
2 epsilon/lambda; expected representation loss at most epsilon forces
E[||p-pbar|| squared] <= 2 epsilon/lambda. If lambda=0, the same result
still controls the represented contrasts through (G.5)--(G.6).

*Proof.* Fix j and put z=dot(p,v_j), q=dot(r,v_j). If q<z, the forecast
declines profitable contracts at prices in (q,z). If q>z, it accepts
unprofitable ones at prices in (z,q). The exact regret in either case is

```math
\int_{\min(z,q)}^{\max(z,q)} |z-t|\,w_j(t)\,dt
 \ge\frac{\rho_j}{2}(z-q)^2.                              \tag{G.7}
```

Uniform density makes the inequality exact. Sum over j for (G.5), then
average over X with r=pbar(c(X)) for (G.6). Since all weights and lower
density bounds are positive, zero loss forces z_j(p)=z_j(pbar) almost surely
for every j. Conversely that equality makes every available decision have
the same conditional payoff, so there is no loss. Finally p-r has coordinate
sum zero, and the Rayleigh quotient on that subspace gives the spectral bound.
QED.

**Minimal qualitative coverage.** The exact zero-loss characterization needs
only positive price probability in every nonempty open subinterval, rather
than a common positive density bound. Any unequal z and q then make the
integral of the strictly positive loss over their intervening prices positive.
A numerical error bound requires quantitative coverage; qualitative support
alone supplies no uniform spectral constant.

**Coverage gaps and their repair.** If all prices avoid an interval containing
two different expectations, those expectations can induce the same action at
every available price. Adding prices inside the gap gives that distinction
positive decision value. A feature vector orthogonal to a missing contrast
never exposes it regardless of price coverage; adding a separating feature
repairs this different failure. Both feature coverage and price coverage matter.

## 3. Individual, common and pooled factual kinds

Agent i has its own goal family satisfying the qualitative coverage condition.
Let pi_i partition contexts by equality of that family's conditional feature
expectations. These are the coarsest context distinctions that optimal
judgment for that agent must retain. Agents may use different labels for the
same kinds; no agreement of vocabulary is assumed.

**Proposition 3 (the shared requirement).** A representation is adequate for
agent i exactly when it determines pi_i. The finest common distinction forced
separately by every agent's goals is the following partition tau: connect x
and x' whenever they belong to the same pi_i cell for at least one i, and
take the connected components. Pooling the agents' required information instead
gives the partition whose labels are the tuples (pi_1(x),...,pi_k(x)).

*Proof.* The individual statement is Theorem 2's zero-loss characterization.
A fact available from every minimal representation must be constant on every
pi_i cell. Therefore it is constant along the connecting edges and on their
components. Conversely a component label is constant on each pi_i cell, so
each agent's required representation determines it. The pooled tuple retains
exactly all the individual labels. QED.

This is a statement about information *required by the goals*. Agents can
voluntarily retain more information, which can enlarge their actual shared
knowledge. Also, near-optimality gives a weighted error statement; it does
not force exact symbolic equality of partitions without a separation margin.

**Example: common hazard, different purposes.** Let contexts correspond to
three independent fair bits (H,A,B), with those bits also the future outcome.
Agent 1's goals price the H and A coordinates; agent 2's price H and B. Each
coordinate has positive goal probability and prices cover [0,1]. Agent 1
requires the four kinds (H,A); agent 2 requires the four kinds (H,B). Their
finest forced common fact is H, a two-cell partition. Pooling their information
recovers all eight kinds. If the common H goals are removed, both agents can
still judge their private outcome perfectly while having no nonconstant
factual distinction forced in common. Restoring those goals restores the
shared hazard requirement. This example has a deterministic outcome given the
full context; in a general noisy world these three coordinate features reveal
marginals and need not identify their joint law.

This is the abstract core's task/performer/outcome/judge typing: a context is
the task instance, a forecasting rule is the performer, a priced decision
produces the performance, and its realized payoff evaluates the judgment.
The later funding game adds actual interaction between agents.

**Support-specific information.** Do not identify tau with an intersection
of linear feature spans. On three deterministic outcome contexts, features
(0,1,2) and (0,1,4) each separate all contexts. Each agent's minimal context
partition is therefore the full three-cell partition, although their centered
one-dimensional feature spans have zero intersection. Across the whole
probability simplex these features do not separately identify all probability
vectors. The actual posterior support and the quantifier matter.

## 4. Resource cost can prioritize the common distinction

In the eight-context example, give both agents equal probability of their
shared and private goals. Evaluate a common representation by the sum of the
agents' expected decision payoffs, and charge kappa times (k-1) for retaining
k cells. This is a declared representation charge, not a measured CPU cost.
The benchmark gives the representation optimizer the population law. Finite
learning and the agents' willingness to fund the representation are separate
obligations.

Enumeration of all 4,140 partitions gives the following exact optimal gross
joint payoff. The constant representation has payoff 1/4.

| Number of cells | Best joint payoff | Gain over a constant |
| ---: | ---: | ---: |
| 1 | 1/4 | 0 |
| 2 | 3/8 | 1/8 |
| 3 | 13/32 | 5/32 |
| 4 | 7/16 | 3/16 |
| 5 | 29/64 | 13/64 |
| 6 | 15/32 | 7/32 |
| 7 | 31/64 | 15/64 |
| 8 | 1/2 | 1/4 |

Consequently, at kappa=1/20 the unique optimal partition retains exactly H.
At kappa=1/50, four partitions with four cells are optimal, and all retain H;
they may retain different private features in different H cells. At
kappa=1/100, retaining all eight contexts is uniquely optimal. At kappa=1/5,
the constant representation is uniquely optimal. Lowering acquisition cost
or amortizing a fixed charge over repeated uses can therefore make richer
distinctions worthwhile. The common hazard is the first distinction worth
paying for in this instance; that priority is a result of these goals and
this environment, not a goal-independent ranking of facts.

This is finite exhaustive evidence about an explicitly declared objective.
It is not a new general clustering algorithm, and no optimizer was asked to
infer the world from data in this enumeration.

## 5. Evidence and relationship to established work

Lemma 1 is standard convex/proper-score geometry. The one-feature uniform-price
identity is the cost-loss representation already used in W1's
[decision bridge](../notebook/P4-R1-C001/assessment.md#when-a-distinction-changes-a-decision).
The feature matrix and partition characterization make the multi-agent
instrumental reading explicit: varied goals can require shared factual content,
different goals can require complementary content, and the two conclusions
have distinct information objects.

The [rational checker](../notebook/P4-R6-C001/goal_geometry.py) and
[saved output](../notebook/P4-R6-C001/goal_geometry.json) independently integrate
realized contract payoffs for 784 forecast pairs under each of two price laws.
They check 8,280 individual adequacy statements across all eight-context
partitions, the common-versus-pooled distinction, both coverage failures and
the price-coverage repair. The finite cost table uses those same partitions.
The [source comparison](../notebook/P4-R6-C001/sources.md) records the primary
results and actual read scopes.
No literature-priority claim is made for these elementary mathematical facts.
The cycle's [observed learner](R6_learned_concepts.md) and
[funding game](R6_shared_observation.md) develop two of these obligations.
Their complete integration, measured computation costs and open-ended
representation construction remain available research directions.
Goal distributions are declared here; their emergence is a W7 question.
