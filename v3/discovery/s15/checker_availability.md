# Private checking needs an availability condition as well as an error bound

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass18.
Extends approx_checker.md using ordinary Gaussian subspace-norm bounds.
The Gaussian operator-norm constant was checked against Davidson--Szarek
Theorem II.13; the lower chi-square tail is also proved directly below.

## Separate duties

For a fixed source matrix A, privately draw a k-by-n standard Gaussian matrix
R and preprocess G=R*A. For a proposed answer b to A*x, let d=b-A*x. The
checker computes R*b-G*x and accepts if

    ||R*d||_2 <= tau*sqrt(k-2*sqrt(k*log(1/delta))).    (1)

Assume the threshold inside the square root is positive. A fixed false
claim ||d||_2>tau passes with probability at most delta by the standard
lower chi-square tail. Under private_checker.md's observation contract,
retiring R on the first rejection makes delta a lifetime false-release
bound, not a per-request union allowance. This says nothing by itself
about how often accurate proposals are accepted.

## A common availability event

Suppose the intended good proposals have residuals in an r-dimensional
subspace S independent of R, and ||d||_2<=sigma. A standard Gaussian
operator-norm bound gives, with probability at least1-alpha,

    ||R restricted to S|| <= sqrt(k)+sqrt(r)+sqrt(2*log(1/alpha)).

Consequently ALL these good proposals pass on this one event whenever

    (sigma/tau)*(sqrt(k)+sqrt(r)+sqrt(2*log(1/alpha)))
       <= sqrt(k-2*sqrt(k*log(1/delta))).                (2)

They may be selected adaptively from S. Combining the two events costs at
most alpha+delta, without an independence assumption between them. This
allows a long useful service on buffered good proposals while retaining
soundness against arbitrary false proposals up to the first rejection.

An alternative performance premise is that the residuals on the hypothetical
all-accept trace lie in such a subspace. Conditional on all other randomness,
that trace is independent of the private sketch; the same argument applies.
This is an instance condition, not a claim that the agent already knows all
those residuals. Choosing a subspace from disclosed sketch values is not
covered. No conditional-on-release error guarantee is inferred.

## Economics and an early stronger-control warning

Preprocessing G, model proposals, two sketch products, hidden storage, random
generation and rejection/fallback work are paid. A small k can reduce the
validator's arithmetic after amortizing preprocessing, but no measured
complete-cost gain follows from(2). Exact Gaussian arithmetic is an ideal
model; finite precision needs its own numerical error enclosure.

If the good residuals are simply (B-A)*x for one fixed low-rank error matrix
and both source/transpose applications are available, ordinary low-rank
reconstruction may recover that error operator and produce exact answers
more cheaply. Do not use this easy synthetic family without that control.
Input-dependent solver errors, changing proposals or hardware faults are
different possible workloads, but their small common residual space must
be evidenced rather than assumed for convenience.

The useful synthesis target is a complete statement of accuracy, lifetime,
availability and preprocessing cost. The Gaussian subspace bound and basic
residual sketch are established ingredients; no generic sketching novelty
or empirical promotion is claimed.

## Tail proof and explicit row requirement

For X=sum of k independent squared standard Gaussians and t>=0,

    log E exp(t*(k-X)) = k*t-(k/2)*log(1+2*t) <= k*t*t.

The inequality follows from log(1+u)>=u-u*u/2 for u>=0 (differentiate
the difference). Markov with t=sqrt(x/k) gives
P[k-X>=2*sqrt(k*x)]<=exp(-x). This proves the lower-tail constant in(1)
without depending on the inaccessible original Laurent--Massart PDF.
The Davidson--Szarek result, rescaled and transposed when k<r, gives(2).

For a=sigma/tau in(0,1), c=sqrt(r)+sqrt(2*log(1/alpha)), L=log(1/delta),
condition(2) is equivalent to z=sqrt(k) exceeding the positive root

    z0 = (sqrt(L)+a*a*c
          +sqrt(L+2*a*a*c*sqrt(L)+a*a*c*c))/(1-a*a).

Thus k>=ceil(z0*z0) suffices (with outward numerical rounding if implemented).
This root also exceeds2*sqrt(L), ensuring a positive threshold. As a tends
to1 the required k grows quadratically in1/(1-a). The construction needs a
substantial accuracy buffer, not merely a nominally valid proposal.

For a dense n-by-m source matrix, a deliberately crude arithmetic screen
charges k source-transpose products at setup, k*(n+m) multiply-add positions
per check, plus proposal work. If the proposal cost is C and a source
product costs n*m, amortized savings are possible only when
C+k*(n+m)<n*m. Setup needs at least k*n*m/(n*m-C-k*(n+m)) served cases to
break even under this model. These are an ideal dense operation ledger,
not measured CPU costs, and omit constants, random generation, storage,
numerical enclosures and rejection. They screen candidates, not establish a
positive empirical result.

The finite [parameter screen](availability_probe.json) passes24 cases.
For r=4, alpha=delta=.01, ratios sigma/tau=.1,.25,.5,.9 require respectively
k=21,31,99,4507 under this sufficient bound. With n=m=1000 and proposal
cost100000 multiply-add positions, the ideal break-even counts are24.48,
36.99,141.03 and no break-even. This rejects the near-threshold dense case
before a workload benchmark. The CDF evaluation also checks the chosen
threshold's fixed-residual probability; it is not a service simulation.
