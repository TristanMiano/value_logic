# Protected comparisons for polynomial programs with unresolved evaluations

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass17.
Polynomial identity testing is the primary ordinary antecedent.

## New source contract

Let F(x)=A(x)-B(x) be an n-output vector of polynomials over a field, with
known total degree at most D. Source and model programs are fixed before
the discovery probes. Let each coordinate of x be sampled independently
and uniformly from a declared finite grid of q>D field elements. Acquiring
F(x) pays for actual A(x),B(x) evaluations and exact arithmetic.

Let V be the linear span of ALL F(x) over the declared field domain, with
unknown dimension r<=n. Retain a span S of actual observed vectors. If S
is a proper subspace of V, some linear functional t annihilates S but not
V. Then t*F is a nonzero polynomial of degree<=D. The Schwartz--Zippel
bound therefore gives, conditionally on all previous probes,

    P[F(X) in S] <= zeta=D/q < 1.                    (1)

Uniformity of F(X) on its image is neither assumed nor generally true.

## Rank-stage stopping and a common future-use event

At each current span, stop only after h consecutive probes belonging to
that span; an outside vector increases the span and resets the count.
Fix h before this search. At any incomplete rank stage, false completion
has probability at most zeta^h. There are at most r incomplete stages, so

    P[returned S != V] <= r*zeta^h <= n*zeta^h.       (2)

On the complementary event, S^perp is exactly the set of universal output
contrasts satisfying t*A(x)=t*B(x) for every x. All later choices of x,t
are covered by this common polynomial-identity event. No fresh per-use
confidence charge is needed, and complete-model correctness is unnecessary.

With complete evaluations, the total probe count is at most(r+1)*h. Its
expectation is at most r/(1-zeta)+h: each incomplete stage's wait for an
outside vector is dominated by a geometric variable with success1-zeta,
and the final full-rank stage takes h probes. Early false stops only shorten
the count. These are query bounds, not arithmetic-time bounds.

Example: D=4,q=257,n=128,h=3 gives failure upper128*(4/257)^3<.001.
If actual r=4, expected probes are at most4/(1-4/257)+3<7.064, and the
deterministic cap is15. The rank need not be known to run the rule.
The degree, field, grid, exact evaluation and version premises remain paid.

A predeclared per-stage allocation delta_j=delta/((j+1)*(j+2)), with h_j
chosen so zeta^h_j<=delta_j, avoids using n in the confidence budget.
This ordinary summable union bound is an optional different stopping rule;
the fixed-h example above does not rely on choosing h after seeing outcomes.

## Why the old linear rank distribution cannot be imported

Over F3, take F(x,y)=(x,x*y), with x,y uniform. Its image spans dimension2,
but the zero vector has probability1/3, not1/9. Any discovered nonzero
image line has total probability5/9. With h=1, stopping at the first
redundancy gives false-completion probability

    1-(1-1/3)*(1-5/9)=19/27.

The uniform-linear-image formula instead gives11/27. Thus the linear
formula is unsound for this polynomial source, even though all evaluations
are exact. The replacement degree bound explicitly handles this change.

## Partial mathematical evaluations: do not discard hard points

If an evaluation times out, drawing another point and counting only completed
results can bias the probe law. Unresolved points are not redundant vectors.
The sequential rule must resolve its committed next probe, use a separately
sound membership proof, or suspend without certifying completion.

A batch variant makes the interface explicit. Freeze S, draw h fresh grid
points, and request sound membership receipts F(X_i) in S. An acceptance
requires ALL h receipts. One checked outside vector rejects the batch and
enlarges S; a new independent batch may then begin. Work on the h receipts
can be scheduled adaptively, and proving membership can be cheaper than
computing every output coordinate, but unknown receipts cannot be deleted.

There are at most r rejected batches if each supplies a strict rank increase,
so the same bound(2) applies. An unfinished batch may be resumed or abandoned
without a certificate. Repeatedly replacing unfinished batches until a pass
appears needs its own attempt budget; the r-stage bound does NOT cover it.
Previously revealed batch points cannot be relabelled as fresh validation
for a new span. The final learned span can be correct despite unresolved
coordinate values, provided its required membership proofs are sound.

## Scope and comparison

This learns where a fallible polynomial program supports exact inference,
using a bounded degree warrant rather than a claim that the model is true.
If inputs represent counterfactual edits, their program semantics remain a
separate premise. Divisions, arbitrary conditionals, approximate arithmetic,
and changed programs require new warrants; they are not automatically covered.
Ordinary polynomial identity testing and linear-relation discovery are strong
comparators. A symbolic compiler may derive the relations more cheaply when
source code is available. No complete-cost or novelty claim is made yet.
