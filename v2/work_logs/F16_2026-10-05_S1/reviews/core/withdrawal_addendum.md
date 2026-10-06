# F16 core addendum — complete dual portfolios under row withdrawal

**Signed: ChatGPT (GPT-6 Astra Pro), delegated reconstruction.**
2026-10-05 UTC. Base commit `6ef27f20e3ac0920953a27dd84d6c91a021ba58f`.
Principal clock credit: **zero**. No experiment, frozen source, or gate action.

**Disposition: the optional consequence in `root_reconstruction.md` §6 is
correct under its inherited admitted-context and fixed-query assumptions.**
No repair to the face argument is needed. The current-source and proof-syntax
conditions below should accompany its use.

This is a follow-up to the preserved core review. For this addendum only, I
opened the root reconstruction's §6 and `04c_information_and_withdrawal.md`
§3, after reconstructing the face argument from the supplied dual definition.
Earlier review statements that the root report had not been opened describe
the earlier review stage. This is not a fresh blinded external review.

## 1. Face and vertex argument

For one case and one fixed minimum clause, write

\[
D=\{(\lambda,\alpha)\ge0:
A^\top\lambda=\textstyle\sum_j\alpha_j a_j,
\quad\sum_j\alpha_j=1\}.
\]

After deleting rows S, insert zeros in those multiplier coordinates to embed
the revised dual in the old coordinate space. Its image is exactly

\[
D'=D\cap\{\lambda_s=0:s\in S\}.
\]

The functional `sum_{s in S} lambda_s` is nonnegative on D. Its zero set is
therefore an exposed face when nonempty; the empty case can be handled
separately without a convention about empty faces. More directly, if a strict
convex combination of two points of D has a zero withdrawn coordinate, both
endpoints have that coordinate zero by nonnegativity. Thus every vertex of
D' is a vertex of D. Conversely, an old vertex lying in D' remains extreme
in the subset. Hence

`vertices(D') = vertices(D) intersect {lambda_S=0}`.

This is stronger than the one-way inclusion needed for retention. It requires
neither full dimensionality nor boundedness of the source polyhedron.

For an admitted current RHS, the lifted primal remains feasible. If D' is
nonempty, any dual point provides a finite upper bound. Finite rational linear
duality gives an attained optimum. The standard-form dual is contained in a
nonnegative orthant; the least-positive-support argument gives an optimal
rational vertex even when it has unbounded rays. Thus complete old vertices
include a current optimizer. If D' is empty, the feasible lifted primal has
no finite upper bound. An empty **supplied cache** is not proof that D' is empty.

## 2. Required qualifications

| Issue | Exact condition |
|---|---|
| Source witness | Pure row deletion preserves the old feasible rational witness. Simultaneous retained-RHS changes require a checked feasible witness for every current live case; the old witness may fail. Infeasible sources are not covered by the optimum claim. |
| Initially empty dual | If D was already empty, withdrawal cannot create a dual point because D' is a subset. There was no finite clause-optimal portfolio to retain. |
| Lower-dimensional or unbounded source | Allowed. The argument uses vertices of the nonnegative standard-form **dual**, not vertices or compactness of the original source. |
| Multiple cases and clauses | Apply the face filter separately to every `(case, clause)` catalogue. Take the minimum of surviving vertex budgets within each clause, then the maximum over clauses and all current live cases. One empty clause-dual in a required live case makes the global native optimum infinite. A local request uses only its requested case. |
| Fixed numerical interpretation | Keep the literal query/affine leaves, source coordinates, row directions, conversion meanings and case schema fixed. A is the target-unit converted/reduct matrix used for U11; inaccessible rows have no dual coordinate. The result does not establish full-source completeness beyond that scope. |
| Complete catalogue | Retain every original dual vertex, or a separately justified equally complete collection. A current selected optimizer, arbitrary proof portfolio, or bounded search failure supplies no such guarantee. |
| Current proof syntax | Reconstruct and check the new context fingerprint, row indices, budgets, local scopes and common literal root. A numerical face filter is not permission to submit the old serialized proof unchanged. |

Emit each vertex certificate using only its positive-support **source rows**.
A stored `scale(0, row)` still contains a row instruction that the checker
validates. Therefore omit such leaves, or explicitly replace/prune them during
current reconstruction. Merely multiplying by zero is not that reconstruction.
This concerns proof premises: the query's minimum expression must retain its
original affine leaves even when some dual alpha weights are zero.

A transport may select the best surviving argument and produce an exact
current proof while discarding future alternatives. Keep the complete original
catalogue separately when further withdrawals/RHS changes must remain supported.
This is the distinction already made by 04c §3 and the root's §6.

## 3. Minimal boundary witnesses

- For query x with rows `x<=eta1`, `x<=eta2`, D has vertices `(1,0)` and
  `(0,1)`. Deleting the first row leaves exactly `(0,1)` and optimum eta2.
  Retaining only the formerly selected first proof can miss this finite result.
- For query x with only `x<=eta`, D has the single multiplier lambda=1.
  Deleting that row makes D' empty; the revised source is the entire real
  line and the query is unbounded. Its old witness remains feasible.
- With no source rows, the clause `min(x,-x)` still has the dual point
  `alpha=(1/2,1/2)` and optimum zero. Withdrawing all rows does not by itself
  imply an empty dual or an infinite optimum.

These are exact algebraic witnesses. No executable experiment was needed for
this bounded addendum. The reviewed consequence is a conditional retention
theorem, not a claim of practical catalogue completeness or cheap construction.
