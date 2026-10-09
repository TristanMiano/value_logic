# Acquisition planning v1: independent mathematical subreview

## Verdict and frozen scope

**PASS within the stipulated finite model.** The independent calculation agrees with every saved numerical field in scope: 24 parameter cases, 1,128 Bellman-table states, and 10,608 exact comparisons, with zero mismatches.

The reviewed source is `v3/checks/07_acquisition_planning.py`, SHA-256 `94fb8efcbb924470d883733f3c317fc0a79c4047089104ee4ee1c03ca5141f37`. Its saved copy in `development/acquisition_planning_run_v1/sources` has the same hash. The evidence is the frozen `development/acquisition_planning_run_v1/result.json` plus its 24 plan JSON files. No candidate code was imported or executed. No broad tests or earlier root checks were rerun.

This is **same-model, nonblind review**. The assignment disclosed the hypotheses, equal prior, fixed horizon, terminal actions, cap-N planning form, expected grid size, and source hash. The generic posterior and Bellman recurrence were written in `independent_derivation.md` before inspecting the candidate source or saved result. The independent program was authored after inspection, using a different value representation and a different forward enumeration. Independence is therefore implementation and reconstruction independence, not a blind external replication.

All work is unmeasured auxiliary work and earns **zero principal credit**. All files written by this subreview are confined to this `auxiliary` directory. Earlier boundary-review artifacts were found under `reviews/proof_agent/acquisition_subreview` and preserved without edits or further version review; this task concerns the separate frozen acquisition-planning v1 source and run.

## Mathematical checks

For t observations and k successes, the high-law and low-law likelihood weights are A = 11^k 9^(t-k) and B = 9^k 11^(t-k). The high-law posterior is q=A/(A+B); the predictive success probability is (11A+9B)/(20(A+B)). Relative to fallback on a fixed future horizon H, deployment has expected advantage H*(2q-1)/20. Terminal stopping value is the maximum of this and zero.

With resource-unit price lambda, acquiring one more observation costs c=1/2+16*lambda. The correct recursion takes the maximum of stopping and the predictive expected child value minus c, with terminal stopping forced at cap N. Candidate tie behavior is optimal: stop on an acquisition tie, and fallback on a deployment tie. The candidate formula and every saved state match this reconstruction.

The independent backward program instead propagates unnormalized likelihood-weighted values U=(A+B)*V. It computes the continuation as the sum of two weighted child values divided by 20, minus c*(A+B). The forward program separately traverses every reached ordered history under theta=9/20 and theta=11/20. It does not aggregate path probabilities by sufficient-statistic state. It verifies terminal probability one, derives the stopping-time distribution, and checks that its implied expected number of observations equals the acquired-prefix sum.

The exact forward conditional-law deployment probabilities, attempt counts, online-control units, gains, and distinct reachable-state counts match the saved results. Their prior average equals the root Bellman value minus the initial lookup cost 8*lambda. The saved all-in values also match after subtracting lambda times the recorded construction units.

## Results across the full grid

Decimals here are rounded for inspection; `independent_results.json` retains exact fractions. The gain column includes the initial lookup and online-control charges, and excludes table construction. The all-in column also subtracts the recorded construction bill.

| Cap N | H | lambda | Root action | E[observations] | Prior gain | All-in prior gain |
|---:|---:|---:|---|---:|---:|---:|
| 1 | 128 | 0 | fallback | 0 | 0 | 0 |
| 1 | 128 | 0.0001 | fallback | 0 | -0.000800 | -1.229000 |
| 1 | 128 | 0.001 | fallback | 0 | -0.008000 | -12.290000 |
| 1 | 512 | 0 | acquire | 1 | 0.780000 | 0.780000 |
| 1 | 512 | 0.0001 | acquire | 1 | 0.777600 | -0.450600 |
| 1 | 512 | 0.001 | acquire | 1 | 0.756000 | -11.526000 |
| 1 | 4096 | 0 | acquire | 1 | 9.740000 | 9.740000 |
| 1 | 4096 | 0.0001 | acquire | 1 | 9.737600 | 8.509400 |
| 1 | 4096 | 0.001 | acquire | 1 | 9.716000 | -2.566000 |
| 1 | 16384 | 0 | acquire | 1 | 40.460000 | 40.460000 |
| 1 | 16384 | 0.0001 | acquire | 1 | 40.457600 | 39.229400 |
| 1 | 16384 | 0.001 | acquire | 1 | 40.436000 | 28.154000 |
| 12 | 128 | 0 | fallback | 0 | 0 | 0 |
| 12 | 128 | 0.0001 | fallback | 0 | -0.000800 | -4.608200 |
| 12 | 128 | 0.001 | fallback | 0 | -0.008000 | -46.082000 |
| 12 | 512 | 0 | acquire | 1 | 0.780000 | 0.780000 |
| 12 | 512 | 0.0001 | acquire | 1 | 0.777600 | -3.829800 |
| 12 | 512 | 0.001 | acquire | 1 | 0.756000 | -45.318000 |
| 12 | 4096 | 0 | acquire | 8.784332 | 22.757220 | 22.757220 |
| 12 | 4096 | 0.0001 | acquire | 8.784332 | 22.742365 | 18.134965 |
| 12 | 4096 | 0.001 | acquire | 8.480963 | 22.612282 | -23.461718 |
| 12 | 16384 | 0 | acquire | 9.224131 | 104.441953 | 104.441953 |
| 12 | 16384 | 0.0001 | acquire | 9.224131 | 104.426394 | 99.818994 |
| 12 | 16384 | 0.001 | acquire | 9.224131 | 104.286367 | 58.212367 |

## Interpretation and limits

1. The Bellman policy is optimal after the fixed table/model acquisition expenditure and initial lookup are sunk. A negative all-in value alongside an `acquire` root action is consistent with that decision stage. These rows do not claim an optimal ex-ante decision to buy the model, build this table, or select between caps.
2. Optimality is Bayesian under the specified two-point prior, conditionally IID observations, cap, fixed future horizon, two terminal actions, and declared per-observation costs. Positive prior value does not guarantee nonnegative conditional value under each law.
3. No conclusion here is a universal sequential identification lower bound, an unknown-law guarantee, or optimality over a larger class with interleaved deployment, horizon consumption, different diagnostics, or alternative control actions.
4. Construction-cost multiplication and subtraction were verified using saved construction-unit counts. The adequacy of the arithmetic tariff, source/core identity bookkeeping beyond the assigned source hash, and any optional-stopping proof or adapter audit remain the parent review's scope. No CPU-cost or human-development-cost claim follows from these checks.

## Reproduction and evidence

- `independent_derivation.md`: preinspection mathematical reconstruction and candidate-specific reconciliation.
- `independent_planning_check.py`: independent exact rational checker; writes only adjacent outputs.
- `independent_results.json`: exact 24-row results, zero-mismatch count, scope statements, and evidence hashes.
- `independent_tables.json`: all 1,128 independently reconstructed state rows.

The bounded command used was `python v3/work_logs/P3_07_2026-10-09_S1/reviews/acquisition_planning_agent/auxiliary/independent_planning_check.py`, run from the repository root. It exited successfully.
