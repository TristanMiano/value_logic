# Certificate-algebra formal reconstruction: first pass

Codex (GPT-6), October28,2026. Supplemental confirmation evidence.

[Dual.lean](Dual.lean) compiled on the first attempt with official Lean4.35.0,
exit0 in914434100ns. The [complete compiler record](dual_attempts/a01.json)
and [seal](dual_seal.json) preserve the exact source, runner, scope and output.
Compiler time was explicitly excluded from engaged research.

The six principal theorems prove weak dual bounds, their affine lower/upper
forms, Farkas exclusion, and attained lower/upper bounds from matching primal
points. Finite sums, arbitrary dimensions and weighted-row identities are
proved inside the unit. The coefficient domain is an arbitrary ordered
commutative ring under standard Lean classes, so this is not merely a check
of finitely many rational points. No new global axiom or omitted proof was
used. Printed dependencies are only propext, Classical.choice and Quot.sound.

Seven helper lemmas generated unused-section-variable warnings: their
algebraic statements do not need all the declared order instances. This is
a harmless over-assumption in the supplemental statements, not a failed
proof or a change to the candidate. The successful source is preserved as
compiled rather than edited and re-executed to suppress cosmetic warnings.

This formal result verifies the abstract mathematical inference from the
identities checked by the Python code. It does not formalize the code's
parser, iteration, input binding or construction of the intended rows, and
it does not establish that an LP producer always finds a certificate. It
does not prove strong duality, bit complexity, local interpolation or the
whole end-to-end range service. Those boundaries remain explicit.
