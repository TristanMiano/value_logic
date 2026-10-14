# Signed contrasts need retained cubes, not only positive masks

**Working DEVELOPMENT; Codex (GPT-6), October 14, 2026.**

The positive-variable-cost SATLIB interpretation can be trivial when one model
is contained in every other. A different, prospectively declared duty assigns
nonnegative costs to both Boolean choices. With m source copies, the common
cost of choosing false cancels between repairs, leaving the signed contrast
d_i=cost(true)-cost(false). Independent pairs induce independent contrast
coordinates, but a contrast law must be derived from its actual pair law.
This changes the duty; it is not a rerun or improvement of uf01 or F01.

For a supplied m-copy action with true-counts a_i and d_i in [l_i,u_i], the
same endpoint argument gives exact regret

```math
R=\sum_i a_i u_i-\min_{v\in V}\sum_i q_i v_i,
\qquad q_i=a_i u_i+(m-a_i)l_i.
```

Now q can be negative. Flip each source variable with negative q, transform
every original clause by that same substitution, and use weights abs(q_i).
The old optimum equals the transformed nonnegative optimum plus
sum_i min(q_i,0). Check the clause substitution and original witness transport;
do not feed signed weights into an interface whose old proof assumes they are
nonnegative. This is ordinary objective normalization, not a new optimization
principle.

A retained branch partition must keep both true and false path assignments.
For a leaf cube, assigned-true coordinates contribute q_i, assigned-false ones
zero, and unassigned ones min(q_i,0) to a valid scalar lower. A positive-only
mask loses information needed for this signed-domain transport. Taking the
minimum across all non-conflict cubes preserves original-source coverage.

The associated leaf regret upper is a sum of coordinate contributions:

* assigned false: a_i u_i;
* assigned true: -(m-a_i) l_i;
* unassigned: max(a_i u_i, -(m-a_i)l_i).

Each decreases under interval refinement. Exact audit reductions are additive
within a fixed leaf; capping each leaf's accumulated reductions at its initial
quota and summing gives the same ordinary conjunction-cover construction.
The action and admitted partition stay fixed. Additional action/proof choices
can yield earlier closure without making this one cover predicate complete.

For one proposed audit i, group current positive residuals into three maxima
R_false, R_true and R_free according to the cube's assignment of i. Let
h=max(a_i u_i,-(m-a_i)l_i). A response t completes the retained-tree duty iff

```math
a_i(u_i-t)\ge R_{\rm false},\qquad
(m-a_i)(t-l_i)\ge R_{\rm true},\qquad
\max(a_i t,-(m-a_i)t)\le h-R_{\rm free}.
```

These four linear inequalities define an interval, possibly empty. Evaluate
degenerate zero coefficients directly. Its conditional probability supports the
same bounded-fee one-query improvement, without solving the source separately
at each hypothetical response. Source proof acquisition, cube retention,
partition maxima, actual receipts and final checks all remain priced work.

A direct contrast query, if offered, must be available to ordinary controls at
the same fee. Comparing it only with buying both absolute costs would exaggerate
the contribution. Proved constant source coordinates can also be omitted by all
controllers in repair-only regret. The older fixed-replacement duty would need
the common absolute cost retained separately.
