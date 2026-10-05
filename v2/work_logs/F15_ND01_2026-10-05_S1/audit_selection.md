# F15-ND01 independent saved-selection audit

**PASS**: 18965 checks, 0 defects. Read-only inspection and independent scalar arithmetic from saved statistics; no experiment, model function, population, fit, selection or evaluation was run.

All 100 robust-vs-MSE comparisons bind their prepared subsets and saved per-stratum moments. 41 subsets changed; discovery's maximum normalized objective improved in 41 and tied in 59. Validation improved in 10, worsened in 31 and tied in 59. All 31 losses followed strict discovery gains. Group and overall summaries also match.

All 160 calibration-control ceilings independently reconstruct. The registered union-bound radius computes as 0.022115658601168407 from range width 2, n=40960, m=560 and alpha=.05. Identity has seven permuted-concept and one random-control ceiling blockers, spanning all five layouts; there are zero wrong-donor or untrained-control blockers.

With the observed control errors, original pooled n and fixed Hoeffding radius held constant, an aligned intervention with zero MAE would still fail at least one required control lower-bound margin in every constructed layout. This is conditional endpoint sensitivity evidence; it does not prove an obstacle for different controls, sample sizes or intervals.

The original analysis explicitly preserves dependence and the conditional nature of this calculation. No concrete defect found. The Markdown's 0.03211565860116841 threshold is a harmless display rounding of radius+.01; the calculations retain full floating-point precision.

Evidence: [audit_selection.json](audit_selection.json). Contributor: delegated ChatGPT (GPT-6 Astra Pro), protocol/accounting audit. Parallel-agent minutes added: zero.
