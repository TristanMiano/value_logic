# A closer ordinary statistical baseline

Codex (GPT-6), October23,2026. DEVELOPMENT; imported theorem, explicit adapter.

Garatti and Campi, *Non-convex scenario optimization*, Theorem4, applies to
the decision M_N=span(z_1,...,z_N), with a new point appropriate exactly
when it belongs to that span. Permuting points leaves the span unchanged;
adding only contained points leaves it unchanged; adding any uncontained
point changes it. Thus all three parts of their Property1 hold. Irreducible
support lists are bases, and their minimum size is J_N, with no unique-basis
or nondegeneracy assumption. The source is linked in literature.md. Its
theorem is imported, not independently reconstructed here.

For confidence1-beta, its bound epsilon_N(k)=1-t(k) is determined by

    (beta/N) sum_{m=k}^{N-1} C(m,k) t^(m-k) = C(N,k)t^(N-k),

with the unique t in(0,1), and epsilon_N(N)=1. Monotonicity in k permits
substituting a truthful upper bound k_bar. The same latent-span containment
argument covers adaptive truthful refinements of the fixed cohort. This
is a closer ordinary alternative than only the earlier stable-compression
bound. It is not automatically time-uniform in N.

At N200, beta0.05, k_bar1, exact integer endpoint checks place this bound
in(0.033689,0.033690]. The new elementary binomial allocation in
sequential_rank.md gives(0.033742,0.033743], so the established scenario
bound is already SLIGHTLY BETTER. The reduction from0.06236148 to0.033743
is real only against the named stable-compression bound; it is not a new
best-in-class statistical improvement. At k0 our binomial allocation is
better than this particular scenario envelope, while the scenario envelope
is better at the other ten selected positive ranks. No minimization of
separately95%-valid envelopes is permitted without a simultaneous argument
or a prospective choice: choosing the smaller after seeing k is a new rule.

The useful candidate left by this comparison is the composition of partial
evidence, a computable hidden-complexity certificate, adaptive stopping,
and an explicit changing inference scope. Ordinary implementations of that
same composition tie. Whether the composition contributes moderate novelty
needs a closer incomplete-data/scenario comparison and a paid-use case.

## Small screen and retained failure

scenario_compare_v2.py uses exact integer polynomial signs on a10^-6 grid
at eleven ranks. Its JSON records endpoints, source hash and observed runtime.
It also checks the learned_scope.md acceptance and budget-expansion example.
The initial scenario_compare.py added an incorrect assertion that N200 was
the earliest rank-three acceptance; exact arithmetic rejected it. N199 is
already sufficient. The manuscript had asserted only that N200 suffices,
which remains true. The failed source/stdout/stderr are retained; this is a
mathematical assertion error, not evidence of a hardware failure.
