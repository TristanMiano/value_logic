# Indexed dispatch over weights, price and regret tolerance

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; a query design following [the uniform regions](reprice_regions_findings.md).
No new solver experiment is needed for this derivation. The principal owns
the clock. The common symmetric radius for the sixteen fixed certificates at
p=6, tau=1 remains **zero**.

## Price and tolerance are query coordinates

The saved witness/tree region has inequalities
`(u-v_l) dot w<=tau` and `u dot w-p<=tau` for repair, or
`p-v_l dot w<=tau` for replacement. A region therefore answers many later
prices and tolerances, not just the price at which it was compiled. A returned
repair is the stored hard-feasible assignment; a returned replacement is
the declared replacement option. Keep clauses, variable meanings, objective
indexing and certificate identities fixed.

Fix a weight cell `c_j-r_j<=w_j<=c_j+r_j` with `c_j-r_j>=0`. For every
repair/tree pair, precompute

```text
D_(u,T) = max_l [(u-v_l) dot c + sum_j |u_j-v_lj|*r_j],
B_u     = sum_j u_j*(c_j+r_j).
```

For every tree precompute `A_T=min_l sum_j v_lj*(c_j-r_j)` and retain the
largest A_T with its tree identity. The fixed pair's exact uniform-cell
conditions become

```text
Repair:       D_(u,T)<=tau and B_u<=p+tau.
Replacement:  p-tau<=max_T A_T, with tau>=0.
```

The two repair constraints are independent support-function maxima, which is
valid because each must hold throughout the entire cell. No supplied
probability law is involved. The cell may be asymmetric around an earlier
weight vector. That can preserve useful directions which a symmetric ball
with zero radius fails to describe.

## A simple two-coordinate index

Store each repair/tree pair as `(D,B,witness_id,tree_id)`. Sort by D, then
store at each prefix the minimum B and the pair attaining it. Pairs dominated
in both coordinates can be removed after paying for that reduction.

For a query (p,tau), binary-search the last D<=tau. The prefix's B<=p+tau
test is necessary and sufficient for some stored repair pair to certify the
whole cell. Replacement uses one subtraction and comparison against the
cached maximum A_T. Both answers retain a specific feasible action and proof.
An application may accept the first passing action or compare p with the
returned repair's B to choose its smaller quoted worst-case cost. Neither
choice claims to discover the globally cheapest unarchived repair.

Index construction costs the coefficient/support passes already made explicit
in the region compiler, plus O(R log R) sorting and O(R) prefix work for R
repair/tree pairs. Storage is O(R), or less after dominated pairs are removed.
The query costs O(log(R+1)) index comparisons. A failed guard only says this
cell-wide fixed-pair index did not answer; it does not reject the particular
weights or prove that more solver work is required.

For row 0's 25% relative cell, the selected repair/tree has `D=1, B=5/2`.
The same tree supplies `A=3/2`. At tau=1, repair is certified whenever
`p>=3/2` and replacement whenever `p<=5/2`. Their union covers every
nonnegative price while remaining uniform over all weights in that cell.
Thus the p=6 example extends to a complete checkable price family with an
explicit action switch. This is a consequence of the stored supports, not
of sampling additional prices.

## Complete query invoice

A query must pay for these operations:

1. Admit the trusted certificate cache and bind the source, objective order,
   checker version and cell identity. This cost may be amortized only while
   that admitted cache remains valid.
2. Read the supplied weight version. For a new version, check its k coordinate
   bounds against the cell. Reusing an already admitted immutable weight token
   needs its identity lookup instead; an unchecked token cannot bypass this.
3. Read and validate p and tau, including nonnegativity. Test replacement and,
   when needed, perform at most `ceil(log2(R+1))` repair-index comparisons,
   one prefix-record read, one addition, and one acceptance comparison.
4. Return the action, witness/tree references and region/cell identity; charge
   lookup, result materialization and any required receipt verification.

The symbolic bill is therefore

```text
C_query = C_cache_admission_or_lookup + C_weight_admission_or_lookup
          + C_price_tolerance + C_index_query + C_action_receipt_output.
```

A cold cache is not a constant-cost query. If the consuming process does not
trust the exporting checker receipt, it must admit the raw source and proofs;
a checksum by itself cannot validate unseen proof bytes. The corresponding
[compact-cache implementation](regions_bundle_findings.md) records that
one-time checking step and subsequent trusted admission separately. Operating a price index
does not remove acquisition, compilation, identity, storage or delivery costs.

## The strong exact fallback is incremental repricing

At one fixed weight version, the archive's best witness and tree supply
numbers U and L with `L<=C*<=U`. These already answer every price/tolerance
query exactly for the archive gate:

```text
p<=L:        replace, regret bound 0;
L<p<U:       replace, regret bound p-L;
p>=U:        use the attaining repair, regret bound U-L.
```

Changing only p or tau therefore requires no mask reevaluation at all. This
is a strong conventional comparator for the region index. The region index's
prospective value is amortization across multiple different weight vectors
within an admitted cell, while preserving a requested tolerance.

For a weight change, cache the cost of each distinct violation/leaf mask and
an inverted index listing which masks contain each objective coordinate.
Changing coordinates J updates a mask by the sum of its selected deltas.
Identical masks can share that arithmetic across proofs while retaining each
source-specific receipt. Update the affected witnesses' costs and tree minima,
then the best witness and maximum tree lower bound. A simple implementation
can rescan only affected components; a maintained min/max tree gives logarithmic
updates per affected role, with its construction and maintenance charged.

With I_J coordinate-to-mask incidences visited and A_J affected mask roles,
the bill includes `C_delta_read + C_incidence_visit(I_J) + C_role_update(A_J)`
plus rebuilding the row's selected extrema and returning their references.
Dense edits can still affect nearly every mask. This mechanism supplies a
complete pointwise archive answer when a cell guard misses, and may itself
be cheaper than building many regions. It is standard incremental maintenance,
not a claim that a new statistical or solver principle was discovered.

The resulting hierarchy is useful without an automatic new-proof purchase:
an admitted cell guard, an exact incremental archive update when necessary,
and fresh proof acquisition only when the resulting pointwise regret bound
still misses the requested duty. Cells and indices remain revisable as actual
price/weight requests reveal which reuse is worth paying for.
