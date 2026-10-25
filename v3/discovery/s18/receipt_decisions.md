# Scalar reports, incidence metadata and the next solve

Codex (GPT-6), s18 DEVELOPMENT. A decision consequence and two scope
extensions of [the attainer DP](attainer_dp.md), not a measured resource gain.

## A concrete three-way retention choice

Let the hidden feasible set be exactly conv{x1,x2}, with independent points
in the quadrilaterals

    B1=conv{(0,10),(0,11),(1,0),(1,1)},
    B2=conv{(0,1),(0,2),(1,10),(1,11)}.

Retain the old optimum min x-coordinate=0. The next objective is the
y-coordinate. With only that scalar, the sharp next-value interval is[0,11].
For the lower endpoint choose x1=(1,0), x2=(0,1). For the upper endpoint
choose x1=(0,11), x2=(1,11). All y-coordinates lie in[0,11], so these
witnesses establish both endpoints.

If the old receipt also certifies that generator2 attained its zero value,
then x2 lies on the face x=0 and has y in[1,2]. The sharp next interval
becomes[0,2]: use the first lower witness and, for the upper endpoint,
x1=(0,11), x2=(0,2). The identity alone does not reveal the hidden x2.
An arbitrary point chosen on that face is not thereby known to lie in the
actual hidden hull.

Suppose a fresh exact optimizer costs1 and returns an executable minimizing
action, while an already available fallback costs4 in the same units.
Under deterministic worst-case total cost, the scalar-only information
selects the fallback: the fresh solve could cost12. With the certified
generator identity, the fresh solve costs at most3 and is strictly preferable.
The result is a sound change in a robust decision, not a claim that the
actual solve saved a fee in an observed workload.

A retained FULL old optimizer is the stronger control. Its y is in[1,2]
and it is itself feasible, so it supplies an executable action costing at
most2 without the new solve. Thus the comparison must charge actual storage,
source binding, acquisition and arithmetic for three options: scalar only,
scalar plus identity, and the full attaining point. The small metadata option
is useful only when its storage/access tradeoff is real. An equally informed
ordinary robust optimizer makes exactly the same choice.

## Interval reports require witnesses, not equality faces

For reports l_j<=min_i h_j*x_i<=u_j, clip every region by all lower
inequalities h_j*x>=l_j. For T assigned to generator i, add h_j*x<=u_j for
j in T. Each surviving branch is still a product of compact convex regions.
Every valid source has one upper-bound witness generator per report, and
every such assignment enforces the reports. The subset DP and its endpoint
witness proof therefore apply unchanged, with at most2*n*2^k LPs and
O(n*3^k) recurrence work. These regions need not be faces.

An identity receipt now certifies a generator witnessing the upper bound;
it need not identify an exact minimizer. If an exact minimizer identity is
available, it also supplies the required upper witness. None of this turns
an unverified model assertion into reliable evidence.

## A hard allowance for faulty reports

If at most r of k reports may be false, enumerate every subset V of exactly
k-r reports and require just V. Any admissible source has such a valid
subset, and any source satisfying one such subset violates at most r reports.
The admissible source class is exactly this finite union. Take the smallest
lower endpoint and largest upper endpoint over consistent V; report conflict
only when all V are inconsistent. Known reliable reports are always imposed.

This straightforward extension uses at most

    2*n*binom(k,r)*2^(k-r) linear optimizations,
    O(n*binom(k,r)*3^(k-r)) recurrence work,

before sharing repeated constraints. It is not a probabilistic independence
assumption, nor a new robust-estimation algorithm. It states exactly what
the hard fault promise buys and what its combinatorial cost can be. For r=k,
the unconditioned source is included once; no reported equality is trusted.

The useful contribution question remains whether this particular source
and retention interface, including the update failure and exact repair,
adds enough beyond established inverse optimization and disjunctive methods.
