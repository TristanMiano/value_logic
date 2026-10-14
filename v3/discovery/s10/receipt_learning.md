# Learn score tails from already purchased information

Codex (GPT-6), DEVELOPMENT, 2026-10-14.

The known-uniform scalar compiler fails on endpoint costs. A reserve caps the
physical loss but does not identify a good policy. Use actual first observations
already bought by the service to learn conservative score laws, without a
compulsory extra pilot stream. This is ordinary on-policy calibration and
confidence-based policy selection, extending the prior S31 comparisons.

For a fixed initial action, coarse scores0,1,2 depend on one latent cost and its
type (a_i in {1,2}, true/false query). Keep four separate type histograms. Pool
only observations of the same type. Assume latent costs are independent across
coordinates and requests, stationary, and share a law within each type.

The decision to observe a previously unobserved coordinate depends only on past
requests and other already observed independent coordinates. Hence its first
observation has the declared type law even when a fallback is selected
adaptively. **Count each coordinate/request once.** A later full-bundle receipt
can repeat an earlier observation after that value caused failure; counting
the duplicate would overweight failure values and destroy this argument.
Correlated coordinates or changing laws invalidate the following confidence
claim. Source-feasibility certificates and the physical reserve do not depend
on that claim and remain separately checkable.

Let d=4 types, delta=1/100 and sample count n>=1 for a type. For each tail
p_r=Pr(score>=r),r=1,2, assign failure probability alpha_n=delta/(4*d*n^2).
The union over all types, tails and positive n is below delta because
2d*sum_n alpha_n=delta*pi^2/12<delta. One-sided Hoeffding gives lower tail bound
empirical_tail-radius with radius squared at least log(1/alpha_n)/(2n).

Use only integer arithmetic for a conservative grid denominator G=1000.
Choose integer b with2^b>=4*d*n^2/delta, and the smallest integer r such that

```math
20n r^2\ge 7b G^2.
```

Then2n(r/G)^2>=0.7b>b log2, so the Hoeffding failure is <=2^{-b}<=alpha_n.
This uses the elementary numerical inequality log2<0.7, not a floating-point
logarithm in the executable confidence check. Let L_1,L_2 be empirical tail
frequencies rounded down to the grid minus r/G, clamped at0, and lower L_2
further if needed to ensure L_2<=L_1. The resulting score probabilities
(1-L_1,L_1-L_2,L_2) are stochastically dominated by the actual type distribution
on the simultaneous event.

Independence gives a coordinatewise quantile coupling. Every actual prefix
score stochastically dominates its conservative counterpart, so each survival
probability, and therefore the inherited positive-coefficient prefix invoice,
is at most the conservative prediction. Choose among a fee order and an
expected-score-per-fee order, every admissible cutoff, and immediate fallback.
Thus conditional expected physical fee<=C whenever the confidence statement is
valid. This is not an unconditional zero-risk guarantee: failure probability,
setup/learning work and any distribution violation remain outside it. An
optional physical reserve supplies its separate pathwise envelope.

Recompile at request counts0,1,2,4,...; the certificate survives between epochs
under the same stationary law. Pay histogram updates and every tested policy.
Compare with empirical tails without confidence padding, their ordinary
reserve wrapper, a correctly specified frozen oracle, exact threshold and
full fallback. A statistically valid lower bound can still be too conservative
or expensive to repay its acquisition/planning cost. This is an open empirical
question, not a promised improvement.
