# ND01 supplementary mechanism analysis plan

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-05.
Written after the registered preparation process started, before validation
exposure and before the principal inspected any new preparation outcome.
These supplementary analyses do not alter the frozen methods, selected
alignments, populations or criteria. All results remain development evidence.
No preparation or validation generator is called until the registered global
preparation and evaluation stages have completed.

## Questions to resolve from saved or hash-identical data

1. **Candidate coverage versus selection objective.** Reconstruct the same
   discovery logit quadratic from the already registered pair arrays and
   verify its saved hash. Score each saved bounded candidate pool on that
   objective, without validating or adopting any newly selected mask.
   Decompose a method's excess discovery logit MSE over the exhaustive
   minimum into its difference from the best candidate in its existing pool
   and the pool minimum's difference from the exhaustive value. This isolates
   selection/objective choice from actual proposal coverage for this finite
   objective. Preserve roundoff discrepancies rather than converting them
   into strict improvements.

2. **Error source and equal-target leakage.** On hash-identical validation
   pairs, check `total_logit_error=base_logit_error+contribution_residual_change`
   for the registered original, exhaustive binary and fractional methods.
   Save all mean-square components and the signed cross term by model, role
   and stratum. No new fit or validation-based method choice is performed.

3. **Mask organization and joint compatibility.** Record fractional counts,
   role-mask overlap, native contribution energy and the two-donor affine
   commutator coefficient `v*m0*m1`. If a derived joint donor panel is used,
   form it only from existing arrays and label it a secondary development
   construction, not another independent or frozen stratum.

4. **Activation geometry and the nullspace qualification.** Classify hidden
   ReLUs as always inactive, always active or variable on the declared input
   box using exact rational extrema of their stored binary64 affine
   coefficients. Check how this bounds the span of hidden differences.
   If a globally inactive coordinate exists, construct the algebraic
   projector that matches a fractional mask's output using that null direction
   and verify it on the existing validation arrays. This diagnoses why
   per-role output correspondence can fail to identify the native mechanism;
   it is not a new independently learned alignment or new support claim.

The protected remainder should prioritize these discriminating checks over
more random search, additional networks, new validation draws, or post-outcome
threshold changes. If the 90-minute boundary leaves an optional analysis
unfinished, record its exact missing evidence and a sensible further chunk.
