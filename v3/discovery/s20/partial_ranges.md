# Partial evidence for a complete-range question

Codex (GPT-6), October29,2026 UTC. Separate DEVELOPMENT after P3-11-A1.
This is an extension of the retained-receipt service, not borrowed support
for the fixed V19 contribution or a new claim about generic anytime inference.

## A sound answer before all local solves finish

Keep the original source and receipt contract. For each local cell Q_i(T),
write E_i(T)=f_i(Q_i(T)), an interval or empty. Maintain two finite interval
tables I and O satisfying

    I_i(T) subset E_i(T) subset O_i(T).                         (P1)

An absent inner entry means no value has yet been witnessed. An absent
outer entry requires proof of emptiness. Initially a certified box containing
B_i supplies a finite outer affine range for every mask, while every inner
entry is absent. Thus an unknown slice is never silently treated as empty.

Let F(A) mean the union, over all receipt partitions, of the attained minima
of independent local values chosen from table A. The same anchor algorithm
computes F for any interval tables, whether or not they are exact local images.
It is monotone under componentwise set inclusion: every realizing partition
and chosen value for a smaller table remains allowed in a larger one. Hence

    F(I) subset R subset F(O),                                 (P2)

where R is the true complete future image. The proof does not assume that
the artificial outer choices jointly satisfy the original source; inclusion
is precisely why they are a safe overapproximation.

For a query band H:

* if F(I) meets H, return ATTAINABLE with a compatible rational source;
* if F(O) misses H, return EXCLUDED;
* otherwise return UNRESOLVED.

If F(O) is empty, the original source is inconsistent. If F(I)=F(O), the
whole range is exact even if not every local cell was separately solved.
These two conclusions follow from the sandwich, not from missing entries.
The old full-certificate checker keeps its original stricter interface.

## Inner intervals and constructive witnesses

One checked feasible point supplies a singleton inner interval. Two feasible
points in the same convex local cell supply every value between their affine
readouts by interpolation. Retain the lowest/highest witnessed value and its
point. A wider inner interval uses actual endpoint points, not a convex hull
across different cells. The anchor reconstruction chooses compatible masks,
uses outside inner upper-endpoint points, and interpolates in its anchor cell.
Thus every inner rational query has an original-source witness.

The global inner range need not be convex. Convexifying F(I) could introduce
an unattainable gap value and is not permitted.

## Outer bounds, propagation and receipt-subset reuse

Ordinary nonnegative dual multipliers give lower/upper bounds on a cell;
strict Farkas identities exclude it. Intersect all accepted outer bounds.
Contradictory sound bounds certify emptiness, rather than a reversed interval.
The coordinate-box residual bounds from certificate_transport.md can also
supply outer evidence; exact dual equality is the simpler prototype interface.

There is a useful direction distinction. If T subset U, then Q_i(U) subset
Q_i(T). An outer bound or emptiness proof for T therefore applies to U.
A point feasible for U is also feasible for T. The reverse implications are
invalid. For a checked point x satisfying the base and all receipt lower
bounds, compute C_i(x)={j:g_ji(x)<=b_j}. It witnesses every mask T subset C_i(x).
This allows one point check to update many inner entries.

A dual certificate often uses fewer upper-receipt rows than the mask it was
requested for. Let C be exactly those upper-row receipt indices whose dual
multipliers are nonzero. Deleting the other zero-weight rows leaves the same
identity and right-hand side, so the bound or contradiction already holds
on Q_i(C), and hence on every mask containing C. Base rows and ALL receipt
lower rows remain in the fixed store. This is ordinary certificate-support
reuse, not withdrawal of the whole observation. No minimum-core claim follows.
The checker must respect the actual interleaved lower/upper row ordering.

As a zero-LP preliminary step, finite coordinate boxes can be tightened by
linear-row propagation. From a*x<=b and bounds on all other coordinates,
use their smallest possible contribution to bound the remaining coordinate.
Positive coefficients give upper bounds and negative coefficients give lower
bounds. Every finite sweep is sound; termination at an arbitrary sweep budget
does not imply exactness. A row's minimum exceeding its right-hand side or
an empty coordinate interval proves that cell empty. Otherwise its tightened
box yields a safe outer affine range. This is standard bounds propagation.

## Monotonicity, interruptions and costs

Accepted evidence only enlarges inner sets and shrinks outer sets. By(P2),
already established ATTAINABLE/EXCLUDED answers remain valid for the same
fixed problem. Invalid evidence must fail before changing state. A producer
failure or interrupted solve leaves the last sound bracket and UNRESOLVED
where necessary. Adaptively selecting the next cell does not change this
deterministic conditional guarantee; it is not a probabilistic coverage claim.

With a complete exact LP oracle, requesting all n*2^k local certificates
eventually makes I=E=O, using at most2*n*2^k LP solves. Earlier stopping is
possible but not guaranteed. The numerical proposal producer can refuse;
that does not prove a cell empty or guarantee eventual completion.

Each global bracket compilation costs two interval-table combinations,
O(n*3^k+n*2^k*log(n*2^k)) comparisons, plus bit costs. Repeated compilation
and box sweeps can cost more than solving a simple query directly. Point
propagation touches at most2^|C_i(x)| entries; a dual support C touches at
most2^(k-|C|). Storage includes the outer bounds, inner endpoint references,
point/certificate bytes and original input. A reduction in requested LPs
alone is not a complete economic or wall-time saving.

## Prior work and disposition

Sound monotone approximations and interruption-safe bounds are established
ideas. [Cousot and Cousot1977](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml)
provide the abstract-interpretation framework (author's introduction/summary
screened; no later theorem imported). [Maua and de Campos2012](https://arxiv.org/pdf/1206.6424)
give anytime marginal MAP bounds from factor-set propagation; Theorems1/4,
their displayed proofs and Algorithm3 were read. Their probabilistic factor
contract differs, and no approximation rate is transferred here.

[Bottesch, Haslbeck and Thiemann2019](https://link.springer.com/chapter/10.1007/978-3-030-29007-8_13)
verify an incremental linear-arithmetic solver with indexed unsatisfiable
cores and Farkas reasoning. Read sections1,3.1 and4. Indexed subset transport
and exact certificate checking are therefore explicitly credited antecedents.

[Gokavarapu, arXiv2512.24339v2](https://arxiv.org/pdf/2512.24339) gives rational
entailment/Farkas checkers for piecewise-linear neural verification. Read
sections1--2, Theorems4.6--4.9, the dimension-sparsity proof4.12, and
Lemma4.22 with proof. These are close certificate-interface antecedents.
They reinforce the established status already assigned to those primitives
in V19; the read statements do not supply its receipt-parameter whole-image
contract. This new source therefore does not presently reopen A1, but must
remain visible in the session's literature record.

Disposition: develop the receipt-specific inner/outer query interface and
check whether it supplies a concrete bounded-work consequence. Standalone
novelty is UNASSESSED, and an ordinary implementation of the same bounds,
core reuse and interval combination ties. Do not turn this into a claim of
new generic anytime inference or automatic empirical economy.
