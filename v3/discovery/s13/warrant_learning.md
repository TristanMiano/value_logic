# Learning every permission's common warrant can be much harder than learning a useful action

Codex (GPT-6), DEVELOPMENT, October20,2026. An elementary counterexample and
ordinary finite-class uniform bound. This is a substantive limit on using the
new maximal-warrant construction as a generic learning recipe.

## A two-coordinate example

Let the true latent thresholds be (theta1,theta2)=(t,t), with t uniform on
{1,...,K}. Actions a1,a2 lie in{0,...,K}, and the goal is y1=>y2 under the
local threshold-response law. Draw N independent complete training examples.
Take the empirical source F_N to be exactly their distinct threshold pairs,
and compile every empirically safe action A(F_N). Let W_N be their common
maximal warrant, as in permission_closure.md.

On the true diagonal, W_N contains exactly the observed values of t. Every
observed value is covered because F_N is contained in W_N. For any unobserved
t, set a1=t and a2=u, where u is the largest observed value at most t, or0
if there is none. Every observed value at most t is at most u, so this action
is empirically safe. At the actual unobserved t it has y1=1,y2=0 and fails.

Consequently

```math
P(\Theta\notin W_N\mid F_N)
 =1-\frac{\#\{\text{distinct observed values}\}}K
 \ \ge\ 1-\frac NK.
```

The expectation over training samples is exactly (1-1/K)^N. With a continuous
uniform t in(0,1), finite observed values have measure zero: the empirical
common warrant has failure probability one for every finite N. This is not
a failure of the algebra; it is a failure of an unwarranted learning claim.

## The quantifiers make the difference

For a *fixed action* (a1,a2), failure is just the interval a2<t<=a1. There are
at most(K+1)^2 actions. The probability that an action of true risk greater
than epsilon has no observed failure is at most exp(-N*epsilon). A union bound
therefore gives

```math
P\!\left(\exists a\in A(F_N):P(G_a^c)>\epsilon\right)
 \le (K+1)^2e^{-N\epsilon}.
```

For K=1,000,000,N=4,000,epsilon=.01 this upper bound is below4.25e-6, while
the common warrant still fails on at least99.6% of new cases. Thus all retained
actions can individually have small population risk even though their union
of possible failures covers nearly the whole population. No contradiction:
"every action has small risk" differs from "with high probability no retained
action fails on this same world."

A data-selected action, or repricing independent of the new latent world,
can use the former guarantee. An action selected using information correlated
with that world needs an appropriate policy/context guarantee; individual
unconditional risks are insufficient. The common warrant supplies that stronger
same-world adaptive protection, but may demand much more evidence.

## What should be developed instead

Do not require a common all-menu warrant when the deployment only needs a
fixed action policy's population risk. Direct policy calibration and ordinary
finite-class/scenario methods are mandatory strong controls. Alternatively,
restrict the action menu, impose a supplied response margin or test a proposed
structured model on held-out cases. Each changes the actual evidence duty.

For example, a supplied diagonal model for all t has common warrant
theta2<=theta1 and correctly licenses all a2>=a1. The empirical finite support
does not infer that continuous structure by itself. Held-out calibration can
test a fixed proposed warrant, but selecting it after the same labels requires
selection control. This note proposes no new sample-compression or VC theorem,
and it does not charge complete threshold labels as free observations.
