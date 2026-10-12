# S15: combining acquisition certificates across fallible models

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

The graph machinery is conditional on an observation law. Correlated bits can
invalidate a certificate obtained from independent fair marginals, as shown in
[prior_robustness.md](prior_robustness.md). A portfolio of alternative models is
one way to keep that law revisable. It introduces a new information channel:
observations can identify which model applies. Ignoring this channel is unsafe.

Let M have a warranted prior W, with model-specific joint laws for the same
actions, observations and charged queries. Let c_aM be the no-observation mean
of action a, c*_M=max_a c_aM, and suppose Gamma_M upper-bounds every feasible
adaptive policy's gain over c*_M conditional on M. A policy unaware of M is
also an allowed policy in each conditional problem. Therefore

    E[value of any policy - query costs]
        <= sum_M W_M (c*_M + Gamma_M).

Relative to the actual available incumbent c*=max_a sum_M W_M c_aM, the upper
bound is

    sum_M W_M Gamma_M + (sum_M W_M c*_M - c*).

The final nonnegative term is the value of revealing M before choosing the
initial action. If the same action maximizes every model, it vanishes. Otherwise
zero within-model acquisition bounds do not certify zero acquisition value.
The construction requires a warranted mixture; weights denoting a deployment
lottery over policies are a different type, as [weight_roles.md](weight_roles.md)
explains. The prior need not assert a model is final, but conditional guarantees
depend on the actual law belonging to the proposed mixture or uncertainty set.

## Minimal obstruction to naive averaging

Two models assign a bit x deterministically +1 or -1, with equal prior weights.
Actions predict + or -, receiving one for a correct prediction and zero
otherwise. Each conditional model already knows its optimal action, so its
acquisition value and Gamma_M are zero. The uninformed mixture's incumbent
value is 1/2. Buying x for cost q<1/2 yields 1-q, a gain 1/2-q. The missing
baseline term is exactly 1/2. Averaging the two zero certificates would have
falsely ruled out this profitable observation.

## Constructive refinements

When the finite family has a common maximizing action, independently checked
no-acquisition certificates immediately give a mixture no-acquisition result.
More generally partition the models into groups with a common good action and
retain group-identification value explicitly. This is a conditional-expectation
decomposition, not a free observation of the model. A future sequential bound
can evaluate a cheap discriminating observation first, update W using the paid
likelihood model, then use the conditional certificates in each child. Every
branch still needs a valid upper bound; a selected promising branch alone gives
only a lower bound on the achievable policy value.

For an uncertainty set of possible W, maximize the displayed bound minus the
fixed incumbent's mixed mean over that set. With a fixed incumbent this is
linear in W and becomes ordinary robust linear optimization. Choosing a new
incumbent after seeing W changes the quantifiers and must be represented as an
available-information action. A cheap conservative bound takes each model's
regret against the same named incumbent. This distinction connects model
revision, counterfactual comparison, value refinement and probabilistic content
without inventing a belief update from a scalar loss alone.

Next useful construction: quantify observations that distinguish competing
models while leaving their decision-relevant within-model certificates intact.
Compare with an equally informed Bayesian/robust decision process. Model
construction, likelihood evaluation and representation expansion remain paid.
