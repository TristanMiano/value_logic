# Certify the rank of hidden training samples without completing them

Codex (GPT-6), DEVELOPMENT, October 22, 2026. An adapter for
learn_affine_warrants.md using ordinary independent-transversal machinery.

The stable-compression confidence bound needs the rank k of the actual
sampled syndromes z_i, while paid receipts provide only affine sets
Z_i containing z_i. The obvious bound dim(span(union Z_i)) can be wasteful:
one uncertain sample can contribute only ONE vector to the actual rank,
even when its possible values span many dimensions.

For any subset I of the N sample indices, put U_I=span(union_(i in I) Z_i).
Then the deterministic certificate

    k <= N-|I|+dim(U_I)                                      (1)

is immediate: the samples in I lie in U_I, and each remaining sample
can increase rank by at most one. The right side can be intersected with
N and ambient dimension r. It can replace k in the increasing confidence
bounds in learn_affine_warrants.md, including after arbitrary truthful
adaptive refinement of this SAME fixed-N cohort.

One candidate I is sufficient for a valid upper bound; finding the best
I is optional computation, not part of the soundness premise. A checkable
certificate may supply a spanning list U containing every Z_i for i in I.
For Z_i=b_i+V_i it suffices to check b_i and each supplied direction of V_i
against U. Ordinary elimination pays for these containments and its rank.

## The best such certificate is exact for the supplied information

In fact

    max_(z_i in Z_i) rank{z_1,...,z_N}
       = min_(I subset [N]) [N-|I|+dim(U_I)].                (2)

This is the independent-transversal form of Rado's theorem, equivalently
linear/partition matroid intersection, not a new rank theorem. The left
side is the maximum number of linearly independent representatives from
distinct sets Z_i. Conversely an independent partial transversal can be
completed by choosing arbitrary elements of the remaining nonempty sets.
The matroid-intersection min-max formula gives the right side.

Primary comparison: D. J. A. Welsh, *Transversal Theory and Matroids*,
Canadian Journal of Mathematics 21 (1969), pp1323-1330,
https://doi.org/10.4153/CJM-1969-145-0. Section 2, printed p1324,
states Rado's theorem and Perfect's partial-transversal corollary in
exactly the rank-deficiency form used here. The formula is imported.

The affine sets need not be enumerated. For each Z_i=b_i+V_i, choose a
finite subset P_i contained in Z_i that spans its linear hull: b_i and
b_i+v for every vector in a basis of V_i suffice. Every union of P_i's
has the same span as the corresponding union of Z_i's. The right side
of (2), and therefore the maximum independent-transversal size, is
unchanged. A conventional linear/partition matroid-intersection algorithm
on these O(N*r) labelled vectors computes the exact value. Alternatively
the rank-minus-cardinality set function in (2) is submodular. Neither
general algorithm is presumed cheap relative to the measurements.

## Useful scope, and an explicit caution

Suppose N-1 cases are certified to have zero syndrome and one case is
known only to lie in a 20-dimensional subspace U of a 1000-dimensional
prior syndrome space. The retained warrant is z in U, so it can retain
980 independent model equations. The naive union-span rank bound is20;
choosing I as the resolved N-1 cases proves k<=1. No value of the last
sample needs to be filled in. This is an algebraic receipt example, not
an assertion that certifying the other cases or the subspace was cheap.

A fixed known U could instead be validated directly with an ordinary
all-pass test, which may give a tighter statistical bound. The present
wrapper is useful when the retained source is data-dependent and the
latent sample span supplies a common protection event. It is not a
universal replacement for direct policy/warrant calibration.

Compressing the final evidence does not mean only the compression cases
were acquired. Every inspected case, partial measurement, failed purchase,
containment check and rank computation remains charged. The possible delta
is a checkable confidence certificate under incomplete training evidence;
the statistical and matroid ingredients are conventional.

Cheap screen: hidden_rank_probe.py passes 240 tiny panels, comparing
2540 complete choices against the subset-deficiency formula and the
succinct affine spanning sets. Seven panels improve the naive rank bound;
240 singleton-refinement checks pass. At N=200, delta0.05, the structured
example's Theorem 10 bound is0.06236148 with k_bar1 versus0.46071480 with
k_bar20. These are formula values on a stated receipt example, not measured
population error or acquisition-cost improvements.
