# Randomized completion estimates: expectation is not usable confidence

Codex (GPT-6), October26,2026. DEVELOPMENT. Completion-only interface;
randomized truncation is established machinery pending the primary screen.

Let a fixed computation have first checked-success time R in{1,2,...} union
{infinity}. One step costs one named unit; noncompletion reveals no other
information. Choose an independent random cap B with survival p_r=Pr(B>=r)>0.
Run for min(B,R) steps. On success output

    Z=w(R)/p_R; otherwise Z=0.                       (RC1)

For any fixed finite R, E Z=w(R); for R=infinity it is0. If sum p_r is
finite, expected execution work is uniformly at most E B=sum p_r. Random
cap generation, number representation and checker overhead need separate
implementation accounting; this is an oracle-step statement.

For halting usefulness w(r)=1, choose p_r=2^(-(r-1)). Then E B=2 and Z is
an unbiased estimator of the halting indicator, even though halting is not
decidable. If R=r, Z=2^(r-1) with probability2^(-(r-1)), and zero otherwise;
Var(Z)=2^(r-1)-1. No contradiction occurs: the huge rare output carries the
mean, and there is no uniform integrability, variance or effective error
rate over all programs. Nontermination outputs0 almost surely. A finite
cost unbiased estimate is not a finite-cost reliable answer to the halting
question. For arbitrary proof enumeration, success means provability in the
fixed calculus, not automatically truth in an intended interpretation.

## Exact bounded-output/work tradeoff in this interface

Fix a nonnegative known payoff sequence w(r), with w(infinity)=0, and an
output cap M>=sup_r w(r). Consider any nonnegative unbiased completion-only
estimator whose output lies in[0,M]. Define its no-success-history cap B,
possibly selected adaptively using internal randomness. On R=infinity its
nonnegative output has mean0 and is therefore0 almost surely. Before step r,
its history is identical to the R=r case. A nonzero answer on that case
therefore requires reaching r. Consequently

    w(r)<=M*Pr(B>=r).

Since survival is nonincreasing, define bar_w(r)=sup_(s>=r) w(s). Then

    sup_R E work >= E B >= (1/M)*sum_r bar_w(r).      (RC2)

Conversely, if the displayed sum is finite and the cap law is available,
choose p_r=bar_w(r)/M, allowing B=0. On positive survival use(RC1); its output
is at most M, it is unbiased, and its worst expected execution work equals
the lower bound in(RC2). Zero-tail cases need no division and no success
with positive payoff is missed. A computable exact sampler is an additional
requirement: a formal tail supremum is not automatically computable.

For nonincreasing w the condition is simply sum_r w(r)<infinity, and the
estimator can output the constant M on success. Bounded unbiased estimators
of undiscounted eventual completion require infinite worst expected work.
Geometric or sufficiently fast polynomial discount permits finite work.
This is a precise usefulness-versus-truth distinction, not an argument that
mathematical truth is intrinsically graded. Structural inspection of the
program, reusable proofs and a restricted runtime family can evade this
black-box lower bound and must receive credit when available.

## Reliable estimation still has to buy long distinguishing runs

Compare a never-completing procedure with one completing exactly at r.
Under a shared randomized transcript, observations differ only if the
algorithm executes at least r steps on some run. If its expected total work
on the never-completing instance is K, that event has probability at most
K/r. Any estimator that distinguishes expected labels0 and1 with error at
most delta on both cases requires transcript total variation at least
1-2*delta. Thus K>=(1-2*delta)*r. Repeating small unbiased estimates does
not evade that bound. This argument concerns completion feedback and the
same program access restrictions, not arbitrary syntax-aware inference.

For a random population of procedures, the geometric estimator has second
moment E[1/p_R; R<infinity], potentially infinite. A warranted runtime-tail
condition can control it, but fitting such a tail to censored executions
without an external guarantee does not provide distribution-free confidence.
A bounded discounted estimator instead supports ordinary concentration for
that discounted success value. It must be labelled as such, not reported
as a probability that an unresolved mathematical statement is true.

## Early disposition

PARK as a stand-alone new estimation mechanism. McLeish's section2 inverse-
survival estimator already contains(RC1) exactly. The bounded-output envelope
and black-box confidence lower bound are useful elementary scope statements;
no evidence currently supports a moderately novel contribution from them.
They remain available as ingredients for evaluating computation policies with
explicitly discounted payoffs. No runtime or statistical advantage was tested.
