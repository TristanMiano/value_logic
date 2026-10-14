# From original basis repairs to weighted-rank observation cover

**Prospective DEVELOPMENT — Codex (GPT-6), October14,2026 UTC.**

Let an admitted original Boolean source describe m independent copies of
a rank-r matroid basis on n cost coordinates. A complete action chooses one
basis per copy. Costs z_i lie in[0,H] and are shared across the corresponding
coordinate in every copy. A mandatory anchor z_0 in{0,A} is added once;
replacement price A=10mrH. This is a structured-source assumption that needs
its own acquisition and checking. It is not a recognizer for arbitrary CNF.

## A robust fallback certificate from an ordinary basis optimization

Supply feasible bases B_1,...,B_m and their integral incidence sum a.
Each a_i is between0 and m, with sum mr. The repair cost is a dot z.
The optimal repair cost without anchor is m times the minimum-weight basis
cost. Consequently the supplied action's exact box regret is

```math
R(a)=\max_{z\in[0,H]^n}\max_{B\in\mathcal B}
       \left(\sum_i a_i z_i-m\sum_{i\in B}z_i\right)
    =H\left(mr-\min_{B\in\mathcal B}\sum_{i\in B}a_i\right).
```

For a fixed comparison basis B, coefficients inside B are nonpositive and
outside are nonnegative. Its maximizing box corner sets inside costs0 and
outside H. Interchange the two finite maxima. The minimizing basis in the
last expression both specifies an attaining corner and permits checking
the bound, provided its optimality is established. For a matroid, ordinary
minimum-weight greedy plus the admitted exchange/rank structure supplies
that optimization. This identity actually holds for any equicardinal
feasible family; the efficient optimizer is the additional matroid premise.

Set the requested tolerance tau=R(a), or any proved larger value below mrH.
If anchor0 is observed, the supplied bases give a valid repair. If anchorA
is observed, replacement has zero regret. This makes anchor acquisition an
executable fallback, independent of any cost probability model.

For a uniform rank-r matroid with m=n cyclic consecutive bases, every a_i=r.
Then tau=Hr(n-r), whereas the all-unknown absolute repair upper is nrH.
The actual returned action comprises n deterministic original bases. It is
not a randomized action whose expected loss is substituted for an
individual-action certificate.

## The full stopping condition without the anchor

Let u_i be observed z_i or H, and d_i=H-u_i. Minimum possible repair upper
cost equals m times the minimum-weight basis at u, since each copy can use
the same minimizing basis. With nonnegative d, basis extension gives

```math
U_*(s)=m\left(rH-r_{M,d}(S)\right),\qquad
r_{M,d}(S)=\max\left\{\sum_{i\in I}d_i:I\subseteq S,\ I\in\mathcal I\right\}.
```

Here S is the queried-coordinate set; unqueried d is zero. Unknown-anchor
replacement cannot meet tau, because its regret is at least A-mrH>tau.
For a repair, combined worst regret is max(R,U), and R<=U. Thus a complete
action exists exactly when U_*<=tau. Let Q=mrH-tau. The exact observable
stopping utility is

```math
g(s)=\min\{Q,\ m r_{M,d}(S)+Q\mathbf1_{\text{anchor observed}}\}.
```

For a fixed realization d, weighted matroid rank is monotone submodular.
One direct proof sorts its finitely many positive levels and writes weighted
rank as a nonnegative sum of ordinary ranks of intersections with the
corresponding level sets. Ordinary rank submodularity and summation prove
the property. Capping a nonnegative monotone submodular utility preserves
it; the anchor is a separate modular contribution. Independent public
coordinate laws therefore permit the same ordinary stochastic-cover
theorem used in graph_cover.md. They are not required for action safety.

This imports known weighted-rank structure. Calinescu, Chekuri, Pal and
Vondrak, [Maximizing a Submodular Set Function Subject to a Matroid
Constraint](https://thibaut.horel.org/submodularity/papers/calinescu2007.pdf),
section1 page2 and section4 pages10–11, explicitly define weighted rank
and its submodularity. No maximization approximation factor from that paper
is asserted for this acquisition problem. The uncertain-weight matroid
paper returned by search could not be opened; its abstract is a lead only,
not evidence of novelty or an imported theorem. The PMC streaming-paper
page hit a browser challenge; its search excerpt is likewise not a read.

## Boundary and finite development screen mc01

The equal-rank family {{0,1},{2,3}} fails basis exchange. For fixed unit
revealed scores, its best-basis reduction is
max(|S intersect{0,1}|,|S intersect{2,3}|). Adding3 to S={0} gives gain0,
while adding3 to T={0,2} gives gain1. Hence arbitrary repair constraints
need not yield submodular observation value. Sharing one cost between
different ground elements also needs a separate closure argument; the
matroid theorem here assigns one queried coordinate per ground element.

Before any paid service, check uniform matroids n2..6 with all nontrivial
ranks, and graphic matroids of triangle, square and K4. Represent each
one-copy source by explicit forbidden-assignment CNF, repeated m times;
this exponential small-instance encoding is a diagnostic, not a scalable
compiler. Use every listed basis once as the fallback action. Check every
one-copy bitmask against the exact basis family, every box corner for the
fallback regret, every partial state in{unknown,0,H/2,H}^n for U_*, and
every pairwise diminishing-return comparison for supported realizations.
Compare weighted greedy with complete basis enumeration. Reject the
nonmatroid exchange family and retain its strict submodularity violation.
No physical query or new resolution acquisition is included in this screen.
