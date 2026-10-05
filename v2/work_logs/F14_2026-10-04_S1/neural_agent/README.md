# Neural subagent development record

Contributor: delegated neural implementation agent in the F14 session, working
from base `6ce41d7`. Its work overlaps the principal agent's session. No
subagent duration is added to the principal protected floor or cumulative
POST-B-1 clock.

## Artifacts and evidence

- `initial_smoke_development.json`: superseded exponential-family evidence;
  the first 128-step development integration,
  retained before later pre-freeze schema/control refinements. Its actual
  embedded configuration, models, candidate scores and outputs are preserved.
  It predates the final all-rival separating stratum and all-family numerical
  gauge report; it is not the frozen experiment.
- `full_budget_development_prepared.json` and its `.sha256`: superseded
  exponential-family evidence; one ordinary
  3,000-step development model plus full 128-candidate discovery, all 20
  hypothesis/control combinations and their saved pools/scores. This file
  was written, hashed and reloaded before diagnostic evaluation.
- `full_budget_development_results.json`: 512 new diagnostic pairs per role
  and stratum, with 8,192 observational task rows, all using development seed
  1400491 after discovery seed 1400401.
- `full_budget_development_metadata.json`: recorded clocks, environment,
  source hash, file hash, peak process RSS and separated CPU/wall times.
- `full_budget_development_summary.json`: a compact inspection view of that
  development integration.
- `tests_neural_14.log`: final focused run; 14 neural development tests pass.

## Current normalized-probability rival family

Before the final freeze, the fourth high-level rival changed from
`exp_sum_half` to `inv_total_cost=1/(J0+J1)`, giving the ordinary competing
description `(p*,1-p*)`. The scientific reason was to test normalization of
expected costs directly, alongside the two eta-factor alternatives. No
training result selected this replacement. All four hypotheses retain the
same capacity and budgets.

The old JSON artifacts listed above remain unchanged as superseded pilot-family
evidence. Current-family validation is stored separately:

- `normalized_geometry_development.json`: model-free acceptance diagnostic and
  an explicit strict interior witness. With 32,768 proposals per role, observed
  acceptance was 15.448% and 15.979%; the frozen rejection budget remains ample.
- `normalized_prepared.json` and `.json.sha256`: current-family full-budget
  discovery, saved and reloaded before diagnostic generation.
- `normalized_results.json`, `normalized_summary.json`, `normalized_metadata.json`:
  512 diagnostic pairs per role/stratum and 8,192 task rows on the original
  development seeds, with one-thread OMP/OpenBLAS/MKL settings before startup.
- `normalized_tests.log`: all 29 focused tests pass, comprising 15 neural
  implementation tests and 14 statistical-contract checks. The added test
  verifies the normalized concepts and their analytic interchange formulas.

Current-family preparation took 1.396956 wall / 1.396897 CPU seconds;
diagnostics took 0.198852 wall / 0.198846 CPU seconds. Recorded peak process
RSS was 47,832 KiB. Every scale-separating comparison used all 512 rows, and
all four numerical gauges passed. No F15 seed, threshold adjustment, additional
search budget, or final 8,192-pair intervention evaluation was used. This run
revalidated the changed generator/control after the prospective design choice.

## Final-family full-count development validation

The subsequent `normalized_fullcount_*` records use the exact saved
`config.v1.json` snapshot and all main neural counts on development seeds
1400401/1400491 only. They include the configuration, prepared model/alignment,
complete diagnostic output, analysis output, runtime metadata and SHA256
sidecars. The prepared artifact was saved, hashed and reloaded before the
8,192-pair-per-stratum diagnostic; ordinary task diagnostics also used 8,192
rows. No F15 seed was consumed.

Every checked resource count matched the protocol: 768,000 training outcomes,
5,120 candidate fits, 3,276,800 selection-pair checks, 81,920 diagnostic pairs,
1,638,400 alignment-pair checks and 112 confidence rows for one development
model. All six rival/role scale comparisons retained 8,192 rows; all four
gauges passed. The largest proposal count in any generator cell was 77,824,
within its frozen cap. Preparation took 1.519107 wall / 1.516489 CPU seconds;
diagnostics took 1.345005 wall / 1.344269 CPU seconds. Peak process RSS was
203,448 KiB with one-thread numerical settings.

The source audit observed a concurrent edit to `analysis.py` during the first
run, while neural code, configuration and protocol remained unchanged. The
raw diagnostic record was therefore reassessed under a checked stable analysis
source without retraining or generating more data. The stable assessment and
`normalized_fullcount_reassessment_receipt.json` retain source/code hashes and
the input artifact hashes. The two assessment artifacts are identical.
Its classification is development-only
`specified_subset_hypothesis_not_supported_at_frozen_thresholds`; it is not an
F15 result or a reason to retune criteria.

## Optional search sensitivity check on the compiled positive calibration

The original `calibration.py` checks supplied known subsets. The separate
`compiled_search_*` artifacts test the actual frozen guided search with
128 candidates per role, without supplying those known subsets to search.
This uses the manually compiled network, zero training, full discovery counts,
and development seeds 1400401/1400491 with 8,192 diagnostic pairs per stratum.
Discovery was saved and hashed before diagnostics.

Both searched and supplied-oracle subsets pass the frozen absolute-MAE,
conditional-base, derived effect-MAE and near/far decision adequacy components
in this constructed example. Searched MAEs range about .0078–.0131; oracle
MAEs about .0012–.0015. Search selects different coordinates, including some
overlap between roles. This does not establish search completeness, exact
coordinate identification, joint constructive abstraction, ordinary learned
structure, or the full matched-control/scale-specificity pilot criterion.
The diagnostic used 256 candidate fits total and no expanded search budget.

## Earlier pilot-family observations

No prospective F15 seed (1500401–1500405 or 1500491–1500495) was executed by
this agent. The earlier pilot below used 512 pairs per stratum; the later
full-count development validation is recorded above.
These development results do not constitute F15, a gate pass, or a scientific
claim about the final population. They validate the full discovery pathway,
serialization boundary, stronger pair generator and diagnostic schema.

The full development run used 768,000 stochastic binary labels and zero
expected-cost training labels; 5,120 candidate evaluations and decoder fits;
and no alignment refits after saving discovery. Preparation took 1.375250
wall seconds / 1.766133 process CPU seconds; diagnostic evaluation took
0.167677 wall seconds / 0.604099 process CPU seconds. Recorded peak process
RSS was 47,316 KiB on this Linux execution host. These values are development
resource observations, not a speed-comparison claim.

Observational task MAE was 0.019149. Identity-model role-0 intervention MAEs
across the five strata ranged 0.033879–0.037939; role-1 ranged
0.030594–0.070549. The experiment therefore visibly distinguishes good
ordinary task prediction from uneven intervention agreement. All four
transported numerical gauges passed. No threshold or search budget was
retuned in response to this full development result.

## Failures and corrections

No numerical training, generator, or native-process failure occurred in
these agent runs. The initial 14 implementation tests passed throughout.
The subsequent independent contract audit deliberately tested malformed
records and exposed three missing guards; its first failure log and corrected
14-test passing run are preserved in `contract_initial_tests.log` and
`contract_revised_tests.log`. [The contract audit](contract_audit.md) records
the findings and their resolution. These were deterministic validation defects.
Two documentation `apply_patch` calls failed because their
expected context began in the middle of an existing line. They made no changes;
the actual lines were read and each narrow patch was corrected. These were
deterministic edit-context errors, not test reruns or host-instability events.
The original failed-tool texts are retained in `editing_error.log`.

## Timing scope

`timing.json` records observed UTC/monotonic clock checks on this runtime.
The initial 81.828-second design segment was observed. Later work mixed
implementation, computational checks and interpretation; not every category
transition had its own matched clock. Those intervals are retained without
inventing a retrospective D/E split or assigning them protected-floor credit.
The full development computation has its own observed start/end interval and
resource measurements. Initial orientation before the first clock remains
unmeasured.
