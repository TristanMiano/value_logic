# R6.8 Conditional rollout values can recover a policy

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** finite reconstruction theorems and rational checks, based on
established Bellman and successor-representation identities. This is an
interpretive advance for C7, not a new reinforcement-learning algorithm.

The author's proposed conversion from policy to values by counting its
trajectories has a precise, invertible form. Retain which state each rollout
started from and the discounted occupancy of each possible destination.
These values recover the policy's induced transition behavior. When actions
are distinguishable in a known environment, they recover the policy itself.
Under additional action-separation conditions, even a single ordinary value
function is sufficient.

This preserves more of C7 than merely observing that an arbitrary reward
cannot be inferred from behavior. It identifies the information that the
value representation must retain, and the conditions under which the proposed
duality holds. It also explains why a reusable predictive representation can
remain valuable across changes of practical goal.

## 1. The rollout-count construction

There are n states, a stationary policy pi and a fixed environment. Together
they induce a row-stochastic state-transition matrix P. Let 0<gamma<1 be a
known discount. Define the conditional occupancy-value matrix

```math
M_{sj}=\mathbb E_\pi\left[\sum_{t\ge0}\gamma^t
                 \mathbf1\{S_t=j\}\mid S_0=s\right].     \tag{V.1}
```

Column j is an ordinary value function for the state reward r_j(s)=1{s=j}.
The complete matrix is a family of such values, not a single scalar attached
to each state independently of the question being asked. Normalizing by
1-gamma makes every row a probability distribution without changing its
information content when gamma is known.

**Theorem 1 (conditional count/value reconstruction).**

```math
M=\sum_{t\ge0}\gamma^tP^t=(I-\gamma P)^{-1},
\qquad P=\frac{I-M^{-1}}\gamma.                          \tag{V.2}
```

*Proof.* The t-step occupancy probabilities are the entries of P^t. The
series converges in the maximum row-sum norm because ||gamma*P||=gamma<1.
Multiplication by I-gamma*P telescopes to I. Inverting and rearranging gives
the second identity. QED.

The successor representation originates in
[Dayan (1993), section 3](https://www.gatsby.ucl.ac.uk/~dayan/papers/d93b.pdf),
including occupancy-based state representations and their discounted version.
The inverse in (V.2) is an immediate consequence of that established identity.
The contribution here is its explicit use to type the author's rollout/value
proposal and state what information it recovers.

Let the known environment have transition rows T(a,s,·). The policy satisfies
P(s,·)=sum_a pi(a|s)T(a,s,·). If these rows are affinely independent at each s,
the mixture weights pi(a|s) are unique and are recovered by linear algebra.
Distinct deterministic next states are a simple sufficient case. If two
actions have identical effects, their individual probabilities are hidden
from state-only rollouts, while their combined effect is still recovered.
Recording action-labelled trajectories, or testing distinguishing effects,
repairs that observational ambiguity.

The fixed environment and stationarity assumptions matter. A hidden memory
state can make observed state transitions non-Markovian; include the needed
history or internal state before applying this finite matrix reconstruction.

## 2. When one value function already identifies the policy

Suppose the environment T, immediate reward r(s,a) and discount are known.
For a value vector V define its continuation values

```math
Q^V(s,a)=r(s,a)+\gamma\sum_{s'}T(s'\mid s,a)V(s').       \tag{V.3}
```

If V is the true value of pi, its Bellman equation says
V(s)=sum_a pi(a|s)Q^V(s,a).

**Proposition 2 (single-value recovery).**

- For a deterministic policy, if exactly one action satisfies Q^V(s,a)=V(s)
  at each state, that action is pi(s), so V identifies the policy.
- For two actions 0 and 1, if Q^V(s,1) differs from Q^V(s,0), even a stochastic
  policy is recovered by

```math
\pi(1\mid s)=\frac{V(s)-Q^V(s,0)}{Q^V(s,1)-Q^V(s,0)}.  \tag{V.4}
```

Both claims follow directly from the Bellman equation. The policy need not
be optimal: the condition is that the relevant action consequences are
distinguishable by this value. For an optimal deterministic policy with a
specified greedy tie rule, the familiar greedy reconstruction from V* is
another sufficient mechanism.

For more than two actions, several value functions for different declared
rewards provide a corresponding linear system. The policy is identifiable
when the vectors consisting of a leading one and those continuation values
are linearly independent across actions. This is a coverage/rank condition,
with the full occupancy family in section 1 as a general finite repair.

### Stability under approximation

Let ||Vhat-V||_infinity<=epsilon. Then every continuation value in (V.3) has
error at most gamma*epsilon. For deterministic recovery, define the gap

```math
d=\min_{s,\ a\ne\pi(s)}|V(s)-Q^V(s,a)|>0.
```

Choosing the action with the smallest Bellman residual recovers pi whenever
d>2(1+gamma)*epsilon. The true action's residual is at most
(1+gamma)*epsilon; every incorrect residual exceeds that value.

For the two-action stochastic case, let
Delta_s=|Q^V(s,1)-Q^V(s,0)|. If Delta_s>2*gamma*epsilon, applying (V.4) to
the approximations and clipping to [0,1] gives

```math
|\widehat\pi(1\mid s)-\pi(1\mid s)|
\le\frac{(1+\gamma)\epsilon}
          {\Delta_s-2\gamma\epsilon}.                  \tag{V.5}
```

*Proof.* Subtract pi times the approximate denominator from the approximate
numerator. The true terms cancel. The remainder is the value error minus
the pi-weighted mean of the two continuation-value errors, of magnitude at
most (1+gamma)*epsilon. The denominator has magnitude at least
Delta_s-2*gamma*epsilon. Clipping toward the probability interval cannot
increase error. QED.

Thus the recovery is quantitatively useful when action consequences remain
separated. Near a tie, more precise evaluations or additional separating
uses are needed; making the statement universal would hide this cost.

## 3. What the duality implies about description length

For finite rational matrices and rational gamma, both transformations in
(V.2) are computable with fixed algorithms. Conditional on n and gamma, their
shortest exact program descriptions therefore satisfy

```math
K(M\mid n,\gamma)=K(P\mid n,\gamma)+O(1).              \tag{V.6}
```

Here K is ordinary shortest-program description length, with a fixed encoding
and universal machine. With a known rational environment whose action-mixture
map is injective, the same statement holds between M and pi, conditional on
that environment. Under Proposition 2's rational separation conditions it
also holds between the full vector V and pi, conditional on T,r,gamma: the
forward direction solves policy evaluation and the reverse performs the
specified Bellman reconstruction.

This is an elementary computable-recoding result. It says that the relevant
behavioral information has not disappeared into a simpler evaluative label.
It is not a bound on runtime, neural-network size or sample complexity, and
it does not turn a large input domain into a description-length lower bound.
Structured policies and their values can both have short descriptions. Giving
the decoder an uncounted complex environment would also invalidate an
unconditional comparison; the conditioning above is essential.

For optimal policies in a fully specified finite MDP, unbounded computation
can itself find the optimum from T and r. The conditional description claim
is then correspondingly weak. The informative bounded question concerns
representation size, evaluation precision and the computation needed to use
the representation, which the simple recoding alone does not settle.

## 4. The boundary suggests which information to retain

A constant state reward gives V(s)=1/(1-gamma) for every policy. This reward
does not separate action consequences. The repaired thesis is not that no
values reveal policy, but that **values for sufficiently separating uses do**,
with Theorem 1 and Proposition 2 describing two concrete routes.

Unconditional stationary visitation counts can likewise agree for different
transition processes. Retaining the starting context and discounted
destination counts restores (V.2). This is a direct refinement of the
[founding rollout proposal](../../posts/condensed-response-hidden-complexity.txt),
not a replacement of it with a non-identifiability verdict.

The full successor matrix is invertible. An exact factorization M=FG through
d real features therefore requires d>=n. This linear-rank statement is
distinct from program description length. Recent primary work by
[Zheng, Jayanth and Eysenbach (2026), v2, section 3.1 and appendix C.1](https://arxiv.org/abs/2602.11399v2)
develops related rank requirements for forward/backward successor-measure
representations and studies constructive approximation methods. Its linear
factorization assumptions do not rule out compact nonlinear descriptions of
structured policies. Here only the necessary rank argument is reconstructed;
the paper's training and empirical claims are not independently assessed.

## 5. What this says about common instrumental values

Several changing goals can reuse the same conditional rollout representation.
Each goal selects a reward vector; multiplying by M predicts that policy's
returns. This explains one stable internal value of factual predictive
structure even when current purposes change. Improving the policy changes M,
so its old predictions need reassessment rather than automatic reuse.

These predictive values need not be a unique terminal utility. Their content
is what the policy tends to bring about and how those consequences serve
specified uses. To infer broader alignment with a person's values requires
evidence about those uses and the policy's choices, not just the existence
of the representation. A positive restricted inference remains available:
successful behavior across separating, actually evaluated tasks constrains
the corresponding behavioral value representation and capability geometry.

The [rational checker](../notebook/P4-R6-C001/policy_values.py) compares
rollout-matrix reconstruction, separated single-value inversion, approximation
bounds and the constant-reward boundary in one small known environment.
The results are finite checks of the stated mechanism; a learned nonlinear
policy/value representation remains a W5/W6 research direction.

The [value-query supplement](R6_value_identification.md) reverses the
information contract: known policies and rewards, unknown action dynamics.
It gives an exact joint-separation criterion, a four-policy single-reward
identification example with a genericity proof, and finite precision bounds.
This connects policy/value duality to the factual-recovery question while
preserving the difference between optimal attainable value and values of
specified interventions.
