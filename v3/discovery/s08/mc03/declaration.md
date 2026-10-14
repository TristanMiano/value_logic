# Shared observations preserve cover; shared costs can harden the fallback

**DEVELOPMENT derivation — Codex (GPT-6), October14,2026 UTC.**

The last boundary in matroid_cover.md can be strengthened. Suppose each
matroid ground element e uses exactly one query coordinate q(e), possibly
shared with other elements. Let E_j be that coordinate's element group.
Every selected element still has cost in[0,H], and every basis has rank r.
For a fixed realized cost vector, give e weight d_e=H-z_q(e). Querying
coordinate set S activates the union of E_j for j in S. Therefore

```math
F(S)=r_{M,d}\!\left(\bigcup_{j\in S} E_j\right)
```

is monotone submodular as a function of queried coordinates. Apply
weighted-rank submodularity to the two activated ground sets. Their union
is the activation of the query union. Their intersection contains the
activation of the query intersection (and equals it for partition groups).
Monotonicity gives the required inequality. This union argument also
permits overlapping activation groups when a query reveals the same fixed
element weight; conflicting/noisy measurements are a different contract.
Here each element has one unique owner coordinate.

Consequently the same exact upper-repair stopping predicate and stochastic
cover guarantee extend to shared coordinates, provided a valid fallback
repair with regret<=tau has separately been admitted. Independence is
needed only across public query coordinates for the imported stochastic
theorem; logical copies/elements sharing a coordinate are not independent.

The fallback proof changes. Let a_j be the total selected-element count
in group j across the m supplied bases, and b_j(B)=|B intersect E_j|.
Its exact worst repair regret is

```math
R(a)=H\max_{B\in\mathcal B}\sum_j(a_j-mb_j(B))_+
    ={H\over2}\max_{B\in\mathcal B}\|a-mb(B)\|_1.
```

For each B, maximize the linear coordinate expression independently on
the box. Equality of the coordinate sums gives the half-L1 expression.
Unlike the one-element-per-query case, coefficients inside a selected
group may have either sign after aggregation. The expression no longer
reduces to one ordinary minimum-weight basis problem.

The earlier graph construction is an exact hardness witness. Take a
partition matroid with one rank-one block per graph edge and two possible
elements representing its endpoints. Group all elements using the same
vertex cost. Use m=2 and a balanced pair of bases, selecting each endpoint
once per edge. Then R=H MaxCut(G), as derived in tolerance_graph.md.
Even this simple partition matroid can have a hard shared-cost fallback
certificate while residual upper-cost observation cover remains a
tractable sum of endpoint maxima. A supplied cut upper certificate is
useful; computing a sharp one is not silently granted.

This gives a reusable separation for the next discovery session: pay once
to admit source structure and a sufficient robust fallback, then use
ordinary grouped-rank cover or baseline-policy improvement to buy only
decision-relevant observations. Optimal fallback is unnecessary for service;
a checked sufficient tolerance bound is enough. Source admission, bound
acquisition, action export and model-selection costs still need an
end-to-end invoice on a broader task than generated graph sources.

**Prospective mc03 screen:** reuse the18 exposed mc01 basis families and
group coordinates modulo ceil(n/2). On every group score in{0,1,2}, check
weighted-rank reduction, every pairwise diminishing-return inequality,
and both exact grouped-regret formulas against every box corner. Include
the triangle partition-source MaxCut equality. No new physical acquisition.
