# S09: nested count sources for changing value questions

Codex (GPT-6), October 11, 2026. DEVELOPMENT; S05/S08T lineage, Q1/Q3/Q4/Q5.
No claim of new greedy optimization or statistical inference.

## Information bottleneck and prospective construction

A global bound sum(y)>=60 for 100 fixed bits gives no positive lower bound
for a selected group of size 20. A separate group bound >=16 does. Changing
weights can therefore make a once sufficient scalar value source useless.
The global-count transport bound is already sharp at that information scope;
another algebraic rearrangement cannot restore the missing information.

Retain a fixed rooted tree whose leaves are the fixed mathematical queries.
For each node v, retain an integer count interval [L_v,U_v] over its descendant
leaves. Leaves also carry hard receipts or feasible base/current bit pairs.
These are constraints on a fixed vector, not independence assumptions.
Statistical intervals, when present, have a simultaneous coverage contract;
hard constraints remain separately typed and authoritative.

Prospective evidence: an exact tree optimizer and endpoint witnesses against
small enumeration; a dynamic subtree-query service with charged update cost;
then assess whether paid hierarchical acquisition is useful. Standard tree
dynamic programming, min-cost flow and laminar constraints are mandatory
ordinary comparisons. An information ablation against only a global count
does not show superiority to an ordinary method given the same tree.

## Exact count propagation

For a leaf, intersect its source interval with its allowed base bits. For an
internal node with children c, the feasible count range is exactly

    l_v = max(L_v, sum_c l_c),   u_v = min(U_v, sum_c u_c).

If l_v>u_v, the source is empty. Otherwise every integer between those bounds
is realizable: child feasible counts are integer intervals and their Minkowski
sum contains every integer between the endpoint sums. Induction constructs
leaf witnesses. This proves feasibility without enumerating truth vectors.

A subtree's unconditional interval can tighten because of its ancestors. With
the parent's globally feasible [a_p,b_p], child c has exact projection

    a_c = max(l_c, a_p - sum_{d!=c} u_d),
    b_c = min(u_c, b_p - sum_{d!=c} l_d).

The siblings can realize every integer in their combined interval. Hence the
formula is both necessary and sufficient, including compatibility with all
ancestors; induction from the root proves exactness. Maintain child endpoint
sums. One local receipt changes only the bottom-up path to root. A requested
subtree bound uses the top-down path to that node. Both cost O(tree height)
arithmetic operations; printing all changed node bounds can still cost O(N).

## Exact signed value optimization

For local base/current pairs S_i and signed rational weight w_i, form
f_i(x)=min{w_i*z:(x,z) in S_i}; unavailable x is forbidden. The source's lower
value is min sum_i f_i(y_i) under the tree counts. The upper value uses max
or negates the weights. These are product relations plus nested counts;
arbitrary coupled CNF constraints are not included.

For each subtree define F_v(k), the minimal cost at count k. A leaf's feasible
domain is an integer interval and its cost has at most one marginal increment.
Inductively represent a child by its smallest feasible count l_c, base cost
F_c(l_c), and a sorted list of increments
F_c(k+1)-F_c(k). To combine children, begin at sum l_c and sum F_c(l_c), merge
their sorted increment lists, and take the cheapest increments for any desired
additional total count. Within each child, earlier increments are no larger,
so tie-breaking by each child's internal order supplies a feasible allocation.
No cheaper allocation can exist than the globally cheapest available multiset.
Thus the parent's cost sequence is discretely convex and exactly that merge.

Intersect with [L_v,U_v]: absorb the increments needed to reach its new lower
endpoint into its base cost; discard increments above its upper endpoint.
The remaining middle slice is still sorted. At the root, take all strictly
negative remaining increments, plus already forced ones. This minimizes over
all allowed total counts. Retain leaf identities in increments and propagate
forced selections to recover an endpoint witness. Exactness follows from the
merge and restriction induction. Maximization is minimization of negative cost.

Each leaf contributes at most one increment on each ancestor level. Merging
d child lists by a heap costs O(N h log d) comparisons in a tree of height h
and maximum degree d, with O(N h) worst-case stored representations if all are
retained. A balanced binary tree allows O(N log N) merge work. Exact rational
bit cost is additional. A chain can be quadratic; shape must be reported.
Weight changes may require rebuilding the cost representation; the logarithmic
update claim above applies to count feasibility/subtree queries, not arbitrary
weighted optimization. This is an explicit ordinary tree optimization kernel.

## Simultaneous acquisition without post-selection leakage

Freeze the tree and risk allocations α_v with sum α_v<=α before generating
the acquisition lottery, or justify each later-created source conditionally
with a fresh lottery and paid risk allocation. A single uniform random leaf
permutation restricts to a uniform permutation within every fixed node.
For each node, a valid all-prefix count confidence sequence therefore covers
its fixed count. A union bound over nodes gives one event of probability at
least 1−α on which all count constraints at all prefixes are true. Independence
between node streams is unnecessary.

A scheduler may adapt which node's next prefix element to evaluate. Cached
hard receipts may resolve that element cheaply; they do not count as a sampled
prefix before its index is actually reached. Unknown outcomes stay in the
partial-label outer source. The simultaneous all-prefix event permits any
adaptive scheduling, later subtree selection and value weights. Choosing a
tree after inspecting this lottery or its sampled answers and reusing the same
nominal α without a selection argument is not licensed. For a balanced fixed
tree, allocations proportional to node size and a summable depth budget avoid
requiring equal risk for every leaf; the cost/power tradeoff still needs testing.

## First constructive probe

[laminar01.json](laminar01.json) matched both rational weighted endpoints in
360 seeded small sources, including 149 infeasible cases and 13,896 feasible
base/current pair worlds. It matched 2,578 static subtree projections and
90 dynamic receipt/restoration cases. One explicit conflict and two invalid
updates were handled. These are finite same-model development checks.

At N=8,192 in one prepared-input run, tree binding cost 13.2645 ms, both
weighted endpoints with witnesses cost 205.0457 ms, 1,000 hard updates cost
10.3132 ms, and 1,000 subtree queries cost 1.7958 ms. The intervals were supplied
fixtures, not acquired confidence bounds. No end-to-end economic claim follows.
