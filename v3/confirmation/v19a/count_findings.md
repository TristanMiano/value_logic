# Finite enumeration counts: accepted proof

Codex (GPT-6), October 28, 2026. Supplemental P3-11-A1 evidence.

[Count.lean](Count.lean) passed on retained attempt 3, exit 0 in 741074800ns.
Both earlier elaboration failures and the unchanged mathematical statements
are documented in [count_repairs.md](count_repairs.md). The
[accepted record](count_attempts/a03.json) and [seal](count_seal.json) preserve
all versions. Compiler execution earns no engaged research credit.

The unit proves a complete enumeration of length-k functions into a finite
alphabet, with list length equal to the alphabet size to power k. It gives
complete binary receipt masks in 2^k entries and block-witness assignments
in n^k entries. A three-symbol encoding enumerates all nested pairs (S,T)
with T subset S in 3^k entries, and every generated pair satisfies inclusion.
Thus the upper bound on one full recurrence-layer scan has a machine-checked
combinatorial enumeration witness. The displayed statements concern list
lengths and coverage, not a separate no-duplicates theorem.

This is elementary finite counting, not a new algorithmic result. It does
not verify the Python bitwise submask iteration, physical memory allocation,
LP solution costs, rational arithmetic costs, or practical speed. Those
remain covered by the written contract and implementation review at their
stated level. The nine printed statements use only propext and Quot.sound;
this unit adds no classical-choice or omitted-proof axiom.
