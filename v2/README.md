# Phase Two Workspace: Value-Based Calculus First

Current control document: [../TODO_v2.md](../TODO_v2.md).
Execution protocol: [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md).
Decision record: [decisions/2026-09-19_calculus_first.md](decisions/2026-09-19_calculus_first.md).

## Current status

**F01 is partial.** Eight worked examples and 26 passing exact-arithmetic
fixture tests are recorded, with 15.97 measured engaged derivation minutes.
The 60-minute floor is not yet met; no calculus has been selected and no gate
has passed. Continue **F01 — requirements and separating examples**, using the
[session record](work_logs/F01_2026-09-20_S1.md) and the roadmap's current pointer.
F02 has not begun.

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

The partial F01 session establishes [project_spec.md](project_spec.md),
[claim_ledger.md](claim_ledger.md), [notation.md](notation.md), and the
[principal derivation note](foundations/01_requirements_and_separating_examples.md).
[Exact fixtures](checks/f01_examples.py) and [results](checks/F01_results.json)
check the example calculations, not a proposed phase-two reasoner.

Further work will populate `foundations/`, `derivations/`, `literature/`,
`verification/`, `experiments/`, and `checkpoints/`. Every research task keeps
derivation notes, source checks, and executable evidence distinguishable.
Timing records use `work_logs/<task>_<session>.md`, based on
[templates/work_item.md](templates/work_item.md); aggregate actuals go in
[time_ledger.csv](time_ledger.csv), initialized by the partial F01 session.
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
python -m unittest discover -s verification -p 'test_v2_f01_examples.py'
```

Both targeted commands passed 26 tests in session S1. The full command was
not run in that session because a full checkout could not be obtained in the
execution container; GitHub reads were available separately. No new CI result
is claimed. The bridge file `verification/test_v2_f01_examples.py` makes the
fixtures discoverable by the existing suite in a full checkout.

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
