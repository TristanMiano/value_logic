# Constant-noise report feasibility with a known consistent source

Codex (GPT-6), October28--29,2026 UTC. Separate DEVELOPMENT; not a premise
or an enlargement of the frozen V19-R/v1 confirmation event.

## Bounded statement

Deciding whether a future scalar minimum can lie in a given rational band
is in NP for the rational compact-polytope receipt model. It is NP-hard
even on the following restricted, promised-consistent instances:

* two independent source blocks, of equal dimension;
* nonempty full-dimensional compact rational base polytopes;
* every old receipt has the same positive width1/20;
* coefficients and right-hand sides from a fixed finite rational set;
* an explicit strictly feasible old source is supplied;
* the complete future image has at most two intervals of constant description
  length, separated by a fixed gap.

This is a reduction from3SAT, not a new assertion that disjunctive or
piecewise-linear feasibility is hard. The useful contract consequence is
that positive observation width, old consistency, two blocks and a tiny
possible output do not by themselves make report inference easy. It does
not prove an optimal3^k dependence, a lower bound for fixed dimension, or
an average-case obstruction. See the separate comparison below.

## Construction

Let F be a3CNF on p variables. Add a gate variable z; let N=p+1. Each
block i in {1,2} has coordinates x_(i,v,+), x_(i,v,-) for N variables.
Both base polytopes impose

    0 <= x_(i,v,s) <= 1,
    19/20 <= x_(i,v,+) + x_(i,v,-) <= 21/20.

Block1 also imposes, for every clause (l1 OR l2 OR l3) in F,

    x_(1,z,+) + x_(1,l1) + x_(1,l2) + x_(1,l3) >= 1/2.       (H1)

A literal selects its corresponding signed coordinate. Repeated literals
are permitted, with their multiplicities included in the row. The all1/2
point is strictly inside every displayed inequality, so each base is
full-dimensional, compact and nonempty. There are k=2N old receipts:

    19/20 <= max(x_(1,v,s), x_(2,v,s)) <= 1.                  (H2)

To use the minimum convention, set each g_(v,s),i=-x_(i,v,s), with receipt
band[-1,-19/20]. The future affine functions are f1=x_(1,z,+) and f2=2.
Thus the future minimum is exactly q=x_(1,z,+). Ask whether q is in[0,1/10].

The reduction has polynomial encoding length. After common-denominator
scaling all numerical magnitudes are bounded constants, independent of F.
No complexity assertion depends on large encoded weights.

## Boolean decoding

Call a coordinate high if it is at least19/20. Both signed coordinates
of one variable cannot be high in a block, since19/10>21/20. By(H2),
each of the two signs is high in some block. There are only two blocks;
therefore exactly one sign is high in each, and they are opposite.
In either block the other coordinate is at most

    21/20 - 19/20 = 1/10.

Decode block1's high positive sign as true. Every false literal then has
coordinate at most1/10. If z and all three literals of an old clause were
false, the left side of(H1) would be at most4/10<1/2. Thus the decoded
assignment satisfies every gated clause (z OR l1 OR l2 OR l3).

If q lies in[0,1/10], z is false, so the decoded old variables satisfy F.
Conversely, any satisfying assignment of F yields a feasible source with
z false: set each true signed coordinate in block1 to39/40, its opposite
to1/40, and use the complementary assignment in block2. All pair sums
are1, every receipt maximum is39/40, and each gated clause has a high
coordinate. In particular q=1/40 lies in the requested band.

Independently of whether F is satisfiable, setting z true yields the same
construction and proves old consistency. This explicit source can be
included in the input. An infinity-norm ball of radius1/100 around every
such constructed source stays strictly feasible: coordinates remain in
(0,1), high coordinates remain above19/20, pair sums in(19/20,21/20),
and a clause row can fall by at most4/100 from a value at least39/40.
Consequently the reduction does not rely on zero-width source fibers.

## Exact scalar image

Decoding already restricts q to[0,1/10] union[19/20,1]. The upper interval
is always wholly attainable: choose any old Boolean assignment, use0/1
coordinates and their complements, and set the gate pairs in blocks1/2
to(q,0)/(0,1). For q in[19/20,1] all constraints hold.

When F is satisfiable, the lower interval is wholly attainable: use a
satisfying old assignment with0/1 coordinates and complements, and set
the gate pairs to(q,19/20)/(19/20,1/20). For every q in[0,1/10], both
pair bands and all receipts hold, and every old clause has a coordinate1.

Therefore the exact image is

    [19/20,1]                         if F is unsatisfiable;
    [0,1/10] union [19/20,1]          if F is satisfiable.     (H3)

The feasibility hardness is not merely the cost of writing exponentially
many interval components. An exact algorithm producing the complete image
in polynomial input-plus-output time would decide3SAT in polynomial time.
This statement uses the standard interval-endpoint output representation.

There is also a constant-gap optimization consequence. The infimum is0
when F is satisfiable and19/20 otherwise. An algorithm estimating that
infimum with absolute error strictly below19/40 on this family would decide
3SAT by thresholding at19/40. A feasible-source approximation with one-sided
additive error strictly below19/20 would also decide it. These are conditional
worst-case claims (unless P=NP), not a prediction of practical solver time.

## Membership and scope of the lower bound

For a general rational instance, guess one upper-receipt witness block
for each old observation and one future-minimum anchor. Add all old lower
bounds, the guessed old upper bounds, all future lower-band bounds and
the anchor's upper-band bound. This is one rational linear feasibility
problem. A nonempty compact rational polytope has a rational vertex of
polynomial encoding length (the usual determinant bound); checking that
point and the discrete choices is polynomial. Hence unrestricted band
feasibility is in NP, and the reduction proves NP-hardness on the stated
promised-consistent subclass. Calling a promise problem NP-complete would
require fixing the promise-problem convention; no such terminology is needed.

The source dimension grows with p. This does not exclude polynomial
algorithms for fixed source dimension, special slopes or restricted
incidence structure. The argument gives neither a base-specific
exponential lower bound nor an unconditional superpolynomial bound.

## Closest comparisons and disposition

[Lauer's switching-regression result](https://arxiv.org/pdf/1510.06920)
proves NP-completeness via two linear models and complementary Boolean
coefficient choices (Proposition1 and its proof, read). Its Remark1 already
allows adaptation to positive error; claiming that earlier work required
exact observations would be misleading. The present paired-coordinate
reduction uses the same general Boolean-selection idea but explicitly
preserves fixed receipt width, full-dimensional independent bases, a supplied
strictly feasible old source, and the exact two-interval future-image promise.

[Lauer's piecewise-affine identification paper](https://arxiv.org/pdf/1509.02348)
also gives a Partition-based hardness proof with two models and an affine
switching classifier (Proposition1/Theorem1, read). Its learned-regression
contract differs from retaining interval optimum observations on prescribed
source polytopes. This is a contract distinction, not evidence that the
general hardness technique is new.

[Reluplex](https://arxiv.org/pdf/1702.01135) gives the established broader
context of NP-complete piecewise-linear network verification (AppendixI).
The present proof does not import its gadgets. Existing inverse-optimization
and disjunctive-programming results remain relevant, as recorded in the
[V19 comparison](../s19/comparison.md).

Disposition: a useful bounded complexity consequence and a sharpened example
for this contract; novelty as a standalone hardness result remains unassessed.
Do not add its success to V19-R/v1's fixed readiness probability. A finite
regression probe below can check the reduction implementation, but cannot
replace the Boolean proof or establish an asymptotic complexity theorem.
