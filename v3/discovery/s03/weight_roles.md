# Three weight roles and a contextual selection boundary

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

The value service uses several kinds of weights. Equal-looking arithmetic does
not make their semantics interchangeable.

1. **Policy mixture Q:** a deployment lottery chooses a program independently
   of the new context under evaluation. Its mean utility is sum Q_p*mu_p. The
   common PAC-Bayes event covers data-selected Q over its specified family.
2. **Model credence W:** weights average fallible predictions of utilities and
   observations. The optimal action under the pooled model maximizes the pooled
   action value. W does not certify model correctness, and its actions need not
   equal a lottery over each model's favorite action.
3. **Value-query coefficients w:** signed linear coefficients may encode changed
   prices or comparisons. An auxiliary nonnegative Q may certify that query,
   but the consumer's signed weights need not denote a probability measure.

For a small distinction, give model A utilities (1,0.9), model B utilities
(0,0.9), and credence W=(1/2,1/2). The pooled decision selects action 1 with
value 0.9. Independently sampling a model and executing its favorite action
chooses actions 0 and 1 equally often; its value under W is only 0.7. Coupling
the sampled model to the unknown true model would instead give 0.95, but that
requires information absent from the stated lottery. This one-step example
does not reject exploratory model sampling as a sequential learning strategy.

The same distinction constrains retained-model claims. If all models share
the same observation law and only their utility coefficients differ, fixed
credence averages those coefficients before ordinary planning. Keeping separate
models has no extra expressive power for that fixed expected-utility query.
It may still help with changed weights, diagnostics, model learning, or robust
criteria; those uses require their own information and cost account.

## Context-dependent choices must be programs themselves

Let contexts be a fair bit. Policy p0 has utilities (1,0), and p1 has utilities
(0,1). Each has population mean 1/2. A context-aware gate that selects p1 on
context 0 and p0 on context 1 gets mean zero, despite each constituent's mean
being 1/2. Therefore an unconditional mixture certificate cannot be applied by
plugging a new context-dependent Q(x) into the old population-mean formula.

The repair is constructive: include the entire gating rule as a fixed program
in the source family, charge its code and evaluation, and bound its own mean.
Alternatively use separately justified conditional sources. The [open-family
construction](open_family.md) can cover a newly proposed gate if its prospective
language/prior already covers that code. It cannot make a mutable, unrecorded
selection rule part of an old certified utility function for free.

This keeps usefulness estimates for fallible models, actual deployed policies,
and mathematical forecast uncertainty distinct. A reported PAC-Bayes posterior
is not automatically a credence distribution over counterfactual semantics.
