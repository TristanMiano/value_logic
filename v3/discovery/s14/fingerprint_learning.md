# Learning a jointly usable model with randomized filters and paid audits

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. A synthesis candidate,
with a decisive access-cost limitation. No new general fingerprinting or
sequential-testing principle is claimed.

## Mechanism and invariant

Use the fixed r-dimensional model-error syndrome z(X) from
learn_affine_warrants.md, with iid cases. Let S_star span the support of z,
and d=dim(S_star). Start with retained coefficient space K_0=F2^r.
For each fresh case, sample a uniform NONZERO a in the current K and buy
the exact linear measurement Y=a*z. If Y=0, keep K. If Y=1, buy enough
additional independent measurements to reconstruct the functional z on K,
then replace K by K intersect ker(z). The positive measurement counts toward
this full audit, so the additional bill is dim(K)-1 measurements.

Each positive audit removes exactly one dimension and preserves every
population-valid equation in S_star-perp. Thus there are at most d positive
audits and at least r-d valid equations remain. Negative fingerprints may
miss a violating case: the final K is NOT guaranteed consistent with all
sampled worlds. Earlier sample-consistency/compression bounds cannot simply
be reused.

Let p(K)=P[z is not orthogonal to K], the risk that ANY retained equation
fails on a new case. Conditional on the past and dim(K)=k>0,

    P(Y=1 | past) = [2^(k-1)/(2^k-1)] * p(K) >= p(K)/2.

K only shrinks, so p(K) never increases. This is the crucial resource/reliance
invariant; individual equation accuracies are not substituted for joint risk.

## A simple anytime-valid acceptance rule

Fix desired epsilon,delta in(0,1), u=epsilon/2, and
A=(1-u/2)/(1-u)>1. After N fingerprints and J positive audits define

    M_N = (1/2)^J * A^(N-J).

Accept when M_N>=1/delta, or immediately if K={0}. Then, with probability
at least1-delta, every accepted K has p(K)<=epsilon, simultaneously over
all stopping times. Later subspaces of an accepted K inherit its guarantee.

Proof: while p(K)>epsilon, the conditional positive probability mu is>=u.
The multiplicative factor has conditional expectation
mu/2+(1-mu)*A<=1. Stop this nonnegative supermartingale at the first time
the decreasing p(K) falls below epsilon. Ville's inequality bounds the
chance of crossing1/delta while risk is still above epsilon. The audit
updates depend on observations, but the next random measurement and iid
case are fresh. No optional-stopping or post-selection exemption is assumed.

Because J<=d, acceptance occurs by any integer N satisfying

    A^(N-d) >= 2^d/delta,

unless K already became zero. The number of paid linear measurements is
at most

    N + d*(r-1) - d*(d-1)/2.                            (1)

The cutoff depends on the unknown population support rank only as an analysis
bound; the implementable stopping rule uses N,J and M_N. If source law drifts,
the iid/monotone-risk argument does not carry over automatically. Multiple
changing epsilon choices need a simultaneous construction, not repeated use
of the same delta. Coverage is unconditional per new case, not conditional
on an adaptively filtered release subset.

## What is actually paid, and an early rejection

(1) counts arbitrary LINEAR measurements, not primitive coordinate reads.
Dense fingerprint formation, basis updates, full audits, storage and server
computation are additional resources. A defensible native service is a remote
checker that already computed each syndrome and charges for returned bits;
then the saving concerns communication, while its computation remains paid.
No such application has been implemented here. Dense matrix-vector examples
do not automatically work: a strong ordinary implementation can often compute
the whole residual vector for about the same cost as one scalar fingerprint.

Coordinate-only access gives a useful obstruction. Under the all-zero
reference, require an algorithm always to retain/accept the complete r-rule
model. For each j, consider an alternative whose syndrome is e_j with
probability rho>epsilon and zero otherwise, independently between cases.
If it checks coordinate j on N_j distinct cases along its all-zero path,
the probability of that indistinguishable path is (1-rho)^N_j. Soundness
at level delta therefore requires N_j>=log(delta)/log(1-rho), for every j.
Total reference cost is at least r*log(delta)/log(1-rho). For randomized
reference-complete algorithms, Jensen gives the same bound in expectation.
Thus replacing one dense parity by one ordinary coordinate measurement
erases the proposed dimension-independent screening advantage.

Disposition: retain the adaptive joint-risk argument as a possible formal
adapter, but defer a learner benchmark until a credible linear-measurement
or communication service and strong ordinary implementation are specified.
Freivalds verification, randomized range learning, sequential scenario
validation and standard test supermartingales are close antecedents.
