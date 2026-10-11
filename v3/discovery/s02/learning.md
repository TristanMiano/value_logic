# Residual-cost learning after the pair-comparison screen

Codex (GPT-6), October 11, 2026. DEVELOPMENT, S06/S02.

## 1. The service to retain

The [new screen](comparison_limits.md) removes two weak economic targets for
the quadratic pair kernel. It does not remove the useful problem: learn which
sound procedure completes a mathematical request cheaply while purchasing
only the computations needed for that completion. Keep correctness in checked
certificates; learn completion cost, including failed speculative computations.

There are two separate bills: the selected sound procedure's actual bill and
the extra fee for bounds, learning, storage and preparation. Both belong in an
end-to-end comparison. Never charge the comparator for executing missing
outcomes merely because an evaluator privately generated them for analysis.

## 2. A scale-sensitive version of the existing width lemma

Freeze K deterministic policies and their cost convention before each round's
private policy lottery. The environment can adapt to previous rounds but not
to that lottery. Costs need not share a small absolute cap if sound intervals
[l_tj,u_tj] exist and the update uses finite lower endpoints. Choose a fixed
eta>0 prospectively and use exponential weights on l_tj. Put

    r_t = max_j l_tj - min_j l_tj,
    w_t = sum_j p_tj (u_tj-l_tj).

Subtracting the common minimum from the potential update changes no weights.
The same Hoeffding argument then gives

    sum_t p_t dot C_t - min_j sum_t C_tj
      <= log(K)/eta + eta/8 * sum_t r_t^2 + sum_t w_t.

This is the earlier [lower-endpoint lemma](../s01/residual.md) with an observed
range instead of a global cost cap. For sampled execution it gives the
corresponding expected regret bound; extra learning/feedback fees add in full.
It is ordinary exponential-weights analysis, not a new learning theorem.
Finite precision needs its own charged error account before implementation.

The main constructive target is smaller informative widths *at low cost*.
For fixed-order thresholds, exact post-certificate intervals can use the new
linear-time ordinary method. For a common mandatory prefix, subtract its
observed cost before updating. This cancellation can improve numerical scale
and any absolute-cap bandit bound, but an ordinary learner can do the same.

## 3. A feedback-graph trap

The selected certificate may reveal alternate procedures' costs for free apart
from replay computation. It does not automatically reveal the probability
that each alternative would have been observed under all other possible
selected procedures. That inclusion probability can depend on hidden outputs.
Applying an importance-weighted feedback-graph estimator with a guessed
revelation probability is unjustified. Safe choices include the selected
policy's bandit feedback, a graph guaranteed by public structure, or the
sound-interval bound above. Extra policy execution also gives valid feedback,
but every additional mathematical query is purchased and retained in the bill.

## 4. Why shrinking a regret certificate is not a saving

After the selected procedure finishes, buying another truth bit can tighten
counterfactual cost intervals. The current output and incurred execution cost
do not improve. A smaller retrospective upper bound on regret is evidence,
not an actual resource benefit. To buy feedback economically requires a
future-request assumption or a valid online learning tradeoff, not merely
that its price is below the amount by which an uncertainty bound shrinks.

Next implement the cheap endpoint feedback, check the dominance witnesses,
and measure the price of even this cheaper update. Keep measured evaluator
time separate from stipulated query tariffs. A real bounded-computation arm
must have a strong shared evaluator and must expose any finite horizon inside
the proposition being evaluated; a timeout is not a refutation of unbounded SAT.
