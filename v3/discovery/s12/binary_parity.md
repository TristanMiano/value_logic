# Parity inference from binary sources and ordered search

Codex (GPT-6), October 19, 2026. DEVELOPMENT derivation, not confirmation.
This connects the transcript representation to task-specific logical inference.

## Affine consequences of a bijunctive source

Let nonempty F be a binary-CNF relation and choose a in F. Put
D={x XOR a:x in F}; it contains zero. Closure of F under coordinatewise majority
implies d AND e is in D: it is majority(a,a XOR d,a XOR e) XOR a.
Consequently V=span over GF(2) of D is closed under AND, by bilinearity.

Every linear AND-closed Boolean space has a disjoint-block basis. To see this,
the OR of all its vectors is in V because u OR v = u XOR v XOR (u AND v).
Call that support indicator one. Partition its active coordinates by equality
of their evaluation maps on V. For each block, AND suitable separating vectors
or their relative complements one XOR v to obtain the block indicator.
The indicators are disjoint, belong to V, and span every vector in V.

Thus the affine hull a+V of F is defined entirely by fixed coordinates and
pairwise equality/inequality consequences of F. A parity with support S is
constant on F exactly when each variable block meets S an even number of times;
its value is then parity(a AND S). If this test fails, some generator in D has
odd parity, so two actual source worlds disagree. No point of the affine hull
is being mistaken for an actual model of F.

These blocks can be obtained with polynomially many ordinary 2-SAT assumption
tests: fixed coordinates and pair polarities suffice. This is not a model-
counting claim, and initial source preparation still costs work. Variation
blocks are not universal safe-edit blocks: x implies y has full affine hull,
while either individual toggle can violate that source. The same distinction
holds after cap-three invoices add clauses to the source.

## A source can reduce the price without an affine invariant

Take the source x_1 <= ... <= x_n. Its n+1 worlds correspond to an ordered
switch position, and it has full affine hull. The parity of all bits alternates
between adjacent positions. In a deterministic coordinate decision tree, each
remaining set of switch positions is an interval. Exact parity therefore
requires a singleton leaf, even though the output is only one bit.

Under cap two, unit private prices, exact invoices, free resets and at least
two available coordinates, each informative episode is an ordinary threshold
query with outgoing fees 1 and 2, whose orientation can be chosen. The earlier
cap-two dominance argument applies. A worst-bill budget B permits at most
L_0=L_1=1 and L_B=L_(B-1)+L_(B-2) leaves for B>=2. Conversely any number of
ordered leaves up to that bound can be split between children with the two
budgets. The exact bill is the least B with Fibonacci_(B+1)>=n+1, where
Fibonacci_1=Fibonacci_2=1. This is ordinary alphabetic search with unequal edge
costs, not a new Fibonacci search principle.

A balanced-position baseline chooses halves at every node and optimally
orients the expensive invoice. With g(1)=0, a=floor(k/2), b=ceil(k/2),

    g(k) = 1 + max(max(g(a),g(b)), 1+min(g(a),g(b))).

For 128 positions, the proposed exact bill is 11 versus balanced bill 14:
21.43% lower declared query fee. This number is prospective until the probe;
it excludes source compilation and controller work. An ordinary optimized
unequal-cost search is the identical strong control and must tie. Uniform
full-cube parity needs 2n under the same cap-two hard-bill contract; that
different-source comparison explains the value of source information but is
not a matched-information performance gain.

Prospective inexpensive screen: all binary-CNF sources through four variables,
all target parities, and an independent interval Bellman oracle through 128
positions. Stop and retain the first discrepancy. No large benchmark is needed
for the elementary adapter.

The first [probe](binary_parity_probe.json) passes all 68,090 parity comparisons
on 4,352 nonempty sources through four variables, plus 128 interval Bellman
comparisons, in 0.0579919 seconds. The 128-position values are indeed 11 and 14.
This is a constructed fee example, not measured application acceleration.

Prior comparison: Efraimidis, [(alpha,beta) Fibonacci Search](https://arxiv.org/pdf/1012.0259),
Sections 2–5, explicitly solves outcome-priced ordered search and derives its
leaf-capacity sequence. Our chain example is a direct instance after compiling
the invoice operation; the number 21.43% is not a new algorithmic discovery.
Henshall et al., [Binary Decision Diagrams for Affine Approximation](https://arxiv.org/pdf/0804.0066),
Section 2.2, gives the affine-envelope and translated-vector-space framework.
Nordh–Zanuttini, [Propositional Abduction is Almost Always Hard](https://www.ijcai.org/Proceedings/05/Papers/0524.pdf),
Section 2 and Proposition 5, supplies the width-two affine class context.
The local block proof specializes those established ideas; no priority claim
is based on failing to find the exact lemma in a quick search.
