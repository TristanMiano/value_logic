# Fallible witness reports and a hard error budget

Codex (GPT-6), s18 DEVELOPMENT. Extends the explicit information contract in
meet_receipts.md and closure_receipts.md. Robust aggregation, resilient convex
hulls and abstract-convexity centerpoints are strong ordinary comparisons.

Assume at most r of m existential reports can be false, with a separately
warranted hard budget0<=r<m. Known feasible points B remain reliable. This
means the unknown F hits every report outside some error set of size at most r.
It is not inferred from model diversity, agreement, or repeated copies of one
prediction. A probabilistic warrant would need its actual common failure event.

For a proper target z under meet closure, replace(M1) by: every zero coordinate
j is supported by a retained point in D_j(z), or by at least r+1 entire
contacts contained in D_j(z). For top, require a retained top or r+1 singleton
top reports. Necessity deletes all at most r qualifying reports and chooses
the other witnesses to avoid that coordinate. Sufficiency leaves at least
one qualifying true report for every required coordinate.

For majority closure, each required unary/binary pattern must likewise have
a retained matching point or r+1 matching whole contact regions. This still
produces an ordinary2-CNF core. Minimum-cost retained evidence becomes a
multicover duty; it does not require a new logical truth calculus.

The subcube meet algorithm still works by treating a coordinate as forced
to one when its active zero-report count is at most r, unless a reliable
retained point supplies it. Adding one coordinates only deactivates reports,
so monotone propagation remains valid. The separate top condition remains
essential.

## Full reported points: a sharp meet-core existence bound

Suppose every report is a complete point and B is empty. If

    m > (d+1)*r,                                                (F1)

the robust meet core is nonempty. Run the preceding propagation. Before a
coordinate is set to one, at most r currently active points have zero there.
Delete those points; active points are exactly those above the growing output.
If all d coordinates were set to one, at most d*r reports were deleted, and
an empty core would require the remaining top multiplicity to be at most r.
That would give m<=(d+1)*r, a contradiction. A proper fixed point therefore
exists, or top passes its test. It is the least robustly guaranteed point.

For r>=1 the threshold is sharp: take r copies of top and r copies of every
coatom(top with one zero). For any proper z, choose a zero coordinate j.
Only r reported points can supply its zero while dominating z. Top itself
has only r copies. Every target therefore fails the corresponding test and
the core is empty at m=(d+1)r.

This is a constructive special case of the known Helly/centerpoint theme,
not a claim that centerpoints are new. Incomplete regions have no comparable
sample-count-only guarantee: repeated fully unspecified regions can leave
the core empty even at r=0. Their informational content matters.

Coordinatewise majority of a majority of valid points is not automatically
a robust repair for a majority-closed F. For F={00,11}, two valid reports00,11
and one bad report01 have majority01 outside F. Our required pair-pattern
counts correctly reject that output. Closure applies to valid inputs; it
does not itself certify that an outlier-resistant aggregate stays feasible.

## No closure assumption: convert a fault budget into contact unions

The condition that F hits all but r contacts is equivalent to F hitting
every union of r+1 distinct contacts. Indeed, missing such a union means
all those r+1 reports are false, and the converse is immediate. Thus the
deterministic total-search reduction applies to this expanded union family.
The expansion can be exponential; choosing a cheapest union includes the
ordinary minimum-k-union problem. It is not an efficient algorithm for
arbitrary input r merely because the earlier contact problem was tractable.

For known action loss h and unrestricted feasible F, the largest compatible
minimum loss is the(r+1)-st smallest value among max_(x in T_i)h(x), further
capped by the best reliable retained point when present. Choose the r reports
with the smallest maxima to be faulty and select a maximizing witness from
each other report to attain the bound. This is ordinary trimming/order
statistics, and remains an existential value bound rather than a recovered
feasible action.

Disposition: useful explicit fault-budget adapter and a sharp full-point
meet threshold. Novelty/readiness unassessed; compare resilient consensus and
abstract convexity before treating it as a new multi-model contribution.

## Full-point majority cores: the corresponding sharp threshold

The robust majority core is the2-CNF forbidding every unary/binary pattern
seen in at most r reports. It is nonempty whenever m>2*d*r, and this
threshold is sharp for r>=1. This is an application of ordinary minimal
unsatisfiable2-CNF structure, not a new generic consensus principle.

For completeness, an unsatisfiable2-CNF on d variables has a minimally
unsatisfiable subset with at most2d clauses. One short route uses the
standard fact that a minimal unsatisfiable2-CNF has at most two unit clauses.
That fact also follows from binary projection completeness: if the binary
part is satisfiable, inconsistency with fixed unary values is witnessed by
at most two such values. In a minimal formula, setting a literal false makes
every clause containing it an indispensable unit clause (use that clause's
private satisfying assignment). Thus each literal occurs at most twice.
If there are u unit clauses, their literals occur only once by subsumption,
so2c-u<=4d-u and c<=2d. An empty clause is a trivial separate case.

If the robust-core formula were unsatisfiable, choose such a subset of at
most2d forbidden-pattern clauses. Every reported point violates at least
one, while each clause is violated by at most r reports. Hence m<=2dr.

Sharpness uses the inconsistent signed cycle
x1=x2=...=xd and xd!=x1, with two clauses per edge (d>=2). Each of its2d
clauses has a private assignment falsifying only that clause: the two
constant vectors for the final inequality, and complementary prefix/suffix
vectors for each chain edge. Take r copies of each private assignment.
Every cycle clause then forbids a pattern supported by only r reports,
so the robust core is empty. For d=1 use r copies of0 and1.

## Full-point affine cores and overlapping proofs

Affine subspaces over F2 have Helly number d+1: an inconsistent collection
of affine equations has an inconsistent subsystem of at most d+1 equations.
The usual safe-area argument therefore guarantees a nonempty robust affine
core for m>(d+1)r. Any d+1 deletion hulls share an undeleted reported point
when that inequality holds; Helly then gives a common point for all hulls.
The bound is sharp using r copies of each of d+1 affinely independent points.
Deleting each point group in turn leaves affine facets with empty intersection.

Nevertheless, deciding membership of a PARTICULAR target can be hard below
that sufficient threshold. For a graph G on d vertices, report the complete
points e_u+e_v for its edges and ask whether target0 is guaranteed under
at most r false reports. The affine separating-functional criterion says
0 is not guaranteed iff some h has h_u+h_v=1 on at least |E|-r edges.
That is exactly a cut of size at least |E|-r. Thus target certainty is the
complement of a MaxCut threshold problem. This is a direct ordinary graph
reduction; no new MaxCut algorithm or distributional assumption is implied.

An intact odd cycle gives a positive proof: XOR its odd number of reported
edge points to obtain0, which belongs to any affine-closed F containing
those points. If r+1 edge-disjoint odd cycles exist, at least one survives
r false reports. Disjointness is sufficient but not necessary. In K4 with
r=1, every deletion of one edge leaves a triangle, hence0 is guaranteed.
There are no two edge-disjoint odd cycles in K4, since its only odd simple
cycles are triangles and any two share an edge. A fractional proof-cover
certificate gives the stronger conclusion: give each of the four triangles
weight1/2. Each edge belongs to two triangles, so breaking every triangle
requires at least total cycle weight2 false edges, exceeding the budget1.

The general certificate is a nonnegative packing of sound proof supports,
with sum of support weights containing each report at most1. If the total
weight exceeds r, not all proofs can be broken by r false reports. This is
ordinary fractional packing/cover duality. A claimed gain must compare it
with that control, not only with disjoint proofs or majority voting.
