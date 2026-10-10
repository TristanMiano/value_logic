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
work while preserving every candidate trace and invoice. On the four-key
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

The prior negative result is unchanged: in option A's `T=3968, B=8`
development comparison, historical uniform v1.1 used **1,039,110 units with
1,702 errors**, adaptive fixed state **1,382,703 with 1,754**, and the cold
ordinary exact table **171,880 with zero errors**. Current uniform v1.2 adds
26 registry units by source transfer, not by a rerun. That source-specific
obstruction remains in its original archives and
[recurrence checkpoint](../checkpoints/B_1_R_P3_B_A.md).

## 5. Structural, counterpossible and transport integration

This section is being finalized against the source-preserving structural
resource-boundary amendment. The retained v3 comparisons already match all
nine independent ordinary outputs, preserve tied minima and unresolved
sources, and reject stale transported warrants. The amended source and exact
current invoices will be identified here before task closure.

## 6. Five-question and 21-duty disposition

The current integration assessment is being reconciled against the original
desiderata and the additive option A overlay. No unrestricted logical
induction, calibration, coherent truth law, counterpossible-policy
identification or ordinary-combination superiority is inferred from these
development records.

## 7. Reproduction, review closure and next boundary

The final source/evidence manifest, executable commands, review dispositions
and exact principal accounting will be linked here at closure. All retained
runs are DEVELOPMENT. P3-09 remains unstarted.
