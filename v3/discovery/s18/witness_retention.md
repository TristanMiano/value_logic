# Forecast-guided retention of checked witnesses

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; broad discovery.
This connects the old edit-aware witness library to future-objective value
receipts. Maximum coverage/facility location and ordinary submodular selection
are direct ancestors. The generic greedy algorithm is not a novelty claim.

## A precise retention objective

Suppose J is a finite bank of already acquired and checked witnesses. A
future context z specifies a source version, objective and decision duty.
A checked guard g_j(z) identifies contexts in which witness j remains valid;
it may be false now and true after a later admissible edit. Let q_j(z) be
its sound upper objective value when valid. Let U0(z) be a sound baseline
upper value available without retaining this bank, and assume bounded gains.

    a_j(z)=1[g_j(z)] * max(0,U0(z)-q_j(z)),
    G_z(B)=max_(j in B) a_j(z), G_z(empty)=0,
    F_P(B)=E_(z~P) G_z(B).                                   (R1)

Retaining B permits the upper bound U0(z)-G_z(B). Its validity is pointwise
and independent of the forecast P. The forecast is used to choose which
certified information to retain, not to turn a fallible prediction into
a feasibility proof. This is proof-strength utility, not yet complete cost.

For B subset C, the gain from adding j is
max(0,a_j(z)-G_z(B)), which is at least its gain after C. Hence G_z and
F_P are monotone submodular. With k equal-sized proof slots, ordinary
marginal-gain greedy obtains at least

    alpha_k=1-(1-1/k)^k >= 1-1/e

times the best k-slot expected gain. To reconstruct the standard proof,
at step t the sum of marginals of any optimal k-set is at least OPT-F(B_t).
The greedy increment is therefore at least that difference divided by k;
iterate the residual inequality k times. This assumes exact marginal values;
computing them and evaluating the forecast are paid operations.

## A fallible task forecast affects usefulness, not soundness

If a forecast Q satisfies |F_P(B)-F_Q(B)|<=eta for every feasible B,
then its greedy set B_Q obeys

    F_P(B_Q) >= alpha_k*max_(|B|<=k)F_P(B)-(1+alpha_k)*eta.       (R2)

This follows by applying the deviation bound to B_Q and a P-optimal set.
For gains in[0,G], eta<=G*TV(P,Q) suffices. That is a conditional robustness
statement; passing a few contexts does not certify a total-variation bound.
With no accuracy warrant, every retained witness still gives a sound result,
but the forecast may choose a useless bank. No probability of mathematical
truth is learned by forecasting future requests.

## Small illustration and strong controls

Across three equally weighted future contexts, let witness gains be
A=(10,10,0), B=(9,9,0), C=(0,0,10), with two slots. Ranking witnesses by
their separate total gains retains A,B and obtains expected gain20/3.
Marginal-gain selection retains A,C and obtains10. This is an elementary
coverage example, not measured savings or a new benchmark. Ordinary maximum
coverage/facility-location selection makes the same choice.

The concrete applicability is a bounded library of SAT assignments, repair
solutions, primal incumbents or other checked witnesses whose usefulness
changes with explicit source edits and objective weights. Their old proof
cost is sunk only when actually paid; it must remain in a cold-start bill.
An ordinary incremental solver may cheaply regenerate a discarded witness,
and an ordinary cache may already make the same diversity choice.

## Costs and a boundary that blocks an unjustified claim

To realize R1, the consumer must determine which guards hold, evaluate
retained objectives and deliver a valid witness. Searching/checking the whole
bank may cost more than the value improvement. Adding a checking fee to each
q_j does not by itself account for failed trials or search over all j.
Those costs need an actual policy and may destroy submodularity of net gain.

For example, suppose a controller always checks every retained witness,
each at fee1, and both A and B individually give improvement1.5 on the only
context. The net gains are .5,.5 and -.5 for {A},{B},{A,B}; monotonicity
already fails. Shared proof chunks also make storage cost nonadditive, so
the equal-slot guarantee cannot simply be relabelled a byte-budget theorem.
Counterfactual guards must be proved or checked under the explicit version
contract; their forecast probability is insufficient.

Disposition: retain this specific adapter and its cost obstruction. Generic
submodular retention is established, and neither a moderately novel guarantee
nor a complete-cost improvement has been demonstrated. A useful next screen
would use an actual existing witness bank and priced context/guard replay,
with ordinary diversity retention and native incremental solving as controls.

## Paid guards: an exact independent-Bernoulli specialization

There is a more useful special case than always checking the entire bank.
Fix one future context. Each retained witness independently survives its
guard with probability p_j>0 under the proposed task law. Checking it costs
c_j>=0 and truthfully reveals survival. Any surviving witness delivers the
same gain G>0 over the fallback. The controller may stop and take the
fallback at any time. This stochastic law concerns future contexts/guards;
it is not assumed by the soundness checker. Its independence is load-bearing
for the following expected-cost calculation.

Define r_j=c_j/p_j and sigma_j=max(0,G-r_j). Discard tests with r_j>=G;
order the remaining tests by increasing r_j, stopping at the first success.
The exchange argument compares adjacent i,j: their expected checking costs
in the two orders differ by c_i*p_j-c_j*p_i. Their success probability and
all later failure probabilities are unchanged. Thus increasing c/p is best.
Every remaining test gives nonnegative continuation value after failures.
Skipping an earlier test cannot improve the optimum: the value of all later
tests is at most G-r_j, where r_j is the smallest later ratio, so the skipped
test's marginal p_i*(G-V_later)-c_i is nonnegative.

Let Z_j equal sigma_j with probability p_j and zero otherwise, independently.
The optimal net expected gain of a bank B is exactly

    H(B)=E[max_(j in B) Z_j].                                (R3)

Indeed, in descending sigma order this expectation is
sum_j p_j*sigma_j*product_(i before j)(1-p_i), equal to the successful
reward minus all incurred inspection costs. Formula(R3) is the Bernoulli
case of the classical Pandora reservation-value transformation, so it does
not introduce a new search algorithm. It shows that H is again monotone
submodular. Averaging over contexts preserves this property; ordinary
greedy retention with k equal slots gets the same alpha_k guarantee while
including these particular inspection costs. This does not cover varying
successful rewards, correlations, shared query feedback or search overhead
without an additional argument.

The primary Pandora comparison supplies that argument for independent rewards
more generally: with reservation value sigma solving E[(v-sigma)+]=c, the
capped value kappa=min(v,sigma) converts optimal paid search to expected maximum
positive capped value. Independent nested inspection chains have an analogous
backward capping recursion. Thus varying rewards or nested independent checks
are not a promising novelty extension of(R3). The bank-selection objective is
still an expectation of a pointwise maximum under that shared coupling. The
submodularity observation is an immediate consequence of the conventional
representation, not evidence of a new stochastic search method.

## Correlation can break the paid-retention reduction

Let two candidate guards be complementary, each true with probability1/2.
Each truthful check costs2/5, and a usable retained witness gives gain1.
One retained witness has optimal net gain1/10. With both retained, one
check reveals which is usable, by the separately warranted complement
relation, so net gain is3/5. Hence H({A})+H({B})=1/5<3/5=H({A,B}).
Submodularity fails. The inference after failure is legitimate only if the
other witness is available and the complement relation is actually known.
If a service separately requires both direct checks, the two-test value is
2/5, which still exceeds1/5, but that is a more restrictive output interface.

This positive specialization and its failure boundary are more informative
than comparing a witness cache with full recomputation alone. A natural
workflow must decide whether its guard probabilities/independence are
learned, stipulated or absent. An identical ordinary Pandora/coverage
controller ties; no fresh fee or CPU saving is claimed here.
