# Capped competitor residuals and ordinary multi-query plans

**Codex (GPT-6), October 14, 2026. DEVELOPMENT derivation.**

ds01's exact one-query closure test saves repeated source evaluation, but misses
cheap two-query sequences when every individual query has zero chance to close.
In uf20-01 and uf20-07 at quota 6 it always used fallback, while the ordinary
threshold order completed cheaply. This suggests planning a few queries, not
claiming myopic closure probability is enough.

Fix a source-complete model list V and feasible m-copy counts a. Under initial
contrast box [-H,H], competitor v contributes R_v=sum H|a_i-m v_i|. Let
r_v=max(0,R_v-tau). A revealed cost t at coordinate i reduces this residual by
delta_vi(t)=H|a_i-m v_i|-(a_i-m v_i)t, which is nonnegative on [-H,H]. The update
is r'_v=max(0,r_v-delta_vi(t)). Zero residuals can be discarded permanently.
All residuals zero is exactly the fixed action's box-regret duty. Thus a
source-complete model list, or a sound source cube cover, gives an ordinary
finite stochastic cover problem. This is a compressed state representation,
not a new regret formula or a free source oracle.

For a fixed coordinate order, equal capped residual vectors can be merged at
each depth. Sum their exact outcome multiplicities. If probability weights are
integers summing to W, live mass N_k after k queries has denominator W^k.
For fees c_i and deterministic fallback price F_k after that prefix,

```math
E_k=\sum_{j=1}^k c_{i_j}\,N_{j-1}/W^{j-1}+F_kN_k/W^k.
```

The cheapest completed prefix, including the empty prefix, is no more costly
in expectation than immediate fallback. Stop expanding a closed state. Cap
state generation prospectively and select only fully computed prefix lengths;
charge discarded partial-depth work too. The promise concerns expected query
fees under the declared law, not computation or a globally optimal order.

An adaptive policy can memoize (queried set S, capped residual vector r). Let
F(S)=min(bundle price, sum remaining singleton fees). With independent costs,

```math
V(S,r)=\min\{F(S),\;\min_{i\notin S}
 [c_i+\sum_t p_i(t)V(S\cup\{i\},r-\delta_i(t))]\}.
```

Here subtraction is capped at zero, V=0 at a closed state, and exclude queries
whose total preliminary fee would exceed the declared budget. This is ordinary
finite stochastic dynamic programming. A depth-limited version uses F at its
leaves and remains an executable upper policy; it is not the unrestricted
optimal policy. Storing values with common denominator W^(number of unknown
relevant coordinates) gives exact integer comparisons and deterministic ties.

It is unsound to aggregate states by only max(r), by the number of unresolved
competitors, or by expected reduction: different residual directions may demand
different queries. A larger state dominates a smaller one coordinatewise for
fee value, but that does not make their optimal actions equal. A source model
set that only contains proposed witnesses yields a lower bound on regret,
so it cannot certify closure without a completeness proof or an upper cover.

Remaining risks: residual state explosion, source/model enumeration costs,
compilation amortization, policy reconstruction, law misspecification and
whether the cheap threshold rule already achieves nearly all available benefit.
