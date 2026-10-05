# Independent F15-ND01 saved-result assessment

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, independent protocol/statistics audit.
This report reads completed development data. It changes no model, selected
alignment, input population, threshold or original F15 disposition.

## Integrity and chronology

The [saved-output audit](audit_saved_outputs.json) passed **46,840 checks**.
All **103** run JSON files have valid SHA256 sidecars, and every actual
prepared/evaluation self-hash matches. All **47** registered ND01 execution,
protocol and dependency files, the five original source preparations, and
all **34** original F14 frozen files still match their registrations.

| Event | UTC |
|---|---|
| Last prepared unit durable | 2026-10-05 17:02:08.307771 |
| Preparation complete | 2026-10-05 17:02:14.636223 |
| Global 15-unit validation gate | 2026-10-05 17:04:36.565220 |
| Exclusive exposure marker | 2026-10-05 17:04:36.568886 |
| First evaluation unit started | 2026-10-05 17:04:36.570270 |
| Evaluation complete | 2026-10-05 17:04:57.737900 |

Both stages completed on **attempt 1**, with no scientific retry. The internal
preparation wall cost was 82.338060 seconds; parent CPU 81.346706 and native
child CPU 0.938807 seconds, totaling 82.285513 CPU seconds. Evaluation cost
21.172718 wall and 21.148612 CPU seconds, with no native child CPU. These are
process costs, not independently added research minutes.

All 15 durable artifacts and their source identities bind the exposure marker.
Search and mask discovery/validation array hashes match. Every one of the
20 search variants, four mask methods, strata, paired moments and recorded
logical/actual work counts is consistent. A non-mutating `--check` invocation
reproduced the saved audit bytes.

The independent [core-summary audit](audit_core_summary.json) passed another
**5,359 checks** against the saved source artifacts. It verifies the complete
CSV row counts (1,000 search, 200 mask, and 1,050 calibration, including 50
separately labelled oracle rows), all 20 search aggregates, all four mask
aggregates, distinct role and both-role model point counts, and the 560
calibration interval values and statuses. The checked summary SHA256 is
`5f51177477784de4af33796cf519108f044412c11da1ab787c8601ab0fbb9043`.

The first audit invocation encountered a **reporting-code defect**: it treated
an event's reference `artifact_hash` as a self-hash. The event's outer SHA was
valid. The corrected auditor distinguishes self-hashing artifact schemas from
event references and checks both appropriately. Its prior source and the
failure are preserved; no scientific artifact or experiment was rerun. See
[audit_failures.jsonl](audit_failures.jsonl), record ND01-AUDIT-REPORT-04.
An exploratory summary read also used a table basename relative to the
repository instead of the analysis directory and failed with
`FileNotFoundError`; the subsequent auditor resolved the actual CSV location
and passed. That read changed no files or scientific outputs.

## Literal complete-endpoint calibration

[Independent interval reconstruction](audit_calibration_saved.json) passed
**9,214 checks** and reproduced all **560** frozen interval rows and their
statistical labels, without importing the experiment's assessment function.

- All five constructed layouts satisfy searched identity **absolute and
  decision adequacy**.
- All **30** same-subset scale comparisons are distinguished.
- All five fail complete identity support because they do not establish
  every required matched-control advantage.
- The identity guided-search mean MAEs by layout are approximately
  .005885, .005867, .008886, .010589 and .004991. Known-subset oracle means
  are about .00135, and every construction-known uniform bound holds.

Thus the literal complete endpoint can be **0/5 despite successful searched
cost-intervention correspondence on a deliberately structured network**.
This is stronger than merely showing that an oracle knows an inaccessible
subset. These are five coordinate layouts of one compiled function, not five
independent ordinary-training solutions.

| Identity matched control | Confidence-qualified .01 advantages | Observed means at least .01 |
|---|---:|---:|
| Optimized random search | 9/10 | 10/10 |
| Optimized permuted-concept search | 3/10 | 5/10 |
| Incorrect donor | 10/10 | 10/10 |
| Untrained network | 10/10 | 10/10 |

No calibration matched-control upper bound falls below the .01 margin.
Nevertheless, even collapsing all intervals to their observed means yields
complete support for only **one** constructed layout. The prescribed margin
against strong optimized controls is therefore material beyond interval width.

## Ordinary-network extraction comparison

The following are **development point summaries**, each averaging the same
ten model/role rows and five equally weighted strata. The role adequacy count
uses only point MAE and near/far decision thresholds; it is not the original
complete support criterion or a confidence-qualified declaration.

| Mask method | Mean probability MAE | Mean near disagreement | Mean equal-target effect RMS | Point adequate roles |
|---|---:|---:|---:|---:|
| Original frozen subset | .039626 | .354932 | .038405 | 3/10 |
| Rounded fractional top eight | .029993 | .308508 | .031772 | 9/10 |
| Exhaustive binary logit-MSE subset | .028251 | .291992 | .030631 | 9/10 |
| Fractional mask | .025032 | .257288 | .026838 | 10/10 |

All five proposal families improve their pooled validation MAE when the
original MSE selector receives 1,024 rather than 128 nested proposals. For
cost correlation the means are .040887 and .033379 respectively. This
supports an attainable search improvement with the source networks unchanged.
The proposed robust selector **worsens** pooled validation MAE in all ten
family-by-budget aggregates. That negative finding should remain visible.

The exhaustive binary comparison makes substantial progress while preserving
an eight-coordinate intervention. Fractional masks improve further on the
same discovery logit objective, but their extra average MAE reduction is
smaller than the overall gain from the original frozen subsets to the
exhaustive binary subsets. Those comparisons also change discovery data and
objective relative to original F15; the arithmetic is not a causal percentage
attribution among causes of its failure.

The evidence supports limited search and endpoint selectivity as concrete
contributors. It also demonstrates a useful relaxation of the binary-mask
restriction. It does not establish technical superposition, prove that useful
cost information was absent, or identify a unique native utility representation.
Ordinary training's lack of an incentive for clean cost modules remains a
salient explanation of why this restricted extraction problem is nontrivial.

## Remaining accounting obligation

The research clock was still open when these scientific audits were completed.
The Research90 floor and ledger close must be established separately by the
final accounting audit. This report supplies no elapsed-time or gate pass.
Parallel reviewer minutes are zero; F16 and Gates C/D remain unattempted.
