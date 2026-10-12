# Prospective heterogeneous mathematical-value service

Codex (GPT-6), October 11, 2026. DEVELOPMENT; S08/S10/S10R.
This follows remote-verified checkpoint `e2f4e8ee977aa3001cbe96c8a69ae7f523f92493`.
No confirmation claim or readiness forecast is selected.

## Fixed source and question

Generate disjoint groups of random 3-CNF instances, with a fixed extra positive
unit on variable 1. Coordinate truth means existence of a satisfying assignment.
Only a strictly checked total assignment is a positive receipt. Native False
and bounded-search None remain unresolved for the service. Group sizes,
variable/clause counts and generator seeds are visible metadata. The source
hash binds every formula and its extra unit. No full-solve history is supplied.

The requested value is the fraction of these fixed mathematical questions that
are true. Warrant that the total count is at least the fixed threshold, or
abstain. Statistical arms use alpha=1/20. An exact receipt-count controller has
a stronger zero-statistical-risk output, which must be stated when comparing
cost. None of these probabilities makes an individual mathematical truth random.

Prospective development cohorts (one generator seed per cohort, 93040+index):

| Cohort | Group sizes | Variables by group | Clause/variable ratios | Target fraction |
|---|---|---|---|---|
| A | 256,256 | 60,160 | 3.8,4.25 | .55 |
| B | 256,256 | 60,220 | 3.8,4.25 | .65 |
| C | 128,128,128,128 | 60,100,160,220 | 3.8,4.05,4.25,4.35 | .60 |

These choices precede their truth and cost outcomes. They are small generative
probes, not held-out confirmation. A cohort can fail to support the requested
action. Record that rather than redefine the threshold after seeing it.

## Controllers and fair information

- **Exact cost-directed receipts:** buy proofs, retaining only checked positives,
  until their count reaches the target or the finite source is exhausted.
- **Direct ordinary test:** uniformly sample the whole population and use the
  earlier exact one-sided finite-population mixture at the fixed target.
  Unknown proof outcomes remain in the sample prefix; their count is not deleted.
- **Ordinary stratum confidence bounds:** use alpha/G anytime count bounds,
  retaining the maximum lower endpoint obtained for each fixed group. Combine
  with hard receipt counts. Sample adaptively using paid production/cost pilot
  information and predicted lower-bound improvement per unit cost.
- **Joint count source:** use the rational positive-proof mixtures with fixed
  eta in {0,1/4,1,4}, numerical count proposals and exact rational certificates.
  A current admissible null allocation guides expected log-evidence gain per
  paid cost. A counterexample permits cheap abstention at that check.
- **Bounded joint variant:** first use a positive conflict budget on new draws,
  then, if necessary, purchase continuations of already sampled unresolved
  computations. Successful continuations refine the existing factor, never add
  another draw. Negative hints may affect scheduling but supply no truth label.

Cost-directed controllers buy an eight-draw pilot per group. Pilot receipts
are included in their statistics, and every pilot call is charged. The direct
uniform arm instead follows its own global uniform stream; its different
acquisitions are part of policy comparison, not a shared-label inference test.
Within-group indexes are drawn on demand after choosing the group. The sampler
must not expose future random identities to an adaptive selection policy.
Seeded repeatability in this local prototype does not authenticate an external
sampling authority.

All controllers may build native solvers lazily, reuse their own state and
strictly check returned positive models. They receive the same formula data,
without free native truth, unrun proof recipes or another arm's cache. Exact
receipt stopping is checked after every accepted proof. Statistical checks can
use growing sample boundaries to avoid paying the optimizer on every call;
record actual checks and all acquisition between them. Controller advice is
fallible and any negative/timing observations have only their declared role.

## Resource and outcome record

Charge lazy solver construction, actual calls including failures, sample
selection, proposal generation, exact profiling, receipt checks and cleanup.
Record formula generation/source binding separately as common input cost.
Record numerical dependency import separately, and report both reused-service
and one-shot bills. Do not amortize startup over hypothetical future work.
Native conflict budgets are not wall-time limits. Use durable per-arm boundary
records and preserve any abrupt failure as an actual incomplete exposure.

After all policies finish, a separate native reference may compute each full
truth for diagnostic action/bound comparison. This uses trusted native UNSAT
for diagnosis, not an independent proof of every negative. Its labels and
cost are not controller inputs. Preserve abstentions, false realized warrants,
proofs, sampled identities, native call counts and complete lifecycle costs.

The strongest specified comparisons include conventional sequential methods,
not just full census or uniform sampling. They may still beat the joint source.
An ordinary controller could implement the identical joint kernel; no universal
strict superiority over that class is asserted. A useful new consequence and
broader transfer remain open even if one development cohort is favorable.

## First exposure and prospective continuation

[hetero01_failure.json](hetero01_failure.json) records an access violation in
MiniSat22 during cohort B's exact controller. Cohort A completed first. Its
diagnostic count was 328 versus target 282; all five returned warrants agreed.
The reused-service lifecycle was 970.5159 ms exact, 588.7757 ms direct,
2,271.9649 ms stratum-gain heuristic, 555.7337 ms joint, and 1,740.2382 ms bounded
joint. Numerical import added 368.5495 ms to the joint service. The small
request-time advantage over direct testing did not survive one-shot startup.
The stratum-gain heuristic's poor allocation is a reason to strengthen the
ordinary comparison, not evidence against stratified inference as a class.

Continue the same fixed cohort recipes using an explicitly recorded Glucose3
engine in a separate source/run. Preserve the original native fault; its root
cause and the old s02 failure remain unexplained. Positive receipt checking
and mathematical source hashes remain the same. Runtime numbers across engines
are not paired solver repetitions or confirmation.

Add a conventional adaptive Neyman-style allocation control. After the paid
pilot, estimate positive-production p_g and mean evaluation cost c_g. Sample
groups to track allocations proportional to
N_g*sqrt(p_g*(1-p_g)/c_g), using largest target-share/current-sample ratio for
the next batch. This is ordinary variance/cost guidance, with no validity
assumption that proof-production frequency equals mathematical truth rate.
Its warrants still use alpha/G anytime lower count bounds and checked receipts.
Charge allocation calculations and retain actual sample paths. Compare it
alongside the previously specified controls on the alternate engine.
