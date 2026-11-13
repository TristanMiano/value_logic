# R6.6 Different fixed goals can acquire the same useful internal priority

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** an exact bounded-planner example and reconstructed established
reward-shaping identities. The outer-learning connection is mathematical;
the example does not simulate an entire self-modifying architecture.

Agents with different fixed final goals can improve by assigning direct
internal value to the same preparatory step. This can be a change in how a
bounded agent pursues its goal, with no change in its preference over complete
outcomes. Completed-task feedback can then teach it whether to keep that
internal priority. This gives W6 a concrete connection to judging judges and
to C5's values assigned to values.

## 1. A common subgoal with distinct final actions

An episode starts at root state s. There are two choices:

- **Direct:** receive payoff 0.4 and end the episode.
- **Prepare:** pay 0.1 and move to prepared state h. From h, choose a final
  action indexed by a goal label. For an agent with fixed goal g, its matching
  action returns one with probability p_g and zero otherwise. Other final
  actions return zero. All final actions end the episode.

Episodes reset at a common scheduled boundary. Thus ending early creates no
extra unpriced opportunities. Payoffs are undiscounted within this finite
episode. The final-goal label is clamped: internal revision cannot change
which terminal outcome it rewards. Consider three agents whose distinct
matching actions have success probabilities 0.7, 0.8 and 0.9.

A one-step planner knows immediate expected rewards but does not propagate
the value of h back to s. It chooses Direct because 0.4 exceeds -0.1. A
two-step planner chooses Prepare and achieves p_g-0.1. A local internal
signal can give the one-step planner the same behavior.

Set a potential Phi(h)=theta, with Phi(s)=0 and zero potential at every
terminal state. Replace the planner's local reward by

```math
r'(x,a,x')=r(x,a,x')+\Phi(x')-\Phi(x).                \tag{B.1}
```

For theta=0.6, Prepare now has immediate value 0.5, so the one-step planner
chooses it. At h all terminal actions lose the same 0.6; their ranking is
unchanged, so each agent chooses its own matching action. The internal signal
has made preparation directly attractive to each agent without making their
desired final outcomes identical.

| Agent's success probability | Raw one-step planner | Shaped one-step planner | Two-step planner | Gain from the shared priority |
| ---: | ---: | ---: | ---: | ---: |
| 0.7 | 0.4 | 0.6 | 0.6 | 0.2 |
| 0.8 | 0.4 | 0.7 | 0.7 | 0.3 |
| 0.9 | 0.4 | 0.8 | 0.8 | 0.4 |

These are expected **actual episode returns**, with the preparation cost
included. They are not shaped-reward totals presented as external benefits.
The two-step planner is an equally informed conventional alternative. The
example makes no measured claim about total computation or learning cost.

## 2. Local value can change while complete preferences remain fixed

For a trajectory ending at time H, summing (B.1) gives

```math
\sum_{t=0}^{H-1}r'_t
=\sum_{t=0}^{H-1}r_t+\Phi(s_H)-\Phi(s_0)
=\sum_{t=0}^{H-1}r_t.                                  \tag{B.2}
```

Thus every completed trajectory retains its original payoff, not merely
the trajectory chosen in the example. More generally, discounted shaping
r'=r+gamma*Phi(s')-Phi(s) telescopes to -Phi(s_0) plus a boundary term.
That term vanishes for bounded Phi on an infinite discounted horizon, or
for zero terminal potential on a finite horizon. Consequently an ideal
planner's policy ranking is unchanged. The benefit in section 1 comes from
the deliberately bounded planner's use of local rewards.

This is the established potential-based shaping mechanism of
[Ng, Harada and Russell (1999), theorem 1 and corollary 2](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf).
Their sufficiency proof substitutes the shifted value into the Bellman
equation. Their necessity statement ranges over otherwise unspecified
transition and reward functions; it does not say that every useful shaping
rule for one known environment must have this form. We use sufficiency here.

This distinction answers part of the terminal/instrumental question. A
preparatory step can become directly rewarded by the agent's operational
machinery while remaining instrumental in its complete-trajectory evaluation.
That is one precise degree of terminal-like treatment. It is different from
an irreversible preference for preparation even after all benefits disappear.
[R6.4](R6_plastic_priorities.md) separately analyzes persistence and resistance
to revision; the two meanings must not be silently equated.

## 3. Judging the internal priority by its consequences

Let an outer learner choose between two inner planners, with theta=0 and
theta=0.6. It observes the chosen planner's actual episode return. It is not
paid the internal shaping bonus. Under the reset and observation contract of
[R6.5](R6_payoff_judgment.md), the shaped planner has net margin at least 0.2
for each of the three agents. Sublinear regret to that planner therefore
implies time-average adoption of the common preparatory priority. Initial
positive preferences over the two planners can differ.

The same conclusion holds under changes among those goals when the uniform
net margin and learning conditions persist. The outer learner evaluates a
judge of actions by the consequences of the judgments it produces. The
object being revised is an internal value signal; the evaluating goal may
remain fixed. This is a concrete typed instance of value applied to value.

The example also supplies a declared realization of R6.4's retention ratios.
Suppose a program's expected positive retention multiplier is 1+V, where V is
its actual expected completed-task return in these units. Then the raw
planner has multiplier 1.4 and the shaped planner has multiplier 1+p_g-0.1.
Their ratios are 8/7, 17/14 and 9/7. With goal revision independent of the
priority, R6.4 applies with R_* = 8/7. The map from payoff to retention is a
separate physical or algorithmic assumption. A higher task score does not
automatically imply more biological reproduction or more retained code.

Online design of an internal reward for a bounded agent is established work.
[Sorg, Singh and Lewis (2010)](https://proceedings.neurips.cc/paper_files/paper/2010/file/168908dd3227b8358eababa07fcaf091-Paper.pdf)
learn reward parameters against an external objective, with explicit bounded
planning and model conditions. The present contribution is the transparent
connection among clamped goals, a shared plastic subgoal, outer judgment and
the separate persistence mechanism; it is not a new reward-design algorithm.

## 4. Conditions for useful agreement and useful divergence

The shaped planner prepares whenever theta>0.5. It therefore also prepares
for p_g=0.3, achieving 0.2 where Direct would achieve 0.4. Potential shaping
still preserves the *ideal* policy ranking, but this particular myopic use
of the potential is now harmful. An outer evaluator using actual returns
can learn to reject it. A deeper planner can reject preparation immediately
if its model is correct. Keeping both possibilities matters: a transformation
safe for an ideal optimizer need not improve every bounded procedure.

More generally, with direct return d, preparation cost c and delayed expected
return p, a common preparation policy has positive actual advantage precisely
when p-c>d. If the second payoff is discounted, replace p by gamma*p. Shared
preferences over preparation are justified for a family with a common positive
margin; goal-dependent costs, deadlines or success rates can rationally
separate that family. Plastic subgoals need not converge beyond this region.

Three other boundaries have constructive counterparts:

- A non-potential bonus paid repeatedly for entering h can reward an
  unproductive cycle. A potential pays back the elevation on return and
  preserves the completed path evaluation under the boundary conditions above.
- If the outer learner never tests an initially disfavored planner, a good
  priority can remain undiscovered. Controlled exploration and recurring reset
  tasks provide a concrete discovery route; their costs must be included.
- If the available internal signals cannot induce preparation, changing only
  their weights cannot realize it. Enlarge the signal vocabulary or increase
  the planner's horizon, then compare the resulting costs and benefits.

## 5. An identical implementation and a genuinely different alternative

For tabular Q-learning, compare a shaped learner with initial Q_0 and an
unshaped learner with initial Q'_0(s,a)=Q_0(s,a)+Phi(s). On the same experience
sequence and with the same step sizes, induction gives

```math
Q'_t(s,a)=Q_t(s,a)+\Phi(s)\quad\hbox{for every }t.       \tag{B.3}
```

Indeed, substituting (B.3) into the unshaped temporal-difference error produces
the shaped error, so each update preserves it. Action selection invariant to
a statewise additive constant, including greedy and epsilon-greedy rules,
then has the same distribution. This is
[Wiewiora's (2003) exact equivalence](https://arxiv.org/abs/1106.5267), not an
empirical performance tie. Counting these implementations as different
scientific mechanisms would exaggerate the comparison.

In contrast, increasing planning depth, learning a transition model, and
learning which local signal to retain are different procedures with different
information and computation costs. Their ability to reach the same useful
behavior does not erase the explanatory point: a bounded reasoner can improve
the way it values an intermediate step while retaining a distinct final goal.

The [exact checker](../notebook/P4-R6-C001/bounded_subgoals.py) tests completed
trajectory totals, the success/cost boundary and Q-update equivalence.
The learning-adoption and goal-revision connections above are mathematical
compositions of separately stated models, not a jointly run implementation.
