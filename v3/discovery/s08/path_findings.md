# Compact path planning: finite reconstruction and remaining duties

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The [interval derivation](path_audits.md) was implemented and executed with
`python v3/discovery/s08/path_audits.py v3/discovery/s08/path01`.
The [frozen implementation](path01/impl.py), [design](path01/design.json) and
[results](path01/results.json) preserve the whole comparison.

All 24 small cases (n=2..7) matched the independent full three-value
query-history Bellman solver, across 86,352 Bellman states. Executing the
compiled policy on all 13,104 source realizations produced a source-uniform
exact local action and the analytically predicted mean invoice in every
case. Another 1,008 probability-box endpoint evaluations verified that a
policy planned at lower extreme probabilities stayed below its original
expected-fee bound. These are conditional policy calculations: **zero new
physical source audits**.

Larger n=16/32/64 planners completed in approximately 0.004/0.028/0.223 seconds
in this one execution. Exact rational table values and operation invoices are
saved. These timings concern table construction only, with supplied source
parameters, and establish no speed claim over an optimized ordinary interval
implementation. Such an implementation can use exactly this recurrence.

The next substantive duties are (1) a history-dependent adversary check of the
conditional lower-probability guarantee, (2) a paid source/action service,
and (3) learning/planning economics rather than a comparison with an
exponentially explicit Bellman representation alone.

## Resolving the robust-proof qualification

The original derivation conservatively left an interchange duty open for
history-dependent laws. The exact minimax conclusion does **not** require
proving optimality of the forced-first interchange under every such law.
First prove the upper bound for the explicitly chosen compiled policy by
induction, using its table inequalities and the conditional probability
bounds after every history. For the lower bound, the uncertainty class
contains the independent product law with parameters exactly l. Under that
law the already proved independent-source optimum is V. No policy can have
worst-law expected cost below its expected cost at that member's optimum.
These two separate bounds establish equality for the broad class.

The upper-bound induction still needs the state to record the complete
remaining duty. After an extreme result, the two adjacent components are
ordinary; after a middle result, the corresponding endpoints are mandatory.
Their table bound sums remain valid after any prior component history because
the conditional probability premise is assumed for **every** permitted
history. Independence is not used in this upper induction. More extreme
probability helps because forced-component table bounds dominate ordinary
ones. The independent law is used only for attainment and the lower bound.

The statement is about conditional lower bounds, not marginal calibration.
The latter does not constrain an adaptive adversary enough. A separate
counterexample or finite adversary check will make this boundary reviewable.
