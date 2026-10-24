# Expected repair work can replace a deterministic proposal cap

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass48.

Consider a learner that proposes a function, receives a fresh public
counterexample if wrong, and repeats until exact acceptance. Its ideal
truth-oracle execution has K incorrect proposals, with E K<=b. All learner
and public-search randomness is independent of the private checker seed.
Replace truth-oracle acceptance by a sealed, perfectly complete checker
with fixed-false-proposal error at most epsilon. Stop on its first acceptance.
Then

    P(incorrect accepted output) <= epsilon * E K <= epsilon*b. (1)

Condition on the entire independent public tape. Up to the first incorrect
acceptance the actual execution is an initial part of the ideal execution;
union bound over its K false proposals, then average. Countable paths use
Tonelli's theorem; E K<infinity implies finite K almost surely. This does
not require a deterministic worst-case K. It is a first-acceptance wrapper,
not an authorization to reset the learner after each acceptance for free.

For iid testing at points from D, let p_i be the actual disagreement mass
of ideal incorrect proposal i. A private k-point batch has error(1-p_i)^k.
Independent public rejection sampling takes mean1/p_i truth queries per
counterexample. Thus the more precise statements are

    P(error) <= E sum_(i<=K) (1-p_i)^k,
    E actual truth queries <= k+E sum_(i<=K) 1/p_i.    (2)

The coupling makes the actual public-search bill a prefix of the ideal bill.
In particular a known gamma lower bound gives epsilon=(1-gamma)^k and
mean bill at most k+b/gamma. Proper learners with an expected equivalence-
query guarantee can therefore be substituted without needing an improper
SOA representation. Such a learner's actual hypotheses, counterexample
distribution, computation and realizability premises must still be supplied.
The recently read proper-learning theorem is a lead, not an imported
black-box implementation or an audited numerical constant.

## A weaker certificate with no uniform disagreement gap

If instead the total ideal expected search bill C=E sum1/p_i is bounded,
then for integer k>=1,

    P(error) <= C * k^k/(k+1)^(k+1) < C/(e*k).       (3)

Indeed p(1-p)^k is maximized at p=1/(k+1), with the displayed maximum.
Multiply its bound by1/p and sum in(2). For the strict inequality use
log(1+x)>x/(1+x) at x=1/k, giving(1+1/k)^(k+1)>e. The exact rational
constant remains the operative finite-k certificate.

Equation(3)'s exact constant is useful as a structural relation between
verification confidence and an expected computation bill. It may require
far more private labels than a known gamma. It does not allow finite-sample
exact identification uniformly over arbitrarily small disagreement regions
without paying for a corresponding bound on search cost.
