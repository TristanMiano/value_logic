# Finite receipt table: accepted integration

Codex (GPT-6), October 28, 2026. Supplemental P3-11-A1 evidence.

[Finite.lean](Finite.lean) passed the first captured compiler attempt,
exit 0 in 1333131800ns. Execution was excluded from engaged research.
The [record](finite_attempts/a01.json) and [seal](finite_seal.json) identify
the source, runner, prospective scope and embedded Integrated dependency.

The new final theorem, `finite_complete_certificate_image`, derives the
original affine source's exact attained-minimum image from a complete local
certificate table indexed by `Fin k -> Bool`. Its witness assignments have
type `Fin k -> I`. With `I = Fin n`, these are exactly the finite families
of 2^k masks and n^k witness assignments in the mathematical reconstruction;
the algorithm avoids enumerating the latter. No infinite mask-table premise
is needed. The extension to Nat row indices is false outside the k receipts.

The proof constructs receipt witnesses in both directions, handles k=0
without choosing a nonexistent receipt, derives all local interval images
from complete certificates, and applies the anchored rearrangement. The
arbitrary-block-space earlier theorem remains a useful general lemma, but
this finite statement is the closest formal statement to the fixed input.

The three new main lemmas use only propext, Classical.choice and Quot.sound.
The remaining non-mechanized interfaces are explicit: rational LP certificate
existence/production, Python parsing and arithmetic, the actual bitmask DP,
finite operation/storage counts, and scientific input validity. The finite
function cardinalities are elementary product counts in the written proof,
not separate cardinality theorems in this Lean file. No empirical novelty
or application claim follows from the successful compilation.
