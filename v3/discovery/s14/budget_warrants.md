# Warrant only the parity consequences the reasoning budget can use

Codex (GPT-6), DEVELOPMENT, October 22, 2026. A different model-pluralism
lead within the task-adequacy family. No new code or cycle-basis algorithm
is claimed. The ordinary antecedents are linear-code duality, bounded
inference and minimum cycle bases; their exact comparison remains to read.

Let a supplied nonempty affine Boolean model be C=x0+V in F2^n. A world x
need not belong to C. A legal certificate predicts one unobserved coordinate
j from at most k exact coordinate receipts: it supplies h in V-perp with
h_j=1 and at most k other nonzero coordinates, and concludes

    x_j = h*x0 + sum_(i!=j) h_i*x_i, over F2.

Checking h's membership and the receipt bindings is paid work. A model
contradiction is not a license to release a prediction without this explicit
certificate. The quantity k prices the support used by a conclusion; total
receipts accumulated over a long history may be larger.

Define D_k as the span of all dual words of Hamming weight at most k+1,
and the weakened source

    W_k = x0 + D_k-perp.

Every legal prediction is correct on W_k, even if the actual world violates
other equations of C. This one event covers adaptive target choices and any
number of releases using the declared support cap. The short equations are
simultaneously true on W_k; no conditional probability substitution is used.

## Exact scope and maximality

No strictly larger source can protect every legal short parity certificate.
A world outside W_k violates at least one generating short word h. Choose
a violated dual word of minimum support size among words supported inside h.
For any j in its support, its other coordinates are consistent with some
world of C: otherwise linear inconsistency supplies a violated dual equation
on those other coordinates, contradicting minimality. Thus there is a
nonempty model source after these at most k receipts, and its prediction
for j is wrong in the actual world. This supplies a legitimate conditional
counterexample, not an inference from an empty source.

Conversely, every single-coordinate consequence of C after observing a set
S of at most k coordinates, with a nonempty conditional source and j outside
S, has such a short dual certificate. If the coordinate is constant on
that affine fiber, its linear functional lies in the span of the model
equations and observed-coordinate functionals; eliminating the observations
produces h supported in S union {j}. Therefore W_k is exactly the largest
world set preserving this bounded-receipt inference service.

As k increases, D_k grows and W_k shrinks. The rank r_k=dim D_k measures
how much of the original model the interface can actually use; global
validity imposes dim(V-perp) equations. If the ranks differ, one may satisfy
every equation of W_k while forcing one omitted independent equation false.
A distribution on that affine slice makes C false on every case while all
legal predictions remain right. This is a conditional construction, not
evidence that a naturally supplied model has such a distribution.

For nonuniform nonnegative receipt prices and all coordinates allowed as
targets, replace the short-word condition by
sum_(i in support(h)) c_i - max_(i in support(h)) c_i <= B.
This means at least one coordinate can be omitted as the target. Its span
gives the analogous warrant. The cost expression is monotone under taking
subsets: deleting a nonmaximum decreases the sum, and deleting a maximum
can only replace it by a smaller maximum. Therefore the minimal violated
subset in the proof is still affordable after omitting its own most expensive
coordinate, and the maximality result extends. Restricted target sets need
a separate argument; the subset may lose every allowed target. This does
not assert an efficient general short-word search.

## Graph models have a compact budget hierarchy

Let coordinates be edges of an undirected simple graph. Model each edge as
the XOR of two hidden vertex labels. Then V is the cut space and V-perp is
the cycle space. A receipt path between an edge's endpoints predicts that
edge, provided the path has at most k edges.

Every dual word is an even subgraph and decomposes into simple cycles. Hence
D_k is precisely the span of cycles of length at most k+1. A minimum total
length cycle basis has the threshold property: its basis cycles of length
at most k+1 span every cycle of length at most k+1.

Proof of that property: if a shorter cycle were outside the span of the
short basis elements, its fundamental dependence with the full basis would
include a longer basis element. Exchanging that element for the cycle
would lower total basis length, contrary to optimality. Thus one prepared
minimum cycle basis represents every support-budget warrant W_k. The
basis algorithm, storage, membership checks and actual receipts all remain
charged; this is not a free preparation oracle.

Example: a triangle and a longer cycle share one vertex, with the longer
cycle length L>3. At k=2 only the triangle equation is required. The long
cycle can have odd parity on every deployment case, so the full graph model
is always false. Any one triangle edge is still inferable correctly from
the other two. At k=L-1 the longer equation becomes relevant. Moving to
that larger reasoning budget is a change of reliance scope and needs a
stronger warrant, even though the nominal model object has not changed.

The example distinguishes useful local adequacy from global truth. It does
not establish savings over ordinary graph inference or direct calibration
of the same allowed predictions. Generic affine codes may make discovering
all short dual words expensive; no general polynomial compiler is claimed.

## Why this is worth a cheap screen, and not yet a benchmark

The specific synthesis is a resource-indexed model-validity requirement:
additional reasoning power can require stronger evidence about a fallible
model. More computation does not itself make old model reliance safer.
A checked support cap lets a reasoner retain useful local consequences while
declining the globally false remainder. The graph case gives a compact
simultaneous hierarchy rather than one separately invented model per budget.

An actual contribution would need a naturally useful scope and a comparison
with bounded consistency, parity-code inference and ordinary task envelopes.
For one target, direct validation may be cheaper. No empirical accuracy,
audit-fee, complete-cost or novel-algorithm claim follows from this note.

The primary-source comparison now confirms the cycle-basis component as
ordinary machinery: Mehlhorn and Michail's *Minimum Cycle Bases: Faster and
Simpler*, introduction and Section 2, explicitly uses the vector matroid and
greedy basis extraction. Jeavons and Petke's *Local Consistency and SAT-Solvers*,
Section 2.1, formalizes a different bounded-consistency closure on local partial
solutions. Our k bounds receipts in a checked conclusion, not the width or
runtime of the calculation that discovers its dual word. That distinction is
essential; no bounded-width tractability theorem is imported into this service.

The executed budget_warrant_probe.py compares the proposed source against
direct inference from every affordable coordinate fiber on 200 small affine
panels, including nonuniform prices. All 4,960 world checks pass; 36 panels
strictly relax global model validity. Three tiny graph panels also pass the
basis-threshold check. The triangle-plus-pentagon example has 128 warranted
worlds at support cap two and 64 at cap four. These are exact finite
development checks, not an application benchmark or independent validation.
