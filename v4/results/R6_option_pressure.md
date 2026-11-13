# R6.9 More useful options create pressure when access and goal weights support it

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** reconstruction of established retargeting arguments, an elementary
weighted extension and an exact finite-menu latency/cost calculation.

Preserving genuinely usable options can help many different goals. How broad
that pressure is depends on which goals occur, how the options are reached,
and what reaching them costs. This result distinguishes three quantities:
the proportion of goals that prefer an option, its expected benefit, and the
behavior a learner eventually adopts. They answer different W6 questions.

## 1. The strongest existing power results use explicit comparisons

[Turner et al., *Optimal Policies Tend To Seek Power*, v10](https://arxiv.org/abs/1912.01683v10)
study attainable discounted outcome distributions and a permutation-based
comparison of reward distributions. Their “most” relation counts elements
of permutation orbits; it is not an estimate of the frequency of motivations
among actual agents. Symmetries copying one attainable family into another
give an injection from unfavorable cases into favorable ones. Extra exposed
choices can make the comparison strict under the stated reward assumptions.

For an actual reward law invariant under the relevant permutations, the
orbit comparison can imply a probability comparison under that law. It is
therefore also too weak a reading to dismiss the theorem as saying nothing
about probabilities. The transfer requires the stated symmetry or an explicit
replacement controlling probability weights.

[Turner and Tadepalli (2022)](https://arxiv.org/abs/2206.13477)
generalize the counting mechanism to parametrically retargetable decision
makers, including bounded procedures. Their multiple disjoint injections
produce a quantitative favorable/unfavorable ratio. The result is not confined
to ideal optimal planners. Neither theorem alone is a temporal learning result
for an arbitrary initially uncommitted agent.

The source-specific proof reconstruction and one support-restriction
clarification are in the [source notes](../notebook/P4-R6-C001/sources.md).
The calculations below expose the corresponding weight and access conditions
in a deliberately simpler setting.

## 2. Weighted retargeting gives a declared prevalence bound

Let a finite parameter set carry probability mass mu. Let A be unfavorable
parameters and B favorable parameters; any remaining mass consists of ties
or cases outside the comparison. Suppose there are injections f_j:A->B with
pairwise disjoint images, and numbers lambda_j>=0 such that

```math
\mu(f_j(x))\ge\lambda_j\mu(x)\quad\hbox{for all }x\in A.
```

**Lemma 1 (weighted retargeting).** Put Lambda=sum_j lambda_j. Then

```math
\mu(B)\ge\Lambda\mu(A),\qquad
\frac{\mu(B)}{\mu(A)+\mu(B)}\ge\frac{\Lambda}{1+\Lambda}
                                                               \tag{O.1}
```

when the conditional denominator is nonzero.

*Proof.* Sum each pointwise inequality over A. Injectivity identifies each
image mass, and disjointness lets the image masses add inside B. Rearranging
the first inequality gives the second. QED.

Uniform mass gives lambda_j=1 and the established counting ratio. For
mu(x) proportional to exp(f(x)), a bound f(f_j(x))-f(x)>=-D_j gives
lambda_j=exp(-D_j). Thus enough retargeting copies can outweigh a bounded
prior bias; arbitrarily severe bias need not be overcome. With a common D,
the sufficient conditional-majority condition is n*exp(-D)>1. No distribution
over real agents is inferred without evidence for those mass comparisons.

This elementary weighted version is a transparent bookkeeping extension,
not a priority claim or a replacement for the more general source results.

## 3. An exact cost and latency boundary

An agent chooses between one immediately available terminal outcome and a
menu of k different outcomes reached after a delay. A goal specifies rewards
R_0,...,R_k drawn independently Uniform[0,1]. The goal is known when the menu
choice is made. The immediate value is A=R_0. The delayed menu's value is

```math
B=\gamma\max_{1\le j\le k}R_j-c,
\qquad 0<\gamma\le1,\quad c\ge0.                       \tag{O.2}
```

Here gamma is the entire delay discount and c is the acquisition cost in the
same utility units. The immediate outcome is not also available after choosing
the delayed route. If it were available with no cost or delay, the nested-set
guarantee of [R6.7](R6_capability_geometry.md) would apply instead.

**Proposition 2 (goal frequency with priced access).** For 0<=c<gamma,

```math
\Pr(B>A)=\frac{\gamma k}{k+1}-c
                  +\frac{c^{k+1}}{(k+1)\gamma^k}.       \tag{O.3}
```

For c>=gamma this probability is zero. Also
E[B]-E[A]=gamma*k/(k+1)-c-1/2.

*Proof.* M=max_j R_j has distribution P(M<=m)=m^k on [0,1]. Conditional
on M=m, the probability of beating the independent uniform R_0 is
(gamma*m-c)_+, since gamma*m-c<=1. Integrate this against k*m^(k-1) on
[c/gamma,1] for (O.3). The mean uses E[M]=k/(k+1). QED.

With zero cost, the k-option route is favored by a fraction gamma*k/(k+1)
of the declared goals. At gamma=1 this is k/(k+1). At gamma=0.4, even
arbitrarily many delayed options do not yield a majority. At gamma=0.6 and
k=3, the fraction is 0.45. Adding c=0.1 reduces it to about 0.350116.

This does not contradict the power theorems. The theorem's specified
attainable distributions, embeddings and discounts must be checked in the
new environment; merely counting outcomes does not preserve them. The
positive characterization is explicit: extra independently useful options
help enough when their discounted access value exceeds the relevant cost.

## 4. Goal frequency, expected value and learned persistence

The agent that commits *before* seeing the current goal compares expected
values, whereas (O.3) counts decisions after the goal is revealed. A learner
needs a feedback and regret analysis as in [R6.5](R6_payoff_judgment.md).
Frequent small benefits need not dominate rare large costs. For example,
a difference of +0.001 on 99% of goals and -1 on 1% gives a favorable-goal
fraction of 0.99 but negative mean -0.00901. Positive mean advantage, positive
majority, and positive cumulative log retention advantage are distinct.
[R6.4](R6_plastic_priorities.md) gives the corresponding retention calculation.

Likewise, separate action labels with identical consequences contribute no
extra capability. If all R_j equal R_0 and gamma<=1,c>=0, the menu cannot
strictly improve the payoff. The constructive repair is genuine new attainable
outcomes, informative context-dependent choices, or reduced access cost—not
more names for the same option.

This frames self-preservation, intelligence and reproduction conditionally.
Continued operation can preserve future choices when its costs and effects
permit the alternatives to remain available. Better judgment can expand
successful contingencies when the agent can use it reliably. Reproduction
can extend goal pursuit if successors retain the relevant ability and purpose,
with resource and interaction effects included. These are useful sufficient
mechanisms, not a claim that every final goal values each named capability.
Their emergence without an initially encoded final objective additionally
requires a selection/revision mechanism such as the one explicitly modeled
in R6.4; that question is a focused bridge to W7.

The [checker](../notebook/P4-R6-C001/option_pressure.py) compares (O.3) with
independent finite-grid enumeration and checks the weighted-mass example.
Its finite cases supplement the proofs; they do not estimate natural-agent
prevalence or demonstrate a newly superior option-seeking algorithm.
