# A private polynomial scope check across adaptive model proposals

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 34.

Combine [private-checker retirement](private_checker.md) with polynomial
error spaces. Let A be a fixed vector polynomial, and require every proposed
model B and every claimed constant linear error space U to have a proved
degree bound deg(A-B)<=D. Draw k independent secret points X_j from a
product grid S^m, |S|=q>D, and acquire the k true vectors A(X_j).
For each proposed pair (B,U), accept exactly when

    A(X_j)-B(X_j) lies in U for every j.

The claimed conclusion is ALL-INPUT membership A(x)-B(x) in U. A false
claim has some annihilator t of U for which t^T(A-B) is a nonzero polynomial.
Schwartz's bound gives fixed-claim acceptance probability <=(D/q)^k.
The annihilator need not be found by the checker; ordinary exact membership
testing suffices. Degree promises require their own sound basis.

Keep every X_j and checked residual private. Expose only accept/reject,
and RETIRE the entire secret sample at the first rejection. The proposer may
adapt to earlier accepts and to public information jointly independent of
the sample, including independently acquired exact anchor evaluations.
The first-false-proposal argument from pass 7 gives

    P(any false scope is ever accepted before retirement) <=(D/q)^k.

True scope claims always pass in exact arithmetic. Thus any number of true
adaptive model revisions can share the same acquired true vectors, without
dividing delta by the number of proposals. An accepted scope can support
all-input skeleton repair, adaptive decision contrasts and algebraically
proved edits on this common event. A failed scope earns no repair guarantee.

For D=4, q=257, k=2 the lifetime bound is 16/66049, approximately .00024225.
Acquisition uses two full true vectors once per private epoch; each proposal
still pays k model evaluations and membership tests. Publicly obtaining a
good candidate U is an additional bill. Two private checks are not a complete
two-query range-learning algorithm. Four public independent range vectors
followed by these two checks are a possible six-vector successful path for
actual rank four, not a deterministic six-vector bound if the proposal fails.

Multiple retired epochs require a valid overall error allocation, e.g.
delta_e summable with k_e chosen so (D/q)^k_e<=delta_e. The dimension of U
can change, but the fixed-claim polynomial degree and exact membership duties
remain. Revealing residuals, query points, seed-dependent timing or checked
sketches invalidates the stated transcript restriction unless separately proved
safe. Host faults and unsound arithmetic are outside the ideal theorem.

Cheap failure screen: in one variable, the sequence x-a for all a in S
consists of false identities. If the verifier continues with the same point
after rejections, one is accepted with certainty. Retirement is essential.

This is an application of private randomized verification/PIT and the earlier
first-false lemma, not a new general reusable-holdout theorem. Compare against
an ordinary private PIT checker with the same transcript and restart rules.
The possible synthesis is cheap all-input correction for changing fallible
models under a common explicit evidence contract; complete costs and novelty
remain unassessed.
## Counterexamples can bound the number of private epochs

Maintain a monotonically growing public space U. On rejection, reveal a
checked residual outside U, add it to U, and retire every point in that
private batch before drawing the next one. Each rejection strictly increases
dim(U). If the union of all proposed model-error images lies in a space of
dimension r, there can be at most r rejections, regardless of model count.
Without a smaller proved bound, r<=n still holds. Within an epoch, public
seed-independent evidence may also enlarge U; this does not harm the lemma.

Use delta_j=delta/[(j+1)(j+2)] in epoch j=0,1,..., and
k_j=ceil(log(delta_j)/log(D/q)). The total probability of any false accepted
scope is <=delta; conditional first-false bounds plus a union bound suffice.
On a history with at most r rejections, at most sum_{j=0}^r k_j true vectors
are acquired. An unfinished epoch counts once. This is a finite acquisition
bound for arbitrarily many proposed models, not a bounded total runtime:
each proposal still costs its model evaluations and membership checks.

For D=4, q=257, delta=.001, the first five batch sizes are 2,3,3,3,3.
Thus a common rank-four error family needs at most fourteen true vectors
under this schedule. If the first public candidate space is already correct
for every proposed model, only the first two are needed. The price is growing
repair dimension and private computation. Learning a joint model-family space
directly, or proving model-edit image bounds, can be substantially better;
fourteen is not compared to the single-model seven-probe certificate as a win.

The finite probe [source](private_scope_probe.py) / [result](private_scope_probe.json)
enumerates all 125,000 pairs of degree-at-most-two polynomials and linear
subspaces in F5^2. All 108,624 false scope claims have at most two passing
points. Two private points with retirement give the sharp 4/25 example;
continuing after rejection accepts a false quadratic with probability one.
This is finite DEVELOPMENT evidence, not independent confirmation. Runtime
118,112,600 ns under Python 3.12.14; the result records the source hash.
