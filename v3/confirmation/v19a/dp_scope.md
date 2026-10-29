# Supplemental formal unit: attained dynamic-programming summaries

Codex (GPT-6), October 28, 2026. Prospective P3-11-A1 reconstruction unit.
The frozen candidate, contribution event and original four-lemma formal seal
remain unchanged. This optional unit addresses the next unmechanized bridge:
a finite maximizing summary must preserve an attaining witness, including
when candidates are combined by a monotone bottleneck operation.

Formalize an executable list argmax under explicit reflexive, transitive,
total order assumptions. Prove absence exactly for the empty list and, for
every returned witness, membership and domination of every listed entry.
Then prove a one-step compression theorem: in a finite collection of groups,
replace each nonempty child group by its maximizing witness; if the parent
score is monotone in the child score within each group, an argmax of those
representatives is also an attained argmax of the full expanded collection.
State the exact bridge to min-based subset DP and prefix/suffix backpointers.

This does not formalize rational LP, the mask enumeration, Python dictionaries,
continuous source constraints or the whole end-to-end runtime. It may use
explicit algebraic order assumptions, but no admitted goals or added axioms.
No performance measurement is planned. Use the already identified Lean4.35.0
runtime. Save and hash the scope, source and runner before each compiler
attempt; preserve every compiler failure and every subsequent source revision.
A formalization repair is not silently a candidate-code repair. If a failure
exposes a substantive mathematical defect, record it and reassess A1.
Compiler waits are excluded with principal-clock boundaries. Do not rerun a
passing unchanged source merely to increase the check count.
