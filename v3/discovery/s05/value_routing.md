# Routing a value query to the cheapest adequate source

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; a constructive continuation of [row flow](row_flow.md) and
[value acquisition](value_acquisition.md). No additional source evaluations.
The principal owns the clock. The interval-cut reduction and sweep were
proposed by the principal; this note derives routing consequences and supplies
the small independent implementation check.

## 1. An attained cheap extremum is already enough

Let `P_CDF` be the pointwise CDF-band source, and `P_row` the stronger source
that retains interval-supported row masses followed by a Kolmogorov corridor
of radius epsilon. The retained source satisfies `P_row subseteq P_CDF`.

The [CDF sweep](cdf_sweep.py) returns an extremizing population vector p for
each payoff endpoint. If that p belongs to P_row, the corresponding value
endpoint is exact for P_row too: the weaker optimum is attained in the
stronger feasible set. Check the two endpoints separately. One may be settled
cheaply while the other merits stronger optimization.

Rejecting a proposed p is **not** proof of a value gap. Another cheap-layer
optimizer may be feasible, particularly when payoffs have ties. The router's
`lower_equality_certified` and `upper_equality_certified` flags are certificates
when true; false means this route did not settle equality.

These statements concern the convex interval-row source in row_flow.md.
Extra moments, unsplittable row assignments, cross-row logical constraints,
or further finite-cohort information require their own feasibility checks.

## 2. Monotone payoffs need no stronger value solver

Write the empirical CDF envelopes as

```text
A(j) = sum_i w_i*1[u_i<=j],
B(j) = sum_i w_i*1[l_i<=j].
L(j) = max(0,A(j)-epsilon),
U(j) = min(1,B(j)+epsilon).
```

Always restore the known support endpoints. Assigning each row to its right
endpoint gives empirical CDF A; its population CDF L is within epsilon.
Assigning each row to its left endpoint gives B; its population CDF U is
also within epsilon. Thus both stochastic extreme distributions L and U
belong to P_row.

For nondecreasing g, minimum expected value uses U and maximum uses L;
reverse the two for nonincreasing g. This follows immediately from the
signed CDF expansion of g in [threshold values](threshold_values.md).
Weak monotonicity, including plateaus, is enough. Hence every monotone
payoff has equal CDF and row-flow bounds. A small number of monotone pieces
alone is insufficient: the two-row source `I_1=[0,2], I_2={1}` with
`g=(0,1,0)` is already a counterexample at epsilon=0.

## 3. Contract every contiguous payoff plateau exactly

Partition the ordered support into maximal contiguous blocks on which g is
constant. Map each row interval to the first and last blocks it intersects,
retain its weight, and keep the same epsilon. This contraction preserves the
row-source value extrema exactly, even when the resulting payoff has several
monotone pieces.

Projection is immediate: retain each block's total p and q mass and the
Kolmogorov constraint at its ending cut. For the reverse direction, lift every
coarse row allocation to any allowed point in its assigned block, obtaining q.
Inside a block of q mass Q and desired p mass P, if Q>0 set
`p_h=(P/Q)*q_h`. At an internal cut the cumulative difference F_q-F_p linearly
interpolates between its values at the two block boundaries. Both boundary
values lie in `[-epsilon,epsilon]`, so every internal value does too. If Q=0,
put P anywhere in the block; the difference then moves monotonically between
the same boundary values. Row support and the block's payoff are preserved.

The pointwise CDF source also projects exactly: retain its bands at block
boundaries; monotonicity permits extending between those boundaries. Therefore
run the cheap sweep and membership check on the contracted source. A passing
coarse extremizer certifies a lift with the same payoff, without insisting on
the original sweep's arbitrary positions within a constant-payoff block.
This can reduce query dimension from the number of chain versions to the
number of requested payoff runs. Building the mapping and row projection costs
linear work in the original support size and number of rows.

## 4. An exact interval-cut membership criterion

Use support states `0,...,m`. For every nonempty contiguous `[a,b]`, let

```text
C(a,b) = sum_(i: a<=l_i and u_i<=b) w_i,
P(a,b) = sum_(h=a..b) p_h,
d(a,b) = 1[a>0] + 1[b<m].
```

Then the proposed population law p belongs to P_row **if and only if**

```text
C(a,b) <= P(a,b) + epsilon*d(a,b)    for all 0<=a<=b<=m.
```

For the proof, cap each state-to-sink arc in the row-flow network by p_h.
Sending unit flow is exactly feasibility for that p. With state subset S
on the source side of a cut, put all rows wholly supported inside S there
too. The least cut capacity for that state subset is

```text
1 - sum_(i:I_i subseteq S) w_i + p(S) + epsilon*|boundary(S)|.
```

Other rows can be left on the sink side; a unit-capacity row-to-state arc
cannot produce a smaller cut by severing one of their allowed destinations.
Max-flow/min-cut therefore requires the displayed condition for every state
subset S. Because each I_i is an interval, contained-row mass, p mass and
chain boundary capacity all add over the disjoint interval components of S.
Conditions on single intervals are consequently necessary and sufficient.

The imported algorithmic fact is the usual max-flow/min-cut theorem. See
[Ford and Fulkerson (1956), Theorem 1, primary paper](https://www.cs.yale.edu/homes/lans/readings/routing/ford-max_flow-1956.pdf)
and the directed residual-cut formulation in
[James Aspnes's author course notes, section 3](https://www.cs.yale.edu/homes/aspnes/pinewiki/MaxFlow.html).
The original theorem statement and the directed cut proof were read; the
specialized interval inequalities above are derived here.

Prefix and suffix conditions are already the cheap CDF bounds. Proper
interior intervals are the information that pointwise envelopes can miss.
For the two-row example and p=(1/2,0,1/2), interval `{1}` requires
`1/2<=2*epsilon`: this p is rejected below epsilon=1/4 and feasible at it.

## 5. Check all interval cuts with a range-add/max sweep

At right endpoint b, maintain one active value for each start a<=b:

```text
V_b(a) = C(a,b)-P(a,b)-epsilon*1[a>0].
```

Before processing the rows ending at b, activate a=b with value
`-epsilon*1[b>0]`. A row `[l_i,b]` adds w_i to all starts `a<=l_i`.
Subtract p_b from every active start. The whole interval family with that
right endpoint is valid exactly when

```text
max_(a<=b) V_b(a) <= epsilon*1[b<m].
```

A segment tree supplies each prefix addition and maximum with its attaining
start. Bucket rows by their right endpoints. This checks all intervals in
`O((n+m+1)*log(m+2))` arithmetic operations and linear space. Rational bit
growth is not claimed constant. A rejection returns an explicit violating
interval, its forced row mass, available p mass and boundary allowance.

[row_routing.py](row_routing.py) implements this sweep. It does not run a
general flow optimization in its operational membership or routing methods.

## 6. Two reusable source-equality gates

If the total weight of rows wholly inside `[1,m-1]` is at most `2*epsilon`,
every proper interior condition is automatic: its left side is at most that
weight and its right side is at least `2*epsilon`. Prefixes and suffixes are
already enforced by P_CDF. The **entire two sources are then equal**, for
every payoff. In particular epsilon>=1/2 is universally sufficient. The
prototype applies this inexpensive gate after plateau contraction.

A further useful gate is absence of strict interval nesting among positive
weight rows. Specifically, no row may have both a strictly smaller left
endpoint and a strictly larger right endpoint than another. For an interior
interval A=[a,b], exact counting gives

```text
A_CDF(b)-B_CDF(a-1)
  = contained_row_mass(A)-strictly_spanning_row_mass(A).
```

If contained mass is positive, a strictly spanning row would strictly contain
a contained row, contradicting the gate. Thus spanning mass is zero whenever
the interior condition is nontrivial. The two CDF endpoint inequalities imply
that condition, proving equality of the sources at every epsilon. Sorting
rows by their left endpoints and checking the maximum right endpoint from
strictly earlier groups detects such nesting in O(n log n). This additional
gate is derived here but not enabled in the prototype; query-specific
membership already handles those cases. Nested censoring is necessary for a
strict gap in these two source sets, though its presence does not by itself
establish a gap for a given payoff or radius.

## 7. Small constructive check and practical routing order

Command: `python v3/discovery/s05/row_routing.py`.
[The results](row_routing_results.json) retain exact inputs, cut witnesses,
source hashes, and operation counts. Twenty-four small fixed-p cases agreed
with direct enumeration of every interval and an independent rational BFS
max-flow calculation with fixed p sink capacities: ten were feasible and
fourteen infeasible. Six payoff cases also compared contracted and original
row-flow values; all matched. Nine of twelve endpoints were certified by the
cheap route. These are targeted implementation checks on synthetic inputs,
not new sampled evidence or a full audit campaign.

The routing order is concrete: contract payoff plateaus; use monotonicity or
a cached source-equality gate when available; otherwise obtain the cheap
CDF extrema and test each proposed extremizer. Purchase stronger value
optimization for an unresolved endpoint only when its possible precision
gain matters to the requested decision. A failed candidate may still warrant
trying another cheap optimizer before paying that bill. Reuse source
compilation, charge query arithmetic and certificate checking, and retain
the common statistical event. Further proof acquisition remains the separate
costed choice developed in value_acquisition.md.
