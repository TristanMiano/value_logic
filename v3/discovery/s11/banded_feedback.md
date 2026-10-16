# Exact feedback for bounded displacements of a reasoning order

Codex (GPT-6), DEVELOPMENT derivation. Extends the local-feedback candidate;
the local information bound, rather than a new online-learning principle, is
the proposed useful delta. Literature priority remains unresolved.

## Interface

The base order is 1,...,n. Query i returns a fixed value x_i and incurs a fixed
nonnegative fee c_i. A checked predicate Stop(R) is monotone under adding true
receipts and depends only on the acquired identity/value set. All policies
stop immediately when Stop is true; if none succeeds they use the same fallback.
Assume Stop(empty) is false; otherwise no query is required. Altering the
computation order does not alter the returned values or the predicate.

For integer d>=1, the candidate family P_d consists of permutations sigma for
which every item i changes position by at most d. The reference execution
stops after L receipts (or obtains all n without a certificate).

## Upper information bound

If a certificate was found, its receipts are contained in the base prefix
1,...,L. In every sigma in P_d, all those items have appeared by position
L+d. Let tau be the position of the last member of this base prefix. The
candidate has stopped by tau, by monotonicity. The item at tau has identity
<=L. Every earlier queried item j has position at most tau-1, so

```math
j\le (\tau-1)+d\le L+2d-1.
```

Consequently the base receipts plus the next min(n-L,2d-1) values determine
the complete cost of EVERY candidate in P_d. Any later unknown value is
provably irrelevant to its execution. If the base never obtains a certificate,
all n values were already bought, and there is no missing information.

This counts additional acquired values, not algorithmic work to enumerate
or optimize the family. The bound is independent of the unknown dependence
between values. It is a counterfactual change of the computation procedure,
not an intervention claiming to change mathematical truth.

## Matching worst-case lower bound

Use the first-positive stopping rule and strictly positive fees. Let base
values before L be zero, value L be one, and all later values be zero. Assume
n>=L+2d-1. The observed base trace is fixed. Each tail identity j in
{L+1,...,L+2d-1} can precede L in an allowed permutation:

- For j<=L+d, swap j and L directly.
- For j>=L+d, exchange the adjacent length-d blocks starting at L; every
  element moves exactly d places, and j is in the first exchanged block.

Changing only that unobserved x_j from zero to one leaves the base trace
unchanged but makes the corresponding candidate stop strictly earlier and
pay strictly less. Thus any exact all-family feedback procedure must query
every one of these 2d-1 values in this worst case. Adaptivity does not help:
on the all-zero tail every unqueried coordinate retains such an indistinguishable
alternative. With a truncated tail the same argument covers every available
item, using a suitably shorter exchange where necessary; the untruncated
2d-1 bound is the asserted matching construction.

At d=1 this gives one extra receipt for all permutations made of disjoint
adjacent exchanges, a larger family than the single-swap neighborhood.

## A compact policy automaton

A permutation prefix is an acquired identity set S of size t. Bounded
displacement means every i<=t-d is already in S and no i>t+d is in S.
The remaining choice lies in the frontier of at most 2d identities. A valid
next item j has j not in S and |j-(t+1)|<=d, and the resulting set must contain
every i<=(t+1)-d. These local conditions characterize exactly P_d by induction.
This gives O(n*4^d) states as a loose bound, each with at most 2d+1 choices.
No claim is made that the loose state count is tight.

For a fixed complete context, the loss of choosing j after S is
c_j 1{not Stop(x restricted to S)}. Add the shared fallback independently.
Every path's accumulated loss is exactly its execution bill even though the
automaton lists all n positions. After a certificate, subsequent transition
losses are zero. The limited receipt set above is enough to compute all
reachable transition losses: if S contains the base certificate, loss is zero;
otherwise an item in S outside the available prefix would imply all base
certificate identities have already appeared, by the same position argument.
This last claim needs careful implementation checking before relying on it.

Exponential weights over paths can then use ordinary forward/backward weighted
path sums, with edge weights updated by their cumulative revealed losses.
That is standard dynamic-programming aggregation of a large expert family.
The contribution question is whether this exact feedback interface plus a
small frontier gives a useful paid learner for local changes, not whether
path aggregation itself is new.

Prospective cheap screen: enumerate all bandwidth-d permutations for small n
and compare the frontier generator; enumerate short binary contexts and verify
the limited receipts determine every cost. Check the lower construction for
d=1,2,3. Do not start a large learning benchmark before this passes and the
closest literature is checked.

## The learner's execution order changes the acquisition bound

The 2d-1 bound above executes the FIXED reference order. A learner competing
over P_d will instead execute some pi in P_d. Do not silently reuse 2d-1 for
that different duty.

Let its certificate trace have L receipts, acquired identity set R, and
M=max(R). Because pi has displacement at most d, M<=L+d. Every candidate
has acquired all members of R by position M+d. The last such member has
identity <=M; every earlier item has identity <=M+2d-1. Hence purchasing
every missing item in the REFERENCE prefix through min(n,M+2d-1) determines
all candidate bills. All L existing receipts lie in this prefix, so the
additional count is at most 3d-1. This may query identities earlier than the
last observed reference identity, not merely append a tail to the executed
order. The exact acquisition list is part of the construction.

This larger worst-case bound is tight. Put the unique positive at reference
identity i=L+d and move it d places earlier in the executed order, shifting
the d intervening items one place later. The observed set is {1,...,L-1,i}.
It omits d items below i and 2d-1 items immediately above i. Each omitted item
can precede i in a candidate: the lower items in the identity order, the higher
items by the direct-swap or block-exchange construction above. On the all-zero
unobserved vector, every omitted value is necessary to distinguish a changed
candidate cost. Assume enough room after i. Thus 3d-1 additional values may
be necessary for exact all-family feedback after an arbitrary family member.

## The loss range also stays local

Let the fixed reference stop at L0 and a candidate stop at tau. Every reference
certificate item is acquired by candidate position L0+d, so tau<=L0+d.
Conversely the candidate's certificate consists only of reference identities
<=tau+d, so the reference must stop by tau+d, giving tau>=L0-d.

The candidate's acquired set contains every identity <=tau-d and none above
tau+d. At most d items can be added to the reference's acquired prefix and
at most d omitted. For omissions use the identity
omitted=L0-tau+added together with added<=max(0,tau+d-L0); for additions use
omitted<=max(0,L0-tau+d). Thus each bill differs from the reference by at most
d*c_max in either direction, and the all-family loss range is <=2d*c_max.
Fallback costs cancel because the existence of a full-set certificate is
order-independent. If none exists all orders buy every item and pay the same
fallback.

This is a range bound for the specified fixed-fee predicate interface, not
for arbitrary program edits. A paid online learner must use the 3d-1 feedback
bound, include its computation work, and compare with a clearly named fixed
local family. The narrower class is a tradeoff for inexpensive counterfactual
information.

## Cheap finite screen and ordinary control

[bf01](bf01/attempts.jsonl) runs the immutable [screen](banded_probe.py) on five
small binary panels, n=5--7, d=1--3, with first-positive, threshold, two-sided
and DNF predicates. Every candidate permutation was compared with a separate
brute permutation filter; every binary world was checked, for up to four
selected executed orders. All five first attempts passed. The largest family
has 675 policies represented by 70 states and 170 edges. Totals: 354,048
counterfactual replays, 108,000 graph-edge checks and 118,016 loss-range checks.
Separate indistinguishable-world constructions require 2, 5 and 8 additional
values at d=1,2,3 after a chosen family member. These are finite DEVELOPMENT
checks, not empirical confirmation or a complete independent proof review.

Short panels sometimes need every remaining value: three cases give no or
very small reduction over full acquisition. The constant-in-n bound matters
when the reference has a substantial unused suffix, not automatically in every
task. Fees and receipt counts here are simulated; no actual audit service was
purchased.

[Gyorgy et al. (2007)](https://www.jmlr.org/papers/volume8/gyoergy07a/gyoergy07a.pdf),
Theorem 3 and its dynamic-programming proof, already implement weighted path
sampling in O(edges) per round. Their partial-monitoring algorithms are strong
ordinary controls: executing a complete preselected permutation reveals all
losses on that path, because every edge after the stopping certificate has
known zero loss. Thus paid full-family feedback is optional. A total-cost
benefit cannot be inferred merely from beating an all-values feedback arm.

## A conservative paid-learning consequence

Fix an oblivious sequence of value vectors and a fixed local comparator family.
Use exponential weights on the paths and independently buy complete local
feedback with probability rho>0 after execution. On audited rounds use all
edge losses divided by rho; otherwise update by zero. These estimates are
unbiased. A path-independent shift of estimated losses leaves the distribution
unchanged. The Hoeffding potential argument therefore uses the FAMILY range
R=2*d*c_max, even though the unshifted full path bill can be much larger.

For any fixed comparator path, the expected execution regret is at most

```math
\frac{\log N}{\eta}+\frac{\eta R^2 T}{8\rho}.
```

The second term follows by taking expectation of the squared estimated range:
it is R^2/rho^2 on the rho fraction of audited rounds and zero otherwise.
Optimizing eta gives R*sqrt(T*log(N)/(2*rho)). Add at most A*rho*T in
feedback fees, A=(3*d-1)*c_max, and all representation, predicate checking,
sampling and updating work. With rho capped at 1, the interior minimizer is
(R^2*log(N)/(8*A^2*T))^(1/3). This is the conventional label-efficient
T^(2/3) tradeoff with a locally bounded acquisition fee; it is not a new regret
principle or a superiority theorem over ordinary semi-bandit methods.

The bound concerns expectation over private learner randomization against a
fixed sequence. Do not silently promote it to adaptive hindsight regret or
claim the fixed reference's smaller 2d-1 fee for an executing learner.
