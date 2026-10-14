# Reuse across distinct prior answers

Codex (GPT-6), DEVELOPMENT, 2026-10-14.

An exact-prior-state interval cache loses reuse after the first query when
observations have many possible values. A different certificate keys only the
set of observed latent costs, while retaining a rigorous neighborhood of their
values. This is ordinary Lipschitz/dominance certification, not a new oracle.

Fix a feasible m-copy action a and an observation pattern P. For two answer
vectors z,z' with the same P, both endpoints of contrast coordinate i shift by

```math
\Delta_i=1_{T_i\in P}(T'_i-T_i)-1_{F_i\in P}(F'_i-F_i).
```

For every feasible competitor v, its pairwise regret therefore changes by
sum_i(a_i-m v_i)Delta_i. Maximizing each term over the relaxed bit v_i in {0,1}
gives the certified bound

```math
R_a(z')\le R_a(z)+\sum_i
\max\{a_i\Delta_i,(a_i-m)\Delta_i\}.
```

If a source-complete check at z gave upper bound U<=tau, retain z, U and a.
Any future z' with the same pattern and the displayed variation <=tau-U may
reuse the action. The test costs O(features), independent of the number of
source models. Combining true/false shifts before taking the maximum preserves
their cancellation. The formula is continuous and distribution-free. With pure
coordinates a_i=0 or m it includes whole favorable monotone directions even
when U=tau; mixed coordinates charge an asymmetric absolute deviation.

Only the anchor upper bound needs source-complete verification. Original-source
feasibility of a remains necessary. A counterfeit action vector or pattern is
unsound. Changing a query tariff does not invalidate correctness, but changes
economic comparisons; changing the observation interval model does invalidate
the certificate unless the shift identity still holds.

Negative reuse can be even simpler: store two feasible witness models and test
their pair-floor expression at the new box, keyed by source. If it exceeds tau,
no source-feasible m-copy action can close there. This requires no exact prior
answers, no complete model enumeration and no precomputed full policy. It does
not justify skipping future information or proclaiming the next query optimal.

Prospective comparison: bounded witness pool, exact source-diagram upper checks,
neighborhood reuse, and pair-floor skips; ordinary mirrored controller; an
otherwise identical controller without cross-request reuse; a fixed-action
threshold controller; and full relevant audit. Charge source compilation,
proposal pool construction, every rejected lookup, retention and output checks.
Keep bounded source admission failures visible. This direction targets reuse
on high-resolution observations, not superiority over ordinary robust methods.
