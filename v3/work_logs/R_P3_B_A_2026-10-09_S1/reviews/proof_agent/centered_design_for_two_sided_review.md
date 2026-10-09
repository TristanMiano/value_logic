# Public-centering extension to the observable certificate

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
R-P3-B-A, prospective D/X derivation and post-run diagnostic plan.
No policy, label, service or random-seed execution is planned.

The first observable diagnostic remains intact. Its two estimates unnecessarily
sample a component of Brier loss already known from the public forecast.
For binary y and emitted q define v=q(1-q) and r=(1-2q)(y-1/2).
Then d=1/2+r and g=d-v. Thus, pathwise across the whole episode,

Brier - unbought conditional mean = sum_selected d - sum_all v.

Every quantity on the right is already public after paid receipts. The two
unknown performance targets therefore have exactly the same residual error.
An interval for either one can transfer to the other without a second union
bound. This is not a probability-of-truth identification theorem.

Center the purchased-label estimator:
U_c=(T-m)/2 + sum_blocks (1/pi_J-1) r_J.
A_c=T/2 - sum_all v + sum_blocks r_J/pi_J.
Then V-U_c=F-A_c=sum_blocks [sum_t r_t-r_J/pi_J].
The increments have conditional mean zero. Define the public predictable
range bound C_k=max_in_block |1-2q_t|/pi_t, bounded by S=B or2B.
The conditional range width of the increment is at most C_k, because each
r_t/pi_t belongs to [-C_k/2,C_k/2].

A random realized sum Q=sum C_k^2 must NOT be inserted into the usual
fixed-variance optimized Hoeffding radius. Instead choose lambda before
reading labels, use the conditional exponential moment, and iterate:
E exp(lambda D - lambda^2 Q/8)<=1.
At fixed m this gives D<=lambda Q/8+log(1/delta)/lambda with probability
at least1-delta. A bounded first-crossing argument also gives the same
inequality simultaneously at all block prefixes for that one fixed lambda.

An exact finite choice is R=S*ceil_sqrt(2m), lambda=8/R, delta=1/40.
Since log40<4, radius Q/R+R/2 suffices and is <=R because Q<=mS^2<=R^2/2.
Use the same sampling event for V and F. Combine it with an independent
terminal-action deviation at delta_a=1/40 to obtain a joint at-least95%
upper certificate for terminal errors AND immutable Brier at the fixed end.
The action step remains fixed-end only; do not claim the whole joint terminal
bound is anytime. Do not optimize lambda retrospectively without correction.

Public deterministic bounds can clip estimates:
V<=sum_unbought max(q,1-q),
F<=sum_all max(q^2,(1-q)^2).
At q=1/2 on every issued round these are exact equalities for their respective
targets, so no sampling uncertainty is necessary. For general q, use clipped
upper bounds only; negative numerical upper bounds may be clipped to zero
without invalidating the probability statement. Realized terminal loss has
only the deterministic T-m cap, not the conditional-mean cap.

After the first public-only diagnostic closes, add a SECOND independently
recorded analysis over the same public archive members for all23 existing
arms. Keep exact fractions for centered estimates, Q, radii and deterministic
caps, the common deviation identity, and all results. Use private scores only
in a subsequent separate comparison stage. This is offline mathematics and
analysis, not a deployed calculator or added free learner computation. Fixed
MT seeds demonstrate formula reconstruction, not frequentist coverage.
