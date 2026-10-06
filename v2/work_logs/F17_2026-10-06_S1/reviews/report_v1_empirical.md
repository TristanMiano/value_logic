# F17 report v1 — empirical consistency review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, same-model internal delegated review.
October 6, 2026. Concurrent principal time credit: **zero**.

Reviewed fixed draft: `v2/work_logs/F17_2026-10-06_S1/drafts/report_v1.md`,
**88,634 bytes**, SHA256
`af2a98350273c59eb2b682e62be9df13c11f8f1f9d67df7b0c94d73e24673784`.

**Disposition: empirical numbers, original claim dispositions and execution
provenance are supported. Minor methods/interpretation clarifications are
requested below. No incorrect count, resource value, reported endpoint or
new scientific result was identified.** This is a scoped report review, not
Gate D or a new scientific assessment.

The full fixed text was read, with detailed comparison of the abstract,
introduction and §§8–10, 12–14 against original F13/F15/ND01 sources and the
new table export. Theorems and external bibliography remain the separate
mathematical and literature reviewers' responsibility. No population,
training, alignment, experiment, test, or saved-data writer was run during
this review. Source and JSON reads only. Root is creating the new claim map
and work-log links; their temporary absence is not a finding against this
fixed draft.

## 1. Confirmed comparisons

| Draft content | Result of comparison |
|---|---|
| Abstract and introduction | Correctly state 68/160 usefulness, equal ordinary service, 5/5 task learning and 0/5 complete neural support; do not use the neural null as a novelty claim. The eight-neuron accessibility explanation is prominent and remains a hypothesis about internal organization. |
| Scientific worked derivation | Equation (22), premises, shared unbounded discrepancy, sample counts and `-4873/770000` bound match F13. Ordinary interpolation/support functions and Gaussian quadrature remain visible. No absolute-accuracy inference is made. |
| Actual self-assessment | Short/long proof costs 5/9, penalty 20, prefix formula and `q<=1/80` non-deterioration threshold match. Parity table values 35/4, 55/4, 0, 1/4, 9 and ordinary 5/6 emitted-node counts match. See small execution-wording repair E6 below. |
| Retention population | 16 initial laws × ten dependent revisions, six methods × two access regimes, 160 episodes, 1,920 method rows and 11,520 scalars are correct. All twelve table rows match the original-unit export. |
| Retention usefulness | Full direct-edit/native criterion is stated, with 68 distinct episodes, all 16 seeds, variant counts 14/14/9/16/15, and 15 selective approximate episodes over eight seeds. Thirty paired-method rows and 718 total useful rows are not treated as independent successes. |
| Ordinary retention controls | All 960 saved equal-information comparisons agree. Marginal information is explicitly weaker. Numerical/service and exclusive-power claims remain separated. |
| Resources | Fresh 1.005003/72.134739 ms, tailored 5.984763/81.452699 ms, cached +81.113254 ms across 98 matched cases, payload 125/143 bytes, total serialized 21,503/20,527 bytes, and repairs 412=60+352 all match the existing summaries/export. Payload is correctly distinct from process memory. |
| Neural task, scales and controls | Four inputs, 32 ReLUs, 193 parameters, 3,000 steps, 768,000 labels/model, 3,840,000 total labels, zero cost-training labels, and four scales agree with the freeze. Discovery's cost-derived counterfactual supervision is explicitly retained. |
| Original neural endpoint | 5/5 task readiness, 50/50 conditional base cells, 0/5 complete support, identity MAE 2/48/0, near decisions 3/6/1, far 10/10, random advantage 0/9/1, permuted 1/10 supported, and incorrect-donor/untrained 10/10 each are correct. Rival MAE counts and 0/5 complete outcomes match. |
| Neural denominator/power | 560 original simultaneous intervals, alpha .05, radius/cutoff rounded as displayed, 25,600 candidates/fits, 409,600 intended pairs plus 409,600 donor records, 40,960 ordinary examples and 8,192,000 evaluations match. No new interval is introduced. |
| Diagnostic table | All four method rows, rounded means, near/far disagreements, role counts and paired-model point counts match the raw ND01 mask evaluations and saved summaries. Original F15 remains 0/5, distinct from development point adequacy. |
| Original environment/chronology | CPython 3.12.14, NumPy 2.3.5, Linux, single-thread environment, both manifest hashes and F15 preparation/validation/exposure/completion timestamps agree. ND01 preservation commit exists with the displayed subject. |
| Original process resources | Preparation 7.628116 wall / 7.621769 child CPU seconds / 44,020 KiB; evaluation 184.274726 / 184.249148 / 248,364 KiB match the actual external records. Nested timers are not added twice. |
| Failure provenance | First-attempt scientific completion, separately preserved zero-byte aggregate, 160 intact original units, 15,833,616-byte exact recovery/hash and 180/181 versus 103/103 sidecars are correct. Historical Windows CRLF, crashes and distinct path-portability defect are not silently repaired or diagnosed as hardware. |
| 288-test statement | Explicitly identified as prior Gate C's first-attempt focused Linux regression, not F17 tests. Original result is exit 0, 288 tests, 56.759545926 external wall seconds. No whole-repository or Windows pass is claimed. |
| Saved verification commands | Existing `freeze verify`, F15 `--check`, ND01 `verify`, ND01 summary `--check` and F17 table `--check` paths are valid. Their branches do not generate populations or fit models. They were not rerun in this review. |
| Claim disposition, future work, attribution | Optional ND02 remains unstarted with a prospective joint-geometry question. Original neural non-support, bounded contribution, internal/non-blind review and no concurrent double counting remain explicit. Gate D is left separate. |

## 2. Minimal requested repairs

### E1 — State the calibration denominator precisely

**Location:** §10.4, immediately after introducing constructed calibration.

The draft's five layouts are correct but their dependence is not stated.
They are rescalings/permutations of one deliberately constructed function,
not five independent training replications. Add:

> The five calibration layouts are positive rescalings and permutations of
> one deliberately constructed function, not five independent ordinary
> training replications.

Source: `F15_ND01_results.md` §1 and `core_summary.json`
`calibration.same_constructed_function_across_layouts`.

### E2 — Define the diagnostic table's criterion, weighting and objective

**Location:** §10.4, around the four-row intervention table.

The current distinction from the complete endpoint is correct. It should
also tell the reader what “point-adequate” and the aggregate mean measure:

> Means weight five validation strata equally, then the two roles and five
> fixed networks equally. Point adequacy requires all five role MAEs to be
> at most .05, near-decision disagreement at most .35, and far disagreement
> at most .10. The exhaustive and fractional methods optimize the same
> finite discovery logit-MSE objective; the table reports probability MAE
> on diagnostic validation pairs.

This prevents the exhaustive search from being read as an exact optimum
for validation probability MAE, or the point count as a confidence support
criterion. Source: ND01 report §3; `tables.json`
`diagnostic_neural.weighting` and `point_adequacy`; original mask records.

### E3 — Retain the adverse selector outcome

**Location:** §10.4, after the development table or its scope paragraph.

Add this complete adverse result alongside the improved search/mask result:

> The proposed worst-stratum selector increased aggregate validation
> probability MAE in all ten proposal-family/budget comparisons relative
> to the original MSE selector; these comparisons reused the same five
> networks and validation arrays.

The ten groups are five proposal families × two nested budgets, each
aggregating two roles over five fixed networks. The overall robust-minus-
original mean MAE change is **+0.0017830418776058619**, although this extra
number is unnecessary in the prose. This is a descriptive selection result,
not ten independent neural experiments. Source:
`selection_diagnostics.json`, `selection_comparison.family_budget_summaries`
and `overall_descriptive_summary`; ND01 report §4.

### E4 — Give the concrete observed joint limitation

**Location:** §10.4, before proposing future ND02.

The draft correctly withholds joint interpretation but can say why the
existing diagnostic specifically leaves that question open:

> On a secondary panel assembled from existing validation arrays, actual
> fractional edits showed nonzero order dependence in all five models:
> mean probability-order RMS was .019126, versus .016329 for original
> subsets and .006024 for exhaustive binary masks. This panel was not a
> frozen joint stratum and received no confirmatory support claim.

All alternatives use the same secondary panel, constructed from existing
role-0 mixed-near bases/donors and existing role-1 mixed-near donors. Exact
mean **probability** RMS values are:

| Existing method | Nonzero model count | Mean probability order RMS |
|---|---:|---:|
| Original subsets | 4/5 | 0.01632916988271114 |
| Exhaustive binary | 1/5 | 0.0060241083571522394 |
| Fractional masks | 5/5 | 0.01912585401774089 |

These are neither logit RMS nor validation errors against a frozen joint
high-level endpoint. No favorable composition order is selected. Source:
`mechanism_results.json`, `secondary_composition`; ND01 report §5.3.

### E5 — Point the regression command citation to the command record

**Location:** §9.1 final sentence.

The linked `regression_attempt1/result.json` records the result, timings and
output hashes, but not the actual command or source manifest. Those exist
in `reviews/technical/regression_plan.json` and the technical review. Keep
the result link and add the command link, or point the combined reference
to `v2/work_logs/C_2026-10-06_S1/reviews/technical/technical_review.md`.
The 288 count and its historical scope are already correct.

### E6 — Avoid implying the cascade is selected at every allowed q

**Location:** §8.2, following equation (23).

“The cascade is then used on later requests” immediately follows a generic
non-deterioration condition. At the equality boundary the frozen tie rule
need not select the cascade; at the actual odd-parity population it selects
fallback. A minimal replacement is:

> The selected policy is then executed on later requests under the declared
> same-population assumption.

The theorem, threshold and parity table require no change. This is a local
precision repair to the execution statement, not a new scientific finding.

## 3. Review limits and completion

No stronger empirical claim is needed to assemble this paper. All requested
repairs are report text or source-link clarifications. They require no new
data, parameter changes, experimental stages or tests. The main statistical
and practical distinctions already survive in v1: original CI non-support
versus violation, ordinary competence versus extracted intervention
structure, diagnostic improvement versus joint adequacy, and mathematical
application versus demonstrated deployment superiority.

This review checked the frozen v1 text only. Final integration should record
the disposition of E1–E6 and preserve this fixed-review provenance; a later
draft is not silently substituted for the reviewed hash.
