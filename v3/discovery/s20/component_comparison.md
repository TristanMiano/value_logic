# A recursive-antichain reading of the sharp component bound

Codex (GPT-6), October 28, 2026. Separate DEVELOPMENT comparison; this
does not change the fixed V19 claim or its confirmation probability.

The [component bound](multinomial_components.md) has a second elementary
proof that makes its debt to classical inequalities clearer. Consider all
partitions terminal under feasible moves to lower-index blocks. After
fixing a prefix (T_1,...,T_(i-1)), the possible next sets T_i are maximal
members of F_i on the remaining items: otherwise some item in a later
block could move into block i. Hence the distinct possible next sets form
an antichain. This is a conditional statement for each fixed prefix; it
does not assert a global antichain for all i-th coordinates.

Let W(P) be the sum of reciprocal multinomial coefficients over suffixes
after a fixed prefix P, using its remaining ground set. Induct on the
number of remaining blocks. For one block W<=1. For more blocks, factor

    1 / multinomial(m; |T|, sizes_of_suffix)
      = 1 / binomial(m,|T|) / multinomial(m-|T|; sizes_of_suffix).

The suffix sums are at most one by induction. The next-set antichain
satisfies the ordinary LYM inequality, so W(P)<=1. At the empty prefix
this is exactly the weighted bound already proved by disjoint first-fit
permutation fibers. Bounding each multinomial denominator by its balanced
maximum gives the component bound. This shows the counting step is a
short recursive use of established machinery, not a new extremal coefficient.

The theorem and proof on pages197--199 of
[Beck--Zaslavsky (2002)](https://people.math.binghamton.edu/zaslav/Tpapers/mhh.pdf)
use this same factorization and LYM induction under coordinatewise
chain-free hypotheses. Our terminal-prefix condition supplies the needed
conditional antichains. Their published theorem should not be quoted as
if arbitrary terminal families satisfy its stronger stated assumptions.

For example, on{a,b,c}, take maximal feasible sets

    F1: {a}, {c}; F2: {a,b}; F3: {c},

and close each family under taking subsets. Both({a},{b},{c}) and
({c},{a,b},empty) are lower-move terminal. Their second coordinates are
strictly nested. They are in the same graph component: move a from block1
to block2, then c from block3 to block1. The example concerns the family
of all terminals; it does not prove that no specially chosen component
representatives could satisfy a stronger theorem.

I also read the definitions and Theorems1.1--1.4 in
[Tian--Wu (2025)](https://www.researchgate.net/publication/392864879_Bollobas_set_pair_inequalities_for_compositions),
pages1--4. Their strong Bollobas condition requires a two-way crossing
between the same pair of block indices, and their Theorem1.2 credits
Tuza's earlier weighted inequality. That hypothesis is not automatic here:
with three unit-capacity blocks, the feasible terminal partitions
({a},{b},{c}) and({c},{a},{b}) differ by a three-cycle and have no such
two-way crossing. They are isolated components. Thus the strong-system
theorem cannot be imported directly for these representatives. The weaker
composition systems in that paper have other bounds; their later proofs
have not been reconstructed in this screen.

Disposition: keep the sharp graph/source-component result as a proposed
application of greedy normalization and recursive LYM, with a full direct
proof. Its useful delta is the bound for this inference source contract,
including a noisy full-dimensional sharpness construction. Do not promote
it as a new general set-system inequality or use the comparison's limited
search coverage to claim priority. No standalone readiness estimate is
assigned in this recurrence.
