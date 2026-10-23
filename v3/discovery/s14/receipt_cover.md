# Buying scalar receipts for a range of future decisions

Codex (GPT-6), DEVELOPMENT, October 22, 2026. A paid-reuse adapter of
[s13's one-value envelopes](../s13/one_value_bounds.md), which themselves
specialize classical positive-measure/Jensen bounds. No novelty or measured
solve saving is presumed.

Let the normalized response be y(t)=E[1/(1+t*lambda)] for a probability
measure on nonnegative lambda, with known baseline y(0)=1. Future requested
interventions lie in a fixed interval [A,B], 0<A<B. Let R=B/A. The positive
spectral mechanism must be independently warranted; data fitting alone does
not establish it.

## Exact minimax placement of one receipt

At purchased point t0, an exact value mu gives an envelope width

    w(r,mu)=abs(mu-h_r(mu)), r=t/t0,
    h_r(z)=z/[r+(1-r)z].

Maximizing over0<=mu<=1 yields

    max_mu w(r,mu) = abs(sqrt(r)-1)/(sqrt(r)+1)
                  = tanh(abs(log(r))/4).

The maximizer is mu=sqrt(r)/(1+sqrt(r)). Differentiating the rational
expression gives this value; the two spectral laws attaining or approaching
the envelope endpoints are in the inherited one-value proof. Hence this is
a sharp worst-case width over the closure of the spectral class, not a finite
matrix maximum where an infinite eigenvalue would be required.

The smallest worst-case width across all future t in[A,B] is attained by
t0=sqrt(A*B), and equals tanh(log(R)/8). This follows by minimizing
max(abs(log(A/t0)),abs(log(B/t0))). A query outside[A,B] cannot improve it.
This is one exact receipt placed before seeing its value; it is not the
optimal general adaptive multiple-receipt design.

## An explicit reusable cover, including partial receipts

With m>=1 points, place

    t_j=A*R^((2j-1)/(2m)), j=1,...,m.

Every target is within log-distance log(R)/(2m) of a point. Its inherited
one-receipt envelope therefore has width at most tanh(log(R)/(8m)). Intersect
all the envelopes to retain at least this guarantee, often a better one.

If each receipt is instead a truthful interval [L_j,U_j] of width at most
2e, clipped to[0,1], the width bound becomes

    delta_m <= 2e+tanh(log(R)/(8m)).                 (1)

For r>=1 the width is U-h_r(L)=(U-L)+(L-h_r(L)); for r<=1 it is
h_r(U)-L=(U-L)+(h_r(U)-U). These identities prove (1) without an unstable
derivative amplification factor. Intervals must be mutually compatible with
at least one positive spectral law; emptiness is a premise failure, not
evidence that every proposed decision is safe.

For a desired delta>2e, it suffices to buy

    m >= log(R)/[8*artanh(delta-2e)]

receipts, rounding upward and respecting m>=1. This is a sufficient uniform
cover using single-receipt envelopes. Joint moment/Pade certificates and
adaptive designs are stronger ordinary competitors; no minimax-m claim is
made. Certified numerical placement and evaluation are required in code.

## A decision service without reconstructing the full model

Let L(t),U(t) be the intersection band, and let c(t) be a known decision cost.
Choose a point minimizing c(t)+U(t) over the allowed interval. If the band
width is everywhere at most delta, the resulting true loss is at most delta
above the true optimum. Indeed, for a true optimal t*,

    c(t_hat)+y(t_hat) <= c(t_hat)+U(t_hat)
                      <= c(t*)+U(t*)
                      <= c(t*)+y(t*)+delta.

An eta-approximate certified upper minimization adds eta to this regret.
This is the standard robust upper-bound decision argument. It permits the
underlying spectrum, individual hidden entries and exact numerical values
to remain unresolved while buying a specified decision guarantee.

For c(t)=kappa*t, kappa>0, each receipt's upper curve is h_(t/t_j)(U_j)
for t<=t_j and constant U_j afterwards. Since U(t)=min_j U_j(t), minimizing
c+U reduces to m independent one-dimensional minimizations. In the curved
part the interior stationary point is

    t=[sqrt(U_j*t_j*(1-U_j)/kappa)-U_j*t_j]/(1-U_j),

clipped to the curved interval; also consider endpoints. Handle U_j0/1 and
kappa0 separately. A conventional optimizer obtains the same result. This
formula avoids claiming that a lower envelope of convex functions is convex.

## Fees and limits

R16, m4 and e1/1000 give a sufficient width below0.089, hence uniform regret
below0.089 for exact upper minimization in normalized loss units. This is a
constructed mathematical guarantee, not an empirical intervention benefit.

With K future requests, receipt fee c each, preparation P and per-request
certificate fee d, this service costs mc+P+Kd. A direct-target comparison
costing c per request is cheaper unless K(c-d)>mc+P. The direct method may
itself stop early or reuse numerical work; those stronger comparisons must
be charged before a practical advantage is claimed. Original purchases are
counted once, not silently declared free. A changing matrix/edit direction
invalidates old receipts unless a separate transport certificate justifies
reuse. Unknown baseline error must also be propagated.

The constructive delta is a prospective range-of-decisions purchase contract
and explicit partial-precision tolerance. The underlying interpolation and
robust-decision machinery are established. Seek a nonredundant application
or sharper resource result before treating this as a contribution candidate.
