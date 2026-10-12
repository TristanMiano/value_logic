# Saturated witnesses acquire a sharper source, but need cost-aware continuation

ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC. DEVELOPMENT.
[Separate implementation](threshold_cnf_v2.py),
[retained-cohort replay](threshold_cnf_v2_results.json),
[unchanged v1 findings](threshold_cnf_findings.md).

This is an explicitly exposed same-input replay of the original nested CNF
cohort and sixteen replacement draws. Each query rule is compared with its
own freshly executed nonsaturated service. No new sample or confirmation is
claimed, and the original implementation/results remain unchanged.

After a checked SAT result at j, the new service tests that witness against
successive added clauses. Each passed addition certifies another SAT prefix
and can raise the retained lower bound on H. The first failed clause stops
that witness's extension; **it never creates an UNSAT result**. Different
witnesses may support different prefixes. Source checks, delta preparation,
literal evaluation, new receipts, storage and later cached-frontier checks
all have explicit charges. Every compared policy receives this same service.

## Positive information gain at a measured price

For the endpoint and minimax query-count policies, saturation derives fourteen
additional SAT receipts without changing their 25 provider calls or 1,492,469
provider-unit bill. It reduces remaining uncertainty about H:

| Checkpoint | Mean H-interval width, original | Mean H-interval width, saturated |
|---|---:|---:|
| After pair `(3,4)` | 2.4375 | 1.5625 |
| After adding `(1,6)` | 0.8125 | 0.3750 |
| After adding `(0,7)` | 0.4375 | 0.3750 |

The first-stage reduction is 35.9%. This is not a new error-rate estimate: it
is a directly measured reduction in unresolved threshold positions, retaining
all draw multiplicities. For integer thresholds, summing the empirical CDF
envelope thickness over t equals this mean interval width, because a row's
upper and lower indicators differ at exactly `u-l` thresholds. Thus the same
extra certificates sharpen the reusable CDF source even when the current
requested pair answers were already exact.

The refinement is paid. The final provider-plus-adapter invoice rises from
1,715,829 to 1,761,919 units for the endpoint bank, about 2.7%. The query-count
planner has essentially the same effect. Its internal planning arithmetic
remains separately measured, as in v1. Whether the sharper source earns back
this extra work across later decisions is still a constructive question.

## More information does not repair an inappropriate cost heuristic

Complete midpoint search becomes more expensive after saturation: provider
calls rise from 31 to 33, provider units from 2,009,909 to 2,284,592, and the
provider-plus-adapter invoice from 2,248,805 to 2,581,795, up 14.8%.

The cause is reconstructable. On row 41 the original method buys SAT at 3,
then UNSAT at 5; checking the existing witness settles 4. Saturation certifies
SAT at 4 immediately, so the midpoint heuristic re-centers its next query at
6. It then buys both UNSAT at 6 and UNSAT at 5. The extra query costs 246,608
provider units. A second row has the same pattern at a smaller cost.

The interval becomes more informative, but the heuristic optimizes positions
as though complete query prices were equal and ignored retained proof state.
The observation is not a counterexample to the value of information under an
optimal controller. It identifies a concrete gap between a threshold-count
planner and a planner for actual mathematical proof expenditure.

## Verification and next constructive options

All requested features match each method's original-service answers. A small
semantic fixture first obtains a SAT witness that fails the next added clause,
then buys a different witness proving that next formula SAT. The failed
extension leaves the UNSAT upper bound unchanged. Later checked UNSAT closes
the true threshold; no timeout or failed witness has been relabeled as false.

Two targeted developments follow. First, retain a useful existing query tree
and prune tests already entailed by new receipts, instead of automatically
re-centering an equal-cost midpoint heuristic. Second, compile clause deltas
during the existing chain-verification pass, removing the prototype's second
syntax pass. Either route can be compared with the current measured service
before investing in a larger source experiment. The promising result here is
a paid method for acquiring more reusable probability information from an
already purchased proof, with its continuation-cost problem made explicit.
