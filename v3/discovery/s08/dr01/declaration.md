# An ordinary acquisition surrogate for the repair stopping duty

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

This revisits the established S04 comparison in [s01](../s01/regions.md).
For a fully specified supported cost world h and feasible source action a,
put h in R_a when that action's regret against repair and replacement is at
most the requested tolerance. A receipt state permits action a exactly when
every compatible world lies in R_a. Regions overlap; identifying the full
cost vector or a unique optimum is unnecessary.

Javdani et al., *Near Optimal Bayesian Active Learning for Decision Making*,
sections 2–4, calls this decision-region determination and uses hyperedge
cutting. Chen et al., *Submodular Surrogates for Value of Information*,
AAAI2015, pages3512–3515, instead combines equivalence-class edge objectives.
Their DIRECT construction and its ordinary graph-coloring refinement are
relevant controls. We use the uncolored construction, with explicit finite
world enumeration and charged region construction. Its probability model
guides acquisition; original-source terminal bounds warrant actions.

Primary texts:
[HEC](https://publications.ri.cmu.edu/storage/publications/pub_files/2014/4/javdani14hec_extended.pdf),
[DIRECT](https://ojs.aaai.org/index.php/AAAI/article/download/9694/9553).
The attempted extended DIRECT PDF was inaccessible. We do not import a
numerical approximation ratio here: the older cover argument has later
corrections, and [Al-Thani et al., Theorem1.5](https://arxiv.org/html/2208.08351)
requires a carefully matched observable, monotone, coverable and adaptive
submodular utility. Finite checks below concern our implementation only.

## Exact implementation on explicit worlds

Remove duplicate regions and any region contained in another retained region.
This preserves the terminal predicate: V contained in a removed region is
also contained in its retained superset. Preserve a concrete source action
for every retained region. Group worlds with identical retained-region
membership masks. Every supported world must have at least one admissible
action, including replacement; otherwise the proposed menu is incomplete.

For an observed version set V with total **unnormalized** prior mass N, let
n_g be its mass in membership class g. In the ECD instance associated with
region a, merge every class inside a and leave outside membership classes
separate. Its remaining edge weight is computed without enumerating pairs:

```math
e_a(V)=\tfrac12\left[N^2-
\left(\sum_{g:a\in g} n_g\right)^2-
\sum_{g:a\notin g}n_g^2\right],\qquad
q(V)=\prod_a e_a(V).
```

All masses in this expression use the original prior, not a renormalized
posterior. The common initial denominator of the normalized DIRECT objective
can be cancelled when comparing queries. For query i, compare

```math
\frac{q(V)-\sum_v\frac{N_v}{N}q(V_{i=v})}{c_i}.
```

Use exact rational comparisons and retain large-integer operation sizes in
the proxy invoice. A zero product is equivalent to the terminal predicate:
one ECD instance has a single remaining class, which either is its own
region or has a shared nonempty membership mask for some other region.
Conversely, a common retained action merges the entire set in its ECD instance.
The empty hypothesis set is invalid, not a free success.

The construction is conventional. The local work is a source-bound,
complete-cost comparison with exact frontier and query-policy services.
Enumerating all worlds and actions is exponential in a succinct star source;
no polynomial general-source claim follows from polynomial work in that
expanded table. Full support is essential for uniform stopping. Zero model
probability may not silently remove a logically compatible cost world.

**Prospective dr01:** construct all24 op01 action-region tables. For the
two degree2 stars, examine every partial receipt state and compare region
containment with the partial-star exact frontier. Check mass-formula edge
weights against direct cross-class pairs and DIRECT one-step adaptive
submodularity on every compatible one-coordinate extension. Use the uniform
prior of op01. For all24 tables, build the greedy query policy and verify
its selected response DAG with policy_safety.py, reporting all construction,
scoring and safety costs. No physical queries in dr01. Any subsequent paid
service must be declared separately and use actual new receipts.
