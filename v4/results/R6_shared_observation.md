# R6.3 Different goals can jointly fund a common observation

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** elementary decision and game-theoretic construction, with exact
finite checks. This is a provision mechanism for the shared information in
[R6.1](R6_goal_judgment.md), not a claim of a new public-goods mechanism.

Common usefulness can support common investment even when nobody values the
others' final goals. A binding conditional cost-sharing agreement supplies
one precise bridge from positive information value to acquiring it. The
agreement's enforcement and the cost of observation are part of the model.

## 1. A physical observation that has not already been given away

In each of T rounds, a fresh fair hazard H is drawn. Agent i's goal concerns
H with probability alpha_i; otherwise it concerns a private outcome it already
observes. Hazard and private goal choices, prices and hazards across rounds
are independent. Hazard goals offer the payoffs 0 and H-t, where t is uniform
on [0,1]. Outcomes become available after the decision. Past outcomes do not
reveal the next independent hazard.

A public sensor, installed before the rounds, reports H through a known
binary symmetric channel with error eta in [0,1/2]. Its reports arrive before
decisions. Its total cost C includes installation, operation, delay and
contract enforcement insofar as those occur in this model. Unlike R6.1's
representation benchmark, H is initially **unobserved**. This cost purchases
new information; it does not charge agents to relearn an already visible bit.

Without the sensor, the hazard posterior is 1/2. With it, the posterior is
eta or 1-eta, with equal probabilities. Since the uniform-price attainable
payoff at probability p is p^2/2, agent i's expected gross benefit is

```math
B_i=\frac{T\alpha_i(1-2\eta)^2}{8}.                    \tag{F.1}
```

This is a benefit under the agent's own goal. Reproduction, agreement or
truthfulness need not be terminal goals for the sensor to be useful. This
particular environment supplies a common instrumental reason to observe H.

## 2. Provision and a specific coordination repair

**Proposition 1 (funded shared judgment).** Suppose benefits and total cost
are common knowledge, the relevant agents can afford their shares, and
S=sum_i B_i>C. On the positive-benefit coalition, choose shares
c_i=C*B_i/S. A sequential offer of these fixed shares, binding only if every
member accepts, has a subgame-perfect provision outcome in which every member
strictly benefits. If instead agents contribute simultaneously to a threshold
fund with refunds on failure, all-zero contributions are also an equilibrium
whenever every B_i<C.

*Proof.* Each fixed share is strictly below its payer's benefit. The last
responder accepts conditional on earlier acceptances; backward induction gives
every preceding acceptance and the proposer's offer. No payment is made if
the contract fails. In the simultaneous game, a unilateral deviation from
zero must pay at least C to provide the sensor, which costs more than its
deviator's benefit. Smaller deviations are refunded. QED.

This is complete-information coordination with an enforceable contract.
It is not a strategy-proof mechanism for unknown private benefits. The
simultaneous game can also have funded equilibria; underprovision here is
an equilibrium-selection problem, not an impossibility of cooperation.

For two agents with alpha_1=alpha_2=1/2, T=1, eta=0 and C=1/10, each benefit
is 1/16. Neither wants to buy the sensor alone. Paying 1/20 each gives each
agent a net improvement of 1/80. Their private final interests remain different.

At eta=1/10, a single round gives each only 1/25, so the total benefit 2/25
is below the cost. Two uses give each 2/25 and make the same shared purchase
worthwhile. If operation costs c per use in addition to a fixed installation
cost C_0, the coalition condition becomes

```math
T\left[\frac{(1-2\eta)^2}{8}\sum_i\alpha_i-c\right]>C_0. \tag{F.2}
```

Reuse helps only if the per-use gross benefit exceeds the per-use expense.
Improving sensor reliability, lowering its cost or increasing useful future
uses are concrete repairs; more repetitions of an uneconomic operation are
not enough.

## 3. An evidence-based agreement and its limits

If a justified pilot or observation experiment supplies simultaneous lower
bounds L_i on the benefits and an upper bound Cbar on total cost, sum_i L_i>
Cbar suffices to choose shares Cbar*L_i/sum_j L_j. On the confidence event,
each participant's expected benefit exceeds its share. This is a conditional
mathematical composition with finite evidence, not an implemented acquisition
controller. The pilot's access and cost must be included; the construction
does not obtain sensor labels for free in order to prove the sensor worth buying.

The [exact check](../notebook/P4-R6-C001/shared_observation.py) derives (F.1)
from realized outcome/payoff integration and enumerates a small contribution
game. Its [saved output](../notebook/P4-R6-C001/shared_observation.json)
records both the funded and unfunded equilibria and the noise/reuse repair.

The C1/C3 progress is a mechanism by which shared practical needs can fund
contact with the world; the common observation has a known interpretation and
is not inferred from consensus alone. Unknown sensor reliability, strategic
misreports, endogenous future goals and private-information contracting remain
separate obligations. The result complements the observed judgment learner;
the two have not been implemented as one combined system.
