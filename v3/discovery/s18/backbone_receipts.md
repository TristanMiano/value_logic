# Which correlations can a bounded reasoner safely discard?

Codex (GPT-6), s18 DEVELOPMENT. Consequence of the exact contact criteria,
not a claim that general logical abstraction or backbones are new.

For any nonempty report region T subset{0,1}^d, let box(T) be the subcube
fixing exactly those coordinates that are constant throughout T. It keeps
the positive and negative backbone literals and discards all correlations
among the remaining coordinates. Computing these literals from an arbitrary
CNF representation can itself be hard; they are not assumed free.

For an unknown meet-closed or majority-closed feasible F, reliable retained
actions B, and any hard fault budget r, replacing every T_i by box(T_i)
preserves the ENTIRE guaranteed feasible-action set exactly.

For meet closure, a target's test asks only whether T_i is contained in
D_j(z), a conjunction of specified positive coordinates and one specified
negative coordinate, or whether T_i={top}. These are conjunctions of unary
conditions. T_i is contained in such a region exactly when box(T_i) is.
For majority closure, every test asks whether the contact forces a particular
unary or binary pattern, again a conjunction of unary conditions. The same
equivalence applies, including its r+1 support count. This proves the claim
without asserting that T_i and box(T_i) have the same feasible witnesses.

Thus the subcube contact representation is without loss for this particular
safe-action duty in these two closure classes. This strengthens the meaning
of the polynomial input restriction. It does not justify assuming that a
fallible report is true, that the source has the required closure, or that
its backbone can be computed without paying for inference.

## Affine closure needs correlations

On three bits take contacts

    T1={000,011}, T2={000,101}, T3={000,110}, B=empty, r=0.

Every selector either contains000 or selects011,101,110. The XOR of those
three is000, an odd affine combination. Hence every compatible affine F
contains000. Replacing the contacts by their boxes fixes only one zero
coordinate per contact. Select100,010,001 from the appropriate boxes.
They all lie in the odd-parity affine plane, which excludes000. The
compressed evidence no longer guarantees that action.

## A safe-action summary need not preserve values

On two bits let T={01,10}, with no retained points or fault allowance, and
let h(x)=x1+x2. Any source hitting T has min_F h<=1; a singleton source
attains1 and is meet-closed as well as majority-closed. Thus1 is the sharp
worst compatible optimum. The box is the whole cube, which allows the
singleton source{11} with optimum2. Both information states have an empty
guaranteed feasible-action core. Their universally executable actions agree,
but their existential value conclusions differ.

For a reasoner expected to answer both action and value questions, discarding
these correlations is therefore not harmless. The information contract must
name the future duty. This is an explicit instance of the author's distinction
between unresolved mathematical truth, a useful value bound, and an action
that can actually be returned.

The next close comparison is characteristic-model reasoning and incomplete
constraint representations. The initial source search found the known Horn
framework again but no inspected theorem about this exact contact interface.
That is an unresolved comparison, not evidence of literature absence.

The subsequent[single-constraint derivation](single_constraint.md) explains
the preservation result more generally for conjunctive clausal source
classes. This strengthens the scope but also gives a simpler ordinary
version-space account, reducing the plausibility of a standalone novelty
claim based only on the Horn/majority formulas.
