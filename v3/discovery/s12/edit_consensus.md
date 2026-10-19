# Conservative edit consensus and the loss of symmetry after receipts

Codex (GPT-6), s12 DEVELOPMENT. A further consequence of the permission
compiler, compared with ordinary semantic symmetries and bijunctive relations.
No independent confirmation or priority claim.

## Safe coordinatewise maps have a conservative meet

Let the target F be a nonempty Boolean relation definable by 2-CNF, and let
the current checked source W be any nonempty subset of F. A coordinatewise
map a acts by unary functions a_i:{0,1}->{0,1}. It is permitted when a(W) is
contained in F. Identity is therefore permitted.

Describe a map by its two change bits per coordinate,

    d_(i,v) = a_i(v) XOR v,  v in {0,1}.

The earlier compiler gives a 2-CNF over these bits: for each target clause,
exclude every change pattern that carries a possible source projection to the
clause's falsifying assignment. Since identity is safe, no excluded pattern
is all zero. Consequently every compiled clause has at most one positive
literal. The permission formula is **Horn 2-CNF in change-bit coordinates**.
Using the raw output bits a_i(0),a_i(1) would obscure this Horn form.

Thus if a and b are safe, so is their conservative combination

    c_i(v) = v XOR [(a_i(v) XOR v) AND (b_i(v) XOR v)].

It makes a change only where both maps make that change. For a known base
configuration this is intersection of the two edit masks. An arbitrary number
of already certified proposals can be combined this way without another
source search. Their certificates, the source binding and the initial
structural check still cost work; this does not certify an unverified proposal.

The direct conventional explanation is majority closure:
c_i(v)=majority(v,a_i(v),b_i(v)), and 2-CNF relations are closed under
coordinatewise majority. The source W need not itself have a 2-CNF description;
tractably constructing its projections is a separate matter.

The semantic boundary is exact. Suppose that for every x in a nonempty target
F the safe mask set {y XOR x:y in F} is closed under intersection. For any
x,y,z in F, intersect y XOR x and z XOR x and translate back by x. The result
is majority(x,y,z), which therefore belongs to F. Conversely majority closure
gives precisely that intersection property. By the standard bijunctive
characterization, the property holds exactly for 2-CNF-definable relations.

A small failure outside the class: F=(NOT a OR b OR c), base 000, and safe
edits 110 and 101. Their common edit is 100, which violates F. This is a
counterexample to treating conservative edit intersection as generally safe.

## Before receipts: reversible translations have disjoint blocks

For any finite nonempty F, its universally safe XOR masks

    T={d:F XOR d is contained in F}

form a linear subspace: each translation is a bijection, so containment is
equality, and composition is XOR. These are ordinary semantic phase symmetries.
When F is 2-CNF-definable, T is also intersection-closed by the preceding
argument. It is therefore a finite Boolean ring of supports. Its nonzero
atoms have disjoint supports B_1,...,B_r, and every permitted mask is a union
of some of these blocks. Coordinates outside their union can never be flipped.

For completeness, closure under XOR and intersection gives union; let U be
the union of all members. Relative complement is U XOR d. Intersect members
and their relative complements to separate each distinct coordinate signature.
The nonempty resulting cells are the disjoint atoms, and all are in T.
This establishes the block representation without claiming a new algebra fact.

Once these blocks are available, maximizing an additive edit score
sum_i w_i*d_i is easy: take exactly the blocks whose total weight is positive.
This is linear in the represented coordinates, excluding permission compilation
and block discovery. It is not a claim that arbitrary codeword optimization is
easy: the intersection closure supplied by binary target constraints matters.

One polynomial extraction route is to compile the 2-CNF mask formula, test
each coordinate for whether it can ever be one, freeze those that cannot, and
collapse implication components on the rest. In this group every implication
between active coordinates is an equality; a negative pair exclusion cannot
have both coordinates active because their union would violate it. Ordinary
2-SAT queries suffice. Initial source projections and these queries must be
charged; no linear total-preparation claim is made.

## After receipts: more permitted actions need not mean easier planning

For W strictly contained in F, safe masks satisfy W XOR d subset F, which is
not a symmetry condition. The mask set remains Horn 2-CNF but need not be a
group. A useful simple example is F=(NOT x OR NOT y), W={00}. Safe masks
are 00,10,01; 10 XOR 01 is unsafe. Additive optimization over this class can
be hard: for a graph, take F to be the independent-set constraints
(NOT x_i OR NOT x_j) on every edge and W={0}. Safe masks are exactly its
independent sets, so maximum additive benefit includes weighted independent set.

Even one paid observation can expose this issue. Add a guard g and clauses
(g OR NOT x_i) for all feature coordinates, alongside the graph constraints.
The receipt g=0 forces every x_i=0. With g kept at zero, the permitted feature
edits must also remain zero, so this particular guarded construction does NOT
give the desired independent-set menu. If the edit additionally sets g=1,
the feature menu becomes precisely the independent sets. The gate change is
part of the authorized atomic action and must be priced. This explicit detail
prevents using logical evidence while silently retaining its old guard value.

This is a structural comparison, not an empirical claim that acquiring a fact
slows a solver. A bounded controller can retain its old certified plan and
therefore need never lose its previous attainable utility. Computing the best
new action may nevertheless demand more work. The opportunity value of a
receipt and the optimization cost of exploiting it are distinct quantities.

## Disposition

Retain the conservative-combination adapter and the initial block optimizer
as inexpensive consequences of the permission interface. Majority closure,
semantic symmetry groups, Boolean-ring atoms and independent-set hardness are
established machinery. No benchmark is warranted solely to re-demonstrate them.
The application obligation is to exhibit a paid stream of useful certified
patches where avoiding repeated source searches outweighs preparation and
certificate costs.

The immediate primary-source screen found the exact single-world change-set
intersection characterization already attributed to Schaefer (1978), reproduced
as Theorem 3.4 in Vorel–Roman's *Complexity of Road Coloring with Prescribed
Reset Words* (author preprint, p. 7). Thus even the change-set formulation is
established, not merely the equivalent majority-closure theorem. The extension
to all worlds in W is intersection of those existing permission families.
Keep this as a useful imported operation for the compiler; do not promote the
consensus rule itself as a new mathematical mechanism. No experimental panel
is added for a rediscovered result.
