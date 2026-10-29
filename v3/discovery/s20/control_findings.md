# Simplifying controls and sharpness: development results

Codex (GPT-6), October 28, 2026. DEVELOPMENT, same-model. The first frozen
execution passed; no retry or exception occurred. See the [plan](control_probe_plan.md),
[freeze](control_freeze.json), [inputs](control_inputs.json), complete
[certificates and witnesses](control_records.jsonl), and [summary](control_result.json).

All six offset-only cases agreed exactly with the O(n*k) analytic control:
four yielded one interval and two were inconsistent. This supports the
implementation comparison; monotonicity and the constructive proof in
simplifying_controls.md establish the general special-case statement.

Adding the third uncalibrated affine piece to the noisy two-piece example
gave the entire interval [197/200,3/2] for the maximum readout (the certificate
uses its negation). Thus the old gap and reciprocal bound disappear under
that explicit model revision. The analytic correction recorded before this
run was confirmed by the rational source/dual certificates.

The full-dimensional noisy two-block constructions returned exactly 2,3,6,10
and 20 nondegenerate interval components for k=2,3,4,5,6. Every adjacent gap
exceeded 7/8, as the proof predicted. In all 12 cases combined, 138 endpoint
or midpoint source witnesses satisfied the original model and all receipts.
These are finite checks of the sharpness construction; the antichain proof
supplies the universal upper bound. The decreasing tolerance is explicit
and no fixed-noise asymptotic claim is made.

The results strengthen the boundaries of the proposed contribution in both
directions: there are cheap conventional cases where keeping a gap-aware
representation is unnecessary, and there are nondegenerate cases where a
single interval necessarily loses attainable-set information. Neither fact
is an empirical speedup or evidence that conventional exact methods fail.
