# Shared latent facts in the paid query/revision regret oracle

Codex (GPT-6), DEVELOPMENT. This extends the interval oracle while preserving
an explicit kind of dependence between original facts. The intended delta is
an exact, compact counterfactual comparison with checked aliases, rather than
discarding those relations in separate coordinate intervals.

## Source and operations

Partition m original signs into G groups. Every coordinate i in group g has
original sign Y_g; a known sign reversal can instead be absorbed into its
weight w_i. This equality is a source premise, not inferred from model
agreement. A query observes an allowed original sign; a flip changes only
that coordinate's output sign, so it need not change other group members.
The last distinction is part of the counterfactual semantics. Query/flip
fees are fixed and nonnegative, and the pathwise operation cap is H.

For the first construction, the r queryable signs are distinct singleton
groups. Their full cells z have known masses p_z. The other group means
theta_zg belong to independent intervals [l_zg,u_zg] conditional on z.
Arbitrary dependence between different hidden groups is allowed. Any such
mean vector has an attaining conditional product law on the G-r latent
signs; this does not impose stochastic independence on every admissible law.

A fixed randomized controller has cell fee C_pi(z) and signed coefficient
s_pi,zi for each original coordinate, as in the earlier oracle. Define its
group response S_zg=sum_{i in g} w_i*s_pi,zi and A_g=sum_{i in g}w_i.
Terminal zero has comparator response zero; terminal one with flipped subset
F_g has response A_g-2*t_g, where t_g=sum_{i in F_g}w_i.

## Convex one-dimensional profile at a terminal history

At query history h let I_h be its compatible cells and P_h their total mass.
For terminal one, the group contribution before comparator flip fees is

```math
G_{hg}(t)=\sum_{z\in I_h}p_z
 \max\{\ell_{zg}(S_{zg}-A_g+2t),u_{zg}(S_{zg}-A_g+2t)\}.
```

This is a convex piecewise-affine function of ONE scalar t even if the group
contains many unequal positive/negative weights. Its breakpoints are
(A_g-S_zg)/2 for nondegenerate, positive-mass intervals. Hence there are at
most |I_h|+1 affine pieces. Each piece extends to a global supporting line,
and G is the maximum of these lines over the entire real axis.

Construct all lines in a sweep. Initially choose every lower endpoint; crossing
a breakpoint changes the corresponding endpoint to its upper endpoint.
Coefficients whose intervals are degenerate contribute one fixed line term.
Ties can be processed together. This obtains lines alpha*t+beta without
enumerating all 2^|I_h| endpoint patterns.

For exactly j flips in group g,

```math
\max_{|F_g|=j}\{G_{hg}(\sum_{i\in F_g}w_i)-P_h\sum_{i\in F_g}f_i\}
=\max_{(\alpha,\beta)}
 \left\{\beta+\text{sum of the j largest }(\alpha w_i-P_h f_i)\right\}.
```

The identity just interchanges two finite maxima. Use the j largest gains
even when negative because this profile fixes j; the outer budget convolution
chooses whether to use fewer flips. Combining group profiles with total
sum_g j_g<=k is an ordinary multiple-choice cardinality dynamic program.
This avoids enumerating all subsets or all distinct weighted subset sums.

Terminal zero contributes `sum_zg p_z*support_[l,u](S_zg)`. Add the controller's
common fee row to either terminal value. The query alternative remains
-a_j*P_h plus the two child regret values. Conditional mean boxes for disjoint
leaf cell sets can be chosen together, giving one common source witness just
as in the original oracle. There is no adversary reselection along execution.

The source witness chooses each group interval endpoint by the sign of
S_zg minus the comparator's group response. The same endpoint is shared by
all aliased original coordinates in that group. This enforces the intended
logical/source dependence rather than independently choosing inconsistent
means for copies of the same fact.

## Size, comparisons and limitations

At a history, each group needs at most |I_h|+1 sorted weighted gain lists,
plus O(G*H^2) budget convolution. Across at most 3^r histories this is
polynomial in m and H for fixed r. Group intervals use (G-r)*2^r numbers;
there is no enumeration of all m-bit truths. Sorting and exact rational
arithmetic costs must still be measured.

This uses ordinary convex piecewise-linear support, top-j selection and
knapsack dynamic programming. It is a proposed structured regret oracle, not
a new robust-optimization framework. A comparator using the same checked
aliases and the same reduction will tie. An independent-coordinate box is
only a named conservative relaxation; its possible larger bound is not a
fair claim of superiority over every ordinary method.

The direct minimax LP for independent coordinate intervals does not immediately
carry over: the supporting-line breakpoints depend on the controller. The new
oracle can supply separating constraints for a convex mixture/flow problem,
but a compact direct LP for this grouped case is not yet established.

Prospective cheap screen: small groups and cells, arbitrary signed weights,
mixed controller rows and zero fees; compare group profiles with explicit
subsets and the regret bound with all interval corners. Include a larger
fixed-r construction to count retained entries and operations. Compare with
the independent-coordinate outer box and retain ties/adverse costs. No broad
benchmark is needed for this cheap screen; discovery remains the stage.

## Observed first screen

[gr01](gr01/attempts.jsonl) completed all six cases on first attempts. The
five small cases check 296 interval corners, 24 unrestricted interleaved
planners and 194 explicit within-group subset profiles. They include mixed
controller rows, signed/zero weights, zero fees, zero-mass cells, zero horizon,
no queries and a horizon above the coordinate count.

The 101-coordinate, three-query, ten-group example retains 64 mass/moment
entries and visits 27 histories. Its exact grouped regret is 3295/372
(about 8.8575), versus 3253/124 (about 26.2339) for the independent-coordinate
outer relaxation of the SAME controller. The group oracle uses 509 affine
lines, 6073 sorted gain entries and 3186 budget-convolution options in that
run. Three small cases tie the outer relaxation and two improve it.

This tighter number is the value of preserving supplied source relationships,
not an observed reduction in executed losses or paid source-admission cost.
An ordinary oracle with the same relationships reproduces it. The executed
source hash and complete inputs/witnesses are in the output files. General
proof and comparison claims remain DEVELOPMENT.
