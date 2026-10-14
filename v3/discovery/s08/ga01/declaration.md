# General graph audits with a checkable ordinary cost guarantee

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

Use the existing original exactly-one product, now on any simple graph. Each
vertex has an independently unconstrained value in {0,1,2}; this describes the
compatible set, not a stochastic independence assumption. Every edge has two
original components choosing its cheaper endpoint. Audit fees are positive.
Call value 1 middle (M), and 0 or 2 extreme (E).

A receipt set resolves an edge precisely when an endpoint has a queried E
value or both endpoints have been queried. Thus every sufficient query set
is a vertex cover. For a fixed realized world, every neighbor of an M vertex
must be queried by every sufficient set: querying that M vertex alone cannot
decide the edge. Writing F for all such mandatory neighbors, the exact
clairvoyant certificate cost is

```math
\mathrm{OPT}(z)=c(F)+\mathrm{VC}_c(G[V\setminus F]).
```

The remaining edges have two E endpoints. This identity is a diagnostic and
proof tool, not permission to give hidden outcomes or an optimal cover oracle
to a controller.

Construct a feasible nonnegative vertex-cover dual y, with incident sums at
most each vertex's fee, and a cover C made entirely of tight vertices. The
ordinary greedy primal-dual procedure raises the dual of each uncovered edge
until an endpoint is tight, then includes all newly tight endpoints. Query
C, then query each outside neighbor of a queried M vertex. Since the outside
is independent, one extra pass resolves every edge.

Let H be the outside vertices forced in that pass, and E0 the edges not
incident to H. Any sufficient set Q contains H, while Q minus H covers E0.
Dual feasibility and tightness give

```math
c(C)+c(H)\leq 2\sum_{e\in E0}y_e+2c(H)
\leq 2c(Q).
```

For the first inequality, edges inside C contribute twice to c(C), edges
from C to the outside contribute once, and the dual weight incident to H is
at most c(H). This proves a pointwise factor two for physical audit fees.
The equal-fee single edge gives a matching deterministic lower bound: make
the first queried endpoint M and the other E. No randomized lower bound is
being claimed.

More usefully, after any completed policy let J be the neighbors of all
observed M vertices. Those vertices are demonstrably mandatory, even if the
M vertex that proves this fact would not itself belong to an optimal set.
A separately checked certificate can report

```math
B=c(J)+\sum_{e\in E(G[V\setminus J])}y_e\leq\mathrm{OPT}(z).
```

The verifier needs only the source graph, positive fee vector, feasible dual
and source-bound receipts. It does not need the full world, a probability
model, an optimal solver or an assertion of actual optimality. Enlarging J
monotonically improves this lower bound because removed incident dual mass
is at most the added vertex fee. The two-pass policy costs at most 2B. A
different heuristic may receive a better or worse checked instance ratio.
Source admission, dual construction/checking, receipts, action checking and
retention are separately priced; factor two is not a complete-cost guarantee.

This is an application of established ordinary uncertainty algorithms.
Halldorsson and de Lima, section 7 of
[Query-Competitive Sorting with Uncertainty](https://arxiv.org/html/2012.09475),
already extend a local-ratio two-factor algorithm to arbitrary graphs whose
edges may need one or both endpoints queried. Bampis et al., section 3.1 of
[Orienting (hyper)graphs under explorable stochastic uncertainty](https://arxiv.org/html/2107.00572),
explicitly use a cover followed by mandatory outside vertices. Neither the
ratio nor the mandatory-set insight is claimed new here. The local work is
the source-bound receipt/cost certificate and its executed comparison.

First finite check ga01: n=2 through 8; path, star, cycle, clique and seeded
sparse graphs; one positive fee vector per graph (seed 8141560). Exhaust all
2^n E/M worlds and all query subsets for the diagnostic optimum. Check the
formula, source action, feasible dual, mandatory lower bound and ratio. Use
alternating 0/2 values for E coordinates, since the edge checker separately
enumerates every still-compatible ternary endpoint value. Add an equal-fee
single-edge tight example and tampered dual, receipt and source controls.
No physical acquisitions in this first mathematical validation. Freeze the
declaration and implementation before execution. A later paid service must
be separately declared and give the same capability to an ordinary control.
