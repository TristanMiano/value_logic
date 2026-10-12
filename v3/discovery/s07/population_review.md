# Focused review of the common-CDF repair service

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT, independent constructive inspection during the principal's active
work. Helper overlap supplies no principal-clock credit. No acquisitions, solver
calls, service reruns, or changes to the service and historical outputs were made
for this review.

## Finding and scope

The construction supports the stated fixed-action repair certificate when the
target is the expected cost of one repair under the uniform law on the fixed
64-row source. Its statistical qualification is one common fixed-sample CDF
event, and its logical qualification is the independently checked original
source proof and feasible actions. Repeated physical identities and subsequent
adaptive inspections do not invalidate that event when their occurrence
multiplicities remain in the empirical CDF.

This is a useful construction of partial cost acquisition, not evidence of an
advantage over the strongest ordinary acquisition policy. In the corrected v2,
the ordinary direct-contrast arm is exactly tied with the relevant-cut arm.
Moreover, the same saved 29 physical cut observations already suffice for a
deterministic finite-cohort certificate at tolerance 2, without requiring the
128-draw inference step. That stronger comparison should accompany any account
of the sampling construction.

Sources inspected: [v1 implementation](population_service_v1.py),
[v1 results](population_results.json), [v1 preservation manifest](population_v1_manifest.json),
[v2 implementation](population_service.py), [v2 results](population_v2_results.json),
[joint repair certificate](../s06/joint_repair.py), and the
[CDF sweep and independent checker](../s05/cdf_sweep.py).

## The precise population objective

Let `m(H)` be the nonnegative cost vector attached to latent mode H, let
`mu = E[m(H)]`, and let `C*(w)` be the minimum original-source feasible repair
cost at weights w. The implementation bounds

`cost(a; mu) - min(p, C*(mu))`,

for the one selected fixed repair or replacement action a. A feasible repair
with violation mask u has expected cost `u dot mu`. The saved post-run
diagnostic uses this same comparator; its field `realized_population_regret`
therefore means regret against the best fixed action for the realized finite
population's mean costs.

It does not automatically bound expected regret against an action that learns
the latent mode before choosing a repair. The latter comparator is

`E[min(p, C*(m(H)))]`.

Their difference is the nonnegative Jensen gap

`min(p, C*(E[m(H)])) - E[min(p, C*(m(H)))]`.

Nonnegativity follows directly because the minimum of the fixed actions' affine
cost functions is concave. This is a distinction between decision objectives,
not a defect in the expected-cost certificate.

Here the only two distinct modes are `(0,4)` and `(4,0)`. Every latent mode
allows a zero-cost feasible repair, so the mode-informed optimum is zero. The
saved true mean is `(17/8,15/8)`, and selected model 2 costs `15/8`. Thus its
fixed-optimum regret is zero, while its expected mode-informed regret is
`15/8`. The equality of that latter number with this run's reported bound is
incidental. For a known balanced distribution, the same two repairs would have
fixed-optimum regret zero and mode-informed regret 2. These objectives cannot be
interchanged in a general claim. The numbers here are derived from the saved
source and diagnostic, after the acquisition decisions.

## One event covers multiplicity, refinements, and chosen actions

Condition on an arbitrary fixed population `H_0,...,H_63`. If the 128 identity
draws are genuinely iid uniform with replacement, their latent values are iid
from that population's uniform empirical distribution. Colliding identities
retain equal latent values, but the unconditional sampling law still has the
iid property. The fixed-n DKW-Massart inequality therefore applies to the full,
possibly unobserved empirical CDF with denominator 128. Massart's original
two-sided inequality gives `P(sup |Fhat_128-F| > r) <= 2 exp(-256 r^2)`;
see the [primary paper, abstract](https://www.researchgate.net/publication/38360933_The_Tight_Constant_in_the_Dvoretzky-Kiefer-Wolfowitz_Inequality)
and [publication record](https://doi.org/10.1214/aop/1176990746).

At `r=1/8`, the exponent is -4. The code's exact positive series check is
conservative: `sum_{k=0}^5 4^k/k! = 643/15 < exp(4)`, hence
`2 exp(-4) < 30/643 < 1/20`. No rounded logarithm is needed.

For a physical identity i with occurrence count c_i and a truthful current
interval `[l_i,u_i]`, define at each cut j

`A_t(j) = sum_i c_i 1{u_i <= j}/128`,

`B_t(j) = sum_i c_i 1{l_i <= j}/128`.

Every refinement satisfies `A_t <= Fhat_128 <= B_t` pointwise. On the single
event `sup |Fhat_128-F| <= 1/8`, the code's interval
`[max(0,A_t-1/8), min(1,B_t+1/8)]` therefore contains the true F at every
stage. This argument is pathwise over all truthful refinements, even when the
next physical identity, cut, stopping time, or final action depends on earlier
observations. It needs no repeated-look or action-count union bound. The saved
implementation uses a simpler fixed first-appearance order, which is covered.

An audit of one identity updates all of its occurrences. Its cost is one
physical audit, not c_i fresh observations. Conversely, replacing denominator
128 with the 59 distinct identities, or treating selectively audited rows as a
new iid sample, would change the statistical argument. The asserted coverage
is over the original draw law, not a conditional 95% guarantee after fixing a
particular collision pattern. The deterministic seeded development execution
is a reproducible realization; it does not itself establish the randomness or
truthfulness assumptions of a deployed sampler and observation provider.

Once the event contains the true distribution, it contains the true mean-cost
vector for every payoff represented as a function of this same H. An adaptive
choice of payoff/action does not require a new concentration result. A different
source, additional unrepresented randomness, or newly increased sample size
would require its own justified construction. Here all relevant cost modes are
public functions of the same H, and all three arms share the same underlying
event; the 1/20 allowance is not spent three times.

## Exact support and the checked logical composition

`PopulationCosts.support(c)` minimizes the negative payoff
`-c dot m(H)` with the quantile sweep, independently checks every emitted
quantile-window minimum, reconstructs a feasible distribution, and checks the
returned mean-cost witness against the exact support value. This supports an
arbitrary finite contrast vector, including negative coefficients. The
expectation is exact over the declared pointwise CDF box, which is an outer
relaxation of a fixed 64-row population; it does not assert that every extremal
probability vector is physically realizable by that population. The established
representation and its proof are documented in [cdf_sweep.md](../s05/cdf_sweep.md).

The common logical query has actual weights `(1,1)` and budget zero. The raw
UNSAT tree is checked against the original hard and soft clauses and recompiled
to covering masks 1 and 2. For every nonnegative weight vector w, its covering
leaves give `L(w)=min(w_1,w_2) <= C*(w)`; the original feasible models 1 and 2
are checked separately. Repricing the checked cover at expected costs is valid
because those costs are nonnegative. A hash alone is not the admission argument.

For a retained repair mask u, `joint.certificate` takes the maximum of zero,
the support of `u dot w-p`, and the supports of each `(u-v) dot w` over checked
cover leaves v. This bounds regret against `min(p,C*(w))` uniformly over its
mean-cost set. The minimum across available checked actions and individual
checked trees remains valid, so selecting the best current certificate on the
same CDF event is sound. The replacement branch uses the corresponding
`p-v dot w` supports. These are bounds for expected costs, as specified above.

## Corrected comparison and a stronger ordinary control

The preserved files give the following actual arm totals. Code admission is
reported separately as 6,725 units; unpriced draw/audit fees, byte costs and
time are not silently zero.

| Version and policy | Physical cut audits | Distinct rows audited | Fully identified rows | Named arm units | Final bound |
|---|---:|---:|---:|---:|---:|
| v1 relevant cut | 29 | 29 | 0 | 70,585 | 15/8 |
| v1 full latent | 58 | 29 | 29 | 122,263 | 15/8 |
| v1 direct contrast | 29 | 29 | 0 | 71,165 | 15/8 |
| v2 relevant cut | 29 | 29 | 0 | 70,605 | 15/8 |
| v2 full latent | 58 | 29 | 29 | 122,283 | 15/8 |
| v2 direct contrast | 29 | 29 | 0 | 70,605 | 15/8 |

The v1 direct arm recompiles the immutable contrast once per audit. The v2
correction charges the same one-time 20-unit compilation to every arm, making
the two relevant-cut policies equal. This is the appropriate reported result;
the v1 difference is not evidence of a value-method advantage.

For the known uniform finite target, an ordinary deterministic alternative
maintains all 64 physical intervals, initializing unobserved IDs to `[0,3]`.
Then, for every cut j,

`count_i(u_i <= j)/64 <= F(j) <= count_i(l_i <= j)/64`.

No probability event is needed for these inequalities. The full independent
row support is also available directly as the sum of per-row maxima divided
by 64, as in the finite-cohort `CostState` construction. Intersecting a
deterministic CDF envelope with the sampling envelope can strengthen either;
for general payoffs, keeping the per-ID support can retain more information
than pointwise CDF endpoints.

A read-only arithmetic examination of every saved v2 relevant-cut prefix gives:

| Saved audit prefix | Known `H<=1` physical IDs | Known `H>1` physical IDs | Deterministic F(1) interval | Best fixed-repair deterministic bound | Saved DKW bound |
|---|---:|---:|---|---:|---:|
| 27 | 13 | 14 | [13/64,25/32] | 9/4 | 19/8 |
| 28 | 13 | 15 | [13/64,49/64] | 17/8 | 9/4 |
| 29 | 13 | 16 | [13/64,3/4] | 2 | 15/8 |

For model 2, the deterministic bound is `max(0,8*upper_F(1)-4)`; for model 1,
it is `max(0,4-8*lower_F(1))`. Replacement at price 6 is dominated. Prefix 29
is the first saved prefix at which their minimum reaches tolerance 2. The
sampling calculation instead uses occurrence counts 34 below, 50 above, and
44 still unresolved at cut 1, giving `F(1) in [9/64,47/64]` and bound 15/8.
Both close at 29 actual observations, with different guarantees and margins.

This prefix calculation buys no new observations and is not an executed,
fully invoiced extra policy. It establishes a concrete ordinary alternative
for the next prospectively charged comparison. It does not establish its
wall-time or total economic cost, or a different audit order's realized
outcomes. Because the 64 physical IDs are public and individually auditable,
the alternative does not fundamentally need 128 random draws; reproducing this
particular draw-derived audit order may still incur planning costs.

## Next constructive improvement

Give every compared policy the same option to retain exact finite-row support
and intersect its deterministic information with a common CDF band. Execute
and invoice that ordinary control before claiming a sampling/acquisition win
on a finite enumerated source. If population inference is the central intended
contribution, state a target where the unobserved population is not exhausted
by 64 enumerable auditable rows, specify the sampling interface, and preserve
the fixed-action expected-cost objective. Continue to expose progress by
relevant-cut uncertainty or the actual certificate bound; fully identified H
counts can remain zero while all action-relevant information has improved.

## Immutable evidence checked

The reviewed bytes agree with the implementation digests recorded in the
corresponding results and the v1 manifest:

| File | SHA-256 |
|---|---|
| population_service_v1.py | `47f60a1e932bbb16b3ff9afbd7d5d06f54608da819601cce97c119aeed8a74ba` |
| population_service.py (v2) | `6c5675a5413e1a0aa723716730343f8b64fde3cb41471ec3b570cc64869114d4` |
| population_results.json | `fc01e44160a28e3c0d52af7debe9b81fd9f093c630886e0e55ee2bac03f720ba` |
| population_v2_results.json | `8772d38dfb68c1d7026fd67bf75d992733b470514d41d2acfe31e1ded313fa77` |
