# Prospective sharp refinement-gap panel

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT after A1.
Freeze the derivation, implementation, this plan, input builder and runner
with the existing decision_cells.py dependency before executing the panel.
Use a fresh directory; retain all failures. No successful reruns.

Use five scalar cells from breakpoints0 and2. Represent each selected cell
by one fixed rational point(-1,0,1,2,3), so all subset signatures are realizable
by normalized finite point unions. Include two declared matrices: the strict
improvement fixture padded by duplicate rows, and the safety/optimality
counterexample padded by duplicates. Add three three-action matrices from
random.Random(51029), integer losses0..13, and one single-action matrix.
Inputs are generated and frozen without executing the method.

For every K subset P with P nonempty, enumerate every nonempty J between
them. Independently compute all exact W_a(J)-min_b W_b(J), compare their
maximum to the proposed formula and check every emitted support witness.
Repeat using original loss and sourcewise regret. Check sharp<=earlier eta,
and record strict improvements and newly certified optimal actions.
Check the strict-improvement and unsafe-but-optimal examples explicitly;
reject unsupported criterion, malformed cell shape and inner outside outer.
Test empty outer status separately. Count all brackets/supports/action bounds;
do not interpret finite enumeration as general code correctness or novelty.
Record runtime and SHA256 of inputs, freeze and result records; machine time
is excluded from research credit. No optimizer or random simulation is needed.
