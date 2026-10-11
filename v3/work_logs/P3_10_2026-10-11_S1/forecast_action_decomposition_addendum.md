# Fixed-mass rounding clarification

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.
This additive note preserves the pre-data derivation and its original hash
`20f3369b402fe471953f210bf409f6d2ef51a721166d2f61f01c8bf1e274b55b`.

The symbol `w` in [the derivation](forecast_action_decomposition.md) uses the
**already integer-rounded fixed-mass learned weights** saved before the block.
“Unrounded reweighting” means only “before the final forecast projection from
`w` to the dyadic issued base `p`.” The bound `5/196608` controls that final
projection's Brier contribution. It does not bound accumulated weight-update
rounding, prove equivalence to a hypothetical real-weight learner, or extend
any regret theorem beyond its original numerical hypotheses.

The exact lower bound corresponding to a measured A2 effect of `1/100` is
`49027/4915200` for the pre-projection mixture advantage. The independent
mechanism observer confirmed the identities on all 126 complete numerical
paths and all 10,752 positions. The full source and result bindings remain in
`forecast_mechanism_observation_A1/results.json`; this note changes no result.

Both the independent broker and certificate reviewers identified this
qualification. It is an exposition clarification, not an execution defect,
replacement endpoint, or additional scientific sample.

## Pointwise signs and aggregate reversals

The sentence about different signs in the original derivation refers to
**aggregation across positions**. For a single binary label, the Brier loss
and the affine binary-error functional are both monotone in distance from that
label. Their changes therefore have the same sign pointwise. Averaging can
reverse the comparison because the Brier change weights those distances
quadratically while the affine functional weights them linearly.

For an exact two-position illustration, take labels `(0, 0)`, reference
forecasts `(1, 0)`, and changed forecasts `(3/4, 1/2)`, with equal weights.
The mean Brier improvement is `3/32`, whereas the mean binary-error-functional
improvement is `-1/8`. The reference-minus-changed forecast-variance term is
`-7/32`, so the decomposition is exactly `3/32 = -1/8 - (-7/32)`.
These are illustrative values, not extra experimental observations.

The independent certificate reviewer identified the missing aggregation
qualification. Its reconstruction confirms that the gate-transfer whole and
first-key slices exhibit an aggregate reversal, with all original endpoint
values and denominators preserved. The distinction does not change the
pointwise identity, the numerical observer, or any frozen score.
