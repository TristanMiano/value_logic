# Phase Two Workspace: Value-Based Calculus First

**Active research direction:** [DIR01](decisions/DIR01_loss_grounded_reflective_direction.md)
connects loss-based value semantics, modest reflection and discovery of learned
neural structure. [Opportunities](opportunities.md) are ranked research leads,
not new results. F01-F03 remain complete; the next task remains F04.

Current control document: [../TODO_v2.md](../TODO_v2.md).
Execution protocol: [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md).
Decision record: [decisions/2026-09-19_calculus_first.md](decisions/2026-09-19_calculus_first.md).

## Current status

**F01 is complete.** The eight worked examples have been reconstructed and
extended with explicit positive repairs, assumption tests, and 50 additional
checks. The two F01 suites pass **76 tests**, and **60.243613 credited derivation
minutes** are recorded across S1 and S2. See the
[completion record](work_logs/F01_2026-09-21_S2.md).

**F02 is complete.** The [candidate note](foundations/02_candidate_semantics.md)
and [reconstruction supplement](foundations/02a_candidate_reconstruction.md)
compare four concrete formulations. The original 53 checks plus 71 continuation
checks give **124 passing dedicated F02 tests**. Credited derivation time is
**61.118295 minutes** across S1 and S2, satisfying D60. The
[completion record](work_logs/F02_2026-09-22_S2.md) preserves actual clocks,
source-check limits, research evidence and the cumulative package disposition.
**F03 is complete at its literature-audit scope.** The
[closing phase-one comparison](literature/01j_phase_one_literature_and_novelty.md)
connects the broad original objectives and concrete phase-one theorems to the
source literature. The register now contains eight core sources and twenty
scoped supplements, with explicit hypotheses and unused stronger claims.
The existing [theorem agenda](literature/01i_calculus_desiderata_and_theorem_agenda.md)
remains proposed, not selected. Twenty new exact finite/metadata checks bring
F03 discovery to **256 passing tests**. The [completion record](work_logs/F03_2026-09-24_S10.md)
records **60.216954 cumulative L minutes**, satisfying L60.
**Next: F04 — hostile examples and candidate discrimination (not started).**
No calculus has been selected, and no readiness gate has passed.

The intended result is a small, explicit calculus with operationally meaningful
value objects, justified inference rules, worked derivations, and an executable
reasoner. Do not assume that the eventual calculus must be scalar-valued,
bounded, probabilistic, contract-based, three-valued, or architecture-specific.
Do not silently equate value with probability, truth, or one uniquely correct
utility function. The formal metatheory may use ordinary mathematics while
making its assumptions explicit.

## Historical inheritance

The completed August 1, 2026 Task 0 note is preserved byte-for-byte in
[inheritance_contracts_archive.md](inheritance_contracts_archive.md). Its
import/reinterpretation/exclusion table describes the superseded
contract-and-inverse plan, not obligations of the current phase.

The old control document is preserved at the repository root as
[TODO_v2_contracts_archive.md](../TODO_v2_contracts_archive.md), so its relative
links keep their original base. The old README is similarly preserved as
[README_phase1_archive.md](../README_phase1_archive.md). These archives do not
supply active execution instructions.

Use phase-one definitions and theorems when their hypotheses and purpose match.
Classify reuse as unchanged, adapted, comparison-only, or not imported. A result
can remain valid in phase one without being a primitive of phase two. Preserve
the original paper, experiment outcomes, and completed task history.

## Planned artifacts

F01 establishes [project_spec.md](project_spec.md),
[claim_ledger.md](claim_ledger.md), [notation.md](notation.md), and the
[principal derivation note](foundations/01_requirements_and_separating_examples.md).
[Exact fixtures](checks/f01_examples.py) and [results](checks/F01_results.json)
check the original example calculations. The
[reconstruction note](foundations/01a_reconstruction_and_information_contracts.md),
[additional fixtures](checks/f01_reconstruction.py), and
[additional results](checks/F01_reconstruction_results.json) audit their limits
and positive extensions. Neither suite is the future phase-two reasoner.

Further work will populate `foundations/`, `derivations/`, `literature/`,
`verification/`, `experiments/`, and `checkpoints/`. Every research task keeps
derivation notes, source checks, and executable evidence distinguishable.
Timing records use `work_logs/<task>_<session>.md`, based on
[templates/work_item.md](templates/work_item.md); aggregate actuals go in
[time_ledger.csv](time_ledger.csv), initialized by S1 and extended by S2.
The final report is `../paper_v2.md` only after the readiness gate passes.

## Validation command

Until F11 adds the new reasoner, run from the repository root:

```text
python -m verification
```

This checks inherited semantics and repository integrity; it does **not**
validate the proposed phase-two calculus. The F01 fixtures can also be run alone:

```text
python -m v2.checks.f01_examples --json v2/checks/F01_results.json
python -m v2.checks.f01_reconstruction --json v2/checks/F01_reconstruction_results.json
python -m unittest discover -s verification -p 'test_v2_f01*.py'
```

The original suite has 26 tests; the reconstruction suite has 50. The combined
local discovery command passes 76. These results check the finite examples,
not unrestricted theorems. Two `verification/test_v2_f01*.py` bridge files include
both suites in the full repository command.

For the completed F01 work, the full command was not run in its research
container because git network name resolution failed. The write-enabled
connection then available published those changes, and their exact GitHub
Actions result was checked before advancing `main`. That historical result is
distinct from both the local targeted checks and validation of new F02 changes.
Consult each commit's workflow result rather than infer a full pass from source
inspection or an earlier commit's checks.

The F02 candidate fixtures can be run separately:

```text
python -m v2.checks.f02_candidates --json v2/checks/F02_results.json
python -m unittest discover -s verification -p 'test_v2_f02_candidates.py'
```

Both commands passed 53 checks in the F02 first session. They are not a general
reasoner or a fresh full-repository pass. In that historical S1 session, exposed
GitHub actions lacked repository writes, and local git cloning failed on DNS.
S2 retested branch creation successfully; the current completion remains a
downloadable package, without a claimed F02 content commit or remote CI pass.
The earlier F01 results are not relabeled as validation of the new changes.

From F11 onward also run:

```text
python -m v2.verification
```

F11 must implement that entry point before recording it as available. If the
environment cannot run a command, record `not run` and the actual reason;
do not infer a pass from source inspection. Check the GitHub Actions result
for the exact pushed commit separately from local validation.

## F02 completion checks and package

Run the following from the repository root using Python 3.10 or newer:

```text
python -m v2.checks.f02_candidates --json v2/checks/F02_results.json
python -m v2.checks.f02_continuation --json v2/checks/F02_continuation_results.json
python -m unittest discover -s verification -p "test_v2_f02*.py"
```

The first two suites contain 53 and 71 tests; combined discovery passes 124.
Both result files reproduce exactly. These are constructed development cases,
not F11's reasoner, a held-out experiment or an unrestricted theorem proof.
The full `python -m verification` was not run in the research environment because
no full checkout could be obtained. No F02 content commit or full CI pass is
claimed by this package. The branch-creation access test succeeded; `main` was
left at the F01 completion snapshot. See the session record and the package's
`START_HERE.md` for the distinction and Windows/WSL installation steps.

The downloadable completion package contains all S1 and S2 changes relative to
`ba551afe7f4c026c075a49b09b341eec446caf1a`; applying the old partial package first
is unnecessary. A separately checked delta supports the exact, clean, committed
S1 state. The helper checks hashes and a clean Git state, stages the selected
patch and restores only changed paths from the index. It never commits or pushes.
The historical S1 delivery limits remain recorded in its unchanged work log.

## Completion and recurrence

Passing Gates A through D requires the evidence in the active roadmap and the
research protocol. A counterexample or changed definition can invalidate a
previous pass. Schedule targeted repair work, preserve the historical record,
and rerun the affected gate before relying on its downstream conclusions.

## F03 partial-audit validation

```text
python -m v2.checks.f03_imports --json v2/checks/F03_import_results.json
python -m unittest discover -s verification -p 'test_v2_f03_imports.py'
```

Both commands passed 31 checks in the partial-audit workspace. These check
specific finite witnesses and source-record integrity, not source authenticity,
unrestricted theorems, a final reasoner, or F03's time floor. The new bridge file
includes them in the existing full command when a complete checkout is used.
Full local repository verification was unavailable in this session; publication
status and CI must be checked for the actual resulting GitHub commit, not inferred
from this note. The original `python -m verification` requirement is unchanged.

### F03 continuation checks

```text
python -m v2.checks.f03_proof_audit --json v2/checks/F03_proof_audit_results.json
python -m unittest discover -s verification -p 'test_v2_f03*.py'
```

The S2 commands pass 39 new and 70 combined tests respectively. They check
explicit arithmetic conventions and finite source adapters, not the complete
Rational Lawvere proof system. S2 expands the source manifest by one targeted
source and updates its integrity test to retain all original source IDs.
The full repository command and exact-commit GitHub Actions requirement remain
unchanged; full local verification was unavailable without a complete checkout.


### F03 S3: Lawvere/value bridge checks

```text
python -m v2.checks.f03_value_bridge --json v2/checks/F03_value_bridge_results.json
python -m unittest discover -s verification -p 'test_v2_f03*.py'
```

S3 passes 32 new and 102 combined tests. These are finite exact-arithmetic
translation checks, not an implementation of either source's complete proof
system. The S2 source test now permits documented supplements while retaining
all original source IDs; the new test checks the exact 8-core/5-supplement
manifest. The initial cardinality failure and its repair are retained in the
session evidence. Existing mathematical assertions were not weakened.

S3 is delivered as a local patch/overlay because repository-write actions are
not exposed in this run and local Git network access fails. No S3 commit, push,
or CI success is asserted here. Full `python -m verification` was not run in
the overlay; use the cloned repository and its actual CI result for that check.


Run the additional belief/KL fixtures with:

```text
python -m v2.checks.f03_belief_kl --json v2/checks/F03_belief_kl_results.json
```

These 33 checks use toleranced floating-point logarithms, not exact symbolic
proof. Historical suite counts above refer to their recorded checkpoints; the
S4R1 combined F03 discovery total was 135.


## F03 S5 checkpoint: context audit (September 24, 2026)

F03 remains **partial**. [The new source/mapping note](literature/01e_belief_value_import_contracts.md)
adds update-context distinctions, a scoped S16 convexity counterexample and
repair, and exact rational logarithm/KL certificates. Its new **40 tests** pass;
combined F03 discovery passes **175**. Use:

```text
python -m v2.checks.f03_context_audit --json v2/checks/F03_context_audit_results.json
python -m unittest discover -s verification -p 'test_v2_f03*.py'
```

The certificate report uses exact fractions; selected numerical reference
tests use explicitly stated binary64 tolerances. This is not a completed
calculus or whole-paper independent verification. The
[S5 work record](work_logs/F03_2026-09-24_S5.md) records actual time, source
inspection limits, and package-only delivery. The authoritative pointer is
still F03; F04 and all gates remain unattempted.


## Latest F03 checkpoint: consolidated source handoff (September 24, 2026)

F03 remains **partial**. The [handoff note](literature/01f_consolidated_source_handoff.md)
and [source-use register](literature/F03_import_contracts.json) consolidate all
18 source identities and spell out import guards. They are not a theorem prover
or a permanent core. Two finite adapters separate directed substitution gains,
pointwise arithmetic, uniform witnesses, and belief/attainment types.

```text
python -m v2.checks.f03_handoff --json v2/checks/F03_handoff_results.json
python -m unittest discover -s verification -p 'test_v2_f03*.py'
```

The new suite passes **14 tests**, and combined F03 discovery passes **189**.
All new numerical fixtures use exact fractions. Source-register tests check
bookkeeping, not the truth of external theorems. See the
[S6 record](work_logs/F03_2026-09-24_S6.md) for clocks and source-access limits.
Cumulative literature time is 38.537260 minutes; 21.462740 remain against L60.
This is an incremental local package based on the author's `9ba491f` commit,
not a push or new CI run. The full repository command was not run locally.
F03 remains selected; F04 and all gates are unattempted.

## S7 source-certificate checks

Run the additional audit fixture with:

```text
python -m v2.checks.f03_checked_derivations --json v2/checks/F03_checked_derivations_results.json
python -m unittest discover -s verification -p 'test_v2_f03*.py'
```

The new suite has 18 tests and combined F03 discovery has 207. The saved JSON
includes two full conditional proof certificates, with 18 and 32 source-rule
nodes. It checks neither the whole RLL system nor operational evidence for the
assumptions. Full repository verification and new CI were not run in S7.


### S8 source-boundary fixtures

```text
python -m v2.checks.f03_context_witness --json v2/checks/F03_context_witness_results.json
python -m unittest discover -s verification -p 'test_v2_f03*.py'
```

The new suite has 15 tests; combined F03 discovery has 222. The general arguments
are in the source-adapter note. The incremental package is not pushed from this
environment; full local repository verification was not run. The restored root
README and phase-one files are unchanged.


## S9: literature-informed attributes and theorem targets

The [agenda note](literature/01i_calculus_desiderata_and_theorem_agenda.md) and
[structured agenda](literature/F03_calculus_agenda.json) separate eight proposed
design questions from five unproved target results. The recommendation is a
sound compositional core plus one substantive operational characterization or
constructive adequate-abstraction result, not every target in one phase.
No philosophical commitment, core selection or readiness gate is added.

Run the small exact-arithmetic illustrations independently with:

```text
python -m v2.checks.f03_theorem_agenda --json v2/checks/F03_theorem_agenda_results.json
```

The fourteen checks validate only elementary examples and record consistency.
The combined F03 discovery command now passes 236 tests; this is not full
repository verification or proof of any proposed main theorem. The package
records local application and targeted test validation separately from CI.
