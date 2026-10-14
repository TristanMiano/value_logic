# Adaptive dual charging and an ordinary implementation correction

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The direct adaptive local-ratio implementation queries an observed M's
unqueried neighbors first. When none are forced, take an edge with two
unqueried endpoints, raise its dual until one endpoint is tight, and query
one such endpoint. Skip a second newly tight endpoint if later receipts make
it unnecessary. This is the ordinary prior-art construction already cited,
specialized to the declared source, not a new competitive algorithm.

Its completed query set is T union F, where every vertex in T is dual-tight
and every vertex in F is proved mandatory by an observed M neighbor. The
final dual is feasible: loads only increase on two unqueried endpoints and
never exceed their fee. T covers the graph after removing F. Therefore the
same charging argument yields

```math
c(T)+c(F)\leq 2\left(c(F)+\sum_{e\in E(G-F)}y_e\right)
\leq 2B\leq 2\mathrm{OPT}.
```

Here B additionally uses any other mandatory vertices justified by all final
receipts. The certificate contains the actual per-request dual. A static dual
need not certify this adaptive policy at factor two even when the policy is
two-competitive, so silently checking it against the old dual would be wrong.

An incremental degree/fee greedy controller uses exactly the same selection
rule as gs01, with lazy degree heaps and an ordered forced-query queue. Every
heap comparison and sift is explicitly counted. This removes the old full
graph rescan after every observation; it does not change that controller's
query order or physical fee. Coefficient arithmetic still has an explicit
unit convention, and these counts are not a CPU timing claim.

ga02 completed all 2,544 small worlds, including greedy trace equality and
adaptive dual/optimum bounds, then died with an access violation during
garbage collection while preparing larger trace replays. Its prefix and
exception log are preserved. A fresh ga03 retry executes the same source.
The author permits such stochastic retries; the record does not attribute
this exception conclusively to a specific hardware defect.

Prospective gs02 after ga03 succeeds: reuse all 12 exposed gs01 graph/fee
vectors and exactly the same 32 rows per case. Execute incremental greedy,
adaptive_dual and its ordinary_adaptive mirror. Each arm pays source
admission and its own useful preparation. Greedy retains the static dual
for the existing lower-bound duty. Adaptive arms construct their actual dual
per request. All arms pay physical receipts, original-action checking and
cost-bound checking/export. Cap 1,152 outputs. Freeze source/dependencies
before acquisition, preserve each interrupted attempt, and independently
reconstruct outputs. These reused rows compare implementations and policies;
they are not a new confirmation sample or evidence of unique value-logic
advantage. gs01 measurements remain unchanged.
