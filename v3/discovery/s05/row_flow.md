# Retaining censored rows in a common value source

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. A stronger source representation alongside the inexpensive
[CDF sweep](cdf_sweep.md), not a replacement of the calibration event.

## Information that pointwise envelopes omit

Consider two equally weighted rows whose possible thresholds are `[0,2]`
and `{1}`. The empirical CDF envelopes permit a distribution assigning half
its mass to 0 and half to 2. Yet every compatible empirical source puts at
least half its mass at 1. For the payoff `1[H=1]`, the exact partial-cohort
value lies in `[1/2,1]`; the pointwise-CDF source gives `[0,1]`.

Thus there are two useful query layers. Pointwise CDF bands are compact and
have a fast exact value kernel. Retaining the row intervals can give a
stronger common source for later nonmonotone values. It does not require a
new proof purchase or a second confidence event.

## A sound joint source

Let row i have weight w_i, with nonnegative weights summing to one, and a
sound interval I_i. Introduce masses z_(i,h), supported on I_i, summing to
w_i for each row. Define q_h = sum_i z_(i,h). Let p be any probability
vector satisfying

```text
|sum_(h<=j) (p_h-q_h)| <= epsilon, for every cut j.
```

Call the projected set of p vectors P_row. For an iid sample use
`w_i=1/n` and the same simultaneous DKW radius as before. On that event,
the actual empirical source is obtained by assigning row i's entire mass
to its hidden H_i, and the actual population law belongs to P_row. This
argument remains valid after adaptive within-row proof work and for later
selected payoffs. It does not extend iid sampling to a selected completion
subset. For an explicitly complete finite cohort, epsilon=0 is exact for
that cohort and makes no population inference.

Allowing a row's mass to split makes a convex outer source. It deliberately
relaxes integrality, repeated-source equality and any additional cross-row
logical constraints. The computed bound is exact for P_row, not automatically
sharp for all information in the source. Every p in P_row obeys the earlier
CDF envelopes enlarged by epsilon, so optimizing over P_row can only improve
their bounds. Summation by parts also gives

```text
E_p g >= sum_i w_i min_(h in I_i) g(h) - epsilon TV(g),
E_p g <= sum_i w_i max_(h in I_i) g(h) + epsilon TV(g).
```

Consequently this source dominates both earlier bounds and their intersection.
For epsilon=0 its expectation extrema equal the direct partial-row extrema.

## Exact reduction to a flow network

Use source and sink nodes, one node per row and one per ordered support
point. Source-to-row capacity is w_i. Each row can send that mass at zero
cost to a point in I_i. Adjacent support points have arcs in both directions,
each with capacity epsilon and zero cost. A support point h can send mass
to the sink at cost g(h). Send total flow one.

The exiting masses are p, and the injected masses are q. Conservation across
cut j says that rightward flow minus leftward flow is F_q(j)-F_p(j), which
has absolute value at most epsilon. Conversely, given compatible p and q,
send positive differences right and negative differences left across each
cut; the same conservation identities produce a feasible flow. Thus minimum
flow cost equals `min_(p in P_row) E_p g`; negate g for the upper bound.

The simplest network lists every allowed row-to-point arc. A segment-tree
cover can instead represent each interval with O(log m) row arcs, O(m)
tree arcs and m leaves feeding the support chain, for O(n log m + m) arcs.
This compression is a construction option; the initial prototype uses the
explicit network. It does not claim a strongly polynomial implementation.

The finite construction combines established censored-data enclosure,
Kolmogorov confidence control and minimum-cost flow. The intended practical
delta is preservation of useful paid information at a transparent extra
query cost. Its common source supports adaptive payoff selection just as
the pointwise source does. The cheapest adequate layer can answer a query;
the stronger layer is available when its extra precision matters.

## Implemented development and when to avoid this extra work

[The rational reference solver](row_flow.py) uses successive shortest paths
and emits an exact feasible flow plus residual node potentials. Checking
capacity, conservation and nonnegative reduced costs proves optimality of
the stated finite flow problem. [The source-bound probe](row_flow_results.json)
compares eleven small constructions with an independently assembled p/z
linear program; its largest floating reference discrepancy is below 6e-17.
The two-row example above has exact lower values 1/2 at epsilon=0 and 3/10
at epsilon=1/10, while its pointwise CDF lower value is zero.

For the actual nested-CNF sample, all 42 tested endpoints equal the earlier
CDF answers, and the additional flow work costs about 292 ms. The wider
common calibration radius leaves no extra precision benefit in these
queries. Preserve that result; do not use the stronger representation merely
because it is available. [Query routing](value_routing.md) develops cheap
structural and feasibility certificates for when the CDF layer is already
exact for the retained-row source.
