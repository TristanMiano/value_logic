# P3-03 development plan — recorded before the first executable check

Contributor: ChatGPT (GPT-6 Astra Pro), October 7, 2026 UTC.
Status: **DEVELOPMENT; no final challenge, freeze, exposure or gate attempt**.

## Target and access

Investigate the finite cover and bounded register-machine implementation in
`v3/checks/03_bounded_logic.py`. The method receives its explicit finite input,
conditional assumptions, loss terms and per-call transaction allowance. It
does not receive a complete satisfying-assignment table or reference VM answer.
The evaluator may exhaustively enumerate small Boolean domains and run a
separately written reference VM. Those results are checks, never method inputs.

Record a manifest with the exact input catalogue, method and evaluator hashes
before executing each attempt. Use a fresh numbered directory; retain failures
and their input bindings. Changes after feedback are development iterations.
No held-out generalization or final validation is claimed.

## Reliable checks

1. Inspect every boundary of small finite refinements. Check disjointness and
   containment of all assignments satisfying the active source, including
   unvisited assignments. Reported intervals must contain the evaluator's exact
   extrema whenever that source is nonempty. A conflict requires an empty source.
2. Check partial Boolean evaluation and the rational loss language against
   independent point evaluation, including negative scaling, residuals, min/max,
   repeated variables and nested expressions. Check narrowing for fixed sources.
3. Compare bounded VM answers with a separate interpreter. Keep a stopped
   producer, an unfinished checker and an admitted signed answer distinct.
   Check horizon zero, a bounded nonhalting execution, both requested bits,
   and one-transaction calls that retain production and checking progress.
4. Check immediate literal uptake, source feasibility status, exact filtering,
   objective/unit changes, premise addition, transitive withdrawal/reset and
   preservation of independently valid receipts.
5. Run identical command transcripts through the value-facing method and its
   ordinary finite constraint/interval interpretation. Compare states, reports
   and resource records. This is an identity reconstruction of one engine,
   not an independently implemented performance rival.

## Exploratory attacks

1. The visited-only upper bound; contradictory assumptions with an unfinished
   nonempty cover; XOR under a one-cell cap; and loss identification without
   identification of truth coordinates.
2. Cross-instance reports with equal epoch counters but different source
   assumptions; changed query versions/horizons/targets; corrupted candidate
   answers, terminal records or request bindings. Fault injection is an
   evaluator attack on internal state, not an advertised external admission API.
3. Withdrawal of a premise supporting other premises; withdrawal of a checked
   receipt; an objective update without a source update; source refinement with
   a valid but less precise earlier report.
4. Expression, input, storage and numerical limits. Check that refusal keeps
   the committed source cover and does not manufacture a truth answer.
5. Lost progress under restart, fresh unresolved queries and insufficient
   capacity: explicit counterexamples to unconditional convergence claims.

## Measurements and stopping

Small exhaustive cases are sufficient to locate the identified risks; do not
inflate case counts as evidence of mathematical generality. Record host wall
and process time separately from capped kernel transactions and detailed work
counters. Report the precise implemented input bounds and any bookkeeping or
serialization excluded from the transaction allowance. No invented task-price
vector, free loss scan, or advantage inferred from differently weighted costs.

Passing development checks supports the concrete implementation examples, not
the universal proof by itself. The principal must state and prove its invariant
and conditional completion claims separately. Stop expanding tests when the
named risks are resolved; spend any protected research remainder on substantive
assumption checks and constructions. Research90 is measured principal engaged
time; concurrent reviewer work earns no additional time credit.
