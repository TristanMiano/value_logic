# Learn a shared error space through paid linear truth queries

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass41.
Random subspace embeddings, adaptive column reconstruction and residual
control variates are conventional comparisons. This is a proposed exact
query interface, not a demonstrated novel algorithm or runtime gain.

## Contract and a simultaneous event

The exact source is A(x) in R^n. At every request a fallible model B_t(x)
may be chosen adaptively. A separately warranted, FIXED subspace R of
dimension at most r contains every possible error A(x)-B_t(x), across the
allowed inputs and model choices. R need not be known, but it must be fixed
independently of the sketch randomness. Merely saying that each model's
errors separately have rank r is insufficient.

Choose G in {0,...,q-1}^(k by n), with independent uniform integer entries,
q>=2 and k>=r. Then

    P(G is not injective on R)
      <= 1-product_(i=0)^(r-1)(1-q^(i-k))
      <= (q^r-1)/[(q-1)*q^k].                    (1)

This works over exact real or rational arithmetic as well as over a finite
field of size q. It is not a finite-precision numerical rank assertion.

Proof for real arithmetic: fix a basis V of R. Conditional on the span of
i independent rows already acquired in GV, its preimage in R^n has
codimension r-i. Given all but r-i suitable coordinates of a new grid row,
at most one choice of those coordinates lies in that preimage. Hence the
chance of no rank increase is at most q^(-(r-i)). Couple this rank process
to the rank of uniform rows over F_q^r, whose full-rank probability after k
rows is the product in(1). When the ranks coincide, the real process has
at least the finite-field chance of increasing; a one-step increase cannot
overtake a process already ahead. For non-prime-power integer q the same
product follows from the scalar recurrence, without invoking a field.
The final bound is the elementary union bound on the product factors.

On this ONE event, injectivity holds for every later error, even for inputs
and models selected after G is public. The fixed common-space warrant makes
that adaptivity safe. If a proposer can choose an arbitrary new error after
seeing G, it can instead choose a nonzero vector in ker(G), invalidating the
argument. A secrecy claim cannot replace the common-space premise.

## Online correction without storing full truth vectors

Fix a requested linear task T:R^n->R^d. Keep columns H_j=G u_j and
Z_j=T u_j for previously acquired independent error witnesses u_j. Their
full n-vectors need not be retained. At a new request:

1. Pay for the model's G B_t(x), T B_t(x), and the exact sketch G A(x).
2. Set g=G(A-B_t). If g is in span(H), solve H a=g and return
   T B_t(x)+Z a.
3. Otherwise pay for T A(x), return it, and append g and
   z=T(A-B_t) as a new column pair.

On the injectivity event, the reconstructed output is exact: if
G[e-sum_j a_j u_j]=0, the bracket lies in R, so it is zero. Every miss adds
an independent error direction, giving at most r expensive task-vector
queries over an arbitrarily long request stream. No independence or
distribution assumption about the requests is used. The model may improve
or change, provided the SAME common-space warrant covers all choices.

Only a statement about the fixed task T follows from storing Z. A newly
chosen unrelated task T' generally needs T'u_j for old witnesses; those
cannot be recovered for free from Z. Storing full u_j or paying for new
task projections is the corresponding ordinary control.

## A transparent conditional price region

If every exact scalar linear source query has the same price c_A, the sketch
costs k queries per request and T A costs d. Over m requests the method
uses at most

    m*k + r*d

scalar truth queries, versus m*d for always acquiring the task directly.
For r=4,k=5,d=100,m=100 this is900 versus10000, a91% reduction in that
SPECIFIED truth-query count. It is not an executed invoice or total-cost
claim. With q=257, (1) gives failure probability below1/65792.

The complete sufficient saving condition is

    C_setup + C_models + C_linear_algebra + C_storage
         < [m*(d-k)-r*d]*c_A,

with all left-hand costs actually incurred. General linear measurements
may cost as much as a full source solve, in which case this region can be
empty. A one-dimensional task with k>=1 usually defeats this motivation.
An identical ordinary randomized reconstruction obtains the same counts.
The natural application and exact literature delta remain open.

## Why it fits the broader program

The retained object is the model's ERROR space, not a probability law over
unresolved outputs. Paid exact measurements detect when an existing
correction is inadequate and teach a new reusable direction. This connects
fallible models, unresolved computations and bounded acquisition. It does
not turn rank assumptions into facts: their warrant is the main scientific
and practical dependency. Approximate subspaces and noisy measurements
require conditioning/error certificates and are not covered by this note.

The primary comparison screen found direct adaptive reconstruction ancestors:
Krishnamurthy–Singh2014 Algorithm1 and Wagner–Zuk2015 noiseless row/column
recovery. Generic algorithm novelty is REJECTED. The note remains useful as
an explicit residual-query contract, not a promoted novel construction.

For a fixed T one may instead sketch the task error T(A-B) directly. It is
enough that these errors share a fixed rank-r_T space inside R^d, even if
the full n-dimensional errors have high rank. Replace G by G_T T and r by
r_T throughout. This is ordinary composition with the requested task; its
linear query price and common-space warrant still have to be available.
