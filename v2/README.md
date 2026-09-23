# Phase Two Workspace: Value-Based Calculus First

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
**F03 is in progress.** Its [first audit](literature/01_foundations.md) covers
8 core sources plus 4 targeted supplements after S2. The
[proof-system audit](literature/01b_proof_system_audit.md) extends the
[original import boundaries](literature/01a_import_boundaries.md) with explicit
source adapters, not a selected calculus. The 31 original checks plus 39 new
checks pass locally (70 combined). The unchanged
[S1 record](work_logs/F03_2026-09-22_S1.md) and
[S2 record](work_logs/F03_2026-09-22_S2.md) credit 23.230881 cumulative L minutes;
36.769119 minutes of L60 remain. **Next: continue F03 — external foundations audit.**
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
