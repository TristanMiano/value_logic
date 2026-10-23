# Stop and refine using a certificate for hidden sample rank

Codex (GPT-6), DEVELOPMENT, October23,2026 UTC. This combines the latent
sample-span event, hidden-rank certificates and a standard test supermartingale.
No new maximal inequality, general learner or free observation service.

## A sharper elementary fixed-cohort alternative

For the fixed feature map in learn_affine_warrants.md, let z_1,...,z_N be
iid latent syndromes, S_N their actual linear span, J_N=dim(S_N), and
p_N=P(z_new not in S_N). Exposing the latent vectors one at a time, the
span grows by one exactly when the next vector is outside it. Its conditional
growth probability is p_(t-1), and these probabilities never increase.
Coupling to iid uniforms gives, for every fixed epsilon and integer k,

    P(p_N>epsilon AND J_N<=k)
      <= sum_(j=0)^k binom(N,j)*epsilon^j*(1-epsilon)^(N-j).       (1)

Indeed on p_N>epsilon every earlier growth probability exceeded epsilon,
so the actual number of growths dominates the sum of the coupled
Bernoulli(epsilon) indicators on that event.

Choose delta_k=delta/[(k+1)*(k+2)] before seeing data; these sum to delta.
For k<N let B_N(k) be the unique epsilon in(0,1) at which the right side
of(1) equals delta_k; set B_N(k)=1 for k>=N. A union bound over k proves

    p_N <= B_N(J_N) with probability at least1-delta.             (2)

B_N is increasing: the binomial lower tail increases with k while its
allowed probability delta_k decreases. Consequently ANY truthful upper
bound k_bar>=J_N can be substituted. In particular the independent-
transversal certificate in hidden_rank.md applies. One event covers all
truthful refinements of that same cohort. This is a conventional coupling
and error-spending construction, not a new binomial confidence principle.
It is an alternative to the imported stable-compression bound; taking the
minimum of separately calibrated bounds requires accounting for both events.

## A sequential rule with a fixed target risk

Now fix epsilon,delta in(0,1) and let the iid cohort grow. Define

    A=(1-epsilon/2)/(1-epsilon)>1,
    M_N=2^(-J_N)*A^(N-J_N), M_0=1.                              (3)

Before p_N first becomes<=epsilon, the next rank-increase probability
mu is>epsilon. The multiplier in(3) is1/2 on a rank increase and A
otherwise, and

    mu/2+(1-mu)*A <= epsilon/2+(1-epsilon)*A =1.

Stop this nonnegative supermartingale at the first safe latent span.
Ville's inequality gives

    P(exists N: p_N>epsilon AND M_N>=1/delta) <= delta.           (4)

Neither J_N nor S_N needs to be fully observed to USE this test. At any
stage, truthful partial receipts Z_i contain z_i. Put S_hat=span(union Z_i)
and provide a certified k_bar>=J_N. Accept the retained equations S_hat-perp
whenever

    2^(-k_bar)*A^(N-k_bar) >= 1/delta.                          (5)

The left side is a lower bound on M_N because(3) decreases with rank.
Also P(z_new not in S_hat)<=p_N. Therefore, with probability at least
1-delta, EVERY accepted span has missing mass<=epsilon, simultaneously
over adaptive sample sizes, truthful refinement of old receipts and all
subsequent selections of rules within the accepted equation space.

This extends refinement_learning.md's fixed-N guarantee. No union penalty
is paid for the number of refinement steps or inspected sample sizes.
The target epsilon and confidence delta remain fixed; choosing them after
looking at the data is not authorized by(4). The next case must be fresh
from the same law, and the feature map must have been fixed in advance.
The guarantee remains unconditional risk on one new case, not conditional
release accuracy or the probability of never erring over infinitely many cases.

If exact rank never exceeds d, full receipts guarantee acceptance by

    N >= [log(1/delta)+d*log(2*A)]/log(A).                       (6)

With incomplete receipts the IMPLEMENTED upper bound may exceed d, so
(6) is not automatically a stopping-time or acquisition-cost guarantee.
In particular the common-row-space observation bottleneck remains.

## Why this is a useful synthesis candidate

The proposed service can purchase a new iid case, refine an older partial
case, or stop, based on the same checkable criterion. A supplied subspace
and index set certify k_bar via N-|I|+dim(U_I); a full matroid-intersection
solve is optional. The resulting rules can weaken a globally false model
while protecting all authorized combinations on a common event.

For the earlier example N=200,199 zero-syndrome cases and one syndrome
known only inside a20-dimensional subspace, k_bar1 is certified without
recovering the last vector. At epsilon1/20 and delta1/20, condition(5)
reduces to(39/38)^199>=40, an exact rational inequality. It can certify
the target5% risk where the earlier stable-compression bound0.06236148
does not. The fixed-N alternative(2) may improve it further; compute the
values in the planned tiny probe before quoting them.

All200 cases, all syndrome/containment/rank receipts and all computation
remain charged. Direct validation of a preselected warrant can be cheaper
and statistically tighter; this construction permits data-dependent rule
selection and shared adaptive refinement. An ordinary implementation of
these same ingredients ties. Novelty and practical economics are unassessed.

Prospective cheap check: exact enumeration of short iid streams on F2^2
under a few rational laws, checking(1) and the probability of ANY unsafe
sequential acceptance. Also certify the displayed rational example and
compute outward rational fixed-N bounds. This is not confirmation or a
general test of all partial-measurement acquisition strategies.

Executed sequential_probe.py: PASS on37 rational laws,8880 joint-tail
inequalities and13320 horizon/target/confidence checks for any unsafe
acceptance through horizon30. The bound for N200,k_bar1,delta0.05 lies
strictly above0.033742 and at most0.033743, certified by rational binomial
tails. This upper endpoint is45.8913% lower than the earlier0.06236148
stable-compression formula at the same confidence. These are compared
guarantees, not observed risks or a claim of a new statistical rate.
The sequential5% target at95% confidence is certified once N>=144 if
k_bar1 is available; the actual acquisition cost of that certificate is
not supplied by this sample-count calculation.
