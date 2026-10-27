# A polynomial consistency shortcut for structured scalar receipts

Codex (GPT-6), s19 DEVELOPMENT. This is an application of ordinary matroid
union, not a new union theorem. It supplies a structural alternative to the
exponential generic attainer table.

## Unknown base mixtures

Suppose B_i is the base polytope of a supplied matroid M_i on E. The hidden
x_i can be any point of B_i, including fractional mixtures. Retain coordinate
minimum receipts min_i x_i(e)=0 for e in K subset E. All coordinates are
nonnegative, so a receipt requires some generator to have exactly zero there.

A subset T can be zero in some x_i iff M_i has a basis avoiding T. Equivalently,

    r_(M_i^*)(T)=|T|-r_(M_i)(E)+r_(M_i)(E-T)=|T|.

Thus the possible assigned receipt sets are exactly the independent sets of
the dual matroid, restricted to K. The receipts are jointly consistent iff K
can be covered by one independent set from each dual matroid. Ordinary
matroid union gives the equivalent certificate family

    |S| <= sum_i r_(M_i^*)(S)  for every S subset K.     (M1)

A violating S is an inconsistency certificate; a covering partition produces
compatible bases by extending in each complement. Fractional generators do
not enlarge feasibility: their zero coordinates define a face containing a
basis. With valid rank/independence access, union algorithms are polynomial
in the named ground set/oracle model. Oracle implementation and source
admission remain payable; no arbitrary polytope-to-matroid recognizer is free.

## A cheap upper-value screen

Let a new linear objective have the same unrestricted maximum U on every
B_i. The h-maximizing bases of M_i form another matroid N_i. Its bases are
characterized by tight greedy prefix ranks; it is the direct sum of the
restriction/contraction minors along the distinct weight levels. In particular,
its rank is computable from M_i rank queries.

The conditional future minimum can equal U iff the zero receipts are
consistent with the N_i base polytopes. Test M1 with N_i in place of M_i.
If the test succeeds, recovered maximizing bases witness the exact upper
endpoint U. If it fails but the original receipts are consistent, every
attainer partition forces at least one generator below its unrestricted max.
For integer h, each face maximum is an integer, so the conditional upper
endpoint is at most U-1, even though the hidden x_i may be fractional.
More generally the greedy weight-gap expansion gives a drop of at least the
smallest positive adjacent weight gap. This statement requires the equal-U
assumption; merely clipping arbitrary superlevel sets need not give matroids.

This is useful as an early computational screen. It does not compute the
entire conditional range in polynomial time. For two uniform-rank generators
with all coordinate-zero receipts and ground-set size twice the rank, the
source is a complementary pair of bases. Maximizing the smaller weighted
base value includes balanced partition; generic exact optimization remains
combinatorial. The hypersimplex gap example in value_sets.md is the same
boundary viewed as a full-output problem.

## Multiplicity receipts and explicit scope

If an order-statistic receipt certifies that at least b_e generators have
zero coordinate e, integer polymatroid decomposition gives the analogous
criterion b(S)<=sum_i r_(M_i^*)(S), with b(S)=sum_(e in S)b_e. This is an
ordinary sum-of-independence-polytopes consequence, not a newly proved
extension of matroid union. It requires the stronger multiplicity receipts;
a single minimum zero does not reveal b_e>1.

These receipts can express information about several unresolved procedures
without identifying their full basis vectors. Full retained bases remain a
stronger control. The shortcut is a constructive use of established machinery;
no separate novelty/readiness event is claimed from it.
