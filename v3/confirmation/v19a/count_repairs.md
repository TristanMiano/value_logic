# Finite enumeration proof compilation history

Codex (GPT-6), October 28, 2026.

Attempt 1 failed while elaborating the higher-order `Fin.cases` argument
inside the list-length rewrite. The eliminator had no expected output
function type in that explicit theorem application. Before attempt 2,
eta-expand it with an explicitly typed `Fin (k+1)` argument. The definitions,
statements and mathematical counting argument do not change. Every failed
source and compiler result is retained; its dependent `sorryAx` diagnostics
are not accepted proof evidence. This is a deterministic elaboration repair.

Attempt 2 still lacked the eliminator's constant motive at the polymorphic
`List.map` application. Before attempt 3 supply `motive := fun _ => A` and
the complete output function type explicitly. The attempt-2 result is a
failure, despite a clock transition note that prematurely described the
intended review as inspection of accepted counts. That note does not establish
a pass; the saved compiler record is authoritative. The mathematical
definition and statement remain unchanged.
