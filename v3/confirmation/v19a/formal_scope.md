# Scope of the optional mechanized reconstruction

Codex (GPT-6), October 28, 2026. Prospective statement of a mathematical
proof unit within P3-11-A1. The fixed V19 candidate is unchanged.

Use the official digest-pinned Lean4.35.0 release and its standard library,
without Mathlib or a numerical solver. Formalize these abstract identities:

1. A collection of existential observation witnesses can be represented
   by one assignment function, with all universal constraints retained.
2. The attained-minimum values of an independent family of nonempty closed
   scalar intervals are exactly the values above at least one lower bound
   and below every upper bound.
3. Taking the union over admissible branches is equivalent to selecting an
   anchor/local label and a compatible outside branch with sufficiently
   high local upper endpoints.
4. An attained largest outside threshold turns an existential threshold
   comparison into a comparison with that largest threshold.

State order laws and local interval/attainment properties as explicit theorem
parameters, not unproved global axioms. The proof unit does not formalize
real convexity, compactness, rational LP duality, bit complexity, the subset
DP implementation, the Python checker or the application geometry. Those
remain separate mathematical/review obligations. In particular, proving a
tautology after assuming AR1 is not an acceptable substitute: the statement
must start with actual local choices and an attained minimum.

Preserve every compiler attempt's complete source, stdout/stderr, command,
exit status and hashes in short numbered files. Proof-writing syntax/type
failures are development of the reconstruction, not hidden empirical trials.
The source statement is governed by this scope; any substantive weakening
must be explicit. Do not use `sorry`, `admit`, unchecked unsafe evaluation,
or new global `axiom` declarations. Print the final theorem dependencies.
Successful compilation establishes only these named formal lemmas under
their visible assumptions and Lean's trust base; it does not independently
confirm the whole contribution event or its novelty.
