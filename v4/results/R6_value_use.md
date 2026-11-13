# R6.15: acquired values can guide action without rewarding endless preparation

**Codex (GPT-6), November 12, 2026. P4-R6-C001; cycle complete; module available to recur.**

An acquired intermediate value can make a bounded agent pursue a useful
subgoal while its final criterion stays fixed. A constructive condition is
to use that value as a forecast of continuation, with an update rule that
can correct it. Paying the forecast repeatedly as if it were a newly earned
outcome can instead make the intermediate state an attractor in its own
right. This separates useful internalization, behavioral persistence and
literal fixation, advancing C5/C7 and the author's terminality question.

The close existing comparison is
[Marklund, Infanger and Van Roy (2025), sections 3 and appendix B.3](https://arxiv.org/html/2507.10995v1):
their average-reward example shows severe consequences from mixing immediate
reward and relative value. The discounted example below extends our own
[R6.6](R6_bounded_subgoals.md) preparation task with a waiting action. The
constructive repair is established potential-based shaping, used to clarify
the relation between a bounded policy and its internal values. This is a
worked synthesis and characterization, not a new shaping theorem.

## 1. A useful preparation state and the price of fixation

At a root state, **Direct** ends the task for reward $d$, while **Prepare**
costs $c$ and reaches state $B$. At $B$, **Complete** ends the task with
expected reward $p$; **Wait** stays at $B$ for reward zero. All future rewards
are discounted by $0<\gamma<1$. Assume $p>0$ and $\gamma p-c>d$.
The optimal behavior is Prepare, Complete, with root value $\gamma p-c$;
$V_*(B)=p$.

Suppose an internal controller instead receives an extra per-step reward
$b>0$ whenever it acts at $B$, including when it completes. The value of
waiting forever becomes $b/(1-\gamma)$ and of completing immediately becomes
$p+b$. Therefore its optimal action at $B$ is Wait exactly when

$$
b>\frac{1-\gamma}{\gamma}p.
\tag{1}
$$

At equality, waiting and completion tie. If the extra reward is
$b=\beta V_*(B)=\beta p$, the boundary is simply
$\beta>(1-\gamma)/\gamma$. With $p=0.8$, $\gamma=0.99$, $c=0.1$,
$d=0.4$ and $\beta=0.02$, the internally rewarded agent prepares and
waits forever. Its true root value is $-0.1$, instead of the attainable
$0.692$. The learned subgoal has become independently rewarding under this
specified internal rule; convergence to it is no guarantee of usefulness.

This boundary also says when the same internal bonus is harmless for the
chosen action: below (1), the controller completes. No claim is made that
all intrinsic rewards or all persistent subgoals suffer this problem.

## 2. A value representation that preserves successful action

Use a potential $\Phi(B)=q$, $\Phi(\text{root})=\Phi(\text{terminal})=0$,
and shaped transition reward

$$
r_\Phi(s,a,s')=r(s,a,s')+\gamma\Phi(s')-\Phi(s).
\tag{2}
$$

For any bounded potential, its infinite discounted contribution telescopes
to $-\Phi(s_0)$. Hence all complete-policy comparisons from the same state
are preserved, including policies that wait indefinitely. This is the
standard [potential-based shaping result](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf).

For the **one-step** controller, the shaped expected rewards are

$$
\begin{array}{c|cc}
 &\text{first action}&\text{second action}\\
\text{root}&d\ (\text{Direct})&-c+\gamma q\ (\text{Prepare})\\
B&p-q\ (\text{Complete})&-(1-\gamma)q\ (\text{Wait}).
\end{array}
\tag{3}
$$

It uniquely chooses Prepare, Complete precisely when

$$
\frac{d+c}{\gamma}<q<\frac p\gamma.
\tag{4}
$$

The correct continuation value $q=p$ lies in this interval under the
assumptions. Thus an initially myopic controller can acquire an internal
priority that makes both steps useful; the internal value need not be a
clamped terminal reward. This is the positive counterpart to (1).

The distinction is operational. The per-step bonus pays repeatedly for
remaining at a promising state. The potential pays for improved prospects
and removes their previously credited value when prospects are used up.
Both are numerical values, but their composition rules differ.

## 3. Approximate values, correction and shared subgoals

**Proposition 1 (approximate continuation guidance).** In any finite
discounted MDP with bounded rewards and known transition expectations, a
one-step controller greedy for (2) with
$\|\Phi-V_*\|_\infty\le\eta$ has

$$
0\le V_*(s)-V_{\pi_\Phi}(s)
\le\frac{2\gamma\eta}{1-\gamma}.
\tag{5}
$$

**Proof.** The action scores $r(s,a)+\gamma\mathbb E\Phi(s')$ differ
from $Q_*(s,a)$ by at most $\gamma\eta$. Choosing their maximum loses at
most $2\gamma\eta$ in the true Bellman backup. Writing
$V_*-V_{\pi_\Phi}=V_*-T_{\pi_\Phi}V_*+
\gamma P_{\pi_\Phi}(V_*-V_{\pi_\Phi})$ and summing the resulting
geometric bound proves (5). $\square$

If several clamped goals share a strictly best action with action-value
margin $\delta$ in a specified state, each controller selects that same
action once its own value error is below $\delta/(2\gamma)$. Their values
can differ numerically and elsewhere in the environment. Repeated successful
judgment can therefore produce common subgoals without equal final rewards.
The margin must be evaluated against actual alternative actions, including
waiting and the costs of preparation.

Equation (4) also exposes a bounded-controller failure that the invariance
theorem alone does not prevent. An overestimate $q>p/\gamma$ makes the
myopic controller wait. A temporal-difference correction on its observed
zero-reward waiting transitions gives

$$
q_{t+1}=q_t+\alpha(\gamma q_t-q_t)
=[1-\alpha(1-\gamma)]q_t,
\qquad0<\alpha\le1.
\tag{6}
$$

It eventually crosses the completion threshold. For this correction to
improve behavior, the expectation $p$ used to evaluate Complete must itself
be available or learned through informative trials. If neither completion
nor another revealing observation occurs and $p$ is unknown, (6) alone is
not a full learning solution. Exploration as in R6.5 supplies a possible
repair; no such joint learner is asserted here.

The same distinction applies to [R6.8](R6_policy_values.md): reconstructing
a policy from its value measurements, choosing an action using a continuation
value, and repeatedly adding that value as a reward are three different
operations. The first two can faithfully express a capable policy. The
third needs its own justification and can change what the agent pursues.

## 4. Evidence and scope

The [checker](../notebook/P4-R6-C001/value_use.py) passed 48 exact bonus
settings, 5808 rational potential/Bellman checks, and 320 approximate-value
checks across 80 random MDPs, including 768 separated-action checks.
In the waiting-correction example with $q_0=0.9$, $p=0.8$, $\gamma=0.99$
and $\alpha=0.1$, correction takes 108 waiting steps. Its true root value is
then about 0.167501, better than permanent fixation at $-0.1$ but below both
the exact-value policy's 0.692 and the immediately available Direct action's
0.4. Eventual revisability does not make the cost of delayed revision vanish.
The prototype retains a fixed state space and a known reward expectation;
learning new concepts and choosing the evaluation rule itself remain W1/W4/W7
directions. Its contribution here is a precise positive answer about how
revisable internal values can support clamped goals, with a characterized
boundary where persistence becomes counterproductive.
