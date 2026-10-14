# A retained proof partition becomes a cost-observation cover

**Working DEVELOPMENT; Codex (GPT-6), October 14, 2026.**

This uses the repository's existing proof-tree lower-bound transport. The new
construction here is its explicit retained-proof audit utility and cheap
single-query completion test, to be compared with ordinary constraint cover.

Admit a binary branch tree over the original Boolean source. Every terminal
node is either an independently checked hard-clause conflict or an open/objective
leaf whose path forces a set S of cost features true. Splits cover both truth
values and never reassign a variable. Every feasible original model reaches a
non-conflict leaf and contains that leaf's forced-feature mask. For every new
nonnegative objective q, the retained tree therefore supplies

```math
L_T(q)=\min_{S\in\mathcal L}\sum_{i\in S}q_i.
```

The old objective budget is not what licenses a new weight evaluation. Source
binding, valid splits/conflicts and the forced-feature meanings do. A complete
old proof may make its initial lower exact; a partial tree with explicit open
frontier leaves gives a weaker but still valid reusable bound. Superset masks
can be removed when a subset mask remains, since q is nonnegative. Charge that
antichain compilation rather than silently retaining a free reduced object.

For m supplied source copies with count vector a and intervals [l,u], the s08
induced objective gives the leaf regret upper

```math
B_S(a;l,u)=\sum_{i\notin S}a_i u_i
           -\sum_{i\in S}(m-a_i)l_i.
```

The tree upper is max_S B_S. It certifies tolerance tau precisely when every
leaf upper is at most tau (for this tree and action). At initial [0,H], put
Q_S=max(B_S(initial)-tau,0). Query i returning t contributes a_i(H-t) to a
leaf not containing i, and (m-a_i)t to a leaf containing i. Both are nonnegative.
For each leaf, cap the accumulated contributions at Q_S and sum over leaves.
This observable utility is a sum of capped additive functions, hence monotone
submodular for every realized cost vector; its goal is sum Q_S. It represents
conjunction of leaf obligations. It need not capture every way a different
proof or a different action could solve the underlying repair request.

Independent coordinate queries and a deterministic always-completing fallback
fit the ordinary stochastic-cover premises. Overlapping grouped queries again
do not have independent item states automatically. No greedy approximation
factor transfers to a larger action/proof portfolio merely from this construction.

## Exact one-query completion interval

At a current state define residual r_S=max(B_S-tau,0). For a proposed unknown
coordinate i, let R_in be the largest residual among leaves containing i and
R_out the largest among leaves not containing it (an empty maximum is zero).
One exact response t closes every leaf iff

```math
(m-a_i)(t-l_i)\ge R_{\rm in},\qquad
a_i(u_i-t)\ge R_{\rm out}.
```

When 0<a_i<m this is the interval from l_i+R_in/(m-a_i) to
u_i-R_out/a_i. For a_i=0 require R_out=0 and use the lower inequality;
for a_i=m require R_in=0 and use the upper inequality. If the endpoints cross,
the query cannot finish. Integrating this interval under the actual conditional
response law gives its completion probability. This avoids independently
reweighting the full proof for every possible response. The maxima, initial
admission and later state updates still have real costs.

The s08 baseline improvement c_i<C p_i then applies with a genuinely executable
fallback and a pre-fallback budget B. Logical correctness is independent of the
probability model; the expected-fee bound is not. This is a source-bound instance
of ordinary constraint evaluation and baseline policy improvement, not a claim
of a new stochastic-cover algorithm or unrestricted optimal query selection.

Next screen: extract masks from uf01's actually acquired original-source proofs;
check transported minima and interval completion against direct original-source
solves on small cases, every compatible box on the existing small sources, and
the full checked proof on the external formulas. Compare preparation and query
cost with sparse cuts, exact source geometry and ordinary retained-tree methods.
