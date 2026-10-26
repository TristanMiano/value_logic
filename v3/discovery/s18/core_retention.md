# How many uncertain-witness receipts must be retained?

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT.
The exact four-square obstruction in [translated_core.md](translated_core.md)
is not just a boundary failure of one three-point formula.

## No dimension-only exact receipt bound

Choose any rational full-dimensional convex n-gon P in R^2 with every listed
center a_i a vertex and with0 in its interior. Let P_i be the hull after
removing vertex i. Every P_i has strictly smaller area than P. Choose rational
t in(0,1) close enough to1 that

    t^2 area(P) > max_i area(P_i).

Set the common uncertainty shape C=-tP and regions B_i=a_i+C. The full
guaranteed hull is

    P minus_Pontryagin(tP) = (1-t)P,

by its facet description, and has positive area. If any one region is removed,
its core is P_i minus_Pontryagin(tP), which is empty: a translate of tP cannot
fit in the smaller-area P_i. Every proper subset therefore has empty core.
This works for arbitrary n at fixed dimension two. These regions may overlap;
the earlier four-square example separately supplies disjoint regions.

Thus neither a dimension-only number of original receipts nor a union of all
fixed small-subset cores generally preserves the exact guaranteed region.
This does not prevent a short derived certificate using all receipts, nor
compression exploiting their shared shape. It limits one particular strategy
of discarding existential receipts based only on ordinary Caratheodory size.

## Margin permits ordinary approximate-hull compression

Now suppose centers lie in a radius-R ball, C is fixed, and a retained subset
has central hull P' subset P with

    h_(P')(u) >= h_P(u)-delta*||u||_2 for every u.

Let K=P minus_Pontryagin(-C), K'=P' minus_Pontryagin(-C). Then

    K minus_Pontryagin(delta*B_2) subset K' subset K.              (R1)

For the first inclusion, y in the left set means
h.y+delta*||h||+h_C(-h)<=h_P(h) for every h. The support approximation
therefore gives h.y+h_C(-h)<=h_(P')(h), proving membership in K'. The second
inclusion follows from P' subset P. In particular an action with a known
delta-radius feasibility margin remains certified after this compression.

A simple constructive bound selects a center maximizing each direction of an
epsilon-net on the unit sphere. Comparing a direction with its nearest net
point loses at most2R*epsilon in support: both centers have norm at most R.
Thus delta=2R*epsilon suffices. This is the standard approximate convex-hull
coreset argument, not a new coreset theorem or an optimal cardinality claim.
It explains why the exact unbounded-necessity construction can coexist with
useful compression when a nonzero margin is available. Computing the net,
support maximizers and retained proof associations remains paid work.

## A planar exact alternative

To retain enough arbitrary verified planar regions B_i to certify the fixed
action0, associate each region with its set of unit directions u for which
min_(x in B_i)u.x>=0. The action is in the common core iff these sets cover
the unit circle. For a region not containing0, this set is a closed angular
arc (possibly empty); for disk uncertainty centered at a with radius r>0,
it is u.a>=r and has angular halfwidth arccos(r/||a||) when||a||>=r.
Known points at0 are a separate immediate certificate.

This arc reduction assumes each nontrivial region excludes0. Regions
containing0 need separate handling: for example a segment through0 can have
two antipodal normal directions rather than one arc. A point region{0}
certifies the action immediately; a larger region containing0 generally does
not. Do not apply the arc algorithm blindly to that wider class.

Minimum-weight circular-arc coverage is then an ordinary geometric retention
control. This is a reduction, not an implemented new acquisition policy: if
unverified candidate regions may fail their checks, their proof success and
failed attempts still need a model and a bill. No query-fee gain follows from
having a cheap offline cover after all witnesses were already verified.
