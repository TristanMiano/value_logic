# Finite decision-cell check, before execution

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT; no optimizer or deployment study.
Freeze implementation, proof, runner, and this plan before exposure. Preserve
each attempt separately and do not rerun passing evidence.

Use breakpoints0,1 and five representatives -1,0,1/2,1,2. Each cell has one of
four statuses: outside O; possible but actually absent; actually present but
not inner-witnessed; inner-witnessed. Enumerate all4^5 status assignments
except those with empty actual R. Use four specified loss matrices: symmetric
indicator costs, crossing three-action costs, the loss-versus-regret dominance
counterexample, and a single action. Evaluate both loss and regret criteria.

Independently compute true worst losses over R for every case. Check lower/
upper containment, the sharper improvement certificate for every action,
both advertised action selectors, certified optimality, and irrelevance of
discarded unknown cells to the true worst vector. Also check that a cell
failing the irrelevance test changes some worst coordinate for the permitted
support J_I union{j}; this tests necessity at bracket-information scope.

Endpoint controls use exact singleton and interval unions, including points
at0 and1, the open interval(0,1), and unbounded tail cells. Validate malformed
unions, cuts, matrix shapes and unknown criteria. A final worked decision
uses the saved noisy-envelope partial records, without rerunning their service
or treating them as new independent evidence. Report proof scope and finite
support counts, not an empirical economic percentage.
