# s10 discovery findings

Codex (GPT-6), October14,2026 UTC. DEVELOPMENT, not confirmation.

The strongest constructive progress is a cheaper checked source compiler, a
small scalar audit policy, reusable source/response certificates, and a sharp
three-score dependence bound. These extend finite capability. They do not yet
support P3-POS01 or superiority over the strongest ordinary combination.

## Recorded fee and computation improvements

In [sf01 checked results](sf01/checked.json), each arm delivers3,584 outputs per
stratum across28 SATLIB sources, including four50-variable sources. At the
source-derived near-target tolerance, scalar prefix spends31,010 physical fee
and14,586,157 counted units; full relevant audit spends72,320 and16,123,044.
These are **57.12% fewer fees and9.53% fewer counted units**, including each arm's
source preparation and checking. The ordinary scalar-prefix implementation ties
every output and both bills. Exact threshold spends only9,657 fee but19,261,900
units; scalar threshold spends32,302 fee and14,453,502 units. Those tradeoffs are
part of the result, not exceptions to omit from its headline.

At fixed tolerance18, prefix spends66,991/15,857,399 versus full audit
72,320/16,123,044: only7.37% fee and1.65% counted-unit savings. One-query spends
32 fewer fees than prefix with more computation. The large near-target gain is
therefore task dependent. Neither tariff is an empirical application price;
native work, memory, storage and other unpriced costs remain unknown.

[Observed horizon analysis](horizon_analysis.json) includes every setup bill:
aggregate improvement in both components first appears and persists from28
requests per source at near-target tolerance, versus88 at fixed18. At128,
15 of28 near-target sources improve both components and10 have higher counted
computation; the other sources have ties or mixed outcomes. Fixed18 improves
both components on8 sources and has higher counted computation on17. No source
has higher physical fees in these selected complete runs. These are observed
prefixes, not extrapolated repayment forecasts. Pooling hides this heterogeneity.

[Exact component analysis](component_analysis.json) treats cost as fee+lambda
times counted units. Near-target prefix belongs to the observed ordinary-menu
lower envelope only for lambda between21353/4675743 and1292/132655, approximately
0.004567--0.009740 fee units per counted unit. Outside that interval, exact or
scalar threshold is better. Its identical ordinary mirror shares the interval.
No10% superiority interval over that full ordinary menu exists. Against full
audit alone, a10% two-component saving exists for lambda<=170390/377087, but
this excludes unknown costs and is not the F01 complete-cost event. At fixed18,
neither component improves10%, so no nonnegative weighting yields that margin.

## Source preparation and source changes

Unit propagation with original-clause reason checking reduces compilation and
checking from14,106,926 to1,390,207 counted units across39 sources, a90.15%
reduction against the previous ordinary branching compiler. On the24 external
20-variable sources alone the reduction is90.41%. This uses established SAT
techniques. It is an implementation improvement over a specific predecessor,
not a comparison with the fastest native solver or general polynomial SAT.

[up50](up50/design.json) prospectively selects four satisfiable and four
unsatisfiable50-variable SATLIB formulas. All eight unit compilations complete;
all eight prior branching compilations reach the50,000-state cap, with paid
prefix invoices preserved. Native PySAT independently agrees on satisfiability
and64 signed optimum values. One admitted source has1,362 models. Native tariffs
are unknown and its objective agreement does not independently prove model counts.

[Source conditioning](source_patches.md) handles168 original-CNF unit patches
on28 satisfiable sources. All exact model sets, signed objectives and1,008
negative controls pass;58 patches are unsatisfiable. Six patches per source cost
7,031,748 units including initial parent admission, versus23,141,569 for fresh
compilation, about69.61% less. All28 six-patch totals improve; only2 of28 first
patches repay setup. Forced variable layers must remain to preserve signed
costs. Positive regret certificates transport to a strengthened source only
when all action witnesses survive; lower witness pairs require both witnesses
to remain feasible. The counterexamples in source_patches.md make these limits
explicit. This is ordinary checked conditioning and amortization.

## Response reuse and stronger ordinary controls

The early complete-proof and retained-cover experiments establish the signed
regret bridge and finite prefix rules, but stronger ordinary threshold controls
often erase their practical advantage. rc04's prefix saves physical fees against
full audit while threshold slightly improves both its components. cp02 saves
two fees against threshold at a cost of414,824 additional counted units.

Positive affine response intervals, negative two-witness regions and response
neighborhoods avoid exact-value cache misses. rr01 reduces counted work relative
to repeated local proposals; a bounded optional budget in br01 cuts threshold's
physical fees15.34% at2.25% more counted work. The broader wt02 transfer loses
most of the fee benefit: neighborhoods spend85,738 fee versus full audit86,528,
and142,203,623 counted units versus27,073,614. That negative transfer result is
why the later scalar policy and source compiler matter. Every ordinary mirror
ties its corresponding mechanism. Proof reuse alone is not economic utility.

## Learning, incorrect laws and dependence

[rl01 checking](rl01/checked.json) reconstructs27,648 outputs,238,058 purchases
and540 learned policies. The confidence learner on independent uniform streams
spends10,224 fee/5,119,942 units versus full37,120/6,254,509. The empirical learner
and correctly specified frozen policy are cheaper still; exact threshold buys
far fewer observations but uses more computation. Endpoint laws make the
conservative learner fall back and add overhead. A changed law produces36
confidence-tail violations; none occur in the finite tests satisfying the stated
stationary-independent assumptions. This is not proof of calibration.

[The fee reserve](fee_reserve.md) gives the separate pathwise bound
total fees<=sum fallback fees+initial allowance. It survives wrong probability
models, but can exhaust exploration and does not bound complete cost or regret
to the best policy. [History-conditional interpretation](learning_interpretation.md)
clarifies the confidence argument: condition on valid past histories, not on a
future all-success event. The fixed-C expectation bound is(1+delta)TC, without
a new learning-rate claim.

[Three-score sharp bound](three_score_sharp.md) proves the exact worst prefix
survival probability from identical marginal laws with arbitrary dependence.
An explicit failure-mass allocation proves sharpness;47,520 exact allocations
and1,056 integer polygons screen its edge cases. Three elementary expressions
match all1,152 earlier exact coupling certificates and avoid their costly LP
enumeration. The sum of separately sharp prefix bounds need not be jointly sharp.
Robustness has a practical cost: applying the cheap formula to the28 exposed
near-target source duties gives a strict expected-fee bound below fallback on
only1 of25 nontrivial duties. That duty is uf50-03, bound51.793 versus65. These
are analytical predictions with zero new purchases, not measured service savings.

[Correlated learning](correlated_learning.md) supplies a next construction:
sample only representatives selected before the first purchase's outcomes, then
use a common conservative score law and the sharp dependence bound. The existing
rl01 learner does not implement it. This remains a proposed service extension.

## Contribution and next test

The work improves checked representations and gives explicit mathematical limits
on when observations, source changes and retained proofs can be combined. It
also supplies less expensive ordinary implementations that a future positive
claim must face. The induced regret objective, knowledge compilation, conditioning,
conservative reserves and marginal moment optimization all have ordinary prior
art; [literature](literature.md) distinguishes imported ideas from local proofs.

The next useful test is a fresh, bounded service combining cheap source admission,
source changes and response reuse where actual requests justify amortization,
with priced native/ordinary alternatives. The dependence-robust learner is worth
a small targeted test, especially the one analytical duty that survives its
conservatism. Do not repeat a broad expensive sweep before these bottlenecks are
resolved. F01 remains unchanged; no candidate is ready for confirmation.
