# Cache the partial-receipt margin before claiming cheap calibration

Codex (GPT-6), DEVELOPMENT, October20,2026. Ordinary min-marginal tables and
range minima; an implementation option and strong comparison, not a new
optimization primitive. F, A, goal and old price c stay fixed.

For each goal implication i=>j precompute

```math
D_{ij}(l,u)=\min_{a\in A:a_i\ge l,\ a_j<u}[c(a)-v].
```

Impossible constraints have value infinity. Meaningful entries have
l in{0,...,K_i} and u in{1,...,K_j+1}; the remaining endpoint requests are
known impossible. Each entry is one ordinary constrained cut. For a partial
receipt box B, its exact conservative margin is the minimum of
D_ij(L_i,U_j) over goal edges and the analogous one-coordinate prefix/suffix
tables for units. After preparation, a complete score needs O(g) table reads,
where g counts the goal clauses. No further optimization is necessary.

Alternatively, the exact action-pair min-marginals already computed to build
all price cutoffs can be reused:

```math
D_{ij}(l,u)=\min_{s\ge l,\ t<u} M_{ij}(s,t),\qquad
M_{ij}(s,t)=\min_{a\in A:a_i=s,a_j=t}[c(a)-v].
```

A two-dimensional suffix/prefix minimum table computes these values in
O((K_i+1)(K_j+1)) comparisons per goal edge after M has been purchased.
This is a representation/work bound, not a measured native runtime gain.
Preparation/storage can be expensive for finely discretized levels.

A newly purchased comparison at coordinate i changes only incident goal
entries and its unit entries. Recompute those table values; a charged minimum
data structure can maintain the row's score. The score increases monotonically
as a truthful interval narrows. Its value is still a lower bound on the actual
unsafe-action gap, preserving calibrated_slack.md's selection argument.

## The stronger ordinary control prevents a misleading headline

An ordinary lazy memoized constrained-cut implementation buys the same
D_ij(l,u) entry only on its first request. It makes no more cut calls than the
eager table and can be strictly cheaper on a short calibration stream. For
these finite endpoints there are only (K_i+1)(K_j+1) meaningful requests per
edge. Comparing eager lookup solely with solving every repeated request from
scratch would therefore be a weak baseline. No large benchmark of that
predictable difference is warranted.

Reusing already purchased M tables may remove additional calls in a combined
compiler/calibrator, but the ordinary control receives that same cache. A useful
delta must concern the combined guarantee, receipt scope, representation or
complete duty, not an ordinary solver denied elementary memoization.

Future repricing does not alter these old-cost calibration margins: its purpose
is to select inside the menu protected by the old allowance. Changing F, the
goal, availability, effects or old reference price does change their meaning
and requires explicit cache invalidation or a proved transport.
