# Layered recurrence reconstruction

Codex (GPT-6), October 28, 2026. Same-model P3-11-A1 proof reconstruction.

The first [retained attempt](layer_attempts/a01.json) accepted
[Layer.lean](Layer.lean), source SHA256
49bfe01cb0fb254a743a5ca095cca547533c07c8e1fce081d6a926993ab3b85d,
in869,861,800ns. It imports only Std and embeds the previously accepted
Dynamic source. Its printed theorems use only Lean's standard axioms;
there are no additional axioms, proof holes or unsafe declarations.

`best_of_cover` proves that replacing a finite candidate list by valid
dominating representatives preserves absence and optimality.
`solve_correct` carries this invariant through arbitrary finite layers,
state-dependent choices, terminal predicates and monotone path extension.
Returned paths belong to the uncompressed path family and dominate every
other legal path. `paths_length` checks the layer count. This covers the
logical induction behind retaining one best predecessor per state; ties
do not require retaining every maximizer.

The optional unit's prospective scope also identified an explicit receipt-mask
specialization. That planned subpart has not been added to this unit: the layer theorem is
generic, and the separate Count unit and written implementation review
still carry that connection. No claim is made to have verified Python
dictionary behavior, bitwise masks, memory use, or machine execution cost.
This additional mathematical unit does not by itself establish novelty
or complete P3-11-A1.
