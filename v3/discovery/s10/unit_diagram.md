# Source admission with checked unit propagation

Codex (GPT-6), DEVELOPMENT, 2026-10-14.

The first diagram compiler repeatedly branches into contradictions that unit
propagation could detect early. It also pays to retain and check those dead
branches. Use ordinary unit propagation, with explicit original-clause reasons,
before each fixed-order branch. This is established SAT reasoning; the work here
is a source-equivalence trace, weighted evaluation compatibility, and billing.

A state remains (depth, active original-clause IDs). Active clauses have not
been satisfied by the assigned prefix. In each clause, literals earlier than
depth are false and may be omitted. Start an empty assignment to future
variables. A recorded unit step (clause ID, literal) is valid when the reason
clause is active, all its other remaining literals are false under preceding
unit steps, and its surviving literal is unassigned. A recorded conflict is
valid when some active clause has no true or unassigned remaining literal.

If the current order variable is forced, emit only its forced live child and
set the other diagram edge to false. Otherwise emit both children. Each child's
active list is obtained solely by satisfying the current variable in the
parent's active original clauses; future unit assignments are recomputed from
that child state, not silently passed as additional premises. This may repeat
work, but makes equivalence checking local and avoids hidden assumptions.

Induction over the fixed order proves that every source model follows exactly
one live path and every live terminal path satisfies the source. Unit reasons
justify every omitted branch. The diagram still emits every live variable
layer, including forced variables, so signed weighted objectives and min-
marginals account for all feature costs. Removing a forced variable's weight
would be unsound even though satisfiability alone is preserved.

The checker need not require propagation to saturation: a valid prefix of unit
steps only gives less pruning. It must validate each reason and every child
active list, enforce node depth/order, bind the original source and features,
and reject unreachable trace states or inconsistent node identities. A state
cap remains necessary; unit propagation does not guarantee polynomial size.

Compare fresh baseline/propagated compilations on all39 exposed sources (the
23 old synthetic/external sources plus16 new numeric sources). Charge producer,
checker, trimming and retained representation separately. Truth enumeration,
64 signed objective/min-marginal checks per source and corrupt-trace controls
are diagnostics, separately billed. No new physical observations are needed.
