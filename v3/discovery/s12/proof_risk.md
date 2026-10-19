# Several fallible supports for one warranted action

Codex (GPT-6), s12. DEVELOPMENT derivation and early prior-work screen.
Connection: Q1/Q3/Q4, with S02/S07/S15/S25. No new family number or promotion.

## Fixed conclusion: logical diversity rather than independent errors

Let P_1,...,P_n be fixed, meaningful premises on a random instance X. Write
E_i={P_i is false}. Assume supplied valid marginal bounds Pr(E_i)<=epsilon_i;
do not assume independent failures or confuse these bounds with confidence
levels for their estimation. The latter requires an additional outer event.
A soundly checked derivation from every premise in S_j establishes one fixed
conclusion Q. There may be several such supports S_1,...,S_m.

If Q is false, the bad-premise set B must intersect every S_j. Let T be the
family of inclusion-minimal such hitting sets. With no additional information,
the sharp upper bound on the event that every listed support is broken is

```math
R=\max_{p\ge0}\left\{\sum_{B\in T}p_B:
  \sum_{B\ni i}p_B\le\epsilon_i\ \forall i,\quad
  \sum_Bp_B\le1\right\}.
```

Why minimal hitting sets suffice: move probability from any failing bad set
to a contained minimal hitting set; this preserves failure and only decreases
marginal failures. Move all nonfailure mass to the empty bad set. Conversely,
any feasible p is realized by putting the remaining mass at the empty set.
This is exact for the Boolean event defined by the listed supports. It is only
an upper bound on Q's falsity if Q can hold for additional reasons.

For nonempty supports and a finite premise universe, ordinary LP duality gives

```math
R=\min\left(1,
 \min_{\lambda\ge0}\left\{\sum_i\lambda_i\epsilon_i:
       \sum_{i\in B}\lambda_i\ge1\quad\forall B\in T\right\}\right).
```

To see the truncation, first drop the total-mass constraint. Its optimum is
the inner dual. If its mass exceeds one, scale a feasible solution to mass
one. Empty supports are unconditional proofs and give R=0; no support gives
no warrant. These degenerate cases should be handled before the formula.

Example: supports {1,2}, {2,3}, {1,3}, all epsilon_i=p<=2/3.
Failure requires two bad premises. Weights lambda_i=1/2 give R<=3p/2.
Put mass p/2 on each of the three two-bad patterns and the rest on all-good:
this attains 3p/2. A single support's union bound is 2p, so using all three
improves that bound by 25%, with arbitrary dependence. This is a constructed
probability-bound comparison, not an empirical error reduction or a gain over
the sharp ordinary reliability calculation. Duplicating one proof gives no
such benefit. Two disjoint supports need not multiply risks: their failures
can be perfectly dependent.

## A certificate that survives adaptive action selection

For multiple candidate actions, let Q_a(X) mean that action a is acceptable.
Each purchased checked proof support for a implies Q_a. A policy may acquire
proofs and exact premise receipts adaptively and select its action from them.
The marginal epsilon_i do not automatically become conditional error bounds
after the policy's observations.

One simple safe interface uses **one fixed nonnegative weight vector lambda**
chosen before this instance, with sum lambda_i*epsilon_i<=alpha. At any receipt
h, accept a proposed action only after checking that every bad-premise pattern
compatible with h and breaking every available support for that action has
weight at least one. An exact hard proof also suffices. Then, pathwise,

```math
\{\text{accepted action is unacceptable}\}
 \subseteq\left\{\sum_i\lambda_i1_{E_i}\ge1\right\}.
```

Markov's inequality gives unconditional failure probability at most alpha.
The action, proof supports, stopping point and audit choices may all depend on
the same observations: they do not change that single dominating event.
This is a reusable risk certificate across a menu, not a separate confidence
claim for every selected action or for every receipt.

A fixed conclusion is a special case and should not be used to manufacture
an adaptive-selection problem: all globally valid supports for that same Q
constrain the same falsity event. The real selection issue appears when the
output conclusion/action changes, or when the premise universe itself is
selected without valid simultaneous calibration.

Counterexample to selecting lambda freely after seeing the instance: there are
n equally likely worlds, exactly premise i fails in world i, and action i is
acceptable iff P_i. Each action alone has error 1/n. An observation revealing
i followed by action i fails with probability one. The selected weight vector
e_i appears to cost only 1/n but is data-dependent. Exact receipts must still
be respected; this example intentionally shows the false marginal-to-selected
risk inference, not a sensible action policy. A common vector covering all
these singleton-action failures needs lambda_i>=1 and costs one.

## Costs and early disposition

Logical supports must actually be checked and bound to the current source.
Their discovery, proof checking, marginal calibration, separation of bad
patterns and storage all cost resources. Testing a proposed lambda requires
a minimum-weight hitting-set or SAT/optimization oracle in general. A proof
portfolio may tighten a bound yet cost more than auditing a premise directly.
An exact receipt can enlarge the certified action menu; it does not turn the
remaining marginal bounds into conditional ones.

The probability calculation is established reliability/PSAT machinery, and
proof-support disjunctions are standard probabilistic logic. The useful
possible adapter is the shared, paid, source-bound certificate for adaptively
chosen actions. No complete-cost advantage or priority claim is established.
Defer a large implementation until a workload makes this distinction useful.
