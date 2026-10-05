# F15 neural results-report review

Reviewer: **delegated ChatGPT (GPT-6 Astra Pro), F15 analysis audit**.
Scope: collaborating F15 report verification, not F16 or independent peer review.
Reviewed `v2/experiments/results.md` snapshot SHA256
`ef97ee03d02d946896f9fa46f7373cf46bba0b5a57693ce3685f8b826a752ada`.
Compared its neural claims with the original five saved evaluations,
`neural_assessment.json`, frozen code/design, and this session's saved-statistic
and parameter audits. No primary output was changed; no samples, fits,
interventions or confidence intervals were generated.

## Overall finding

The neural result tables, support/violation counts, work denominators and
confidence interpretations agree with the original records. The report correctly
distinguishes unsupported identity MAE from the actual near-decision violation,
and a rejected **.01 material advantage** from evidence of a negative advantage.
No numerical discrepancy or result-changing analysis error was found.

Two wording corrections and one diagnostic addition are recommended before close.

## 1. Add the optimal-base qualification to the log-contribution statement

In §5.1, the statement that exact interchange requires corresponding log-cost
contribution differences omits the frozen derivation's **exact optimal base
network** assumption. For an arbitrary base logit `z(b)`, exact intervention
requires `phi(d)-phi(b)=logit(pH)-z(b)`; it becomes the log-cost difference when
`z(b)=logit(p*(b))`. This matters because the actual ordinary networks only
approximate the optimum.

Suggested narrow correction:

> With an exact optimal base network, exact interchange in this affine-output
> architecture would require the corresponding log-cost differences in the
> selected logit contribution. The tested claim is approximate on the specified
> pair populations.

This preserves the frozen design and avoids upgrading its conditional argument.

## 2. Narrow “diagnostic forward work is separately accounted”

In §5.1, the count **8,192,000 alignment/role/pair evaluations** is correct and
excludes additional gauge/diagnostic work. However, the saved final neural
resource object has pair count, alignment-role-pair count, total wall/CPU time
and refit count; it does not provide an exhaustive separate count/timer for all
gauge and diagnostic forward calls. Discovery has additional specific forward
counts, and the original files retain gauge/diagnostic results, but that is a
narrower statement than fully separate final-forward accounting.

Suggested replacement:

> This pair-evaluation count excludes additional gauge and diagnostic forwards.
> Their results are retained, and their compute is included in the measured
> evaluation wall/CPU totals; the frozen output does not isolate every such
> forward call as a separate resource count.

No population regeneration or frozen amendment is needed for this reporting
precision. Do not present the main alignment count as the complete compute cost.

## 3. Give the existing decoder/ordinary diagnostic outputs a clear disposition

The required diagnostics are present in the original evaluations and the derived
`neural_interventions.json`, but the main report barely interprets them. A short
descriptive paragraph/table would make the ordinary baselines and null behavior
visible without asking the reader to inspect 1,000 cells.

The following numbers are equal-weight descriptive averages of the ten fixed
identity model/role cells per stratum, copied/calculated from saved statistics.
They introduce no new inferential claim or interval.

| Identity stratum | Selected interchange MAE | No-swap MAE | Whole-layer-swap MAE |
|---|---:|---:|---:|
| mixed_near | .037669 | .148122 | .147509 |
| mixed_far | .043149 | .149848 | .149415 |
| preserve_other | .040218 | .147439 | .015418 |
| equal_target | .032265 | .015196 | .147880 |
| scale_separating | .045251 | .164234 | .141749 |

The selected interventions fit better descriptively than simple output copying
on mixed/separating strata. Whole-layer copying fits the preserve-other condition
well because the high-level target equals the donor optimum there. No-swap fits
equal-target well because the target equals the base optimum. These designed
degeneracies explain why neither stratum alone establishes the proposed partial
relation. They do not substitute for the frozen per-cell thresholds or matched
search controls.

Other concise retained diagnostics worth naming:

- Identity observational decoder NRMSE ranges `.134963–.284814`; its weighted
  log-contribution RMSE ranges `.106159–.183766`. These have no registered
  acceptance thresholds and supply no causal-use conclusion.
- In equal-target cells, the expected high-level intervention is null, but
  recorded output-effect RMS ranges `.029847–.052271`. This is a descriptive
  lack of exact invariance, not a new falsification of the .05 MAE hypothesis.
- All five saved records pass the **same constructed unused-duplicate witness**:
  decoder error zero and unused-unit logit effect zero, while the used-unit
  effect is 1.9. Label it method calibration; it is not five independently
  learned demonstrations and receives no ordinary-training success credit.
- Adjusted-effect errors and decoder drift remain secondary diagnostics.
  The derived mean-absolute adjusted-effect bound must not be labeled an RMSE
  or a per-example guarantee. The current report does not make that mistake.

## Confirmed substantive claims

- Denominators agree: five trained models, 3,840,000 binary labels, zero cost
  labels, 25,600 candidate evaluations/decoder fits, 409,600 intended pairs,
  409,600 independent incorrect-donor pair records, 40,960 ordinary task inputs,
  1,000 intervention cells and 8,192,000 arm/role/pair evaluations.
- All 560 original confidence rows remain within the one frozen family. Each
  hypothesis table correctly has 50 MAE, 20 decision and 40 matched-control
  cells; these are correlated claims, not independent replications.
- Ordinary readiness is 5/5 and conditional-base support 50/50. Identity MAE
  support/inconclusive/violation is 2/48/0; full pilot support is 0/5.
- Seed `1500494`, role 0, near disagreement interval exceeds `.35` throughout.
  Seed `1500493`, role 1, random-control advantage interval is
  `[-.036990,.007241]`: its upper end is below `.01` but above zero. The report
  correctly rejects the material-advantage requirement without claiming random
  is strictly superior at that confidence level.
- All four hypothesis tables' MAE, decision and control counts match the saved
  intervals. No rival passes its full adequacy/specificity conjunction; “0/5”
  is correct. For clarity, full rival conjunctions do not include identity's
  same-subset scale criterion, but their adequacy failures make the distinction
  immaterial to these zero counts.
- Scale-specificity counts `4/10`, `5/10`, `1/10`, gauge maximum
  `2.6645352591003757e-15`, overlap counts and composition maxima agree. Their
  stated conditional/per-role scope is appropriate.
- Saved-model diagnostics are presented descriptively, with no demonstrated
  cause attributed to inactive neurons, small search coverage or selection
  effects. The neural null is not relabeled a novelty or gate pass.

The recommendations change explanation and accounting precision, not any frozen
criterion or scientific disposition. Parallel delegate time is non-additive.
