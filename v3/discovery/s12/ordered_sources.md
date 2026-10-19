# Ordered-valued models with interval receipts

Codex (GPT-6), October 19, 2026. DEVELOPMENT constructive extension.
This is a possible bridge from Boolean permissions to bounded ordinal or
integer configurations. The median/majority algebra is established CSP
machinery; closest-prior comparison and a cheap finite screen remain due.

The first finite screen is now [interval_probe.json](interval_probe.json):
48 bounded difference-constraint sources, 1,152 interval panels, 7,838 cached
projection comparisons, and the explicit nonconvex-receipt counterexample.
It passes in 0.1560312 seconds together with the temporal checks. This tests
a natural subclass, not every median-closed relation.

## A stronger receipt interface under an explicit structural condition

Let each variable range over a finite totally ordered set. Let nonempty source
F be closed under coordinatewise median of any three of its worlds. A receipt
is a conjunction of interval restrictions x_i in I_i; repeated restrictions
intersect their intervals. Let F_I be the resulting source, assumed nonempty,
and let A_i be its exact remaining unary values. For every pair i,j,

    P_ij(F_I) = P_ij(F) intersect (A_i times A_j).

Given an initially realizable pair (a,b) whose two values remain individually
possible, take x in F with that pair, y in F_I with y_i=a, and z in F_I with
z_j=b. Their coordinatewise median belongs to F. At every receipt coordinate,
two input values lie in its interval, so the median does too. At i and j, two
inputs agree with the desired value. This supplies the required F_I witness.

Interval convexity is essential. In the median-closed ordered source
x<=z<=y over {0,1,2}, restrict z to the NONCONVEX set {0,2}. Pair (x,y)=11
was initially possible and both coordinate values one remain possible, but
that pair is now excluded. Merely retaining endpoint unary domains misses it.

## Why the local tables can serve wider scopes and detect conflicts

Any minimally forbidden partial assignment in a median-closed relation has
size at most two. Otherwise choose three different coordinates of a minimally
forbidden pattern and, for each, a source world satisfying the pattern with
that one coordinate omitted. Their median satisfies the entire pattern,
contradiction. This argument also applies to every projection and to F_I,
since intersecting interval constraints preserves median closure.

The same three-witness argument applies to a minimally inconsistent FAMILY
of interval receipts: if three or more restrictions are minimally inconsistent,
choose worlds omitting three different restrictions. Every restriction is
satisfied by at least two of the three worlds, so their median satisfies all.
Thus inconsistency is witnessed by one interval or two intervals, including
their incompatibility with the original source. Initial unary/pair projections
can detect this exactly.

Adjoining a candidate singleton x_i=a to a consistent interval receipt is also
an interval restriction. If it becomes inconsistent, one original receipt
interval already conflicts with this value (or F itself excludes it). Hence
the exact surviving A_i can be found by support checks against the original
pair tables and the receipt intervals. Arc-consistency propagation over the
complete prepared binary projection network is sufficient; it is not asserted
for an arbitrary unprepared binary CSP network.

With exact A_i and the pair identity, every larger cached projection obeys
the same coordinate-filtering rule. A forbidden pattern in F_I has a forbidden
singleton or pair; that pair was either already forbidden in F or loses a
unary value under I. Thus an originally compatible whole pattern survives
exactly when all of its values survive individually.

## Costs and monotone lineage

Preparation may require expensive source inference. Supplying syntactically
binary constraints does not establish median closure or give the complete
projection network for free. After preparing all needed inter-variable pair
tables, an ordinary support-count implementation deletes each table tuple at
most once along a monotone receipt stream. Its total propagation work is
linear in the installed table incidences and submitted restrictions, with
domain-value deletion work also charged. This can be quadratic in the number
of variables and quadratic in domain size, unlike the compact Boolean input-
implication-graph bound. No general linear-in-input claim is made.
This accounting assumes interval endpoints are supplied as domain indices;
locating arbitrary numeric endpoints adds its actual search/comparison work.

A current register can be a known monotone (increasing or decreasing) function
of one original ordered variable, or a constant. Copies, monotone transforms
and compositions retain this one-origin form. Exact observations or interval
tests of the current register pull back to intervals of the original variable
(or an empty set/conflict). Current pair projections are images of the cached
original pair table; shared origins use the unary table. Store and evaluate
the monotone maps at their actual representation cost, not as free operations.

This extends the lineage/permission idea to coarse exact observations, such as
an interval or clamp output, without revealing the original value. Arbitrary
nonmonotone transforms, combining two unknown origins, or nonconvex observations
lose the guarantee. It does not make utility optimization over allowed actions
easy. A useful application would have to supply a genuinely median-closed
model and an inexpensive ordered observation/edit interface.

Bodirsky and Mamino (2018), Section 2.2, Theorem 2.1, explicitly state the
majority-polymorphism and binary-projection antecedent; their Section 3
includes TVPI constraints and more general median-closed semilinear relations.
The retained delta here is interval-conditioned cache reuse and its lineage
interface, not a new median-closure tractability theorem.
