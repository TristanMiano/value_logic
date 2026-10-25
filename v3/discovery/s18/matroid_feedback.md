# Candidate extension to matroid choices with tied utilities

Codex (GPT-6), s18 DEVELOPMENT. This is a new extension of the single-item
beatpath adapter, not a claim about all M-convex sets. The key exchange
lemma below is reconstructed explicitly; a stronger two-sided exchange
bijection is neither assumed nor needed.

## Contract and ordinary algorithm

A fixed unknown vector u in R^d values named ground elements, with ties
allowed. On each round a nonempty matroid base family on those elements is
given by a valid independence oracle. The learner returns a basis B; the
feedback gives a feasible basis A, which is u-optimal on all but C rounds.
C need not be known. Matroids and their ranks may change across rounds.

Maintain the same pair counts and strongest-path strict order as in
beatpath_feedback.md. Choose any total extension and run ordinary matroid
greedy in that order to obtain B. On feedback A, increment c_ab once for
each a in A, b outside A with A-a+b a basis. These are safe weak comparisons
u_a>=u_b on every uncorrupted round. A false directed pair is consequently
incremented at most C times, even if one corrupted basis yields many pairs.

## A one-sided ordered exchange matching

Let B be a greedy basis for a strict priority order and A any other basis
of the same matroid. There is a bijection between B\A and A\B matching each
b to an a such that b precedes a and A-a+b is a basis.

Proof by Hall's condition. For X subset B\A, let N(X) be all such eligible
a. Suppose |N(X)|<|X|. For b in X, its fundamental circuit relative to A
contains, apart from b, only elements of N(X), elements of A intersect B,
or elements preceding b: a later element of A\B in that circuit would be
an eligible neighbor. Thus b is in the closure of those three sets.

Greedy spans every priority prefix, so all elements preceding b are in
the closure of the elements of B preceding b. Put D=(B\X) union N(X).
Process X in priority order. The circuit observation and induction put
each b in closure(D), since all earlier elements of X have already been
shown to lie there. Therefore B is contained in closure(D). But

    |D| = |B|-|X|+|N(X)| < |B| = rank(B),

which is impossible. Hall yields a matching and equal cardinalities make
it a bijection. Only exchange feasibility at A was used.

## Charging a genuinely suboptimal round

When A is truly optimal, every matched pair satisfies u_a>=u_b by local
exchange optimality. If B is suboptimal, summing the matched differences
gives u(A)-u(B)>0, so at least one pair has u_a>u_b. That pair is inverted
in the learner's priority order. The strongest-path high-count lemma
therefore implies c_ab<=C before this round, and the update increments it.
Charge the round to one such pair. A pair can receive at most C+1 charges;
there are at most binom(d,2) strict true pairs. Corrupted rounds add at most C.

Hence the number of truly suboptimal basis choices is at most

    binom(d,2)*(C+1)+C.                                  (M1)

If every round's utility range across feasible bases is at most M, total
regret is at most M times (M1). There is no utility-gap factor, fixed
tie-breaking assumption on the feedback, or known corruption ceiling.
Winning-edge strongest paths have the same guarantee. Known C0 permits
the same C0+1 counter saturation as for single alternatives.

Per round, path closure takes O(d^3) elementary operations; greedy uses at
most d independence queries; feedback extraction uses at most d^2 queries
(and representation/copy costs). Counts take O(d^2 log(T+1)) bits. This is
not a free optimization or feedback oracle: those costs remain explicit.

The stronger distinct-coordinate rate in the close Oki--Sakaue paper is
not beaten. The potential increment is a simple polynomial procedure
covering ties AND adversarially corrupted optimum feedback together.
Existing ordered-exchange, robust ranking and inverse-optimization results
may already imply it. Check that question before treating this extension
as a moderately novel contribution. No general M-convex lift is claimed.
