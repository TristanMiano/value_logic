# Compact support certificates for changed value queries

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; same-model construction.

The common event in [S12](policy_bank.md) supports [weighted queries](bank_transport.md).
The first exact-log implementation produced large rational denominators. Keep
that implementation and exposure unchanged. [bank_compact.py](bank_compact.py)
rounds each already rigorous log upper endpoint upward to a dyadic with 40
fraction bits. Thus each log bound grows by less than 2^-40. The KL upper bound
grows by at most 2^-40 because Q sums to one. The final lower certificate loses
at most 2*2^-40/(lambda*t); clipping at zero cannot increase that loss.
This bounds rounding relative to the old series certificate, not relative to
the exact logarithm. The old series remainder remains included.

For a weighted query, an ordinary numerical water-filling search supplies B,Q.
The independent exact algebraic check evaluates

    B*L(Q) + sum_theta min(w_theta-B*Q_theta,0).

At the convex optimum, let eta=lambda*t, a=P*exp(lambda*S), and
C=exp(lambda^2*t/8)/alpha. With multiplier nu, set
Q_theta=a_theta*exp(-eta*mu_theta)/C and B=nu*eta*C. Interior coordinates obey
B*Q=w. At a lower-clipped coordinate B*Q<=w; at an upper-clipped coordinate
B*Q>=w. These complementary conditions explain the min correction. The advice
uses floating exponentials and bisection; its posterior and B are rounded to
rationals before checking. Neither an optimality claim nor a floating residual
is needed for the final lower bound. A trivial box and positive-part query are
also tried. Signed queries are allowed; their lower bounds can be negative.

[support01.json](support01.json) reuses all ten explicitly exposed bank stages.
Every rounded certificate obeyed the stated loss bound. One hundred generated
weighted queries had numerical primal/certified-dual differences no larger
than 4.201e-7. Those primal diagnostics are from the same water-filling advice,
not independent optimization or statistical confirmation. All arithmetic and
advice took 117.274 ms in this small run; this excludes source acquisition.

In the asymmetric supplied example S=(128,0), t=128, lambda=1/2, alpha=1/20,
P=(1/2,1/2), weights (1,1), the certified lower bound is about 0.879868;
the direct uniform-posterior alternative is about 0.7814. This improvement is
ordinary box-constrained support optimization, not new statistical information.
The records include all inputs, source hashes, command runtime and exact values.
The construction still needs an actual priced acquisition application.
