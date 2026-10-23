# Learn useful output comparisons when a complete linear model is usually wrong

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass15.
Combines product_scope.md and the private-checker lineage. Randomized range
finding and annihilator duality are ordinary methods; no generic novelty claim.

## Fixed mathematical source

Let the true source be a fixed linear map A:F2^m->F2^n and the fallible model
be B of the same shape. The linearity and version binding are separately
warranted. Write E=A-B, with unknown rank d. A paid random probe draws
u uniformly from F2^m and acquires BOTH Au and Bu, hence Eu. This is an
actual pair of model/source evaluations, not a free residual-vector oracle.

Apply product_scope.md's range-stopping rule to these residuals: retain their
span S_t and stop when total redundant probes t-dim(S_t) reaches h. The
existing exact rank calculation gives

    P[S_stop != image(E)]
      = 1-product_(ell=h to d+h-1)(1-2^(-ell))
      < 2^(1-h),                                      (1)

for d>0, and zero failure for d=0. The number of probes is at most d+h.
The unknown rank is not supplied to the algorithm.

On the one successful range event, the learned set of safe output parities
is exactly T=S_stop^perp. Every t in T satisfies

    t*A*x = t*B*x for EVERY x.                         (2)

If t is outside T, a source input x with t*E*x=1 exists, so no universal
agreement claim for that parity is justified. Thus T is maximal for this
universal linear-comparison duty. Once the common event holds, later x,t
choices can be arbitrary and adaptive. There is no per-use union penalty.

Example: n=128,m=256,d=4,h=11. At most15 paid source/model pairs learn a
124-dimensional protected parity space, with failure upper below1/1024.
For uniform inputs the COMPLETE model agrees with A only2^(-4)=1/16 of
the time, yet all these parities are exact on the common range event.
This repairs a different usefulness duty after collision_corrector.md's
linear-mismatch rejection: it does not claim to correct the whole vector.

## Comparisons and economics

An ordinary randomized range finder given the same paired evaluations ties.
A predeclared candidate protected space can be checked more cheaply without
learning the maximal space; it is a different information duty. Recovering
all256 input columns is an unnecessarily strong baseline for(2), so its
larger bill is not a claimed comparative speedup. Basis insertion, full
source/model evaluation, parity application, storage and all rejected
probes remain paid. If d is large, the discovery cost can erase the benefit.

Equation(2) is distribution-free over future x because the source is a fixed
linear operator. It is not a learned causal-intervention semantics. If x is
an intervention description, the interpretation Ax must itself be justified
by the executable/physical contract.

## Multiple revisions: an early invalid shortcut

For k predeclared versions E_1,...,E_k, one could learn the joint image of
the block operator [E_1 ... E_k]. A uniform block probe requires evaluating
every E_j on its sampled input and summing; it pays k source/model pairs.
It does not become one call merely because the block notation is compact.

Choosing one random version per probe does NOT preserve(1). If exactly one
version has a rank-one nonzero error and all others have zero error, a
uniform version/input probe is nonzero with probability1/(2k). After h
zero probes the chance of falsely declaring a zero joint image is

    (1-1/(2k))^h,

which can be near1. The half-probability rank argument requires an actual
uniform vector in the joint image, not a mixture that misses rare versions.
This blocks a tempting cheap counterfactual-transfer claim before a harness.

## Private checking as an alternative acquisition interface

A privately retained batch of independently sampled Au vectors can instead
check proposed linear claims t*(A-B)=0 by evaluating t*(A-B)u. Under the
private-checker contract, first-false-claim control supports arbitrary
accepted claims until the first rejection; the source batch need not be
refreshed after each acceptance. A rejection retires that batch before its
contents are disclosed or used to adapt further proposals. This is a
different duty from public maximal-range discovery.

The model B and t must be fixed independently of the hidden probes given
the permitted accept-only transcript. If model evaluation leaks the probe
to its proposer, or if public residual vectors are reused as private tests,
that premise fails. Trusted linear-map evaluation and the absence of extra
channels are parts of the interface, not an assumed property of arbitrary
black-box model programs. No measured performance claim is made here.
