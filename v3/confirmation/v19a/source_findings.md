# Source interface: accepted formal reconstruction

Codex (GPT-6), October 28, 2026. Supplemental P3-11-A1 evidence.

The second retained [compiler attempt](source_attempts/a02.json) accepts
[Source.lean](Source.lean), with no omitted proofs or additional axioms.
Its execution took 1076138500ns, separately excluded from engaged research.
The deterministic first failure and its repair are in
[source_repairs.md](source_repairs.md); that failed attempt is not a pass.

The four new main statements prove (1) equivalence of the padded linear rows
and original affine receipt conditions; (2) equality of the shared source
with a union over receipt-witness assignments; (3) equality of its attained
minimum image with the union of local interval images; and (4) its anchored
rearrangement. They quantify over actual source vectors and permit different
block spaces. The first theorem connects the original lower/upper affine
inequalities with the LP sign convention. The remaining theorems treat a
local-image equivalence as an explicit premise; the sealed Local proof
establishes that premise when supplied with attained dual certificates.

The assignment proof uses an explicitly supplied block for receipt indices
outside the finite range. It neither imposes upper constraints on those
indices nor assumes the receipt minima have unique winners. The proof is
about attained minima; a finite nonempty block family satisfies this
interpretation. An infinite family with an unattained infimum would not.

The matrix has zero upper rows for inactive receipts. Python instead omits
those rows. Zero-row padding preserves feasibility but is not a formal proof
of Python's row-list implementation. The mathematical interval/certificate
integration, actual JSON/Fraction parsing, finite-mask implementation and
resource bounds have distinct obligations. No end-to-end runtime proof is
claimed. The accepted proof depends only on propext, Classical.choice and
Quot.sound; unused-instance and deprecated-simplifier warnings are retained.
