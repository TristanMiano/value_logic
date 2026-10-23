# A private randomized checker reused until its first rejection

Codex (GPT-6), October 23, 2026. DEVELOPMENT; first derivation, prior-work
comparison pending. This is a different acquisition direction from the
numerical value-receipt bounds.

## General proposed contract

Fix a truth relation T(c) for claims c, independent of a private random seed
R. A checker V_R(c) returns only accept/reject and has:

1. Perfect completeness: every true c is accepted for every R.
2. Pointwise soundness: for each fixed false c, P_R[V_R(c)=accept]<=delta.
3. No seed-dependent observations before an accepted claim, other than the
   single accept bit. In particular no residual, seed, or timing information
   is exposed to the proposer.

A fallible proposer can adapt its next claim to all earlier accepted
claims, their values, external observations independent of R, and its own
randomness. The service permanently retires this seed at its first reject.
Before retirement it releases only accepted claims.

**Proposed lifetime guarantee:** the probability of ever releasing a false
claim before retirement is at most delta, regardless of the number of true
claims or adaptive requests.

Couple the interaction to an ideal checker that accepts precisely true
claims. Condition on the fixed source and proposer/external randomness.
Until the first false claim, every actual accept bit is deterministic by
perfect completeness, so the two transcripts coincide and are independent
of R. The ideal transcript's first false claim c_star is consequently fixed
independently of R. If it is rejected, the actual service retires and has
released no false claim. If any false claim is ever released, c_star must
have been accepted. Pointwise soundness bounds that event by delta. If the
ideal trace contains no false claim, the event is empty. Integrating over
the independent source/proposer randomness preserves the bound.

This is an unconditional lifetime correctness event. It does not assert
that a chosen accepted claim has conditional error delta after conditioning
on its release. It also does not permit continuing to use this seed after
a rejection, exposing the seed, or treating an imperfectly complete test
as perfectly complete. Those changes break the argument's transcript step.

## Matrix-vector claims with one preprocessing pass

Let A be a fixed n-by-m matrix over F_q. Privately draw r uniformly in F_q^n
and compute g=A^T r exactly. For a proposed x and b, check

    r^T b == g^T x.

The intended truth relation is b=A x. Correct claims always pass. For a
fixed false claim the residual b-Ax is nonzero, so its dot product with r
vanishes with probability exactly 1/q. The lifetime contract therefore
allows adaptive x and b using this one private fingerprint, until the
first rejection, with failure probability at most 1/q.

Preprocessing costs one exact transposed matrix-vector product, plus
sampling/storing n field elements. Each proposal costs n+m field products
and the corresponding sums, plus construction of x and b and the proposal
itself. Comparison with exact recomputation must count the latter costs.
A cheap approximate/low-rank model can help only when it often gives an
EXACT product on the requested inputs. Nearness over a real norm is not
exact finite-field correctness, and rounding would change this contract.

On rejection, an ordinary exact fallback may answer the current query,
but subsequent requests must use exact computation or a fresh independent
fingerprint. With preassigned error ceilings delta_j for refreshed epochs,
sum(delta_j) bounds lifetime failure by a union bound. Rebuilding the
fingerprint, fixing the model and all failed proposals remain paid.

## Early limits and proposed usefulness screen

- Revealing r allows a proposer to choose a nonzero residual in its kernel
  when n>=2. A public Freivalds-style challenge does not have this reuse duty.
- Rejection feedback while retaining the same seed can progressively learn
  a favorable residual; the fail-stop rule is load-bearing.
- A full exact matrix-vector prover plus this checker loses total work to
  the exact product alone. The plausible source is cheap model-generated
  proposals with checked fallbacks, not moving unpriced work to a prover.
- A model whose correctness pattern depends on a secret seeded sketch
  violates the stated independence unless separately analyzed.
- A mathematically fixed source can still have fallible proposed values.
  The randomization bounds the chance of accepting a false proposal; it
  does not put a probability distribution on unresolved mathematical truth.

The first cheap screens should identify the closest reusable private
verification literature, construct an explicit failure of same-seed reuse
after rejection, and price a model/proposal duty against a direct ordinary
method. The generic first-false-claim argument may already be established;
it must not be advertised as novel before that comparison.

## First source screen and a stronger observation

AppendixB.1 of Dumas--Zucca and Section3.2 of Slalom explicitly contain
the private fingerprint/preprocessing mechanism. It is established, not a
new invention here; see [read scopes](literature.md). The narrower
lifetime/retirement contract remains a comparison question.

Perfect completeness is actually unnecessary for the stated lifetime
error guarantee. Fix the source and all randomness other than R, and run
the proposer along the hypothetical **all-accept transcript**. This fixes
its first false claim independently of R. An actual run either retires
before that point or presents that same claim; any false release requires
accepting it. Pointwise soundness still bounds that event by delta.
Perfect completeness only prevents needless retirement on true claims.
The initial proof above is valid under its stronger premise, but the
initial warning that imperfect completeness itself breaks correctness was
overrestrictive. No failed execution is hidden by this refinement.

For a concrete failure of reuse AFTER rejection, work over F2 with n=2.
Submit false residual e1, then e2 if rejected, then e1+e2 if both rejected.
For every private r in F2^2, some false residual is accepted within three
checks. With permanent retirement at the first rejection, the failure
probability is exactly1/2. Thus private randomness alone does not justify
unrestricted reuse, even with perfect completeness.

Versioned rank-one source edits can retain the same private seed while
updating g exactly: if A_new=A+u*v^T, then

    g_new=g+v*(u^T*r).

This costs linear work in the two dimensions, in addition to acquiring
and validating the edit. The all-accept argument permits adaptive edits
whose source semantics and values are independent of R along that
transcript. It does not permit exposing g or unchecked edits. This is a
standard linear update used within the proposed lifetime adapter.
