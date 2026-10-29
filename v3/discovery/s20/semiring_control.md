# An ordinary inside-outside reconstruction of AR1

Codex (GPT-6), October 28, 2026. DEVELOPMENT. This is a strong comparison,
not a separate novelty claim or an independent confirmation.

## Established machinery

[Goodman (1999), section 4, Theorems 4 and 5](https://aclanthology.org/J99-4004.pdf)
defines outside values for commutative semirings and gives the reverse
recurrence on nonlooping derivations. The outside object removes one
subderivation and combines all possible surrounding derivations. This is
exactly the general kind of object needed by our outside caps. The reading
covered section 4's definitions and these proofs, plus section 5's storage
caution. The earlier abstract of Eisner (2016) led to this stronger source;
its probabilistic differentiation theorem alone would not justify a max/min
calculus at ties. [Pouly, Schneuwly and Kohlas (2011), section 2.2.1](https://marcpouly.ch/pdf/poulyschneuwlykohlas11.pdf)
explicitly lists the bottleneck algebra with max as addition and min as
multiplication. Neither this algebra nor generic outside computation is new.

## Our explicit specialization

Let a local leaf (i,T) carry its attainable compact scalar set A_iT, empty
when the slice is infeasible. Use set union as addition and

    A * B = {min(a,b): a in A, b in B}

as multiplication. The zero is the empty set and the identity is the
singleton {+infinity}. These operations form a commutative idempotent
semiring: associativity and distributivity follow pointwise from min and
Cartesian products. The subset-partition circuit chooses one leaf per
generator, with their assigned receipt subsets forming a partition of K.
Its set-valued evaluation is the exact future image. Product source domains
are what makes each multiplication semantically legitimate.

For nonempty compact A,B the elementary identity

    A * B = (A intersect (-infinity,max B])
            union (B intersect (-infinity,max A])

holds: every minimum is one operand, and the other need only be at least
it. Conversely, its maximum is an available witness for that inequality.
The map A -> max A (empty -> -infinity) takes union to max and * to min.
It therefore evaluates the same circuit in the ordinary bottleneck algebra.

For each local leaf, an outside computation in that algebra yields the
largest possible minimum of all other leaves in a full derivation containing
it. In the partition circuit this is C_i(K minus T). Every realized minimum
is attained at some leaf, so the complete circuit image is

    union_(i,T) (A_iT intersect (-infinity,C_i(K minus T)]).

With convex local slices and affine readouts, A_iT is the interval [ell,u],
and this is AR1. Prefix/suffix subset convolution is one explicit ordinary
implementation of the outside computation. Generic graph construction can
store O(n*3^k) dependency edges; the structured implementation avoids that
storage and keeps O(n*2^k) table entries. This is a resource accounting
distinction, not a new outside algorithm.

## Consequence for the contribution assessment

The algorithm can be derived from an established semiring framework plus
local affine interval images and the displayed scalar clipping identity.
This is stronger prior overlap than merely saying that 'dynamic programming
is known'. The proposed contribution must be judged as the precise
receipt-conditioned whole-range specialization, its explicit parameter and
output bounds, source reconstruction and checked contract. A claim to a new
general inference algebra, inside-outside mechanism or bottleneck primitive
would be false. Whether this specialization is moderately novel remains a
judgment requiring the application literature comparison; successful tests
cannot answer it.

The interval-weight bottleneck literature is an additional lead, not yet a
fully read comparator. The author PDF for Kasperski--Zielinski's
*Possibilistic Bottleneck Combinatorial Optimization Problems with Ill-known
Weights* was found through search, but direct retrieval timed out. Search
excerpts concern optimality/deviation under independent interval weights;
they do not establish the exact scope of every result in that paper.
