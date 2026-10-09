# Independent acquisition-planning reconstruction

Scope: a bounded mathematical subreview of the two-law Bayesian experiment, reconstructed before inspecting the candidate planning source or saved numerical result. This is same-model review. It is nonblind: the assignment disclosed the two laws, prior, fixed future horizon, terminal actions, cap-N dynamic-programming form, 24-row expectation, and frozen source hash. All work is unmeasured auxiliary work with zero principal credit.

The two latent laws are theta-minus = 9/20 and theta-plus = 11/20, with prior probability 1/2 each. Conditional on the law, acquisition samples are IID Bernoulli(theta). After t samples with k successes, put A = 11^k 9^(t-k) and B = 9^k 11^(t-k). Bayes' rule gives q(t,k) = P(theta-plus | history) = A/(A+B), and the posterior predictive probability of success is p(t,k) = (11A+9B)/(20(A+B)). A particular ordered history has mixture probability (A+B)/(2*20^t); an unrestricted count state additionally has its binomial multiplicity.

The future exploitation horizon H is fixed independently of the number of acquisition samples. The two terminal actions are fallback, worth H/2, and deployment, worth H*(9/20 + q/10). Subtracting the fallback baseline gives deployment advantage D(t,k) = H*(2q-1)/20, so the optimal terminal advantage is S(t,k) = max(0,D(t,k)). At a deployment tie, fallback can be selected without changing value.

Let c >= 0 be the direct cost of one acquisition observation. For a sample cap N, the optimal additional value relative to fallback obeys the finite backward recursion

    V(N,k) = S(N,k),
    C(t,k) = -c + p(t,k)*V(t+1,k+1) + (1-p(t,k))*V(t+1,k),
    V(t,k) = max(S(t,k), C(t,k))  for t < N.

Sampling only when C(t,k) > S(t,k), and stopping on ties, specifies one optimal deterministic policy. Any fixed ex-ante planning bill subtracts from V(0,0) after solving this observation-allocation problem; because it is identical for every policy reached after paying it, it does not change the interior recurrence. An optional planner purchase instead compares the post-bill value with the bypass value zero.

Independent verification can enumerate reach probability forward from (0,0). Each sampling state contributes its reach probability to E[T], then sends probability p to (t+1,k+1) and 1-p to (t+1,k). Each stopping state contributes its reach probability times D(t,k) if deployment is selected, otherwise zero. Consequently the sum of terminal expected deployment advantage minus c*E[T] must equal V(0,0) exactly. Exact rational arithmetic is sufficient: every prior, transition, payoff, and price is rational.

This establishes a Bayes-optimal policy only within the stated finite acquisition cap and fixed-horizon two-terminal-action model. It does not supply a fixed-sample identification lower bound for arbitrary sequential policies, nor does it imply optimality over interleaved deployment, a consumed exploitation horizon, unknown laws, or alternative observation/control mechanisms.

## Candidate-specific review

The frozen candidate source and the run's saved copy both have SHA-256 `94fb8efcbb924470d883733f3c317fc0a79c4047089104ee4ee1c03ca5141f37`. Candidate-specific parameters are c = 1/2 + 16*lambda and an initial lookup bill of 8*lambda. Thus its saved root Bellman value is V(0,0); the prior gain excluding construction is V(0,0) - 8*lambda; the all-in prior gain further subtracts lambda times the declared construction-unit count. Stopping on acquisition ties, and choosing fallback on deployment ties, match the reconstructed optimal tie convention.

For the independent implementation, define U(t,k) = (A+B)*V(t,k). Then the weighted stopping value is max(0,H*(A-B)/20), and the weighted continuation value is

    U_continue(t,k) = -c*(A+B) + [U(t+1,k+1) + U(t+1,k)]/20.

The child likelihood weights are (11A,9B) after success and (9A,11B) after failure. This avoids copying the candidate's posterior-predictive Bellman arithmetic. The independent forward calculation enumerates individual ordered binary histories under each law, without merging their masses by count state, and derives its expected attempt count independently from both acquired prefixes and the terminal stopping-time distribution.

All 24 cases and all 1,128 saved state rows agree exactly. Across posterior, predictive, terminal, continuation, policy, Bellman, forward-law, and resulting gain fields, 10,608 exact comparisons produced zero mismatches. Full evidence and the independent implementation are adjacent to this derivation. Construction-price multiplication and all-in subtraction were checked using the saved unit count; the separate source/core/tariff audit belongs to the parent reviewer.
