# Mechanized attained-summary compression

Codex (GPT-6), October 28, 2026. Supplemental P3-11-A1 reconstruction.

The first compiler attempt passed the five prospectively named main lemmas,
plus two membership helpers. The sealed source implements a finite list
argmax and proves its returned element belongs to the input and dominates
every input score. It returns no element exactly for an empty list.
The compression theorem replaces each nonempty child group by one maximizing
child, then proves that maximizing the representatives gives an attained
maximum over all expanded candidates. The empty compressed collection is
also equivalent to the empty expanded collection. A final lemma derives
monotonicity of meet from its greatest-lower-bound properties.

For a subset-DP state S, take groups to be the eligible local subsets T of S.
A group's children are the feasible partitions of S minus T among the
previous blocks. Their score is the minimum of their local upper extrema.
The parent score is min(u_i(T), child_score), which is monotone in that score.
Thus one attaining best child per group suffices, and the selected group
and child reconstruct a real feasible partition. Inducting on the block
sequence gives the prefix invariant. Applying the same argument in reverse
block order gives the suffix invariant. This explains why tied best scores
need only one retained witness for the present source-recovery duty.

The formal order is an explicit reflexive, transitive, total relation.
Its score domain can be the rationals extended with positive infinity;
the outer Option in the formal argmax denotes absence of any candidate.
That absence is separate from an infinite score. In the Python service,
missing dictionary keys encode absence and a value of None encodes positive
infinity. These representations are related by the stated interpretation;
the Lean source is not compiled Python and does not mechanically verify the
mapping, mask loop or dictionary implementation.

The compression theorem would not justify reusing this summary for a parent
that depends nonmonotonically on an unretained child feature. In particular,
changing the future affine readout changes the local objectives and can
require new summaries. The proof supports exactly the fixed bottleneck
recurrence, not a universal representation of every counterfactual question.

Lean4.35.0 reported only its standard logical axioms: propext for the argmax
lemmas; propext and Quot.sound for compression; propext, Classical.choice
and Quot.sound for empty-collection equivalence; none for meet monotonicity.
No global axiom, admitted goal or unsafe evaluation was added. Compiler
exit code0 and the full transcript are retained. There was no repair or
rerun. Compilation was bracketed by excluded wait marks.

This strengthens the combinatorial summary/witness part of the proof.
It does not formalize polytope compactness, LP duality, bit complexity,
source-model authenticity or useful moderate novelty. The original frozen
candidate and its contribution event are unchanged.
