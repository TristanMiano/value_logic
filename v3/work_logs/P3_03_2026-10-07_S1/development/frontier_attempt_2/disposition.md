# Completed parity cases and prospective remainder

This attempt completed the six planned parity cases and 1,501 assertions,
then failed while admitting the first ordering input. The evaluator supplied
JSON integers for the rational literal and scale; the kernel requires exact
integer or fraction **strings** in those positions and correctly refused them.
The six complete parity traces, original evaluator, input catalogue, manifest
and overall FAIL summary remain unchanged. The summary's empty `cases` array
results from the exception before the evaluator returned its accumulated
case summaries; the complete parity records are in `traces.json`.

The next fresh attempt will supply `"1"` and `"-1"` in the ordering AST and
run only the six ordering and two withdrawal cases, using the explicit
`--part ordering_withdrawal` selector. It will not repeat the completed parity
computation. No scientific kernel change, new case family or altered threshold
is introduced. A separate read-only evidence reconciliation will verify the
saved parity source sets/counts and link both attempts without changing their
historical summaries.
