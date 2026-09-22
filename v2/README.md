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

**Next: F02 — derive competing semantic candidates.** It has not begun.
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

The full command was not run in the research container: a full checkout could
not be obtained because git network name resolution failed. Connected GitHub
reads and writes are available separately. Full GitHub Actions verification is
checked for the exact publication commit before advancing `main`; it is distinct
from the local targeted checks. Consult the commit's workflow result rather than
infer a full pass from this note or from source inspection.

From F11 onward also run:

```text
python -m v2.verification
```

F11 must implement that entry point before recording it as available. If the
environment cannot run a command, record `not run` and the actual reason;
do not infer a pass from source inspection. Check the GitHub Actions result
for the exact pushed commit separately from local validation.

## Completion and recurrence

Passing Gates A through D requires the evidence in the active roadmap and the
research protocol. A counterexample or changed definition can invalidate a
previous pass. Schedule targeted repair work, preserve the historical record,
and rerun the affected gate before relying on its downstream conclusions.
