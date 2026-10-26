# Value-equivalence reuse needs the right affine anchor

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; cheap boundary screen.
This does not replace the inherited S11L/s11 potential-compression results.

A Bellman update with unknown reward is affine in its continuation value:

    T v = r + gamma P v.

If two models agree on T v_i for supplied functions v_i, they automatically
agree on every affine combination sum alpha_i v_i with sum alpha_i=1.
They need not agree on every linear combination. For example, take two states,
one action, gamma=1/2 and v=(0,1). Model1 has every transition go to state1
and reward1/2 at both states. Model2 has every transition go to state2 and
reward0. Both give Tv=(1/2,1/2). At2v they give(1/2,1/2) and(1,1), and at0
they give different rewards. All transitions are valid stochastic rows.

The repair is elementary: retain the zero-function update (the reward), assume
the same known reward in every model, or restrict the reuse to the affine
hull of the original functions. Once rewards match, continuation differences
have linear reuse. With an explicit unknown-reward anchor v0, the sufficient
representation is one affine offset and the span of v_i-v0. A constant
continuation also identifies reward because P1=1 in this stochastic setting.

This is a hypothesis check for our own proposed interface. The2020 value-
equivalence paper's displayed span proposition prompted it, but this note does
not claim a new literature correction: the full supplementary proof, possible
shared-reward conventions and later revisions have not been compared here.
The inherited s11 construction supplies immediate charges and operators, so
this example does not invalidate its canonical policy-difference space.

Counterfactual reward changes are therefore a separate information duty.
Agreement on one value calculation can hide a reward/transition cancellation;
using the same scalar receipt at a changed reward or continuation may break
it. This is an affine-identification obstruction, not evidence of superiority
over ordinary value-aware models or linear algebra.
