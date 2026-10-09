# Selective-feedback development comparison

Contributor: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-09 UTC.
Stage: **DEVELOPMENT**. Separate same-model implementation/analysis assignment;
zero principal clock credit. The recorded batch uses controller
`r-p3-b-a-blocked-prod-v1.1`, service `r-p3ba-euler-services-v1.2`, and harness
`r-p3ba-selective-development-v1`. Their complete hashes and copies are in the
[manifest](run_001/manifest.json) and `run_001/sources`.

## Outcome

**The exact-quota implementation completed every planned arm. Bounded state
substantially reduces its representation overhead, while the ordinary exact
table remains cheaper and makes no errors on this mathematical service.**
There is no demonstrated forecast superiority or economical learning advantage
over that table.

The [prospective run plan](../run_plan_v1.json) fixed 16 main arms and four
variation arms before execution. Horizons are 992 and 3,968, block sizes are
2, 4, 8 and 16, and state is exact integer weights or 16-bit normalized state.
The tape cycles through all 248 Euler queries using the answer-free affine
index `(73*t+19) mod 248`. A main seed and two specified variation seeds provide
reproducible development traces. They are not IID replications, confidence
intervals or a selection procedure for a final policy.

All **20 learner arms and eight ordinary control runs** passed their declared
completion and protocol checks. The program recorded 26.783329927 seconds of
elapsed runtime, separate from its abstract operation tariff and from research
accounting. A separate [saved-evidence audit](saved_evidence_audit.json)
reconciles 43,648 learner rows, 9,796 bought receipts and 19,840 control rows
without executing a new scientific run. It checks resource sums, transcript
binding, private-label separation, paired selector paths and reported scores.
The full [result](run_001/result.json) and each arm/control summary remain
directly readable. Large raw records are packaged through the verified
[raw archive](raw_traces_v1.zip), [path/hash manifest](raw_archive_manifest_v1.json)
and [verification receipt](raw_archive_verification_v1.json).

After this batch, controller v1.2 added an exception annotation for a denied
initial funding charge. The [separate transfer record](current_registry_reprice_v1.json)
verifies that the only source changes are that guard and the version marker.
Successful-path operations are unchanged; fresh source procurement costs
**26 additional units**. Current v1.2 cold costs are therefore derived by adding
26 units, or 0.026 at the declared unit price, to each observed learner bill.
Controls are unchanged. Every figure below remains the actual v1.1 observation;
the transfer is not a rerun and does not relabel its hashes or physical runtime.

## Resource and decision results

The following are the main-seed results at horizon 3,968. Resource units include
the complete standalone source registry, learner initialization, randomness,
forecasting, updates, storage, output and actual purchased computations.

| Block size | Exact-state units | 16-bit-state units | Exact-state terminal errors | 16-bit-state terminal errors |
|---|---:|---:|---:|---:|
| 2 | 3,207,923 | 1,792,525 | 957 | 954 |
| 4 | 3,158,529 | 1,291,318 | 1,447 | 1,476 |
| 8 | 2,935,898 | 1,039,110 | 1,703 | 1,702 |
| 16 | 1,983,337 | 914,093 | 1,830 | 1,830 |

For block size 8, 16-bit state reduces the implemented resource bill by about
64.6%. Peak retained weight size changes from 1,342 bits to 18 bits, and peak
prediction arithmetic from 1,355 to 39 bits. The sampler has its separately
declared 95-bit working allowance; the prediction number is not a measurement
of every integer or of Python heap use.

The realized errors do not establish that normalized state predicts better.
For example, block size 4 has 29 more errors in the normalized trace. Both
states have the same selector and action-bit paths within each paired arm,
but their numerical weight trajectories differ. The theorem supplies an
expert-relative allowance for normalized state, not a promise of identical
predictions or pointwise proximity to the exact-state trajectory.

At horizon 992, exact-state resource units range from 271,265 to 466,620;
16-bit units range from 243,781 to 464,269. The two additional block-size-8
seeds also finish, with exact/normalized error pairs 442/442 and 434/435.
These are the prespecified additional traces, with no retuning or extra seed
search. Individual exact results are retained in `run_001/learner_arms`.

Every independently executed ordinary exact control makes zero errors:

| Control | Cold units, 992 queries | Cold units, 3,968 queries |
|---|---:|---:|
| Direct fast binary action | 98,261 | 355,613 |
| Checked always-BUY | 292,861 | 1,134,013 |
| Initially empty semantic cache | 66,244 | 178,636 |
| Quadratic-residue table | **53,536** | **171,880** |

The common primitive price is 1/1,000. Thus the table costs 53.536 and 171.880
loss units respectively, including construction and source procurement. These
costs are unchanged between task price 1 and task price 100 because the table
has no task errors. For comparison, the horizon-3,968, block-size-8 normalized
learner costs 2,741.110 at task price 1: 1,702 task-error units plus 1,039.110
resource-cost units. The saved summaries retain exact rational values for both
declared task prices and complete category vectors.

The table's construction uses 1,611 units, including its actual prime checks,
124 square/reduce evaluations and storage. Its recorded lookup maximum is
41 units. A complete 248-query cycle uses 9,862 lookup units. The cache uses
503 initialization units, 25,166 units for its first complete domain cycle,
and 9,366 for each warm cycle. The table and cache have therefore been compared
with their actual different cold and repeated-use costs.

## A resource obstruction that does not depend on a favorable seed

The principal independently reconstructed the following source-specific
comparison. Let A(q) denote the family-admission debit for a valid query.
The implemented four-expert evaluation costs A(q)+9, whereas exact table
lookup costs A(q)+10. Each learner close additionally pays 12 units for its
identity/state checks. All its remaining work and purchased computations have
nonnegative cost.

For the recorded source closures, learner registry costs 18,970 and table
registry costs 12,477. Table construction costs 1,611. Consequently, on any
successfully completed admitted fixed tape under this source-bound contract,

```math
R_{\mathrm{learner}}-R_{\mathrm{table}}
\ge 4{,}882+11T+R_{\mathrm{purchases}}.
```

This lower bound ignores the learner's other arithmetic, randomness, storage
and output costs. The saved-evidence audit checks the inequality against all
20 recorded arms, but the argument is the explicit tariff comparison, not a
statistical inference from their seeds. With nonnegative task prices, a common
nonnegative primitive-unit price, and zero table errors, this gives a scoped
economic obstruction for the specified learner/table implementations.

**The conclusion is robust to granting all learner setup for free.** Keeping
only the expert evaluation, 12-unit close charge and purchased service bill
still gives

```math
R_{\mathrm{learner,ongoing}}-R_{\mathrm{table,lookups}}
\ge 11T+R_{\mathrm{purchases}}.
```

The 11T term alone covers the table's 1,611 construction units by T=147;
for the equal power-of-two-block contract, every legal horizon at least 148
therefore suffices. This removes dependence on source-file-size pricing for
the planned horizons. Category-specific prices or a changed required service
need their own comparison; the result is not a lower bound on every selective
learner or an assertion about physical hardware.

The table's event counts were not recorded as an independent observed field
in these invoices. Source reconstruction gives 368 construction pay-bundle
events and at most nine per lookup, hence at most 74,096 at horizon 8,192,
within the existing 100,000-event cap. The resource envelope is at most
1,611 + 41 times 8,192 = 337,483 units, within the existing 10-million-unit
meter. These are source-derived bounds, distinguished from the observed
41-unit lookup maximum and actual bills above.

## What the scores and certificates mean

Each arm retains three different quantities: realized sampled terminal loss,
expected terminal loss conditional on its realized selector path, and the
immutable all-issued Brier score. Conditional action expectations integrate
only the action bits. Weights do not depend on sampled actions on this fixed
tape, so this calculation is exact; it is not an expectation over the
selectors that determine the learning trajectory.

For example, the horizon-3,968, block-size-8, normalized arm has realized
terminal loss 1,702, conditional expected terminal loss approximately 1,676.902,
and Brier score approximately 1,418.955. Its rigorous unconditional expected
terminal upper bound is approximately 1,924.352. The state allowance is about
0.370855 and the separate action rounding allowance is retained. All displayed
approximations refer to exact fractions saved in the result. Logarithms in the
certificate use 32 terms of the positive atanh series plus a rational upper
bound on its remaining tail.

The expectation bounds were **not** used as per-seed pass/fail tests. A finite
seeded trace is neither a proof of fair randomness nor an empirical verification
of an unconditional expectation inequality. The principal's derivation and
independent proof review establish the theorem under its stated premises.

The four fixed experts have all-issued losses 1,984, 1,984, 2,112 and 1,856 at
horizon 3,968. Purchasing a current answer itself improves a comparator's
terminal decisions. On the block-size-8 normalized selector path, replacing
unbought actions by the fixed lower-half expert gives 1,625 errors, below the
learner's 1,702, while keeping the same complete executed resource bill. This
is explicitly a counterfactual output-action-substitution diagnostic. Its
price includes every actual purchased receipt and all controller/setup costs;
it is not a separately optimized deployed policy or retrospective authorization
to choose a best expert. It helps separate paid correction from learning value.

## Information and preservation boundary

`execute()` receives only the immutable public query tape, the fixed contract,
seed and a resource-only setup invoice. Only selected checked receipts enter
its update API. The harness saves the complete learner-visible transcript and
bought invoices before invoking the independent repeated-multiplication
evaluator. Unbought labels and per-row scores appear in separate postclosed
files. Evaluator source procurement and truth computation have their own
invoices and are excluded from deployment cost.

The batch stopped only after completing the prespecified plan. No scientific
failure, hidden retry, source change or additional population occurred. The
ordinary blocked product-weights algorithm is identified as an ordinary
equivalence; it was not duplicated under another name as extra evidence.
No final freeze, P3-08 work or further recurrence is selected by these results.
