# History-conditional interpretation of learned prefix bounds

Codex (GPT-6), 2026-10-14. Additive clarification of the executed learning design.

The phrase "conditional expected physical fee <= C whenever the confidence
statement is valid" in receipt_learning.md must mean **at each past history
whose currently stored bounds are below the true stationary type tails**.
It must not mean expectation conditional on the event that all future confidence
intervals also succeed. Conditioning on that future event can change the law of
the very responses whose cost is being predicted.

Fix a request boundary and its complete past history H. The stored policy and
all its conservative score laws are then fixed. If the stored lower tails at H
are valid, fresh latent variables are independent with their stationary laws,
so the coupling proves E[A | H] <= C. This is the useful predictable guarantee.
The probability of encountering any invalid stored bound is at most delta under
the stated assumptions and the first-observation accounting rule. Every realized
request fee remains at most 2C, whether its probability model is correct or not.
For a fixed source and fixed C, splitting by the past-measurable good-history
event therefore yields E[A_t] <= (1+delta)C. Linearity gives
E[sum_{t=1}^T A_t] <= (1+delta)TC. This is an expectation bound, not a pathwise
bound or a learning-regret rate. The separate reserve supplies a pathwise
physical-fee envelope, with its explicit initial allowance.

The executed switch test has 36 confidence-tail violations, all in the changed
law regime; none are reported under the stationary independent law assumptions.
This is a diagnostic finite result, not an empirical calibration proof. Marginal
coverage under correlated costs cannot rescue the product convolution: joint
prefix survival probabilities require independence (or a checked conditional
model). The tests use synthetic distributions; no empirical cost law is inferred
for an application. Computation and confidence maintenance remain paid, and their
cost can outweigh acquisition savings.
