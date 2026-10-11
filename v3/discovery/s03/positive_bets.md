# S10: censored positive-proof bets with exact count allocation

Codex (GPT-6), October 11, 2026. DEVELOPMENT; S06/S08/S09 lineage.
Prospective cheap development, not a frozen confirmation claim.

## Why not simply multiply the existing partial intervals?

The earlier censored count hull is a valid source for one group. A Bonferroni
collection is valid simultaneously but loses relationships among groups. With
fully resolved labels, ordinary likelihood-ratio processes can be interleaved
across disjoint groups under predictable group selection. Their joint source
can be profiled over count allocations. This is established statistical work.

For partially resolved labels, taking the union over possible completions is
safe but can destroy the log-concavity used by cheap optimization. Example:
N=100, sampled s=10, known positive k=0, known negative z=9, leaving one unknown.
With the earlier rho=1/2 working count mixture, q(0)=13/44 and q(1)=1/22.
Define r(M)=max_{e in {0,1}} H_M(e)/q(e). Then

    r(0)=44/13, r(1)=198/65, r(2)=4.

The middle square is smaller than the product of its neighbors. Thus r is
not log-concave, and blindly applying the fully labeled greedy profile is
invalid. This does not reject the outer-source guarantee; it rejects that
computational shortcut. A different sequential construction follows.

## A positive-only factor

Fix disjoint groups of deterministic mathematical questions. In one group,
N is population size, M its true positive count, j previous uniform draws,
and k the number of checked positive receipts among those draws. The next
group is selected before its next uniform remaining index is generated.
The receipt indicator Z is 1 only for a sound checked positive proof; otherwise
it is 0. This is a production indicator, not a negative truth label. Proof
budget, procedure and censoring can depend on the drawn item and past history.

Let e be the unknown actual positive count in the previous prefix. Always
e>=k. For a hypothesized upper count m>=k, under M<=m,

    E[Z | past] <= E[Y | past] = (M-e)/(N-j)
                    <= mu_m := min(1,(m-k)/(N-j)).

This conditions on all previous sampled truths if necessary, even if the
controller has not resolved them. It requires a fresh uniform next index;
looking ahead at future sample identities before choosing the group is not
covered. A hidden precommitted permutation or on-demand uniform selection
satisfies the requirement. Deterministic side information and checked caches
do not make truth random, nor change the uniform index lottery.

Choose a finite rational eta>=0 before the next index is revealed. Eta may
depend on past receipts, budgets and a fallible prediction, but is independent
of the hypothetical count m when building the computational form below. Define

    factor_m(Z) = (1+eta*Z)/(1+eta*mu_m).

Its conditional expectation is at most one under M<=m, and it is nonnegative.
The product E_t(m) starts at one and is a nonnegative supermartingale for each
fixed upper-count null. If observed k>m, hard receipts refute that null directly.
No unknown outcome is deleted; every sampled failure supplies Z=0 and reduces
the test wealth. There is no assumption that censoring is independent of truth.

For disjoint groups, multiply the factors in the actually chosen sequence.
Predictable group selection preserves the conditional expectation inequality
under every vector of upper-count nulls. In particular, at the fixed true count
vector M, Ville's inequality gives

    Pr(ever E_t(M) >= 1/alpha) <= alpha.

The count source C_t={m: each m_g>=k_g and product_g E_gt(m_g)<1/alpha}
therefore contains the true vector simultaneously with probability >=1−alpha.
Pointwise receipt/revision constraints can refine it, and subsequent count
targets can adapt to history without an extra query-risk charge. Source identity,
sampling authority and the hard-evidence conflict policy remain required.

This statement does not apply to overlapping groups with duplicated factors,
post hoc changes to the partition, chosen favorable seeds, or unknown labels
quietly treated as sound refutations. Power and proof-production cost remain
separate from the validity statement.

## Exact profiling of a total-count null

Store the trace (j,k_before,eta,Z) for each group. At the current boundary,
restrict integer m to [k_final,N]. Every denominator term has form

    1+eta*min(1,(m-k_before)/(N-j)).

It is a positive nondecreasing concave function of m. Its logarithm is concave;
the negative logarithm is convex. The numerator is independent of m. Hence
log E_g(m) is decreasing and discretely convex over that integer domain.
Its marginal ratios E_g(m+1)/E_g(m) are nondecreasing and at most one. Ratios
are rational and can be compared exactly without numerical logarithms.

To test total positives >=T, profile the complementary allocations
sum_g m_g<=T−1. If sum k_g>=T, checked receipts alone settle the claim.
Otherwise start at all m_g=k_g and spend the remaining count allowance by
taking the smallest available marginal ratio at each step. A group's later
ratios are no smaller than its earlier ones, so ordinary convex resource
allocation proves optimality. Use all available allowance, since each factor
decreases with m. Reject the union of null allocations only if this minimum
product reaches 1/alpha. Under any true null vector, that vector is among the
allocations, so a false warrant entails crossing its own valid process.

The cheap algorithm is over count allocations, not over all truth vectors.
The naive exact implementation still costs O((T−sum k) log G) marginal choices,
with each new ratio requiring the group's stored trace arithmetic. Big-integer
cost and repeated profiling may erase evaluator savings. For two groups the
profile along a fixed total is convex and admits binary search of its ratio
sign; that is a possible next repair, not yet a measured speedup.

## Fallible betting advice and a convex mixture repair

At a reference null mean mu and a forecast proof-production rate p, the
single-step expected log factor is p log(1+eta)−log(1+eta*mu). When p>mu its
stationary optimum is eta=(p−mu)/(mu*(1−p)); otherwise eta=0. This is an ordinary
log-growth calculation under the forecast, not a validity premise. The
forecast concerns checked proof yield, which can be much lower than truth rate.
The allocation prototype can use bounded rational advice or several fixed
eta values; every schedule must remain predictable and independent of the
hypothetical m for the stated convex profiling result.

A fixed nonnegative mixture of such processes within each group is also valid.
Its logarithm is log-sum-exp of convex functions of m, hence convex, and it is
still decreasing. Thus per-group mixing preserves the exact greedy allocation
kernel. An eta=0 component is constant one and protects some wealth against a
bad production forecast, at a price in evidence. Multiplying these per-group
mixtures remains separable. Mixing whole joint strategies instead is valid
but generally loses separability; do not apply the same greedy proof to it.

## Closest comparison and prospective probe

Spertus and Stark, [Sweeter than SUITE](https://arxiv.org/pdf/2207.03379),
§§3.3–3.7 (v3 PDF pp.4–7), already develop intersection supermartingales,
optimization over stratum nulls, and predictable adaptive stratum selection.
Their §3.6 distinguishes test efficiency from the tractability of profiling.
These are direct ordinary antecedents. The present developmental specialization
uses checked positive production, a conservative remaining-count mean and an
exact rational convex allocation kernel. It does not claim the product or
adaptive-sampling principle as new, or comparison against their implementations.

Hait, [Target-Aware Sequential Inference](https://arxiv.org/abs/2609.37873v2),
abstract inspected only, distinguishes single-target, target-set and local
guarantees. This is a recent comparison lead; no theorem is imported from it.

Next: exact small count-allocation comparisons, finite sequential boundary
checks under deliberately truth-dependent censoring, and controller-cost
measurement. Keep a simple ordinary one-group lower test and Bonferroni
stratum confidence bounds as controls. Novelty, complete economics and material
readiness remain unresolved; do not start extensive adversarial confirmation.

## First finite outcome and the cost obstacle

[bets01.json](bets01.json) matched exact profiling on 200 small cases and
15,999 admissible null vectors. Its 64 exact sequential cases covered all
two-group truth counts at N_g=3, two alpha values, and two proof-production
rules including a truth-dependent censor. All true-null crossing probabilities
were at most their levels. These small checks support development, not a
general proof or independent verification. The fixed-bet and mixed-bet timing
rows use different generated traces and must not be read as a paired comparison.

The naive profiling cost is a serious obstacle: a four-group N_g=256,
32-draw-per-group mixed example cost 202.6331 ms for one profile. That can
outweigh the SAT evaluator savings observed earlier. It warrants a structural
repair before a larger experiment.

## Proposal plus exact exchange certificate

Any feasible allocation x with total T−1 selects a prefix of each group's
nondecreasing marginal-ratio sequence. It is optimal exactly when

    largest selected marginal ratio <= smallest unselected marginal ratio,

ignoring absent selected/unselected lists at their bounds. Necessity follows
by exchanging one unit from the largest selected ratio r to the smallest
unselected ratio p: the product changes by p/r<1. For sufficiency, all selected
increments are then no more costly than any unselected ones, so they form a
globally cheapest multiset of the required size. This is ordinary separable
discrete convex allocation, now an executable certificate for the value source.

A fallible proposal can supply x. Check only its adjacent ratios, and repair
violations by those exchanges. Order tied increments consistently by group and
within-group position. Relative to the corresponding canonical greedy optimum,
each strict exchange removes an excess chosen increment and supplies a missing
one. The number of exchanges is at most half the initial L1 distance to that
optimum; the procedure may stop earlier at another tied optimum. Exactness does
not require the proposal to be accurate. A heap implementation needs O(G+d log G)
ratio-management work; a simpler small-G scan costs O(G(d+1)). Ratio evaluation
and rational bit cost remain separately charged.

For a concrete analytic proposal at eta=1, ignoring saturation, the derivative
of log E_g(m) is −sum_j 1/(N_g+m−j−k_before_j). Replacing j+k_before by its
trace average a_g gives approximate derivative −s_g/(N_g+m−a_g). Equalizing
these approximate derivatives yields m_g≈c*s_g−N_g+a_g, clipped to [k_g,N_g].
Choose c to meet the count budget, round to a feasible integer allocation, and
verify/repair it exactly. For mixtures this remains only a heuristic. Computing
the proposal and failed repairs are part of the controller bill.

There is an additional decision-specific shortcut. If any proposed feasible
allocation already has product wealth <1/alpha, it lies in the current source
and disproves the *availability of this aggregate warrant*. The service can
abstain without finding the exact minimum. This is not evidence that the
actual action is wrong. To return a positive warrant, it still needs the exact
optimality certificate or another proved lower bound on the minimum.

A current null witness can later guide which group to sample: forecast the
positive-production log gain at its component and divide by a paid cost model.
Choosing a bet from that witness is allowed when it is fixed before the next
index draw and the resulting recorded eta is used for every hypothetical count
in the source update. This prospective allocation heuristic remains fallible;
the exact source and warrant contract do not depend on its accuracy.

## Exchange-profile outcome and next repair

[exchange01.json](exchange01.json) matched the full greedy optimum on 240
small cases for both proposals. Early counterexamples were feasible and below
the threshold; counted strict exchanges obeyed the stated distance bound in
those fixtures. Paired prepared traces reduced a two-group mixed profile from
127.5455 ms to 18.0591 ms, and a four-group equal-prefix profile from 197.5411
to 30.9525 ms. On heterogeneous prefixes the trace approximation was poor:
662 exchanges and 1,274.8476 ms, close to the original 1,348.5212 ms. The
proportional proposal was better there at 603.8148 ms. An eight-group negative
warrant case fell from 1,291.1324 ms to 49.3585 ms with early counterexample
stopping. This mixed result motivates a better proposal, not a favorable-only
summary or an end-to-end saving claim.

The eta=1 derivative approximation ignores which component of a mixture carries
its wealth. For component r, let l_r(m)=log E_gr(m), and let d_r(m) be its
derivative away from saturation knots. Then

    d_r(m) = -sum_{unsaturated draws} eta_r /
                  (remaining + eta_r*(m-k_before)),
    d_g(m) = sum_r softmax(log weight_r+l_r(m)) * d_r(m).

This derivative is nondecreasing because log wealth is convex. A continuous
resource allocation proposal can solve d_g(m)+lambda=0 with box constraints
and sum m=T−1, using ordinary scalar dual search. At a saturation knot the
subgradient interval replaces the derivative. Numerical results remain advice:
round to a feasible integer allocation, then use the exact rational exchange
certificate. An inaccurate float, overflow or failed optimizer must not become
a positive warrant. All proposal work is charged. This is ordinary convex
optimization plus exact repair; its utility is an empirical resource question.

## Numerical advice outcome

[float01.json](float01.json) matched the exact greedy value on 90 additional
small sources. On four paired prepared traces, ordinary SLSQP advice followed
by exact rational checking/repair took 5.9386, 11.2118, 29.5213 and 21.5622 ms,
versus full greedy profiling at 132.7054, 206.0730, 1,362.6001 and 1,291.0059 ms.
The first three proposals needed no exchange; the fourth needed one. A numerical
proposal with early counterexample output took 14.9743 ms on the fourth case.
SciPy 1.15.3 dependency imports cost another 403.8213 ms in this process.
These are local kernel timings, with common traces explicitly retained. They
do not yet establish a complete service benefit or a novelty claim. Floating
success status was not used as the correctness certificate.

The next useful question is economic rather than another optimizer tweak:
does a complete positive-proof service with heterogeneous mathematical groups
save enough actual evaluator work to repay this controller, sampling, proof
checking and startup bill? Compare cost-directed ordinary stratum intervals
as well as one-group direct tests. A weak uniform sampler is insufficient.
