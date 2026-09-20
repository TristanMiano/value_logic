# Phase Two Workspace: Value-Based Calculus First

Current control document: [../TODO_v2.md](../TODO_v2.md).
Execution protocol: [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md).
Decision record: [decisions/2026-09-19_calculus_first.md](decisions/2026-09-19_calculus_first.md).

## Current status

The calculus-first phase is authorized; substantive research has not yet begun.
The next task is **F01 — requirements and separating examples**. Follow the
roadmap's current pointer if a later repair queue changes that selection.

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

F01 establishes `project_spec.md`, `claim_ledger.md`, `notation.md`, and
`foundations/01_requirements_and_separating_examples.md`. These paths are
prospective outputs, not files assumed already present.

Further work will populate `foundations/`, `derivations/`, `literature/`,
`verification/`, `experiments/`, and `checkpoints/`. Every research task keeps
derivation notes, source checks, and executable evidence distinguishable.
Timing records use `work_logs/<task>_<session>.md`, based on
[templates/work_item.md](templates/work_item.md); aggregate actuals go in
`time_ledger.csv`, created by F01. The final report is `../paper_v2.md` only
after the readiness gate passes.

## Validation command

Until F11 adds the new reasoner, run from the repository root:

```text
python -m verification
```

This checks inherited semantics and repository integrity; it does **not**
validate the proposed phase-two calculus. From F11 onward also run:

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
