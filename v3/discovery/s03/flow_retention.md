# S13F: retained flow certificates under explicit changes

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

A feasible allocation f on a fixed prerequisite graph supplies upper bound
U=sum_e r_e-sum_{e,i}f_ei. It may already be useful even if it is not a maximum
flow. A changed consumer query need not discard that checked work.

## Demands, prices and prerequisite removal

Suppose row identities and primitive identities retain their semantics, but
rewards change from r to r', prices from q to q', and supports R_e to R'_e.
Apply the following conservative repair:

1. Delete every old allocation on a removed prerequisite incidence. Let D be
   the total deleted amount. Support expansion leaves old incidences valid.
2. Trim each row's retained amount to at most its new reward r'_e.
3. Trim each column's retained amount to at most its new price q'_i.

Trimming only removes nonnegative allocation, so earlier constraints remain
valid. A linear pass after grouping rows/columns suffices. The final f' is
feasible and hence certifies U'=sum r'-sum f'. The total amount lost is at most

    D + sum_e(r_e-r'_e)_+ + sum_i(q_i-q'_i)_+.

This follows because the old row/column totals did not exceed r/q, and each
earlier repair step only reduced those totals. Rearranging gives

    U' <= U + sum_e(r'_e-r_e)_+ + sum_i(q_i-q'_i)_+ + D.

It is a one-sided deterministic sensitivity guarantee for this retained
witness, not a probabilistic forecast. Any feasible repaired flow can also
initialize an ordinary residual max-flow computation. Its existing mass need
not be thrown away when the cheap certificate is too loose.

## What the version relation must establish

Repricing and changed posterior multipliers can produce new nonnegative
rewards on the same named terms. A checked comparison of supports/prices can
then authorize the repair. A changed physical model, different primitive
meaning, merged term or altered observation law is not validated merely by
reusing its index. Canonical simplification may require a separate row map or
a new graph. The certificate checker proves only the supplied finite graph
inequalities and its relation to an already justified acquisition bound.

Sunk query costs give an instructive limit. Suppose one reward r=1 requires
bits {1,2}, with prices (3/4,1/4), and the old full certificate allocates those
amounts to the two bits. After bit 1 is learned by another task, the new future
problem has support {2} and only price 1/4. Removing the first incidence loses
3/4 of certificate mass; the new upper bound is 3/4, not zero. The old no-gain
statement concerned paying for the whole task, and remains valid at that
scope. It cannot be used as a zero bound for the cheaper continuation.

## Comparison and intended use

This is ordinary feasible-flow reuse and weak-duality accounting, adapted to
versioned value-query witnesses. An equally informed incremental max-flow
solver may use the same repair, so superiority over that class is not claimed.
The plausible use is fast checked responses to many small tariff/reward
changes, with paid augmentation only when a tighter answer matters. Measure
initial construction, every repair and check, query quality, and any fallback
before assessing material usefulness. Reuse count alone is not a result.

## First repair implementation and a better retention target

[repair01.json](repair01.json) uses 80 explicit perturbations of old inputs and
a 32-step tariff/reward trace. All repaired bounds contain the exact optimum
and obey the sensitivity inequality. Local filling with unused capacity helps,
but only 17 of 32 trace bounds are zero, while the maximum looseness is 3/32.
Repair plus old/new checks totals 170.247 ms, versus 109.530 ms for cold integer
exact flow plus check; common initial construction costs 3.177 ms. The sunk-cost
example correctly returns 3/4. Thus this implementation loses both precision
and time on the trace. A full incremental residual-flow control is unimplemented
and could be stronger still. Do not claim a reuse advantage from these results.

The failure motivates a different unit of retention: certify a whole family
of consumer parameters once, instead of editing a witness for every query.
For a fixed graph and boxes r<=r_hi, q>=q_lo, a feasible allocation at the
corner (r_hi,q_lo) gives an upper bound U_box for every query in the box, by
monotonicity of the closure objective. If U_box=0, all such future queries have
the same no-gain answer, so only parameter membership and semantic version
checks remain. No actual query needs to instantiate or trim the old flow.
For independent parameter boxes the corner is itself admissible, so it gives
the exact worst-case closure value over the box, when solved exactly. A box
relaxation of a correlated family can be conservative.

More generally, if demands and capacities are affine in a parameter omega in
a known polytope, the closure optimum is convex in omega: it is a maximum of
linear batch objectives. Its worst case is therefore bounded by the maximum
over vertices (and attained at a vertex for a compact polytope). Feasible flows
for corresponding vertices can be convexly combined to certify an interior
query. The parameter's convex decomposition must itself be checked or given
by the consumer contract. This is standard parametric/robust flow reasoning.
It changes the amortization unit without granting a free pointwise model of
logical uncertainty. The ordinary comparator may use the same family bound.

## Box-family kernel result

[envelope01.json](envelope01.json) constructs and checks one corner certificate
before generating 96 tariff/reward queries on the earlier ample-capacity graph.
All 96 exact optima and the family bound are zero. Preparation costs 3.927 ms;
preparation plus all version/dimension/box membership checks costs 22.651 ms,
versus 315.333 ms for 96 cold exact solves and checks. Three out-of-contract
queries are rejected. This positive scoped amortization result includes setup
and per-query membership, but takes the graph semantics as supplied. An ordinary
flow-envelope service can provide the identical behavior. It is DEVELOPMENT,
not external usefulness evidence or a P3-POS01 claim. The nonconstant extension
is the [exact scalar price profile](price_profiles.md).
