# Tolerated repair error, middle receipts and minimum knapsack

**Prospective DEVELOPMENT derivation — Codex (GPT-6), October 14, 2026 UTC.**

The original source has two separate exactly-one components for every edge.
They need not choose the same endpoint. If k of the two choose endpoint a,
their regret is the following expression, with k in {0,1,2}:

```math
kz_a+(2-k)z_b-2\min(z_a,z_b)
=|z_a-z_b|+(k-1)(z_a-z_b).
```

After any receipts, choose the proved cheaper endpoint on resolved edges.
For every remaining edge choose each endpoint once. Let U be unqueried
vertices and M the queried vertices whose value is 1. A fixed action's regret
is convex in the remaining costs, so its maximum over [0,2]^U is attained
at an extreme vector. On those vectors, the balanced action's regret is

```math
R(r)=2\mathrm{MaxCut}(G[U])+|E(M,U)|.
```

This action is minimax optimal, not merely feasible. On unresolved edges,
complement every unknown cost around 1. Known middle endpoints stay fixed;
the absolute-value sum stays the same and the action's signed imbalance term
changes sign. For any other action, at least one of that pair of worlds has
regret at least the balanced value. Resolved edges cannot improve this bound
by being deliberately chosen incorrectly, because their regret is nonnegative.
Maximize over extreme worlds. This proves the claimed minimax value.

If G is bipartite, every induced unknown graph is bipartite and its full edge
set is cuttable. A checked two-coloring therefore gives the exact formula

```math
R(r)=2|E(U,U)|+|E(M,U)|.
```

The attaining extreme world uses the two colors on U; each middle/unknown
edge contributes one regardless of that color. Original-clause feasibility,
source binding and the choice of the two components still need checking.
An odd-cycle source cannot be admitted to the simple exact formula without
a different maximum-cut certificate. The edgewise expression is still a
valid upper bound there, but may buy unnecessary audits.

Define observable utility g=2|E|-R. For a fixed E/M realization this equals
the sum over edges of min(2, sum of selected endpoint scores), where an E
vertex has score 2 and an M vertex score 1. This is normalized, monotone and
submodular, determined entirely by acquired states. For integer tolerance
tau, truncate utility at Q=max(0,2|E|-tau). Reaching Q is exactly sufficient.

The all-M world is the least informative possible outcome of every query.
For a fixed queried set S, its residual is

```math
R_M(S)=2|E|-\sum_{i\in S}\deg(i).
```

Consequently the exact worst-case physical audit fee, even over adaptive
policies, is the minimum-knapsack value selecting vertices of total degree
at least Q. Lower bound: run any policy on all-M. Upper bound: query a minimum
knapsack set; the all-M calculation guarantees tolerance on every outcome.
Stopping earlier on E receipts can only reduce its fee. Degree-quota DP is
an executed ordinary planner, not an assumed optimal oracle. This theorem
concerns bipartite sources and audit fees, not total service computation.

For a prior-free adaptive alternative, let d_i count unknown neighbors and
b_i count observed M neighbors. Querying i reduces regret by
2d_i+b_i on E and d_i+b_i on M. At each step, maximize
min(remaining quota,d_i+b_i)/c_i. The actual capped gain is at least that
minimum and at most twice it. Hence this policy is a factor-two approximate
greedy policy for the realized, truncated deterministic submodular function.
The standard integer submodular-cover charging argument gives 2H(Q) times
the best sufficient query-set fee for that realized world, pointwise. This
does not require stochastic independence or known probabilities. The bound
is loose at zero tolerance, where the preceding local-ratio policy already
gives factor two. A sharper bound is not assumed.

If independent E probabilities are explicitly supplied, an exact expected
capped-gain greedy choice instead fits the ordinary stochastic-cover result
of Hellerstein, Kletenik and Parthasarathy,
[A Tight Bound for Stochastic Submodular Cover](https://arxiv.org/html/2102.01149),
sections 1–3: H(Q) times the optimum expected adaptive fee for integer utility.
The assumptions are independence, pointwise submodularity, observable utility
and coverability. Its approximation theorem is prior art. Estimated marginals
or an arbitrary correlated source do not satisfy those premises automatically.
The newer correlated adaptive-submodular result has separate assumptions and
constants; no version of it is silently imported here.

Finite tg01 screen before any paid service: bipartite path/star/even-cycle
graphs n=2..6 with at most six edges, plus triangle as a boundary case. Check
every partial ternary observation pattern; compare balanced regret with all
compatible ternary worlds and, for n<=4, every 3^m component-count action.
Verify the general maximum-cut formula and the bipartite simplification.
For each bipartite graph and tau in {0,floor(m/2),m,2m}, check all-M knapsack
against a complete minimax E/M query-policy Bellman recurrence and check
prior-free greedy against exhaustive realized sufficient query sets on all
2^n worlds. Add wrong coloring and wrong-source negative controls. Freeze
the declaration and implementation before execution. No physical audits are
bought by these finite mathematical checks.
