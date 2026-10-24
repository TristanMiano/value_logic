# Keep a private check while buying public repairs

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass32.
This extends the feedback contract in s15/private_scope.md; its historical
retirement guarantee is preserved. Generic randomized checking and union
bounds are established. Complete novelty/economics remain unassessed.

## Count false proposals, not successful revisions

Let an exact one-sided randomized checker accept every true claim. Each
fixed false claim passes with probability at most epsilon. Its random seed
is private; only the Boolean result is exposed. Public evidence and proposer
randomness are jointly independent of the seed. Reuse the seed, but stop
after B rejections (or otherwise ensure at most B false claims on the ideal
transcript). Then

    P(any false claim is accepted) <= B*epsilon.       (1)

There is no multiplier for arbitrarily many true claims. To prove this,
fix the entire independent public random tape and follow the deterministic
ideal transcript which accepts exactly the true claims. Before the first
false acceptance the actual transcript equals this ideal one. Its first B
false claims are therefore fixed independently of the private seed. A union
bound over them proves (1). Average over the public tape afterward.

The distinction in the stopping rule matters: allowing B rejections AND
one more possibly false proposal uses (B+1)*epsilon. Revealing a private
counterexample, sample-dependent timing, or an unprotected sketch invalidates
this proof. Continuing through unbounded rejections can fail with probability
one, as the historical x-a example already shows.

More generally, a checker can reserve a fixed-claim error charge before each
query, deduct it on rejection and refund it on acceptance. If the charges
along every ideal all-correct transcript sum to at most delta, the first-error
argument bounds any false acceptance by delta. This is a lifetime error
budget, not a posterior probability that a particular accepted claim is true.

## A rank-bounded repair service

Use the polynomial scope interface: A is a fixed vector polynomial; every
admissible model B has deg(A-B)<=D. All error images lie in a common unknown
linear space R with proved dim(R)<=r. Maintain a PUBLIC U subset R from
actual checked residuals, initially dimension d0. Draw k private grid points,
q>D choices per coordinate, and acquire A at them. Check each proposed
scope A-B in U at all k points, exposing only accept/reject.

On rejection, do NOT expose or recycle a private residual into public U.
Instead draw fresh independent PUBLIC points until a residual A(x)-B(x)
outside U is found. Add that vector to U. Each such repair increases dim(U),
so on the ideal transcript there are at most r-d0 false scope proposals.
Once dim(U)=r, the common-rank promise implies U=R and further scope checks
are unnecessary for admissible models. Thus one private batch suffices with

    P(any false all-input scope accepted) <= (r-d0)*(D/q)^k.    (2)

If no smaller rank bound is warranted, use r=n. A degree promise, exact
membership arithmetic and a fixed admissible-family/common-space promise
are actual assumptions. They are not learned merely by passing this test.

For each genuinely false scope, a fresh public point produces an outside
residual with probability at least1-D/q. This follows by fixing one nonzero
annihilator polynomial. Conditional on the current history, the new point is
independent. Public search therefore needs at most q/(q-D) truth-vector
queries in expectation per repair. On the event that the private checker
rejects, falsity is certain; no false rejection occurs in exact arithmetic.

The expected total truth-vector acquisition, including the sealed sample, is

    k + (r-d0)*q/(q-D).                              (3)

The public search has an unbounded tail; a capped search may abstain, and
must not silently accept when its cap is reached. Per-proposal model calls,
membership arithmetic, construction of U, storage and all degree/rank
warrants remain paid. Unlimited true proposals do not mean finite runtime.

## Worked resource comparison and its limits

For D=4, q=257, r=4, d0=0, k=2, equation(2) gives

    64/66049 < .001.

Equation(3) is 2+4*257/253 =1534/253, about6.06324 true vectors.
The s15 retirement schedule's first five private batches have sizes2,3,3,3,3,
giving a fourteen-vector upper bound when four publicized private failures
retire their batches. Here private acquisition is two vectors, while separate
public counterexample search is added. This compares an expected upper bound
with a prior fixed upper bound under different feedback rules; it is NOT an
observed56.7% saving or a universal advantage over ordinary range learning.

A two-public-probe cap per repair uses at most ten truth vectors including
the initial batch. The probability of any public search failing within its
cap is at most4*(4/257)^2. Such failure leads to abstention, not an unsound
scope. Keep this completeness probability separate from (2)'s soundness.

Strong controls include ordinary private PIT with this same feedback rule,
direct learning of the common error space when the family is accessible,
symbolic error-span proofs, and a fresh private batch with no public search.
An identical ordinary implementation ties. The possible synthesis is a
concrete way to preserve expensive sealed truth evaluations across changing
fallible models, while learning corrections from separately paid evidence.

## Strengthening the comparison before calling it a gain

The fourteen-vector historical schedule is not the strongest fresh-batch
control for this newly declared rank bound. Since dim(U)=r certifies completion,
there is no need for a final fifth batch. Allocate delta/r to each of at most
r fresh epochs. In the worked case k=2 in every epoch already suffices, so
this control acquires at most EIGHT true vectors. It reveals a failed private
residual and retires its batch; no additional public search is needed.

The persistent-private expected bound6.06324 is about24.21% below that
eight-vector bound. This can be a resource comparison for a stream containing
a true accepted proposal before each of four rejected scope proposals:
each fresh epoch then has to acquire both validation vectors. It is still
a constructed access contract, not an observed application saving. If every
first proposal is false, a lazy fresh checker can often stop after its first
truth-vector call and be cheaper. Both policies need the same complete
pricing and the proposer must not observe private sample-dependent timing.

Grid size is another strong control. If evaluation bit complexity and the
input interface permit q=16000, k=1 has4D/q=.001 and expected acquisition
at most1+4*16000/15996, about5.00100 vectors. Larger inputs can cost more;
keeping q=257 fixed is an interface restriction, not universally optimal.
Do not advertise the comparison to fourteen while omitting these controls.

## A finite leak counterexample

private_repairs_probe.py enumerates42 independent-public outcomes over F7
and seven outcomes of a leaky variant. Take A(x)=(x,x^2), U=0, B=0.
After a rejection, a fresh nonzero public point b yields U=span(b,b^2).
Propose B'=A-(x-b)e1. Its scope is false, and it passes only when the
secret point equals b. Including initial false acceptance, the exact failure
rate is2/7, below the two-proposal degree bound4/7.

If instead U is built from the PRIVATE failing point a, even publishing only
U discloses a via its slope. The same proposal with b=a then passes falsely;
the overall failure rate is1. The hidden-point premise is substantive.
The probe uses exact field arithmetic, records source hash/version/runtime,
and is finite DEVELOPMENT evidence only.
