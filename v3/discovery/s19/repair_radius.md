# A quantitative consistency radius for fallible scalar receipts

Codex (GPT-6), October26,2026. DEVELOPMENT derivation; a small adapter to
ordinary bottleneck partitioning, not a separate novelty claim.

Assume the same independent compact rational source polytopes as AR1.
Receipt j admits[a_j,b_j]. Fix declared positive scales s_j and let an
error budget delta enlarge it to[a_j-s_j*delta,b_j+s_j*delta]. The scales
must be supplied; they are neither learned error rates nor probabilities.
Define the least common enlargement admitting a source as delta_star.

For each block i and receipt subset T solve one local LP:

    d_i(T)=min delta
    subject to delta>=0, x_i in B_i,
      g_ji(x_i)>=a_j-s_j*delta for every j,
      g_ji(x_i)<=b_j+s_j*delta for j in T.

All these LPs attain finite optima when the B_i are nonempty and scales
are positive. The full radius is exactly

    delta_star = min_(partition T_1,...,T_n of K) max_i d_i(T_i).

Every globally consistent relaxed source supplies a witness partition and
local values no larger than its budget. Conversely, at a partition's
maximum local value, each local optimizer remains feasible because all
constraints expand monotonically. Their independent product is a common
source at that budget. A min-max subset recurrence computes the partition
after n*2^k local LPs; its primitive is conventional subset convolution.

One can include a proposed new reported band as another receipt, or give
it a different declared scale. A positive optimum measures how far the
entire collection lies from joint consistency under this specific metric.
It does not identify the mistaken report, warrant the source regions,
or justify which assertion to revise. Weighted withdrawal in
receipt_withdrawals.md answers a different, discrete revision question.

Rational primal witnesses and ordinary LP duals can certify local radii;
the subset recurrence can be recomputed. No new implementation or checker
coverage is claimed here. The strong comparison is direct min-max residual
fitting through mixed-integer optimization. PARK standalone novelty: this
is a useful interpretation and a clean boundary for the larger inference
construction, not evidence of a new general model-repair principle.
