# Joint acquisition of cost observations and checked repair evidence

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC.
DEVELOPMENT; extension of S27/S28. Readiness remains **unassessed**,
P3-POS01 **OUTSTANDING**, and P3-11 deferred. This entry synthesizes the recorded
work; its preparation makes no new acquisition or diagnostic run.

## What became usable

There is now a callable service that buys observations of uncertain penalty
costs and purchases logical repair evidence, retaining both across requests.
It can return a checked feasible repair or replacement with a regret bound
valid for every cost vector still allowed by the paid observations. Full cost
identification is not required for every output.

The clearest scoped example is the v2 `logic_first` arm: its first request
closes after **six cost observations and two logical purchases**, while four of
the eight cost rows remain completely unobserved. Requests 0–12 close before
the common cost set becomes a singleton. The final output gates are reconstructed
from actual raw evidence in [the focused check](joint_check_results.json).
This demonstrates an executable joined evidence path on the admitted source.
It does not establish that its acquisition rule is economically preferable.

The current shared-deficit acquisition proposal is expensive. It buys more
observations and logical purchases than the audit-first control and performs
many more paid support queries. It has **no demonstrated total-cost advantage**.
That outcome motivates smaller priced purchase bundles and the
[complete fallback](complete_findings.md), rather than promotion of this
particular priority rule.

## 1. The observation contract is a fixed finite cohort

[`joint_source.json`](joint_source.json) commits one fixed cohort of eight
cost rows, each belonging to the same public set of six possible eight-feature
cost vectors. A controller receives those possible vectors and paid coordinate
observations. The realized mode indices are held by the declared synthetic
observation interface. No mode probabilities or population sampling law are
supplied to the controller.

An audit buys one exact `(row, coordinate, value)` observation. Its receipt
binds the cost-source identity, row/feature meanings, call number, observed
value and invoice. Each current row set `Q_i` is the subset of public vectors
consistent with that row's receipts. All untouched possibilities remain.
The target cost vector in the implementation is the **cohort sum**:

```text
W = Q_1 + ... + Q_8,
h_W(c) = sum_i max_(z in Q_i) c dot z.
```

This exact support identity uses the declared Cartesian product of allowed row
states. It does not assume that the physical rows were generated independently
or that observed cells are iid samples. Adaptively selected audits simply
filter the warranted set. A conflicting observation produces an empty-set
error, not a vacuous action certificate. The warrant remains relative to the
committed source and its truthful observation interface; a checksum alone does
not validate an external sensor or an unseen proof.
The six-mode catalog is a supplied source contract, not a population model
learned or validated by these audits. A deployment needs its own warrant for
the stated support set and measurement meanings.

Dividing the internal objective by eight reports cohort means. The sixteen
requests use replacement price **48** and tolerance **4** internally, or
mean price **6** and tolerance **0.5**. These differ from the separate
[native eighty-request stream](native_findings.md), which supplies objective
weights and uses price 6 and tolerance 1 directly. The native stream is not an
uncertain-cost acquisition comparison for this sixteen-request duty.

The population-confidence extension in [the theory note](acq_theory.md) needs
its own iid/bounded-source assumptions and time-uniform coverage allowance.
Those assumptions are not needed or claimed for this finite cohort, and this
run provides no population generalization.

## 2. The output certificate joins costs with checked logical work

The hard and soft clause meanings remain fixed for each logical source. An
admitted feasible repair has Boolean violation vector u. A checked branching
proof P retains support vectors v with
`L_P(w)=min_v v dot w <= C*(w)` for every admitted nonnegative objective w.
The fixed repair's uniform regret certificate against the best repair or
replacement is

```text
G(u,P,W) = max(0, h_W(u)-p, max_v h_W(u-v)).
G(replace,P,W) = max(0, max_v [p+h_W(-v)]).
```

The service chooses the smallest complete certificate across retained actions
and individual proofs. That is safe; it can be looser than optimizing with the
pointwise envelope of several proofs. A stronger envelope calculation would
have to be constructed, checked and charged separately.

Cost observations can shrink W. Logical purchases can add a feasible action
or a reusable lower proof. The service checks the gate after each purchase,
retains earlier evidence and returns the actual action with its evidence.
An unresolved region or native attempt is preserved as unresolved, not
interpreted as proof that the current action is poor.

Each arm maintains its own actual `PersistentIHS` objects for the logical
sources it uses. The adapter retains a MiniSat object, learned clauses, the
native HiGHS hitting-set model, objective-independent core rows and explicit
previous hitting-set starts. Objective updates and native searches are actual
paid calls. This does not establish reuse of a HiGHS branch-and-bound tree.

Native optimum/lower statuses and raw cores are advisory for the independent
lower-proof bank. When negative evidence is needed, the adapter separately
pays the finite branching provider and checks its raw proof before retaining
its supports. A checked feasible witness can be retained independently of
whether the rest of an attempted purchase completed. The finite proof bridge
has no demonstrated scalable advantage over supported native proof export.

## 3. Why v1 led to v2

The first executed [`joint_repair.py`](joint_repair.py) and
[`joint_results.json`](joint_results.json) joined the observation interface,
uniform certificates and persistent native purchases. Its current-action rule
used an admitted feasible competitor to detect cost ambiguity, then targeted
a coordinate audit at the relevant contrast. This was a useful first callable
construction, but it did not price an observation's effect on many later
requests sharing the same cost cohort.

| v1 policy | Checked | Audits | Logical purchases | Cache closures | Named arm-operation subtotal |
|---|---:|---:|---:|---:|---:|
| Certificate-directed | 16 | 16 | 23 | 1 | 1,236,694 |
| Audit-first | 16 | 14 | 13 | 5 | 641,712 |
| Logic-first | 16 | 14 | 18 | 5 | 1,304,454 |

Those subtotals include modeled service operations, native adapter/setup,
separate proof-provider work and audit software. They exclude shared current
admission, native-search prices and external observation prices. The initial
current admission record separately contains 4,374 source/witness units,
3,601 proof/compilation units and 76,521 raw read/hash units. Historical
acquisition of 77,646 units remains separate.

[`joint_repair_v2.py`](joint_repair_v2.py) preserves that executed version and
makes two constructive changes. First, it compiles action/proof contrast
templates, each contrast's dot products with the public cost modes, and
row-subset extrema. All four policies use this same implementation and the
same raw-checked compact initial bank. Second, it adds a shared-audit priority
over the current and known future request suffix:

```text
Phi(D) = sum_remaining_requests max(0, current_certificate_bound - tolerance).
```

For each supported coordinate audit, the implementation conditions the common
row state on every possible observation, recomputes all suffix deficits, and
scores the worst-outcome reduction. The same possible outcome is applied to
all requests before summing. Rows with identical current mode sets share a
quote when the source contract and audit price make them exchangeable.

This is a precisely defined information priority. It is not an expected value,
a forecast of future proof-production cost or a theorem about total spending.
When the guaranteed deficit reduction is zero, the rule sometimes uses known
feasible-action ambiguity and a possible-gain tie-break, explicitly marked as
exploratory. It does not assign probabilities to the audit outcomes.

The simpler v2 controls retain the same representations and supported native
reuse. Audit-first requests the first informative coordinate while its gate
remains open; logic-first buys an available unresolved point query first;
certificate-directed uses the current feasible-action ambiguity rule. The v2
fixed-order fallback also avoids calculating a full audit menu when only the
first informative coordinate is requested. Consequently, this is a development
amendment with policy and accounting changes, not a pure cache ablation. The
certificate-directed audit count changes from sixteen to fifteen. The source
is already exposed, and v2 executes **new actual acquisitions** against it;
it is not a zero-search replay or independent validation population.

## 4. All four v2 arms: outputs and paid resources

The following results come from
[`joint_v2_results.json`](joint_v2_results.json). Every arm closes all sixteen
requested gates, with zero unresolved final requests and maximum certified
regret 4 in cohort-sum units.

| v2 policy | Audits | Logical purchases | Cache closures | Outputs before full cost identification | Post-run summed action cost | Post-run summed realized regret |
|---|---:|---:|---:|---:|---:|---:|
| Shared deficit | 16 | 14 | 5 | 2 | 328 | 2 |
| Audit-first | 14 | 13 | 5 | 0 | 330 | 4 |
| Logic-first | 14 | 18 | 5 | 13 | 328 | 2 |
| Certificate-directed | 15 | 23 | 1 | 13 | 328 | 2 |

The last two columns are explicitly **post-controller diagnostics**, in
cohort-sum units. All methods deliver the requested tolerance; their returned
actions need not have identical realized cost. Divide these quantities by
eight for cohort-mean units. The small action-cost difference does not settle
the full acquisition-cost comparison.

| Executed named operation component | Shared deficit | Audit-first | Logic-first | Certificate-directed |
|---|---:|---:|---:|---:|
| Service/source/compiled-certificate operations | 43,325,591 | 338,365 | 426,643 | 502,366 |
| Native adapter operations | 6,770 | 6,766 | 8,456 | 10,085 |
| Native setup operations | 3,104 | 3,104 | 3,104 | 4,176 |
| Separately paid proof-provider operations | 30,691 | 31,916 | 43,276 | 49,743 |
| Audit provider software | 64 | 56 | 56 | 60 |
| **Named arm-operation subtotal** | **43,366,220** | **380,207** | **481,535** | **566,430** |

The v2 initial raw/cache admission costs **92,969 units**, actually paid once
before the four arms receive the same admitted bank. A new standalone consumer
must establish its admission chain; this fee is common only under an actual
shared-admission comparison. Historical acquisition of **77,646** is not added
again as new work. External audit prices and native-search prices remain
unassigned. The source-manifest read/hash is outside the arm operation counters
and has no separately itemized price or timing component. JSON serialization
and allocation are timed but have no
additional operation tariff, and native working memory is not separately
measured. These subtotals are therefore not total monetary costs.

The native calls are real and preserve each arm's own paid state:

| Native resource count | Shared deficit | Audit-first | Logic-first | Certificate-directed |
|---|---:|---:|---:|---:|
| Resident logical-source engines initialized | 11 | 11 | 11 | 15 |
| Hitting-set calls | 59 | 57 | 63 | 74 |
| SAT calls | 50 | 48 | 50 | 58 |
| Core rows added | 45 | 44 | 45 | 51 |
| Objective updates | 12 | 11 | 16 | 22 |
| Explicit previous-MIP starts | 3 | 2 | 7 | 8 |
| Independently checked negative-proof purchases | 9 | 9 | 13 | 16 |

All arms use the same source and spending limits: at most 64 observations,
128 logical purchases and 80 purchase steps per request; each native purchase
has the declared round, SAT-conflict, MIP-node/time, proof-unit and adapter-unit
caps in the source manifest. These are a resource vector, not interchangeable
currencies. A future capped failure must retain partial checked work and its
unresolved invoice even though no such final failure occurred here.

Recorded whole-arm wall times were **2,797.860 / 250.511 / 303.522 / 366.319 ms**
in the table's policy order. The corresponding recorded native-search wall
times were **210.479 / 195.909 / 235.462 / 275.991 ms**. Process CPU and per-call
timings are retained in the result. This was one ordered development execution,
not a calibrated runtime benchmark.

### Why the shared priority has not earned an efficiency claim

The shared rule bought sixteen audits and fourteen logical purchases, compared
with audit-first's fourteen and thirteen. It saved 1,225 proof-provider units,
but that local difference is overwhelmed in its declared operation subtotal
by the cost of evaluating many hypothetical suffix states.

Its compiled row-extrema cache recorded **1,825,170 hits** and **4,102 misses**.
Those hits did not make its computation free: repeated coefficient/row key
lookups cost **23,850,355 units**, and support/argmax summation cost
**16,463,448 units**. The shared score retained 150,806 serialized support-cache
bytes, 11,213 profile bytes and 56,929 template bytes. The corresponding three
component sums for shared deficit, audit-first, logic-first and
certificate-directed are **218,948 / 125,674 / 155,940 / 188,925 bytes**, excluding
native working memory and Python object overhead.

This supports a specific development conclusion: pricing the common effect
of observations is meaningful, but this broad repeated-evaluation rule is too
expensive on the recorded small source to support an acquisition-efficiency
claim. Cache-hit counts and positive deficit scores are insufficient cost
evidence. It remains possible to develop cheaper shared updates or a small
complete audit/proof bundle; the present result does not establish their value.

## 5. Evidence, diagnostics and comparison scope

Both execute functions place the exhaustive diagnostic **after every paid arm
has finished**. The diagnostic computes realized-cost optima only then; none
feeds a gate, native query budget or within-run purchase decision. Its own
recorded tariff is **310,930 units for v1** and **414,577 for v2**, separate from
the service invoices. Later development can be informed by this exposure,
which is why v2 remains DEVELOPMENT rather than fresh confirmation.

[`joint_check.py`](joint_check.py) and
[`joint_check_results.json`](joint_check_results.json) provide a focused
same-model reconstruction of v2. They re-admit the 29 historical witnesses
and 18 raw proof trees, verify all 59 recorded audit observations across arms,
check 21 new witness receipts and 47 new branching proof receipts, and rebuild
all event/request certificates and **64 final gates** using direct common-source
support calculations. The replay makes **zero new native calls, zero provider
calls, zero cost observations and no new diagnostic-optimum calls**. Its
**3,827,979-unit** replay invoice is separate from the acquisition runs.

That check does not independently audit every prospective portfolio quote,
prove policy optimality or calibrate runtime prices. It confirms the narrower,
load-bearing result: the recorded paid evidence supports the returned output
certificates. Source and implementation hashes are recorded for both versions
and the replay; original files and receipts remain preserved.

The [primary-source bridge](acquisition_sources.md) identifies minimax-regret
elicitation, constrained configuration optimization, anytime constraint
generation and retained constraints as close conventional capabilities. The
uncertain-cost formulation, query selection and reuse should not be claimed
as novel merely because they are expressed through this service. Likewise,
adaptive-submodular greedy guarantees need their outcome-prior and diminishing-
return hypotheses; monotone shrinking of W does not provide them. The current
controls share compiled representations, raw admission, supported native state,
proof bridge and tolerance. They are useful conventional comparisons, not an
exhaustive implementation of every strong regret-elicitation planner.

## 6. What to buy next: the constructive lesson

The action-specific obstruction is useful: if an admitted competitor v has
`h_W(u-v)>tau`, no stronger lower proof can certify that same repair u over
unchanged W. The relevant next move is a cost observation or a different
action. Conversely, a contrast that fails everywhere in W for a fixed
action/proof pair cannot be repaired by cost refinement alone. These are
directional tests for fixed evidence choices, not universal prescriptions to
alternate audits and search.

A purchase's guaranteed certificate gain requires every admissible outcome
and its complete bill. If a capped logical call can return no progress, its
one-step worst-outcome gain can be zero. W supplies plausible costs, not an
outcome distribution or a solver-runtime law. Audit and proof purchases can
also be complementary: both singleton guaranteed gains may vanish while a
small combined purchase closes the desired output. The derivation and worked
case are retained in [acq_theory.md](acq_theory.md).

The [complete-call contract](contract_findings.md) and
[executed complete fallback](complete_findings.md) turn that issue into a usable
alternative on this small finite source. The public full-calibration tree
requires at most sixteen observations; balanced independently checked bounded
calls then require at most four per request for this price/tolerance. The
executed fallback used fourteen observations and fourteen direct branching
calls to close all sixteen requests. It is a complete finite purchase option
under its stated cap/execution contract, with costs still separated from CPU
and external prices. It makes no native-IHS or economic-superiority claim.

The best next constructive move is a **small priced audit/proof bundle** using
this complete option, the admitted compiled supports and each controller's
actual warm state. Price prospective planning work and express unknown audit
and CPU prices as regions. Keep the broader generative question open: when
does learning exactly the costs relevant to a certifiable action beat simply
calibrating the whole small source or using a strong conventional controller?
