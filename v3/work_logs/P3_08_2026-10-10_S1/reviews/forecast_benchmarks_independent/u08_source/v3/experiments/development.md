# P3-08 — executable methods and matched ordinary controls

Contributor: **ChatGPT (GPT-6 Astra Pro)**. **DEVELOPMENT**, October 10, 2026.
Task: **P3-08**, attempt **P3-08-1**, session **2026-10-10-S1**.
Baseline main: `a818baf5b8838ac452ee77aa3d2ffd4d4fce0aad`.

**This development record implements a finite combined reasoner with live,
checked hard answers and preserves a valid statistical reference path. It
does not establish an economic advantage over the strongest ordinary
combination.** All queries, implementations, refinements and comparisons in
this directory are development material. No final population, hypothesis
threshold, challenge freeze or final evaluation is created here.

Task accounting and publication status are recorded in the
[session log](../work_logs/P3_08_2026-10-10_S1.md). That record must be closed
before task completion is inferred. The historical P3-06 addendum, original
B_1 checkpoint, selected option A recurrence and their source-bound failures
and results remain preserved. P3-09 and the optional recurrences are separate
author choices.

## 1. What changed and what the comparison means

The main new capability is an owned execution path which joins finite paid
learning to a versioned hard-answer store. A checked answer can change later
eligible actions and truth coordinates, including later requests in the same
block, while the original expert forecasts, selected purchase, random-bit
path and block update remain available for analysis. An epoch withdrawal
stops the current service even if the withdrawal itself cannot be fully
funded. Retaining an old name does not restore an old warrant.

Two mathematical constructions support the new interface. First, exact
observable corrections translate valid base performance intervals to the
live service on the same event. Second, a snapshot taken before block
selection gives a predictable alternative reference; changes learned inside
that block are then accounted for separately. A finite, predeclared rate
grid has an explicit union penalty. The implementation pays for calculating
these reports from public records and bought answers. It does not read
unbought evaluator truth.

The comparison also adds a general bounded CNF decision-program service,
checked DPLL and enumeration, proof-budget fallbacks, ordinary marginal
expected-cost decisions, exact caches, a combined ordinary controller, and
both fixed no-purchase actions. Paid hashing is available to both sides.
The structural arm independently reconstructs the accepted finite repair
and replacement semantics and executes changed-scope checks and fallback.

These additions support **P3-N01 at the existing modest formal-adaptation
and implementation-synthesis scope**. The useful delta is the explicit
composition and its checked limits. Ordinary probability/cost notation can
run the identical numerical kernel and invoice, and the independent
structural solver matches the finite outputs more cheaply on the declared
fixtures. Renaming those methods does not establish an additional
contribution. Affirmative **Q3 advantage remains open**.

### Services and quantities

| Quantity or service | Meaning in this record |
|---|---|
| Deterministic answer `y_t` | Whether the bounded input CNF program is satisfiable under its fixed Boolean interpretation. Random input generation does not randomize that truth. |
| Issued forecast `q_t` | A fallible dyadic prediction issued before the current computation. A current prior hard receipt can supply a singleton. Earlier forecasts remain immutable. |
| Terminal answer | The bit delivered at the current request's deadline. A successful current purchase can correct this bit without rewriting the issued forecast. |
| `F` | Sum of immutable issued Brier scores. This is a separate forecast diagnostic, not the terminal error count. |
| `V` | For the broker's lottery, the conditional mean of unselected terminal errors given its action-independent selection and hard history. The ordinary greedy policies do not inherit this action interpretation. |
| `Z` | Realized terminal error count, measured only in the separate private evaluator. |
| Local units | Actual paid operation bill under the declared method tariff, excluding its separately recorded installed source bundle. |
| Cold units | Local units plus the common installed source bill. This is a specified suite-installation service, not a claim to minimize binary size or startup cost. |
| Optional report | A paid, public-only local performance calculation, with a separate source and execution bill. It is not included in terminal-only rankings. |
| Free oracle diagnostic | The evaluator supplies correct answers and forecasts with zero charged work. It is expressly nonimplementable and excluded from paid policy rankings. |

The primary CNF comparison is the common terminal-answer and retained word
record service. Every method can inspect the same public queries and call
the same paid solvers. Methods need not pay for advice they do not use.
The common output format retains enough information to audit predictions,
terminal answers and knowledge status; it is not a minimal terminal-bit
transport. An ordinary implementation may also use the accepted candidate
kernel or an even leaner terminal interface. Neither possibility is excluded
to create an advantage.

For a fixed completed record, the symmetric priced objective is
`Z + lambda * cold_units`. Repricing that record does not rerun its decisions.
Each ordinary combination actually run at a different `lambda` is a different
acquisition/history path. A retrospective minimum over a catalogue of records
is a comparison summary, not a free deployable method which knows which
record will be best.

## 2. Executable methods and source contracts

### Deterministic program arm

[p308_cnf.py](p308_cnf.py) admits immutable, canonically sorted CNF programs
with 1–12 variables, at most 64 clauses and clause width at most four.
Duplicates and tautologies remain in the supplied encoding. Public supplier
sorting performs no truth computation; deployed admission and input reads
are charged. A complete semantic key includes interpretation version,
source version, variable count and every clause/literal. A changed request
ID may reuse the same mathematical answer; a changed source version may not.

The provider offers complete assignment enumeration and complete DPLL with
unit and pure-literal propagation. Successful SAT answers receive a separate
clause/witness check. UNSAT receives an independent complete assignment check
or a separately checked empty-clause/opposing-unit certificate. A capped or
failed search supplies no hard answer, and its actual spent work is retained.
The maximum source envelope is computed from public shape, not from the
answer or a subsequently observed cheap run. This small finite family is
not a hardness claim or an assertion that these are optimized SAT solvers.

The tariff records bounded word operations for admission, source enrolment,
literal evaluation, checking, acquisition, caching, storage, advice,
fixed-width arithmetic, selection, random bits and output. Numeric operations
pay before their bounded result is allocated. The implementation environment
and tariff treat certain finite primitives as units; the invoice does not
claim to count Python interpreter instructions, operating-system work,
physical CPU time or whole-process heap bytes. Source closure and the
environment are recorded separately in every sealed run.

| Method | Behavior and admitted information | Guarantee boundary |
|---|---|---|
| `finite_uniform` | Six fixed syntactic binary experts, finite-state mixture, one uniform checked purchase per block; fixed lottery actions. | Inherited selective-feedback result under the actual quota, bits, exogenous tape and funding premises. |
| `finite_tickets` | The same base mechanism with paid whole-block public lookahead and a positive ticket distribution favoring disagreement relative to a public fee proxy. | Actual propensities are owned and recorded; the fee heuristic is not an optimal computation policy. |
| `value_uniform`, `value_tickets` | The corresponding base path plus paid live hard answers, retaining every original forecast/action statistic. | Pointwise corrections and the new report constructions apply. Purchases are not skipped when an answer becomes known. |
| Hashed value variants | The same candidate output, selector, receipt, action-bit and update paths with paid hard-key indexing. | Complete-key and scope checks remain mandatory, even for hash collisions. |
| `probability_cost` | The same public expert library and a uniform paid feedback schedule, with greedy marginal expected-cost actions. | No inherited lottery-action theorem; the fallible marginal is not a coherent law of arithmetic truth. |
| `proof_enumeration`, `proof_dpll` | Attempt a checked computation under a fixed 2,048-unit provider cap; retain a named fallback when unresolved. | A failed proof attempt is not a refutation. All attempts, including failures, are charged. |
| `exact_enumeration`, `exact_dpll` | Complete paid computation and check for every query. | Exactness is conditional on this admitted finite service and sufficient resources. |
| `exact_cache`, `exact_cache_hashed` | Complete checked DPLL on a cache miss, with paid FIFO retention and full-key current-version reuse. | No free prepopulation or omitted original acquisition bill. |
| `ordinary_combo`, hashed variant | Greedy costs, paid syntactic experts, a fixed exploration schedule, checked cache, optional capped DPLL probes and optional full purchases based on public/previously observed costs. | A credible explicit combination, not an optimized value-of-computation theorem or a proof of price-monotone total spending. |
| `no_compute_0`, `no_compute_1` | Deliver the separately named fixed bit, paying admission and the common output/retention service; no expert, random or provider work. | Neither uses evaluation truth to choose the better fixed answer. |
| Ordinary kernel mirror | Interpret the same `q` as the ordinary marginal cost pair `(q,1-q)` and call the same paid kernel. | Exact implementation equivalence; not another independent experiment or evidence for a notation advantage. |

The primary implementation files are [broker](p308_broker.py),
[ordinary controllers](p308_ordinary.py), [shared hashed cache](p308_hashcache.py),
[ordinary mirrors](p308_mirrors.py), [priced reporter](p308_reporting.py) and
[common tariff adapter](p308_common.py). The closure also includes the three
unchanged P3-07 selective-feedback/adapter files named in each source manifest.

### Hard evidence, failures and resource limits

The owned broker, not an arbitrary external caller, generates the selector,
records the actual propensity, performs the selected purchase, absorbs the
provider invoice and binds the returned receipt to the exact query, source,
provider and version. Local typed records are not cryptographic authentication
of a remote provider. A receipt validator alone would not license a different
caller to choose labels or propensities after seeing outcomes.

Hard answers form a finite, versioned conjunction of received Boolean
coordinates. Unknown coordinates retain `[0,1]`; a sound received bit fixes
its own coordinate. This implementation does not infer unreceived
cross-query Boolean relations. Conflicting current answers supply no active
warrant. Append-only history plus generation changes prevents returning to
an earlier epoch label from silently reviving an old answer. New index nodes
and entries are committed only after their combined charge is admitted.

The all-path funding envelope reserves the maximum possible checked purchase
in each public block and bounds the controller, numerical, storage and bit
work. It uses no average bucket occupancy or lucky seed. Capacity must also
cover the successful quota. A completed underfunded realization retains its
observed result but does not establish the successful-purchase statistical
premise. Reporting has a separate completion envelope.

Seven real broker boundary defects were found and repaired during review,
including fail-open withdrawal, malformed inputs/solver names, mutation of
returned trace aliases and a post-horizon block attempt. The original
findings, failed checks, amended check assumption and repaired source are
preserved in the [review directory](../work_logs/P3_08_2026-10-10_S1/reviews/).
The subsequent hashed index passed collision, conflict, stale-generation,
atomic-denial, funded-cap and output-path checks; its
[design and cap](../work_logs/P3_08_2026-10-10_S1/reviews/hard_hash_index/design_and_cap.md)
has a separate same-model reconstruction.

## 3. Live performance reporting and its limits

### Exact correction of a retained base path

Let `H_t` indicate that a current sound answer is known immediately before
issue. The base purchase/update/bit path is retained. For its immutable
forecast `q_t`, the observable corrections are

\[
\Delta_F=\sum_{H_t}(q_t-y_t)^2,\qquad
\Delta_V=\sum_{H_t,\,t\text{ unselected}}d_t,\qquad
\Delta_Z=\sum_{H_t,\,t\text{ unselected}}
  \mathbf 1\{a_t^{\rm base}\ne y_t\},
\]

where `d_t=q_t+(1-2q_t)y_t` is the base lottery error mean. Every truth bit
used in these corrections already has a current checked receipt. Pathwise,
`F_live=F_base-Delta_F`, `V_live=V_base-Delta_V`, and
`Z_live=Z_base-Delta_Z`.

Subtracting the exact correction from both endpoints of a valid base interval
is valid on the same event. This is stronger than inferring an upper bound
from domination alone: domination would not justify a lower bound. The
corrected Brier and conditional-action centers retain the shared base
sampling residual, including when the current selection influences which
later same-block requests become known. The
[complete derivation](../derivations/08_live_hard_performance.md) preserves
the counterexamples to naive live-vector centering.

### Predictable snapshots and a predeclared grid

At block entry, freeze which coordinates already have sound answers. This
snapshot is predictable before the block selector. Its zero residual on
known coordinates can reduce the conditional range and quadratic bound.
Answers newly learned inside the block are handled by the exact translation
above, rather than being inserted retrospectively into a supposedly
predictable vector. Hard-disabled episodes use a zero hard mask throughout.

The [snapshot derivation](../derivations/08_snapshot_live_reporting.md)
also permits a fixed finite rate grid determined by the public horizon and
selector. With `J<=9` rates, its integer confidence penalty is
`c=ceil(log2(80J))`; optimizing over that declared grid is licensed by a
finite union bound. Choosing a reporting basis after inspecting episode
outcomes needs a separate allowance. A smaller quadratic term does not
guarantee a tighter final interval: the grid penalty, changed center and
deterministic clipping matter.

The default bounds are joint, two-sided, fixed-end 95% for the declared
episode's `F,V,Z`, subject to the stated fair-bit, soundness, predictability,
selection and all-path-completion premises. They are not simultaneous over
all arms, anytime bounds, calibrated truth probabilities or a future
generalization guarantee. The public report checks its interface and funding
conditions; it cannot establish physical fair bits by examining a seeded
development run. When every unselected live answer is already known, the
service can also identify the exact `V=Z=0` and fully observed Brier total.

[p308_reporting.py](p308_reporting.py) uses paid bounded integer arithmetic,
full public-key and receipt checks, explicit storage and exact rational
output pairs. Its universal completion allowance is deliberately generous,
`2^48` word units; observed bills are much smaller. A low reporting budget
retains the failed invoice and emits no purported confidence interval.

### What the development reports show

The first common comparison produced 45 public reports. The new reporting
constructions were then applied, explicitly retrospectively, in four ways
to each of those 45 saved broker traces. All **180** exact independent
formula comparisons passed, with no private-score reads in that independent
audit. The snapshot quadratic term was strictly smaller on **15 of 45**
episodes. Snapshot/grid radii were smaller than base/fixed on **16**, but
larger on **29**; they were larger than snapshot/fixed on **30**. These
adverse results are retained. Often deterministic caps leave the reported
terminal endpoint unchanged despite a smaller raw radius.

The new common comparison separately executed **63** public snapshot/grid
reports. All corrected identities and shared residuals passed subsequent
private comparison. No uncovered interval was observed on these saved
traces. That last fact is only an implementation diagnostic; it is not
evidence establishing 95% coverage.

An independent endpoint audit makes the practical limitation more precise.
Among the 63 new reports, statistical intervals strictly improve the
deterministic **upper** endpoint in 6 Brier, 6 conditional-action and 11
realized-action records; no lower endpoint improves. There are 11 records
with any endpoint gain and no empty confidence conflicts. Among the 180
retrospective replays, the corresponding upper-endpoint counts are 36, 36
and 59, again with no lower gain. Within a fixed reporting basis, the grid
improves some raw radii but **none of the delivered interval endpoints** in
that replay. These are counts of records, not independent trials. A more
sophisticated radius is not automatically a more useful delivered report.

The [exact budget-selection witness](../derivations/08_budget_selection_counterexample.md)
shows why completion cannot casually become a conditioning event. In an
explicit sixteen-block toy provider, all `65,536` selector strings can be
enumerated: an underfunded account completes on only `17`, and the Brier
interval fails on every one of those completed paths. The unconditional
failure probability is still only `17/32768 < 1/40`. Its public toy fees are
separate from the CNF tariff; the witness isolates the funding assumption
instead of alleging that seeded CNF runs verify coverage.

## 4. Development design and terminal-answer comparison

The [first plan](../work_logs/P3_08_2026-10-10_S1/development/comparison_plan_v1.md)
preceded generation of these public cohorts. The
[additive second plan](../work_logs/P3_08_2026-10-10_S1/development/comparison_plan_v2.md)
followed inspection of the first results. It deliberately strengthens
controls and indexing on the same exposed development tapes; it is not
held-out confirmation.

| Public cohort | Requests | Construction and purpose |
|---|---:|---|
| `cold_mixed` | 64 | Bounded public CNF generator with seed 3081013, several variable sizes, shapes and densities, and declared repeat positions. It probes cold computation and heterogeneous fees. |
| `repeat_online` | 128 | The first 32 public programs repeated four times with new request IDs. Identical keys already present among the first 32 are retained; there are 28 distinct keys here. It admits strong online exact reuse. |
| `cheap_structure` | 64 | Four repeated 12-variable programs: opposing units, positive units, empty conjunction and an empty clause. These intentionally expose inexpensive ordinary shortcuts. |

All three stochastic policy seeds are retained: **11, 29, 47**. The first
closure has 114 executions; the stronger second closure has **186**, all
complete. Deterministic controls are executed once rather than counted as
three independent replications. Public policy and report records are sealed
before the separate bit-mask truth evaluator runs. There are 60 distinct
program keys across the full cohort collection. The evaluator's truth API is
not an import of any policy.

The second common closure contains eleven files and 224,740 bytes. Each run
pays the same **48,274-unit** core source bill. Its terminal comparison keeps
the optional reporter's source and execution invoice separate. The actual
source snapshots, hashes, Python/platform record, public seal and private
score seal are in
[common_v2](../work_logs/P3_08_2026-10-10_S1/development/common_v2/).

### Representative exact records

The following are seed 11 records, with **local** units for readability.
Add 48,274 to each for the specified cold installation. All other seeds,
prices, successes and adverse outcomes remain in the machine-readable
scores and exact [analysis](p308_analyze.py); this table is not a selected
evaluation population.

| Cohort | Method | Terminal errors | Local units |
|---|---|---:|---:|
| Cold | Finite uniform | 16 | 369,343 |
| Cold | Live uniform, hashed | 16 | 425,658 |
| Cold | Finite tickets | 16 | 247,426 |
| Cold | Live tickets, hashed | 16 | 299,162 |
| Cold | Probability-to-cost | 12 | 545,553 |
| Cold | Ordinary combination, hashed, `lambda=1/100000` | 0 | 1,018,527 |
| Cold | Exact DPLL | 0 | 2,009,348 |
| Cold | Exact cache, hashed | 0 | 2,120,344 |
| Cold | Fixed answer one, no purchase | 31 | 14,538 |
| Repeated | Finite uniform | 28 | 2,905,607 |
| Repeated | Live uniform, hashed | 20 | 3,039,592 |
| Repeated | Finite tickets | 41 | 526,319 |
| Repeated | Live tickets, hashed | 32 | 641,839 |
| Repeated | Probability-to-cost | 29 | 2,274,379 |
| Repeated | Ordinary combination, hashed, `lambda=0` | 0 | 2,189,022 |
| Repeated | Exact cache, hashed | 0 | 1,874,485 |
| Repeated | Either named fixed answer, no purchase | 64 | 28,944 |
| Cheap structure | Finite uniform | 10 | 52,629 |
| Cheap structure | Live uniform, linear | 2 | 65,478 |
| Cheap structure | Live uniform, hashed | 2 | 68,480 |
| Cheap structure | Exact DPLL | 0 | 48,808 |
| Cheap structure | Exact cache, linear | 0 | 24,515 |
| Cheap structure | Exact cache, hashed | 0 | 27,414 |
| Cheap structure | Either named fixed answer, no purchase | 32 | 9,176 |

Hard answers deliver their promised pointwise improvement on repeated known
queries, but that improvement has a bill. For repeated seed 11 uniform
execution, hashed hard integration saves eight terminal errors and adds
133,985 units. For those two fixed realized paths it helps the priced
objective only below `lambda=8/133985`; this is a retrospective repricing
identity, not a learned or optimal acquisition rule. On the cold seed 11
paths, hard integration saves no errors and adds work.

Hashing also has a visible limit. On cold/repeated tapes it reduces lookup
work while preserving the mathematical trace and selected checked answers;
the operation invoice changes. On the four-key
cheap cohort it increases both candidate and ordinary cache bills. For
example, the exact linear cache costs 24,515 units and its hashed counterpart
27,414 for the identical zero-error service. The comparison does not hide
the cheaper linear option.

The optional report is material: seed 11 live hashed uniform execution adds
315,906 report units on cold queries, 843,012 on repeated queries and 62,016
on cheap structure. These are actual additional source-plus-execution bills.
The report may be useful as a separately requested service; its existence
does not make terminal answers cheaper or establish a superior ordinary
comparison under unequal delivered reports.

### Adverse controls and economic interpretation

For all declared prices `0, 1/100000, 1/10000, 1/1000, 1/100`, the exact
native-price catalogue comparison retains all ordinary controls. At seed 11,
positive-price winners are the ordinary combination on the cold tape at
`1/100000`, the hashed exact cache on the repeated tape at that price,
the linear exact cache on the cheap tape through `1/1000`, and a named
no-purchase answer when computation is sufficiently expensive. The complete
seed-wise table is in the analysis output. A best-in-catalogue choice made
after evaluation is not presented as a deployable oracle. In addition,
every candidate has its identical ordinary-kernel interpretation.

Exact enumeration is deliberately retained even where DPLL is much better.
On cheap structure, seed 11 complete enumeration costs 7,506,888 local units
and DPLL 48,808 for the same zero-error terminal service. The bounded DPLL
fallback can also have more errors than bounded enumeration on a different
tape; a shorter producer path is not a universal capped-service advantage.
Exact computation's earlier half forecasts can have substantial issued
Brier loss while its eventual terminal answers have zero errors. Those
metrics must not be combined into one accuracy ordering.

The ordinary combination's cost estimate is a public shape proxy or the mean
of its own earlier successful full purchases. Failed full calls remain
censored, not rewritten as cheap completed answers. Capped failures and
changed information can still make its behavior inefficient. Its mandatory
exploration purchases can be costly at high prices; the no-purchase endpoints
make that limitation visible. No optimal value-of-computation conclusion
follows from comparing estimated immediate error with a prospective fee.

One exact trace demonstrates nonmonotone spending. On repeated seed 11,
raising the hashed combination's price from zero to `1/100000` changes its
local bill from **2,189,022 to 2,192,224** units and its errors from zero to
one. The higher price skips an initially productive full purchase after a
capped failure; later information and cache state diverge. Capped failures
increase from 13 to 18, total provider attempts from 41 to 44, and cache hits
fall from 100 to 82. Provider work rises by 8,192 units while other work falls
by 4,990, giving the exact **3,202-unit** net increase. The
[independent trace review](../work_logs/P3_08_2026-10-10_S1/reviews/common_v2_analysis/review.md)
retains the first decision's public estimate and actual invoice. This is a
counterexample to a price-monotone interpretation of this heuristic, not to
ordinary expected-cost arithmetic.

### Forecast quality and the contribution of learning

The [forecast audit](../work_logs/P3_08_2026-10-10_S1/development/forecast_benchmarks/)
reads the already sealed advice, forecasts and private evaluation truth.
It compares the six named fixed experts, constant one half, and an unchanged
equal-weight mixture, both exact and dyadically truncated. These are
explicit evaluation benchmarks, with **no new paid deployment claim**.
The hindsight best expert is not chosen by a deployable oracle. The perfect-
foresight evaluator diagnostic has zero Brier and terminal loss, with no
claim that its answers or computation are available to a policy for free.

The 63 method/source records contain **18 scenario/selector/seed
configurations**. The base learner beats the half forecast and both static
equal mixtures in every one. It beats the best individual expert on all six
repeated-query configurations, and loses to that benchmark on the twelve
cold/cheap configurations. This is more informative forecast evidence than
the old modular-family null result, which is still retained below.

To separate learning from already acquired truth, the audit also gives each
benchmark exactly the same hard answer wherever that answer was current
before issuance. This reuses the recorded learner acquisition history; it
does not execute the static benchmark with its own ticket selector or paid
information policy. Such a policy could acquire a different hard history.
The table counts better/equal/worse Brier outcomes across the 18
configurations; hard-disabled live outputs equal the base outputs.

| Forecast comparison | Base, all issued positions | Hard-on live, matched known answers |
|---|---:|---:|
| Versus constant one half | 18 / 0 / 0 | 17 / 0 / 1 |
| Versus hindsight best fixed expert | 6 / 0 / 12 | 7 / 0 / 11 |
| Versus static equal mixture, exact | 18 / 0 / 0 | 11 / 0 / 7 |
| Versus static equal mixture, dyadic | 18 / 0 / 0 | 11 / 0 / 7 |

All seven adverse matched-live/static configurations are retained: the six
cheap-structure configurations and repeated uniform seed 11. The sole
matched-live/half loss is cheap-structure uniform seed 29. This subset is
determined by the episode's prior information history, so the counts are
descriptive and establish no IID or population claim. Lower Brier does not
by itself imply fewer terminal errors or a better objective after paying
for selected answers. The independent reconstruction checked every exact
score and chronological hard mask on all 5,376 recorded positions.

The inherited fixed-expert bound keeps its **original comparator**. Writing
`F^H=F-Delta` and `F_i^H=F_i-Delta_i`, the live-versus-upgraded-expert
excess is `F^H-F_i^H=(F-F_i)+(Delta_i-Delta)`. The last term has no
established nonpositive bound. Pointwise improvement of the learner therefore
transfers its applicable upper bound against the original fixed expert, and
does not establish regret against an expert that is also corrected on the
realized hard mask. The matched-history table is an empirical development
comparison only; it does not strengthen U08's theorem.

### Paid selected-receipt reuse with an unchanged learning path

The separately justified [reuse construction](../derivations/08_selected_receipt_reuse.md)
distinguishes one selected logical receipt per block from a new physical cold
computation. A paid checked cache hit can supply that receipt while the
selector, actual propensity, base/live forecast, update and action-bit paths
remain identical. The adapter changes its provider identity and bill; it does
not drop or reallocate the selection. Each episode owns a fresh instance,
and its 131,072-unit additional service envelope covers full collision scans
and retention. An ordinary kernel can use the same adapter.

The current adapter is **p308-selected-receipt-cache-v1.1**. Independent review
found that v1 could pay 48 initial units, fail its response prepayment, and
still return a typed direct failure record. V1.1 admits accounts of at least
576 units and prepays its conservative response first. Below-minimum rejection
admits no paid work; later denial returns a paid no-answer response and retains
its spent prefix. The exact successful fee increase is `512-Q` for a Q-word
key. Every earlier source, failure and completed v1 record is preserved.

The amended source-bound matrix repeats the same **48** exposed development
episodes: 36 repeated-tape rows across both selectors, hard off/on and three
seeds, plus 12 cold/cheap seed 11 rows. All complete. All **32 paired
mathematical paths and report contents match exactly**, including weights,
blocks and consumed bits. All pairs reduce physical cold calls, but only
**12 save units; 20 cost more**. Those counts include coupled source/feature
variants and are not independent evidence for a success probability.

Each amended row pays the same **50,115-unit** source bill. This is 1,841
above common_v2's bill, entirely due to procuring the added adapter. Adding
that common source cost to older unchanged-policy records is an explicitly
labelled accounting transfer, not a rerun. The following are local seed 11
hard-on bills, with identical errors within every row comparison:

| Cohort / selector | Errors | Cold provider | Linear reuse | Hashed reuse | Cold calls with reuse / logical receipts |
|---|---:|---:|---:|---:|---:|
| Repeated / uniform | 20 | 3,039,592 | 1,958,131 | 1,896,683 | 23 / 32 |
| Repeated / tickets | 32 | 641,839 | 700,899 | 679,409 | 17 / 32 |
| Cold / uniform | 16 | 425,658 | 485,695 | 468,754 | 15 / 16 |
| Cold / tickets | 16 | 299,162 | 339,275 | 329,918 | 14 / 16 |
| Cheap / uniform | 2 | 68,480 | 76,955 | 77,922 | 4 / 16 |
| Cheap / tickets | 6 | 72,801 | 81,768 | 82,914 | 4 / 16 |

The exact invoice decomposition explains the mixed result:
`net units saved = avoided cold-provider units - added adapter units`.
Repeated uniform seed 11 hashed reuse avoids **1,234,954** cold units and
adds **92,045**, saving **1,142,909**. The ticket path avoids only **30,033**
and adds **67,603**, losing **37,570**. A high hit count alone says little
about economic value when the avoided computations were cheap. Across all
32 pairs, nonprovider operations and report invoices are identical; remaining
account limits differ as expected. The
[exact decomposition](../work_logs/P3_08_2026-10-10_S1/development/selected_receipt_reuse/analysis_v1_1/)
and [independent source review](../work_logs/P3_08_2026-10-10_S1/reviews/cached_service_v1_1/review.md)
bind all 896 cached selected invoices, 530 cold children and 366 hits.

### Known asymmetric stakes and normalized units

A further [declared extension](../work_logs/P3_08_2026-10-10_S1/reviews/asymmetric_results_v1_1.md)
uses the unchanged ordinary v1.4 source on the cold tape, with normalized
`(FP,FN)` stakes `(1/2,3/2)`, `(1,1)` and `(3/2,1/2)`, and resource prices
zero and `1/10000`. It retains 57 complete records: 45 fresh executions and
12 explicitly source/settings/tape-matched symmetric reuses, producing 54
normalized economic rows. All share the 48,274-unit original source bill.

The ordinary base action is one exactly when `q > FP/(FP+FN)`, with ties
choosing zero. Its thresholds are one quarter, one half and three quarters.
All twelve raw `(1,3)` executions at twice the normalized resource price
produce identical actions, purchases, states and resource totals, and exactly
twice the normalized objective. The scale is supplied to the executing policy;
this is more than dividing a final reported score by two.

For `probability_cost`, the information and q paths are unchanged by the
stakes. This isolates the readout effect. Mean weighted task loss is **7**
under low-FP stakes, against **23/2** when merely repricing the old symmetric
actions; under high-FP stakes it is **23/2**, against **55/6** for those
repriced symmetric actions. The first improves by `9/2`; the second worsens
by `7/3`. Issued Brier and resource bills are unchanged. Correct expected-cost
algebra is compatible with a worse realized decision when q is inaccurate.

In contrast, the combined controller's acquisitions change at `1/10000`.
All six asymmetric-versus-symmetric comparisons have different provider
invoice sequences, changing 12–40 later base forecasts per configuration.
These are fresh information paths, not fixed-history repricing. A supplied
constant-action endpoint still has the lowest recorded objective at that
nonzero price in each orientation. The first harness attempt's tuple/list
comparison failure is retained; its full public archive is byte-identical to
the corrected attempt, and it received no private scoring.

### Intermediate prices: a useful policy regime with a strict interpretation

The five native prices do not establish a ranking over every positive price.
The [exact price-envelope analysis](../work_logs/P3_08_2026-10-10_S1/development/price_envelope/)
therefore solves every pairwise inequality for all **234** completed common_v2
and amended-reuse records, separately by scenario/seed. It uses each recorded
combination's **fixed acquisition parameter**, and reprices its observed
terminal errors and units. It does not execute the native controller at a new
price. All old records receive the same explicit 1,841-unit source-procurement
transfer, making the shared installation bill 50,115; optional reporting stays
outside this terminal-answer comparison.

For seed 11, the finite ticket policy is a lowest-cost recorded line on the
cold tape for `10/429931 <= lambda <= 15/232888`. The live hashed ticket policy
with cold selected receipts is a lowest-cost recorded line on the repeated
tape for `16/616323 <= lambda <= 4/118297`. At endpoints the adjacent lines
tie. The cheap cohort's linear exact cache remains the frontier until
`lambda=32/15339`, followed by a supplied constant answer. Every interval is
checked with exact rational arithmetic against all supplied lines.

This establishes a useful **fixed-record intermediate-price regime** for
some paid-feedback policies among the listed configurations. The identity
ordinary-kernel interpretation remains available on every candidate frontier
line, so it establishes **no advantage over that strongest ordinary
implementation**. The envelope is a hindsight catalogue, not a deployed
method selector or evidence for an unexecuted native-price acquisition rule.
Seed variation and all ordinary frontier segments, including bounded proof
evaluation and no-computation endpoints, remain in the complete results.

The prior negative result is unchanged: in option A's `T=3968, B=8`
development comparison, historical uniform v1.1 used **1,039,110 units with
1,702 errors**, adaptive fixed state **1,382,703 with 1,754**, and the cold
ordinary exact table **171,880 with zero errors**. Current uniform v1.2 adds
26 registry units by source transfer, not by a rerun. That source-specific
obstruction remains in its original archives and
[recurrence checkpoint](../checkpoints/B_1_R_P3_B_A.md).

## 5. Structural, counterpossible and transport integration

The separate [structural implementation](p308_structural.py), version
**p308-structural-v4.1**, executes the inherited P3-04/05 interfaces against an
independently written ordinary finite structural/repair solver. This arm and
the selective-feedback broker are distinct implementations. The learner has
not been made into a counterpossible inference engine.

Both structural methods receive the same constraints, dependencies, source
cases, repair ranks, action losses and output obligation. Each pays for its
own source admission, inputs, search, checking, retention and readout. The
paid resource-failure API covers the **nine exact published fixtures on
CPython 3.12.14**, with admitted integer budgets at least 100,000 units.
This is a finite source-bound contract; no arbitrary-input or different-runtime
completion claim follows. The transport demonstration uses its separately
declared fixed 50,000,000-unit account.

### Genuine counterpossible content and all tied alternatives

The original quoted contradiction has **zero ordinary Boolean satisfying
valuations**. The exceptional paired-support interpretation and its repair
rule are supplied explicitly, while the original ordinary interpretation is
retained. There are two tied minimizing alternatives. Both are included in
the receiving decision: one fixed implementable action has worst loss **3**.
The labelled casewise action oracle has loss **0**, but cannot be deployed
without learning which hidden case obtains. It is a free diagnostic, not an
ordinary competitor with the same information.

When unresolved external source cases are added, repair minimization occurs
inside each source case. Selecting whichever source is easiest would instead
give the misleading value zero; keeping all supplied sources outside that
minimization preserves fixed-action loss three. The fixed-falsity example
remains infeasible. Conditioning on the false original antecedent is also
infeasible, while occurrence, actor, shared-code, stored-copy and predictor
replacements are distinct supplied changes, with recorded commitment losses
**7, 7, 5, 4, 2**. The output depends on the declared operation and dependency
structure; observational agreement does not identify those missing choices.

### Matched outputs and current charges

All nine candidate/ordinary outputs agree exactly, and the ordinary solver is
cheaper in all nine cases. These are **STRUCTURAL-VM-v1 event-tariff units**.
They have no declared exchange rate with the CNF word units above.

| Published fixture | Candidate units | Ordinary units | Result |
|---|---:|---:|---|
| Counterpossible, tied minima | 833,231 | 403,492 | Equal |
| Unresolved external sources | 1,075,376 | 616,776 | Equal |
| Fixed falsity constant | 181,480 | 106,210 | Equal |
| Conditioning | 114,776 | 72,133 | Equal |
| Occurrence replacement | 123,850 | 80,690 | Equal |
| Actor replacement | 123,052 | 80,915 | Equal |
| Shared replacement | 123,094 | 80,923 | Equal |
| Shared and stored-copy replacement | 123,014 | 80,873 | Equal |
| Shared, copy and new predictor | 123,240 | 81,078 | Equal |

The transport result has the same 3,223-byte terminal payload and bounds
`-1 -> 1 -> 3`: objective repricing adds two, then withdrawal of the `q`
frame requires a fresh check. On each scope change, an actual attempt to read
the prior warrant is rejected before the new calculation. The candidate
spends **496,823** units; the ordinary implementation spends **388,681**.
A forged proof and an ordinary false-bound attempt are separately rejected,
retaining their **19,489** and **26,495** paid units. Equal output plus more
cost is an adverse result for the candidate implementation, even where its
explicit dependency interface is useful.

### Resource failure and the exact tariff boundary

The measured primitive is a worker `opcode` trace event, with an additional
unit for each bounded worker `c_call` event and explicit source/input/storage/
terminal-byte charges. It is not every interpreter operation, physical CPU
time or whole-process heap use. The
[authoritative additive tariff note](../work_logs/P3_08_2026-10-10_S1/development/structural/tariff_v4_1_scope_note.md)
supersedes broader wording in older notes without changing any invoice.

Review found real gaps in the earlier handler: source/input admission and
success serialization could fail outside the paid failure path. The amended
handler covers those stages and protects a 1,024-unit failure tranche inside
its terminal reserve. Its fixed UNKNOWN/no-answer/no-warrant response costs
**142 units**: two observed worker opcode events and 140 bytes. Genuine
post-admission failures preserve spent prefixes of **88,504** and **49,321**
units, for final bills **88,646** and **49,463**. A denied operation itself is
not charged, and a failed computation yields no action warrant.

All **15 focused boundary checks** pass, including fresh-process first-call
tracing, source/input denials and explicitly labelled terminal fault
injections. The first tracing probe failed and is preserved. Earlier v1–v3
mathematical outputs remain historical evidence; their invoices do not support
the corrected full event-charge claim. The
[v4.1 analysis](../work_logs/P3_08_2026-10-10_S1/development/structural/analysis_v4_1.md),
copied sources, amendments, complete invoices and independent reconciliations
identify exactly which implementation now supports that claim.

## 6. Five-question and 21-duty disposition

**P3-N01 remains SUPPORTED at modest formal-adaptation and implementation-
synthesis scope.** The new contribution is the finite composition: owned
selection and current receipts, immutable historical forecasts, live hard
resolution, justified public report transformations, charged computation and
observable failure/version boundaries. The concentration tools, ordinary
expected-cost algebra, exact solving and caching remain ordinary antecedents.
No priority or generic algorithmic superiority is asserted. Negative results
alone would not establish the constructive contribution.

The major change from the option-A overlay is **U04's finite integration gap
is closed for the owned CNF broker**. A current sound answer fixes the next
eligible live coordinate and stale authority is withdrawn. This does not
implement a universal combined reasoner, arbitrary cross-query inference, or
a joint integration with the separate structural arm.

| Primary question | Current answer and consequential limit |
|---|---|
| **Q1 — logical uncertainty** | Executable paid finite forecasts now coexist with current hard answers and immutable scoring history. The learned marginals are not a coherent joint law of arithmetic truth. |
| **Q2 — logical counterfactuals** | The supplied change/repair operations, tied alternatives, fixed receiving actions and genuine counterpossible distinction have paid finite executions. The ordinary solver matches their answers and is cheaper; structural and exception-policy identification remain supplied assumptions. |
| **Q3 — multiple useful fallible models** | There is a specified fixed-library guarantee and a stronger ordinary comparison. **Affirmative benefit over the strongest credible ordinary combination remains open.** An identical ordinary kernel can reproduce the candidate's service and bill. |
| **Q4 — usefulness when thinking costs** | Hard corrections, paid reporting, actual propensities and failure invoices close specific finite interfaces. The declared allocation and acquisition heuristics are not optimal; higher computation prices need not lower their realized total bills. |
| **Q5 — probability information in values** | Known stakes determine exact ordinary action thresholds and units; public loss centers share a precisely identified residual. These identities do not turn a fallible loss estimate or sampling interval into a recovered joint truth law. |

The following covers **all 21 original duties**. “Inherited” retains the
earlier theorem and every stated premise; it does not import that theorem into
the new learner. This is an additive implementation assessment, not another
P3-B gate or an authorization to advance beyond P3-08.

| Duty | P3-08 disposition and boundary |
|---|---|
| **U01 — admitted bounded computation** | Extended finite implementation: owned selection, labels, bits, hard state and public reports use admitted information and explicit tariffs. Structural execution has its separate nine-fixture/runtime scope; no global CPU/heap or malicious-code guarantee. |
| **U02 — evidence and failure states** | Checked answers, pending/unknown, conflict, stale scope and resource/receipt failure remain distinct. Failed prefixes retain their bills and are never scored as observed false labels. |
| **U03 — represented Boolean coherence** | Earlier conditional finite semantics are inherited. The hard store represents only a conjunction of received coordinates; the numerical forecast vector is not a coherent joint law and does not implement unreceived entailment closure. |
| **U04 — hard resolution and dependencies** | The finite owned-broker integration gap is closed: sound current receipts harden eligible coordinates, preserve old forecasts and invalidate stale authority. Exact translations and predictable snapshots justify the composed performance estimates. |
| **U05 — eventual correctness** | Earlier fixed-query results retain their stream, soundness and capacity premises. Retaining one current exact answer is not a proof that all unresolved queries will be discovered, or a new infinite-stream convergence theorem. |
| **U06 — prediction before resolution** | New issued forecasts and all paid advice precede current receipts. Exact repeat reuse is post-resolution knowledge, not anticipatory learning. An economical advantage on fresh mathematics remains open. |
| **U07 — calibration** | Earlier calibration/selected-feature scope remains separate. Aggregate Brier/action confidence intervals establish no calibration, coherent law or Logical Induction non-exploitation claim. |
| **U08 — fixed-expert learning bounds** | The accepted base selective-feedback path is retained. Sound corrections transfer applicable upper bounds against the original fixed experts, not against an expert upgraded with the realized hard-answer mask. Adaptive-policy regret and greedy-action guarantees are not imported. |
| **U09 — feedback timing and selection** | Exact positive propensities, exogenous tapes, frozen blocks and one successful selected receipt remain essential. The live correction has its own argument; arbitrary missing, delayed or action-dependent discovery needs another one. |
| **V01 — typed values and losses** | Deterministic truth, hard evidence, fallible forecasts, action lotteries, realized loss, confidence intervals and resource invoices are distinct. The structural event tariff is separate from the word tariff. |
| **V02 — information recovery** | Earlier finite source/fiber characterizations remain. The new exact shared-residual identities recover specified loss relationships, not an entire probability law or extra mathematical answers from a scalar cost. |
| **V03 — forecast-to-action bridge** | Sound pointwise corrections and the fixed-end action argument apply to the named lottery. Ordinary greedy rules use explicit known-stakes algebra; their cost estimates are not assumed uniformly accurate and need not improve realized loss. |
| **V04 — paid resources and usefulness** | Source, inference, acquisition, checking, storage, readout and admitted failures have explicit finite accounts and separate completion conditions. No optimal value-of-computation or physical-runtime theorem is established. |
| **M01 — scoped models and ordinary comparison** | Exact, cached, greedy, proof-only, fixed-action and identical-kernel controls are retained. The finite synthesis remains useful at its stated scope; affirmative Q3 economic advantage remains open. |
| **R01 — scope, version and withdrawal** | Hard generations prevent old-name revival; structural reads reject changed warrants before recheck/transport. Reports retain their historical scope, and changed stakes or objectives require the corresponding current warrant. |
| **C01 — distinct hypothetical changes** | Conditioning, occurrence, actor, shared code, stored-copy/predictor replacement and paired-support repair have separate executed interfaces. No general new counterfactual semantics is selected. |
| **C02 — structural identification** | Dependency and repair information are supplied. Unresolved sources remain outside minimization; neither implementation identifies an absent causal structure or an objectively preferred exception policy. |
| **C03 — feasibility, ties and decisions** | Complete tied minima and feasibility checks are charged. One implementable receiving action is distinguished from the forbidden casewise oracle; infeasibility supplies no useful-action warrant. |
| **C04 — genuine counterpossibles** | The original classical contradiction remains unsatisfiable and the exceptional paired-support rules are explicit. This finite structural test has not been joined to the selective-feedback learner. |
| **I01 — operational equivalence** | Kernel identity, complete-key routing and selected-receipt coupling identify the mathematical paths actually preserved. Invoices may change. Repricing a fixed record differs from rerunning a price-sensitive acquisition policy; matching nine outputs is not a universal representation theorem. |
| **F01 — versioned self-assessment** | Paid public reporting reconstructs the current episode without unbought labels. It provides no self-proof, endogenous-feedback reflection, future guarantee, anytime coverage or empirical proof of fair randomness. |

## 7. Reproduction, review closure and next boundary

The final source/evidence manifest, executable commands, review dispositions
and exact principal accounting will be linked here at closure. All retained
runs are DEVELOPMENT. P3-09 remains unstarted.
